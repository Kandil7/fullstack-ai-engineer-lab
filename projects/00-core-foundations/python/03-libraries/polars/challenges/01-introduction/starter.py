"""
Challenge 01: Polars Introduction — Starter Code
==================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import polars as pl


def build_features_frame(raw: dict[str, list]) -> pl.DataFrame:
    """Build a typed feature frame from raw column dicts.

    Columns: sample_id (Int64), score (Float64), split (String).
    The schema must be forced explicitly, never inferred.
    """
    raise NotImplementedError


def column_stats(df: pl.DataFrame) -> dict[str, tuple[float, float, float]]:
    """Return {col: (mean, min, max)} for every numeric column.

    Vectorized expressions only: no Python loops over rows, no .apply().
    """
    raise NotImplementedError


def estimate_numeric_bytes(df: pl.DataFrame) -> int:
    """Estimate the in-memory bytes of numeric columns from dtype widths.

    Sum of row_count * dtype_width over numeric columns only.
    Must be O(columns), not O(rows).
    """
    raise NotImplementedError
