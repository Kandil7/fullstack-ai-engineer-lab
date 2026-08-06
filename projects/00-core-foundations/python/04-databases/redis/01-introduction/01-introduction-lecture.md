# Databases — 01: Redis Introduction

## Topic Overview

Redis is an **in-memory, single-threaded key-value store** whose killer feature is
latency: most operations complete in microseconds because the dataset lives in RAM
and one process executes commands sequentially — no locks, no disk seeks. It is the
workhorse of production caching, session storage, rate limiting, queues, and
distributed coordination in every large web stack (Twitter, GitHub, Stack Overflow
all run it at massive scale).

Redis is not a "database of record": it trades durability and query richness for
speed. You do not put your source of truth in Redis; you put the *hot* subset of it
in Redis and accept that a restart may lose data (unless you enable persistence).

This whole series runs against a **dictionary-based stand-in** (`redis_client.py`)
that mirrors the real protocol commands 1:1, because the lab environment has no
Redis server. Everything you learn here — the command names, the semantics, the
failure modes — transfers directly to `redis-py`.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why Redis is fast (in-memory + single-threaded event loop) and what it gives up for that speed
2. Set and read keys with `SET`/`GET`, and use `SET ... NX/XX` for create-only / update-only writes
3. Read key metadata with `EXISTS`, `TTL`, `TYPE`, and delete with `DEL`
4. Explain the difference between an in-memory cache and a database of record
5. Use expiration (`EXPIRE`/`SET ... EX`) to bound memory growth
6. Choose between real Redis, a stand-in client, and other stores given an environment constraint
7. Explain what the single-threaded model implies for `KEYS` and blocking commands
8. Name the eviction policies and when each one applies

## Prerequisites

| Need | Where |
|---|---|
| Python dicts | `01-core-python/04-dictionaries.py` |
| Basic `while`/`if` control flow | `01-core-python/02-control-flow.py` |
| Time complexity notation | `06-dsa/01-big-o-lecture.md` |

## 1. What Redis Actually Is

Redis is a **data structure server**. Unlike a relational database, which stores
rows in tables and answers SQL, Redis stores *keys* (strings) mapped to *values* of
a small set of rich types: strings, hashes, lists, sets, sorted sets, streams, and
a few more. Commands are simple verbs: `SET`, `GET`, `LPUSH`, `SADD`, `ZADD`.

```python
from redis_client import get_client

r = get_client()          # dict-backed stand-in; identical API to redis-py
r.set("user:42:name", "sara")
print(r.get("user:42:name"))

# Output:
# sara
```

Every value lives in RAM, so `GET` is a dict lookup — O(1), microseconds. The
cost: memory is the capacity limit, and unless you configure persistence a restart
empties the store.

## 2. Why Single-Threaded Is a Feature

Redis executes commands **one at a time** on one thread. This sounds like a
bottleneck, but it is the source of its correctness and simplicity: there is never
a race between two clients mutating the same key, because commands are atomic by
construction. `INCR` is safe with 1,000 concurrent clients without transactions.

```python
r.set("hits", 0)
for _ in range(100):
    r.incr("hits")        # atomic read-modify-write — no lost updates
print(r.get("hits"))

# Output:
# 100
```

The single thread also means: **never run `KEYS` in production** (it scans every
key and blocks everything), and long-running commands (big `SORT`, huge `MGET`)
delay all other clients. That is why Redis has `SCAN` (incremental, non-blocking)
and why scripts must stay short.

## 3. Strings: The Foundation

Strings are byte arrays up to 512 MB. They are not just text: Redis numbers are
strings, and `INCR`/`DECR` do atomic integer arithmetic on them. Strings power
caches, counters, and every "blob" use case.

```python
r.set("count", 10)
r.incr("count")            # 11
r.incrby("count", 4)       # 15
print(r.get("count"), r.get("count").__class__.__name__)

# Output:
# 15 str
```

## 4. Expiration: TTL

Every key can carry a **time-to-live**. Expired keys vanish automatically; the
store never grows unboundedly. This is the difference between a cache (bounded by
TTL) and a database (bounded by disk).

```python
r.set("temp", "x", ex=5)
print(r.ttl("temp"))       # 5, 4, 3 ... counting down
r.expire("temp", 100)      # extend an existing key
print(r.ttl("temp"))

# Output:
# 5
# 100
```

Our stand-in uses a monotonic `ManualClock` so you can fast-forward time in tests.
Real Redis uses wall-clock time; the API is identical.

## 5. NX and XX: Create-Only and Update-Only

`SET key value NX` only writes if the key is **absent** (create-only, the basis of
locks). `SET key value XX` only writes if the key **exists** (update-only). Both
are atomic, which makes them safe against races:

```python
r.set("job", "a", nx=True)     # first writer wins
print(r.get("job"))
r.set("job", "b", nx=True)     # ignored — key exists
print(r.get("job"))

# Output:
# a
# a
```

## 6. Key Metadata: EXISTS, TYPE, TTL, DEL

Keys are cheap to inspect: `EXISTS` (O(1)), `TYPE` (what value type lives there),
`TTL` (remaining life, `-1` = forever, `-2` = gone), `DEL` (remove).

```python
r.set("meta", "v")
print(r.exists("meta"), r.type("meta"), r.ttl("meta"))
r.delete("meta")
print(r.exists("meta"))

# Output:
# 1 str -1
# 0
```

## 7. Namespacing Keys

There are no tables or databases-with-schemas in Redis — just flat keys. Teams
conventionally build namespaces with **colons**: `user:42:name`, `order:7:items`,
`cache:product:99`. The colon is not special to Redis; it is a human convention
that keeps keys sortable and greppable. `SCAN "user:*"` can then find a namespace.

## 8. The Stand-In Client and Why We Use It

`redis_client.py` implements the commands we need against plain dicts, with three
production features modeled honestly: expiration (via a `ManualClock`), `NX/XX`
semantics, and `maxmemory` eviction policies. Code written against it runs
unchanged against a real server if you set `REDIS_REAL=1`.

```python
r.set("k", 1, nx=True)
assert r.get("k") == "1"
```

This is the same pattern the whole series uses: **model the protocol, not a mock
of the tests** — so the learning transfers.

## 9. Eviction: When Memory Is Full

Real Redis lets you cap memory (`maxmemory`) and pick an **eviction policy**:

| Policy | Behavior |
|---|---|
| `noeviction` | writes fail with OOM error |
| `allkeys-lru` | evict least-recently-used key among ALL |
| `volatile-lru` | evict LRU among keys **with TTL** only |
| `allkeys-random` / `volatile-random` | random eviction |
| `volatile-ttl` | evict the key with the shortest remaining TTL |

The stand-in implements `allkeys-lru` and `volatile-lru` with an access-order
tracking, so exercises can *assert* eviction instead of guessing.

## 10. Redis vs the Alternatives

| Need | Redis | Postgres/MySQL | Memcached |
|---|---|---|---|
| Caching hot reads | ✅ microsecond | ❌ millisecond | ✅ (strings only) |
| Data structures (sets, sorted sets) | ✅ | ❌ | ❌ |
| Durability of source of truth | ⚠️ persistence is best-effort | ✅ ACID | ❌ |
| Rich queries / joins | ❌ | ✅ | ❌ |
| Streaming (pub/sub, streams) | ✅ | ❌ | ❌ |

Rule of thumb: **Redis for the hot path, Postgres for the truth.** If you need
both, use Redis as a write-through cache in front of Postgres.

## Common Mistakes to Avoid

### Mistake 1: Using Redis as a database of record
```
# WRONG — data vanishes on restart without persistence configured
r.set("orders", pickled_orders)          # 10 GB of truth in RAM

# CORRECT — Redis caches; Postgres stores
r.set("orders:today", pickled_orders, ex=3600)
```

### Mistake 2: Running `KEYS *` in production
```
# WRONG — scans the whole keyspace, blocks the single thread for seconds
r.keys("*")                     # O(N), freezes every other client

# CORRECT — incremental scan or an index key
r.scan(cursor=0, match="user:*")
```

### Mistake 3: Ignoring TTL on caches
```
# WRONG — cache grows forever, then eviction thrashes
r.set("page:1", html)

# CORRECT — every cache entry has a life
r.set("page:1", html, ex=300)
```

### Mistake 4: Expecting type safety on strings
```
# WRONG — incr on a non-integer string errors at runtime
r.set("v", "abc")
r.incr("v")                     # RedisError: value is not an integer

# CORRECT — treat strings as bytes; validate before arithmetic
```

## Best Practices

1. Always set a TTL on cache entries; a cache without TTL is a leak.
2. Use `NX` for create-only writes and `XX` for update-only writes — they are atomic.
3. Namespace keys with colons (`tenant:user:42:cart`) and document the scheme.
4. Never run `KEYS` in production; use `SCAN` with a cursor.
5. Keep values small: Redis performance degrades past ~1 MB values.
6. Use hashes instead of thousands of string keys for one object (`user:42` hash vs `user:42:name`, `user:42:email`).
7. Prefer `INCR` over read-modify-write in application code — atomicity is free.
8. Cap memory with `maxmemory` and choose the eviction policy deliberately.
9. Separate cache keyspace from durable keyspace (different prefixes, different TTLs).
10. Measure: a cache only helps if the hit rate is high and the TTL matches data staleness.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| `GET` / `SET` | O(1) | O(1) per key | — |
| `EXISTS` / `TYPE` / `TTL` | O(1) | O(1) | — |
| `DEL` | O(1) per key | frees value | batch `UNLINK` (lazy) for big values |
| `INCR` | O(1) | O(1) | — |
| `KEYS pattern` | O(N) over all keys | O(N) buffer | `SCAN` — O(1) per step |
| `EXPIRE` | O(1) | O(1) | fold into `SET ... EX` |

Memory is the real cost: every key + value lives in RAM. 1M keys of ~100 bytes is
~100+ MB before overhead; namespaces and long keys make it worse.

## AI Engineering Relevance

**Where this shows up:** every LLM application runs on a Redis-shaped cache —
prompt/response caching, rate limiting for model APIs, session state for chat
UIs, and job queues for embedding batch jobs.

| Concept here | Used for |
|---|---|
| `SET ... EX` | caching LLM responses keyed by prompt hash — 90% of repeated prompt traffic never hits the model |
| `INCR` + TTL | token-bucket rate limiting on an LLM gateway |
| `ZADD`/`ZRANGE` | ranking candidates by relevance score in a reranker |
| Hashes | storing one embedding job's status per key, all fields atomic |

**Scale note:** a single Redis instance handles ~100k ops/sec; when the prompt
cache outgrows RAM, you shard by key hash or move hot tenants to a dedicated
instance. The single-threaded model means one slow `KEYS` call stalls every LLM
request sharing that instance — cache-key hygiene is a production requirement.

## Practice Exercises

### Exercise 1: Counter with TTL (Difficulty: Easy)
Set key `visits` to `0` with a 60-second TTL, `INCR` it three times, and return
`(value, ttl_remaining > 0)`.

### Exercise 2: First-writer-wins (Difficulty: Easy)
Implement `claim(key, owner)` that atomically sets `key = owner` only if absent and
returns whether this caller won.

### Exercise 3: Key health report (Difficulty: Medium)
Write `health(r, keys)` returning a dict `{key: (exists, type, ttl)}` for a list of
keys — no exceptions on missing keys.

### Exercise 4: Cache with refresh (Difficulty: Medium)
Implement `cached(r, key, compute, ttl)` that returns the cached value or computes,
stores with TTL, and *extends* the TTL on hit (a sliding-window cache).

### Exercise 5: Namespace inventory (Difficulty: Medium)
Given a flat store, return `{namespace: count}` for all keys of the form
`ns:rest`, using `scan` — never `KEYS`.

## Summary

| Concept | Description |
|---|---|
| In-memory, single-threaded | microsecond ops, atomic commands, no locks |
| Strings | byte values up to 512 MB; numbers are strings with atomic `INCR` |
| TTL | `EXPIRE`/`SET EX` bound cache lifetime — the cache/database difference |
| NX / XX | atomic create-only / update-only writes |
| Namespaces | colon convention replaces tables |
| Eviction | `maxmemory` policies: LRU, random, TTL-based, or noeviction |

Redis is the fastest tool in the stack because it refuses to be general: no joins,
no disk, one thread, rich-but-fixed data types. The exercises in this series build
the patterns — caching, rate limiting, locks, queues, pub/sub — that turn a "fast
dict" into a production infrastructure layer.

## Quick Reference

| Task | Idiom |
|---|---|
| Set with TTL | `r.set(k, v, ex=300)` |
| Set only if absent | `r.set(k, v, nx=True)` |
| Atomic increment | `r.incr(k)` |
| Check TTL | `r.ttl(k)` (`-1` forever, `-2` gone) |
| Delete | `r.delete(k)` |
| Scan without blocking | `r.scan(cursor=0, match="user:*")` |

## Next Steps

Next: **[Redis 02 — Data Structures](02-data-structures-lecture.md)** — strings,
hashes, lists, sets, sorted sets, and which one to reach for.

Continues in: **[Phase 5 — Backend](../phase-5-backend/01-fastapi-lecture.md)** —
caching, sessions, and queues are where Redis meets web frameworks.

Official docs: [redis.io/docs](https://redis.io/docs), [redis-py](https://redis-py.readthedocs.io/)
