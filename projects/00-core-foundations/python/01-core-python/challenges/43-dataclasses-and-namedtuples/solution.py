"""Challenge 43 solution — reference implementation with reasoning comments."""
from __future__ import annotations

import heapq
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __post_init__(self) -> None:
        # Reject NaN and +/-inf — coordinates must be finite.
        if not math.isfinite(self.x) or not math.isfinite(self.y):
            raise ValueError(f"Point coordinates must be finite: {(self.x, self.y)}")


@dataclass(order=True)
class Hit:
    # Ordering walks fields left to right: score first, then doc.
    score: float
    doc: str


def rank_hits(hits: list[tuple[str, float]]) -> list[str]:
    """Rank (doc, score) pairs: score descending, ties by doc ascending.

    The dataclass orders by (score, doc) ascending; we negate the score so
    higher scores sort first, and doc ties then resolve ascending.
    """
    return [h.doc for h in sorted(Hit(-score, doc) for doc, score in hits)]


@dataclass(frozen=True, slots=True)
class Embedding:
    id: str
    vector: tuple[float, ...]

    def __post_init__(self) -> None:
        # frozen + slots: validated by RecordStore before construction
        pass


class RecordStore:
    def __init__(self, dim: int) -> None:
        if dim < 1:
            raise ValueError("dim must be >= 1")
        self.dim = dim
        self._records: list[Embedding] = []

    def add(self, id: str, vector: tuple[float, ...]) -> None:
        if len(vector) != self.dim:
            raise ValueError(f"expected dim {self.dim}, got {len(vector)}")
        if not all(math.isfinite(v) for v in vector):
            raise ValueError("vector must be finite")
        self._records.append(Embedding(id, vector))

    def top_k(self, k: int) -> list[Embedding]:
        """Return the k embeddings with the largest mean vector value."""
        if k <= 0:
            return []
        # nlargest is O(n log k); sorted()[:k] would be O(n log n).
        return heapq.nlargest(
            k, self._records, key=lambda e: sum(e.vector) / len(e.vector)
        )
