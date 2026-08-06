"""
Challenge 41: Advanced Time Series — Tests
===========================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest challenges/41-timeseries-advanced/test_challenge.py -q
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


def _daily_series(n: int = 30, start: str = "2024-01-01") -> pd.Series:
    rng = np.random.RandomState(11)
    idx = pd.date_range(start, periods=n, freq="D")
    return pd.Series(rng.uniform(10, 20, n), index=idx)


class TestNoLeakRolling:
    """Bronze: the window must exclude the current row."""

    def test_basic(self) -> None:
        s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        result = mod.no_leak_rolling(s, 3)
        assert result.isna().tolist()[:3] == [True, True, True]
        assert result.iloc[3:] .tolist() == [2.0, 3.0], \
            "row t must be the mean of rows t-3..t-1, NOT t"

    def test_window_two(self) -> None:
        s = pd.Series([10.0, 20.0, 30.0])
        result = mod.no_leak_rolling(s, 2)
        assert np.isnan(result.iloc[0]) and np.isnan(result.iloc[1])
        assert result.iloc[2] == 15.0, \
            "row 2 must be the mean of rows 0..1 = 15.0"

    def test_empty(self) -> None:
        s = pd.Series(dtype="float64")
        assert len(mod.no_leak_rolling(s, 3)) == 0

    def test_excludes_current_value(self) -> None:
        s = pd.Series([100.0, 1.0, 1.0])
        result = mod.no_leak_rolling(s, 2)
        assert result.iloc[2] == 50.5, \
            "row 2's window is rows 0..1 (mean 50.5); if the current " \
            "value (1.0) were included the result would be 1.0"

    def test_window_larger_than_series(self) -> None:
        s = pd.Series([1.0, 2.0])
        result = mod.no_leak_rolling(s, 5)
        assert bool(result.isna().all())


class TestBuildFeatures:
    """Silver: past-only lag/window/delta features."""

    def test_known_values(self) -> None:
        s = pd.Series([10.0, 20.0, 30.0, 50.0],
                      index=pd.date_range("2024-01-01", periods=4, freq="D"))
        feats = mod.build_features(s, 2)
        assert np.isnan(feats["lag_1"].iloc[0])
        assert feats["lag_1"].iloc[1:].tolist() == [10.0, 20.0, 30.0]
        assert np.isnan(feats["mean_w"].iloc[0]) and np.isnan(feats["mean_w"].iloc[1])
        assert feats["mean_w"].iloc[2:].tolist() == [15.0, 25.0]
        assert np.allclose(feats["pct_chg"].iloc[1:].tolist(),
                           [1.0, 0.5, 2.0 / 3.0])

    def test_window_excludes_current(self) -> None:
        s = _daily_series(30)
        feats = mod.build_features(s, 5)
        for t in range(5, 30):
            expected = float(s.iloc[t - 5:t].mean())  # rows t-5 .. t-1
            assert abs(feats["mean_w"].iloc[t] - expected) < 1e-9, \
                f"mean_w at {t} must use rows t-5..t-1"

    def test_lag_is_previous_value(self) -> None:
        s = _daily_series(30)
        feats = mod.build_features(s, 5)
        assert feats["lag_1"].iloc[10] == s.iloc[9]

    def test_constant_series_zero_pct_change(self) -> None:
        s = pd.Series([7.0] * 6)
        feats = mod.build_features(s, 3)
        assert np.allclose(feats["pct_chg"].iloc[1:].tolist(), [0.0] * 5)

    def test_column_names(self) -> None:
        s = _daily_series(10)
        feats = mod.build_features(s, 3)
        assert feats.columns.tolist() == ["value", "lag_1", "mean_w", "pct_chg"]

    def test_index_preserved(self) -> None:
        s = _daily_series(10)
        feats = mod.build_features(s, 3)
        assert feats.index.equals(s.index)


class TestFeaturesWithoutFuture:
    """Gold: slicing first, future spike changes nothing."""

    def test_truncated_rows(self) -> None:
        s = _daily_series(30)
        cutoff = pd.Timestamp("2024-01-20")
        truncated = mod.features_without_future(s, cutoff, 5)
        assert len(truncated) == 19, "strictly before cutoff"

    def test_matches_full_on_overlap(self) -> None:
        s = _daily_series(30)
        cutoff = pd.Timestamp("2024-01-20")
        truncated = mod.features_without_future(s, cutoff, 5)
        full = mod.build_features(s, 5)
        assert mod.verify_no_future_leak(full, truncated) is True

    def test_future_spike_changes_nothing(self) -> None:
        s = _daily_series(30)
        spike = s.copy()
        spike.iloc[25:] += 1_000_000.0     # a gigantic future event
        cutoff = pd.Timestamp("2024-01-20")
        truncated_clean = mod.features_without_future(s, cutoff, 5)
        truncated_spike = mod.features_without_future(spike, cutoff, 5)
        assert mod.verify_no_future_leak(truncated_spike, truncated_clean) is True, \
            "features before the cutoff must not see the future spike"

    def test_cutoff_before_first_window_is_empty(self) -> None:
        s = _daily_series(30)
        cutoff = pd.Timestamp("2024-01-03")
        truncated = mod.features_without_future(s, cutoff, 5)
        assert len(truncated) == 0 or bool(truncated["mean_w"].isna().all())

    def test_cutoff_at_series_end_keeps_all(self) -> None:
        s = _daily_series(30)
        cutoff = pd.Timestamp("2024-02-01")
        truncated = mod.features_without_future(s, cutoff, 5)
        assert len(truncated) == 30

    def test_verify_rejects_modified_features(self) -> None:
        """The verifier must be strict enough to catch a real leak."""
        s = _daily_series(30)
        full = mod.build_features(s, 5)
        truncated = mod.features_without_future(s, pd.Timestamp("2024-01-20"), 5)
        broken = truncated.copy()
        broken["mean_w"] = broken["mean_w"] + 1.0
        assert mod.verify_no_future_leak(full, broken) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
