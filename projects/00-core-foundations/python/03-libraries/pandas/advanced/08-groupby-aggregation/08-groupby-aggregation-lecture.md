# 03-libraries/pandas (advanced) — 08: GroupBy & Aggregation

## Topic Overview

GroupBy is pandas' split-apply-combine: split rows by key, apply a function
to each group, combine the results. The three verbs — `groupby(...).agg()`,
`.transform()`, and `.filter()` — cover statistics, per-row aligned outputs,
and group-level selection.

For AI engineers, groupby is the segmentation engine of analytics: metrics by
model version, latency by region, engagement by user cohort. `transform` is
the one that matters most for features — it produces per-group statistics
*aligned to the original rows*, which is exactly what feature engineering
needs.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Group by one or multiple keys
2. Aggregate with `.agg()` (named and multiple aggregations)
3. Use `.transform()` for row-aligned group statistics
4. Use `.filter()` for group-level row selection
5. Use `groupby` with `apply` and know when it is warranted
6. Handle the groupby object's index vs original index
7. Build grouped features without leakage

## Prerequisites

| Need | Where |
|------|-------|
| Selection | `02-indexing-selection-lecture.md` |
| Missing data | `04-missing-data-lecture.md` |
| Aggregations | `07-datetime-lecture.md` (resample) |

## 1. The Split-Apply-Combine Shape

```python
import pandas as pd

df = pd.DataFrame({
    "model": ["a", "b", "a", "b"],
    "split": ["train", "train", "val", "val"],
    "f1": [0.81, 0.79, 0.83, 0.80],
})

df.groupby("model")["f1"].mean()
# model
# a    0.82
# b    0.795
```

The group key becomes the index; the grouped column is aggregated. `as_index=False`
keeps the key as a column — usually what you want for further use.

## 2. `.agg()` — One or Many Aggregations

```python
df.groupby("model", as_index=False)["f1"].agg(["mean", "std", "count"])

# Named aggregations (multiple columns, multiple functions)
df.groupby("model", as_index=False).agg(
    f1_mean=("f1", "mean"),
    f1_max=("f1", "max"),
)
```

`.agg` accepts a list of functions, a dict of column->function, or the named
`(column, function)` tuple syntax — the production form with readable output
columns.

## 3. `.transform()` — Row-Aligned Group Statistics

```python
# Per-group mean, broadcast back to the ORIGINAL rows
df["f1_group_mean"] = df.groupby("model")["f1"].transform("mean")

# Per-group z-score (the standard grouped feature)
df["f1_z"] = df.groupby("model")["f1"].transform(lambda x: (x - x.mean()) / x.std())
```

`transform` keeps the original index — each row gets its group's statistic.
This is the mechanism for group-mean imputation (topic 04) and for
group-normalized features. The leakage rule applies: compute from train rows
only, then apply.

## 4. `.filter()` — Group-Level Selection

```python
# Keep only groups with >= 3 rows (drop tiny cohorts)
df.groupby("model").filter(lambda g: len(g) >= 3)

# Keep groups whose mean passes a threshold
df.groupby("model").filter(lambda g: g["f1"].mean() > 0.8)
```

`.filter` drops *whole groups* based on a predicate on the group — different
from row masks. Use it for minimum-cohort gates and group-quality rules.

## 5. Multiple Keys — The Grouping Tuple

```python
df.groupby(["model", "split"], as_index=False).agg(
    f1_mean=("f1", "mean"),
    count=("f1", "count"),
)
```

Multiple keys form a tuple grouping; `as_index=False` keeps both keys as
columns. This is the standard metrics-by-model-and-split report shape.

## 6. `.apply()` — The Escape Hatch (Use Sparingly)

```python
df.groupby("model")["f1"].apply(lambda s: s.max() - s.min())
```

`.apply` passes whole groups to a function and is powerful but slow and
surprising (it can reshape). Prefer `agg`/`transform`; reach for `apply` only
for computations the verbs cannot express — and never for simple stats.

## 7. Production Pattern — Grouped Feature Builder

```python
def add_group_features(
    df: pd.DataFrame,
    key: str,
    value: str,
    stats: tuple[str, ...] = ("mean", "std"),
) -> pd.DataFrame:
    """Attach per-group stats as new row-aligned columns."""
    out = df.copy()
    for stat in stats:
        out[f"{value}_{stat}_by_{key}"] = (
            df.groupby(key)[value].transform(stat)
        )
    return out
```

Grouped features with explicit names (`f1_mean_by_model`) — reviewable,
reusable, and applied identically at train and serve time.

## Common Mistakes to Avoid

### Mistake 1: Forgetting `as_index=False`

```python
# WRONG — group key buried in the index, join surprises later
g = df.groupby("model")["f1"].mean()
# CORRECT — keep the key as a column
g = df.groupby("model", as_index=False)["f1"].mean()
```

### Mistake 2: transform vs agg confusion

```python
# WRONG — agg collapses rows; you lose the original frame alignment
df["m"] = df.groupby("model")["f1"].agg("mean")
# CORRECT — transform broadcasts back to every row
df["m"] = df.groupby("model")["f1"].transform("mean")
```

### Mistake 3: Grouped statistics leaking across splits

```python
# WRONG — group mean computed on train+test together
# CORRECT — fit group stats on train, apply to test with the same mapping
```

### Mistake 4: `apply` for simple statistics

```python
# WRONG — apply is ~10-100x slower than the verbs
df.groupby("m")["x"].apply(np.mean)
# CORRECT
df.groupby("m")["x"].mean()
```

## Best Practices

1. `as_index=False` when the result feeds further joins/plots
2. `agg` with named `(col, func)` tuples for readable output
3. `transform` for row-aligned group features
4. `.filter` for group-level gates (min cohort, quality thresholds)
5. Fit grouped statistics on train only, apply to test/serve
6. Prefer agg/transform over apply; apply only for exotic shapes

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `groupby(...)` | O(n) | hashing pass |
| `.agg` | O(n) per function | vectorized |
| `.transform` | O(n) per stat | aligned output |
| `.filter` | O(n x groups) | predicate per group |
| `.apply` | O(groups x group work) | Python-level, slow |

**At scale:** agg/transform are near-linear and vectorized — fine at 10M rows.
`.apply` runs Python per group; at 1M groups it is the bottleneck. Reshape
the computation into verbs whenever possible.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| grouped metrics | model/version/region performance reports |
| transform features | per-user or per-item normalized features |
| group-mean impute | missing-value filling within cohorts |
| `.filter` | dropping under-sampled classes/cohorts |
| multiple keys | metrics by model x split x region |
| leak discipline | group stats fit on train only |

**Scale note:** grouped features are everywhere in tabular ML — and the number
one place group leakage hides is the "compute the group mean on the full
frame before splitting" pattern. Same rule as scaling and imputation.

## Practice Exercises

### Exercise 1: Metrics Report (Easy)
Group by `model`, aggregate `f1` with mean/std/count, `as_index=False`.

### Exercise 2: Grouped Z-Score (Medium)
Add `f1_z_by_model` via transform and verify per-group mean ~0 and std ~1.

### Exercise 3: Cohort Gate (Hard)
Filter to models with at least 5 rows and mean f1 > 0.8; report how many
groups were dropped.

## Summary

| Concept | Description |
|---------|-------------|
| split-apply-combine | group -> function -> combine |
| `.agg` | named, multi-function aggregation |
| `.transform` | row-aligned group statistics (features) |
| `.filter` | group-level row selection |
| multiple keys | grouping tuples |
| `.apply` | slow escape hatch — use sparingly |
| leakage | group stats fit on train only |

GroupBy turns a flat frame into segmented insights — and into the feature
columns that power tabular models. Choose the verb by what you need: collapsed
(`agg`), aligned (`transform`), or gated (`filter`).

## Quick Reference

| Task | Idiom |
|------|-------|
| Mean per group | `df.groupby("k")["v"].mean()` |
| Keep key as column | `df.groupby("k", as_index=False)` |
| Named aggs | `.agg(m=("v", "mean"), n=("v", "count"))` |
| Row-aligned stat | `df["m"] = df.groupby("k")["v"].transform("mean")` |
| Group gate | `df.groupby("k").filter(lambda g: len(g) >= 3)` |
| Multiple keys | `df.groupby(["k1", "k2"])` |
| Grouped z | `g.transform(lambda x: (x - x.mean()) / x.std())` |

## Next Steps

Next: **[09-pivot-tables](09-pivot-tables-lecture.md)** — reshaping groups into tables.
Continues in: **[07-machine-learning — 10 train/test](../../../../07-machine-learning/lectures/10-train-test-lecture.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/groupby.html
