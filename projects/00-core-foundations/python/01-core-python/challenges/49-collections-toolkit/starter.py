"""
Challenge 49: Collections Toolkit — Starter Code
==================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Iterable


def top_k_tokens(tokens: list[str], k: int) -> list[tuple[str, int]]:
    """Return the k most frequent tokens as (token, count) pairs.

    Order: count descending, then alphabetically among ties.
    """
    raise NotImplementedError


def top_k_scores(scores: Iterable[float], k: int) -> list[float]:
    """Return the k largest scores, descending. O(n log k), not O(n log n)."""
    raise NotImplementedError


def top_k_stream(
    stream: Iterable[tuple[str, float]],
    k: int,
) -> list[tuple[str, float]]:
    """Return the k highest-scoring (doc_id, score) pairs, descending.

    Single pass, O(k) memory — never materialize the stream.
    """
    raise NotImplementedError
