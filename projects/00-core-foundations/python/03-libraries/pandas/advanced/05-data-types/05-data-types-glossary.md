# Data Types & Conversion — Glossary 05 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| dtype | Concept | The type of a column; decides ops, memory, model input |
| `object` dtype | Type | Python-object column (strings) — slow, ~50 B/cell |
| `int64` | Type | 64-bit integer column |
| `float64` | Type | 64-bit float column (the default numeric) |
| `bool` / `boolean` | Type | Boolean; `boolean` is the nullable variant |
| `datetime64[ns]` | Type | Timestamp column (optionally timezone-aware) |
| `category` | Type | Compressed repeated labels via integer codes |
| `astype()` | Method | Explicit dtype conversion (raises on impossible) |
| `to_numeric()` | Function | Parse strings to numbers; `errors="coerce"` -> NaN |
| `to_datetime()` | Function | Parse strings to timestamps |
| `pd.NA` | Sentinel | Type-aware missing for nullable dtypes |
| `Int64` | Type | Nullable integer dtype |
| `string` dtype | Type | True pandas string dtype (vs object) |
| `.cat.codes` | Accessor | Integer codes of a categorical column |
| `.cat.categories` | Accessor | The distinct label list |
| ordered category | Concept | Categorical with a defined ordering |
| `memory_usage(deep=True)` | Method | True bytes including object payloads |

## Detailed Definitions

### dtype
**Definition**: The type attached to every pandas column — it determines which
operations work, memory cost, and what the model sees.
**Example**:
```python
df.dtypes
```
**Related**: `astype()`, memory

### `object` dtype
**Definition**: A column of Python objects, usually strings; flexible but slow
and memory-heavy (~50 B/cell vs 1-8 for real dtypes).
**Related**: `string` dtype, memory

### `int64`
**Definition**: 64-bit integer dtype; cannot hold NaN (missing forces float
unless using `Int64`).
**Related**: `Int64`

### `float64`
**Definition**: The default numeric dtype; 8 bytes/cell. `float32` halves the
memory at reduced precision.
**Related**: memory

### `bool` / `boolean`
**Definition**: Boolean columns; `boolean` is the nullable variant accepting
`pd.NA`.
**Related**: `pd.NA`

### `datetime64[ns]`
**Definition**: Timestamp dtype enabling time logic (resample, dt accessor);
can be timezone-aware as `datetime64[ns, tz]`.
**Related**: `to_datetime()`

### `category`
**Definition**: Dtype storing each unique label once and referencing it by
integer code — smaller and faster for low-cardinality repeated labels.
**Example**:
```python
df["split"] = df["split"].astype("category")
```
**Related**: `.cat.codes`, ordered category

### `astype()`
**Definition**: Explicit conversion of a column; raises on non-convertible
values — the promise form of casting.
**Example**:
```python
df["score"] = df["score"].astype("float32")
```
**Complexity**: O(n).
**Related**: `to_numeric()`

### `to_numeric()`
**Definition**: Parses strings/objects into numbers; `errors="coerce"` turns
unparseable values into NaN instead of raising.
**Example**:
```python
pd.to_numeric(df["n"], errors="coerce")
```
**Related**: `astype()`

### `to_datetime()`
**Definition**: Parses strings into `datetime64`; `format=` speeds known
layouts; errors can be coerced.
**Example**:
```python
pd.to_datetime(df["created"])
```
**Related**: `datetime64[ns]`

### `pd.NA`
**Definition**: The type-aware missing sentinel used by nullable dtypes —
unlike NaN it knows it is an integer/string/boolean missing.
**Related**: `Int64`, `string` dtype

### `Int64`
**Definition**: Nullable integer dtype — integer values WITH missing, avoiding
the silent float cast.
**Example**:
```python
pd.Series([1, 2, None], dtype="Int64")
```
**Related**: `pd.NA`

### `string` dtype
**Definition**: pandas' true string dtype (vs `object` containing str) —
proper string semantics and `pd.NA` support.
**Related**: `object` dtype

### `.cat.codes`
**Definition**: The integer code per row of a categorical column — the
numeric view ML models actually consume.
**Example**:
```python
df["split_code"] = df["split"].cat.codes
```
**Related**: `category`

### `.cat.categories`
**Definition**: The distinct labels of a categorical column, in code order.
**Related**: `category`, `.cat.codes`

### ordered category
**Definition**: A categorical with a declared `<` ordering (`categories=[...],
ordered=True`) enabling ordinal comparisons.
**Example**:
```python
pd.Categorical(x, categories=["s", "m", "l"], ordered=True)
```
**Related**: `category`

### `memory_usage(deep=True)`
**Definition**: True byte usage per column, including object payloads — the
real budget view (plain `memory_usage` misses string internals).
**Related**: dtype, memory

## Key Concepts Summary

### The type families
- Numeric: int64/float64 (+ float32 for memory)
- Boolean: bool / nullable boolean
- Time: datetime64[ns] (optionally tz-aware)
- Text: object (legacy) / string (proper)
- Categorical: category — codes, not strings

### Parsing vs casting
- `astype` — promise cast; raises on impossible input
- `to_numeric`/`to_datetime` — parse real types from strings; `coerce` dirty input
- nullable dtypes keep types alive alongside missingness

### Memory discipline
- dtype choice IS the memory budget: float32 halves, category compresses
- `memory_usage(deep=True)` is the only honest measurement for object columns

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `category` — ___
2. `to_numeric(errors="coerce")` — ___
3. `Int64` — ___
4. `.cat.codes` — ___
5. `datetime64[ns]` — ___
6. `astype("float32")` — ___
7. `pd.NA` — ___
8. `string` dtype — ___

A. Timestamp column dtype
B. Integer codes of a categorical
C. Compressed repeated labels
D. Nullable integer dtype
E. Parses with unparseable -> NaN
F. Halves numeric memory
G. Type-aware missing sentinel
H. True pandas string dtype

**Answers:** 1-C, 2-E, 3-D, 4-B, 5-A, 6-F, 7-G, 8-H
