# Pandas Pitfalls — Glossary 44 (pandas)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| chained assignment | Anti-pattern | Two-step write (`df[m]["c"]=x`) that may silently vanish |
| `SettingWithCopyWarning` | Warning | pandas telling you the write target is ambiguous |
| index alignment | Concept | Operations match labels, not positions |
| `reindex` | Method | Aligns to a target index, filling gaps |
| `inplace=True` | Anti-pattern | Returns None; cannot chain; saves nothing |
| NaN | Sentinel | Missing value that never equals itself |
| `isna()` / `notna()` | Method | The only honest missing-value predicates |
| dtype upcasting | Concept | Mixing types silently widens a column's dtype |
| `iterrows` | Anti-pattern | Series-per-row Python loop; slowest option |
| `itertuples` | Method | Tuple-per-row loop; 20-50x faster |
| vectorization | Concept | Whole-column C-speed operations |
| merge explosion | Concept | Duplicate keys multiplying rows |
| `is_unique` | Property | Whether a column's values are all distinct |
| copy-on-write | Concept | pandas 3.x default; writes copy instead of aliasing |
| shallow copy | Concept | Shares data blocks; writes reach the parent |
| `fill_method` | Parameter | `pct_change`'s default `'pad'` ffills gaps, fabricating deltas |
| contract check | Pattern | Assert shape/uniqueness before risky operations |

## Detailed Definitions

### chained assignment
**Definition**: Writing through two selections — `df[mask]["col"] = x` or
`sub = df.iloc[:2]; sub["col"] = x`. pandas cannot prove view-vs-copy, so
it warns and the write may not reach the frame.
**Example**:
```python
# WRONG
sub = df[df["a"] > 1]
sub["flag"] = 1          # df["flag"] unchanged
```
**Related**: `SettingWithCopyWarning`, `.loc`

### contract check
**Definition**: The habit of asserting assumptions before expensive or
risky operations — e.g. `assert other[key].is_unique` before a merge.
**Related**: merge explosion, `is_unique`

### copy-on-write
**Definition**: The pandas 3.x semantics (opt-in in 2.x): every write to an
object derived from another triggers a copy, so aliases never silently
mutate their parents. Code that relies on aliasing breaks under CoW.
**Example**:
```python
pd.set_option("mode.copy_on_write", True)
```
**Related**: shallow copy

### dtype upcasting
**Definition**: pandas' safe-dtype selection when values mix: int+float ->
float64, int+string -> object. pandas 2.2 warns on incompatible setitem;
3.x raises. Either way the contract changes.
**Example**:
```python
df["id"] = [1, 2, 3]
df.loc[2, "id"] = "oops"   # dtype becomes object
```
**Related**: `.loc`

### index alignment
**Definition**: Binary operations match on labels. Mismatched indices
produce NaN at unmatched positions instead of errors.
**Example**:
```python
pd.Series([1, 2], index=[0, 1]) + pd.Series([10, 20], index=[1, 2])
# -> [nan, 12.0, nan]
```
**Related**: `reindex`

### `inplace=True`
**Definition**: The parameter on dropna/fillna/sort_values that returns
None instead of the frame — breaking chains, saving nothing.
**Example**:
```python
df.dropna(inplace=True).assign(x=1)   # AttributeError: 'NoneType'
```
**Related**: chained assignment

### `is_unique`
**Definition**: A Series property: True when all values are distinct. The
pre-merge guard against cardinality explosions.
**Example**:
```python
assert right["key"].is_unique
```
**Related**: merge explosion, contract check

### `isna()` / `notna()`
**Definition**: The vectorized predicates for missing values. `NaN == NaN`
is False; these are the only reliable checks.
**Example**:
```python
s[s.notna()]
```
**Related**: NaN

### `itertuples`
**Definition**: Iterates rows as lightweight tuples (namedtuple) — 20-50x
faster than `iterrows` because no Series is built per row.
**Example**:
```python
for row in df.itertuples(index=False):
    ... row.a ...
```
**Related**: `iterrows`, vectorization

### `iterrows`
**Definition**: Iterates rows as (index, Series) pairs. Each iteration
builds a Series and runs Python — the slowest row loop.
**Related**: `itertuples`, vectorization

### merge explosion
**Definition**: A merge that multiplies rows because keys are not unique on
one or both sides — a 2x3 duplicate-key merge yields 6 rows.
**Example**:
```python
len(orders.merge(profile, on="cust"))   # > len(orders)
```
**Related**: `is_unique`, contract check

### NaN
**Definition**: The missing-value sentinel with the property `NaN != NaN`.
Any comparison with `==`/`!=` involving NaN is always False/True
respectively — use `isna()`.
**Related**: `isna()` / `notna()`

### `reindex`
**Definition**: Aligns a Series/DataFrame to a target index or columns,
filling missing entries (optionally with a fill value) — the alignment
repair tool.
**Example**:
```python
left.reindex(right.index)
test_d.reindex(columns=train_d.columns, fill_value=0)
```
**Related**: index alignment

### `SettingWithCopyWarning`
**Definition**: The warning pandas emits on chained writes — its way of
saying "I cannot prove this writes where you think". Treat every instance
as a bug to fix with `.loc`.
**Related**: chained assignment

### shallow copy
**Definition**: `.copy(deep=False)` — shares underlying data blocks with
the parent. Writes through it propagate; CoW changes that behavior.
**Related**: copy-on-write

### vectorization
**Definition**: Operating on whole columns in C-speed loops instead of
Python per-row loops — the permanent fix for `iterrows`-class slowness.
**Related**: `itertuples`, `iterrows`

### `fill_method`
**Definition**: The `pct_change()` parameter controlling missing-value
handling. Its default `'pad'` ffill-replaces gaps BEFORE computing deltas —
`[10, NaN, 20]` becomes `[NaN, 0.0, 1.0]`, fabricating a "no change" and a
delta computed from a value that never existed. `fill_method=None` surfaces
each gap as NaN instead (and is the future default).
**Example**:
```python
s = pd.Series([10.0, float("nan"), 20.0])
print(s.pct_change().tolist())               # [nan, 0.0, 1.0] -- fabricated
print(s.pct_change(fill_method=None).tolist())  # [nan, nan, nan] -- honest
```
**Related**: NaN

## Key Concepts Summary

### The write rules
- One `.loc` selection; never chain selections for writes
- `inplace=True` returns None — use explicit rebinding
- Check dtypes after any mixed-type setitem

### The comparison rules
- `isna()`/`notna()` for missing; never `== np.nan`
- Alignment matches labels — `reindex` to repair
- `pct_change` needs `fill_method=None` — the default ffill fabricates deltas

### The performance rules
- Vectorize; `itertuples` when you must loop; `iterrows` never
- Assert `is_unique` before merges

### The future rules
- CoW changes aliasing semantics — write for both modes
- Shallow-copy mutations are behavior, not an accident

## Practice Terms

Match each term to its definition (answers at the bottom).

1. chained assignment — ___
2. `isna()` — ___
3. index alignment — ___
4. `inplace=True` — ___
5. merge explosion — ___
6. `itertuples` — ___
7. copy-on-write — ___
8. `is_unique` — ___
9. `fill_method` — ___

A. Labels-based matching that yields NaN
B. Two-step write that may vanish
C. Returns None and cannot chain
D. The honest missing-value predicate
E. Writes copy instead of aliasing
F. Tuple-per-row loop
G. Duplicate keys multiplying rows
H. Pre-merge uniqueness check
I. `pct_change`'s ffill default — fabricates deltas across gaps

**Answers:** 1-B, 2-D, 3-A, 4-C, 5-G, 6-F, 7-E, 8-H, 9-I
