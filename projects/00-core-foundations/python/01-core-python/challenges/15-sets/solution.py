"""
Challenge 15: Sets — Reference Solution
========================================
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator


def dedupe_chunks(chunk_ids: list[str]) -> list[str]:
    """Return chunk_ids with duplicates removed, preserving first-seen order.

    Why this approach: a `seen` set gives O(1) membership, so the whole pass is
    O(n). The obvious alternative, `if cid not in result` against the output
    list, is O(n) per check and O(n^2) overall -- at n=20k that is ~200M
    comparisons instead of 20k. `list(set(ids))` is O(n) but loses order, and
    retrieval order is rank order, so it is wrong here regardless of speed.
    """
    seen: set[str] = set()
    result: list[str] = []
    for cid in chunk_ids:
        if cid not in seen:
            seen.add(cid)
            result.append(cid)
    return result


def filter_stopwords(tokens: list[str], stopwords: set[str]) -> list[str]:
    """Return tokens with every stopword removed, preserving order.

    Why this approach: `in` on a set hashes once -- O(1) per token, O(n) total.
    The same code against a *list* of stopwords scans it every time: O(n*m).
    With 10k tokens and a 500-word stopword list that is 5M comparisons versus
    10k. Same source line, 500x the work; the container type is the decision.
    """
    return [tok for tok in tokens if tok not in stopwords]


def novel_chunks(
    retrieved: Iterable[str],
    already_sent: set[str],
) -> Iterator[str]:
    """Yield chunk ids from `retrieved` not in `already_sent`, first-seen only.

    Why this approach: a generator holds only the local `seen` set, so a
    100M-id retrieval stream costs memory proportional to the number of
    *novel* ids rather than the stream length -- `set(retrieved) - already_sent`
    would materialize the entire stream and also destroy rank order.
    `already_sent` is copied into a local `seen` so the caller's set is never
    mutated; mutating a caller's context set is how a dedup bug turns into a
    silently-shrinking context window across turns.
    """
    seen = set(already_sent)
    for cid in retrieved:
        if cid not in seen:
            seen.add(cid)
            yield cid
