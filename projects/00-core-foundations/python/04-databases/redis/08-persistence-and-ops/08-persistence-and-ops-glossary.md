# Redis — Glossary 08

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| AOF | Persistence | append-only file replaying every write |
| AOF rewrite | Persistence | compacting the AOF to the current state |
| BGSAVE | Persistence | background snapshot to RDB |
| CRC16 | Cluster | hash the key to choose its slot |
| Cursor | Ops | SCAN's pagination handle for incremental iteration |
| Durability | Persistence | how much committed data survives a crash |
| Eviction | Memory | deleting keys under memory pressure |
| fsync | Persistence | flushing the write buffer to disk |
| Hash slot | Cluster | the 16384 buckets keys map into |
| Hash tag | Cluster | forcing keys into one slot for multi-key ops |
| KEYS | Ops | the dangerous full-key scan — never in production |
| LFU | Eviction | evict least-frequently-used keys |
| LRU | Eviction | evict least-recently-used keys |
| Maxmemory | Memory | the configured memory ceiling |
| Noeviction | Eviction | refuse writes when memory is full |
| RDB | Persistence | point-in-time compressed snapshot |
| Replication | Ops | copying data to follower nodes |
| Save point | Persistence | conditions that trigger an RDB snapshot |
| SCAN | Ops | incremental, non-blocking key iteration |
| Snapshot | Persistence | a point-in-time dump of the dataset |

## Detailed Definitions

### AOF
**Definition**: The append-only-file persistence: every write is appended as
a command and replayed at startup — the most durable option.
**Example**:
```python
# config: appendonly yes, appendfsync everysec
# on restart: replay the AOF to rebuild the dataset
```
```text
# durability sits between "any second lost" and RDB's last-snapshot
```
**Complexity**: O(1) amortized per write.
**Related**: fsync, Durability, AOF rewrite

### AOF rewrite
**Definition**: Compacting the AOF by writing the current dataset as fresh
commands — the file stops growing forever.
**Example**:
```python
# 1M INCRs become one final value in the rewritten AOF
```
```text
# rewrites run automatically and safely in the background
```
**Complexity**: O(dataset) periodically.
**Related**: AOF, Durability

### BGSAVE
**Definition**: Forking to write an RDB snapshot in the background — the
dataset is captured without blocking the server.
**Example**:
```python
# auto: triggered by save points (e.g. 900s + 1 change)
# manual: BGSAVE when you want a backup point
```
```text
# the fork cost is the memory-price of RDB
```
**Complexity**: O(dataset) in background.
**Related**: RDB, Save point

### CRC16
**Definition**: The hash function mapping a key to one of 16384 slots —
the first step of cluster routing.
**Example**:
```python
slot = crc16(key) % 16384      # which bucket?
node = slot_owner[slot]        # which node owns it?
```
```text
# the client, not the server, does the routing in cluster mode
```
**Complexity**: O(key length).
**Related**: Hash slot, Hash tag

### Cursor
**Definition**: SCAN's pagination handle: each call returns a next cursor
(0 = done), so iteration never holds the whole keyspace.
**Example**:
```python
cursor = 0
while True:
    cursor, keys = r.scan(cursor, match="cache:*", count=100)
    # process this page...
    if cursor == 0:
        break
```
```text
# a cursor session may see keys added mid-scan — it is a snapshot
# approximation, which is fine for cleanup jobs
```
**Complexity**: O(page) per call.
**Related**: SCAN, KEYS

### Durability
**Definition**: How much acknowledged data survives a crash — from RDB's
"since last snapshot" to AOF everysec's "≤1 second".
**Example**:
```python
# RDB: lose everything after the last save point
# AOF everysec: lose at most ~1 second
# AOF always: lose nothing (at fsync cost)
```
```text
# choose durability against throughput, not against taste
```
**Complexity**: n/a — the design axis.
**Related**: RDB, AOF, fsync

### Eviction
**Definition**: Redis deleting keys to stay under maxmemory — the policy
defines which keys die first.
**Example**:
```python
# allkeys-lru: least recently used, any key
# volatile-ttl: shortest remaining TTL first
```
```text
# a cache is only a cache if eviction is configured
```
**Complexity**: O(1) amortized.
**Related**: LRU, LFU, Maxmemory

### fsync
**Definition**: Flushing the OS write buffer to disk; the frequency decides
the durability/throughput trade.
**Example**:
```python
# everysec: flush once per second (default; ~1s loss max)
# always: flush every command (slowest, most durable)
# no: OS decides (fastest, crash can lose a lot)
```
```text
# everysec is the usual production choice
```
**Complexity**: O(1) at the chosen cadence.
**Related**: AOF, Durability

### Hash slot
**Definition**: One of the 16384 buckets a key maps into; each cluster node
owns a contiguous range of slots.
**Example**:
```python
# key "user:1" -> crc16 -> slot 1062 -> owned by node-3
# moving slots = resharding; moving keys = anything goes
```
```text
# slot ownership, not key ownership, is the cluster contract
```
**Complexity**: O(1) per lookup.
**Related**: CRC16, Hash tag

### Hash tag
**Definition**: Using `{...}` in a key so only the braces' content is hashed
— forcing related keys into the same slot for multi-key atomicity.
**Example**:
```python
# "user:{42}:cart" and "user:{42}:profile" -> same slot
# MULTI/EXEC across them is legal; without the tag it is not
```
```text
# tags concentrate load — use them for related keys only
```
**Complexity**: O(1).
**Related**: Hash slot, CRC16

### KEYS
**Definition**: The command that blocks the whole server scanning every key
— the production anti-pattern SCAN exists to replace.
**Example**:
```python
# NEVER: r.keys("*") in production (O(N) blocking)
# instead: SCAN with a cursor
```
```text
# one accidental keys() at 10M keys = multi-second stall
```
**Complexity**: O(N) blocking.
**Related**: SCAN, Cursor

### LFU
**Definition**: Least-frequently-used eviction: keys used often survive even
if untouched recently; a periodic decay prevents permanent residency.
**Example**:
```python
# maxmemory-policy allkeys-lfu
# hot keys stay; one-hit wonders leave first
```
```text
# better than LRU for skewed access (the AI/LLM cache shape)
```
**Complexity**: O(1) amortized.
**Related**: Eviction, LRU

### LRU
**Definition**: Least-recently-used eviction: the key untouched the longest
is evicted first — the classic cache policy.
**Example**:
```python
# maxmemory-policy allkeys-lru
# approximate LRU: sampling, not a perfect order
```
```text
# the default answer for "which cache policy"
```
**Complexity**: O(1) amortized.
**Related**: Eviction, LFU

### Maxmemory
**Definition**: The configured memory ceiling; when reached, the eviction
policy decides what dies.
**Example**:
```python
# maxmemory 512mb
# maxmemory-policy allkeys-lru
```
```text
# without a ceiling, a runaway cache OOMs the instance
```
**Complexity**: n/a — configuration.
**Related**: Eviction, Noeviction

### Noeviction
**Definition**: The policy that refuses writes when memory is full —
guaranteed data survival at the cost of write errors.
**Example**:
```python
# maxmemory-policy noeviction
# SET fails with OOM when full; GETs keep working
```
```text
# right for stores, wrong for caches
```
**Complexity**: O(1).
**Related**: Maxmemory, Eviction

### RDB
**Definition**: The point-in-time compressed snapshot of the whole dataset —
fast to load, bounded by snapshot frequency in durability.
**Example**:
```python
# dump.rdb written at save points (900s/1, 300s/10, 60s/10000)
```
```text
# load speed and simplicity; the loss window is the trade
```
**Complexity**: O(dataset) per snapshot.
**Related**: BGSAVE, Snapshot, Save point

### Replication
**Definition**: Copying the primary's data to follower nodes — the basis of
read scaling and failover.
**Example**:
```python
# replicaof primary 6379
# reads fan out to replicas; writes stay on the primary
```
```text
# replicas can serve RDB backups without touching the primary
```
**Complexity**: O(dataset) initial + O(ops) steady.
**Related**: Durability, RDB

### Save point
**Definition**: The rules that trigger an automatic RDB snapshot, expressed
as time + number of changes.
**Example**:
```python
# save 900 1      # 15 min and ≥1 change
# save 300 10     # 5 min and ≥10 changes
# save 60 10000   # 1 min and ≥10000 changes
```
```text
# save points define the maximum snapshot loss window
```
**Complexity**: checked on writes.
**Related**: RDB, BGSAVE

### SCAN
**Definition**: Incremental key iteration returning pages of keys plus a
cursor — non-blocking, unlike KEYS.
**Example**:
```python
cursor, keys = r.scan(0, match="cache:*", count=100)
print(cursor, len(keys))  # e.g. 427, 100 — keep calling with 427
```
```text
# the only production-safe way to walk the keyspace
```
**Complexity**: O(page) per call, no full lock.
**Related**: Cursor, KEYS

### Snapshot
**Definition**: A point-in-time capture of the dataset — the RDB file's
content, used for backups and restores.
**Example**:
```python
# cp dump.rdb backup-$(date).rdb  ->  off-machine restore point
```
```text
# snapshots are the backup story; AOF is the fine-grained story
```
**Complexity**: O(dataset).
**Related**: RDB, BGSAVE

## Key Concepts Summary

### Persistence axes
- RDB: point-in-time snapshot, fast loads, loss = last save point
- AOF: command log, ~1s loss with everysec, compacted by rewrites
- fsync frequency is the durability slider; save points set the RDB window

### Memory
- maxmemory + a policy: LRU (recency), LFU (frequency), volatile-ttl
  (shortest TTL), noeviction (refuse writes — the only no-loss policy)
- A cache without eviction is a memory leak

### Operations
- SCAN with cursors, never KEYS
- Cluster: CRC16 -> 16384 slots; hash tags pull related keys together
- Replicas scale reads and provide backup copies

## Practice Terms

Match each term to its definition (answers at the bottom).

1. AOF — ___
2. RDB — ___
3. Save point — ___
4. LRU — ___
5. Noeviction — ___
6. SCAN — ___
7. Hash tag — ___
8. KEYS — ___

a) Point-in-time snapshot file
b) Append-only command log
c) Conditions triggering a snapshot
d) Evict least-recently-used keys
e) Refuse writes when memory is full
f) Incremental, non-blocking iteration
g) {braces} force one slot for related keys
h) The blocking full-scan anti-pattern

**Answers:** 1-b, 2-a, 3-c, 4-d, 5-e, 6-f, 7-g, 8-h
