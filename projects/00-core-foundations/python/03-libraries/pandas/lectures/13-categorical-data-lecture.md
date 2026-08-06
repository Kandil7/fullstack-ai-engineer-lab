# Pandas Categorical Data

> **Topic 13 — Advanced pandas series.** The `category` dtype, `get_dummies`,
> and `factorize` — how to store, analyze, and encode categorical data like a
> production data engineer.

Companion exercise: `advanced/13-categorical-data.py`

---

## 1. Why Categoricals Matter

Categorical data (gender, country, product category, device type) appears in
almost every real dataset. Storing it as plain `object` strings wastes memory
and hides the fact that only a small fixed set of values is possible.

The `category` dtype stores the **unique values once** and references them by
**integer code**:

- **Memory savings** — often 10–50× smaller than `object` columns.
- **Semantic meaning** — pandas knows the allowed values and their order.
- **Better analysis** — `value_counts`, sorting, and grouping respect the
  category structure.

### Memory comparison

```python
import pandas as pd
import numpy as np

values = np.random.choice(["low", "medium", "high"], size=1_000_000)
s_obj = pd.Series(values)
s_cat = s_obj.astype("category")

print(s_obj.memory_usage(deep=True))  # ~64 MB (each string stored repeatedly)
print(s_cat.memory_usage(deep=True))  # ~1 MB (codes + 3 unique strings)
```

## 2. Creating & Managing Categoricals

```python
df = pd.DataFrame({"region": ["north", "south", "north", "east", "south"]})

# Convert to categorical
df["region"] = df["region"].astype("category")

# Inspect
df["region"].dtype                     # CategoricalDtype
df["region"].cat.categories            # Index(['east', 'north', 'south'], dtype='object')
df["region"].cat.codes                 # integer codes (0 = 'east', ...)
```

Key `cat` accessor methods:

- `astype("category")` — convert a column.
- `cat.categories` — the set of unique values.
- `cat.codes` — the underlying integer codes.
- `cat.set_categories([...])` — declare the **full** allowed set (great for
  keeping `low/medium/high` even when a category is absent in a subset).
- `cat.rename_categories({...})` — relabel values in place.
- `cat.add_categories / remove_categories` — maintain the allowed set.
- **Ordered categories** — `pd.Categorical(values, categories=[...], ordered=True)`
  enables `<`, `>`, and meaningful `min/max` comparisons.

### Ordered categoricals power ranking logic

```python
status = pd.Categorical(
    ["active", "new", "banned", "new"],
    categories=["new", "active", "banned"],
    ordered=True,
)
print(status < "banned")  # True True True True — ordering is meaningful
```

## 3. Encoding Categoricals for Machine Learning

ML models need numbers. Three standard encodings:

### a) One-hot encoding — `pd.get_dummies`

```python
df = pd.DataFrame({"color": ["red", "blue", "green", "red"]})
encoded = pd.get_dummies(df["color"], prefix="color")
#    color_blue  color_green  color_red
# 0           0            0          1
# 1           1            0          0
# 2           0            1          0
# 3           0            0          1
```

Use `dtype=float`/`dtype=int` to control output type and `drop_first=True`
to avoid the dummy-variable trap (perfect multicollinearity).

### b) Integer / label encoding — `factorize`

```python
codes, uniques = pd.factorize(df["color"])
# codes:   array([0, 1, 2, 0])
# uniques: Index(['red', 'blue', 'green'])
```

`factorize` maps each unique value to an integer code — compact, but the model
may wrongly treat the integers as ordered. Only use when the category is
**ordinal** or when a tree model can recover splits anyway.

### c) Ordinal encoding — `cat.codes`

For genuinely ordered categories (t-shirt size, rating tier), encode via the
ordered categorical's codes so the numeric order matches the semantic order.

## 4. Real-World Use Case — User Acquisition Analysis

```python
df = pd.DataFrame({
    "user_id": range(1, 1001),
    "plan": np.random.choice(["free", "pro", "enterprise"], 1000, p=[0.7, 0.25, 0.05]),
    "region": np.random.choice(["emea", "amer", "apac"], 1000),
})

# 1. Compact storage
df["plan"] = df["plan"].astype("category")
df["region"] = df["region"].astype("category")

# 2. Declare the full category set so counts include zeros
df["plan"] = df["plan"].cat.set_categories(["free", "pro", "enterprise"])

# 3. Clean conversion rates per plan
conversion = df.groupby("plan", observed=True)["user_id"].count() / len(df)

# 4. Feature for an ML model — one-hot the region
features = pd.get_dummies(df, columns=["region"], dtype=int)

# 5. Ordered tier as an ordinal feature
tier = pd.Categorical(df["plan"], categories=["free", "pro", "enterprise"], ordered=True)
df["tier_code"] = tier.codes
```

## 5. Pitfalls to Avoid

- **`observed` warning**: with pandas ≥ 1.5, `groupby` on categoricals defaults
  to `observed=False` (include empty categories). Pass `observed=True` for
  smaller, faster groups unless you explicitly want zero-count groups.
- **Never `factorize` blindly**: it assigns codes by first-seen order, which is
  arbitrary. Use explicit `categories=[...]` for ordinals.
- **Watch the dummy-variable trap**: when adding an intercept, drop one dummy
  column (`drop_first=True`) or the model matrix becomes singular.
- **Converting back**: `.astype(object)` or `.astype(str)` returns the labels,
  handy before exporting to CSV/JSON.

## Key Takeaways

1. `category` dtype = unique values + integer codes → big memory savings and
   richer semantics.
2. Ordered categoricals give you meaningful comparisons and ranking.
3. `get_dummies` for one-hot, `factorize` for quick integer labels, ordered
   `codes` for genuine ordinals.
4. Declare full category sets (`set_categories`) to keep zero-count groups
   visible in reports.
