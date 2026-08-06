# 03-libraries/pandas (advanced) — 12: Apply & Map

## Topic Overview

Custom transformations: `Series.map` (value-to-value remapping), `Series.apply`
(row-wise function), `DataFrame.apply` (column or row-wise), `applymap`
(element-wise, deprecated in favor of `df.map`), and `pipe` (chained function
calls on the frame). The rule that separates senior code: **vectorized and
`.map` first; `.apply` second; Python loops last.**

For AI engineers, map is the encoding and normalization tool (label -> code,
bucket -> value), apply handles per-row logic that vectorization can't
express cleanly, and pipe turns a pipeline of transforms into readable,
testable functions. Know which tool each job needs — and the cost of guessing
wrong.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Remap values with `Series.map`
2. Apply row-wise functions with `Series.apply`
3. Use `DataFrame.apply` with `axis=` semantics
4. Use element-wise `df.map` (and know `applymap`'s deprecation)
5. Chain transforms with `pipe`
6. Explain vectorized > map > apply > loop performance
7. Choose the right tool per transformation

## Prerequisites

| Need | Where |
|------|-------|
| Functions | `01-core-python/21-functions.py` |
| GroupBy transform | `08-groupby-aggregation-lecture.md` |
| String methods | `06-string-methods-lecture.md` |

## 1. `map` — Value-to-Value Remapping

```python
df["split_code"] = df["split"].map({"train": 0, "val": 1, "test": 2})
df["size_code"] = df["size"].map({"s": 0, "m": 1, "l": 2})
df["is_gold"] = df["label"].map(lambda x: x == "gold").astype(int)
```

`map` takes a dict (missing keys -> NaN) or a callable. It is the encoding
tool: categorical strings to codes, label mappings, and simple per-value
transforms — all vectorized at C speed.

## 2. `apply` on a Series — Row-Wise Function

```python
df["normalized"] = df["text"].apply(lambda t: " ".join(t.split()[:50]))
df["domain"] = df["url"].apply(extract_domain)
```

`Series.apply` calls the function per element — Python speed. Use it when the
transform is per-value logic with Python branches (parsing, extracting) that
the vectorized methods cannot express.

## 3. `apply` on a DataFrame — Columns or Rows

```python
df.apply(lambda col: col.max() - col.min(), axis=0)   # per column
df.apply(lambda row: row["a"] / row["b"], axis=1)     # per row
```

`axis=0` (default) applies to columns; `axis=1` to rows. Row-wise apply is
the slowest common pandas operation — avoid in hot paths.

## 4. Element-Wise — `df.map` (3.3+) and `applymap`

```python
df.map(lambda x: x if pd.notna(x) else 0)   # element-wise, modern form
df.applymap(fn)                              # deprecated in pandas 3.x
```

Element-wise mapping over the whole frame: use `df.map` on pandas >= 3, note
`applymap` deprecation on older series of the docs.

## 5. `pipe` — Function Chaining

```python
def drop_dupes(df, subset): ...
def scale(df, cols): ...

df = (df
      .pipe(drop_dupes, subset=["user_id"])
      .pipe(scale, cols=["latency_ms"])
      .pipe(add_window_features, col="count", windows=(3, 7)))
```

`pipe` passes the frame to a function (with extra args) and returns the
result — turning a chain of transformations into readable, individually
testable functions. This is the refactoring target for long method chains.

## 6. The Performance Ladder

```python
vectorized  >  Series.map  >  Series.apply  >  DataFrame.apply(axis=1)  >  Python loop
```

Rule of thumb: reach for the leftmost tool that expresses the transform.
Vectorized (`.str`, arithmetic, comparisons) is ~100x map, which is ~10-100x
apply. Per-row apply on 10M rows is minutes; on the same data vectorized is
seconds.

## 7. Production Pattern — Encode with Fallback

```python
def encode_labels(series: pd.Series, mapping: dict, default: int = -1) -> pd.Series:
    """Map labels to codes with an explicit fallback for unknown values."""
    return series.map(mapping).fillna(default).astype(int)
```

Explicit default handling beats silent NaN: an unknown label becomes `-1`,
which the model can learn rather than a NaN that flows into training.

## Common Mistakes to Avoid

### Mistake 1: `apply` where `map` suffices

```python
# WRONG — apply is Python-speed for a dict lookup
df["c"] = df["x"].apply(lambda v: mapping[v])
# CORRECT — vectorized remap
df["c"] = df["x"].map(mapping)
```

### Mistake 2: map on a DataFrame (it's a Series method)

```python
# WRONG — Series.map on a frame misbehaves or raises
df.map({...})
# CORRECT — per column
df["c"] = df["c"].map({...})
```

### Mistake 3: Row-wise apply in hot loops

```python
# WRONG — O(n) Python calls; minutes at scale
df["ratio"] = df.apply(lambda r: r["a"] / r["b"], axis=1)
# CORRECT — vectorized
df["ratio"] = df["a"] / df["b"]
```

### Mistake 4: Long method chains without pipe

```python
# WRONG — untestable, unreviewable chain
df.drop_duplicates().assign(...).query(...).merge(...).reset_index()
# CORRECT — named functions via pipe
```

## Best Practices

1. Vectorized operations first; `.map` for remaps; `.apply` only for per-row logic
2. Always provide fallbacks (fillna/default) for unknown mapped keys
3. Prefer `axis=0` apply over `axis=1`; avoid row-wise in hot paths
4. Use `pipe` to turn chains into named, tested functions
5. Use `df.map` (modern) for element-wise whole-frame transforms
6. Profile when in doubt — the ladder is a guide, not a law

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| vectorized op | O(n) C-speed | the default choice |
| `Series.map` | O(n) | hashed lookup |
| `Series.apply` | O(n) Python | ~10-100x slower than map |
| `DataFrame.apply(axis=1)` | O(n) Python | slowest common op |
| `df.map` | O(n x cols) | element-wise |
| `pipe` | O(frame) | just a function call |

**At scale:** the difference between vectorized and row-wise apply is the
difference between seconds and hours on 10M rows. Write the vectorized form
first; apply is the deliberate exception, not the default.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| map | label -> code encoding, bucket mapping |
| apply | per-row text/URL parsing logic |
| pipe | the readable, testable feature pipeline |
| default fallbacks | unknown-label handling at intake |
| performance ladder | keeping 10M-row cleaning feasible |

**Scale note:** feature pipelines that mix 50 apply calls on a 10M-row frame
silently cost hours per run. The map-vs-apply discipline is a cost lever that
shows up in every retraining cycle.

## Practice Exercises

### Exercise 1: Label Encoding (Easy)
Map `["train","val","test"]` to codes with a default of -1; verify an unknown
value becomes -1.

### Exercise 2: Per-Row Logic (Medium)
Use `Series.apply` to extract the domain from a URL column, then vectorize the
same logic with `.str` where possible and compare.

### Exercise 3: Pipe Pipeline (Hard)
Refactor a 6-step transformation chain into `pipe`d named functions with unit
tests for each stage.

## Summary

| Concept | Description |
|---------|-------------|
| `map` | vectorized value remapping with fallback |
| `Series.apply` | per-value Python functions |
| `DataFrame.apply` | column/row-wise; axis matters |
| `df.map` | element-wise whole-frame |
| `pipe` | readable chained transforms |
| performance ladder | vectorized > map > apply > loop |

Custom transformations are where pipelines earn their logic — and their
runtime. Choose the leftmost tool that works, and the pipeline stays both
correct and fast.

## Quick Reference

| Task | Idiom |
|------|-------|
| Remap dict | `s.map({...})` |
| Remap with default | `s.map(m).fillna(default)` |
| Per-value function | `s.apply(fn)` |
| Per-column stats | `df.apply(np.max, axis=0)` |
| Per-row logic | `df.apply(fn, axis=1)` (avoid in hot paths) |
| Element-wise | `df.map(fn)` |
| Chain functions | `df.pipe(fn, **kwargs)` |

## Next Steps

Next: **[13-categorical-data](13-categorical-data-lecture.md)** — encoding and the category dtype.
Continues in: **[07-machine-learning — 31 feature engineering](../../../../07-machine-learning/lectures/31-feature-engineering-lecture.md)**.
Official docs: https://pandas.pydata.org/docs/user_guide/basics.html#iteration
