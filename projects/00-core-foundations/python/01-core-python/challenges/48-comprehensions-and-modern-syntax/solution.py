"""
Challenge 48: Comprehensions & Modern Syntax — Reference Solution
==================================================================
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator


def tokenize_and_filter(texts: list[str], min_len: int) -> list[str]:
    """Return uppercased tokens with len(token) >= min_len.

    Why this approach: a single list comprehension expresses transform
    (t.upper()) and filter (len(t) >= min_len) in one readable line.
    O(n) time, O(n) space for the result.
    """
    return [t.upper() for t in texts if len(t) >= min_len]


def parse_floats(
    values: list[str],
    parser: Callable[[str], float | None],
) -> list[float]:
    """Return parsed floats for values parser() does not map to None.

    Why this approach: the walrus computes the parse once per value and
    binds it, so the condition and the result share one call. A naive
    double-parse would call parser 2n times; this is exactly n. O(n)
    calls, O(n) space for the result.
    """
    return [parsed for v in values if (parsed := parser(v)) is not None]


def dedupe_stream(rows: Iterable[str]) -> Iterator[str]:
    """Yield rows in first-seen order, dropping duplicates, lazily.

    Why this approach: a generator with a seen-set yields as it consumes,
    so the first output needs only the first distinct prefix of the input.
    Each row is fetched exactly once; the set holds only unique rows
    (O(unique) memory, which is the minimum for exact dedup).
    """
    seen: set[str] = set()
    for row in rows:
        if row not in seen:
            seen.add(row)
            yield row
