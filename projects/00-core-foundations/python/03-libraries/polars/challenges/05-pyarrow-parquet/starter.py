"""
Challenge 05: PyArrow & Parquet — Starter Code
===============================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import polars as pl


def write_zstd_parquet(df: pl.DataFrame, path: str) -> int:
    """Write zstd parquet, return the on-disk size in bytes."""
    raise NotImplementedError


def compression_compare(df: pl.DataFrame, csv_path: str, pq_path: str) -> dict[str, int]:
    """Export csv + zstd parquet; return both sizes."""
    raise NotImplementedError


def roundtrip_zero_copy(df: pl.DataFrame, path: str) -> dict[str, object]:
    """Read back a numeric column without copying; report match + zero_copy."""
    raise NotImplementedError
