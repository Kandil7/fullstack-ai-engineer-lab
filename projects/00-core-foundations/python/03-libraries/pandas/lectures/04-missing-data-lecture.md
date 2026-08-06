# 03-libraries/pandas (advanced) — 04: Missing Data

## Topic Overview

Missing values are the most common form of dirty data — and the most
consequential, because their handling is a *modeling decision*. pandas
represents them as `NaN` (float) or `None`/`pd.NA`, and gives you the toolkit:
`isna()`/`notna()` to find them, `dropna()` to remove them, `fillna()` and
`interpolate()` to impute them.

For AI engineers the rule that separates juniors from seniors: **the choice of
missing-value strategy is an evaluation decision, not a cleanup detail.**
Imputing with the training-set mean, dropping rows, or flagging missingness as
a feature changes the model — and doing it after a train/test split (or on the
whole dataset) leaks information and inflates scores.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Detect missing values with `isna()`/`notna()` and count them
2. Drop rows/columns with `dropna(how=, thresh=, subset=)`
3. Fill with constants, forward/backward values, and means
4. Interpolate ordered data with `interpolate()`
5. Understand `NaN` vs `None` vs `pd.NA` semantics
6. Explain why imputation must happen per-fold inside CV
7. Use missingness itself as a feature (isna-based columns)

## Prerequisites

| Need | Where |
|------|-------|
| Selection and masks | `02-indexing-selection-lecture.md` |
| dtypes | `05-data-types-lecture.md` |
| train/test discipline | `07-machine-learning/10-train-test-lecture.md` |

## 1. Representing Missing: NaN, None, pd.NA

```python
import pandas as pd
import numpy as np

s = pd.Series([1.0, np.nan, 3.0, None])
print(s)
# 0    1.0
# 1    NaN
# 2    3.0
# 3    NaN
```

In a float column, both `np.nan` and `None` become `NaN`. `pd.NA` is the
type-aware missing sentinel for nullable dtypes (`Int64`, `string`) — it knows
its type and propagates through operations without the float-cast surprise.

## 2. Detecting and Counting

```python
df.isna()            # element-wise boolean frame
df.isna().sum()      # per-column counts
df.isna().mean()     # per-column fractions
df[df["score"].isna()]   # rows with missing score
```

`isna().mean()` is the decision input: 0.001 missing is noise (drop those
rows); 0.3 missing needs imputation strategy; 0.95 missing is a column that
should be deleted or turned into a flag.

## 3. Dropping — `dropna`

```python
df.dropna()                              # drop any row with ANY missing
df.dropna(how="all")                     # drop rows where ALL missing
df.dropna(subset=["score", "label"])     # require these columns complete
df.dropna(axis=1, thresh=int(0.8 * len(df)))  # keep cols with >=80% data
```

`thresh` is the production tool: "keep columns with at least N non-null" as a
data-quality gate at intake.

## 4. Filling — `fillna`

```python
df["score"].fillna(0.0)                      # constant
df["score"].fillna(df["score"].mean())       # mean imputation
df["prev"].fillna(method="ffill")            # forward fill (ordered data)
df["next"].fillna(method="bfill")            # backward fill
df["score"].fillna(df.groupby("split")["score"].transform("mean"))  # per-group mean
```

The per-group mean (by split, by category) preserves group structure — usually
better than a global mean. `method="ffill"` is the time-series default for
sensor/price gaps.

## 5. Interpolation — `interpolate`

```python
df["temp"].interpolate(method="linear")      # fill along the index
df["temp"].interpolate(method="time")        # time-weighted
df["temp"].interpolate(method="quadratic")   # curve-fitted
```

For ordered data (time series, sequences), interpolation is smarter than a
constant: it fits the local shape. Use `limit_direction="both"` to handle
leading/trailing gaps.

## 6. The Leakage Rule — Impute Inside the Split

```python
# WRONG — mean computed on the FULL dataset leaks test info into training
df["score"] = df["score"].fillna(df["score"].mean())
train, test = split(df)

# CORRECT — fit imputer on train only, apply to both
train_mean = train["score"].mean()
train["score"] = train["score"].fillna(train_mean)
test["score"] = test["score"].fillna(train_mean)
```

Any statistic used to fill missing values must come from the training rows
only. This is the same discipline as scaling before splitting (see
`07-machine-learning/09-scale`).

## 7. Missingness as a Feature

Sometimes *whether a value is missing* is itself predictive (a sensor that
went offline, a field only filled for a subpopulation). Encode it:

```python
df["score_missing"] = df["score"].isna().astype(int)
df["score"] = df["score"].fillna(0.0)
```

The flag lets the model learn the pattern of missingness instead of assuming
it is random (MCAR vs MNAR — missing not at random is a real signal).

## 8. Production Pattern — Declarative Cleaning

```python
def clean_missing(
    df: pd.DataFrame,
    *,
    drop_thresh: float = 0.8,
    fill_rules: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Drop sparse columns, then apply fill rules column by column."""
    out = df.copy()
    keep = out.columns[out.notna().mean() >= drop_thresh]
    out = out[keep]
    for col, strategy in (fill_rules or {}).items():
        if strategy == "zero":
            out[col] = out[col].fillna(0)
        elif strategy == "mean":
            out[col] = out[col].fillna(out[col].mean())
        elif strategy == "ffill":
            out[col] = out[col].ffill()
    return out
```

One function, reviewed once, applied everywhere: the missing-data policy lives
in code, not in ad-hoc notebooks.

## Common Mistakes to Avoid

### Mistake 1: Filling before the split

```python
# WRONG — mean imputation on all data leaks test into train
# CORRECT — fit imputation statistics on train only
```

### Mistake 2: `fillna(0)` on categorical-ish numeric

```python
# WRONG — 0 becomes a real, meaningful value the model trusts
df["income"].fillna(0)
# CORRECT — add an isna flag, or impute per group
```

### Mistake 3: Forgetting `pd.NA` vs NaN propagation

```python
# WRONG — int column with NaN silently becomes float
s = pd.Series([1, 2, None])    # dtype float64 — surprised?
# CORRECT — use Int64 nullable dtype if you must keep integers
s = pd.Series([1, 2, None], dtype="Int64")
```

### Mistake 4: `dropna()` on the wrong axis

```python
# WRONG — drops whole ROWS for one missing cell, wasting data
df.dropna()
# CORRECT — think: drop columns via axis=1 + thresh, rows via subset
```

## Best Practices

1. Start every pipeline with `isna().mean()` — know the missing map
2. Decide drop-vs-impute per column by missing fraction
3. Fit imputation statistics on train, apply to train/test/val
4. Use `thresh=` for column-level completeness gates
5. `ffill`/`interpolate` for ordered data; per-group means for categories
6. Encode missingness as a flag when it may be informative
7. Keep the policy in a named function, not scattered code

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `isna()` | O(n) | vectorized |
| `dropna()` | O(n) | copy of surviving rows |
| `fillna(constant)` | O(n) | in-place friendly |
| `fillna(mean)` | O(n) | mean computed in one pass |
| `ffill`/`bfill` | O(n) | order-dependent |
| `interpolate()` | O(n) | per-gap solve |
| groupby-mean impute | O(n) | transform pass |

**At scale:** all O(n) vectorized. The real cost is in the copies and in
choice quality: at 10M rows, imputing with a per-group mean vs a global mean
is a modeling decision worth evaluating, not a convenience.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| isna flags | modeling MNAR missingness in tabular data |
| per-split imputation | the leakage rule that keeps eval honest |
| `thresh=` gates | intake data-quality checks in MLOps pipelines |
| ffill/interpolate | sensor and log gaps in time-series features |
| groupby-mean | preserving group structure in imputation |

**Scale note:** in an automated retraining pipeline, missing-data policy runs
on every new batch. A policy that leaks (global mean before split) silently
inflates every reported metric — this is one of the top causes of
"great offline, bad online" models.

## Practice Exercises

### Exercise 1: Missing Map (Easy)
Build a function returning per-column missing fractions and the list of
columns above a 0.2 threshold.

### Exercise 2: Per-Split Imputation (Medium)
Split a frame, fit the train mean, apply to both splits, and assert the test
imputation used the TRAIN statistic (compare against a wrong global-mean
version).

### Exercise 3: Interpolation by Group (Hard)
For a time-series frame with a `sensor_id` column, forward-fill within each
sensor group (groupby + transform ffill) and assert no cross-sensor leakage.

## Summary

| Concept | Description |
|---------|-------------|
| NaN / None / pd.NA | missing sentinels with different semantics |
| `isna().mean()` | the missing map that drives decisions |
| `dropna` | row/column removal with `how`/`thresh`/`subset` |
| `fillna` | constant, ffill/bfill, mean, per-group mean |
| `interpolate` | order-aware filling for sequences |
| leakage rule | imputation statistics fit on train only |
| isna flags | missingness as a feature |

Missing data is not an accident to paper over — it is a modeling signal with a
policy. Decide it deliberately, encode it in code, and keep the evaluation
honest.

## Quick Reference

| Task | Idiom |
|------|-------|
| Missing map | `df.isna().mean()` |
| Rows with any missing | `df.dropna()` |
| Require columns complete | `df.dropna(subset=[...])` |
| Keep cols >= 80% | `df.dropna(axis=1, thresh=int(0.8*len(df)))` |
| Constant fill | `df["c"].fillna(0)` |
| Mean fill | `df["c"].fillna(df["c"].mean())` |
| Forward fill | `df["c"].ffill()` |
| Interpolate | `df["c"].interpolate(method="time")` |
| Missing flag | `df["c_miss"] = df["c"].isna().astype(int)` |

## Next Steps

Next: **[05-data-types](05-data-types-lecture.md)** — dtypes and conversion.
Continues in: **[07-machine-learning — 04 clean data](../../../../07-machine-learning/lectures/04-clean-data-lecture.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/missing_data.html
