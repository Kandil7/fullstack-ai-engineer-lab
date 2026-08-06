# Redis — Glossary 03

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Cache | Pattern | store of expensive answers near the client |
| Cache-aside | Pattern | lazy: read cache, load on miss, store with TTL |
| Cache penetration | Failure | queries for missing keys never hit the cache |
| Cache stampede | Failure | hot key expires and every request misses at once |
| Delete invalidation | Pattern | removing a key on write so the next read reloads |
| Hit rate | Metric | fraction of reads answered from cache |
| Jitter | Pattern | random wait that de-synchronizes stampede retries |
| LRU | Eviction | evict the least-recently-used entry first |
| Negative caching | Pattern | caching the "does not exist" answer briefly |
| Refresh-ahead | Pattern | reloading a hot key just before it expires |
| SET NX lock | Primitive | atomic claim that only one caller wins |
| Single-flight | Pattern | only one request loads; others wait or retry |
| TTL | Key | expiry that bounds staleness and heals crashes |
| Write-back | Pattern | write cache only, flush to DB later (lossy) |
| Write-through | Pattern | write DB and cache on every write |

## Detailed Definitions

### Cache
**Definition**: A store of computed answers (DB rows, LLM responses) placed
where repeated questions avoid recomputation.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.set("profile:7", "expensive-result", ex=300)
print(r.get("profile:7"))  # -> expensive-result
```
```text
# second caller never pays the original cost
```
**Complexity**: O(1) read; memory O(entries).
**Related**: Cache-aside, TTL, Hit rate

### Cache-aside
**Definition**: The default caching pattern: check cache, return on hit, load
from source on miss, store with TTL.
**Example**:
```python
def get_profile(user_id):
    cached = r.get(f"profile:{user_id}")
    if cached is not None:
        return cached              # hit
    value = expensive_load(user_id)  # miss
    r.set(f"profile:{user_id}", value, ex=300)
    return value
```
```text
# cache is optional on the read path: a Redis outage just slows reads
```
**Complexity**: O(1) cache read; miss costs the load.
**Related**: Cache, Write-through, TTL

### Cache penetration
**Definition**: The failure where queries for keys that do not exist all
miss, because the cache correctly holds nothing — every one hits the DB.
**Example**:
```python
# bad IDs deleted users: cache never has them, DB takes every query
# fix: cache "NIL" with a short TTL
r.set(f"user:{user_id}", "NIL", ex=60)
```
```text
# the DB can be melted by requests for nothing
```
**Complexity**: without fix O(1) DB load per bad query.
**Related**: Negative caching, Cache-aside

### Cache stampede
**Definition**: The failure where a hot key expires and N concurrent requests
all miss and all load — the "thundering herd".
**Example**:
```python
# WRONG: 10k requests see a miss and each calls the source
if r.get("hot") is None:
    value = expensive_load()  # 10k times

# CORRECT: NX lock so exactly one loads
```
```text
# single-flight turns N loads into 1
```
**Complexity**: without fix O(N) concurrent loads.
**Related**: Single-flight, SET NX lock

### Delete invalidation
**Definition**: Removing a cache key on write so the next read performs a
fresh load — simpler than updating the cache in place.
**Example**:
```python
def invalidate(user_id):
    r.delete(f"profile:{user_id}")  # next read repopulates
```
```text
# delete, don't overwrite-with-old: avoids a stale window
```
**Complexity**: O(1).
**Related**: Cache-aside, Write-through

### Hit rate
**Definition**: The fraction of reads served from cache; the number that
tells you whether the cache earns its memory.
**Example**:
```python
def avg_read_cost(h, db_cost, cache_cost):
    return h * cache_cost + (1 - h) * db_cost

print(avg_read_cost(0.9, 10.0, 0.1))  # -> 1.09 ms
```
```text
# below ~0.8 the cache is mostly overhead
```
**Complexity**: n/a — a metric, updated per read.
**Related**: Cache, LRU

### Jitter
**Definition**: A random delay added to retries so multiple callers do not
re-attempt the same miss in lockstep.
**Example**:
```python
import random

def retry_delay(attempt):
    base = 2 ** attempt            # exponential backoff
    return base + random.uniform(0, 1)  # + jitter de-synchronizes
```
```text
# synchronized retries create synchronized stampedes
```
**Complexity**: O(1).
**Related**: Cache stampede, Single-flight

### LRU
**Definition**: Least-recently-used eviction: when memory is full, the
coldest entry dies first — the classic cache policy.
**Example**:
```python
# conceptual: maxmemory-policy allkeys-lru in redis.conf
# hot keys survive; the key untouched for longest is evicted
```
```text
# matches the 80/20 rule: 80% of reads hit 20% of keys
```
**Complexity**: O(1) tracked per access.
**Related**: Cache, Hit rate

### Negative caching
**Definition**: Caching the absence of a result with a short TTL so repeated
misses do not hammer the source.
**Example**:
```python
if value is None:
    r.set(f"user:{user_id}", "NIL", ex=60)  # negative answer
else:
    r.set(f"user:{user_id}", value, ex=300)
```
```text
# short TTL: the absence is not permanent
```
**Complexity**: O(1) per entry.
**Related**: Cache penetration, TTL

### Refresh-ahead
**Definition**: Reloading a hot key just before its TTL expires, so the
expiry never creates a miss at all.
**Example**:
```python
# background task: at TTL - 60s, re-run the expensive load
# and set a fresh TTL — readers never see the gap
```
```text
# the proactive alternative to single-flight; costs a watchdog job
```
**Complexity**: one background load per refresh window.
**Related**: TTL, Cache stampede, Jitter

### SET NX lock
**Definition**: Using `SET key value NX PX` as an atomic claim: exactly one
caller succeeds, and the claim self-expires.
**Example**:
```python
from redis_client import RedisClient, ManualClock

r = RedisClient(clock=ManualClock(0.0))
print(r.set("lock:hot", "w1", nx=True, ex=10))  # -> True
print(r.set("lock:hot", "w2", nx=True, ex=10))  # -> False
```
```text
# the single-flight primitive; see the distributed locks lecture
```
**Complexity**: O(1).
**Related**: Single-flight, Cache stampede

### Single-flight
**Definition**: The pattern where only one concurrent request performs the
load; the rest wait briefly or get the stale value.
**Example**:
```python
if r.set(f"lock:profile:{uid}", "loading", nx=True, ex=10):
    value = expensive_load(uid)
    r.set(f"profile:{uid}", value, ex=300)
    r.delete(f"lock:profile:{uid}")
# losers: retry the cache for a bounded number of spins
```
```text
# one load for 10k requests; the DB survives
```
**Complexity**: O(1) lock + bounded retry.
**Related**: Cache stampede, SET NX lock

### TTL
**Definition**: The expiry on every cache entry — the staleness contract and
the crash-healing mechanism in one.
**Example**:
```python
r.set("profile:1", value, ex=300)  # 300s of freshness
```
```text
# too short: misses rise; too long: stale reads
```
**Complexity**: O(1).
**Related**: Cache-aside, Negative caching

### Write-back
**Definition**: The pattern where writes go only to the cache and are flushed
to the database later — fastest, and lossy on crash.
**Example**:
```python
r.hincrby("metrics", name, 1)  # acknowledged instantly
# background flush later: read hash -> batch to the warehouse
```
```text
# use only when loss is affordable (counters, analytics)
```
**Complexity**: O(1) write; flush cost batched.
**Related**: Write-through, Cache-aside

### Write-through
**Definition**: The pattern where every write updates the database AND the
cache, so reads never see stale data.
**Example**:
```python
db_write(user_id, value)              # source of truth first
r.set(f"profile:{user_id}", value, ex=300)  # then the cache
```
```text
# DB first, cache second: the cache is a projection of the DB
```
**Complexity**: two writes per update.
**Related**: Cache-aside, Delete invalidation

## Key Concepts Summary

### Patterns
- Cache-aside is the default; write-through for never-stale reads
- Write-back is the fast-and-lossy exception — only for dispensable data
- Invalidation by delete; DB first, cache second

### Failures
- Stampede: hot key expires, herd misses -> single-flight with SET NX
- Penetration: missing keys never cache -> negative caching with short TTL
- Both appear only under real load — design for them before launch
- Jitter de-synchronizes retries; refresh-ahead pre-warms expiring keys

### Metrics
- Hit rate decides whether the cache pays for its RAM (target ~0.8+)
- LRU + TTL keep the working set bounded; stale data heals by expiry

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Cache-aside — ___
2. Write-through — ___
3. Stampede — ___
4. Negative caching — ___
5. Single-flight — ___
6. Hit rate — ___
7. Delete invalidation — ___
8. Write-back — ___
9. Jitter — ___
10. Refresh-ahead — ___

a) DB and cache updated on every write
b) Load on miss, store with TTL
c) Herd of misses when a hot key expires
d) Caching "does not exist" briefly
e) One loader for N concurrent requests
f) Fraction of reads served from cache
g) Remove key on write, reload on next read
h) Cache-only writes, flushed later
i) Random wait that de-synchronizes retries
j) Reload before expiry, so no miss happens

**Answers:** 1-b, 2-a, 3-c, 4-d, 5-e, 6-f, 7-g, 8-h, 9-i, 10-j
