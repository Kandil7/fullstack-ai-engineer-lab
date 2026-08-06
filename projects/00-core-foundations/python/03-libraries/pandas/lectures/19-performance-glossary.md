# Performance — Glossary

> Companion reference for the **Pandas Performance** lecture. Reach for it
> while working through `advanced/19-performance.py`.

## Vectorization

- **Vectorized operation**: A whole-Series operation executed in compiled C — the default way to transform data.
- **`iterrows()`**: Row iteration returning Series per row — the slowest iteration method; avoid.
- **`itertuples()`**: Row iteration returning namedtuples — ~10× faster than `iterrows`, use when a loop is unavoidable.
- **`.apply(func, axis=1, raw=True)`**: Row-wise apply passing raw NumPy arrays instead of Series — faster row loops.
- **List comprehension + assign once**: `df["new"] = [f(a, b) for a, b in zip(...)]` — often the fastest Python-level loop.

## Memory

- **`df.memory_usage(deep=True)`**: Per-column memory including the underlying object data.
- **`category` dtype**: Stores unique strings once + integer codes; 10–50× smaller for repeating strings.
- **Downcasting**: `pd.to_numeric(col, downcast="unsigned"|"float"|"integer")` — shrink 64-bit columns to fit.
- **`bool` dtype**: 1 byte per flag vs 8 for `int64`.
- **`astype`**: Explicit dtype conversion (`float32`, `uint32`, `bool`, `category`).

## Habits

- **`usecols`**: Read only needed columns.
- **`nrows=`**: Preview first N rows.
- **Parquet**: `to_parquet`/`read_parquet` — compressed, fast, dtype-preserving.
- **`groupby.agg(...)` named aggregations**: C-accelerated grouped math; prefer over `apply`.
- **`%timeit`**: IPython magic for measuring expression speed.
- **`inplace=`**: Readability choice, **not** a speed optimization.
- **`isin`**: Vectorized membership test — `df[df["col"].isin(values)]`.

## Real-World Patterns

- **Clickstream compression**: `category` on page/country/browser + downcast IDs + vectorized `isin` flags.
- **Merge on index keys**: faster than merging on unindexed columns.
