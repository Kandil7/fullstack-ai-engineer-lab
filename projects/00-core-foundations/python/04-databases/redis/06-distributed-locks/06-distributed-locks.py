"""
Redis — 06: Distributed Locks
==============================================
Topics: SET NX PX, lock expiry, fencing tokens, Redlock and its critics,
        when you actually need a distributed lock

Why this matters for AI/backend engineering:
    Two API servers must not both run the same fine-tuning job, refresh
    the same embedding index, or re-serve the same expensive cache
    recompute. A lock held in Redis coordinates processes that share
    nothing else. Getting expiry and ownership right is the difference
    between a harmless guard and a silent correctness bug.

Run:      python 06-distributed-locks.py
Verify:   python 06-distributed-locks.py --verify
Reference: https://redis.io/docs/latest/develop/use/patterns/distributed-locks/
"""

from __future__ import annotations

import sys
import time as _time

from redis_client import ManualClock, RedisClient, get_client

# ============================================================
# 1. The Lock — SET NX PX
# ============================================================
# NX: only set if the key does not exist (acquire).
# PX: expiry in ms (auto-release on crash).
# The acquire+expiry MUST be one atomic command; SETNX followed by a
# separate EXPIRE would leak a permanent lock if the process died between
# the two calls.

def acquire(lock_name: str, token: str, ttl_s: float, client: RedisClient) -> bool:
    """SET lock NX PX in one shot; token proves ownership."""
    return client.set(f"lock:{lock_name}", token, nx=True, ex=ttl_s)


def release(lock_name: str, token: str, client: RedisClient) -> bool:
    """Releases only if WE own the lock (compare-and-delete)."""
    if client.get(f"lock:{lock_name}") == token:
        client.delete(f"lock:{lock_name}")
        return True
    return False  # lock expired or another holder — do NOT delete


clock = ManualClock(start=0.0)
lc: RedisClient = RedisClient(clock=clock)

acquired_1 = acquire("job:embed", "worker-a", 30, lc)
acquired_2 = acquire("job:embed", "worker-b", 30, lc)
print(f"worker-a acquired: {acquired_1}")
print(f"worker-b acquired: {acquired_2} (NX rejects second holder)")

# Output:
# worker-a acquired: True
# worker-b acquired: False (NX rejects second holder)

# ============================================================
# 2. Lock Expiry — the crash case
# ============================================================
# worker-a dies mid-job; the lock expires and worker-b takes over.
# Without expiry, the job would be stuck forever.

clock.advance(31)   # lock TTL (30s) elapses
print(f"after expiry, lock exists? {lc.exists('lock:job:embed')}")

# Output:
# after expiry, lock exists? 0

acquired_3 = acquire("job:embed", "worker-b", 30, lc)
print(f"worker-b acquires after crash-timeout: {acquired_3}")

# Output:
# worker-b acquires after crash-timeout: True

# ============================================================
# 3. Safe Release — token ownership
# ============================================================
# Never release with DEL alone: worker-a's late release must not delete
# worker-b's lock. Compare token first (real Redis: Lua script).

print(f"worker-a stale release: {release('job:embed', 'worker-a', lc)} (must be False)")
print(f"worker-b own release:   {release('job:embed', 'worker-b', lc)} (must be True)")

# Output:
# worker-a stale release: False (must be False)
# worker-b own release:   True (must be True)

# ============================================================
# 4. Fencing Tokens — the expiry trap
# ============================================================
# Danger: worker-a's lock expires at 30s, but worker-a is only paused
# (GC pause / slow network), not dead. At t=35 worker-a RESUMES and
# writes — while worker-b (holding the lock since t=31) is also writing.
# Two writers again!
#
# Fix: fencing token. The lock grants a monotonically increasing token;
# the resource (DB) rejects any write whose token is older than the last
# accepted one. Locks alone cannot fix paused-process races.

def next_token() -> int:
    next_token._n = getattr(next_token, "_n", 0) + 1
    return next_token._n


lock = {"holder": None, "token": None}
fenced_db = {"last_token": 0}


def fenced_write(data: str, token: int, db: dict) -> bool:
    if token <= db["last_token"]:
        return False  # stale or replayed writer — reject
    db["last_token"] = token
    db["data"] = data
    return True


tok_a = next_token()
lock.update({"holder": "a", "token": tok_a})
fenced_write("a: result", tok_a, fenced_db)     # a writes with token 1

lock.update({"holder": "b", "token": next_token()})
fenced_write("b: result", lock["token"], fenced_db)

# a resumes late and tries to write with its OLD token
stale_write = fenced_write("a: stale overwrite", tok_a, fenced_db)
print(f"\nstale writer (token {tok_a}) accepted? {stale_write}")
print(f"db data: {fenced_db['data']}")

# Output:
# stale writer (token 1) accepted? False
# db data: b: result

# ============================================================
# 5. Redlock and Its Critics
# ============================================================
# Redlock: acquire the lock on N/2+1 independent Redis nodes; release on
# all. It tolerates node crashes. Critics (Martin Kleppmann) show a
# paused process can still violate mutual exclusion even under Redlock,
# because the pause can exceed ALL lock TTLs. Consensus:
#   - For most systems: a single Redis lock + fencing tokens + short TTL
#     is sufficient and much simpler.
#   - Redlock only helps when you truly need safety across independent
#     node failures AND can afford the complexity.

# ============================================================
# 6. When You Actually Need One
# ============================================================
# NEED: multi-process jobs that must run once (index rebuild, migration),
#       cache stampede single-flight, distributed leader election.
# DON'T NEED: single-process concurrency (use threading.Lock),
#       serialized writes in a single DB (use DB transactions).

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: SETNX then EXPIRE in two calls -> permanent lock on crash.
# CORRECT: atomic SET NX PX.
#
# MISTAKE: DEL to release -> deleting someone else's lock.
# CORRECT: compare token, delete only if owned.
#
# MISTAKE: no fencing token -> paused holder resumes and double-writes.
# CORRECT: monotonic tokens checked at the resource.
#
# MISTAKE: defaulting to Redlock for a simple cache stampede.
# CORRECT: one Redis lock + TTL + jitter is usually enough.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # NX mutual exclusion: two holders cannot both acquire
    vc = RedisClient(clock=ManualClock(0.0))
    assert acquire("l:1", "a", 10, vc) is True, "first acquire succeeds"
    assert acquire("l:1", "b", 10, vc) is False, "second acquire fails (NX)"

    # expiry frees the lock automatically
    assert vc.ttl("lock:l:1") == 10, "SET NX PX must attach the TTL immediately"

    # stale release must not delete a lock held by someone else
    assert release("l:1", "a", vc) is True, "owner releases its own lock"
    assert acquire("l:1", "b", 10, vc) is True, "lock reusable after release"
    assert release("l:1", "ghost", vc) is False, \
        "non-owner release must be rejected"

    # fencing: stale tokens are rejected by the resource
    fresh_db = {"last_token": 0}
    t1 = next_token()
    assert fenced_write("first", t1, fresh_db) is True, "first write accepted"
    assert fenced_write("stale", t1, fresh_db) is False, \
        "replayed token must be rejected"
    assert fenced_write("new", next_token(), fresh_db) is True, \
        "newer token accepted"

    # crash timeout: lock becomes acquirable after TTL
    ck = ManualClock(start=50.0)
    cc: RedisClient = RedisClient(clock=ck)
    acquire("l:2", "a", 5, cc)
    ck.advance(6)
    assert acquire("l:2", "b", 5, cc) is True, \
        "expired lock must be acquirable by a new holder"

    print("[OK] 06-distributed-locks: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. SET NX PX = atomic acquire with crash-safe expiry")
        print("2. Token ownership prevents deleting others' locks")
        print("3. Fencing tokens stop paused writers from double-writing")
        print("4. Single Redis + TTL + tokens beats Redlock for most systems")
        _verify()  # always runs, so plain execution is also a test
