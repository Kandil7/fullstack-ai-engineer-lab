# NumPy Lecture 10: Array Iterating — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| nditer | Efficient multi-dim iterator | `np.nditer(arr)` |
| ndenumerate | Index + value iterator | `np.ndenumerate(arr)` |
| flat | Flat iterator for any array | `arr.flat` |
| for loop | Basic iteration | `for x in arr:` |
| axis | Dimension to iterate | `axis=0`, `axis=1` |
| Vectorization | Element-wise operations | `arr * 2` |
| op_flags | Modify elements in nditer | `['readwrite']` |
| order | Iteration order (C/F) | `order='C'`, `order='F'` |
| zip | Parallel iteration | `zip(arr1, arr2)` |
| enumerate | Index + value | `enumerate(arr)` |
| Element-wise | Operation per element | `arr + 1` |
| Row-major | C order (row-first) | Default |
| Column-major | F order (column-first) | `order='F'` |

---

## Alphabetical Glossary

### A

#### Axis
A dimension along which iteration occurs.

```python
import numpy as np

matrix = np.array([[1, 2, 3], [4, 5, 6]])

# Iterate along axis 0 (rows)
for row in matrix:
    print(row)
# [1 2 3]
# [4 5 6]

# Iterate along axis 1 (columns)
for col in matrix.T:
    print(col)
# [1 4]
# [2 5]
# [3 6]
```

**Related:** nditer, shape, iterate

---

### E

#### Element-wise
An operation applied independently to each element.

```python
arr = np.array([1, 2, 3, 4, 5])

# Element-wise operations
print(arr * 2)    # [2 4 6 8 10]
print(arr ** 2)   # [1 4 9 16 25]
print(np.sqrt(arr))  # [1. 1.414 1.732 2. 2.236]
```

**Related:** vectorization, ufunc

---

#### Enumerate
Get index and value while iterating.

```python
arr = np.array([10, 20, 30])

# Python enumerate
for i, val in enumerate(arr):
    print(f"Index {i}: {val}")

# NumPy ndenumerate (for multi-dim)
matrix = np.array([[1, 2], [3, 4]])
for idx, val in np.ndenumerate(matrix):
    print(f"Index {idx}: {val}")
```

**Related:** ndenumerate, nditer

---

### F

#### Flat
Iterator that yields all elements as if array were 1D.

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])

# Iterate over all elements
for element in matrix.flat:
    print(element, end=' ')
print()
# 1 2 3 4 5 6

# Access by flat index
print(matrix.flat[0])  # 1
print(matrix.flat[4])  # 5
```

**Related:** ravel, flatten, nditer

---

### I

#### Iterate
Traverse through array elements one by one.

```python
arr = np.array([1, 2, 3, 4, 5])

# Basic iteration
for element in arr:
    print(element)
```

**Related:** nditer, for loop, vectorization

---

### N

#### Ndenumerate
Iterate over array yielding (index, value) pairs.

```python
arr = np.array([[10, 20], [30, 40]])

for index, value in np.ndenumerate(arr):
    print(f"Index {index}: {value}")
# Index (0, 0): 10
# Index (0, 1): 20
# Index (1, 0): 30
# Index (1, 1): 40
```

**Related:** nditer, enumerate

---

#### Nditer
Efficient multi-dimensional array iterator.

```python
arr = np.arange(12).reshape(3, 4)

# Basic iteration
for element in np.nditer(arr):
    print(element, end=' ')
print()
# 0 1 2 3 4 5 6 7 8 9 10 11

# With order control
for element in np.nditer(arr, order='F'):
    print(element, end=' ')
print()
# 0 4 8 1 5 9 2 6 10 3 7 11

# With modification
for element in np.nditer(arr, op_flags=['readwrite']):
    element[...] = element * 2
```

**Related:** ndenumerate, flat, order

---

### O

#### Order
Iteration order: 'C' (row-major) or 'F' (column-major).

```python
arr = np.arange(12).reshape(3, 4)

# C order (default)
for element in np.nditer(arr, order='C'):
    print(element, end=' ')
print()
# 0 1 2 3 4 5 6 7 8 9 10 11

# F order
for element in np.nditer(arr, order='F'):
    print(element, end=' ')
print()
# 0 4 8 1 5 9 2 6 10 3 7 11
```

**Related:** contiguous, row-major, column-major

---

#### Op_flags
Flags to control nditer behavior (e.g., allow modification).

```python
arr = np.array([1, 2, 3], dtype=float)

# Default: read-only
for element in np.nditer(arr):
    pass  # element[...] = 0  # Error!

# With readwrite flag
for element in np.nditer(arr, op_flags=['readwrite']):
    element[...] = element * 2

print(arr)  # [2. 4. 6.]
```

**Related:** nditer, readwrite

---

### R

#### Readwrite
Op_flag that allows modifying elements during iteration.

```python
arr = np.arange(5).astype(float)

for element in np.nditer(arr, op_flags=['readwrite']):
    element[...] = element ** 2

print(arr)  # [ 0.  1.  4.  9. 16.]
```

**Related:** nditer, op_flags

---

#### Row-major
C-style memory layout (rows first, default).

```python
arr = np.arange(12).reshape(3, 4)

# C order iteration
for element in np.nditer(arr, order='C'):
    print(element, end=' ')
print()
# 0 1 2 3 4 5 6 7 8 9 10 11
```

**Related:** column-major, order, contiguous

---

### V

#### Vectorization
Performing operations on entire arrays instead of element-by-element loops.

```python
arr = np.arange(1000000)

# Vectorized (fast)
result = arr * 2

# Loop (slow)
result = np.zeros_like(arr)
for i in range(len(arr)):
    result[i] = arr[i] * 2
```

**Related:** element-wise, ufunc, nditer

---

### Z

#### Zip
Iterate over multiple arrays in parallel.

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([10, 20, 30])

for a, b in zip(arr1, arr2):
    print(f"{a} + {b} = {a + b}")
# 1 + 10 = 11
# 2 + 20 = 22
# 3 + 30 = 33
```

**Related:** nditer, parallel iteration

---

## Iteration Methods Comparison

| Method | Returns | Use Case | Performance |
|--------|---------|----------|-------------|
| `for x in arr` | Elements | 1D or row iteration | Fast |
| `np.nditer(arr)` | Elements | Multi-dim iteration | Fast |
| `np.nditer(arr, order='F')` | Elements | Column-major | Fast |
| `np.ndenumerate(arr)` | (index, value) | Need indices | Fast |
| `arr.flat` | Elements | Flat iteration | Fast |
| `zip(arr1, arr2)` | Tuples | Parallel iteration | Fast |
| `enumerate(arr)` | (index, value) | 1D with indices | Fast |

## When to Use Vectorization vs Iteration

| Task | Recommended |
|------|-------------|
| Element-wise math | Vectorized (`arr * 2`) |
| Conditional operations | `np.where()` |
| Aggregations | `arr.sum()`, `arr.mean()` |
| Complex per-element logic | Iteration (with `nditer`) |
| Need indices | `np.ndenumerate()` |
| Parallel arrays | `zip()` or `np.nditer()` |
