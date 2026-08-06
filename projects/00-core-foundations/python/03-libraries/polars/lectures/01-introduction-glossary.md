# Introduction to Polars — Glossary 01

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| Arrow | Format | Columnar, typed in-memory format shared by Polars, pandas, DuckDB |
| collect() | Method | Executes a LazyFrame plan and returns a DataFrame |
| columnar | Concept | Storage layout keeping one column's values contiguous |
| DataFrame | Type | Eager, columnar table of named, typed Series |
| dtype | Concept | Arrow type of a column (Int64, Float64, String, ...) |
| eager | Execution | Mode where every call runs immediately |
| estimated_size() | Method | In-memory footprint of a frame in bytes |
| Expr | Type | A lazy recipe for a column operation |
| height/width | Property | Row count / column count of a DataFrame |
| index | Concept | Row-label system pandas has and Polars deliberately lacks |
| lazy | Execution | Mode where calls build a plan, executed once at collect() |
| LazyFrame | Type | A query plan; not data until collected |
| row() | Method | Positional row access (`df.row(2)`) |
| scan_csv() | Function | Opens a CSV as a LazyFrame without loading data |
| schema | Property | `{column: Arrow dtype}` contract of a frame |
| Series | Type | One named, typed column |
| SIMD | Concept | Single-instruction-multiple-data CPU vectorization |
| to_numpy() | Method | Convert a Series to a NumPy array (view or copy) |
| zero-copy | Concept | Sharing buffers between tools instead of converting |

## Detailed Definitions

### Arrow
**Definition**: A cross-language columnar memory format. Polars stores
its data in Arrow buffers, which is why it can hand frames to pyarrow,
DuckDB, and PyTorch without conversion.
**Example**:
```python
import pyarrow as pa
t = pa.table({"score": pa.array([0.9, 0.4])})
print(t.schema)
```
```text
score: double
```
**Complexity**: O(1) to wrap existing buffers.
**Related**: columnar, zero-copy

### collect()
**Definition**: The LazyFrame method that executes the query plan and
returns an eager DataFrame. Everything before it is free.
**Example**:
```python
import polars as pl
lf = pl.LazyFrame({"a": [1, 2, 3]})
df = lf.filter(pl.col("a") > 1).collect()
print(df.rows())
```
```text
[(2,), (3,)]
```
**Complexity**: O(plan cost).
**Related**: lazy, LazyFrame

### columnar
**Definition**: Storage layout where each column's values live in one
contiguous buffer. Contrast with row-oriented storage where each record
is stored together.
**Related**: Arrow, SIMD

### DataFrame
**Definition**: The primary eager container: a named collection of typed
columns (Series) plus a schema. Built column-first from a dict of lists.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"id": [1, 2], "split": ["a", "b"]})
print(df.shape)
```
```text
(2, 2)
```
**Complexity**: O(n) to build.
**Related**: Series, schema

### dtype
**Definition**: The Arrow data type of a column: `Int64`, `Float64`,
`String`, `Boolean`, and friends. Types travel with the data into
Parquet and Arrow.
**Example**:
```python
import polars as pl
s = pl.Series("x", [1, 2])
print(s.dtype)
```
```text
Int64
```
**Related**: schema, Arrow

### eager
**Definition**: Execution mode where each method call runs immediately
and returns concrete data. The default for DataFrame methods.
**Related**: lazy, collect()

### estimated_size()
**Definition**: Returns the estimated in-memory size of a frame in
bytes; the number to consult before choosing eager vs streaming.
**Related**: LazyFrame, streaming

### Expr
**Definition**: A lazy, composable recipe for a column operation that
holds no data and runs only inside a context (select, with_columns,
filter, group_by.agg).
**Example**:
```python
import polars as pl
e = (pl.col("score") * 100).alias("pct")
print(type(e).__name__)
```
```text
Expr
```
**Related**: lazy, select

### height/width
**Definition**: `df.height` is the row count; `df.width` the column
count. The tuple `df.shape` gives both.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
print(df.height, df.width, df.shape)
```
```text
3 2 (3, 2)
```
**Related**: DataFrame

### index
**Definition**: The row-label system pandas builds on; Polars
deliberately has none. Rows are addressed by position (`.row(i)`) or by
predicate (`.filter(...)`).
**Related**: row(), filter

### lazy
**Definition**: Execution mode where method calls append nodes to a plan
(LazyFrame). Nothing runs until `collect()` or a sink executes it.
**Related**: LazyFrame, collect()

### LazyFrame
**Definition**: A query plan: scan + pending transformations. Not data.
Created by `df.lazy()` or `scan_*`; executed by `.collect()`.
**Example**:
```python
import polars as pl
lf = pl.LazyFrame({"a": [1, 2]})
print(type(lf).__name__)
```
```text
LazyFrame
```
**Related**: lazy, collect(), scan_csv()

### row()
**Definition**: Positional row access returning a tuple of values, in
place of pandas `iloc`.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"a": [1, 2], "b": ["x", "y"]})
print(df.row(1))
```
```text
(2, 'y')
```
**Complexity**: O(1) for a single row.
**Related**: index, filter

### scan_csv()
**Definition**: Opens a CSV file as a LazyFrame: reads the header and
metadata but no data until `collect()`. The lazy counterpart of
`read_csv()`.
**Related**: LazyFrame, lazy

### schema
**Definition**: A mapping of column names to Arrow dtypes describing a
frame's typed contract.
**Example**:
```python
import polars as pl
df = pl.DataFrame({"s": [0.5], "k": ["a"]})
print(df.schema)
```
```text
Schema({'s': Float64, 'k': String})
```
**Related**: dtype, DataFrame

### Series
**Definition**: One named, typed column — the unit of columnar work.
`df["score"]` returns a Series.
**Related**: DataFrame, dtype

### SIMD
**Definition**: CPU vectorization where one instruction processes many
values. Columnar layouts enable it because whole columns sit in
contiguous buffers.
**Related**: columnar, Arrow

### to_numpy()
**Definition**: Converts a Series to a NumPy array. With
`allow_copy=False` it returns a view when the dtype permits; strings
raise because they cannot be viewed.
**Example**:
```python
import polars as pl
import numpy as np
s = pl.Series("x", [1.0, 2.0])
arr = s.to_numpy(allow_copy=False)
print(np.shares_memory(s.to_numpy(), arr))
```
```text
True
```
**Complexity**: O(1) view or O(n) copy.
**Related**: zero-copy, Arrow

### zero-copy
**Definition**: Sharing the same memory buffers between tools (Arrow,
Polars, NumPy) instead of converting. Detected with `np.shares_memory`.
**Related**: to_numpy(), Arrow

## Key Concepts Summary

### Memory Model
- Polars stores data in Arrow columnar buffers
- Whole-column operations hit one contiguous buffer -> SIMD-friendly
- No index means no per-row label overhead

### Execution Models
- Eager: DataFrame methods run immediately
- Lazy: LazyFrame builds a plan; collect() runs it once
- Same expression syntax works in both modes

### Data Contract
- Schema maps every column to an explicit Arrow dtype
- Types travel into Parquet, Arrow, and PyTorch
- ASCII-safe inspection: `to_dict(as_series=False)`, `.rows()`

## Practice Terms

Match each term to its definition (answers at the bottom).

1. LazyFrame — ___
2. columnar — ___
3. dtype — ___
4. scan_csv() — ___
5. zero-copy — ___

A. Execution mode where calls build a plan run once at collect()
B. Opening a file as metadata-only until collected
C. Storage layout keeping column values contiguous
D. Sharing memory buffers between tools instead of converting
E. Arrow type of a column (Int64, Float64, String)

**Answers:** 1-A, 2-C, 3-E, 4-B, 5-D
