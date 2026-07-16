# NumPy Lecture 04: Array Indexing

## 🎯 Topic Overview

Array indexing is how you access and modify individual elements or groups of elements in NumPy arrays. This lecture covers single-element indexing, negative indexing, multidimensional indexing, integer array indexing, and boolean array indexing. Mastering indexing is essential for data manipulation.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Access single elements using positive and negative indices
2. Index multidimensional arrays along different axes
3. Use integer array indexing (fancy indexing)
4. Apply boolean array indexing (masking)
5. Understand the difference between indexing and slicing
6. Use `np.newaxis` for dimension expansion
7. Avoid common indexing pitfalls

---

## 1. Single Element Indexing

### 1.1 Basic 1D Indexing

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Positive indexing (0-based)
print(arr[0])   # 10 (first element)
print(arr[2])   # 30 (third element)
print(arr[4])   # 50 (last element)

# Negative indexing
print(arr[-1])  # 50 (last element)
print(arr[-2])  # 40 (second to last)
print(arr[-5])  # 10 (first element)

# Out of range
# arr[5]  # IndexError: index 5 is out of bounds
```

### 1.2 2D Array Indexing

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Access by row, column
print(matrix[0, 0])   # 1 (first row, first column)
print(matrix[0, 2])   # 3 (first row, third column)
print(matrix[2, 1])   # 8 (third row, second column)

# Negative indexing
print(matrix[-1, -1]) # 9 (last row, last column)
print(matrix[-2, 0])  # 4 (second row, first column)

# Single index returns entire row
print(matrix[0])      # [1 2 3]
print(matrix[1])      # [4 5 6]
```

### 1.3 3D Array Indexing

```python
tensor = np.array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]]])

# Access by depth, row, column
print(tensor[0, 0, 0])  # 1
print(tensor[0, 1, 1])  # 4
print(tensor[1, 0, 1])  # 6
print(tensor[1, 1, 0])  # 7

# Access entire depth
print(tensor[0])        # [[1 2] [3 4]]
```

---

## 2. Multidimensional Indexing

### 2.1 Row and Column Selection

```python
matrix = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12]])

# Select entire row
print(matrix[0])       # [1 2 3 4]
print(matrix[1])       # [5 6 7 8]

# Select entire column
print(matrix[:, 0])    # [1 5 9]
print(matrix[:, 2])    # [3 7 11]

# Select specific row and column
print(matrix[0, 0])    # 1
print(matrix[1, 2])    # 7
```

### 2.2 Axis-Based Indexing

```python
# Understanding axes
arr_3d = np.random.rand(2, 3, 4)  # 2 blocks, 3 rows, 4 columns

# Axis 0 — blocks (depth)
print(arr_3d[0].shape)   # (3, 4)
print(arr_3d[1].shape)   # (3, 4)

# Axis 1 — rows
print(arr_3d[:, 0].shape)  # (2, 4)

# Axis 2 — columns
print(arr_3d[:, :, 0].shape)  # (2, 3)
```

---

## 3. Integer Array Indexing (Fancy Indexing)

### 3.1 Basic Fancy Indexing

```python
arr = np.array([10, 20, 30, 40, 50, 60, 70, 80])

# Index with a list of indices
indices = [0, 2, 4, 6]
print(arr[indices])  # [10 30 50 70]

# Repeating indices
indices = [0, 0, 1, 1, 2, 2]
print(arr[indices])  # [10 10 20 20 30 30]
```

### 3.2 2D Fancy Indexing

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Select rows 0 and 2
print(matrix[[0, 2]])
# [[1 2 3]
#  [7 8 9]]

# Select specific elements
rows = [0, 1, 2]
cols = [0, 1, 2]
print(matrix[rows, cols])  # [1 5 9] — diagonal elements

# Different rows and columns
rows = [0, 0, 1]
cols = [0, 1, 2]
print(matrix[rows, cols])  # [1 2 6]
```

### 3.3 Advanced Fancy Indexing

```python
matrix = np.arange(12).reshape(3, 4)
print(matrix)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Select (0,0), (1,2), (2,3)
indices = np.array([[0, 0], [1, 2], [2, 3]])
print(matrix[indices[:, 0], indices[:, 1]])  # [0 6 11]

# Using np.ix_ for open mesh indexing
ix = np.ix_([0, 2], [0, 2])
print(matrix[ix])
# [[ 0  2]
#  [ 8 10]]
```

---

## 4. Boolean Array Indexing (Masking)

### 4.1 Basic Boolean Indexing

```python
arr = np.array([10, 20, 30, 40, 50])

# Create boolean mask
mask = arr > 30
print(mask)  # [False False False  True  True]

# Apply mask
print(arr[mask])  # [40 50]

# Direct boolean indexing
print(arr[arr > 30])  # [40 50]

# Multiple conditions
print(arr[(arr > 20) & (arr < 50)])  # [30 40]
```

### 4.2 2D Boolean Indexing

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Boolean mask for entire matrix
mask = matrix > 5
print(mask)
# [[False False False]
#  [False False  True]
#  [ True  True  True]]

# Select matching elements (flattened)
print(matrix[mask])  # [6 7 8 9]

# Select rows where any element > 5
row_mask = np.any(matrix > 5, axis=1)
print(matrix[row_mask])
# [[4 5 6]
#  [7 8 9]]

# Select columns where all elements > 2
col_mask = np.all(matrix > 2, axis=0)
print(matrix[:, col_mask])
# [[3]
#  [6]
#  [9]]
```

### 4.3 Boolean Indexing for Assignment

```python
arr = np.array([1, 2, 3, 4, 5])

# Replace all elements > 3 with 0
arr[arr > 3] = 0
print(arr)  # [1 2 3 0 0]

# Replace all even numbers with -1
arr = np.array([1, 2, 3, 4, 5])
arr[arr % 2 == 0] = -1
print(arr)  # [ 1 -1  3 -1  5]

# Using np.where for conditional assignment
arr = np.array([1, 2, 3, 4, 5])
arr = np.where(arr > 3, 0, arr)  # Replace > 3 with 0, else keep
print(arr)  # [1 2 3 0 0]
```

---

## 5. np.where — Conditional Selection

```python
arr = np.array([1, 2, 3, 4, 5])

# Basic where: np.where(condition, x, y)
result = np.where(arr > 3, 0, arr)
print(result)  # [1 2 3 0 0]

# With different replacement values
result = np.where(arr > 3, arr * 10, arr)
print(result)  # [ 1  2  3 40 50]

# 2D example
matrix = np.array([[1, 2], [3, 4]])
result = np.where(matrix > 2, 100, 0)
print(result)
# [[  0   0]
#  [100 100]]

# With only condition (returns indices)
indices = np.where(arr > 3)
print(indices)  # (array([3, 4]),)
```

---

## 6. np.newaxis — Dimension Expansion

```python
arr = np.array([1, 2, 3, 4, 5])

# Original shape
print(arr.shape)       # (5,)

# Add new axis at position 1 (column vector)
col = arr[:, np.newaxis]
print(col.shape)       # (5, 1)
print(col)
# [[1]
#  [2]
#  [3]
#  [4]
#  [5]]

# Add new axis at position 0 (row vector)
row = arr[np.newaxis, :]
print(row.shape)       # (1, 5)
print(row)             # [[1 2 3 4 5]]

# Equivalent using reshape
col = arr.reshape(-1, 1)
row = arr.reshape(1, -1)
```

---

## 7. Indexing vs Slicing

### Key Differences

```python
arr = np.array([1, 2, 3, 4, 5])

# Indexing — returns a SCALAR
element = arr[0]
print(type(element))  # <class 'numpy.int64'>

# Slicing — returns an ARRAY
subset = arr[0:2]
print(type(subset))  # <class 'numpy.ndarray'>
print(subset.shape)  # (2,)

# Integer array indexing — returns an ARRAY
fancy = arr[[0, 2]]
print(type(fancy))   # <class 'numpy.ndarray'>
print(fancy.shape)   # (2,)

# Boolean indexing — returns an ARRAY
bool_arr = arr[arr > 2]
print(type(bool_arr))  # <class 'numpy.ndarray'>
print(bool_arr.shape)  # (3,)
```

### View vs Copy in Indexing

```python
arr = np.array([1, 2, 3, 4, 5])

# Slicing returns a VIEW (shares memory)
view = arr[1:3]
view[0] = 99
print(arr)  # [ 1 99  3  4  5] — arr is modified!

# Fancy indexing returns a COPY (independent memory)
copy = arr[[0, 2, 4]]
copy[0] = 999
print(arr)  # [ 1 99  3  4  5] — arr is NOT modified

# Boolean indexing returns a COPY
bool_copy = arr[arr > 3]
bool_copy[0] = 999
print(arr)  # [ 1 99  3  4  5] — arr is NOT modified
```

---

## 8. Common Mistakes to Avoid

### Mistake 1: Using Float as Index
```python
arr = np.array([10, 20, 30, 40, 50])
# arr[1.5]  # IndexError: only integers can be used for indexing
arr[1]      # Correct — returns 20
```

### Mistake 2: Modifying a View
```python
arr = np.array([1, 2, 3, 4, 5])
view = arr[1:3]
view[0] = 99
print(arr)  # [ 1 99  3  4  5] — unintended modification!

# Fix: use .copy()
copy = arr[1:3].copy()
copy[0] = 99
print(arr)  # [1 2 3 4 5] — arr unchanged
```

### Mistake 3: Wrong Shape for Boolean Indexing
```python
matrix = np.array([[1, 2], [3, 4], [5, 6]])
mask = np.array([True, False, True])

# WRONG — shapes don't align
# matrix[mask]  # This will work but may not be what you want

# RIGHT — use axis parameter
rows = matrix[mask]  # Selects rows 0 and 2
```

### Mistake 4: Forgetting Parentheses in Conditions
```python
arr = np.array([1, 2, 3, 4, 5])

# WRONG — operator precedence error
# arr[arr > 2 & arr < 4]  # Error!

# RIGHT — use parentheses
result = arr[(arr > 2) & (arr < 4)]  # [3]
```

---

## 9. Best Practices

1. **Use negative indexing** for accessing from the end: `arr[-1]`
2. **Use boolean indexing** for conditional selection: `arr[arr > 0]`
3. **Use `np.where()`** for conditional assignment
4. **Use `.copy()`** when you need an independent copy
5. **Always use parentheses** with `&` and `|` operators
6. **Check array shape** before indexing operations
7. **Use `np.newaxis`** for dimension expansion
8. **Prefer boolean indexing** over loop-based filtering

---

## 10. Practice Exercises

### Exercise 1: Basic Indexing
```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# a) Get first element
# b) Get last element
# c) Get 5th element
# d) Get 3rd to last element
# e) Get elements at indices 0, 2, 4, 6, 8

# Solutions:
print(arr[0])        # 10
print(arr[-1])       # 100
print(arr[4])        # 50
print(arr[-3])       # 80
print(arr[0:9:2])    # [10 30 50 70 90]
```

### Exercise 2: 2D Indexing
```python
matrix = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12],
                   [13, 14, 15, 16]])

# a) Get element at row 1, column 2
# b) Get entire row 2
# c) Get entire column 0
# d) Get submatrix rows 0-1, columns 1-2

# Solutions:
print(matrix[1, 2])    # 7
print(matrix[2])       # [9 10 11 12]
print(matrix[:, 0])    # [1 5 9 13]
print(matrix[0:2, 1:3])
# [[2 3]
#  [6 7]]
```

### Exercise 3: Boolean Indexing
```python
arr = np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

# a) Get all elements greater than 25
# b) Get all elements between 15 and 35
# c) Get all even numbers
# d) Replace all elements > 30 with 0

# Solutions:
print(arr[arr > 25])              # [30 35 40 45 50]
print(arr[(arr >= 15) & (arr <= 35)])  # [15 20 25 30 35]
print(arr[arr % 2 == 0])          # [10 20 30 40 50]
arr_copy = arr.copy()
arr_copy[arr_copy > 30] = 0
print(arr_copy)
```

### Exercise 4: Fancy Indexing
```python
matrix = np.arange(20).reshape(4, 5)
print(matrix)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]

# a) Select elements at (0,0), (1,1), (2,2), (3,3)
# b) Select rows 0 and 3
# c) Select columns 1 and 4

# Solutions:
diag_idx = np.arange(4)
print(matrix[diag_idx, diag_idx])  # [ 0  6 12 18]
print(matrix[[0, 3]])
print(matrix[:, [1, 4]])
```

---

## 11. Summary

| Method | Returns | Use Case |
|--------|---------|----------|
| `arr[i]` | Scalar | Single element |
| `arr[i, j]` | Scalar | 2D element |
| `arr[i:j]` | View | Slice of array |
| `arr[[indices]]` | Copy | Select specific elements |
| `arr[condition]` | Copy | Conditional selection |
| `np.where(cond, x, y)` | Array | Conditional assignment |
| `arr[:, np.newaxis]` | View | Dimension expansion |

### Key Takeaways

1. NumPy uses 0-based indexing (first element is at index 0)
2. Negative indexing counts from the end (-1 is last)
3. Boolean indexing is powerful for conditional selection
4. Fancy indexing returns a copy; slicing returns a view
5. Use `np.where()` for conditional assignment
6. Always use parentheses with `&` and `|` operators
7. `np.newaxis` expands array dimensions

---

## 🔗 Next Lecture

→ [05-array-slicing-lecture.md](./05-array-slicing-lecture.md) — Array Slicing
