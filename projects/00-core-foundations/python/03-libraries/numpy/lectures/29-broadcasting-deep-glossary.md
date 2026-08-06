# Broadcasting Deep — Glossary 29

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `(n,)` vs `(n,1)` | Shape | A 1-D vector has no column-ness; `(n,1)` is an explicit column |
| `broadcast_shapes` | Function | Returns the result shape of two compatible shapes without allocating |
| `broadcast_to` | Function | Returns a read-only view of an array stretched to a target shape |
| Broadcasting | Concept | Rules for elementwise ops on arrays of different but compatible shapes |
| `expand_dims` | Function | Inserts a size-1 axis at a named position |
| Failure case | Concept | Trailing dims neither equal nor 1 raise `ValueError` |
| `keepdims` | Parameter | Reduction flag that preserves the reduced axis as size 1 |
| Leading dims | Concept | Dimensions before the rightmost; treated as 1 when missing |
| `newaxis` | Alias | `None` used in indexing to insert a size-1 axis |
| One-hot encoding | Pattern | `(labels[:, None] == arange(k))` builds the matrix in one pass |
| Outer product | Pattern | `a[:, None] * b[None, :]` — O(n·m) silent allocation |
| Reduction | Concept | Operation that removes an axis (`sum`, `mean`, `max`) |
| Shape alignment | Concept | Shapes are compared from the trailing dimension leftward |
| Size-1 stretch | Concept | A dimension of size 1 is replicated logically, not copied |
| `ValueError` | Error | Raised when shapes cannot broadcast |
| Z-score bug | Bug | Subtracting a row vector where a column vector was intended |

## Detailed Definitions

### `(n,)` vs `(n,1)`
**Definition**: A shape `(n,)` array is a rank-1 vector with no axis
orientation; `(n,1)` is a rank-2 column. `.T` is a no-op on `(n,)`, and a
`(n,)` vector broadcasts along rows, never columns.

**Example**:
```python
import numpy as np

v = np.arange(4)
print(v.shape, v.T.shape)              # (4,) (4,)
print(v[:, None].shape)                # (4, 1)
mat = np.ones((4, 3))
print((mat + v[:, None]).shape)        # (4, 3) -- column add
```

**Complexity**: O(1) — reshaping a view, no data movement.
**Related**: `newaxis`, `keepdims`, Shape alignment

---

### `broadcast_shapes`
**Definition**: Pure function that computes the result shape of a
broadcast without building the arrays — the fastest way to check
compatibility.

**Example**:
```python
import numpy as np

print(np.broadcast_shapes((3, 1), (1, 4)))   # (3, 4)
print(np.broadcast_shapes((5,), (3, 4)))     # ValueError? no -- raises
```

```text
(3, 4)
Traceback: ValueError: shape mismatch
```

**Complexity**: O(rank) — compares dimensions only.
**Related**: Broadcasting, Failure case

---

### `broadcast_to`
**Definition**: Returns a view of `arr` with the shape `shape`, applying
broadcast stretching. The view is read-only; any write raises.

**Example**:
```python
import numpy as np

a = np.arange(3)
stretched = np.broadcast_to(a[:, None], (3, 4))
print(stretched.shape)                     # (3, 4)
print(stretched.base is not None)          # True -- no copy
print(stretched.flags.writeable)           # False
```

**Complexity**: O(1) time and O(1) extra memory — a view.
**Related**: Size-1 stretch, Outer product, Silent allocation

---

### Broadcasting
**Definition**: NumPy's mechanism for elementwise operations on arrays of
different shapes: align trailing dims, require equal-or-1, stretch size-1
dims to match. The result has the elementwise maximum of each dimension.

**Example**:
```python
import numpy as np

a = np.ones((3, 1))
b = np.ones(4)
c = a + b
print(c.shape)                             # (3, 4)
```

**Complexity**: O(result size) time, O(result size) memory for the result.
**Related**: Shape alignment, Size-1 stretch, Failure case

---

### `expand_dims`
**Definition**: Function that inserts a size-1 axis at position `axis` —
the named form of `arr[:, None]` / `arr[None, :]` slicing.

**Example**:
```python
import numpy as np

v = np.arange(4)
print(np.expand_dims(v, 1).shape)          # (4, 1)
print(np.expand_dims(v, 0).shape)          # (1, 4)
print(v[:, None].shape)                    # (4, 1) -- equivalent
```

**Complexity**: O(1) — view.
**Related**: `newaxis`, `(n,)` vs `(n,1)`

---

### Failure case
**Definition**: Any pair of shapes whose trailing dimensions are neither
equal nor 1. NumPy raises `ValueError` with both operand shapes in the
message — read it from the rightmost dimension leftward.

**Example**:
```python
import numpy as np

try:
    np.ones((3, 2)) + np.ones((2, 3))
except ValueError as e:
    print(type(e).__name__)
    print(str(e)[:60])
```

```text
ValueError
operands could not be broadcast together with shapes (3,2) (2,3)
```

**Complexity**: — raises, no work done.
**Related**: `ValueError`, Shape alignment

---

### `keepdims`
**Definition**: Boolean parameter on reductions (`sum`, `mean`, `max`,
`norm` via `np.linalg`). When `True`, the reduced axis is kept as size 1,
so the result broadcasts cleanly against the original array.

**Example**:
```python
import numpy as np

X = np.random.default_rng(0).normal(size=(6, 3))
m = X.mean(axis=1, keepdims=True)
print(m.shape)                             # (6, 1)
print((X - m).shape)                       # (6, 3) -- row centered
```

**Complexity**: O(1) shape effect; reduction itself O(n).
**Related**: Reduction, `(n,)` vs `(n,1)`, Z-score bug

---

### Leading dims
**Definition**: Dimensions to the left of the trailing one. When an operand
has fewer dims, its leading dims are treated as size 1, which can then
stretch to match the other operand.

**Example**:
```python
import numpy as np

big = np.ones((2, 5, 3))
small = np.ones((5, 3))                    # treated as (1, 5, 3)
print((big + small).shape)                 # (2, 5, 3)
```

**Complexity**: O(1) — conceptual padding only.
**Related**: Shape alignment, Broadcasting

---

### `newaxis`
**Definition**: Alias for `None`. Used inside an index expression to insert
a size-1 axis at that exact position: `v[:, None]` → `(n,1)`,
`v[None, :]` → `(1,n)`.

**Example**:
```python
import numpy as np

v = np.arange(3)
print(v[np.newaxis, :].shape)              # (1, 3)
print(v[:, np.newaxis].shape)              # (3, 1)
```

**Complexity**: O(1) — view.
**Related**: `expand_dims`, `(n,)` vs `(n,1)`

---

### One-hot encoding
**Definition**: Pattern converting integer labels in `[0, k)` to an `(n, k)`
matrix where row `i` is all zeros except a 1 at `labels[i]`. Built with a
single broadcast comparison.

**Example**:
```python
import numpy as np

labels = np.array([0, 2, 1])
oh = (labels[:, None] == np.arange(3)).astype(np.float32)
print(oh.shape)                            # (3, 3)
print(oh.sum(axis=1))                      # [1. 1. 1.]
```

**Complexity**: O(n·k) time and memory.
**Related**: Broadcasting, `newaxis`

---

### Outer product
**Definition**: `a[:, None] * b[None, :]` produces the `(n, m)` matrix of
all pairwise products. Elegant — and a silent O(n·m) allocation.

**Example**:
```python
import numpy as np

a = np.arange(3)
b = np.arange(4)
outer = a[:, None] * b[None, :]
print(outer.shape)                         # (3, 4)
print(outer.nbytes, "bytes")               # 96 bytes for 3x4 float64
```

**Complexity**: O(n·m) time and O(n·m) memory — the memory is the cost.
**Related**: Silent allocation, `broadcast_to`

---

### Reduction
**Definition**: Operation that collapses one or more axes (`sum`, `mean`,
`max`, `argmin`). The reduced axis disappears from the shape unless
`keepdims=True`.

**Example**:
```python
import numpy as np

X = np.arange(12).reshape(3, 4)
print(X.sum(axis=0).shape)                 # (4,)
print(X.sum(axis=0, keepdims=True).shape)  # (1, 4)
```

**Complexity**: O(n) over the reduced elements.
**Related**: `keepdims`, Leading dims

---

### Shape alignment
**Definition**: The act of comparing two shapes from the rightmost
dimension leftward. This order is why `(4,)` pairs with the *last* axis of
`(3, 4)`, not the first.

**Example**:
```python
import numpy as np

# (4,) aligns with the trailing axis of (3, 4)
print(np.broadcast_shapes((3, 4), (4,)))   # (3, 4)
# (3,) clashes with the trailing 4
try:
    np.broadcast_shapes((3, 4), (3,))
except ValueError:
    print("mismatch")
```

```text
(3, 4)
mismatch
```

**Complexity**: O(rank).
**Related**: Broadcasting, Failure case

---

### Size-1 stretch
**Definition**: A dimension of size 1 is conceptually replicated to match
its partner. No copy is made for the operand — the ufunc reads it
repeatedly; only the result materializes.

**Example**:
```python
import numpy as np

a = np.array([[1.0], [2.0]])               # (2, 1)
b = np.array([[10.0, 20.0]])               # (1, 2)
print(a + b)
# [[11. 21.]
#  [12. 22.]]
```

**Complexity**: O(result) time; the stretch itself is O(1).
**Related**: Broadcasting, `broadcast_to`, Silent allocation

---

### Silent allocation
**Definition**: A broadcast expression whose *result* has the full stretched
shape. The operands are cheap; the result can explode — an outer product of
two 100k-length vectors is 80 GB of float64.

**Example**:
```python
import numpy as np

a = np.arange(100_000)
outer = a[:, None] * a[None, :]            # 100_000 x 100_000
print(outer.nbytes / 1e9, "GB")            # 80.0 GB
```

**Complexity**: O(n·m) memory — check before running.
**Related**: Outer product, `broadcast_to`

---

### `ValueError`
**Definition**: The exception NumPy raises for incompatible shapes. The
message names both shapes; the fix is usually an explicit `[:, None]` or
`keepdims=True` on the reduction that produced the wrong rank.

**Example**:
```python
import numpy as np

try:
    np.ones((2, 3)) + np.ones((2, 4))
except ValueError as e:
    print("raise as expected")
```

```text
raise as expected
```

**Complexity**: —.
**Related**: Failure case, Shape alignment

---

### Z-score bug
**Definition**: Subtracting a row-wise mean/vector where a column-wise one
was intended. Either raises `ValueError` or — worse — broadcasts silently
and produces wrong values that pass shape checks.

**Example**:
```python
import numpy as np

X = np.random.default_rng(1).normal(size=(100, 3))
# WRONG intent: row centering via column broadcast
wrong = X - X.mean(axis=0)      # runs, but rows not centered
row_centered = X - X.mean(axis=1, keepdims=True)
print(np.abs(row_centered.mean(axis=1)).max())   # ~0
print(np.abs(wrong.mean(axis=1)).max())          # not ~0
```

**Complexity**: O(n) per pass; the bug costs debugging hours.
**Related**: `keepdims`, `(n,)` vs `(n,1)`

## Key Concepts Summary

### The rules
- Align from the trailing dimension; equal or 1 is compatible; 1s stretch.
- Missing leading dims are treated as 1.
- Incompatible trailing dims raise `ValueError`.

### The tools
- `None` / `np.newaxis` inserts size-1 axes; `expand_dims` is the named form.
- `keepdims=True` keeps reduced axes so results broadcast back cleanly.
- `broadcast_to` gives a free read-only stretched view.

### The traps
- `(n,)` has no column-ness — `.T` is a no-op.
- Outer products silently allocate O(n·m).
- Reductions that lose an axis turn column math into row math.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `broadcast_to` — ___
2. `keepdims` — ___
3. `(n,1)` — ___
4. Outer product — ___
5. Z-score bug — ___
6. `newaxis` — ___

**Answers:**
1. e, 2. d, 3. f, 4. a, 5. b, 6. c

a. `a[:, None] * b[None, :]` — full n-by-m matrix, silent allocation
b. Row mean subtracted where column mean was intended
c. `None` inside indexing, inserts a size-1 axis
d. Reduction flag that preserves the reduced axis as size 1
e. Read-only view of an array stretched to a target shape
f. An explicit column vector of length n, rank 2

---

**Related docs:** [NumPy broadcasting basics](https://numpy.org/doc/stable/user/basics.broadcasting.html) ·
[`np.broadcast_to`](https://numpy.org/doc/stable/reference/generated/numpy.broadcast_to.html) ·
[`np.expand_dims`](https://numpy.org/doc/stable/reference/generated/numpy.expand_dims.html) ·
[Back to lecture](29-broadcasting-deep-lecture.md)
