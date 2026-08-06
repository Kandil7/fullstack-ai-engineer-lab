# 31 — Concurrency Patterns Glossary

## Quick Reference

| Term | Definition | Complexity |
|---|---|---|
| Backpressure | Slowing or refusing the producer when a buffer is full, instead of growing memory without bound | O(1) |
| Bounded queue | A queue with a fixed `maxsize`; producers block/time out when full | put/get O(1) |
| Producer-consumer | Pattern where producers enqueue work and consumers dequeue and process it | O(1) per transfer |
| Worker pool | A fixed set of threads that execute queued tasks (`ThreadPoolExecutor`) | submit O(1) |
| Fan-out | Splitting one batch into chunks processed in parallel | O(n) work |
| Fan-in | Merging partial results back into one ordered result | O(n) work |
| Token bucket | Rate limiter: capacity tokens, refilled at a rate per second | O(1) |
| Injectable clock | Passing `now=...`/`sleep=...` so time-dependent code is testable | — |
| Circuit breaker | Fails fast after N failures; half-open probes recovery after cooldown | O(1) |
| Closed state | Breaker normal: calls pass through, failures counted | O(1) |
| Open state | Breaker fail-fast: calls rejected without touching the dependency | O(1) |
| Half-open state | One trial call allowed after cooldown; success closes, failure reopens | O(1) |
| Short-circuit | Rejecting a call because the circuit is open | O(1) |
| Retry | Re-attempting a transient failure a bounded number of times | O(attempts) |
| Exponential backoff | Delay doubles per attempt: `base * 2 ** attempt` | O(1) per delay |
| Full jitter | Random delay in `[0, window]` to desynchronize retrying clients | O(1) |
| Graceful shutdown | Stop accepting new work, drain in-flight work, then exit | O(work) |
| Idempotency | Re-applying an operation yields the same result as applying once | O(1) per op |
| Deadlock | Threads wait on each other forever; no progress possible | — |
| Livelock | Threads keep acting but never make progress | — |
| Starvation | A ready thread never gets to run/acquire | — |
| Bulkhead | Isolated worker pools per dependency so one slow provider cannot exhaust another's | O(1) |
| Condition variable | `threading.Condition`: wait + notify for blocking coordination | O(1) |
| R1.1 | This repo's deadlock: bounded producer/consumer that hangs when run on one thread | — |

## Detailed Definitions

### Backpressure
**Definition:** The mechanism by which a slow consumer slows down a fast
producer: when the buffer is full, the producer blocks (or times out)
instead of the system buffering without bound. An unbounded queue between a
fast loader and a slow embedding API is a memory leak with a deadline.

```python
import queue

q = queue.Queue(maxsize=2)
q.put(1)
q.put(2)
try:
    q.put(3, timeout=0.05)          # full -> blocks, then raises
except queue.Full:
    print("producer refused (backpressure)")
```

```text
# Output:
# producer refused (backpressure)
```

**Related Terms:** Bounded queue, Producer-consumer, R1.1

### Bounded queue
**Definition:** `queue.Queue(maxsize=n)` — a thread-safe FIFO whose `put`
blocks (or times out) once `n` items are queued. The bound is what turns an
unbounded memory growth into a controllable stop. Fixing R1.1 means the
queue has a bound *and* every `put` carries a timeout.

```python
q = queue.Queue(maxsize=2)

def bounded_put(q_, item, timeout=0.05):
    try:
        q_.put(item, timeout=timeout)
        return True
    except queue.Full:
        return False

print(bounded_put(q, 1), bounded_put(q, 2), bounded_put(q, 3))
```

```text
# Output:
# True True False
```

**Related Terms:** Backpressure, Producer-consumer

### Producer-consumer
**Definition:** The pattern where one or more producers enqueue work items
and one or more consumers dequeue and process them, decoupled by a queue.
The R1.1 bug was a producer-consumer where producer and consumer ran on the
*same thread*, so the producer's blocking wait could never be satisfied.

```python
import queue

q = queue.Queue(maxsize=3)
for i in range(3):
    q.put(i)                    # producer side
while not q.empty():
    print(q.get())              # consumer side (same thread, but never full)
```

```text
# Output:
# 0
# 1
# 2
```

**Related Terms:** Bounded queue, Worker pool, R1.1

### Worker pool
**Definition:** A fixed set of threads that execute tasks from an internal
queue. `ThreadPoolExecutor(max_workers=k)` caps concurrency at `k`; `map`
preserves input order in results.

```python
import time
from concurrent.futures import ThreadPoolExecutor

def fetch(x):
    time.sleep(0.01)
    return x * 2

with ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(fetch, range(4))))
```

```text
# Output:
# [0, 2, 4, 6]
```

**Related Terms:** Fan-out, Fan-in, Bulkhead

### Fan-out / Fan-in
**Definition:** Fan-out splits a batch into chunks processed in parallel;
fan-in merges the partial results back in the original order. This is how
10,000 chunks get embedded without 10,000 sequential round-trips.

```python
from concurrent.futures import ThreadPoolExecutor

def fan_out_fan_in(items, workers):
    chunk_size = max(1, len(items) // workers)
    chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        partials = list(pool.map(lambda c: [x * 2 for x in c], chunks))
    merged = []
    for part in partials:
        merged.extend(part)
    return merged

print(fan_out_fan_in([1, 2, 3, 4], 2))
```

```text
# Output:
# [2, 4, 6, 8]
```

**Related Terms:** Worker pool, Fan-in, Fan-out

### Token bucket
**Definition:** A rate limiter holding `capacity` tokens, refilled at
`rate` tokens/second. Each request spends one token; empty bucket = refused.
Allows bursts up to capacity, then enforces the steady rate. The clock is
injected so tests run instantly.

```python
class TokenBucket:
    def __init__(self, capacity, rate, now=time.monotonic):
        self.capacity = capacity
        self.rate = rate
        self._now = now
        self.tokens = float(capacity)
        self.last_refill = now()

    def try_acquire(self):
        elapsed = self._now() - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = self._now()
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False
```

**Related Terms:** Rate limiting, Injectable clock

### Injectable clock
**Definition:** Passing `now=...` (for time) and `sleep=...` (for delays)
into time-dependent code, so tests control time instead of sleeping. Every
rate limiter, breaker, and retry in this topic uses it; this is what makes
the exercises run in milliseconds and never flake on CI.

```python
fake = {"t": 0.0}

def fake_clock():
    return fake["t"]

bucket = TokenBucket(capacity=2, rate=1.0, now=fake_clock)
fake["t"] += 0.5
print(bucket.try_acquire())
```

```text
# Output:
# True
```

**Related Terms:** Token bucket, Circuit breaker, Retry

### Circuit breaker
**Definition:** A state machine wrapping a fragile callable: closed (normal,
count failures), open (fail fast, do not touch the dependency), half-open
(after cooldown, one trial call decides). Protects both your latency and the
failing provider.

```python
# states: closed -> (N failures) -> open -> (cooldown) -> half_open
# half-open success -> closed ; half-open failure -> open
```

**Related Terms:** Closed state, Open state, Half-open state, Short-circuit

### Closed state
**Definition:** Breaker normal mode: every call reaches the dependency;
failures are counted; reaching the threshold opens the circuit.

**Related Terms:** Circuit breaker, Open state

### Open state
**Definition:** Breaker fail-fast mode: calls raise immediately without
invoking the dependency, until `open_until` elapses. The `short_circuited`
counter records how many calls were rejected this way.

**Related Terms:** Circuit breaker, Short-circuit

### Half-open state
**Definition:** Breaker probe mode: after the cooldown, exactly one trial
call is allowed. Success closes the circuit (dependency recovered);
failure reopens it (still down, cooldown restarts).

**Related Terms:** Circuit breaker, Open state

### Short-circuit
**Definition:** Rejecting a call instantly because the circuit is open —
the dependency is never touched. This is what converts "wait for the
provider timeout" into "fail in microseconds".

**Related Terms:** Circuit breaker, Open state

### Retry
**Definition:** Re-attempting an operation a bounded number of times, only
for *transient* failures (429, 5xx, network). Never retry 4xx client
errors. Each retry sleeps `uniform(0, base * 2 ** attempt)` (full jitter).

```python
def retry_with_jitter(fn, attempts=4, base_delay=0.1, sleep=time.sleep,
                      rng=None):
    rng = rng or random.Random(0)
    last_error = None
    for attempt in range(attempts):
        try:
            return fn()
        except Exception as exc:
            last_error = exc
            if attempt + 1 < attempts:
                sleep(rng.uniform(0.0, base_delay * (2 ** attempt)))
    raise RuntimeError(f"failed after {attempts} attempts: {last_error}")
```

**Related Terms:** Exponential backoff, Full jitter

### Exponential backoff
**Definition:** Growing the retry delay window per attempt: `base_delay *
2 ** attempt` (e.g. 0.1, 0.2, 0.4, 0.8). Combined with jitter, it prevents
re-stampeding the provider.

**Related Terms:** Retry, Full jitter

### Full jitter
**Definition:** Choosing the delay uniformly in `[0, window]` instead of
using the full window. Randomized delays desynchronize a thundering herd of
clients that would otherwise all retry at the same fixed times.

**Related Terms:** Retry, Exponential backoff

### Graceful shutdown
**Definition:** Signaling a worker to stop accepting *new* work, draining
*in-flight* work, and only then exiting. Implemented with an `Event` + a
`get(timeout=...)` loop that exits when the event is set and the queue is
empty.

```python
import queue
import threading

class Worker:
    def __init__(self, q_):
        self.q = q_
        self.stop_event = threading.Event()
        self.processed = []

    def run(self):
        while not self.stop_event.is_set():
            try:
                item = self.q.get(timeout=0.05)
            except queue.Empty:
                continue
            self.processed.append(item)
            self.q.task_done()
```

**Related Terms:** Idempotency, Worker pool

### Idempotency
**Definition:** An operation whose re-application gives the same result as
a single application. Makes retries and job restarts safe: re-processing a
chunk is a no-op when writes are keyed by content hash.

```python
def apply_twice_equals_once(ops):
    return sorted(set(ops))

print(apply_twice_equals_once(["a", "b", "a"]))
```

```text
# Output:
# ['a', 'b']
```

**Related Terms:** Graceful shutdown, Retry

### Deadlock
**Definition:** A state where threads wait on each other forever and no
progress is possible. R1.1 is the repo's canonical deadlock: a producer
blocked inside `not_full.wait()` on a full buffer while the only consumer
is the same blocked thread. The fix: bounded waits (`timeout=`) or proven
concurrent consumer threads.

```python
lock = threading.Lock()
# lock.acquire(timeout=0.05) returns False instead of hanging forever
```

**Related Terms:** Livelock, Starvation, R1.1

### Livelock
**Definition:** Threads keep *acting* — retrying, yielding, responding to
each other — but never make progress (two polite robots each waiting for
the other to go first). Unlike deadlock, CPU stays busy; like deadlock,
nothing completes. Fix: give up after a bounded number of attempts.

**Related Terms:** Deadlock, Starvation

### Starvation
**Definition:** A thread is runnable but never gets the resource it needs —
never scheduled, or every `get()` finds the queue empty because higher
priority consumers drain it. Fix: fairness mechanisms (e.g. priority-aware
queues, aging).

**Related Terms:** Deadlock, Livelock

### Bulkhead
**Definition:** Isolating dependencies into separate worker pools so a slow
or dead provider cannot consume the pool capacity of a healthy one. The
name comes from ship compartments: one flooded room does not sink the
whole ship.

```python
# pool_a for provider A, pool_b for provider B:
# provider A hanging does not starve provider B's workers
```

**Related Terms:** Worker pool, Circuit breaker

### Condition variable
**Definition:** `threading.Condition` — a lock plus `wait()`/`notify()`
primitives for blocking coordination. Correct but dangerous: `wait()` blocks
until *some other thread* calls `notify()`. R1.1's bug was using it without
proving that other thread exists.

**Related Terms:** Deadlock, R1.1

### R1.1
**Definition:** This repo's first recorded hang: the bounded producer/
consumer in `06-data-structures-algorithms/04-queues.py`. Producer and
consumer ran on the same thread, so `produce()` blocked forever on a full
buffer; CI killed it at the 30-second timeout (exit 124). The correct
pattern — bounded queue + timeout, or real concurrent threads — is this
topic's central worked example.

```python
# The fix shape:
# q = queue.Queue(maxsize=n)
# q.put(item, timeout=t)   -> queue.Full instead of a hang
```

**Related Terms:** Deadlock, Bounded queue, Producer-consumer

## Key Concepts Summary

1. **Bounded waits defeat the three failure modes.** Deadlock, livelock,
   and starvation are all "waiting forever" in different disguises. Every
   `wait()`, `put()`, `get()`, `acquire()` gets a timeout or cancellation
   path — that alone kills the R1.1 class of bugs.
2. **Backpressure is memory protection.** The bound on the queue is the
   cap on memory between producer and consumer. No bound = unbounded
   growth; bounded + timeout = catchable, recoverable.
3. **Inject time.** Clock injection (`now=`, `sleep=`) is what lets token
   buckets, breakers, and retries be tested in milliseconds with zero
   flakiness.
4. **Fail fast beats retry-only.** A circuit breaker protects the provider
   from your retries and protects your latency from the provider's
   timeouts. They compose: breaker + retry-with-jitter = survive transient
   issues, fail fast on real ones.
5. **Graceful + idempotent = crash-safe.** Drain on shutdown, dedupe by
   content hash on restart. Batch jobs become resumable instead of
   re-runnable.

## Practice Terms

1. **Define backpressure and give the R1.1 connection.**
   *Answer:* Backpressure refuses or blocks the producer when the buffer is
   full. R1.1 was a producer blocked *forever* on a full buffer because the
   consumer never ran — bounded queue + timeout is the backpressure that
   converts that hang into a catchable `queue.Full`.
2. **Why does the breaker count `short_circuited`?**
   *Answer:* To observe fail-fast behavior without touching the dependency:
   each rejected call is counted instead of invoking `fn`, so tests can
   assert the provider stayed untouched while the circuit was open.
3. **Why jitter, not fixed delay?**
   *Answer:* Fixed delays synchronize retrying clients into a thundering
   herd that re-stampedes the provider at the same instants. Random delays
   in the backoff window desynchronize them.
4. **When are threads the wrong tool?**
   *Answer:* For CPU-bound work — the GIL serializes Python bytecode, so a
   thread pool on pure computation adds overhead. Threads are for
   I/O-bound work (sockets, files, APIs); CPU work belongs in processes or
   native libraries.
5. **What does graceful shutdown guarantee?**
   *Answer:* No new work is accepted, all in-flight (already-queued) work
   completes, and the thread exits — so no item is lost and the job can
   resume idempotently on restart.
