# 03-libraries/pandas (advanced) — 02: Indexing & Selection

## Topic Overview

Selection is where pandas either feels magical or bites you. Three tools cover
almost everything: `df["col"]` (column by name), `df.loc` (label-based rows),
`df.iloc` (position-based rows), and boolean masks (`df[df.score > 0.5]`).
The core rule: **`loc` is inclusive of the end label, `iloc` is exclusive of
the end position** — the same half-open convention as Python slicing.

For AI engineers selection is the data-slicing layer: train/val/test by index,
filtering to high-confidence predictions, masking out out-of-distribution
rows. A single wrong `loc` vs `iloc` — or a chained-assignment warning — can
silently train a model on the wrong rows.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Select columns by name and slice rows with `[]`
2. Use `.loc` for label-based selection with inclusive ends
3. Use `.iloc` for position-based selection with exclusive ends
4. Build boolean masks and combine them with `&`, `|`, `~`
5. Select with `.isin()`, `.between()`, and `.query()`
6. Set values with `.loc`/`.iloc` without chained-assignment bugs
7. Explain why chained indexing fails and how to fix it

## Prerequisites

| Need | Where |
|------|-------|
| DataFrame/Series basics | `03-series-lecture.md`, `04-dataframes-lecture.md` |
| Boolean Series | `11-booleans.py` (core) |
| Slicing semantics | `05-array-slicing-lecture.md` (NumPy) |

## 1. Column Selection and Row Slicing

```python
import pandas as pd

df = pd.DataFrame(
    {"doc": ["a", "b", "c", "d"], "score": [0.1, 0.9, 0.5, 0.8]},
    index=["r1", "r2", "r3", "r4"],
)

df["score"]            # Series — column by name
df[["doc", "score"]]   # DataFrame — list of columns
df[1:3]                # rows by POSITION (half-open) — label-agnostic
```

`df[1:3]` slices positions 1..2 — it does not care about the index labels.
This positional slice is the source of many `loc`/`iloc` mix-ups.

## 2. `.loc` — Label-Based, Inclusive

```python
df.loc["r2"]             # row by label
df.loc[["r2", "r4"]]     # list of labels
df.loc["r1":"r3"]        # label slice — INCLUSIVE of 'r3'
df.loc["r1":"r3", "score"]  # rows and columns together
```

`.loc` works on the index labels and includes both ends. This is what you want
when rows carry meaningful ids (timestamps, doc ids) rather than positions.

## 3. `.iloc` — Position-Based, Exclusive

```python
df.iloc[0]               # first row by position
df.iloc[1:3]             # positions 1..2 — EXCLUSIVE of 3
df.iloc[:, 0]            # all rows, first column
df.iloc[-1]              # last row
```

`.iloc` is pure position, half-open, exactly like list slicing. Use it when
the index is not meaningful (a shuffled frame, a numeric range).

## 4. Boolean Masks — The Workhorse

```python
high = df[df["score"] > 0.7]          # mask selects rows where True
top = df[(df["score"] > 0.7) & (df["doc"].str.startswith("a"))]
either = df[df["score"].isna() | df["score"] > 0.9]
```

Rules: `&`, `|`, `~` (not `and`/`or`/`not` — those need Python booleans), and
parentheses around each comparison because `&` binds tighter than `>`.

## 5. `.isin`, `.between`, `.query`

```python
df[df["doc"].isin(["a", "c"])]
df[df["score"].between(0.4, 0.9, inclusive="both")]
df.query("score > 0.7 and doc != 'b'")      # string-query DSL
```

`query` reads almost like SQL and is handy for long filter chains; `.isin` is
the set-membership filter (dedup IDs, allow-lists); `.between` is the range
mask with explicit inclusivity.

## 6. Setting Values — Never Chained

```python
# WRONG — chained assignment can silently do nothing (SettingWithCopyWarning)
df[df["score"] > 0.7]["flag"] = 1

# CORRECT — single .loc operation
df.loc[df["score"] > 0.7, "flag"] = 1
```

Chained indexing (`df[mask]["col"] = x`) first returns a *copy*, then sets on
the copy — the original frame is unchanged, often silently. One `.loc` does
the whole operation on the original.

## 7. Production Pattern — Train/Val/Test by Mask

```python
def split_mask(n: int, frac_train: float = 0.7, seed: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Deterministic boolean masks for train/val/test (stratify externally)."""
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    k_train = int(n * frac_train)
    k_val = int(n * (frac_train + (1 - frac_train) / 2))
    return idx[:k_train], idx[k_train:k_val], idx[k_val:]

train_i, val_i, test_i = split_mask(len(df))
train = df.iloc[train_i]
val = df.iloc[val_i]
test = df.iloc[test_i]
```

Positional `iloc` slicing over a shuffled permutation is the clean way to
split — no index-label surprises, and the masks are reusable across frames.

## Common Mistakes to Avoid

### Mistake 1: `loc` vs `iloc` inclusivity

```python
# WRONG — expects 3 rows, gets 2
df.iloc[1:3]    # positions 1,2 (half-open)
# CORRECT for 3 rows by label
df.loc["r1":"r3"]   # includes 'r3'
```

### Mistake 2: `and`/`or` inside masks

```python
# WRONG — ValueError: ambiguous truth value
df[(df.a > 1) and (df.b < 2)]
# CORRECT
df[(df.a > 1) & (df.b < 2)]
```

### Mistake 3: Chained assignment

```python
# WRONG — sets on a copy
df[df.a > 1]["flag"] = 1
# CORRECT
df.loc[df.a > 1, "flag"] = 1
```

### Mistake 4: Setting on a slice view vs copy

```python
# WRONG — SettingWithCopyWarning, changes may not persist
sub = df[df.a > 1]
sub["x"] = 0
# CORRECT — copy explicitly when you intend to detach
sub = df[df.a > 1].copy()
```

## Best Practices

1. Column names with `[]`; rows with `.loc`/`.iloc` — never bare slices
2. Use `.loc` for labeled indexes, `.iloc` for positions
3. Wrap each mask comparison in parentheses
4. Set values in one `.loc` statement, never chained
5. Use `.copy()` when detaching a sub-frame you will mutate
6. `.isin`/`.between`/`.query` for readable compound filters

## Complexity and Cost

| Operation | Cost | Notes |
|-----------|------|-------|
| `df["col"]` | O(1) | metadata lookup |
| `.loc[label]` | O(1) avg | hash lookup on the index |
| `.iloc[pos]` | O(1) | direct position |
| boolean mask | O(n) | vectorized comparison |
| mask + `&`/`\|` | O(n) | per-mask pass |
| `.query()` | O(n) | parses then evaluates |

**At scale:** masks are O(n) vectorized passes — fine at 10M rows. The hidden
cost is `df[mask].copy()` materializations: each copies the selected rows.
Chain masks into one expression instead of building intermediate frames.

## AI Engineering Relevance

**Where this shows up:**

| Concept | AI/Backend Use Case |
|---------|---------------------|
| boolean masks | filtering to high-confidence predictions |
| `.loc` setting | labeling rows, flagging anomalies in place |
| train/val/test masks | deterministic dataset splits |
| `.isin` | allow-list filtering of eval documents |
| `.query` | readable filter chains in experiment code |
| `.copy()` | avoiding mutation surprises in feature pipelines |

**Scale note:** when the corpus is 100M rows, `df[df.x > t]` builds a full
copy. Filter early (downstream of loading) and drop unneeded columns before
masking — memory is the real constraint, not CPU.

## Practice Exercises

### Exercise 1: Mask Arithmetic (Easy)
Given a frame of `score` and `label`, select rows where `score > 0.7` OR
`label == "gold"`, using parentheses correctly.

### Exercise 2: loc vs iloc (Medium)
Build a frame with string labels `["q1"..."q6"]`; select `q2` through `q4`
with `.loc`, then positions 1..3 with `.iloc`, and explain the difference.

### Exercise 3: In-Place Flagging (Hard)
Write `flag_duplicates(df, key_col, flag_col)` that marks the first
occurrence of each key as `"original"` and later ones as `"duplicate"` using
a single `.loc` assignment with a boolean mask.

## Summary

| Concept | Description |
|---------|-------------|
| `df["col"]` | column by name |
| `.loc` | label selection, inclusive |
| `.iloc` | positional selection, half-open |
| boolean masks | `&`/`\|`/`~` with parens, never `and`/`or` |
| `.isin`/`.between`/`.query` | readable compound filters |
| `.loc` setting | one operation, never chained |
| `.copy()` | explicit detachment before mutation |

Selection is the vocabulary of every pandas pipeline. Learn the three
selector families and the mask rules once, and the "wrong rows" bug class
disappears.

## Quick Reference

| Task | Idiom |
|------|-------|
| Column | `df["col"]` |
| Label rows | `df.loc["a":"c"]` (inclusive) |
| Position rows | `df.iloc[1:3]` (exclusive) |
| Mask | `df[(df.a > 1) & (df.b < 2)]` |
| In set | `df[df.a.isin([1, 2])]` |
| In range | `df[df.a.between(0, 1)]` |
| Query DSL | `df.query("a > 1 and b < 2")` |
| Set by mask | `df.loc[mask, "col"] = value` |

## Next Steps

Next: **[03-filtering](03-filtering-lecture.md)** — advanced query techniques.
Continues in: **[06-data-structures-algorithms — 13 binary search](../../../../06-data-structures-algorithms/lectures/13-binary-search-lecture.md)** (thinking about the masks you filter).
Official docs: https://pandas.pydata.org/docs/user_guide/indexing.html
