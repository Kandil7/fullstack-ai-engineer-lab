# NumPy Lecture 13: Array Search — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| where | Find elements by condition | `np.where(arr > 0)` |
| argmax | Index of maximum value | `np.argmax(arr)` |
| argmin | Index of minimum value | `np.argmin(arr)` |
| nonzero | Indices of non-zero elements | `np.nonzero(arr)` |
| searchsorted | Binary search in sorted array | `np.searchsorted(arr, v)` |
| Boolean indexing | Select by condition | `arr[arr > 0]` |
| mask | Boolean array for filtering | `arr > 0` |
| Condition | Boolean expression | `arr > 0`, `arr == 5` |
| Side | Left/right insertion point | `side='left'`, `side='right'` |
| all | Test if all elements True | `np.all(arr > 0)` |
| any | Test if any element True | `np.any(arr > 0)` |

---

## Alphabetical Glossary

### A

#### All
Test if all elements along an axis are True.

```python
import numpy as np

matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Test if all elements > 0
print(np.all(matrix > 0))  # True

# Test along axis 0 (columns)
print(np.all(matrix > 5, axis=0))  # [False False False]

# Test along axis 1 (rows)
print(np.all(matrix > 5, axis=1))  # [False False  True]
```

**Related:** any, boolean indexing

---

#### Any
Test if any element along an axis is True.

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Test if any element > 5
print(np.any(matrix > 5))  # True

# Test along axis 0 (columns)
print(np.any(matrix > 5, axis=0))  # [ True  True  True]

# Test along axis 1 (rows)
print(np.any(matrix > 5, axis=1))  # [False  True  True]
```

**Related:** all, boolean indexing

---

#### Argmax
Return index of maximum value along an axis.

```python
arr = np.array([10, 50, 30, 80, 20])

# Index of maximum
print(np.argmax(arr))  # 3 (index of 80)

# 2D example
matrix = np.array([[1, 5, 3],
                   [9, 2, 7]])

# Max along axis 0 (columns)
print(np.argmax(matrix, axis=0))  # [1 0 1]

# Max along axis 1 (rows)
print(np.argmax(matrix, axis=1))  # [1 0]

# Get actual values
max_values = matrix[np.arange(2), np.argmax(matrix, axis=1)]
print(max_values)  # [5 9]
```

**Related:** argmin, max, where

---

#### Argmin
Return index of minimum value along an axis.

```python
arr = np.array([10, 50, 30, 80, 20])

# Index of minimum
print(np.argmin(arr))  # 0 (index of 10)

# 2D example
matrix = np.array([[1, 5, 3],
                   [9, 2, 7]])

# Min along axis 0 (columns)
print(np.argmin(matrix, axis=0))  # [0 1 0]

# Min along axis 1 (rows)
print(np.argmin(matrix, axis=1))  # [0 1]
```

**Related:** argmax, min, where

---

### B

#### Boolean Indexing
Select elements using a boolean mask.

```python
arr = np.array([10, 20, 30, 40, 50])

# Boolean mask
mask = arr > 30
result = arr[mask]
print(result)  # [40 50]

# Multiple conditions
mask = (arr > 20) & (arr < 50)
result = arr[mask]
print(result)  # [30 40]
```

**Related:** where, mask, condition

---

### C

#### Condition
Boolean expression used for filtering.

```python
arr = np.array([1, 2, 3, 4, 5])

# Simple condition
mask = arr > 3
print(mask)  # [False False False  True  True]

# Multiple conditions
mask = (arr > 1) & (arr < 5)
print(mask)  # [False  True  True  True  False]
```

**Related:** boolean indexing, where, mask

---

### M

#### Mask
Boolean array used for conditional selection.

```python
arr = np.array([10, 20, 30, 40, 50])

# Create mask
mask = arr > 30
print(mask)  # [False False False  True  True]

# Use mask
result = arr[mask]
print(result)  # [40 50]

# Use mask for assignment
arr[mask] = 0
print(arr)  # [10 20 30  0  0]
```

**Related:** boolean indexing, where, condition

---

### N

#### Nonzero
Return indices of non-zero elements.

```python
arr = np.array([0, 0, 3, 0, 5, 0, 7])

# Indices of non-zero
indices = np.nonzero(arr)
print(indices)  # (array([2, 4, 6]),)

# Get values
values = arr[indices]
print(values)  # [3 5 7]

# 2D example
matrix = np.array([[0, 1, 0],
                   [2, 0, 3]])
rows, cols = np.nonzero(matrix)
print(f"Rows: {rows}")  # [0 1 1]
print(f"Cols: {cols}")  # [1 0 2]
```

**Related:** where, boolean indexing

---

### S

#### Searchsorted
Binary search to find insertion point in sorted array.

```python
arr = np.array([10, 20, 30, 40, 50])

# Left insertion point
idx = np.searchsorted(arr, 25, side='left')
print(idx)  # 2

# Right insertion point
idx = np.searchsorted(arr, 25, side='right')
print(idx)  # 2

# Exact value
idx = np.searchsorted(arr, 30, side='left')
print(idx)  # 2

idx = np.searchsorted(arr, 30, side='right')
print(idx)  # 3

# Multiple values
values = np.array([5, 25, 35, 55])
indices = np.searchsorted(arr, values)
print(indices)  # [0 2 3 5]
```

**Note:** Array must be sorted!

**Related:** where, binary search

---

#### Side
Parameter for searchsorted: 'left' or 'right' insertion point.

```python
arr = np.array([10, 20, 30, 30, 30, 40, 50])

# Left: first position where value can be inserted
print(np.searchsorted(arr, 30, side='left'))  # 2

# Right: last position where value can be inserted
print(np.searchsorted(arr, 30, side='right'))  # 5
```

**Related:** searchsorted

---

### W

#### Where
Find elements or indices based on condition.

```python
arr = np.array([10, 20, 30, 40, 50])

# Find indices where condition is True
indices = np.where(arr > 30)
print(indices)  # (array([3, 4]),)

# Get values
values = arr[indices]
print(values)  # [40 50]

# Conditional assignment
result = np.where(arr > 30, 0, arr)
print(result)  # [10 20 30  0  0]

# 2D
matrix = np.array([[1, 2], [3, 4]])
indices = np.where(matrix > 2)
print(indices)  # (array([1, 1]), array([0, 1]))
```

**Related:** boolean indexing, argmax, argmin

---

## Search Methods Comparison

| Method | Returns | Use Case |
|--------|---------|----------|
| `np.where()` | Indices/tuple | Conditional search |
| `np.argmax()` | Index | Find max position |
| `np.argmin()` | Index | Find min position |
| `np.nonzero()` | Indices | Non-zero elements |
| `np.searchsorted()` | Index | Binary search (sorted) |
| `arr[mask]` | Values | Boolean filtering |
| `np.all()` | Boolean | Test all elements |
| `np.any()` | Boolean | Test any element |

## Quick Search Patterns

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Find elements > 25
result = arr[arr > 25]

# Find indices > 25
indices = np.where(arr > 25)[0]

# Find closest to 33
closest = arr[np.argmin(np.abs(arr - 33))]

# Find all occurrences of 30
occurrences = np.where(arr == 30)[0]
```
