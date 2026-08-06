# 03-libraries/pandas (advanced) — 09: Pivot Tables & Reshaping

## Topic Overview

Reshaping changes the *layout* of data without changing its content. The
verbs: `pivot` (index -> columns), `pivot_table` (pivot with aggregation),
`melt` (wide -> long), `stack`/`unstack` (index <-> columns). Wide data is
convenient for humans and ML matrices; long (tidy) data is the canonical form
for groupby, plotting, and model training.

For AI engineers, reshaping is the bridge between storage formats and model
inputs: a per-user-per-day metrics table pivots into a feature matrix;
long-format event logs melt into grouped features. Getting wide-vs-long right
is the difference between clean feature matrices and index-confusion bugs.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Pivot a long table wide with `pivot`
2. Use `pivot_table` with aggregations and `fill_value`
3. Melt a wide table long with `melt`
4. Use `stack`/`unstack` on multi-level indexes
5. Explain wide vs long (tidy) and when each is right
6. Reverse a melt with pivot (round-trip discipline)

## Prerequisites

| Need | Where |
|------|-------|
| GroupBy | `08-groupby-aggregation-lecture.md` |
| MultiIndex | `18-multiindex-lecture.md` |
| Indexing | `02-indexing-selection-lecture.md` |

## 1. `pivot` — Long to Wide, No Aggregation

```python
df = pd.DataFrame({
    "user": ["u1", "u1", "u2", "u2"],
    "day": [1, 2, 1, 2],
    "score": [0.5, 0.6, 0.7, 0.8],
})

df.pivot(index="user", columns="day", values="score")
# day   1    2
# user
# u1   0.5  0.6
# u2   0.7  0.8
```

`pivot` requires exactly one value per (index, columns) cell — duplicate
combinations raise. When duplicates exist, you need `pivot_table` with an
aggregation.

## 2. `pivot_table` — Pivot with Aggregation

```python
df.pivot_table(index="user", columns="day", values="score", aggfunc="mean")
df.pivot_table(..., aggfunc="sum", fill_value=0)     # densify empty cells
df.pivot_table(index="user", columns="day", values="score",
               aggfunc={"score": "mean", "latency": "median"})
```

`pivot_table` handles duplicates by aggregating and can fill empty cells —
the realistic production form (e.g. sparse events densified to 0).

## 3. `melt` — Wide to Long (Tidy)

```python
wide = pd.DataFrame({
    "user": ["u1", "u2"],
    "day1": [0.5, 0.7],
    "day2": [0.6, 0.8],
})

wide.melt(id_vars=["user"], var_name="day", value_name="score")
#   user   day  score
# 0   u1  day1    0.5
# 1   u2  day1    0.7
# 2   u1  day2    0.6
# 3   u2  day2    0.8
```

`melt` converts columns into rows — the inverse of pivot. Long format is what
`groupby`, seaborn, and most modeling loops expect; `id_vars` stays put.

## 4. `stack` / `unstack` — Index to Columns

```python
df.set_index(["user", "day"]).stack()      # columns -> index level
df.set_index(["user", "day"]).unstack()    # index level -> columns
```

`stack`/`unstack` move levels between the index and the columns. They are the
MultiIndex-level versions of melt/pivot — use them when reshaping levels
rather than named columns.

## 5. Wide vs Long — Choosing the Layout

```python
# LONG (tidy): one observation per row — groupby/plotting/model-ready
# WIDE: one row per entity, columns per attribute — feature matrices, display
```

The rules of thumb: long for analysis (groupby, aggregation, plotting,
statsmodels); wide for model feature matrices (one row per sample) and for
human-readable reports. Most pipelines store long and pivot at the boundary.

## 6. Production Pattern — Tidy-to-Matrix

```python
def build_feature_matrix(events: pd.DataFrame, agg: dict) -> pd.DataFrame:
    """Long events -> one row per (user, day) feature matrix."""
    tidy = events.groupby(["user", "day"], as_index=False).agg(agg)
    matrix = tidy.pivot(index="user", columns="day", values="score").fillna(0)
    return matrix
```

Long storage, grouped aggregation, pivot to matrix, densify — the standard
feature-matrix assembly line.

## Common Mistakes to Avoid

### Mistake 1: `pivot` on data with duplicates

```python
# WRONG — ValueError on duplicate (index, columns) cells
df.pivot(index="user", columns="day", values="score")
# CORRECT — aggregate first
df.pivot_table(..., aggfunc="mean")
```

### Mistake 2: Melt without id_vars

```python
# WRONG — every non-id column becomes a row; user column gets melted away
# CORRECT — keep the entity column
wide.melt(id_vars=["user"])
```

### Mistake 3: Confusing stack/unstack direction

```python
# WRONG — expecting columns -> rows
df.stack()    # actually moves COLUMNS into the INDEX
# CORRECT — melt for named columns; stack for index levels
```

### Mistake 4: Pivot table with NaN that should be 0

```python
# WRONG — sparse cells stay NaN, breaking downstream math
# CORRECT — fill_value=0 when absence means zero
```

## Best Practices

1. Store long/tidy; pivot only at the consumption boundary
2. Use `pivot_table` whenever duplicates are possible
3. `fill_value=0` when absence-of-event means zero
4. `melt` with explicit `id_vars` to keep entity columns
5. Round-trip test: melt(pivot(x)) == x (for lossless layouts)
6. Prefer stack/unstack for MultiIndex levels, melt/pivot for named columns

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `pivot` | O(n) | index/column hash lookup |
| `pivot_table` | O(n) + agg | aggregation pass |
| `melt` | O(n) | column->row expansion |
| `stack`/`unstack` | O(n) | level moves |
| densify + fill | O(rows x cols) | wide matrix can blow up |

**At scale:** wide matrices grow as (entities x categories) — pivoting 10M
events with 10k distinct days creates a 10M x 10k matrix (~sparse). Densify
deliberately or keep sparse representations for big layouts.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| pivot to matrix | entity x feature model input construction |
| pivot_table | session/event aggregation into features |
| melt | converting wide model outputs to tidy eval frames |
| tidy-first | the storage convention that keeps pipelines clean |
| densify | filling absent events as zeros for models |

**Scale note:** feature-matrix assembly is where reshape mistakes become model
bugs — a wrong pivot silently reorders rows and misaligns labels. Always
round-trip test reshapes and assert index order before training.

## Practice Exercises

### Exercise 1: Pivot (Easy)
Pivot `user x day -> score` into a wide frame and back with melt; verify the
round-trip on a lossless example.

### Exercise 2: Pivot Table with Duplicates (Medium)
Add duplicate (user, day) rows; confirm `pivot` raises and `pivot_table(aggfunc="mean")`
succeeds.

### Exercise 3: Feature Matrix (Hard)
Write `build_feature_matrix(events, agg)` for events with duplicates, verify
the output has one row per user and 0-filled absent days, and that the index
matches the users exactly.

## Summary

| Concept | Description |
|---------|-------------|
| `pivot` | long -> wide, unique cells only |
| `pivot_table` | pivot with aggregation and filling |
| `melt` | wide -> long (tidy), inverse of pivot |
| `stack`/`unstack` | move levels between index and columns |
| wide vs long | choose by consumer: matrices vs analysis |
| round-trip | verify reshapes are lossless |

Reshaping is layout, not content. Keep data tidy in storage, pivot at the
boundary, and verify the round-trip — the feature matrix you train on will be
the one you intended.

## Quick Reference

| Task | Idiom |
|------|-------|
| Long -> wide | `df.pivot(index="u", columns="day", values="v")` |
| With aggregation | `df.pivot_table(index="u", columns="day", values="v", aggfunc="mean")` |
| Densify zeros | `pivot_table(..., fill_value=0)` |
| Wide -> long | `df.melt(id_vars=["u"], var_name="day", value_name="v")` |
| Index -> columns | `df.unstack()` |
| Columns -> index | `df.stack()` |

## Next Steps

Next: **[10-merging-joining](10-merging-joining-lecture.md)** — combining frames.
Continues in: **[04-databases — SQL joins](../../../04-databases/mysql/lectures/11-join-lecture.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/reshaping.html
