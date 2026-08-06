# Advanced Python - 21: Concurrency Comparison

## Topic Overview

Sequential, threads, processes, and async can all run the same workload — but they are not interchangeable. This lecture answers the question every inference server and batch pipeline is built around: **which one should I use, and how do I know?** The answer is not a rule of thumb; it is a measurement. I/O-bound work (waiting on a network, a disk, another service) overlaps beautifully in threads or async. CPU-bound work (pure arithmetic in Python) is serialized by the GIL in threads and only truly parallelizes across processes. Async gives thread-scale concurrency at kilobytes of memory per task.

This is the synthesis topic of the concurrency section: `04-async-await.py` taught the primitives, `16-threading.py` taught locks and pools, `17-multiprocessing.py` taught processes — this lecture compares all four strategies side by side on the same workloads and gives you the decision flowchart to choose between them. The companion exercise `21-concurrency-comparison.py` measures everything you read here on your own machine.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Classify any workload as I/O-bound or CPU-bound
2. Explain what the GIL is, what it protects, and what it blocks
3. Predict when threads will speed up a workload and when they cannot
4. Explain why processes pay a startup cost and when it is worth paying
5. Use the unified `concurrent.futures` API for both thread and process pools
6. Describe async as cooperative single-threaded concurrency
7. Read a side-by-side benchmark table and explain each column
8. Apply the four-way decision flowchart to a real service design

---

## Prerequisites

| Need | Where |
|---|---|
| Threads, locks, pools | `16-threading-lecture.md` |
| Processes, shared state | `17-multiprocessing-lecture.md` |
| Async primitives | `04-async-await-lecture.md` |
| The GIL concept | `16-threading-lecture.md` |
| Timing basics | `25-profiling-and-optimization-lecture.md` |

---

## 1. The Two Workload Families

Every task you will ever parallelize is mostly one of two things: it spends its time **waiting** or it spends its time **computing**.

```python
import time

def io_task(delay: float) -> float:
    """I/O-bound: the CPU is idle while we wait on something else."""
    time.sleep(delay)          # releases the GIL: other threads can run
    return delay

def cpu_task(n: int) -> int:
    """CPU-bound: pure arithmetic, the GIL is held for the whole loop."""
    total = 0
    for i in range(n):
        total += i * i
    return total
```

```
No output -- these are the workloads we will measure in section 3.
```

An I/O-bound task (an HTTP call to an embedding API, reading a file, waiting on a database) uses almost no CPU — it waits. A CPU-bound task (tokenizing 1M documents, a Python loop over a matrix) uses the CPU the whole time and never yields. Everything below follows from this single distinction.

---

## 2. The GIL: What It Is and What It Costs

The Global Interpreter Lock is a mutex inside CPython that allows **exactly one thread to execute Python bytecode at a time**. It exists because CPython's memory management (reference counting) is not thread-safe without it.

```python
import threading

shared = 0
def increment() -> None:
    global shared
    for _ in range(1_000_000):
        shared += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(shared)  # 1000000: serialized -- the GIL let only one thread run at a time
```

```
1000000
```

The crucial nuance: the GIL is **released** during blocking I/O. `time.sleep`, socket reads, file reads, and database waits all drop the lock, so other threads can run. That is exactly why threads help I/O-bound code: the threads mostly wait, and waiting does not need the lock. CPU-bound code never releases the lock, so four threads compute at the speed of one. Since Python 3.13 the GIL has a faster scheduling algorithm, but the fundamental serialization of bytecode remains (free-threaded builds exist but are not the default).

---

## 3. Measuring All Four Strategies

The exercise `21-concurrency-comparison.py` runs the same workload four ways and prints a table. For I/O: 50 sleeps of 0.01s. For CPU: 24M arithmetic iterations.

```python
# Representative output from the exercise (your machine will differ):
# --- I/O-bound: 50 sleeps of 0.01s ---
#   sequential: 0.517s
#      threads: 0.074s     (7x faster: the sleeps overlap)
#    processes: 0.401s     (pays spawn cost, no benefit on pure I/O)
#        async: 0.014s     (37x faster: one thread, zero spawn)
# --- CPU-bound: 24M pure arithmetic iterations ---
#   sequential: 1.660s
#      threads: 1.576s     (0.95x: the GIL serializes arithmetic)
#    processes: 0.750s     (2.2x faster: four real cores)
```

```
See the block above -- the table is the measured truth.
```

Three facts fall out: threads overlap I/O waits by ~7x; threads do not speed up CPU work (0.95x — noise); processes speed up CPU work by ~2.2x on 4 workers. Async beats even threads on I/O because it creates no OS threads at all.

---

## 4. Threads: The I/O Sweet Spot

Threads are the right tool when the work is I/O-bound **and** the code is synchronous. `ThreadPoolExecutor` gives you a pool with one API call.

```python
from concurrent.futures import ThreadPoolExecutor

def fetch_one(url: str) -> str:
    time.sleep(0.01)          # simulated HTTP
    return f"ok:{url}"

urls = [f"http://api/{i}" for i in range(50)]
with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch_one, urls))
print(len(results), results[0])
```

```
50 ok:http://api/0
```

Rules that keep threads safe: share state through `queue.Queue` or `concurrent.futures` results, never through bare globals; use a `Lock` if you must mutate shared objects; keep the pool sized to the waiting, not to the cores.

---

## 5. Processes: The CPU Escape Hatch

When the GIL blocks parallel CPU work, processes escape it entirely: each worker is a full interpreter with its own GIL. The cost is startup — on Windows, **spawn** imports the module in every worker, which takes ~0.3-0.5s for 4 workers.

```python
from concurrent.futures import ProcessPoolExecutor

def crunch(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total

with ProcessPoolExecutor(max_workers=4) as pool:
    totals = list(pool.map(crunch, [6_000_000] * 4))
print(sum(totals) > 0)   # the pool worked; 4x speedup for big enough n
```

```
True
```

Two hard rules for process pools on Windows: worker functions must live at **module top level** (spawn re-imports the module; closures crash with `AttributeError: Can't get local object`), and the workload must be **big enough to amortize spawn**. 50 tiny sleeps in processes lose to threads (0.40s vs 0.07s in the table above) because spawn swamps the work.

---

## 6. Async: Cooperative Concurrency on One Thread

Async runs thousands of tasks on one thread by **cooperation**: each task yields at every `await`, and the event loop resumes whichever task is ready. No OS threads, no spawn cost, kilobytes per task.

```python
import asyncio

async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)      # yields: the loop runs other tasks
    return f"{name}:done"

async def main() -> None:
    results = await asyncio.gather(*(fetch(f"t{i}", 0.01) for i in range(50)))
    print(len(results), results[0])

asyncio.run(main())
```

```
50 t0:done
```

Async is the right default for I/O-bound work in modern services: 200 concurrent LLM calls are 200 tasks, not 200 threads. The caveat: the whole codebase must be async — a single blocking `time.sleep` freezes the entire loop (see `22-asyncio-advanced-lecture.md`).

---

## 7. Memory: The Hidden Fourth Dimension

Speed is only half the comparison. The number of concurrent units each strategy can afford differs by orders of magnitude.

| Strategy | ~memory per 1000 units (measured in exercise 21) |
|---|---|
| async tasks | ~70 KB traced |
| threads | ~150 KB objects + ~8 MB native stack each once started |
| processes | full interpreter each (~10-30 MB); 1000 processes ~ 10-30 GB |

```
This is why "1000 concurrent requests" means async -- threads would need
~8 GB of stacks and processes are simply impossible at that scale.
```

---

## 8. `concurrent.futures`: One API, Two Executors

The entire comparison above uses two classes that share one interface: `map()`, `submit()`, context-manager shutdown.

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def work(n: int) -> int:
    return n * n

for Executor in (ThreadPoolExecutor, ProcessPoolExecutor):
    with Executor(max_workers=4) as pool:
        print(Executor.__name__, list(pool.map(work, [1, 2, 3])))
```

```
ThreadPoolExecutor [1, 4, 9]
ProcessPoolExecutor [1, 4, 9]
```

Swapping the concurrency strategy is a one-line change: the executor class. That is the unified API's value — write the pipeline once, choose the executor when you know whether the workload is I/O- or CPU-bound.

---

## 9. The Decision Flowchart

```
Is the workload waiting (network, disk, service)?
|
+-- yes: I/O-bound
|      |
|      +-- can the code be async?  -> async (default: scale, KB memory)
|      |
|      +-- sync-only codebase?     -> ThreadPoolExecutor (overlap waits)
|
+-- no: CPU-bound
       |
       +-- Python arithmetic?      -> ProcessPoolExecutor (escape the GIL)
       |
       +-- numeric hot loop?       -> NumPy / C / Rust, not more processes
```

```
(Flowchart -- no program output.)
```

The last branch matters: if the "CPU-bound" work is matrix math, the real answer is vectorization (a Python loop over 1M rows is ~100x slower than the NumPy equivalent), not 16 processes. Processes parallelize Python; vectorization removes the Python.

---

## Common Mistakes to Avoid

### Mistake 1: Threads for CPU-bound work
```
# WRONG -- the GIL serializes the arithmetic, ~1x speedup at best
with ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(cpu_task, chunks))
# CORRECT -- processes each run their chunk on a real core
with ProcessPoolExecutor(max_workers=8) as pool:
    list(pool.map(cpu_task, chunks))
```

### Mistake 2: Processes for tiny workloads
```
# WRONG -- spawn cost (~0.3-0.5s on Windows) exceeds the work
with ProcessPoolExecutor(max_workers=4) as pool:
    list(pool.map(io_task, [0.01] * 50))     # loses to threads
# CORRECT -- processes only when the work amortizes startup (seconds of CPU)
```

### Mistake 3: A thread per request
```
# WRONG -- 1000 threads x 8 MB stack = 8 GB virtual memory
threads = [threading.Thread(target=fetch, args=(i,)) for i in range(1000)]
# CORRECT -- a bounded pool (max_workers=8) or async tasks
```

### Mistake 4: Benchmarking only the strategy you like
```
# WRONG -- "threads are 7x faster than sequential" proves nothing about
#          the CPU-bound case. Measure the SAME workload 4 ways.
# CORRECT -- run the side-by-side table from section 3 every time.
```

### Mistake 5: Forgetting Windows spawn rules
```
# WRONG -- a closure as the pool target crashes on Windows
with ProcessPoolExecutor() as pool:
    pool.map(lambda x: x * 2, range(10))
# CORRECT -- module-level functions only; guard entry points with
#            if __name__ == "__main__":
```

---

## Best Practices

1. **Classify first**: I/O-bound or CPU-bound — everything follows from this.
2. **Default to async** for new I/O-bound code; it scales further than threads.
3. **Use `concurrent.futures`** for pools; prefer it over raw thread/process objects.
4. **Keep CPU work big enough** to amortize process spawn before comparing.
5. **Never assert on wall-clock** in CI; assert on *ratios* between strategies.
6. **Put process workers at module level** for Windows spawn compatibility.
7. **Measure memory too**: async wins at 1000s of concurrent units; processes are impossible there.
8. **Check the workload shape again after refactoring**: an async pipeline can silently become CPU-bound.
9. **Size thread pools to the wait, not the cores**; size process pools to the cores.
10. **Reach for vectorization first** when the CPU-bound work is numeric.

---

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Thread creation | ~50-100 µs each + ~8 MB stack reservation | ~8 MB/thread (virtual) | async task — ~KB, µs |
| Process spawn (Windows) | ~0.1-0.5 s per pool | full interpreter per worker (~10-30 MB) | async/threads for I/O |
| `time.sleep` in a thread | releases GIL, others run | 0 | `asyncio.sleep` — one thread, no stack |
| Python CPU loop, 4 threads | ~1x sequential (GIL) | 0 | 4 processes — ~3-4x on 4 cores |
| Python CPU loop, 4 processes | ~2-4x sequential (spawn amortized) | 4 interpreters | NumPy/C — 10-100x |
| 1000 async tasks | µs each, cooperative | ~70 KB traced total | threads — ~8 GB stacks |

---

## AI Engineering Relevance

**Where this shows up:** an embedding pipeline over 10k documents is the exact comparison above, twice. If the embeddings come from an API (OpenAI, Cohere), the workload is I/O-bound — the correct design is async with a `Semaphore` for rate limits, or threads if the codebase is sync. If the embeddings come from a local model (sentence-transformers), the workload is CPU-bound — a `ProcessPoolExecutor` over a few workers parallelizes the batch, or better, the model does the vectorization internally.

| Concept here | Used for |
|---|---|
| Async + semaphore | 200 concurrent LLM calls under a provider rate limit |
| Process pool | parallel local-model inference across documents |
| GIL reasoning | why inference servers use processes (or async), not threads |
| Spawn cost awareness | batch jobs that must decide pool size vs startup |

**Scale note:** at 1k concurrent requests, async tasks cost ~70 KB of bookkeeping; threads cost ~8 GB of stacks; processes are not an option. At 10k documents, a CPU-bound process pool must chunk large enough that spawn (~0.5s) is <1% of the run. The decision you make at 100 requests is forced on you again at 10k — the flowchart does not change, only the stakes.

---

## Practice Exercises

### Exercise 1: Classify the Workload (Difficulty: Easy)
For each task, state I/O-bound or CPU-bound and the best strategy: (a) calling an embedding API; (b) tokenizing 1M docs with a pure-Python loop; (c) loading 10 parquet files from disk; (d) computing cosine similarity of 100k vectors with NumPy.

### Exercise 2: One API, Two Executors (Difficulty: Easy)
Write `run_with(executor_cls, data, fn)` that maps `fn` over `data` using any `concurrent.futures` executor class. Verify it works with both `ThreadPoolExecutor` and `ProcessPoolExecutor` on a pure function.

### Exercise 3: Threads Help I/O, Not CPU (Difficulty: Medium)
Implement `benchmark(kind: str) -> (float, float)` that runs 30 units of work sequentially and on a 6-thread pool, returning both times. For `kind="io"` use `time.sleep(0.01)`; for `kind="cpu"` use 1M iterations. Print both tables and the ratios.

### Exercise 4: Spawn-Cost Amortization (Difficulty: Medium)
Measure a process pool on CPU chunks of size 10^5, 10^6, 10^7 (4 workers). Print the speedup per size. At what size does the pool beat sequential? Explain the crossover with spawn cost.

### Exercise 5: The Memory Column (Difficulty: Hard)
Using `tracemalloc`, measure the traced memory of 500 async tasks vs 500 thread objects vs 500 process objects. Print all three numbers and explain why processes "win" the memory comparison only until you start them.

### Exercise 6: Decision Flowchart on a Real Service (Difficulty: Hard)
Design the concurrency strategy for a RAG service: 1000 documents to chunk+embed via an API with a 50 req/s rate limit, then a local reranker (CPU) on the top-100. Specify async vs processes per stage, with Semaphore for the API and a pool size for the reranker. Justify each choice with the measured facts from this lecture.

---

## Summary

| Concept | Description |
|---|---|
| I/O-bound | waits on network/disk/service; threads and async overlap the waits |
| CPU-bound | pure computation; GIL serializes threads, processes parallelize |
| GIL | one thread executes bytecode at a time; released during blocking I/O |
| Threads | ~7x on I/O, ~1x on CPU, ~8 MB stack each |
| Processes | ~2-4x on CPU, full interpreter per worker, ~0.3-0.5s spawn |
| Async | one thread, thousands of tasks, ~KB each, I/O-bound only |
| `concurrent.futures` | one API for both pools; swap by class |
| Decision | async for API I/O, processes for local CPU, vectorize the numerics |

The threads/processes/async decision is not a personality preference: it is a measurement. The same workload, run four ways on one machine, answers the question better than any blog post. Every inference server, embedding job, and batch pipeline in this course will reuse this exact comparison.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Run I/O work concurrently (async) | `asyncio.gather(*(f(i) for i in items))` |
| Run I/O work on a pool (sync) | `ThreadPoolExecutor(max_workers=8).map(f, items)` |
| Run CPU work in parallel | `ProcessPoolExecutor(max_workers=os.cpu_count()).map(f, items)` |
| Cap concurrent API calls | `asyncio.Semaphore(n)` around each call |
| Measure one strategy | `time.perf_counter()` around the pool context |
| Compare strategies fairly | run the same workload all 4 ways, print a table |
| Protect against spawn crashes | workers at module level + `if __name__ == "__main__":` |

---

## Next Steps

Next: **[22-asyncio-advanced-lecture.md](22-asyncio-advanced-lecture.md)** — TaskGroup cancellation, semaphores, and never blocking the loop: the production async toolkit this lecture pointed at.
Continues in: **[Phase 8 — MLOps: model serving](../../08-mlops/lectures/)-lecture.md** — where the async-vs-processes choice becomes a deployment decision.
Official docs: [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html), [threading](https://docs.python.org/3/library/threading.html), [multiprocessing](https://docs.python.org/3/library/multiprocessing.html), [asyncio](https://docs.python.org/3/library/asyncio.html), [GIL glossary](https://docs.python.org/3/glossary.html#term-global-interpreter-lock).
