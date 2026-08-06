"""
Challenge 42: GroupBy Internals — Tests
========================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest challenges/42-groupby-internals/test_challenge.py -q
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


def _teams_df(n_per_team: int = 4) -> pd.DataFrame:
    rng = np.random.RandomState(3)
    teams = np.repeat(["a", "b"], n_per_team)
    return pd.DataFrame({
        "team": teams,
        "score": rng.uniform(0, 100, len(teams)),
        "age": rng.randint(20, 40, len(teams)),
    })


class TestManualGroupMean:
    """Bronze: hand-rolled split-apply-combine, no native groupby."""

    def test_known_means(self) -> None:
        df = pd.DataFrame({"team": ["a", "a", "a", "b", "b"],
                           "x": [1.0, 2.0, 3.0, 10.0, 20.0],
                           "y": [10.0, 20.0, 30.0, 1.0, 2.0]})
        result = mod.manual_group_mean(df, "team")
        assert result.index.tolist() == ["a", "b"]
        assert np.allclose(result.loc["a"], [2.0, 20.0])
        assert np.allclose(result.loc["b"], [15.0, 1.5])

    def test_does_not_call_groupby(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _boom(*args, **kwargs):
            raise AssertionError("manual_group_mean must not call groupby")

        monkeypatch.setattr(pd.DataFrame, "groupby", _boom)
        df = _teams_df(3)
        result = mod.manual_group_mean(df, "team")
        assert result.shape == (2, 2)

    def test_numeric_columns_only(self) -> None:
        df = pd.DataFrame({"team": ["a", "b"], "x": [1.0, 2.0],
                           "name": ["alice", "bob"]})
        result = mod.manual_group_mean(df, "team")
        assert result.columns.tolist() == ["x"]

    def test_empty_frame(self) -> None:
        df = pd.DataFrame({"team": pd.Series(dtype="str"),
                           "x": pd.Series(dtype="float64")})
        result = mod.manual_group_mean(df, "team")
        assert len(result) == 0

    def test_missing_key(self) -> None:
        df = pd.DataFrame({"x": [1.0]})
        with pytest.raises(KeyError):
            mod.manual_group_mean(df, "nope")

    def test_index_is_key_values(self) -> None:
        df = _teams_df(3)
        result = mod.manual_group_mean(df, "team")
        assert result.index.tolist() == ["a", "b"]


class TestGroupMetrics:
    """Silver: mean/max/count per numeric column, MultiIndex result."""

    def test_layout(self) -> None:
        df = _teams_df(4)
        result = mod.group_metrics(df, "team")
        assert result.columns.nlevels == 2
        assert set(result.columns.get_level_values(0)) == {"score", "age"}
        assert set(result.columns.get_level_values(1)) == {"mean", "max", "count"}
        assert result.shape == (2, 6)

    def test_values_match_native(self) -> None:
        df = _teams_df(4)
        result = mod.group_metrics(df, "team")
        native = df.groupby("team")[["score", "age"]].agg(
            ["mean", "max", "count"])
        assert np.allclose(result.to_numpy(), native.to_numpy())

    def test_count_skips_nan(self) -> None:
        df = pd.DataFrame({"team": ["a", "a", "b"],
                           "x": [1.0, np.nan, 5.0]})
        result = mod.group_metrics(df, "team")
        assert result.loc["a", ("x", "count")] == 1.0
        assert result.loc["b", ("x", "count")] == 1.0

    def test_all_nan_group_count_is_zero(self) -> None:
        df = pd.DataFrame({"team": ["a", "a", "b"],
                           "x": [np.nan, np.nan, 1.0]})
        result = mod.group_metrics(df, "team")
        assert result.loc["a", ("x", "count")] == 0.0, \
            "count must count non-NaN values, not group size"

    def test_single_column(self) -> None:
        df = pd.DataFrame({"team": ["a", "b"], "x": [1.0, 2.0]})
        result = mod.group_metrics(df, "team")
        assert result.shape == (2, 3)

    def test_mean_skips_nan(self) -> None:
        df = pd.DataFrame({"team": ["a", "a", "a"],
                           "x": [1.0, 2.0, np.nan]})
        result = mod.group_metrics(df, "team")
        assert abs(result.loc["a", ("x", "mean")] - 1.5) < 1e-9


class TestCohortRetention:
    """Gold: first-month cohorts, months-since columns, fraction retained."""

    def test_known_matrix(self) -> None:
        df = pd.DataFrame({
            "user_id": [1, 1, 2],
            "month": ["2024-01", "2024-02", "2024-01"],
        })
        result = mod.cohort_retention(df)
        assert result.index.tolist() == ["2024-01"]
        assert result.columns.tolist() == [0, 1]
        assert np.allclose(result.iloc[0].tolist(), [1.0, 0.5])

    def test_two_cohorts(self) -> None:
        df = pd.DataFrame({
            "user_id": [1, 1, 2, 3],
            "month": ["2024-01", "2024-02", "2024-02", "2024-02"],
        })
        result = mod.cohort_retention(df)
        assert result.index.tolist() == ["2024-01", "2024-02"]
        # cohort 2024-01: 1 user, active in month 0 and month 1 -> [1.0, 1.0]
        assert np.allclose(result.loc["2024-01"].tolist(), [1.0, 1.0])
        # cohort 2024-02: 2 users, both active in month 0 -> [1.0, 0.0]
        assert np.allclose(result.loc["2024-02"].tolist(), [1.0, 0.0])

    def test_diagonal_for_single_month_users(self) -> None:
        users = [f"u{i}" for i in range(5)]
        df = pd.DataFrame({"user_id": users,
                           "month": ["2024-01"] * 5})
        result = mod.cohort_retention(df)
        assert result.shape == (1, 1)
        assert result.iloc[0, 0] == 1.0

    def test_empty(self) -> None:
        df = pd.DataFrame({"user_id": pd.Series(dtype="int64"),
                           "month": pd.Series(dtype="str")})
        result = mod.cohort_retention(df)
        assert len(result) == 0

    def test_values_are_fractions_not_counts(self) -> None:
        df = pd.DataFrame({
            "user_id": [1, 1, 2, 2, 3],
            "month": ["2024-01", "2024-02", "2024-01", "2024-02", "2024-02"],
        })
        result = mod.cohort_retention(df)
        # cohort 2024-01 has 2 users; both return in month 1 -> [1.0, 1.0]
        assert np.allclose(result.loc["2024-01"].tolist(), [1.0, 1.0])
        # cohort 2024-02 has 1 user (u3) -> [1.0, 0.0]
        assert np.allclose(result.loc["2024-02"].tolist(), [1.0, 0.0])

    def test_column_zero_always_one(self) -> None:
        df = pd.DataFrame({
            "user_id": [1, 2, 3, 4],
            "month": ["2024-01", "2024-01", "2024-02", "2024-02"],
        })
        result = mod.cohort_retention(df)
        assert bool((result[0] == 1.0).all()), \
            "month 0 retention is 1.0 by construction"

    def test_realistic_retention_drop(self) -> None:
        df = pd.DataFrame({
            "user_id": [1, 1, 2, 3, 4],
            "month": ["2024-01", "2024-02", "2024-01", "2024-01", "2024-01"],
        })
        result = mod.cohort_retention(df)
        # 4 users join in 2024-01, only 1 returns in 2024-02 -> [1.0, 0.25]
        assert np.allclose(result.loc["2024-01"].tolist(), [1.0, 0.25])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
