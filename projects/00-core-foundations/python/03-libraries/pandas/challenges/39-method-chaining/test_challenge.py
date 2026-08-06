"""
Challenge 39: Method Chaining — Tests
======================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest challenges/39-method-chaining/test_challenge.py -q
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


class TestChainFilterAssign:
    """Bronze: filter + log1p assign, input untouched."""

    def test_basic(self) -> None:
        frame = pd.DataFrame({"spend": [50.0, 120.0, 300.0]})
        result = mod.chain_filter_assign(frame, 100.0)
        assert len(result) == 2
        assert result["spend"].tolist() == [120.0, 300.0]

    def test_log_spend_values(self) -> None:
        frame = pd.DataFrame({"spend": [120.0, 300.0]})
        result = mod.chain_filter_assign(frame, 100.0)
        expected = np.log1p([120.0, 300.0])
        assert np.allclose(result["log_spend"].values, expected)

    def test_empty_result_keeps_columns(self) -> None:
        frame = pd.DataFrame({"spend": [10.0, 20.0]})
        result = mod.chain_filter_assign(frame, 100.0)
        assert len(result) == 0
        assert result.columns.tolist() == ["spend", "log_spend"]

    def test_strict_greater_than(self) -> None:
        frame = pd.DataFrame({"spend": [50.0, 120.0]})
        result = mod.chain_filter_assign(frame, 50.0)
        assert result["spend"].tolist() == [120.0]

    def test_input_not_mutated(self) -> None:
        frame = pd.DataFrame({"spend": [50.0, 120.0, 300.0]})
        original = frame.copy()
        mod.chain_filter_assign(frame, 100.0)
        pd.testing.assert_frame_equal(frame, original)


class TestFeatureChain:
    """Silver: callable ranks the filtered frame; NaN rows dropped."""

    def _free_only(self) -> pd.DataFrame:
        return pd.DataFrame({
            "spend": [400.0, 350.0, 200.0, 50.0, 300.0],
            "plan": ["pro", "pro", "free", "free", "free"],
        })

    def test_rank_on_filtered_frame(self) -> None:
        frame = self._free_only()
        result = mod.feature_chain(frame)
        # The frame is sorted by spend descending; check rank by spend value.
        ranks = dict(zip(result["spend"].tolist(), result["rank"].tolist()))
        assert ranks[300.0] == 1.0 and ranks[200.0] == 2.0 and ranks[50.0] == 3.0, \
            "rank must be computed on the FILTERED frame (callable)"

    def test_nan_rows_dropped(self) -> None:
        frame = pd.DataFrame({"spend": [1.0, np.nan, 3.0],
                              "plan": ["free", "free", "free"]})
        result = mod.feature_chain(frame)
        assert len(result) == 2
        assert result["spend"].tolist() == [3.0, 1.0]  # sorted desc

    def test_all_columns_present(self) -> None:
        frame = self._free_only()
        result = mod.feature_chain(frame)
        for col in ["spend", "log_spend", "rank", "is_power_user"]:
            assert col in result.columns, f"missing column {col}"

    def test_sorted_descending(self) -> None:
        frame = self._free_only()
        result = mod.feature_chain(frame)
        assert result["spend"].is_monotonic_decreasing or \
            result["spend"].iloc[0] >= result["spend"].iloc[-1]

    def test_empty_result_keeps_columns(self) -> None:
        frame = pd.DataFrame({"spend": [0.0, -1.0], "plan": ["a", "b"]})
        result = mod.feature_chain(frame)
        assert len(result) == 0
        for col in ["spend", "log_spend", "rank", "is_power_user"]:
            assert col in result.columns

    def test_log_spend_matches_formula(self) -> None:
        frame = self._free_only()
        result = mod.feature_chain(frame)
        assert np.allclose(result["log_spend"].values,
                           np.log1p(result["spend"].values))


class TestAddRankAfterFilter:
    """Gold: rank post-query; ranking first then filtering fails."""

    def test_rank_excludes_filtered_rows(self) -> None:
        frame = pd.DataFrame({
            "spend": [400.0, 350.0, 200.0, 50.0, 300.0],
            "plan": ["pro", "pro", "free", "free", "free"],
        })
        result = mod.add_rank_after_filter(frame, "plan == 'free'", "spend")
        assert result["rank"].tolist() == [2.0, 3.0, 1.0], \
            "rank must be computed AFTER the query"

    def test_rank_spend_above_threshold(self) -> None:
        frame = pd.DataFrame({"spend": [400.0, 350.0, 200.0, 50.0, 300.0]})
        result = mod.add_rank_after_filter(frame, "spend > 100", "spend")
        # Kept rows: 400, 350, 200, 300 -> ranks 1, 2, 4, 3
        assert result["rank"].tolist() == [1.0, 2.0, 4.0, 3.0]

    def test_filter_preserves_index(self) -> None:
        frame = pd.DataFrame({"spend": [1.0, 2.0, 3.0, 4.0, 5.0]})
        result = mod.add_rank_after_filter(frame, "spend >= 3", "spend")
        assert result.index.tolist() == [2, 3, 4], \
            "query must preserve the original index labels"


class TestPipeThrough:
    """Gold: sequential (frame) -> frame application."""

    def test_applies_in_order(self) -> None:
        frame = pd.DataFrame({"spend": [50.0, 120.0, 300.0]})
        add_log = lambda f: f.assign(log_spend=np.log1p(f["spend"]))
        add_double = lambda f: f.assign(doubled=f["spend"] * 2)
        result = mod.pipe_through(frame, add_log, add_double)
        assert "log_spend" in result.columns
        assert "doubled" in result.columns

    def test_identity_with_no_transforms(self) -> None:
        frame = pd.DataFrame({"a": [1, 2, 3]})
        result = mod.pipe_through(frame)
        pd.testing.assert_frame_equal(result, frame)

    def test_order_matters(self) -> None:
        frame = pd.DataFrame({"v": [1.0, 2.0]})
        add_one = lambda f: f.assign(v=f["v"] + 1)
        times_ten = lambda f: f.assign(v=f["v"] * 10)
        result = mod.pipe_through(frame, add_one, times_ten)
        assert result["v"].tolist() == [20.0, 30.0], \
            "transforms must apply in the given order"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
