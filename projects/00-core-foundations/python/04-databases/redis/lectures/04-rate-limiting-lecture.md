# Databases — 04: Redis Rate Limiting

## Topic Overview

Rate limiting is the discipline of controlling how much traffic a client,
an API key, or a tenant may send. LLM providers rate-limit you by tokens per
minute; you must rate-limit your users the same way — otherwise one runaway
loop burns a whole budget or a noisy neighbor starves the rest of the system.

Redis is the natural coordination point because the limit must hold **across
processes**: with ten API replicas, an in-process counter would let traffic
through ten times over. The three canonical algorithms are the fixed window
(`INCR` + `EXPIRE`), the sliding window (a sorted set of timestamps), and the
token bucket (capacity + refill rate). Each is a different trade of memory,
precision, and burst behavior.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Implement a fixed-window limiter with `INCR` + `EXPIRE` in O(1)
2. Explain the fixed-window boundary weakness (double-rate bursts at rollover)
3. Implement a sliding-window limiter on a sorted set of timestamps
4. Implement a token bucket and explain its burst-plus-sustain behavior
5. Explain why check-then-act sequences must be atomic (Lua scripts, `WATCH`)
6. Give the TTL to every rate-limit key so counters never leak memory
7. Explain how a shared Redis counter enforces one limit across all replicas
8. Choose the right algorithm per requirement (strictness, burst, memory)

## Prerequisites

| Need | Where |
|---|---|
| `INCR`, `EXPIRE`, sorted sets | [02-data-structures-lecture.md](02-data-structures-lecture.md) |
| `SET NX` and atomicity thinking | [03-caching-patterns-lecture.md](03-caching-patterns-lecture.md) |
| Distributed-systems basics | [03-distributed-systems-lecture.md](../../03-systems/03-distributed-systems-lecture.md) |

## 1. Fixed Window — INCR + EXPIRE

The cheapest correct limiter: the key embeds the window id, `INCR` counts each
call, and the first call attaches an `EXPIRE` so the window self-clears.

```python
from redis_client import RedisClient, ManualClock

class FixedWindowLimiter:
    def __init__(self, client, limit, window_s):
        self._c, self._limit, self._window = client, limit, window_s

    def allow(self, user, now):
        key = f"rl:fw:{user}:{int(now // self._window)}"
        count = self._c.incr(key)
        if count == 1:
            self._c.expire(key, self._window)
        return count <= self._limit

clock = ManualClock(start=0.0)
fw = FixedWindowLimiter(RedisClient(clock=clock), limit=3, window_s=60)
print([fw.allow("alice", clock()) for _ in range(4)])

# Output:
# [True, True, True, False]
```

One command pair, O(1), zero bookkeeping. Its weakness is the boundary: at
23:59:59 a client uses 3 slots, at 00:00:00 the window resets and it gets 3
more — an effective doubling of the rate for a single burst.

## 2. Sliding Window — the Timestamp ZSET

The sliding window keeps the last N request timestamps in a sorted set per
user. Every call removes entries older than `now - window`, then admits if the
count is below the limit. There is no boundary to exploit: the window is a
continuous slice of time, not a partition of it.

```python
class SlidingWindowLimiter:
    def __init__(self, client, limit, window_s):
        self._c, self._limit, self._window = client, limit, window_s
        self._seq = 0

    def allow(self, user, now):
        key = f"rl:sw:{user}"
        self._c.zremrangebyscore(key, 0, now - self._window - 1e-9)
        if self._c.zcard(key) >= self._limit:
            return False
        self._seq += 1
        self._c.zadd(key, {f"r{self._seq}": now})
        self._c.expire(key, self._window)
        return True
```

Requests at t=0, t=30, t=60 are all allowed with limit 3; the second request at
t=61 is rejected — the t=0 entry has slid out of the window. Cost: O(limit)
memory per active user and a few zset ops per call.

## 3. Token Bucket — Smooth Bursts

The token bucket holds up to `capacity` tokens and refills at `rate` tokens per
second. Each request spends one token. The result is the friendliest behavior
for real traffic: a client may burst up to capacity instantly, then is held at
exactly the refill rate.

```python
class TokenBucketLimiter:
    def __init__(self, client, capacity, refill_rate):
        self._c, self._capacity, self._rate = client, capacity, refill_rate

    def allow(self, user, now):
        key = f"rl:tb:{user}"
        tokens = float(self._c.hget(key, "tokens") or self._capacity)
        last = float(self._c.hget(key, "last") or now)
        tokens = min(self._capacity, tokens + (now - last) * self._rate)
        if tokens < 1.0:
            self._c.hset(key, {"tokens": str(tokens), "last": str(now)})
            return False
        self._c.hset(key, {"tokens": str(tokens - 1.0), "last": str(now)})
        return True
```

State per user is two hash fields, and the refill math is the same whether the
bucket was last touched 1 second or 1 hour ago — no timers needed.

## 4. Atomicity — Check-Then-Act Must Be One Unit

The token bucket above *looks* atomic, but a read of `tokens`, then a write of
`tokens - 1`, is two round trips. Two concurrent requests can both read 1.0,
both decide they may spend, and both write 0.0 — over-admission under load.
Real Redis solves this with a Lua script (`EVAL`): the whole check-and-spend
runs inside the server, uninterrupted. The stand-in client models the same
contract with `register_script` + `evalsha`.

```python
def _lua_token_bucket(client, keys, args):
    key, capacity, rate = keys[0], float(args[0]), float(args[1])
    now = client._clock()
    tokens = float(client.hget(key, "tokens") or capacity)
    last = float(client.hget(key, "last") or now)
    tokens = min(capacity, tokens + (now - last) * rate)
    if tokens < 1.0:
        client.hset(key, {"tokens": str(tokens), "last": str(now)})
        return "0"
    client.hset(key, {"tokens": str(tokens - 1.0), "last": str(now)})
    return "1"
```

Any place you read a value and decide a write based on it is a race; the fix is
always the same — make it one atomic unit (Lua, or `WATCH`/`MULTI`).

## 5. Distributed Limits — Why Redis at All

With N API servers, a per-process counter allows Nx the intended rate: ten
replicas, each admitting 100 req/s, admit 1000 req/s overall. A counter in
Redis is shared by construction, so the limit is global. This single property —
one counter, many processes — is the entire reason rate-limit state lives in
Redis instead of a Python dict.

## Common Mistakes to Avoid

### Mistake 1: Fixed window for strict limits
```
# WRONG — boundary rollover lets a client double-burst
# CORRECT — sliding window or token bucket when bursts must be exact
```

### Mistake 2: Checking, then acting, in two round trips
```
# WRONG — two requests can both read the same token count and over-admit
tokens = hget(key, "tokens"); hset(key, tokens - 1)

# CORRECT — one Lua script / WATCH transaction
```

### Mistake 3: Rate limiting per process in a distributed deployment
```
# WRONG — 10 replicas each allow the full limit: 10x throughput
# CORRECT — shared Redis counter; the limit is global by construction
```

### Mistake 4: Forgetting the EXPIRE
```
# WRONG — counters accumulate forever; memory grows with every user
r.incr(f"rl:{user}:{window}")

# CORRECT — every rate-limit key carries a TTL
```

## Best Practices

1. Default to sliding window or token bucket; fixed window only for coarse limits.
2. TTL every key — a rate-limit key is ephemeral by definition.
3. Put check-then-act sequences in Lua scripts; never trust two round trips.
4. Key by user OR API key OR tenant — decide what the limit applies to.
5. Return the remaining budget and retry-after so clients can self-throttle.
6. Use token bucket for LLM calls (burst then sustain at provider rate).
7. Monitor rejection rate; a limiter silently rejecting everything is a bug.
8. Add jitter to retries, or synchronized clients create a retry stampede.
9. Keep the window math in one place — three limiters with three semantics is fine; three implementations of the same one is not.
10. Test with a fake clock (as the exercises do); real-time tests are flaky.

## Complexity and Cost

| Algorithm | Time per call | Memory per user | Burst behavior |
|---|---|---|---|
| Fixed window | O(1) | O(1) | doubles at boundaries |
| Sliding window | O(limit) zset ops | O(limit) | exact, no boundary |
| Token bucket | O(1) | O(2) fields | burst up to capacity |

The sliding window is the most memory-hungry (one timestamp per request in the
window); the token bucket matches it on strictness with constant memory. For
millions of users, prefer token bucket; for strict per-second guarantees, pay
for the zset.

## AI Engineering Relevance

**Where this shows up:** provider rate limits are the hard wall of every LLM
application. You are simultaneously the *client* of OpenAI/Anthropic limits and
the *provider* of limits to your own users.

| Concept here | Used for |
|---|---|
| Token bucket | staying inside tokens-per-minute provider limits |
| Sliding window | per-user quotas on a shared model endpoint |
| Atomic Lua scripts | decrementing a shared token budget exactly once |
| Distributed counters | one global limit across many API replicas |
| `INCR` + `EXPIRE` | per-minute request caps on cheap non-LLM endpoints |

**Scale note:** a provider token bucket is expensive state — if it is wrong,
you either burn money (over-admission) or 429 your users (under-admission). The
Lua-scripted bucket in this lecture is literally the shape of the middleware
you would ship to a shared gateway.

## Practice Exercises

### Exercise 1: Fixed window boundary (Difficulty: Easy)
With limit 3 and window 60, prove that calls at t=0, t=1, t=2 pass and the
fourth at t=2 fails, and that a call at t=61 succeeds (fresh window).

### Exercise 2: Sliding window expiration (Difficulty: Easy)
With limit 2, allow calls at t=0 and t=1, reject t=59, and allow t=62 — the
t=0 entry has left the window.

### Exercise 3: Token bucket refill (Difficulty: Medium)
Capacity 2, rate 1: show the burst pattern `[T, T, F, F]`, advance 2 seconds,
and show two more calls succeed.

### Exercise 4: Lua-atomic spend (Difficulty: Medium)
Register the token-bucket script and verify three rapid spends with capacity 2
return `['1', '1', '0']` — no double admission.

### Exercise 5: Distributed global limit (Difficulty: Hard)
Simulate two "replica" limiter instances sharing one `RedisClient`; prove the
combined admitted count never exceeds the limit across both, while two separate
clients would double it.

## Summary

| Concept | Description |
|---|---|
| Fixed window | `INCR` + `EXPIRE` per window-id; O(1); boundary bursts |
| Sliding window | zset of timestamps; exact; O(limit) memory |
| Token bucket | capacity + refill; bursts then sustained rate |
| Atomicity | check-then-act in Lua or `WATCH`, never two round trips |
| Distributed | one shared counter = one global limit |

All three algorithms are tiny. The engineering is in the guarantees: knowing
exactly which bursts are possible, which states are race-prone, and which keys
must expire.

## Quick Reference

| Task | Idiom |
|---|---|
| Fixed window | `INCR rl:fw:<user>:<win>`; on first, `EXPIRE 60` |
| Sliding window | `ZREMRANGEBYSCORE 0 now-w`; if `ZCARD < limit`, `ZADD now` |
| Token bucket | hash `tokens` + `last`; refill = `(now-last)*rate` |
| Atomic version | Lua `EVAL` script; `evalsha` by SHA |
| TTL hygiene | `EXPIRE key window` on every limiter |

## Next Steps

Next: **[Redis 05 — Pub/Sub and Streams](05-pubsub-and-streams-lecture.md)** —
decoupling producers from consumers, durable logs, and consumer groups.

Continues in: **[Phase 5 — Backend](../../06-phase-5-backend/01-fastapi-lecture.md)** —
middleware that applies these limiters to real endpoints.

Official docs: [redis.io/docs/latest/develop/use/patterns/](https://redis.io/docs/latest/develop/use/patterns/)
