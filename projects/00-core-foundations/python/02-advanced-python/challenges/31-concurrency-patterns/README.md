# Challenge 31: Concurrency Patterns

Build the reliability toolkit of a batch embedding job: rate limiting,
bounded producer-consumer with backpressure, and a circuit breaker —
all deterministic via injected clocks.

## 🥉 Bronze — Token Bucket (~15 min)

**Task:** Implement `TokenBucket` with `try_acquire() -> bool`. It holds
`capacity` tokens, refilled at `rate` tokens per second. The clock is
**injected** (`now` callable, defaults to `time.monotonic`).

| Input | Expected |
|-------|----------|
| `TokenBucket(capacity=3, rate=1.0, now=fake)` + 3 calls at t=0 | `True, True, True` |
| 4th call at t=0 | `False` (bucket empty) |
| advance clock +1.0s, call | `True` (exactly 1 token refilled) |
| advance clock +100s, call | `True` and bucket still capped at capacity |

**Constraints:** n ≤ 10^6 calls. Never exceed `capacity` tokens. All tests
use a fake clock — zero sleeping.

---

## 🥈 Silver — Bounded Producer-Consumer Pipeline (~35 min)

**Task:** Implement `BoundedPipeline(maxsize: int)` — a producer-consumer
with a bounded queue and **backpressure**: the producer may not grow the
queue beyond `maxsize`, and may not block forever.

**API:**
```python
class BoundedPipeline:
    def __init__(self, maxsize: int): ...
    def produce(self, item: int, timeout: float) -> bool: ...  # False if full
    def consume(self, timeout: float) -> int | None: ...       # None if empty
    def max_observed(self) -> int: ...   # largest size the queue ever held
    def drained(self) -> bool: ...       # empty AND no producer blocked
```

| Input | Expected |
|-------|----------|
| `produce` 1,2,3 into maxsize=2 | `True, True, False` (backpressure) |
| after `consume`, `produce` again | `True` |
| `max_observed` after 100 produces/consumes with maxsize=5 | `<= 5` |
| mixed produce/consume, all drained | `drained() == True`, no item lost |

**Constraints:** n ≤ 10^3 items. `produce` must return `False` within
`timeout` — never hang. `consume` returns items in FIFO order.

---

## 🥇 Gold — Circuit Breaker + Retry with Jitter (~75 min)

**Task:** Implement `CircuitBreaker(fn, threshold, cooldown, now)` with
states `closed → open → half_open` and a `retry_with_jitter(fn, attempts,
base_delay, sleep, rng)` helper. Both must be fully deterministic.

**API:**
```python
class CircuitBreaker:
    def call(self) -> int: ...                    # raises RuntimeError when open
    @property
    def state(self) -> str: ...                   # closed | open | half_open
    @property
    def short_circuited(self) -> int: ...         # calls rejected while open

def retry_with_jitter(fn, attempts=4, base_delay=0.1,
                      sleep=time.sleep, rng=None) -> int: ...
```

| Input | Expected |
|-------|----------|
| 3 failures with threshold=3 | `state == "open"` |
| call while open | raises `RuntimeError`, `short_circuited` += 1, `fn` NOT invoked |
| clock += cooldown, call succeeds | `state == "closed"`, result returned |
| clock += cooldown, call fails | `state == "open"` again |
| `retry_with_jitter` fn fails twice then returns 7 | returns `7`; 2 delays recorded, each `<= base * 2 ** attempt` |
| `retry_with_jitter` always fails | raises `RuntimeError` after `attempts` invocations |

**Constraints:** `fn` must never be invoked while the circuit is open
(assert via a counting wrapper). All timing via injected `now`/`sleep` —
tests run in milliseconds. n ≤ 10^3 calls.

**Follow-up:** how would you add bulkheads (per-dependency pools) and
idempotent retries (content-hash keys) on top of these two pieces?

---

## Running

```bash
pytest challenges/31-concurrency-patterns/test_challenge.py -v
```
