"""
Challenge 42: GroupBy Internals — Reference Solution
======================================================
Why this approach:
- manual_group_mean: reimplements split-apply-combine by hand — unique keys,
  boolean filtering per key, mean over numeric columns, concat back. The
  "no native groupby" guard in the tests exists to force this.
- group_metrics: one pass over numeric columns, per-column agg computed via
  groupby (the user may use groupby here; only Bronze is manual), then
  stacked into a MultiIndex via sortlevel for a canonical (column, metric)
  layout.
- cohort_retention: groupby("user_id")["month"].min() = first purchase month
  per user; months since = month index - cohort index; then group users by
  cohort and by months-since, count unique users, and normalize each cohort
  row by its size (column 0 is always 1.0 by construction).
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def manual_group_mean(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """Split by key, mean the numeric columns, combine (no native groupby)."""
    numeric = df.select_dtypes(include="number").columns
    rows = []
    for key_val in df[key].unique():
        group = df[df[key] == key_val]
        rows.append(group[numeric].mean().rename(key_val))
    if not rows:
        return pd.DataFrame(columns=numeric, dtype="float64")
    return pd.concat(rows, axis=1).T


def group_metrics(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """mean/max/count per numeric column per group, MultiIndex result."""
    parts = []
    for col in df.select_dtypes(include="number").columns:
        agg = df.groupby(key)[col].agg(["mean", "max", "count"])
        agg.columns = pd.MultiIndex.from_product([[col], ["mean", "max", "count"]])
        parts.append(agg)
    # concat keeps (column, metric) order matching the native agg layout
    return pd.concat(parts, axis=1).sort_index(axis=0)


def cohort_retention(df: pd.DataFrame) -> pd.DataFrame:
    """Retention matrix: rows = first-purchase month, cols = months since."""
    if df.empty:
        return pd.DataFrame()
    month_idx = pd.Series(
        pd.RangeIndex(len(pd.unique(df["month"]))),
        index=pd.unique(df["month"]),
    )
    first = df.groupby("user_id")["month"].min().rename("first")
    merged = df.merge(first, left_on="user_id", right_index=True)
    merged["cohort"] = merged["first"]
    merged["months_since"] = merged["month"].map(month_idx) - \
        merged["cohort"].map(month_idx)
    counts = (merged.groupby(["cohort", "months_since"])["user_id"]
              .nunique().unstack(fill_value=0))
    sizes = merged.groupby("cohort")["user_id"].nunique()
    return counts.div(sizes, axis=0)
