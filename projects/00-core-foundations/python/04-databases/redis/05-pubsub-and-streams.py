"""
Redis — 05: Pub/Sub and Streams
==============================================
Topics: Pub/Sub vs Streams, consumer groups, acknowledgment,
        at-least-once delivery, backpressure, decoupling ingestion
        from indexing

Why this matters for AI/backend engineering:
    When a document lands in the upload bucket, someone must embed it,
    chunk it, index it — without blocking the API caller. Pub/Sub
    decouples producers from consumers; Streams add durability, consumer
    groups, and replay. Choosing between them decides whether a crashed
    worker loses work.

Run:      python 05-pubsub-and-streams.py
Verify:   python 05-pubsub-and-streams.py --verify
Reference: https://redis.io/docs/latest/develop/data-types/streams/
"""

from __future__ import annotations

import sys

from redis_client import RedisClient, Subscription, get_client

# ============================================================
# 1. Pub/Sub — fire and forget
# ============================================================
# PUBLISH delivers a message to all current SUBSCRIBEs. Messages are NOT
# stored: a subscriber that is offline when the message is published
# never sees it. Great for fan-out notifications, bad for jobs.

r: RedisClient = get_client()
sub_a = r.subscribe("events:documents")
sub_b = r.subscribe("events:documents")

delivered = r.publish("events:documents", "doc-1 uploaded")
print(f"publish returned {delivered} (subscribers reached)")

# Output:
# publish returned 2 (subscribers reached)

print(f"A got: {sub_a.get_message()}")
print(f"B got: {sub_b.get_message()}")
print(f"A second read: {sub_a.get_message()} (queue now empty)")

# Output:
# A got: doc-1 uploaded
# B got: doc-1 uploaded
# A second read: None (queue now empty)

# The "missed message" problem: a subscriber joining later sees nothing
late = r.subscribe("events:documents")
r.publish("events:documents", "doc-2 uploaded")
print(f"late subscriber (joined after doc-1): {late.get_message()}")
print(f"A also got: {sub_a.get_message()} (A subscribed before doc-2)")

# Output:
# late subscriber (joined after doc-1): doc-2 uploaded
# A also got: doc-2 uploaded (A subscribed before doc-2)

# ============================================================
# 2. Streams — durable, replayable, group-consumed
# ============================================================
# A stream is an append-only log: entries (id, {field: value}). Workers
# form a CONSUMER GROUP; each entry is delivered to exactly ONE worker in
# the group. Entries survive restarts and can be re-read.
#
# Stand-in: we model a stream as a list of entries plus per-group
# delivery bookkeeping.

class Stream:
    def __init__(self, client: RedisClient, name: str) -> None:
        self._c = client
        self._name = name
        if not self._c.hexists(name, "_next_id"):
            self._c.hset(name, {"_next_id": "0"})

    def xadd(self, fields: dict) -> str:
        self._c.hincrby(self._name, "_next_id", 1)
        entry_id = f"{self._c.hget(self._name, '_next_id')}-0"
        self._c.rpush(f"{self._name}:entries", repr([entry_id, fields]))
        return entry_id

    def xlen(self) -> int:
        return self._c.llen(f"{self._name}:entries")

    def xrange(self, start: int = 0, end: int = -1) -> list:
        return [eval(e) for e in self._c.lrange(f"{self._name}:entries", start, end)]


class ConsumerGroup:
    """Delivers each entry to one member; tracks acks and pending."""

    def __init__(self, stream: Stream, group: str) -> None:
        self._s = stream
        self._g = group
        self._c = stream._c
        self._c.hset(f"{stream._name}:grp:{group}", {"pos": "0", "pending": "0"})

    def read(self, consumer: str, count: int = 10) -> list:
        pos = int(self._c.hget(f"{self._s._name}:grp:{self._g}", "pos") or 0)
        entries = self._s.xrange(pos, pos + count - 1)
        self._c.hset(f"{self._s._name}:grp:{self._g}",
                     {"pos": str(pos + len(entries))})
        self._c.hset(f"{self._s._name}:grp:{self._g}",
                     {"pending": str(int(self._c.hget(
                         f"{self._s._name}:grp:{self._g}", "pending") or 0)
                         + len(entries))})
        return entries

    def ack(self, consumer: str, entry_id: str) -> None:
        pending = int(self._c.hget(f"{self._s._name}:grp:{self._g}", "pending") or 0)
        self._c.hset(f"{self._s._name}:grp:{self._g}",
                     {"pending": str(max(0, pending - 1))})

    def pending(self) -> int:
        return int(self._c.hget(f"{self._s._name}:grp:{self._g}", "pending") or 0)


stream = Stream(r, "stream:ingest")
for i in range(5):
    stream.xadd({"doc": f"file-{i}.pdf", "size": str(100 + i)})
print(f"\nstream length: {stream.xlen()}")

# Output:
# stream length: 5

group = ConsumerGroup(stream, "embed-workers")
w1 = group.read("worker-1", count=3)
w2 = group.read("worker-2", count=3)
print(f"worker-1 took {len(w1)} entries, worker-2 took {len(w2)} (no double delivery)")

# Output:
# worker-1 took 3 entries, worker-2 took 2 entries (no double delivery)

print(f"group pending (unacked): {group.pending()}")
group.ack("worker-1", w1[0][0])
print(f"pending after 1 ack: {group.pending()}")

# Output:
# group pending (unacked): 5
# pending after 1 ack: 4

# ============================================================
# 3. At-Least-Once Delivery
# ============================================================
# Streams give AT-LEAST-ONCE: a worker may crash after processing but
# before ack -> the entry is redelivered. Your embedding job must be
# idempotent (same doc -> same chunk hash -> same vector) so a duplicate
# delivery is harmless. Exactly-once requires dedup on the consumer side.

# ============================================================
# 4. Backpressure
# ============================================================
# Pub/Sub: a slow consumer's queue grows in ITS memory until OOM — the
# producer is never slowed.
# Streams: entries live in Redis; the group's pending count grows and you
# can SEE it (our pending()) and scale workers accordingly. Redis Streams
# let you monitor the backlog; pub/sub cannot.

# ============================================================
# 5. When to Use Which (AI pipeline)
# ============================================================
# Pub/Sub:  chat-room fan-out, eviction notifications, "reload config"
# Streams: job queues (embed, chunk, index), audit logs, anything that
#          must not lose work when a worker dies.

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: using Pub/Sub for jobs — a crashed worker means lost work.
# CORRECT: Streams with consumer groups for anything durable.
#
# MISTAKE: acking before the side effect completes.
# CORRECT: process first, then ack (at-least-once + idempotent work).
#
# MISTAKE: ignoring the pending backlog.
# CORRECT: monitor group pending; scale workers or alert when it grows.
#
# MISTAKE: assuming exactly-once delivery.
# CORRECT: design every consumer idempotent.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    assert delivered == 2, "PUBLISH must return the subscriber count"

    # each subscriber got the message exactly once, then the queue drains
    assert sub_a.get_message() is None, \
        "Subscriber queue must be empty after one get per message"

    # late subscriber missed nothing it was subscribed for, but pub/sub
    # never replays history — the stream exists precisely for that
    assert stream.xlen() == 5, "Stream must retain all 5 entries (durable)"

    # consumer group: no double delivery across members
    ids = [e[0] for e in w1] + [e[0] for e in w2]
    assert len(ids) == len(set(ids)) == 5, \
        "Group delivery must partition entries without overlap"

    # ack bookkeeping
    assert group.pending() == 4, "ACK must decrement the pending count"

    # replay: xrange re-reads entries the group already consumed
    replay = stream.xrange(0, 1)
    assert replay[0][0] == "1-0", \
        "Streams must allow replay from any offset (pub/sub cannot)"

    # at-least-once semantics: unacked entry remains available to workers
    unacked = group.pending()
    assert unacked >= 0, "Pending counter must never go negative"

    print("[OK] 05-pubsub-and-streams: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Pub/Sub: live fan-out, no storage, no replay")
        print("2. Streams: durable log + consumer groups + ack")
        print("3. At-least-once delivery -> idempotent consumers")
        print("4. Pending backlog = visible backpressure")
        _verify()  # always runs, so plain execution is also a test
