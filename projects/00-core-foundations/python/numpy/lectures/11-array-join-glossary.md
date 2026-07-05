# NumPy Lecture 11: Array Join — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| concatenate | Join along existing axis | `np.concatenate([a, b])` |
| stack | Join along new axis | `np.stack([a, b])` |
| vstack | Vertical stack (axis 0) | `np.vstack([a, b])` |
| hstack | Horizontal stack (axis 1) | `np.hstack([a, b])` |
| dstack | Depth stack (axis 2) | `np.dstack([a, b])` |
| row_stack | Alias for vstack | `np.row_stack([a, b])` |
| column_stack | Column-wise stack | `np.column_stack([a, b])` |
| axis | Dimension for joining | `axis=0`, `axis=1` |
| Join | Combine arrays | `np.concatenate()` |
| Stack | Create new dimension | `np.stack()` |
| Concatenate | Join existing arrays | `np.concatenate()` |
| Split | Opposite of join | `np.split()` |

---

## Alphabetical Glossary

### C

#### Column Stack
Stack 1D arrays as columns of a 2D array.

```python
import numpy as np

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

result = np.column_stack([arr1, arr2])
print(result)
# [[1 4]
#  [2 5]
#  [3 6]]
print(result.shape)  # (3, 2)
```

**Related:** hstack, concatenate, axis

---

#### Concatenate
Join arrays along an existing axis.

```python
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

# Along axis 0 (rows)
result = np.concatenate([arr1, arr2], axis=0)
print(result)
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]

# Along axis 1 (columns)
result = np.concatenate([arr1, arr2], axis=1)
print(result)
# [[1 2 5 6]
#  [3 4 7 8]]
```

**Related:** stack, vstack, hstack

---

### D

#### Dstack
Stack arrays along the third axis (depth).

```python
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

result = np.dstack([arr1, arr2])
print(result)
# [[[1 5]
#   [2 6]]
#  [[3 7]
#   [4 8]]]
print(result.shape)  # (2, 2, 2)
```

**Related:** stack, vstack, hstack

---

### H

#### Hstack
Stack arrays horizontally (along axis 1).

```python
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

result = np.hstack([arr1, arr2])
print(result)
# [[1 2 5 6]
#  [3 4 7 8]]
print(result.shape)  # (2, 4)

# For 1D arrays
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
result = np.hstack([arr1, arr2])
print(result)  # [1 2 3 4 5 6]
```

**Related:** vstack, concatenate, axis

---

### R

#### Row Stack
Alias for vstack — stack arrays vertically.

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

result = np.row_stack([arr1, arr2])
print(result)
# [[1 2 3]
#  [4 5 6]]
```

**Related:** vstack, concatenate

---

### S

#### Stack
Join arrays along a new axis.

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

**Related:** concatenate, vstack, hstack

---

### V

#### Vstack
Stack arrays vertically (along axis 0).

```python
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

result = np.vstack([arr1, arr2])
print(result)
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]
print(result.shape)  # (4, 2)

# For 1D arrays
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
result = np.vstack([arr1, arr2])
print(result)
# [[1 2 3]
#  [4 5 6]]
```

**Related:** hstack, concatenate, axis

---

## Join Methods Comparison

| Method | Axis | Creates New Dim | Use Case |
|--------|------|-----------------|----------|
| `np.concatenate()` | Existing | No | General joining |
| `np.stack()` | New | Yes | New dimension |
| `np.vstack()` | 0 | No | Add rows |
| `np.hstack()` | 1 | No | Add columns |
| `np.dstack()` | 2 | Yes | 3D stacking |
| `np.row_stack()` | 0 | No | Alias for vstack |
| `np.column_stack()` | 1 | No | Column vectors |

## Axis Selection Guide

| Goal | Function | Axis |
|------|----------|------|
| Add rows | `vstack()` | 0 |
| Add columns | `hstack()` | 1 |
| Stack 2D into 3D | `dstack()` | 2 |
| Create new dim | `stack()` | any |
| Join existing dims | `concatenate()` | 0 or 1 |
