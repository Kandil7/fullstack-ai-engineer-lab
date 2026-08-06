# Asyncio Advanced Quiz

## Topic Overview
This quiz covers the production asyncio toolkit: TaskGroup fail-fast
semantics, cancellation and shielding, `asyncio.timeout` deadlines,
bounded queues, semaphores, async context managers and iterators, and
the golden rule of never blocking the loop.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

---

## Questions

### Question 1
**What happens in a `TaskGroup` when one child task raises?**

A) The group waits for the remaining tasks, then reports the error
B) The group cancels every remaining task and raises `ExceptionGroup`
C) The failing task is retried automatically
D) The group raises the error but leaves siblings running

**Difficulty:** Easy

---

### Question 2
**Where can `CancelledError` be delivered to a task?**

A) At any statement in the task body
B) Only at an `await` point
C) Only inside a `try` block
D) Only when the task calls `task.cancel()` itself

**Difficulty:** Easy

---

### Question 3
**What is the output of this code?**
```python
import asyncio

async def main():
    async with asyncio.timeout(0.05):
        await asyncio.sleep(0.2)

try:
    asyncio.run(main())
except TimeoutError:
    print("timed out")
```

A) `timed out`
B) (no output — the sleep wins)
C) `TimeoutError` is swallowed silently
D) `CancelledError`

**Difficulty:** Easy

---

### Question 4
**What is the output of this code?**
```python
import asyncio

async def main():
    sem = asyncio.Semaphore(2)
    in_flight = 0
    peak = 0

    async def call():
        nonlocal in_flight, peak
        async with sem:
            in_flight += 1
            peak = max(peak, in_flight)
            await asyncio.sleep(0.01)
            in_flight -= 1

    await asyncio.gather(*(call() for _ in range(6)))
    print(peak)

asyncio.run(main())
```

A) `6`
B) `2`
C) `1`
D) `0`

**Difficulty:** Easy

---

### Question 5
**Which statement about `asyncio.shield(task)` is TRUE?**

A) The shielded task ignores the GIL
B) The shielded work survives cancellation of the outer wait
C) Shielded tasks cannot be awaited
D) Shield means the task runs in a thread

**Difficulty:** Easy

---

### Question 6
**Which is the correct way to sleep in a coroutine?**

A) `time.sleep(1)`
B) `await asyncio.sleep(1)`
C) `asyncio.sleep(1)`
D) `await time.sleep(1)`

**Difficulty:** Easy

---

### Question 7
**What is the output of this code?**
```python
import asyncio

class Tokens:
    def __init__(self, words):
        self._words = words
        self._i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._i >= len(self._words):
            raise StopAsyncIteration
        w = self._words[self._i]
        self._i += 1
        return w

async def main():
    print([w async for w in Tokens(["a", "b"])])

asyncio.run(main())
```

A) `['a', 'b']`
B) `['a', 'b', 'a', 'b']`
C) `[]`
D) `TypeError: 'Tokens' object is not iterable`

**Difficulty:** Medium

---

### Question 8
**A producer is faster than its consumers. With `Queue(maxsize=3)`, what happens to the producer?**

A) It raises `QueueFull` and crashes
B) It parks at `put()` until there is room — backpressure
C) It keeps buffering in an internal list
D) The queue silently drops items

**Difficulty:** Medium

---

### Question 9
**What is the output of this code?**
```python
import asyncio

async def main():
    q = asyncio.Queue()
    await q.put(1)
    await q.put(2)
    print(q.get_nowait(), q.get_nowait())

asyncio.run(main())
```

A) `2 1`
B) `1 2`
C) `<coroutine object ...>`
D) `QueueEmpty` exception

**Difficulty:** Medium

---

### Question 10
**Two consumers wait on one queue. To end them cleanly, you should:**

A) Cancel both consumers after the producer finishes
B) Push one `None` sentinel per consumer
C) Push one sentinel and let both race for it
D) Close the queue — `asyncio.Queue.close()`

**Difficulty:** Medium

---

### Question 11
**What is the difference between `asyncio.gather` and a `TaskGroup` on failure?**

A) None — they are aliases
B) Gather continues and collects partial results; TaskGroup cancels siblings
C) TaskGroup continues; gather cancels everything
D) Gather retries failed tasks; TaskGroup does not

**Difficulty:** Medium

---

### Question 12
**What is the output of this code?**
```python
import asyncio

async def main():
    task = asyncio.create_task(asyncio.sleep(10))
    await asyncio.sleep(0.01)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("cancelled")

asyncio.run(main())
```

A) `cancelled`
B) (nothing — the sleep finishes)
C) `RuntimeError`
D) `timeout`

**Difficulty:** Medium

---

### Question 13
**Which statement about `asyncio.to_thread` is TRUE?**

A) It runs a coroutine in a separate process
B) It bridges a blocking sync function into a worker thread
C) It converts a thread pool into async tasks
D) It is the async replacement for `time.sleep`

**Difficulty:** Medium

---

### Question 14
**What is the output of this code?**
```python
import asyncio

async def main():
    async with asyncio.TaskGroup() as g:
        g.create_task(asyncio.sleep(0.1))
        raise KeyError("boom")
    print("unreachable")

try:
    asyncio.run(main())
except BaseExceptionGroup as eg:
    print(type(eg.exceptions[0]).__name__)

asyncio.run(asyncio.sleep(0))  # keep the loop warm
```

A) `KeyError`
B) `boom`
C) `unreachable`
D) `CancelledError`

**Difficulty:** Hard

---

### Question 15
**Two coroutines each call `time.sleep(0.2)`; two others each `await asyncio.sleep(0.2)`. What do the groups measure?**

A) 0.4 and 0.4 — same cost
B) 0.4 and 0.2 — blocking serializes, async overlaps
C) 0.2 and 0.4 — async is slower
D) 0.2 and 0.2 — both overlap

**Difficulty:** Hard

---

### Question 16
**A request task is cancelled mid-generation. Which pattern lets the buffered response still be flushed?**

A) Wrap the flush in `asyncio.shield`
B) Catch `TimeoutError` around the flush
C) Call `task.cancel()` twice
D) Move the flush before the first `await`

**Difficulty:** Hard

---

### Question 17
**What is the output of this code?**
```python
import asyncio

async def main():
    async def producer():
        for i in range(4):
            await q.put(i)

    async def consumer():
        total = 0
        while True:
            item = await q.get()
            if item is None:
                return total
            total += item

    q = asyncio.Queue()
    await asyncio.gather(producer(), consumer())

asyncio.run(main())
```

A) `6`
B) `4`
C) `10`
D) The code hangs — the consumer waits forever for the sentinel

**Difficulty:** Hard

---

### Question 18
**Which design caps in-flight API calls at 50 while 200 are queued?**

A) `Queue(maxsize=200)` alone
B) `Semaphore(50)` around the call site
C) `TaskGroup` with 200 tasks
D) `asyncio.timeout(0.05)` per call

**Difficulty:** Hard

---

### Question 19
**A pipeline must abort when any document fails to embed. Which primitive implements that?**

A) `asyncio.gather(..., return_exceptions=True)`
B) `TaskGroup` — one failure cancels the batch
C) `Semaphore(1)` around the whole pipeline
D) `asyncio.to_thread` per document

**Difficulty:** Hard

---

### Question 20
**What is the output of this code?**
```python
import asyncio

async def main():
    start = asyncio.get_event_loop().time()
    async with asyncio.TaskGroup() as g:
        g.create_task(asyncio.sleep(0.05))
        g.create_task(asyncio.sleep(0.05))
    print(round(asyncio.get_event_loop().time() - start, 2))

asyncio.run(main())
```

A) `0.10`
B) `0.05`
C) `0.00`
D) `0.15`

**Difficulty:** Medium

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! Orchestration is yours.
- 14-17: Good! Review the failure-semantics questions.
- 10-13: Fair. Re-read the TaskGroup and queue sections.
- Below 10: Revisit the lecture and the exercise before continuing.

---

## Answer Key

1. **B) The group cancels every remaining task and raises
   `ExceptionGroup`** — fail-fast is the entire point of TaskGroup. A
   describes `gather`, C is false (no retry), D is false (siblings
   are cancelled).

2. **B) Only at an `await` point** — cancellation is delivered where
   the task yields. A is false, C is false (it can land outside
   `try`), D is backwards (cancel comes from outside).

3. **A) `timed out`** — `asyncio.timeout` raises `TimeoutError` past
   the deadline; the outer `try` prints. B is false (0.2 > 0.05), C
   is false (it is raised), D is false (`TimeoutError`, not
   `CancelledError`).

4. **B) `2`** — the semaphore caps in-flight work at 2; the peak
   proves it. A is the number of calls, C would be a limit of 1, D
   means the gate never engaged.

5. **B) The shielded work survives cancellation of the outer wait** —
   shield is the cancellation exception. A and D are false, C is
   false (you can await it afterwards).

6. **B) `await asyncio.sleep(1)`** — the cooperative form. A freezes
   the loop, C schedules nothing (missing await), D calls a sync
   function with await — an error.

7. **A) `['a', 'b']`** — the async iterator protocol drives the
   comprehension. B repeats the stream, C would need immediate
   exhaustion, D is false (`async for` uses `__aiter__`).

8. **B) It parks at `put()` until there is room — backpressure** —
   the bounded queue is the memory-safe seam. A is false (put
   awaits), C is false (no hidden buffer), D is false (nothing
   drops).

9. **B) `1 2`** — FIFO; `get_nowait` returns immediately when items
   exist. A is reversed, C confuses it with `q.get()` without await,
   D is false (items are present).

10. **B) Push one `None` sentinel per consumer** — each consumer
    needs its own end signal. A risks cancelling mid-`get`, C leaves
    one consumer hung, D is false (queues have no `close`).

11. **B) Gather continues and collects partial results; TaskGroup
    cancels siblings** — the failure-semantics split. A is false, C
    is the reverse, D is false (neither retries).

12. **A) `cancelled`** — `cancel()` delivers `CancelledError` at the
    task's next await; the handler prints. B is false (the sleep
    never finishes), C and D are false.

13. **B) It bridges a blocking sync function into a worker thread** —
    the sanctioned bridge for legacy code. A is false (thread, not
    process), C is backwards, D is false (never sleep the loop).

14. **A) `KeyError`** — the group raises `ExceptionGroup` wrapping
    the KeyError; the handler unwraps it. B is the message, C is
    unreachable, D is the wrong exception type.

15. **B) 0.4 and 0.2 — blocking serializes, async overlaps** — the
    measured golden rule. A ignores the overlap, C reverses it, D is
    false for the blocking pair.

16. **A) Wrap the flush in `asyncio.shield`** — the flush survives
    the request cancellation. B is the wrong exception, C does
    nothing useful, D does not protect the flush itself.

17. **D) The code hangs — the consumer waits forever for the
    sentinel** — no sentinel was pushed. A and B assume completion,
    C is the wrong sum.

18. **B) `Semaphore(50)` around the call site** — the rate limit
    becomes code. A bounds buffering, not calls, C creates all 200
    eagerly, D is a deadline, not a cap.

19. **B) `TaskGroup` — one failure cancels the batch** — fail-fast
    aborts embedding runs on the first bad document. A explicitly
    collects partial results, C serializes, D bridges threads.

20. **B) `0.05`** — two overlapping sleeps take one sleep's time. A
    is the sequential result, C is impossible, D invents overhead.
