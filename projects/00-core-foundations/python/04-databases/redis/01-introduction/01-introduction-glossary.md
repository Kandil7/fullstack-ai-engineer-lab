# Redis — Glossary 01

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| AOF | Persistence | append-only log of writes, replayed on restart |
| Connection pool | Client | set of reusable TCP connections to Redis |
| EXPIRE | Key | set a key's time-to-live in seconds |
| GET | Command | read the string value of a key |
| INCR | Command | atomically increment an integer string |
| Key-value store | Model | database mapping keys to values, no schema |
| Latency | Ops | the reason Redis lives in memory: sub-ms ops |
| Memory-only | Storage | data held in RAM; persistence is optional |
| RDB | Persistence | point-in-time snapshot file |
| redis-py | Client | official Python driver for Redis |
| SET | Command | write a string value to a key |
| SET NX | Command | set only if the key does not exist |
| Single-threaded | Ops | one command at a time; fast ops keep it safe |
| TTL | Key | time-to-live; the key expires after this |
| Wrong tool | Design | cases where Redis is the wrong choice |

## Detailed Definitions

### AOF
**Definition**: The append-only-file persistence mode: every write is
appended to a log that is replayed on restart, losing at most the writes not
yet fsynced.
**Example**:
```python
# conceptual: appendonly yes in redis.conf
# a crash after "SET k v" replays the log and restores k -> v
```
```text
# durability: near-zero loss; cost: bigger file, slower replay
```
**Complexity**: O(1) amortized per write; replay O(log size).
**Related**: RDB, Persistence, Fsync

### Connection pool
**Definition**: A pre-opened set of TCP connections reused across requests,
avoiding the cost of a new connection per command.
**Example**:
```python
from redis_client import get_client

r = get_client()          # stand-in returns a pooled client
print(r.set("k", "v"))    # reuses an idle connection
```
```text
# real redis-py: redis.Redis(connection_pool=pool)
```
**Complexity**: one pool per process; O(1) per acquire/release.
**Related**: redis-py, Latency

### EXPIRE
**Definition**: Command that sets a key's TTL in seconds; the key is removed
when the timer elapses.
**Example**:
```python
from redis_client import RedisClient, ManualClock

r = RedisClient(clock=ManualClock(0.0))
r.set("session:1", "data")
r.expire("session:1", 30)
print(r.ttl("session:1"))  # -> 30
```
```text
# the key disappears 30s later without any explicit delete
```
**Complexity**: O(1).
**Related**: TTL, SET, Memory-only

### GET
**Definition**: Command that returns the string value stored under a key, or
None when absent.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.set("name", "sara")
print(r.get("name"))    # -> sara
print(r.get("missing")) # -> None
```
```text
# reads are O(1) because the value lives in memory
```
**Complexity**: O(1).
**Related**: SET, Key-value store

### INCR
**Definition**: Command that atomically increments the integer stored in a
string, creating it as 0 first when absent.
**Example**:
```python
from redis_client import get_client

r = get_client()
print(r.incr("hits"))   # -> 1
print(r.incr("hits"))   # -> 2
```
```text
# atomic: two concurrent INCRs never lose a count
```
**Complexity**: O(1).
**Related**: SET, Single-threaded

### Key-value store
**Definition**: A database family where values are addressed by keys with no
schema and no query language — the simplest data model.
**Example**:
```python
r.set("user:42:name", "sara")   # key:value pairs
r.set("feature:dark", "on")
print(r.get("feature:dark"))    # -> on
```
```text
# no tables, no columns, no joins — just key -> value
```
**Complexity**: O(1) per key op.
**Related**: Memory-only, GET, SET

### Latency
**Definition**: The round-trip time of a command; in Redis, typically
sub-millisecond because everything lives in RAM.
**Example**:
```python
# conceptual: a local Redis GET/PUT is ~0.1-0.5 ms
# vs tens of ms for a disk-backed database
```
```text
# latency is the entire value proposition of Redis
```
**Complexity**: dominated by network + serialization.
**Related**: Memory-only, Connection pool

### Memory-only
**Definition**: Redis stores the dataset in RAM; persistence to disk is a
separate, optional mechanism.
**Example**:
```python
# conceptual: 1 GB dataset needs ~1 GB RAM
# restart without persistence = empty dataset
```
```text
# memory is why it is fast and why it is expensive
```
**Complexity**: O(dataset) RAM.
**Related**: RDB, AOF, TTL

### RDB
**Definition**: Redis's snapshot persistence: a point-in-time dump of the
whole dataset, written on a schedule.
**Example**:
```python
# conceptual: save every 60s if 1000+ writes happened
# a crash loses writes since the last snapshot
```
```text
# compact file, fast load; RPO = snapshot interval
```
**Complexity**: O(dataset) per snapshot.
**Related**: AOF, Persistence

### redis-py
**Definition**: The official Python client library for Redis; the pattern all
stand-in exercises mirror.
**Example**:
```python
# real code:
# import redis
# r = redis.Redis(host="localhost", port=6379)
# r.set("k", "v"); r.get("k")
```
```text
# the stand-in RedisClient in this repo follows the same API
```
**Complexity**: O(1) per method call.
**Related**: Connection pool, SET, GET

### SET
**Definition**: Command that stores a string value under a key, overwriting
whatever was there.
**Example**:
```python
from redis_client import get_client

r = get_client()
r.set("greeting", "hello")
print(r.get("greeting"))  # -> hello
```
```text
# the most basic write in Redis
```
**Complexity**: O(1).
**Related**: GET, TTL, SET NX

### SET NX
**Definition**: SET with the NX flag: succeed only if the key does not exist
yet — the primitive for locks and single-flight claims.
**Example**:
```python
from redis_client import RedisClient, ManualClock

r = RedisClient(clock=ManualClock(0.0))
print(r.set("lock:job", "a", nx=True, ex=30))  # -> True
print(r.set("lock:job", "b", nx=True, ex=30))  # -> False
```
```text
# one atomic command: acquire + expiry together
```
**Complexity**: O(1).
**Related**: SET, EXPIRE, TTL

### Single-threaded
**Definition**: Redis executes commands one at a time on one thread, which is
safe because every command is O(1)-ish and fast.
**Example**:
```python
# conceptual: 1000 clients issue commands
# they are serialized: no two commands overlap
```
```text
# implication: one slow command (KEYS *) stalls everything
```
**Complexity**: O(1) per command keeps the model safe.
**Related**: INCR, Latency

### TTL
**Definition**: Time-to-live: the remaining seconds before a key expires and
is removed automatically.
**Example**:
```python
from redis_client import RedisClient, ManualClock

r = RedisClient(clock=ManualClock(0.0))
r.set("code", "1234", ex=300)
print(r.ttl("code"))  # -> 300
```
```text
# TTL is Redis's garbage collector: state that must die
```
**Complexity**: O(1).
**Related**: EXPIRE, Memory-only

### Wrong tool
**Definition**: The situations where Redis is the wrong choice: large
datasets, complex queries, durable storage, relational integrity.
**Example**:
```python
# WRONG: 500 GB of logs in Redis (RAM cost)
# WRONG: "find users whose age > 30" (no query language)
# WRONG: the only copy of critical records (no AOF, no replicas)
```
```text
# right: caches, queues, counters, sessions, rate limits
```
**Complexity**: n/a — a design decision.
**Related**: Key-value store, Memory-only

## Key Concepts Summary

### The model
- Keys are strings; values are strings (in this lecture) — no schema
- Everything lives in memory: sub-ms latency is the whole point
- TTL makes ephemeral state (sessions, codes, caches) self-cleaning

### The commands
- SET/GET are the atom; INCR adds atomic counters
- EXPIRE/TTL manage lifetimes; SET NX adds conditional writes
- The single-threaded model makes these O(1) ops composable

### Operations
- Connection pooling keeps client overhead near zero
- RDB and AOF decide what survives a restart
- Knowing when Redis is the WRONG tool is part of the skill

## Practice Terms

Match each term to its definition (answers at the bottom).

1. TTL — ___
2. INCR — ___
3. SET NX — ___
4. Connection pool — ___
5. RDB — ___
6. Single-threaded — ___
7. Memory-only — ___
8. Key-value store — ___

a) Snapshot file of the whole dataset
b) One command at a time, serialized
c) Time-to-live before a key expires
d) Reused TCP connections in the client
e) Atomic counter increment
f) Data held in RAM, not on disk
g) Set only if the key does not exist
h) Database mapping keys to values without schema

**Answers:** 1-c, 2-e, 3-g, 4-d, 5-a, 6-b, 7-f, 8-h
