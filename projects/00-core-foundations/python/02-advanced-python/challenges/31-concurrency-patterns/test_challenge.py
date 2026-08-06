"""
Challenge 31: Concurrency Patterns — Hidden Tests
=================================================
All timing is injected: fake clocks for buckets/breakers, recorded
sleeps for retries. Tests run in milliseconds and never sleep.
"""

from __future__ import annotations

import importlib.util
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution")
import pytest  # noqa: E402


class FakeClock:
    """Injectable clock: tests advance time instantly."""

    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


# ============================================================
# Bronze: Token Bucket
# ============================================================

def test_burst_up_to_capacity():
    clock = FakeClock()
    bucket = solution.TokenBucket(capacity=3, rate=1.0, now=clock)
    assert [bucket.try_acquire() for _ in range(3)] == [True, True, True]
    assert bucket.try_acquire() is False, "4th instant request must be refused"


def test_refill_exactly_rate():
    clock = FakeClock()
    bucket = solution.TokenBucket(capacity=10, rate=1.0, now=clock)
    for _ in range(10):
        bucket.try_acquire()
    assert bucket.try_acquire() is False
    clock.advance(1.0)
    assert bucket.try_acquire() is True, "1s at rate 1.0 -> exactly one token"
    assert bucket.try_acquire() is False, "and that token is now spent"


def test_tokens_never_exceed_capacity():
    clock = FakeClock()
    bucket = solution.TokenBucket(capacity=3, rate=5.0, now=clock)
    clock.advance(100.0)          # 500 tokens would accrue; capped at 3
    assert bucket.try_acquire() is True
    assert bucket.try_acquire() is True
    assert bucket.try_acquire() is True
    assert bucket.try_acquire() is False, "must never exceed capacity"


def test_zero_rate_never_refills():
    clock = FakeClock()
    bucket = solution.TokenBucket(capacity=1, rate=0.0, now=clock)
    assert bucket.try_acquire() is True
    clock.advance(1000.0)
    assert bucket.try_acquire() is False, "rate 0.0 -> no tokens ever"


def test_bucket_initial_burst():
    clock = FakeClock()
    bucket = solution.TokenBucket(capacity=2, rate=1.0, now=clock)
    assert bucket.try_acquire() is True
    assert bucket.try_acquire() is True


# ============================================================
# Silver: Bounded Pipeline
# ============================================================

def test_backpressure_never_exceeds_maxsize():
    pipe = solution.BoundedPipeline(maxsize=2)
    assert pipe.produce(1) is True
    assert pipe.produce(2) is True
    assert pipe.produce(3) is False, "full -> refused, not blocked, not grown"
    assert pipe.max_observed() == 2, "queue size never exceeded maxsize"
    assert pipe.consume() == 1
    assert pipe.produce(3) is True, "room freed -> producer accepted again"


def test_fifo_order_and_drain():
    pipe = solution.BoundedPipeline(maxsize=3)
    assert [pipe.produce(i) for i in range(3)] == [True, True, True]
    assert pipe.max_observed() == 3
    assert [pipe.consume() for _ in range(3)] == [0, 1, 2], "FIFO preserved"
    assert pipe.drained() is True


def test_produce_returns_false_not_hang():
    pipe = solution.BoundedPipeline(maxsize=1)
    pipe.produce(1)
    start = time.monotonic()
    result = pipe.produce(2, timeout=0.05)
    elapsed = time.monotonic() - start
    assert result is False
    assert elapsed < 1.0, "produce on a full queue must return, not hang"


def test_drained_and_empty_consume():
    pipe = solution.BoundedPipeline(maxsize=2)
    assert pipe.drained() is True
    assert pipe.consume() is None, "empty -> None, not block"


def test_roundtrip_no_loss():
    pipe = solution.BoundedPipeline(maxsize=5)
    out = []
    # produce/consume in waves: the bound is respected, nothing is lost
    for wave in range(10):
        for i in range(5):
            assert pipe.produce(wave * 5 + i) is True
        assert pipe.max_observed() == 5, "bound respected across waves"
        for _ in range(5):
            item = pipe.consume()
            assert item is not None, "every produced item is consumed"
            out.append(item)
    assert out == list(range(50)), "no item lost, order preserved"
    assert pipe.drained() is True


# ============================================================
# Gold: Circuit Breaker
# ============================================================

def _counting_fail(fail_times: int):
    """Returns (fn, counter) where fn fails `fail_times` times then returns 42."""
    state = {"n": 0}

    def fn() -> int:
        state["n"] += 1
        if state["n"] <= fail_times:
            raise ConnectionError("down")
        return 42

    return fn, state


def test_breaker_opens_after_threshold():
    clock = FakeClock()
    fn, state = _counting_fail(10**6)          # always fails
    breaker = solution.CircuitBreaker(fn, threshold=3, cooldown=1.0, now=clock)
    for _ in range(3):
        with pytest.raises(ConnectionError):
            breaker.call()
    assert breaker.state == "open"


def test_breaker_short_circuits_without_calling_fn():
    clock = FakeClock()
    fn, state = _counting_fail(10**6)
    breaker = solution.CircuitBreaker(fn, threshold=2, cooldown=1.0, now=clock)
    for _ in range(2):
        with pytest.raises(ConnectionError):
            breaker.call()
    before = state["n"]
    with pytest.raises(RuntimeError):
        breaker.call()
    assert breaker.short_circuited == 1
    assert state["n"] == before, "fn must not be invoked while open"


def test_breaker_recovers_half_open():
    clock = FakeClock()
    fn, state = _counting_fail(3)               # succeeds on 4th call
    breaker = solution.CircuitBreaker(fn, threshold=3, cooldown=1.0, now=clock)
    for _ in range(3):
        with pytest.raises(ConnectionError):
            breaker.call()
    assert breaker.state == "open"
    clock.advance(1.0)                          # cooldown elapsed
    assert breaker.call() == 42                 # half-open trial succeeds
    assert breaker.state == "closed"
    assert breaker.call() == 42                 # fully closed again


def test_breaker_half_open_failure_reopens():
    clock = FakeClock()
    fn, state = _counting_fail(10**6)           # still failing
    breaker = solution.CircuitBreaker(fn, threshold=2, cooldown=1.0, now=clock)
    for _ in range(2):
        with pytest.raises(ConnectionError):
            breaker.call()
    clock.advance(1.0)
    with pytest.raises(ConnectionError):
        breaker.call()                          # half-open trial fails
    assert breaker.state == "open"


def test_breaker_success_resets_failure_count():
    clock = FakeClock()
    state = {"fail": True}

    def controllable() -> int:
        if state["fail"]:
            raise ConnectionError("down")
        return 42

    breaker = solution.CircuitBreaker(controllable, threshold=3,
                                      cooldown=1.0, now=clock)
    with pytest.raises(ConnectionError):
        breaker.call()                        # failure 1
    state["fail"] = False
    assert breaker.call() == 42               # success resets failures
    state["fail"] = True
    with pytest.raises(ConnectionError):
        breaker.call()                        # failure 1 again (reset!)
    assert breaker.state == "closed", "only 1 failure since last reset"


# ============================================================
# Gold: Retry with Jitter
# ============================================================

def test_retry_succeeds_and_records_delays():
    delays: list[float] = []

    def log_sleep(d: float) -> None:
        delays.append(d)

    fn, state = _counting_fail(2)
    result = solution.retry_with_jitter(fn, attempts=4, base_delay=0.1,
                                        sleep=log_sleep)
    assert result == 42
    assert len(delays) == 2, "one jittered delay per failed attempt"
    assert delays[0] <= 0.1, "attempt 0 window is [0, base]"
    assert delays[1] <= 0.2, "attempt 1 window is [0, base*2]"
    assert all(d >= 0.0 for d in delays)


def test_retry_exhausts_and_raises():
    delays: list[float] = []

    def log_sleep(d: float) -> None:
        delays.append(d)

    fn, state = _counting_fail(10**6)
    with pytest.raises(RuntimeError):
        solution.retry_with_jitter(fn, attempts=3, base_delay=0.1,
                                   sleep=log_sleep)
    assert state["n"] == 3, "exactly `attempts` invocations"
    assert len(delays) == 2, "no delay after the final attempt"


def test_retry_delays_are_randomized_not_fixed():
    delays_a: list[float] = []
    delays_b: list[float] = []

    def log_a(d: float) -> None:
        delays_a.append(d)

    def log_b(d: float) -> None:
        delays_b.append(d)

    fn1, _ = _counting_fail(1)
    fn2, _ = _counting_fail(1)
    solution.retry_with_jitter(fn1, attempts=2, base_delay=0.5, sleep=log_a,
                               rng=random.Random(1))
    solution.retry_with_jitter(fn2, attempts=2, base_delay=0.5, sleep=log_b,
                               rng=random.Random(2))
    assert delays_a[0] != delays_b[0], "different seeds -> different delays"


def test_retry_first_try_success_no_delay():
    delays: list[float] = []
    solution.retry_with_jitter(lambda: 7, sleep=lambda d: delays.append(d))
    assert delays == [], "no sleep when the first attempt succeeds"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
