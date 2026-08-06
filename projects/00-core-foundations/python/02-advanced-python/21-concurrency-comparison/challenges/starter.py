"""Challenge 21: Concurrency Comparison — starter (signatures only)."""

from __future__ import annotations


def choose_model(workload: str, calls: int) -> str:
    """Return the concurrency model for a workload.

    "io" + many calls -> "async"; "io" + few calls -> "threads";
    "cpu" -> "processes"; anything else -> ValueError.
    """
    raise NotImplementedError


def run_io_overlap(sleeps: int, delay: float) -> float:
    """Run `sleeps` I/O waits of `delay` s on a thread pool; return elapsed.

    Overlapped execution must take far less than sleeps * delay.
    """
    raise NotImplementedError


def run_cpu_sequential(chunks: int, work: int) -> float:
    """Run `chunks` CPU units of `work // chunks` each in a plain loop.

    Return the total elapsed time.
    """
    raise NotImplementedError


def run_cpu_parallel(chunks: int, work: int) -> float:
    """Run the same total work across a ProcessPoolExecutor.

    Return the total elapsed time. Must beat the sequential version.
    """
    raise NotImplementedError


def _cpu_worker(n: int) -> int:
    """Return sum(i * i for i in range(n)). Must be module-level."""
    raise NotImplementedError
