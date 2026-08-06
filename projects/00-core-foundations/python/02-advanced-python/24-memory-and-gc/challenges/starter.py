"""Challenge 24: Memory Management and GC — starter (signatures only)."""

from __future__ import annotations


class Node:
    def __init__(self, name: str = "") -> None:
        self.name = name
        self.peer: Node | None = None


class PlainEntry:
    def __init__(self, text: str, chunk_id: int) -> None:
        self.text = text
        self.chunk_id = chunk_id


class SlottedEntry:
    __slots__ = ("text", "chunk_id")

    def __init__(self, text: str, chunk_id: int) -> None:
        self.text = text
        self.chunk_id = chunk_id


class Entry:
    def __init__(self, text: str) -> None:
        self.text = text


def collect_cycle(n: int) -> int:
    """Build an n-node cycle, del the roots, collect; return freed count."""
    raise NotImplementedError


def slots_ratio(n: int) -> float:
    """Return plain_total / slotted_total at n instances, __dict__ included."""
    raise NotImplementedError


def weak_cache_trap() -> tuple[int, int, int]:
    """Return (trap_len, alive_len, after_del_len) for a WeakValueDictionary."""
    raise NotImplementedError


def sum_materialized(n: int) -> tuple[int, int]:
    """Return (total, tracemalloc peak) building [i for i in range(n)]."""
    raise NotImplementedError


def sum_streamed(n: int) -> tuple[int, int]:
    """Return (total, tracemalloc peak) summing range(n) directly."""
    raise NotImplementedError
