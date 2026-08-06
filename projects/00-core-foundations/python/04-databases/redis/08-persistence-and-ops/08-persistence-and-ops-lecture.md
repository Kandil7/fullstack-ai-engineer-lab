# Databases — 08: Redis Persistence and Operations

## Topic Overview

Redis holds your cache, your queue, and your rate-limit state. Two one-line
configs decide most of its production behavior: **persistence** decides what
survives a restart, and **eviction policy** decides what dies when memory runs
out. Both have very different failure modes, and both are easier to reason
about before an incident than during one.

This lecture covers the two persistence philosophies (RDB snapshots vs. the AOF
append-only log), the eviction policies and who they kill, memory reporting as
capacity planning, `SCAN` instead of `KEYS` as the operational discipline, and
the cluster basics that scale Redis past one node.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain RDB snapshots and compute what a crash loses (RPO = interval)
2. Explain AOF and the fsync policy tradeoff (durability vs. write cost)
3. Choose RDB, AOF, or both for a given dataset
4. Describe `noeviction`, `allkeys-lru`, `volatile-ttl` and their victims
5. Pick an eviction policy for caches, queues, and rate-limit keys
6. Report and size memory usage per key and per dataset
7. Use `SCAN` with a cursor instead of blocking `KEYS`
8. Explain hash-slot sharding and hash tags in a cluster

## Prerequisites

| Need | Where |
|---|---|
| TTL and key lifecycle | [03-caching-patterns-lecture.md](03-caching-patterns-lecture.md) |
| Durability vocabulary (RPO/RTO) | [01-database-fundamentals-lecture.md](../01-database-fundamentals-lecture.md) |
| Cache/queue workloads | [07-session-and-queues-lecture.md](07-session-and-queues-lecture.md) |

## 1. RDB vs AOF — Two Persistence Philosophies

**RDB** is a point-in-time **snapshot** of the whole dataset, written on a
schedule (e.g. every 30s). Loading is fast and the file is compact — but a
crash loses everything written since the last snapshot. **AOF** is an
**append-only log** of every write, replayed on start; with fsync per write it
loses at most one write, but the log is bigger and replay is slower. Modern
Redis defaults to both: AOF for durability, RDB for fast restarts.

```python
def simulate_rdb_restore(snapshot_interval, crash, writes):
    last_snapshot = (int(crash) // snapshot_interval) * snapshot_interval
    return sum(1 for t, _ in writes if last_snapshot < t <= crash)

writes = [(i * 10.0, f"w{i}") for i in range(10)]   # one write per 10s
rdb_loss = simulate_rdb_restore(snapshot_interval=30, crash=85.0, writes=writes)
print(f"RDB (snapshot every 30s): lose {rdb_loss} write(s) after a crash at t=85")
print(f"AOF (fsync every write):  lose 0 writes after a crash")

# Output:
# RDB (snapshot every 30s): lose 2 write(s) after a crash at t=85
# AOF (fsync every write):  lose 0 writes after a crash
```

The tradeoff is the RPO/RTO story from databases: how much data may you lose
(RPO), and how fast must you come back (RTO)? Snapshot for speed, log for
durability, both for most production systems.

## 2. Eviction Policies — Who Dies at maxmemory

`maxmemory` bounds the store; `maxmemory-policy` picks the victim when it is
full:

| Policy | Victim | Use case |
|---|---|---|
| `noeviction` | none — writes FAIL loudly | queues, rate-limit keys |
| `allkeys-lru` | least-recently-used key anywhere | pure caches |
| `volatile-ttl` | keys with the earliest TTL | mixed: keep TTL-less keys |
| `allkeys-random` | anything | degenerate, rarely useful |

For caches, `allkeys-lru` is the classic choice: cold entries die, hot entries
survive, writes keep succeeding. For rate-limit keys, `noeviction` is safer —
evicting a limit means letting traffic through.

```python
def fill_then_evict(policy):
    c = RedisClient(clock=ManualClock(0.0))
    c.set_maxmemory(150, policy=policy)
    ok = True
    for i in range(10):
        try:
            c.set(f"k:{i}", "x" * 20)
        except MemoryError:
            ok = False
    return ok, c.keys()

print("noeviction: all 10 writes accepted?", fill_then_evict("noeviction")[0])
ok, keys = fill_then_evict("allkeys-lru")
print(f"allkeys-lru: all writes accepted? {ok} | surviving keys: {keys}")

# Output:
# noeviction: all 10 writes accepted? False
# allkeys-lru: all writes accepted? True | surviving keys: ['k:6', 'k:7', 'k:8', 'k:9']
```

## 3. Volatile Policies — TTL-Less Keys Are Sacred

`volatile-ttl` evicts only keys **with** a TTL, earliest expiry first — keys
without TTL survive no matter what. This is the policy for mixed workloads
where "must keep" data is deliberately TTL-less while cache data expires.

```python
vc = RedisClient(clock=ManualClock(0.0))
vc.set_maxmemory(150, policy="volatile-ttl")
for i in range(8):
    vc.set(f"v:{i}", "y" * 20, ex=1000 - i * 100)   # v:0 expires latest
vc.set("no-ttl:1", "z" * 20)
vc.set("no-ttl:2", "z" * 20)
print(f"volatile-ttl: no-ttl keys survived? "
      f"{bool(vc.exists('no-ttl:1') and vc.exists('no-ttl:2'))}")

# Output:
# volatile-ttl: no-ttl keys survived? True
```

## 4. Memory Reporting

`INFO memory` and `MEMORY USAGE key` report footprints; knowing your per-key
size is how you size `maxmemory` *before* an incident, not after.

```python
c = RedisClient(clock=ManualClock(0.0))
c.set("tiny", "a")
c.set("big", "x" * 500)
c.rpush("list:many", *range(50))
print(f"memory: tiny={c._key_size('tiny')}B big={c._key_size('big')}B "
      f"list:many={c._key_size('list:many')}B")

# Output:
# memory: tiny=17B big=516B list:many=1616B
```

Sizing is linear: 1M keys at 1 KB each is ~1 GB of maxmemory before anything
else runs. Report, alert, and size — in that order.

## 5. SCAN, Not KEYS

`KEYS *` blocks the server for the entire scan — on a busy production cache
that is seconds of frozen service. `SCAN` returns small cursor-driven batches;
the server keeps serving between them. The discipline is simple: in
automation, always `SCAN`.

```python
c2 = RedisClient(clock=ManualClock(0.0))
for i in range(50):
    c2.set(f"user:{i}:profile", "p")
cursor, seen = 0, 0
while True:
    cursor, batch = c2.scan(cursor, match="user:*", count=10)
    seen += len(batch)
    if cursor == 0:
        break
print(f"SCAN batches over 50 keys with count=10: {seen} keys found (cursor loop)")

# Output:
# SCAN batches over 50 keys with count=10: 50 keys found (cursor loop)
```

## 6. Cluster Basics — Hash Slots and Hash Tags

A Redis Cluster shards keys across **16,384 hash slots**: `CRC16(key) % 16384`.
Clients route by slot, so the key name decides the node. Hash tags — `{user:1}`
— hash only the braced text, forcing related keys into the same slot so
multi-key operations stay possible.

```python
def hash_slot(key):
    tag = key
    if "{" in key and "}" in key:
        start = key.index("{") + 1
        end = key.index("}", start)
        if start < end:
            tag = key[start:end]
    crc = 0
    for ch in tag.encode():
        crc = ((crc << 5) - crc + ch) & 0xFFFFFFFF
    return crc % 16384

print(f"slot('user:1:profile') = {hash_slot('user:1:profile')}")
print(f"slot('{{user:1}}:profile') = {hash_slot('{user:1}:profile')} "
      f"(hash tag forces same slot)")

# Output:
# slot('user:1:profile') = 15985
# slot('{user:1}:profile') = 16335 (hash tag forces same slot)
```

Sharding changes the failure story: a key lives on one node, so "the cluster"
fails per-node — which is why replicas and cross-slot discipline matter.

## Common Mistakes to Avoid

### Mistake 1: noeviction + no monitoring
```
# WRONG — cache writes start failing at 3 AM; the app 500s
# CORRECT — allkeys-lru for pure caches; alert on maxmemory usage
```

### Mistake 2: KEYS * in production scripts
```
# WRONG — blocks the server for the whole scan
keys = r.keys("*")

# CORRECT — SCAN with a cursor in small batches
```

### Mistake 3: RDB-only for a queue you cannot afford to lose
```
# WRONG — a crash between snapshots loses every queued job
# CORRECT — AOF (or streams + consumer groups) when loss is unacceptable
```

### Mistake 4: TTL-less keys under allkeys-lru
```
# WRONG — "no TTL means safe" is false; LRU evicts them exactly first
# CORRECT — volatile policies for must-keep keys, or size above the working set
```

## Best Practices

1. Use RDB + AOF together; snapshot for restart speed, log for durability.
2. Choose eviction by workload: `allkeys-lru` for caches, `noeviction` for
   rate limits and queues.
3. Give "must keep" data no TTL *and* use a volatile policy so it survives.
4. Report memory continuously; size maxmemory from real usage, not guesses.
5. `SCAN`, never `KEYS`, in any automated script.
6. Keep `maxmemory` below the instance RAM — Redis shares memory with the OS.
7. Alert on eviction counts: evictions are the first symptom of undersizing.
8. Use hash tags sparingly — they cluster hot keys onto one node.
9. Test restores, not just backups: a snapshot you never restored is a guess.
10. Document the persistence/eviction config per environment; they differ.

## Complexity and Cost

| Decision | Cost | Failure mode |
|---|---|---|
| RDB only | cheap, small file | lose up to one snapshot interval |
| AOF every write | write cost per op | nearly nothing |
| AOF fsync 1s | amortized | lose ≤1s on power loss |
| noeviction | none | writes fail when full |
| allkeys-lru | O(1) tracking | hot caches survive, cold die |
| volatile-ttl | O(1) tracking | TTL-less keys never evicted |

The operational budget is mostly *planning*: these are one-line configs whose
failure modes only appear under load or restart. The price of not planning is
an incident at 3 AM.

## AI Engineering Relevance

**Where this shows up:** AI state is exactly what these configs protect — cached
embeddings, queued indexing jobs, and shared token budgets.

| Concept here | Used for |
|---|---|
| RDB vs AOF | surviving a restart with your embedding cache and job queue |
| Eviction policies | cached completions dying gracefully instead of failing writes |
| Memory reporting | sizing the embedding-cache tier before the launch |
| `SCAN` | batch inventory of cache keys for migration |
| Hash slots | sharding a tenant's cache across cluster nodes |

**Scale note:** an embedding cache at 90% hit rate is valuable *and* heavy — a
few million 768-dim vectors eat gigabytes. Eviction policy decides whether the
cache degrades gracefully (LRU evicts cold vectors) or fails loudly
(noeviction). Size it before launch; the alert after is a postmortem.

## Practice Exercises

### Exercise 1: RDB loss window (Difficulty: Easy)
With a 30s snapshot and a crash at t=85, verify exactly the writes since the
last snapshot are lost (count 2 for one-write-per-10s).

### Exercise 2: noeviction vs allkeys-lru (Difficulty: Easy)
Fill past maxmemory under both policies; verify `noeviction` rejects writes
while `allkeys-lru` keeps accepting by evicting the oldest keys first.

### Exercise 3: volatile-ttl survivors (Difficulty: Medium)
Under `volatile-ttl`, verify TTL-less keys survive eviction while TTL-bearing
keys with the earliest TTL die first.

### Exercise 4: Memory sizing (Difficulty: Medium)
Measure `tiny` (17B), `big` (516B), and a 50-element list; verify the ranking
is proportional to value size, then estimate the footprint of 1M such keys.

### Exercise 5: Hash tags (Difficulty: Hard)
Verify `hash_slot("{user:1}:profile") == hash_slot("{user:1}:settings")`
while `user:1:profile` and `user:2:profile` land on different slots — the
cluster-placement contract.

## Summary

| Concept | Description |
|---|---|
| RDB | scheduled snapshot; fast restart, lossy window |
| AOF | append-only log; durable, heavier |
| noeviction | fail writes when full — safe, loud |
| allkeys-lru | evict least-recently-used; the cache default |
| volatile-ttl | evict expiring keys only |
| Memory reporting | size before the incident |
| SCAN | cursor batches; never block with KEYS |
| Hash slots | CRC16 % 16384; tags force co-location |

Persistence and eviction are the two configs that decide what your Redis holds
after a crash and what it holds when the RAM runs out. Both are one line each —
and both deserve a test.

## Quick Reference

| Task | Idiom |
|---|---|
| Durability | `appendonly yes`; RDB schedule + AOF |
| Cache eviction | `maxmemory-policy allkeys-lru` |
| Safe writes | `maxmemory-policy noeviction` for queues/limits |
| Protect TTL-less | `maxmemory-policy volatile-ttl` |
| Inventory | `SCAN cursor MATCH pattern COUNT n` |
| Memory | `INFO memory`, `MEMORY USAGE key` |
| Co-locate keys | `{tag}:suffix` in key names |

## Next Steps

Next: **[MongoDB 01 — Documents and Collections](mongodb/01-documents-and-collections-lecture.md)** —
the document model as the other major database family.

Continues in: **[Phase 5 — Backend](../../06-phase-5-backend/01-fastapi-lecture.md)** —
operating the caches and queues behind a real API.

Official docs: [redis.io/docs/latest/operate/oss_and_stack/management/persistence/](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)
