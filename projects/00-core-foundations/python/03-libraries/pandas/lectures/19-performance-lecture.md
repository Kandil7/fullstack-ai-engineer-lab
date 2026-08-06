# Pandas Performance: Optimization, Memory, Best Practices

> **Topic 19 — Advanced pandas series.** Making pandas fast and lean:
> vectorization, dtype tuning, memory measurement, and the habits that keep
> pipelines snappy at scale.

Companion exercise: `advanced/19-performance.py`

---

## 1. The Golden Rule: Vectorize

Pandas operations on whole Series run in **compiled C**; Python loops run one
interpreted step per element. Never loop over rows when a vectorized form
exists.

```python
import numpy as np
import pandas as pd

n = 1_000_000
df = pd.DataFrame({"a": np.random.rand(n), "b": np.random.rand(n)})

# Fast — vectorized
df["c"] = df["a"] * df["b"] + 1

# Slow — element-wise loop
df["c"] = [a * b + 1 for a, b in zip(df["a"], df["b"])]

# Slowest — itertuples/iterrows
for row in df.itertuples():
    pass
```

**Measured speedups**: vectorized vs `iterrows` is typically **100–1000×**.

## 2. Efficient Row Iteration (When You Must)

If a transformation genuinely can't be vectorized, use the least-worst options:

```python
# itertuples: namedtuple per row — ~10× faster than iterrows
for row in df.itertuples(index=False):
    use(row.a, row.b)

# .apply(axis=1) with raw=True: NumPy array instead of Series
df["score"] = df.apply(compute_score, axis=1, raw=True)

# Vectorize the inner work anyway: build a list, assign once
df["new"] = [f(a, b) for a, b in zip(df["a"], df["b"])]
```

## 3. Memory: The `category` dtype Is Your Friend

String columns repeat values — the `category` dtype stores each unique string
once:

```python
df["region"] = df["region"].astype("category")
df["plan"] = df["plan"].astype("category")

print(df.memory_usage(deep=True))  # collapsed vs object columns
```

For high-cardinality-but-repeating columns (region, plan, device, status) this
can shrink memory 10–50×.

## 4. Measure Before You Optimize

```python
# Size of each column
df.memory_usage(deep=True)

# Fast timing in a notebook / script
%timeit df["a"] + df["b"]                      # (IPython)
import time; t0 = time.perf_counter(); df["a"] + df["b"]; print(time.perf_counter() - t0)
```

Optimize the columns that are actually large — guessing wastes effort.

## 5. dtype Tuning

```python
# Downcast numeric columns (64-bit -> 32/16-bit when values fit)
df["id"] = pd.to_numeric(df["id"], downcast="unsigned")
df["score"] = pd.to_numeric(df["score"], downcast="float")

# int vs float: integers where possible (less memory, faster)
# bool dtype for flags (1 byte vs 8)
df["is_vip"] = df["is_vip"].astype(bool)
```

## 6. I/O & Algorithmic Habits

- **Read only what you need**: `usecols=[...]`, `parse_dates` only the date
  columns, `nrows=` for exploration.
- **Parquet over CSV**: `to_parquet`/`read_parquet` is faster to read and far
  smaller on disk.
- **Avoid `apply` in hot loops**: `groupby.transform` and `groupby.agg` with
  named aggregations are C-accelerated.
- **`inplace` is not faster** — it's a readability choice, not a speed win.
- **Merge on sorted/unique keys**: set the join key as the index when possible.

## 7. Real-World Use Case — Wide Log Data

```python
# A 50M-row clickstream that must stay on one box
df = pd.read_parquet("events.parquet")

# 1. Compress high-cardinality strings
for col in ["page", "country", "browser"]:
    df[col] = df[col].astype("category")

# 2. Downcast numerics
df["user_id"] = pd.to_numeric(df["user_id"], downcast="unsigned")
df["session_ms"] = pd.to_numeric(df["session_ms"], downcast="float")

# 3. Vectorized derived features
df["is_mobile"] = df["browser"].isin(["android", "ios"])

# 4. Grouped aggregation instead of loops
by_page = df.groupby("page", observed=True).agg(
    users=("user_id", "nunique"),
    avg_ms=("session_ms", "mean"),
)

print(df.memory_usage(deep=True).sum() / 1e6, "MB")
```

## Key Takeaways

1. **Vectorize first** — 100–1000× wins over loops.
2. Use `itertuples`/`raw=True` only when a loop is unavoidable.
3. `category` dtype + downcasting slash memory usage dramatically.
4. Measure with `memory_usage`/`%timeit` before optimizing blindly.
5. Choose formats (Parquet) and reads (`usecols`) that minimize work.
