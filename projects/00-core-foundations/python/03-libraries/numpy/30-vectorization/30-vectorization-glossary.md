# Vectorization — Glossary 30

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `einsum` | Function | Einstein notation for named-axis array operations |
| Boolean mask | Pattern | A bool array selecting positions for read or write |
| BLAS | Background | Optimized linear-algebra kernels behind `@` and matmul |
| Broadcasting | Concept | Shape-stretching rules that make elementwise ops uniform (lecture 29) |
| `fromiter` | Function | Builds an array from a Python iterable, element by element |
| Interpreter overhead | Concept | Per-element Python dispatch cost that vectorization removes |
| Masked reduction | Pattern | `vals[mask].sum()` — aggregate over selected positions |
| `np.clip` | Function | Clamp values to `[lo, hi]` in one vectorized pass |
| `np.maximum` | Function | Elementwise max — the vectorized ReLU |
| `np.vectorize` | Function | Wraps a scalar function as a ufunc-style callable — NOT fast |
| `np.where` | Function | Elementwise select between two arrays by a condition |
| Ragged data | Concept | Variable-length rows that cannot form a dense 2-D array |
| Scalar function | Concept | A function of one number, used as a ufunc building block |
| Temporary buffer | Concept | A full-size intermediate array allocated by an expression |
| Ufunc | Concept | Universal function — elementwise C loop over array operands |
| Vectorization | Concept | Expressing array math without per-element Python loops |

## Detailed Definitions

### BLAS
**Definition**: Basic Linear Algebra Subprograms — the highly tuned
Fortran/C kernels (`dgemm`, `daxpy`, ...) that NumPy calls for
`@`, `dot`, `matmul`, and many reductions. Vectorized code gets BLAS;
loops never do.

**Example**:
```python
import numpy as np

A = np.random.default_rng(0).normal(size=(2000, 2000))
B = np.random.default_rng(1).normal(size=(2000, 2000))
C = A @ B          # BLAS dgemm: ~8e9 flops in compiled code
print(C.shape)     # (2000, 2000)
```

**Complexity**: O(n·m·k) work at ~10-100 GFLOP/s.
**Related**: Vectorization, Ufunc, Temporary buffer

---

### Boolean mask
**Definition**: A boolean array, same leading shape as the data, used
for selection `vals[mask]` or scatter `vals[mask] = 0`.

**Example**:
```python
import numpy as np

vals = np.array([-3.0, 1.0, -2.0, 4.0])
mask = vals < 0
print(mask)            # [ True False  True False]
vals[mask] = 0.0
print(vals)            # [0. 1. 0. 4.]
```

**Complexity**: O(n) per mask operation.
**Related**: Masked reduction, `np.where`

---

### Broadcasting
**Definition**: The rules by which arrays of different shapes combine
elementwise (align trailing dims; equal-or-1 compatible; size-1 dims
stretch). Vectorization depends on it: `(B, T, D)` math with `(D,)`
vectors works without loops.

**Example**:
```python
import numpy as np

batch = np.ones((8, 5))
bias = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
print((batch + bias).shape)     # (8, 5)
```

**Complexity**: O(result size).
**Related**: Ufunc, Vectorization

---

### `einsum`
**Definition**: `np.einsum("subscripts", *operands)` — each letter is
an axis; repeated letters on the input side are summed over; the
output side lists kept axes. Expresses dot, outer, trace, transpose,
and batch products.

**Example**:
```python
import numpy as np

A = np.random.default_rng(2).normal(size=(4, 5))
B = np.random.default_rng(3).normal(size=(5, 6))
print(np.allclose(np.einsum("ij,jk->ik", A, B), A @ B))   # True
print(np.einsum("ii->", np.ones((5, 5))))                 # 5.0
```

**Complexity**: same as the equivalent BLAS op, slightly slower at
large sizes; O(1) clarity win.
**Related**: Vectorization, BLAS, Temporary buffer

---

### `fromiter`
**Definition**: Creates an array by iterating a Python generator —
the efficient way to *build* from a loop you cannot avoid, but still
per-element Python.

**Example**:
```python
import numpy as np

arr = np.fromiter((i * i for i in range(5)), dtype=np.int64)
print(arr)                     # [ 0  1  4  9 16]
```

**Complexity**: O(n) interpreter steps.
**Related**: Interpreter overhead, Ragged data

---

### Interpreter overhead
**Definition**: The per-element cost of Python-level dispatch —
attribute lookups, bytecode, boxing — that makes loops 10-100×
slower than compiled ufuncs. Vectorization removes it.

**Example**:
```python
import numpy as np

x = np.random.default_rng(0).normal(size=1_000_000)
vec = np.maximum(x, 0.0)        # one C pass
# the loop equivalent touches 1e6 elements through the interpreter
```

**Complexity**: ~50-200 ns per interpreter step vs ~1-5 ns per
compiled element.
**Related**: Ufunc, Vectorization

---

### Masked reduction
**Definition**: Aggregate over the positions where a condition holds:
`vals[mask].sum()`, `(x > 0).mean()`. One pass, compiled.

**Example**:
```python
import numpy as np

vals = np.random.default_rng(1).normal(size=100_000)
print(int((vals > 0).sum()))                  # count positives
print(np.allclose(vals[vals > 0].sum(),
                  np.where(vals > 0, vals, 0.0).sum()))  # True
```

**Complexity**: O(n).
**Related**: Boolean mask, `np.where`

---

### `np.clip`
**Definition**: Clamps values into `[lo, hi]` in one vectorized pass.
Prefer it over nested `np.where` for this exact job.

**Example**:
```python
import numpy as np

x = np.array([-5.0, 0.5, 3.0, 9.0])
print(np.clip(x, 0.0, 1.0))     # [0.  0.5 1.  1. ]
```

**Complexity**: O(n).
**Related**: `np.where`, `np.maximum`

---

### `np.maximum`
**Definition**: Elementwise maximum of two arrays — one expression
implements ReLU (`np.maximum(x, 0)`).

**Example**:
```python
import numpy as np

x = np.array([-2.0, -0.5, 0.0, 1.5])
print(np.maximum(x, 0.0))       # [0.  0.  0.  1.5]
```

**Complexity**: O(n).
**Related**: Ufunc, `np.where`

---

### `np.vectorize`
**Definition**: Wraps a Python scalar function so it can be called
with array arguments and broadcasting — but every element still
passes through the interpreter. Convenience, not performance.

**Example**:
```python
import numpy as np

def f(x):
    return x * 2 if x > 0 else -x

f_vec = np.vectorize(f)
x = np.array([-1.0, 2.0, 3.0])
print(f_vec(x))                 # [ 1.  4.  6.]
```

**Complexity**: O(n) interpreter calls — same class as the loop.
**Related**: Interpreter overhead, Scalar function, Vectorization

---

### `np.where`
**Definition**: `np.where(cond, a, b)` returns `a` where `cond` is
True, `b` elsewhere — the vectorized if-else. Both arms are computed;
selection happens elementwise.

**Example**:
```python
import numpy as np

x = np.array([-2.0, 3.0, -1.0])
print(np.where(x > 0, x, 0.0))  # [0. 3. 0.]
```

**Complexity**: O(n) time, O(n) output.
**Related**: Boolean mask, `np.clip`

---

### Ragged data
**Definition**: Rows of different lengths — no dense 2-D array. The
loop-over-outer/vectorize-inner pattern applies: iterate rows, use
vectorized ops inside each body.

**Example**:
```python
import numpy as np

rows = [np.array([1.0, 2.0]), np.array([3.0, 4.0, 5.0, 6.0])]
stats = np.array([(r.mean(), r.std()) for r in rows])
print(stats.shape)              # (2, 2)
```

**Complexity**: O(#rows) interpreter steps + O(total elements) work.
**Related**: `fromiter`, Interpreter overhead

---

### Scalar function
**Definition**: A function of one number (`def f(x): return x * 2`).
Ufuncs vectorize it; `np.vectorize` does not — it just calls it in a
loop.

**Example**:
```python
import numpy as np

def f(x):
    return x * 2 if x > 0 else -x

# vectorized rewrite, no scalar function at all:
x = np.array([-1.0, 2.0])
print(np.where(x > 0, x * 2, -x))   # [1. 4.]
```

**Complexity**: —.
**Related**: `np.vectorize`, Ufunc

---

### Temporary buffer
**Definition**: A full-size intermediate array that an expression
allocates (`(a * b) + (c * d)` makes `a*b` and `c*d` first). At 1M
elements each temporary is 8 MB of float64; memory traffic, not
flops, usually dominates.

**Example**:
```python
import numpy as np

a = np.ones(1_000_000)
b = np.ones(1_000_000)
y = np.empty_like(a)
np.multiply(a, b, out=y)   # same result, no intermediate
print(y.sum())             # 1000000.0
```

**Complexity**: O(n) per temporary.
**Related**: Vectorization, BLAS, Complexity and Cost

---

### Ufunc
**Definition**: Universal function — an elementwise operation over
array operands implemented as a compiled loop (`np.add`, `np.exp`,
`np.maximum`). The building block of vectorization.

**Example**:
```python
import numpy as np

x = np.array([1.0, 4.0, 9.0])
print(np.sqrt(x))           # [1. 2. 3.]
```

**Complexity**: O(n), compiled.
**Related**: Vectorization, `np.maximum`, Broadcasting

---

### Vectorization
**Definition**: The practice of expressing array math without
per-element Python loops, so the work runs in compiled ufunc/BLAS
code. The central performance skill for AI engineering.

**Example**:
```python
import numpy as np

# loop (slow)  vs  vectorized (fast)
x = np.random.default_rng(0).normal(size=100_000)
y_loop = [max(v, 0.0) for v in x]
y_vec = np.maximum(x, 0.0)
print(np.allclose(y_loop, y_vec))     # True
```

**Complexity**: O(n) compiled vs O(n) interpreter steps.
**Related**: Ufunc, Interpreter overhead, `einsum`

## Key Concepts Summary

### The rewrites
- Elementwise loops → ufuncs (`np.maximum`, `np.exp`, ...).
- Scalar branches → `np.where` / `np.clip`.
- Filter loops → boolean masks + masked reductions.

### The tools
- `einsum` for named-axis math; verify against `@` and `.T`.
- `keepdims` + `newaxis` keep broadcast shapes sane.
- `out=` arguments reuse buffers instead of allocating temporaries.

### The truths
- `np.vectorize` is a loop in disguise.
- Ragged data legitimately needs an outer loop — vectorize the body.
- Print timings; never assert wall clock.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `np.vectorize` — ___
2. `einsum` — ___
3. Boolean mask — ___
4. Ufunc — ___
5. Temporary buffer — ___
6. Ragged data — ___

**Answers:**
1. b, 2. e, 3. f, 4. a, 5. c, 6. d

a. Compiled elementwise operation (`np.add`, `np.maximum`)
b. Scalar-function wrapper that still iterates in Python
c. Full-size intermediate allocated by an expression
d. Variable-length rows needing a loop-outer pattern
e. Named-axis notation for dot, trace, outer, batch matmul
f. Boolean array selecting positions for read or write

---

**Related docs:** [NumPy einsum](https://numpy.org/doc/stable/reference/generated/numpy.einsum.html) ·
[`np.vectorize`](https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html) ·
[ufunc reference](https://numpy.org/doc/stable/reference/ufuncs.html) ·
[Back to lecture](30-vectorization-lecture.md)
