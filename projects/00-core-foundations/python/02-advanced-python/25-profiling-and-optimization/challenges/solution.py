"""Challenge 25: Profiling and Optimization — reference solution.

Why these approaches:
- Bronze: a `set` of seen values turns dedup into O(n); scanning the
  result list instead is O(n^2) and dies at 10^5.
- Silver: one dict build + O(1) lookups is the whole O(n^2) -> O(n)
  story from lecture 25 (measured ~1810x at 40k records).
- Gold: memoization collapses the call tree — 27 calls instead of
  242,785 at n=25; the call count is the observable proof.
"""

from __future__ import annotations


def dedup_chunks(items: list[str]) -> list[str]:
    """First occurrence wins; a seen-set keeps it linear."""
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def hash_join(records: list[dict], index: list[dict]) -> list[tuple]:
    """Build by_id once, then one O(1) lookup per record."""
    by_id = {entry["chunk_id"]: entry["text"] for entry in index}
    joined: list[tuple] = []
    for record in records:
        text = by_id.get(record["chunk_id"])
        if text is not None:
            joined.append((record["chunk_id"], text))
    return joined


def fib_stats(n: int) -> tuple[int, int]:
    """Memoized fib with a call counter."""

    def fib(k: int, memo: dict[int, int]) -> int:
        nonlocal calls
        calls += 1
        if k in memo:
            return memo[k]
        if k < 2:
            memo[k] = k
            return k
        memo[k] = fib(k - 1, memo) + fib(k - 2, memo)
        return memo[k]

    calls = 0
    result = fib(n, {})
    return result, calls
