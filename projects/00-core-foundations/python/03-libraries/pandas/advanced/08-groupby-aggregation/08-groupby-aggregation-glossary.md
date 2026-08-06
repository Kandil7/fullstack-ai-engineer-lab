# GroupBy & Aggregation — Glossary 08 (pandas advanced)

## Quick Reference Table

| Term | Category | One-Line Definition |
|------|----------|---------------------|
| split-apply-combine | Concept | Group -> function -> combine pattern |
| `groupby()` | Method | Splits rows by key(s) |
| `.agg()` | Method | Collapses each group to summary statistics |
| named aggregation | Syntax | `agg(m=("col", "mean"))` — readable outputs |
| `.transform()` | Method | Group statistics broadcast to original rows |
| `.filter()` | Method | Drops whole groups by predicate |
| `.apply()` | Method | Passes whole groups to a function (slow) |
| `as_index=False` | Option | Keeps the group key as a column |
| group key | Concept | The column(s) defining the groups |
| grouped z-score | Pattern | Per-group standardization via transform |
| group-mean impute | Pattern | Filling missing with per-group means |
| leakage | Bug | Group stats computed with future/outside data |

## Detailed Definitions

### split-apply-combine
**Definition**: The three-step pattern underlying all groupby work: split by
key, apply a function per group, combine the results.
**Related**: `groupby()`, `.agg()`

### `groupby()`
**Definition**: Splits the frame by key column(s); returns a GroupBy object
that `.agg`/`.transform`/`.filter` consume.
**Example**:
```python
df.groupby("model")
```
**Complexity**: O(n) hashing pass.
**Related**: group key

### `.agg()`
**Definition**: Collapses each group to summary rows — one row per group,
with one or many named aggregations.
**Example**:
```python
df.groupby("model", as_index=False).agg(
    m=("f1", "mean"), n=("f1", "count"))
```
**Related**: named aggregation

### named aggregation
**Definition**: The `agg(col=("source", "func"))` syntax producing readable
output column names.
**Related**: `.agg()`

### `.transform()`
**Definition**: Applies a per-group function and returns a result ALIGNED to
the original rows — the group-feature builder.
**Example**:
```python
df["m"] = df.groupby("model")["f1"].transform("mean")
```
**Related**: group-mean impute, grouped z-score

### `.filter()`
**Definition**: Keeps rows whose GROUPS satisfy a predicate — group-level
selection, not row masks.
**Example**:
```python
df.groupby("model").filter(lambda g: len(g) >= 3)
```
**Related**: cohort gates

### `.apply()`
**Definition**: Passes each whole group to a function; powerful, Python-speed,
can reshape — use only when agg/transform cannot express the logic.
**Related**: `.agg()`, `.transform()`

### `as_index=False`
**Definition**: Keeps the group key(s) as columns instead of moving them into
the index.
**Related**: `groupby()`

### group key
**Definition**: The column(s) partitioning the rows; one or many, forming a
grouping tuple.
**Related**: `groupby()`

### grouped z-score
**Definition**: Standardizing within groups via transform:
`(x - group_mean) / group_std` aligned to rows.
**Related**: `.transform()`

### group-mean impute
**Definition**: Filling missing values with each row's group mean — preserves
group structure; fit on train only.
**Related**: `.transform()`, missing data

### leakage
**Definition**: Group statistics computed on data outside the training rows
(or across a time boundary) leaking into training.
**Related**: train/test discipline

## Key Concepts Summary

### The three verbs
- `.agg` — collapse groups to summary rows
- `.transform` — broadcast group stats to original rows (features)
- `.filter` — keep/drop whole groups by predicate

### Index discipline
- `as_index=False` when the result feeds joins or plots

### Leak discipline
- Fit group statistics on train only; apply the mapping to test/serve

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `.agg()` — ___
2. `.transform()` — ___
3. `.filter()` — ___
4. `as_index=False` — ___
5. named aggregation — ___
6. `.apply()` — ___
7. grouped z-score — ___
8. group-mean impute — ___

A. Collapses groups to summary rows
B. Row-aligned group statistics
C. Keeps the group key as a column
D. Group-level selection by predicate
E. `agg(m=("col", "mean"))` syntax
F. Per-group standardization via transform
G. Slow escape hatch passing whole groups
H. Filling missing with group means

**Answers:** 1-A, 2-B, 3-D, 4-C, 5-E, 6-G, 7-F, 8-H
