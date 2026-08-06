"""Challenge 21: Concurrency Comparison — reference solution.

Why these approaches:
- Bronze is a pure decision table from the lecture's rules.
- Silver uses ThreadPoolExecutor because time.sleep releases the GIL,
  so I/O waits genuinely overlap — measured, not asserted.
- Gold uses ProcessPoolExecutor with a TOP-LEVEL worker: Windows spawn
  re-imports the worker's module, so lambdas/nested functions fail.
"""

from __future__ import annotations

import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def choose_model(workload: str, calls: int) -> str:
    """Decision table: I/O-bound + many calls -> async, few -> threads,
    CPU-bound -> processes (GIL), unknown -> ValueError."""
    if workload == "io":
        return "async" if calls > 100 else "threads"
    if workload == "cpu":
        return "processes"
    raise ValueError(f"unknown workload: {workload}")


def run_io_overlap(sleeps: int, delay: float) -> float:
    """Overlap `sleeps` waits of `delay` s across 8 worker threads."""
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(time.sleep, [delay] * sleeps))
    return time.perf_counter() - start


def run_cpu_sequential(chunks: int, work: int) -> float:
    """Baseline: run each chunk one after another in this process."""
    start = time.perf_counter()
    for _ in range(chunks):
        _cpu_worker(work // chunks)
    return time.perf_counter() - start


def run_cpu_parallel(chunks: int, work: int) -> float:
    """One process per chunk: each worker gets its own GIL, so the
    bytecode actually runs in parallel (on multiple cores)."""
    unit = work // chunks
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=chunks) as pool:
        list(pool.map(_cpu_worker, [unit] * chunks))
    return time.perf_counter() - start


def _cpu_worker(n: int) -> int:
    """Pure CPU work. Module-level on purpose: spawn re-imports this
    module in each child process."""
    return sum(i * i for i in range(n))
