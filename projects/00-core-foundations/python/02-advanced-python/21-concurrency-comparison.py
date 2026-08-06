"""
Advanced Python - 21: Concurrency Comparison
==============================================
Topics: GIL mechanics; I/O-bound vs CPU-bound; sequential vs threads vs
        processes vs async; concurrent.futures unified API; decision flow.

Why this matters for AI/backend engineering:
    Every inference server, embedding job, and batch pipeline makes this
    exact choice. Embedding 10k documents: use async/threads when the work
    waits on an API (I/O-bound); use processes when a local model hogs the
    CPU. Picking wrong can mean a 10x latency difference or a server that
    cannot use its cores. This file measures the difference instead of
    guessing.

Run:      python 21-concurrency-comparison.py
Verify:   python 21-concurrency-comparison.py --verify
Reference: https://docs.python.org/3/library/concurrent.futures.html
           https://docs.python.org/3/glossary.html#term-global-interpreter-lock
"""

from __future__ import annotations

import asyncio
import multiprocessing
import os
import random
import sys
import threading
import time
import tracemalloc
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

random.seed(42)
os.environ.setdefault("MPLBACKEND", "Agg")   # never open a GUI window

# ============================================================
# 1. The Two Workloads
# ============================================================
# One I/O-bound and one CPU-bound task. Both live at module top level:
# on Windows, every spawned worker process re-imports this module, so
# picklable, importable functions are mandatory (closures crash spawn).
# Complexity: io_task is O(1) wall-clock (~delay); cpu_task is O(n) work.

def io_task(delay: float) -> float:
    """Simulate one I/O-bound unit: a network round-trip of `delay` seconds."""
    time.sleep(delay)          # sleep releases the GIL, so threads can overlap
    return delay


def cpu_task(n: int) -> int:
    """Simulate one CPU-bound unit: pure arithmetic that holds the GIL."""
    total = 0
    for i in range(n):
        total += i * i
    return total


# ============================================================
# 2. The Four Execution Strategies
# ============================================================
# Sequential: one after another. Threads: concurrent.futures, GIL applies.
# Processes: real parallelism, pays spawn cost. Async: cooperative, one
# thread, thousands of tasks. The last three share one signature so the
# comparison is apples-to-apples.

def run_sequential(delays: list[float]) -> float:
    """Run I/O tasks one at a time. Complexity: O(k) wall-clock."""
    start = time.perf_counter()
    for d in delays:
        io_task(d)
    return time.perf_counter() - start


def run_threads(delays: list[float], workers: int = 8) -> float:
    """Run I/O tasks on a thread pool. GIL is released during sleep."""
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(io_task, delays))
    return time.perf_counter() - start


def run_processes(delays: list[float], workers: int = 4) -> float:
    """Run I/O tasks in processes. Pays full interpreter spawn cost."""
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        list(pool.map(io_task, delays))
    return time.perf_counter() - start


async def _async_sleep(delay: float) -> None:
    """Coroutine that yields to the event loop instead of blocking."""
    await asyncio.sleep(delay)


async def _run_async_io(delays: list[float]) -> None:
    """Gather all sleeps inside a running loop (gather needs a loop)."""
    await asyncio.gather(*(_async_sleep(d) for d in delays))


def run_async(delays: list[float]) -> float:
    """Run I/O tasks on ONE thread, cooperatively interleaved."""
    start = time.perf_counter()
    asyncio.run(_run_async_io(delays))
    return time.perf_counter() - start


def run_cpu_sequential(chunks: list[int]) -> float:
    """CPU-bound, one at a time. Complexity: O(sum of chunks)."""
    start = time.perf_counter()
    for n in chunks:
        cpu_task(n)
    return time.perf_counter() - start


def run_cpu_threads(chunks: list[int], workers: int = 4) -> float:
    """CPU-bound on threads: the GIL serializes the arithmetic."""
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(cpu_task, chunks))
    return time.perf_counter() - start


def run_cpu_processes(chunks: list[int], workers: int = 4) -> float:
    """CPU-bound in processes: each worker runs its chunk in parallel."""
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        list(pool.map(cpu_task, chunks))
    return time.perf_counter() - start


# ============================================================
# 3. Measured Head-to-Head
# ============================================================
# Timings are printed, never asserted on: wall-clock is not reproducible.
# Assertions later use *ratios* between the strategies on the same machine.
# CPU work must be big enough to amortize Windows process spawn (~0.3-0.5s
# for 4 workers) or the "processes win" claim becomes unmeasurable.

_CPU_TOTAL: int = 24_000_000          # iterations split across 4 workers
_CPU_CHUNK: int = _CPU_TOTAL // 4     # per-worker share

def demo_io_comparison() -> dict[str, float]:
    """Measure 50 tiny I/O tasks (50 x 0.01s) four ways."""
    delays = [0.01] * 50
    results: dict[str, float] = {}
    print("\n--- I/O-bound: 50 sleeps of 0.01s ---")
    results["sequential"] = run_sequential(delays)
    results["threads"] = run_threads(delays)
    results["processes"] = run_processes(delays)
    results["async"] = run_async(delays)
    for name, elapsed in results.items():
        print(f"  {name:>10}: {elapsed:.3f}s")
    print(f"  -> threads/async overlap the sleeps; processes pay spawn cost")
    return results


def demo_cpu_comparison() -> dict[str, float]:
    """Measure the same arithmetic chunked across 4 workers."""
    chunks = [_CPU_CHUNK] * 4          # 24M iterations total, ~1.5s sequential
    results: dict[str, float] = {}
    print("\n--- CPU-bound: 24M pure arithmetic iterations ---")
    results["sequential"] = run_cpu_sequential(chunks)
    results["threads"] = run_cpu_threads(chunks)
    results["processes"] = run_cpu_processes(chunks)
    for name, elapsed in results.items():
        print(f"  {name:>10}: {elapsed:.3f}s")
    print(f"  -> threads cannot help (GIL); processes use all cores")
    return results


# ============================================================
# 4. Memory Per Unit of Concurrency
# ============================================================
# 1000 tasks fit in <1 MB. 1000 threads need ~2 MB of objects plus ~8 MB
# native stack reservation each once started. 1000 processes are ~10-30 GB:
# each one is a full interpreter. This is WHY async wins at scale.

async def _make_tasks(count: int) -> list[asyncio.Task[None]]:
    """Create `count` idle tasks inside a running loop."""
    async def _noop() -> None:
        return None
    return [asyncio.create_task(_noop()) for _ in range(count)]


def traced_delta(create: object, count: int) -> int:
    """Return traced bytes created by `create(count)`, in a clean trace."""
    tracemalloc.start()
    before = tracemalloc.take_snapshot()
    if create is _make_tasks:                          # async needs a loop
        async def _inner() -> int:
            tasks = await _make_tasks(count)
            for t in tasks:
                t.cancel()
            return 0
        asyncio.run(_inner())
    else:
        objs = create(count)                           # type: ignore[operator]
        del objs
    after = tracemalloc.take_snapshot()
    tracemalloc.stop()
    return sum(s.size_diff for s in after.compare_to(before, "filename"))


def demo_memory_comparison(verbose: bool = True) -> tuple[int, int, int]:
    """Measure traced memory for 1000 tasks / threads / processes."""
    count = 1000
    if verbose:
        print("\n--- Traced memory for 1000 units of concurrency ---")
    tasks_mem = traced_delta(_make_tasks, count)
    threads_mem = traced_delta(
        lambda n: [threading.Thread(target=io_task, args=(0.0,)) for _ in range(n)],
        count,
    )
    processes_mem = traced_delta(
        lambda n: [multiprocessing.Process(target=io_task, args=(0.0,)) for _ in range(n)],
        count,
    )
    if verbose:
        print(f"  asyncio tasks  : ~{tasks_mem // 1024:>5} KB")
        print(f"  threads        : ~{threads_mem // 1024:>5} KB + ~8 MB stack each when started")
        print(f"  process shells : ~{processes_mem // 1024:>5} KB + full interpreter (~10-30 MB) each when started")
        print(f"  -> 1000 processes would be ~10-30 GB; 1000 tasks fit in <1 MB")
    return tasks_mem, threads_mem, processes_mem


# ============================================================
# 5. The Decision Flowchart
# ============================================================
# Is the workload waiting on something (network, disk, another service)?
#   yes -> I/O-bound: async first (thousands of tasks, KB each); threads if
#          the code is sync-only and refactoring to async is too costly.
#   no  -> CPU-bound: processes / multiprocessing for CPU-hungry Python;
#          for the hot loop itself, reach for NumPy/C/Rust instead.
# Never: threads for CPU-bound Python. The GIL makes it a slower sequential.


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: using a ThreadPoolExecutor on a CPU-bound loop expecting
#   speedup -- the GIL serializes bytecode, so 4 threads run at ~1x.
# CORRECT:
#   ProcessPoolExecutor for CPU-bound; keep the workload big enough that
#   spawn cost (~0.3-1s on Windows) is amortized.
# MISTAKE: 100 threads for 100k I/O tasks (8 MB stack each = 800 MB).
# CORRECT: async tasks (KB each) or a small thread pool + queue.
# MISTAKE: benchmarking one strategy only.
# CORRECT: measure all four on the same workload before choosing.


# ============================================================
# Self-Verification  (MANDATORY -- every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # 1. Correctness across strategies: results must agree.
    chunks = [_CPU_CHUNK] * 4
    expected = sum(cpu_task(n) for n in chunks)
    with ThreadPoolExecutor(max_workers=4) as pool:
        threaded_total = sum(pool.map(cpu_task, chunks))
    with ProcessPoolExecutor(max_workers=4) as pool:
        processed_total = sum(pool.map(cpu_task, chunks))
    assert threaded_total == expected, \
        "threaded CPU result must equal the sequential result"
    assert processed_total == expected, \
        "process CPU result must equal the sequential result"

    # 2. Threads beat sequential on I/O (sleeps overlap: ~7x on the bench).
    delays = [0.01] * 50
    seq_io = run_sequential(delays)
    thr_io = run_threads(delays)
    assert thr_io < seq_io * 0.5, \
        "threads must beat sequential on I/O-bound work (got %s vs %s)" % (thr_io, seq_io)

    # 3. Threads do NOT beat sequential on CPU (the GIL).
    seq_cpu = run_cpu_sequential(chunks)
    thr_cpu = run_cpu_threads(chunks)
    assert thr_cpu >= seq_cpu * 0.85, \
        "threads must NOT beat sequential on CPU-bound work (GIL): %s vs %s" % (thr_cpu, seq_cpu)

    # 4. Processes DO beat sequential on CPU (spawn cost amortized).
    proc_cpu = run_cpu_processes(chunks)
    assert proc_cpu < seq_cpu * 0.85, \
        "processes must beat sequential on CPU-bound work: %s vs %s" % (proc_cpu, seq_cpu)

    # 5. Async uses the least memory per unit of concurrency.
    tasks_mem, threads_mem, _ = demo_memory_comparison(verbose=False)
    assert tasks_mem < threads_mem, \
        "async tasks must use less traced memory than threads: %s vs %s" % (tasks_mem, threads_mem)

    # 6. Async overlaps I/O like threads do.
    async_io = run_async(delays)
    assert async_io < seq_io * 0.5, \
        "async must beat sequential on I/O-bound work (got %s vs %s)" % (async_io, seq_io)

    print("\n[OK] 21-concurrency-comparison: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("=" * 60)
        print("CONCURRENCY COMPARISON: 4 WAYS TO RUN THE SAME WORK")
        print("=" * 60)
        io_times = demo_io_comparison()
        cpu_times = demo_cpu_comparison()
        demo_memory_comparison()
        print("\n--- Decision ---")
        print("  I/O-bound  -> async (or threads for sync code): %.3fs vs %.3fs sequential"
              % (io_times["async"], io_times["sequential"]))
        print("  CPU-bound  -> processes: %.3fs vs %.3fs sequential"
              % (cpu_times["processes"], cpu_times["sequential"]))
        print("  threads on CPU -> no help: %.3fs (GIL)" % cpu_times["threads"])
        print("\n1. Threads overlap I/O waits; processes run CPU in parallel.")
        print("2. Processes pay spawn cost; keep CPU work big enough to amortize it.")
        print("3. Async gives thread-scale concurrency at KB memory per task.")
        _verify()
