# 31 — Concurrency Patterns Lecture

## 1. Topic Overview

Concurrency is not about running things "at the same time" — it is about
**coordination under constraints**: a provider that allows 10 requests per
second, a model endpoint that returns 429s, a batch job that must finish
before the SLA, a queue that must not grow to 10 GB. The patterns in this
topic are the *reusable shapes* for that coordination:

- **Producer-consumer** with bounded queues and backpressure
- **Worker pools** with bounded concurrency
- **Fan-out / fan-in** for parallel batch processing
- **Rate limiting** with a token bucket
- **Circuit breaker** for failing-fast on degraded dependencies
- **Bulkhead** for isolating slow dependencies from each other
- **Retry with backoff + jitter** for transient failures
- **Graceful shutdown and idempotency** for crash-safe jobs

This topic is the threading complement to `04-async-await.py` and
`22-asyncio-advanced.py`. Where asyncio handles thousands of cooperative
coroutines on one thread, these patterns manage **preemptive threads** whose
scheduling you cannot control — which is exactly why the patterns exist: to
make uncontrolled scheduling behave predictably.

The worked example is **R1.1**, a real deadlock found in this repo's own
`06-data-structures-algorithms/04-queues.py`. It is the best teacher this
topic has: a bounded buffer with condition variables that hangs forever when
the producer and consumer do not actually run concurrently. We will dissect
it, then build the version that cannot hang.

## 2. Learning Objectives

By the end of this lecture you will be able to:

1. Explain backpressure and implement a producer-consumer pipeline with a
   bounded queue whose producer *blocks or times out* instead of growing
   memory without limit.
2. Diagnose the R1.1 deadlock shape: a producer waiting forever on a full
   queue because no consumer is scheduled to drain it.
3. Use `ThreadPoolExecutor` with a bounded number of workers, and describe
   when threads are the right tool (I/O-bound) vs. when they are not
   (CPU-bound, due to the GIL).
4. Implement fan-out/fan-in so parallel chunks merge in deterministic order.
5. Build a token bucket with an **injectable clock** and a circuit breaker
   with closed/open/half-open states.
6. Implement retry with exponential backoff and full jitter.
7. Implement graceful shutdown (drain in-flight work) and explain why
   idempotency makes retries and replays safe.
8. Distinguish deadlock, livelock, and starvation, and give the fix for each.

## 3. Prerequisites

- **Phase 1 fundamentals**: functions, classes, exceptions, generators.
- **`02-generators.py`** — generator-based pipelines feed producer-consumer.
- **`16-threading.py`** — `threading.Thread`, `Lock`, `Event`, `queue.Queue`.
- **`21-concurrency-comparison`** and **`22-asyncio-advanced`** — know when
  threads beat asyncio and vice versa.
- **`06-data-structures-algorithms/04-queues.py`** — the R1.1 bounded buffer
  (read it *before* this lecture; we reference it throughout).

## 4. Key Concepts

### 4.1 The R1.1 Deadlock — a Real Bug from This Repo

`06-data-structures-algorithms/04-queues.py` contains a `BoundedBuffer` built
on condition variables:

```python
import threading
from collections import deque

class BoundedBuffer:
    """Thread-safe bounded buffer (producer-consumer problem)"""

    def __init__(self, capacity):
        self.buffer = deque()
        self.capacity = capacity
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def produce(self, item):
        with self.not_full:
            while len(self.buffer) >= self.capacity:
                self.not_full.wait()       # <-- BLOCKS HERE, forever
            self.buffer.append(item)
            self.not_empty.notify()

    def consume(self):
        with self.not_empty:
            while not self.buffer:
                self.not_empty.wait()
            item = self.buffer.popleft()
            self.not_full.notify()
            return item
```

**The bug:** `produce()` and `consume()` are correct *only if they run in
different threads*. The original demo called both on the **same thread**:

```python
buffer = BoundedBuffer(3)
for i in range(5):
    buffer.produce(i)          # blocks forever on the 4th item!
```

`produce()` fills the buffer to capacity 3, then waits on `not_full` for a
consumer that will never run — **because the same thread is still inside
`produce()`**. The program hangs. In CI it hit the 30-second timeout and
died with exit code 124 (`run_smoke_tests.py` records it as R1.1).

```text
# Output (the hang — never returns):
# produce(3) -> blocks inside not_full.wait() forever
# process killed by CI timeout (exit 124)
```

**Lesson:** a blocking `wait()` is only safe when you can *prove* another
thread will eventually call the matching `notify()`. That proof is exactly
what concurrency patterns formalize.

### 4.2 The Fix: `queue.Queue` with a Bound and a Timeout

`queue.Queue` is the battle-tested bounded buffer: a lock + condition
variable pair you do not have to get right. The two R1.1-killers are gone
when you add a **timeout**:

```python
import queue

q = queue.Queue(maxsize=2)     # the bound = the backpressure limit

def bounded_put(q_: queue.Queue, item: int, timeout: float = 0.05) -> bool:
    """Try to enqueue; return False instead of hanging forever. O(1)."""
    try:
        q_.put(item, timeout=timeout)
        return True
    except queue.Full:
        return False

q.put(1)
q.put(2)
print(bounded_put(q, 3))       # full -> returns False, does NOT hang
print(q.get(), q.get())        # drain
print(bounded_put(q, 3))       # now there is room -> True
```

```text
# Output:
# False
# 1 2
# True
```

**Backpressure defined:** when the buffer is full, the producer is *slowed
down* (blocked) or *refused* (timeout) rather than the system buffering
without bound. An unbounded queue between a document loader and an embedding
service is "a memory leak with a deadline" — the queue grows at the
producer's rate, which is faster than the network-bound consumer's rate.
Bounded + timeout keeps memory flat and turns a hang into a catchable
`queue.Full`.

### 4.3 Worker Pools: Bounded Concurrency

`ThreadPoolExecutor` caps how many threads exist, so 1,000 documents never
create 1,000 threads:

```python
import time
from concurrent.futures import ThreadPoolExecutor

def fetch(url_id: int) -> int:
    time.sleep(0.01)            # simulated network latency
    return url_id * 2

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch, range(8)))
print(results)
```

```text
# Output:
# [0, 2, 4, 6, 8, 10, 12, 14]
```

- `pool.map` preserves input order in the results — deterministic.
- `max_workers=4` means at most 4 in-flight requests, no matter the batch.
- The `with` block calls `shutdown(wait=True)` on exit: it *drains* queued
  work before returning.

**Threads vs. processes reminder:** threads are right for I/O-bound work
(waiting on sockets, files, APIs). For CPU-bound math (tokenization of a
huge corpus, feature computation), the GIL serializes Python bytecode, so
use `multiprocessing` (topic 17) or a native library. A thread pool on CPU
work gives you *more overhead*, not more throughput.

### 4.4 Fan-Out / Fan-In

Fan-out splits one batch into chunks processed in parallel; fan-in merges
the partial results back into one ordered result:

```python
from concurrent.futures import ThreadPoolExecutor

def fan_out_fan_in(items, workers):
    chunk_size = max(1, len(items) // workers)
    chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        partials = list(pool.map(lambda c: [x * 2 for x in c], chunks))
    merged = []
    for part in partials:
        merged.extend(part)      # chunks re-merged in submission order
    return merged

print(fan_out_fan_in(list(range(10)), 4))
```

```text
# Output:
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

**Why this matters for AI:** embedding a 10,000-chunk corpus is fan-out
(chunks → parallel embed calls) + fan-in (embeddings → one vector store
insert). Order preservation matters when chunk positions define context
windows. The deterministic merge above is the pattern vector stores assume.

### 4.5 Rate Limiting: Token Bucket

A token bucket allows bursts up to `capacity`, then enforces a steady
`rate`. Every request spends a token; tokens refill at `rate` per second.

```python
import time
from typing import Callable

class TokenBucket:
    def __init__(self, capacity: int, rate: float,
                 now: Callable[[], float] = time.monotonic):
        self.capacity = capacity
        self.rate = rate
        self._now = now
        self.tokens = float(capacity)
        self.last_refill = now()

    def _refill(self):
        elapsed = self._now() - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = self._now()

    def try_acquire(self) -> bool:
        self._refill()
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False
```

**The clock is injected** (`now=...`), which makes it testable without
sleeping: `time.monotonic` in production, a fake clock in tests:

```python
fake_now = {"t": 0.0}

def fake_clock() -> float:
    return fake_now["t"]

bucket = TokenBucket(capacity=3, rate=1.0, now=fake_clock)
print([bucket.try_acquire() for _ in range(3)])   # burst of 3 allowed
print(bucket.try_acquire())                        # 4th -> refused
fake_now["t"] += 1.0                               # 1 second passes
print(bucket.try_acquire())                        # exactly 1 token
```

```text
# Output:
# [True, True, True]
# False
# True
```

**AI hook:** embedding providers publish rate limits (e.g. 3,000 RPM). A
token bucket in front of the client means your batch job stays inside the
contract and gets no 429s — and when you *do* get one, the retry pattern in
4.7 decides what happens next.

### 4.6 Circuit Breaker: Fail Fast, Recover Slowly

A breaker wraps a fragile callable and tracks failures. After `threshold`
consecutive failures it **opens**: subsequent calls fail immediately without
touching the dependency. After `cooldown`, it goes **half-open** and allows
one trial call; success closes it, failure reopens it.

```python
class CircuitBreaker:
    def __init__(self, fn, threshold=3, cooldown=1.0,
                 now=time.monotonic):
        self.fn = fn
        self.threshold = threshold
        self.cooldown = cooldown
        self._now = now
        self.failures = 0
        self.state = "closed"        # closed | open | half_open
        self.open_until = 0.0
        self.short_circuited = 0

    def call(self):
        now = self._now()
        if self.state == "open":
            if now >= self.open_until:
                self.state = "half_open"
            else:
                self.short_circuited += 1
                raise RuntimeError("circuit open")
        try:
            result = self.fn()
        except Exception:
            self.failures += 1
            if self.failures >= self.threshold:
                self.state = "open"
                self.open_until = now + self.cooldown
            raise
        self.failures = 0
        self.state = "closed"
        return result
```

Demo with a fake clock — no waiting:

```python
calls = {"n": 0}

def flaky():
    calls["n"] += 1
    if calls["n"] <= 3:
        raise ConnectionError("provider down")
    return 42

fake_clock = {"t": 0.0}

def breaker_clock():
    return fake_clock["t"]

breaker = CircuitBreaker(flaky, threshold=3, cooldown=1.0, now=breaker_clock)
for _ in range(3):
    try:
        breaker.call()
    except ConnectionError:
        pass
print(breaker.state)                        # open after 3 failures
before = calls["n"]
try:
    breaker.call()
except RuntimeError:
    pass
print(breaker.short_circuited, calls["n"] == before)   # fail fast, provider untouched
fake_clock["t"] += 1.0                      # cooldown elapsed
print(breaker.call())                       # half-open trial succeeds
print(breaker.state)                        # closed again
```

```text
# Output:
# open
# 1 True
# 42
# closed
```

**Why a breaker beats "just retry":** when a model endpoint is down, every
retry *adds load to the thing that is failing*. The breaker converts "call
the broken provider and wait for its timeout" into "fail in microseconds".
That protects both your latency SLA and the provider's recovery.

### 4.7 Retry with Exponential Backoff + Jitter

Transient failures (429, 503, connection reset) deserve retries; permanent
ones do not. The retry must **back off** so you do not re-stampede, and
**jitter** so thousands of clients retrying at the same fixed delay do not
synchronize into waves.

```python
import random

def retry_with_jitter(fn, attempts=4, base_delay=0.1,
                      sleep=time.sleep, rng=None):
    rng = rng or random.Random(0)
    last_error = None
    for attempt in range(attempts):
        try:
            return fn()
        except Exception as exc:
            last_error = exc
            if attempt + 1 < attempts:
                delay = rng.uniform(0.0, base_delay * (2 ** attempt))
                sleep(delay)
    raise RuntimeError(f"failed after {attempts} attempts: {last_error}")
```

The `sleep` parameter is injected so tests observe delays instead of
waiting:

```python
delays = []

def log_sleep(d):
    delays.append(d)

state = {"n": 0}

def flaky_twice():
    state["n"] += 1
    if state["n"] <= 2:
        raise TimeoutError("429")
    return 7

print(retry_with_jitter(flaky_twice, sleep=log_sleep))
print(delays)   # attempt 0 window [0, 0.1], attempt 1 window [0, 0.2]
```

```text
# Output:
# 7
# [0.084..., 0.152...]
```

**Rules of thumb:** retry *only* on transient errors (429/5xx/network),
never on 4xx; cap attempts (3–5); cap the max delay; add full jitter
(`uniform(0, base * 2 ** attempt)`) to desynchronize clients.

### 4.8 Graceful Shutdown and Idempotency

A worker must stop on signal **without losing in-flight work**. The pattern
is: a `stop()` that sets an `Event`, and a loop that checks it between
`get(timeout=...)` calls — so it exits when stopped **and** the queue is
drained:

```python
import threading
import queue

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
            self.processed.append(item * 10)
            self.q.task_done()

    def stop(self):
        self.stop_event.set()

work_q = queue.Queue()
for i in range(5):
    work_q.put(i)
worker = Worker(work_q)
t = threading.Thread(target=worker.run)
t.start()
time.sleep(0.01)          # let it consume a couple of items
worker.stop()             # graceful: no NEW work, drain the REST
t.join(timeout=2.0)
print(sorted(worker.processed))
```

```text
# Output:
# [0, 10, 20, 30, 40]
```

**Idempotency** makes the retries and replays above safe: an operation that
produces the same result no matter how many times it is applied can be
retried without duplication.

```python
def apply_twice_equals_once(ops):
    """Idempotent dedup: repeating an idempotent op changes nothing."""
    return sorted(set(ops))

print(apply_twice_equals_once(["a", "b", "a"]))
```

```text
# Output:
# ['a', 'b']
```

**AI hook:** batch embedding jobs crash mid-run. On restart, the job
re-processes everything *unless* embeddings are keyed by content hash — an
idempotent write (upsert by hash) makes the replay a no-op for completed
chunks.

### 4.9 Deadlock, Livelock, Starvation — the Failure Modes

- **Deadlock** — threads wait on each other forever. The R1.1 producer
  blocked on a full queue with no consumer is a deadlock. Symptom you can
  observe safely: `lock.acquire(timeout=...)` returns `False`.
- **Livelock** — threads keep *acting* (retrying, yielding) but never make
  progress. Two processes each "wait for the other to go first" forever.
- **Starvation** — a thread is *ready* but never gets scheduled/acquires,
  e.g. a low-priority consumer that never sees a non-empty queue.

All three share one prevention theme: **make waiting bounded**. Every
`wait()`, `put()`, `get()`, `acquire()` gets a timeout or a cancellation
path, so "waiting forever" is structurally impossible.

```python
lock_a = threading.Lock()
lock_b = threading.Lock()
print(lock_a.acquire(timeout=0.05))   # uncontended -> True, never hangs
print(lock_b.acquire(timeout=0.05))
lock_a.release()
lock_b.release()
```

```text
# Output:
# True
# True
```

### 4.10 Bulkhead: Isolate Dependencies

A bulkhead gives each dependency its own worker pool, so one slow provider
cannot exhaust the pool of another (ship compartments: one flooded room
does not sink the ship):

```python
from concurrent.futures import ThreadPoolExecutor

def run_bulkhead(chunks):
    results = []
    with ThreadPoolExecutor(max_workers=2) as pool_a, \
            ThreadPoolExecutor(max_workers=2) as pool_b:
        mid = len(chunks) // 2
        futs_a = [pool_a.submit(lambda c: [x + 1 for x in c], c)
                  for c in chunks[:mid]]
        futs_b = [pool_b.submit(lambda c: [x + 1 for x in c], c)
                  for c in chunks[mid:]]
        results = [f.result() for f in futs_a + futs_b]
    merged = []
    for r in results:
        merged.extend(r)
    return merged

print(run_bulkhead([[1, 2], [3, 4]]))
```

```text
# Output:
# [2, 3, 4, 5]
```

## 5. Common Mistakes

1. **Unbounded `put()` — the R1.1 hang.** `q.put(item)` on a full queue
   blocks forever. Always `put(item, timeout=...)` and handle `queue.Full`,
   or make the queue's bound explicit and documented.
2. **Producer and consumer on the same thread.** Any blocking `wait()` with
   no other thread to `notify()` is a guaranteed deadlock (R1.1's exact
   shape). If you must run them together, use non-blocking timeouts.
3. **Fixed-delay retries.** `time.sleep(1.0)` between retries synchronizes a
   thundering herd — everyone retries at the same instant. Backoff + jitter
   is the fix.
4. **No circuit breaker, retries only.** Retrying a dead provider adds load
   to the failure. Fail fast after N failures, then probe with half-open.
5. **Threads for CPU-bound work.** The GIL serializes bytecode; a thread
   pool on pure computation is slower than sequential. Use processes or
   native libs.
6. **Testing with wall-clock asserts.** `assert elapsed < 0.5` is flaky on
   CI. Inject the clock (`now=`) and the sleep (`sleep=`) — the patterns in
   4.5 and 4.7 are deterministic because of this.
7. **Stopping a worker with `terminate`-style hacks.** Killing a thread
   mid-write loses data. Graceful shutdown (Event + drain) is the only
   crash-safe stop.

## 6. Best Practices

- **Every wait is bounded**: `get(timeout=)`, `put(timeout=)`,
  `acquire(timeout=)`, `join(timeout=)`. An unbounded wait is a bug waiting
  for a deadline.
- **Share state only through `queue.Queue` or futures results**, never bare
  globals. If you must mutate shared objects, hold one `Lock` for the
  critical section and nothing else.
- **Size pools to the waiting, not the cores**: 4 workers for 3,000 RPM
  provider = 4 in-flight requests. 64 workers on a 1-RPS provider just
  queues.
- **One circuit per dependency** (embedding provider, reranker, vector
  store), each with its own threshold/cooldown.
- **Inject time everywhere** (`now`, `sleep`): determinism is a testing
  superpower.
- **Log state transitions** (open/closed/half-open, retry attempts) — they
  are the first thing you grep in an incident.
- **Idempotent writes by content hash** make every retry and restart safe.

## 7. Complexity and Cost

| Pattern | Time (per op) | Space | Failure cost when wrong |
|---|---|---|---|
| Bounded queue put/get | O(1) | O(bound) | Hang (R1.1) or OOM |
| ThreadPoolExecutor | O(1) submit | O(workers + queue) | Thread explosion |
| Token bucket | O(1) | O(1) | 429 storms / SLA breach |
| Circuit breaker | O(1) | O(1) | Latency pile-up |
| Retry w/ jitter | O(attempts) | O(1) | Re-stampede |
| Fan-out/fan-in | O(n) work | O(n) buffers | Order corruption |

**Scale notes:** at 10k documents, an unbounded queue between chunking and
embedding grows to gigabytes while the embedding provider crawls at its
rate limit; the bounded queue's backpressure keeps memory flat. At 200
concurrent calls, one retry storm multiplies provider load by the number of
clients — the breaker converts that into microsecond failures. The
primitives are the same at every scale; the cost of getting them wrong
grows linearly with the concurrency.

## 8. AI Engineering Relevance

This topic is the reliability layer of every batch and online ML system:

- **Batch embedding jobs** = producer-consumer: load documents → bound the
  queue → fan out to the provider → token-bucket the requests → retry with
  jitter → breaker per provider → bulkhead per dependency → graceful
  shutdown on kill signal → resume idempotently.
- **RAG ingestion pipelines** are the same shape with chunking as the
  producer and the vector store as the consumer.
- **Online serving** (a chat API with a model backend) uses the breaker
  pattern to fail fast with a canned response instead of piling up requests
  when the model is down.
- **Evaluation harnesses** calling a paid LLM API literally save money per
  token bucket: `capacity` = burst, `rate` = your RPM contract.
- The R1.1 lesson transfers directly: any pipeline where the producer can
  outrun the consumer needs a bounded buffer, or it will hang (batch) or
  OOM (stream).

## 9. Practice Exercises

1. **Bounded pipeline (R1.1 fix):** build `Pipeline(load, embed, maxsize=4)`
   where `load` produces and `embed` consumes, using `queue.Queue(maxsize=4)`
   and `put(timeout=0.1)`. Assert that when the consumer is slow, the
   producer's `put` raises `queue.Full` instead of the queue exceeding 4.
2. **Token bucket against a fake clock:** implement `TokenBucket` and assert
   burst = capacity, refusal at 0 tokens, exactly `rate` tokens after 1s,
   and that tokens never exceed capacity. No sleeps anywhere.
3. **Circuit breaker state machine:** drive closed → open → half-open →
   closed with a fake clock and a stub callable; assert the provider is
   untouched while open.
4. **Retry with recorded delays:** inject `sleep`, make a callable fail
   twice then succeed, and assert the recorded delays are within the
   exponential windows `[0, base*2^attempt]`.
5. **Graceful drain:** enqueue 50 items, stop the worker after ~10, assert
   all 50 are processed (drain completes) and the thread exits.
6. **Deadlock demo turned test:** with `acquire(timeout=)`, assert that the
   R1.1 same-thread producer-consumer *would* hang by showing the bounded
   `put` returns False (the timeout path) instead of blocking.

## 10. Summary

- **Backpressure** = bounded queue + timeout; it is the fix for R1.1's
  deadlock and for unbounded memory in pipelines.
- **Worker pools** bound concurrency; threads are for I/O-bound work only.
- **Fan-out/fan-in** parallelizes batches while preserving order.
- **Token bucket** enforces provider rate contracts with an injectable
  clock.
- **Circuit breaker** fails fast on degraded dependencies and probes
  recovery via half-open.
- **Retry** uses exponential backoff + jitter, only on transient errors.
- **Graceful shutdown** drains; **idempotency** makes retries/replays safe.
- **Deadlock/livelock/starvation** are all defeated by the same rule: make
  every wait bounded.

## 11. Quick Reference

| Need | Tool |
|---|---|
| Buffer between producer and consumer | `queue.Queue(maxsize=n)` + `put(timeout=)` |
| Bounded parallelism for I/O tasks | `ThreadPoolExecutor(max_workers=k)` |
| Parallel batch with ordered results | `pool.map` (fan-out/fan-in) |
| Respect a provider rate limit | Token bucket with injected clock |
| Fail fast on a dead dependency | Circuit breaker (closed/open/half-open) |
| Survive transient 429/5xx | Retry: backoff + full jitter |
| Stop a job without losing work | `Event` + `get(timeout=)` drain loop |
| Repeat a job safely | Idempotent writes (content-hash keys) |
| Keep slow providers apart | Bulkhead: one pool per dependency |
| Safe lock acquisition | `lock.acquire(timeout=...)` |

## 12. Next Steps

- **`32-metaprogramming`** — the `@tool` decorator registry pattern used by
  agent frameworks to auto-discover callable tools (a decorator that reads
  the function's signature and builds a JSON schema — pure metaprogramming).
- **`34-debugging-techniques`** — how to actually find the R1.1-style hang:
  faulthandler, `py-spy dump`, and thread dumps.
- **`22-asyncio-advanced.py`** — the async twin of this topic: bounded
  `asyncio.Queue`, `Semaphore` rate limiting, and cancellation.
- **`08-mlops`** — deployment layers that make these patterns observable:
  retries, timeouts, and circuit breakers are standard fields in model
  serving configs.
