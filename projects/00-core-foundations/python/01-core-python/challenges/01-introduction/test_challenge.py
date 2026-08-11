"""
Challenge 01: Introduction -- Tests
===================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    CHALLENGE_USE_SOLUTION=1 python -m pytest 01-core-python/challenges/01-introduction -q

Guards count remote lookups and use tracemalloc -- never wall-clock time.
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

SUPPORTED_MIN = (3, 10, 0)


class SupportMatrix:
    """Spy for the remote support-matrix lookup; records every call."""

    def __init__(self, minimum: tuple[int, int, int] = SUPPORTED_MIN) -> None:
        self.minimum = minimum
        self.calls: list[tuple[int, int, int]] = []

    def __call__(self, version: tuple[int, int, int]) -> bool:
        self.calls.append(version)
        return version >= self.minimum


def _banners(n: int, distinct: int) -> list[str]:
    """n deterministic banners drawn from `distinct` interpreter versions."""
    return [f"Python 3.{(i * 7919) % distinct}.2" for i in range(n)]


class TestParseVersion:
    """Bronze: banner -> (major, minor, micro)."""

    def test_full_banner(self) -> None:
        assert mod.parse_version("Python 3.11.4") == (3, 11, 4)

    def test_bare_numbers(self) -> None:
        assert mod.parse_version("3.11.4") == (3, 11, 4)

    def test_missing_micro_defaults_to_zero(self) -> None:
        assert mod.parse_version("Python 3.11") == (3, 11, 0)

    def test_major_only(self) -> None:
        assert mod.parse_version("3") == (3, 0, 0)

    def test_case_insensitive_prefix_and_whitespace(self) -> None:
        assert mod.parse_version("  PYTHON  3.12.1 ") == (3, 12, 1)

    def test_zero_components(self) -> None:
        assert mod.parse_version("Python 0.0.0") == (0, 0, 0)

    def test_double_digit_components(self) -> None:
        assert mod.parse_version("Python 3.14.10") == (3, 14, 10)

    def test_prerelease_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.parse_version("Python 3.13.0rc1")

    def test_empty_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.parse_version("")

    def test_prefix_only_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.parse_version("Python")

    def test_four_components_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.parse_version("3.11.4.1")

    def test_negative_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.parse_version("-3.11.4")

    def test_non_ascii_digits_rejected(self) -> None:
        """int() accepts Arabic-Indic digits; a version parser must not.

        "\\u0661\\u0661" is ARABIC-INDIC DIGIT ONE twice: str.isdigit() says
        True and int() returns 11, so a bare int() parser silently accepts a
        banner no interpreter ever printed.
        """
        with pytest.raises(ValueError):
            mod.parse_version("3.١١.4")

    def test_ordering_is_numeric_not_lexicographic(self) -> None:
        assert mod.parse_version("3.9.0") < mod.parse_version("3.10.0")


class TestUnsupportedNodes:
    """Silver: memoized support lookup, call-count guard."""

    def test_basic(self) -> None:
        matrix = SupportMatrix()
        nodes = [("n1", "Python 3.11.4"), ("n2", "Python 3.8.10")]
        assert mod.unsupported_nodes(nodes, matrix) == ["n2"]

    def test_empty(self) -> None:
        matrix = SupportMatrix()
        assert mod.unsupported_nodes([], matrix) == []
        assert matrix.calls == []

    def test_single_supported(self) -> None:
        assert mod.unsupported_nodes([("n1", "3.12.0")], SupportMatrix()) == []

    def test_all_unsupported_preserves_order(self) -> None:
        matrix = SupportMatrix()
        nodes = [("c", "3.7.0"), ("a", "3.8.0"), ("b", "3.9.9")]
        assert mod.unsupported_nodes(nodes, matrix) == ["c", "a", "b"]

    def test_malformed_counts_as_unsupported(self) -> None:
        matrix = SupportMatrix()
        nodes = [("n1", "Python 3.13.0rc1"), ("n2", "3.12.0")]
        assert mod.unsupported_nodes(nodes, matrix) == ["n1"]

    def test_malformed_never_reaches_the_matrix(self) -> None:
        matrix = SupportMatrix()
        mod.unsupported_nodes([("n1", "not-a-version")], matrix)
        assert matrix.calls == [], "a banner that does not parse must not cost a lookup"

    def test_duplicate_ids_all_reported(self) -> None:
        matrix = SupportMatrix()
        nodes = [("n1", "3.8.0"), ("n1", "3.8.0")]
        assert mod.unsupported_nodes(nodes, matrix) == ["n1", "n1"]

    def test_boundary_version_is_supported(self) -> None:
        matrix = SupportMatrix(minimum=(3, 10, 0))
        assert mod.unsupported_nodes([("n1", "3.10.0")], matrix) == []

    def test_does_not_mutate_input(self) -> None:
        nodes = [("n1", "3.8.0"), ("n2", "3.12.0")]
        original = list(nodes)
        mod.unsupported_nodes(nodes, SupportMatrix())
        assert nodes == original

    def test_lookup_budget_guard(self) -> None:
        """The support matrix is a remote call: one lookup per DISTINCT version.

        20k nodes running 12 builds must cost 12 lookups. Calling it per node
        costs 20000 -- 1666x over budget.
        """
        matrix = SupportMatrix(minimum=(3, 10, 0))
        distinct = 12
        n = 20_000
        nodes = [(f"node-{i}", b) for i, b in enumerate(_banners(n, distinct))]

        result = mod.unsupported_nodes(nodes, matrix)

        assert len(result) > 0, "some nodes should be unsupported"
        assert len(matrix.calls) <= distinct, (
            f"{len(matrix.calls)} support lookups for {distinct} distinct versions; "
            "memoize on the parsed version instead of calling once per node"
        )

    def test_lookup_budget_all_distinct_adversarial(self) -> None:
        """Worst case for the cache: every node a different version. The cache
        must not make things worse -- still exactly one lookup per version."""
        matrix = SupportMatrix(minimum=(3, 10, 0))
        n = 2_000
        nodes = [(f"node-{i}", f"3.{i}.0") for i in range(n)]

        mod.unsupported_nodes(nodes, matrix)

        assert len(matrix.calls) <= n, "never more than one lookup per distinct version"
        assert len(set(matrix.calls)) == len(matrix.calls), "no version looked up twice"


class TestFleetReport:
    """Gold: single-pass inventory, memory ceiling + one-shot iterator guards."""

    def test_basic(self) -> None:
        report = mod.fleet_report(["Python 3.11.4", "Python 3.11.4", "Python 3.9.1"])
        assert report["total"] == 3
        assert report["malformed"] == 0
        assert report["counts"] == {(3, 11, 4): 2, (3, 9, 1): 1}
        assert report["minimum"] == (3, 9, 1)

    def test_empty(self) -> None:
        report = mod.fleet_report([])
        assert report == {"total": 0, "malformed": 0, "counts": {}, "minimum": None}

    def test_all_malformed(self) -> None:
        report = mod.fleet_report(["", "nope", "3.13.0rc1"])
        assert report["total"] == 3
        assert report["malformed"] == 3
        assert report["counts"] == {}
        assert report["minimum"] is None

    def test_single(self) -> None:
        report = mod.fleet_report(["3.12"])
        assert report["counts"] == {(3, 12, 0): 1}
        assert report["minimum"] == (3, 12, 0)

    def test_minimum_is_numeric_not_lexicographic(self) -> None:
        """'3.10' < '3.9' as strings; as versions the minimum is 3.9.0."""
        report = mod.fleet_report(["3.10.0", "3.9.0", "3.11.0"])
        assert report["minimum"] == (3, 9, 0)

    def test_mixed_malformed_and_valid(self) -> None:
        report = mod.fleet_report(["3.11.0", "garbage", "Python 3.11.0", "3.13.0b2"])
        assert report["total"] == 4
        assert report["malformed"] == 2
        assert report["counts"] == {(3, 11, 0): 2}

    def test_consumes_one_shot_iterator_exactly_once(self) -> None:
        """A generator can only be walked once. Any solution that stores the
        lines and re-iterates sees an empty sequence on pass two."""
        pulls = [0]

        def source():
            for banner in ["3.11.0", "3.9.0", "bad", "3.12.1"]:
                pulls[0] += 1
                yield banner

        report = mod.fleet_report(source())
        assert pulls[0] == 4, "every line must be pulled exactly once"
        assert report["total"] == 4
        assert report["malformed"] == 1
        assert report["minimum"] == (3, 9, 0)

    def test_correctness_against_reference(self) -> None:
        banners = _banners(5_000, distinct=40)
        report = mod.fleet_report(banners)
        expected: dict[tuple[int, int, int], int] = {}
        for b in banners:
            version = (3, int(b.split(".")[1]), 2)
            expected[version] = expected.get(version, 0) + 1
        assert report["counts"] == expected
        assert report["total"] == 5_000
        assert report["malformed"] == 0
        assert report["minimum"] == min(expected)

    def test_memory_ceiling_guard(self) -> None:
        """400k banners over 40 distinct versions must cost memory proportional
        to the version table, not the log. list(banners) is ~26 MB."""
        n = 400_000
        distinct = 40
        stream = (f"Python 3.{(i * 7919) % distinct}.2" for i in range(n))

        tracemalloc.start()
        try:
            report = mod.fleet_report(stream)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()

        assert report["total"] == n
        assert len(report["counts"]) == distinct
        assert peak < 2 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 2 MB ceiling; the log must be "
            "consumed lazily in one pass, never materialized"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
