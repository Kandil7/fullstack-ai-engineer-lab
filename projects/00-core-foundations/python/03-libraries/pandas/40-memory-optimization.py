"""
Pandas -- 40: Memory Optimization
==============================================
Topics: dtype downcasting, category dtype for low-cardinality strings,
        memory_usage(deep=True), chunked read_csv, measured before/after

Why this matters for AI/backend engineering:
    A "small" DataFrame that fits in a Jupyter notebook can OOM a
    container or blow up your bill when it becomes a 200M-row feature
    table. Right-sizing dtypes is the cheapest optimization in the
    data stack: it is pure win -- same values, same query results,
    up to 90% less RAM, faster scans, better cache locality.

Run:      python 40-memory-optimization.py
Verify:   python 40-memory-optimization.py --verify
Reference: https://pandas.pydata.org/docs/user_guide/scale.html
"""

from __future__ import annotations

import io
import sys

import numpy as np
import pandas as pd

np.random.seed(42)

# ============================================================
# 1. Where the Memory Actually Goes
# ============================================================
# memory_usage() counts the raw dtype bytes per column.
# memory_usage(deep=True) also counts the objects BEHIND object
# columns -- for strings this is usually 50+ bytes per value, not 8.

# Example 1: object vs category vs numeric -- same "values"
n = 100_000
categories = np.array(["alpha", "beta", "gamma", "delta", "epsilon"])
obj_series = pd.Series(np.random.choice(categories, n))
cat_series = obj_series.astype("category")
num_series = pd.Series(np.random.randint(0, 100, n))

print("object  (100k strings):", obj_series.memory_usage(deep=True), "bytes")
print("category (same values):", cat_series.memory_usage(deep=True), "bytes")
print("int64  (100k integers):", num_series.memory_usage(deep=True), "bytes")

# Output (this environment; numpy picks int32 for randint on Windows):
# object  (100k strings): 5420424 bytes
# category (same values): 100575 bytes
# int64  (100k integers): 400132 bytes


# ============================================================
# 2. Downcasting Integers and Floats
# ============================================================
# pandas infers int64/float64 by default. If your data fits in a
# smaller range, downcasting is free: int8 .. int64, float32.

# Example 2: downcast ints and floats
ints = pd.Series(np.random.randint(0, 100, 100_000))
floats = pd.Series(np.random.uniform(0, 1, 100_000))

ints_small = pd.to_numeric(ints, downcast="integer")
floats_small = pd.to_numeric(floats, downcast="float")

print("int64 memory:", ints.memory_usage(deep=True),
      "-> downcast:", ints_small.memory_usage(deep=True),
      "dtype:", ints_small.dtype)
print("float64 memory:", floats.memory_usage(deep=True),
      "-> downcast:", floats_small.memory_usage(deep=True),
      "dtype:", floats_small.dtype)

# Output:
# int64 memory: 400132 -> downcast: 100132 dtype: int8
# float64 memory: 800132 -> downcast: 400132 dtype: float32


# ============================================================
# 3. The Category dtype -- When It Pays and When It Does Not
# ============================================================
# category stores each unique value once plus an int code per row.
# Payoff: few unique values, many rows. Break-even is roughly
# unique_count * len(value) ~ n * bytes_per_int_code. For high-
# cardinality columns (user_ids, timestamps) it is usually WORSE
# than object and much worse than a plain numeric column.

# Example 3: low cardinality -- category wins big
low_card = pd.Series(np.random.choice(categories, 100_000))
low_card_cat = low_card.astype("category")
savings = 1 - low_card_cat.memory_usage(deep=True) / low_card.memory_usage(deep=True)
print(f"Low cardinality savings: {savings:.1%}")

# Example 4: high cardinality -- category can lose
high_card = pd.Series([f"user_{i:06d}" for i in range(100_000)])
high_card_cat = high_card.astype("category")
print("High-card object:", high_card.memory_usage(deep=True),
      "| category:", high_card_cat.memory_usage(deep=True))

# Output:
# Low cardinality savings: 98.1%
# High-card object: 6000132 | category: 8513708


# ============================================================
# 4. Full-Frame Audit and Optimization
# ============================================================
# The production move: one audit pass over the whole DataFrame,
# then one optimization pass. Rows: int8/16/32/64 by range.
# Floats: float32 when precision allows. Strings: category when
# unique-count is a small fraction of rows.

# Example 5: build a wide, wasteful frame, then fix it
waste = pd.DataFrame({
    "user_id": np.random.randint(1, 50_000, 100_000),
    "score": np.random.uniform(0, 1, 100_000),
    "tier": np.random.choice(["free", "pro", "enterprise"], 100_000),
    "is_active": np.random.choice([True, False], 100_000),
    "region": np.random.choice(["us", "eu", "ap", "latam", "mea"], 100_000),
})

def audit(frame: pd.DataFrame) -> pd.Series:
    """Per-column memory usage, deep (objects counted)."""
    return frame.memory_usage(deep=True)

def optimize_dtypes(frame: pd.DataFrame) -> pd.DataFrame:
    """Right-size every column without changing its values."""
    out = frame.copy()
    for col in out.columns:
        col_type = out[col].dtype
        if pd.api.types.is_integer_dtype(col_type):
            out[col] = pd.to_numeric(out[col], downcast="integer")
        elif pd.api.types.is_float_dtype(col_type):
            out[col] = pd.to_numeric(out[col], downcast="float")
        elif pd.api.types.is_bool_dtype(col_type):
            continue  # bool is already 1 byte
        elif pd.api.types.is_object_dtype(col_type):
            n_unique = out[col].nunique()
            if n_unique / len(out) < 0.1:      # low cardinality heuristic
                out[col] = out[col].astype("category")
    return out

before = audit(waste).sum()
fixed = optimize_dtypes(waste)
after = audit(fixed).sum()
print("Before:", before, "bytes | After:", after,
      "bytes | Saved:", f"{1 - after / before:.1%}")
print("user_id dtype:", fixed["user_id"].dtype,
      "| score dtype:", fixed["score"].dtype,
      "| tier dtype:", fixed["tier"].dtype,
      "| is_active dtype:", fixed["is_active"].dtype,
      "| region dtype:", fixed["region"].dtype)

# Output:
# Before: 11946390 bytes | After: 1100835 bytes | Saved: 90.8%
# user_id dtype: int32 | score dtype: float32 | tier dtype: category | is_active dtype: bool | region dtype: category


# ============================================================
# 5. Values Are Untouched -- Verify Before/After
# ============================================================
# Integers, booleans, and categories survive exactly. Floats downcast
# to float32 round at ~1e-7 -- usually fine for ML features, never
# fine for money or exact IDs. Always verify per column, with the
# tolerance the USE CASE demands.

# Example 6: per-column equality after optimization
# Note: compare VALUES, not dtypes -- Series.equals() is False whenever
# dtypes differ (object vs category), even with identical values.
for col in waste.columns:
    if waste[col].dtype == np.float64 and fixed[col].dtype == np.float32:
        max_rounding = float(np.abs(waste[col] - fixed[col]).max())
        print(f"{col}: exact values={bool((waste[col] == fixed[col]).all())} "
              f"| allclose={np.allclose(waste[col], fixed[col], atol=1e-6)} "
              f"| max rounding {max_rounding:.2e}")
    else:
        print(f"{col}: exact values={bool((waste[col] == fixed[col]).all())}")

# Output:
# user_id: exact values=True
# score: exact values=False | allclose=True | max rounding 2.98e-08
# tier: exact values=True
# is_active: exact values=True
# region: exact values=True


# ============================================================
# 6. Chunked Reads -- When the File Is Bigger Than RAM
# ============================================================
# read_csv(..., chunksize=K) returns an iterator of K-row frames.
# Stream the file, aggregate per chunk, then combine -- peak memory
# stays bounded by the chunk size, not the file size.

# Example 7: build a CSV and read it in chunks
csv_text = pd.DataFrame({
    "x": np.arange(1000),
    "y": np.random.randn(1000).round(3),
}).to_csv(index=False)

full = pd.read_csv(io.StringIO(csv_text))
chunked = pd.concat(
    pd.read_csv(io.StringIO(csv_text), chunksize=250),
    ignore_index=True,
)
print("Chunked read equals full read:", full.equals(chunked))

# Example 8: streamed aggregation -- same result, bounded memory
def streamed_mean(text: str, col: str, chunksize: int) -> float:
    """Mean of a column without ever loading the whole file."""
    total = 0.0
    count = 0
    for chunk in pd.read_csv(io.StringIO(text), chunksize=chunksize):
        total += float(chunk[col].sum())
        count += int(chunk[col].count())
    return total / count

print("Full mean:", round(float(full["y"].mean()), 6),
      "| Streamed mean:", round(streamed_mean(csv_text, "y", 250), 6))

# Output:
# Chunked read equals full read: True
# Full mean: 0.024382 | Streamed mean: 0.024382


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: trusting memory_usage() without deep=True for strings
#   df.memory_usage().sum()      # counts 8-byte pointers, hides the
#                                # actual string bytes
# CORRECT:
#   df.memory_usage(deep=True).sum()
#
# MISTAKE: converting high-cardinality strings to category
#   df["user_id"].astype("category")   # often MORE memory, slower ops
# CORRECT:
#   df["user_id"].astype("category") only when nunique()/len < ~0.1
#
# MISTAKE: downcasting without verifying values
#   pd.to_numeric(col, downcast="float")  # float32 can round
# CORRECT: assert (col - downcast(col)).abs().max() is tiny, or keep 64-bit
#   when exactness matters (money, ids > 2^53)


# ============================================================
# Self-Verification  (MANDATORY)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # Category uses dramatically less memory for low-cardinality strings.
    assert cat_series.memory_usage(deep=True) < obj_series.memory_usage(deep=True), \
        "category must be smaller than object for low cardinality"
    assert savings > 0.5, "low-cardinality category must save >50%"

    # Downcasting actually shrinks the memory footprint.
    assert ints_small.memory_usage(deep=True) < ints.memory_usage(deep=True), \
        "int downcast must reduce memory"
    assert floats_small.memory_usage(deep=True) < floats.memory_usage(deep=True), \
        "float downcast must reduce memory"
    assert floats_small.dtype == np.dtype("float32"), "float must land on float32"

    # The optimized frame is strictly smaller than the original.
    assert after < before, "optimization must reduce total memory"

    # Integers, booleans, and categories must survive byte-for-byte.
    assert bool((waste["user_id"] == fixed["user_id"]).all()), \
        "int downcast must preserve integer values exactly"
    assert bool((waste["tier"] == fixed["tier"]).all()), \
        "category conversion must preserve string values exactly"
    assert bool((waste["is_active"] == fixed["is_active"]).all()), \
        "bool column must be untouched"
    assert bool((waste["region"] == fixed["region"]).all()), \
        "region category must preserve values"

    # Floats round at float32 precision -- allowed within tolerance.
    assert np.allclose(waste["score"], fixed["score"], atol=1e-6), \
        "float32 downcast must stay within 1e-6"
    assert not waste["score"].equals(fixed["score"]), \
        "float64->float32 must round (the precision cost must exist)"

    # The user_id column (50k unique, int range) must be downcast to int32.
    assert fixed["user_id"].dtype == np.dtype("int32"), \
        "user_id range fits in int32"

    # Low-cardinality strings must become categorical.
    assert str(fixed["tier"].dtype) == "category", \
        "tier must be optimized to category"
    assert str(fixed["region"].dtype) == "category", \
        "region must be optimized to category"

    # Chunked reading and streamed aggregation equal the full-frame results.
    assert full.equals(chunked), "chunked concat must equal full read"
    assert abs(streamed_mean(csv_text, "y", 250)
               - float(full["y"].mean())) < 1e-9, \
        "streamed mean must equal full mean"

    print("[OK] 40-memory-optimization: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. deep=True is the only honest memory count.")
        print("2. Downcast ints/floats + categorize low-cardinality strings.")
        print("3. Chunked reads bound peak memory for huge files.")
        _verify()          # always runs, so plain execution is also a test
