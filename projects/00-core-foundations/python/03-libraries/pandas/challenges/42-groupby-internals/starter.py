"""
Challenge 42: GroupBy Internals — Starter
==========================================
Fill in the bodies. Do not change signatures or docstrings.
"""

from __future__ import annotations

import pandas as pd


def manual_group_mean(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """Split by key, mean the numeric columns, combine (no native groupby)."""
    raise NotImplementedError


def group_metrics(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """mean/max/count per numeric column per group, MultiIndex result."""
    raise NotImplementedError


def cohort_retention(df: pd.DataFrame) -> pd.DataFrame:
    """Retention matrix: rows = first-purchase month, cols = months since."""
    raise NotImplementedError
