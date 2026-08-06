"""
Challenge 43: Pandas for ML — Tests
====================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest challenges/43-pandas-for-ml/test_challenge.py -q
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
from sklearn.preprocessing import StandardScaler


class TestChronoSplit:
    """Bronze: chronological train/test split."""

    def test_basic_fraction(self) -> None:
        df = pd.DataFrame({"x": range(10)})
        train, test = mod.chrono_split(df, 0.6)
        assert len(train) == 6 and len(test) == 4
        assert train["x"].tolist() == [0, 1, 2, 3, 4, 5]
        assert test["x"].tolist() == [6, 7, 8, 9]

    def test_zero_fraction(self) -> None:
        df = pd.DataFrame({"x": range(10)})
        train, test = mod.chrono_split(df, 0.0)
        assert len(train) == 0 and len(test) == 10

    def test_full_fraction(self) -> None:
        df = pd.DataFrame({"x": range(10)})
        train, test = mod.chrono_split(df, 1.0)
        assert len(train) == 10 and len(test) == 0

    def test_chronological_order_guaranteed(self) -> None:
        df = pd.DataFrame({"t": pd.date_range("2024-01-01", periods=50, freq="D")})
        train, test = mod.chrono_split(df, 0.7)
        assert train["t"].max() <= test["t"].min()

    def test_does_not_modify_input(self) -> None:
        df = pd.DataFrame({"x": range(10)})
        _ = mod.chrono_split(df, 0.5)
        assert df["x"].tolist() == list(range(10))

    def test_uneven_fraction_rounds_down(self) -> None:
        df = pd.DataFrame({"x": range(7)})
        train, test = mod.chrono_split(df, 0.5)
        assert len(train) == 3 and len(test) == 4


class TestFitScaleTrainTest:
    """Silver: scaler fitted on train only."""

    def test_known_values(self) -> None:
        X_train = pd.DataFrame({"x": [0.0, 2.0]})
        X_test = pd.DataFrame({"x": [0.0, 10.0]})
        tr_s, te_s, fitted = mod.fit_scale_train_test(
            X_train, X_test, StandardScaler())
        # train mean 1, std 1 -> test 0 -> -1.0, test 10 -> 9.0
        assert np.allclose(te_s["x"].tolist(), [-1.0, 9.0]), \
            "test must be scaled by TRAIN mean/std, not pooled"

    def test_returns_fitted_scaler(self) -> None:
        X_train = pd.DataFrame({"x": [0.0, 2.0]})
        X_test = pd.DataFrame({"x": [5.0]})
        _, _, fitted = mod.fit_scale_train_test(X_train, X_test, StandardScaler())
        assert hasattr(fitted, "mean_")
        assert np.allclose(fitted.mean_, [1.0])
        assert np.allclose(fitted.scale_, [1.0])

    def test_constant_train_column(self) -> None:
        X_train = pd.DataFrame({"x": [5.0, 5.0, 5.0]})
        X_test = pd.DataFrame({"x": [5.0, 6.0]})
        tr_s, te_s, _ = mod.fit_scale_train_test(X_train, X_test, StandardScaler())
        assert np.allclose(tr_s["x"].tolist(), [0.0, 0.0, 0.0])

    def test_multi_column(self) -> None:
        X_train = pd.DataFrame({"a": [0.0, 2.0], "b": [10.0, 20.0]})
        X_test = pd.DataFrame({"a": [0.0, 10.0], "b": [15.0, 30.0]})
        tr_s, te_s, _ = mod.fit_scale_train_test(
            X_train, X_test, StandardScaler())
        assert te_s.shape == (2, 2)
        assert np.allclose(te_s["a"].tolist(), [-1.0, 9.0])

    def test_train_scaled_is_standard(self) -> None:
        X_train = pd.DataFrame({"x": [0.0, 2.0, 4.0, 6.0]})
        X_test = pd.DataFrame({"x": [1.0]})
        tr_s, _, _ = mod.fit_scale_train_test(X_train, X_test, StandardScaler())
        assert abs(float(tr_s["x"].mean())) < 1e-9
        # sklearn's scale_ is the POPULATION std (ddof=0); match it here
        assert abs(float(tr_s["x"].std(ddof=0)) - 1.0) < 1e-9


class TestPipelines:
    """Gold: no-leak beats leaky on unseen-data rmse."""

    @staticmethod
    def _linear_df(n: int = 100, noise: float = 1.0,
                   slope: float = 2.0) -> pd.DataFrame:
        rng = np.random.RandomState(7)
        x = np.linspace(0, 10, n)
        y = slope * x + rng.normal(0, noise, n)
        return pd.DataFrame({"x": x, "y": y})

    def test_no_leak_beats_leaky(self) -> None:
        df = self._linear_df(100, noise=1.0)
        _, rmse_clean, _ = mod.evaluate_no_leak_pipeline(
            df, "y", 0.6, StandardScaler())
        _, rmse_leaky, _ = mod.evaluate_leaky_pipeline(
            df, "y", 0.6, StandardScaler())
        assert rmse_clean < rmse_leaky, \
            f"no-leak {rmse_clean:.4f} should beat leaky {rmse_leaky:.4f}"

    def test_perfect_linear_near_zero_rmse(self) -> None:
        df = self._linear_df(100, noise=0.0, slope=3.0)
        _, rmse, _ = mod.evaluate_no_leak_pipeline(
            df, "y", 0.6, StandardScaler(), alpha=1e-12)
        assert rmse < 1e-9

    def test_constant_target_finite(self) -> None:
        rng = np.random.RandomState(1)
        df = pd.DataFrame({"x": rng.uniform(0, 1, 50),
                           "y": np.full(50, 42.0)})
        _, rmse_clean, _ = mod.evaluate_no_leak_pipeline(
            df, "y", 0.6, StandardScaler())
        _, rmse_leaky, _ = mod.evaluate_leaky_pipeline(
            df, "y", 0.6, StandardScaler())
        assert np.isfinite(rmse_clean) and np.isfinite(rmse_leaky)

    def test_scaled_test_contains_prediction_column(self) -> None:
        df = self._linear_df(100, noise=0.5)
        _, _, scaled_test = mod.evaluate_no_leak_pipeline(
            df, "y", 0.6, StandardScaler())
        assert "prediction" in scaled_test.columns
        assert "y" in scaled_test.columns
        assert len(scaled_test) == 40

    def test_leaky_uses_pooled_scaler(self) -> None:
        """The leaky pipeline must scale test with pooled fit: build a frame
        where the test mean differs strongly from train mean, and verify the
        leaky scaled test column differs from the clean one."""
        df = self._linear_df(100, noise=0.0)
        _, _, clean = mod.evaluate_no_leak_pipeline(df, "y", 0.5, StandardScaler())
        _, _, leaky = mod.evaluate_leaky_pipeline(df, "y", 0.5, StandardScaler())
        assert not np.allclose(clean["x"].to_numpy(), leaky["x"].to_numpy()), \
            "pooled scaling must shift the test features"

    def test_rmse_returns_float(self) -> None:
        df = self._linear_df(50, noise=0.5)
        _, rmse, _ = mod.evaluate_no_leak_pipeline(df, "y", 0.6, StandardScaler())
        assert isinstance(rmse, float)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
