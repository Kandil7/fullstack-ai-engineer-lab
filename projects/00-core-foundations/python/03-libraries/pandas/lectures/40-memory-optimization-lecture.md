# 03-libraries/pandas — 40: Memory Optimization

## Topic Overview

Memory optimization in pandas means choosing dtypes and access patterns so the
same data uses less RAM and scans faster: downcasting integers and floats,
converting low-cardinality strings to `category`, measuring honestly with
`memory_usage(deep=True)`, and reading files in chunks when they exceed RAM.
No values change — only the bytes behind them.

For AI engineers this is the difference between a feature table that fits in
the training container and one that OOMs it or costs three times as much in
cloud memory. A 200M-row user-feature table at 90 bytes/row is 18 GB; the same
table optimized is under 2 GB — and every GB of RAM in a data pipeline has a
price and a failure mode. This lecture covers the optimization pass you can
run on any DataFrame in ten minutes, and the verification discipline that
keeps it honest.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Measure real per-column memory with `memory_usage(deep=True)`
2. Downcast integer and float columns with `pd.to_numeric`
3. Decide when `category` wins — and when it loses
4. Run a full-frame audit-and-optimize pass
5. Verify values survive optimization (int/bool/category exact; float32 rounds)
6. Read files in chunks to bound peak memory
7. Stream an aggregation without loading the whole file

## Prerequisites

| Need | Where |
|------|-------|
| dtypes | `05-data-types-lecture.md` |
| `astype` / `to_numeric` | `05-data-types-lecture.md` |
| I/O basics | `14-io-csv-json-lecture.md` |

## 1. Measuring Honestly — `deep=True`

Plain `memory_usage()` counts the dtype bytes: 8 bytes per int64/float64 cell.
But an `object` column holds *pointers* to Python strings that live
elsewhere — each string payload is 50+ bytes of its own. `deep=True` walks
the objects and counts the truth.

```python
import numpy as np
import pandas as pd

np.random.seed(42)
n = 100_000
cats = np.array(["alpha", "beta", "gamma", "delta", "epsilon"])

obj = pd.Series(np.random.choice(cats, n))
cat = obj.astype("category")
nums = pd.Series(np.random.randint(0, 100, n))

print("object (100k strings):", obj.memory_usage(deep=True))
print("category (same values):", cat.memory_usage(deep=True))
print("int (100k ints):", nums.memory_usage(deep=True))
```

```text
object (100k strings): 5420424
category (same values): 100575
int (100k ints): 400132
```

The object column costs ~5.4 MB; the categorical version of the *same*
values costs ~0.1 MB. The rule: `memory_usage()` without `deep=True` is a
lie for any column with strings.

## 2. Downcasting Numerics

pandas infers int64/float64 by default — the safest, not the smallest.
If your range fits in a smaller width, downcasting is free.

```python
ints = pd.Series(np.random.randint(0, 100, 100_000))
floats = pd.Series(np.random.uniform(0, 1, 100_000))

ints_small = pd.to_numeric(ints, downcast="integer")
floats_small = pd.to_numeric(floats, downcast="float")

print(ints.memory_usage(deep=True), "->", ints_small.memory_usage(deep=True),
      ints_small.dtype)                    # 400132 -> 100132 int8
print(floats.memory_usage(deep=True), "->", floats_small.memory_usage(deep=True),
      floats_small.dtype)                  # 800132 -> 400132 float32
```

```text
400132 -> 100132 int8
800132 -> 400132 float32
```

`downcast="integer"` picks the smallest int type that holds the data
(int8/int16/int32/int64); `downcast="float"` lands on float32 (there is no
smaller float in numpy). Note the numbers above are for numpy int32 inputs on
Windows — the dtype outcomes are what matter, and they are deterministic.

## 3. `category` — When It Pays and When It Does Not

`category` stores each unique value once plus a small integer code per row.
Payoff condition: **few unique values, many rows**. Break-even is roughly
`unique_count * string_len ~ rows * bytes_per_code`. High-cardinality
columns — user_ids, timestamps, free text — lose or tie.

```python
low_card = pd.Series(np.random.choice(cats, 100_000)).astype("category")
print(1 - low_card.memory_usage(deep=True) / obj.memory_usage(deep=True))   # ~98%

high_card = pd.Series([f"user_{i:06d}" for i in range(100_000)])
high_cat = high_card.astype("category")
print(high_card.memory_usage(deep=True), high_cat.memory_usage(deep=True))
# 6000132 8513708  <- category LOSES on high cardinality
```

```text
0.981...
6000132 8513708
```

The heuristic used in production: convert to `category` when
`nunique() / len(frame) < 0.1` — and verify with `memory_usage` anyway.

## 4. The Full-Frame Optimization Pass

A generic pass: iterate columns, downcast numerics, categorize low-cardinality
strings, leave booleans alone.

```python
def audit(frame: pd.DataFrame) -> pd.Series:
    return frame.memory_usage(deep=True)

def optimize_dtypes(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    for col in out.columns:
        t = out[col].dtype
        if pd.api.types.is_integer_dtype(t):
            out[col] = pd.to_numeric(out[col], downcast="integer")
        elif pd.api.types.is_float_dtype(t):
            out[col] = pd.to_numeric(out[col], downcast="float")
        elif pd.api.types.is_bool_dtype(t):
            continue
        elif pd.api.types.is_object_dtype(t):
            if out[col].nunique() / len(out) < 0.1:
                out[col] = out[col].astype("category")
    return out

waste = pd.DataFrame({
    "user_id": np.random.randint(1, 50_000, 100_000),
    "score": np.random.uniform(0, 1, 100_000),
    "tier": np.random.choice(["free", "pro", "enterprise"], 100_000),
    "is_active": np.random.choice([True, False], 100_000),
    "region": np.random.choice(["us", "eu", "ap", "latam", "mea"], 100_000),
})
fixed = optimize_dtypes(waste)
print(audit(waste).sum(), "->", audit(fixed).sum())
# 11946390 -> 1100835
```

```text
11946390 -> 1100835
```

One function, ten minutes of work, ~91% savings — and every value intact.

## 5. Verification — the Float32 Catch

Integers, booleans, and categories survive exactly. Floats downcast to
float32 round at ~1e-7 relative. Usually fine for ML features; never fine
for money or IDs. Verify per column with the tolerance the use case demands.

```python
for col in waste.columns:
    if waste[col].dtype == np.float64 and fixed[col].dtype == np.float32:
        print(col, np.abs(waste[col] - fixed[col]).max())
    else:
        print(col, (waste[col] == fixed[col]).all())
```

```text
user_id True
score 2.98e-08
tier True
is_active True
region True
```

Note: compare **values**, not `.equals()` — `.equals()` returns False when
dtypes differ (object vs category) even with identical values.

## 6. Chunked Reads — Bigger Files Than RAM

`read_csv(..., chunksize=K)` returns an iterator of K-row frames. Stream the
file, aggregate per chunk, combine — peak memory is bounded by the chunk,
not the file.

```python
import io

text = pd.DataFrame({"x": np.arange(1000),
                     "y": np.random.randn(1000)}).to_csv(index=False)

full = pd.read_csv(io.StringIO(text))
chunked = pd.concat(pd.read_csv(io.StringIO(text), chunksize=250),
                    ignore_index=True)
print(full.equals(chunked))                     # True

def streamed_mean(csv_text: str, col: str, cs: int) -> float:
    total = count = 0.0
    for chunk in pd.read_csv(io.StringIO(csv_text), chunksize=cs):
        total += chunk[col].sum()
        count += chunk[col].count()
    return total / count

print(full["y"].mean() == streamed_mean(text, "y", 250))   # True
```

```text
True
True
```

The streamed mean is exact (sums are associative in floating point order —
for production, prefer `float64` accumulation or `kahan` if you care).

## Common Mistakes to Avoid

### Mistake 1: trusting `memory_usage()` without `deep=True`

```python
# WRONG — 8 bytes per pointer; hides string payloads
df.memory_usage().sum()
# CORRECT — counts object internals
df.memory_usage(deep=True).sum()
```

### Mistake 2: categorizing high-cardinality strings

```python
# WRONG — 100k unique user_ids: category is BIGGER and slower
df["user_id"].astype("category")
# CORRECT — category only when nunique()/len < ~0.1
if df["col"].nunique() / len(df) < 0.1:
    df["col"] = df["col"].astype("category")
```

### Mistake 3: downcasting floats without checking precision

```python
# WRONG — money in float32 rounds at ~1e-7 * magnitude
df["price"].astype("float32")
# CORRECT — keep 64-bit for exactness-critical columns
# (or use Decimal / integer cents)
```

### Mistake 4: loading a huge file "just to look"

```python
# WRONG — 10 GB CSV into RAM to compute one mean
df = pd.read_csv("huge.csv")
df["y"].mean()
# CORRECT — stream it
for chunk in pd.read_csv("huge.csv", chunksize=100_000):
    ...
```

## Best Practices

1. Audit with `memory_usage(deep=True)` before and after every change
2. Downcast ints/floats with `pd.to_numeric(..., downcast=...)`
3. Convert to `category` only below ~10% cardinality
4. Verify values after every dtype pass — with the tolerance the domain allows
5. Keep money/exact IDs in 64-bit (or integer cents)
6. Stream files bigger than a quarter of RAM with `chunksize`
7. One `optimize_dtypes` function for the whole pipeline, reviewed once
8. Document the memory budget per table; flag regressions in review

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|-----------|------|-------|---------------------|
| `memory_usage()` | O(n) | O(1) | — |
| `memory_usage(deep=True)` | O(n) | O(n) walk | — |
| `pd.to_numeric(downcast=...)` | O(n) | O(n) temp | in-place `astype` after range check |
| `astype("category")` | O(n) | O(unique) | only when cardinality is low |
| `read_csv(chunksize=K)` | O(n) total | O(K) peak | always for huge files |
| full load of a 10 GB file | O(n) | O(n) | chunked read — O(K) peak |

**At scale:** RAM is the first thing that breaks in a data pipeline. The
optimization pass above is deterministic, reviewed once, and reusable; the
chunked-read pattern is what keeps a 500 GB CSV processable on one box.

## AI Engineering Relevance

**Where this shows up:** feature-store tables, training data loaders, batch
ETL — anywhere a DataFrame must fit in a worker's memory budget.

| Concept here | Used for |
|--------------|----------|
| `deep=True` audit | knowing the true cost before requesting cluster memory |
| category dtype | compressed categorical features (plan, region, country) |
| int/float downcast | 2-4x cheaper numeric feature matrices |
| chunked read | training on files larger than the loader's RAM |
| float32 policy | halving feature-matrix memory where precision allows |

**Scale note:** a 1M-row notebook frame needs no optimization; a 200M-row
training snapshot does. The same `optimize_dtypes` that saves 91% at 1M rows
saves the same fraction at 200M — the absolute GBs are what change the bill.

## Practice Exercises

### Exercise 1: Audit a Wasteful Frame (Easy)
Build a 50k-row frame with an int, a float, a low-card string, and a
high-card string column. Report `memory_usage(deep=True)` per column.

### Exercise 2: Downcast Correctly (Medium)
For a column of `np.random.randint(0, 1_000_000, 100_000)`, downcast and
verify the dtype is int32; for `randint(0, 127)` verify int8. Confirm values
are unchanged.

### Exercise 3: Category Decision (Medium)
Given a column with 5 categories and one with 50k unique values out of 100k
rows, decide conversion per the 10% heuristic and verify the memory result
matches the decision.

### Exercise 4: Streamed Aggregation (Hard)
Write a `streamed_mean` and a `streamed_median` (hint: you cannot stream a
median exactly — collect per-chunk quantiles and discuss the trade-off) for a
CSV built in memory, and verify against the full-frame result.

## Summary

| Concept | Description |
|---------|-------------|
| `memory_usage(deep=True)` | the only honest measurement |
| downcast | smallest int/float dtype that holds the data |
| `category` | compressed repeated labels; wins below ~10% cardinality |
| optimization pass | one reviewed function, applied pipeline-wide |
| float32 rounding | ~1e-7 relative; decide per column |
| chunked read | O(K) peak memory for arbitrarily large files |

Memory optimization is the cheapest performance work in the data stack: same
values, same results, 50-90% less RAM. Measure honestly, right-size dtypes,
verify values — and your feature tables stop being the thing that OOMs the
training job.

## Quick Reference

| Task | Idiom |
|------|-------|
| True memory | `df.memory_usage(deep=True)` |
| Downcast ints | `pd.to_numeric(s, downcast="integer")` |
| Downcast floats | `pd.to_numeric(s, downcast="float")` |
| Low-card → category | `s.astype("category")` if `s.nunique()/len(s) < 0.1` |
| Full pass | `optimize_dtypes(df)` (copy, per-column downcast/categorize) |
| Chunked read | `pd.read_csv(f, chunksize=100_000)` |
| Streamed mean | accumulate `sum`/`count` per chunk |

## Next Steps

Next: **[41 — Advanced Time Series](41-timeseries-advanced-lecture.md)** —
DatetimeIndex, resampling, and no-leakage rolling features.
Continues in: **[40 — Memory Optimization challenge](../challenges/40-memory-optimization/README.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/scale.html
