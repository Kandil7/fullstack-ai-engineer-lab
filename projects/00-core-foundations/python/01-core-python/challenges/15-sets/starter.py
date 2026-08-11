"""
Challenge 15: Sets — Starter Code
==================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator


def dedupe_chunks(chunk_ids: list[str]) -> list[str]:
    """Return chunk_ids with duplicates removed, preserving first-seen order."""
    raise NotImplementedError


def filter_stopwords(tokens: list[str], stopwords: set[str]) -> list[str]:
    """Return tokens with every stopword removed, preserving order.

    Membership must be O(1) per token, not O(len(stopwords)).
    """
    raise NotImplementedError


def novel_chunks(
    retrieved: Iterable[str],
    already_sent: set[str],
) -> Iterator[str]:
    """Yield chunk ids from `retrieved` not in `already_sent`, first-seen only.

    Lazy and single-pass: never materialize `retrieved`. Must not mutate
    `already_sent`.
    """
    raise NotImplementedError
