# Databases — 02: Redis Data Structures

## Topic Overview

Redis is a data structure server: the value stored under a key is not a blob but a
**typed structure** with its own commands and complexity guarantees. The five core
types are strings, hashes, lists, sets, and sorted sets. Choosing the right type
is the single highest-leverage design decision in a Redis system: it decides
whether a feature is O(1) or O(N), whether it needs application-side coordination,
and how much memory it burns.

This lecture maps each type to the production problems it solves — hashes for
objects, lists for queues, sets for membership, sorted sets for leaderboards and
rankings — and builds the mental model of *which command family to reach for*.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Set and read hash fields with `HSET`/`HGET`/`HGETALL` and update a single field atomically
2. Use lists as FIFO queues with `LPUSH`/`RPOP` and explain why they are O(1)
3. Use sets for membership and deduplication with `SADD`/`SISMEMBER`/`SMEMBERS` and the O(1) cost
4. Use sorted sets for rankings with `ZADD`/`ZRANGE`/`ZRANK` and explain the skip-list cost model
5. Choose the correct type for a given problem by matching access patterns
6. Read back each type's data with the correct Python-facing shapes
7. Explain when a hash beats twenty string keys
8. Combine types to model real objects (user profiles, carts, leaderboards)

## Prerequisites

| Need | Where |
|---|---|
| Redis keys, SET/GET, TTL | [01-introduction-lecture.md](01-introduction-lecture.md) |
| Python dict and list operations | `01-core-python/04-dictionaries.py` |
| Big-O thinking | `06-dsa/01-big-o-lecture.md` |

## 1. Strings — Already Known, One Reminder

Strings are the atom everything else is built from: a string value, up to 512 MB,
with O(1) `GET`/`SET` and atomic counters. When a feature needs *one* scalar per
key (a counter, a flag, a cached blob), strings are correct — not a fallback.

```python
from redis_client import get_client

r = get_client()
r.set("feature:dark-mode", "on")
print(r.get("feature:dark-mode"), r.type("feature:dark-mode"))

# Output:
# on string
```

## 2. Hashes — One Object, Many Fields

A hash stores **fields → values** under one key: `HSET user:42 name sara email sara@x.com`.
Every field operation is O(1), and `HINCRBY` atomically increments one field. This
is the canonical model for an object: one key per entity, fields as attributes.

```python
r.hset("user:42", "name", "sara")
r.hset("user:42", "email", "sara@x.com")
r.hincrby("user:42", "login_count", 1)
print(r.hgetall("user:42"))
print(r.hget("user:42", "name"))

# Output:
# {'name': 'sara', 'email': 'sara@x.com', 'login_count': '1'}
# sara
```

Twenty string keys (`user:42:name`, `user:42:email`, ...) would do the same job —
but a hash keeps one object in one place, so `DEL user:42` removes it as a unit,
`HGETALL` loads it in one round trip, and memory overhead is amortized.

## 3. Lists — Queues and Stacks

Lists are ordered sequences of strings. `LPUSH`/`RPUSH` push on either end,
`LPOP`/`RPOP` pop — all O(1). A list with `LPUSH` + `RPOP` (or the reverse) is a
**FIFO queue**; with same-side push/pop it is a stack. Lists are the raw material
of worker queues: producers `LPUSH` jobs, consumers `RPOP` them.

```python
r.lpush("queue:jobs", "job-1", "job-2")   # -> ['job-2', 'job-1']
print(r.rpop("queue:jobs"))               # FIFO: oldest first
print(r.rpop("queue:jobs"))
print(r.rpop("queue:jobs"))               # empty -> None

# Output:
# job-1
# job-2
# None
```

The O(1) ends are the point: growing a list by 1M jobs costs constant work per
job, and `LLEN` tells a worker instantly how deep the backlog is.

## 4. Sets — Membership and Deduplication

Sets are **unordered collections of unique strings**. `SADD` adds (ignoring
duplicates), `SISMEMBER` asks "is it in there?" in O(1), `SMEMBERS` lists all, and
`SREM` removes. Sets solve membership ("is this user allowed?", "has this ID been
seen?") and deduplication (a crawler's seen-URL set) with constant-time answers.

```python
r.sadd("tags:ml", "vector", "retrieval", "vector")   # 'vector' added once
print(r.smembers("tags:ml"))
print(r.sismember("tags:ml", "vector"), r.sismember("tags:ml", "sql"))

# Output:
# {'vector', 'retrieval'}
# True False
```

`SCARD` (size), `SINTER` (intersection: "users who liked X *and* Y"), `SUNION`,
and `SDIFF` turn sets into a small set-algebra engine.

## 5. Sorted Sets — Rankings and Ranges

Sorted sets are sets whose members carry a **score** (a float), kept ordered by
score via a skip list. `ZADD` inserts or updates (O(log n)), `ZRANGE` returns the
lowest-scored slice, `ZREVRANGE` the highest, `ZRANK` gives a member's position,
`ZINCRBY` adjusts a score atomically. This is the type for leaderboards, priority
queues, and any "top-N by score" query.

```python
r.zadd("leaderboard", {"alice": 100, "bob": 250, "carol": 150})
print(r.zrevrange("leaderboard", 0, 1, withscores=True))   # top 2
r.zincrby("leaderboard", 200, "alice")
print(r.zrank("leaderboard", "alice"))                     # 0 = first now

# Output:
# [('bob', 250.0), ('carol', 150.0)]
# 0
```

## 6. The Type Selection Table

| Need | Type | Commands | Cost |
|---|---|---|---|
| scalar / counter / blob | string | `GET`/`SET`/`INCR` | O(1) |
| one object, many fields | hash | `HGET`/`HSET`/`HINCRBY` | O(1) per field |
| FIFO queue / stack | list | `LPUSH`/`RPOP` | O(1) ends |
| membership / uniqueness | set | `SADD`/`SISMEMBER` | O(1) |
| ranking / range by score | sorted set | `ZADD`/`ZRANGE`/`ZRANK` | O(log n) |
| append-only event log | stream | `XADD`/`XREAD` | O(log n) |

If your access pattern is "give me the top 10", sorted set. If it is "is this in
the list?", set. If it is "process in order", list. If it is "show me the user",
hash. Reach for the type that matches the *question*, not the one you already
know.

## 7. Composing Types — The Profile Problem

Real objects rarely fit one type. A user profile is a hash (`user:42`), their
followers are a set (`followers:42`), their activity feed is a list
(`feed:42`), and their leaderboard position lives in a global sorted set. The
same entity is *projected* into several structures, each tuned to one query.

```python
r.hset("user:42", "name", "sara")
r.sadd("followers:42", "1", "2", "3")
r.lpush("feed:42", "post-9", "post-8")
print(r.hget("user:42", "name"), r.scard("followers:42"), r.llen("feed:42"))

# Output:
# sara 3 2
```

This denormalization is normal in Redis: you pay write-time fan-out so reads are
single O(1) calls. The cost is consistency — you, not the database, must keep the
projections in sync (see the transactions lecture).

## Common Mistakes to Avoid

### Mistake 1: Storing objects as JSON in a string
```
# WRONG — every field update rewrites the whole blob; no partial GET
r.set("user:42", json.dumps(user))

# CORRECT — a hash makes fields first-class and atomic
r.hset("user:42", "name", "sara")
```

### Mistake 2: Using a list where membership is the question
```
# WRONG — SISMEMBER on a list is O(N) and duplicates pile up
r.lpush("allowed", "a")                      # then .count() each check

# CORRECT — sets exist for exactly this
r.sadd("allowed", "a")
```

### Mistake 3: Using a set where order or ranking is needed
```
# WRONG — sets are unordered; 'top 10' needs a sort you do not have
r.sadd("scores", "bob:250", "alice:100")

# CORRECT — sorted set keeps the order server-side
r.zadd("scores", {"bob": 250, "alice": 100})
```

### Mistake 4: Polling an empty queue with RPOP
```
# WRONG — busy loop burns CPU and server time
while (job := r.rpop("queue:jobs")) is None:
    pass

# CORRECT — blocking pop or a backoff
job = r.rpop("queue:jobs", timeout=5)        # stand-in: bounded wait
```

### Mistake 5: Forgetting that ZRANGE is ascending by default
```
# WRONG — the 'top' is actually the bottom
r.zrange("leaderboard", 0, 4)                # lowest scores first

# CORRECT — ZREVRANGE for descending
r.zrevrange("leaderboard", 0, 4)
```

## Best Practices

1. One entity, one hash key — never spread an object across string keys.
2. Pick the type by the *query*, not by convenience: membership → set, rank → sorted set, order → list.
3. Use `HSET` multi-field to set a whole object in one round trip.
4. Read `HGETALL` once and cache the dict client-side instead of N `HGET`s.
5. Keep list values small; a list is not a message bus for large payloads.
6. Use `ZINCRBY` for score updates instead of read-modify-write.
7. Bound lists when they can grow forever (`LTRIM` keeps the newest N).
8. Know the shapes: sets come back as Python `set`, hashes as `dict`, sorted-set ranges as lists of (member, score).
9. Fan-out projections at write time; never compute a feed on read.
10. Document the type-per-key in the codebase — `user:42` hash vs `followers:42` set must be obvious.

## Complexity and Cost

| Operation | Time | Space |
|---|---|---|
| `HSET`/`HGET`/`HINCRBY` | O(1) per field | O(fields) |
| `LPUSH`/`RPOP`/`LLEN` | O(1) | O(n) |
| `SADD`/`SISMEMBER`/`SCARD` | O(1) | O(members) |
| `SMEMBERS` | O(n) — returns everything | O(n) buffer |
| `ZADD`/`ZRANK`/`ZINCRBY` | O(log n) | O(n) skip list |
| `ZRANGE` | O(log n + k) | O(k) buffer |
| `LTRIM` | O(n) in worst case | frees trimmed tail |

Memory notes: hashes and zsets use ~2x the raw data in pointers/headers;
long member names in sets are stored twice. 1M-member zsets are a few tens of MB —
fine — but 1M *distinct* string keys each with 1 KB values will eat a GB.

## AI Engineering Relevance

**Where this shows up:** ranking pipelines, feature stores, and agent memory all
map onto these five types directly.

| Concept here | Used for |
|---|---|
| Sorted sets | storing reranker scores for candidate documents; `ZREVRANGE 0 19` = the top-20 context |
| Sets | deduplicating seen chunks/URLs in an ingestion pipeline |
| Hashes | one hash per document: text, embedding id, source, checksum |
| Lists | FIFO queues of embedding batch jobs |
| Strings + TTL | cached LLM responses and token-bucket counters |

**Scale note:** a leaderboard with 10M members still answers "top 100" in
microseconds with a sorted set — but a `ZRANGE` over a huge range returns big
payloads. Cache the top-k and update it with `ZINCRBY`+re-read instead of pushing
the whole ranking to every client.

## Practice Exercises

### Exercise 1: Object modeling (Difficulty: Easy)
Store a product (id, name, price, stock) as a hash and `HINCRBY` the stock by -1
when an order happens. Return the new stock.

### Exercise 2: FIFO worker queue (Difficulty: Easy)
Implement `produce(r, job)` and `consume(r)` using `LPUSH`/`RPOP`, and verify
FIFO order with three jobs.

### Exercise 3: Dedup filter (Difficulty: Medium)
Write `seen(r, item)` that returns True only the first time an item is seen
(use a set; O(1) per call, no duplicates stored twice).

### Exercise 4: Leaderboard top-3 (Difficulty: Medium)
Given `{"alice": 10, "bob": 30, "carol": 20, "dave": 25}`, store in a sorted set
and return the top-3 names with their scores in descending order.

### Exercise 5: Followers with intersection (Difficulty: Hard)
Maintain `followers:A` and `followers:B` sets; return the users who follow both
(`SINTER`), the total unique followers (`SUNION` + `SCARD`), and users A follows
but B does not (`SDIFF`).

## Summary

| Concept | Description |
|---|---|
| String | scalar, counter, blob — the atom |
| Hash | object with O(1) field access and atomic field increments |
| List | FIFO queue / stack via O(1) end operations |
| Set | O(1) membership, deduplication, set algebra |
| Sorted set | O(log n) ranking, top-N, score updates |
| Projection | the same entity fanned out into several types, one per query |

The five types are a small toolbox with enormous coverage: every common web
backend pattern — sessions, carts, feeds, leaderboards, queues, filters — is a
composition of them. Choosing the type first, and designing the key namespace
second, makes the rest of the series (caching, rate limiting, locks) nearly
mechanical.

## Quick Reference

| Task | Idiom |
|---|---|
| Set object field | `r.hset("user:42", "name", "sara")` |
| Increment field | `r.hincrby("user:42", "count", 1)` |
| Push / pop queue | `r.lpush("q", job)` / `r.rpop("q")` |
| Add unique | `r.sadd("seen", item)` |
| Membership | `r.sismember("seen", item)` |
| Top-3 by score | `r.zrevrange("lb", 0, 2, withscores=True)` |

## Next Steps

Next: **[Redis 03 — Caching Patterns](03-caching-patterns-lecture.md)** — cache
aside, write-through, stampede protection, and hit-rate math.

Continues in: **[Phase 5 — Backend](../../06-phase-5-backend/01-fastapi-lecture.md)** —
where sessions and caches meet the web layer.

Official docs: [redis.io/docs/data-types](https://redis.io/docs/data-types/)
