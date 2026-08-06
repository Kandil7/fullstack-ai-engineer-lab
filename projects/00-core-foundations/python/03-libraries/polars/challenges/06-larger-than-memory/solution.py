"""
Challenge 06: Larger Than Memory — Reference Solution
=======================================================
"""

from __future__ import annotations

import polars as pl


def streaming_count(path: str) -> dict[str, object]:
    """Count CSV rows via the streaming engine.

    Why this approach: a streaming count touches every row but keeps
    only the running total in memory — the canonical larger-than-memory
    pattern. The flag makes the contract explicit for readers.
    """
    rows = (
        pl.scan_csv(path)
        .select(pl.len())
        .collect(engine="streaming")[0, 0]
    )
    return {"rows": int(rows), "streaming": True}


def chunked_stats(dir_path: str, column: str) -> dict[str, float]:
    """Aggregate across parquet shards with a single streaming scan.

    Why this approach: one scan of the directory pushes len + mean into
    each shard scan; the streaming engine folds the partial results so
    peak memory is one chunk, not the full dataset.
    """
    out = (
        pl.scan_parquet(dir_path)
        .select(pl.len(), pl.col(column).mean())
        .collect(engine="streaming")
    )
    return {"rows": float(out[0, 0]), "mean": float(out[0, 1])}


def sink_join(left_dir: str, right_dir: str, left_key: str, right_key: str, out_path: str) -> int:
    """Lazy join two shard dirs; sink to parquet; return written rows.

    Why this approach: sink_parquet streams the joined result straight
    to disk chunk by chunk, so neither the join input nor the output
    ever exists fully in RAM. Counting via a fresh streaming scan keeps
    the verification lazy too.
    """
    lf = pl.scan_parquet(left_dir)
    rf = pl.scan_parquet(right_dir)
    lf.join(rf, left_on=left_key, right_on=right_key, how="inner").sink_parquet(
        out_path, engine="streaming"
    )
    return pl.scan_parquet(out_path).select(pl.len()).collect(engine="streaming")[0, 0]
