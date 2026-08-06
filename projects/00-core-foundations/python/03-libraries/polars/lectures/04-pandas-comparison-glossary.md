# pandas Comparison — Glossary 04

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| .apply() | pandas | Row/column-wise Python function application (slow path) |
| boolean mask | pandas | Filtering via `df[df["a"] > 1]` |
| groupby().agg() | pandas | Grouped aggregation via a dict of column->function |
| .iloc / .loc | pandas | Positional / label indexing; absent in Polars |
| inplace=True | pandas | Mutating argument; returns None, cannot chain |
| merge() | pandas | pandas join: `a.merge(b, on="k", how="left")` |
| pl.map_batches | polars | Batch-wise Python function application |
| parity check | Concept | Verifying two engines produce identical results |
| reset_index() | pandas | Flattens a groupby index back to columns |
| transform() | pandas | Group-aligned aggregation (window analog) |
| with_columns | polars | Pure transform: new frame, input never mutated |
| null vs NaN | Concept | Polars `null` vs pandas float `NaN` semantics |
| benchmark | Concept | Measured comparison; printed, never asserted |
| migration guide | Concept | Ordered port: idioms, applies, dtypes, nulls, parity |
| group_by().agg() | polars | Grouped aggregation via named expressions |
| .over() | polars | Window aggregate mapped back to rows |
| tz-aware series | pandas | Timezone-aware time series; pandas' strong suit |

## Detailed Definitions

### .apply()
**Definition**: pandas row- or column-wise Python function application.
Flexible but slow — Python dispatch per element. Polars has no
first-class equivalent; logic should be rewritten as expressions.
**Example**:
```python
import pandas as pd
s = pd.Series([1.0, 2.0, 3.0])
print(s.apply(lambda v: v * 2 if v > 1 else 0.0).tolist())
```
```text
[0.0, 4.0, 6.0]
```
**Complexity**: O(n) Python dispatches.
**Related**: pl.map_batches, boolean mask

### boolean mask
**Definition**: pandas filtering idiom: a boolean Series in square
brackets selects rows. Polars uses `filter(expr)` instead.
**Example**:
```python
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3]})
print(df[df["a"] > 1]["a"].tolist())
```
```text
[2, 3]
```
**Related**: filter, merge()

### groupby().agg()
**Definition**: pandas grouped aggregation taking a dict mapping output
name to (column, function). Polars uses named expressions instead of
string dicts.
**Example**:
```python
import pandas as pd
df = pd.DataFrame({"k": ["a", "b"], "v": [1, 2]})
print(df.groupby("k").agg(total=("v", "sum")).reset_index().values.tolist())
```
```text
[['a', 1], ['b', 2]]
```
**Related**: group_by().agg(), reset_index()

### .iloc / .loc
**Definition**: pandas positional and label indexing. Polars has no
index; use `.row(i)` or `filter()` instead.
**Related**: boolean mask, filter

### inplace=True
**Definition**: pandas parameter that mutates and returns None — breaks
chaining and saves nothing. Polars has no inplace; every transform
returns a new frame.
**Related**: with_columns, boolean mask

### merge()
**Definition**: The pandas join function: `a.merge(b, on="k",
how="left")`. Polars equivalent: `a.join(b, on="k", how="left")`.
**Example**:
```python
import pandas as pd
a = pd.DataFrame({"k": [1, 2], "x": [10, 20]})
b = pd.DataFrame({"k": [1, 2], "y": [100, 200]})
print(a.merge(b, on="k").shape)
```
```text
(2, 3)
```
**Related**: groupby().agg(), boolean mask

### pl.map_batches
**Definition**: Polars' boundary function for Python callables: applies
a function to whole batches instead of per element, keeping the
vectorized pipeline intact.
**Related**: .apply(), with_columns

### parity check
**Definition**: Running the same data through two implementations and
comparing outputs exactly — the verification step of any migration.
**Related**: migration guide, benchmark

### reset_index()
**Definition**: Flattens a pandas groupby index back into a normal
column; needed because pandas groupby results are indexed by group key.
Polars output is already flat.
**Related**: groupby().agg(), index

### transform()
**Definition**: pandas group-aligned aggregation returning one value per
row (e.g., group sum repeated per member). Polars equivalent:
`pl.col("v").sum().over("k")`.
**Related**: .over(), groupby().agg()

### with_columns
**Definition**: Polars transform context returning a NEW frame with
added/replaced columns; the input frame can never be mutated by a chain.
**Related**: inplace=True, transform()

### null vs NaN
**Definition**: Polars represents missing values as typed `null` in any
dtype; pandas uses float `NaN` (and `NaT` for dates). Both aggregate
identically, but equality semantics differ.
**Related**: migration guide, parity check

### benchmark
**Definition**: A measured comparison of implementations. In teaching
files: best-of-N wall-clock times, printed for the reader, never
asserted — wall-clock is not reproducible.
**Related**: parity check, migration guide

### migration guide
**Definition**: The ordered port plan: inventory idioms, isolate
applies, pin dtypes, check null semantics, verify parity, benchmark.
**Related**: parity check, null vs NaN

### group_by().agg()
**Definition**: Polars grouped aggregation taking named expressions;
same split-apply-combine as pandas but with optimizer-visible recipes.
**Related**: groupby().agg(), with_columns

### .over()
**Definition**: Polars window operator: aggregate per group, aligned
back to rows. The expression-based successor to pandas `transform()`.
**Related**: transform(), group_by().agg()

### tz-aware series
**Definition**: pandas time series with timezone metadata, backed by
mature resample rules and business calendars — one of the cases where
pandas remains the right tool.
**Related**: migration guide, benchmark

## Key Concepts Summary

### Same Ideas, Two Grammars
- Filter: boolean mask vs `filter(expr)`
- Group: `groupby().agg({...})` vs `group_by().agg(exprs)`
- Join: `merge(on=, how=)` vs `join(on=, how=)`
- New columns: assignment (mutating) vs `with_columns` (pure)

### Where the Differences Matter
- No index, no inplace, no .loc/.iloc in Polars
- apply has no first-class Polars equivalent — rewrite as expressions
- Null semantics: typed `null` vs float `NaN`

### Migration Discipline
- Verify parity on a sample before porting at scale
- Measure honestly: print, never assert wall-clock
- Keep pandas when tz time series or apply-heavy research dominate

## Practice Terms

Match each term to its definition (answers at the bottom).

1. transform() — ___
2. with_columns — ___
3. parity check — ___
4. pl.map_batches — ___
5. reset_index() — ___

A. Polars pure transform returning a new frame
B. Group-aligned aggregate; pandas window analog
C. Python function applied to whole batches in Polars
D. Flattens a pandas groupby index back to columns
E. Verifying two engines produce identical results

**Answers:** 1-B, 2-A, 3-E, 4-C, 5-D
