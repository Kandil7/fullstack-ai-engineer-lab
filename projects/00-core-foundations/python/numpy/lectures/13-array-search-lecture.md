# NumPy Lecture 13: Array Search

## 🎯 Topic Overview

Searching arrays is essential for finding elements, indices, and values. This lecture covers `where()`, `argmax()`, `argmin()`, `nonzero()`, `searchsorted()`, and boolean indexing for search operations.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Find elements using `np.where()`
2. Get indices of min/max values with `argmin()`/`argmax()`
3. Find non-zero elements with `nonzero()`
4. Use `searchsorted()` for sorted arrays
5. Apply boolean indexing for conditional search
6. Combine multiple search conditions

---

## 1. `np.where()` — Conditional Search

### 1.1 Basic where

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# Find where condition is True
indices = np.where(arr > 50)
print(indices)  # (array([5, 6, 7, 8, 9]),)

# Get the values
values = arr[indices]
print(values)  # [ 60  70  80  90 100]
```

### 1.2 where with Conditional Assignment

```python
arr = np.array([1, 2, 3, 4, 5])

# Replace elements based on condition
result = np.where(arr > 3, 0, arr)
print(result)  # [1 2 3 0 0]

# With different replacements
result = np.where(arr > 3, arr * 10, arr)
print(result)  # [ 1  2  3 40 50]
```

### 1.3 where with 2D Arrays

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Find indices where condition is True
indices = np.where(matrix > 5)
print(indices)
# (array([1, 1, 2, 2, 2]), array([1, 2, 0, 1, 2]))

# Get values
values = matrix[indices]
print(values)  # [6 7 8 9]
```

---

## 2. `argmax()` and `argmin()` — Index of Extremes

### 2.1 Basic argmax/argmin

```python
arr = np.array([10, 50, 30, 80, 20, 90, 40])

# Index of maximum value
max_idx = np.argmax(arr)
print(f"Max index: {max_idx}, Max value: {arr[max_idx]}")
# Max index: 5, Max value: 90

# Index of minimum value
min_idx = np.argmin(arr)
print(f"Min index: {min_idx}, Min value: {arr[min_idx]}")
# Min index: 0, Min value: 10
```

### 2.2 argmax/argmin with Axis

```python
matrix = np.array([[1, 5, 3],
                   [9, 2, 7],
                   [4, 8, 6]])

# Max along axis 0 (columns)
max_col = np.argmax(matrix, axis=0)
print(f"Max indices per column: {max_col}")  # [1 2 1]

# Max along axis 1 (rows)
max_row = np.argmax(matrix, axis=1)
print(f"Max indices per row: {max_row}")  # [1 0 1]

# Get actual values
max_values = matrix[np.arange(3), max_row]
print(f"Max values per row: {max_values}")  # [5 9 8]
```

---

## 3. `nonzero()` — Find Non-zero Elements

```python
arr = np.array([0, 0, 3, 0, 5, 0, 7, 0, 0])

# Find indices of non-zero elements
indices = np.nonzero(arr)
print(indices)  # (array([2, 4, 6]),)

# Get non-zero values
values = arr[indices]
print(values)  # [3 5 7]

# 2D example
matrix = np.array([[0, 1, 0],
                   [2, 0, 3],
                   [0, 4, 0]])

# Find non-zero indices
rows, cols = np.nonzero(matrix)
print(f"Rows: {rows}")  # [0 1 1 2]
print(f"Cols: {cols}")  # [1 0 2 1]

# Get values
values = matrix[rows, cols]
print(values)  # [1 2 3 4]
```

---

## 4. `searchsorted()` — Binary Search

### 4.1 Basic searchsorted

```python
arr = np.array([10, 20, 30, 40, 50])

# Find where 35 would be inserted (left side)
idx = np.searchsorted(arr, 35, side='left')
print(f"Insert at: {idx}")  # 2

# Find where 35 would be inserted (right side)
idx = np.searchsorted(arr, 35, side='right')
print(f"Insert at: {idx}")  # 2

# Find where 30 would be inserted
idx = np.searchsorted(arr, 30, side='left')
print(f"Insert at: {idx}")  # 2

idx = np.searchsorted(arr, 30, side='right')
print(f"Insert at: {idx}")  # 3
```

### 4.2 searchsorted with Multiple Values

```python
arr = np.array([10, 20, 30, 40, 50])
values = np.array([5, 25, 35, 55])

# Find insertion points for multiple values
indices = np.searchsorted(arr, values)
print(indices)  # [0 2 3 5]
```

---

## 5. Boolean Indexing for Search

### 5.1 Basic Boolean Search

```python
arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# Find elements > 50
mask = arr > 50
result = arr[mask]
print(result)  # [ 60  70  80  90 100]

# Find elements between 30 and 70
mask = (arr >= 30) & (arr <= 70)
result = arr[mask]
print(result)  # [30 40 50 60 70]

# Find even numbers
mask = arr % 2 == 0
result = arr[mask]
print(result)  # [10 20 30 40 50 60 70 80 90 100]
```

### 5.2 Boolean Search with np.where

```python
arr = np.array([10, 20, 30, 40, 50])

# Get indices where condition is True
indices = np.where(arr > 25)[0]
print(indices)  # [2 3 4]

# Get values
values = arr[indices]
print(values)  # [30 40 50]
```

---

## 6. Combined Search Operations

### 6.1 Find All Matching Elements

```python
matrix = np.random.randint(0, 100, (5, 5))
print(matrix)

# Find all elements > 50
rows, cols = np.where(matrix > 50)
print(f"Indices: {list(zip(rows, cols))}")

# Get values
values = matrix[rows, cols]
print(f"Values: {values}")
```

### 6.2 Find Closest Value

```python
arr = np.array([10, 20, 30, 40, 50])
target = 33

# Find closest value
idx = np.argmin(np.abs(arr - target))
print(f"Closest: {arr[idx]} at index {idx}")  # 30 at index 2
```

### 6.3 Find First/Last Occurrence

```python
arr = np.array([1, 2, 3, 2, 4, 2, 5])

# Find all occurrences of 2
indices = np.where(arr == 2)[0]
print(f"All indices: {indices}")  # [1 3 5]
print(f"First: {indices[0]}")     # 1
print(f"Last: {indices[-1]}")     # 5
```

---

## 7. Common Mistakes to Avoid

### Mistake 1: Forgetting where Returns Tuple
```python
arr = np.array([10, 20, 30, 40, 50])

# where returns a tuple
indices = np.where(arr > 30)
print(indices)  # (array([3, 4]),)

# Get the array from tuple
indices = np.where(arr > 30)[0]
print(indices)  # [3 4]
```

### Mistake 2: Confusing argmax with max
```python
arr = np.array([10, 50, 30])

# argmax returns INDEX, not value
print(np.argmax(arr))  # 1 (index of 50)

# To get the value
print(arr[np.argmax(arr)])  # 50
```

### Mistake 3: searchsorted Requires Sorted Array
```python
arr = np.array([10, 20, 30, 40, 50])

# searchsorted works on sorted arrays
print(np.searchsorted(arr, 25))  # 2

# Unsorted array gives wrong results
arr_unsorted = np.array([50, 10, 40, 20, 30])
print(np.searchsorted(arr_unsorted, 25))  # Wrong!
```

---

## 8. Best Practices

1. **Use `np.where()`** for conditional search and assignment
2. **Use `argmax()`/`argmin()`** to find indices of extremes
3. **Use `nonzero()`** to find non-zero elements
4. **Use `searchsorted()`** for binary search in sorted arrays
5. **Use boolean indexing** for complex conditions
6. **Remember where returns a tuple** — use `[0]` to extract
7. **Check array is sorted** before using `searchsorted()`

---

## 9. Practice Exercises

### Exercise 1: Basic Search
```python
import numpy as np

arr = np.array([15, 23, 42, 8, 16, 31, 27, 58, 12, 39])

# a) Find all elements > 25
# b) Find indices of elements > 25
# c) Find element closest to 30
# d) Find index of maximum element
# e) Find index of minimum element

result_a = arr[arr > 25]
result_b = np.where(arr > 25)[0]
result_c = arr[np.argmin(np.abs(arr - 30))]
result_d = np.argmax(arr)
result_e = np.argmin(arr)

print(f"Elements > 25: {result_a}")
print(f"Indices > 25: {result_b}")
print(f"Closest to 30: {result_c}")
print(f"Max index: {result_d}, Max value: {arr[result_d]}")
print(f"Min index: {result_e}, Min value: {arr[result_e]}")
```

### Exercise 2: 2D Search
```python
matrix = np.random.randint(0, 100, (4, 4))
print(matrix)

# Find all elements > 50
rows, cols = np.where(matrix > 50)
print(f"Elements > 50:")
for r, c in zip(rows, cols):
    print(f"  [{r},{c}] = {matrix[r,c]}")
```

### Exercise 3: searchsorted
```python
arr = np.array([10, 20, 30, 40, 50])

# Find where these values would be inserted
values = [5, 15, 25, 35, 45, 55]
indices = np.searchsorted(arr, values)

for val, idx in zip(values, indices):
    print(f"{val} would be inserted at index {idx}")
```

### Exercise 4: Complex Search
```python
# Find all rows where all elements are > 10
matrix = np.random.randint(0, 50, (5, 5))
print(matrix)

rows_all = np.all(matrix > 10, axis=1)
print(f"\nRows where all elements > 10:")
print(matrix[rows_all])
```

---

## 10. Summary

| Function | Description | Returns |
|----------|-------------|---------|
| `np.where(cond)` | Indices where condition is True | Tuple of arrays |
| `np.where(cond, x, y)` | Conditional assignment | Array |
| `np.argmax(arr)` | Index of maximum | Integer |
| `np.argmin(arr)` | Index of minimum | Integer |
| `np.nonzero(arr)` | Indices of non-zero | Tuple of arrays |
| `np.searchsorted(arr, v)` | Binary search | Integer or array |
| `arr[arr > 0]` | Boolean indexing | Array |

### Key Takeaways

1. `np.where()` returns a tuple of arrays (use `[0]` for 1D)
2. `argmax()`/`argmin()` return indices, not values
3. `nonzero()` finds indices of non-zero elements
4. `searchsorted()` performs binary search (requires sorted array)
5. Boolean indexing is powerful for conditional search
6. Use `np.all()` and `np.any()` for row/column conditions

---

## 🔗 Next Lecture

→ [14-array-sort-lecture.md](./14-array-sort-lecture.md) — Array Sort
