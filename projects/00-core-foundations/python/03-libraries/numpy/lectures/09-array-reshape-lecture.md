# NumPy Lecture 09: Array Reshape

## 🎯 Topic Overview

Reshaping is the process of changing an array's shape without modifying its data. This lecture covers `reshape()`, `ravel()`, `flatten()`, `transpose()`, and advanced reshaping techniques. Mastering reshape is essential for data preparation and manipulation.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Change array shape using `reshape()`
2. Flatten arrays with `ravel()` and `flatten()`
3. Transpose arrays with `.T` and `transpose()`
4. Use `-1` for automatic dimension calculation
5. Understand when reshape creates views vs copies
6. Handle reshape errors gracefully

---

## 1. Basic Reshaping with `reshape()`

### 1.1 Reshape Syntax

```python
import numpy as np

arr = np.arange(12)
print(arr)        # [ 0  1  2  3  4  5  6  7  8  9 10 11]
print(arr.shape)  # (12,)

# Reshape to 3×4
arr_3x4 = arr.reshape(3, 4)
print(arr_3x4)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
print(arr_3x4.shape)  # (3, 4)

# Reshape to 4×3
arr_4x3 = arr.reshape(4, 3)
print(arr_4x3)
# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]
#  [ 9 10 11]]
print(arr_4x3.shape)  # (4, 3)

# Reshape to 3D
arr_3d = arr.reshape(2, 3, 2)
print(arr_3d.shape)   # (2, 3, 2)
```

### 1.2 Using `-1` for Auto-calculation

```python
arr = np.arange(12)

# Let NumPy calculate one dimension
arr_3x4 = arr.reshape(3, -1)   # (3, 4)
arr_4x3 = arr.reshape(-1, 3)   # (4, 3)
arr_2x6 = arr.reshape(2, -1)   # (2, 6)
arr_6x2 = arr.reshape(-1, 2)   # (6, 2)

print(arr_3x4.shape)  # (3, 4)
print(arr_4x3.shape)  # (4, 3)
print(arr_2x6.shape)  # (2, 6)
print(arr_6x2.shape)  # (6, 2)

# 3D with -1
arr_3d = arr.reshape(2, -1, 2)  # (2, 3, 2)
print(arr_3d.shape)  # (2, 3, 2)
```

---

## 2. Flattening Arrays

### 2.1 `ravel()` — Flatten (Returns View When Possible)

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)  # (2, 3)

# ravel returns a flattened view
flat = arr.ravel()
print(flat.shape)  # (12,)
print(flat)        # [1 2 3 4 5 6]

# ravel shares memory with original
print(np.shares_memory(arr, flat))  # True

# Modify flat — original modified!
flat[0] = 999
print(arr)
# [[999   2   3]
#  [  4   5   6]]
```

### 2.2 `flatten()` — Flatten (Returns Copy)

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# flatten returns a copy
flat = arr.flatten()
print(flat.shape)  # (6,)
print(flat)        # [1 2 3 4 5 6]

# flatten does NOT share memory
print(np.shares_memory(arr, flat))  # False

# Modify flat — original NOT modified
flat[0] = 999
print(arr)
# [[1 2 3]
#  [4 5 6]]
```

### 2.3 `ravel()` vs `flatten()`

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# ravel — view (memory efficient)
flat_view = arr.ravel()
print(f"ravel shares memory: {np.shares_memory(arr, flat_view)}")

# flatten — copy (safe)
flat_copy = arr.flatten()
print(f"flatten shares memory: {np.shares_memory(arr, flat_copy)}")

# Performance comparison
import time

arr_large = np.arange(1000000).reshape(1000, 1000)

start = time.time()
_ = arr_large.ravel()
print(f"ravel: {time.time() - start:.6f}s")

start = time.time()
_ = arr_large.flatten()
print(f"flatten: {time.time() - start:.6f}s")
```

---

## 3. Transposing Arrays

### 3.1 `.T` Attribute

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)  # (2, 3)

# Transpose
transposed = arr.T
print(transposed.shape)  # (3, 2)
print(transposed)
# [[1 4]
#  [2 5]
#  [3 6]]

# Transpose shares memory
print(np.shares_memory(arr, transposed))  # True

# Modify transpose — original modified!
transposed[0, 0] = 999
print(arr)
# [[999   2   3]
#  [  4   5   6]]
```

### 3.2 `transpose()` Function

```python
arr = np.arange(24).reshape(2, 3, 4)
print(arr.shape)  # (2, 3, 4)

# Transpose all axes
transposed = arr.transpose()
print(transposed.shape)  # (4, 3, 2)

# Transpose specific axes
transposed = arr.transpose(2, 0, 1)  # (4, 2, 3)
print(transposed.shape)  # (4, 2, 3)

# Using swapaxes
swapped = arr.swapaxes(0, 2)
print(swapped.shape)  # (4, 3, 2)
```

---

## 4. Advanced Reshaping

### 4.1 `reshape()` with Tuple

```python
arr = np.arange(12)

# Using tuple for shape
arr_2d = arr.reshape((3, 4))
print(arr_2d.shape)  # (3, 4)

# Using list for shape
arr_2d = arr.reshape([4, 3])
print(arr_2d.shape)  # (4, 3)
```

### 4.2 `np.reshape()` Function

```python
arr = np.arange(12)

# Function syntax
arr_2d = np.reshape(arr, (3, 4))
print(arr_2d.shape)  # (3, 4)

# With -1
arr_2d = np.reshape(arr, (4, -1))
print(arr_2d.shape)  # (4, 3)
```

### 4.3 Reshape and Order

```python
arr = np.arange(12).reshape(3, 4)
print(arr)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# C order (row-major, default)
flat_c = arr.reshape(-1, order='C')
print(flat_c)  # [ 0  1  2  3  4  5  6  7  8  9 10 11]

# F order (column-major)
flat_f = arr.reshape(-1, order='F')
print(flat_f)  # [ 0  4  8  1  5  9  2  6 10  3  7 11]

# A order (preserve memory layout)
flat_a = arr.reshape(-1, order='A')
```

---

## 5. View vs Copy in Reshape

### 5.1 When Reshape Returns a View

```python
arr = np.arange(12)

# reshape returns a view when array is contiguous
view = arr.reshape(3, 4)
print(np.shares_memory(arr, view))  # True

# ravel returns a view when possible
view = arr.reshape(3, 4).ravel()
print(np.shares_memory(arr, view))  # True
```

### 5.2 When Reshape Returns a Copy

```python
arr = np.arange(12)

# Non-contiguous array may force copy
arr_nc = arr[::2]  # Non-contiguous
reshaped = arr_nc.reshape(3, 2)
print(np.shares_memory(arr_nc, reshaped))  # May be False

# flatten always returns a copy
copy = arr.reshape(3, 4).flatten()
print(np.shares_memory(arr, copy))  # False
```

---

## 6. Common Reshape Patterns

### 6.1 Adding/Removing Dimensions

```python
# Add dimension
arr = np.array([1, 2, 3])
print(arr.shape)  # (3,)

# Add row dimension
row = arr.reshape(1, -1)
print(row.shape)  # (1, 3)

# Add column dimension
col = arr.reshape(-1, 1)
print(col.shape)  # (3, 1)

# Remove dimension
arr = np.zeros((1, 3, 1, 4))
squeezed = arr.reshape(3, 4)
print(squeezed.shape)  # (3, 4)
```

### 6.2 Swapping Axes

```python
arr = np.zeros((2, 3, 4))

# Transpose
transposed = arr.T
print(transposed.shape)  # (4, 3, 2)

# Swap specific axes
swapped = arr.transpose(1, 0, 2)
print(swapped.shape)  # (3, 2, 4)

# Move axis
moved = np.moveaxis(arr, 0, -1)
print(moved.shape)  # (3, 4, 2)
```

### 6.3 Repeat and Tile

```python
arr = np.array([1, 2, 3])

# Repeat elements
repeated = np.repeat(arr, 3)
print(repeated)  # [1 1 1 2 2 2 3 3 3]

# Tile array
tiled = np.tile(arr, 3)
print(tiled)  # [1 2 3 1 2 3 1 2 3]

# 2D tiling
arr_2d = np.array([[1, 2], [3, 4]])
tiled_2d = np.tile(arr_2d, (2, 3))
print(tiled_2d)
# [[1 2 1 2 1 2]
#  [3 4 3 4 3 4]
#  [1 2 1 2 1 2]
#  [3 4 3 4 3 4]]
```

---

## 7. Common Mistakes to Avoid

### Mistake 1: Reshape with Wrong Total Size
```python
arr = np.arange(12)
# arr.reshape(3, 5)  # ValueError: cannot reshape array of size 12 into shape (3,5)
```

### Mistake 2: Modifying a View Through Reshape
```python
arr = np.arange(12).reshape(3, 4)
view = arr.ravel()
view[0] = 999
print(arr[0, 0])  # 999 — modified!

# Fix: use .copy()
copy = arr.ravel().copy()
copy[0] = 999
print(arr[0, 0])  # 0 — unchanged
```

### Mistake 3: Confusing ravel and flatten
```python
arr = np.array([[1, 2], [3, 4]])

# ravel — may be view
flat_view = arr.ravel()
flat_view[0] = 999
print(arr[0, 0])  # 999 — modified!

# flatten — always copy
arr = np.array([[1, 2], [3, 4]])
flat_copy = arr.flatten()
flat_copy[0] = 999
print(arr[0, 0])  # 1 — unchanged
```

---

## 8. Best Practices

1. **Use `-1`** for automatic dimension calculation
2. **Prefer `ravel()`** for memory efficiency (view when possible)
3. **Use `flatten()`** when you need a guaranteed copy
4. **Check `np.shares_memory()`** if unsure about memory sharing
5. **Use `.T`** for simple 2D transposition
6. **Use `transpose()`** for 3D+ array axis reordering
7. **Validate shape** before reshape: `np.prod(new_shape) == arr.size`

---

## 9. Practice Exercises

### Exercise 1: Basic Reshaping
```python
import numpy as np

arr = np.arange(24)

# a) Reshape to (4, 6)
# b) Reshape to (6, 4)
# c) Reshape to (2, 3, 4)
# d) Reshape to (4, 3, 2)
# e) Reshape to (2, 12) using -1

reshapes = [
    (4, 6),
    (6, 4),
    (2, 3, 4),
    (4, 3, 2),
    (2, -1),
]

for shape in reshapes:
    reshaped = arr.reshape(shape)
    print(f"Shape {shape}: {reshaped.shape}")
```

### Exercise 2: Flatten Comparison
```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Compare ravel and flatten
flat_view = arr.ravel()
flat_copy = arr.flatten()

# Modify both
flat_view[0] = 999
flat_copy[0] = 888

print(f"After modifying ravel: arr[0,0] = {arr[0,0]}")  # 999
print(f"After modifying flatten: flat_copy[0] = {flat_copy[0]}")  # 888
```

### Exercise 3: Transpose
```python
arr = np.arange(24).reshape(2, 3, 4)

# a) Transpose all axes
# b) Transpose axes 0 and 2
# c) Swap axes 1 and 2
# d) Move axis 0 to position 2

print(f"Original: {arr.shape}")
print(f"Transpose all: {arr.T.shape}")
print(f"Transpose 0,2: {arr.transpose(2, 0, 1).shape}")
print(f"Swap 1,2: {arr.swapaxes(1, 2).shape}")
print(f"Move axis: {np.moveaxis(arr, 0, 2).shape}")
```

### Exercise 4: Practical Reshaping
```python
# Reshape image data
# Original: (100, 100, 3) — RGB image
# Target: (10000, 3) — pixels as rows

img = np.random.randint(0, 256, (100, 100, 3))
print(f"Original shape: {img.shape}")

# Reshape to pixels
pixels = img.reshape(-1, 3)
print(f"Pixels shape: {pixels.shape}")

# Reshape back
img_restored = pixels.reshape(100, 100, 3)
print(f"Restored shape: {img_restored.shape}")
```

---

## 10. Summary

| Method | Returns | Memory | Use Case |
|--------|---------|--------|----------|
| `reshape()` | View/Copy | Shared* | Change dimensions |
| `ravel()` | View | Shared* | Flatten (memory efficient) |
| `flatten()` | Copy | Independent | Flatten (safe) |
| `.T` | View | Shared | 2D transpose |
| `transpose()` | View | Shared | N-D transpose |
| `swapaxes()` | View | Shared | Swap two axes |
| `moveaxis()` | View | Shared | Move axis to new position |
| `np.tile()` | Copy | Independent | Repeat array |
| `np.repeat()` | Copy | Independent | Repeat elements |

*May return copy if array is non-contiguous

### Key Takeaways

1. `reshape()` changes shape without changing data
2. Use `-1` for automatic dimension calculation
3. `ravel()` returns view; `flatten()` returns copy
4. `.T` transposes 2D; `transpose()` for 3D+
5. Views share memory — modifications affect original
6. Always validate shape before reshape

---

## 🔗 Next Lecture

→ [10-array-iterating-lecture.md](./10-array-iterating-lecture.md) — Array Iterating
