# NumPy Lecture 11: Array Join

## 🎯 Topic Overview

Joining arrays is the process of combining multiple arrays into one. NumPy provides several functions for concatenation, stacking, and hstacking. This lecture covers `concatenate()`, `stack()`, `hstack()`, `vstack()`, and `dstack()`.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Concatenate arrays along different axes
2. Stack arrays to create new dimensions
3. Use hstack, vstack, dstack for convenience
4. Understand axis requirements for joining
5. Handle shape mismatches in joining
6. Choose the right joining method

---

## 1. Basic Concatenation with `np.concatenate()`

### 1.1 1D Arrays

```python
import numpy as np

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Concatenate 1D arrays
result = np.concatenate([arr1, arr2])
print(result)  # [1 2 3 4 5 6]
```

### 1.2 2D Arrays

```python
arr1 = np.array([[1, 2, 3],
                 [4, 5, 6]])

arr2 = np.array([[7, 8, 9],
                 [10, 11, 12]])

# Concatenate along axis 0 (rows)
result = np.concatenate([arr1, arr2], axis=0)
print(result)
# [[ 1  2  3]
#  [ 4  5  6]
#  [ 7  8  9]
#  [10 11 12]]
print(result.shape)  # (4, 3)

# Concatenate along axis 1 (columns)
result = np.concatenate([arr1, arr2], axis=1)
print(result)
# [[ 1  2  3  7  8  9]
#  [ 4  5  6 10 11 12]]
print(result.shape)  # (2, 6)
```

---

## 2. Stacking Arrays

### 2.1 `np.stack()` — Create New Dimension

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Stack along new axis 0
result = np.stack([arr1, arr2], axis=0)
print(result)
# [[1 2 3]
#  [4 5 6]]
print(result.shape)  # (2, 3)

# Stack along new axis 1
result = np.stack([arr1, arr2], axis=1)
print(result)
# [[1 4]
#  [2 5]
#  [3 6]]
print(result.shape)  # (3, 2)
```

### 2.2 `np.vstack()` — Vertical Stack

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Vertical stack (like concatenate axis=0)
result = np.vstack([arr1, arr2])
print(result)
# [[1 2 3]
#  [4 5 6]]
print(result.shape)  # (2, 3)

# 2D arrays
arr3 = np.array([[1, 2], [3, 4]])
arr4 = np.array([[5, 6], [7, 8]])

result = np.vstack([arr3, arr4])
print(result)
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]
```

### 2.3 `np.hstack()` — Horizontal Stack

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Horizontal stack (like concatenate axis=1 for 2D)
result = np.hstack([arr1, arr2])
print(result)  # [1 2 3 4 5 6]

# 2D arrays
arr3 = np.array([[1, 2], [3, 4]])
arr4 = np.array([[5, 6], [7, 8]])

result = np.hstack([arr3, arr4])
print(result)
# [[1 2 5 6]
#  [3 4 7 8]]
```

### 2.4 `np.dstack()` — Depth Stack

```python
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

# Depth stack (along axis 2)
result = np.dstack([arr1, arr2])
print(result)
# [[[1 5]
#   [2 6]]
#  [[3 7]
#   [4 8]]]
print(result.shape)  # (2, 2, 2)
```

---

## 3. Convenience Functions

### 3.1 `np.row_stack()` — Alias for vstack

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

result = np.row_stack([arr1, arr2])
print(result)
# [[1 2 3]
#  [4 5 6]]
```

### 3.2 `np.column_stack()` — Column-wise Stack

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Column stack (treats 1D as columns)
result = np.column_stack([arr1, arr2])
print(result)
# [[1 4]
#  [2 5]
#  [3 6]]
print(result.shape)  # (3, 2)
```

---

## 4. Axis Requirements

### 4.1 Matching Dimensions

```python
arr1 = np.array([[1, 2], [3, 4]])  # (2, 2)
arr2 = np.array([[5, 6], [7, 8]])  # (2, 2)

# axis=0: concatenate rows (columns must match)
result = np.concatenate([arr1, arr2], axis=0)
print(result.shape)  # (4, 2)

# axis=1: concatenate columns (rows must match)
result = np.concatenate([arr1, arr2], axis=1)
print(result.shape)  # (2, 4)
```

### 4.2 Shape Mismatch Errors

```python
arr1 = np.array([[1, 2], [3, 4]])  # (2, 2)
arr2 = np.array([[5, 6, 7], [8, 9, 10]])  # (2, 3)

# axis=0: columns must match (2 vs 3)
# np.concatenate([arr1, arr2], axis=0)  # ValueError!

# axis=1: rows must match (2 == 2)
result = np.concatenate([arr1, arr2], axis=1)
print(result.shape)  # (2, 5)
```

---

## 5. Common Joining Patterns

### 5.1 Building Arrays Incrementally

```python
# Build array row by row
rows = []
for i in range(5):
    rows.append(np.arange(i*3, (i+1)*3))

result = np.vstack(rows)
print(result)
# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]
#  [ 9 10 11]
#  [12 13 14]]
```

### 5.2 Adding Borders

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# Add row of zeros at top and bottom
border_row = np.zeros((1, 3), dtype=int)
arr_with_borders = np.vstack([border_row, arr, border_row])
print(arr_with_borders)
# [[0 0 0]
#  [1 2 3]
#  [4 5 6]
#  [7 8 9]
#  [0 0 0]]

# Add column of zeros on sides
border_col = np.zeros((5, 1), dtype=int)
arr_with_borders = np.hstack([border_col, arr_with_borders, border_col])
print(arr_with_borders)
# [[0 0 0 0 0]
#  [0 1 2 3 0]
#  [0 4 5 6 0]
#  [0 7 8 9 0]
#  [0 0 0 0 0]]
```

---

## 6. Common Mistakes to Avoid

### Mistake 1: Wrong Axis for Concatenation
```python
arr1 = np.array([[1, 2, 3]])
arr2 = np.array([[4, 5, 6]])

# axis=0: stacks vertically
result = np.concatenate([arr1, arr2], axis=0)
print(result.shape)  # (2, 3)

# axis=1: stacks horizontally
result = np.concatenate([arr1, arr2], axis=1)
print(result.shape)  # (1, 6)
```

### Mistake 2: Shape Mismatch
```python
arr1 = np.array([[1, 2], [3, 4]])  # (2, 2)
arr2 = np.array([[5, 6, 7]])        # (1, 3)

# np.concatenate([arr1, arr2], axis=0)  # ValueError!
# np.concatenate([arr1, arr2], axis=1)  # ValueError!

# Fix: ensure matching dimensions
arr2 = np.array([[5, 6], [7, 8]])  # (2, 2)
result = np.concatenate([arr1, arr2], axis=0)  # OK
```

### Mistake 3: Confusing stack vs concatenate
```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# concatenate: joins existing arrays
result = np.concatenate([arr1, arr2])
print(result.shape)  # (6,)

# stack: creates new dimension
result = np.stack([arr1, arr2])
print(result.shape)  # (2, 3)
```

---

## 7. Best Practices

1. **Use `axis=0`** for vertical stacking (adding rows)
2. **Use `axis=1`** for horizontal stacking (adding columns)
3. **Check shapes** before joining to avoid errors
4. **Use `np.vstack()`** and `np.hstack()`** for convenience
5. **Use `np.stack()`** when you need a new dimension
6. **Pre-allocate arrays** if joining many small arrays
7. **Consider `np.append()`** for single element additions (but it's slow)

---

## 8. Practice Exercises

### Exercise 1: Basic Concatenation
```python
import numpy as np

arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])
arr3 = np.array([[9, 10], [11, 12]])

# a) Concatenate all along axis 0
# b) Concatenate all along axis 1

result_0 = np.concatenate([arr1, arr2, arr3], axis=0)
result_1 = np.concatenate([arr1, arr2, arr3], axis=1)

print("Axis 0:")
print(result_0)
print("\nAxis 1:")
print(result_1)
```

### Exercise 2: Stacking
```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr3 = np.array([7, 8, 9])

# a) Stack vertically (vstack)
# b) Stack horizontally (hstack)
# c) Stack with new axis (stack)

print("vstack:")
print(np.vstack([arr1, arr2, arr3]))

print("\nhstack:")
print(np.hstack([arr1, arr2, arr3]))

print("\nstack axis=0:")
print(np.stack([arr1, arr2, arr3], axis=0))

print("\nstack axis=1:")
print(np.stack([arr1, arr2, arr3], axis=1))
```

### Exercise 3: Building Arrays
```python
# Build a 5x5 identity matrix by stacking
zeros = np.zeros((5, 5), dtype=int)
for i in range(5):
    zeros[i, i] = 1

# Alternative: use np.eye()
identity = np.eye(5, dtype=int)
print(identity)
```

### Exercise 4: Adding Borders
```python
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# Add border of 9s around the array
border = np.full((1, 3), 9, dtype=int)
arr_border = np.vstack([border, arr, border])

border_col = np.full((5, 1), 9, dtype=int)
arr_border = np.hstack([border_col, arr_border, border_col])

print(arr_border)
# [[9 9 9 9 9]
#  [9 1 2 3 9]
#  [9 4 5 6 9]
#  [9 7 8 9 9]
#  [9 9 9 9 9]]
```

---

## 9. Summary

| Function | Description | Axis | Use Case |
|----------|-------------|------|----------|
| `np.concatenate()` | Join along existing axis | 0 or 1 | General joining |
| `np.stack()` | Join along new axis | 0, 1, or 2 | Create new dimension |
| `np.vstack()` | Vertical stack | 0 | Add rows |
| `np.hstack()` | Horizontal stack | 1 | Add columns |
| `np.dstack()` | Depth stack | 2 | 3D stacking |
| `np.row_stack()` | Alias for vstack | 0 | Add rows |
| `np.column_stack()` | Column-wise stack | 1 | Column vectors |

### Key Takeaways

1. `concatenate()` joins arrays along existing axes
2. `stack()` creates a new dimension
3. `vstack()` stacks vertically (axis 0)
4. `hstack()` stacks horizontally (axis 1)
5. `dstack()` stacks along depth (axis 2)
6. All arrays must have matching dimensions for the join axis
7. Use `axis=0` for rows, `axis=1` for columns

---

## 🔗 Next Lecture

→ [12-array-split-lecture.md](./12-array-split-lecture.md) — Array Split
