# 03-libraries/polars — 01: Introduction to Polars

## Topic Overview

Polars is a DataFrame library for Rust and Python that is rapidly becoming
the professional default for large-scale data work. Where pandas grew out of
statistics research and NumPy, Polars grew out of two engineering facts:
RAM is expensive and CPUs are wide. Its core design — the Arrow memory
format, an expression API, and lazy query optimization — targets exactly the
workloads AI engineers hit daily: feature pipelines over millions of rows,
Parquet corpora, and repeated reads of the same columns.

The first fact to internalize is that Polars is *not* "pandas, but faster".
It is a different memory model (columnar Arrow buffers instead of
row-oriented NumPy blocks with a separate index), a different API (every
transform is an expression that the optimizer can see), and a different
execution model (eager and lazy, with the lazy engine doing the heavy
lifting). This lecture establishes the mental model: what a DataFrame is,
what the Arrow memory model buys you, and what "eager vs lazy" actually
means before you ever call `.collect()`.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build a Polars DataFrame from a dict of columns and inspect its schema
2. Explain why columnar (Arrow) storage is faster than row-oriented storage
   for analytics workloads
3. Distinguish a DataFrame (data, eager) from a LazyFrame (plan, lazy)
4. Convert between eager and lazy mode with `.lazy()` and `.collect()`
5. Read a Polars table output and interpret the shape/schema header
6. Identify the three most common pandas habits that break in Polars
7. State the AI-specific reason Parquet + Arrow + Polars are one ecosystem

## Prerequisites

| Need | Where |
|------|-------|
| Python containers (list, dict) | `01-core-python/lectures/03-lists-lecture.md` |
| NumPy arrays and dtypes | `03-libraries/numpy/lectures/01-array-creating-lecture.md` |
| pandas DataFrame basics (for contrast) | `03-libraries/pandas/lectures/03-dataframes-lecture.md` |
| CSV/Parquet data formats | `03-libraries/pandas/lectures/05-load-data-csv-lecture.md` |

## 1. Installing and Importing Polars

Polars is a single pip install with no system dependencies; on Windows the
wheel bundles its own Rust core. In exercises that treat Polars as optional
(CI machines that may not have it), guard the import and exit cleanly.

```python
try:
    import polars as pl
except ImportError:
    print("[skip] polars not installed - install with: pip install polars")
    raise SystemExit(0)
```

The import convention is `import polars as pl`, mirroring `pd` for pandas
and `np` for numpy. There is no `polars.DataFrame` without `pl.` — the
module *is* the namespace.

## 2. Building a DataFrame: Dict-of-Columns

A Polars DataFrame is constructed from **columns**, not rows. Each key
becomes a typed column; each value is a list (or any sequence) of that
column's data.

```python
import polars as pl

df = pl.DataFrame(
    {
        "sample_id": [1, 2, 3, 4],
        "embedding_dim": [384, 384, 384, 384],
        "score": [0.91, 0.44, 0.87, 0.12],
        "split": ["train", "train", "valid", "valid"],
    }
)
print(df.to_dict(as_series=False))
print(df.shape, df.columns)
```

```text
{'sample_id': [1, 2, 3, 4], 'embedding_dim': [384, 384, 384, 384],
 'score': [0.91, 0.44, 0.87, 0.12], 'split': ['train', 'train', 'valid', 'valid']}
(4, 4) ['sample_id', 'embedding_dim', 'score', 'split']
```

Note the print style: the pretty table renderer uses box-drawing Unicode
that crashes Windows cp1252 consoles, so teaching files print
`to_dict(as_series=False)` or `.rows()` instead. The data is identical.

Type inference is automatic: ints become `Int64`, floats `Float64`,
strings `String`. You can override with `schema=` when inference is wrong
(e.g., a column of `"1"`, `"2"` strings that should be ints).

## 3. Schema: The Typed Contract

`df.schema` maps column names to Arrow data types. This is not cosmetic:
the types travel with the data into Parquet, DuckDB, and PyTorch, and they
decide which operations are legal (`Int64 + Int64` yes, `String + Int64`
no).

```python
import polars as pl

df = pl.DataFrame({"score": [0.9, 0.4], "split": ["a", "b"]})
print(df.schema)
```

```text
Schema({'score': Float64, 'split': String})
```

Every type is an Arrow type, not a Python type. The columnar storage that
makes Polars fast starts here: each column is one typed buffer, and the
schema is that buffer's contract.

## 4. The Arrow Memory Model: Why Columnar Wins

Two ways to lay out the same table in memory:

- **Row-oriented** (CSV, JSON, most OLTP databases): each record's fields
  are stored together. Reading one column across 1M rows touches 1M
  scattered locations.
- **Column-oriented** (Arrow, Parquet): each column's values are stored
  contiguously. Reading one column touches one contiguous buffer.

```python
import polars as pl

df = pl.DataFrame({"score": [0.9, 0.4, 0.87, 0.12]})
mean = df["score"].mean()          # one contiguous f64 buffer, SIMD-able
print(f"{mean:.3f}")
```

```text
0.573
```

Columnar wins for analytics because queries touch whole columns, not whole
rows: means, filters, and joins read contiguous memory, which is
cache-friendly and vectorizable. It also compresses better in Parquet,
because similar values sit next to each other. The cost: row-wise
inserts and "give me record 5000" are slower than in row stores — a
trade-off analytics accepts gladly.

## 5. Series: One Typed Column

`df["score"]` returns a `Series`: the column with its name and dtype. It is
the unit of columnar work — all the arithmetic you do to a column happens
on the Series (or, more idiomatically, on an expression over it).

```python
import polars as pl

s = pl.Series("score", [0.9, 0.4, 0.87, 0.12])
print(s.dtype, s.mean())
```

```text
Float64 0.5725
```

Series support vectorized arithmetic, comparisons, and the same null
semantics as columns in a DataFrame. In practice you rarely construct them
directly; you get them by indexing a DataFrame.

## 6. Eager vs Lazy: The Two Execution Models

Eager mode (the default for `pl.DataFrame`) executes every call
immediately — pandas-style. Lazy mode wraps work in a `LazyFrame`, a query
plan that runs *once* when you call `.collect()`.

```python
import polars as pl

df = pl.DataFrame({"score": [0.9, 0.4, 0.87, 0.12], "split": ["a", "a", "b", "b"]})

eager = df.filter(pl.col("score") > 0.5)              # runs now
lazy = df.lazy().filter(pl.col("score") > 0.5)        # just a plan
result = lazy.collect()                               # runs now

print(eager.equals(result))
```

```text
True
```

Why would you defer work? Because the optimizer can reorder a whole
pipeline — pushing a filter before a join, dropping unneeded columns at
the file scan — when it sees the entire plan instead of one call at a
time. Lazy is not "delayed"; it is "optimizable".

## 7. Inspecting a LazyFrame: Explain, Don't Execute

The plan is inspectable before it runs. `LazyFrame.explain()` renders the
optimized plan as text; `collect_schema()` reveals the output schema
without touching the data.

```python
import polars as pl

lf = pl.LazyFrame({"score": [0.9, 0.4], "split": ["a", "b"]})
plan = lf.filter(pl.col("score") > 0.5).explain(optimized=True)
print("FILTER" in plan)     # the optimizer kept the filter node
print(lf.collect_schema().names())
```

```text
True
['score', 'split']
```

This is the debugging superpower of the lazy engine: you can read *what
will happen* and catch a plan that scans 50GB when it should scan 200MB —
before it runs.

## 8. Reading Data: read_* vs scan_*

Eager readers (`pl.read_csv`, `pl.read_parquet`) load everything into
memory now. Lazy scanners (`pl.scan_csv`, `pl.scan_parquet`) open metadata
and return a LazyFrame. The scanner is the default for anything larger
than RAM.

```python
import polars as pl

lf = pl.scan_csv("events.csv")       # schema + row estimate, no data
print(lf.collect().height)           # now the file is actually read
```

```text
2000
```

Rule of thumb: if the file might not fit in RAM, or you only need a few
columns, scan. If it is a small scratch file, `read_*` is fine. You can
always move between them — `.lazy()` and `.collect()` are free.

## 9. What Polars Does NOT Have (pandas Habits to Drop)

Three pandas habits break immediately:

```python
import polars as pl

df = pl.DataFrame({"id": [1, 2, 3], "score": [0.9, 0.4, 0.7]})
# df.iloc[1]              # AttributeError: no positional index
# df.loc[df["id"] == 2]   # AttributeError: no .loc
# df["score"].apply(...)  # slow per-element path, discouraged
print(df.row(1))
print(df.filter(pl.col("id") == 2).rows())
```

```text
(2, 0.4)
[(2, 0.4)]
```

There is no index. Rows are found by position (`.row(i)`) or by predicate
(`.filter(...)`). There is no `inplace=True`. There is no row-wise
`apply` as a first-class citizen — you use expressions (next topic), which
are both faster and inspectable.

## 10. The Ecosystem: Arrow, Parquet, DuckDB, PyTorch

Polars does not own its memory format; Arrow does. That is the strategic
bet: a Polars DataFrame can be handed to DuckDB, written as Parquet, or
converted to a PyTorch tensor without a format conversion, because they
all speak Arrow. For AI work this means: load a Parquet corpus once,
train on the same buffers, and never serialize through CSV again.

```python
import polars as pl
import numpy as np

df = pl.DataFrame({"x": np.arange(5.0)})
arr = df["x"].to_numpy(allow_copy=False)   # zero-copy view when possible
print(np.shares_memory(df["x"].to_numpy(), arr))
```

```text
True
```

## Common Mistakes to Avoid

### Mistake 1: Expecting an Index
```
# WRONG — there is no index in Polars
df.loc[2]        # AttributeError
# CORRECT — positional or declarative access
df.row(2)
df.filter(pl.col("id") == 2)
```

### Mistake 2: Forgetting .collect() on a LazyFrame
```
# WRONG — a LazyFrame is a plan, not data
result = df.lazy().filter(...)   # prints "LazyFrame", not rows
# CORRECT — execute the plan
result = df.lazy().filter(...).collect()
```

### Mistake 3: Using .apply() for column math
```
# WRONG — Python per-element dispatch, kills the speed advantage
df["score"].apply(lambda x: x * 2)
# CORRECT — expression, vectorized and optimizer-visible
df.with_columns((pl.col("score") * 2).alias("double"))
```

### Mistake 4: Printing raw tables on Windows
```
# WRONG — the table renderer uses box-drawing Unicode; cp1252 crashes
print(df)
# CORRECT — ASCII-safe views
print(df.to_dict(as_series=False))
print(df.rows())
```

### Mistake 5: Scanning when you meant reading (and vice versa)
```
# WRONG — collect() right after scan for a tiny file is fine but noisy
# WRONG — read_csv on a 50GB file will OOM
# CORRECT — scan big, read small; convert freely with .lazy()/.collect()
```

## Best Practices

1. Build DataFrames column-first: dict of lists, not list of dicts
2. Prefer `pl.col("name")` over string column names inside expressions
3. Inspect `df.schema` before writing downstream code — types travel
4. Scan, don't read, anything that might exceed RAM
5. Use `--verify` on exercises: plain runs are also tests
6. Never print raw `explain()` output on Windows; print booleans instead
7. Keep nulls explicit: Polars represents missing data with `null`, not
   Python `None` in object columns
8. Use `.rows()` and `.to_dict(as_series=False)` for ASCII-safe inspection
9. Convert to numpy with `allow_copy=False` and check `shares_memory`
10. Read the optimized plan before profiling: the plan, not the CPU, is
    usually the bottleneck

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|-----------|------|-------|---------------------|
| `pl.DataFrame(dict_of_lists)` | O(n) total | O(n) | pre-size lists; avoid list-of-dicts |
| `df["col"].mean()` | O(n) | O(1) | — (one pass, SIMD) |
| `df.filter(predicate)` | O(n) | O(n) output | push the filter into a scan |
| `df.lazy().collect()` | O(plan) | O(output) | keep it lazy; stream when possible |
| `df.to_numpy()` | O(1) or O(n) | O(1) or O(n) | `allow_copy=False` for a view |

The dominant cost in data work is **memory**, not CPU: a columnar layout
makes each pass cache-friendly, and the plan optimizer avoids whole
materializations. Always ask: "which bytes does this query actually need?"

## AI Engineering Relevance

**Where this shows up:** every feature pipeline that feeds a training run
or an inference service. Feature stores, eval harnesses, and data
validation jobs are all "read table, transform columns, write table" — the
exact shape Polars optimizes.

| Concept here | Used for |
|--------------|----------|
| Dict-of-columns construction | turning raw event logs into typed feature tables |
| Arrow memory model | zero-copy handoff to PyTorch DataLoaders |
| `scan_*` + lazy | ETL over corpora that do not fit in RAM |
| Schema contract | validating feature types before training starts |
| `.to_numpy(allow_copy=False)` | feeding embedding columns into model code |

**Scale note:** at 1M rows pandas is "fine"; at 100M rows pandas needs
chunking tricks while Polars scans and streams. At 50GB the question stops
being "which library" and becomes "which bytes do we touch" — that is the
lazy plan.

## Practice Exercises

### Exercise 1: Build a Schema (Difficulty: Easy)
Construct a `pl.DataFrame` from dict-of-columns with 3 columns (id, score,
split) and verify `df.shape == (5, 3)` and `schema["score"] == Float64`.

### Exercise 2: Eager vs Lazy Equivalence (Difficulty: Easy)
Write `eager_pipeline(df)` and `lazy_pipeline(df)` that both filter
`score > 0.5` and add `score_pct = score * 100`. Assert `eager.equals(lazy)`.

### Exercise 3: Columnar Mean (Difficulty: Medium)
Given a DataFrame with 100k floats, compute the mean via `df["col"]`
and via `pl.col("col").mean()` inside a `select`. Assert both agree to
1e-12. (Solutions live in `challenges/01-introduction/`.)

### Exercise 4: Type Inference Trap (Difficulty: Medium)
Build a DataFrame where one column is `["1", "2", "3"]` and one is
`[1, 2, 3]`. Assert the dtypes differ, then rebuild the string column
with `schema={"nums": pl.Int64}` and assert it becomes Int64.

### Exercise 5: Plan Reading (Difficulty: Hard)
For `df.lazy().filter(...).explain(optimized=True)`, write a function that
returns `True` iff the plan contains a FILTER node. Run it against a
filter-only plan and a select-only plan; explain the difference.

## Summary

| Concept | Description |
|---------|-------------|
| DataFrame | Eager, columnar table of typed Series |
| Series | One typed column; the unit of columnar work |
| Schema | `{column: Arrow dtype}` contract that travels with data |
| Arrow | Columnar memory format shared across the ecosystem |
| LazyFrame | A query plan; executes once at `.collect()` |
| `scan_*` | Open file metadata without loading data |
| No index | Rows by position `.row(i)` or predicate `.filter()` |

Polars is not pandas with a speed toggle; it is a columnar, typed,
plan-optimizing engine. The DataFrame is where you start, but the
LazyFrame is where the performance lives — and both speak the same
expression language, which is the subject of the next topic.

## Quick Reference

| Task | Idiom |
|------|-------|
| Build a frame | `pl.DataFrame({"a": [1, 2], "b": ["x", "y"]})` |
| Inspect schema | `df.schema` |
| Shape | `df.shape`, `df.height`, `df.width` |
| One column | `df["score"]` (Series) |
| Eager -> lazy | `df.lazy()` |
| Lazy -> eager | `lf.collect()` |
| Read CSV eager | `pl.read_csv(path)` |
| Scan CSV lazy | `pl.scan_csv(path)` |
| ASCII-safe print | `df.to_dict(as_series=False)`, `df.rows()` |
| Column mean | `df["score"].mean()` |
| Zero-copy numpy | `df["score"].to_numpy(allow_copy=False)` |

## Next Steps

Next: **[02 Expressions](02-expressions-lecture.md)** — the expression API
that makes Polars fast and composable.
Continues in: **[Phase 4 — ML Libraries](../../../04-ml-libraries/README.md)**
Official docs: https://docs.pola.rs/user-guide/getting-started/
