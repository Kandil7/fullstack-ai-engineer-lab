# NumPy Lecture 08: Array Shape — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| shape | Tuple of array dimensions | `arr.shape` |
| ndim | Number of dimensions | `arr.ndim` |
| size | Total number of elements | `arr.size` |
| itemsize | Bytes per element | `arr.itemsize` |
| nbytes | Total bytes in array | `arr.nbytes` |
| strides | Bytes per axis step | `arr.strides` |
| axis | Dimension of array | `axis=0`, `axis=1` |
| Scalar | 0D array | `np.array(42)` |
| Vector | 1D array | `np.array([1, 2, 3])` |
| Matrix | 2D array | `np.array([[1, 2], [3, 4]])` |
| Tensor | 3D+ array | `np.zeros((2, 3, 4))` |
| Row vector | 2D array (1, n) | `arr.reshape(1, -1)` |
| Column vector | 2D array (n, 1) | `arr.reshape(-1, 1)` |
| Broadcasting | Shape alignment rules | `arr + scalar` |
| squeeze | Remove size-1 dims | `np.squeeze(arr)` |
| newaxis | Insert new dimension | `arr[:, np.newaxis]` |

---

## Alphabetical Glossary

### A

#### Axis
A dimension of an array. For 2D arrays: axis 0 = rows, axis 1 = columns.

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)     # (2, 3)
print(arr.shape[0])  # 2 (rows = axis 0)
print(arr.shape[1])  # 3 (columns = axis 1)

# Operations along axis
print(arr.sum(axis=0))  # [5 7 9] — sum along rows
print(arr.sum(axis=1))  # [6 15] — sum along columns
```

**Related:** shape, ndim, broadcasting

---

### B

#### Broadcasting
Automatic shape alignment for array operations.

```python
# Scalar broadcasting
arr = np.array([1, 2, 3])
result = arr + 5  # (3,) + () → (3,)

# 1D broadcasting
a = np.array([[1, 2, 3], [4, 5, 6]])  # (2, 3)
b = np.array([10, 20, 30])             # (3,)
c = a + b  # (2, 3) + (3,) → (2, 3)

# Rules: align from right, prepend 1s to smaller
a = np.zeros((3, 4))
b = np.zeros((4,))       # → (1, 4) → (3, 4)
c = a + b
```

**Related:** shape, axis, compatible shapes

---

### C

#### Column Vector
A 2D array with shape (n, 1).

```python
arr = np.array([1, 2, 3, 4, 5])
col = arr.reshape(-1, 1)
print(col.shape)  # (5, 1)
print(col)
# [[1]
#  [2]
#  [3]
#  [4]
#  [5]]

# Using np.newaxis
col = arr[:, np.newaxis]
print(col.shape)  # (5, 1)
```

**Related:** row vector, reshape, newaxis

---

#### Compatible Shapes
Array shapes that can be broadcast together.

```python
# Compatible
a = np.zeros((3, 4))
b = np.zeros((4,))        # Broadcasts to (3, 4)
c = np.zeros((3, 1))      # Broadcasts to (3, 4)
d = np.zeros((2, 3, 4))   # Broadcasts to (2, 3, 4)

# Incompatible
a = np.zeros((3, 4))
b = np.zeros((3, 2))      # Cannot broadcast!
```

**Related:** broadcasting, shape

---

### M

#### Matrix
A 2D array.

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])
print(matrix.shape)  # (2, 3)
print(matrix.ndim)   # 2

# Square matrix
square = np.eye(3)
print(square.shape)  # (3, 3)
```

**Related:** vector, tensor, shape

---

### N

#### Newaxis
Insert a new axis into an array.

```python
arr = np.array([1, 2, 3, 4, 5])
print(arr.shape)  # (5,)

# Add axis at position 0
row = arr[np.newaxis, :]
print(row.shape)  # (1, 5)

# Add axis at position 1
col = arr[:, np.newaxis]
print(col.shape)  # (5, 1)

# For broadcasting
a = np.array([1, 2, 3])      # (3,)
b = np.array([10, 20])       # (2,)
c = a[:, np.newaxis] + b     # (3, 2)
```

**Related:** reshape, dimension expansion

---

#### Ndim
The number of dimensions (axes) of an array.

```python
arr_0d = np.array(42)
arr_1d = np.array([1, 2, 3])
arr_2d = np.array([[1, 2], [3, 4]])
arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])

print(arr_0d.ndim)  # 0
print(arr_1d.ndim)  # 1
print(arr_2d.ndim)  # 2
print(arr_3d.ndim)  # 3
```

**Related:** shape, size, ndim

---

### R

#### Reshape
Change the shape of an array without changing its data.

```python
arr = np.arange(12)

# Reshape to 2D
arr_2d = arr.reshape(3, 4)
print(arr_2d.shape)  # (3, 4)

# Reshape to 3D
arr_3d = arr.reshape(2, 3, 2)
print(arr_3d.shape)  # (2, 3, 2)

# Use -1 for automatic dimension
arr_2d = arr.reshape(-1, 4)  # (3, 4)
arr_2d = arr.reshape(3, -1)  # (3, 4)
```

**Related:** shape, newaxis, squeeze

---

#### Row Vector
A 2D array with shape (1, n).

```python
arr = np.array([1, 2, 3, 4, 5])
row = arr.reshape(1, -1)
print(row.shape)  # (1, 5)
print(row)        # [[1 2 3 4 5]]

# Using np.newaxis
row = arr[np.newaxis, :]
print(row.shape)  # (1, 5)
```

**Related:** column vector, reshape, newaxis

---

### S

#### Scalar
A 0-dimensional array.

```python
scalar = np.array(42)
print(scalar.shape)  # ()
print(scalar.ndim)   # 0
print(scalar.size)   # 1

# Scalar operations
print(scalar + 10)   # 52
print(scalar * 2)    # 84
```

**Related:** vector, matrix

---

#### Shape
Tuple of array dimensions.

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)  # (2, 3)

# Shape components
print(arr.shape[0])  # 2 (rows)
print(arr.shape[1])  # 3 (columns)

# Total elements
print(np.prod(arr.shape))  # 6
```

**Related:** ndim, size, strides

---

#### Size
Total number of elements in the array.

```python
arr = np.zeros((3, 4))
print(arr.size)  # 12

# Size equals product of shape
print(np.prod(arr.shape))  # 12
```

**Related:** shape, ndim, nbytes

---

#### Squeeze
Remove size-1 dimensions from an array.

```python
arr = np.array([[[1, 2, 3]]])
print(arr.shape)  # (1, 1, 3)

squeezed = np.squeeze(arr)
print(squeezed.shape)  # (3,)

# Remove specific axis
arr_4d = np.zeros((1, 2, 1, 3))
squeezed = np.squeeze(arr_4d, axis=0)
print(squeezed.shape)  # (2, 1, 3)
```

**Related:** newaxis, reshape

---

### T

#### Tensor
A 3D or higher-dimensional array.

```python
tensor = np.zeros((2, 3, 4))
print(tensor.shape)  # (2, 3, 4)
print(tensor.ndim)   # 3

# Common tensor shapes
# Image batch: (batch, height, width, channels)
batch = np.zeros((32, 100, 200, 3))
print(batch.shape)  # (32, 100, 200, 3)
```

**Related:** matrix, vector, shape

---

## Shape Patterns

```python
import numpy as np

# Common patterns
print(f"Scalar: {np.array(42).shape}")           # ()
print(f"Vector: {np.array([1, 2, 3]).shape}")    # (3,)
print(f"Matrix: {np.zeros((3, 4)).shape}")       # (3, 4)
print(f"Tensor: {np.zeros((2, 3, 4)).shape}")    # (2, 3, 4)

# Adding dimensions
arr = np.array([1, 2, 3])
print(f"Row:    {arr.reshape(1, -1).shape}")     # (1, 3)
print(f"Col:    {arr.reshape(-1, 1).shape}")     # (3, 1)

# Removing dimensions
arr = np.zeros((1, 3, 1, 4))
print(f"Squeeze: {np.squeeze(arr).shape}")        # (3, 4)
```
