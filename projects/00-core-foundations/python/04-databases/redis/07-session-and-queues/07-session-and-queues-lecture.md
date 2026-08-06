# Databases — 07: Redis Sessions and Queues

## Topic Overview

Long-running AI work — embedding 10k chunks, fine-tuning, batch evaluation —
must not block the API. You enqueue a job, return `202 Accepted`, and a worker
executes it asynchronously. Redis is the broker for this entire layer: sessions
ride hashes with TTLs, FIFO jobs ride lists, priority jobs ride sorted sets,
scheduled jobs ride timestamp-scored sorted sets, and reliability comes from
leases plus recovery.

This lecture is the stateful anatomy of a web service: how a login becomes a
session, a session becomes a job, a job becomes a queue, and a queue becomes
reliable.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Store a session as a hash with a TTL and slide the expiry on activity
2. Explain why a session without a TTL leaks memory forever
3. Implement a FIFO job queue with `RPUSH`/`LPOP` and O(1) ops
4. Implement a priority queue on a sorted set (low score = urgent)
5. Implement a delayed queue that promotes due jobs into the live queue
6. Explain the lease/heartbeat pattern for crash recovery
7. Explain why at-least-once delivery demands idempotent jobs
8. Compare list queues, sorted-set queues, and streams for job delivery

## Prerequisites

| Need | Where |
|---|---|
| Hashes, lists, sorted sets | [02-data-structures-lecture.md](02-data-structures-lecture.md) |
| TTL and invalidation | [03-caching-patterns-lecture.md](03-caching-patterns-lecture.md) |
| At-least-once and groups | [05-pubsub-and-streams-lecture.md](05-pubsub-and-streams-lecture.md) |

## 1. Sessions — Hash + TTL, Sliding Renewal

A session is a hash under one key with a TTL bounding idle time. Every
authenticated request *slides* the window: `EXPIRE` resets the countdown, so a
user active every 29 minutes stays logged in while one idle for 31 minutes is
dropped.

```python
from redis_client import RedisClient, ManualClock

clock = ManualClock(start=0.0)
r = RedisClient(clock=clock)

r.hset("session:abc123", {"user_id": "42", "role": "admin", "created": "0"})
r.expire("session:abc123", 1800)
clock.advance(1500)
r.expire("session:abc123", 1800)          # user active -> slide the window
print(f"ttl after activity at 1500s: {r.ttl('session:abc123')}s (slid back to 1800)")
clock.advance(1801)
print(f"idle > 30min -> session gone: {r.exists('session:abc123') == 0}")

# Output:
# ttl after activity at 1500s: 1800s (slid back to 1800)
# idle > 30min -> session gone: True
```

Sessions are the canonical "data that must die": without TTLs, every login ever
made lives in memory until the server restarts.

## 2. FIFO Job Queue — Lists

A producer `RPUSH`es jobs, workers `LPOP` them. That is the entire RQ broker:
a list plus result keys and TTLs. `LPUSH`+`RPOP` gives FIFO order with O(1) end
operations, and `LLEN` reports the backlog instantly.

```python
class FIFOQueue:
    def __init__(self, client, name):
        self._c, self._name = client, name

    def enqueue(self, job):
        self._c.rpush(self._name, repr(job))

    def dequeue(self):
        raw = self._c.lpop(self._name)
        return eval(raw) if raw is not None else None

q = FIFOQueue(r, "queue:embed")
q.enqueue({"doc": "a.pdf", "chunks": 12})
q.enqueue({"doc": "b.pdf", "chunks": 40})
print(f"first dequeued = {q.dequeue()['doc']} (oldest first)")

# Output:
# first dequeued = a.pdf (oldest first)
```

## 3. Priority Queue — Sorted Sets

A list has one order. When urgent work must jump the line, use a sorted set
scored by priority; workers take the **lowest** score first. To keep FIFO order
*within* a priority level, encode the sequence number into the score:
`priority * 1_000_000 + seq`.

```python
class PriorityQueue:
    def enqueue(self, job, priority):
        self._seq += 1
        score = float(priority * 1_000_000 + self._seq)
        self._c.zadd(self._name, {repr(job): score})

    def dequeue(self):
        hits = self._c.zrange(self._name, 0, 0, withscores=True)
        if not hits:
            return None
        raw, _ = hits[0]
        self._c.zrem(self._name, raw)
        return eval(raw)

pq = PriorityQueue(r, "queue:index")
pq.enqueue({"job": "reindex-all"}, priority=5)
pq.enqueue({"job": "index-new-doc"}, priority=1)
pq.enqueue({"job": "reindex-since-yesterday"}, priority=3)
print(f"first = {pq.dequeue()['job']} (highest urgency)")

# Output:
# first = index-new-doc (highest urgency)
```

This is how Celery implements priority: a sorted set, not special machinery.

## 4. Delayed and Scheduled Jobs

Scheduling is the same idea with a different score: a sorted set keyed by
"run at" timestamp. A sweeper promotes due jobs (score <= now) into the live
FIFO queue. Celery's ETA and RQ's scheduler work exactly this way.

```python
class DelayedQueue:
    def schedule(self, job, run_at):
        self._c.zadd(self._name, {repr(job): run_at})

    def promote_due(self, now):
        due = self._c.zrangebyscore(self._name, 0, now)
        for raw in due:
            self._fifo.enqueue(eval(raw))
        self._c.zrem(self._name, *due)
        return len(due)
```

## 5. Reliability — Lease, Heartbeat, Recovery

A naive `LPOP` loses the job if the worker crashes mid-execution. The fix is a
lease: the worker moves the job to an "in-progress" list and sets a lease key
with a TTL (its heartbeat). On completion it acks; if it dies, the lease
expires and a sweeper re-enqueues the job. The result is **at-least-once**
delivery — the same guarantee streams give (lecture 05) — which means every
job must be idempotent.

```python
class ReliableWorker:
    def take(self):
        job = self._fifo.dequeue()
        if job is not None:
            self._c.rpush("in-progress", repr(job))
            self._c.set("lease:in-progress", str(self._c._clock()), ex=self._lease)
        return job

    def recover_stale(self):
        if self._c.get("lease:in-progress") is not None:
            return 0                                  # lease alive
        entries = self._c.lrange("in-progress", 0, -1)
        if not entries:
            return 0
        self._c.delete("in-progress")
        for e in entries:
            self._fifo.enqueue(eval(e))
        return len(entries)
```

## Common Mistakes to Avoid

### Mistake 1: Sessions without TTL
```
# WRONG — memory grows forever with dead sessions
r.hset("session:abc", {"user": "1"})

# CORRECT — EXPIRE on create, slide on activity
```

### Mistake 2: One list for all jobs
```
# WRONG — a flood of low-priority work starves urgent jobs
# CORRECT — priority via sorted sets (or separate queues + weights)
```

### Mistake 3: LPOP then crash
```
# WRONG — the popped job vanishes with the worker
job = r.lpop("queue")

# CORRECT — lease + recovery, or streams consumer groups
```

### Mistake 4: Full payloads in the queue
```
# WRONG — metadata changes require re-enqueueing; payloads bloat keys
r.rpush("queue", json.dumps(full_doc))

# CORRECT — enqueue job ids; workers read the payload from the DB
```

## Best Practices

1. Every session key carries a TTL; slide it on activity, never lazily.
2. FIFO lists for the default path; sorted sets for priority/scheduling.
3. Enqueue ids, not payloads — the queue is a pointer, not a store.
4. Lease every in-flight job; recover expired leases promptly.
5. Make jobs idempotent — at-least-once means duplicates happen.
6. Keep result keys with TTLs (a result nobody reads is garbage).
7. Monitor queue depth and recovery count; both are alert-worthy.
8. Use `LLEN`/`ZCARD` as cheap backlog probes before scaling workers.
9. Name queues by role (`queue:embed`, `queue:index`), not by host.
10. Prefer streams when you need replay or audit history (lecture 05).

## Complexity and Cost

| Structure | Enqueue | Dequeue | Notes |
|---|---|---|---|
| List FIFO | O(1) `RPUSH` | O(1) `LPOP` | one order, no priority |
| Sorted-set priority | O(log n) | O(log n) | priority + FIFO tie-break |
| Delayed (zset by time) | O(log n) | sweeper O(k) | promote due entries |
| Lease recovery | O(1) + TTL | O(n) scan | at-least-once guarantee |

All are cheap; the real cost is design: which queue, which score, which lease
duration. A lease shorter than the job's worst case causes spurious recovery; a
longer one delays recovery of genuinely crashed work.

## AI Engineering Relevance

**Where this shows up:** every asynchronous AI workload is a queue consumer —
embedding, chunking, indexing, evaluation, fine-tuning.

| Concept here | Used for |
|---|---|
| FIFO queue | embedding batches in order |
| Priority queue | urgent index updates ahead of bulk imports |
| Delayed queue | scheduled nightly re-embedding sweeps |
| Lease + recovery | a crashed embedder's jobs return to the queue |
| Session hashes | chat session state with idle timeout |

**Scale note:** an indexing job for a 10k-document corpus is *hours* of work —
enqueue it, return 202, and let workers chew. The queue decouples API latency
from job duration, and the lease decouples job completion from worker
lifetime.

## Practice Exercises

### Exercise 1: Session slide (Difficulty: Easy)
Create a session with TTL 30, advance 20 seconds, renew, and verify the TTL is
back to 30; then verify idle expiry after 31 seconds.

### Exercise 2: FIFO order (Difficulty: Easy)
Enqueue three jobs and verify they dequeue in enqueue order, with size
decreasing from 3.

### Exercise 3: Priority with FIFO tie-break (Difficulty: Medium)
Enqueue priority-9, priority-1, priority-9 jobs; verify the priority-1 job
comes first and the two priority-9 jobs come in enqueue order.

### Exercise 4: Delayed promotion (Difficulty: Medium)
Schedule jobs at t=30 and t=60; advance to t=45 and verify only the t=30 job
promotes into the live queue.

### Exercise 5: Crash recovery (Difficulty: Hard)
Take a job, advance past the lease, and verify recovery re-enqueues it; then
take, ack, and verify recovery stays idle (acked work is never re-run).

## Summary

| Concept | Description |
|---|---|
| Sessions | hash + TTL, slide on activity |
| FIFO queue | `RPUSH`/`LPOP` lists, O(1) |
| Priority queue | sorted set, low score first, seq tie-break |
| Delayed queue | zset by run-at; sweeper promotes due jobs |
| Lease + recovery | heartbeat TTL; crashed jobs re-enqueue |
| Idempotency | the price of at-least-once |

Sessions and queues are where Redis earns its keep in a web service: state with
a lifetime, work with an order, and failures that heal themselves.

## Quick Reference

| Task | Idiom |
|---|---|
| Create session | `HSET session:<id> fields` + `EXPIRE 1800` |
| Slide session | `EXPIRE session:<id> 1800` |
| FIFO enqueue / dequeue | `RPUSH queue job` / `LPOP queue` |
| Priority enqueue | `ZADD queue score*1e6+seq job` |
| Take lowest | `ZRANGE queue 0 0` + `ZREM` |
| Schedule | `ZADD sched run_at job`; sweep `ZRANGEBYSCORE 0 now` |
| Lease | `SET lease:<q> now EX <ttl>`; recover when absent |

## Next Steps

Next: **[Redis 08 — Persistence and Operations](08-persistence-and-ops-lecture.md)** —
what survives a restart, what dies at maxmemory, and how to operate it.

Continues in: **[Phase 5 — Backend](../../06-phase-5-backend/01-fastapi-lecture.md)** —
real background workers behind a web API.

Official docs: [python-rq.org](https://python-rq.org/)
