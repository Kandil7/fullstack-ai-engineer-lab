"""
Challenge 41: Advanced Time Series — Reference Solution
=========================================================
Why this approach:
- no_leak_rolling: rolling(window).mean() then .shift(1) — at row t the
  window covers rows t-window..t-1. The shift is the entire trick.
- build_features: shift for lag, rolling+shift for the window, pct_change
  for the relative delta — every column is past-only by construction.
- features_without_future: slice BEFORE building features, so the future
  is physically absent; the identical values prove nothing leaked.
- verify_no_future_leak: compare the overlapping rows of the two feature
  tables with np.allclose — a structural, not statistical, check.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def no_leak_rolling(series: pd.Series, window: int) -> pd.Series:
    """Rolling mean EXCLUDING the current row (shifted by one)."""
    return series.rolling(window).mean().shift(1)


def build_features(series: pd.Series, window: int) -> pd.DataFrame:
    """Feature table: value, lag_1, mean_w (no leak), pct_chg."""
    return pd.DataFrame({
        "value": series,
        "lag_1": series.shift(1),
        "mean_w": series.rolling(window).mean().shift(1),
        "pct_chg": series.pct_change(),
    })


def features_without_future(series: pd.Series, cutoff: pd.Timestamp,
                            window: int) -> pd.DataFrame:
    """Feature table restricted to rows strictly before cutoff."""
    past = series[series.index < cutoff]
    return build_features(past, window)


def verify_no_future_leak(full: pd.DataFrame, truncated: pd.DataFrame) -> bool:
    """True if truncated features match full features on overlapping rows."""
    overlap = full.loc[truncated.index, truncated.columns]
    return bool(np.allclose(overlap.to_numpy(dtype=float),
                            truncated.to_numpy(dtype=float),
                            equal_nan=True))
