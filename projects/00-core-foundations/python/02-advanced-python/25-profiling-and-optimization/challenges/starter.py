"""Challenge 25: Profiling and Optimization — starter (signatures only)."""

from __future__ import annotations


def dedup_chunks(items: list[str]) -> list[str]:
    """First-occurrence dedup, order preserved. Must be O(n) (set-based)."""
    raise NotImplementedError


def hash_join(records: list[dict], index: list[dict]) -> list[tuple]:
    """Join records to index on chunk_id; skip records with missing ids."""
    raise NotImplementedError


def fib_stats(n: int) -> tuple[int, int]:
    """Return (fib(n), number of recursive calls) with memoization."""
    raise NotImplementedError
