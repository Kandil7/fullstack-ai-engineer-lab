# Advanced Indexing — Glossary 34

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `argpartition` | Function | Indices of a partial sort: O(n) top-k |
| `argsort` | Function | Indices of a full sort: O(n log n) |
| Boolean mask | Pattern | Same-shape True/False array selecting positions |
| `digitize` | Function | Bucket indices for values against bin edges |
| Fancy indexing | Pattern | Integer-array indexing: select, reorder, duplicate — always a copy |
| `ix_` | Function | Grid selector: rows × cols submatrix |
| Masked assignment | Pattern | Writing through a boolean mask: `x[mask] = v` |
| `put` | Function | Scatter write into an array at given indices |
| `searchsorted` | Function | Insertion points in a sorted array, O(log n) per query |
| `shares_memory` | Function | True when two arrays alias the same buffer |
| `side` | Parameter | Which side of a bin edge owns equal values |
| `take` | Function | Gather along an axis with wrap/clip/raise modes |
| Top-k | Pattern | The k largest/smallest elements, unsorted |
| View | Concept | Array sharing memory with its base |
| `return_counts` | Parameter | `unique` option emitting the label histogram |
| `unique` | Function | Sorted unique values; with counts, a categorical histogram |
| `permutation` | Function | Random index order for shuffling |

## Detailed Definitions

### `argpartition`
**Definition**: `np.argpartition(x, k)` returns indices such that
`x[idx[k]]` is the (k+1)-th smallest and all left entries are ≤
it. O(n) average — the top-k tool.

**Example**:
```python
import numpy as np

x = np.random.default_rng(2).normal(size=100_000)
k = 5
idx = np.argpartition(x, -k)[-k:]          # k largest, unsorted
print(np.array_equal(np.sort(x[idx]), np.sort(x)[-k:]))  # True
```

**Complexity**: O(n) average; slice + `np.sort` of k winners.
**Related**: `argsort`, Top-k

---

### `argsort`
**Definition**: Indices that sort the array completely:
`x[np.argsort(x)]` is sorted ascending. O(n log n) — use only
when the full order is needed.

**Example**:
```python
import numpy as np

x = np.array([3.0, 1.0, 2.0])
print(np.argsort(x))            # [1 2 0]
print(x[np.argsort(x)])         # [1. 2. 3.]
```

**Complexity**: O(n log n), O(n) index buffer.
**Related**: `argpartition`

---

### Boolean mask
**Definition**: A same-shaped array of True/False that selects
positions when used as an index: `x[x > 0]` returns the positive
entries, as a copy.

**Example**:
```python
import numpy as np

x = np.array([1.0, -2.0, 3.0])
print(x[x > 0.0])               # [1. 3.]
print((x > 0.0).sum())          # 2
```

**Complexity**: O(n) mask build, O(kept) copy.
**Related**: Masked assignment, Fancy indexing

---

### `digitize`
**Definition**: `np.digitize(v, bins)` returns bucket indices —
the same as `np.searchsorted(bins, v, side="right")`. Bins must
be sorted.

**Example**:
```python
import numpy as np

bins = np.array([0.0, 0.5, 1.0])
print(np.digitize([0.0, 0.5, 0.75], bins))   # [1 2 2]
```

**Complexity**: O(k log n).
**Related**: `searchsorted`, `side`

---

### Fancy indexing
**Definition**: Indexing with integer arrays:
`x[[i0, i1, ...]]`. Selects in the given order, allows
duplicates, and **always returns a copy** — never a view.

**Example**:
```python
import numpy as np

a = np.arange(6.0)
b = a[[3, 0, 3]]
print(b)                          # [3. 0. 3.]
print(np.shares_memory(a, b))     # False
```

**Complexity**: O(selected).
**Related**: View, Boolean mask

---

### `ix_`
**Definition**: `np.ix_(rows, cols)` wraps index arrays so
`M[np.ix_(rows, cols)]` selects the full rows × cols grid —
equivalent to `M[rows][:, cols]` — instead of elementwise pairing.

**Example**:
```python
import numpy as np

M = np.arange(20.0).reshape(4, 5)
grid = M[np.ix_([0, 3], [1, 2, 4])]
print(grid.shape)                 # (2, 3)
```

**Complexity**: O(rows·cols) copy.
**Related**: Fancy indexing

---

### Masked assignment
**Definition**: Writing through a boolean mask:
`x[x < -1.0] = -1.0` clamps in place — no loop, no copy.

**Example**:
```python
import numpy as np

x = np.array([-3.0, 1.0, -2.0])
x[x < -1.0] = -1.0
print(x)                          # [-1.  1. -1.]
```

**Complexity**: O(n) write.
**Related**: Boolean mask

---

### `put`
**Definition**: `np.put(dst, idx, vals)` writes values at
indices into an existing array (raises by default on
out-of-bounds) — the scatter counterpart to `take`.

**Example**:
```python
import numpy as np

dst = np.zeros(6)
np.put(dst, [0, 2], [9.0, -9.0])
print(dst)                        # [ 9.  0. -9.  0.  0.  0.]
```

**Complexity**: O(k).
**Related**: `take`

---

### `searchsorted`
**Definition**: `np.searchsorted(bins, v)` returns where each v
would insert to keep bins sorted: O(log n) per query. `side`
decides edge ownership.

**Example**:
```python
import numpy as np

bins = np.array([0.0, 0.5, 1.0])
print(np.searchsorted(bins, [0.0, 0.5, 0.75], side="left"))   # [0 1 2]
print(np.searchsorted(bins, [0.0, 0.5, 0.75], side="right"))  # [1 2 2]
```

**Complexity**: O(k log n).
**Related**: `digitize`, `side`

---

### `shares_memory`
**Definition**: `np.shares_memory(a, b)` is True when a and b
alias the same underlying buffer — the definitive view-vs-copy
check.

**Example**:
```python
import numpy as np

base = np.arange(8.0)
print(np.shares_memory(base, base[::2]))    # True -- view
print(np.shares_memory(base, base[[0, 2]]))  # False -- copy
```

**Complexity**: O(1).
**Related**: View

---

### `side`
**Definition**: `searchsorted` parameter. `"left"`: first index
with `bins[i] >= v`; `"right"`: first index with `bins[i] > v`.
Equal values go to the following bucket with `"right"`.

**Example**:
```python
import numpy as np

bins = np.array([0.0, 0.5, 1.0])
print(np.searchsorted(bins, 0.5, side="left"))   # 1
print(np.searchsorted(bins, 0.5, side="right"))  # 2
```

**Complexity**: —.
**Related**: `searchsorted`, `digitize`

---

### `take`
**Definition**: `np.take(a, idx, axis=..., mode=...)` gathers
elements along an axis with an explicit boundary policy:
`"wrap"`, `"clip"`, or `"raise"` (default).

**Example**:
```python
import numpy as np

x = np.arange(6)
print(np.take(x, [7, 8], mode="wrap"))    # [1 2]
print(np.take(x, [-3, 9], mode="clip"))   # [0 5]
```

**Complexity**: O(k).
**Related**: `put`

---

### Top-k
**Definition**: The k largest/smallest elements of an array —
cheaper than a full sort; `argpartition` returns their indices in
O(n). The winners are unsorted.

**Example**:
```python
import numpy as np

x = np.array([5.0, 1.0, 9.0, 2.0, 7.0])
idx = np.argpartition(x, -2)[-2:]
print(np.sort(x[idx]))              # [7. 9.]
```

**Complexity**: O(n) average.
**Related**: `argpartition`, `argsort`

---

### View
**Definition**: An array that aliases another's buffer: basic
slices (`x[::2]`), transposes, and some reshapes are views.
Writing through a view changes the base.

**Example**:
```python
import numpy as np

base = np.arange(10.0)
v = base[::2]
v[:] = -1.0
print(base[0])                      # -1.0 -- wrote through
```

**Complexity**: O(1) to create.
**Related**: `shares_memory`, Fancy indexing

---

### `return_counts`
**Definition**: `np.unique(x, return_counts=True)` additionally
returns how often each unique value occurs — the categorical
histogram.

**Example**:
```python
import numpy as np

lab = np.array([1, 0, 1, 2, 1])
uniq, counts = np.unique(lab, return_counts=True)
print(uniq)                         # [0 1 2]
print(counts)                       # [1 3 1]
```

**Complexity**: O(n log n) via sort.
**Related**: `unique`

---

### `unique`
**Definition**: Sorted unique values of an array. With
`return_counts`, gives class cardinality; with `return_index`,
first occurrences.

**Example**:
```python
import numpy as np

print(np.unique([3, 1, 3, 2, 1]))   # [1 2 3]
```

**Complexity**: O(n log n).
**Related**: `return_counts`

---

### `permutation`
**Definition**: `rng.permutation(n)` returns a random ordering of
`range(n)` — the shuffle index for fancy indexing. Seeded RNGs
make it reproducible.

**Example**:
```python
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(6, 4))
S = X[rng.permutation(X.shape[0])]
print(np.shares_memory(X, S))       # False
```

**Complexity**: O(n).
**Related**: Fancy indexing

## Key Concepts Summary

### Selection tools
- Fancy indexing: reorder/duplicate rows — always a copy.
- Boolean masks: filter and clamp in place.
- `np.ix_`: grids, not pairings.

### Boundary policy
- `take`/`put` with `wrap`/`clip`/`raise`.
- `searchsorted` with `side="left"|"right"`; `digitize` = right.

### Retrieval and stats
- `argpartition` for O(n) top-k; sort only the winners.
- `unique(return_counts=True)` for label histograms.

### Memory semantics
- Basic slices are views; advanced indexing copies.
- `shares_memory` settles any doubt.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Fancy indexing — ___
2. `argpartition` — ___
3. `ix_` — ___
4. `side="right"` — ___
5. View — ___
6. `digitize` — ___

**Answers:**
1. c, 2. e, 3. a, 4. f, 5. b, 6. d

a. Grid selection equivalent to `M[rows][:, cols]`
b. Array aliasing another's buffer; writes pass through
c. Integer-array indexing that always copies
d. Bucket indices; `searchsorted` with `side="right"`
e. O(n) partial-sort indices for top-k
f. Equal boundary values belong to the following bucket

---

**Related docs:** [Indexing basics](https://numpy.org/doc/stable/user/basics.indexing.html) ·
[`np.searchsorted`](https://numpy.org/doc/stable/reference/generated/numpy.searchsorted.html) ·
[Back to lecture](34-advanced-indexing-lecture.md)
