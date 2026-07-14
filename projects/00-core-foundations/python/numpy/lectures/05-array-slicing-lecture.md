# NumPy Lecture 05: Array Slicing

## 🎯 Topic Overview

Slicing is a powerful way to extract subarrays from NumPy arrays without copying data. This lecture covers 1D slicing, 2D slicing, step slicing, negative slicing, and advanced techniques like ellipsis and np.newaxis. Understanding slicing is crucial for efficient data manipulation.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Slice 1D arrays using start:stop:step syntax
2. Slice 2D and multidimensional arrays
3. Use negative slicing and step values
4. Combine slicing with np.newaxis for dimension expansion
5. Use ellipsis (...) for convenient indexing
6. Understand views vs copies in slicing
7. Avoid common slicing pitfalls

---

## 1. Basic 1D Slicing

### Syntax: `arr[start:stop:step]`

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# Basic slicing — elements 1 to 4 (stop is exclusive)
print(arr[1:5])      # [20 30 40 50]

# From start to index 5
print(arr[:5])       # [10 20 30 40 50]

# From index 3 to end
print(arr[3:])       # [40 50 60 70 80 90 100]

# Entire array (copy)
print(arr[:])        # [10 20 30 40 50 60 70 80 90 100]
```

### Step Value

```python
arr = np.arange(10)  # [0 1 2 3 4 5 6 7 8 9]

# Every 2nd element
print(arr[::2])      # [0 2 4 6 8]

# Every 3rd element
print(arr[::3])      # [0 3 6 9]

# With start and stop
print(arr[1:8:2])    # [1 3 5 7]

# Reversed array
print(arr[::-1])     # [9 8 7 6 5 4 3 2 1 0]

# Reversed with step
print(arr[::-2])     # [9 7 5 3 1]
```

---

## 2. 2D Slicing

### Row and Column Slicing

```python
matrix = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12],
                   [13, 14, 15, 16]])

# First row
print(matrix[0])        # [1 2 3 4]

# First two rows
print(matrix[:2])
# [[1 2 3 4]
#  [5 6 7 8]]

# Last two rows
print(matrix[-2:])
# [[ 9 10 11 12]
#  [13 14 15 16]]

# First column
print(matrix[:, 0])     # [1 5 9 13]

# First two columns
print(matrix[:, :2])
# [[ 1  2]
#  [ 5  6]
#  [ 9 10]
#  [13 14]]

# Middle 2×2 submatrix
print(matrix[1:3, 1:3])
# [[ 6  7]
#  [10 11]]
```

### Row-wise and Column-wise Slicing

```python
matrix = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12],
                   [13, 14, 15, 16]])

# Every other row
print(matrix[::2])
# [[ 1  2  3  4]
#  [ 9 10 11 12]]

# Every other column
print(matrix[:, ::2])
# [[ 1  3]
#  [ 5  7]
#  [ 9 11]
#  [13 15]]

# Reverse rows
print(matrix[::-1])
# [[13 14 15 16]
#  [ 9 10 11 12]
#  [ 5  6  7  8]
#  [ 1  2  3  4]]

# Reverse columns
print(matrix[:, ::-1])
# [[ 4  3  2  1]
#  [ 8  7  6  5]
#  [12 11 10  9]
#  [16 15 14 13]]
```

---

## 3. Negative Slicing

```python
arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# Last 3 elements
print(arr[-3:])       # [80 90 100]

# Everything except last 3
print(arr[:-3])       # [10 20 30 40 50 60 70]

# From 3rd to last to end
print(arr[-3::1])     # [80 90 100]

# Reversed last 5
print(arr[-5::-1])    # [50 40 30 20 10]

# 2D negative slicing
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Last row
print(matrix[-1])     # [7 8 9]

# Last column
print(matrix[:, -1])  # [3 6 9]

# Bottom-right 2×2
print(matrix[-2:, -2:])
# [[5 6]
#  [8 9]]
```

---

## 4. Advanced Slicing Techniques

### 4.1 Ellipsis (...)

```python
arr_3d = np.random.rand(2, 3, 4)

# Select all along first two axes, specific third
print(arr_3d[:, :, 0].shape)  # (2, 3)
print(arr_3d[..., 0].shape)   # (2, 3) — equivalent!

# Select all along first axis, specific second and third
print(arr_3d[0, :, :].shape)  # (3, 4)
print(arr_3d[0, ...].shape)   # (3, 4) — equivalent!
```

### 4.2 np.newaxis for Dimension Expansion

```python
arr = np.array([1, 2, 3, 4, 5])
print(arr.shape)       # (5,)

# Add new axis at position 1
col = arr[:, np.newaxis]
print(col.shape)       # (5, 1)
print(col)
# [[1]
#  [2]
#  [3]
#  [4]
#  [5]]

# Add new axis at position 0
row = arr[np.newaxis, :]
print(row.shape)       # (1, 5)
print(row)             # [[1 2 3 4 5]]

# For broadcasting
a = np.array([1, 2, 3])      # (3,)
b = np.array([10, 20])       # (2,)
c = a[:, np.newaxis] + b     # (3, 2)
print(c)
# [[11 21]
#  [12 22]
#  [13 23]]
```

### 4.3 Strided Slicing

```python
arr = np.arange(20).reshape(4, 5)
print(arr)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]

# Every other row and column
print(arr[::2, ::2])
# [[ 0  2  4]
#  [10 12 14]]

# Reverse with step
print(arr[::-2, ::-2])
# [[19 17 15]
#  [ 9  7  5]]
```

---

## 5. Views vs Copies

### Slicing Returns a VIEW

```python
arr = np.array([10, 20, 30, 40, 50])

# Slicing creates a view (shares memory)
view = arr[1:3]
print(view)  # [20 30]

# Modify the view
view[0] = 999
print(arr)   # [ 10 999  30  40  50] — original is modified!

# Check if they share memory
print(np.shares_memory(arr, view))  # True
```

### When to Use .copy()

```python
arr = np.array([10, 20, 30, 40, 50])

# Explicit copy (independent memory)
copy = arr[1:3].copy()
print(copy)  # [20 30]

# Modify the copy
copy[0] = 999
print(arr)   # [10 20 30 40 50] — original is NOT modified

# Check memory
print(np.shares_memory(arr, copy))  # False
```

### Memory Efficiency

```python
import sys

arr = np.arange(1000000)

# View — no extra memory
view = arr[::2]
print(f"View size: {sys.getsizeof(view)}")  # Small!

# Copy — copies all data
copy = arr[::2].copy()
print(f"Copy size: {sys.getsizeof(copy)}")  # Large!

# Shares memory check
print(np.shares_memory(arr, view))   # True
print(np.shares_memory(arr, copy))   # False
```

---

## 6. Slicing for Assignment

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Replace first 5 elements
arr[:5] = 0
print(arr)  # [ 0  0  0  0  0  6  7  8  9 10]

# Replace every other element
arr[::2] = -1
print(arr)  # [-1  0 -1  0 -1  6 -1  8 -1 10]

# Replace with a range
arr[3:7] = np.arange(100, 104)
print(arr)  # [-1  0 -1 100 101 102 103  8 -1 10]

# 2D assignment
matrix = np.zeros((3, 3), dtype=int)
matrix[0] = [1, 2, 3]
matrix[:, 1] = [4, 5, 6]
print(matrix)
# [[1 4 3]
#  [0 5 0]
#  [0 6 0]]
```

---

## 7. Common Slicing Patterns

### 7.1 Flattening and Reshaping with Slicing

```python
# Flatten 2D to 1D
matrix = np.array([[1, 2, 3], [4, 5, 6]])
flat = matrix.ravel()  # or matrix.reshape(-1)
print(flat)  # [1 2 3 4 5 6]

# Reshape with slicing
arr = np.arange(20)
reshaped = arr.reshape(4, 5)
print(reshaped)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]
```

### 7.2 Diagonal Extraction

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Main diagonal
diag = matrix[np.arange(3), np.arange(3)]
print(diag)  # [1 5 9]

# Or use np.diag()
print(np.diag(matrix))  # [1 5 9]

# Anti-diagonal
anti = matrix[np.arange(3), np.arange(2, -1, -1)]
print(anti)  # [3 5 7]
```

### 7.3 Upper and Lower Triangular

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Upper triangle (excluding diagonal)
for i in range(3):
    for j in range(i+1, 3):
        print(f"matrix[{i},{j}] = {matrix[i,j]}")
# matrix[0,1] = 2
# matrix[0,2] = 3
# matrix[1,2] = 6

# Lower triangle (excluding diagonal)
for i in range(3):
    for j in range(i):
        print(f"matrix[{i},{j}] = {matrix[i,j]}")
# matrix[1,0] = 4
# matrix[2,0] = 7
# matrix[2,1] = 8
```

---

## 8. Common Mistakes to Avoid

### Mistake 1: Forgetting Stop is Exclusive
```python
arr = np.array([10, 20, 30, 40, 50])
print(arr[1:3])  # [20 30] — NOT including index 3!
```

### Mistake 2: Modifying Through a View
```python
arr = np.array([1, 2, 3, 4, 5])
view = arr[1:3]
view[0] = 99
print(arr)  # [ 1 99  3  4  5] — unintended!

# Fix: use .copy()
copy = arr[1:3].copy()
copy[0] = 99
print(arr)  # [1 2 3 4 5] — unchanged
```

### Mistake 3: Using Float Indices
```python
arr = np.array([1, 2, 3, 4, 5])
# arr[1.5:3.5]  # TypeError: slice indices must be integers
arr[1:4]        # Correct
```

### Mistake 4: Confusing Slicing and Indexing
```python
arr = np.array([10, 20, 30, 40, 50])

# Indexing — returns scalar
print(type(arr[0]))    # <class 'numpy.int64'>

# Slicing — returns array
print(type(arr[0:1]))  # <class 'numpy.ndarray'>
```

---

## 9. Best Practices

1. **Use slicing over loops** — slicing is vectorized and fast
2. **Be mindful of views** — use `.copy()` when you need independent data
3. **Use negative indexing** for accessing from the end
4. **Use `...` (ellipsis)** for cleaner multidimensional slicing
5. **Use `np.newaxis`** for dimension expansion
6. **Check shapes after slicing** — unexpected shapes cause broadcasting errors
7. **Avoid chained assignments** — `arr[0:3][0] = 5` doesn't modify `arr`

---

## 10. Practice Exercises

### Exercise 1: Basic Slicing
```python
import numpy as np

arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# a) Get elements 3 to 7
# b) Get every other element
# c) Get elements in reverse order
# d) Get last 4 elements
# e) Get elements from index 2 to 8 with step 3

# Solutions:
print(arr[3:8])    # [3 4 5 6 7]
print(arr[::2])    # [0 2 4 6 8]
print(arr[::-1])   # [9 8 7 6 5 4 3 2 1 0]
print(arr[-4:])    # [6 7 8 9]
print(arr[2:8:3])  # [2 5]
```

### Exercise 2: 2D Slicing
```python
matrix = np.array([[1, 2, 3, 4, 5],
                   [6, 7, 8, 9, 10],
                   [11, 12, 13, 14, 15],
                   [16, 17, 18, 19, 20],
                   [21, 22, 23, 24, 25]])

# a) Get top-left 3×3
# b) Get bottom-right 2×2
# c) Get center element
# d) Get all rows, columns 1 and 3
# e) Get rows 1-3, all columns

# Solutions:
print(matrix[:3, :3])
print(matrix[-2:, -2:])
print(matrix[2, 2])
print(matrix[:, [1, 3]])
print(matrix[1:4])
```

### Exercise 3: Views vs Copies
```python
arr = np.array([1, 2, 3, 4, 5])

# Create a view and a copy
view = arr[1:4]
copy = arr[1:4].copy()

# Modify the view
view[0] = 99

# Question: What is arr now? What about copy?
print(arr)    # [ 1 99  3  4  5]
print(copy)   # [2 3 4]

# Verify memory sharing
print(np.shares_memory(arr, view))   # True
print(np.shares_memory(arr, copy))   # False
```

### Exercise 4: Advanced Slicing
```python
arr = np.arange(20).reshape(4, 5)
print(arr)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]

# a) Get every other element (both directions)
# b) Get the main diagonal
# c) Get the anti-diagonal
# d) Get corners: (0,0), (0,4), (3,0), (3,4)
# e) Reverse both rows and columns

# Solutions:
print(arr[::2, ::2])
# [[ 0  2  4]
#  [10 12 14]]

print(arr[np.arange(4), np.arange(4)])  # [ 0  6 12 18]

print(arr[np.arange(4), np.arange(3, -1, -1)])  # [ 4  8 12 16]

print(arr[[0, 0, 3, 3], [0, 4, 0, 4]])  # [ 0  4 15 19]

print(arr[::-1, ::-1])
# [[19 18 17 16 15]
#  [14 13 12 11 10]
#  [ 9  8  7  6  5]
#  [ 4  3  2  1  0]]
```

---

## 11. Summary

| Syntax | Description | Example |
|--------|-------------|---------|
| `arr[start:stop]` | Elements from start to stop-1 | `arr[1:4]` |
| `arr[start:]` | From start to end | `arr[3:]` |
| `arr[:stop]` | From beginning to stop-1 | `arr[:4]` |
| `arr[::step]` | Every step elements | `arr[::2]` |
| `arr[::-1]` | Reversed array | `arr[::-1]` |
| `arr[start:stop:step]` | Full control | `arr[1:8:2]` |
| `arr[..., i]` | Ellipsis shorthand | `arr[..., 0]` |
| `arr[:, np.newaxis]` | Add dimension | Column vector |
| `arr[start:stop].copy()` | Explicit copy | Independent data |

### Key Takeaways

1. Slicing uses `start:stop:step` syntax (stop is exclusive)
2. Slicing returns a VIEW — modifying it changes the original
3. Use `.copy()` when you need independent data
4. Negative indices count from the end (-1 is last)
5. Ellipsis `...` simplifies multidimensional slicing
6. `np.newaxis` expands array dimensions for broadcasting
7. Slicing is vectorized — much faster than Python loops

---

## 🔗 Next Lecture

→ [06-data-types-lecture.md](./06-data-types-lecture.md) — Data Types
