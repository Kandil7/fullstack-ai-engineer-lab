# Merging & Joining — Glossary 10 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| `merge()` | Method | SQL-style join on key columns |
| `how=` | Argument | inner/left/right/outer join semantics |
| `on=` | Argument | Shared key column(s) |
| `left_on=` / `right_on=` | Arguments | Keys when names differ |
| cardinality | Concept | Row duplication from repeated keys |
| fan-out | Bug | Duplicated keys multiplying output rows |
| `join()` | Method | Index-based merge convenience |
| `concat()` | Function | Positional stacking along axis |
| `axis=0` / `axis=1` | Argument | Stack rows / attach columns |
| `ignore_index=True` | Option | Renumber the output RangeIndex |
| `combine_first()` | Method | Left wins; fill NaN from right |
| `suffixes` | Argument | `_x`/`_y` handling for colliding names |
| one-to-many | Concept | One left row matching many right rows |
| validated merge | Pattern | Merge wrapped with row-count asserts |

## Detailed Definitions

### `merge()`
**Definition**: Combines two frames on key columns with SQL join semantics —
the primary combining tool.
**Example**:
```python
users.merge(events, on="user_id", how="left")
```
**Complexity**: O(n log n) typical (hash/sort join).
**Related**: `how=`, `on=`

### `how=`
**Definition**: The join type: inner (match only), left (keep left rows),
right, outer (union of keys).
**Related**: `merge()`

### `on=`
**Definition**: Names the shared key column(s) used to match rows.
**Related**: `left_on=` / `right_on=`

### `left_on=` / `right_on=`
**Definition**: Key specifications when the two frames name the join key
differently.
**Related**: `on=`

### cardinality
**Definition**: The multiplicity of keys in each frame; one-to-one,
one-to-many, many-to-many — determines merge output size.
**Related**: fan-out

### fan-out
**Definition**: A duplicated key on either side causing its row to appear
multiple times in the output — silent data inflation.
**Related**: cardinality, validated merge

### `join()`
**Definition**: `merge` on the index by default — the convenience form for
index-keyed frames.
**Example**:
```python
a.set_index("k").join(b, how="left")
```
**Related**: `merge()`

### `concat()`
**Definition**: Stacks frames along an axis without key matching —
positional combination, not a join.
**Example**:
```python
pd.concat([df1, df2], ignore_index=True)
```
**Complexity**: O(n).
**Related**: `axis=0`, `axis=1`

### `axis=0` / `axis=1`
**Definition**: The stacking direction: 0 stacks rows (same columns), 1
attaches columns (same rows).
**Related**: `concat()`

### `ignore_index=True`
**Definition**: `concat` option discarding incoming indexes and issuing a
fresh RangeIndex — avoids duplicate-index bugs.
**Related**: `concat()`

### `combine_first()`
**Definition**: Returns a frame where the left operand's non-null values win
and its NaNs are filled from the right.
**Example**:
```python
cur.combine_first(prev)
```
**Related**: filling, missing data

### `suffixes`
**Definition**: `merge` option controlling names for colliding columns
(default `_x`/`_y`).
**Related**: `merge()`

### one-to-many
**Definition**: A join cardinality where one left row matches several right
rows — the source of fan-out when unintended.
**Related**: cardinality

### validated merge
**Definition**: Wrapping a merge with row-count assertions and duplicate-key
warnings so fan-out is caught immediately.
**Related**: fan-out

## Key Concepts Summary

### The combining family
- merge: key-based SQL joins
- join: index-based merges
- concat: positional stacking
- combine_first: sibling filling

### The fan-out rule
- Duplicated keys multiply rows — check counts after every merge
- Aggregate or dedupe the many-side before joining

### Discipline
- Always state `how=`
- `left_on`/`right_on` for mismatched names
- Validated helpers with row-count asserts

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `merge(how="left")` — ___
2. `concat` — ___
3. fan-out — ___
4. `combine_first` — ___
5. `join` — ___
6. `left_on`/`right_on` — ___
7. `how="inner"` — ___
8. `ignore_index=True` — ___

A. Keep all left rows
B. Only matching keys
C. Duplicated keys inflating output rows
D. Positional stacking
E. Index-based merge
F. Differing key names
G. Fresh RangeIndex after concat
H. Left wins, NaN from right

**Answers:** 1-A, 2-D, 3-C, 4-H, 5-E, 6-F, 7-B, 8-G
