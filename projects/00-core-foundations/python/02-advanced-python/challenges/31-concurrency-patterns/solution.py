"""
Challenge 31: Concurrency Patterns — Solution
=============================================
Deterministic: every time-dependent piece uses the injected clock or
sleep callable. Zero wall-clock asserts, zero sleeps in tests.
"""

from __future__ import annotations

import queue
import random
import time
from typing import Callable


# ============================================================
# Bronze: Token Bucket
# ============================================================

class TokenBucket:
    """Rate limiter: capacity tokens, refilled at rate/second.

    now: injectable clock (defaults to time.monotonic).
    """

    def __init__(self, capacity: int, rate: float,
                 now: Callable[[], float] = time.monotonic) -> None:
        self.capacity = capacity
        self.rate = rate
        self._now = now
        self.tokens = float(capacity)
        self.last_refill = now()

    def _refill(self) -> None:
        """Add tokens earned since the last refill. O(1)."""
        elapsed = self._now() - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = self._now()

    def try_acquire(self) -> bool:
        """Take one token if available; False when the bucket is empty. O(1)."""
        self._refill()
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


# ============================================================
# Silver: Bounded Producer-Consumer Pipeline
# ============================================================

class BoundedPipeline:
    """Bounded queue with backpressure: produce never hangs, never
    exceeds maxsize. FIFO consume. Tracks the max size ever observed."""

    def __init__(self, maxsize: int) -> None:
        self.maxsize = maxsize
        self._q: queue.Queue[int] = queue.Queue(maxsize=maxsize)
        self._observed = 0

    def _track(self) -> None:
        """Update the max-observed watermark. O(1)."""
        size = self._q.qsize()
        if size > self._observed:
            self._observed = size

    def produce(self, item: int, timeout: float = 0.05) -> bool:
        """Return True if enqueued, False if full within timeout. O(1)."""
        try:
            self._q.put(item, timeout=timeout)
        except queue.Full:
            return False
        self._track()
        return True

    def consume(self, timeout: float = 0.05) -> int | None:
        """Return the next FIFO item, or None if empty within timeout. O(1)."""
        try:
            return self._q.get(timeout=timeout)
        except queue.Empty:
            return None

    def max_observed(self) -> int:
        """Largest queue size ever held. O(1)."""
        return self._observed

    def drained(self) -> bool:
        """True when the queue is empty (everything consumed). O(1)."""
        return self._q.empty()


# ============================================================
# Gold: Circuit Breaker + Retry with Jitter
# ============================================================

class CircuitBreaker:
    """Fail-fast wrapper: closed -> (threshold failures) -> open ->
    (cooldown) -> half_open -> success closes / failure reopens."""

    def __init__(self, fn: Callable[[], int], threshold: int = 3,
                 cooldown: float = 1.0,
                 now: Callable[[], float] = time.monotonic) -> None:
        self.fn = fn
        self.threshold = threshold
        self.cooldown = cooldown
        self._now = now
        self._state = "closed"
        self._failures = 0
        self._open_until = 0.0
        self._short_circuited = 0

    @property
    def state(self) -> str:
        """closed | open | half_open."""
        # Lazy transition: once the cooldown elapses while open, the
        # next read/probe exposes half_open. The call() method uses the
        # same rule, so state and behavior never disagree.
        if self._state == "open" and self._now() >= self._open_until:
            self._state = "half_open"
        return self._state

    @property
    def short_circuited(self) -> int:
        """Calls rejected while open (fn never invoked for them). O(1)."""
        return self._short_circuited

    def call(self) -> int:
        """Run fn, or fail fast while open. O(1) state logic."""
        now = self._now()
        if self._state == "open":
            if now >= self._open_until:
                self._state = "half_open"
            else:
                self._short_circuited += 1
                raise RuntimeError("circuit open")
        try:
            result = self.fn()
        except Exception:
            self._failures += 1
            if self._failures >= self.threshold:
                self._state = "open"
                self._open_until = now + self.cooldown
            raise
        self._failures = 0
        self._state = "closed"
        return result


def retry_with_jitter(fn: Callable[[], int], attempts: int = 4,
                      base_delay: float = 0.1,
                      sleep: Callable[[float], None] = time.sleep,
                      rng: random.Random | None = None) -> int:
    """Retry with exponential backoff + full jitter: delay in
    [0, base_delay * 2 ** attempt]. Raises RuntimeError when exhausted."""
    rng = rng or random.Random(0)
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            return fn()
        except Exception as exc:          # noqa: BLE001 - retry is the point
            last_error = exc
            if attempt + 1 < attempts:
                delay = rng.uniform(0.0, base_delay * (2 ** attempt))
                sleep(delay)
    raise RuntimeError(f"failed after {attempts} attempts: {last_error}")
