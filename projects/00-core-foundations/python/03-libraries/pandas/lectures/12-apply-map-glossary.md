# Apply / Map / Vectorize — Glossary

> Companion reference for the **Apply, Map & Vectorize** lecture. Terms are
> organized by concept — reach for this glossary while working through the
> companion exercise `advanced/12-apply-map.py`.

## Element-wise Operations

- **Element-wise (vectorized) operation**: An operation applied simultaneously to every element of a Series, implemented in compiled C code — no Python loop. This is the *default* way to transform columns in pandas.
- **Vectorization**: Expressing a transformation as operations on whole arrays instead of per-element Python loops. Typically 10–100× faster than `apply` and the single most important pandas performance habit.

## Mapping & Transforming

- **`Series.map(dict_or_callable)`**: Element-wise transform of one Series. With a `dict`, values are looked up (missing keys become `NaN`); with a callable, it is applied to each element. Returns a **new** Series.
- **`Series.apply(callable)`**: Apply a function to each element (or, with `axis=1` on a DataFrame, to each row). Slower than vectorized ops and `map` because the function runs in Python.
- **`DataFrame.apply(func, axis=0|1)`**: `axis=0` (default) applies `func` to each **column**; `axis=1` applies it to each **row**. Use `axis=1` sparingly — row-wise `apply` with a lambda is the slowest common pandas pattern.
- **`DataFrame.applymap(func)`**: Apply a function element-wise to **every cell** of a DataFrame (values only, not index/columns). Deprecated in pandas 2.1+ in favor of `DataFrame.map`.
- **`DataFrame.map(func)`**: The modern (pandas ≥ 2.1) replacement for `applymap` for element-wise DataFrame transformations.

## Group-level Transforms

- **`DataFrame.groupby(keys).transform(func)`**: Apply `func` **within each group** and return a result *aligned to the original index* — same shape as the input. Perfect for "subtract the group mean" or "fill NaN with the group median".
- **`DataFrame.groupby(keys).apply(func)`**: Apply `func` to each group **as a whole**, returning a reduced or transformed result whose shape depends on `func`. `transform` and `agg` are usually more predictable.

## Function Utilities

- **`functools.partial(func, ...)`**: Pre-fill some of `func`'s arguments, returning a callable that takes the rest. Great for passing column values plus a fixed constant/configuration into `apply` or `map`.
- **Lambda**: An inline anonymous function (`lambda x: x * 2`). Convenient, but for anything non-trivial prefer a named function — it is testable, readable, and reusable.
- **`pd.cut(values, bins, labels=...)`**: Bin continuous values into discrete intervals (buckets) — e.g., ages into `0-18`, `19-35`, `36+`. Returns a categorical Series, ideal for `value_counts`, charts, or feature engineering.
- **`pd.qcut(values, q, labels=...)`**: Bin into **quantile-based** buckets, so each bucket holds (approximately) the same number of observations. Prefer when you want balanced groups regardless of distribution shape.

## Performance Concepts

- **Vectorized wins**: arithmetic (`df["a"] + df["b"]`), comparisons, `str`/`dt` accessors — all compiled. Reach for `map` when a dict lookup is needed, `apply` only when no vectorized/map option exists, and `axis=1` row-wise `apply` as a last resort.
- **`raw=True`**: In `DataFrame.apply`, pass `raw=True` so the function receives a raw NumPy array row/column instead of a Series — shaves the Series construction overhead and can speed up row-wise ops noticeably.
- **Caching results**: If the same `apply` result is needed in several places, compute once into a column/variable instead of re-running the loop.

## Real-World Patterns

- **Unit conversions**: `df["price_usd"] = df["price_eur"].map(EUR_TO_USD)` with a lookup dict.
- **Categorical labeling**: `df["bucket"] = pd.cut(df["age"], bins=[0, 18, 35, 65, 120])`.
- **Row-level business logic**: `df.apply(compute_risk_score, axis=1, raw=True)` for a complex scoring rule that cannot be expressed with vectorized ops.
- **Group-normalized features**: `df["zscore"] = df.groupby("store")["sales"].transform(lambda s: (s - s.mean()) / s.std())`.
