# 03-libraries/polars — 04: pandas Comparison

## Topic Overview

Every AI team that has pandas code will, at some point, ask: "should we
port it to Polars?" The honest answer is: *it depends on the scale, the
ecosystem, and the team* — and the only way to answer it well is to be
fluent in both grammars. This lecture is the translation table. For the
four operations that dominate feature pipelines — filtering,
grouped aggregation, joining, and deriving columns — you will see the
pandas idiom and the Polars idiom side by side, verified to produce
identical results on the same data.

The second half is about measurement and judgment. Benchmarks are printed
and read, not asserted, because wall-clock time is not reproducible. And
the migration question gets a real answer: Polars wins on scale,
Parquet/Arrow interop, and optimizer-visible pipelines; pandas remains
the right tool for timezone-heavy time series, apply-heavy research
code, and teams whose entire tooling stack already speaks pandas.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Translate the four core pandas idioms into Polars equivalents
2. Verify cross-engine equivalence of results on shared data
3. Explain why `.apply()` has no first-class Polars equivalent
4. Measure and compare pipelines without asserting on wall-clock time
5. List three scenarios where pandas is still the right choice
6. State the migration risks (index, mutation, dtype semantics)
7. Read a pandas codebase and sketch its Polars port

## Prerequisites

| Need | Where |
|------|-------|
| pandas DataFrames | `03-libraries/pandas/lectures/03-dataframes-lecture.md` |
| Polars expressions/contexts | `02-expressions-lecture.md` |
| Lazy evaluation | `03-lazy-evaluation-lecture.md` |

## 1. Filtering: Mask vs Predicate

Both engines filter rows vectorized; the grammar differs. pandas uses a
boolean mask in square brackets. Polars uses `.filter()` with an Expr
predicate.

```python
import pandas as pd
import polars as pl

pdf = pd.DataFrame({"campaign": ["a", "b", "a", "c"],
                    "revenue": [10.0, 5.0, 30.0, 12.0]})
plf = pl.from_pandas(pdf)

p_out = pdf[(pdf["campaign"] == "a") & (pdf["revenue"] >= 10.0)]
l_out = plf.filter((pl.col("campaign") == "a") & (pl.col("revenue") >= 10.0))

print(len(p_out), l_out.height)
```

```text
2 2
```

The mask syntax forces you to repeat `pdf[...]` for every term; the Expr
predicate reads like a sentence. Both are O(n); both are cache-friendly.

## 2. Grouped Aggregation: Dict vs Expressions

pandas `groupby().agg({...})` takes a dict mapping columns to functions.
Polars `group_by().agg(...)` takes named expressions — which, unlike a
dict of strings, can be inspected and reused by the optimizer.

```python
import pandas as pd
import polars as pl

pdf = pd.DataFrame({"campaign": ["a", "b", "a"],
                    "converted": [1, 0, 1], "revenue": [10.0, 5.0, 30.0]})
plf = pl.from_pandas(pdf)

g_p = (pdf.groupby("campaign")
       .agg(conversions=("converted", "sum"),
            revenue=("revenue", "mean"))
       .reset_index())

g_l = (plf.group_by("campaign")
       .agg(pl.col("converted").sum().alias("conversions"),
            pl.col("revenue").mean().alias("revenue"))
       .sort("campaign"))

print(g_p.sort_values("campaign")["conversions"].tolist())
print(g_l.sort("campaign")["conversions"].to_list())
```

```text
[2, 0]
[2, 0]
```

`reset_index()` is the pandas escape hatch from the groupby index; Polars
has no index to escape from — `group_by` output is always a flat frame.

## 3. Joins: merge vs join

Both default to inner joins and both take `how=`/`on=`. The shapes and
the null semantics match.

```python
import pandas as pd
import polars as pl

meta_p = pd.DataFrame({"campaign": ["a", "b"], "budget": [1000, 800]})
meta_l = pl.from_pandas(meta_p)

pdf = pd.DataFrame({"campaign": ["a", "b", "c"], "revenue": [1.0, 2.0, 3.0]})
plf = pl.from_pandas(pdf)

j_p = pdf.merge(meta_p, on="campaign", how="left")
j_l = plf.join(meta_l, on="campaign", how="left")

print(j_p.shape, j_l.shape)
print(j_l.filter(pl.col("budget").is_null()).height)   # c has no budget
```

```text
(3, 3) (3, 3)
1
```

One subtle difference: pandas infers `object` dtype for mixed missing
columns in older versions; Polars keeps the column's real dtype with
`null` values. The nulls are the same; the dtype story is cleaner in
Polars.

## 4. New Columns: Assignment vs with_columns

pandas writes into the frame (`df["new"] = ...`) — or a copy of it.
Polars `with_columns()` *returns* a new frame; the input is never
mutated. This is the safety property that makes chains reviewable.

```python
import pandas as pd
import polars as pl

pdf = pd.DataFrame({"user": ["a", "b", "a"], "revenue": [10.0, 20.0, 30.0]})
plf = pl.from_pandas(pdf)

n_p = pdf.copy()
n_p["revenue_per_user"] = n_p["revenue"] / n_p.groupby("user")["revenue"].transform("sum")

n_l = plf.with_columns(
    (pl.col("revenue") / pl.col("revenue").sum().over("user"))
    .alias("revenue_per_user")
)

print(n_p["revenue_per_user"].iloc[0], n_l["revenue_per_user"][0])
print(list(pdf.columns))          # original untouched by the polars chain
```

```text
0.25 0.25
['user', 'revenue']
```

The pandas version needs `.copy()` to avoid mutating the source; the
Polars version cannot mutate anything, because every transform returns a
new frame. `transform("sum")` and `.sum().over("user")` are the same
window computation — one string-based, one expression-based.

## 5. The Apply Question: Where the Translation Stops

pandas `apply` is the Swiss-army knife: row-wise, column-wise, with any
Python callable. Polars deliberately has no fast per-element apply —
element-wise Python dispatch would destroy the columnar advantage. The
translation is not "apply with a different name"; it is "rewrite the
logic as an expression".

```python
import pandas as pd
import polars as pl

pdf = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
plf = pl.from_pandas(pdf)

# pandas row-wise
p_out = pdf["x"].apply(lambda v: v * 2 if v > 1 else 0.0)

# polars expression - same logic, vectorized, optimizer-visible
l_out = plf.with_columns(
    pl.when(pl.col("x") > 1).then(pl.col("x") * 2).otherwise(0.0).alias("y")
)

print(p_out.tolist(), l_out["y"].to_list())
```

```text
[0.0, 4.0, 6.0] [0.0, 4.0, 6.0]
```

When a function genuinely cannot be expressed natively (e.g., a custom
tokenizer), `pl.map_batches` applies it to whole batches — still far
cheaper than per-element dispatch, and it keeps the plan intact.

## 6. Measuring Honestly: Print, Don't Assert

Benchmarks belong in reports, not in CI gates. Wall-clock time depends on
the machine, the OS, the cache state, and the version — an assertion like
`assert polars_time < pandas_time` will fail on a loaded CI box even when
the code is right. The honest pattern: run several times, keep the best,
print the numbers.

```python
import time
import pandas as pd
import polars as pl

pdf = pd.DataFrame({"a": range(1_000_000), "b": range(1_000_000)})
plf = pl.from_pandas(pdf)

def measure(fn):
    best = float("inf")
    for _ in range(3):
        t0 = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t0)
    return best * 1000

ms_p = measure(lambda: pdf[pdf["a"] > 500_000])
ms_l = measure(lambda: plf.filter(pl.col("a") > 500_000))
print(f"pandas: {ms_p:.1f} ms, polars: {ms_l:.1f} ms")
```

```text
pandas: 21.3 ms, polars: 2.1 ms
```

The numbers will differ on your machine — that is the point. The *shape*
of the result (columnar engine faster on wide scans, gap widening with
data size) is what you should take away, not the specific digits.

## 7. Migration Guide: Order of Operations

Porting a pandas pipeline to Polars in a way that survives review:

1. **Inventory the idioms**: filter, groupby, merge, assign, pivot,
   window — each has a direct translation.
2. **Isolate the applies**: every row-wise `apply` is a candidate for
   expression rewriting; these are the risky items, do them last.
3. **Pin the dtypes**: pandas `object` columns need explicit `pl.String`
   or `pl.Categorical` decisions before the port.
4. **Check the null semantics**: pandas `NaN` in float columns vs Polars
   `null` — they behave the same in aggregates, differently in equality.
5. **Verify equivalence**: run both on a fixed sample and compare
   `to_dict()` outputs exactly.
6. **Benchmark, then ship**: print measurements at the new scale, don't
   assert them.

## 8. When pandas Is Still Right

Porting is not always a win. Three cases where pandas remains the better
call:

- **Timezone-heavy time series**: pandas `resample` rules and tz-aware
  indexes are far more mature than Polars' time handling.
- **Apply-heavy research code**: a notebook full of row-wise Python
  functions gains little from a columnar engine, because the bottleneck
  is Python either way.
- **Pandas-native ecosystems**: if your stack (SQLAlchemy, statsmodels,
  seaborn, most tutorials) assumes pandas, the interop tax of converting
  to and from Polars can exceed the speed gain.

The decision rule is scale and shape: large, fixed, vectorized pipelines
over Parquet corpora -> Polars. Small, exploratory, Python-heavy
notebooks -> pandas. And the two interoperate zero-copy through Arrow,
so "migrate" rarely needs to mean "delete the pandas code".

## Common Mistakes to Avoid

### Mistake 1: Porting .apply() Line by Line
```
# WRONG — slow per-element dispatch, the speed advantage is gone
plf.with_columns(pl.col("x").apply(my_py_fn))
# CORRECT — rewrite as an expression, or use pl.map_batches
plf.with_columns(pl.when(pl.col("x") > 1).then(pl.col("x") * 2).otherwise(0.0))
```

### Mistake 2: Reaching for .loc / .iloc
```
# WRONG — Polars has no index
plf.loc[plf["a"] == 2]
# CORRECT — positional or declarative
plf.row(2)
plf.filter(pl.col("a") == 2)
```

### Mistake 3: Asserting on Benchmarks
```
# WRONG — flaky on shared CI machines
assert polars_time < pandas_time
# CORRECT — print measurements; gate on correctness and memory only
```

### Mistake 4: Expecting inplace Behavior
```
# WRONG — there is no inplace=True; nothing mutates
df.with_columns(pl.col("a") * 2)   # result discarded, df unchanged
# CORRECT — bind the new frame
df = df.with_columns(pl.col("a") * 2)
```

### Mistake 5: Assuming the Port Is Free of Semantics
```
# WRONG — pandas NaN != NaN but float-null != null is False in Polars
# CORRECT — read the dtype and null rules per column before porting
```

## Best Practices

1. Verify equivalence on a sample before porting at scale
2. Rewrite `apply` as expressions; use `map_batches` only when forced
3. Measure with best-of-N and print; never assert wall-clock times
4. Pin explicit dtypes for every `object` column in the pandas source
5. Keep the pandas original until the Polars port passes parity checks
6. Use `pl.from_pandas` / `df.to_pandas()` for incremental migration
7. Prefer `.sum().over("user")` over `groupby().transform()` translations
8. Document which pandas version the port replaces (API drift matters)
9. Test nulls explicitly: equality, grouping, and joins all interact
10. Port the hot path first (the 10% of code that reads 90% of bytes)

## Complexity and Cost

| Operation | pandas | Polars | Cheaper alternative |
|-----------|--------|--------|---------------------|
| Filter mask | O(n) | O(n) | push predicate into scan (lazy) |
| groupby().agg({}) | O(n log g) | O(n log g) | fewer agg passes |
| merge on key | O(n log n) | O(n log n) | sort-merge vs hash tuning |
| transform window | O(n log g) | O(n log g) | `.over()` in one expression |
| row-wise apply | O(n) Python | — | rewrite as expression |

Both engines are O(n) on the hot paths; the practical difference is the
constant factor (columnar SIMD kernels vs interpreted dispatch) and
memory behavior (no index, no copies in Polars chains). At 10M rows the
constant factors decide the job; at 1B rows only the plan does.

## AI Engineering Relevance

**Where this shows up:** every legacy feature pipeline being migrated to
a scale that pandas cannot serve. Feature stores, training corpora, and
eval harnesses are the three places this migration actually happens.

| Concept here | Used for |
|--------------|----------|
| filter/group_by/join parity | porting legacy pandas ETL to Polars |
| expression rewrite of apply | removing Python hot loops from feature code |
| measured comparison | justifying a migration in a review |
| `pl.from_pandas` interop | migrating incrementally, table by table |
| pandas-when-right cases | not over-migrating time-series research code |

**Scale note:** the migration decision flips at roughly the point where
pandas needs chunked reading tricks: 10-100M rows. Below that, either
tool is fine; above it, the lazy plan and the Arrow memory model are the
difference between a batch job and a streaming job.

## Practice Exercises

### Exercise 1: Filter Parity (Difficulty: Easy)
Write `pandas_filter(df, campaign, min_rev)` and `polars_filter(df, ...)`
on shared data; assert identical row counts and row values.

### Exercise 2: Groupby Parity (Difficulty: Easy)
Compute per-campaign `conversions`, `revenue` mean, and event count in
both engines; assert the numeric outputs match exactly.

### Exercise 3: Window Translation (Difficulty: Medium)
Translate pandas `groupby("user")["revenue"].transform("sum")` into
`.sum().over("user")`; assert per-row share values agree to 1e-12.

### Exercise 4: Apply Rewrite (Difficulty: Medium)
Rewrite `df["x"].apply(lambda v: v * 2 if v > 1 else 0.0)` as a
`pl.when/then/otherwise` expression; assert identical outputs.

### Exercise 5: Parity Harness (Difficulty: Hard)
Build a `parity_check(pandas_fn, polars_fn, df)` helper that runs both
on the same rows and reports (not asserts) timing plus an exact-value
equality verdict. Use it on a 3-step pipeline.

## Summary

| Concept | Description |
|---------|-------------|
| Filter | pandas mask vs Polars `filter(Expr)` |
| Grouped agg | pandas agg dict vs Polars named expressions |
| Join | `merge(on=, how=)` vs `join(on=, how=)` |
| New columns | assignment (mutating) vs `with_columns` (pure) |
| Apply | no first-class Polars equivalent; rewrite as expressions |
| Measurement | print best-of-N, never assert wall-clock |
| pandas-when-right | tz time series, apply-heavy research, pandas ecosystems |

The two libraries speak different grammars for the same ideas, and the
differences are exactly where the safety and speed live: expressions
instead of string dicts, new frames instead of mutation, plans instead
of eager steps. Port with parity checks, measure honestly, and keep the
pandas code until the Polars code proves equal.

## Quick Reference

| Task | pandas | Polars |
|------|--------|--------|
| Filter | `df[mask]` | `df.filter(expr)` |
| Group + agg | `df.groupby("k").agg({...})` | `df.group_by("k").agg(expr...)` |
| Left join | `a.merge(b, on="k", how="left")` | `a.join(b, on="k", how="left")` |
| New column | `df["y"] = ...` | `df.with_columns(expr.alias("y"))` |
| Window share | `df.groupby("k")["v"].transform("sum")` | `pl.col("v").sum().over("k")` |
| Row access | `df.iloc[i]` | `df.row(i)` |
| Row-wise fn | `df.apply(fn, axis=1)` | `pl.when/otherwise` or `map_batches` |
| Convert | `df.to_pandas()` | `df.to_polars()` / `pl.from_pandas(df)` |

## Next Steps

Next: **[05 PyArrow and Parquet](05-pyarrow-parquet-lecture.md)** — the
storage and interchange layer both libraries share.
Continues in: **[Phase 4 — ML Libraries](../../../04-ml-libraries/README.md)**
Official docs: https://docs.pola.rs/user-guide/migration/pandas/
