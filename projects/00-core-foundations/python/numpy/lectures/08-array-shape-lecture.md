# NumPy Lecture 08: Array Shape

## 🎯 Topic Overview

The shape of an array defines its dimensions — the number of elements along each axis. Understanding shape is fundamental to array operations, broadcasting, and debugging. This lecture covers shape inspection, manipulation, and common shape-related patterns.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Inspect array shape using `.shape`, `.ndim`, `.size`
2. Understand the relationship between shape and dimensions
3. Work with 0D, 1D, 2D, and 3D arrays
4. Identify and fix shape mismatches
5. Use shape for broadcasting
6. Understand shape in the context of linear algebra

---

## 1. Array Shape Basics

### 1.1 Shape Attribute

```python
import numpy as np

# 0D array (scalar)
scalar = np.array(42)
print(scalar.shape)  # ()
print(scalar.ndim)   # 0

# 1D array (vector)
arr_1d = np.array([1, 2, 3, 4, 5])
print(arr_1d.shape)  # (5,)
print(arr_1d.ndim)   # 1

# 2D array (matrix)
arr_2d = np.array([[1, 2, 3],
                   [4, 5, 6]])
print(arr_2d.shape)  # (2, 3) — 2 rows, 3 columns
print(arr_2d.ndim)   # 2

# 3D array (tensor)
arr_3d = np.array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]]])
print(arr_3d.shape)  # (2, 2, 2) — 2 blocks, 2 rows, 2 columns
print(arr_3d.ndim)   # 3
```

### 1.2 Shape Components

```python
arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

print(f"Shape: {arr.shape}")        # (3, 4)
print(f"Rows (axis 0): {arr.shape[0]}")   # 3
print(f"Columns (axis 1): {arr.shape[1]}") # 4
print(f"Ndim: {arr.ndim}")          # 2
print(f"Size: {arr.size}")          # 12
print(f"Itemsize: {arr.itemsize}")  # 8
print(f"Nbytes: {arr.nbytes}")      # 96
```

---

## 2. Dimensional Patterns

### 2.1 0D Arrays (Scalars)

```python
scalar = np.array(42)
print(scalar.shape)  # ()
print(scalar.ndim)   # 0
print(scalar.size)   # 1

# Scalar operations
print(scalar + 10)   # 52
print(scalar * 2)    # 84
```

### 2.2 1D Arrays (Vectors)

```python
vector = np.array([1, 2, 3, 4, 5])
print(vector.shape)  # (5,)
print(vector.ndim)   # 1
print(vector.size)   # 5

# Row vector vs column vector
row = vector.reshape(1, -1)    # (1, 5)
col = vector.reshape(-1, 1)    # (5, 1)
print(f"Row: {row.shape}")     # (1, 5)
print(f"Col: {col.shape}")     # (5, 1)
```

### 2.3 2D Arrays (Matrices)

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
print(matrix.shape)  # (3, 3)
print(matrix.ndim)   # 2

# Common matrix shapes
print(np.zeros((3, 4)).shape)   # (3, 4) — 3×4 matrix
print(np.ones((5,)).shape)      # (5,) — 1D array (NOT a row vector!)
print(np.eye(3).shape)          # (3, 3) — identity matrix
```

### 2.4 3D Arrays (Tensors)

```python
tensor = np.random.rand(2, 3, 4)
print(tensor.shape)  # (2, 3, 4)
print(tensor.ndim)   # 3

# Common 3D shapes
# Image: (height, width, channels)
img = np.zeros((100, 200, 3))
print(img.shape)     # (100, 200, 3)

# Batch of images: (batch, height, width, channels)
batch = np.zeros((32, 100, 200, 3))
print(batch.shape)   # (32, 100, 200, 3)
```

---

## 3. Shape Inspection Tools

### 3.1 Complete Shape Information

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# All shape-related attributes
print(f"shape:    {arr.shape}")      # (2, 3)
print(f"ndim:     {arr.ndim}")       # 2
print(f"size:     {arr.size}")       # 6
print(f"itemsize: {arr.itemsize}")   # 8 bytes
print(f"nbytes:   {arr.nbytes}")     # 48 bytes
print(f"dtype:    {arr.dtype}")      # int64
print(f"strides:  {arr.strides}")    # (24, 8) bytes

# Total elements
print(f"Total elements: {np.prod(arr.shape)}")  # 6
```

### 3.2 Shape Validation

```python
def validate_shape(arr, expected_shape):
    """Validate array shape matches expected."""
    if arr.shape != expected_shape:
        raise ValueError(
            f"Expected shape {expected_shape}, got {arr.shape}"
        )
    return True

# Usage
arr = np.zeros((3, 4))
validate_shape(arr, (3, 4))  # OK
# validate_shape(arr, (4, 3))  # ValueError!
```

---

## 4. Shape and Broadcasting

### 4.1 Broadcasting Rules

```python
# Rule 1: Arrays with different ndim — prepend 1s to smaller shape
a = np.array([1, 2, 3])          # shape (3,)
b = np.array([[1], [2], [3]])    # shape (3, 1)

# Broadcasting: (3,) → (1, 3) → (3, 3)
#               (3, 1) → (3, 3)
c = a + b
print(c.shape)  # (3, 3)
print(c)
# [[2 3 4]
#  [3 4 5]
#  [4 5 6]]
```

### 4.2 Shape Compatibility

```python
# Broadcasting compatible
a = np.zeros((3, 4))
b = np.zeros((4,))        # Broadcasts to (3, 4)
c = a + b

a = np.zeros((3, 4))
b = np.zeros((3, 1))      # Broadcasts to (3, 4)
c = a + b

# Broadcasting incompatible
a = np.zeros((3, 4))
b = np.zeros((3, 2))      # Cannot broadcast!
# a + b  # ValueError: operands could not be broadcast together
```

---

## 5. Common Shape Patterns

### 5.1 Adding Dimensions

```python
arr = np.array([1, 2, 3, 4, 5])
print(arr.shape)  # (5,)

# Add new axis at position 1 (column vector)
col = arr[:, np.newaxis]
print(col.shape)  # (5, 1)

# Add new axis at position 0 (row vector)
row = arr[np.newaxis, :]
print(row.shape)  # (1, 5)

# Using reshape
col = arr.reshape(-1, 1)
row = arr.reshape(1, -1)
```

### 5.2 Removing Dimensions

```python
arr = np.array([[[1, 2, 3]]])
print(arr.shape)  # (1, 1, 3)

# Remove size-1 dimensions
squeezed = np.squeeze(arr)
print(squeezed.shape)  # (3,)

# Remove specific axis
arr_4d = np.zeros((1, 2, 1, 3))
squeezed = np.squeeze(arr_4d, axis=0)  # Remove axis 0
print(squeezed.shape)  # (2, 1, 3)
```

### 5.3 Swapping Axes

```python
arr = np.zeros((2, 3, 4))
print(arr.shape)  # (2, 3, 4)

# Transpose
transposed = arr.T
print(transposed.shape)  # (4, 3, 2)

# Specific axis swap
swapped = np.swapaxes(arr, 0, 2)
print(swapped.shape)  # (4, 3, 2)

# Move axis
moved = np.moveaxis(arr, 0, -1)
print(moved.shape)  # (3, 4, 2)
```

---

## 6. Shape and Linear Algebra

### 6.1 Matrix Operations

```python
# Matrix multiplication shape rules
A = np.zeros((3, 4))  # 3×4 matrix
B = np.zeros((4, 2))  # 4×2 matrix

# A @ B → (3, 2) matrix
C = A @ B
print(C.shape)  # (3, 2)

# Inner dimensions must match!
A = np.zeros((3, 4))
B = np.zeros((5, 2))
# A @ B  # ValueError: matmul: Input operand 1 has a mismatch
```

### 6.2 Dot Product

```python
# 1D dot product
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.dot(a, b).shape)  # () — scalar

# 2D dot product
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(np.dot(a, b).shape)  # (2, 2)
```

---

## 7. Common Mistakes to Avoid

### Mistake 1: Forgetting Shape When Indexing
```python
arr = np.array([1, 2, 3, 4, 5])
# arr[0, 0]  # IndexError: too many indices for array

# 1D array — single index
print(arr[0])  # 1

# 2D array — two indices needed
matrix = np.array([[1, 2], [3, 4]])
print(matrix[0, 0])  # 1
```

### Mistake 2: Shape Mismatch in Operations
```python
a = np.array([1, 2, 3])      # (3,)
b = np.array([1, 2, 3, 4])   # (4,)
# a + b  # ValueError: operands could not be broadcast together
```

### Mistake 3: Wrong Shape for Multiplication
```python
A = np.zeros((3, 4))
B = np.zeros((3, 4))
# A @ B  # ValueError: inner dimensions must match

# Fix: transpose B
B_T = B.T  # (4, 3)
C = A @ B_T  # (3, 3) — works!
```

### Mistake 4: Confusing Row and Column Vectors
```python
arr = np.array([1, 2, 3])
print(arr.shape)  # (3,) — 1D array, NOT a row vector!

# For true row/column vectors:
row = arr.reshape(1, -1)  # (1, 3)
col = arr.reshape(-1, 1)  # (3, 1)
```

---

## 8. Best Practices

1. **Always check `arr.shape`** before operations
2. **Use `reshape(-1, 1)`** for column vectors
3. **Use `reshape(1, -1)`** for row vectors
4. **Use `np.newaxis`** for dimension expansion
5. **Use `np.squeeze()`** to remove size-1 dimensions
6. **Check broadcasting compatibility** before operations
7. **Remember: 1D arrays are NOT row or column vectors**

---

## 9. Practice Exercises

### Exercise 1: Shape Inspection
```python
import numpy as np

# Create arrays and print shape information
# a) Array of zeros with shape (3, 4, 5)
# b) Identity matrix
# c) Array of ones with shape (2, 3, 4, 5)

arr_a = np.zeros((3, 4, 5))
arr_b = np.eye(3)
arr_c = np.ones((2, 3, 4, 5))

for name, arr in [("a", arr_a), ("b", arr_b), ("c", arr_c)]:
    print(f"Array {name}: shape={arr.shape}, ndim={arr.ndim}, size={arr.size}")
```

### Exercise 2: Shape Manipulation
```python
arr = np.arange(24)

# a) Reshape to (4, 6)
# b) Reshape to (2, 3, 4)
# c) Reshape to (2, 12) — 2D with 2 rows
# d) Reshape to (24, 1) — column vector
# e) Reshape to (1, 24) — row vector

reshapes = [
    (4, 6),
    (2, 3, 4),
    (2, 12),
    (24, 1),
    (1, 24),
]

for shape in reshapes:
    reshaped = arr.reshape(shape)
    print(f"Shape {shape}: ndim={reshaped.ndim}")
```

### Exercise 3: Broadcasting
```python
# Predict the output shape of these operations
a = np.zeros((3, 4))
b = np.zeros((4,))
c = np.zeros((3, 1))
d = np.zeros((2, 3, 4))
e = np.zeros((4, 5))

# a) a + b → shape?
# b) a + c → shape?
# c) d + a → shape?
# d) a + e → shape?

shapes = [
    ("a + b", a + b),
    ("a + c", a + c),
    ("d + a", d + a),
]

for op, result in shapes:
    print(f"{op}: {result.shape}")

# e) a + e → ValueError (incompatible)
```

### Exercise 4: Dimension Manipulation
```python
arr = np.array([1, 2, 3, 4, 5])

# a) Add new axis at position 0 (row vector)
# b) Add new axis at position 1 (column vector)
# c) From (1, 5) to (5,)
# d) From (5, 1) to (5,)

row = arr[np.newaxis, :]     # (1, 5)
col = arr[:, np.newaxis]     # (5, 1)

squeezed_row = np.squeeze(row)  # (5,)
squeezed_col = np.squeeze(col)  # (5,)

print(f"Row: {row.shape} → {squeezed_row.shape}")
print(f"Col: {col.shape} → {squeezed_col.shape}")
```

---

## 10. Summary

| Attribute | Description | Example |
|-----------|-------------|---------|
| `.shape` | Tuple of dimensions | `(3, 4)` |
| `.ndim` | Number of dimensions | `2` |
| `.size` | Total elements | `12` |
| `.itemsize` | Bytes per element | `8` |
| `.nbytes` | Total bytes | `96` |
| `.strides` | Bytes per axis step | `(32, 8)` |

### Key Takeaways

1. Shape is a tuple of dimensions: `(rows, columns)` for 2D
2. 0D arrays have shape `()`, 1D have shape `(n,)`, 2D have shape `(m, n)`
3. Use `np.newaxis` or `reshape` to add/remove dimensions
4. Broadcasting requires compatible shapes
5. Matrix multiplication requires inner dimensions to match
6. 1D arrays are NOT row or column vectors — use `reshape` to be explicit

---

## 🔗 Next Lecture

→ [09-array-reshape-lecture.md](./09-array-reshape-lecture.md) — Array Reshape
