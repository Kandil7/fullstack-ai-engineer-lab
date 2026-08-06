# GroupBy Internals — Glossary 42 (pandas)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| split-apply-combine | Concept | The three phases behind every groupby |
| `groupby` | Method | Groups rows by key(s) for grouped operations |
| `agg` | Method | Shrinks to one row per group with aggregate functions |
| named aggregation | Pattern | `agg(avg=("col", "mean"))` — named output columns |
| `transform` | Method | Same-length output; each row gets its group's statistic |
| `filter` | Method | Keeps whole groups matching a predicate |
| `apply` | Method | Arbitrary per-group function; the slow path |
| group key | Concept | The column(s) defining group membership |
| MultiIndex | Type | Hierarchical index from multi-key groupby |
| `unstack` | Method | Pivots one index level into columns |
| `reset_index` | Method | Moves group keys back to columns |
| `sort=False` | Parameter | Keeps first-appearance key order |
| `Grouper` | Object | Time-frequency group key (see 41) |
| `pivot_table` | Method | agg-style reshaping without explicit groupby |

## Detailed Definitions

### `agg`
**Definition**: Applies one or more functions per group and returns one row
per group. Accepts built-in names, callables, lists, and per-column dicts.
**Example**:
```python
df.groupby("team")["score"].agg(["mean", "max"])
```
**Complexity**: O(n) per function.
**Related**: named aggregation, `transform`

### `apply`
**Definition**: Calls a function with each group (DataFrame or Series) and
combines results. Most flexible verb; slowest — Python per group.
**Example**:
```python
df.groupby("team")["score"].apply(lambda g: g.iloc[0] - g.iloc[-1])
```
**Complexity**: O(groups) Python calls.
**Related**: `agg`, `transform`

### `filter`
**Definition**: Keeps entire groups for which the predicate returns True.
Groups are atomic — never partially filtered.
**Example**:
```python
df.groupby("team").filter(lambda g: len(g) >= 2)
```
**Complexity**: O(n x predicate cost).
**Related**: `groupby`, boolean indexing

### group key
**Definition**: The column (or columns) whose values define group
membership; passed positionally to `groupby`.
**Related**: `groupby`, MultiIndex

### `groupby`
**Definition**: The split-apply-combine entry point: groups rows by key,
then agg/transform/filter/apply operate on the groups.
**Example**:
```python
df.groupby("team")["score"].mean()
```
**Complexity**: O(n) to build group indices.
**Related**: `agg`, `transform`, `filter`, `apply`

### `Grouper`
**Definition**: A time-frequency grouping key — `groupby(Grouper(freq="W"))`
equals `resample("W")` (see lecture 41).
**Related**: MultiIndex

### MultiIndex
**Definition**: Hierarchical index produced by multi-key groupby — levels
like `("Jan", "NY")`. `unstack`/`stack` reshape it.
**Example**:
```python
sales.groupby(["month", "city"])["amount"].sum().index.names
```
**Related**: `unstack`, group key

### named aggregation
**Definition**: The `agg(avg=("col", "mean"))` form: output column name,
source column, and function on one line — the reviewable feature-table
pattern.
**Example**:
```python
df.groupby("user_id").agg(total=("amount", "sum"),
                          count=("amount", "count"))
```
**Related**: `agg`

### `pivot_table`
**Definition**: Aggregation-with-reshaping: values, index, columns, aggfunc
in one call — the wide-matrix alternative to groupby+unstack.
**Related**: `unstack`, `agg`

### `reset_index`
**Definition**: Moves group keys from the index back into columns — the
final step before joining group features onto a base frame.
**Example**:
```python
df.groupby("user_id").agg(...).reset_index()
```
**Related**: MultiIndex

### `sort=False`
**Definition**: Groupby parameter preserving first-appearance key order
instead of sorting keys ascending.
**Related**: group key

### split-apply-combine
**Definition**: The mechanism behind groupby: split by key, apply an
operation to each sub-frame, combine results into one object. Reproducible
manually with a dict loop.
**Related**: `groupby`

### `transform`
**Definition**: Returns the same length as the input: each row receives its
group's statistic. Used for deviation features, shares, and centered values.
**Example**:
```python
df["team_mean"] = df.groupby("team")["score"].transform("mean")
```
**Complexity**: O(n), vectorized.
**Related**: `agg`, `filter`

### `unstack`
**Definition**: Pivots one level of a MultiIndex into columns — turns a
long cohort-by-month series into a wide matrix.
**Example**:
```python
cohort.unstack()
```
**Related**: MultiIndex, `pivot_table`

## Key Concepts Summary

### Verb selection by output shape
- `agg` — one row per group (features, summaries)
- `transform` — same rows, group statistics per row
- `filter` — whole groups dropped or kept
- `apply` — anything, at Python speed

### Feature-table pattern
- One named-agg pass per entity
- `reset_index` before merge
- Verify column names and one hand-computed row

### Reshaping
- Multi-key groupby -> MultiIndex
- `unstack` for wide matrices; `pivot_table` for direct wide agg

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `agg` — ___
2. `transform` — ___
3. `filter` — ___
4. `apply` — ___
5. named aggregation — ___
6. split-apply-combine — ___
7. `unstack` — ___
8. `reset_index` — ___

A. Same length as input; group statistic per row
B. One row per group with aggregate functions
C. The three-phase groupby mechanism
D. Keeps whole groups by predicate
E. Arbitrary per-group Python function
F. Pivots one index level into columns
G. Moves keys back to columns
H. `agg(avg=("col", "mean"))` form

**Answers:** 1-B, 2-A, 3-D, 4-E, 5-H, 6-C, 7-F, 8-G
