# NumPy Lecture 29: Broadcasting, Deep

## Topic Overview

Broadcasting is NumPy's rule for combining arrays of *different* shapes. A
`(3, 4)` matrix plus a `(4,)` vector works in one expression; a `(3, 2)` matrix
plus a `(2, 3)` matrix raises `ValueError`. The rules that decide between those
two outcomes are precise, short, and â€” once internalized â€” explain most shape
bugs in real pipelines.

Lecture 21 introduced broadcasting as "NumPy stretches the smaller array."
This lecture goes deeper: the three formal rules, how `newaxis` inserts axes
on demand, when broadcasting *silently allocates* memory, the classic
`(n,)` vs `(n, 1)` confusion, and the exact failure mode when shapes cannot
broadcast. The payoff is the AI hook: batch inference is one broadcast
expression, and row normalization is one `keepdims=True` away from a silent
bug.

## Learning Objectives

By the end of this lecture, you will be able to:

1. State the three broadcasting rules and apply them to predict a result shape
2. Use `np.newaxis` (and `None`) to insert size-1 axes at any position
3. Distinguish a `(n,)` vector from a `(n, 1)` column and fix bugs with
   `reshape`, `[:, None]`, and `keepdims=True`
4. Explain when broadcasting allocates a full result array (outer products)
   and when `np.broadcast_to` provides a free, read-only view
5. Predict exactly which shape pairs raise `ValueError`, and read the error
   message to fix the code
6. Apply broadcasting to batch inference (bias add, softmax, normalization)
   and one-hot encoding in a single vectorized pass

## Prerequisites

| Need | Where |
|---|---|
| Basic array creation and `shape` | `08-array-shape-lecture.md` |
| `reshape`, `ravel`, `squeeze` | `09-array-reshape-lecture.md` |
| Views vs copies and `base` | `07-copy-vs-view-lecture.md` |
| Ufunc elementwise arithmetic | `21-ufunc-arithmetic-lecture.md` |
| `np.where` and boolean masks | `15-array-filter-lecture.md` |

---

## 1. The Three Rules

Broadcasting compares shapes **from the trailing (rightmost) dimension
leftward**. Two dimensions are *compatible* if they are equal or one of them
is 1. A dimension of size 1 is stretched to match its partner; missing leading
dimensions are treated as size 1.

```python
import numpy as np

# Rule 1: trailing alignment. (4,) pairs with the last axis of (3, 4).
x = np.ones((3, 4))
v = np.ones(4)
print((x + v).shape)          # (3, 4)

# Rule 2: dims equal OR one is 1.
a = np.ones((3, 1))
b = np.ones((1, 4))
print((a + b).shape)          # (3, 4)  -- both 1s stretch

# Rule 3: missing leading dims are treated as 1.
big = np.ones((2, 5, 3))
small = np.ones((5, 3))
print((big + small).shape)    # (2, 5, 3)
```

```
(3, 4)
(3, 4)
(2, 5, 3)
```

Read the third example carefully: `(5, 3)` becomes `(1, 5, 3)`, then the
leading 1 stretches to 2. Every step is mechanical: align, compare, stretch.

---

## 2. Size-1 Dimensions Stretch, They Do Not Copy

When NumPy says a dimension "stretches," it does not mean a copy is made.
The ufunc loops over the *logical* result shape and reads the size-1 operand
repeatedly. That is why `x + v` on a 1GB `x` costs one new 1GB array, not two.

```python
a = np.arange(3).reshape(3, 1)   # (3, 1)
b = np.arange(4)                 # (4,)  -> (1, 4)
c = a + b                        # logical shape (3, 4)
print(c)
# [[0 1 2 3]
#  [1 2 3 4]
#  [2 3 4 5]]

# Proof of stretching: c[i, j] == a[i, 0] + b[j]
print(c[2, 3] == a[2, 0] + b[3])  # True
```

```
[[0 1 2 3]
 [1 2 3 4]
 [2 3 4 5]]
True
```

This "stretch by reference" is exactly why broadcasting is cheap to *express*:
the cost is in the result array, not in the operands.

---

## 3. `newaxis`: Inserting Axes by Hand

`np.newaxis` is an alias for `None`. Written inside an index expression, it
inserts a size-1 axis at that position. `v[:, None]` turns `(4,)` into `(4, 1)`;
`v[None, :]` turns it into `(1, 4)`.

```python
v = np.arange(4)
print(v.shape)         # (4,)
print(v[:, None].shape)  # (4, 1)
print(v[None, :].shape)  # (1, 4)

# Add v as a ROW to a (3, 4) matrix: both spellings are identical.
mat = np.ones((3, 4))
row_add = mat + v
row_add2 = mat + v[None, :]
print(np.array_equal(row_add, row_add2))   # True

# Add v as a COLUMN to a (4, 3) matrix.
mat2 = np.ones((4, 3))
col_add = mat2 + v[:, None]
print(col_add.shape)     # (4, 3)
```

```
(4,)
(4, 1)
(1, 4)
True
(4, 3)
```

The symmetry is the point: the *same* data, one `None` on either side of the
colon, adds along a different axis. Getting this wrong is the `(n,)` vs
`(n, 1)` bug from the exercise â€” usually silent, sometimes fatal.

---

## 4. When Broadcasting Silently Allocates

Broadcasting itself does not allocate stretched copies. But the **result** of
any operation has the logical broadcast shape, and that result is materialized.
The classic trap is the outer product:

```python
a = np.arange(5)
b = np.arange(4)

outer = a[:, None] * b[None, :]        # (5, 4) -- full materialized array
print(outer.shape)                     # (5, 4)
print(outer.nbytes, "bytes")           # 160 bytes = 5*4*8
print(a.nbytes + b.nbytes, "bytes of input")   # 72 bytes total input
```

```
(5, 4)
160 bytes
72 bytes of input
```

A 10,000-element vocabulary outer product is 800MB of float64 before you
blink. When you only need the *view*, `np.broadcast_to` gives it to you for
free â€” but read-only:

```python
lazy = np.broadcast_to(a[:, None], (5, 4))
print(lazy.base is not None)        # True -- no copy
print(lazy.flags.writeable)         # False -- read-only
```

```
True
False
```

**Rule of thumb:** if your broadcast expression's output shape is
`n * m` and you never needed `n * m` values, reach for `broadcast_to`
or restructure the math (see the einsum lecture, `30-vectorization.py`).

---

## 5. `(n,)` vs `(n, 1)`: The Bug That Ships

A 1-D array has no column-ness. Three facts follow:

```python
v = np.array([1.0, 2.0, 3.0])

# Fact 1: .T is a no-op on 1-D data.
print(v.T.shape)                     # (3,)

# Fact 2: mean(axis=1) on 1-D data fails.
try:
    v.mean(axis=1)
except ValueError as e:
    print("mean(axis=1) on 1-D:", type(e).__name__)

# Fact 3: subtracting a row vector where a column was meant
# either raises (lucky) or broadcasts wrongly (unlucky).
data = np.random.default_rng(42).normal(size=(100, 3))
row_means = data.mean(axis=1)        # (100,)
try:
    data - row_means                  # (100,3) vs (100,)
except ValueError as e:
    print("wrong:", str(e)[:50], "...")
correct = data - data.mean(axis=0)    # (3,) -> fine, it IS a row op
```

```
(3,)
mean(axis=1) on 1-D: ValueError
wrong: operands could not be broadcast together with shapes (100,3) ...
```

The unlucky variant: `data - data.mean(axis=0)` when you meant the *row*
means. It never raises â€” the shapes *do* broadcast â€” but every row gets the
same column correction. Always verify `result.shape == (B, D)`.

---

## 6. Failure Cases: Reading the ValueError

When a trailing dimension is neither equal nor 1, NumPy raises:

```python
np.ones((3, 2)) + np.ones((2, 3))
```

```
ValueError: operands could not be broadcast together with shapes (3,2) (2,3)
```

```python
np.ones((3, 2)) + np.ones((2, 4))
```

```
ValueError: operands could not be broadcast together with shapes (3,2) (2,4)
```

The message lists both shapes in the order you wrote them. The fix procedure:

1. Read the last dimensions first: `(3,2)` vs `(2,3)` â†’ `2` vs `3` clash.
2. Decide which side is meant to be a column or row vector.
3. Insert `None` (`x[:, None]`) or call `np.reshape` / `np.expand_dims`.
4. Re-run and print the result shape before trusting the math.

---

## 7. Broadcasting with Reductions: `keepdims`

Reductions remove the axis they reduce. That is exactly when shapes stop
matching: `X.mean(axis=0)` gives `(D,)`, and `X - X.mean(axis=0)` works for
*column* centering only by luck of trailing alignment.

```python
X = np.random.default_rng(0).normal(size=(6, 3))

# Column center: (6,3) - (3,) -- trailing dims align. OK.
col_centered = X - X.mean(axis=0)

# Row center: (6,3) - (6,) -- trailing 3 vs 6 clash. Raises.
try:
    X - X.mean(axis=1)
except ValueError as e:
    print("row center raises:", str(e)[:45], "...")

# keepdims=True keeps (6, 1), which broadcasts along columns.
row_centered = X - X.mean(axis=1, keepdims=True)
print(row_centered.shape)                          # (6, 3)
print(np.allclose(row_centered.mean(axis=1), 0))   # True
```

```
row center raises: operands could not be broadcast together ...
(6, 3)
True
```

`keepdims=True` is the production fix: it makes the reduced array keep the
axis it reduced, so the broadcast direction is explicit and self-documenting.

---

## 8. Broadcasting in Batch Inference

Batch inference is one broadcast expression after another. Given a `(B, D)`
batch of embeddings:

```python
rng = np.random.default_rng(42)
batch = rng.normal(size=(8, 5))     # 8 embeddings, dim 5
bias = rng.normal(size=5)           # per-dim bias

# 1. Add a bias vector: (8,5) + (5,) -> (8,5).
logits = batch + bias

# 2. Softmax along rows: keepdims keeps (8,1) to divide by.
logits -= logits.max(axis=1, keepdims=True)      # numerical stability
exp = np.exp(logits)
probs = exp / exp.sum(axis=1, keepdims=True)
print(probs.shape, probs.sum(axis=1))            # (8, 5) rows sum to 1

# 3. L2-normalize embeddings: (8,5) / (8,1) -> (8,5).
norms = np.linalg.norm(batch, axis=1, keepdims=True)
normed = batch / norms
print(np.allclose(np.linalg.norm(normed, axis=1), 1.0))   # True
```

```
(8, 5) [1. 1. 1. 1. 1. 1. 1. 1.]
True
```

Every step is O(B*D) work with no Python loop â€” the same expression serves
one query or 10,000 in a batch, which is what makes GPU/vectorized serving
fast.

---

## 9. One-Hot Encoding in One Broadcast

Integer labels â†’ one-hot matrix is a single comparison that broadcasts:

```python
labels = np.array([0, 2, 1, 2, 0])
k = 3
one_hot = (labels[:, None] == np.arange(k)[None, :]).astype(np.float32)
print(one_hot.shape)
print(one_hot)
```

```
(5, 3)
[[1. 0. 0.]
 [0. 0. 1.]
 [0. 1. 0.]
 [0. 0. 1.]
 [1. 0. 0.]]
```

`labels[:, None]` is `(5, 1)`; `arange(k)[None, :]` is `(1, 3)`. The
comparison broadcasts to `(5, 3)` in one pass. This is the pattern inside
every `to_categorical` / `OneHotEncoder` implementation.

---

## Common Mistakes to Avoid

### Mistake 1: Relying on `.T` to fix 1-D data
```
# WRONG â€” .T is a no-op on 1-D arrays
centered = data - data.mean(axis=1).T      # still (100,)
# CORRECT â€” insert the axis explicitly
centered = data - data.mean(axis=1)[:, None]
```

### Mistake 2: `(3,)` where `(3, 1)` was needed
```
# WRONG â€” trailing dims (3,) vs (3,4) clash or align wrongly
col = np.array([1, 2, 3])
try:
    np.ones((3, 4)) + col          # ValueError
except ValueError:
    pass
# CORRECT
col = np.array([1, 2, 3])[:, None] # (3, 1)
np.ones((3, 4)) + col
```

### Mistake 3: Forgetting the result is materialized
```
# WRONG â€” silently builds an n*m array you never needed
dist = a[:, None] * b[None, :]     # O(n*m) memory
# CORRECT â€” view when possible, or restructure with einsum
lazy = np.broadcast_to(a[:, None], (n, m))     # read-only view
```

### Mistake 4: Trusting "it ran, so it's right"
```
# WRONG â€” runs fine, does the wrong thing (column means on rows)
bad = data - data.mean(axis=0)     # meant row centering
# CORRECT
good = data - data.mean(axis=1, keepdims=True)
# Always assert the output shape after any broadcast expression.
```

### Mistake 5: Using `expand_dims` when slicing syntax is clearer
```
# Acceptable but noisier
col = np.expand_dims(v, axis=1)
# Clearer â€” the axis position is visible at the call site
col = v[:, None]
```

---

## Best Practices

1. **Predict shapes before running:** say the three rules out loud for any
   expression mixing ranks; verify with `.shape` immediately.
2. **Use `keepdims=True` on every reduction that feeds another broadcast.**
3. **Prefer `v[:, None]` / `v[None, :]` over `expand_dims`** â€” the axis
   placement is visible where you write the math.
4. **Treat `broadcast_to` as the default when you only need a stretched
   view**, and remember it is read-only.
5. **Never rely on `.T` for 1-D data**; reshape explicitly.
6. **Check for silent outer products** when two 1-D arrays meet with
   `[:, None]` and `[None, :]` â€” confirm you actually want `n*m` values.
7. **Read ValueError messages from the trailing dimension leftward.**
8. **Assert output shapes in `_verify()`** blocks; a broadcast bug is
   invisible to `np.allclose` when it does not raise.
9. **Keep broadcast ops in one expression** (chain `+`, `-`, `/` with
   keepdims) so intermediates are never accidentally 1-D.
10. **Document the intended shape in the docstring** of functions that
    broadcast (`(B, D)` in, `(B, K)` out) â€” shape contracts beat luck.

---

## Complexity and Cost

Memory is the dominant cost of broadcasting, not time.

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| `x + v` with `x` (B,D), `v` (D,) | O(BÂ·D) | O(BÂ·D) result | in-place `x += v` â€” O(1) extra |
| `a[:, None] * b[None, :]` outer | O(nÂ·m) | O(nÂ·m) â€” **silent blowup** | `broadcast_to` view â€” O(1); or einsum into a reduction |
| `np.broadcast_to(v, (B, D))` | O(1) | O(1) view, read-only | â€” |
| `data - mean(axis=1, keepdims=True)` | O(BÂ·D) | O(BÂ·D) result | â€” |
| one-hot `(labels[:, None] == arange(k))` | O(nÂ·k) | O(nÂ·k) | sparse one-hot â€” O(n) nnz |

**Scale note:** a `(1M, 768)` embedding matrix plus a `(768,)` bias is a
6 GB result per pass at float64 â€” the broadcast is free, the allocation is
not. At 1M rows, prefer float32 and in-place ufuncs (`np.add(batch, bias,
out=batch)`).

---

## AI Engineering Relevance

**Where this shows up:** every layer of an embedding service â€” tokenizer
padding, batch bias adds, softmax temperature scaling, L2-normalization
before a vector-store insert, and one-hot label conversion in training
pipelines.

| Concept here | Used for |
|---|---|
| `(B, D) + (D,)` | adding per-dim bias/scale to a batch (batch inference) |
| `keepdims=True` reductions | softmax denominators, z-scoring, normalization |
| `labels[:, None] == arange(k)` | one-hot encoding, cross-entropy target matrices |
| `broadcast_to` | attention masks, tile-free position encoding |
| `(n,)` vs `(n,1)` discipline | embedding similarity: `X @ q` needs matching shapes |

**Scale note:** at 200 req/s with batch size 32 and dim 768, broadcasting
removes ~32Ã—768 Python-level operations per request. The alternative â€”
per-vector loops in Python â€” costs 10â€“100Ã— wall time before the first
matmul even runs.

---

## Practice Exercises

### Exercise 1: Predict the Shape (Difficulty: Easy)
For each pair, state whether it broadcasts and the result shape. Then
confirm with NumPy: `(3,1)+(1,4)`, `(2,3,1)+(4,)`, `(5,)+(5,1)`,
`(2,3)+(3,2)`, `(6,1)+(1,6,1)`.

### Exercise 2: Column Center a Matrix (Difficulty: Easy)
Write `center_columns(X: np.ndarray) -> np.ndarray` that subtracts the
column mean from each column using `keepdims=True`. Verify each output
column has mean â‰ˆ 0. Input `(100, 4)` â†’ output `(100, 4)`.

### Exercise 3: Row Normalize Without keepdims (Difficulty: Medium)
Reimplement `row_normalize` from the exercise **without** `keepdims`,
using `[:, None]` explicitly. Verify it matches the `keepdims` version
exactly with `np.allclose`.

### Exercise 4: One-Hot in Pure Broadcasting (Difficulty: Medium)
Build `one_hot(labels, k)` with `==` broadcasting as in Section 9. Test
with `labels = [0, 3, 1, 3, 0]`, `k = 4`, and assert row sums are all 1.

### Exercise 5: Budget the Outer Product (Difficulty: Hard)
For `a, b` of length `n = 200_000` each, compute the byte cost of
`a[:, None] * b[None, :]`. Then compute the same reduction
(`a @ b` for the sum) and show the memory difference. No timing â€” just
`nbytes` math and `np.broadcast_to` reasoning.

---

## Summary

| Concept | Description |
|---|---|
| Three rules | align trailing dims; equal-or-1 compatible; 1s stretch |
| `newaxis` / `None` | inserts size-1 axis at any position |
| Silent allocation | result of a broadcast has the full logical shape |
| `(n,)` vs `(n,1)` | `(n,)` has no column-ness; `.T` is a no-op on 1-D |
| `keepdims=True` | reductions keep the reduced axis for safe broadcasting |
| `ValueError` | raised when a trailing dim is neither equal nor 1 |
| `broadcast_to` | free read-only view of a stretched array |

Broadcasting is the difference between "shape bug in production at 3am" and
"one expression that just works." The rules are three lines; the discipline
is checking result shapes and using `keepdims` / `newaxis` so the intent is
visible in the code. Master this and batch inference math reads like prose.

---

## Quick Reference

| Task | Idiom |
|---|---|
| Add a row vector | `mat + v` or `mat + v[None, :]` |
| Add a column vector | `mat + v[:, None]` |
| Center columns | `X - X.mean(axis=0)` |
| Center rows | `X - X.mean(axis=1, keepdims=True)` |
| L2-normalize rows | `X / np.linalg.norm(X, axis=1, keepdims=True)` |
| Outer product | `a[:, None] * b[None, :]` |
| Stretch without copy | `np.broadcast_to(v, shape)` (read-only) |
| One-hot labels | `(labels[:, None] == np.arange(k))` |
| Check compatibility | `np.broadcast_shapes(s1, s2)` |

---

## Next Steps

Next: **[30 â€” Vectorization](30-vectorization-lecture.md)** â€” turning the
loops you just avoided into measured, vectorized equivalents, including
`np.where`, masking, and `einsum`.
Continues in: **[Phase 3 â€” NumPy linear algebra](33-linear-algebra-lecture.md)**
for `@`, `solve`, and cosine similarity as matmul.
Official docs: [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html),
[`np.broadcast_to`](https://numpy.org/doc/stable/reference/generated/numpy.broadcast_to.html),
[`np.broadcast_shapes`](https://numpy.org/doc/stable/reference/generated/numpy.broadcast_shapes.html).
