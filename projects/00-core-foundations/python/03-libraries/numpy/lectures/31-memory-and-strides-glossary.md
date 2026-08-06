# Memory and Strides — Glossary 31

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `ascontiguousarray` | Function | Returns C-contiguous data, copying only when layout is wrong |
| `asfortranarray` | Function | Forces F (column-major) layout, copying when needed |
| `astype` | Function | Casts dtype — always a new buffer |
| `base` | Attribute | The array owning the buffer; `None` means self-owned |
| Buffer | Concept | The raw memory block an ndarray points into |
| C contiguous | Layout | Row-major: last axis has stride = itemsize |
| Cache line | Concept | ~64-byte block of memory moved per miss |
| Cache locality | Concept | Sequential access pattern that maximizes cache hits |
| `copy()` | Method | Explicit full copy of the buffer |
| F contiguous | Layout | Column-major: first axis has stride = itemsize |
| Fancy indexing | Pattern | Integer-array indexing — always copies |
| Itemsize | Attribute | Bytes per element (`float64` = 8) |
| `nbytes` | Attribute | Logical bytes: size × itemsize |
| `reshape` | Method | New shape; view if layout allows, copy otherwise |
| `shares_memory` | Function | Proof that two arrays alias one buffer |
| Strides | Attribute | Byte offsets to step per axis |
| View | Concept | New array header over an existing buffer |

## Detailed Definitions

### `ascontiguousarray`
**Definition**: Returns the input itself when it is already
C-contiguous; otherwise returns a **copy** with C layout. The
standard handoff idiom at Python→compiled-kernel boundaries.

**Example**:
```python
import numpy as np

a = np.arange(12).reshape(3, 4)
t = a.T
print(np.ascontiguousarray(a) is a)    # True -- no copy
print(np.ascontiguousarray(t) is not t)  # True -- copy
print(np.ascontiguousarray(t).strides) # (32, 8)
```

**Complexity**: O(1) when contiguous, O(n) copy otherwise.
**Related**: C contiguous, `asfortranarray`, View

---

### `asfortranarray`
**Definition**: Forces Fortran (column-major) layout — the mirrored
version of `ascontiguousarray`, used when a Fortran/BLAS consumer
walks columns first.

**Example**:
```python
import numpy as np

c = np.zeros((3, 4))
f = np.asfortranarray(c)
print(f.strides)                  # (8, 24)
print(f.flags.f_contiguous)       # True
```

**Complexity**: O(1) or O(n) copy, same rule as its mirror.
**Related**: F contiguous, `ascontiguousarray`

---

### `astype`
**Definition**: Returns a new array with a new dtype. Because
itemsize changes, the byte map cannot be shared — `astype` always
copies.

**Example**:
```python
import numpy as np

x = np.arange(4, dtype=np.float64)
y = x.astype(np.float32)
print(y.base is None)             # True -- new buffer
print(y.itemsize)                 # 4
```

**Complexity**: O(n) copy.
**Related**: Itemsize, `copy()`

---

### `base`
**Definition**: Attribute holding the array that owns the data
buffer; `None` for self-owned arrays. The reliable view-vs-copy
test: `arr.base is not None` means a view.

**Example**:
```python
import numpy as np

a = np.arange(10)
print(a.base)                     # None
print(a[2:5].base is a)           # True
print(a[[0, 1]].base is None)     # True -- fancy indexing copied
```

**Complexity**: O(1).
**Related**: View, `shares_memory`

---

### Buffer
**Definition**: The raw contiguous memory block an ndarray header
points to. Views share it; copies own their own.

**Example**:
```python
import numpy as np

a = np.arange(6)
b = a[::2]                        # view into a's buffer
b[0] = 99
print(a)                          # [99  1 99  3 99  5]
```

**Complexity**: —.
**Related**: View, `base`

---

### C contiguous
**Definition**: Row-major layout — the last axis is contiguous
(stride = itemsize); each earlier axis's stride is the product of
the inner sizes. The NumPy default.

**Example**:
```python
import numpy as np

x = np.zeros((4, 6), dtype=np.float64)
print(x.strides)                  # (48, 8)
print(x.flags.c_contiguous)       # True
```

**Complexity**: —.
**Related**: F contiguous, Strides

---

### Cache line
**Definition**: The unit of memory transfer between RAM and CPU
caches (typically 64 bytes). Reading 8 bytes of a line wastes the
other 56 if you never use them.

**Example**:
```python
import numpy as np

# 8-byte float64 reads drag in 64-byte lines: 8 elements per line
x = np.zeros(1000, dtype=np.float64)
print(x.strides)                  # (8,)
```

**Complexity**: —.
**Related**: Cache locality, Strides

---

### Cache locality
**Definition**: The degree to which memory accesses are sequential.
Contiguous axis access hits fully-used cache lines; strided access
multiplies memory traffic — the physical reason layout matters.

**Example**:
```python
import numpy as np

big = np.random.default_rng(0).normal(size=(4000, 4000))
row_sum = big.sum(axis=1)     # sequential per row
col_sum = big.sum(axis=0)     # strided per column -- measure locally
```

**Complexity**: sequential ≈ O(n) line fills; strided up to 8×
traffic for float64.
**Related**: Cache line, C contiguous, Strides

---

### `copy()`
**Definition**: Explicit method returning a full copy of the buffer
with the same shape/dtype — the deliberate escape hatch from view
aliasing.

**Example**:
```python
import numpy as np

a = np.arange(4)
c = a.copy()
c[0] = 99
print(a)                          # [0 1 2 3] -- unaffected
print(c)                          # [99  1  2  3]
```

**Complexity**: O(n).
**Related**: View, `astype`

---

### F contiguous
**Definition**: Column-major layout — the first axis is contiguous.
Swapped stride pattern versus C; produced by `order='F'` creation,
`np.asfortranarray`, and `.T` of C data.

**Example**:
```python
import numpy as np

f = np.zeros((3, 4), dtype=np.float32, order="F")
print(f.strides)                  # (4, 12)
```

**Complexity**: —.
**Related**: C contiguous, `asfortranarray`

---

### Fancy indexing
**Definition**: Indexing with integer arrays/lists. Cannot be
expressed as slice+stride, so it **always copies**.

**Example**:
```python
import numpy as np

a = np.arange(10)
print(a[[0, 4, 9]].base is None)  # True -- copy
```

**Complexity**: O(k) for k selected elements.
**Related**: View, `base`

---

### Itemsize
**Definition**: Bytes per element of the dtype (`float64`=8,
`float32`=4, `float16`=2, `int8`=1). Fixes the last-axis stride of
contiguous arrays and the `nbytes` arithmetic.

**Example**:
```python
import numpy as np

for dt in (np.float64, np.float32, np.float16):
    print(dt.__name__, np.zeros(1, dtype=dt).itemsize)
# float64 8
# float32 4
# float16 2
```

**Complexity**: —.
**Related**: `nbytes`, Strides

---

### `nbytes`
**Definition**: `size × itemsize` — the logical footprint of the
array object. Views report their own logical size while sharing a
buffer; summing `nbytes` across views double-counts.

**Example**:
```python
import numpy as np

a = np.zeros((1000, 1000), dtype=np.float64)
b = a[:, 0]                       # view
print(a.nbytes)                   # 8000000
print(b.nbytes)                   # 8000 -- shares a's buffer
```

**Complexity**: O(1).
**Related**: Itemsize, Buffer, View

---

### `reshape`
**Definition**: Returns a new view when the target shape is
compatible with the current memory order; otherwise copies. Test
with `base` — never assume.

**Example**:
```python
import numpy as np

a = np.arange(12).reshape(3, 4)
print(a.reshape(4, 3).base is a)      # True -- view
print(a.T.reshape(12).base is a)      # False -- copy
```

**Complexity**: O(1) view or O(n) copy.
**Related**: View, C contiguous

---

### `shares_memory`
**Definition**: Function proving whether two arrays alias any part
of one buffer — stronger and more convenient than `base` chains in
tests.

**Example**:
```python
import numpy as np

a = np.arange(12).reshape(3, 4)
print(np.shares_memory(a, a[1:, :]))   # True
print(np.shares_memory(a, a.copy()))   # False
```

**Complexity**: O(1) bounds check (no element scan by default).
**Related**: `base`, View

---

### Strides
**Definition**: Tuple of byte offsets — `strides[k]` is the jump
along axis k. Element `(i0, i1)` of a 2-D array lives at
`i0*strides[0] + i1*strides[1]` bytes into the buffer.

**Example**:
```python
import numpy as np

x = np.zeros((4, 6), dtype=np.float64)
print(x.strides)                  # (48, 8)
y = x.T
print(y.strides)                  # (8, 48) -- swapped
```

**Complexity**: —.
**Related**: C contiguous, F contiguous, Cache locality

---

### View
**Definition**: A new ndarray header (shape/strides/dtype) pointing
into an existing buffer. Slices, `.T`, and some reshapes are views:
O(1) creation, shared writes.

**Example**:
```python
import numpy as np

a = np.arange(6)
v = a[1:5:2]
print(v)                          # [1 3]
v[0] = -1
print(a)                          # [ 0 -1  2  3  4  5]
```

**Complexity**: O(1).
**Related**: Buffer, `base`, Fancy indexing

## Key Concepts Summary

### The memory model
- ndarray = buffer + shape + dtype + strides.
- Strides map axes to byte offsets; contiguity is a stride pattern.

### The view/copy split
- Views: slices, `.T`, contiguous reshapes.
- Copies: fancy indexing, boolean masks, `astype`, `.copy()`.
- Test: `arr.base is None`.

### The layout discipline
- C order is the default; F order serves column-major consumers.
- `ascontiguousarray` repairs layout at boundaries, O(1) when fine.
- Cache locality makes layout a performance decision; measure.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Strides — ___
2. `base` — ___
3. Fancy indexing — ___
4. `ascontiguousarray` — ___
5. Cache line — ___
6. `nbytes` — ___

**Answers:**
1. d, 2. f, 3. a, 4. c, 5. e, 6. b

a. Integer-array indexing that always copies
b. Logical bytes of the array: size × itemsize
c. Layout repair: no-op on C data, copy otherwise
d. Byte offsets to step per axis
e. ~64-byte unit of memory transfer
f. The array owning the buffer; `None` when self-owned

---

**Related docs:** [ndarray.strides](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.strides.html) ·
[`np.ascontiguousarray`](https://numpy.org/doc/stable/reference/generated/numpy.ascontiguousarray.html) ·
[`np.shares_memory`](https://numpy.org/doc/stable/reference/generated/numpy.shares_memory.html) ·
[Back to lecture](31-memory-and-strides-lecture.md)
