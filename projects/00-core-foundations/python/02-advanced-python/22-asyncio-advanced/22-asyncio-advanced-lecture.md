# Advanced Python - 22: Asyncio Advanced

## Topic Overview

`04-async-await.py` taught you the primitives: `async def`, `await`, `gather`, `Semaphore`. This lecture is the production toolkit: how real services orchestrate hundreds of concurrent calls without breaking. The headline difference is **fail-fast semantics** — a `TaskGroup` cancels every sibling the moment one child fails, which is what you want when one bad embedding should abort a batch, not silently poison it. Cancellation and shielding decide who gets to stop what, and when. `asyncio.timeout` turns latency SLOs into code. Async context managers and iterators stream tokens instead of buffering whole responses. Queues give backpressure; semaphores respect provider rate limits; `run_in_executor` bridges the sync code you cannot rewrite. The golden rule — **never block the loop** — is demonstrated with a measurement, not an assertion.

Where `21-concurrency-comparison-lecture.md` decided *whether* to go async, this lecture decides *how* to survive at scale once you have.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose `TaskGroup` over `gather` by failure semantics, not habit
2. Cancel tasks and shield critical work from cancellation
3. Apply `asyncio.timeout` as a deadline over a whole block
4. Write async context managers and async iterators
5. Build producer-consumer pipelines with bounded queues
6. Cap concurrency observably with `Semaphore`
7. Bridge blocking sync code with `asyncio.to_thread` / `run_in_executor`
8. Prove with a measurement why `time.sleep` must never appear in a coroutine

---

## Prerequisites

| Need | Where |
|---|---|
| Async basics: await, gather, tasks | `04-async-await-lecture.md` |
| Why async beats threads on I/O | `21-concurrency-comparison-lecture.md` |
| Context managers (sync) | `03-context-managers-lecture.md` |
| Generators and iterators | `02-generators-lecture.md` |
| Exception groups (3.11+) | Python docs: `ExceptionGroup` |

---

## 1. TaskGroup vs gather

`asyncio.gather` is best-effort: it waits for everything and only reports failures at the end. A `TaskGroup` (Python 3.11+) is fail-fast: the moment any child raises, the group **cancels every remaining task**, then raises an `ExceptionGroup` with the failures.

```python
import asyncio

async def fetch(name: str, delay: float, fail: bool = False) -> str:
    await asyncio.sleep(delay)
    if fail:
        raise ValueError(f"{name} failed")
    return f"{name}:ok"

async def demo_task_group() -> None:
    cancelled: list[str] = []
    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(fetch("a", 0.05))
            group.create_task(fetch("boom", 0.02, fail=True))
            group.create_task(_watch("c", 0.3, cancelled))
    except ExceptionGroup as eg:
        print(type(eg).__name__, [e.__class__.__name__ for e in eg.exceptions])
    print("cancelled by group:", cancelled)

async def _watch(name: str, delay: float, cancelled: list[str]) -> None:
    try:
        await fetch(name, delay)
    except asyncio.CancelledError:
        cancelled.append(name)
        raise
```

```
ExceptionGroup ['ValueError']
cancelled by group: ['c']
```

The rule of thumb: **TaskGroup when one failure should abort the batch** (a malformed document stops the whole embedding run); **gather with `return_exceptions=True` when partial results are acceptable** (one bad row should not kill a report).

---

## 2. Cancellation: Who Can Stop What

Cancelling a task raises `CancelledError` inside it at its next `await`. The task can clean up in a `finally` and must re-raise to confirm cancellation.

```python
async def demo_cancel() -> None:
    task = asyncio.create_task(fetch("slow", 5.0))
    await asyncio.sleep(0.01)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("cancelled as expected")
```

```
cancelled as expected
```

Cancellation is the mechanism behind "client disconnected mid-generation": the request task gets cancelled, and every downstream await (the streaming loop, the queue) stops promptly. Design cleanup paths around `CancelledError`, not around exceptions you expect to survive.

---

## 3. Shielding: Work That Must Finish

`asyncio.shield` protects an inner awaitable from the cancellation of the outer awaiter. The outer wait may be cancelled; the shielded task keeps running. You can still collect its result afterwards.

```python
async def demo_shield() -> str:
    task = asyncio.create_task(fetch("shielded", 0.1))
    try:
        async with asyncio.timeout(0.02):
            await asyncio.shield(task)      # timeout fires, shield absorbs it
    except TimeoutError:
        print("outer wait timed out")
    result = await task                     # shielded work finished anyway
    print("shielded completed:", result)
    return result
```

```
outer wait timed out
shielded completed: shielded:ok
```

Use shield for the operations that must complete even if the caller gives up: flushing a generation buffer, writing a checkpoint, acknowledging a queue message. Do not shield everything — shielded tasks are exactly the ones that keep running after you "cancelled" a request.

---

## 4. asyncio.timeout: Deadlines as Code

`asyncio.wait_for` wraps a single awaitable; `asyncio.timeout` (3.11+) is a context manager whose deadline covers an entire block. Latency SLOs on model endpoints are implemented exactly like this.

```python
async def demo_timeout() -> None:
    try:
        async with asyncio.timeout(0.05):
            await fetch("slow", 0.5)
    except TimeoutError:
        print("TimeoutError raised past the deadline")
```

```
TimeoutError raised past the deadline
```

The block form matters: a pipeline that calls a model, then a reranker, then writes to a queue shares one deadline — if the total exceeds it, the whole unit of work fails fast rather than dribbling past its SLO.

---

## 5. Async Context Managers and Iterators

`__aenter__` / `__aexit__` and `__aiter__` / `__anext__` are the async twins of the sync protocol. Async iterators are how you stream tokens from a model: O(1) memory, one chunk at a time, instead of buffering the whole response.

```python
class TokenStream:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens
        self._i = 0

    def __aiter__(self) -> "TokenStream":
        return self

    async def __anext__(self) -> str:
        if self._i >= len(self._tokens):
            raise StopAsyncIteration
        await asyncio.sleep(0.01)
        token = self._tokens[self._i]
        self._i += 1
        return token

async def demo_iter() -> None:
    out: list[str] = []
    async for token in TokenStream(["token", "by", "token"]):
        out.append(token)
    print(out)
```

```
['token', 'by', 'token']
```

Async context managers wrap session lifecycles (a DB connection, an HTTP client, a lock) exactly like sync `with` blocks, and the `async with` form is what `httpx.AsyncClient`, `aiohttp.ClientSession`, and database drivers expose.

---

## 6. Queues: Bounded Backpressure

`asyncio.Queue(maxsize=n)` parks a producer when the queue is full and parks consumers when it is empty. A bounded queue is the difference between "the provider throttled us" and "we buffered 10 GB of documents in memory".

```python
async def demo_queue() -> int:
    queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=3)
    processed: list[str] = []

    async def producer() -> None:
        for i in range(8):
            await queue.put(f"item-{i}")     # parks when full
        await queue.put(None)                # sentinel: no more work
        await queue.put(None)                # one per consumer

    async def consumer(name: str) -> None:
        while True:
            item = await queue.get()
            if item is None:
                return
            await asyncio.sleep(0.005)
            processed.append(f"{name}:{item}")

    async with asyncio.TaskGroup() as group:
        group.create_task(producer())
        group.create_task(consumer("c1"))
        group.create_task(consumer("c2"))
    return len(processed)
```

```
8
```

The sentinel pattern (a `None` per consumer) is the standard way to signal "no more work" — prefer it over cancelling consumers mid-`get()`, which can swallow items.

---

## 7. Semaphore: Rate Limits Made Observable

A `Semaphore(n)` caps how many coroutines may be inside the guarded region. Track the max in-flight to *prove* the cap works — an observable assertion, not a hope.

```python
async def demo_semaphore() -> tuple[int, int]:
    sem = asyncio.Semaphore(3)
    in_flight = 0
    max_seen = 0

    async def limited(name: str) -> str:
        nonlocal in_flight, max_seen
        async with sem:
            in_flight += 1
            max_seen = max(max_seen, in_flight)
            await asyncio.sleep(0.02)
            in_flight -= 1
            return f"{name}:ok"

    results = await asyncio.gather(*(limited(f"r{i}") for i in range(8)))
    return len(results), max_seen
```

```
(8, 3)
```

A provider's "10 requests per second" becomes `Semaphore(10)` around the call site. The observable max-in-flight check is exactly what the exercise asserts: `max_seen <= 3` and `max_seen == 3` — the cap is respected *and* actually used.

---

## 8. run_in_executor: Bridging Sync Code

Some blocking code cannot be rewritten: a sync driver, a legacy library, a CPU-bound utility. `asyncio.to_thread` (or `loop.run_in_executor`) ships the call to a worker thread so the loop stays responsive.

```python
import time

def _blocking_db_query(query: str) -> str:
    time.sleep(0.05)          # a sync driver we cannot change
    return f"result-of-{query}"

async def demo_to_thread() -> str:
    result = await asyncio.to_thread(_blocking_db_query, "SELECT 1")
    return result
```

```
result-of-SELECT 1
```

The bridge is for *occasional* blocking calls, not for the hot path: each `to_thread` parks a real OS thread, and thread-per-call defeats the memory advantage of async. If a call blocks for a long time, consider pushing the whole stage into a thread pool or a subprocess instead.

---

## 9. Never Block the Loop (Measured)

`time.sleep` inside a coroutine freezes the entire event loop — every other task stalls. The measurement makes it undeniable:

```python
async def _direct_block() -> None:
    time.sleep(0.15)                      # blocks ALL tasks on the loop

async def demo_blocking() -> tuple[float, float]:
    start = time.perf_counter()
    async with asyncio.TaskGroup() as group:
        group.create_task(_direct_block())
        group.create_task(_direct_block())
    blocking = time.perf_counter() - start

    start = time.perf_counter()
    async with asyncio.TaskGroup() as group:
        group.create_task(asyncio.sleep(0.15))
        group.create_task(asyncio.sleep(0.15))
    cooperative = time.perf_counter() - start
    return blocking, cooperative
```

```
(0.30, 0.15)   # two time.sleep calls serialize; two asyncio.sleep overlap
```

Two `time.sleep(0.15)` calls take 0.30s — the loop was frozen, the tasks ran one after another. Two `asyncio.sleep(0.15)` calls take 0.15s — they overlapped. One blocking call in a 200-call pipeline costs the same as 200 blocking calls. This is why the exercise asserts `blocking >= cooperative * 1.5` as a *ratio*: the shape of the result is deterministic even when absolute times are not.

---

## Common Mistakes to Avoid

### Mistake 1: `time.sleep` in a coroutine
```
# WRONG -- freezes every task on the loop
async def slow() -> None:
    time.sleep(1)
# CORRECT
async def slow() -> None:
    await asyncio.sleep(1)
# or, for real blocking work you cannot refactor:
    await asyncio.to_thread(blocking_fn)
```

### Mistake 2: `gather` when you need fail-fast
```
# WRONG -- one failure does not stop the rest, and you find out only at the end
await asyncio.gather(*tasks)
# CORRECT -- one failure cancels the siblings and surfaces as ExceptionGroup
async with asyncio.TaskGroup() as group:
    for t in tasks:
        group.create_task(t)
```

### Mistake 3: Unbounded task creation
```
# WRONG -- 10k create_task calls = 10k concurrent provider requests
tasks = [asyncio.create_task(call_api(i)) for i in range(10_000)]
# CORRECT -- semaphore caps in-flight work; queue adds backpressure
sem = asyncio.Semaphore(50)
```

### Mistake 4: Cancelling and expecting clean completion
```
# WRONG -- cancel() raises CancelledError inside; unhandled, the task
#          is cancelled but you never know
task.cancel()
# CORRECT -- await the task and handle CancelledError for cleanup
task.cancel()
try:
    await task
except asyncio.CancelledError:
    ...  # clean up, then re-raise
```

### Mistake 5: `asyncio.run` inside a coroutine
```
# WRONG -- asyncio.run creates a NEW loop; calling it inside a running
#          coroutine is an error
async def inner() -> None:
    asyncio.run(other())          # RuntimeError: cannot run from a running loop
# CORRECT -- await the coroutine directly; run() only at the top level
```

---

## Best Practices

1. **Use `TaskGroup` for batches** where one failure should abort everything.
2. **Shield only what must survive**; cancellation should mean something.
3. **Put SLOs in code** with `asyncio.timeout` blocks, not comments.
4. **Bound every queue**; unbounded queues are memory leaks with a deadline.
5. **Track max in-flight** to verify semaphores observably.
6. **Bridge, don't embed** blocking calls: `to_thread` for legacy sync code.
7. **Never `time.sleep` in a coroutine** — the loop belongs to everyone.
8. **Use sentinels** to end consumers instead of cancelling them.
9. **Clean up on `CancelledError`** in `finally` blocks.
10. **Note the version floor**: `TaskGroup` and `asyncio.timeout` need Python 3.11+.

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| `asyncio.sleep` in a task | yields, loop continues | ~KB/task | `time.sleep` — blocks everything (never) |
| Task creation | ~µs, no OS thread | ~KB each | thread creation — ~8 MB stack |
| `Semaphore` acquire/release | O(1) | O(1) | none — it is already the minimal gate |
| Bounded queue put/get | O(1) amortized | bounded by maxsize | unbounded list — O(n) memory drift |
| `to_thread` per call | thread park + run | OS thread (~8 MB virtual) | async-native code — no thread |
| `TaskGroup` cancel-on-fail | O(tasks) total | O(tasks) | `gather` — no cancellation, partial results |

---

## AI Engineering Relevance

**Where this shows up:** streaming responses from multiple models at once (one task per provider stream), a bounded-concurrency embedding pipeline (semaphore at the API limit, queue between chunking and embedding), and graceful cancellation when a client disconnects mid-generation (cancel the request task, shield the flush). The phase doc's canonical case — 200 concurrent LLM calls — is the direct application of sections 1, 6, and 7: a TaskGroup over 200 tasks, a queue feeding them, a semaphore capping them.

| Concept here | Used for |
|---|---|
| `TaskGroup` | aborting a batch when one document fails to embed |
| `Semaphore` + queue | respecting a provider's 50 req/s rate limit |
| `asyncio.timeout` | per-request latency SLOs on a model endpoint |
| shield | finishing a generation buffer after the client disconnects |
| async iterators | streaming tokens instead of buffering responses |
| `to_thread` | calling a sync reranker inside an async pipeline |

**Scale note:** at 200 concurrent calls, one blocking `time.sleep` multiplies the whole batch's latency by 200 (section 9's 2x measurement generalizes). At 10k documents, an unbounded queue between chunking and embedding grows to gigabytes; the bounded queue's backpressure is what keeps memory flat. The primitives are the same at every scale; the cost of getting them wrong grows linearly with the concurrency.

---

## Practice Exercises

### Exercise 1: TaskGroup Fail-Fast (Difficulty: Easy)
Create a `TaskGroup` with three tasks: two succeed, one raises after 0.01s. Verify the third task is cancelled (record it in a list) and the group raises `ExceptionGroup`. Repeat with `gather(..., return_exceptions=True)` and explain the difference.

### Exercise 2: Shielded Flush (Difficulty: Medium)
Write a coroutine that simulates streaming 10 chunks, shielded from a `timeout(0.02)`; collect the full stream afterwards. Assert all 10 chunks arrived despite the timeout.

### Exercise 3: Bounded Pipeline (Difficulty: Medium)
Build producer-consumer with `Queue(maxsize=2)`: a producer emits 20 items, two consumers process each with a 0.01s sleep. Assert all 20 processed and that the queue never exceeded its bound (track `maxsize` observed in a variable).

### Exercise 4: Rate-Limited Calls (Difficulty: Medium)
Implement `call_with_limit(n_calls, limit)` that runs `n_calls` API simulators under `Semaphore(limit)`, tracking max in-flight. Assert `max_in_flight <= limit` and `max_in_flight == limit`.

### Exercise 5: Loop-Blocking Proof (Difficulty: Hard)
Measure a TaskGroup of two `time.sleep(0.2)` coroutines vs two `asyncio.sleep(0.2)` coroutines. Assert the ratio `blocking / cooperative >= 1.5`. Print both numbers. Explain what happens to the other 198 tasks in a 200-call batch.

### Exercise 6: Async Stream with Context (Difficulty: Hard)
Write an `AsyncSession` context manager around a `TokenStream`, and stream a simulated model response inside `async with`. Assert the session opened before the first token and closed after the last, and that the tokens arrived in order.

---

## Summary

| Concept | Description |
|---|---|
| `TaskGroup` | fail-fast batch: one failure cancels siblings, raises `ExceptionGroup` |
| `gather` | best-effort collection: partial results, no auto-cancel |
| Cancellation | `CancelledError` raised at the next `await`; clean up in `finally` |
| `shield` | inner work survives the caller's cancellation |
| `asyncio.timeout` | a deadline over a whole block, not one call |
| Async context/iter | `async with` / `async for` twins of the sync protocols |
| Bounded queue | backpressure: producer parks when full, consumers park when empty |
| `Semaphore` | observable cap on in-flight work |
| `to_thread` | bridge blocking sync code without freezing the loop |
| Never block the loop | `time.sleep` serializes; `asyncio.sleep` overlaps — measured |

Async at scale is not about the `async def` keyword — it is about orchestration: who fails fast, who gets cancelled, who must finish, how many are in flight, and what happens when one component blocks. Every production async AI service is a composition of these primitives.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Fail-fast batch | `async with asyncio.TaskGroup() as g: g.create_task(...)` |
| Best-effort batch | `await asyncio.gather(*tasks, return_exceptions=True)` |
| Deadline over a block | `async with asyncio.timeout(0.5): ...` |
| Protect critical work | `await asyncio.shield(task)` |
| Cap concurrency | `async with asyncio.Semaphore(50): ...` |
| Backpressure | `asyncio.Queue(maxsize=n)` + sentinels |
| Bridge sync code | `await asyncio.to_thread(sync_fn, arg)` |
| Sleep in a coroutine | `await asyncio.sleep(secs)` — never `time.sleep` |

---

## Next Steps

Next: **[23-typing-advanced-lecture.md](23-typing-advanced-lecture.md)** — type the async pipeline: `ParamSpec` for decorators, `Protocol` for retriever interfaces, and the typing toolkit behind LLM tool schemas.
Continues in: **[31-concurrency-patterns](../../../02-advanced-python/31-concurrency-patterns.py)** (Phase 2 topic 31) — producer-consumer at scale, token buckets, circuit breakers, and graceful shutdown.
Official docs: [asyncio](https://docs.python.org/3/library/asyncio.html), [TaskGroup](https://docs.python.org/3/library/asyncio-task.html#task-groups), [timeout](https://docs.python.org/3/library/asyncio-task.html#asyncio.timeout), [queue](https://docs.python.org/3/library/asyncio-queue.html).
