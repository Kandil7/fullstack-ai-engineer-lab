# Databases — 05: Redis Pub/Sub and Streams

## Topic Overview

When a document lands in the upload bucket, someone must embed it, chunk it,
and index it — without blocking the API caller. This is a *decoupling* problem:
producers and consumers should not share a call stack, a process, or a clock.
Redis offers two answers with very different guarantees.

**Pub/Sub** is live fan-out: `PUBLISH` delivers a message to every current
subscriber and stores nothing. Fast, simple, and lossy — a subscriber that is
offline at publish time never sees the message. **Streams** are a durable,
append-only log with consumer groups: entries survive restarts, are delivered
to exactly one worker per group, can be acknowledged, and can be replayed.
Choosing between them decides whether a crashed worker loses work.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Publish and subscribe, and explain why pub/sub is fire-and-forget
2. Explain the missed-message problem (no storage, no replay)
3. Add entries to a stream and read them back in order
4. Create a consumer group and explain single-delivery partitioning
5. Acknowledge work and track the group's pending backlog
6. Explain at-least-once delivery and why consumers must be idempotent
7. Compare pub/sub and streams on durability, backpressure, and replay
8. Choose the right primitive for a given AI pipeline stage

## Prerequisites

| Need | Where |
|---|---|
| Lists and sorted sets | [02-data-structures-lecture.md](02-data-structures-lecture.md) |
| Job queues as lists | [07-session-and-queues-lecture.md](07-session-and-queues-lecture.md) |
| At-least-once thinking | [02-distributed-systems-lecture.md](../../03-systems/02-distributed-systems-lecture.md) |

## 1. Pub/Sub — Live Fan-Out, Nothing Stored

A subscriber registers interest in a channel; a publisher sends a message; Redis
delivers it to every *currently connected* subscriber and returns the count.
That is the whole model — there is no history.

```python
from redis_client import get_client

r = get_client()
sub_a = r.subscribe("events:documents")
sub_b = r.subscribe("events:documents")

delivered = r.publish("events:documents", "doc-1 uploaded")
print(f"publish returned {delivered} (subscribers reached)")
print(f"A got: {sub_a.get_message()}")
print(f"B got: {sub_b.get_message()}")
print(f"A second read: {sub_a.get_message()} (queue now empty)")

# Output:
# publish returned 2 (subscribers reached)
# A got: doc-1 uploaded
# B got: doc-1 uploaded
# A second read: None (queue now empty)
```

A subscriber that joins *after* the publish sees nothing. The missed-message
problem is a feature of the design: pub/sub is for notifications ("reload the
config", "a user logged in"), never for work that must not be lost.

## 2. Streams — the Durable Log

A stream is an append-only sequence of entries, each `(id, {field: value})`.
`XADD` appends (the id is auto-generated and monotonic), `XLEN` reports depth,
`XRANGE` reads any slice. Entries live in Redis, survive restarts, and can be
re-read any number of times — this is what "durable" means here.

```python
class Stream:  # stand-in modeled on XADD/XLEN/XRANGE
    ...
    def xadd(self, fields): ...      # returns entry id
    def xlen(self): ...              # number of entries
    def xrange(self, start=0, end=-1): ...

stream = Stream(r, "stream:ingest")
for i in range(5):
    stream.xadd({"doc": f"file-{i}.pdf", "size": str(100 + i)})
print(f"stream length: {stream.xlen()}")

# Output:
# stream length: 5
```

## 3. Consumer Groups — One Delivery Per Worker

A consumer group is a named cursor over a stream shared by a set of workers.
Each entry is delivered to **exactly one** member of the group: five entries,
two workers, and work is partitioned without overlap. Workers also maintain a
*pending* count — entries delivered but not yet acknowledged.

```python
group = ConsumerGroup(stream, "embed-workers")
w1 = group.read("worker-1", count=3)
w2 = group.read("worker-2", count=3)
print(f"worker-1 took {len(w1)} entries, worker-2 took {len(w2)} (no double delivery)")
print(f"group pending (unacked): {group.pending()}")
group.ack("worker-1", w1[0][0])
print(f"pending after 1 ack: {group.pending()}")

# Output:
# worker-1 took 3 entries, worker-2 took 2 entries (no double delivery)
# group pending (unacked): 5
# pending after 1 ack: 4
```

This is exactly the semantics of a job queue, minus the work itself.

## 4. At-Least-Once Delivery

A worker can crash after processing but *before* acknowledging. The entry stays
unacked, so it will be redelivered to another worker. The guarantee is
**at-least-once**: every entry is processed at least once, some may be processed
twice. Exactly-once is not available — it must be *built* by making consumers
idempotent. An embedding job is naturally idempotent: the same document
produces the same chunk hash and the same vector, so re-embedding is harmless.
Any job that is *not* idempotent (sending an email, charging a card) must carry
a dedup key the consumer checks before acting.

## 5. Backpressure — What Happens When Consumers Are Slow

Pub/Sub has no backpressure: a slow consumer's in-memory queue grows until the
client process OOMs, and the producer never even knows. Streams make the
backlog **visible**: the group's pending count grows in Redis, and you can
monitor it, alert on it, and scale workers against it. Being able to *see* the
backlog is the difference between an outage and a graph going up.

## 6. Choosing the Primitive (AI Pipeline Map)

| Need | Primitive |
|---|---|
| Chat-room fan-out, config reload, eviction notices | Pub/Sub |
| Embed / chunk / index job queue | Streams + consumer groups |
| Audit log, event sourcing, replay | Streams |
| Anything that must not lose work on crash | Streams |

Rule of thumb: if losing a message is acceptable, pub/sub is cheaper; if losing
it is not, streams are the answer — and their cost is small.

## Common Mistakes to Avoid

### Mistake 1: Using pub/sub for jobs
```
# WRONG — the worker is down at publish time: work is lost forever
r.publish("queue:embed", job)

# CORRECT — streams (or lists) persist until a worker consumes them
```

### Mistake 2: Acknowledging before the side effect completes
```
# WRONG — crash after ack = work done 0 times (loss)
group.ack(...)          # then do the work

# CORRECT — process first, then ack (at-least-once)
```

### Mistake 3: Ignoring the pending backlog
```
# WRONG — the group pending counter grows until latency dies
# CORRECT — monitor pending; scale workers or alert when it grows
```

### Mistake 4: Assuming exactly-once delivery
```
# WRONG — a crash between work and ack redelivers the entry
# CORRECT — design every consumer to be idempotent
```

## Best Practices

1. Use pub/sub only for notifications; streams for work.
2. Process, then ack — never the reverse.
3. Make consumers idempotent; at-least-once demands it.
4. Monitor group pending counts; treat growth as an alert.
5. Keep stream entries small; put payloads in the DB, ids in the stream.
6. Use a bounded stream (`XTRIM`) for hot logs so disk stays bounded.
7. Name groups after their role (`embed-workers`), not their host.
8. Read with a consumer name per worker instance to see the partition map.
9. Use `XRANGE` for replay and audits; groups for live consumption.
10. Test crash behavior: kill a worker mid-job and verify the redelivery.

## Complexity and Cost

| Primitive | Publish cost | Delivery guarantee | Backlog visibility |
|---|---|---|---|
| Pub/Sub | O(subscribers) | at-most-once, live only | none — lost or buffered client-side |
| Stream + group | O(log n) append | at-least-once, durable | pending count in Redis |

Streams cost disk (entries persist) and a little latency per append; pub/sub
costs nothing to store because it stores nothing. For an ingestion pipeline the
durability is worth the extra bytes every time.

## AI Engineering Relevance

**Where this shows up:** the entire "ingest → embed → index" pipeline is a
producer/consumer problem, and it is the canonical modern use of Redis Streams.

| Concept here | Used for |
|---|---|
| Pub/Sub | notifying frontends that an indexing job finished |
| Streams | the embed/chunk/index job queue itself |
| Consumer groups | N workers partitioning 10k-document batches |
| Pending backlog | alerting when embedding falls behind ingestion |
| At-least-once + idempotent | re-embedding a chunk is harmless — dedupe by chunk hash |

**Scale note:** producer rates vary wildly in AI pipelines (a bulk import bursts
10k docs; a live system trickles). Streams absorb the burst into the pending
count while workers scale — the classic "buffer, don't drop" answer.

## Practice Exercises

### Exercise 1: Subscriber count (Difficulty: Easy)
Create two subscribers, publish once, and verify `PUBLISH` returns 2 and each
subscriber receives the message exactly once.

### Exercise 2: The missed-message problem (Difficulty: Easy)
Subscribe *after* a publish and show the late subscriber sees nothing — then
show the same data survives when written to a stream.

### Exercise 3: Group partitioning (Difficulty: Medium)
Add 5 entries, read with two workers, and verify the delivered ids are exactly
the 5 entries with no overlap.

### Exercise 4: Ack bookkeeping (Difficulty: Medium)
Verify pending goes 5 → 4 after one ack, and that replay from offset 0 returns
entry `1-0` — something pub/sub cannot do.

### Exercise 5: Crash redelivery (Difficulty: Hard)
Simulate a worker that reads but never acks; verify the pending count reflects
the unacked entry and a second read re-delivers it (at-least-once).

## Summary

| Concept | Description |
|---|---|
| Pub/Sub | live fan-out, no storage, no replay, at-most-once |
| Streams | durable append-only log, replayable |
| Consumer groups | each entry to exactly one worker |
| Ack / pending | visibility into how much work is outstanding |
| At-least-once | redelivery after crash → idempotent consumers |
| Backpressure | streams make the backlog visible; pub/sub cannot |

The choice is about guarantees, not speed. When work must survive a crash, pay
for streams; when a notification can be missed, pub/sub is the lighter tool.

## Quick Reference

| Task | Idiom |
|---|---|
| Publish | `PUBLISH channel msg` → subscriber count |
| Subscribe | `SUBSCRIBE channel`; read per-message |
| Append | `XADD stream {field: value}` → id |
| Read range | `XRANGE stream start end` |
| Group read | `XREADGROUP GROUP g consumer COUNT n` |
| Acknowledge | `XACK stream g id` |
| Backlog | group pending count |

## Next Steps

Next: **[Redis 06 — Distributed Locks](06-distributed-locks-lecture.md)** —
coordinating processes that must not run the same job twice.

Continues in: **[Phase 5 — Backend](../../06-phase-5-backend/01-fastapi-lecture.md)** —
background workers wired to real web endpoints.

Official docs: [redis.io/docs/latest/develop/data-types/streams/](https://redis.io/docs/latest/develop/data-types/streams/)
