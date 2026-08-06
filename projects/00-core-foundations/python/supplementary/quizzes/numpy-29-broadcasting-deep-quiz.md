# NumPy 29 — Broadcasting Deep Quiz

## Topic Overview
Broadcasting rules, `newaxis`, silent allocation, `(n,)` vs `(n,1)`,
`keepdims`, and failure cases. These mechanics sit behind every batch
inference expression and most embedding math.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer
- Difficulty mix: 6 Easy / 9 Medium / 5 Hard

---

## Questions

### Question 1 (Easy)
**What is the result shape of `np.ones((3, 1)) + np.ones((1, 4))`?**

A) `(3, 1)`
B) `(1, 4)`
C) `(3, 4)`
D) `ValueError`

**Difficulty:** Easy

### Question 2 (Easy)
**Which expression turns a 1-D array `v` of shape `(n,)` into a column
vector of shape `(n, 1)`?**

A) `v.T`
B) `v[:, None]`
C) `v[None, :]`
D) `v.reshape(1, n)`

**Difficulty:** Easy

### Question 3 (Easy)
**What does `v.T` return for a 1-D array `v = np.array([1, 2, 3])`?**

A) A shape `(3, 1)` array
B) A shape `(1, 3)` array
C) The same shape `(3,)` array — `.T` is a no-op on 1-D data
D) A copy of the array

**Difficulty:** Easy

### Question 4 (Easy)
**What is the shape of `(np.ones((2, 5, 3)) + np.ones((5, 3)))`?**

A) `(2, 5, 3)`
B) `(5, 3)`
C) `(2, 5, 6)`
D) `ValueError`

**Difficulty:** Easy

### Question 5 (Easy)
**Which of these raises `ValueError`?**

A) `np.ones((3, 4)) + np.ones(4)`
B) `np.ones((3, 1)) + np.ones((1, 4))`
C) `np.ones((3, 2)) + np.ones((2, 3))`
D) `np.ones((2, 5, 3)) + np.ones((5, 3))`

**Difficulty:** Easy

### Question 6 (Easy)
**What is `np.broadcast_to(v[:, None], (5, 4))`?**

A) A full `(5, 4)` copy of the stretched array
B) A read-only view of shape `(5, 4)` that allocates nothing
C) An error, because `v` has the wrong dtype
D) A shape `(4, 5)` transposed array

**Difficulty:** Easy

### Question 7 (Medium)
**What does this code print?**

```python
import numpy as np
a = np.arange(3)
b = np.arange(4)
print((a[:, None] * b[None, :]).shape)
```

A) `(3,)`
B) `(4,)`
C) `(3, 4)`
D) `(4, 3)`

**Difficulty:** Medium

### Question 8 (Medium)
**What does this code print?**

```python
import numpy as np
v = np.arange(3)
m = np.ones((3, 4))
print((m + v[:, None]).shape)
```

A) `(3, 4)`
B) `(4, 3)`
C) `(3,)`
D) `ValueError`

**Difficulty:** Medium

### Question 9 (Medium)
**What does this code print?**

```python
import numpy as np
X = np.ones((6, 4))
mu = X.mean(axis=1, keepdims=True)
print((X - mu).shape)
```

A) `(6, 4)`
B) `(6,)`
C) `(4,)`
D) `ValueError`

**Difficulty:** Medium

### Question 10 (Medium)
**What does this code print?**

```python
import numpy as np
labels = np.array([0, 2, 1])
oh = (labels[:, None] == np.arange(3)).astype(np.float32)
print(oh.shape, oh[1].sum())
```

A) `(3, 3)` `1.0`
B) `(3,)` `1.0`
C) `(3, 3)` `2.0`
D) `(3, 2)` `1.0`

**Difficulty:** Medium

### Question 11 (Medium)
**Why does `data - data.mean(axis=0)` center columns correctly while
`data - data.mean(axis=1)` raises for `data` of shape `(100, 3)`?**

A) Because `mean(axis=0)` returns a scalar
B) Because `(3,)` aligns with the trailing axis of `(100, 3)`, while
`(100,)` clashes with it
C) Because `mean(axis=1)` requires float32 input
D) Because NumPy forbids subtracting row means

**Difficulty:** Medium

### Question 12 (Medium)
**What is the memory cost of `a[:, None] * b[None, :]` when `a` and `b`
are both float64 arrays of length 100,000?**

A) 1.6 MB
B) 80 GB
C) 800 KB
D) 160 MB

**Difficulty:** Medium

### Question 13 (Medium)
**Which of the following is `False` about `np.broadcast_to`?**

A) The returned array is read-only
B) It returns a view, not a copy
C) It can produce a writable copy of any stretch
D) It raises if the target shape is not broadcast-compatible

**Difficulty:** Medium

### Question 14 (Medium)
**What does this code print?**

```python
import numpy as np
a = np.ones((3, 1))
b = np.ones((1, 4))
c = a + b
print(c[2, 3], c.shape)
```

A) `1.0 (3, 1)`
B) `2.0 (3, 4)`
C) `2.0 (1, 4)`
D) `1.0 (3, 4)`

**Difficulty:** Medium

### Question 15 (Medium)
**What does this code print?**

```python
import numpy as np
x = np.arange(5)
y = np.broadcast_to(x[:, None], (5, 3))
try:
    y[0, 0] = 99
except ValueError as e:
    print(type(e).__name__)
```

A) `ValueError`
B) `IndexError`
C) Nothing — the write succeeds
D) `TypeError`

**Difficulty:** Medium

### Question 16 (Hard)
**What does this code print?**

```python
import numpy as np
a = np.ones((2, 3))
b = np.ones((3, 2))
try:
    print((a + b).shape)
except ValueError:
    print("raise")
```

A) `(2, 2)`
B) `(3, 3)`
C) `raise`
D) `(2, 3)`

**Difficulty:** Hard

### Question 17 (Hard)
**You z-score a dataset with `z = (X - X.mean(axis=0)) / X.std(axis=0)`
where `X` is `(1000, 50)`. Which statement is true?**

A) Columns are centered; broadcasting relies on trailing alignment
B) Rows are centered; the result is wrong for column-wise z-scoring
C) It raises `ValueError`
D) Both A and B are true depending on dtype

**Difficulty:** Hard

### Question 18 (Hard)
**Which expression computes pairwise L2 distances with O(n·m) memory,
never materializing an `(n, m, d)` tensor?**

A) `np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2))`
B) `np.sqrt(a[:, None] * b[None, :])`
C) `np.sqrt((a * a).sum(1)[:, None] + (b * b).sum(1)[None, :] - 2 * (a @ b.T))`
D) `np.sqrt(np.sum(a) + np.sum(b))`

**Difficulty:** Hard

### Question 19 (Hard)
**What does this code print?**

```python
import numpy as np
v = np.arange(4)
try:
    np.ones((4, 3)) + v[:, None]
except ValueError as e:
    print("raise")
else:
    print("ok")
```

A) `raise` — `(4, 1)` clashes with `(4, 3)` on the first axis
B) `ok` — `(4, 1)` stretches along columns to `(4, 3)`
C) `raise` — `.T` is required first
D) `ok` — the result is `(1, 3)`

**Difficulty:** Hard

### Question 20 (Hard)
**A batch of embeddings `B` is `(128, 768)` and a bias `bias` is
`(768,)`. Which line is both correct and memory-lean for adding the
bias in place?**

A) `B = B + bias`
B) `np.add(B, bias, out=B)`
C) `B += np.broadcast_to(bias, B.shape)`
D) `B = B + np.tile(bias, (128, 1))`

**Difficulty:** Hard

---

## Score Tracking

Count your correct answers: _____ / 20

**Scoring Guide:** 18–20 → expert; 14–17 → solid, review the failed
areas; 10–13 → re-read the lecture; below 10 → redo the exercise with
the shapes printed at every step.

## Answer Key

1. **C) `(3, 4)`** — both size-1 dims stretch to the max of each pair.
A/B are operand shapes, not the result; D misreads compatible dims.
2. **B) `v[:, None]`** — inserts the axis after the length axis.
A is a no-op on 1-D; C makes `(1, n)`; D makes a row too.
3. **C) Same shape `(3,)`** — transpose is a no-op for rank-1. A/B
would require an inserted axis; D confuses views with transpose.
4. **A) `(2, 5, 3)`** — the missing leading dim is treated as 1 and
stretches to 2. B ignores the stretch; C mis-adds dims; D forgets
Rule 3.
5. **C) `(3, 2) + (2, 3)`** — trailing 2 vs 3 clash. A, B, D are all
compatible per the rules.
6. **B) A read-only view of shape `(5, 4)` that allocates nothing** —
that is the whole point of `broadcast_to`. A claims a copy; C is
nonsense; D confuses transpose semantics.
7. **C) `(3, 4)`** — outer product shape n×m. A/B are the inputs' own
shapes; D swaps the operands.
8. **D) `ValueError`** — `(4, 1)` against `(3, 4)`: trailing 4 vs 1 is
fine, then 3 vs 4 clashes. A would require a length-3 column vector.
9. **A) `(6, 4)`** — `keepdims` keeps `(6, 1)`, which broadcasts
against `(6, 4)`. B/C lose the axis; D misapplies the rule.
10. **A) `(3, 3)` `1.0`** — one-hot is `(n, k)`; row 1 has a single 1.
C would need two matches; B/D have wrong shapes.
11. **B)** — `(3,)` aligns with the trailing axis (column mean works);
`(100,)` vs trailing 3 raises. A is false (returns `(3,)`); C and D
misidentify the mechanism.
12. **B) 80 GB** — 100k × 100k × 8 bytes = 8×10¹⁰ bytes. A/C/D
underestimate by orders of magnitude — this is the silent-allocation
trap.
13. **C)** — `broadcast_to` is *always* read-only; it never gives a
writable copy. A, B, D are true properties.
14. **B) `2.0 (3, 4)`** — elementwise add of two 1s gives 2.0; result
is the broadcast shape. A/D show the wrong value; C the wrong shape.
15. **A) `ValueError`** — writing through a `broadcast_to` view raises
`ValueError: assignment destination is read-only`. B/D name the wrong
exception; C is false by design.
16. **C) `raise`** — `(2, 3)` vs `(3, 2)`: trailing 3 vs 2 clash. A/B
would require compatible trailing dims; D is the first operand's shape.
17. **A)** — `(1000, 50) - (50,)` aligns trailing dims, so columns are
centered. B reverses axes; C is false (it runs); D is a non-sequitur.
18. **C)** — the squared-distance identity keeps memory at O(n·m);
the matmul never materializes `(n, m, d)`. A materializes the full
tensor; B computes an outer product, not distances; D is not pairwise.
19. **B) `ok`** — `(4, 1)` vs `(4, 3)`: trailing 1 vs 3 stretches, then
4 vs 4 matches; the column adds along rows. A misreads Rule 2; C's `.T`
is irrelevant; D shows the wrong result shape.
20. **B) `np.add(B, bias, out=B)`** — in-place, no extra `(128, 768)`
allocation. A allocates a new result; C forces a full-size view (then
copies into B); D tiles an explicit `(128, 768)` array — the exact
allocation broadcasting exists to avoid.
