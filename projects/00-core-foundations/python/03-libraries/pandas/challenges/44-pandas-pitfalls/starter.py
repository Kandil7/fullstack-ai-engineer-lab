"""
Challenge 44: Pandas Pitfalls — Starter
========================================
Fill in the bodies. Do not change signatures or docstrings.
"""

from __future__ import annotations

import pandas as pd


def filter_below(df: pd.DataFrame, col: str, threshold: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(kept rows where col < threshold, dropped rows). NaN rows are dropped."""
    raise NotImplementedError


def merge_check_duplicates(left: pd.DataFrame, right: pd.DataFrame, on: str) -> pd.DataFrame:
    """Inner merge on `on`, raising ValueError if either side has duplicate keys."""
    raise NotImplementedError


def count_nan_mismatches(a: pd.Series, b: pd.Series) -> int:
    """Positions where exactly one of a, b is NaN."""
    raise NotImplementedError


def safe_pct_change(series: pd.Series) -> pd.Series:
    """pct_change WITHOUT the silent ffill: gaps surface as NaN, not fabricated deltas."""
    raise NotImplementedError
