# Memory Optimization — Glossary 40 (pandas)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `memory_usage(deep=True)` | Method | True byte count including string/object payloads |
| downcast | Concept | Choosing the smallest dtype that holds the data |
| `pd.to_numeric(downcast=)` | Function | Range-aware int/float narrowing |
| `category` dtype | Type | Unique labels stored once + integer codes per row |
| cardinality | Concept | Number of distinct values in a column |
| `nunique()` | Method | Count of distinct values |
| `int8` … `int64` | Type | Integer widths; 1-8 bytes per cell |
| `float32` | Type | Half-size float; rounds at ~1e-7 relative |
| `float64` | Type | Default float; 8 bytes, full precision |
| `object` dtype | Type | Python-object column; ~50+ bytes per string cell |
| `chunksize` | Parameter | Rows per chunk in `read_csv`; bounds peak memory |
| streaming aggregation | Pattern | Accumulate per-chunk stats without full materialization |
| `pd.concat` | Function | Combines chunk frames into one |
| audit pass | Pattern | Measuring every column before optimizing |
| optimization pass | Pattern | The reviewed copy->downcast->categorize function |
| value preservation | Concept | Verification that optimization changed no values |

## Detailed Definitions

### audit pass
**Definition**: The first step of any memory work: `memory_usage(deep=True)`
per column, before touching dtypes, so the optimization has a measured
baseline.
**Example**:
```python
waste.memory_usage(deep=True)
```
**Complexity**: O(n) with a deep walk.
**Related**: optimization pass, `memory_usage(deep=True)`

### cardinality
**Definition**: The number of distinct values in a column. Low cardinality
(few distinct) is the condition under which `category` pays off.
**Related**: `nunique()`, `category` dtype

### `category` dtype
**Definition**: A compressed representation storing each distinct label once
plus an integer code per row — dramatically smaller for repeated labels,
worse for high-cardinality text.
**Example**:
```python
df["tier"].astype("category")
```
**Complexity**: O(n) to build; O(1) per lookup.
**Related**: cardinality, `object` dtype

### `chunksize`
**Definition**: `read_csv(..., chunksize=K)` returns an iterator of K-row
frames. Peak memory is O(K) regardless of file size.
**Example**:
```python
for chunk in pd.read_csv("huge.csv", chunksize=100_000):
    process(chunk)
```
**Complexity**: O(K) peak space.
**Related**: streaming aggregation

### downcast
**Definition**: Converting a column to the smallest dtype that still holds
every value — int64 to int32/int16/int8, float64 to float32. Same values,
fewer bytes.
**Related**: `pd.to_numeric(downcast=)`, `float32`

### `float32`
**Definition**: 32-bit float — half the memory of float64, with relative
rounding around 1e-7. Fine for most ML features; not for money or exact IDs.
**Related**: `float64`, downcast

### `float64`
**Definition**: The default float dtype, 8 bytes per cell, full double
precision. The safe default; the memory optimization is deciding when
float32 is acceptable.
**Related**: `float32`, downcast

### `int8` … `int64`
**Definition**: Integer widths from 1 to 8 bytes. pandas infers int64 by
default; `downcast="integer"` picks the smallest that fits the range.
**Related**: downcast, `pd.to_numeric(downcast=)`

### `memory_usage(deep=True)`
**Definition**: Per-column byte counts including object payloads — the only
honest measurement for string columns. Plain `memory_usage()` counts only
pointers.
**Example**:
```python
df.memory_usage(deep=True).sum()
```
**Complexity**: O(n), deep walk for objects.
**Related**: audit pass, `object` dtype

### `nunique()`
**Definition**: Count of distinct values in a column — the numerator of the
cardinality heuristic (`nunique() / len(df) < 0.1`).
**Related**: cardinality, `category` dtype

### `object` dtype
**Definition**: A column of Python objects (usually strings). Flexible but
expensive: each cell is a pointer plus a 50+ byte string payload, and every
op pays Python overhead.
**Related**: `category` dtype, `memory_usage(deep=True)`

### optimization pass
**Definition**: The reviewed, reusable function that copies a frame and
right-sizes every column: downcast ints/floats, categorize low-cardinality
strings, leave booleans alone.
**Example**:
```python
def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_integer_dtype(out[col].dtype):
            out[col] = pd.to_numeric(out[col], downcast="integer")
        ...
    return out
```
**Complexity**: O(n) per column.
**Related**: audit pass, value preservation

### `pd.concat`
**Definition**: Combines a sequence of frames into one — the combine phase of
the chunked-read pattern.
**Example**:
```python
pd.concat(pd.read_csv(f, chunksize=250), ignore_index=True)
```
**Related**: `chunksize`

### `pd.to_numeric(downcast=)`
**Definition**: Parses/narrows to the smallest compatible numeric dtype;
`downcast="integer"` or `"float"`.
**Example**:
```python
pd.to_numeric(df["score"], downcast="float")
```
**Complexity**: O(n).
**Related**: downcast, `float32`

### streaming aggregation
**Definition**: Accumulating per-chunk sums/counts across chunked reads so
peak memory is bounded while the result equals the full-frame computation.
**Example**:
```python
total = count = 0.0
for chunk in pd.read_csv(f, chunksize=100_000):
    total += chunk["y"].sum(); count += chunk["y"].count()
mean = total / count
```
**Related**: `chunksize`

### value preservation
**Definition**: The verification contract after any dtype pass: ints, bools,
and categories compare equal value-for-value; floats stay within float32
rounding of the originals.
**Related**: optimization pass, `float32`

## Key Concepts Summary

### Measurement
- `memory_usage()` = pointers only; `deep=True` = the truth
- Audit before optimizing; re-audit after

### Dtype selection
- Downcast numerics to the smallest safe width
- `category` wins below ~10% cardinality, loses above
- float32 rounds at ~1e-7 — a policy decision, not free lunch

### Big-file access
- `chunksize` bounds peak memory to one chunk
- Streamed sums/counts reproduce full-frame results

### Verification
- Values must survive: exact for int/bool/category, tolerance for floats
- `.equals()` lies across dtypes; compare values

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `memory_usage(deep=True)` — ___
2. downcast — ___
3. `category` dtype — ___
4. cardinality — ___
5. `chunksize` — ___
6. `float32` — ___
7. optimization pass — ___
8. streaming aggregation — ___

A. Number of distinct values in a column
B. Smallest dtype that still holds all values
C. True bytes including string payloads
D. Bounds peak memory to K rows
E. Rounds at ~1e-7 relative
F. Labels stored once + integer codes
G. Per-chunk accumulation without full materialization
H. The reviewed copy/downcast/categorize function

**Answers:** 1-C, 2-B, 3-F, 4-A, 5-D, 6-E, 7-H, 8-G
