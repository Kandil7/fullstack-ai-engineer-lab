# MultiIndex — Glossary

> Companion reference for the **MultiIndex** lecture. Reach for it while
> working through `advanced/18-multiindex.py`.

## Core Concepts

- **MultiIndex**: A hierarchical index where each row/column key is a tuple of labels across named *levels*.
- **Level**: One dimension of the hierarchy (e.g. `region`, `city`, `quarter`).
- **`pd.MultiIndex.from_tuples(list, names=...)`**: Build from a list of tuples.
- **`pd.MultiIndex.from_product([[...],[...]], names=...)`**: Build from the Cartesian product of level values — great for complete grids.
- **`pd.MultiIndex.from_arrays([[...],[...]])`**: Build column-wise from parallel arrays.
- **`df.set_index(["a", "b"])`**: Promote columns into a MultiIndex.
- **`df.reset_index()`**: Move index levels back into columns.

## Selection

- **`df.xs(label, level="name")`**: Cross-section — all rows for one level's label, across all other levels.
- **`df.xs(label, level="name", drop_level=False)`**: Keep the level in the result.
- **`df.xs(label, level="name", axis=1)`**: Apply to a MultiIndex on columns.
- **`df.loc[("a", 1)]`**: Exact-tuple selection — all levels must be specified.
- **`df.loc["a"]`**: Partial selection — works only for the **outermost** level.
- **`df.loc[("a", slice(None))]`**: Explicit "all values" for a deeper level.
- **Slicing rule**: `.loc["a":"b"]`-style slices require a **sorted** index — call `sort_index()` first.

## Reordering & Reshaping

- **`df.swaplevel(0, 1)`**: Swap two levels of the index.
- **`df.reorder_levels(["city", "region"])`**: Reorder levels arbitrarily.
- **`df.sort_index()`**: Sort by all levels — prerequisite for slicing.
- **`df.unstack(level=...)`**: Pivot the innermost (or given) index level into columns (long → wide).
- **`df.stack(level=...)`**: Move columns back into the index (wide → long).
- **`df.droplevel("name")`**: Drop a level without the cost of `reset_index`.

## Real-World Patterns

- **Data cubes**: `groupby(["region", "month", "channel"]).sum()` → pivot with `unstack`.
- **Within-group ranking**: `pivot.groupby(level="region").rank(ascending=False)`.
- **Cross-sectional reports**: `.xs("north", level="region")` then `unstack()` for channels-as-columns.
