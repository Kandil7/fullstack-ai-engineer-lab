# NumPy Lecture 10: Array Iterating

## 🎯 Topic Overview

Iterating over arrays is a fundamental operation. While NumPy encourages vectorized operations, sometimes you need to iterate. This lecture covers `nditer`, `ndenumerate`, flat iteration, and when to use loops vs vectorized operations.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Iterate over arrays with Python `for` loops
2. Use `np.nditer()` for efficient iteration
3. Use `np.ndenumerate()` to get indices and values
4. Iterate over flat arrays with `.flat`
5. Understand when to iterate vs vectorize
6. Optimize iteration performance

---

## 1. Basic Iteration with For Loops

### 1.1 1D Array Iteration

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Iterate over 1D array
for element in arr:
    print(element)
# 10 20 30 40 50
```

### 1.2 2D Array Iteration

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Iterate over rows (axis 0)
print("Iterating over rows:")
for row in matrix:
    print(row)
# [1 2 3]
# [4 5 6]
# [7 8 9]

# Iterate over columns (axis 1)
print("\nIterating over columns:")
for col in matrix.T:
    print(col)
# [1 4 7]
# [2 5 8]
# [3 6 9]
```

### 1.3 3D Array Iteration

```python
tensor = np.arange(24).reshape(2, 3, 4)

# Iterate over first dimension
print("Iterating over depth:")
for depth in tensor:
    print(depth.shape)  # (3, 4)
```

---

## 2. `np.nditer()` — Efficient Iteration

### 2.1 Basic nditer

```python
arr = np.arange(12).reshape(3, 4)

# Iterate over all elements
for element in np.nditer(arr):
    print(element, end=' ')
# 0 1 2 3 4 5 6 7 8 9 10 11

print()

# nditer handles multi-dimensional iteration automatically
```

### 2.2 Controlling Iteration Order

```python
arr = np.arange(12).reshape(3, 4)

# C order (row-major, default)
print("C order:")
for element in np.nditer(arr, order='C'):
    print(element, end=' ')
print()
# 0 1 2 3 4 5 6 7 8 9 10 11

# F order (column-major)
print("F order:")
for element in np.nditer(arr, order='F'):
    print(element, end=' ')
print()
# 0 4 8 1 5 9 2 6 10 3 7 11
```

### 2.3 Modifying Elements with nditer

```python
arr = np.arange(12).reshape(3, 4).astype(float)

# Read-only by default
for element in np.nditer(arr):
    pass  # element[...] = 0  # ValueError!

# Use op_flags to allow modification
for element in np.nditer(arr, op_flags=['readwrite']):
    element[...] = element * 2

print(arr)
# [[ 0.  2.  4.  6.]
#  [ 8. 10. 12. 14.]
#  [16. 18. 20. 22.]]
```

---

## 3. `np.ndenumerate()` — Indices and Values

### 3.1 Basic ndenumerate

```python
arr = np.array([[10, 20, 30],
                [40, 50, 60]])

# Get index and value
for index, value in np.ndenumerate(arr):
    print(f"Index {index}: {value}")
# Index (0, 0): 10
# Index (0, 1): 20
# Index (0, 2): 30
# Index (1, 0): 40
# Index (1, 1): 50
# Index (1, 2): 60
```

### 3.2 ndenumerate with 3D

```python
arr = np.arange(8).reshape(2, 2, 2)

for index, value in np.ndenumerate(arr):
    print(f"Index {index}: {value}")
# Index (0, 0, 0): 0
# Index (0, 0, 1): 1
# Index (0, 1, 0): 2
# Index (0, 1, 1): 3
# Index (1, 0, 0): 4
# Index (1, 0, 1): 5
# Index (1, 1, 0): 6
# Index (1, 1, 1): 7
```

---

## 4. Flat Iteration with `.flat`

### 4.1 Basic Flat Iteration

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Iterate over all elements (flattened)
for element in matrix.flat:
    print(element, end=' ')
print()
# 1 2 3 4 5 6 7 8 9

# Access by flat index
print(matrix.flat[0])   # 1
print(matrix.flat[4])   # 5
print(matrix.flat[8])   # 9
```

### 4.2 Flat Iteration with 3D

```python
arr = np.arange(8).reshape(2, 2, 2)

for element in arr.flat:
    print(element, end=' ')
print()
# 0 1 2 3 4 5 6 7
```

---

## 5. When to Iterate vs Vectorize

### 5.1 Vectorized Operations (Preferred)

```python
import time

arr = np.arange(1000000)

# Vectorized operation (fast)
start = time.time()
result = arr * 2
print(f"Vectorized: {time.time() - start:.4f}s")

# Python loop (slow)
start = time.time()
result = np.zeros_like(arr)
for i in range(len(arr)):
    result[i] = arr[i] * 2
print(f"Python loop: {time.time() - start:.4f}s")

# Result is the same, but vectorized is 10-100x faster!
```

### 5.2 When Iteration is Necessary

```python
arr = np.array([1, 2, 3, 4, 5])

# Complex operations that can't be vectorized
for i, val in enumerate(arr):
    if val % 2 == 0:
        arr[i] = val ** 2
    else:
        arr[i] = val ** 3

print(arr)  # [1 4 27 16 125]

# Or use np.where (better)
arr = np.array([1, 2, 3, 4, 5])
arr = np.where(arr % 2 == 0, arr ** 2, arr ** 3)
print(arr)  # [1 4 27 16 125]
```

---

## 6. Advanced Iteration Patterns

### 6.1 Iterating Over Specific Axes

```python
arr = np.arange(12).reshape(3, 4)

# Iterate over columns
for col in arr.T:
    print(col)
# [0 4 8]
# [1 5 9]
# [2 6 10]
# [3 7 11]

# Iterate over depth (3D)
tensor = np.arange(24).reshape(2, 3, 4)
for depth in tensor:
    print(depth.shape)  # (3, 4)
```

### 6.2 Parallel Iteration

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([10, 20, 30])

# Use zip for parallel iteration
for a, b in zip(arr1, arr2):
    print(f"{a} + {b} = {a + b}")
# 1 + 10 = 11
# 2 + 20 = 22
# 3 + 30 = 33

# Or use nditer for parallel
for x, y in np.nditer([arr1, arr2]):
    print(f"{x} + {y} = {x + y}")
```

---

## 7. Common Mistakes to Avoid

### Mistake 1: Using Python Loops for Element-wise Operations
```python
# SLOW — Python loop
arr = np.arange(1000000)
result = np.zeros_like(arr)
for i in range(len(arr)):
    result[i] = arr[i] * 2

# FAST — Vectorized
result = arr * 2
```

### Mistake 2: Modifying Through nditer Without Flags
```python
arr = np.array([1, 2, 3], dtype=float)

# This will error
# for element in np.nditer(arr):
#     element[...] = 0  # ValueError: read-only!

# Fix: use op_flags
for element in np.nditer(arr, op_flags=['readwrite']):
    element[...] = 0
```

### Mistake 3: Not Using ndenumerate When Indices Are Needed
```python
# INEFFICIENT
arr = np.array([10, 20, 30])
for i in range(len(arr)):
    print(f"Index {i}: {arr[i]}")

# BETTER
for i, val in np.ndenumerate(arr):
    print(f"Index {i}: {val}")
```

---

## 8. Best Practices

1. **Prefer vectorized operations** over Python loops
2. **Use `np.nditer()`** for multi-dimensional iteration
3. **Use `np.ndenumerate()`** when you need indices
4. **Use `.flat`** for iterating over all elements
5. **Use `order='F'`** for column-major iteration
6. **Use `op_flags=['readwrite']`** to modify elements
7. **Avoid Python loops** for element-wise operations

---

## 9. Practice Exercises

### Exercise 1: Basic Iteration
```python
import numpy as np

matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# a) Iterate over rows and print each
# b) Iterate over columns and print each
# c) Iterate over all elements and print each

print("Rows:")
for row in matrix:
    print(row)

print("\nColumns:")
for col in matrix.T:
    print(col)

print("\nAll elements:")
for element in matrix.flat:
    print(element, end=' ')
print()
```

### Exercise 2: ndenumerate
```python
arr = np.array([[10, 20, 30],
                [40, 50, 60],
                [70, 80, 90]])

# Find indices of all elements > 50
indices = []
for index, value in np.ndenumerate(arr):
    if value > 50:
        indices.append(index)

print(f"Indices: {indices}")  # [(1, 2), (2, 0), (2, 1), (2, 2)]
```

### Exercise 3: Vectorized vs Loop
```python
import time

arr = np.arange(1000000)

# Compare performance
start = time.time()
result_loop = np.zeros_like(arr)
for i in range(len(arr)):
    result_loop[i] = arr[i] ** 2
loop_time = time.time() - start

start = time.time()
result_vec = arr ** 2
vec_time = time.time() - start

print(f"Loop: {loop_time:.4f}s")
print(f"Vectorized: {vec_time:.4f}s")
print(f"Speedup: {loop_time / vec_time:.1f}x")
```

### Exercise 4: nditer Modification
```python
arr = np.arange(12).reshape(3, 4).astype(float)

# Double all even numbers
for element in np.nditer(arr, op_flags=['readwrite']):
    if element % 2 == 0:
        element[...] = element * 2

print(arr)
# [[ 0.  1.  4.  3.]
#  [ 8.  5. 12.  7.]
#  [16.  9. 20. 11.]]
```

---

## 10. Summary

| Method | Description | Use Case |
|--------|-------------|----------|
| `for x in arr` | Iterate over axis 0 | 1D or row iteration |
| `np.nditer(arr)` | Efficient multi-dim iteration | All elements |
| `np.ndenumerate(arr)` | Index + value iteration | Need indices |
| `arr.flat` | Flat iterator | All elements 1D |
| `zip(arr1, arr2)` | Parallel iteration | Multiple arrays |

### Key Takeaways

1. Python `for` loops iterate over axis 0 (rows for 2D)
2. `np.nditer()` provides efficient multi-dimensional iteration
3. `np.ndenumerate()` returns both indices and values
4. `.flat` provides a flat iterator for any dimensionality
5. **Always prefer vectorized operations** over Python loops
6. Use `op_flags=['readwrite']` to modify elements in nditer
7. Use `order='F'` for column-major iteration

---

## 🔗 Next Lecture

→ [11-array-join-lecture.md](./11-array-join-lecture.md) — Array Join
