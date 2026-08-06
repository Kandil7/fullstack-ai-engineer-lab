# NumPy 30 — Vectorization Quiz

## Topic Overview
Loop → vectorized rewrites, `np.where` vs branches, masking, `einsum`,
honest loop exceptions, and why `np.vectorize` is not fast. These are
the rewrite patterns behind every embedding hot path.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer
- Difficulty mix: 6 Easy / 9 Medium / 5 Hard

---

## Questions

### Question 1 (Easy)
**Which expression computes ReLU (`max(x, 0)`) elementwise?**

A) `np.maximum(x, 0)`
B) `np.max(x, 0)`
C) `x.max(0)`
D) `max(x, 0)`

**Difficulty:** Easy

### Question 2 (Easy)
**What is the value of `np.array_equal(np.einsum("ij->ji", A), A.T)` for
any 2-D array `A`?**

A) `False` — einsum sums over `i`
B) `True` — `ij->ji` is the transpose
C) `False` — einsum requires `np.transpose`
D) It raises `ValueError`

**Difficulty:** Easy

### Question 3 (Easy)
**What does `vals[mask].sum()` compute, where `mask = vals > 0`?**

A) The sum of all values
B) The sum of positive values
C) The count of positive values
D) The sum of negative values

**Difficulty:** Easy

### Question 4 (Easy)
**What does this code print?**

```python
import numpy as np
x = np.array([-2.0, 3.0, -1.0])
print(np.where(x > 0, x, 0.0))
```

A) `[-2. 3. -1.]`
B) `[0. 3. 0.]`
C) `[-2. 0. -1.]`
D) `[0. 0. 0.]`

**Difficulty:** Easy

### Question 5 (Easy)
**Which statement about `np.vectorize` is true?**

A) It compiles the function to C and is as fast as a ufunc
B) It calls the Python function once per element — a loop in disguise
C) It is only usable with `numba`
D) It is required for broadcasting to work

**Difficulty:** Easy

### Question 6 (Easy)
**What is the shape of `np.einsum("i,j->ij", np.ones(3), np.ones(4))`?**

A) `(3,)`
B) `(4,)`
C) `(3, 4)`
D) `(12,)`

**Difficulty:** Easy

### Question 7 (Medium)
**What does this code print?**

```python
import numpy as np
A = np.arange(9).reshape(3, 3)
print(np.einsum("ii->", A))
```

A) `9`
B) `12`
C) `36`
D) `3`

**Difficulty:** Medium

### Question 8 (Medium)
**What does this code print?**

```python
import numpy as np
vals = np.array([1.0, -2.0, 3.0, -4.0])
vals[vals < 0] = 0.0
print(vals)
```

A) `[1. -2. 3. -4.]`
B) `[1. 0. 3. 0.]`
C) `[0. 0. 0. 0.]`
D) `[1. 2. 3. 4.]`

**Difficulty:** Medium

### Question 9 (Medium)
**Which of these is the correct batched matmul via einsum for
`batch` of shape `(8, 4, 5)` and `B` of shape `(5, 6)`?**

A) `np.einsum("bij,bjk->bik", batch, B)`
B) `np.einsum("bij,jk->bik", batch, B)`
C) `np.einsum("bij,jk->bjk", batch, B)`
D) `np.einsum("ij,jk->ik", batch, B)`

**Difficulty:** Medium

### Question 10 (Medium)
**What does this code print?**

```python
import numpy as np
x = np.array([0.5, 2.0, -1.5])
print(np.clip(x, 0.0, 1.0))
```

A) `[0.5 2. -1.5]`
B) `[0.5 1. 0.]`
C) `[0. 1. 0.]`
D) `[0.5 1. -1.5]`

**Difficulty:** Medium

### Question 11 (Medium)
**For `X` of shape `(100, 3)`, what happens with
`X - X.mean(axis=1)`?**

A) It centers each row correctly
B) It centers each column correctly
C) It raises `ValueError` — `(100,)` clashes with the trailing 3
D) It returns a scalar

**Difficulty:** Medium

### Question 12 (Medium)
**Why is `np.fromiter((f(v) for v in arr), dtype=float)` still slow?**

A) It allocates a huge buffer
B) It still visits every element through the Python interpreter
C) `fromiter` sorts the result
D) It converts to float32 by default

**Difficulty:** Medium

### Question 13 (Medium)
**What does this code print?**

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(np.einsum("i,i->", a, b))
```

A) `[10 40 90]`
B) `140`
C) `60`
D) `(3,)`

**Difficulty:** Medium

### Question 14 (Medium)
**Which masked expression returns the count of values in `[0, 10)`?**

A) `(vals >= 0) & (vals < 10)`
B) `np.sum(vals >= 0 & vals < 10)`
C) `np.count((vals > 0) | (vals < 10))`
D) `len(vals[np.logical_and(vals, 10)])`

**Difficulty:** Medium

### Question 15 (Medium)
**What does this code print?**

```python
import numpy as np
X = np.random.default_rng(0).normal(size=(10_000, 4))
out = np.where(X > 0, X, -X)
print(np.allclose(out, np.abs(X)))
```

A) `False` — where has different rounding
B) `True`
C) It raises because shapes differ
D) `nan`

**Difficulty:** Medium

### Question 16 (Hard)
**What does this code print?**

```python
import numpy as np
x = np.array([1.0, 2.0, 3.0])
y = np.where(x > 1, np.where(x > 2, "big", "mid"), "small")
print(y)
```

A) `['small' 'mid' 'big']`
B) `['big' 'mid' 'small']`
C) `['small' 'big' 'mid']`
D) Raises `TypeError` — where needs numeric arrays

**Difficulty:** Hard

### Question 17 (Hard)
**You must z-score each row of `X` shape `(1_000_000, 64)`. Which
expression is correct AND keeps memory at O(n·d)?**

A) `(X - X.mean(axis=1)) / X.std(axis=1)`
B) `(X - X.mean(axis=1, keepdims=True)) / X.std(axis=1, keepdims=True)`
C) `(X - X.mean(axis=0)) / X.std(axis=0)`
D) `(X - X.mean(axis=1)[None, :]) / X.std(axis=1)[None, :]`

**Difficulty:** Hard

### Question 18 (Hard)
**What does this code print?**

```python
import numpy as np
arr = np.arange(6).reshape(2, 3)
out = np.einsum("ij->ji", arr)
print(out)
```

A) `[[0 1 2] [3 4 5]]`
B) `[[0 3] [1 4] [2 5]]`
C) `[0 1 2 3 4 5]`
D) `[[0 1] [2 3] [4 5]]`

**Difficulty:** Hard

### Question 19 (Hard)
**Which statement about the loop-outer/vectorize-inner pattern for
ragged rows is correct?**

A) Python overhead scales with total element count
B) Python overhead scales with row count; each body is compiled
C) It requires `np.vectorize` to be fast
D) It is never necessary — ragged data can always be padded for free

**Difficulty:** Hard

### Question 20 (Hard)
**What does this code print?**

```python
import numpy as np
x = np.array([1.0, -1.0])
mask = x > 0
print(np.where(mask, x, x * 10).sum())
```

A) `-9.0`
B) `1.0`
C) `-19.0`
D) `2.0`

**Difficulty:** Hard

---

## Score Tracking

Count your correct answers: _____ / 20

**Scoring Guide:** 18–20 → expert; 14–17 → solid, review the failed
areas; 10–13 → re-read the lecture; below 10 → redo the exercise with
a printed reference loop beside each vectorized expression.

## Answer Key

1. **A) `np.maximum(x, 0)`** — elementwise max; it is a ufunc.
`np.max` reduces (wrong shape); `x.max(0)` reduces over axis 0;
`max(x, 0)` is Python scalar logic and fails on arrays.
2. **B) `True`** — `ij->ji` swaps axes = transpose. A misreads the
notation; C adds an unnecessary function; D is false.
3. **B) The sum of positive values** — the mask selects, `.sum()`
aggregates. A ignores the mask; C confuses count with sum; D is the
complement.
4. **B) `[0. 3. 0.]`** — where keeps `x` for positives, 0 otherwise.
A is the input; C zeroes the positives; D zeroes everything.
5. **B) It calls the Python function once per element** — vectorize
adds a call signature, not speed. A is the common myth; C ties it to
numba; D is false — broadcasting works on plain ufuncs.
6. **C) `(3, 4)`** — `i,j->ij` is the outer product shape. A/B are
input shapes; D is the flattened size, not the shape.
7. **B) `12`** — `ii->` sums the diagonal: 0+4+8. A is 3²; C is the
total sum; D is the matrix dimension.
8. **B) `[1. 0. 3. 0.]`** — mask-assign zeroes negatives. A shows no
update; C zeroes everything; D takes absolute values.
9. **B) `np.einsum("bij,jk->bik", batch, B)`** — the batch axis `b`
belongs to the first operand and output; `B` is 2-D so it has no `b`.
A assigns `b` to a 2-D array (raises); C/D name the output wrong.
10. **B) `[0.5 1. 0.]`** — clip clamps 2.0 → 1.0 and -1.5 → 0.0.
A shows no clamping; C clamps 0.5 wrongly; D leaves -1.5 below lo.
11. **C) It raises `ValueError`** — `(100, 3)` vs `(100,)`: trailing 3
vs 100 clash. A/B both misidentify the result; D is nonsense.
12. **B) It still visits every element through the Python interpreter**
— `fromiter` is a construction tool, not a speedup. A is wrong (the
buffer is sized); C is false; D is false.
13. **B) `140`** — `i,i->` is the dot product: 10+40+90. A is the
elementwise product; C is the sum of `a` times 20 by accident; D is
a shape, not a value.
14. **A) `(vals >= 0) & (vals < 10)`** — combined masks, and `sum()`
counts True. B mis-parenthesizes (needs parentheses around each
comparison); C uses the wrong operator and function; D is invalid.
15. **B) `True`** — `where(x>0, x, -x)` is exactly `abs`. A invents
rounding differences; C/D are false.
16. **A) `['small' 'mid' 'big']`** — nested where reads as
if/elif/else; values above 2 get "big". B reverses the order; C
misplaces "mid"; D is false — where handles strings.
17. **B) `keepdims=True` on both reductions** — the means and stds
stay at `(n, 1)`, broadcasting along columns; no extra arrays beyond
the result. A raises (`(n,)` clashes with trailing 64); C z-scores
columns, not rows; D puts the row vector on the *wrong* side —
`(1, n)` vs `(n, 64)` raises for n ≠ 64.
18. **B) `[[0 3] [1 4] [2 5]]`** — transpose of the 2×3 array. A is
the input; C is flattened; D is a different reshape.
19. **B) Python overhead scales with row count; each body is compiled**
— that is the whole pattern. A describes the doubly-nested loop; C
misuses vectorize; D ignores raggedness.
20. **A) `-9.0`** — where keeps 1.0 for the positive and 10×(-1) =
-10 for the negative; sum = -9. B ignores the negative branch; C
mixes sign conventions; D double-counts.
