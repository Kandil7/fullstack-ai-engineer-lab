# 03-libraries/pandas — 42: GroupBy Internals

## Topic Overview

`groupby` implements split-apply-combine: split the frame into sub-frames by
key, apply an operation to each, combine the results. The real skill is not
the syntax — it is choosing the right *verb*: `agg` shrinks to one row per
group, `transform` keeps the original row count with group-wise values,
`filter` drops whole groups, and `apply` runs arbitrary functions per group
at Python speed.

For AI engineers, groupby is where per-user, per-cohort, and per-time-period
features are born: total spend, average session length, order counts. Getting
the verb wrong — using `transform` when you need `agg`, or `apply` when a
built-in exists — produces either wrong-shaped features or pipelines that
take 100x longer than they should. This lecture builds both the mental model
and the performance ordering.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain split-apply-combine and reproduce it manually
2. Aggregate with multiple functions via lists and dicts
3. Use named aggregation (`agg(avg=("col", "mean"))`)
4. Use `transform` when output must match input length
5. Use `filter` to keep whole groups
6. Use `apply` knowing it is the slow path
7. Group by multiple keys and reshape with `unstack`
8. Build a per-user feature table with one named-agg pass

## Prerequisites

| Need | Where |
|------|-------|
| Filtering | `03-filtering-lecture.md` |
| Method chaining | `39-method-chaining-lecture.md` |
| MultiIndex | `18-multiindex-lecture.md` |

## 1. Split-Apply-Combine, Step by Step

Everything groupby does is three phases. Doing them manually makes the
mechanics obvious — and proves groupby is not magic.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "team": ["a", "b", "a", "c", "b", "a"],
    "score": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
})

manual: dict[str, float] = {}
for key, sub in df.groupby("team"):        # SPLIT
    manual[key] = sub["score"].mean()      # APPLY
manual_result = pd.Series(manual).sort_index()   # COMBINE

native = df.groupby("team")["score"].mean()
print(manual_result.tolist())              # [33.33, 35.0, 40.0]
print(manual_result.equals(native))        # True
```

```text
[33.33, 35.0, 40.0]
True
```

## 2. `agg` — Many Functions, One Pass

`agg` applies one or more functions and returns **one row per group** — the
frame shrinks. Mix built-in names, callables, and per-column dictionaries.

```python
multi = df.groupby("team").agg(["mean", "max"])
print(multi.columns.tolist())   # [('score', 'mean'), ('score', 'max')]

named = df.groupby("team").agg(avg=("score", "mean"),
                               peak=("score", "max"),
                               count=("score", "count"))
print(named.to_dict("index"))
# {'a': {'avg': 33.33, 'peak': 60.0, 'count': 3}, ...}
```

```text
[('score', 'mean'), ('score', 'max')]
{'a': {'avg': 33.33, 'peak': 60.0, 'count': 3}, 'b': {'avg': 35.0, 'peak': 50.0, 'count': 2}, 'c': {'avg': 40.0, 'peak': 40.0, 'count': 1}}
```

Named aggregation (`avg=("score", "mean")`) is the reviewable form: the
output column name, source column, and function live on one line.

## 3. `transform` — Same Shape, Group-Wise Values

`transform` returns a frame with the **same number of rows**: each row gets
its group's statistic. That is what makes "score minus team mean" and "share
of team total" possible — both classic features.

```python
df["team_mean"] = df.groupby("team")["score"].transform("mean")
df["delta"] = df["score"] - df["team_mean"]
df["share"] = df["score"] / df.groupby("team")["score"].transform("sum")
print(df.round(3).to_string(index=False))
```

```text
team  score  team_mean   delta  share
   a   10.0     33.333 -23.333  0.100
   b   20.0     35.000 -15.000  0.286
   a   30.0     33.333  -3.333  0.300
   c   40.0     40.000   0.000  1.000
   b   50.0     35.000  15.000  0.714
   a   60.0     33.333  26.667  0.600
```

## 4. `filter` — Keep Whole Groups

`filter(predicate)` keeps entire groups for which the predicate is True.
Rows are never partially filtered — groups are atomic.

```python
big = df.groupby("team").filter(lambda g: len(g) >= 2)
print(sorted(big["team"].unique().tolist()))   # ['a', 'b']
print(len(big))                                # 5
```

```text
['a', 'b']
5
```

Team `c` (one row) is dropped entirely; teams `a` and `b` keep all their rows.

## 5. `apply` — The Flexible Slow Path

`apply(func)` passes each group's DataFrame (or Series) to `func` and
combines the results. Most flexible, **slowest**: arbitrary Python per group.

```python
first_last = df.groupby("team")["score"].apply(lambda g: g.iloc[0] - g.iloc[-1])
print(first_last.sort_index().tolist())   # [-50.0, -30.0, 0.0]
```

```text
[-50.0, -30.0, 0.0]
```

`apply` is for results no built-in verb can express. If a built-in can, use
the built-in.

## 6. The Performance Ordering

For the same computation, built-in `agg` is the fast path, `transform` is
also vectorized, and `apply` is Python-per-group. On 100k groups, `apply`
means 100k Python calls.

```python
big_df = pd.DataFrame({
    "key": np.random.randint(0, 1000, 20_000),
    "val": np.random.randn(20_000),
})

agg_mean = big_df.groupby("key")["val"].mean().sort_index()

# transform: one value per row -> first row per key
tf = (big_df.assign(m=big_df.groupby("key")["val"].transform("mean"))
           .drop_duplicates("key")[["key", "m"]]
           .set_index("key")["m"].sort_index())

ap = big_df.groupby("key")["val"].apply(lambda g: g.mean()).sort_index()

print(np.allclose(agg_mean.values, tf.values))   # True
print(np.allclose(agg_mean.values, ap.values))   # True
```

```text
True
True
```

All three agree numerically. They do not agree on cost: `agg` and
`transform` are C-vectorized; `apply` pays Python per group.

## 7. Multiple Keys and Reshaping

Pass a list to `groupby` for composite keys; the result has a MultiIndex.
`unstack` turns one level into columns — the cohort-by-month matrix.

```python
sales = pd.DataFrame({
    "month": np.repeat(["Jan", "Feb", "Mar"], 4),
    "city": np.tile(["NY", "SF", "NY", "SF"], 3),
    "amount": np.random.uniform(10, 100, 12).round(1),
})
cohort = sales.groupby(["month", "city"])["amount"].sum()
print(cohort.index.names)          # ['month', 'city']
matrix = cohort.unstack()
print(matrix.round(1).to_string())
```

```text
['month', 'city']
city      NY    SF
month
Feb     95.2  98.3
Jan    166.0  96.8
Mar     98.9  49.9
```

## 8. Production Pattern — One Pass to a Feature Table

The senior shape: one `groupby` with named agg producing all group-level
features, then `reset_index` for the join back.

```python
def group_features(frame: pd.DataFrame) -> pd.DataFrame:
    return (
        frame
        .groupby("user_id")
        .agg(total_spend=("amount", "sum"),
             avg_spend=("amount", "mean"),
             order_count=("amount", "count"),
             max_spend=("amount", "max"))
        .reset_index()
    )
```

One pass, named columns, ready to merge onto the base frame — and each
statistic is reviewable on its own line.

## Common Mistakes to Avoid

### Mistake 1: `apply` when `agg` suffices

```python
# WRONG — Python-per-group; 100x slower for the same result
df.groupby("k")["v"].apply(lambda g: g.mean())
# CORRECT — vectorized built-in
df.groupby("k")["v"].mean()
```

### Mistake 2: `transform` when you meant `agg` (shape bug)

```python
# WRONG — same length as input; you wanted one row per group
result = df.groupby("k")["v"].transform("mean")
# CORRECT — shrinks to one row per group
result = df.groupby("k")["v"].mean()
```

### Mistake 3: assuming keys are sorted

```python
# default sorts keys; first-appearance order needs the flag
df.groupby("k").mean()                 # sorted
df.groupby("k", sort=False).mean()     # first-appearance
```

### Mistake 4: forgetting NaN behavior

```python
# sum() skips NaN; count() counts non-NaN — they answer
# different questions about the same missing data
```

## Best Practices

1. Decide by output shape: `agg` shrinks, `transform` preserves, `filter` drops
2. Use named agg for readable, reviewable feature columns
3. Reach for `apply` only when no built-in verb expresses the result
4. Keep `transform` results aligned by index — never assume position
5. Check key uniqueness/sortedness explicitly when order matters
6. Handle NaN semantics explicitly (`min_count`, `dropna=False`)
7. Combine multiple statistics in ONE groupby pass, not several
8. `reset_index()` after group-level features before joining back

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|-----------|------|-------|---------------------|
| `groupby(...).mean()` | O(n) | O(groups) | — |
| `.agg(["mean","max"])` | O(n) per func | O(groups) | one pass, many funcs |
| `.transform("mean")` | O(n) | O(n) | — |
| `.filter(pred)` | O(n x pred) | O(n) | boolean mask when possible |
| `.apply(f)` | O(groups) Python calls | O(n) | built-in agg — C speed |
| `groupby` + `unstack` | O(n) | O(groups x levels) | pivot_table for wide output |

**At scale:** on 1M rows with 100k groups, `agg`/`transform` finish in
milliseconds-to-seconds; `apply` with a Python function takes minutes. When a
custom per-group function is unavoidable, vectorize inside the function
(operate on the whole sub-frame) or use `numba` — never a row loop.

## AI Engineering Relevance

**Where this shows up:** user-level feature tables for churn/CLV models,
cohort analytics, session aggregation, and any per-entity statistic.

| Concept here | Used for |
|--------------|----------|
| named `agg` | one-pass per-user features (spend, count, max, avg) |
| `transform` | deviation-from-group-mean features, shares |
| `filter` | dropping low-volume groups before modeling |
| `apply` (sparingly) | custom per-group statistics |
| multi-key groupby | cohort x month matrices |
| `reset_index` | feature tables ready to merge back |

**Scale note:** feature pipelines run groupby every day on every user.
Choosing `agg` over `apply` is not a micro-optimization — it is the
difference between a nightly job that finishes in minutes and one that eats
the whole window.

## Practice Exercises

### Exercise 1: Manual Split-Apply-Combine (Easy)
Reproduce `df.groupby("team")["score"].max()` manually with a dict loop and
verify equality.

### Exercise 2: Named Aggregation (Medium)
From an orders frame, build per-user `total`, `avg`, `count`, and `max`
features in one named-agg pass; verify the column names and one user's values.

### Exercise 3: Transform vs Agg (Medium)
Compute "order amount minus user average" using `transform`, and verify the
result has the same length as the input while the mean per user is ~0.

### Exercise 4: Cohort Matrix (Hard)
From month x city sales, build the unstacked matrix, then melt it back and
verify round-trip equality with the original groupby.

## Summary

| Concept | Description |
|---------|-------------|
| split-apply-combine | the three-phase mechanism behind groupby |
| `agg` | shrinks to one row per group; named form is reviewable |
| `transform` | same shape; per-row group statistics |
| `filter` | keeps whole groups by predicate |
| `apply` | per-group Python — flexible, slow, last resort |
| multi-key + `unstack` | composite groups reshaped to matrices |
| feature table | one named-agg pass, reset_index, merge back |

GroupBy is a verb-selection problem: choose by output shape first, by speed
second. `agg`/`transform` cover 95% of feature engineering; `apply` is the
escape hatch you know the price of.

## Quick Reference

| Task | Idiom |
|------|-------|
| One stat per group | `df.groupby("k")["v"].mean()` |
| Many stats | `df.groupby("k")["v"].agg(["mean", "max"])` |
| Named stats | `df.groupby("k").agg(avg=("v", "mean"))` |
| Row-wise group stat | `df.groupby("k")["v"].transform("mean")` |
| Keep big groups | `df.groupby("k").filter(lambda g: len(g) >= 2)` |
| Custom per group | `df.groupby("k")["v"].apply(f)` |
| Two keys | `df.groupby(["a", "b"]).sum()` |
| Wide matrix | `df.groupby(["a", "b"])["v"].sum().unstack()` |

## Next Steps

Next: **[43 — Pandas for ML](43-pandas-for-ml-lecture.md)** — feature
matrices, splits without leakage, and sklearn interop.
Continues in: **[42 — GroupBy Internals challenge](../challenges/42-groupby-internals/README.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/groupby.html
