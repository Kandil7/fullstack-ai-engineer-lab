"""
Challenge 41: Advanced Time Series — Starter
=============================================
Fill in the bodies. Do not change signatures or docstrings.
"""

from __future__ import annotations

import pandas as pd


def no_leak_rolling(series: pd.Series, window: int) -> pd.Series:
    """Rolling mean EXCLUDING the current row (shifted by one)."""
    raise NotImplementedError


def build_features(series: pd.Series, window: int) -> pd.DataFrame:
    """Feature table: value, lag_1, mean_w (no leak), pct_chg."""
    raise NotImplementedError


def features_without_future(series: pd.Series, cutoff: pd.Timestamp,
                            window: int) -> pd.DataFrame:
    """Feature table restricted to rows strictly before cutoff."""
    raise NotImplementedError


def verify_no_future_leak(full: pd.DataFrame, truncated: pd.DataFrame) -> bool:
    """True if truncated features match full features on overlapping rows."""
    raise NotImplementedError
