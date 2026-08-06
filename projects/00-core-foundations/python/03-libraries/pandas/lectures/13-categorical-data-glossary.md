# Categorical Data — Glossary

> Companion reference for the **Categorical Data** lecture. Reach for it while
> working through `advanced/13-categorical-data.py`.

## The Category Dtype

- **`category` dtype**: A pandas dtype that stores a fixed set of unique values (the *categories*) and references them by integer code. Cuts memory and adds semantic meaning compared to `object` strings.
- **`CategoricalDtype`**: The full dtype object; can carry `categories` and `ordered=True` explicitly.
- **`pd.Categorical(values, categories=..., ordered=...)`**: Constructor for a categorical with explicit categories and optional ordering.
- **`.astype("category")`**: Convert a column/Series to categorical dtype.
- **`cat.categories`**: The unique value set (an `Index`).
- **`cat.codes`**: The underlying integer codes referencing `categories`.
- **`cat.set_categories([...])`**: Declare the full allowed set — keeps absent categories visible in counts.
- **`cat.rename_categories({...})`**: Relabel category values.
- **`cat.add_categories / cat.remove_categories`**: Grow or shrink the allowed set.
- **`cat.as_ordered() / as_unordered()`**: Toggle ordering on an existing categorical.
- **Ordered categorical**: `ordered=True` enables `<`, `>`, `min`, `max`, `sort_values` with semantic order.
- **`observed=True|False`**: `groupby` behavior with categoricals — `False` includes empty (zero-count) categories, `True` only observed ones.

## Encoding for Machine Learning

- **`pd.get_dummies(df_or_series, prefix=..., drop_first=..., dtype=...)`**: One-hot encode categorical columns into indicator columns.
- **Dummy-variable trap**: Including all one-hot columns plus an intercept creates perfect multicollinearity — drop one column with `drop_first=True`.
- **`pd.factorize(values)`**: Map unique values to integer codes. Returns `(codes, uniques)` — codes are first-seen order, **not** semantic order.
- **Label encoding**: Assigning arbitrary integers to categories; fine for trees, dangerous for linear models (implies fake ordering).
- **Ordinal encoding**: Encoding ordered categories via `cat.codes` so integer order matches semantic order (e.g., `free < pro < enterprise`).

## Real-World Patterns

- **Memory compression**: `df[col] = df[col].astype("category")` on high-cardinality string columns can shrink a DataFrame from gigabytes to megabytes.
- **Zero-count reporting**: `set_categories` before `value_counts`/`groupby(observed=False)` keeps missing categories visible in reports.
- **Feature engineering**: one-hot low-cardinality columns with `get_dummies`, ordinal-encode ranked tiers, `factorize` high-cardinality IDs when trees are used.
