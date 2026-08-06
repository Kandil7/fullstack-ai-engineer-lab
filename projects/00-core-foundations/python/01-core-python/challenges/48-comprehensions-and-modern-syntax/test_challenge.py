"""
Challenge 48: Comprehensions & Modern Syntax — Tests
======================================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest challenges/48-comprehensions-and-modern-syntax/test_challenge.py -q

Performance guards use operation counting (call/fetch counts), never wall-clock time.
"""

from __future__ import annotations

import importlib.util
import inspect
import os
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(
    TARGET, Path(__file__).parent / f"{TARGET}.py"
)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


def _float_or_none(s: str) -> float | None:
    try:
        return float(s)
    except ValueError:
        return None


def _counting_parser(counter: list[int]) -> "callable":
    def parser(s: str) -> float | None:
        counter.append(1)
        return _float_or_none(s)

    return parser


class CountingIter:
    """Iterable that records how many items were fetched via __next__."""

    def __init__(self, items: list[str]) -> None:
        self.items = items
        self.fetched = 0

    def __iter__(self) -> "CountingIter":
        return self

    def __next__(self) -> str:
        if self.fetched >= len(self.items):
            raise StopIteration
        item = self.items[self.fetched]
        self.fetched += 1
        return item


class TestTokenizeAndFilter:
    """Bronze: comprehension transform + filter."""

    def test_basic(self) -> None:
        assert mod.tokenize_and_filter(["the", "cat", "on", "mat"], 3) == [
            "THE", "CAT", "MAT",
        ]

    def test_min_len_2(self) -> None:
        assert mod.tokenize_and_filter(["a", "ab", "abc"], 2) == ["AB", "ABC"]

    def test_nothing_matches(self) -> None:
        assert mod.tokenize_and_filter(["a", "b"], 5) == []

    def test_empty(self) -> None:
        assert mod.tokenize_and_filter([], 1) == []

    def test_exact_boundary(self) -> None:
        assert mod.tokenize_and_filter(["ok", "no", "i"], 2) == ["OK", "NO"]

    def test_duplicates_kept(self) -> None:
        assert mod.tokenize_and_filter(["a", "a"], 1) == ["A", "A"]


class TestParseFloats:
    """Silver: parse-once semantics with call counting."""

    def test_mixed(self) -> None:
        assert mod.parse_floats(["3.14", "abc", "2.5"], _float_or_none) == [3.14, 2.5]

    def test_all_valid(self) -> None:
        assert mod.parse_floats(["1", "2", "3"], _float_or_none) == [1.0, 2.0, 3.0]

    def test_all_invalid(self) -> None:
        assert mod.parse_floats(["x", "y"], _float_or_none) == []

    def test_empty(self) -> None:
        assert mod.parse_floats([], _float_or_none) == []

    def test_negative_and_zero(self) -> None:
        assert mod.parse_floats(["-1.5", "0"], _float_or_none) == [-1.5, 0.0]

    def test_duplicates_kept(self) -> None:
        assert mod.parse_floats(["1.0", "1.0"], _float_or_none) == [1.0, 1.0]

    def test_parse_once_guard(self) -> None:
        """Operation-counting guard: exactly one parser call per value."""
        counter: list[int] = []
        values = ["1", "x", "2.5", "y", "3", "z"]
        result = mod.parse_floats(values, _counting_parser(counter))
        assert result == [1.0, 2.5, 3.0]
        assert len(counter) == len(values), (
            "parser must run exactly once per value; a double-parse calls it 2n times"
        )


class TestDedupeStream:
    """Gold: lazy generator, single pass, first-seen order."""

    def test_basic_dedupe(self) -> None:
        assert list(mod.dedupe_stream(["a", "b", "a", "c", "b"])) == ["a", "b", "c"]

    def test_all_duplicates(self) -> None:
        assert list(mod.dedupe_stream(["x", "x", "x"])) == ["x"]

    def test_empty(self) -> None:
        assert list(mod.dedupe_stream([])) == []

    def test_single(self) -> None:
        assert list(mod.dedupe_stream(["a"])) == ["a"]

    def test_all_unique(self) -> None:
        assert list(mod.dedupe_stream(["a", "b", "c"])) == ["a", "b", "c"]

    def test_is_generator(self) -> None:
        assert inspect.isgenerator(mod.dedupe_stream(["a"])), "must return a generator"

    def test_laziness_guard(self) -> None:
        """Producing the FIRST output must not consume the whole input."""
        it = CountingIter(["a", "b", "a", "c"])
        gen = mod.dedupe_stream(it)
        first = next(gen)
        assert first == "a"
        assert it.fetched <= 2, (
            "first output must require only a bounded prefix (lazy); "
            "materializing the input consumes everything"
        )

    def test_single_pass_guard(self) -> None:
        """Operation-counting guard: every input row fetched exactly once."""
        rows = [f"row-{i % 7}" for i in range(500)]
        it = CountingIter(rows)
        result = list(mod.dedupe_stream(it))
        assert result == ["row-0", "row-1", "row-2", "row-3", "row-4", "row-5", "row-6"]
        assert it.fetched == len(rows), "full consumption must fetch each row once"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
