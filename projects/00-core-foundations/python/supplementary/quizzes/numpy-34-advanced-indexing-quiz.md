# NumPy 34 — Advanced Indexing Quiz

20 questions · 6 Easy · 9 Medium · 5 Hard · ≥8 code-output.
Answers with full explanations and distractor analysis at the end.

---

## Easy

**E1 (code-output).** What prints?
```python
import numpy as np
scores = np.array([0.9, 0.4, 0.7, 0.2, 0.8])
print(scores[[3, 0, 4]])
```

- A) `[0.9 0.4 0.7 0.2 0.8]`
- B) `[0.2 0.9 0.8]`
- C) `[0.4 0.2 0.8]`
- D) `[0.2 0.7 0.8]`

**E2 (code-output).** What prints?
```python
import numpy as np
x = np.array([1.0, -2.0, 3.0, -4.0])
print(x[x > 0.0])
print((x > 0.0).sum())
```

- A) `[1. 3.]`, `2`
- B) `[1. -2. 3. -4.]`, `4`
- C) `[1. 3.]`, `4`
- D) `[3. 1.]`, `2`

**E3.** Fancy indexing `x[[0, 2]]` returns:

- A) a view sharing memory with `x`
- B) a copy that never shares memory with `x`
- C) a view if the indices are ascending, else a copy
- D) a new array that becomes a view after `reshape`

**E4 (code-output).** What prints?
```python
import numpy as np
x = np.arange(6)
print(np.take(x, [7, 8], mode="wrap"))
print(np.take(x, [-3, 9], mode="clip"))
```

- A) `[1 2]`, `[0 5]`
- B) `[7 8]`, `[-3 9]`
- C) `[0 1]`, `[3 5]`
- D) raises `IndexError` twice

**E5.** Which function returns the indices of the k largest elements without a full sort?

- A) `np.argsort(x)[:k]`
- B) `np.argpartition(x, -k)[-k:]`
- C) `np.argmax(x, axis=-1)` repeated k times
- D) `np.searchsorted(x, k)`

**E6 (code-output).** What prints?
```python
import numpy as np
bins = np.array([0.0, 0.5, 1.0])
print(np.digitize([0.0, 0.5, 0.75], bins))
```

- A) `[0 1 1]`
- B) `[1 2 2]`
- C) `[0 0 1]`
- D) `[0 1 2]`

---

## Medium

**M1 (code-output).** What prints?
```python
import numpy as np
M = np.arange(20.0).reshape(4, 5)
rows = np.array([0, 3])
cols = np.array([1, 2, 4])
print(M[np.ix_(rows, cols)].shape)
print(M[np.ix_(rows, cols)][0, 1])
```

- A) `(2, 3)`, `2.0`
- B) `(2, 3)`, `17.0`
- C) `(2, 2)`, `2.0`
- D) `(2, 3)`, `1.0`

**M2.** `x[::2][0] = 99` on a float array — what happens to `x`?

- A) Nothing; the slice is a copy
- B) `x[0]` becomes 99 — `x[::2]` is a view
- C) Raises `ValueError` — read-only view
- D) `x[1]` becomes 99 — stride offset

**M3 (code-output).** What prints?
```python
import numpy as np
base = np.arange(8.0)
a = base[::2]
b = base[[0, 2, 4]]
print(np.shares_memory(base, a))
print(np.shares_memory(base, b))
```

- A) `True`, `True`
- B) `True`, `False`
- C) `False`, `True`
- D) `False`, `False`

**M4.** `np.argpartition(x, 4)[:4]` guarantees:

- A) the 4 smallest elements, sorted ascending
- B) the 4 smallest elements, unsorted
- C) the 4 largest elements, unsorted
- D) exactly the elements at indices 0–4 of `x`

**M5 (code-output).** What prints?
```python
import numpy as np
bins = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
v = np.array([0.05, 0.25, 0.8, 2.0, -1.0])
print(np.searchsorted(bins, v, side="right"))
```

- A) `[1 2 4 5 0]`
- B) `[0 1 3 4 0]`
- C) `[1 1 4 5 0]`
- D) `[1 2 4 4 0]`

**M6.** You need every pair `(row_i, col_j)` value for rows `[1, 4]` and cols `[0, 3]` of a matrix. `M[[1, 4], [0, 3]]` gives:

- A) the 2×2 grid — same as `np.ix_`
- B) a 2-element diagonal pairing: `(1,0)` and `(4,3)`
- C) a 4-element flattened selection
- D) raises — mixed integer indexing is invalid

**M7 (code-output).** What prints?
```python
import numpy as np
x = np.array([-3.0, 1.0, -2.0, 4.0])
x[x < -1.0] = -1.0
print(x)
```

- A) `[-3.  1. -2.  4.]`
- B) `[-1.  1. -1.  4.]`
- C) `[-1. -1. -1. -1.]`
- D) `[-3.  1. -1.  4.]`

**M8.** Which statement about `np.unique(labels, return_counts=True)` is true?

- A) It requires labels to be integers
- B) The counts sum to the number of elements
- C) It returns labels sorted by count, descending
- D) It only works on 1-D arrays of shape `(n,)` — 2-D fails

**M9 (code-output).** What prints?
```python
import numpy as np
x = np.array([3.0, 1.0, 2.0])
print(np.argsort(x))
print(x[np.argsort(x)])
```

- A) `[1 2 0]`, `[1. 2. 3.]`
- B) `[0 2 1]`, `[3. 2. 1.]`
- C) `[1 2 0]`, `[3. 1. 2.]`
- D) `[0 1 2]`, `[1. 2. 3.]`

---

## Hard

**H1 (code-output).** What prints?
```python
import numpy as np
rng = np.random.default_rng(42)
X = rng.normal(size=(6, 4))
S = X[rng.permutation(X.shape[0])]
S[:] = 0.0
print(X[0, 0] == 0.0, np.shares_memory(X, S))
```

- A) `True`, `True`
- B) `True`, `False`
- C) `False`, `False`
- D) `False`, `True`

**H2.** A retrieval service computes cosine scores `s` for 1M candidates and needs top-50. The best choice and reason:

- A) `np.sort(s)[-50:]` — sort is the clearest, cost O(n log n) is fine
- B) `np.argpartition(s, -50)[-50:]` — O(n), no full order needed; sort only the 50 winners
- C) `np.argsort(s)[-50:]` — returns indices AND sorts
- D) `np.max(s)` in a loop — reads each element once

**H3 (code-output).** What prints?
```python
import numpy as np
bins = np.array([0.0, 0.5, 1.0])
v = np.array([0.0, 0.5, 0.75])
print(np.searchsorted(bins, v, side="left"))
print(np.searchsorted(bins, v, side="right"))
```

- A) `[0 1 2]`, `[1 2 2]`
- B) `[0 1 1]`, `[1 2 2]`
- C) `[1 2 2]`, `[0 1 2]`
- D) `[0 1 2]`, `[0 1 2]`

**H4.** `X` is `(100_000, 128)` float64 (102 MB). You must find the 10 nearest rows to a query. Which memory behavior is correct for the efficient solution?

- A) Peak ≈ 200 MB — a full 100k×100k distance matrix is unavoidable
- B) Peak ≈ 102 MB + O(n) — one broadcast subtract (X − query), one distance vector, one index array; `argpartition` needs no distance matrix
- C) Peak ≈ 0 — distances can be computed in registers
- D) Peak ≈ 102 MB — `argsort` reuses the input buffer

**H5.** `x` is sorted ascending. `np.searchsorted(x, v, side="left")` returns `k`. Which statement is always true?

- A) `x[k] == v` when `v` is present
- B) `k` is the count of elements strictly less than `v`
- C) `k` is the count of elements ≤ `v`
- D) `x[k-1] < v ≤ x[k]` for all `k` (with boundary conventions)

---

## Answer Key

**E1 — B.** Fancy indexing selects in the given order: indices 3, 0, 4 → values 0.2, 0.9, 0.8.
*Distractors:* A ignores the indices; C/D use wrong index→value mappings.

**E2 — A.** The mask keeps positives: [1.0, 3.0]; `(x > 0.0).sum()` counts True = 2.
*Distractors:* B returns the whole array (no filter); C confuses the count with the array size; D reverses order (fancy order is preserved, not sorted).

**E3 — B.** Integer-array (fancy) indexing always produces a new array — a copy.
*Distractors:* A is the view rule for basic slices; C invents a conditional rule; D is meaningless (reshape is unrelated).

**E4 — A.** `wrap` modulo-6: 7→1, 8→2; `clip` clamps to [0, 5]: −3→0, 9→5.
*Distractors:* B is no mode at all; C misapplies wrap/clip; D is the `raise` behavior, not these modes.

**E5 — B.** `argpartition` is the O(n) partial-sort index tool; `[-k:]` selects the k largest partition.
*Distractors:* A is a full sort; C is O(k·n); D is bucketing, not ranking.

**E6 — B.** `digitize` ≡ `searchsorted(side="right")`: 0.0→1, 0.5→2, 0.75→2 (edges `[0, 0.5, 1]`).
*Distractors:* A is the `side="left"` variant for 0.0/0.5 but misplaces 0.75; C/D mix conventions.

**M1 — A.** `np.ix_` gives the (2, 3) grid; `[0, 1]` = row 0 of `[0, 3]` (M[0]=[0,1,2,3,4]), col 1 → 1.0… wait: row index 0 → M row 0 → cols [1, 2, 4] → grid[0] = [1., 2., 4.]; grid[0, 1] = 2.0. ✓ A.
*Distractors:* B indexes `[0, 1]` as the second row's value at column 0 of cols (M[3][1] = 17.0 — that's grid[1, 1]… no, grid[1] = [16., 17., 19.], grid[1,0]=16, grid[1,1]=17 — B is grid[1,1] misplaced); C assumes 2×2 pairing; D is the unpaired elementwise `M[rows, cols]` = [M[0,1], M[3,2]] → [1., 17.] — first element 1.0.

**M2 — B.** `x[::2]` is a basic slice → view; writing through it changes `x[0]`.
*Distractors:* A is the fancy-indexing rule; C is false (views are writable unless read-only); D misplaces the stride offset.

**M3 — B.** `base[::2]` is a view (shares memory); `base[[0, 2, 4]]` is fancy indexing → copy.
*Distractors:* A assumes both share; C/D reverse the semantics.

**M4 — B.** `argpartition(x, 4)` puts the 4th-smallest at position 4 with smaller-or-equal values before it — unsorted.
*Distractors:* A adds sorting (not guaranteed); C flips to largest; D misreads the partition semantics.

**M5 — A.** `side="right"`: first edge > v: 0.05→1; 0.25→2 (edge 0.25 is not > 0.25; next is 0.5); 0.8→4; 2.0→5 (beyond end); −1.0→0.
*Distractors:* B is the `side="left"` set; C misplaces 0.25 (counts it as its own bucket); D drops the beyond-end case.

**M6 — B.** `M[[1, 4], [0, 3]]` pairs indices elementwise — a 2-element selection.
*Distractors:* A is what `np.ix_` does (the trap this question exposes); C is the flattened `M[rows][:, cols]` size only via ix_; D is false — mixed integer indexing is valid.

**M7 — B.** Masked assignment clamps both −3.0 and −2.0 to −1.0; 1.0 and 4.0 untouched.
*Distractors:* A shows no write; C clamps everything; D clamps only one value.

**M8 — B.** Counts always partition the input: sum == n.
*Distractors:* A is false (works on any hashable-ish sortable dtype); C is false (sorted by *value*, not count); D is false — `unique` flattens (use `axis=0` for rows in newer NumPy).

**M9 — A.** `argsort` gives the permutation [1, 2, 0]; indexing recovers the sorted array.
*Distractors:* B/C/D shuffle the permutation or the values incorrectly.

**H1 — C.** `rng.permutation` + fancy indexing → copy; writing through `S` does NOT touch `X`; `shares_memory` is False. The whole point of the pattern: shuffle *copies* so training data stays intact.
*Distractors:* A assumes the copy writes through (view semantics); B is contradictory (True shares + isolated write); D is the view behavior you'd get from `X[::2]`.

**H2 — B.** `argpartition` is O(n) and returns indices; only the 50 winners need sorting (the `np.sort` on the slice).
*Distractors:* A sorts the whole array (O(n log n)) and returns values, not indices; C is a full sort; D is O(n·k) and Python-slow.

**H3 — A.** `side="left"`: first bin ≥ v → [0, 1, 2]. `side="right"`: first bin > v → 0.0→1, 0.5→2, 0.75→2.
*Distractors:* B misapplies "left" (0.75 should map to index 2: bin 1.0 ≥ 0.75); C swaps the two; D claims they're identical (they differ exactly on boundary hits).

**H4 — B.** The efficient solution materializes one `(n, d)` subtraction (≈ input), one `(n,)` distance vector, and one `(n,)` index buffer — no distance matrix, no full-sort buffer.
*Distractors:* A is the brute-force matrix (n² — catastrophic); C is impossible (arrays live in memory); D is false — `argsort` allocates a fresh index array, and you don't need its full order anyway.

**H5 — B.** With `side="left"`, the insertion index equals the count of elements strictly less than v — by definition of the first position where `x[i] >= v`.
*Distractors:* A is false when v is absent; C is the `side="right"` count; D misstates the boundary (for v below all elements, k=0 and `x[-1]` is not < v).

---

**Scoring:** 17+ Expert · 13–16 Practitioner · 8–12 Proficient · <8 Novice.
**Related:** [Lecture 34](03-libraries/numpy/lectures/34-advanced-indexing-lecture.md) ·
[Glossary 34](03-libraries/numpy/lectures/34-advanced-indexing-glossary.md) ·
[Challenge 34](03-libraries/numpy/challenges/34-advanced-indexing/README.md)
