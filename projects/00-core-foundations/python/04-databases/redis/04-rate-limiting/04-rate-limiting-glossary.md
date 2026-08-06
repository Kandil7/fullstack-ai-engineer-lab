# Redis — Glossary 04

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| 429 Too Many Requests | Protocol | HTTP status returned when a limit is exceeded |
| Atomicity | Correctness | a check-then-act sequence that cannot interleave |
| Burst | Traffic | a short spike above the sustained rate |
| Distributed limit | Design | one shared counter across many processes |
| EXPIRE | Key | TTL attached so limit keys self-clean |
| Fixed window | Algorithm | per-window INCR+EXPIRE; O(1), boundary bursts |
| INCR | Primitive | atomic counter per user per window |
| Lua script | Primitive | server-side atomic block executed by EVAL |
| Quota | Policy | the allowed amount per user/tenant/period |
| Rate limit | Policy | maximum requests (or tokens) per time unit |
| Refill rate | Algorithm | tokens added per second in a token bucket |
| Sliding window | Algorithm | zset of timestamps; exact, no boundary burst |
| Token bucket | Algorithm | capacity + refill; burst then sustain |
| Window id | Algorithm | fixed-window partition, e.g. epoch // 60 |

## Detailed Definitions

### 429 Too Many Requests
**Definition**: The HTTP status a rate limiter returns when a client exceeds
its allowed rate; clients should retry with backoff.
**Example**:
```python
# conceptual: the API middleware returns 429 with Retry-After
# when the Redis limiter says allow() is False
```
```text
# 429 is the contract: try later, not harder
```
**Complexity**: n/a — protocol behavior.
**Related**: Rate limit, Distributed limit

### Atomicity
**Definition**: The property that a check-then-act sequence (read count,
decide, write) cannot interleave with another caller.
**Example**:
```python
# WRONG: two callers both read tokens == 1.0, both spend
# CORRECT: Lua script does the whole check-and-spend in one step
```
```text
# without atomicity, limits over-admit exactly under load
```
**Complexity**: atomic primitives cost one round trip.
**Related**: Lua script, Token bucket

### Burst
**Definition**: A short spike of traffic above the sustained rate; how a
limiter treats bursts defines its character.
**Example**:
```python
# fixed window: bursts double at boundaries
# sliding window: bursts are bounded by the window
# token bucket: bursts up to capacity, then exactly refill rate
```
```text
# "burst then sustain" is the friendliest real-world behavior
```
**Complexity**: n/a — a workload property.
**Related**: Token bucket, Fixed window

### Distributed limit
**Definition**: A rate limit enforced through shared Redis state, so N API
replicas together admit no more than the intended total.
**Example**:
```python
# one counter in Redis shared by 10 servers
# vs per-process counters: 10x the intended rate
```
```text
# the whole reason limit state lives in Redis, not a dict
```
**Complexity**: O(1) shared counter per call.
**Related**: Rate limit, INCR

### EXPIRE
**Definition**: The TTL attached to every rate-limit key so counters do not
accumulate forever.
**Example**:
```python
count = r.incr(f"rl:fw:{user}:{window}")
if count == 1:
    r.expire(f"rl:fw:{user}:{window}", 60)  # self-clearing window
```
```text
# forgetting this = memory grows with every user ever
```
**Complexity**: O(1).
**Related**: Fixed window, INCR

### Fixed window
**Definition**: The simplest limiter: count calls per window-id with INCR,
EXPIRE the key — O(1) and leak-proof.
**Example**:
```python
key = f"rl:fw:{user}:{int(now // 60)}"
count = r.incr(key)
if count == 1:
    r.expire(key, 60)
print(count <= 3)  # limit 3 per minute
```
```text
# weakness: 23:59:59 + 00:00:00 = double burst
```
**Complexity**: O(1) per call.
**Related**: Window id, INCR, EXPIRE

### INCR
**Definition**: The atomic counter primitive at the heart of fixed-window
rate limiting.
**Example**:
```python
from redis_client import get_client

r = get_client()
print(r.incr("rl:alice:0"))  # -> 1
print(r.incr("rl:alice:0"))  # -> 2
```
```text
# atomic: concurrent calls never lose a count
```
**Complexity**: O(1).
**Related**: Fixed window, Distributed limit

### Lua script
**Definition**: A block of commands executed atomically inside the server
via EVAL — the fix for check-then-act races.
**Example**:
```python
# conceptual: EVAL "local t=redis.call('HGET',...); ... return ok"
# registered via register_script + called by evalsha
verdicts = [lc.evalsha("token_bucket", ["rl:dave"], [2.0, 1.0]) for _ in range(3)]
print(verdicts)  # ['1', '1', '0'] — no double admission
```
```text
# the script is the unit of atomicity, not the individual commands
```
**Complexity**: O(1) per script execution.
**Related**: Atomicity, Token bucket

### Quota
**Definition**: The policy amount — requests per period or tokens per minute
— assigned to a user, key, or tenant.
**Example**:
```python
# conceptual: free tier quota = 1000 requests/hour
# provider quota = 200k tokens/minute
```
```text
# quotas are the policy; limiters are the enforcement
```
**Complexity**: n/a — configuration.
**Related**: Rate limit, Distributed limit

### Rate limit
**Definition**: A policy that caps how much traffic a caller may send in a
time unit — the protection against runaway loops and noisy neighbors.
**Example**:
```python
# conceptual: allow(user) -> bool
# False means "reject this call" (429)
```
```text
# LLM providers rate-limit you; you rate-limit your users
```
**Complexity**: O(1) per call with good design.
**Related**: Quota, 429 Too Many Requests

### Refill rate
**Definition**: In a token bucket, the number of tokens added per second —
the sustained rate after a burst.
**Example**:
```python
tokens = min(capacity, tokens + (now - last) * rate)
# rate = 1.0 -> one request allowed per second sustained
```
```text
# refill math is the same after 1s or 1h idle
```
**Complexity**: O(1).
**Related**: Token bucket, Burst

### Sliding window
**Definition**: A limiter keeping request timestamps in a sorted set; the
window is a continuous slice of time, so no boundary bursts exist.
**Example**:
```python
r.zremrangebyscore(key, 0, now - window - 1e-9)
if r.zcard(key) >= limit:
    return False
r.zadd(key, {f"r{seq}": now})
r.expire(key, window)
```
```text
# exact windows; costs O(limit) memory per active user
```
**Complexity**: O(limit) zset ops per call.
**Related**: Fixed window, Token bucket

### Token bucket
**Definition**: A limiter with a capacity and a refill rate: clients may
burst to capacity instantly, then are held at the refill rate.
**Example**:
```python
# capacity 2, rate 1: [True, True, False, False]
# after 2s idle: [True, True, ...] again
```
```text
# constant memory per user; the standard for LLM call budgets
```
**Complexity**: O(1) per call.
**Related**: Refill rate, Burst, Atomicity

### Window id
**Definition**: The fixed-window partition label derived from the clock —
`int(now // window)` — that makes counters per-window.
**Example**:
```python
# now = 125s, window = 60s -> window id 2 (second minute)
key = f"rl:fw:{user}:{int(now // 60)}"
```
```text
# the window rollover is where the boundary burst lives
```
**Complexity**: O(1).
**Related**: Fixed window, Sliding window

## Key Concepts Summary

### Algorithms
- Fixed window: INCR + EXPIRE, O(1), boundary bursts
- Sliding window: zset of timestamps, exact, O(limit) memory
- Token bucket: capacity + refill, bursts then sustained rate

### Correctness
- Check-then-act must be atomic: Lua EVAL or WATCH, never two round trips
- Every rate-limit key carries a TTL or memory leaks forever
- The shared Redis counter makes the limit global across replicas

### Policy
- Quota defines the amount; the limiter enforces it; 429 is the response
- Bursts are the differentiator: bucket-friendly, fixed-window fragile

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Fixed window — ___
2. Sliding window — ___
3. Token bucket — ___
4. Lua script — ___
5. 429 — ___
6. Window id — ___
7. Refill rate — ___
8. Distributed limit — ___

a) Continuous time slice, no boundary burst
b) INCR + EXPIRE per window partition
c) Atomic server-side block via EVAL
d) HTTP status for exceeding a limit
e) Tokens added per second
f) One shared counter across all replicas
g) Capacity + refill, burst then sustain
h) int(now // window) key suffix

**Answers:** 1-b, 2-a, 3-g, 4-c, 5-d, 6-h, 7-e, 8-f
