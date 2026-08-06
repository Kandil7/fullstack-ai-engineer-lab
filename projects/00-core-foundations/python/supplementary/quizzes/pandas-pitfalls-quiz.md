# Pandas Pitfalls Quiz (Topic 44)

## Topic Overview
This quiz covers the costliest pandas mistakes: chained assignment and
SettingWithCopyWarning, index alignment, `inplace=True`, `NaN != NaN`,
silent dtype upcasting, `iterrows` performance, `pct_change`'s ffill
fabrication, merge cardinality explosions, and copy-on-write semantics.

**Difficulty:** Intermediate to Advanced
**Questions:** 20 (6 Easy, 9 Medium, 5 Hard)
**Time:** ~30 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What is a chained assignment?**

A) Assigning the same value twice
B) Writing through two selections, e.g., `df[df.a > 2]["flag"] = 1`
C) Assigning in a loop
D) Assigning a column to itself

**Correct Answer:** B
**Explanation:** `df[mask]["col"] = x` selects rows, then writes into that
selection. pandas cannot prove whether the selection is a view or a copy,
so the write may silently vanish (with a warning).

---

### Question 2 [Easy]
**Which single expression correctly sets `flag = 1` where `a > 2`?**

A) `df[df.a > 2]["flag"] = 1`
B) `df.loc[df.a > 2, "flag"] = 1`
C) `df.loc[df.a > 2]["flag"] = 1`
D) `df["flag"][df.a > 2] = 1`

**Correct Answer:** B
**Explanation:** One `.loc` call with the mask AND the column name — a
single selection, no ambiguity. A, C, D are all chained writes.

---

### Question 3 [Easy]
**Why is `s[s != np.nan]` broken?**

A) It is too slow
B) `NaN != NaN` is True-ish... in fact NaN never equals anything, so the
comparison removes nothing
C) It raises TypeError
D) It drops valid rows

**Correct Answer:** B
**Explanation:** NaN is not equal to ANY value, including itself — so
`s != np.nan` is True for every row including NaN rows, and nothing is
filtered. Use `s.notna()`.

---

### Question 4 [Easy]
**What does `df.dropna(inplace=True)` return?**

A) The modified DataFrame
B) `None`
C) A boolean mask
D) A copy

**Correct Answer:** B
**Explanation:** Every `inplace=True` method returns None — the
transformation happens in place. This breaks method chaining and surprises
everyone once.

---

### Question 5 [Easy]
**What is the reliable way to detect a SettingWithCopyWarning in tests?**

A) Match warning message text
B) Check `w.category.__name__ == "SettingWithCopyWarning"`
C) Check the stack trace
D) Compare memory addresses

**Correct Answer:** B
**Explanation:** Message text changes between pandas versions; the warning
CATEGORY is stable. The verified probe pattern:
`any(w.category.__name__ == "SettingWithCopyWarning" for w in caught)`.

---

### Question 6 [Easy]
**Which loop is the slowest for row-wise work?**

A) `itertuples`
B) Vectorized operations
C) `iterrows`
D) `apply` with a vectorized function

**Correct Answer:** C
**Explanation:** `iterrows` constructs a full Series per row — O(n) Python
overhead. The exercise measured ~0.58s vs ~0.012s for `itertuples` on 20k
rows (≈50x).

---

### Question 7 [Medium]
**What does the following code print?**

```python
import numpy as np, pandas as pd
s = pd.Series([1.0, np.nan, 3.0, np.nan])
print(len(s[s != np.nan]))
```

A) `2`
B) `4`
C) `3`
D) `0`

**Correct Answer:** B
**Explanation:** `s != np.nan` is True everywhere (NaN never equals
anything), so the filter keeps all 4 rows. The exercise verified exactly
this: "NaN != NaN filter keeps 4/4".

---

### Question 8 [Medium]
**Index alignment means `s1 + s2` with different indices:**

A) Adds positionally
B) Aligns by label; non-overlapping labels become NaN
C) Raises
D) Drops non-matching rows

**Correct Answer:** B
**Explanation:** pandas aligns by index LABEL. Mismatched labels produce
NaN in the result — the classic "why is my arithmetic NaN?" bug. Fix with
`reindex`/`reset_index` when you truly mean positional.

---

### Question 9 [Medium]
**A frame with int column `a` gets `df["a"] = df["a"].astype(str)`. What
happens?**

A) Silent upcast to object — ints become strings
B) The column is deleted
C) A FutureWarning is raised
D) Nothing

**Correct Answer:** A (with a FutureWarning in 2.x)
**Explanation:** Mixing types (int + str) upcasts the column to object
silently (in 2.2.3 it emits a FutureWarning; in 3.0 it will raise). The
result: ids that LOOK numeric but are strings — comparisons and merges
change behavior.

---

### Question 10 [Medium]
**Why is `df.merge(profile, on="cust")` dangerous when `profile` has
duplicate customers?**

A) It raises
B) Each duplicate key multiplies rows — 1 order x 3 profiles = 3 rows
C) It drops the duplicates
D) It only keeps the first

**Correct Answer:** B
**Explanation:** A merge emits one output row per KEY MATCH. Duplicates on
either side create a cross-product within the key — the exercise's 3x3
duplicate-key merge produced 6 rows. Guard with `key.is_unique` first.

---

### Question 11 [Medium]
**What does `df.copy(deep=False)` share with the parent?**

A) Nothing
B) The underlying data blocks — writes through it may propagate
C) Only the index
D) Only column names

**Correct Answer:** B
**Explanation:** `copy(deep=False)` shares data blocks; mutation through
the shallow copy reaches the parent — UNLESS copy-on-write is enabled,
which copies at the first write.

---

### Question 12 [Medium]
**Under CoW (pandas 3.x default), `sub = df.iloc[:2]; sub["c"] = 1` — what
happens to `df`?**

A) `df` gains column c with value 1 in the first two rows
B) `df` is unchanged — the write triggers a copy on `sub`
C) `df` loses its first two rows
D) It raises

**Correct Answer:** B
**Explanation:** CoW isolates derived frames: the first mutation of `sub`
copies the data, so `df` stays intact. Under CoW-off (2.x classic), the
write could propagate — the exercise showed `[99, 2, 3]` vs `[1, 2, 3]`.

---

### Question 13 [Medium]
**What is the output of the following code?**

```python
import pandas as pd
s = pd.Series([10.0, float("nan"), 20.0])
print(s.pct_change().tolist())
```

A) `[nan, nan, nan]`
B) `[nan, 0.0, 1.0]` — the default ffill fabricates deltas
C) `[nan, -0.5, 1.0]`
D) `[nan, 10.0, 10.0]`

**Correct Answer:** B
**Explanation:** Default `pct_change()` fills gaps with
`fill_method="pad"`: the missing value becomes 10, so position 1 = 0.0
("no change") and position 2 = (20-10)/10 = 1.0 — a delta computed from a
value that never existed. Use `pct_change(fill_method=None)` for honest NaN.

---

### Question 14 [Medium]
**Which of these produces a FutureWarning in pandas 2.2.3?**

A) `df.copy(deep=False)`
B) `s.pct_change()` — the default fill_method='pad' is deprecated
C) `df.groupby("team").mean()`
D) `pd.to_datetime("2024-01-01")`

**Correct Answer:** B
**Explanation:** The default 'pad' fill in `pct_change` is deprecated and
will be removed — pandas wants explicit `fill_method=None` or an explicit
fill. The other options are stable APIs.

---

### Question 15 [Medium]
**What does the `merge_check_duplicates` guard do BEFORE merging?**

A) Sorts both frames
B) Checks `left[on].duplicated().any() or right[on].duplicated().any()`
and raises ValueError if either has duplicates
C) Drops NaN keys
D) Converts keys to strings

**Correct Answer:** B
**Explanation:** The guard converts a silent row explosion into a loud,
immediate error: check both sides' key columns for duplicates, raise
before pandas multiplies anything.

---

### Question 16 [Hard]
**Why does `df[df.a > 2]["flag"] = 1` warn in one pandas version and stay
silent in another?**

A) pandas changes the warning randomly
B) The warning fires based on whether the intermediate selection is a view
or a copy — an implementation detail that differs by version, operation,
and CoW mode; never rely on it
C) Only 64-bit pandas warns
D) Warnings depend on the console

**Correct Answer:** B
**Explanation:** SettingWithCopyWarning depends on internals pandas cannot
guarantee. The probe showed boolean-mask chains warning, iloc-slice writes
warning, and loc-based chains sometimes NOT warning. The fix is the same
everywhere: one `.loc[mask, col] = x`.

---

### Question 17 [Hard]
**A probe verified that in pandas 2.2.3 a column-write on an iloc slice
does NOT propagate under CoW-off, but a single-cell write
`df2.iloc[0, 1] = 99` DOES. What does this imply?**

A) Slice writes are safer than cell writes
B) Write propagation depends on HOW the memory is shared (block-level vs
single element) — design code that works in BOTH CoW modes instead of
relying on either
C) CoW-off is deterministic
D) iloc is deprecated

**Correct Answer:** B
**Explanation:** The propagation rules differ by write pattern — the
exercise used `copy(deep=False)` + single-cell write to demonstrate the
CoW-off propagation, and column writes on slices silently not propagating.
The lesson: never rely on aliasing behavior; write mode-independent code.

---

### Question 18 [Hard]
**Which statement about `safe_pct_change` (fill_method=None) is TRUE?**

A) It fills gaps with 0
B) Every NaN-window becomes NaN — missing data surfaces and the human
decides how to treat it
C) It is slower than the default
D) It raises on NaN

**Correct Answer:** B
**Explanation:** `fill_method=None` disables the ffill: any window whose
previous value is missing yields NaN. This is the honest default for
financial dashboards — a "no change" must never be fabricated from a gap.

---

### Question 19 [Hard]
**`iterrows` and `itertuples` return the SAME values in the exercise, yet
one is ~50x slower. What is the structural reason?**

A) `iterrows` uses more memory
B) `iterrows` builds a full Series (name, index, dtype checks) per row;
`itertuples` yields lightweight named tuples
C) `itertuples` skips NaN
D) `iterrows` sorts rows

**Correct Answer:** B
**Explanation:** Per-row Series construction is the cost: ~0.579s vs
~0.012s on 20k rows. Vectorized operations are yet another order faster.
Same answer, three cost classes — the trap is that ALL return correct
values, so the cost is invisible until scale.

---

### Question 20 [Hard]
**Which code fragment fails LOUDLY instead of silently corrupting data?**

A) `df[df.a > 2]["flag"] = 1`
B) `df.merge(profile, on="cust")` with duplicate customers
C) `assert profile["cust"].is_unique` before the merge
D) `s[s != np.nan]`

**Correct Answer:** C
**Explanation:** A, B, D all "work" while silently doing the wrong thing.
An explicit `assert is_unique` (or the challenge's ValueError guard) makes
the invariant checkable — pandas will never volunteer that it forgave a
bug.

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|---|--------|
| 1 | B | 6 | C | 11 | B | 16 | B |
| 2 | B | 7 | B | 12 | B | 17 | B |
| 3 | B | 8 | B | 13 | B | 18 | B |
| 4 | B | 9 | A | 14 | B | 19 | B |
| 5 | B | 10 | B | 15 | B | 20 | C |

## Scoring Guide

| Score | Proficiency |
|-------|-------------|
| 18-20 | Expert — you will not be bitten by pandas forgiveness |
| 14-17 | Proficient — review CoW semantics and chained writes |
| 10-13 | Developing — redo lecture 44 and the bug-hunt challenge |
| < 10 | Beginner — study the pitfalls catalog before proceeding |
