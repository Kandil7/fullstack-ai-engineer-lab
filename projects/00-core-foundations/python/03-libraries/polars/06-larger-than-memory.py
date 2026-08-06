"""
Polars — 06: Larger Than Memory
=================================
Topics: streaming engine; sinks; batch processing; out-of-core joins.

Why this matters for AI/backend engineering:
    A 50GB training corpus will not fit in RAM — but it must still be
    aggregated, joined, and converted. Polars handles this in three
    ways: the streaming engine (collect(engine="streaming")) processes
    data in batches instead of materializing the whole frame, sinks
    write lazy plans straight to disk, and joins stream when one side
    fits in memory. This file demonstrates the mechanics on a modest
    dataset so CI stays fast; the same code scales to hundreds of GB.

Run:      python 06-larger-than-memory.py
Verify:   python 06-larger-than-memory.py --verify
Reference: https://docs.pola.rs/user-guide/concepts/streaming/
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import numpy as np

try:
    import polars as pl
except ImportError:  # pragma: no cover - optional dependency
    print("[skip] polars not installed - install with: pip install polars")
    sys.exit(0)

_TMP = tempfile.TemporaryDirectory()
_OUT = Path(_TMP.name)

# Build a "large" dataset as 4 parquet shards (real corpora have hundreds
# of such files). 2M rows total — big enough to exercise streaming paths,
# small enough to stay well under the 20s runtime budget.
rng = np.random.default_rng(42)
N_SHARDS, ROWS_PER_SHARD = 4, 500_000
for shard in range(N_SHARDS):
    rows = {
        "user": rng.integers(0, 200_000, ROWS_PER_SHARD),
        "token_count": rng.integers(1, 500, ROWS_PER_SHARD),
        "prompt_type": rng.choice(["chat", "rag", "code"], ROWS_PER_SHARD),
    }
    pl.DataFrame(rows).write_parquet(_OUT / f"shard-{shard}.parquet")

BIG_CORPUS = pl.scan_parquet(_OUT)          # 4 files, one lazy table


# ============================================================
# 1. Streaming collect: process in batches, not all at once
# ============================================================
# collect(engine="streaming") runs the plan in bounded-memory batches.
# The result is identical to a regular collect; only the memory profile
# differs. Aggregates (sum, mean, count) are computed per batch and
# merged — no single 2M-row intermediate is ever built.

def streaming_aggregate() -> dict[str, int]:
    """Per-type totals computed via the streaming engine."""
    return dict(
        BIG_CORPUS.group_by("prompt_type")
        .agg(pl.col("token_count").sum().alias("total_tokens"))
        .sort("prompt_type")
        .collect(engine="streaming")
        .rows()
    )


# Example 1: the streaming engine returns the same numbers as eager
streamed = streaming_aggregate()
eager = dict(
    BIG_CORPUS.group_by("prompt_type")
    .agg(pl.col("token_count").sum().alias("total_tokens"))
    .sort("prompt_type")
    .collect()
    .rows()
)
print(f"streaming == eager: {streamed == eager}")
print(f"chat tokens: {streamed['chat']}")

# Output:
# streaming == eager: True
# chat tokens: 166736154


# ============================================================
# 2. Sinks: write a plan to disk without materializing
# ============================================================
# sink_parquet() consumes a LazyFrame and writes the result directly to
# disk. The intermediate DataFrame that a collect()+write would build
# never exists. This is the "ETL that touches 50GB" write path.

def sink_reduced_corpus() -> Path:
    """Write only chat rows, only two columns, via a sink."""
    out = _OUT / "chat-only.parquet"
    (
        BIG_CORPUS.filter(pl.col("prompt_type") == "chat")
        .select("user", "token_count")
        .sink_parquet(out)
    )
    return out


# Example 2: the sink file exists and holds the projected rows
sink_path = sink_reduced_corpus()
print(f"sink exists: {sink_path.exists()}, size: {sink_path.stat().st_size}")

# Output:
# sink exists: True, size: 4621890


# ============================================================
# 3. Batch processing: file-by-file accumulation
# ============================================================
# The most robust out-of-core pattern is shard-at-a-time processing:
# open each parquet file, reduce it to a tiny aggregate, merge. Peak
# memory is one shard + one aggregate row, no matter the corpus size.

def batch_aggregate() -> dict[str, int]:
    """Per-type token totals via a shard loop (bounded memory)."""
    totals: dict[str, int] = {}
    for shard_path in sorted(_OUT.glob("shard-*.parquet")):
        partial = dict(
            pl.scan_parquet(shard_path)
            .group_by("prompt_type")
            .agg(pl.col("token_count").sum().alias("total_tokens"))
            .collect()
            .rows()
        )
        for key, value in partial.items():
            totals[key] = totals.get(key, 0) + value
    return totals


# Example 3: the batch loop matches the single streaming pass
print(f"batch == streaming: {batch_aggregate() == streamed}")

# Output:
# batch == streaming: True


# ============================================================
# 4. Out-of-core join: big left side, small right side
# ============================================================
# When one side of a join fits in memory (user metadata, label maps,
# tokenizer vocab), Polars streams the big side through and looks up the
# small side — no full hash table for the big table.

meta = pl.DataFrame(
    {"user": [0, 1, 2, 3], "tier": ["free", "pro", "pro", "free"]}
)

def streamed_join() -> pl.DataFrame:
    """Join the 2M-row corpus with a tiny tier table, streaming."""
    return (
        BIG_CORPUS.select("user", "token_count")
        .join(meta.lazy(), on="user", how="left")
        .collect(engine="streaming")
    )


# Example 4: every big-side row gets its tier (unknown users -> null).
# We summarize as (user, tier, rows) so the output is stable and short.
joined = streamed_join()
print(joined.height, joined.columns)
print(joined.filter(pl.col("user") < 4).group_by("user", "tier").len().sort("user").rows())

# Output:
# 2000000 ['user', 'token_count', 'tier']
# [(0, 'free', 13), (1, 'pro', 6), (2, 'pro', 14), (3, 'free', 10)]


# ============================================================
# 5. Counting without materializing: metadata-first queries
# ============================================================
# Some questions never need the data: pl.len() on a lazy scan reads
# row-group metadata. This is the "how big is my corpus" query that must
# not load the corpus.

def corpus_row_count() -> int:
    """Count rows across all shards using only the lazy plan."""
    return BIG_CORPUS.select(pl.len()).collect(engine="streaming")[0, 0]


# Example 5: the count equals shards * rows_per_shard
print(corpus_row_count())

# Output:
# 2000000


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: collecting before filtering, "to be safe"
#   big = pl.scan_parquet(d).collect()   # whole corpus in RAM
#   small = big.filter(...)              # too late
# CORRECT: filter and select on the lazy frame, then collect
#
# MISTAKE: using a Python loop over rows to "process" a big file
#   for row in big_df.iter_rows():       # O(n) Python dispatch
# CORRECT: vectorized expressions; shard-at-a-time loops over FILES
#
# MISTAKE: assuming sink_parquet works on eager DataFrames
#   pl.DataFrame(...).sink_parquet(p)    # AttributeError
# CORRECT: sink only exists on LazyFrames: df.lazy().sink_parquet(p)


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    streamed_local = streaming_aggregate()
    assert set(streamed_local) == {"chat", "code", "rag"}, \
        "streaming group_by must cover all three prompt types"
    assert streamed_local["chat"] > 0, "aggregates must be positive"
    assert streamed_local["chat"] == 166736154, \
        "seeded data must reproduce the exact chat token total"

    eager_local = dict(
        BIG_CORPUS.group_by("prompt_type")
        .agg(pl.col("token_count").sum().alias("total_tokens"))
        .sort("prompt_type")
        .collect()
        .rows()
    )
    assert streamed_local == eager_local, \
        "streaming and eager engines must agree exactly"

    sink_path = sink_reduced_corpus()
    assert sink_path.exists() and sink_path.stat().st_size > 100_000, \
        "sink must produce a non-trivial parquet file"
    sink_rows = pl.scan_parquet(sink_path).collect().height
    total_rows = pl.read_parquet(_OUT / "chat-only.parquet").height
    assert sink_rows == total_rows, "sink file must be readable and stable"
    assert sink_rows < 2_000_000, "projection must drop non-chat rows"

    assert batch_aggregate() == streamed_local, \
        "shard-at-a-time loop must match the single streaming pass"

    joined = streamed_join()
    assert joined.height == 2_000_000, \
        "left join must keep every big-side row"
    assert joined.columns == ["user", "token_count", "tier"], \
        "join must bring the tier column"
    assert joined["tier"].null_count() > 0, \
        "users missing from metadata must get null tiers"
    tier_counts = (
        joined.group_by("tier").agg(pl.len()).sort("tier", nulls_last=True).rows()
    )
    assert tier_counts[0][0] == "free", \
        "free must sort first when nulls are pushed to the end"
    assert tier_counts[-1][0] is None, \
        "most rows belong to unknown users and get a null tier"

    assert corpus_row_count() == 2_000_000, \
        "lazy count must equal shards x rows_per_shard"

    print("[OK] 06-larger-than-memory: all checks passed")


if __name__ == "__main__":
    try:
        if "--verify" in sys.argv:
            _verify()
        else:
            print("\n--- Summary ---")
            print("1. collect(engine='streaming') batches; same numbers, lower peak RAM")
            print("2. sink_parquet writes plans to disk without materializing")
            print("3. Shard loops and small-side joins keep memory bounded")
            _verify()   # always runs, so plain execution is also a test
    finally:
        _TMP.cleanup()   # close handles + delete temp files (Windows-safe)
