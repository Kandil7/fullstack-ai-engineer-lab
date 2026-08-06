# Databases — 03: Redis Caching Patterns

## Topic Overview

Caching is why Redis exists. A cache stores the answer to an expensive question
(database query, LLM call, API fetch) next to the client, so repeat questions
never pay the full cost. The engineering content is not "use a cache" — it is
*which* pattern: cache-aside, write-through, write-back, each with different
consistency and failure properties.

This lecture builds the canonical patterns with the stand-in client, then adds
the production layer: TTL strategy, cache stampedes (thundering herd),
penetration (querying for things that do not exist), and hit-rate math so you can
tell whether a cache is paying for itself.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Implement cache-aside (lazy) reads and explain what happens on a miss
2. Explain write-through and why it keeps the cache warm at write cost
3. Compare cache-aside, write-through, and write-back on staleness and risk
4. Use a TTL strategy that bounds staleness without thrashing
5. Prevent a cache stampede with `SET NX`-based single-flight locking
6. Prevent cache penetration with negative-cache entries
7. Compute and interpret hit rate, and estimate the latency win
8. Decide when a cache hurts instead of helps

## Prerequisites

| Need | Where |
|---|---|
| SET/GET with NX and TTL | [01-introduction-lecture.md](01-introduction-lecture.md) |
| Redis data structures | [02-data-structures-lecture.md](02-data-structures-lecture.md) |
| Python functions and closures | `02-advanced-python/01-decorators.py` |

## 1. Cache-Aside (Lazy Loading)

The workhorse pattern. On a read: check the cache; on a hit, return; on a miss,
load from the source of truth, store in the cache with a TTL, return. The cache
is populated *on demand* — the first request pays the full cost, everyone after
pays microseconds.

```python
from redis_client import get_client

r = get_client()

def expensive_load(user_id: int) -> str:
    return f"profile-{user_id}"           # stand-in for a DB query

def get_profile(user_id: int) -> str:
    cached = r.get(f"profile:{user_id}")
    if cached is not None:
        return cached
    value = expensive_load(user_id)        # miss: pay the full cost once
    r.set(f"profile:{user_id}", value, ex=300)
    return value

print(get_profile(7))                      # miss, then cached
print(get_profile(7))                      # hit

# Output:
# profile-7
# profile-7
```

The failure mode is benign: if Redis is down, reads just hit the database — the
cache is *optional* on the read path.

## 2. Write-Through

Cache-aside leaves the cache stale until a read miss. Write-through updates the
cache **on every write**: write the source of truth, then write the cache. Reads
never see stale data (as long as no other writer bypasses the pattern), at the
cost of doing two writes per update.

```python
def save_profile(user_id: int, value: str) -> None:
    # source of truth (database) first
    db_write(user_id, value)               # stand-in: no-op
    # then the cache — never the other way around
    r.set(f"profile:{user_id}", value, ex=300)
```

Order matters: **DB first, cache second**. If the cache write fails, the cache is
stale but correctable (TTL heals it); if the DB write fails, the cache must not
claim success.

## 3. Write-Back (and Why It Is Rare)

Write-back updates only the cache and flushes to the database later (batch or on
eviction). It is the fastest write path and the most dangerous: a crash between
cache and DB loses acknowledged writes. Use it only when you can afford loss
(analytics counters) or have a durable log to replay.

```python
def save_metric(name: str, value: int) -> None:
    r.hincrby("metrics", name, value)      # acknowledged instantly
    # background job later: read hash, batch to the warehouse
```

## 4. The TTL Strategy

TTL is the staleness contract. Too short: miss rate rises, the DB eats load.
Too long: users see stale data. The standard play: a TTL around the data's
natural lifetime, plus explicit invalidation on write when the pattern allows it
(delete the key; the next read repopulates).

```python
def invalidate(user_id: int) -> None:
    r.delete(f"profile:{user_id}")         # next read does a fresh load
```

Sliding TTL (refresh on hit) keeps hot entries alive forever while cold entries
expire — but a *permanently* hot entry never refreshes its content; prefer
absolute TTL for content that changes.

## 5. Cache Stampede (Thundering Herd)

A stampede is what happens when a hot key expires and 10,000 requests all miss at
once: every one of them loads the source, and the database melts. The fix is
**single-flight**: only one request loads, the rest wait for it or get the stale
value.

```python
def get_profile_safe(user_id: int) -> str:
    cached = r.get(f"profile:{user_id}")
    if cached is not None:
        return cached
    # atomically claim the right to load
    if r.set(f"lock:profile:{user_id}", "loading", nx=True, ex=10):
        try:
            value = expensive_load(user_id)
            r.set(f"profile:{user_id}", value, ex=300)
            return value
        finally:
            r.delete(f"lock:profile:{user_id}")
    # lost the race: someone else is loading; wait briefly, then retry
    for _ in range(5):
        cached = r.get(f"profile:{user_id}")
        if cached is not None:
            return cached
        r.incr("spins")                    # stand-in for a short sleep
    return expensive_load(user_id)         # bounded fallback
```

The `NX` lock makes the claim atomic — without it, two "winners" can both load.

## 6. Cache Penetration (Negative Caching)

Penetration is the *other* stampede: queries for keys that do not exist (a deleted
user, a bad ID). Every request misses, because the cache correctly holds nothing,
and each one hits the DB. The fix is to cache the **negative answer** with a short
TTL.

```python
def get_user_or_none(user_id: int) -> str | None:
    cached = r.get(f"user:{user_id}")
    if cached == "NIL":                    # cached negative
        return None
    if cached is not None:
        return cached
    value = db_lookup(user_id)             # stand-in: None or value
    if value is None:
        r.set(f"user:{user_id}", "NIL", ex=60)   # short negative TTL
    else:
        r.set(f"user:{user_id}", value, ex=300)
    return value
```

## 7. Hit-Rate Math

A cache is only worth its memory if the hit rate is high enough. With hit rate h,
DB cost D, and cache cost C (much smaller), the average read cost is
`h*C + (1-h)*D`. The win becomes visible when h passes ~0.8, and the classic 80/20
rule (80% of reads hit 20% of keys) is why TTL + LRU eviction work so well
together.

```python
def avg_read_cost(h: float, db_cost: float, cache_cost: float) -> float:
    return h * cache_cost + (1 - h) * db_cost

for h in (0.0, 0.5, 0.9, 0.99):
    print(f"h={h:.2f}: avg cost = {avg_read_cost(h, 10.0, 0.1):.2f} ms")

# Output:
# h=0.00: avg cost = 10.00 ms
# h=0.50: avg cost = 5.05 ms
# h=0.90: avg cost = 1.09 ms
# h=0.99: avg cost = 0.20 ms
```

If your hit rate sits at 0.3, the cache is mostly overhead — fix the TTL or the
key design before buying more RAM.

## Common Mistakes to Avoid

### Mistake 1: Writing to the cache before the database
```
# WRONG — cache says success, DB write fails: permanent lie
r.set("user:1", value); db_write(1, value)

# CORRECT — DB first; cache is a projection of the DB
db_write(1, value); r.set("user:1", value, ex=300)
```

### Mistake 2: No TTL on cache entries
```
# WRONG — grows forever, eviction thrashes, stale data never heals
r.set("profile:1", profile)

# CORRECT — every entry expires
r.set("profile:1", profile, ex=300)
```

### Mistake 3: No single-flight on a hot key
```
# WRONG — 10k requests miss together and hammer the DB
if r.get("hot") is None:
    value = expensive()            # 10k times

# CORRECT — NX lock so exactly one loads
```

### Mistake 4: Not caching negative results
```
# WRONG — every bad-ID query hits the DB forever
if (v := r.get(k)) is None: return db_lookup(k)

# CORRECT — cache 'NIL' with a short TTL
```

### Mistake 5: Caching data that must be instantly consistent
```
# WRONG — a balance shown to a customer cannot be 60s stale
r.set("balance:7", balance, ex=60)

# CORRECT — authoritative reads skip the cache (or use write-through)
```

## Best Practices

1. Cache-aside by default; write-through when stale reads are unacceptable.
2. TTL on every entry; choose it from the data's real freshness need.
3. DB first, cache second — the cache is a projection, never the source.
4. Invalidate by delete, not by overwrite-with-old (avoids a stale window).
5. Single-flight hot keys; negative-cache missing keys.
6. Monitor hit rate; below ~0.8 the cache is not paying for itself.
7. Keep values small; a 1 MB cached blob evicts 100 useful small entries.
8. Use the same key convention everywhere so invalidation is easy to find.
9. Cache *derived* data (rendered HTML, reranked lists), not just raw rows.
10. Treat cache failure as "slow path", never as an error path.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Cache hit | O(1) read | O(1) | — |
| Cache miss + load | O(1) + DB cost | O(1) per entry | raise TTL to cut misses |
| Stampede (no single-flight) | O(N) concurrent loads | N buffers | `SET NX` lock — O(1) |
| Write-through | 2 writes | 1 extra entry | write-back (risky) |
| Invalidation | O(1) delete | — | — |

The dominant cost is memory: every cached entry competes for RAM that could hold
more entries or more hot keys. LRU eviction + TTL keeps the working set bounded,
but a cache holding 10x the DB's data is a bug, not a feature.

## AI Engineering Relevance

**Where this shows up:** LLM applications are latency- and cost-bound, which makes
them the biggest caching consumers in modern stacks.

| Concept here | Used for |
|---|---|
| Cache-aside + prompt hash key | identical LLM prompts answered from cache instead of the model |
| Single-flight | the exact same prompt arriving from 1,000 clients at once |
| Negative caching | caching "no answer for this query" to survive embedding misses |
| Write-through | refreshing a reranked candidate list after document updates |
| Hit-rate math | deciding whether an LLM cache pays for its memory |

**Scale note:** LLM caching is the strongest cache known: identical prompts share
prefixes, so a 90% hit rate on a popular assistant endpoint is routine — and the
"database" being saved is a paid model call costing milliseconds *and* money. The
same stampede math applies: a viral prompt expiring from cache will burn the
model budget in seconds without single-flight.

## Practice Exercises

### Exercise 1: Cache-aside wrapper (Difficulty: Easy)
Write `cached_get(r, key, load, ttl)` that returns cached or loads, stores with
TTL, and returns the value. Prove a second call returns without calling `load`.

### Exercise 2: Hit-rate monitor (Difficulty: Easy)
Instrument `cached_get` with `r.incr("stats:hits")` / `r.incr("stats:misses")`
and return the current hit rate.

### Exercise 3: Single-flight loader (Difficulty: Medium)
Implement `get_hot(r, load)` where concurrent callers produce exactly one `load`
call (count loads in a list to prove it).

### Exercise 4: Negative cache (Difficulty: Medium)
Implement `lookup(r, id, fetch)` that caches `None` results with a 60s TTL and
returns them without calling `fetch`.

### Exercise 5: Write-through invalidation (Difficulty: Medium)
Implement `save_user(r, id, value, db_write)` that writes the DB, then refreshes
the cache, then returns; verify the cache reflects the new value immediately.

## Summary

| Concept | Description |
|---|---|
| Cache-aside | lazy populate on miss; the default pattern |
| Write-through | DB + cache on every write; never stale, always two writes |
| Write-back | cache-only writes, flush later; fast, lossy |
| TTL | the staleness contract; too short thrashes, too long lies |
| Stampede | hot-key expiry -> herd; fixed by `SET NX` single-flight |
| Penetration | missing keys never cached; fixed by short negative TTLs |
| Hit rate | the number that tells you whether the cache earns its RAM |

Caching looks trivial and is not: the patterns differ in consistency and failure
behavior, and the two production killers — stampede and penetration — appear only
under real load. Every pattern here is a few commands (`GET`, `SET EX`, `SET NX`,
`DEL`) combined in a deliberate order.

## Quick Reference

| Task | Idiom |
|---|---|
| Cache read | `r.get(k)` then `r.set(k, v, ex=300)` on miss |
| Atomic claim | `r.set(k, v, nx=True, ex=10)` |
| Invalidate | `r.delete(k)` |
| Negative entry | `r.set(k, "NIL", ex=60)` |
| Hit counter | `r.incr("stats:hits")` |

## Next Steps

Next: **[Redis 04 — Rate Limiting](04-rate-limiting-lecture.md)** — fixed windows,
sliding windows, token buckets, and the counting primitives that make them safe.

Continues in: **[Phase 5 — Backend](../../06-phase-5-backend/01-fastapi-lecture.md)** —
cache middleware and API throttling in web frameworks.

Official docs: [redis.io/docs/latest/develop/use/patterns/](https://redis.io/docs/latest/develop/use/patterns/)
