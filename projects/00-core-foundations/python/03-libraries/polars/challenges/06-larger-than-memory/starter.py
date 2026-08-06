"""
Challenge 06: Larger Than Memory — Starter Code
=================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import polars as pl


def streaming_count(path: str) -> dict[str, object]:
    """Count CSV rows via the streaming engine."""
    raise NotImplementedError


def chunked_stats(dir_path: str, column: str) -> dict[str, float]:
    """Aggregate across parquet shards with a single streaming scan."""
    raise NotImplementedError


def sink_join(left_dir: str, right_dir: str, left_key: str, right_key: str, out_path: str) -> int:
    """Lazy join two shard dirs; sink to parquet; return written rows."""
    raise NotImplementedError
