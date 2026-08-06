"""
Challenge 44: Pandas Pitfalls — Reference Solution
====================================================
Why this approach:
- filter_below: NaN comparisons are always False, so df[col] < threshold
  already excludes NaN rows; the KEPT set is that mask, the DROPPED set is
  its complement — explicit so the caller knows NaN rows went to dropped.
- merge_check_duplicates: duplicated(on) is True for every row that has a
  key seen before; ANY such row means the key column isn't unique, and a
  merge would silently multiply rows.
- count_nan_mismatches: XOR of the two NaN masks — positions where the
  NaN-ness differs. Identical patterns -> 0.
- safe_pct_change: the DEFAULT pct_change calls fill_method='pad', silently
  FFILLING gaps — [10, NaN, 20] -> [NaN, 0.0, 1.0] fabricates a 0% delta at
  the missing position and a 100% delta computed from a filled value. The
  safe version passes fill_method=None so every gap-window surfaces as NaN
  (and the deprecation warning for the default is avoided by being explicit).
"""

from __future__ import annotations

import pandas as pd


def filter_below(df: pd.DataFrame, col: str, threshold: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(kept rows where col < threshold, dropped rows). NaN rows are dropped."""
    mask = df[col] < threshold
    return df[mask].copy(), df[~mask].copy()


def merge_check_duplicates(left: pd.DataFrame, right: pd.DataFrame, on: str) -> pd.DataFrame:
    """Inner merge on `on`, raising ValueError if either side has duplicate keys."""
    if left[on].duplicated().any() or right[on].duplicated().any():
        raise ValueError("merge key has duplicates — rows would multiply silently")
    return left.merge(right, on=on)


def count_nan_mismatches(a: pd.Series, b: pd.Series) -> int:
    """Positions where exactly one of a, b is NaN."""
    return int((a.isna() ^ b.isna()).sum())


def safe_pct_change(series: pd.Series) -> pd.Series:
    """pct_change WITHOUT the silent ffill: gaps surface as NaN, not fabricated deltas."""
    return series.pct_change(fill_method=None)
