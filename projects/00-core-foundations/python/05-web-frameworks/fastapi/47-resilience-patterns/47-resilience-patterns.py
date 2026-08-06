"""
FastAPI — 47: Resilience Patterns
===================================
Topics: timeouts; retries with jitter; circuit breakers; bulkheads;
        fallbacks and degradation; tenacity; cascading-failure prevention

Why this matters for AI/backend engineering:
    Dependencies fail: the LLM provider 5xxs, the vector DB slows, the
    upstream times out. Resilience is the set of patterns that keeps
    ONE dependency's failure from becoming YOUR outage. Timeouts bound
    the wait; retries with jitter survive transient blips; circuit
    breakers stop hammering a dying dependency; bulkheads isolate
    failure; fallbacks keep the product usable. Cascading failure is
    the thing to prevent — the provider blip that becomes your SLO
    breach that becomes a retry storm.

Run:      python 47-resilience-patterns.py
Verify:   python 47-resilience-patterns.py --verify
Reference: https://tenacity.readthedocs.io/
"""

from __future__ import annotations

import random
import sys
import time
from typing import Callable, Optional

# ============================================================
# 1. Timeouts — always set one
# ============================================================
# An un-timed external call can hang forever, wedging a worker. The
# timeout bounds the damage: fail fast, return the fallback, free the
# worker. Rule: every outbound call has an explicit timeout.

def call_with_timeout(fn: Callable[[], str], timeout: float) -> str:
    """Simulated timeout wrapper (real code: httpx timeout=..., async wait_for)."""
    start = time.monotonic()
    deadline = start + timeout
    while True:
        try:
            return fn()
        except Exception:
            if time.monotonic() >= deadline:
                raise TimeoutError(f"call exceeded {timeout}s")


def slow_provider(seconds: float) -> str:
    time.sleep(seconds)
    return "ok"


print("=== 1. Timeouts ===")
t0 = time.monotonic()
try:
    call_with_timeout(lambda: slow_provider(0.3), timeout=0.05)
except TimeoutError as e:
    print(f"timeout fired after {(time.monotonic()-t0)*1000:.0f}ms: {e}")
print()

# ============================================================
# 2. Retries with jitter + exponential backoff
# ============================================================
# Retry transient failures — but with backoff (don't hammer) and
# jitter (don't synchronize). The classic retry-storm: 1000 clients
# all retry at the same instant after a blip.

def retry_with_backoff(fn: Callable[[], str], attempts: int = 4,
                       base_delay: float = 0.02, jitter: float = 0.005,
                       rng: random.Random | None = None) -> str:
    rng = rng or random.Random()
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            return fn()
        except Exception as e:
            last = e
            delay = base_delay * (2 ** attempt) + rng.uniform(0, jitter)
            time.sleep(delay)
    raise last  # type: ignore[misc]


flaky = {"calls": 0}
def flaky_provider() -> str:
    flaky["calls"] += 1
    if flaky["calls"] <= 2:
        raise ConnectionError("transient blip")
    return "ok"


print("=== 2. Retries with backoff + jitter ===")
result = retry_with_backoff(flaky_provider)
print(f"succeeded after {flaky['calls']} calls (2 failures retried): {result}")
print()

# ============================================================
# 3. Circuit breaker — stop hammering the dying dependency
# ============================================================
# States: CLOSED (normal), OPEN (stop calling, fail fast), HALF-OPEN
# (test with one call). Trip on failure threshold; cool down; probe.
# The breaker converts a slow-motion outage into fast failures that
# protect the whole system.

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, cooldown: float = 0.1) -> None:
        self.threshold = failure_threshold
        self.cooldown = cooldown
        self.failures = 0
        self.state = "closed"          # closed | open | half-open
        self._opened_at = 0.0

    def allow(self) -> bool:
        now = time.monotonic()
        if self.state == "open":
            if now - self._opened_at >= self.cooldown:
                self.state = "half-open"     # probe with one call
                return True
            return False
        return True

    def record_success(self) -> None:
        self.failures = 0
        self.state = "closed"

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.threshold:
            self.state = "open"
            self._opened_at = time.monotonic()


def guarded_call(breaker: CircuitBreaker, fn: Callable[[], str]) -> str:
    if not breaker.allow():
        raise RuntimeError("circuit open — fast fail")
    try:
        result = fn()
    except Exception:
        breaker.record_failure()
        raise
    breaker.record_success()
    return result


dead = {"fail": True}
def dying_provider() -> str:
    if dead["fail"]:
        raise ConnectionError("downstream is down")
    return "ok"

breaker = CircuitBreaker(failure_threshold=2, cooldown=0.05)
print("=== 3. Circuit breaker ===")
for i in range(3):
    try:
        guarded_call(breaker, dying_provider)
    except RuntimeError as e:
        print(f"call {i+1}: fast-fail ({e})")
    except ConnectionError:
        pass
print(f"state after 2 failures: {breaker.state}")
time.sleep(0.06)
breaker.record_failure()  # probe call fails again
print(f"state after probe failure: {breaker.state}")
dead["fail"] = False
print(f"probe allowed: {breaker.allow()} -> state: {breaker.state}")
print(f"recovered call: {guarded_call(breaker, dying_provider)} -> state: {breaker.state}")
print()

# ============================================================
# 4. Bulkhead — isolate failure per dependency
# ============================================================
# One slow dependency should not exhaust the shared pool. Bulkheads
# give each dependency its own concurrency/thread budget — a blast
# wall between dependencies.

class Bulkhead:
    def __init__(self, slots: int) -> None:
        self.slots = slots
        self.used = 0

    def try_acquire(self) -> bool:
        if self.used >= self.slots:
            return False
        self.used += 1
        return True

    def release(self) -> None:
        self.used = max(0, self.used - 1)


print("=== 4. Bulkheads ===")
retrieval = Bulkhead(2)
for i in range(3):
    got = retrieval.try_acquire()
    print(f"  retrieval slot {i+1}: {'acquired' if got else 'rejected (bulkhead full)'}")
    if got:
        retrieval.release()
print()

# ============================================================
# 5. Fallbacks and degradation
# ============================================================
# When the premium path fails, degrade gracefully: cached results,
# a cheaper model, a smaller context. The product stays usable.

def generate_with_fallback(primary: Callable[[], str],
                           fallback: Callable[[], str]) -> str:
    try:
        return primary()
    except Exception:
        return fallback()


print("=== 5. Fallbacks ===")
primary = lambda: (_ for _ in ()).throw(ConnectionError("provider down"))
fallback = lambda: "cached-completion"
print(f"degraded result: {generate_with_fallback(primary, fallback)}")
print()

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: no timeouts — one hung provider wedges workers forever
# CORRECT: explicit timeout on EVERY outbound call
#
# MISTAKE: retries without backoff/jitter — synchronized retry storms
# CORRECT: exponential backoff + jitter; cap attempts
#
# MISTAKE: retrying non-transient failures (4xx, bad input) forever
# CORRECT: retry 5xx/timeouts only; fail fast on 4xx
#
# MISTAKE: no circuit breaker — a dying dependency is hammered until
#   its outage becomes yours
# CORRECT: breaker trips on threshold; probes after cooldown
#
# MISTAKE: one shared pool for all dependencies
# CORRECT: bulkheads per dependency

# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""

    # 1. Timeout fires
    t0 = time.monotonic()
    try:
        call_with_timeout(lambda: slow_provider(0.2), timeout=0.02)
        assert False, "timeout must fire"
    except TimeoutError:
        assert time.monotonic() - t0 < 0.15, "timeout must fire fast"

    # 2. Retry succeeds after transient failures
    calls = {"n": 0}
    def flaky2() -> str:
        calls["n"] += 1
        if calls["n"] <= 2:
            raise ConnectionError("blip")
        return "ok"
    assert retry_with_backoff(flaky2) == "ok"
    assert calls["n"] == 3, "two retries then success"

    # 3. Circuit breaker trips and recovers
    b = CircuitBreaker(failure_threshold=2, cooldown=0.02)
    assert b.allow() is True, "closed allows"
    b.record_failure(); b.record_failure()
    assert b.state == "open", "trips after threshold"
    assert b.allow() is False, "open fast-fails"
    time.sleep(0.03)
    assert b.allow() is True, "cooldown probes (half-open)"
    b.record_success()
    assert b.state == "closed", "success closes the circuit"

    # 4. Bulkhead rejects beyond slots
    bh = Bulkhead(2)
    assert bh.try_acquire() and bh.try_acquire()
    assert bh.try_acquire() is False, "third concurrent call rejected"
    bh.release()
    assert bh.try_acquire() is True, "released slot reusable"

    # 5. Fallback on failure
    def boom() -> str:
        raise RuntimeError("down")
    assert generate_with_fallback(boom, lambda: "cached") == "cached"

    print("[OK] 47-resilience-patterns: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Timeout every outbound call")
        print("2. Retry transient failures: backoff + jitter, capped")
        print("3. Circuit breaker: fast-fail, probe, recover")
        print("4. Bulkheads isolate dependencies; fallbacks degrade")
        print("5. The goal: one dependency's failure != your outage")
        _verify()          # always runs, so plain execution is also a test
