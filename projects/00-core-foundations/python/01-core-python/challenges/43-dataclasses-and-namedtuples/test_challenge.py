"""
Challenge 43: Dataclasses & NamedTuples — Hidden Tests
======================================================
Imports the reference solution (solution.py) and verifies correctness,
edge cases, and performance constraints.
"""

from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent

def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # required: dataclasses/etc. look up __module__
    spec.loader.exec_module(mod)
    return mod

solution = _load("solution")
import pytest


class TestPoint:
    def test_constructs(self):
        p = solution.Point(1.0, 2.0)
        assert p.x == 1.0 and p.y == 2.0

    def test_rejects_nan(self):
        with pytest.raises(ValueError):
            solution.Point(float("nan"), 0.0)

    def test_rejects_inf(self):
        with pytest.raises(ValueError):
            solution.Point(1.0, float("inf"))

    def test_frozen(self):
        with pytest.raises(Exception) as ei:
            solution.Point(1, 2).x = 5
        assert type(ei.value).__name__ == "FrozenInstanceError"

    def test_equality(self):
        assert solution.Point(1, 2) == solution.Point(1, 2)


class TestRankHits:
    def test_basic_order(self):
        assert solution.rank_hits([("b", 0.5), ("a", 0.9), ("c", 0.5)]) == ["a", "b", "c"]

    def test_ties_break_alpha(self):
        assert solution.rank_hits([("x", 0.1), ("a", 0.1)]) == ["a", "x"]

    def test_empty(self):
        assert solution.rank_hits([]) == []

    def test_single(self):
        assert solution.rank_hits([("only", 1.0)]) == ["only"]

    def test_negative_scores(self):
        assert solution.rank_hits([("b", -1.0), ("a", -0.1)]) == ["a", "b"]

    def test_performance(self):
        n = 100_000
        hits = [(f"doc{i}", float(i % 100)) for i in range(n)]
        start = time.perf_counter()
        out = solution.rank_hits(hits)
        elapsed = time.perf_counter() - start
        assert len(out) == n
        # highest score is 99.0; the tie-break picks the lexicographically
        # smallest doc id among that group
        expected_first = min(f"doc{i}" for i in range(n) if i % 100 == 99)
        assert out[0] == expected_first, "highest score with tie-break first"
        assert elapsed < 5.0, f"rank_hits too slow: {elapsed:.2f}s"


class TestRecordStore:
    def test_add_and_dim_check(self):
        store = solution.RecordStore(3)
        store.add("a", (1.0, 2.0, 3.0))
        with pytest.raises(ValueError):
            store.add("b", (1.0, 2.0))          # wrong dim
        with pytest.raises(ValueError):
            store.add("c", (1.0, float("nan"), 3.0))

    def test_top_k_ordering(self):
        store = solution.RecordStore(2)
        store.add("low", (0.0, 0.0))
        store.add("high", (1.0, 1.0))
        store.add("mid", (0.5, 0.5))
        assert [e.id for e in store.top_k(2)] == ["high", "mid"]

    def test_top_k_zero_and_overflow(self):
        store = solution.RecordStore(1)
        store.add("a", (1.0,))
        assert store.top_k(0) == []
        assert store.top_k(10)[0].id == "a"      # k > n is safe

    def test_empty_store(self):
        assert solution.RecordStore(1).top_k(1) == []

    def test_slots_used(self):
        # dataclass(slots=True) produces a real __slots__ tuple
        assert hasattr(solution.Embedding, "__slots__")
        assert set(solution.Embedding.__slots__) == {"id", "vector"}
        # and no per-instance __dict__
        e = solution.Embedding("x", (1.0,))
        assert not hasattr(e, "__dict__"), "slots instances must not carry a dict"

    def test_performance(self):
        store = solution.RecordStore(4)
        start = time.perf_counter()
        for i in range(50_000):
            store.add(f"id{i}", (float(i), 0.0, 1.0, 2.0))
        assert len(store.top_k(5)) == 5
        elapsed = time.perf_counter() - start
        assert elapsed < 10.0, f"RecordStore too slow: {elapsed:.2f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
