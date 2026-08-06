# Redis — Glossary 05

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Acknowledgment | Delivery | the signal that a worker finished an entry |
| At-least-once | Delivery | every entry processed ≥1 time; duplicates possible |
| Backpressure | Ops | how the system reacts when consumers lag |
| Channel | Pub/Sub | named topic that subscribers listen to |
| Consumer group | Stream | named cursor shared by workers over a stream |
| Exactly-once | Delivery | no loss and no duplicates; must be built by the app |
| Idempotent | Design | repeating the work has no extra effect |
| Missed message | Pub/Sub | a message published while you were offline |
| Pending | Stream | entries delivered but not yet acknowledged |
| PUBLISH | Pub/Sub | deliver a message to all current subscribers |
| Pub/Sub | Pattern | live fan-out with no storage, no replay |
| Replay | Stream | re-reading entries from any offset |
| Stream | Type | durable append-only log of (id, fields) entries |
| SUBSCRIBE | Pub/Sub | register interest in a channel |
| XACK | Stream | acknowledge an entry in a consumer group |
| XADD | Stream | append an entry to a stream |
| XRANGE | Stream | read a slice of the log by id |

## Detailed Definitions

### Acknowledgment
**Definition**: The explicit signal a worker sends (XACK) to say an entry is
fully processed; unacked entries stay pending.
**Example**:
```python
group.ack("worker-1", entry_id)  # done, remove from pending
```
```text
# ack AFTER the side effect, never before
```
**Complexity**: O(1).
**Related**: Pending, At-least-once

### At-least-once
**Definition**: The delivery guarantee of streams with groups: every entry is
delivered at least once; a crash before ack means redelivery.
**Example**:
```python
# worker processes, crashes before ack -> entry redelivered
# consequence: consumers must be idempotent
```
```text
# exactly-once is not offered; dedup is an app concern
```
**Complexity**: n/a — a semantic guarantee.
**Related**: Idempotent, Acknowledgment, Exactly-once

### Backpressure
**Definition**: The system's behavior when producers outpace consumers; in
streams the pending backlog makes it visible and actionable.
**Example**:
```python
# pub/sub: a slow subscriber's buffer grows in ITS memory until OOM
# streams: group pending grows in Redis — monitor, alert, scale
```
```text
# visible backpressure is the operational win of streams
```
**Complexity**: n/a — monitored via pending counts.
**Related**: Pending, Pub/Sub

### Channel
**Definition**: The named topic in pub/sub that publishers write to and
subscribers listen on.
**Example**:
```python
r.subscribe("events:documents")          # listen
r.publish("events:documents", "doc-1")   # announce
```
```text
# no history: subscribers only see what arrives while connected
```
**Complexity**: O(subscribers) per publish.
**Related**: PUBLISH, SUBSCRIBE

### Consumer group
**Definition**: A named cursor over a stream shared by several workers; each
entry is delivered to exactly one member of the group.
**Example**:
```python
w1 = group.read("worker-1", count=3)
w2 = group.read("worker-2", count=3)
# 5 entries partitioned across two workers, no overlap
```
```text
# the group, not the worker, owns the position in the log
```
**Complexity**: O(1) per delivery.
**Related**: Stream, Acknowledgment, Pending

### Exactly-once
**Definition**: The guarantee that each entry is processed exactly once —
not offered by streams; achieved by idempotent consumers plus dedup keys.
**Example**:
```python
# at-least-once + idempotency + dedup key = effectively-once
# dedup: skip if "job:<id>:done" already set
```
```text
# the strongest guarantee is built, not bought
```
**Complexity**: extra check per message.
**Related**: At-least-once, Idempotent

### Idempotent
**Definition**: An operation whose repeated execution has no additional
effect — the requirement for at-least-once consumers.
**Example**:
```python
# embedding is naturally idempotent:
# same doc -> same chunk hash -> same vector, re-running is harmless
# sending an email is not: needs a dedup key checked before send
```
```text
# idempotency is how you live with redelivery
```
**Complexity**: n/a — a design property.
**Related**: At-least-once, Exactly-once

### Missed message
**Definition**: In pub/sub, a message published while a subscriber was not
connected is gone — the core limitation of the model.
**Example**:
```python
late = r.subscribe("events:documents")  # joins after doc-1 was published
print(late.get_message())               # doc-2 arrives; doc-1 is lost
```
```text
# the stream exists precisely because of this
```
**Complexity**: n/a.
**Related**: Pub/Sub, Stream

### Pending
**Definition**: The count of entries a consumer group has delivered but not
yet acknowledged — the visible backlog.
**Example**:
```python
print(group.pending())  # 5 after delivery, 4 after one ack
```
```text
# the operational metric for stream health
```
**Complexity**: O(1).
**Related**: Acknowledgment, Backpressure

### PUBLISH
**Definition**: The pub/sub command that delivers a message to every current
subscriber and returns how many received it.
**Example**:
```python
delivered = r.publish("events:documents", "doc-1 uploaded")
print(delivered)  # -> 2 (subscribers reached)
```
```text
# fire-and-forget: nothing is stored
```
**Complexity**: O(subscribers).
**Related**: SUBSCRIBE, Channel, Pub/Sub

### Pub/Sub
**Definition**: The pattern of live message fan-out with no storage: fast,
simple, and lossy for offline subscribers.
**Example**:
```python
sub_a = r.subscribe("events:documents")
r.publish("events:documents", "hello")
print(sub_a.get_message())  # -> hello
```
```text
# for notifications, not for jobs
```
**Complexity**: O(1) per subscriber per message.
**Related**: Channel, Missed message, Stream

### Replay
**Definition**: Re-reading stream entries from an earlier offset — possible
because streams persist, impossible with pub/sub.
**Example**:
```python
replay = stream.xrange(0, 1)
print(replay[0][0])  # -> '1-0' (the first entry, again)
```
```text
# replay powers audits, retries, and rebuilds
```
**Complexity**: O(offset + count).
**Related**: Stream, XRANGE

### Stream
**Definition**: Redis's durable append-only log: entries with auto-generated
ids, replayable, and consumable by groups.
**Example**:
```python
stream = Stream(r, "stream:ingest")
stream.xadd({"doc": "file-0.pdf", "size": "100"})
print(stream.xlen())  # -> 1
```
```text
# the job-queue primitive for pipelines that must not lose work
```
**Complexity**: O(log n) per append.
**Related**: XADD, Consumer group, Pub/Sub

### SUBSCRIBE
**Definition**: The pub/sub command registering a client's interest in a
channel; messages arrive while subscribed.
**Example**:
```python
sub = r.subscribe("events:documents")
print(sub.get_message())  # next message, or None if empty
```
```text
# subscribing later means missing earlier messages
```
**Complexity**: O(1).
**Related**: PUBLISH, Channel

### XACK
**Definition**: The command acknowledging a delivered entry, removing it from
the group's pending set.
**Example**:
```python
group.ack("worker-1", "1-0")  # mark entry 1-0 finished
print(group.pending())        # decremented
```
```text
# ack is the "done" signal in at-least-once delivery
```
**Complexity**: O(1).
**Related**: Acknowledgment, Consumer group

### XADD
**Definition**: The command appending an entry to a stream, returning its
auto-generated monotonic id.
**Example**:
```python
entry_id = stream.xadd({"doc": "file-1.pdf", "size": "101"})
print(entry_id)  # -> '2-0'
```
```text
# ids are ordered, so XRANGE can slice by position
```
**Complexity**: O(log n).
**Related**: Stream, XRANGE

### XRANGE
**Definition**: The command reading a slice of a stream by id — the replay
and audit primitive.
**Example**:
```python
entries = stream.xrange(0, 1)  # first two entries
print(len(entries))            # -> 2
```
```text
# read-only: does not move any consumer group position
```
**Complexity**: O(offset + count).
**Related**: Stream, Replay

## Key Concepts Summary

### Two primitives
- Pub/Sub: live fan-out, no storage, at-most-once, misses messages
- Streams: durable log, replayable, consumer groups, at-least-once

### Delivery semantics
- Groups partition entries across workers without double delivery
- Ack after the side effect; unacked entries stay pending and redeliver
- At-least-once is the contract — consumers must be idempotent

### Operations
- Pending count is the visible backlog: monitor, alert, scale workers
- Pub/Sub backpressure is invisible until the client OOMs

## Practice Terms

Match each term to its definition (answers at the bottom).

1. PUBLISH — ___
2. Consumer group — ___
3. XACK — ___
4. At-least-once — ___
5. Pending — ___
6. Idempotent — ___
7. Replay — ___
8. Missed message — ___

a) Signal that an entry is finished
b) Deliver to all current subscribers, store nothing
c) Delivered but unacknowledged entries
d) Redelivery after crash; duplicates possible
e) Re-reading entries from an old offset
f) A message gone because you were offline
g) One cursor shared by many workers
h) Repeating the work has no extra effect

**Answers:** 1-b, 2-g, 3-a, 4-d, 5-c, 6-h, 7-e, 8-f
