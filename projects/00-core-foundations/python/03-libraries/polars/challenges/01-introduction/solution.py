"""
Challenge 01: Polars Introduction — Reference Solution
========================================================
"""

from __future__ import annotations

import polars as pl

_NUMERIC_WIDTHS = {
    pl.Int8: 8,
    pl.Int16: 16,
    pl.Int32: 32,
    pl.Int64: 64,
    pl.UInt8: 8,
    pl.UInt16: 16,
    pl.UInt32: 32,
    pl.UInt64: 64,
    pl.Float32: 32,
    pl.Float64: 64,
}


def build_features_frame(raw: dict[str, list]) -> pl.DataFrame:
    """Build a typed feature frame from raw column dicts.

    Why this approach: DataFrame construction infers dtypes, and Polars
    refuses to silently reinterpret "1" as an int at build time (strict
    mode). The explicit, version-robust idiom is to construct and then
    .cast() the columns that must change type. Casting is the contract
    that keeps feature pipelines honest.
    """
    return pl.DataFrame(raw).with_columns(
        pl.col("sample_id").cast(pl.Int64),
        pl.col("score").cast(pl.Float64),
    )


def column_stats(df: pl.DataFrame) -> dict[str, tuple[float, float, float]]:
    """Return {col: (mean, min, max)} for every numeric column.

    Why this approach: each statistic is a vectorized kernel over one
    column; the loop iterates over COLUMNS (O(columns) iterations), never
    over rows. A Python loop over rows would be O(n) dispatches.
    """
    result: dict[str, tuple[float, float, float]] = {}
    for name, dtype in df.schema.items():
        if dtype in _NUMERIC_WIDTHS:
            series = df[name]
            result[name] = (
                float(series.mean()),
                float(series.min()),
                float(series.max()),
            )
    return result


def estimate_numeric_bytes(df: pl.DataFrame) -> int:
    """Estimate the in-memory bytes of numeric columns from dtype widths.

    Why this approach: walking the schema is O(columns) regardless of row
    count; the width table maps Arrow dtypes to bit widths. This is the
    back-of-envelope estimate behind eager-vs-streaming decisions.
    """
    total = 0
    for name, dtype in df.schema.items():
        width = _NUMERIC_WIDTHS.get(dtype)
        if width is not None:
            total += df.height * (width // 8)
    return total
