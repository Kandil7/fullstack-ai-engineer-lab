"""
Challenge 49: Collections Toolkit — Reference Solution
=======================================================
"""

from __future__ import annotations

import heapq
from collections import Counter
from collections.abc import Iterable


def top_k_tokens(tokens: list[str], k: int) -> list[tuple[str, int]]:
    """Return the k most frequent tokens as (token, count) pairs.

    Why this approach: Counter builds the frequency table in O(n), then a
    sort on (-count, token) gives deterministic ordering with alphabetical
    tie-breaks. O(n log n) for the full sort, O(k) to slice.
    """
    if k <= 0:
        return []
    freq = Counter(tokens)
    ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:k]


def top_k_scores(scores: Iterable[float], k: int) -> list[float]:
    """Return the k largest scores, descending.

    Why this approach: heapq.nlargest scans the input once, keeping a heap
    of size k — O(n log k) time and O(k) space. sorted()[:k] would be
    O(n log n); at n=10^6, k=10 that is ~20M comparisons vs ~1M.
    """
    if k <= 0:
        return []
    return heapq.nlargest(k, scores)


def top_k_stream(
    stream: Iterable[tuple[str, float]],
    k: int,
) -> list[tuple[str, float]]:
    """Return the k highest-scoring (doc_id, score) pairs, descending.

    Why this approach: nlargest with key=score ranks tuples by the score
    field (plain tuple comparison would sort lexicographically by doc_id).
    The stream is consumed once; only the k-element heap is retained, so
    memory stays O(k) regardless of stream length.
    """
    if k <= 0:
        return []
    return heapq.nlargest(k, stream, key=lambda item: item[1])
