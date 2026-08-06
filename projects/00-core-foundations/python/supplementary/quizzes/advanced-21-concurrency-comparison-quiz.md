# Concurrency Comparison Quiz

## Topic Overview
This quiz covers choosing between threads, processes, and async; the
GIL and what it does and does not serialize; I/O-bound vs CPU-bound
workloads; and the measured trade-offs behind each model.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

---

## Questions

### Question 1
**Which concurrency model is the right default for CPU-bound work in CPython?**

A) Threads — they run on multiple cores
B) Processes — each gets its own GIL
C) Async — coroutines are the fastest
D) None — CPU work must stay sequential

**Difficulty:** Easy

---

### Question 2
**What exactly does the GIL serialize?**

A) I/O operations like file reads
B) Execution of Python bytecode across threads
C) Access to the garbage collector only
D) Network calls in the standard library

**Difficulty:** Easy

---

### Question 3
**What is the output of this code?**
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=2) as ex:
    print(list(ex.map(lambda x: x * x, [1, 2, 3])))
```

A) `[1, 4, 9]`
B) `[1, 2, 3]`
C) `[1, 4, 9, 16]`
D) `<generator object ...>`

**Difficulty:** Easy

---

### Question 4
**What is the output of this code?**
```python
import asyncio

async def main():
    results = await asyncio.gather(
        *(asyncio.sleep(0.01, result=i) for i in range(3))
    )
    print(results)

asyncio.run(main())
```

A) `[0, 1, 2]`
B) `[None, None, None]`
C) `(0, 1, 2)`
D) `0 1 2`

**Difficulty:** Easy

---

### Question 5
**Why does threading speed up I/O-bound programs despite the GIL?**

A) Threads bypass the GIL entirely
B) The GIL is released during most I/O waits, so threads overlap them
C) The interpreter runs each thread on a separate core
D) I/O work is executed by the C extension, never Python

**Difficulty:** Easy

---

### Question 6
**You need 8 concurrent HTTP calls. Which is the simplest reasonable choice?**

A) `ThreadPoolExecutor` with 8 workers
B) A `ProcessPoolExecutor` — processes are always faster
C) `asyncio.gather` — but only if you rewrite in async
D) Sequential calls — concurrency adds risk

**Difficulty:** Easy

---

### Question 7
**What is the output of this code?**
```python
import threading

lock = threading.Lock()
count = 0

def inc():
    global count
    with lock:
        count += 1

threads = [threading.Thread(target=inc) for _ in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(count)
```

A) `0`
B) `1`
C) `3`
D) A value that varies between runs

**Difficulty:** Medium

---

### Question 8
**What is the single biggest reason process pools beat thread pools on CPU work?**

A) Processes share memory, so no copying is needed
B) Each process has its own GIL, so bytecode truly runs in parallel
C) Process startup is cheaper than thread startup
D) The interpreter assigns each process a faster core

**Difficulty:** Medium

---

### Question 9
**Which of these workers will FAIL on Windows `spawn`?**

A) `def worker(x): return x + 1` at module top level
B) A lambda assigned to a module-level name
C) `def worker(x): return x + 1` nested inside `main()`
D) A method of a module-level class

**Difficulty:** Medium

---

### Question 10
**What is the output of this code?**
```python
import time

def fetch():
    time.sleep(0.1)

start = time.perf_counter()
t1 = threading.Thread(target=fetch)
t2 = threading.Thread(target=fetch)
t1.start()
t2.start()
t1.join()
t2.join()
print(round(time.perf_counter() - start, 1))
```

A) `0.1` — the sleeps overlapped
B) `0.2` — the sleeps serialized
C) `0.0` — threads do not wait
D) `0.3` — thread overhead added time

**Difficulty:** Medium

---

### Question 11
**Why can a single `time.sleep` in an asyncio coroutine hurt an entire service?**

A) It raises an exception that cancels all tasks
B) It blocks the event loop, stalling every other task
C) It consumes one full core with busy-waiting
D) It is fine — each coroutine has its own thread

**Difficulty:** Medium

---

### Question 12
**A batch of 5,000 concurrent I/O waits. Which model costs least memory?**

A) 5,000 OS threads — about 40 GB of stacks
B) 5,000 asyncio tasks — about 350 MB
C) 5,000 asyncio tasks — a few hundred KB total
D) 5,000 processes — each shares one stack

**Difficulty:** Medium

---

### Question 13
**What is the output of this code?**
```python
import queue

q = queue.Queue()
q.put("a")
q.put("b")
print(q.get(), q.get())
```

A) `b a`
B) `a b`
C) `a a`
D) `TypeError: queue is empty`

**Difficulty:** Medium

---

### Question 14
**Which statement about a `Lock` is FALSE?**

A) It makes compound operations like `count += 1` atomic
B) Only one thread can hold it at a time
C) It is released automatically when the thread exits the `with` block
D) It makes the protected code run on a separate core

**Difficulty:** Medium

---

### Question 15
**What is the output of this code?**
```python
from concurrent.futures import ProcessPoolExecutor

def cube(x):
    return x ** 3

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=2) as ex:
        print(list(ex.map(cube, [1, 2, 3])))
```

A) `[1, 8, 27]`
B) `[3, 6, 9]`
C) `[1, 2, 3]`
D) `[1, 8]`

**Difficulty:** Hard

---

### Question 16
**Why is `if __name__ == "__main__":` typically required around a process-pool block on Windows?**

A) It speeds up the pool by skipping module imports
B) Spawn re-imports the module in each child — the guard prevents infinite recursion
C) It lets the pool use `fork` on Windows
D) It is only needed for `ThreadPoolExecutor`, not processes

**Difficulty:** Hard

---

### Question 17
**You benchmark a function five times: `[0.11, 0.09, 0.31, 0.10, 0.09]`. Which value best represents the machine's capability?**

A) The mean, `0.14`
B) The maximum, `0.31`
C) The minimum, `0.09`
D) The median, `0.10` — no, the mode

**Difficulty:** Hard

---

### Question 18
**What is the most likely output of this code?**
```python
import threading

counter = 0

def bump():
    global counter
    for _ in range(50_000):
        counter += 1

ts = [threading.Thread(target=bump) for _ in range(2)]
for t in ts:
    t.start()
for t in ts:
    t.join()
print(counter)
```

A) `100000` — always
B) `0` — the writes cancel out
C) `50000` — threads double up
D) A value at or below `100000` — lost updates are possible

**Difficulty:** Hard

---

### Question 19
**You must call an LLM API 200 times with a 50 req/s rate limit. Which design is the right shape?**

A) 200 threads, no gate — the provider throttles us
B) 200 asyncio tasks gated by `Semaphore(50)` (or fewer, by time)
C) A process pool with 200 workers
D) Sequential calls — rate limits forbid concurrency

**Difficulty:** Hard

---

### Question 20
**Which statement is TRUE about where blocking is acceptable?**

A) `time.sleep` in a thread blocks only that thread
B) `time.sleep` in a coroutine blocks only that coroutine
C) `time.sleep` in a coroutine is the standard way to simulate I/O
D) Blocking calls are safe anywhere as long as they are short

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! The concurrency model is yours.
- 14-17: Good! Review the mistakes you missed.
- 10-13: Fair. Re-read the decision table and GIL sections.
- Below 10: Revisit the lecture and the exercise before continuing.

---

## Answer Key

1. **B) Processes — each gets its own GIL** — only processes run Python
   bytecode in parallel. A is false (the GIL serializes threads), C is
   false (async is single-threaded), D is false (processes exist
   precisely for this).

2. **B) Execution of Python bytecode across threads** — one thread
   executes bytecode at a time. A is false (I/O releases the GIL), C
   is too narrow, D is false (network calls are I/O).

3. **A) `[1, 4, 9]`** — `map` on an executor returns the transformed
   values in input order. B is the input, C adds an extra element, D
   confuses lazy iterators with the materialized list.

4. **A) `[0, 1, 2]`** — `sleep(..., result=i)` returns `i`; `gather`
   preserves order. B would need no `result`, C is the tuple syntax,
   D prints without the list wrapper.

5. **B) The GIL is released during most I/O waits, so threads overlap
   them** — waiting threads hold no GIL. A is false (the GIL still
   exists), C is false (threads share one interpreter), D is false.

6. **A) `ThreadPoolExecutor` with 8 workers** — simplest correct tool
   for a handful of I/O calls. B overkills (spawn cost, pickling),
   C is right only if the codebase is already async, D abandons
   concurrency.

7. **C) `3`** — the lock makes each increment atomic; the answer is
   deterministic. A and B undercount, D is the unlocked behavior.

8. **B) Each process has its own GIL, so bytecode truly runs in
   parallel** — the whole reason to pay spawn cost. A is backwards
   (processes do NOT share memory), C is false (spawn is expensive),
   D is meaningless.

9. **C) A worker nested inside `main()`** — spawn cannot import a
   local function; `AttributeError: Can't get local object`. A is the
   correct pattern, B and D are importable by name.

10. **A) `0.1` — the sleeps overlapped** — `time.sleep` releases the
    GIL, so both threads wait simultaneously. B is the sequential
    result, C ignores waiting, D invents overhead that dwarfs the
    wait.

11. **B) It blocks the event loop, stalling every other task** — one
    coroutine freezing the loop freezes all 199 siblings. A is false,
    C is false (it stalls, not burns a core), D is false (one thread
    runs the loop).

12. **C) 5,000 asyncio tasks — a few hundred KB total** — the async
    advantage. A is absurdly high, B overstates (tasks are KB-scale,
    ~350 MB would need millions), D is wrong (processes each carry a
    full interpreter).

13. **B) `a b`** — FIFO order. A is reversed, C duplicates, D is
    false — the queue is not empty.

14. **D) It makes the protected code run on a separate core** — a
    lock does no such thing. A, B, C are all true properties of
    `Lock`.

15. **A) `[1, 8, 27]`** — `map` preserves order across processes. B is
    multiplication, C is identity, D drops the last result.

16. **B) Spawn re-imports the module in each child — the guard
    prevents infinite recursion** — the child re-executes the module
    body. A is false (imports still run), C is false (Windows has no
    fork), D is false (threads do not re-import).

17. **C) The minimum, `0.09`** — best-of-N is the least noisy
    estimate; interference only adds time. A is dragged up by the
    0.31 outlier, B is the worst sample, D misapplies the median.

18. **D) A value at or below `100000` — lost updates are possible** —
    `counter += 1` is read-add-write; interleaving loses updates. A
    is the locked outcome, B and C are false.

19. **B) 200 asyncio tasks gated by `Semaphore(50)` (or fewer, by
    time)** — the rate limit becomes code, memory stays flat. A
    abdicates control, C is wrong (CPU-bound tool for I/O), D is
    overcautious.

20. **A) `time.sleep` in a thread blocks only that thread** — the one
    safe place for blocking. B and C are false (it freezes the whole
    loop), D is false (short blocking in a loop is still blocking).
