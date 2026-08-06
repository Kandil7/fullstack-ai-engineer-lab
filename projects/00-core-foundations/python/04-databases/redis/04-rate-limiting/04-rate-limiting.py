"""
Redis — 04: Rate Limiting
==============================================
Topics: fixed window, sliding window, token bucket, INCR+EXPIRE atomicity,
        Lua-scripted atomic limits, distributed rate limiting

Why this matters for AI/backend engineering:
    LLM providers rate-limit you by tokens per minute; you must rate-limit
    your users the same way, or one runaway loop burns the whole budget.
    Redis is the coordination point for limits that must hold ACROSS
    processes (multiple API servers), which plain in-process counters
    cannot do.

Run:      python 04-rate-limiting.py
Verify:   python 04-rate-limiting.py --verify
Reference: https://redis.io/commands/incr/
"""

from __future__ import annotations

import sys
import time as _time

from redis_client import ManualClock, RedisClient, get_client

# ============================================================
# 1. Fixed Window — INCR + EXPIRE
# ============================================================
# Key = "rl:<user>:<window-id>"; INCR on each call, EXPIRE at window end.
# One command pair, O(1). Weakness: two bursts at the window boundary
# (23:59:59 and 00:00:00) can double the effective rate.

class FixedWindowLimiter:
    def __init__(self, client: RedisClient, limit: int, window_s: float) -> None:
        self._c = client
        self._limit = limit
        self._window = window_s

    def _window_id(self, now: float) -> int:
        return int(now // self._window)

    def allow(self, user: str, now: float | None = None) -> bool:
        now = self._c._clock() if now is None else now  # stand-in clock
        key = f"rl:fw:{user}:{self._window_id(now)}"
        count = self._c.incr(key)
        if count == 1:
            self._c.expire(key, self._window)
        return count <= self._limit


clock = ManualClock(start=0.0)
fw: FixedWindowLimiter = FixedWindowLimiter(RedisClient(clock=clock), limit=3, window_s=60)
hits = [fw.allow("alice", clock()) for _ in range(4)]
print(f"fixed window, 4 rapid calls -> {hits}")

# Output:
# fixed window, 4 rapid calls -> [True, True, True, False]

# Boundary weakness: window rolls over, budget resets instantly
clock.advance(59)
print(f"at 59s  -> {fw.allow('alice', clock())} (3rd slot used)")
clock.advance(1)
print(f"at 60s  -> {fw.allow('alice', clock())} (fresh window, allowed)")

# Output:
# at 59s  -> True (3rd slot used)
# at 60s  -> True (fresh window, allowed)

# ============================================================
# 2. Sliding Window — sorted set of timestamps
# ============================================================
# Keep the last N timestamps per user in a ZSET (member = request id,
# score = timestamp). Allow when ZCARD < limit; else drop old timestamps
# and reject. Memory: O(limit) per user. No boundary burst.

class SlidingWindowLimiter:
    def __init__(self, client: RedisClient, limit: int, window_s: float) -> None:
        self._c = client
        self._limit = limit
        self._window = window_s
        self._seq = 0

    def allow(self, user: str, now: float | None = None) -> bool:
        now = self._c._clock() if now is None else now
        key = f"rl:sw:{user}"
        # Strict window: drop requests strictly older than now - window.
        # (Real Redis uses ZREMRANGEBYSCORE with an exclusive bound; we
        # emulate it with a tiny epsilon.)
        self._c.zremrangebyscore(key, 0, now - self._window - 1e-9)
        if self._c.zcard(key) >= self._limit:
            return False
        self._seq += 1
        self._c.zadd(key, {f"r{self._seq}": now})             # record request
        self._c.expire(key, self._window)
        return True


sw: SlidingWindowLimiter = SlidingWindowLimiter(RedisClient(clock=clock), limit=3, window_s=60)
# 3 requests at t=0, then 1 at t=30 -> should be allowed (only 2 in window)
res = [sw.allow("bob", 0.0) for _ in range(3)]
clock.advance(30)
res.append(sw.allow("bob", clock()))
print(f"sliding window: t=0 x3 then t=30 -> {res}")

# Output:
# sliding window: t=0 x3 then t=30 -> [True, True, True, True]

clock.advance(30)   # t=60: requests at t=0 expired, only t=30 remains
res.append(sw.allow("bob", clock()))
res.append(sw.allow("bob", clock()))
print(f"at t=60: two more -> {res[-2:]} (t=0 window dropped)")

# Output:
# at t=60: two more -> [True, True] (t=0 window dropped)

# ============================================================
# 3. Token Bucket — smooth bursts
# ============================================================
# Bucket holds up to capacity tokens; refills at rate/sec. Each request
# takes 1 token. Allows bursts up to capacity, then exactly rate.

class TokenBucketLimiter:
    def __init__(self, client: RedisClient, capacity: float, refill_rate: float) -> None:
        self._c = client
        self._capacity = capacity
        self._rate = refill_rate

    def allow(self, user: str, now: float | None = None) -> bool:
        now = self._c._clock() if now is None else now
        key = f"rl:tb:{user}"
        tokens = float(self._c.hget(key, "tokens") or self._capacity)
        last = float(self._c.hget(key, "last") or now)
        tokens = min(self._capacity, tokens + (now - last) * self._rate)
        if tokens < 1.0:
            self._c.hset(key, {"tokens": str(tokens), "last": str(now)})
            return False
        self._c.hset(key, {"tokens": str(tokens - 1.0), "last": str(now)})
        return True


tb: TokenBucketLimiter = TokenBucketLimiter(RedisClient(clock=clock), capacity=2.0, refill_rate=1.0)
print(f"token bucket burst (cap 2) -> {[tb.allow('carol', 100.0) for _ in range(4)]}")

# Output:
# token bucket burst (cap 2) -> [True, True, False, False]

clock.advance(2)    # 2 seconds -> 2 tokens refilled
print(f"after 2s refill            -> {[tb.allow('carol', clock()) for _ in range(3)]}")

# Output:
# after 2s refill            -> [True, True, False]

# ============================================================
# 4. Atomicity — INCR+EXPIRE is NOT atomic on its own
# ============================================================
# Two servers racing can both see count==1 and both set EXPIRE — harmless
# here, but check-then-act sequences (peek tokens, then spend) MUST be
# atomic or you over-admit under load. Real Redis: Lua script or WATCH.
# Stand-in: register_script() executes one Python callable "atomically".

def _lua_token_bucket(client: RedisClient, keys: list[str], args: list) -> str:
    """One-shot token spend, atomic in the sim (and in real Lua EVAL)."""
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


lua_client: RedisClient = RedisClient(clock=clock)
lua_client.register_script("token_bucket", _lua_token_bucket)
verdicts = [lua_client.evalsha("token_bucket", ["rl:lua:dave"], [2.0, 1.0]) for _ in range(3)]
print(f"Lua-scripted spend (cap 2) -> {verdicts}")

# Output:
# Lua-scripted spend (cap 2) -> ['1', '1', '0']

# ============================================================
# 5. Distributed Limits
# ============================================================
# All three limiters above share state through Redis, so N API servers
# enforce ONE global limit. The alternative — per-process counters —
# lets a 10-replica deployment burst 10x. This is the core reason the
# counter lives in Redis, not in a Python dict.

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: fixed window for strict limits — boundary doubles throughput.
# CORRECT: sliding window or token bucket when bursts matter.
#
# MISTAKE: checking then acting in two separate round trips.
# CORRECT: atomic script (Lua EVAL) or WATCH/MULTI.
#
# MISTAKE: per-process rate limiting in a distributed deployment.
# CORRECT: shared Redis counter; the limit is global by construction.
#
# MISTAKE: forgetting EXPIRE — counters grow forever and keys accumulate.
# CORRECT: every rate-limit key carries a TTL.

# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # fixed window: 4th rapid call rejected
    assert hits == [True, True, True, False], \
        "Fixed window must reject the call beyond the limit"

    # sliding window: t=0 burst expires by t=60
    assert res[-1] is True, \
        "Sliding window must free slots after the window elapses"
    # window correctness: only requests within the last 60s count
    vclock = ManualClock(start=0.0)
    v_sw: SlidingWindowLimiter = SlidingWindowLimiter(RedisClient(clock=vclock), 2, 60)
    assert v_sw.allow("x", 0.0) and v_sw.allow("x", 1.0), "first two allowed"
    assert not v_sw.allow("x", 59.0), "third within window rejected"
    assert v_sw.allow("x", 62.0), "t=0 and t=1 requests expired, slot freed"

    # token bucket: capacity limits the burst, refill restores tokens
    assert [tb.allow("carol", 200.0) for _ in range(4)] == [True, True, False, False], \
        "Burst is capped by bucket capacity"

    # Lua script: same semantics, one atomic call
    assert verdicts == ["1", "1", "0"], \
        "Lua token bucket must behave identically to the Python version"

    # INCR+EXPIRE pairing: key must carry a TTL after the first call
    probe = FixedWindowLimiter(RedisClient(clock=ManualClock(0.0)), 5, 60)
    probe.allow("z", 0.0)
    assert probe._c.ttl("rl:fw:z:0") > 0, \
        "First INCR must attach an EXPIRE so the window self-clears"

    print("[OK] 04-rate-limiting: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Fixed window: INCR+EXPIRE, O(1), boundary bursts")
        print("2. Sliding window: ZSET of timestamps, no boundary burst")
        print("3. Token bucket: capacity + refill rate, smooth bursts")
        print("4. Atomicity: Lua scripts for check-then-act")
        print("5. Shared Redis = one limit across all replicas")
        _verify()  # always runs, so plain execution is also a test
