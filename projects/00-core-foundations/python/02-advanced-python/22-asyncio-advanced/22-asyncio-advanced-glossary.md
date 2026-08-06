# Asyncio Advanced — Glossary 22

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| asyncio.timeout | API | Context manager imposing a deadline over an entire block |
| async context manager | Protocol | `__aenter__`/`__aexit__` twin of `with`, used via `async with` |
| async iterator | Protocol | `__aiter__`/`__anext__` twin of iteration, used via `async for` |
| await | Keyword | Yields control to the event loop until the awaited coroutine finishes |
| backpressure | Concept | Producers park when consumers fall behind; bounded queues enforce it |
| CancelledError | Exception | Raised inside a task when someone calls `task.cancel()` |
| fail-fast | Concept | One task failure aborts the whole batch via group cancellation |
| gather | API | Waits for many awaitables; best-effort, no auto-cancellation |
| Queue (asyncio) | Data structure | Bounded async FIFO; `put` parks when full, `get` parks when empty |
| Semaphore | Sync primitive | Caps how many coroutines may enter a guarded region |
| sentinel | Pattern | A special value (`None`) signaling "no more work" to consumers |
| shield | API | Protects inner work from cancellation of the outer awaiter |
| Task | Concept | A coroutine scheduled on the loop; cancellable, awaitable |
| TaskGroup | API | Fail-fast batch manager; cancels siblings, raises ExceptionGroup |
| to_thread | API | Runs a blocking sync function in a worker thread |

## Detailed Definitions

### asyncio.timeout
**Definition**: A context manager (3.11+) that raises `TimeoutError` if the enclosed block exceeds a deadline. Unlike `wait_for`, it covers a whole block of awaits — exactly what a latency SLO on a pipeline wants.
**Example**:
```python
import asyncio

async def main() -> str:
    try:
        async with asyncio.timeout(0.05):
            await asyncio.sleep(0.2)      # exceeds the deadline
    except TimeoutError:
        return "timed out"
    return "finished"

print(asyncio.run(main()))
```
```text
timed out
```
**Related**: TaskGroup, shield, Task

### async context manager
**Definition**: An object with `__aenter__` and `__aexit__` used with `async with`. Wraps session lifecycles — HTTP clients, DB connections, locks — that need async setup and teardown.
**Example**:
```python
import asyncio

class Session:
    def __init__(self) -> None:
        self.closed = False
    async def __aenter__(self) -> "Session":
        await asyncio.sleep(0.01)         # async setup
        return self
    async def __aexit__(self, *exc) -> bool:
        self.closed = True                # async teardown
        return False

async def main() -> bool:
    async with Session() as s:
        pass
    return s.closed

print(asyncio.run(main()))
```
```text
True
```
**Related**: async iterator, await

### async iterator
**Definition**: An object with `__aiter__` and `__anext__` (raising `StopAsyncIteration` when done), used with `async for`. The streaming primitive: tokens arrive one at a time instead of buffering a whole response.
**Example**:
```python
import asyncio

class Tokens:
    def __init__(self, words: list[str]) -> None:
        self._words = words
        self._i = 0
    def __aiter__(self) -> "Tokens":
        return self
    async def __anext__(self) -> str:
        if self._i >= len(self._words):
            raise StopAsyncIteration
        word = self._words[self._i]
        self._i += 1
        await asyncio.sleep(0.01)
        return word

async def main() -> list[str]:
    return [w async for w in Tokens(["a", "b"])]

print(asyncio.run(main()))
```
```text
['a', 'b']
```
**Related**: async context manager, await

### await
**Definition**: The keyword that hands control to the event loop until the awaited object completes. Every `await` is a yield point — the loop runs other tasks meanwhile. It is also the cancellation checkpoint: `CancelledError` can only be delivered at an `await`.
**Example**:
```python
import asyncio

async def main() -> str:
    await asyncio.sleep(0.01)     # loop runs other tasks here
    return "back"

print(asyncio.run(main()))
```
```text
back
```
**Related**: coroutine (glossary 21), event loop (glossary 21), CancelledError

### backpressure
**Definition**: The system's way of slowing producers when consumers cannot keep up. In asyncio it is implemented by bounded queues: `put` parks a fast producer instead of letting memory grow unboundedly.
**Example**:
```python
import asyncio

async def main() -> tuple[int, int]:
    q: asyncio.Queue[int] = asyncio.Queue(maxsize=2)
    puts = 0
    async def producer() -> None:
        nonlocal puts
        for i in range(4):
            await q.put(i)        # parks when the queue is full
            puts += 1
    async def consumer() -> None:
        while True:
            try:
                q.get_nowait()
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.01)
                continue
            await asyncio.sleep(0)
            if q.empty() and puts == 4:
                return
    await asyncio.gather(producer(), consumer())
    return puts, q.maxsize

print(asyncio.run(main()))
```
```text
(4, 2)
```
**Related**: Queue (asyncio), sentinel, Semaphore

### CancelledError
**Definition**: Raised inside a task at its next `await` when `task.cancel()` is called. In Python 3.8+ it inherits from `BaseException`, so a bare `except Exception` does not swallow it. Clean up in `finally` and re-raise to confirm cancellation.
**Example**:
```python
import asyncio

async def worker() -> str:
    try:
        await asyncio.sleep(10)
    finally:
        print("cleanup ran")
    return "done"

async def main() -> str:
    t = asyncio.create_task(worker())
    await asyncio.sleep(0.01)
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        return "cancelled"

print(asyncio.run(main()))
```
```text
cleanup ran
cancelled
```
**Related**: Task, shield, TaskGroup

### fail-fast
**Definition**: The semantics of `TaskGroup`: when any child raises, the group cancels every remaining task and raises `ExceptionGroup`. Opposite of `gather(return_exceptions=True)`, which collects partial results and continues.
**Example**:
```python
import asyncio

async def main() -> str:
    cancelled: list[str] = []
    async def good(name: str) -> None:
        try:
            await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            cancelled.append(name)
            raise
    try:
        async with asyncio.TaskGroup() as g:
            g.create_task(good("a"))
            g.create_task(good("b"))
            raise ValueError("boom")
    except ExceptionGroup:
        pass
    return ",".join(sorted(cancelled))

print(asyncio.run(main()))
```
```text
a,b
```
**Related**: TaskGroup, gather, CancelledError

### gather
**Definition**: `asyncio.gather(*awaitables)` waits for all of them and returns results in order. It is best-effort: a failure does not cancel siblings by default; pass `return_exceptions=True` to collect failures as values.
**Example**:
```python
import asyncio

async def maybe(n: int) -> int:
    if n == 2:
        raise ValueError("bad")
    return n

async def main() -> list:
    results = await asyncio.gather(maybe(1), maybe(2), return_exceptions=True)
    return [type(r).__name__ if isinstance(r, BaseException) else r for r in results]

print(asyncio.run(main()))
```
```text
[1, 'ValueError']
```
**Related**: TaskGroup, fail-fast

### Queue (asyncio)
**Definition**: The async FIFO (`asyncio.Queue(maxsize=n)`). `put` awaits until there is room; `get` awaits until an item exists. A bounded queue is the memory-safe seam between producer and consumer stages.
**Example**:
```python
import asyncio

async def main() -> list[int]:
    q: asyncio.Queue[int] = asyncio.Queue(maxsize=1)
    await q.put(1)
    got: list[int] = []
    for _ in range(2):
        got.append(await q.get())
        await q.put(got[-1] + 1)
    return got

print(asyncio.run(main()))
```
```text
[1, 2]
```
**Complexity**: O(1) amortized put/get.
**Related**: backpressure, sentinel, Semaphore

### Semaphore
**Definition**: An async counter capping how many coroutines may hold it at once. `async with sem:` acquires before entry and releases on exit. This is how provider rate limits become code: `Semaphore(50)` = at most 50 in-flight calls.
**Example**:
```python
import asyncio

async def main() -> int:
    sem = asyncio.Semaphore(2)
    in_flight = 0
    max_seen = 0
    async def call(n: int) -> None:
        nonlocal in_flight, max_seen
        async with sem:
            in_flight += 1
            max_seen = max(max_seen, in_flight)
            await asyncio.sleep(0.01)
            in_flight -= 1
    await asyncio.gather(*(call(i) for i in range(5)))
    return max_seen

print(asyncio.run(main()))
```
```text
2
```
**Complexity**: O(1) acquire/release.
**Related**: Queue (asyncio), backpressure

### sentinel
**Definition**: A special value pushed onto a queue to signal consumers that no more work is coming. Use one sentinel per consumer, or consumers will wait forever after the last real item.
**Example**:
```python
import asyncio

async def main() -> list[int]:
    q: asyncio.Queue[int | None] = asyncio.Queue()
    await q.put(1)
    await q.put(2)
    await q.put(None)                # sentinel: no more work
    got: list[int] = []
    while True:
        item = await q.get()
        if item is None:
            return got
        got.append(item)

print(asyncio.run(main()))
```
```text
[1, 2]
```
**Related**: Queue (asyncio), backpressure

### shield
**Definition**: `asyncio.shield(awaitable)` runs inner work insulated from the cancellation of the outer await. If the outer wait is cancelled, the shielded task keeps running; you can still await its result afterwards. For work that must complete: flushes, checkpoints, acks.
**Example**:
```python
import asyncio

async def main() -> str:
    t = asyncio.create_task(asyncio.sleep(0.1))
    try:
        async with asyncio.timeout(0.01):
            await asyncio.shield(t)          # outer cancels, inner survives
    except TimeoutError:
        pass
    await t                                  # shielded work finished anyway
    return "shielded completed"

print(asyncio.run(main()))
```
```text
shielded completed
```
**Related**: CancelledError, Task, asyncio.timeout

### Task
**Definition**: A coroutine scheduled on the event loop via `asyncio.create_task`. Tasks run concurrently with the caller, are awaitable, and can be cancelled. Without creating tasks, coroutines only run sequentially inside `gather`.
**Example**:
```python
import asyncio

async def main() -> float:
    start = asyncio.get_event_loop().time()
    t1 = asyncio.create_task(asyncio.sleep(0.05))
    t2 = asyncio.create_task(asyncio.sleep(0.05))
    await t1
    await t2
    return round(asyncio.get_event_loop().time() - start, 2)

print(asyncio.run(main()))
```
```text
0.05   # both tasks overlapped
```
**Related**: TaskGroup, CancelledError, gather

### TaskGroup
**Definition**: `asyncio.TaskGroup()` (3.11+) — an `async with` block that tracks child tasks created via `group.create_task()`. If any child fails, the group cancels the rest and raises `ExceptionGroup` on exit. The modern replacement for `gather` when one failure should abort the batch.
**Example**:
```python
import asyncio

async def main() -> str:
    try:
        async with asyncio.TaskGroup() as g:
            g.create_task(asyncio.sleep(0.1))       # will be cancelled
            raise KeyError("missing")
    except ExceptionGroup as eg:
        return eg.exceptions[0].__class__.__name__

print(asyncio.run(main()))
```
```text
KeyError
```
**Related**: fail-fast, gather, CancelledError

### to_thread
**Definition**: `asyncio.to_thread(func, *args)` runs a blocking sync function in a worker thread and awaits its result. The sanctioned bridge for legacy sync code (drivers, CPU-bound utilities) you cannot rewrite as async — used sparingly, because each call parks a real OS thread.
**Example**:
```python
import asyncio, time

def legacy_query(q: str) -> str:
    time.sleep(0.02)                # blocking sync driver
    return f"result:{q}"

async def main() -> str:
    return await asyncio.to_thread(legacy_query, "SELECT 1")

print(asyncio.run(main()))
```
```text
result:SELECT 1
```
**Related**: await, event loop (glossary 21), Task

## Key Concepts Summary

### Orchestration, Not Syntax
- `TaskGroup` = fail-fast batches; `gather` = best-effort collection.
- Cancellation lands at the next `await`; clean up in `finally`.
- `shield` for work that must finish; `timeout` for deadlines over whole blocks.

### Memory-Safe Pipelines
- Bounded queues enforce backpressure: producers park instead of buffering.
- `Semaphore` caps in-flight work — the provider rate limit in code.
- Sentinels tell consumers the stream is over; one per consumer.

### The Golden Rule
- Never `time.sleep` in a coroutine — it freezes every task on the loop.
- Bridge unavoidable blocking calls with `to_thread`.
- Async iterators/context managers stream and scope resources instead of buffering.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. TaskGroup — ___
2. shield — ___
3. sentinel — ___
4. Semaphore — ___
5. asyncio.timeout — ___
6. CancelledError — ___
7. to_thread — ___
8. backpressure — ___
9. async iterator — ___
10. gather — ___

A. Deadline over an entire block, raising TimeoutError
B. Fail-fast batch manager cancelling siblings on failure
C. Protects inner work from the caller's cancellation
D. A value signaling "no more work" to consumers
E. Caps concurrent entries into a guarded region
F. Raised at the next await when a task is cancelled
G. Runs blocking sync code in a worker thread
H. Producers park when consumers fall behind
I. Streaming tokens via __aiter__/__anext__
J. Best-effort wait over many awaitables

**Answers:** 1-B, 2-C, 3-D, 4-E, 5-A, 6-F, 7-G, 8-H, 9-I, 10-J
