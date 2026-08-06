"""
Challenge 49: Collections Toolkit — Tests
==========================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest challenges/49-collections-toolkit/test_challenge.py -q

Performance guards use comparison counting and tracemalloc — never wall-clock time.
"""

from __future__ import annotations

import heapq
import importlib.util
import os
import random
import tracemalloc
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(
    TARGET, Path(__file__).parent / f"{TARGET}.py"
)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


class CountingFloat:
    """Float wrapper that counts every __lt__/__gt__ comparison."""

    __slots__ = ("val", "counter")

    def __init__(self, val: float, counter: list[int]) -> None:
        self.val = val
        self.counter = counter

    def __lt__(self, other: "CountingFloat") -> bool:
        self.counter[0] += 1
        return self.val < other.val

    def __gt__(self, other: "CountingFloat") -> bool:
        self.counter[0] += 1
        return self.val > other.val

    def __repr__(self) -> str:
        return f"CF({self.val})"


def _distinct_scores(n: int, modulus: int = 10**6) -> list[float]:
    """n pairwise-distinct scores in [0, 1): i*7919 mod 10^6 (7919 coprime)."""
    return [((i * 7919) % modulus) / modulus for i in range(n)]


class TestTopKTokens:
    """Bronze: Counter + deterministic tie-break."""

    def test_basic(self) -> None:
        assert mod.top_k_tokens(["a", "b", "a", "c", "a", "b"], 2) == [("a", 3), ("b", 2)]

    def test_k_one(self) -> None:
        assert mod.top_k_tokens(["x", "y"], 1) == [("x", 1)]

    def test_alphabetical_tie_break(self) -> None:
        assert mod.top_k_tokens(["b", "a", "b", "a"], 2) == [("a", 2), ("b", 2)]

    def test_empty(self) -> None:
        assert mod.top_k_tokens([], 3) == []

    def test_k_zero(self) -> None:
        assert mod.top_k_tokens(["a", "b"], 0) == []

    def test_k_gt_unique(self) -> None:
        result = mod.top_k_tokens(["b", "a", "c"], 10)
        assert result == [("a", 1), ("b", 1), ("c", 1)]

    def test_duplicates_count(self) -> None:
        assert mod.top_k_tokens(["q"] * 5 + ["r"], 2) == [("q", 5), ("r", 1)]


class TestTopKScores:
    """Silver: heap-based top-k, comparison budget guard."""

    def test_basic(self) -> None:
        assert mod.top_k_scores([0.1, 0.9, 0.4, 0.8], 2) == [0.9, 0.8]

    def test_single(self) -> None:
        assert mod.top_k_scores([5.0], 1) == [5.0]

    def test_k_gt_n(self) -> None:
        assert mod.top_k_scores([1.0, 2.0], 5) == [2.0, 1.0]

    def test_empty(self) -> None:
        assert mod.top_k_scores([], 3) == []

    def test_k_zero(self) -> None:
        assert mod.top_k_scores([1.0, 2.0], 0) == []

    def test_duplicates(self) -> None:
        assert mod.top_k_scores([3.0, 3.0, 1.0], 2) == [3.0, 3.0]

    def test_negatives(self) -> None:
        assert mod.top_k_scores([-1.0, -5.0, -2.0], 2) == [-1.0, -2.0]

    def test_correctness_on_seeded_random(self) -> None:
        rng = random.Random(42)
        data = [rng.random() for _ in range(2_000)]
        expected = sorted(data, reverse=True)[:10]
        assert mod.top_k_scores(data, 10) == expected

    def test_comparison_budget_guard_random(self) -> None:
        """Operation-counting guard: n log k budget, not n log n."""
        rng = random.Random(7)
        counter: list[int] = [0]
        n = 100_000
        data = [CountingFloat(rng.random(), counter) for _ in range(n)]
        result = mod.top_k_scores(data, 10)
        assert len(result) == 10
        assert counter[0] <= 10 * n, (
            f"comparisons {counter[0]} exceed budget {10 * n}; "
            "sorted()[:k] is O(n log n) and must fail this guard"
        )

    def test_comparison_budget_guard_adversarial(self) -> None:
        """Descending input forces a replacement on every element — the
        heap's worst case — and must still stay under the budget."""
        counter: list[int] = [0]
        n = 100_000
        data = [CountingFloat((n - i) / n, counter) for i in range(n)]
        result = mod.top_k_scores(data, 10)
        assert len(result) == 10
        assert counter[0] <= 10 * n, "heap worst case must stay under 10n comparisons"


class TestTopKStream:
    """Gold: streaming top-k, memory ceiling guard."""

    def test_basic(self) -> None:
        stream = [("a", 0.1), ("b", 0.9), ("c", 0.5)]
        assert mod.top_k_stream(stream, 2) == [("b", 0.9), ("c", 0.5)]

    def test_ties_any_order(self) -> None:
        stream = [("a", 0.7), ("b", 0.7)]
        result = mod.top_k_stream(stream, 2)
        assert sorted(result) == sorted([("a", 0.7), ("b", 0.7)])

    def test_empty(self) -> None:
        assert mod.top_k_stream([], 5) == []

    def test_k_zero(self) -> None:
        assert mod.top_k_stream([("a", 1.0)], 0) == []

    def test_k_gt_n(self) -> None:
        result = mod.top_k_stream([("a", 0.2), ("b", 0.9)], 5)
        assert result == [("b", 0.9), ("a", 0.2)]

    def test_duplicate_scores_distinct_ids(self) -> None:
        stream = [("a", 0.5), ("b", 0.5), ("c", 0.9)]
        result = mod.top_k_stream(stream, 2)
        assert result[0] == ("c", 0.9)
        assert len(result) == 2

    def test_correctness_on_distinct_scores(self) -> None:
        n = 20_000
        pairs = [(f"doc-{i}", s) for i, s in enumerate(_distinct_scores(n))]
        expected = sorted(pairs, key=lambda t: t[1], reverse=True)[:10]
        assert mod.top_k_stream(pairs, 10) == expected

    def test_memory_ceiling_guard(self) -> None:
        """tracemalloc guard: 10^6-item stream must not be materialized.
        Materializing ~140 MB of tuples blows the 30 MB ceiling; a heap of
        size k stays under 1 MB."""
        n = 10**6
        pairs = [(f"doc-{i}", ((i * 7919) % 10**6) / 10**6) for i in range(n)]
        expected_top = heapq.nlargest(10, pairs, key=lambda t: t[1])

        tracemalloc.start()
        try:
            result = mod.top_k_stream((p for p in pairs), 10)
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

        assert len(result) == 10
        assert result == expected_top, "must return exactly the top-k by score"
        assert peak < 30 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 30 MB ceiling; "
            "the stream must not be materialized (heap of size k only)"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
