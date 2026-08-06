"""Challenge 24: Memory Management and GC — reference solution.

Why these approaches:
- Bronze: refcounts cannot see cycles; gc.collect() frees exactly the
  n nodes, which is the observable contract.
- Silver: sys.getsizeof(instance) is 48 B for both classes on 3.13 —
  the per-instance __dict__ is the real cost, so honest sizing adds it.
- Gold: weak caches evict temporaries instantly (trap), and
  tracemalloc makes the materialize-vs-stream difference undeniable.
"""

from __future__ import annotations

import gc
import sys
import tracemalloc
import weakref


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


def _count_nodes() -> int:
    return sum(1 for o in gc.get_objects() if isinstance(o, Node))


def collect_cycle(n: int) -> int:
    """Wire n Nodes into a cycle, drop the roots, force a collection.

    NOTE: iterate by index — a `for node in nodes` loop variable would
    keep the last node alive and make the whole cycle reachable.
    """
    nodes = [Node(str(i)) for i in range(n)]
    for i in range(n):
        nodes[i].peer = nodes[(i + 1) % n]
    before = _count_nodes()
    del nodes
    gc.collect()
    after = _count_nodes()
    return before - after


def _total_bytes(records: list) -> int:
    """Honest sizing: include __dict__ on 3.13, where getsizeof(instance)
    is 48 bytes for both plain and slotted classes."""
    size = 0
    for inst in records:
        size += sys.getsizeof(inst)
        if hasattr(inst, "__dict__"):
            size += sys.getsizeof(inst.__dict__)
    return size


def slots_ratio(n: int) -> float:
    plain = [PlainEntry("text", i) for i in range(n)]
    slotted = [SlottedEntry("text", i) for i in range(n)]
    return _total_bytes(plain) / _total_bytes(slotted)


def weak_cache_trap() -> tuple[int, int, int]:
    """Trap: a temporary value dies at line end; an owned value lives;
    deleting the owner evicts the entry."""
    cache: weakref.WeakValueDictionary[int, Entry] = weakref.WeakValueDictionary()

    cache[1] = Entry("temp")            # temporary: evicted instantly
    trap_len = len(cache)

    e = Entry("owned")                  # strong owner elsewhere
    cache[2] = e
    alive_len = len(cache)

    del e
    after_del_len = len(cache)
    return trap_len, alive_len, after_del_len


def sum_materialized(n: int) -> tuple[int, int]:
    """Materialize a list of n ints, sum it; report (total, peak)."""
    tracemalloc.start()
    total = sum([i for i in range(n)])
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return total, peak


def sum_streamed(n: int) -> tuple[int, int]:
    """Sum range(n) directly; report (total, peak)."""
    tracemalloc.start()
    total = sum(i for i in range(n))
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return total, peak
