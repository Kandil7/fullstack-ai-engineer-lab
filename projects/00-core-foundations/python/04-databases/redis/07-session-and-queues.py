"""
Redis — 07: Sessions and Queues
==============================================
Topics: session storage, job queues (list-based), priority queues via
        sorted sets, RQ/Celery broker patterns

Why this matters for AI/backend engineering:
    Long-running AI work (embedding 10k chunks, fine-tuning, batch
    evaluation) must not block the API. You enqueue a job, return 202,
    and a worker executes it. Redis is the broker: sessions ride hashes
    with TTL, FIFO jobs ride lists, priority jobs ride sorted sets.

Run:      python 07-session-and-queues.py
Verify:   python 07-session-and-queues.py --verify
Reference: https://python-rq.org/
"""

from __future__ import annotations

import sys

from redis_client import ManualClock, RedisClient, get_client

# ============================================================
# 1. Sessions — hash per session, TTL, sliding renewal
# ============================================================
# Key: session:<id> (hash), TTL bounds idle time. Renew on activity:
# EXPIRE resets the clock. Sliding sessions: 30 min idle -> logout.

clock = ManualClock(start=0.0)
r: RedisClient = RedisClient(clock=clock)

r.hset("session:abc123", {"user_id": "42", "role": "admin", "created": "0"})
r.expire("session:abc123", 1800)
print(f"session created, ttl={r.ttl('session:abc123')}s")

# Output:
# session created, ttl=1800s

clock.advance(1500)
r.expire("session:abc123", 1800)          # user active -> slide the window
print(f"ttl after activity at 1500s: {r.ttl('session:abc123')}s (slid back to 1800)")

# Output:
# ttl after activity at 1500s: 1800s (slid back to 1800)

clock.advance(1801)
print(f"idle > 30min -> session gone: {r.exists('session:abc123') == 0}")

# Output:
# idle > 30min -> session gone: True

# ============================================================
# 2. FIFO Job Queue — lists
# ============================================================
# Producer RPUSHes jobs; workers LPOP them. That is the whole RQ broker:
# RQ = "simple" queue on lists (plus result keys and TTLs).

class FIFOQueue:
    def __init__(self, client: RedisClient, name: str) -> None:
        self._c = client
        self._name = name

    def enqueue(self, job: dict) -> None:
        self._c.rpush(self._name, repr(job))

    def dequeue(self) -> dict | None:
        raw = self._c.lpop(self._name)
        return eval(raw) if raw is not None else None

    def size(self) -> int:
        return self._c.llen(self._name)


q = FIFOQueue(r, "queue:embed")
q.enqueue({"doc": "a.pdf", "chunks": 12})
q.enqueue({"doc": "b.pdf", "chunks": 40})
q.enqueue({"doc": "c.pdf", "chunks": 7})
job = q.dequeue()
print(f"\nFIFO: first dequeued = {job['doc']} (oldest first)")
print(f"remaining: {q.size()}")

# Output:
# FIFO: first dequeued = a.pdf (oldest first)
# remaining: 2

# ============================================================
# 3. Priority Queue — sorted sets
# ============================================================
# ZADD job with priority as the score; workers ZRANGEBYSCORE... take the
# LOWEST score (most urgent). Celery's priority queues work this way.
# Tie-break by enqueue sequence so FIFO holds within a priority level.

class PriorityQueue:
    def __init__(self, client: RedisClient, name: str) -> None:
        self._c = client
        self._name = name
        self._seq = 0

    def enqueue(self, job: dict, priority: int) -> None:
        self._seq += 1
        # score = priority * 1e6 + seq -> lower priority number first,
        # and within one priority, earlier enqueue first
        score = float(priority * 1_000_000 + self._seq)
        self._c.zadd(self._name, {repr(job): score})

    def dequeue(self) -> dict | None:
        hits = self._c.zrange(self._name, 0, 0, withscores=True)
        if not hits:
            return None
        raw, _score = hits[0]
        self._c.zrem(self._name, raw)
        return eval(raw)

    def size(self) -> int:
        return self._c.zcard(self._name)


pq = PriorityQueue(r, "queue:index")
pq.enqueue({"job": "reindex-all"}, priority=5)     # low priority
pq.enqueue({"job": "index-new-doc"}, priority=1)   # high priority
pq.enqueue({"job": "reindex-since-yesterday"}, priority=3)
print(f"\npriority queue: first = {pq.dequeue()['job']} (highest urgency)")
print(f"priority queue: second = {pq.dequeue()['job']}")

# Output:
# priority queue: first = index-new-doc (highest urgency)
# priority queue: second = reindex-since-yesterday

# ============================================================
# 4. Delayed / Scheduled Jobs
# ============================================================
# Schedule = sorted set keyed by "run at" timestamp; a sweeper promotes
# due jobs into the live queue. (Celery ETA; RQ scheduler.)
# NOTE: fresh client + clock so scheduled times are relative to t=0.

class DelayedQueue:
    def __init__(self, client: RedisClient, fifo: FIFOQueue,
                 schedule_name: str) -> None:
        self._c = client
        self._fifo = fifo
        self._name = schedule_name

    def schedule(self, job: dict, run_at: float) -> None:
        self._c.zadd(self._name, {repr(job): run_at})

    def promote_due(self, now: float) -> int:
        due = self._c.zrangebyscore(self._name, 0, now)
        for raw in due:
            self._fifo.enqueue(eval(raw))
        self._c.zrem(self._name, *due)
        return len(due)


qclock = ManualClock(start=0.0)
qc: RedisClient = RedisClient(clock=qclock)
q2 = FIFOQueue(qc, "queue:embed:workers")
dq = DelayedQueue(qc, q2, "queue:scheduled")
dq.schedule({"doc": "z.pdf"}, run_at=60.0)
dq.schedule({"doc": "y.pdf"}, run_at=30.0)
qclock.advance(45)
promoted = dq.promote_due(qclock())
print(f"\nscheduled: promoted {promoted} job(s) at t=45 (y due, z not yet)")
print(f"fifo now has {q2.size()} job(s)")

# Output:
# scheduled: promoted 1 job(s) at t=45 (y due, z not yet)
# fifo now has 1 job(s)

# ============================================================
# 5. Worker Loop with Heartbeat / Lease
# ============================================================
# A worker pops a job, pushes it to "in-progress", and sets a lease key
# with a TTL (the heartbeat). On completion it acks. If the worker dies,
# the lease expires and a sweeper re-enqueues the job — at-least-once,
# the same guarantee Streams give (topic 05).

class ReliableWorker:
    def __init__(self, client: RedisClient, fifo: FIFOQueue,
                 lease_s: float = 60) -> None:
        self._c = client
        self._fifo = fifo
        self._lease = lease_s

    def take(self) -> dict | None:
        job = self._fifo.dequeue()
        if job is not None:
            self._c.rpush("in-progress", repr(job))
            self._c.set("lease:in-progress", str(self._c._clock()),
                        ex=self._lease)   # heartbeat with TTL
        return job

    def ack(self, job: dict) -> None:
        entries = self._c.lrange("in-progress", 0, -1)
        remaining = [e for e in entries if eval(e) != job]
        self._c.delete("in-progress")
        for e in remaining:
            self._c.rpush("in-progress", e)
        if not remaining:
            self._c.delete("lease:in-progress")

    def recover_stale(self) -> int:
        """Re-enqueue jobs whose lease expired (worker crashed)."""
        if self._c.get("lease:in-progress") is not None:
            return 0                                  # lease alive
        entries = self._c.lrange("in-progress", 0, -1)
        if not entries:
            return 0
        self._c.delete("in-progress")
        for e in entries:
            self._fifo.enqueue(eval(e))
        return len(entries)


worker = ReliableWorker(qc, q2, lease_s=60)
taken = worker.take()
print(f"\nworker took: {taken['doc']}")
qclock.advance(61)                       # worker dies before acking
recovered = worker.recover_stale()
print(f"worker crashed -> {recovered} job(s) recovered to queue")

# Output:
# worker took: y.pdf
# worker crashed -> 1 job(s) recovered to queue

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: sessions without TTL -> memory grows forever with dead sessions.
# CORRECT: EXPIRE on create, slide on activity.
#
# MISTAKE: one list for all jobs -> a flood of low-priority work starves
#   urgent jobs.
# CORRECT: priority via sorted sets (or separate queues + weights).
#
# MISTAKE: LPOP then crash -> job lost.
# CORRECT: lease/TTL + recovery, or Streams consumer groups (topic 05).
#
# MISTAKE: storing full payloads in queue keys; metadata changes need
#   re-enqueue.
# CORRECT: enqueue job ids; workers read the payload from the DB.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # sliding session: activity resets the idle window
    assert r.exists("session:abc123") == 0, \
        "Session must expire after 30+ idle minutes"

    # FIFO order preserved
    vc = RedisClient(clock=ManualClock(0.0))
    fq = FIFOQueue(vc, "q")
    fq.enqueue({"n": 1})
    fq.enqueue({"n": 2})
    assert fq.dequeue() == {"n": 1} and fq.dequeue() == {"n": 2}, \
        "FIFO must deliver in enqueue order"

    # priority: low score first, FIFO within priority
    vp = PriorityQueue(vc, "qp")
    vp.enqueue({"n": "low"}, priority=9)
    vp.enqueue({"n": "high"}, priority=1)
    vp.enqueue({"n": "low2"}, priority=9)
    assert vp.dequeue() == {"n": "high"}, "priority 1 must beat priority 9"
    assert vp.dequeue() == {"n": "low"}, "FIFO within priority 9"
    assert vp.dequeue() == {"n": "low2"}, "second priority-9 job"

    # delayed queue promotes only due jobs
    dclock = ManualClock(start=0.0)
    dc: RedisClient = RedisClient(clock=dclock)
    df = FIFOQueue(dc, "dq")
    dd = DelayedQueue(dc, df, "sched")
    dd.schedule({"n": "later"}, run_at=100.0)
    dd.schedule({"n": "now"}, run_at=10.0)
    dclock.advance(50)
    assert dd.promote_due(dclock()) == 1, "only the due job promotes"
    assert df.size() == 1, "one job now in the live queue"

    # reliable worker: crashed job is recovered after the lease
    assert taken == {"doc": "y.pdf"}, "worker took the promoted FIFO job"
    assert recovered == 1, "expired lease must return the job to the queue"

    # acking a job clears the lease so recovery stays idle
    w2 = ReliableWorker(qc, q2, lease_s=60)
    taken2 = w2.take()
    w2.ack(taken2)
    assert w2.recover_stale() == 0, "acked work must not be recovered"

    # session slide: EXPIRE on activity resets TTL
    sc = RedisClient(clock=ManualClock(0.0))
    sc.hset("s:1", {"u": "1"})
    sc.expire("s:1", 30)
    sc._clock.advance(20)
    sc.expire("s:1", 30)
    assert sc.ttl("s:1") == 30, "renewal must slide the expiry window"

    print("[OK] 07-session-and-queues: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Sessions: hash + TTL, slide on activity")
        print("2. FIFO jobs: RPUSH/LPOP lists")
        print("3. Priority jobs: sorted sets, low score first")
        print("4. Reliability: lease + recovery = at-least-once")
        _verify()  # always runs, so plain execution is also a test
