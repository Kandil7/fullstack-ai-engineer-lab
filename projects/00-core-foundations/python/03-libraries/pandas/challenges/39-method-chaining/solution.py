"""
Challenge 39: Method Chaining — Reference Solution
====================================================
Why this approach:
- chain_filter_assign: .query() returns a NEW frame, so the input is
  never mutated; log_spend via callable keeps the chain safe.
- feature_chain: starts with .copy() for defense, filters BEFORE
  ranking, and uses callables so rank/is_power_user describe the
  filtered cohort. sort_values last.
- add_rank_after_filter: query first, then rank the result — the
  precomputed-Series version (rank full frame) is the bug this pins.
- pipe_through: a simple loop of (frame) -> frame callables; no
  magic, and it fails loudly if any transform returns None.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def chain_filter_assign(frame: pd.DataFrame, min_spend: float) -> pd.DataFrame:
    """Return a NEW frame with spend > min_spend plus a log_spend column.

    The input frame must not be modified.
    """
    return (
        frame
        .query("spend > @min_spend")
        .assign(log_spend=lambda d: np.log1p(d["spend"]))
    )


def feature_chain(frame: pd.DataFrame) -> pd.DataFrame:
    """Production chain: copy -> dropna -> free + spend>0 -> log/rank/power -> sort.

    rank must be computed on the FILTERED frame (use a callable).
    """
    return (
        frame
        .copy()
        .dropna()
        .query("plan == 'free' and spend > 0")
        .assign(
            log_spend=lambda d: np.log1p(d["spend"]),
            rank=lambda d: d["spend"].rank(ascending=False),
            is_power_user=lambda d: d["spend"] >= d["spend"].quantile(0.8),
        )
        .sort_values("spend", ascending=False)
    )


def add_rank_after_filter(frame: pd.DataFrame, filter_expr: str,
                          col: str) -> pd.DataFrame:
    """Query the frame, then add a descending rank computed post-filter."""
    filtered = frame.query(filter_expr)
    return filtered.assign(rank=filtered[col].rank(ascending=False))


def pipe_through(frame: pd.DataFrame, *transforms) -> pd.DataFrame:
    """Apply transforms sequentially, each (frame) -> frame."""
    result = frame
    for transform in transforms:
        result = transform(result)
    return result
