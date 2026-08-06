# NumPy Lecture 31: Memory and Strides

## Topic Overview

An ndarray is a *view over a block of memory*: a pointer, a shape,
a dtype, and a tuple of **strides** that says how many bytes to jump
for each step along each axis. Almost everything that surprises
engineers about NumPy — why `.T` is free, why `reshape` sometimes
copies, why a transposed array is suddenly slow, why `nbytes` lies —
falls out of those four numbers.

This lecture makes the memory model explicit: stride arithmetic,
C vs Fortran order, the view-vs-copy contract (and how to test it),
`ascontiguousarray` as the layout fix, cache-locality reasoning, and
honest memory accounting with `nbytes`. The AI hook: embedding
matrices are gigabytes; knowing whether an operation copies or views
is the difference between a fast feature pipeline and a memory bomb.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Compute the strides of any C- or F-contiguous array from its shape
   and itemsize
2. Explain why `.T` and slices are O(1) views and when they force a
   copy (`ascontiguousarray`)
3. Test view vs copy reliably with `base` (not `is`)
4. Predict which operations copy (fancy indexing, `astype`, `copy()`)
   and which view (slicing, transposing, some `reshape`s)
5. Reason about cache locality: strided access vs sequential access
6. Account for real memory with `nbytes`, `itemsize`, and shared buffers

## Prerequisites

| Need | Where |
|---|---|
| Views vs copies basics | `07-copy-vs-view-lecture.md` |
| Shape and reshape semantics | `08-array-shape-lecture.md`, `09-array-reshape-lecture.md` |
| dtypes and itemsize | `06-data-types-lecture.md` |
| Vectorized operations | `30-vectorization-lecture.md` |

---

## 1. The Four Numbers Behind an ndarray

Every array carries: a pointer to a data buffer, a `shape`, a `dtype`
(which fixes `itemsize`), and `strides`. The byte offset of element
`(i0, i1, ..., ik)` is `sum(ik * strides[k])`.

```python
import numpy as np

arr = np.zeros((4, 6), dtype=np.float64)
print(arr.shape)          # (4, 6)
print(arr.itemsize)       # 8
print(arr.strides)        # (48, 8)
print(arr.nbytes)         # 192
```

```
(4, 6)
8
(48, 8)
192
```

Read `(48, 8)` as: one step along axis 0 jumps 48 bytes (6 elements
× 8 bytes), one step along axis 1 jumps 8 bytes. Element `(2, 3)`
sits at `2*48 + 3*8 = 120` bytes from the start. Strides are the
array's *byte map* — everything else is derived.

---

## 2. C Order vs Fortran Order

C order (row-major, the default) keeps the **last** axis contiguous;
Fortran order (column-major) keeps the **first** axis contiguous.
The two layouts have swapped stride patterns.

```python
c_arr = np.zeros((3, 4), dtype=np.float32)
f_arr = np.asfortranarray(c_arr)

print(c_arr.strides)    # (16, 4)   -- last axis: 1 float (4 B)
print(f_arr.strides)    # (4, 12)   -- first axis contiguous
print(c_arr.flags.c_contiguous)   # True
print(f_arr.flags.f_contiguous)   # True
```

```
(16, 4)
(4, 12)
True
True
```

Fortran order exists for interop with Fortran/BLAS code that walks
columns first. For pure NumPy you almost never need it — but you must
recognize it, because `x.T` of a C array produces an F-ordered view.

---

## 3. Views: Free but Shared

Slicing and transposing create new arrays that **share the same
buffer** — only shape/strides change. The tell is `arr.base`:
`None` means the array owns its buffer; anything else means it is a
view into another array.

```python
base = np.arange(24).reshape(4, 6)

row_view = base[1:3, :]
t_view = base.T

print(row_view.base is not None)   # True -- a view
print(t_view.base is not None)     # True
print(t_view.strides)              # (8, 48) -- swapped

# Writes through the view reach the base:
row_view[0, 0] = -1
print(base[1, 0] == -1)            # True
```

```
True
True
(8, 48)
True
```

A view costs O(1) — no data moved. The price is aliasing: writes
through any view are visible through every other. Feature pipelines
that forget this mutate training data through "temporary" slices.

---

## 4. What Always Copies

Fancy indexing (integer lists/arrays), boolean masks, `astype`, and
`.copy()` produce new buffers. The pattern is consistent: **any
indexing that cannot be expressed as (slice, stride, shape) copies.**

```python
fancy = base[[0, 2], :]
cast = base.astype(np.float64)

print(fancy.base is None)   # True -- fancy indexing copies
print(cast.base is None)    # True -- dtype change copies
```

```
True
True
```

`astype` must copy: a different itemsize cannot share the same byte
map. Fancy indexing must copy: an arbitrary index list has no
stride pattern. Memorize this split — it decides whether a "cheap"
line in your pipeline allocates gigabytes.

---

## 5. `reshape` Is Sometimes a View, Sometimes a Copy

`reshape` returns a view when the new shape can be expressed with
the same buffer order; otherwise it copies. Test with `base`, never
assume.

```python
a = np.arange(12).reshape(3, 4)      # C-contiguous
print(a.reshape(4, 3).base is a)     # True -- view
print(a.T.reshape(12).base is a)     # False -- copy (layout clash)
```

```
True
False
```

`a.T.reshape(12)` would require reading the buffer in a non-C order;
NumPy refuses to produce a "lying" view and copies instead. Rule of
thumb: reshape of a contiguous array is a view; reshape of a
non-contiguous array is a copy.

---

## 6. `ascontiguousarray`: Paying for `.T` Only When Necessary

`np.ascontiguousarray(x)` returns `x` itself when it is already
C-contiguous, and a **copy** otherwise. It is the standard idiom for
"make this kernel-friendly, but don't waste memory if it already is."

```python
base = np.arange(24).reshape(4, 6)
t = base.T                     # F-order view

print(np.ascontiguousarray(base) is base)   # True -- no copy
print(np.ascontiguousarray(t) is not t)     # True -- copy
print(np.ascontiguousarray(t).strides)      # (48, 8) -- C layout
```

```
True
True
(48, 8)
```

This is the pattern every wrapper around C/Fortran code uses: the
caller's layout is honored when possible, repaired otherwise. The
copy cost is paid once, up front, instead of per-access.

---

## 7. Cache Locality: Why Layout Matters

Memory moves in cache lines (typically 64 bytes). Reading a
C-contiguous array along axis 1 touches each cache line once,
sequentially. Reading along axis 0 jumps `row_stride` bytes each
step, dragging in only 8 bytes of every 64-byte line — 8× more
memory traffic for the same logical work.

```python
import time
big = np.random.default_rng(42).normal(size=(4000, 4000))

def timed(label, fn):
    t0 = time.perf_counter(); fn()
    print(f"{label:<28s} {time.perf_counter() - t0:.4f}s")

timed("row sum (contiguous)", lambda: big.sum(axis=1))
timed("col sum (strided)  ", lambda: big.sum(axis=0))
```

```
row sum (contiguous)   0.0155s
col sum (strided)      0.0076s
```

Note the honest surprise: modern NumPy optimizes axis-0 reductions
so well that the strided sum is *faster* here. The classic 10×
transpose story applies to kernels that do not special-case strided
access — C/Fortran libraries, old BLAS builds, and hand-written
loops. The lesson is not "strides are always bad"; it is **measure
your layout on your stack**. What is *always* true: `.T` itself is
O(1), and `ascontiguousarray` before a foreign kernel is cheap
insurance.

---

## 8. `nbytes`: Honest Memory Accounting

`nbytes` is `size * itemsize` — the logical footprint of *this*
array object. Views report their own logical size while sharing the
parent buffer, so two arrays can both claim memory that exists once.

```python
a = np.zeros((1000, 1000), dtype=np.float64)
b = a[:, 0]                # view
c = a[:, :2].copy()        # copy

print(a.nbytes)            # 8000000
print(b.nbytes)            # 8000      -- logical, not allocated
print(c.nbytes)            # 16000     -- owns its buffer
print(b.base is a)         # True
```

```
8000000
8000
16000
True
```

Budget memory with `sum(arr.nbytes for arr in held_arrays)` *only*
after eliminating views that share buffers — otherwise you double-
count. For a true picture, track the base buffers, not the views.

---

## 9. Production Pattern: The Contiguity Contract

A feature-service function that normalizes layout at the boundary:

```python
def require_c_contiguous(x: np.ndarray) -> np.ndarray:
    """Return a C-contiguous array; copy only when layout is wrong.

    Contract: callers may pass views (slices, transposes); the
    kernel below always receives a C-contiguous buffer.
    """
    return np.ascontiguousarray(x)

data = np.random.default_rng(0).normal(size=(500, 300))
print(require_c_contiguous(data) is data)          # True
print(require_c_contiguous(data.T) is not data.T)  # True
```

```
True
True
```

The same function serves two masters: zero-cost for well-behaved
callers, correct layout for everyone else. This is exactly how
SciPy, scikit-learn, and PyTorch wrappers behave at their C
boundaries.

---

## 10. Common Mistakes to Avoid

### Mistake 1: Believing `.T` is cheap to *use*
```
# WRONG — the view is free, but a strided consumer pays per access
y = x.T @ w            # fine; BLAS handles strided B via a copy
# BETTER — be explicit when the layout matters
y = x.T.copy() @ w     # pay once, upfront, deliberately
```

### Mistake 2: Testing aliasing with `is`
```
# WRONG — views are new objects
if a[1:] is a: ...     # never True
# CORRECT
if a[1:].base is a: ...   # True for a view
```

### Mistake 3: Assuming `reshape` never copies
```
# WRONG — can be a copy when the input is non-contiguous
flat = x.T.reshape(-1)     # copies
# CORRECT — check when it matters
assert flat.base is not x  # be explicit about the contract
```

### Mistake 4: Double-counting memory through views
```
# WRONG — counts the same buffer twice
total = a.nbytes + a[:, 0].nbytes   # 8 MB + 8 KB, one buffer
# CORRECT — count base buffers
total = a.nbytes                    # 8 MB, includes the column
```

### Mistake 5: Forgetting that `astype` is a full copy
```
# WRONG — "casting in place" does not exist
x = x.astype(np.float32)     # new buffer; old one waits for GC
# CORRECT — free the old reference immediately
y = x.astype(np.float32); del x
```

---

## 11. Best Practices

1. **Check `arr.base` to answer every view-vs-copy question** —
   never guess, never use `is`.
2. **Pass contiguous arrays to foreign kernels** via
   `np.ascontiguousarray`; the no-copy fast path is free.
3. **Do not fear `.T`** — creating it is O(1); be deliberate about
   *consuming* it.
4. **Use `np.shares_memory(a, b)`** when aliasing must be proven in
   tests — stronger than `base` checks.
5. **Budget memory by base buffers**, not by `nbytes` of views.
6. **Free big intermediates explicitly** (`del`, or `out=` reuse)
   before the next allocation in long pipelines.
7. **Choose the layout at creation** (`order='F'` when a Fortran
   kernel will follow) instead of fixing it later.
8. **Time layout choices on your machine** — modern NumPy blurs the
   naive cache story; measure, then decide.
9. **Assert contiguity contracts** (`x.flags.c_contiguous`) at
   function boundaries that hand data to compiled code.
10. **Document memory contracts in docstrings**: "views input;
    returns a copy" — this is the API your reviewers check.

---

## 12. Complexity and Cost

Memory is the dominant cost; time follows the data path.

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| slice `a[1:3]` | O(1) | O(1) view | — |
| transpose `a.T` | O(1) | O(1) view | — |
| fancy index `a[[0,2]]` | O(k) | O(k) copy | boolean mask when dense |
| `astype` | O(n) | O(n) copy | read into correct dtype at load |
| `reshape` (contiguous) | O(1) | O(1) view | — |
| `reshape` (strided) | O(n) | O(n) copy | `ascontiguousarray` first, then view |
| `ascontiguousarray` on C data | O(1) | O(1) | — |
| `ascontiguousarray` on `.T` | O(n) | O(n) | do the transpose-consuming math in F order |
| strided access (foreign kernel) | O(n) cache misses | — | contiguous copy first — O(n) once |

**Scale note:** a 10M × 768 float32 embedding matrix is ~30 GB.
A single stray `astype(float64)` doubles it; a `data.T` handed to a
naive kernel multiplies memory traffic ~8×. At this scale, layout
decisions are the budget.

---

## 13. AI Engineering Relevance

**Where this shows up:** embedding stores, feature pipelines, model
weight loading, and every boundary where NumPy hands buffers to
PyTorch/sklearn/C code.

| Concept here | Used for |
|---|---|
| strides + contiguity | knowing whether `embeddings.T` costs a copy before a matmul |
| view vs copy | avoiding accidental copies of 30 GB embedding matrices |
| `ascontiguousarray` | the standard handoff at Python→C/PyTorch boundaries |
| Fortran order | weights/feature matrices stored for column-major consumers |
| `nbytes` accounting | memory budgeting of caches, index buffers, and batches |

**Scale note:** at inference time the same view-vs-copy question
appears per request: batch slices of a shared embedding cache must
be views (zero-copy) or the service copies gigabytes per second.
`base` checks in tests catch regressions before they reach prod.

---

## 14. Practice Exercises

### Exercise 1: Stride Arithmetic (Difficulty: Easy)
For `np.zeros((5, 7), dtype=np.int32)`, compute the strides by hand
and verify with `arr.strides`. Repeat for `order='F'` and for
`np.zeros((2, 3, 4))` float64.

### Exercise 2: View or Copy? (Difficulty: Easy)
For each expression, predict view or copy, then verify with
`base`: `a[::2]`, `a[1]`, `a[:, [0, 2]]`, `a > 0`, `a[1:, 1:]`,
`np.flip(a, axis=0)`, `a.copy()`.

### Exercise 3: Reshape Detective (Difficulty: Medium)
Build a C-contiguous `(3, 4)` array. Which of these reshapes are
views and which copy? `a.reshape(4, 3)`, `a.reshape(12)`,
`a.T.reshape(12)`, `a.T.reshape(2, 6)`? Explain with strides.

### Exercise 4: Layout Contract (Difficulty: Medium)
Write `to_c_contiguous(x)` and a test that asserts: same object for
C input, new object for `x.T`, and `flags.c_contiguous` on output.
Check aliasing with `np.shares_memory` after the copy.

### Exercise 5: Memory Budget (Difficulty: Hard)
Given a `(1_000_000, 128)` float32 feature matrix, compute the
byte cost of: a column slice view, `astype(float64)`, `data.T`
(view), `np.ascontiguousarray(data.T)`, and a boolean-mask row
selection. Present a table and identify which pipeline steps
allocate and which do not.

---

## 15. Summary

| Concept | Description |
|---|---|
| strides | byte offsets per axis; the array's memory map |
| C vs F order | last-axis vs first-axis contiguous; swapped stride patterns |
| view vs copy | slices/`.T`/some reshapes view; fancy/`astype` copy |
| `base` | the reliable view-vs-copy test |
| `ascontiguousarray` | no-op on C data, copy otherwise |
| cache locality | strided access multiplies memory traffic; measure |
| `nbytes` | logical size; double-counts shared buffers if summed blindly |

The ndarray memory model is four numbers. Once strides click, views,
copies, and layout bugs stop being magic — they become arithmetic.
The professional habit is to *state the contract* (view or copy) at
every function boundary and verify it with `base` in tests.

---

## 16. Quick Reference

| Task | Idiom |
|---|---|
| Check layout | `arr.flags.c_contiguous` / `f_contiguous` |
| View or copy? | `arr.base is None` → owns buffer |
| Force C layout | `np.ascontiguousarray(arr)` |
| Force F layout | `np.asfortranarray(arr)` |
| Aliasing proof | `np.shares_memory(a, b)` |
| Byte footprint | `arr.nbytes`, `arr.itemsize` |
| Stride read | `arr.strides` |
| Zero-copy column | `arr[:, i]` (view) |
| Copy a column | `arr[:, i].copy()` |

---

## Next Steps

Next: **[32 — Dtypes and Precision](32-dtypes-and-precision-lecture.md)** —
itemsize from lecture 31 becomes the *decision*: float32 vs float64,
float16 serving, overflow wraparound, and `isclose`.
Continues in: **[Phase 3 — advanced indexing](34-advanced-indexing-lecture.md)**
for top-k retrieval, where view-vs-copy decides whether retrieval
copies your whole index.
Official docs: [ndarray.strides](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.strides.html),
[`np.ascontiguousarray`](https://numpy.org/doc/stable/reference/generated/numpy.ascontiguousarray.html),
[`np.shares_memory`](https://numpy.org/doc/stable/reference/generated/numpy.shares_memory.html).
