# Pandas MultiIndex: Hierarchical Indexing, xs, swaplevel

> **Topic 18 — Advanced pandas series.** Multi-level indexes for complex data:
> building them, selecting with `.xs`, reordering with `swaplevel`, and
> unstacking for analysis.

Companion exercise: `advanced/18-multiindex.py`

---

## 1. What Is a MultiIndex?

A MultiIndex is a **hierarchical index**: rows (or columns) are identified by
a tuple of keys instead of a single label. Perfect for data with natural
grouping — `(region, store)`, `(year, month)`, `(customer, order)`.

```python
import pandas as pd

df = pd.DataFrame(
    {"sales": [120, 90, 200, 150, 80, 60]},
    index=pd.MultiIndex.from_tuples(
        [("north", "Boston"), ("north", "NYC"),
         ("south", "Atlanta"), ("south", "Miami"),
         ("west", "Seattle"), ("west", "LA")],
        names=["region", "city"],
    ),
)
#                 sales
# region city
# north  Boston    120
#        NYC        90
# south  Atlanta   200
#        Miami     150
# west   Seattle    80
#        LA         60
```

## 2. Building MultiIndexes

```python
# From tuples
idx = pd.MultiIndex.from_tuples([("a", 1), ("a", 2), ("b", 1)], names=["let", "num"])

# From product of levels
idx = pd.MultiIndex.from_product([["north", "south"], ["Q1", "Q2"]], names=["region", "quarter"])

# From arrays (column-wise)
idx = pd.MultiIndex.from_arrays([["a", "a", "b"], [1, 2, 1]])

# From a grouped frame
grouped = df.groupby(["region", "city"], as_index=True).sum()  # group keys become the index

# set_index / reset_index convert columns <-> index
df2 = raw.set_index(["region", "city"])
df2 = df2.reset_index()
```

## 3. Selecting with `.xs` (cross-section)

`.xs` grabs a **single level's slice across all remaining levels** — the
cleanest way to query a MultiIndex:

```python
# All rows for region "north"
df.xs("north", level="region")

# All rows where quarter = "Q2" (works on columns too)
df.xs("Q2", level="quarter", axis=1)

# Drop the level from the result
df.xs("north", level="region", drop_level=False)
```

Compare with `.loc`:

```python
df.loc[("north", "Boston")]        # exact tuple — must be fully specified
df.loc["north"]                    # partial — works if level order matches
df.loc[("north", slice(None))]     # explicit "all" for deeper levels
```

## 4. Reordering & Swapping Levels

```python
# Swap the order of levels (both index levels)
swapped = df.swaplevel(0, 1)

# Sort by the new order — required for slicing
swapped = swapped.sort_index()

# Reorder levels arbitrarily
df.reorder_levels(["city", "region"])
```

`swaplevel` + `sort_index` is the standard trick before slicing on a
previously-outer level.

## 5. Stack / Unstack — Reshaping

```python
# unstack: move the innermost index level into columns
wide = df.unstack()          # cities become columns
# sales
# city    Atlanta  Boston  LA  Miami  NYC  Seattle
# region
# north      NaN     120  NaN    NaN   90      NaN
# south      200     NaN  NaN    150  NaN      NaN
# west        NaN     NaN   60    NaN  NaN       80

# stack: move columns back into the index
long = wide.stack()

# unstack(level=0) / stack(level=0) control which level moves
```

## 6. Real-World Use Case — Regional Sales Cube

```python
df = pd.read_csv("sales.csv")
pivot = df.groupby(["region", "month", "channel"])["revenue"].sum()

# North vs South by channel
north = pivot.xs("north", level="region")
north.unstack()          # channels as columns, months as rows

# Quarter-over-quarter comparison
quarterly = pivot.unstack(level="month").T.swaplevel().sort_index()

# Ranking within each region
rank = pivot.groupby(level="region").rank(ascending=False)
```

## 7. Pitfalls to Avoid

- **Slice requires sorted levels**: `df.loc["north":"south"]` and partial
  slicing raise/silently misbehave on unsorted indexes — call `sort_index()`.
- **`df.loc["north"]` works only when "north" is the **outermost** level** —
  otherwise use `.xs(..., level="region")`.
- **`reset_index` on a huge index is slow** — prefer `droplevel` when you only
  need to drop a level.
- **Groupby vs MultiIndex**: `as_index=False` keeps group keys as columns; the
  default makes them the index. Pick deliberately.

## Key Takeaways

1. MultiIndex = hierarchical tuples; build with `from_tuples/from_product/from_arrays` or `set_index`.
2. `.xs(..., level=...)` is the query tool — single-level slicing across all others.
3. `swaplevel` + `sort_index` reorders; `unstack`/`stack` reshapes between long and wide.
4. Keep indexes sorted before any `.loc` slicing.
