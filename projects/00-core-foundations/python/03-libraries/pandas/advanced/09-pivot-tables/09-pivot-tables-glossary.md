# Pivot Tables & Reshaping — Glossary 09 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| reshape | Concept | Changing layout without changing content |
| `pivot()` | Method | Long -> wide; one value per cell required |
| `pivot_table()` | Method | Pivot with aggregation + filling |
| `melt()` | Method | Wide -> long (tidy); inverse of pivot |
| `id_vars` | Argument | Columns that stay as identifiers in melt |
| `var_name` / `value_name` | Arguments | Output names for melted columns |
| `stack()` | Method | Columns -> index levels |
| `unstack()` | Method | Index levels -> columns |
| tidy (long) data | Concept | One observation per row |
| wide data | Concept | One row per entity, columns per attribute |
| `fill_value=0` | Argument | Densify empty pivot cells |
| round-trip | Concept | pivot(melt(x)) == x where lossless |

## Detailed Definitions

### reshape
**Definition**: Rearranging a frame's layout (rows/columns/index) while
preserving its content — the family pivot/melt/stack/unstack.
**Related**: `pivot()`, `melt()`

### `pivot()`
**Definition**: Indexes rows by one column, spreads another into columns,
fills with a third — long to wide. Duplicate cells raise.
**Example**:
```python
df.pivot(index="user", columns="day", values="score")
```
**Related**: `pivot_table()`

### `pivot_table()`
**Definition**: The duplicate-safe pivot: aggregates repeated cells and can
fill empty ones.
**Example**:
```python
df.pivot_table(index="u", columns="day", values="v", aggfunc="mean", fill_value=0)
```
**Related**: `pivot()`, `fill_value=0`

### `melt()`
**Definition**: Unpivots columns into rows, keeping `id_vars` fixed — wide to
long, the tidy-ing operation.
**Example**:
```python
wide.melt(id_vars=["user"], var_name="day", value_name="score")
```
**Related**: `id_vars`, tidy data

### `id_vars`
**Definition**: `melt` argument listing the columns that remain as identifiers
(not melted into rows).
**Related**: `melt()`

### `var_name` / `value_name`
**Definition**: `melt` output names for the melted column-name column and the
value column.
**Related**: `melt()`

### `stack()`
**Definition**: Moves columns into an additional index level — the
MultiIndex-side of melt.
**Related**: `unstack()`

### `unstack()`
**Definition**: Moves an index level into columns — the MultiIndex-side of
pivot.
**Related**: `stack()`

### tidy (long) data
**Definition**: One observation per row — the canonical layout for groupby,
plotting, and modeling.
**Related**: `melt()`

### wide data
**Definition**: One row per entity with attributes spread across columns — for
feature matrices and reports.
**Related**: `pivot()`

### `fill_value=0`
**Definition**: `pivot_table` option replacing empty cells with a value —
correct when absence means zero.
**Related**: `pivot_table()`

### round-trip
**Definition**: Applying inverse reshapes and asserting equality —
`melt(pivot(x)) == x` for lossless layouts; the reshape safety test.
**Related**: reshape

## Key Concepts Summary

### The reshape family
- pivot / pivot_table: long -> wide
- melt: wide -> long
- stack / unstack: index <-> columns for MultiIndex levels

### Layout choice
- Long/tidy for analysis and modeling
- Wide for feature matrices and display
- Store long; pivot at the boundary

### Safety
- `pivot_table` when duplicates possible
- `fill_value=0` when absence is zero
- Round-trip tests before trusting a reshape

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `pivot()` — ___
2. `pivot_table()` — ___
3. `melt()` — ___
4. `stack()` — ___
5. `unstack()` — ___
6. `id_vars` — ___
7. tidy data — ___
8. `fill_value=0` — ___

A. Long -> wide, unique cells only
B. Wide -> long
C. Duplicate-safe pivot with aggregation
D. Columns -> index levels
E. Index levels -> columns
F. Densify empty cells
G. Columns kept as identifiers in melt
H. One observation per row

**Answers:** 1-A, 2-C, 3-B, 4-D, 5-E, 6-G, 7-H, 8-F
