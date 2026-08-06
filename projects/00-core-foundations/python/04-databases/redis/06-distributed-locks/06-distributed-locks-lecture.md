# Databases — 06: Redis Distributed Locks

## Topic Overview

Two API servers must not both run the same fine-tuning job, refresh the same
embedding index, or recompute the same expensive cache entry. A distributed
lock — held in Redis, observed by every process — is the coordination point for
processes that share nothing else.

The correctness surface is small and sharp: acquire must be atomic with an
expiry (`SET NX PX`), release must prove ownership (compare-and-delete), and
even then a *paused* holder can violate mutual exclusion — which is what
fencing tokens exist to fix. This lecture builds the lock, then the traps, then
the honest question: when do you actually need one at all?

## Learning Objectives

By the end of this lecture, you will be able to:

1. Acquire a lock with `SET NX PX` in one atomic command
2. Explain why `SETNX` followed by a separate `EXPIRE` is a bug
3. Release safely with a token: never delete a lock you do not own
4. Explain the lock-expiry/crash cycle and its TTL math
5. Describe the paused-holder race and why locks alone cannot fix it
6. Implement a fencing-token check at the resource
7. Summarize Redlock and its critics (Kleppmann) and the consensus
8. Decide when a distributed lock is needed and when it is not

## Prerequisites

| Need | Where |
|---|---|
| `SET NX` single-flight | [03-caching-patterns-lecture.md](03-caching-patterns-lecture.md) |
| Atomicity via Lua | [04-rate-limiting-lecture.md](04-rate-limiting-lecture.md) |
| Distributed systems failures | [03-distributed-systems-lecture.md](../../03-systems/03-distributed-systems-lecture.md) |

## 1. The Lock — SET NX PX

`NX` means "only set if the key does not exist" — that is the acquire. `PX` is
the expiry in milliseconds — the crash safety. Both must arrive in **one**
command: `SET lock name NX PX`. If acquire and expiry are separate round trips,
a process that dies between them leaves a permanent lock.

```python
from redis_client import RedisClient, ManualClock

def acquire(lock_name, token, ttl_s, client):
    """SET lock NX PX in one shot; token proves ownership."""
    return client.set(f"lock:{lock_name}", token, nx=True, ex=ttl_s)

clock = ManualClock(start=0.0)
lc = RedisClient(clock=clock)
print(f"worker-a acquired: {acquire('job:embed', 'worker-a', 30, lc)}")
print(f"worker-b acquired: {acquire('job:embed', 'worker-b', 30, lc)} (NX rejects second holder)")

# Output:
# worker-a acquired: True
# worker-b acquired: False (NX rejects second holder)
```

## 2. Expiry — the Crash Case

If the holder crashes mid-job, nothing releases the lock — except the TTL. When
the expiry elapses, the key disappears and another worker can acquire. The TTL
is a promise: *no job may run longer than the lock TTL without renewing*.

```python
clock.advance(31)   # lock TTL (30s) elapses
print(f"after expiry, lock exists? {lc.exists('lock:job:embed')}")
print(f"worker-b acquires after crash-timeout: {acquire('job:embed', 'worker-b', 30, lc)}")

# Output:
# after expiry, lock exists? 0
# worker-b acquires after crash-timeout: True
```

## 3. Safe Release — Token Ownership

Releasing with plain `DEL` is the classic bug: worker-a's lock expired,
worker-b acquired, and worker-a's delayed cleanup deletes *worker-b's* lock.
The fix is to store a random token in the lock value and delete only if the
value still matches — compare-and-delete (a Lua script in real Redis).

```python
def release(lock_name, token, client):
    if client.get(f"lock:{lock_name}") == token:
        client.delete(f"lock:{lock_name}")
        return True
    return False  # lock expired or another holder — do NOT delete
```

A stale release must return `False`, never delete.

## 4. The Fencing-Token Trap

Expiry handles *dead* holders. It cannot handle **paused** ones. Worker-a's
lock expires at t=30 during a GC pause; worker-b acquires at t=31 and starts
writing; at t=35 worker-a resumes and writes too — two writers, despite a
"correct" lock.

The fix lives at the resource, not the lock: the lock grants a monotonically
increasing fencing token, and the database rejects any write whose token is
older than the last accepted one.

```python
def fenced_write(data, token, db):
    if token <= db["last_token"]:
        return False  # stale or replayed writer — reject
    db["last_token"] = token
    db["data"] = data
    return True
```

Locks answer "may I start?"; fencing tokens answer "may I still write?" A
paused process that resumes late is caught by the second question.

## 5. Redlock and Its Critics

Redlock acquires the lock on a quorum (N/2+1) of *independent* Redis nodes,
tolerating node crashes. Martin Kleppmann's critique shows a paused process can
still violate mutual exclusion even under Redlock — a pause longer than every
TTL cannot be healed by more nodes. The consensus for practical systems:

- A single Redis lock + short TTL + fencing tokens is sufficient for most uses
  and dramatically simpler.
- Redlock only earns its complexity when you need safety across independent
  node failures *and* cannot use fencing tokens.

## 6. When You Actually Need One

| Need one | Do NOT need one |
|---|---|
| multi-process job that must run once (index rebuild, migration) | single-process concurrency → `threading.Lock` |
| cache stampede single-flight across replicas | serialized writes in one DB → DB transactions |
| distributed leader election | any case where the DB itself coordinates |

Distributed locks are a last resort, not a default. If the database already
serializes the critical section, adding a Redis lock is a second source of
truth for no benefit.

## Common Mistakes to Avoid

### Mistake 1: SETNX, then EXPIRE, in two calls
```
# WRONG — crash between the two = permanent lock
r.setnx("lock:job", "a"); r.expire("lock:job", 30)

# CORRECT — atomic SET NX PX
r.set("lock:job", "a", nx=True, ex=30)
```

### Mistake 2: Releasing with DEL
```
# WRONG — deletes whoever holds the lock now, not you
r.delete("lock:job")

# CORRECT — compare token, delete only if owned
```

### Mistake 3: No fencing token
```
# WRONG — a paused holder resumes and double-writes
# CORRECT — monotonic tokens checked at the resource
```

### Mistake 4: Redlock for a simple stampede
```
# WRONG — five nodes of complexity for one hot cache key
# CORRECT — one Redis lock + TTL + jitter is usually enough
```

## Best Practices

1. `SET NX PX` — acquire and expiry are one atomic command.
2. Random token per acquire; compare-and-delete on release.
3. TTL = worst-case job duration; renew (heartbeat) for longer jobs.
4. Fence the resource: tokens checked by the DB, not by the lock.
5. Keep the critical section as small as possible — the TTL is a deadline.
6. Retry acquisition with backoff + jitter; synchronized retries stampede.
7. Log token and holder on every acquire/release for debugging.
8. Prefer DB transactions and single-process primitives when they suffice.
9. Alert on lock contention; a lock everyone waits on is a bottleneck.
10. Test the crash paths: kill a holder, pause a holder, expire a lock.

## Complexity and Cost

| Operation | Cost | Failure mode |
|---|---|---|
| Acquire (`SET NX PX`) | O(1) | returns False — caller retries |
| Release (compare-delete) | O(1) | stale release rejected |
| TTL expiry | O(1) background | lock freed while holder paused |
| Fencing check | O(1) at resource | stale writes rejected |

The cost is not CPU — it is *correctness surface*. Every lock adds expiry math,
token checks, and a failure story. Each one must be exercised, or it will fail
at the worst moment.

## AI Engineering Relevance

**Where this shows up:** expensive shared AI resources are exactly what locks
protect — model fine-tuning, embedding-index rebuilds, and shared cache
recomputation.

| Concept here | Used for |
|---|---|
| `SET NX PX` single-flight | one replica recomputes a hot cache, others wait |
| Lock + lease | index rebuilds that must not run twice |
| Fencing tokens | versioned writes to a shared vector store |
| Leader election | one worker runs the scheduled embedding sweep |

**Scale note:** LLM cache stampedes are the most common real-world distributed
lock in modern systems — the lock is cheaper than the model call it saves. But
remember the fencing lesson: the *model budget* is the resource; a paused
winner re-calling the model is the double-write you fence against.

## Practice Exercises

### Exercise 1: Mutual exclusion (Difficulty: Easy)
Acquire the same lock with two tokens; verify the second fails while the first
holds, and succeeds after release.

### Exercise 2: Expiry frees the lock (Difficulty: Easy)
Acquire with TTL 10, advance the clock 11 seconds, and verify a new acquire
succeeds without any explicit release.

### Exercise 3: Safe release (Difficulty: Medium)
Show that a stale release (wrong token) returns `False` and leaves the lock
intact; the owner's release returns `True`.

### Exercise 4: Fencing tokens (Difficulty: Medium)
Write twice with tokens 1 and 2, then attempt a stale write with token 1 —
verify the resource rejects it and keeps the newest data.

### Exercise 5: Crash-timeout full cycle (Difficulty: Hard)
Acquire, advance past TTL, have a second process acquire, and verify a stale
release from the first process cannot delete the second's lock (the combined
expiry + ownership story).

## Summary

| Concept | Description |
|---|---|
| `SET NX PX` | one atomic acquire-with-expiry |
| Token ownership | release only your own lock |
| TTL | crash safety; also a deadline for the critical section |
| Paused holder | locks cannot fix it; fencing tokens at the resource do |
| Redlock | quorum acquisition; complexity justified only rarely |
| Need analysis | locks are a last resort after DB/single-process options |

A distributed lock is a tiny command with a deep failure model. Master the
traps (separate EXPIRE, blind DEL, paused holders) and you can use it with
confidence — or recognize when you do not need it at all.

## Quick Reference

| Task | Idiom |
|---|---|
| Acquire | `SET lock:<name> <token> NX PX <ms>` |
| Renew | `EXPIRE lock:<name> <s>` (with ownership check) |
| Release | compare value to token, then `DEL` (Lua) |
| Fence | resource rejects `token <= last_token` |
| Retry | backoff + jitter, bounded attempts |

## Next Steps

Next: **[Redis 07 — Sessions and Queues](07-session-and-queues-lecture.md)** —
the stateful layers of a web service: sessions, FIFO jobs, and priorities.

Continues in: **[Phase 5 — Backend](../../06-phase-5-backend/01-fastapi-lecture.md)** —
locks and leases protecting real background jobs.

Official docs: [redis.io/docs/latest/develop/use/patterns/distributed-locks/](https://redis.io/docs/latest/develop/use/patterns/distributed-locks/)
