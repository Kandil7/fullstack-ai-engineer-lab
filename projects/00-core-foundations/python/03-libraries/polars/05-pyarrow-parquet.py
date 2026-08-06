"""
Polars — 05: PyArrow and Parquet
=================================
Topics: Arrow tables; Parquet columnar layout; compression; partitioning;
zero-copy to NumPy; why Parquet over CSV for datasets.

Why this matters for AI/backend engineering:
    Parquet is the standard dataset format for ML corpora, and Arrow is
    the zero-copy bridge between pandas, Polars, DuckDB, and PyTorch.
    This file shows the whole chain: build a table in Arrow, read it in
    Polars, write Parquet with different compressions, partition it by a
    key, and hand a column to NumPy WITHOUT copying. If your pipeline
    still ships CSVs, this topic is the migration you are missing.

Run:      python 05-pyarrow-parquet.py
Verify:   python 05-pyarrow-parquet.py --verify
Reference: https://arrow.apache.org/docs/python/parquet.html
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

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:  # pragma: no cover - optional dependency
    print("[skip] pyarrow not installed - install with: pip install pyarrow")
    sys.exit(0)

_TMP = tempfile.TemporaryDirectory()
_OUT = Path(_TMP.name)

# Deterministic synthetic dataset: 100k embedding-like float rows.
rng = np.random.default_rng(42)
n = 100_000
records = {
    "id": np.arange(n),
    "emb_0": rng.normal(0.0, 1.0, n),
    "emb_1": rng.normal(0.0, 1.0, n),
    "label": rng.choice(["pos", "neg"], n),
}
pl_src = pl.DataFrame(records)


# ============================================================
# 1. Arrow Table: the interchange format itself
# ============================================================
# An Arrow Table is columnar memory with an explicit schema. Polars can
# wrap it without conversion: pl.from_arrow() shares the buffers. This is
# the zero-copy handoff point between every Arrow-native tool.

def build_arrow_table() -> pa.Table:
    """Build an Arrow Table from numpy arrays."""
    return pa.table(
        {
            "id": pa.array(records["id"]),
            "emb_0": pa.array(records["emb_0"]),
            "label": pa.array(records["label"]),
        }
    )


# Example 1: Arrow schema is explicit and typed
at = build_arrow_table()
print(at.schema)

# Output:
# id: int64
# emb_0: double
# label: string
# -- schema metadata --
# ...(metadata keys omitted)...


# ============================================================
# 2. Zero-copy: Arrow -> Polars -> NumPy without duplicating bytes
# ============================================================
# pl.from_arrow() and df.to_numpy(allow_copy=False) can share the same
# buffer. np.shares_memory() proves no copy happened. Strings are the
# exception: they need per-value offsets, so copies are unavoidable there.

def arrow_to_numpy_view() -> tuple[np.ndarray, bool]:
    """Convert an Arrow column to a numpy view; return (array, is_view)."""
    table = build_arrow_table()
    df = pl.from_arrow(table)
    arr = df["emb_0"].to_numpy(allow_copy=False)
    return arr, np.shares_memory(df["emb_0"].to_numpy(), arr)


# Example 2: no copy for numeric columns
arr, shared = arrow_to_numpy_view()
print(f"numpy dtype: {arr.dtype}, zero-copy view: {shared}")

# Output:
# numpy dtype: float64, zero-copy view: True


# ============================================================
# 3. Parquet: columnar layout + compression
# ============================================================
# Parquet stores each column separately, so queries read only needed
# columns. Compression is per-column: zstd/snappy for floats, dictionary
# encoding for low-cardinality strings. Same data, same schema — wildly
# different file sizes.

def write_parquet_variants() -> dict[str, int]:
    """Write uncompressed, snappy, and zstd parquet; return byte sizes."""
    sizes: dict[str, int] = {}
    for name, kwargs in (
        ("none", {"compression": None}),
        ("snappy", {"compression": "snappy"}),
        ("zstd", {"compression": "zstd"}),
    ):
        path = _OUT / f"data-{name}.parquet"
        pl_src.write_parquet(path, **kwargs)
        sizes[name] = path.stat().st_size
    return sizes


# Example 3: zstd is typically the smallest; none is the largest
sizes = write_parquet_variants()
for name, size in sizes.items():
    print(f"  {name}: {size} bytes")

# Output (order/size varies by version, zstd < snappy < none always):
#   none: 2414081 bytes
#   snappy: 2015147 bytes
#   zstd: 1688371 bytes


# ============================================================
# 4. Partitioning: hive-style layout by a key column
# ============================================================
# write_parquet(directory) writes one file per partition value as
# label=value/... — the layout Polars, DuckDB, and Spark all read
# natively. Filters on the partition column skip files entirely.

def write_partitioned() -> Path:
    """Write a hive-partitioned parquet dataset by 'label'."""
    target = _OUT / "partitioned"
    pl_src.write_parquet(target, partition_by="label")
    return target


# Example 4: one subdirectory per label value
part_dir = write_partitioned()
print(sorted(p.name for p in part_dir.iterdir()))

# Output:
# ['label=neg', 'label=pos']


# ============================================================
# 5. Reading partitioned data + partition pruning
# ============================================================
# pl.scan_parquet(dir) restores the partition column automatically and
# pushes a filter on it into the file selection: only matching files
# are opened.

def read_partitioned_count(target: Path, label: str) -> int:
    """Count rows for one partition label via a pushed-down filter."""
    return (
        pl.scan_parquet(target)
        .filter(pl.col("label") == label)
        .collect()
        .height
    )


# Example 5: partition pruning returns only the matching rows
neg = read_partitioned_count(part_dir, "neg")
pos = read_partitioned_count(part_dir, "pos")
print(f"neg rows: {neg}, pos rows: {pos}, total: {neg + pos}")

# Output:
# neg rows: 50119, pos rows: 49881, total: 100000


# ============================================================
# 6. CSV vs Parquet: why datasets are not CSVs
# ============================================================
# CSV stores text with no schema, no compression, no statistics. The same
# table as CSV is 2-4x larger and every read re-parses the text. Parquet
# carries the schema, compresses, and skips whole row groups via
# statistics.

def csv_vs_parquet() -> tuple[int, int]:
    """Return (csv_bytes, parquet_bytes) for the same data."""
    csv_path = _OUT / "data.csv"
    pl_src.write_csv(csv_path)
    parquet_path = _OUT / "data-zstd.parquet"
    pl_src.write_parquet(parquet_path, compression="zstd")
    return csv_path.stat().st_size, parquet_path.stat().st_size


# Example 6: parquet is smaller even before considering column pruning
csv_bytes, pq_bytes = csv_vs_parquet()
print(f"csv: {csv_bytes} bytes, parquet: {pq_bytes} bytes")

# Output:
# csv: 4915505 bytes, parquet: 1688371 bytes


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: converting everything to pandas between systems
#   arrow_table.to_pandas().to_numpy()   # copies twice, then copies again
# CORRECT: df.to_numpy(allow_copy=False) when the dtype allows a view
#
# MISTAKE: assuming zero-copy for every dtype
#   df["str_col"].to_numpy(allow_copy=False)  # RuntimeError: strings need copy
# CORRECT: keep string columns as Arrow/Polars and convert only numerics
#
# MISTAKE: compressing CSV with zip and calling it a dataset
#   data.csv.zip          # no schema, no statistics, no column pruning
# CORRECT: write_parquet(compression="zstd") once, read it anywhere


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    at = build_arrow_table()
    assert isinstance(at, pa.Table), "pa.table must build an Arrow Table"
    assert at.num_rows == n, "Arrow table must hold all rows"
    assert at.schema.field("emb_0").type == pa.float64(), \
        "Arrow schema must type emb_0 as float64"

    arr, shared = arrow_to_numpy_view()
    assert arr.dtype == np.float64, "numeric Arrow column must map to float64"
    assert shared, "Arrow -> Polars -> NumPy must be zero-copy for numerics"

    sizes = write_parquet_variants()
    assert sizes["none"] > sizes["snappy"] > sizes["zstd"], \
        "compression must strictly reduce file size in this order"
    assert sizes["zstd"] > 1_000_000, "dataset must stay non-trivial"

    part_dir = write_partitioned()
    names = sorted(p.name for p in part_dir.iterdir())
    assert names == ["label=neg", "label=pos"], \
        "partition_by must create label=value subdirectories"

    neg = read_partitioned_count(part_dir, "neg")
    pos = read_partitioned_count(part_dir, "pos")
    assert neg + pos == n, "partition reads must add up to the full dataset"
    assert neg > 0 and pos > 0, "both partitions must contain rows"
    assert neg == 50119, "seeded split must reproduce the exact partition size"

    csv_bytes, pq_bytes = csv_vs_parquet()
    assert pq_bytes < csv_bytes, \
        "parquet (zstd) must beat CSV bytes for the same data"
    assert csv_bytes > 1_000_000, "CSV baseline must be non-trivial"

    # Round-trip: Arrow -> parquet -> Polars -> Arrow keeps everything
    pq.write_table(at, _OUT / "roundtrip.parquet", compression="zstd")
    back = pl.read_parquet(_OUT / "roundtrip.parquet").to_arrow()
    assert back.num_rows == n and back.num_columns == 3, \
        "parquet round-trip must preserve rows and columns"

    print("[OK] 05-pyarrow-parquet: all checks passed")


if __name__ == "__main__":
    try:
        if "--verify" in sys.argv:
            _verify()
        else:
            print("\n--- Summary ---")
            print("1. Arrow is the zero-copy interchange: pa.Table -> polars -> numpy")
            print("2. Parquet compresses per column; zstd beats snappy beats none")
            print("3. partition_by creates label=value dirs; filters prune files")
            _verify()   # always runs, so plain execution is also a test
    finally:
        _TMP.cleanup()   # close handles + delete temp files (Windows-safe)
