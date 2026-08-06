"""
Challenge 44: Pandas Pitfalls — Tests
======================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest challenges/44-pandas-pitfalls/test_challenge.py -q
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(
    TARGET, Path(__file__).parent / f"{TARGET}.py"
)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import numpy as np
import pandas as pd
import pytest  # noqa: E402


class TestFilterBelow:
    """Bronze: NaN-aware filtering with explicit kept/dropped split."""

    def test_known_split(self) -> None:
        df = pd.DataFrame({"x": [1.0, np.nan, 5.0]})
        kept, dropped = mod.filter_below(df, "x", 4.0)
        assert len(kept) == 1 and kept.iloc[0]["x"] == 1.0
        assert len(dropped) == 2
        assert np.isnan(dropped.iloc[0]["x"]) and dropped.iloc[1]["x"] == 5.0

    def test_all_nan(self) -> None:
        df = pd.DataFrame({"x": [np.nan, np.nan]})
        kept, dropped = mod.filter_below(df, "x", 10.0)
        assert len(kept) == 0 and len(dropped) == 2

    def test_no_nan(self) -> None:
        df = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
        kept, dropped = mod.filter_below(df, "x", 2.5)
        assert len(kept) == 2 and len(dropped) == 1

    def test_partition_union(self) -> None:
        df = pd.DataFrame({"x": [1.0, np.nan, 5.0, 2.0, np.nan]})
        kept, dropped = mod.filter_below(df, "x", 3.0)
        assert len(kept) + len(dropped) == len(df)
        assert set(kept.index).isdisjoint(set(dropped.index))

    def test_kept_rows_are_past(self) -> None:
        df = pd.DataFrame({"x": [1.0, np.nan, 5.0]})
        kept, _ = mod.filter_below(df, "x", 4.0)
        assert kept["x"].tolist() == [1.0]

    def test_empty(self) -> None:
        df = pd.DataFrame({"x": pd.Series(dtype="float64")})
        kept, dropped = mod.filter_below(df, "x", 1.0)
        assert len(kept) == 0 and len(dropped) == 0


class TestMergeCheckDuplicates:
    """Silver: duplicate-key merges must raise before multiplying rows."""

    def test_normal_merge(self) -> None:
        left = pd.DataFrame({"key": ["a", "b"], "l": [1, 2]})
        right = pd.DataFrame({"key": ["a", "b"], "r": [10, 20]})
        result = mod.merge_check_duplicates(left, right, "key")
        assert len(result) == 2
        assert sorted(result["key"].tolist()) == ["a", "b"]

    def test_duplicate_in_left_raises(self) -> None:
        left = pd.DataFrame({"key": ["a", "a"], "l": [1, 2]})
        right = pd.DataFrame({"key": ["a", "b"], "r": [10, 20]})
        with pytest.raises(ValueError):
            mod.merge_check_duplicates(left, right, "key")

    def test_duplicate_in_right_raises(self) -> None:
        left = pd.DataFrame({"key": ["a", "b"], "l": [1, 2]})
        right = pd.DataFrame({"key": ["a", "a"], "r": [10, 20]})
        with pytest.raises(ValueError):
            mod.merge_check_duplicates(left, right, "key")

    def test_both_duplicate_raises(self) -> None:
        left = pd.DataFrame({"key": ["a", "a"], "l": [1, 2]})
        right = pd.DataFrame({"key": ["a", "a"], "r": [10, 20]})
        with pytest.raises(ValueError):
            mod.merge_check_duplicates(left, right, "key")

    def test_disjoint_keys_inner_semantics(self) -> None:
        left = pd.DataFrame({"key": ["a", "b"], "l": [1, 2]})
        right = pd.DataFrame({"key": ["b", "c"], "r": [10, 20]})
        result = mod.merge_check_duplicates(left, right, "key")
        assert result["key"].tolist() == ["b"]

    def test_does_not_mutate_inputs(self) -> None:
        left = pd.DataFrame({"key": ["a", "b"], "l": [1, 2]})
        right = pd.DataFrame({"key": ["a", "b"], "r": [10, 20]})
        mod.merge_check_duplicates(left, right, "key")
        assert left.shape == (2, 2) and right.shape == (2, 2)


class TestCountNanMismatches:
    """Gold part 1: XOR of NaN masks."""

    def test_known_mismatch(self) -> None:
        a = pd.Series([1.0, np.nan, np.nan])
        b = pd.Series([1.0, 2.0, np.nan])
        assert mod.count_nan_mismatches(a, b) == 1

    def test_identical_patterns_zero(self) -> None:
        a = pd.Series([1.0, np.nan, 3.0])
        b = pd.Series([9.0, np.nan, 7.0])
        assert mod.count_nan_mismatches(a, b) == 0

    def test_all_mismatched(self) -> None:
        a = pd.Series([1.0, 2.0])
        b = pd.Series([np.nan, np.nan])
        assert mod.count_nan_mismatches(a, b) == 2

    def test_reversed_mismatch_counts_same(self) -> None:
        a = pd.Series([1.0, np.nan, 2.0])
        b = pd.Series([np.nan, np.nan, 1.0])
        assert mod.count_nan_mismatches(a, b) == \
            mod.count_nan_mismatches(b, a) == 1

    def test_empty(self) -> None:
        a = pd.Series(dtype="float64")
        b = pd.Series(dtype="float64")
        assert mod.count_nan_mismatches(a, b) == 0

    def test_returns_int(self) -> None:
        a = pd.Series([1.0, np.nan])
        b = pd.Series([np.nan, 2.0])
        assert isinstance(mod.count_nan_mismatches(a, b), int)


class TestSafePctChange:
    """Gold part 2: no silent ffill — gaps surface as NaN."""

    def test_known_values(self) -> None:
        s = pd.Series([10.0, 20.0, 30.0])
        result = mod.safe_pct_change(s)
        assert np.isnan(result.iloc[0])
        assert np.allclose(result.iloc[1:].tolist(), [1.0, 0.5])

    def test_gap_is_not_fabricated(self) -> None:
        s = pd.Series([10.0, np.nan, 20.0])
        result = mod.safe_pct_change(s)
        assert bool(result.isna().all()), \
            "default pct_change would fabricate [NaN, 0.0, 1.0] via ffill; " \
            "the safe version must surface the gap as NaN"

    def test_leading_nan_stays_nan(self) -> None:
        s = pd.Series([np.nan, 10.0, 20.0])
        result = mod.safe_pct_change(s)
        assert np.isnan(result.iloc[0]) and np.isnan(result.iloc[1])
        assert result.iloc[2] == 1.0, \
            "the window at position 2 is (10, 20) — no gap, delta is 1.0"

    def test_all_nan(self) -> None:
        s = pd.Series([np.nan, np.nan])
        result = mod.safe_pct_change(s)
        assert bool(result.isna().all())

    def test_zero_before_is_infinite(self) -> None:
        s = pd.Series([0.0, 10.0])
        result = mod.safe_pct_change(s)
        assert np.isinf(result.iloc[1]), \
            "division by zero must stay inf, not be masked by any fill"

    def test_constant_series(self) -> None:
        s = pd.Series([5.0, 5.0, 5.0])
        result = mod.safe_pct_change(s)
        assert np.allclose(result.iloc[1:].tolist(), [0.0, 0.0])

    def test_negative_change(self) -> None:
        s = pd.Series([20.0, 10.0])
        result = mod.safe_pct_change(s)
        assert result.iloc[1] == -0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
