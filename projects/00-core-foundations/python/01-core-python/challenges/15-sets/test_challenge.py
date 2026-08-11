"""
Challenge 15: Sets — Tests
===========================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    CHALLENGE_USE_SOLUTION=1 python -m pytest 01-core-python/challenges/15-sets -q

Performance guards count comparisons and use tracemalloc — never wall-clock time.
"""

from __future__ import annotations

import importlib.util
import os
import tracemalloc
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


class CountingStr(str):
    """str subclass that counts every equality comparison it takes part in.

    Hashing is inherited from str, so set membership stays O(1) and costs no
    counted comparison -- a set-based solution registers ~0 while a list- or
    output-scan solution registers one count per element examined.
    """

    _counter: list[int] = [0]

    def __eq__(self, other: object) -> bool:
        CountingStr._counter[0] += 1
        return str.__eq__(self, other)

    def __ne__(self, other: object) -> bool:
        CountingStr._counter[0] += 1
        return str.__ne__(self, other)

    __hash__ = str.__hash__


def _reset_counter() -> list[int]:
    CountingStr._counter[0] = 0
    return CountingStr._counter


def _ids(n: int, distinct: int) -> list[str]:
    """n chunk ids drawn from `distinct` values, non-monotonic and deterministic."""
    return [f"chunk-{(i * 7919) % distinct}" for i in range(n)]


class TestDedupeChunks:
    """Bronze: order-preserving dedup via a seen-set."""

    def test_basic(self) -> None:
        assert mod.dedupe_chunks(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]

    def test_preserves_first_seen_order(self) -> None:
        assert mod.dedupe_chunks(["z", "y", "x", "z"]) == ["z", "y", "x"]

    def test_empty(self) -> None:
        assert mod.dedupe_chunks([]) == []

    def test_single(self) -> None:
        assert mod.dedupe_chunks(["only"]) == ["only"]

    def test_all_duplicates(self) -> None:
        assert mod.dedupe_chunks(["d"] * 6) == ["d"]

    def test_no_duplicates_is_identity(self) -> None:
        assert mod.dedupe_chunks(["a", "b", "c"]) == ["a", "b", "c"]

    def test_does_not_mutate_input(self) -> None:
        original = ["a", "b", "a"]
        mod.dedupe_chunks(original)
        assert original == ["a", "b", "a"]

    def test_rejects_set_shortcut_ordering(self) -> None:
        """list(set(...)) would not reliably produce this exact order."""
        ids = [f"chunk-{i}" for i in (9, 3, 7, 3, 1, 9, 5)]
        assert mod.dedupe_chunks(ids) == ["chunk-9", "chunk-3", "chunk-7", "chunk-1", "chunk-5"]


class TestFilterStopwords:
    """Silver: set membership, comparison budget guard."""

    def test_basic(self) -> None:
        assert mod.filter_stopwords(["the", "cat", "sat"], {"the"}) == ["cat", "sat"]

    def test_empty_tokens(self) -> None:
        assert mod.filter_stopwords([], {"the"}) == []

    def test_empty_stopwords_is_identity(self) -> None:
        assert mod.filter_stopwords(["a", "b"], set()) == ["a", "b"]

    def test_all_filtered(self) -> None:
        assert mod.filter_stopwords(["the", "a"], {"the", "a"}) == []

    def test_keeps_duplicates_of_kept_tokens(self) -> None:
        assert mod.filter_stopwords(["ml", "ml", "the"], {"the"}) == ["ml", "ml"]

    def test_preserves_order(self) -> None:
        tokens = ["rag", "the", "index", "a", "recall"]
        assert mod.filter_stopwords(tokens, {"the", "a"}) == ["rag", "index", "recall"]

    def test_case_sensitive(self) -> None:
        assert mod.filter_stopwords(["The", "the"], {"the"}) == ["The"]

    def test_comparison_budget_guard(self) -> None:
        """Set membership costs ~0 counted comparisons; scanning a 500-item
        stopword collection costs ~n*m. Budget is deliberately loose (2n) so
        only an O(n*m) scan can fail it."""
        counter = _reset_counter()
        n = 10_000
        tokens = [CountingStr(f"tok-{i % 997}") for i in range(n)]
        stopwords = {CountingStr(f"tok-{i}") for i in range(500)}

        result = mod.filter_stopwords(tokens, stopwords)

        assert len(result) < n, "some tokens should have been filtered"
        assert counter[0] <= 2 * n, (
            f"comparisons {counter[0]} exceed budget {2 * n}; membership must be "
            "O(1) set lookup, not a scan over the stopword collection"
        )


class TestNovelChunks:
    """Gold: lazy single-pass novelty filter, memory ceiling guard."""

    def test_basic(self) -> None:
        result = list(mod.novel_chunks(["a", "b", "c"], {"b"}))
        assert result == ["a", "c"]

    def test_dedupes_within_stream(self) -> None:
        assert list(mod.novel_chunks(["a", "a", "b"], set())) == ["a", "b"]

    def test_empty_stream(self) -> None:
        assert list(mod.novel_chunks([], {"a"})) == []

    def test_everything_already_sent(self) -> None:
        assert list(mod.novel_chunks(["a", "b"], {"a", "b"})) == []

    def test_preserves_rank_order(self) -> None:
        retrieved = ["rank1", "rank2", "rank3", "rank4"]
        assert list(mod.novel_chunks(retrieved, {"rank2"})) == ["rank1", "rank3", "rank4"]

    def test_does_not_mutate_caller_set(self) -> None:
        already = {"a"}
        list(mod.novel_chunks(["b", "c"], already))
        assert already == {"a"}, "mutating the caller's context set is a real-world bug"

    def test_is_lazy(self) -> None:
        """Must not consume the iterable before the first next() call."""
        consumed: list[str] = []

        def tracking() -> object:
            for cid in ["a", "b", "c"]:
                consumed.append(cid)
                yield cid

        gen = mod.novel_chunks(tracking(), set())
        assert consumed == [], "generator body must not run before first next()"
        first = next(iter(gen))
        assert first == "a"
        assert len(consumed) == 1, "must pull one item at a time, not drain the stream"

    def test_correctness_against_reference(self) -> None:
        ids = _ids(5_000, distinct=1_200)
        already = {f"chunk-{i}" for i in range(0, 1_200, 3)}
        expected: list[str] = []
        seen = set(already)
        for cid in ids:
            if cid not in seen:
                seen.add(cid)
                expected.append(cid)
        assert list(mod.novel_chunks(ids, already)) == expected

    def test_memory_ceiling_guard(self) -> None:
        """A 400k-id stream with only 500 distinct novel ids must cost memory
        proportional to the novel set, not the stream. Materializing the stream
        (set(retrieved) or list(retrieved)) blows the ceiling."""
        n = 400_000
        distinct = 500
        stream = (f"chunk-{(i * 7919) % distinct}" for i in range(n))

        tracemalloc.start()
        try:
            result = list(mod.novel_chunks(stream, set()))
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()

        assert len(result) == distinct, "each distinct id yielded exactly once"
        assert peak < 2 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 2 MB ceiling; the stream must "
            "be consumed lazily, never materialized"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
