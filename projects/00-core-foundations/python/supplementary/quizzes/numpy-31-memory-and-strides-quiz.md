# NumPy 31 — Memory and Strides Quiz

## Topic Overview
Strides, C vs Fortran order, view vs copy, `ascontiguousarray`,
cache locality, and `nbytes` accounting. These mechanics decide
whether a "cheap" pipeline line allocates gigabytes.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer
- Difficulty mix: 6 Easy / 9 Medium / 5 Hard

---

## Questions

### Question 1 (Easy)
**What are the strides of a C-contiguous float64 array of shape
`(4, 6)`?**

A) `(8, 48)`
B) `(48, 8)`
C) `(32, 8)`
D) `(4, 6)`

**Difficulty:** Easy

### Question 2 (Easy)
**Which operation always returns a copy, never a view?**

A) `a[1:3]`
B) `a.T`
C) `a.astype(np.float32)`
D) `a.reshape(2, 6)` on a contiguous `(3, 4)` array

**Difficulty:** Easy

### Question 3 (Easy)
**For a 1-D array `a`, what does `a.T` return?**

A) A shape `(n, 1)` copy
B) A view of the same shape — transpose is a no-op on 1-D
C) A shape `(1, n)` view
D) A `ValueError`

**Difficulty:** Easy

### Question 4 (Easy)
**What does `arr.base is None` mean?**

A) The array is a view
B) The array owns its data buffer
C) The array is empty
D) The array is Fortran-contiguous

**Difficulty:** Easy

### Question 5 (Easy)
**What is the `nbytes` of `np.zeros((1000, 1000), dtype=np.float32)`?**

A) 1,000,000 bytes
B) 4,000,000 bytes
C) 8,000,000 bytes
D) 1000 bytes

**Difficulty:** Easy

### Question 6 (Easy)
**Which layout keeps the LAST axis contiguous?**

A) Fortran order
B) C order (row-major)
C) Both
D) Neither

**Difficulty:** Easy

### Question 7 (Medium)
**What does this code print?**

```python
import numpy as np
a = np.arange(12).reshape(3, 4)
print(a.T.strides)
```

A) `(32, 8)`
B) `(8, 32)`
C) `(16, 4)`
D) `(4, 16)`

**Difficulty:** Medium

### Question 8 (Medium)
**What does this code print?**

```python
import numpy as np
a = np.arange(10)
b = a[2:5]
b[0] = 99
print(a[2])
```

A) `2`
B) `99`
C) `0`
D) `ValueError`

**Difficulty:** Medium

### Question 9 (Medium)
**Which expression returns `True`?**

A) `np.ascontiguousarray(a) is a` for any `a`
B) `np.ascontiguousarray(a.T) is a.T` for any 2-D `a`
C) `np.ascontiguousarray(a) is a` for C-contiguous `a`
D) `np.ascontiguousarray(a).base is a` for any `a`

**Difficulty:** Medium

### Question 10 (Medium)
**What does this code print?**

```python
import numpy as np
a = np.arange(12).reshape(3, 4)
print(a.reshape(4, 3).base is a)
```

A) `False` — reshape always copies
B) `True` — layout-compatible reshape is a view
C) It raises `ValueError`
D) `None`

**Difficulty:** Medium

### Question 11 (Medium)
**Why does a strided access pattern (e.g., reading column-wise on a
C-contiguous array) cost more memory traffic?**

A) It uses more CPU registers
B) Each 64-byte cache line is only partially used, so more lines
must be fetched
C) NumPy copies the array implicitly
D) It triggers garbage collection

**Difficulty:** Medium

### Question 12 (Medium)
**What does this code print?**

```python
import numpy as np
a = np.zeros((1000, 1000), dtype=np.float64)
b = a[:, 0]
print(b.nbytes, b.base is a)
```

A) `8000 True`
B) `8000000 True`
C) `8000 False`
D) `8000000 False`

**Difficulty:** Medium

### Question 13 (Medium)
**Which of these operations on a `(10000, 768)` float32 array
allocates the most memory?**

A) `X[100:200]`
B) `X.T`
C) `X.astype(np.float64)`
D) `np.ascontiguousarray(X)`

**Difficulty:** Medium

### Question 14 (Medium)
**What does this code print?**

```python
import numpy as np
a = np.arange(6)
print(np.shares_memory(a, a[::2]))
```

A) `False` — strided slicing copies
B) `True` — strided slicing is a view
C) It raises — shapes differ
D) `None`

**Difficulty:** Medium

### Question 15 (Medium)
**When does `np.ascontiguousarray(x)` copy `x`?**

A) Always
B) Never
C) When `x` is not C-contiguous (e.g., a transpose or F-order view)
D) When `x` is larger than the L3 cache

**Difficulty:** Medium

### Question 16 (Hard)
**What does this code print?**

```python
import numpy as np
a = np.arange(12).reshape(3, 4)
b = a.T
print(b.reshape(12).base is a)
```

A) `True` — reshape is always a view
B) `False` — reshaping a non-contiguous view copies
C) It raises `ValueError`
D) `None`

**Difficulty:** Hard

### Question 17 (Hard)
**An embedding matrix `E` of shape `(1_000_000, 768)` float32 is
served from memory. Which pipeline step allocates an extra
~3 GB buffer?**

A) `batch = E[start:end]` — row slice
B) `batch = E[[i for i in range(0, 1000)]]` — fancy index
C) `batch = E[start:end].copy()`
D) Both B and C

**Difficulty:** Hard

### Question 18 (Hard)
**What is the byte offset of element `(2, 3)` in a C-contiguous
float64 array of shape `(4, 6)`?**

A) 48
B) 120
C) 96
D) 192

**Difficulty:** Hard

### Question 19 (Hard)
**A C/Fortran kernel receives a transposed view and iterates it
naively. The 10× slowdown comes from:**

A) The transpose allocating a full copy
B) Cache-miss amplification: each strided step wastes most of a
cache line
C) Python overhead in the kernel
D) The kernel re-checking contiguity per element

**Difficulty:** Hard

### Question 20 (Hard)
**What does this code print?**

```python
import numpy as np
a = np.arange(8).reshape(2, 4)
b = a[0:1, :]
c = np.ascontiguousarray(a)
print(b.base is a, c is a)
```

A) `False False`
B) `True True`
C) `True False`
D) `False True`

**Difficulty:** Hard

---

## Score Tracking

Count your correct answers: _____ / 20

**Scoring Guide:** 18–20 → expert; 14–17 → solid, review the failed
areas; 10–13 → re-read the lecture; below 10 → rerun the exercise and
print `base`, `strides`, and `nbytes` for every array you create.

## Answer Key

1. **B) `(48, 8)`** — last axis steps itemsize (8); axis 0 steps
6×8=48. A is the transposed pattern; C is a 3×4 array's strides;
D is the shape.
2. **C) `a.astype(np.float32)`** — dtype change cannot share a byte
map. A/B are views; D is a view for contiguous input.
3. **B) A view of the same shape** — `.T` is a no-op on 1-D data.
A/C invent new shapes; D misapplies broadcasting errors.
4. **B) The array owns its data buffer** — `base` is `None` exactly
for self-owned arrays. A is the opposite reading; C/D are unrelated.
5. **B) 4,000,000 bytes** — 1e6 elements × 4 bytes. A forgets
itemsize; C uses float64; D uses the wrong dimension.
6. **B) C order (row-major)** — last axis contiguous. Fortran keeps
the FIRST axis contiguous; the others are false.
7. **B) `(8, 32)`** — `.T` swaps strides: axis 0 steps 8, axis 1
steps 4×8=32. A is the original; C/D use float32-sized values.
8. **B) `99`** — the slice is a view; the write propagates to `a`.
A ignores aliasing; C is the pre-write value; D is wrong.
9. **C) `np.ascontiguousarray(a) is a` for C-contiguous `a`** — the
fast path is identity. A fails for non-contiguous input; B fails
because `.T` of C data is copied; D is never reliably true.
10. **B) `True`** — reshaping a C-contiguous array in a
layout-compatible way is a view. A is the common myth; C/D are
nonsense.
11. **B)** — partial cache-line use forces more line fetches. A/C/D
misidentify the mechanism; this is the physical cost of strides.
12. **A) `8000 True`** — a column view reports its logical 8000
bytes but shares `a`'s buffer. B double-counts; C/D break the
aliasing fact.
13. **C) `X.astype(np.float64)`** — doubles itemsize: ~61 MB. A/B
are O(1) views; D is a no-op on C-contiguous input.
14. **B) `True`** — `a[::2]` is a strided *view*. A is the myth;
C/D are wrong.
15. **C) When `x` is not C-contiguous** — identity otherwise. A/B
are absolutes; D invents a size trigger.
16. **B) `False`** — `b` is an F-order view; a layout-incompatible
reshape copies. A is the false general rule; C/D are wrong.
17. **D) Both B and C** — fancy indexing copies (~3 MB for 1000
rows of 768 float32 — small here, but scaled to full-index
selection it is the whole matrix), and `.copy()` is explicit.
A is a view. The trap is that B *looks* like A.
18. **B) 120** — 2×48 + 3×8. A is one axis alone; C mis-multiplies;
D is the total size.
19. **B)** — each strided step fetches a line and uses 8 of 64
bytes. A is false (`.T` is a view); C/D misattribute the cost.
20. **B) `True True`** — `b` is a slice view of `a`; `c` is the
same object because `a` is already C-contiguous. The other pairs
misread one of the two facts.
