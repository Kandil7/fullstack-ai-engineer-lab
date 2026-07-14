# NumPy Lecture 04: Array Indexing — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Index | Position of element in array | `arr[0]` |
| Positive index | 0-based from start | `arr[0]`, `arr[1]` |
| Negative index | Count from end | `arr[-1]`, `arr[-2]` |
| Fancy indexing | Integer array indexing | `arr[[0, 2, 4]]` |
| Boolean indexing | Mask-based selection | `arr[arr > 0]` |
| Mask | Boolean array for filtering | `arr > 0` |
| np.where | Conditional selection/assignment | `np.where(arr>0, 1, 0)` |
| np.newaxis | Dimension expansion | `arr[:, np.newaxis]` |
| View | Array sharing memory with original | `arr[0:3]` |
| Copy | Independent array copy | `arr[[0, 1]].copy()` |
| Scalar | Single element from array | `arr[0]` returns scalar |
| Axis | Dimension for indexing | `axis=0`, `axis=1` |
| Open mesh | Cross-product indexing | `np.ix_([0,1], [0,1])` |
| Ellipsis | Shorthand for all remaining axes | `arr[..., 0]` |
| np.ix_ | Open mesh indexing | `np.ix_([0,2], [0,2])` |

---

## Alphabetical Glossary

### A

#### Axis
A dimension along which indexing occurs. For 2D arrays: axis 0 = rows, axis 1 = columns.

```python
import numpy as np

matrix = np.array([[1, 2, 3], [4, 5, 6]])

# Index along axis 0 (rows)
print(matrix[0, :])   # [1 2 3] — first row
print(matrix[:, 0])   # [1 4] — first column

# Index along axis 1 (columns)
print(matrix[0, :])   # [1 2 3] — all columns of row 0
print(matrix[1, :])   # [4 5 6] — all columns of row 1
```

**Related:** ndim, shape, indexing

---

### B

#### Boolean Indexing
Select elements using a boolean mask array.

```python
arr = np.array([10, 20, 30, 40, 50])

# Create mask
mask = arr > 30
print(mask)  # [False False False  True  True]

# Apply mask
print(arr[mask])  # [40 50]

# Direct boolean indexing
print(arr[arr > 30])  # [40 50]

# Multiple conditions
print(arr[(arr > 20) & (arr < 50)])  # [30 40]

# For assignment
arr[arr > 30] = 0
print(arr)  # [10 20 30  0  0]
```

**Related:** mask, np.where, fancy indexing

---

### E

#### Ellipsis (...)
Shorthand for selecting all remaining axes.

```python
arr_3d = np.random.rand(2, 3, 4)

# Equivalent indexing
print(arr_3d[:, :, 0].shape)  # (2, 3)
print(arr_3d[..., 0].shape)   # (2, 3)

# Select all elements along last axis
print(arr_3d[..., 0])
```

**Related:** indexing, newaxis, slice

---

### F

#### Fancy Indexing
Indexing using integer arrays to select specific elements.

```python
arr = np.array([10, 20, 30, 40, 50])

# Select specific indices
print(arr[[0, 2, 4]])  # [10 30 50]

# 2D fancy indexing
matrix = np.array([[1, 2], [3, 4], [5, 6]])
print(matrix[[0, 2]])  # Selects rows 0 and 2

# Cross indexing
rows = [0, 1, 2]
cols = [0, 1, 0]
print(matrix[rows, cols])  # [1 4 5]

# Open mesh indexing
ix = np.ix_([0, 2], [0, 1])
print(matrix[ix])
# [[1 2]
#  [5 6]]
```

**Related:** boolean indexing, indexing, np.ix_

---

### I

#### Index
Position of an element in an array (0-based).

```python
arr = np.array([10, 20, 30, 40, 50])

# Access by index
print(arr[0])   # 10 — first element
print(arr[4])   # 50 — last element
print(arr[-1])  # 50 — last element (negative)

# Out of range
# arr[5]  # IndexError: index out of bounds
```

**Related:** positive index, negative index, fancy indexing

---

### M

#### Mask
A boolean array used for conditional selection.

```python
arr = np.array([10, 20, 30, 40, 50])

# Create mask
mask = arr > 30
print(mask)  # [False False False  True  True]

# Use mask for selection
print(arr[mask])  # [40 50]

# Use mask for assignment
arr[mask] = 0
print(arr)  # [10 20 30  0  0]

# Complex masks
mask = (arr > 10) & (arr < 40)
print(arr[mask])  # [20 30]
```

**Related:** boolean indexing, np.where

---

### N

#### Newaxis
Insert a new axis into an array, changing its shape.

```python
arr = np.array([1, 2, 3, 4, 5])
print(arr.shape)  # (5,)

# Add new axis at position 1 (column vector)
col = arr[:, np.newaxis]
print(col.shape)  # (5, 1)

# Add new axis at position 0 (row vector)
row = arr[np.newaxis, :]
print(row.shape)  # (1, 5)

# For broadcasting
a = np.array([1, 2, 3])      # shape (3,)
b = np.array([10, 20])       # shape (2,)
# a[:, np.newaxis] + b  # shape (3, 2)
```

**Related:** reshape, broadcasting, slice

---

#### np.ix_
Create open mesh for cross-product indexing.

```python
matrix = np.arange(12).reshape(3, 4)
print(matrix)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Select (0,0), (0,2), (2,0), (2,2)
ix = np.ix_([0, 2], [0, 2])
print(matrix[ix])
# [[ 0  2]
#  [ 8 10]]
```

**Related:** fancy indexing, open mesh

---

#### np.where
Return elements chosen from x or y based on condition.

```python
arr = np.array([1, 2, 3, 4, 5])

# Basic: np.where(condition, x, y)
result = np.where(arr > 3, 0, arr)
print(result)  # [1 2 3 0 0]

# With different replacements
result = np.where(arr > 3, arr * 10, arr)
print(result)  # [ 1  2  3 40 50]

# Only condition (returns indices)
indices = np.where(arr > 3)
print(indices)  # (array([3, 4]),)

# 2D
matrix = np.array([[1, 2], [3, 4]])
result = np.where(matrix > 2, 100, 0)
print(result)
# [[  0   0]
#  [100 100]]
```

**Related:** boolean indexing, conditional assignment

---

### O

#### Open Mesh
Cross-product of indices for selecting non-contiguous elements.

```python
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Select rows 0,2 and columns 0,2
ix = np.ix_([0, 2], [0, 2])
result = matrix[ix]
print(result)
# [[1 3]
#  [7 9]]

# Equivalent with fancy indexing
rows = [0, 0, 2, 2]
cols = [0, 2, 0, 2]
result = matrix[rows, cols].reshape(2, 2)
```

**Related:** np.ix_, fancy indexing

---

### P

#### Positive Index
Index counting from the start (0-based).

```python
arr = np.array([10, 20, 30, 40, 50])

print(arr[0])   # 10 — first
print(arr[1])   # 20 — second
print(arr[4])   # 50 — fifth (last)
```

**Related:** negative index, indexing

---

### S

#### Scalar
A single element extracted from an array.

```python
arr = np.array([10, 20, 30, 40, 50])

element = arr[0]
print(element)      # 10
print(type(element))  # <class 'numpy.int64'>

# Compare with slicing (returns array)
subset = arr[0:1]
print(subset)        # [10]
print(type(subset))  # <class 'numpy.ndarray'>
```

**Related:** indexing, slicing

---

#### Slice
Select a range of elements using start:stop:step syntax.

```python
arr = np.array([10, 20, 30, 40, 50])

# Basic slicing
print(arr[1:4])    # [20 30 40]
print(arr[::2])    # [10 30 50]
print(arr[::-1])   # [50 40 30 20 10]

# 2D slicing
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix[0:2, 1:3])
# [[2 3]
#  [5 6]]
```

**Related:** indexing, view, copy

---

### V

#### View
A new array object that shares memory with the original.

```python
arr = np.array([1, 2, 3, 4, 5])

# Slicing returns a view
view = arr[1:3]
view[0] = 99
print(arr)  # [ 1 99  3  4  5] — arr is modified!

# Check if view shares memory
print(np.shares_memory(arr, view))  # True
```

**Related:** copy, shares_memory

---

## Indexing Patterns

```python
import numpy as np

arr = np.arange(20).reshape(4, 5)
print(arr)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]

# Single element
print(arr[1, 2])        # 7

# Row
print(arr[1])           # [5 6 7 8 9]

# Column
print(arr[:, 2])        # [ 2  7 12 17]

# Submatrix
print(arr[0:2, 1:3])
# [[1 2]
#  [6 7]]

# Diagonal
print(arr[np.arange(4), np.arange(4)])  # [ 0  6 12 18]

# Anti-diagonal
print(arr[np.arange(4), np.arange(3, -1, -1)])  # [ 4  8 12 16]

# Boolean mask
print(arr[arr > 10])    # [11 12 13 14 15 16 17 18 19]

# Conditional
print(arr[(arr > 5) & (arr < 15)])  # [ 6  7  8  9 10 11 12 13 14]
```
