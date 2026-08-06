# Inspecting Data — Glossary 01 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `df.head()` | Method | First n rows (default 5) |
| `df.tail()` | Method | Last n rows |
| `df.shape` | Attribute | (rows, columns) tuple |
| `df.dtypes` | Attribute | Series of column dtypes |
| `df.select_dtypes` | Method | Filter columns by dtype |
| `df.info()` | Method | Non-null counts + dtypes + memory |
| `df.describe()` | Method | Summary statistics for numeric (or all) columns |
| `df.nunique()` | Method | Unique value counts per column |
| `value_counts()` | Method | Frequency table for a Series |
| `isna()` | Method | Missing-value mask |
| `memory_usage()` | Method | Bytes used per column |
| `object` dtype | Concept | Python-object column (usually strings) |
| `category` dtype | Concept | Compressed repeated labels |
| cardinality | Concept | Number of distinct values |
| class balance | Concept | Proportion of each target class |
| missing fraction | Concept | `isna().mean()` — share of missing values |

## Detailed Definitions

### `df.head()`
**Definition**: Returns the first n rows (default 5) — the quick look at
structure and sample values.
**Example**:
```python
df.head(3)   # first three rows
```
**Related**: `df.tail()`

### `df.tail()`
**Definition**: Returns the last n rows; useful when rows are time-ordered and
the newest are at the end.
**Related**: `df.head()`

### `df.shape`
**Definition**: A `(rows, columns)` tuple held as metadata — O(1), the first
sanity check on any frame.
**Example**:
```python
df.shape   # (100_000, 12)
```
**Related**: `df.ndim`

### `df.dtypes`
**Definition**: A Series mapping column names to their dtype — the type
contract that determines every downstream operation.
**Related**: `select_dtypes`, `object` dtype

### `df.select_dtypes`
**Definition**: Returns a sub-frame of columns whose dtype matches
`include=`/`exclude=`.
**Example**:
```python
df.select_dtypes(include=["number", "bool"])
```
**Related**: `df.dtypes`

### `df.info()`
**Definition**: Prints index info, per-column non-null counts, dtypes, and
estimated memory — the combined intake view.
**Related**: `memory_usage()`, missing fraction

### `df.describe()`
**Definition**: Computes count/mean/std/min/quartiles/max for numeric columns;
use `include="object"` for categorical summaries (count, unique, top, freq).
**Related**: skew, outliers

### `df.nunique()`
**Definition**: Number of distinct values per column — the cardinality probe
that drives encoding decisions.
**Example**:
```python
df.nunique()   # label: 2, sentence: 1000, score: 997
```
**Related**: `value_counts()`, cardinality

### `value_counts()`
**Definition**: Frequency (and with `normalize=True`, proportion) of each
distinct value in a Series.
**Example**:
```python
df["label"].value_counts(normalize=True)
```
**Related**: class balance

### `isna()`
**Definition**: Element-wise mask of missing values; `.sum()` gives per-column
counts, `.mean()` gives fractions.
**Example**:
```python
df.isna().mean()   # missing fraction per column
```
**Related**: missing fraction

### `memory_usage()`
**Definition**: Bytes per column; `deep=True` includes the object payloads
(Python strings cost ~50 B each).
**Related**: `df.info()`

### `object` dtype
**Definition**: Columns of Python objects — typically strings; slow and
un-vectorized compared to dedicated dtypes.
**Related**: `category` dtype, dtypes

### `category` dtype
**Definition**: Categorical dtype compressing repeated labels to integer codes
— smaller and faster for high-cardinality-but-few-unique columns.
**Related**: `object` dtype

### cardinality
**Definition**: The number of distinct values in a column; drives encoding:
low -> one-hot/category, high -> embeddings/frequency.
**Related**: `nunique()`

### class balance
**Definition**: The proportion of each class in a target column; imbalance
changes evaluation and training strategy.
**Related**: `value_counts(normalize=True)`

### missing fraction
**Definition**: The share of missing values per column (`isna().mean()`);
0.01 vs 0.9 demand different handling.
**Related**: `isna()`

## Key Concepts Summary

### The five intake commands
- `df.head()` / `df.tail()` — sample rows
- `df.shape` — dimensions
- `df.dtypes` — type contract
- `df.info()` — non-null counts + memory
- `df.describe()` — distributions

### Cardinality and balance
- `nunique()` — how many distinct values
- `value_counts(normalize=True)` — class proportions
- both decide encoding and evaluation strategy

### Missing data
- `isna().sum()` — counts
- `isna().mean()` — fractions (the decision input)

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `df.shape` — ___
2. `df.describe()` — ___
3. `df.nunique()` — ___
4. `value_counts(normalize=True)` — ___
5. `isna().mean()` — ___
6. `select_dtypes` — ___
7. `category` dtype — ___
8. `memory_usage(deep=True)` — ___

A. (rows, columns) metadata
B. Missing fraction per column
C. Unique count per column
D. Filter columns by dtype
E. Compressed repeated labels
F. Class proportions
G. Summary statistics
H. True bytes including string payloads

**Answers:** 1-A, 2-G, 3-C, 4-F, 5-B, 6-D, 7-E, 8-H
