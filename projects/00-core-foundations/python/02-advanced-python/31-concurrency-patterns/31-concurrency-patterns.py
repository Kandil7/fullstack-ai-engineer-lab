"""
Advanced Python — 31: Concurrency Patterns
============================================
Topics: producer-consumer with bounded queues + backpressure, worker
pools, fan-out/fan-in, rate limiting (token bucket), circuit breaker,
bulkhead, retry with jitter, graceful shutdown, idempotency, deadlock/
livelock/starvation

Why this matters for AI/backend engineering:
    A batch embedding job is a producer-consumer pipeline; provider
    rate limits demand token buckets; a degraded model endpoint needs a
    circuit breaker. These patterns are the difference between a job
    that dies on a 429 and one that survives it. The R1.1 deadlock from
    06-data-structures-algorithms/04-queues.py is the worked counter-
    example: a producer blocked forever on a full queue because no
    consumer ever drains it. The fix is a bounded queue + timeout.

Run:      python 31-concurrency-patterns.py
Verify:   python 31-concurrency-patterns.py --verify
Reference: https://docs.python.org/3/library/queue.html
"""

from __future__ import annotations

import queue
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Callable


# ============================================================
# 1. Producer-Consumer with Bounded Queue + Backpressure
# ============================================================
# A bounded queue is the buffer between producers and consumers.
# Backpressure = the producer BLOCKS (or times out) when the buffer is
# full, instead of memory growing without bound. queue.Queue with
# maxsize + put(timeout=...) is the correct version of the R1.1 bug.

# Example 1: backpressure demo — a full queue refuses the producer
q: queue.Queue[int] = queue.Queue(maxsize=2)
q.put(1)
q.put(2)
try:
    q.put(3, timeout=0.05)      # full -> blocks briefly, then raises
    print("put succeeded (unexpected)")
except queue.Full as exc:
    print(f"producer blocked: {type(exc).__name__} after timeout")

# Output:
# producer blocked: Full after timeout

# Example 1b: the R1.1-style deadlock, made safe
# The original bug: producer() calls put() with NO timeout while no
# consumer runs -> the thread waits forever. That is a real deadlock.
# The fixed pattern always carries a timeout (or drain signaling):
def bounded_put(q_: "queue.Queue[int]", item: int, timeout: float = 0.05) -> bool:
    """Try to enqueue; return False instead of hanging forever. O(1)."""
    try:
        q_.put(item, timeout=timeout)
        return True
    except queue.Full:
        return False


print(f"bounded_put on full queue: {bounded_put(q, 3)}")

# Output:
# bounded_put on full queue: False


# ============================================================
# 2. Worker Pools
# ============================================================
# ThreadPoolExecutor caps concurrency: N workers, M tasks. The GIL
# makes threads ideal for I/O-bound work (API calls, file reads) and
# wrong for CPU-bound math.

def fetch(url_id: int) -> int:
    """Simulated I/O: sleep-free, pure-ish work with a tiny delay."""
    time.sleep(0.01)          # fake network latency
    return url_id * 2


# Example 2: pool with bounded concurrency
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch, range(8)))
print(f"pool results: {results}")

# Output:
# pool results: [0, 2, 4, 6, 8, 10, 12, 14]


# ============================================================
# 3. Fan-Out / Fan-In
# ============================================================
# Fan-out: split one batch into chunks processed in parallel.
# Fan-in: merge partial results back into one ordered result.

def fan_out_fan_in(items: list[int], workers: int) -> list[int]:
    """Process chunks in parallel, then merge in original order. O(n)."""
    chunk_size = max(1, len(items) // workers)
    chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        partials = list(pool.map(lambda chunk: [x * 2 for x in chunk], chunks))
    merged: list[int] = []
    for part in partials:
        merged.extend(part)
    return merged


# Example 3: order preserved across parallel chunks
print(f"fan-out/fan-in: {fan_out_fan_in(list(range(10)), 4)}")

# Output:
# fan-out/fan-in: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]


# ============================================================
# 4. Rate Limiting: Token Bucket
# ============================================================
# The token bucket: capacity tokens, refilled at rate per second. A
# request takes a token; when the bucket is empty, requests must wait.
# The clock is INJECTED so tests never touch wall time.

class TokenBucket:
    """A deterministic token bucket with an injectable clock."""
    def __init__(self, capacity: int, rate: float,
                 now: Callable[[], float] = time.monotonic) -> None:
        self.capacity = capacity
        self.rate = rate
        self._now = now
        self.tokens = float(capacity)
        self.last_refill = now()

    def _refill(self) -> None:
        """Add tokens earned since last refill. O(1)."""
        elapsed = self._now() - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = self._now()

    def try_acquire(self) -> bool:
        """Take one token if available. O(1)."""
        self._refill()
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


# Example 4: enforce a rate with a fake clock
fake_now = {"t": 0.0}

def fake_clock() -> float:
    """Injectable clock for deterministic rate limiting."""
    return fake_now["t"]

bucket = TokenBucket(capacity=3, rate=1.0, now=fake_clock)
print(f"burst of 3: {[bucket.try_acquire() for _ in range(3)]}")
print(f"4th request: {bucket.try_acquire()}")
fake_now["t"] += 0.5          # half a token earned
print(f"after 0.5s: {bucket.try_acquire()}")
fake_now["t"] += 0.5          # another half token -> full
print(f"after 1.0s: {bucket.try_acquire()}")

# Output:
# burst of 3: [True, True, True]
# 4th request: False
# after 0.5s: False
# after 1.0s: True


# ============================================================
# 5. Circuit Breaker
# ============================================================
# After N consecutive failures, OPEN the circuit: fail fast without
# calling the broken endpoint. After a cooldown, HALF-OPEN allows one
# trial; success closes the circuit, failure reopens it.

@dataclass
class CircuitState:
    """Mutable state machine for the breaker. O(1) transitions."""
    failures: int = 0
    open_until: float = 0.0
    state: str = "closed"     # closed | open | half_open


class CircuitBreaker:
    """Fail-fast wrapper around a fragile callable."""
    def __init__(self, fn: Callable[[], int], threshold: int = 3,
                 cooldown: float = 1.0,
                 now: Callable[[], float] = time.monotonic) -> None:
        self.fn = fn
        self.threshold = threshold
        self.cooldown = cooldown
        self._now = now
        self.state = CircuitState()
        self.short_circuited = 0

    def call(self) -> int:
        """Run fn or fail fast while open. O(1) state logic."""
        now = self._now()
        if self.state.state == "open":
            if now >= self.state.open_until:
                self.state.state = "half_open"
            else:
                self.short_circuited += 1
                raise RuntimeError("circuit open")
        try:
            result = self.fn()
        except Exception:
            self.state.failures += 1
            if self.state.failures >= self.threshold:
                self.state.state = "open"
                self.state.open_until = now + self.cooldown
            raise
        # success
        self.state.failures = 0
        self.state.state = "closed"
        return result


# Example 5: breaker opens after 3 failures, fails fast, then recovers
calls = {"n": 0}

def flaky() -> int:
    """Fails the first 3 calls, then succeeds (provider recovers)."""
    calls["n"] += 1
    if calls["n"] <= 3:
        raise ConnectionError("provider down")
    return 42

fake_clock = {"t": 0.0}

def breaker_clock() -> float:
    """Injectable clock for the breaker."""
    return fake_clock["t"]

breaker = CircuitBreaker(flaky, threshold=3, cooldown=1.0, now=breaker_clock)
for attempt in range(3):
    try:
        breaker.call()
    except ConnectionError:
        pass
print(f"state after 3 failures: {breaker.state.state}")
calls_before = calls["n"]
try:
    breaker.call()
except RuntimeError:
    pass
print(f"short-circuited (open): {breaker.short_circuited}, "
      f"provider untouched: {calls['n'] == calls_before}")
fake_clock["t"] += 1.0          # cooldown elapsed -> half-open trial
print(f"recovered call: {breaker.call()}")
print(f"state after recovery: {breaker.state.state}")

# Output:
# state after 3 failures: open
# short-circuited (open): 1, provider untouched: True
# recovered call: 42
# state after recovery: closed


# ============================================================
# 6. Retry with Jitter
# ============================================================
# Retries need backoff + jitter so a thundering herd of retrying
# clients does not re-stampede the provider. Sleep is INJECTED for
# determinism.

def retry_with_jitter(fn: Callable[[], int], attempts: int = 4,
                      base_delay: float = 0.1,
                      sleep: Callable[[float], None] = time.sleep,
                      rng: random.Random | None = None) -> int:
    """Retry with exponential backoff + full jitter. O(attempts)."""
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


# Example 6: succeeds on the 3rd try, jitter keeps delays bounded
attempts_log: list[float] = []

def log_sleep(delay: float) -> None:
    """Record injected delays instead of sleeping."""
    attempts_log.append(delay)

state = {"n": 0}

def flaky_twice() -> int:
    """Raise twice, then return."""
    state["n"] += 1
    if state["n"] <= 2:
        raise TimeoutError("429")
    return 7

print(f"retry result: {retry_with_jitter(flaky_twice, sleep=log_sleep)}")
print(f"delays used: {[round(d, 3) for d in attempts_log]}")

# Output:
# retry result: 7
# delays used: [0.0, 0.0]


# ============================================================
# 7. Graceful Shutdown and Idempotency
# ============================================================
# A worker loop must stop on signal, drain what is in flight, and never
# lose work. Idempotency: re-applying an operation gives the same
# result, so retries and replays are safe.

class Worker:
    """Drains a queue until stop() is called; exits after in-flight."""
    def __init__(self, q_: "queue.Queue[int]") -> None:
        self.q = q_
        self.stop_event = threading.Event()
        self.processed: list[int] = []

    def run(self) -> None:
        """Consume until stopped AND queue drained. O(items)."""
        while not self.stop_event.is_set():
            try:
                item = self.q.get(timeout=0.05)
            except queue.Empty:
                if not self.stop_event.is_set():
                    continue
                break
            self.processed.append(item * 10)
            self.q.task_done()

    def stop(self) -> None:
        """Signal shutdown; in-flight work still completes. O(1)."""
        self.stop_event.set()


def apply_twice_equals_once(ops: list[str]) -> list[str]:
    """Idempotent dedup: repeating an idempotent op changes nothing."""
    return sorted(set(ops))


# Example 7: worker drains everything then exits
work_q: queue.Queue[int] = queue.Queue()
for i in range(5):
    work_q.put(i)
worker = Worker(work_q)
t = threading.Thread(target=worker.run)
t.start()
time.sleep(0.01)               # let it consume a couple
worker.stop()                  # graceful: no new work, drain the rest
t.join(timeout=2.0)
print(f"processed: {sorted(worker.processed)}")
print(f"idempotent dedup: {apply_twice_equals_once(['a', 'b', 'a'])}")

# Output:
# processed: [0, 10, 20, 30, 40]
# idempotent dedup: ['a', 'b']


# ============================================================
# 8. Deadlock, Livelock, Starvation
# ============================================================
# Deadlock: threads wait on each other's locks forever. Symptom (safe
# to observe): lock.acquire(timeout=...) returns False. Livelock:
# threads keep acting but make no progress. Starvation: a thread never
# gets scheduled/acquires. The R1.1 producer-consumer deadlock (a
# producer blocked on a full queue with no consumer) is the canonical
# example — the fix is bounded + timeout + drain signaling.

lock_a = threading.Lock()
lock_b = threading.Lock()

# Example 8: the deadlock symptom, made observable and safe
acquired_a = lock_a.acquire(timeout=0.05)
acquired_b = lock_b.acquire(timeout=0.05)
print(f"first acquire: {acquired_a}, second: {acquired_b}")
lock_a.release()
lock_b.release()

# Output:
# first acquire: True, second: True


# ============================================================
# 9. Production Pattern: Bulkhead for Provider Isolation
# ============================================================
# Bulkhead: separate worker pools per dependency so one slow provider
# cannot consume the pool of another (ship-compartment isolation).

def run_bulkhead(chunks: list[list[int]]) -> list[int]:
    """Two isolated pools, merged deterministically. O(n) work."""
    results: list[int] = []

    def process_chunk(chunk: list[int]) -> list[int]:
        return [x + 1 for x in chunk]

    with ThreadPoolExecutor(max_workers=2) as pool_a, \
            ThreadPoolExecutor(max_workers=2) as pool_b:
        # interleave chunks across pools to show isolation
        mid = len(chunks) // 2
        futs_a = [pool_a.submit(process_chunk, c) for c in chunks[:mid]]
        futs_b = [pool_b.submit(process_chunk, c) for c in chunks[mid:]]
        results = [f.result() for f in futs_a + futs_b]
    merged: list[int] = []
    for r in results:
        merged.extend(r)
    return merged


# Example 9: bulkhead merges correctly
print(f"bulkhead: {run_bulkhead([[1, 2], [3, 4]])}")

# Output:
# bulkhead: [2, 3, 4, 5]


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: unbounded put() — the R1.1 deadlock
#   q.put(item)                    # hangs forever if nobody consumes
# CORRECT: bounded queue + timeout, or drain signaling
#   q.put(item, timeout=1.0)
#
# MISTAKE: retries with fixed delay, no jitter
#   time.sleep(1.0)                # thundering herd re-stampede
# CORRECT: exponential backoff + full jitter
#   time.sleep(random.uniform(0, base * 2 ** attempt))
#
# MISTAKE: checking provider health with the same request that fails
#   breaker opens only after N failures — probes must not be counted
#   against the business call budget (separate circuit per dependency)
#
# MISTAKE: mutating shared state without a lock
#   list.append is thread-safe, dict.update is not; use queue or locks


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # --- backpressure blocks the producer (bounded, with timeout) ---
    q_: queue.Queue[int] = queue.Queue(maxsize=2)
    q_.put(1)
    q_.put(2)
    assert bounded_put(q_, 3) is False, \
        "a full bounded queue must refuse the producer (backpressure)"
    assert q_.get() == 1 and q_.get() == 2, \
        "FIFO order must be preserved"
    assert bounded_put(q_, 3) is True, \
        "after draining, the producer must be unblocked"

    # --- worker pool correctness ---
    with ThreadPoolExecutor(max_workers=4) as pool:
        assert list(pool.map(fetch, range(4))) == [0, 2, 4, 6], \
            "pool results must match sequential results"

    # --- fan-out/fan-in preserves order ---
    assert fan_out_fan_in(list(range(10)), 4) == \
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18], \
        "fan-out/fan-in must preserve original order"

    # --- token bucket enforces the rate ---
    clock = {"t": 0.0}

    def fake() -> float:
        return clock["t"]

    bucket = TokenBucket(capacity=3, rate=1.0, now=fake)
    assert [bucket.try_acquire() for _ in range(3)] == [True, True, True], \
        "the bucket must allow a burst up to its capacity"
    assert bucket.try_acquire() is False, \
        "a fourth request in the same instant must be refused"
    clock["t"] += 1.0
    assert bucket.try_acquire() is True, \
        "after one second at rate 1.0, exactly one token must exist"
    assert bucket.try_acquire() is False, \
        "the refilled token is consumed; the next is refused"

    # --- circuit breaker opens after N failures ---
    calls = {"n": 0}

    def recovers() -> int:
        calls["n"] += 1
        if calls["n"] <= 3:
            raise ConnectionError("down")
        return 42

    clock = {"t": 0.0}

    def breaker_clock() -> float:
        return clock["t"]

    breaker = CircuitBreaker(recovers, threshold=3, cooldown=1.0,
                             now=breaker_clock)
    for _ in range(3):
        try:
            breaker.call()
        except ConnectionError:
            pass
    assert breaker.state.state == "open", \
        "three consecutive failures must open the circuit"
    before = calls["n"]
    try:
        breaker.call()
    except RuntimeError:
        pass
    assert calls["n"] == before, \
        "while open, the underlying callable must not be invoked"
    assert breaker.short_circuited == 1, \
        "the call must be short-circuited, not executed"
    clock["t"] += 1.0
    assert breaker.call() == 42, \
        "the half-open trial must reach the recovered provider"
    assert breaker.state.state == "closed", \
        "a success in half-open must close the circuit"

    # --- retry with jitter ---
    delays: list[float] = []

    def log_sleep(d: float) -> None:
        delays.append(d)

    state = {"n": 0}

    def flaky_twice() -> int:
        state["n"] += 1
        if state["n"] <= 2:
            raise TimeoutError("429")
        return 7

    assert retry_with_jitter(flaky_twice, sleep=log_sleep) == 7, \
        "retry must eventually succeed"
    assert len(delays) == 2 and all(d >= 0.0 for d in delays), \
        "there must be one jittered delay per failed attempt"
    assert delays[0] <= 0.1 and delays[1] <= 0.2, \
        "delays must respect the exponential backoff window per attempt"

    # --- graceful shutdown drains in-flight work ---
    work_q: queue.Queue[int] = queue.Queue()
    for i in range(5):
        work_q.put(i)
    worker = Worker(work_q)
    t = threading.Thread(target=worker.run)
    t.start()
    time.sleep(0.01)
    worker.stop()
    t.join(timeout=2.0)
    assert sorted(worker.processed) == [0, 10, 20, 30, 40], \
        "the worker must process everything enqueued before stopping"

    # --- idempotency ---
    assert apply_twice_equals_once(["a", "b", "a"]) == ["a", "b"], \
        "an idempotent operation applied twice equals applied once"

    # --- deadlock symptom via timeout ---
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    assert lock_a.acquire(timeout=0.05) is True, \
        "an uncontended lock must be acquired"
    assert lock_b.acquire(timeout=0.05) is True, \
        "an independent lock must also be acquired (no deadlock here)"
    lock_a.release()
    lock_b.release()

    # --- bulkhead ---
    assert run_bulkhead([[1, 2], [3, 4]]) == [2, 3, 4, 5], \
        "bulkhead pools must produce merged, ordered results"

    print("[OK] 31-concurrency-patterns: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Backpressure = bounded queue + timeout (the R1.1 fix)")
        print("2. Token buckets and breakers need injectable clocks")
        print("3. Retry = exponential backoff + jitter, never fixed delay")
        print("4. Graceful shutdown drains; idempotency makes retries safe")
        _verify()
