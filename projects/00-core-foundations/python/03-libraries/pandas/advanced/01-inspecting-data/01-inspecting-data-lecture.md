# 03-libraries/pandas (advanced) — 01: Inspecting Data

## Topic Overview

Before any analysis, you must *see* the data: shape, column types, missing
counts, summary statistics, and sample rows. pandas gives you `df.head()`,
`df.info()`, `df.describe()`, `df.dtypes`, `df.shape`, and `df.nunique()` —
the first five commands of every data science session.

For AI engineers this is the intake check on every dataset: is the label column
the dtype you think? Is the feature numeric or categorical? How much is
missing? These answers decide the whole downstream pipeline — a `category`
column read as `object` silently becomes a model feature of 10,000 distinct
strings.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `df.head()`/`df.tail()` to sample rows
2. Read `df.shape` and `df.ndim`
3. Inspect dtypes with `df.dtypes` and `df.select_dtypes`
4. Read `df.info()` (memory usage, non-null counts)
5. Interpret `df.describe()` including `include=` options
6. Count unique values with `df.nunique()` and `value_counts()`
7. Detect missing data with `df.isna().sum()`
8. Build an intake checklist before modeling

## Prerequisites

| Need | Where |
|------|-------|
| DataFrame basics | `04-dataframes-lecture.md` (base series) |
| Series basics | `03-series-lecture.md` |
| NumPy dtypes | `03-libraries/numpy/lectures/06-data-types-lecture.md` |

## 1. Shape and Sample Rows

```python
import pandas as pd

df = pd.DataFrame({
    "sentence": ["the cat", "a dog", "the bird", "a fish"],
    "label": ["pos", "neg", "pos", "neg"],
    "score": [0.9, 0.1, 0.8, 0.2],
})

df.shape          # (4, 3) — rows, columns
df.head(2)        # first 2 rows
df.tail(1)        # last row
```

`shape` is the first sanity check: does this match your expectation from the
source (file line count, API count)? A wrong shape is the cheapest bug to
catch.

## 2. Dtypes — The Type Contract

```python
df.dtypes
# sentence    object
# label       object
# score      float64

df.select_dtypes(include=["number"])   # only numeric columns
df.select_dtypes(exclude=["object"])
```

The dtype tells you how pandas will treat the column. `object` columns are
strings (or mixed) — slow and un-vectorized; `category` compresses repeated
labels; `datetime64` enables time logic. **Converting early** (see
`05-data-types`) fixes the whole downstream.

## 3. `info()` — Non-Null Counts and Memory

```python
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 4 entries, 0 to 3
# Data columns (total 3 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   sentence  4 non-null      object
#  1   label     4 non-null      object
#  2   score     4 non-null      float64
# dtypes: float64(1), object(2)
# memory usage: 240+ bytes
```

`info()` answers three questions at once: how many rows, how many non-null per
column, and the memory footprint. The non-null count is your first missing-data
scan — a column that *should* be complete but isn't is a pipeline bug, not a
data quirk.

## 4. `describe()` — Summary Statistics

```python
df.describe()
#           score
# count  4.000000
# mean   0.500000
# std    0.408248
# min    0.100000
# 25%    0.175000
# 50%    0.500000
# 75%    0.825000
# max    0.900000
```

Numeric columns get count/mean/std/min/quartiles/max. Non-numeric columns are
skipped by default; include them explicitly:

```python
df.describe(include="object")   # count, unique, top, freq
```

Mean >> median flags skew; a max 10x the 75th percentile flags outliers. This
is the statistical intake exam for every feature.

## 5. `nunique()` and `value_counts()` — Cardinality

```python
df.nunique()          # unique values per column
df["label"].value_counts()
# neg    2
# pos    2

df["label"].value_counts(normalize=True)   # proportions
```

Cardinality decides encoding strategy: 2 values -> binary; <20 values ->
one-hot/category; 10,000 values -> embeddings or frequency features.
`value_counts(normalize=True)` reveals class balance — the first question for
any classifier (see imbalanced learning).

## 6. Missing Data Scan

```python
df.isna().sum()       # missing per column
df.isna().mean()      # missing fraction per column
```

`df.isna().mean()` is the better view: 0.01 vs 0.9 missing fraction call for
completely different strategies (drop vs impute vs model). A 90%-missing
column is usually a column that should not exist.

## 7. Production Pattern — The Intake Checklist

```python
def intake_report(df: pd.DataFrame) -> dict:
    """Five-number intake summary for any new dataset."""
    return {
        "shape": df.shape,
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isna().mean().to_dict(),
        "unique": df.nunique().to_dict(),
        "memory_mb": df.memory_usage(deep=True).sum() / 1e6,
    }
```

Run this on every new dataset before any modeling. It is the data-scientist
equivalent of a pilot's pre-flight checklist — cheap, fast, and it catches the
expensive mistakes early.

## Common Mistakes to Avoid

### Mistake 1: Trusting `head()` for completeness

```python
# WRONG — head() hides missing/odd tail rows
print(df.head())
# CORRECT — combine head, info, describe, isna().sum()
```

### Mistake 2: Forgetting `include=` in describe

```python
# WRONG — silently drops every categorical column
df.describe()
# CORRECT — see them too
df.describe(include="object")
```

### Mistake 3: Reading shape wrong

```python
# WRONG — transposed intuition (rows vs columns)
df.shape   # (4, 3) means 4 rows, 3 columns
```

### Mistake 4: Ignoring dtypes before modeling

```python
# WRONG — a "numeric-looking" object column breaks vectorized ops
df["score"].astype(float)   # later, painfully
# CORRECT — check dtypes at intake and convert once
```

## Best Practices

1. Always run `shape` first — cheapest correctness check
2. Inspect dtypes before any transformation
3. Use `info()` to see non-null counts and memory together
4. Read `describe()` for skew and outliers before modeling
5. Check `nunique()`/`value_counts()` to plan encodings
6. Compute `isna().mean()` for missing fractions, not just sums
7. Write an intake_report function and reuse it on every dataset

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `df.head(n)` | O(n) | n <= 10 typical |
| `df.shape` | O(1) | stored metadata |
| `df.dtypes` | O(1) | stored metadata |
| `df.info()` | O(columns) + memory scan | cheap |
| `df.describe()` | O(rows x cols) | single pass per column |
| `df.nunique()` | O(rows) per column | hashing |
| `df.isna().sum()` | O(rows x cols) | vectorized |

**At scale:** on a 10M-row frame these are all single vectorized passes —
cheap enough to run repeatedly. `memory_usage(deep=True)` is the one to watch:
object columns of Python strings cost ~50 bytes each, not 8.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| dtypes | label columns (int vs string) before training |
| `isna().mean()` | deciding drop-vs-impute on dataset features |
| `nunique()` | whether a column is an ID, a category, or a text feature |
| `describe()` | spotting outliers that break normalization |
| `info()` | memory budget for loading a dataset into RAM |
| `value_counts(normalize=True)` | class imbalance check before training |

**Scale note:** the intake report that takes 2 seconds on 100k rows takes 2
minutes on 10M rows and 20 minutes on 100M — profile it and cache the results
as metadata (see 08-mlops data validation).

## Practice Exercises

### Exercise 1: Intake Scan (Easy)
Build the `intake_report(df)` function and run it on a small frame with one
missing value, one object column, and one float column.

### Exercise 2: Cardinality Report (Medium)
For a frame of model predictions with columns `model`, `prediction`,
`confidence`, report unique counts, class balance of `prediction`, and
missing fraction of `confidence`.

### Exercise 3: Type-Contract Check (Hard)
Write `validate_intake(df, expected: dict)` that raises if a column's dtype
does not match the expected contract (e.g. `{"label": "category", "score":
"float64"}`), and reports the mismatches.

## Summary

| Concept | Description |
|---------|-------------|
| `shape` | rows x columns sanity check |
| `dtypes` | the type contract that drives every operation |
| `info()` | non-null counts + memory in one view |
| `describe()` | distribution summary, skew, outliers |
| `nunique()` / `value_counts()` | cardinality and class balance |
| `isna().mean()` | missing-fraction scan |
| intake report | the reusable pre-flight checklist |

Inspection is the first and cheapest step of every pipeline. A dataset you
understand at intake is a dataset you will not be surprised by later.

## Quick Reference

| Task | Idiom |
|------|-------|
| First rows | `df.head(n)` |
| Dtypes | `df.dtypes` |
| Non-null + memory | `df.info()` |
| Stats | `df.describe(include="all")` |
| Cardinality | `df.nunique()` |
| Class balance | `df["c"].value_counts(normalize=True)` |
| Missing fraction | `df.isna().mean()` |
| Memory | `df.memory_usage(deep=True)` |

## Next Steps

Next: **[02-indexing-selection](02-indexing-selection-lecture.md)** — loc, iloc, boolean masks.
Continues in: **[08-mlops — 10 data validation](../../../../08-mlops/lectures/10-data-validation-lecture.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/10min.html
