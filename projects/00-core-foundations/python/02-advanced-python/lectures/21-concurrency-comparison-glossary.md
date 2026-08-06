# Concurrency Comparison — Glossary 21

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| asyncio | Module | Event-loop based single-thread concurrency for I/O-bound work |
| concurrency | Concept | Many tasks in progress at once; tasks may not run simultaneously |
| coroutine | Function | `async def` function; runs only when awaited on an event loop |
| CPU-bound | Workload | Work limited by processor speed; benefits from multiprocessing |
| event loop | Concept | Single thread scheduling coroutines; yields at every `await` |
| GIL | Concept | CPython lock allowing one thread to execute bytecode at a time |
| I/O-bound | Workload | Work limited by waiting on I/O; benefits from threads/async |
| Lock | Sync primitive | Mutual-exclusion guard protecting a shared resource |
| multiprocessing | Module | Spawns separate interpreter processes; bypasses the GIL |
| parallelism | Concept | Many tasks executing simultaneously on many cores |
| ProcessPoolExecutor | Executor | Pool of worker processes; `submit`/`map` over pickled tasks |
| race condition | Bug | Outcome depends on interleaving of unsynchronized threads |
| spawn context | Concept | Windows/macOS process start: fresh interpreter per worker |
| synchronous | Concept | One task to completion before the next starts |
| ThreadPoolExecutor | Executor | Pool of worker threads; good for I/O-bound calls |
| thread safety | Concept | Correctness of a structure when accessed from many threads |

## Detailed Definitions

### asyncio
**Definition**: The standard library's single-threaded, event-loop-based concurrency framework. Best for I/O-bound workloads with thousands of concurrent operations, because tasks cost only a few KB each — far less than threads.
**Example**:
```python
import asyncio

async def fetch(name: str) -> str:
    await asyncio.sleep(0.01)
    return f"{name}:ok"

async def main() -> list[str]:
    return await asyncio.gather(fetch("a"), fetch("b"), fetch("c"))

print(asyncio.run(main()))
```
```text
['a:ok', 'b:ok', 'c:ok']
```
**Complexity**: O(tasks) memory; no OS threads involved.
**Related**: coroutine, event loop, I/O-bound

### concurrency
**Definition**: Structuring a program as many independent tasks that make progress interleaved. Concurrency is a *structure*; parallelism is a *hardware* property. Threads and async both deliver concurrency; only multiprocessing delivers parallelism on CPython.
**Example**:
```python
import threading, time

results: list[str] = []

def work(name: str) -> None:
    time.sleep(0.01)
    results.append(name)

threads = [threading.Thread(target=work, args=(f"t{i}",)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(sorted(results))
```
```text
['t0', 't1', 't2']
```
**Related**: parallelism, GIL, race condition

### coroutine
**Definition**: A function declared with `async def`. Calling it returns a coroutine object; its body runs only when awaited or scheduled on the event loop. Coroutines cannot `time.sleep` — they must `await asyncio.sleep`, or they freeze the loop.
**Example**:
```python
import asyncio

async def tick() -> str:
    await asyncio.sleep(0.01)
    return "tick"

c = tick()                      # body has NOT run yet
print(asyncio.run(c))           # loop drives it
```
```text
tick
```
**Related**: asyncio, event loop

### CPU-bound
**Definition**: A workload whose runtime is dominated by processor computation (loops, math, hashing). On CPython the GIL serializes threads, so threading gives no speedup — use processes (or vectorized libraries) instead.
**Example**:
```python
from concurrent.futures import ProcessPoolExecutor

def burn(n: int) -> int:
    return sum(i * i for i in range(n))     # pure CPU work

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=2) as ex:
        total = sum(ex.map(burn, [1_000_000, 1_000_000]))
    print(total)
```
```text
666667666666000000
```
**Complexity**: O(n) per worker; parallel across processes.
**Related**: GIL, multiprocessing, parallelism

### event loop
**Definition**: The single thread inside asyncio that schedules coroutines. A coroutine yields at every `await`; the loop runs the next ready coroutine. If any coroutine calls `time.sleep`, the whole loop stalls for everyone.
**Example**:
```python
import asyncio

async def main() -> float:
    start = asyncio.get_event_loop().time()
    await asyncio.sleep(0.05)               # yields to the loop
    return asyncio.get_event_loop().time() - start

print(round(asyncio.run(main()), 3))
```
```text
0.05
```
**Related**: asyncio, coroutine, I/O-bound

### GIL
**Definition**: The Global Interpreter Lock — a CPython mutex allowing only one thread to execute Python bytecode at a time. It makes Python threads safe for bytecode but useless for CPU-bound speedups; process-based parallelism bypasses it.
**Example**:
```python
import threading, time

def spin() -> None:
    s = 0
    for _ in range(3_000_000):
        s += 1

start = time.perf_counter()
t1 = threading.Thread(target=spin)
t2 = threading.Thread(target=spin)
t1.start(); t2.start(); t1.join(); t2.join()
print(round(time.perf_counter() - start, 2), "s for two threads")
```
```text
0.35 s for two threads   # ~same as one thread: the GIL serializes bytecode
```
**Related**: CPU-bound, threading, parallelism

### I/O-bound
**Definition**: A workload whose runtime is dominated by waiting — network calls, disk reads, API requests. Waiting releases the GIL, so threads *and* async both win big; async wins on memory when there are thousands of waits.
**Example**:
```python
import asyncio

async def wait(t: float) -> None:
    await asyncio.sleep(t)                  # simulated network wait

async def main() -> float:
    start = asyncio.get_event_loop().time()
    await asyncio.gather(*(wait(0.05) for _ in range(20)))   # 20 waits overlap
    return asyncio.get_event_loop().time() - start

print(round(asyncio.run(main()), 3), "s for 20 waits")
```
```text
0.05 s for 20 waits   # all 20 overlapped on one thread
```
**Related**: asyncio, threading, event loop

### Lock
**Definition**: A mutual-exclusion primitive from `threading`. Only one thread holds a lock at a time, so increments, appends, and compound updates become atomic. Without it, two threads interleave and corrupt shared state.
**Example**:
```python
import threading

counter = 0
lock = threading.Lock()

def bump() -> None:
    global counter
    for _ in range(10_000):
        with lock:
            counter += 1

threads = [threading.Thread(target=bump) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)
```
```text
40000
```
**Complexity**: O(1) acquire/release.
**Related**: race condition, thread safety, threading

### multiprocessing
**Definition**: The standard library module (and pattern) for parallelism: separate interpreter processes, each with its own memory and its own GIL. Communication happens via pickling, which is why workers must be importable at module top level.
**Example**:
```python
from multiprocessing import Pool

def square(x: int) -> int:
    return x * x

if __name__ == "__main__":
    with Pool(2) as pool:
        print(pool.map(square, [1, 2, 3, 4]))
```
```text
[1, 4, 9, 16]
```
**Complexity**: process startup is expensive (~0.3-0.5 s on Windows spawn).
**Related**: ProcessPoolExecutor, spawn context, CPU-bound

### parallelism
**Definition**: Actually executing many tasks at the same instant on different cores. Only processes (or C extensions like NumPy releasing the GIL) give true parallelism in CPython. Threads give concurrency, not parallelism.
**Example**:
```python
from concurrent.futures import ProcessPoolExecutor
import os

def pid() -> int:
    return os.getpid()

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=2) as ex:
        print(sorted(ex.map(pid, [0, 0, 0])))
```
```text
[1234, 1234, 5678]   # two distinct PIDs: two real processes
```
**Related**: concurrency, CPU-bound, multiprocessing

### ProcessPoolExecutor
**Definition**: The `concurrent.futures` high-level pool over worker processes. Call `submit(fn, arg)` or `map(fn, iterable)`; results come back as futures. Bypasses the GIL but pays pickling and spawn overhead per task.
**Example**:
```python
from concurrent.futures import ProcessPoolExecutor

def cube(x: int) -> int:
    return x ** 3

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=2) as ex:
        print(list(ex.map(cube, [1, 2, 3])))
```
```text
[1, 8, 27]
```
**Complexity**: spawn ~0.3-0.5 s per worker on Windows; worth it only when the work is long.
**Related**: multiprocessing, spawn context, CPU-bound

### race condition
**Definition**: A bug where the outcome depends on which thread reaches which statement first. Classic symptom: `counter += 1` from many threads loses updates. Fixed with a `Lock` or a thread-safe structure.
**Example**:
```python
import threading

counter = 0

def bump() -> None:
    global counter
    for _ in range(50_000):
        counter += 1                # read + add + write: NOT atomic

threads = [threading.Thread(target=bump) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter, "expected 100000")
```
```text
81234 expected 100000   # lost updates from interleaving
```
**Related**: Lock, thread safety, threading

### spawn context
**Definition**: The process-start method on Windows (and macOS) that launches a fresh Python interpreter and re-imports the worker module — which is why workers must be top-level functions, never lambdas or locals. Linux's default is `fork`, which inherits memory.
**Example**:
```python
import multiprocessing as mp

def worker(x: int) -> int:
    return x + 1

if __name__ == "__main__":
    ctx = mp.get_context("spawn")
    with ctx.Pool(1) as pool:
        print(pool.map(worker, [1]))
```
```text
[2]
```
**Related**: multiprocessing, ProcessPoolExecutor

### synchronous
**Definition**: Executing one operation to completion before starting the next. The baseline every concurrency model is compared against: predictable, but it serializes waits that could overlap.
**Example**:
```python
import time

def fetch(n: str) -> None:
    time.sleep(0.05)

start = time.perf_counter()
for i in range(3):
    fetch(str(i))
print(round(time.perf_counter() - start, 2), "s sequential")
```
```text
0.15 s sequential   # 3 waits of 0.05, back to back
```
**Related**: concurrency, I/O-bound

### ThreadPoolExecutor
**Definition**: A pool of worker threads from `concurrent.futures`. Ideal for I/O-bound calls (HTTP requests, DB queries) that release the GIL while waiting. Do not expect CPU speedups from it.
**Example**:
```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch(url: str) -> str:
    time.sleep(0.05)
    return f"{url}:ok"

with ThreadPoolExecutor(max_workers=3) as ex:
    start = time.perf_counter()
    results = list(ex.map(fetch, ["a", "b", "c"]))
print(round(time.perf_counter() - start, 2), "s", results)
```
```text
0.05 s ['a:ok', 'b:ok', 'c:ok']
```
**Related**: threading, I/O-bound, GIL

### threading
**Definition**: The standard library module for threads — OS-level units of execution sharing one interpreter. Threads share memory (so no pickling) but fight over the GIL for CPU work; each thread carries ~8 MB of stack.
**Example**:
```python
import threading, time

results: list[str] = []
lock = threading.Lock()

def work(name: str) -> None:
    time.sleep(0.01)
    with lock:
        results.append(name)

threads = [threading.Thread(target=work, args=(f"t{i}",)) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(len(results))
```
```text
4
```
**Related**: ThreadPoolExecutor, GIL, Lock

### thread safety
**Definition**: The property that a structure behaves correctly when accessed from multiple threads. CPython's GIL makes individual bytecodes safe, but compound operations (`counter += 1`, `list.append` + read) still need locks or thread-safe containers.
**Example**:
```python
import queue, threading

q: queue.Queue[int] = queue.Queue()   # thread-safe by design

def produce() -> None:
    for i in range(5):
        q.put(i)

t = threading.Thread(target=produce)
t.start()
print([q.get() for _ in range(5)])
t.join()
```
```text
[0, 1, 2, 3, 4]
```
**Related**: Lock, race condition, threading

## Key Concepts Summary

### Choosing the Right Model
- I/O-bound + few calls → `ThreadPoolExecutor` (simple, shared memory).
- I/O-bound + many concurrent waits → `asyncio` (KB-scale tasks).
- CPU-bound → processes (`ProcessPoolExecutor`), because the GIL blocks threads.
- Never guess: measure sequential vs threads vs processes vs async on your real workload.

### The GIL Explains Everything
- Threads are concurrency, not parallelism, on CPython.
- The GIL is released during I/O waits — that is why threads help I/O.
- Processes each own a GIL — that is why they help CPU.
- C extensions (NumPy) can release the GIL — vectorization is "parallel for free".

### Shared State Safety
- Compound updates (`+=`, `append` then read) are race-prone.
- `Lock` makes critical sections atomic.
- `queue.Queue` is thread-safe; prefer it over manual locking.
- Windows spawn requires top-level, importable worker functions.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. GIL — ___
2. I/O-bound — ___
3. spawn context — ___
4. race condition — ___
5. event loop — ___
6. ProcessPoolExecutor — ___
7. coroutine — ___
8. concurrency — ___
9. Lock — ___
10. parallelism — ___

A. Many tasks in progress, possibly interleaved on one core
B. The CPython lock that serializes bytecode across threads
C. Work dominated by waiting; threads/async shine here
D. Outcome depends on thread interleaving; lost updates
E. Windows process start that re-imports the worker module
F. An `async def` function driven by awaiting
G. Pool of worker processes bypassing the GIL
H. The scheduler that runs coroutines, yielding at `await`
I. Many tasks executing simultaneously on many cores
J. Mutual-exclusion primitive making critical sections atomic

**Answers:** 1-B, 2-C, 3-E, 4-D, 5-H, 6-G, 7-F, 8-A, 9-J, 10-I
