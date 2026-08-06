"""
Challenge 48: Comprehensions & Modern Syntax — Starter Code
============================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator


def tokenize_and_filter(texts: list[str], min_len: int) -> list[str]:
    """Return uppercased tokens with len(token) >= min_len.

    Must be a single list comprehension (transform + filter).
    """
    raise NotImplementedError


def parse_floats(
    values: list[str],
    parser: Callable[[str], float | None],
) -> list[float]:
    """Return parsed floats for values parser() does not map to None.

    Each value must be parsed EXACTLY once (walrus := or loop variable).
    """
    raise NotImplementedError


def dedupe_stream(rows: Iterable[str]) -> Iterator[str]:
    """Yield rows in first-seen order, dropping duplicates, lazily.

    Must be a generator: the first output requires only a bounded prefix
    of the input. Single pass, dedup set is the only retained state.
    """
    raise NotImplementedError
