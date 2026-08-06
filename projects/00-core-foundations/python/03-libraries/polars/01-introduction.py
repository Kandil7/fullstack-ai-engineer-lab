"""
Polars — 01: Introduction
==========================
Topics: why Polars; the Arrow memory model; eager vs lazy execution.

Why this matters for AI/backend engineering:
    Feature pipelines start with tabular data, and tabular data starts with
    memory layout. Polars stores columns in Arrow format: contiguous,
    columnar, SIMD-friendly buffers that are shared zero-copy with pandas,
    DuckDB, PyTorch, and every Arrow-native tool. That shared layout is why
    a 50GB training corpus is loaded once and never converted — the same
    bytes are queried by Polars, trained on by PyTorch, and shipped as
    Parquet. This file builds the mental model before the API surface.

Run:      python 01-introduction.py
Verify:   python 01-introduction.py --verify
Reference: https://docs.pola.rs/user-guide/getting-started/
"""

from __future__ import annotations

import sys

try:
    import polars as pl
except ImportError:  # pragma: no cover - optional dependency
    print("[skip] polars not installed - install with: pip install polars")
    sys.exit(0)

# ============================================================
# 1. Creating a DataFrame: dict-of-columns is the native shape
# ============================================================
# A Polars DataFrame is built from *columns*, not rows. Each column is a
# Series: a typed Arrow buffer with a name. Columnar construction is the
# shape Arrow was designed for, so this is the fastest path in.

# Example 1: build a tiny feature table from dicts of columns.
# NOTE: we print to_dict()/rows() instead of the pretty table — the
# box-drawing characters in the table renderer break Windows cp1252
# consoles. The DATA is identical either way.
df = pl.DataFrame(
    {
        "sample_id": [1, 2, 3, 4],
        "embedding_dim": [384, 384, 384, 384],
        "score": [0.91, 0.44, 0.87, 0.12],
        "split": ["train", "train", "valid", "valid"],
    }
)
print(df.to_dict(as_series=False))
print(df.schema)

# Output:
# {'sample_id': [1, 2, 3, 4], 'embedding_dim': [384, 384, 384, 384],
#  'score': [0.91, 0.44, 0.87, 0.12], 'split': ['train', 'train', 'valid', 'valid']}
# Schema({'sample_id': Int64, 'embedding_dim': Int64, 'score': Float64, 'split': String})


# ============================================================
# 2. Schema: the typed contract of the table
# ============================================================
# df.schema is a dict {column: DataType}. Types are explicit and Arrow
# based (i64, f64, str, ...), NOT Python objects. Knowing the schema
# matters because downstream consumers (Parquet files, DuckDB, PyTorch
# tensors) all inherit these types.

def show_schema(frame: pl.DataFrame) -> dict[str, pl.DataType]:
    """Return the {column: dtype} schema of a DataFrame."""
    return dict(frame.schema)


# Example 2: inspect the schema via rows (ASCII-safe view of the table)
print(df.rows())

# Output:
# [(1, 384, 0.91, 'train'), (2, 384, 0.44, 'train'),
#  (3, 384, 0.87, 'valid'), (4, 384, 0.12, 'valid')]


# ============================================================
# 3. Arrow memory model: why columnar wins
# ============================================================
# Row-oriented storage keeps one record's fields together (CSV, JSON, most
# databases). Columnar storage keeps one field's values together (Arrow,
# Parquet). Columnar wins for analytics because a query touches whole
# columns: `score.mean()` reads one contiguous f64 buffer — cache-friendly,
# SIMD-vectorizable, and compressible (Parquet column statistics).
# Complexity: O(1) per column access; scans are O(n) but at memory speed.

# Example 3: columnar operation reads one buffer
mean_score = df["score"].mean()
print(f"mean score: {mean_score:.3f}")

# Output:
# mean score: 0.585


# ============================================================
# 4. Eager vs lazy: when does anything actually run?
# ============================================================
# Eager mode runs each call immediately (pandas-style). Lazy mode builds a
# query plan and runs it once at .collect(). Lazy is not "slower" — it lets
# the optimizer reorder work: filters before joins, projections before
# scans. The same expression syntax works in both modes.

def eager_pipeline(frame: pl.DataFrame) -> pl.DataFrame:
    """Eager: every call executes immediately."""
    filtered = frame.filter(pl.col("score") > 0.5)
    return filtered.with_columns((pl.col("score") * 100).alias("score_pct"))


def lazy_pipeline(frame: pl.DataFrame) -> pl.DataFrame:
    """Lazy: builds a plan; nothing runs until .collect()."""
    plan = frame.lazy().filter(pl.col("score") > 0.5).with_columns(
        (pl.col("score") * 100).alias("score_pct")
    )
    return plan.collect()


# Example 4: same result, two execution models
eager = eager_pipeline(df)
lazy = lazy_pipeline(df)
print(f"eager rows: {eager.height}, lazy rows: {lazy.height}")
print(f"same result: {eager.equals(lazy)}")

# Output:
# eager rows: 2, lazy rows: 2
# same result: True


# ============================================================
# 5. What a LazyFrame is: a plan, not data
# ============================================================
# frame.lazy() returns a LazyFrame: the query DAG. You can stack arbitrary
# transformations and inspect the plan with .explain() BEFORE running it.
# This is the core of Polars performance: the optimizer sees the whole
# pipeline, so it can push filters down to the file scan.

def describe_plan(frame: pl.DataFrame) -> str:
    """Return the optimized query plan as text."""
    return frame.lazy().filter(pl.col("score") > 0.5).explain(optimized=True)


# Example 5: the plan is inspectable without executing
plan_text = describe_plan(df)
print(f"plan mentions FILTER: {'FILTER' in plan_text}")
print(f"plan is inspectable: {len(plan_text) > 50}")

# Output:
# plan mentions FILTER: True
# plan is inspectable: True


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: expecting an index like pandas
#   df.iloc[2]                      # AttributeError - no positional index
# CORRECT:
#   df.row(2)                       # positional row access
#   df.filter(pl.col("id") == 2)    # declarative row selection
#
# MISTAKE: forgetting .collect() on a lazy plan
#   result = df.lazy().filter(...)  # LazyFrame, not data!
# CORRECT:
#   result = df.lazy().filter(...).collect()
#
# MISTAKE: assuming .apply()/Python loops are the fast path
#   df["score"].apply(lambda x: x * 2)   # slow: Python per element
# CORRECT:
#   df.with_columns((pl.col("score") * 2).alias("double"))  # vectorized


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    assert isinstance(df, pl.DataFrame), "pl.DataFrame must construct a DataFrame"
    assert df.shape == (4, 4), "dict-of-columns must build 4 rows x 4 cols"
    assert df.height == 4 and df.width == 4, "height/width must match the shape"

    schema = show_schema(df)
    assert schema["score"] == pl.Float64, "float literals must infer Float64"
    assert schema["split"] == pl.String, "string literals must infer String"
    assert schema["sample_id"] == pl.Int64, "int literals must infer Int64"

    assert abs(mean_score - 0.585) < 1e-9, "mean must be computed column-wise"
    assert df["score"].dtype == pl.Float64, "column access must return the dtype"

    eager = eager_pipeline(df)
    lazy = lazy_pipeline(df)
    assert eager.height == 2, "filter score > 0.5 keeps two rows"
    assert eager.equals(lazy), "eager and lazy pipelines must agree"
    assert "score_pct" in eager.columns, "with_columns must add the alias"
    assert abs(eager["score_pct"][0] - 91.0) < 1e-9, \
        "score_pct must be score * 100"

    plan = df.lazy().filter(pl.col("score") > 0.5).explain(optimized=True)
    assert "FILTER" in plan, "the plan must contain a FILTER node"
    assert isinstance(df.lazy(), pl.LazyFrame), \
        ".lazy() must return a LazyFrame, not data"

    print("[OK] 01-introduction: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. DataFrames are dict-of-columns; each column is a typed Series")
        print("2. Arrow is columnar: whole-column ops hit one contiguous buffer")
        print("3. Lazy builds a plan; collect() executes it once, optimized")
        _verify()   # always runs, so plain execution is also a test
