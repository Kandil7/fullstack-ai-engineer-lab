# NumPy Lecture 05: Array Slicing — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Slice | Range of elements: start:stop:step | `arr[1:4]` |
| Start | Beginning index of slice | `arr[2:]` |
| Stop | Ending index (exclusive) | `arr[:5]` |
| Step | Interval between elements | `arr[::2]` |
| Negative index | Count from end | `arr[-3:]` |
| View | Shared memory array | `arr[1:3]` |
| Copy | Independent memory array | `arr[1:3].copy()` |
| Ellipsis | Shorthand for remaining axes | `arr[..., 0]` |
| np.newaxis | Insert new axis | `arr[:, np.newaxis]` |
| Stride | Step between elements | `arr[::2]` |
| Reverse | Step of -1 | `arr[::-1]` |
| Subarray | Array extracted by slicing | `arr[1:4]` |
| Contiguous | Adjacent memory layout | Default slicing |

---

## Alphabetical Glossary

### C

#### Contiguous
Memory layout where elements are stored in adjacent locations. Slicing may or may not preserve contiguity.

```python
import numpy as np

arr = np.arange(20).reshape(4, 5)

# Contiguous slice
slice1 = arr[0:2]
print(slice1.flags['C_CONTIGUOUS'])  # True

# Non-contiguous slice (every other row)
slice2 = arr[::2]
print(slice2.flags['C_CONTIGUOUS'])  # False (if original was C-contiguous)
```

**Related:** strides, memory layout, view

---

#### Copy
An array that is an independent copy of the original, with its own memory.

```python
arr = np.array([1, 2, 3, 4, 5])

# Explicit copy
copy = arr[1:3].copy()
copy[0] = 99
print(arr)   # [1 2 3 4 5] — unchanged

# Check if copy shares memory
print(np.shares_memory(arr, copy))  # False
```

**Related:** view, shares_memory

---

### E

#### Ellipsis (...)
Shorthand for selecting all remaining axes in a multidimensional array.

```python
arr_3d = np.random.rand(2, 3, 4)

# Select along last axis
print(arr_3d[:, :, 0].shape)  # (2, 3)
print(arr_3d[..., 0].shape)   # (2, 3) — equivalent

# Select along first axis
print(arr_3d[0, :, :].shape)  # (3, 4)
print(arr_3d[0, ...].shape)   # (3, 4) — equivalent

# Select along middle axis
print(arr_3d[:, 0, :].shape)  # (2, 4)
print(arr_3d[:, 0, ...].shape)  # (2, 4) — equivalent
```

**Related:** indexing, newaxis, slice

---

### N

#### Newaxis
Insert a new axis into an array, expanding its dimensions.

```python
arr = np.array([1, 2, 3, 4, 5])
print(arr.shape)  # (5,)

# Add axis at position 1 (column vector)
col = arr[:, np.newaxis]
print(col.shape)  # (5, 1)
print(col)
# [[1]
#  [2]
#  [3]
#  [4]
#  [5]]

# Add axis at position 0 (row vector)
row = arr[np.newaxis, :]
print(row.shape)  # (1, 5)
print(row)        # [[1 2 3 4 5]]

# For broadcasting
a = np.array([1, 2, 3])      # shape (3,)
b = np.array([10, 20])       # shape (2,)
c = a[:, np.newaxis] + b     # shape (3, 2)
print(c)
# [[11 21]
#  [12 22]
#  [13 23]]
```

**Related:** reshape, broadcasting, slice

---

### R

#### Reverse
Reverse the order of elements using step of -1.

```python
arr = np.array([1, 2, 3, 4, 5])

# Reverse entire array
print(arr[::-1])  # [5 4 3 2 1]

# Reverse with step -2
print(arr[::-2])  # [5 3 1]

# 2D reversal
matrix = np.array([[1, 2], [3, 4], [5, 6]])
print(matrix[::-1])      # Reverse rows
print(matrix[:, ::-1])   # Reverse columns
print(matrix[::-1, ::-1])  # Reverse both
```

**Related:** slice, step

---

### S

#### Slice
Select a range of elements from an array.

```python
arr = np.array([10, 20, 30, 40, 50])

# Basic slice
print(arr[1:4])    # [20 30 40]

# Slice with step
print(arr[::2])    # [10 30 50]

# Reverse slice
print(arr[::-1])   # [50 40 30 20 10]

# 2D slice
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix[0:2, 1:3])
# [[2 3]
#  [5 6]]
```

**Related:** start, stop, step, view

---

#### Start
The beginning index of a slice (inclusive).

```python
arr = np.array([10, 20, 30, 40, 50])

print(arr[2:])     # [30 40 50] — from index 2 to end
print(arr[0:3])    # [10 20 30] — from index 0 to 2
```

**Related:** stop, step, slice

---

#### Step
The interval between elements in a slice.

```python
arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

print(arr[::2])    # [10 30 50 70 90] — every 2nd element
print(arr[::3])    # [10 40 70 100] — every 3rd element
print(arr[1:8:2])  # [20 40 60 80] — from 1 to 7, every 2nd
print(arr[::-1])   # [100 90 80 70 60 50 40 30 20 10] — reversed
```

**Related:** start, stop, slice

---

#### Stop
The ending index of a slice (exclusive).

```python
arr = np.array([10, 20, 30, 40, 50])

print(arr[:3])     # [10 20 30] — up to but not including index 3
print(arr[1:4])    # [20 30 40] — from 1 to 3
```

**Related:** start, step, slice

---

#### Strides
The number of bytes to move to the next element along each axis.

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.strides)  # (24, 8) — 24 bytes to next row, 8 to next column

# Sliced array strides
sliced = arr[::2]
print(sliced.strides)  # (48, 8) — step increased
```

**Related:** contiguous, memory layout

---

### V

#### View
A new array object that shares memory with the original array.

```python
arr = np.array([1, 2, 3, 4, 5])

# Slicing creates a view
view = arr[1:3]
view[0] = 99
print(arr)   # [ 1 99  3  4  5] — original modified!

# Check if shares memory
print(np.shares_memory(arr, view))  # True
```

**Related:** copy, shares_memory, contiguous

---

## Slicing Patterns

### Basic Patterns

```python
import numpy as np

arr = np.arange(10)

# All elements
print(arr[:])           # [0 1 2 3 4 5 6 7 8 9]

# From start
print(arr[:5])          # [0 1 2 3 4]

# To end
print(arr[5:])          # [5 6 7 8 9]

# Every other
print(arr[::2])         # [0 2 4 6 8]

# Reversed
print(arr[::-1])        # [9 8 7 6 5 4 3 2 1 0]

# Reversed every other
print(arr[::-2])        # [9 7 5 3 1]
```

### 2D Patterns

```python
matrix = np.arange(20).reshape(4, 5)

# First row
print(matrix[0])

# First column
print(matrix[:, 0])

# Submatrix
print(matrix[1:3, 1:3])

# Every other row and column
print(matrix[::2, ::2])

# Diagonal
print(matrix[np.arange(4), np.arange(4)])
```

### Advanced Patterns

```python
arr_3d = np.random.rand(2, 3, 4)

# Using ellipsis
print(arr_3d[..., 0].shape)   # (2, 3)
print(arr_3d[0, ...].shape)   # (3, 4)

# Using newaxis
arr = np.array([1, 2, 3])
col = arr[:, np.newaxis]  # (3, 1)
row = arr[np.newaxis, :]  # (1, 3)
```
