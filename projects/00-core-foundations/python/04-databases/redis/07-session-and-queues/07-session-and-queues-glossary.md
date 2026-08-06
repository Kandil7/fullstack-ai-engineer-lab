# Redis — Glossary 07

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Delay queue | Queue | entries parked under future timestamps |
| FIFO queue | Queue | LPUSH in, RPOP out — strict order |
| Heartbeat | Lease | periodic lease renewal by the working consumer |
| Lazy expiry | Session | cleanups done on access, not by a timer |
| Lease | Queue | temporary exclusive claim on a queued item |
| LPUSH | Primitive | push an item to the list head |
| Priority queue | Queue | zset ordered by score, not arrival |
| Promotion | Queue | moving due delay entries into the work list |
| Recovery | Queue | reclaiming leases whose heartbeat died |
| Redelivery | Queue | recovered items returning to the queue |
| RPOP | Primitive | pop an item from the list tail |
| Score | Primitive | the sorting number in a zset |
| Session | Pattern | server-side state keyed by session id |
| Session key | Session | the `session:<sid>` hash holding fields |
| Slide | Session | refresh the TTL on every activity |
| Sorted set | Type | zset — members ordered by score |
| Timeout | Session | max idle lifetime; expiry after it |
| Worker | Queue | the consumer loop: pop, work, ack |
| ZADD | Primitive | add a member with a score |
| ZPOPMIN | Primitive | pop the lowest-scored member |

## Detailed Definitions

### Delay queue
**Definition**: A queue whose items are parked under future timestamps and
only promoted when they become due — scheduling without a timer.
**Example**:
```python
delay.zadd("jobs:delayed", {msg: future_ts})   # park until future_ts
# every poll: promote all members with score <= now into the work list
```
```text
# enables retries, rate-spaced sends, and timeouts-as-queues
```
**Complexity**: O(log n) per add/pop.
**Related**: Promotion, Sorted set, Score

### FIFO queue
**Definition**: A list where producers LPUSH and consumers RPOP — first in,
first out, strict arrival order.
**Example**:
```python
work.lpush("jobs:work", "job-1")
work.lpush("jobs:work", "job-2")
print(work.rpop("jobs:work"))  # -> job-1 (oldest first)
```
```text
# the simplest queue; no priorities, no scheduling
```
**Complexity**: O(1) per op.
**Related**: LPUSH, RPOP, Worker

### Heartbeat
**Definition**: Periodic renewal of a lease so the system knows the consumer
is alive; a dead heartbeat lets the lease expire and the item recover.
**Example**:
```python
# consumer holds lease "job-1 | worker-a" for 30s, renews every 10s
# worker-a dies -> no renewal -> lease expires -> item redelivered
```
```text
# the heartbeat converts liveness into a measurable time
```
**Complexity**: O(1) per beat.
**Related**: Lease, Recovery

### Lazy expiry
**Definition**: Cleaning expired sessions on access instead of scanning —
you only pay when the key is actually touched.
**Example**:
```python
# Redis lazy-deletes keys whose TTL passed when they are accessed
# pattern: check-and-delete on read, never a full sweep
```
```text
# O(1) on demand, no background scans
```
**Complexity**: O(1) per access.
**Related**: Session, Timeout, Slide

### Lease
**Definition**: A temporary exclusive claim on a queued item, so a worker can
work without holding a lock the whole time.
**Example**:
```python
lease = claim("job-1", "worker-a", ttl=30)
# no other worker gets job-1 until lease expiry
# worker-a processes; on success it DELETES the item outright
```
```text
# leases bound how long a claim lasts — crash-safe by design
```
**Complexity**: O(1).
**Related**: Heartbeat, Recovery, Redelivery

### LPUSH
**Definition**: Push an item onto the head of a list — the producer side of
the FIFO queue.
**Example**:
```python
work.lpush("jobs:work", "job-3")   # head
print(work.llen("jobs:work"))      # -> 3
```
```text
# producers never block; backpressure shows as list growth
```
**Complexity**: O(1).
**Related**: FIFO queue, RPOP

### Priority queue
**Definition**: A zset used as a queue, ordered by score so higher-priority
items pop first regardless of arrival.
**Example**:
```python
# urgent scores 0, normal scores 1: ZPOPMIN always takes urgent first
print(z.zpopmin("jobs:prio")[0][0])  # highest priority
```
```text
# scores are the ordering authority; duplicates are allowed
```
**Complexity**: O(log n) per op.
**Related**: Sorted set, ZADD, ZPOPMIN

### Promotion
**Definition**: Moving due delay-queue entries (score <= now) into the work
list so they become processable.
**Example**:
```python
due = delay.zpopmin_by_score(now)   # members with score <= now
for msg in due:
    work.lpush("jobs:work", msg)    # now workable
```
```text
# the poll loop runs every tick — the delay queue's only engine
```
**Complexity**: O(due) per tick.
**Related**: Delay queue, Sorted set

### Recovery
**Definition**: Reclaiming leases whose heartbeat died (lease TTL expired),
so the item is not lost with the consumer.
**Example**:
```python
# worker-a's lease on job-1 expired without ack
# a scan finds it and returns it to the work list
# (in Redis: stream groups do this via XAUTOCLAIM / pending IDs)
```
```text
# recovery is what turns at-least-once from theory into practice
```
**Complexity**: O(pending) on the reclaim scan.
**Related**: Lease, Heartbeat, Redelivery

### Redelivery
**Definition**: A recovered item being handed to a consumer again — the
second half of the crash-recovery cycle.
**Example**:
```python
# job-1 was in-flight with worker-a; now it is on the work list again
print(work.rpop("jobs:work"))  # -> job-1, retried
```
```text
# consumers must be idempotent: redelivery is normal
```
**Complexity**: O(1) per redelivery.
**Related**: Recovery, Lease

### RPOP
**Definition**: Pop an item from the tail of a list — the consumer side of
the FIFO queue.
**Example**:
```python
job = work.rpop("jobs:work")   # oldest first
print(job)                     # -> job-1
```
```text
# the natural partner of LPUSH: FIFO by construction
```
**Complexity**: O(1).
**Related**: FIFO queue, LPUSH

### Score
**Definition**: The double stored with each zset member that defines its
sort position; lower scores sort and pop first.
**Example**:
```python
z.zadd("jobs:prio", {"urgent": 0, "normal": 1})
# score 0 < score 1, so urgent always pops first
```
```text
# scores can encode timestamps (delay queue) or priority
```
**Complexity**: O(1) per compare.
**Related**: Sorted set, ZADD, Priority queue

### Session
**Definition**: Server-side state keyed by session id — Redis keeps it out
of the cookie, off the disk, and shared across replicas.
**Example**:
```python
client.hset(f"session:{sid}", "user_id", "42")
client.expire(f"session:{sid}", 3600)
```
```text
# the classic stateless-server / shared-state trade
```
**Complexity**: O(1) per access.
**Related**: Session key, Timeout, Slide

### Session key
**Definition**: The Redis key `session:<sid>` — typically a hash holding the
session fields.
**Example**:
```python
key = f"session:{sid}"
client.hset(key, "user_id", "42")       # field per attribute
client.expire(key, 3600)                 # lifetime bound
```
```text
# the sid lives in the cookie; everything else lives here
```
**Complexity**: O(1).
**Related**: Session, Slide

### Slide
**Definition**: Refreshing the session TTL on every activity — idle
timeouts, not absolute ones.
**Example**:
```python
# on each request:
client.expire(f"session:{sid}", 3600)   # the clock restarts
# inactive for 1h -> gone; active forever -> stays
```
```text
# "idle timeout" is the default UX expectation
```
**Complexity**: O(1) per request.
**Related**: Session key, Timeout, Lazy expiry

### Sorted set
**Definition**: The Redis type pairing members with scores, ordered by
score — the substrate of priority and delay queues.
**Example**:
```python
z.zadd("jobs:prio", {"urgent": 0, "normal": 1})
print(z.zrange("jobs:prio", 0, -1))  # -> ['urgent', 'normal']
```
```text
# where lists give FIFO, zsets give ORDER
```
**Complexity**: O(log n) per op.
**Related**: ZADD, ZPOPMIN, Score

### Timeout
**Definition**: The max idle lifetime of a session; expiry after it — the
security control that abandoned sessions do not live forever.
**Example**:
```python
client.expire(f"session:{sid}", 3600)   # 1h idle -> dead
print(client.ttl(f"session:{sid}"))     # seconds remaining
```
```text
# combined with slide: idle timeout; without slide: absolute
```
**Complexity**: O(1).
**Related**: Session, Slide, Lazy expiry

### Worker
**Definition**: The consumer loop: pop an item, process it, delete/ack it —
with leases so crashes redeliver instead of losing work.
**Example**:
```python
while True:
    item = claim_and_pop()      # lease-bound pop
    process(item)               # the actual job
    delete_if_done(item)        # ack: remove from the system
```
```text
# the worker contract: at-least-once, idempotent handlers
```
**Complexity**: O(1) per iteration.
**Related**: FIFO queue, Lease, Redelivery

### ZADD
**Definition**: Add a member with a score to a zset — the write side of
priority and delay queues.
**Example**:
```python
z.zadd("jobs:delayed", {msg: future_ts})   # park until future_ts
z.zadd("jobs:prio", {"urgent": 0})          # priority ordering
```
```text
# adding is O(log n); order is always maintained
```
**Complexity**: O(log n).
**Related**: Sorted set, Score, Delay queue

### ZPOPMIN
**Definition**: Pop the member with the lowest score — the read side of
priority queues; for delay queues, pop-when-due.
**Example**:
```python
member = z.zpopmin("jobs:prio")[0][0]   # lowest score first
```
```text
# with scores as timestamps, ZPOPMIN is "oldest first"
```
**Complexity**: O(log n).
**Related**: Priority queue, Delay queue

## Key Concepts Summary

### Queues
- FIFO: LPUSH + RPOP, strict arrival order
- Priority: zset scores order the pops
- Delay: future scores park work until due; promotion moves it out

### Sessions
- Session state lives in Redis: `session:<sid>` hashes with TTL
- Slide + timeout = idle expiry; lazy expiry cleans on access
- Sessions buy stateless replicas; they cost a shared-store dependency

### Reliable work
- Leases bound in-flight claims; heartbeats renew them
- Dead heartbeats -> recovery -> redelivery: at-least-once, so handlers
  must be idempotent

## Practice Terms

Match each term to its definition (answers at the bottom).

1. FIFO queue — ___
2. Delay queue — ___
3. Promotion — ___
4. Lease — ___
5. Recovery — ___
6. Slide — ___
7. Lazy expiry — ___
8. ZPOPMIN — ___

a) Parked under future timestamps
b) LPUSH in, RPOP out
c) TTL refreshed on every activity
d) Moving due entries into the work list
e) Temporary exclusive claim on an item
f) Cleanup on access, not by timer
g) Reclaiming items whose heartbeat died
h) Pop the lowest-scored member

**Answers:** 1-b, 2-a, 3-d, 4-e, 5-g, 6-c, 7-f, 8-h
