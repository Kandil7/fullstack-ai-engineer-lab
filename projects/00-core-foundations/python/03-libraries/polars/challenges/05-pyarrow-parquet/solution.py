"""
Challenge 05: PyArrow & Parquet — Reference Solution
======================================================
"""

from __future__ import annotations

import os

import polars as pl


def write_zstd_parquet(df: pl.DataFrame, path: str) -> int:
    """Write zstd parquet, return the on-disk size in bytes.

    Why this approach: zstd is the default parquet compression in Polars
    and gives the best size/speed trade-off for ML artifacts; the size
    check proves compression is active on the given frame.
    """
    df.write_parquet(path, compression="zstd")
    return os.path.getsize(path)


def compression_compare(df: pl.DataFrame, csv_path: str, pq_path: str) -> dict[str, int]:
    """Export csv + zstd parquet; return both sizes.

    Why this approach: comparing raw CSV vs columnar + zstd is the
    standard storage decision; a repetitive string column shows why
    parquet wins on ML feature stores.
    """
    df.write_csv(csv_path)
    df.write_parquet(pq_path, compression="zstd")
    return {
        "csv_bytes": os.path.getsize(csv_path),
        "parquet_bytes": os.path.getsize(pq_path),
    }


def roundtrip_zero_copy(df: pl.DataFrame, path: str) -> dict[str, object]:
    """Read back a numeric column without copying; report match + zero_copy.

    Why this approach: allow_copy=False makes the zero-copy contract
    explicit — a copy is an error, not a silent slowdown. Only a
    contiguous numeric column can be served straight from the arrow
    buffer, which is what makes numpy interop zero-overhead.
    """
    df.write_parquet(path, compression="zstd")
    restored = pl.scan_parquet(path).collect()
    source = df["score"].to_list()
    try:
        arr = restored["score"].to_numpy(allow_copy=False)
        zero_copy = True
    except RuntimeError:
        zero_copy = False
        arr = restored["score"].to_numpy()
    match = bool(len(arr) == len(source) and all(
        float(a) == float(b) for a, b in zip(arr, source)
    ))
    return {"match": match, "zero_copy": zero_copy}
