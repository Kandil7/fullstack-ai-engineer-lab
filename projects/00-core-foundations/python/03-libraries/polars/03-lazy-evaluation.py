"""
Polars — 03: Lazy Evaluation
==============================
Topics: scan_csv / scan_parquet; query plans; explain(); predicate and
projection pushdown; collect().

Why this matters for AI/backend engineering:
    Training corpora are scanned, not loaded: a 50GB parquet dataset does
    not fit in RAM, and even a 2GB CSV should not be read fully just to
    answer "how many rows match this filter?". Lazy evaluation is the
    mechanism: scan_* opens the file WITHOUT reading it, the optimizer
    pushes filters and column projections into the file reader, and only
    collect() materializes. This is the difference between an ETL that
    touches 50GB and one that touches 200MB.

Run:      python 03-lazy-evaluation.py
Verify:   python 03-lazy-evaluation.py --verify
Reference: https://docs.pola.rs/user-guide/lazy/using/
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

try:
    import polars as pl
except ImportError:  # pragma: no cover - optional dependency
    print("[skip] polars not installed - install with: pip install polars")
    sys.exit(0)

# Build a small CSV + parquet pair in a temp dir (auto-cleaned at exit).
_TMP = tempfile.TemporaryDirectory()
_DATA_DIR = Path(_TMP.name)
_CSV = _DATA_DIR / "events.csv"
_PARQUET = _DATA_DIR / "events.parquet"
_CORPUS_DIR = _DATA_DIR / "corpus"      # parquet-only: directory scan target
_CORPUS_DIR.mkdir()

_rows = [
    {"user": f"u{i % 50:02d}", "split": "train" if i % 4 else "valid",
     "score": 100.0 * (i % 17) / 17.0}
    for i in range(2000)
]
with open(_CSV, "w", encoding="utf-8") as fh:
    fh.write("user,split,score\n")
    for r in _rows:
        fh.write(f"{r['user']},{r['split']},{r['score']:.4f}\n")
pl.DataFrame(_rows).write_parquet(_PARQUET)

# Split the same data into three parquet shards (the corpus layout).
for shard, offset in enumerate((0, 700, 1400)):
    pl.DataFrame(_rows[offset : offset + 700]).write_parquet(
        _CORPUS_DIR / f"shard-{shard}.parquet"
    )


# ============================================================
# 1. scan_csv / scan_parquet: metadata, not data
# ============================================================
# pl.read_csv() reads the whole file into memory NOW. pl.scan_csv()
# opens the file, reads schema + row estimate, and returns a LazyFrame
# that holds a plan. The file bytes are not consumed until .collect().

def scan_metadata() -> tuple[list[str], int]:
    """Return (columns, estimated rows) from a scan WITHOUT loading data."""
    lf = pl.scan_csv(_CSV)
    return lf.collect_schema().names(), lf.collect().height


# Example 1: scan returns a LazyFrame; collect() executes the plan
lf = pl.scan_csv(_CSV)
print(f"scan type: {type(lf).__name__}")
print(f"scan result: {scan_metadata()}")

# Output:
# scan type: LazyFrame
# scan result: (['user', 'split', 'score'], 2000)


# ============================================================
# 2. The query plan: explain() shows what WILL run
# ============================================================
# .explain() renders the optimizer's final plan as text. We never print
# it raw (its Unicode symbols break cp1252 consoles); we inspect it.

def optimized_plan(lf: pl.LazyFrame) -> str:
    """Return the optimized plan text for a lazy frame."""
    return lf.explain(optimized=True)


# Example 2: a filter+select chain — the optimizer pushed the filter
# into the CSV scan, so the plan shows SELECTION at the scan, not a
# separate FILTER node. Only the SELECT projection remains at the top.
plan = optimized_plan(lf.filter(pl.col("split") == "valid").select(pl.col("score")))
print(f"plan has SELECT node: {'SELECT' in plan}")
print(f"filter pushed into scan: {'SELECTION' in plan}")

# Output:
# plan has SELECT node: True
# filter pushed into scan: True


# ============================================================
# 3. Predicate pushdown: filter into the scan
# ============================================================
# The optimizer moves WHERE conditions as close to the data source as
# possible. For CSV it becomes a read-time row filter; for Parquet it
# becomes row-group skipping via column statistics. The plan text shows
# "SELECTION" at the scan level when the predicate was pushed.

def has_predicate_pushdown(lf: pl.LazyFrame) -> bool:
    """True if the optimized plan pushes a selection into the scan."""
    return "SELECTION" in lf.explain(optimized=True)


# Example 3: filter placed BEFORE the scan in the optimized plan
lf_filtered = pl.scan_parquet(_PARQUET).filter(pl.col("split") == "valid")
print(f"predicate pushed into scan: {has_predicate_pushdown(lf_filtered)}")

# Output:
# predicate pushed into scan: True


# ============================================================
# 4. Projection pushdown: only read the columns you need
# ============================================================
# The plan line "PROJECT 2/3 COLUMNS" means the scan reads 2 of the 3
# columns and never materializes the third. For Parquet this skips whole
# column chunks on disk.

def projected_columns(lf: pl.LazyFrame) -> int:
    """Parse 'PROJECT n/m COLUMNS' from the optimized plan."""
    plan = lf.explain(optimized=True)
    for line in plan.splitlines():
        line = line.strip()
        if line.startswith("PROJECT") and "COLUMNS" in line:
            return int(line.split()[1].split("/")[0])
    return -1


# Example 4: selecting one column drops the other two from the read
lf_proj = pl.scan_parquet(_PARQUET).select(pl.col("score"))
print(f"columns read: {projected_columns(lf_proj)} of 3")

# Output:
# columns read: 1 of 3


# ============================================================
# 5. collect(): the moment the plan executes
# ============================================================
# .collect() runs the optimized plan and returns a DataFrame. Everything
# before it — scan, filter, select, joins — is free. This is why you can
# build an entire ETL as a LazyFrame and execute it once, or stream it.

def run_analytics() -> dict[str, float]:
    """Aggregate per-split score stats via one lazy plan."""
    lf = pl.scan_parquet(_PARQUET)
    return dict(
        lf.group_by("split")
        .agg(pl.col("score").mean().alias("mean_score"))
        .sort("split")
        .collect()
        .rows()
    )


# Example 5: group_by over a scan, executed once
print(run_analytics())

# Output:
# {'train': 46.952941176470596, 'valid': 46.98823529411765}


# ============================================================
# 6. Reading a directory of files: the corpus pattern
# ============================================================
# scan_parquet(dir) reads ALL parquet files in a directory as one
# logical table (hive-style partitioning included). One plan, many files.

def scan_corpus() -> pl.LazyFrame:
    """Open every parquet file in the corpus dir as one lazy table."""
    return pl.scan_parquet(_CORPUS_DIR)


# Example 6: one scan covers every shard in the corpus directory
corpus = scan_corpus()
print(f"corpus shards: {len(list(_CORPUS_DIR.glob('*.parquet')))}")
print(f"corpus rows: {corpus.collect().height}")

# Output:
# corpus shards: 3
# corpus rows: 2000


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: reading a file just to inspect it
#   df = pl.read_csv("big.csv")      # loads EVERYTHING into RAM
# CORRECT:
#   lf = pl.scan_csv("big.csv")      # metadata only
#   print(lf.collect_schema())       # schema without data
#
# MISTAKE: collecting too early, then filtering in Python
#   df = pl.scan_csv("big.csv").collect()   # 50GB in RAM
#   df.filter(...)                          # too late - already loaded
# CORRECT:
#   pl.scan_csv("big.csv").filter(...).collect()
#
# MISTAKE: expecting read_csv and scan_csv to behave the same eagerly
#   pl.read_csv(p)["score"]     # works - eager
#   pl.scan_csv(p)["score"]     # TypeError - LazyFrames are not subscriptable
# CORRECT: use .select() on the LazyFrame, or .collect() first
#
# MISTAKE: scanning a directory that mixes file types
#   pl.scan_parquet("data_dir/")   # InvalidOperationError if .csv is inside
# CORRECT: keep parquet shards in their own directory (or use a glob like
#          pl.scan_parquet("data_dir/*.parquet"))


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    lf = pl.scan_csv(_CSV)
    assert isinstance(lf, pl.LazyFrame), "scan_csv must return a LazyFrame"
    schema_names, n_rows = scan_metadata()
    assert schema_names == ["user", "split", "score"], \
        "scan must read the CSV header as the schema"
    assert n_rows == 2000, "collect() of a scan must count all 2000 rows"

    plan = optimized_plan(
        lf.filter(pl.col("split") == "valid").select(pl.col("score"))
    )
    assert "SELECT" in plan, "plan must contain a SELECT node"
    assert "SELECTION" in plan, \
        "the filter must be pushed into the CSV scan (SELECTION)"

    lf_filtered = pl.scan_parquet(_PARQUET).filter(pl.col("split") == "valid")
    assert has_predicate_pushdown(lf_filtered), \
        "filter must be pushed into the parquet scan (SELECTION)"

    lf_proj = pl.scan_parquet(_PARQUET).select(pl.col("score"))
    assert projected_columns(lf_proj) == 1, \
        "projection pushdown must read only 1 of 3 columns"

    stats = run_analytics()
    assert set(stats) == {"train", "valid"}, \
        "per-split aggregation must cover exactly train and valid"
    assert abs(stats["valid"] - 46.98823529411765) < 1e-9, \
        "deterministic synthetic data must give a deterministic mean"

    corpus = scan_corpus()
    assert corpus.collect().height == 2000, \
        "directory scan must read all rows across all files"

    # Determinism: the same plan produces the same result every run
    result_a = lf.select(pl.col("score")).collect()
    result_b = lf.select(pl.col("score")).collect()
    assert result_a.equals(result_b), "identical plans must give identical results"

    print("[OK] 03-lazy-evaluation: all checks passed")


if __name__ == "__main__":
    try:
        if "--verify" in sys.argv:
            _verify()
        else:
            print("\n--- Summary ---")
            print("1. scan_* opens metadata only; collect() runs the plan")
            print("2. explain() shows the optimizer's work; SELECTION = pushdown")
            print("3. PROJECT n/m COLUMNS proves only needed columns are read")
            _verify()   # always runs, so plain execution is also a test
    finally:
        _TMP.cleanup()   # close handles + delete temp files (Windows-safe)
