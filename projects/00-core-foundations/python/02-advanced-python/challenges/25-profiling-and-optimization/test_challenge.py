"""
Challenge 25: Profiling and Optimization — Hidden Tests
========================================================
Runs against starter.py by default; set CHALLENGE_MODULE=solution to
verify the reference implementation.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import time
from pathlib import Path

import pytest

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


target = _load(os.environ.get("CHALLENGE_MODULE", "starter"))


class TestDedup:
    def test_basic(self):
        assert target.dedup_chunks(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]

    def test_single(self):
        assert target.dedup_chunks(["x"]) == ["x"]

    def test_empty(self):
        assert target.dedup_chunks([]) == []

    def test_all_duplicates(self):
        assert target.dedup_chunks(["a", "a", "a"]) == ["a"]

    def test_order_preserved_first_occurrence(self):
        assert target.dedup_chunks(["c", "a", "c", "b", "a"]) == ["c", "a", "b"]

    def test_performance_linear(self):
        items = [f"chunk-{i % 1000}" for i in range(100_000)]
        start = time.perf_counter()
        out = target.dedup_chunks(items)
        elapsed = time.perf_counter() - start
        assert len(out) == 1000
        assert elapsed < 2.0, (
            f"dedup took {elapsed:.2f}s: O(n^2) in-list scan, use a set"
        )


class TestHashJoin:
    def test_joins_matching(self):
        records = [{"chunk_id": 1, "op": "add"}]
        index = [{"chunk_id": 1, "text": "A"}]
        assert target.hash_join(records, index) == [(1, "A")]

    def test_skips_missing(self):
        records = [{"chunk_id": 1, "op": "add"}, {"chunk_id": 2, "op": "del"}]
        index = [{"chunk_id": 1, "text": "A"}]
        assert target.hash_join(records, index) == [(1, "A")]

    def test_empty(self):
        assert target.hash_join([], [{"chunk_id": 1, "text": "A"}]) == []
        assert target.hash_join([{"chunk_id": 1, "op": "x"}], []) == []

    def test_duplicates_keep_all_records(self):
        records = [
            {"chunk_id": 1, "op": "a"},
            {"chunk_id": 1, "op": "b"},
        ]
        index = [{"chunk_id": 1, "text": "A"}]
        assert target.hash_join(records, index) == [(1, "A"), (1, "A")]

    def test_performance_dict_join(self):
        n = 25_000
        records = [{"chunk_id": i, "op": "add"} for i in range(n)]
        index = [{"chunk_id": i, "text": f"t{i}"} for i in reversed(range(n))]
        start = time.perf_counter()
        joined = target.hash_join(records, index)
        elapsed = time.perf_counter() - start
        assert len(joined) == n
        assert joined[0] == (0, "t0")
        assert elapsed < 1.0, (
            f"join took {elapsed:.2f}s: nested scan is O(n^2), use a dict"
        )


class TestFibStats:
    def test_zero(self):
        result, calls = target.fib_stats(0)
        assert result == 0 and calls == 1

    def test_one(self):
        result, calls = target.fib_stats(1)
        assert result == 1 and calls == 1

    def test_ten(self):
        result, calls = target.fib_stats(10)
        assert result == 55
        assert calls <= 20, f"{calls} calls: memoization missing"

    def test_twenty_five(self):
        result, calls = target.fib_stats(25)
        assert result == 75025
        assert calls <= 60, (
            f"{calls} calls at n=25: naive fib makes 242,785 — memoize"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
