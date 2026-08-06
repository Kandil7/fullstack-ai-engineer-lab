"""Challenge 43 starter — fill in the bodies (never return working code)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __post_init__(self) -> None:
        raise NotImplementedError


@dataclass(order=True)
class Hit:
    score: float
    doc: str


def rank_hits(hits: list[tuple[str, float]]) -> list[str]:
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Embedding:
    id: str
    vector: tuple[float, ...]

    def __post_init__(self) -> None:
        raise NotImplementedError


class RecordStore:
    def __init__(self, dim: int) -> None:
        raise NotImplementedError

    def add(self, id: str, vector: tuple[float, ...]) -> None:
        raise NotImplementedError

    def top_k(self, k: int) -> list[Embedding]:
        raise NotImplementedError
