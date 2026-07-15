# NumPy Lecture 09: Array Reshape — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| reshape | Change array shape | `arr.reshape(3, 4)` |
| ravel | Flatten to 1D (view) | `arr.ravel()` |
| flatten | Flatten to 1D (copy) | `arr.flatten()` |
| transpose | Swap axes | `arr.T`, `arr.transpose()` |
| swapaxes | Swap two axes | `arr.swapaxes(0, 1)` |
| moveaxis | Move axis to position | `np.moveaxis(arr, 0, 2)` |
| -1 | Auto-calculate dimension | `arr.reshape(3, -1)` |
| order | Memory layout (C/F/A) | `arr.reshape(-1, order='C')` |
| tile | Repeat array | `np.tile(arr, 3)` |
| repeat | Repeat elements | `np.repeat(arr, 3)` |
| squeeze | Remove size-1 dims | `np.squeeze(arr)` |
| newaxis | Insert new dimension | `arr[:, np.newaxis]` |
| contiguous | Adjacent memory | `arr.flags['C_CONTIGUOUS']` |
| view | Shared memory array | `arr.ravel()` (usually) |
| copy | Independent memory | `arr.flatten()` (always) |

---

## Alphabetical Glossary

### A

#### Auto-calculate Dimension
Use `-1` in reshape to let NumPy compute one dimension.

```python
import numpy as np

arr = np.arange(12)

# Let NumPy calculate columns
arr_3x4 = arr.reshape(3, -1)
print(arr_3x4.shape)  # (3, 4)

# Let NumPy calculate rows
arr_4x3 = arr.reshape(-1, 3)
print(arr_4x3.shape)  # (4, 3)

# 3D with auto-calculation
arr_3d = arr.reshape(2, -1, 2)
print(arr_3d.shape)  # (2, 3, 2)
```

**Related:** reshape, shape

---

### C

#### Contiguous
Memory layout where elements are stored in adjacent locations.

```python
arr = np.arange(12).reshape(3, 4)
print(arr.flags['C_CONTIGUOUS'])  # True

# Non-contiguous slice
arr_nc = arr[::2]
print(arr_nc.flags['C_CONTIGUOUS'])  # False
```

**Related:** view, reshape, strides

---

#### Copy
An array with independent memory.

```python
arr = np.array([[1, 2], [3, 4]])

# flatten always returns copy
copy = arr.flatten()
print(np.shares_memory(arr, copy))  # False
```

**Related:** view, flatten, ravel

---

### F

#### Flatten
Return a 1D copy of the array (always returns copy).

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

flat = arr.flatten()
print(flat.shape)  # (6,)
print(flat)        # [1 2 3 4 5 6]

# Always a copy
print(np.shares_memory(arr, flat))  # False

# Modify copy — original unchanged
flat[0] = 999
print(arr[0, 0])  # 1
```

**Related:** ravel, copy, reshape

---

### M

#### Moveaxis
Move an array axis to a new position.

```python
arr = np.zeros((2, 3, 4))
print(arr.shape)  # (2, 3, 4)

# Move axis 0 to position 2
moved = np.moveaxis(arr, 0, 2)
print(moved.shape)  # (3, 4, 2)

# Move multiple axes
moved = np.moveaxis(arr, [0, 1], [2, 0])
print(moved.shape)  # (3, 4, 2)
```

**Related:** transpose, swapaxes

---

### O

#### Order
Memory layout for reshape: 'C' (row-major), 'F' (column-major), 'A' (preserve).

```python
arr = np.arange(12).reshape(3, 4)

# C order (row-major, default)
flat_c = arr.reshape(-1, order='C')
print(flat_c)  # [ 0  1  2  3  4  5  6  7  8  9 10 11]

# F order (column-major)
flat_f = arr.reshape(-1, order='F')
print(flat_f)  # [ 0  4  8  1  5  9  2  6 10  3  7 11]
```

**Related:** contiguous, memory layout

---

### R

#### Ravel
Flatten array to 1D (returns view when possible).

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# ravel returns view
flat = arr.ravel()
print(np.shares_memory(arr, flat))  # True

# Modify view — original modified
flat[0] = 999
print(arr[0, 0])  # 999
```

**Related:** flatten, view, reshape

---

#### Repeat
Repeat elements of an array.

```python
arr = np.array([1, 2, 3])

# Repeat each element 3 times
repeated = np.repeat(arr, 3)
print(repeated)  # [1 1 1 2 2 2 3 3 3]

# Repeat along axis
arr_2d = np.array([[1, 2], [3, 4]])
repeated = np.repeat(arr_2d, 2, axis=0)
print(repeated)
# [[1 2]
#  [1 2]
#  [3 4]
#  [3 4]]
```

**Related:** tile, reshape

---

#### Reshape
Change the shape of an array without changing data.

```python
arr = np.arange(12)

# Basic reshape
arr_2d = arr.reshape(3, 4)
print(arr_2d.shape)  # (3, 4)

# With -1
arr_2d = arr.reshape(4, -1)
print(arr_2d.shape)  # (4, 3)

# 3D reshape
arr_3d = arr.reshape(2, 3, 2)
print(arr_3d.shape)  # (2, 3, 2)

# Returns view when possible
print(np.shares_memory(arr, arr_2d))  # True
```

**Related:** ravel, flatten, shape, -1

---

### S

#### Shape
Tuple of array dimensions.

```python
arr = np.zeros((3, 4))
print(arr.shape)  # (3, 4)
print(arr.ndim)   # 2
print(arr.size)   # 12
```

**Related:** reshape, ndim, size

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

#### Swapaxes
Swap two axes of an array.

```python
arr = np.zeros((2, 3, 4))
print(arr.shape)  # (2, 3, 4)

# Swap axes 0 and 1
swapped = arr.swapaxes(0, 1)
print(swapped.shape)  # (3, 2, 4)

# Swap axes 1 and 2
swapped = arr.swapaxes(1, 2)
print(swapped.shape)  # (2, 4, 3)
```

**Related:** transpose, moveaxis

---

### T

#### Tile
Repeat an array a number of times.

```python
arr = np.array([1, 2, 3])

# Tile 3 times
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

**Related:** repeat, reshape

---

#### Transpose
Reverse or permute axes of an array.

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.shape)  # (2, 3)

# .T attribute
transposed = arr.T
print(transposed.shape)  # (3, 2)

# transpose() function
transposed = arr.transpose()
print(transposed.shape)  # (3, 2)

# 3D transpose
arr_3d = np.zeros((2, 3, 4))
transposed = arr_3d.transpose(2, 0, 1)
print(transposed.shape)  # (4, 2, 3)
```

**Related:** swapaxes, moveaxis, .T

---

### V

#### View
A new array object that shares memory with the original.

```python
arr = np.arange(12)

# reshape returns view when possible
view = arr.reshape(3, 4)
print(np.shares_memory(arr, view))  # True

# ravel returns view when possible
view = arr.reshape(3, 4).ravel()
print(np.shares_memory(arr, view))  # True

# Modify view — original modified
view[0] = 999
print(arr[0])  # 999
```

**Related:** copy, shares_memory, base

---

## Reshape Methods Comparison

| Method | Returns | Shares Memory | Use Case |
|--------|---------|---------------|----------|
| `reshape()` | View | Yes* | Change dimensions |
| `ravel()` | View | Yes* | Flatten (memory efficient) |
| `flatten()` | Copy | No | Flatten (safe) |
| `.T` | View | Yes | 2D transpose |
| `transpose()` | View | Yes | N-D transpose |
| `swapaxes()` | View | Yes | Swap two axes |
| `moveaxis()` | View | Yes | Move axis position |
| `np.tile()` | Copy | No | Repeat array |
| `np.repeat()` | Copy | No | Repeat elements |
| `np.squeeze()` | View | Yes | Remove size-1 dims |

*May return copy if array is non-contiguous
