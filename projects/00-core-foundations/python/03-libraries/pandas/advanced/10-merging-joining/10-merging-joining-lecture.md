# 03-libraries/pandas (advanced) — 10: Merging & Joining

## Topic Overview

Combining frames is the relational heart of pandas: `merge` (SQL-style joins
on keys), `join` (index-based convenience for merge), `concat` (stacking
rows/columns), and `combine_first` (fill missing from a sibling). The key
concepts carry over directly from SQL: inner, left, right, outer; one-to-one,
one-to-many, many-to-many.

For AI engineers, merging is how features meet labels, how predictions meet
ground truth, and how log frames join user tables. The cardinality mistakes —
a duplicated key silently multiplying rows — are among the most common silent
data-corruption bugs in feature engineering.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Merge frames with `how=` inner/left/right/outer and `on=`
2. Understand join cardinalities and detect row multiplication
3. Use `join` for index-based merges
4. Use `concat` for stacking rows and columns
5. Use `combine_first` for sibling filling
6. Validate merge results (row counts, duplicate keys)
7. Build feature-label merges without accidental fan-out

## Prerequisites

| Need | Where |
|------|-------|
| Selection/indexing | `02-indexing-selection-lecture.md` |
| GroupBy | `08-groupby-aggregation-lecture.md` |
| SQL joins | `04-databases/mysql/11-join-lecture.md` |

## 1. `merge` — SQL-Style Joins

```python
users = pd.DataFrame({"user_id": [1, 2, 3], "plan": ["free", "pro", "pro"]})
events = pd.DataFrame({"user_id": [1, 1, 2], "event": ["view", "click", "view"]})

users.merge(events, on="user_id", how="inner")   # only matching users
users.merge(events, on="user_id", how="left")    # all users, NaN for none
users.merge(events, on="user_id", how="outer")   # all keys both sides
```

`how` selects the join semantics exactly as SQL: inner (match only), left
(keep left rows), right, outer (union). `on=` names the shared key; use
`left_on=`/`right_on=` when the key names differ.

## 2. Cardinality — The Row-Multiplication Trap

```python
# One-to-many: user 1 appears twice in events -> user 1 appears twice in the merge
users.merge(events, on="user_id")
#   user_id  plan  event
# 0       1  free   view
# 1       1  free  click     <- duplicated!
```

A duplicated key on either side multiplies rows — the fan-out that silently
inflates counts and biases aggregates. **Always check** `len(result) ==
expected` after merges with potentially duplicated keys, or dedupe first.

## 3. `join` — Index-Based Merging

```python
users.set_index("user_id").join(
    events.groupby("user_id")["event"].count(), how="left"
)
```

`join` merges on the index by default — the convenient form when keys live in
indexes. It is `merge(left_index=True, right_index=True)` under the hood.

## 4. `concat` — Stacking, Not Matching

```python
pd.concat([df_q1, df_q2], axis=0)      # stack rows (same columns)
pd.concat([features, labels], axis=1)  # attach columns (same rows)
pd.concat([a, b], ignore_index=True)   # renumber a RangeIndex
```

`concat` stacks along an axis without key matching: rows (axis=0) or columns
(axis=1). Unlike merge it does not align on keys — it stacks by position or
index; `ignore_index=True` avoids duplicate-index surprises.

## 5. `combine_first` — Fill from a Sibling

```python
df.fill_missing = df.combine_first(df_prior)   # df wins where non-null
```

`combine_first` keeps the left frame's values and fills its NaNs from the
right — the "prefer this source, fall back to that one" merge.

## 6. Production Pattern — Feature-Label Merge with Validation

```python
def merge_checked(left: pd.DataFrame, right: pd.DataFrame, on: str, how: str = "left") -> pd.DataFrame:
    """Merge, then assert the row count is consistent with the join type."""
    before = len(left)
    out = left.merge(right, on=on, how=how)
    if how == "left":
        assert len(out) >= before, "left join cannot lose rows"
        # fan-out check: warn when rows multiplied beyond expectation
        if len(out) > before:
            dupes = right[on].duplicated().sum()
            print(f"[warn] fan-out: {len(out) - before} extra rows "
                  f"(duplicated keys in right: {dupes})")
    return out
```

A merge that validates its own row count catches the fan-out bug at the
moment it happens — not in the model's eval curve.

## Common Mistakes to Avoid

### Mistake 1: Ignoring cardinality

```python
# WRONG — duplicated keys multiply rows silently
df = users.merge(events, on="user_id")
# CORRECT — check counts, dedupe or aggregate the right side first
```

### Mistake 2: merge vs concat confusion

```python
# WRONG — concat stacks; it does not match keys
pd.concat([users, events])
# CORRECT — merge for key matching
users.merge(events, on="user_id")
```

### Mistake 3: Missing `left_on`/`right_on` for differing key names

```python
# WRONG — KeyError or silent wrong-key join
a.merge(b, on="id")   # when b's key is 'user_id'
# CORRECT
a.merge(b, left_on="id", right_on="user_id")
```

### Mistake 4: `suffixes` collision after merge

```python
# WRONG — duplicated column names like score_x/score_y surprise you later
a.merge(b, on="id")
# CORRECT — rename before, or read the _x/_y suffixes deliberately
```

## Best Practices

1. State `how=` explicitly every time — never rely on a default
2. Check row counts after every merge; assume fan-out until proven otherwise
3. Dedupe or aggregate the many-side before joining
4. Use `join` for index keys, `merge` for named keys, `concat` for stacking
5. Handle differing key names with `left_on`/`right_on`
6. Wrap merges in validated helpers (row-count asserts)
7. Test merges on small samples before the full pipeline

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `merge` | O(n log n) | sort-merge or hash join |
| inner/left/outer | O(n) output | output size varies by match |
| `join` | O(n log n) | index-based |
| `concat` | O(n) | plain stacking |
| `combine_first` | O(n) | element-wise fill |

**At scale:** merge cost is dominated by the hashing/sorting pass and the
output size. Fan-out is the real danger: a 1:N join with 100x duplication
turns a 10M-row merge into a billion-row frame — memory death. Validate
before, not after.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| feature-label merge | joining user features to target labels |
| one-to-many | events -> user aggregates (aggregate first!) |
| left join | predictions to ground truth with all samples |
| concat | stacking sharded datasets |
| combine_first | filling feature gaps from a backup source |
| validated merge | the fan-out guard in feature pipelines |

**Scale note:** the "great offline, broken online" class of bugs often traces
to a feature-merge fan-out that inflated training rows (and leakage). The
row-count assert is the cheapest insurance in feature engineering.

## Practice Exercises

### Exercise 1: Join Types (Easy)
Merge users x events with inner/left/outer and report the row counts for each.

### Exercise 2: Fan-Out Detection (Medium)
Create a users frame and an events frame where one user has 3 events; merge
and confirm the user appears 3x; then fix by aggregating events per user first.

### Exercise 3: Validated Merge (Hard)
Implement `merge_checked` and write a test where a duplicated key in the right
frame triggers the warning path with the correct extra-row count.

## Summary

| Concept | Description |
|---------|-------------|
| `merge` | SQL-style joins with `how=` and `on=` |
| cardinality | duplicated keys multiply rows — the silent bug |
| `join` | index-based merging convenience |
| `concat` | positional stacking along an axis |
| `combine_first` | sibling-source filling |
| validation | row-count asserts around every merge |

Merging is where datasets combine — and where silent corruption happens.
State the join semantics, check the counts, and never let a fan-out reach a
model unnoticed.

## Quick Reference

| Task | Idiom |
|------|-------|
| Inner join | `a.merge(b, on="k", how="inner")` |
| Left join | `a.merge(b, on="k", how="left")` |
| Differing keys | `a.merge(b, left_on="x", right_on="y")` |
| Index join | `a.join(b, how="left")` |
| Stack rows | `pd.concat([a, b], ignore_index=True)` |
| Attach columns | `pd.concat([a, b], axis=1)` |
| Fill from sibling | `a.combine_first(b)` |
| Check fan-out | `assert len(out) >= len(left)` |

## Next Steps

Next: **[11-window-functions](11-window-functions-lecture.md)** — rolling, expanding, ewm.
Continues in: **[07-datetime](07-datetime-lecture.md)** for time-windowed merges.
Official docs: https://pandas.pydata.org/docs/user_guide/merging.html
