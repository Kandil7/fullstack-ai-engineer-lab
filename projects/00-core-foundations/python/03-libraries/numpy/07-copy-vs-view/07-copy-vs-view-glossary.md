# NumPy Lecture 07: Copy vs View — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| View | Array sharing memory with original | `arr[1:3]` |
| Copy | Independent array with own memory | `arr[1:3].copy()` |
| shares_memory | Check if arrays share memory | `np.shares_memory(a, b)` |
| base | Reference to parent array | `view.base` |
| Memory sharing | Arrays using same data buffer | `view.base is arr` |
| Contiguous | Adjacent memory layout | `arr.flags['C_CONTIGUOUS']` |
| .copy() | Create explicit copy | `arr.copy()` |
| np.copy() | Create explicit copy | `np.copy(arr)` |
| flatten() | 1D copy of array | `arr.flatten()` |
| ravel() | 1D view (or copy if needed) | `arr.ravel()` |
| reshape | Change shape (view if possible) | `arr.reshape(3, 4)` |
| Transpose | Swap axes (view) | `arr.T` |
| Chained indexing | Multiple indexing operations | `arr[0:2][0:2]` |
| Fancy indexing | Integer array indexing | `arr[[0, 2, 4]]` |
| Boolean indexing | Mask-based selection | `arr[arr > 0]` |

---

## Alphabetical Glossary

### B

#### Base
Reference to the parent array from which a view was created.

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
view = arr[1:3]

print(view.base is arr)   # True — view is derived from arr
print(view.base)          # [1 2 3 4 5] — original array

copy = arr[1:3].copy()
print(copy.base is None)  # True — copy has no parent
```

**Related:** shares_memory, view

---

#### Boolean Indexing
Select elements using a boolean mask (creates a copy).

```python
arr = np.array([10, 20, 30, 40, 50])

# Boolean indexing creates a copy
mask = arr > 30
result = arr[mask]
print(np.shares_memory(arr, result))  # False

# Modify result — original unchanged
result[0] = 999
print(arr)  # [10 20 30 40 50]
```

**Related:** fancy indexing, mask, copy

---

### C

#### Contiguous
Memory layout where elements are stored in adjacent locations.

```python
arr = np.arange(20).reshape(4, 5)

# C-contiguous (row-major)
print(arr.flags['C_CONTIGUOUS'])  # True

# Non-contiguous slice
view = arr[::2, ::2]
print(view.flags['C_CONTIGUOUS'])  # False
```

**Related:** strides, memory layout, view

---

#### Copy
An array with independent memory, not sharing data with the original.

```python
arr = np.array([1, 2, 3, 4, 5])

# Explicit copy
copy = arr[1:3].copy()
print(np.shares_memory(arr, copy))  # False

# Modify copy — original unchanged
copy[0] = 999
print(arr)  # [1 2 3 4 5]
```

**Related:** view, shares_memory, .copy()

---

#### Copy() Method
Create an explicit copy of an array.

```python
arr = np.array([1, 2, 3, 4, 5])

copy = arr.copy()
print(np.shares_memory(arr, copy))  # False

# Copy of slice
copy = arr[1:3].copy()
print(np.shares_memory(arr, copy))  # False
```

**Related:** np.copy(), copy, view

---

### F

#### Fancy Indexing
Indexing using integer arrays (creates a copy).

```python
arr = np.array([10, 20, 30, 40, 50])

# Fancy indexing creates a copy
indices = [0, 2, 4]
result = arr[indices]
print(np.shares_memory(arr, result))  # False

# Modify result — original unchanged
result[0] = 999
print(arr)  # [10 20 30 40 50]
```

**Related:** boolean indexing, copy

---

#### Flatten
Return a 1D copy of the array.

```python
arr = np.array([[1, 2], [3, 4]])

flat = arr.flatten()
print(np.shares_memory(arr, flat))  # False — always returns copy

# Equivalent to arr.reshape(-1).copy()
```

**Related:** ravel, reshape, copy

---

### M

#### Memory Sharing
When two or more arrays use the same underlying data buffer.

```python
arr = np.array([1, 2, 3, 4, 5])

# View shares memory
view = arr[1:3]
print(np.shares_memory(arr, view))  # True

# Copy does not share memory
copy = arr[1:3].copy()
print(np.shares_memory(arr, copy))  # False
```

**Related:** shares_memory, view, base

---

### N

#### Np.copy()
Function to create an explicit copy of an array.

```python
arr = np.array([1, 2, 3, 4, 5])

copy = np.copy(arr[1:3])
print(np.shares_memory(arr, copy))  # False

# Equivalent to arr[1:3].copy()
```

**Related:** .copy(), copy, view

---

### R

#### Ravel
Return a flattened view of the array (or copy if needed).

```python
arr = np.array([[1, 2], [3, 4]])

# ravel returns a view when possible
view = arr.ravel()
print(np.shares_memory(arr, view))  # True

# If array is non-contiguous, ravel returns a copy
arr_noncontig = np.arange(20).reshape(4, 5)[::2]
copy = arr_noncontig.ravel()
print(np.shares_memory(arr_noncontig, copy))  # May be False
```

**Related:** flatten, reshape, view

---

#### Reshape
Change the shape of an array (returns view when possible).

```python
arr = np.arange(12)

# reshape returns a view when possible
view = arr.reshape(3, 4)
print(np.shares_memory(arr, view))  # True

# If reshape needs to copy data
arr_noncontig = np.arange(20)[::2]
copy = arr_noncontig.reshape(5)
print(np.shares_memory(arr_noncontig, copy))  # May be False
```

**Related:** ravel, view, contiguous

---

### S

#### Shares_memory
Check if two arrays share the same memory.

```python
arr = np.array([1, 2, 3, 4, 5])

# View shares memory
view = arr[1:3]
print(np.shares_memory(arr, view))  # True

# Copy does not share memory
copy = arr[1:3].copy()
print(np.shares_memory(arr, copy))  # False

# Fancy indexing creates copy
fancy = arr[[0, 2, 4]]
print(np.shares_memory(arr, fancy))  # False
```

**Related:** memory sharing, view, base

---

### T

#### Transpose
Swap axes of an array (returns view).

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# Transpose returns a view
view = arr.T
print(np.shares_memory(arr, view))  # True

# Modify view — original modified
view[0, 0] = 999
print(arr)  # [[999   2   3]
            #  [  4   5   6]]
```

**Related:** view, reshape

---

### V

#### View
A new array object that shares memory with the original.

```python
arr = np.array([1, 2, 3, 4, 5])

# Slicing creates a view
view = arr[1:3]
print(np.shares_memory(arr, view))  # True

# Modify view — original modified
view[0] = 999
print(arr)  # [ 1 999  3  4  5]

# View attributes
print(view.base is arr)    # True
print(view.shape)          # (2,)
print(view.dtype == arr.dtype)  # True
```

**Related:** base, shares_memory, copy

---

## Operations Summary

| Operation | Returns | Shares Memory | Example |
|-----------|---------|---------------|---------|
| `arr[1:3]` | View | Yes | `view = arr[1:3]` |
| `arr[[0, 2]]` | Copy | No | `copy = arr[[0, 2]]` |
| `arr[arr > 0]` | Copy | No | `copy = arr[arr > 0]` |
| `arr.copy()` | Copy | No | `copy = arr.copy()` |
| `np.copy(arr)` | Copy | No | `copy = np.copy(arr)` |
| `arr.reshape(n)` | View | Yes* | `view = arr.reshape(3)` |
| `arr.T` | View | Yes | `view = arr.T` |
| `arr.ravel()` | View | Yes* | `view = arr.ravel()` |
| `arr.flatten()` | Copy | No | `copy = arr.flatten()` |
| `arr.astype(dtype)` | Copy | No | `copy = arr.astype(float)` |
| `np.where(cond)` | Copy | No | `copy = np.where(arr > 0)` |

*May return copy if array is non-contiguous
