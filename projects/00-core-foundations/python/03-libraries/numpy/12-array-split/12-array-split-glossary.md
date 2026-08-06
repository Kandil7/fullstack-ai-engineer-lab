# NumPy Lecture 12: Array Split — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| split | Split into equal parts or at indices | `np.split(arr, 3)` |
| array_split | Split (allows unequal parts) | `np.array_split(arr, 3)` |
| vsplit | Vertical split (axis 0) | `np.vsplit(arr, 2)` |
| hsplit | Horizontal split (axis 1) | `np.hsplit(arr, 2)` |
| dsplit | Depth split (axis 2) | `np.dsplit(arr, 2)` |
| split indices | Points to split at | `np.split(arr, [3, 7])` |
| Equal split | All parts same size | `np.split(arr, 3)` |
| Unequal split | Parts different sizes | `np.array_split(arr, 3)` |
| Axis | Dimension for splitting | `axis=0`, `axis=1` |
| Subarray | Result of split | `parts[0]` |
| Rejoin | Combine split parts | `np.concatenate(parts)` |

---

## Alphabetical Glossary

### A

#### Array_split
Split array into multiple subarrays (allows unequal division).

```python
import numpy as np

arr = np.arange(10)

# Unequal split into 3 parts
parts = np.array_split(arr, 3)
print([len(p) for p in parts])  # [4, 3, 3]

for i, part in enumerate(parts):
    print(f"Part {i}: {part}")
# Part 0: [0 1 2 3]
# Part 1: [4 5 6]
# Part 2: [7 8 9]
```

**Note:** Unlike `split()`, `array_split()` handles uneven division.

**Related:** split, vsplit, hsplit

---

### D

#### Dsplit
Split array along the third axis (depth).

```python
arr = np.arange(24).reshape(2, 3, 4)
print(arr.shape)  # (2, 3, 4)

# Split into 2 parts along depth
parts = np.dsplit(arr, 2)
print(parts[0].shape)  # (2, 3, 2)
print(parts[1].shape)  # (2, 3, 2)
```

**Related:** vsplit, hsplit, axis

---

### E

#### Equal Split
Split array into parts of equal size.

```python
arr = np.arange(12)

# Equal split into 3 parts
parts = np.split(arr, 3)
print([len(p) for p in parts])  # [4, 4, 4]

for part in parts:
    print(part)
# [0 1 2 3]
# [4 5 6 7]
# [8 9 10 11]
```

**Related:** split, array_split

---

### H

#### Hsplit
Split array horizontally (along axis 1).

```python
arr = np.arange(12).reshape(3, 4)
print(arr)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Split into 2 horizontal parts
parts = np.hsplit(arr, 2)
print(parts[0])
# [[0 1]
#  [4 5]
#  [8 9]]
print(parts[1])
# [[ 2  3]
#  [ 6  7]
#  [10 11]]

# Split at specific column index
parts = np.hsplit(arr, [1, 3])
print([p.shape for p in parts])  # [(3, 1), (3, 2), (3, 1)]
```

**Related:** vsplit, split, axis

---

### S

#### Split
Split array into equal parts or at specific indices.

```python
arr = np.arange(12)

# Equal split
parts = np.split(arr, 3)
print([len(p) for p in parts])  # [4, 4, 4]

# Split at indices
parts = np.split(arr, [3, 7])
print([len(p) for p in parts])  # [3, 4, 5]
```

**Related:** array_split, vsplit, hsplit

---

#### Split Indices
Points where the array is split.

```python
arr = np.arange(10)

# Split at indices 3 and 7
parts = np.split(arr, [3, 7])
print(parts)
# [array([0, 1, 2]),
#  array([3, 4, 5, 6]),
#  array([7, 8, 9])]

# Part 0: arr[0:3]
# Part 1: arr[3:7]
# Part 2: arr[7:]
```

**Related:** split, array_split

---

### U

#### Unequal Split
Split array into parts of different sizes.

```python
arr = np.arange(10)

# Unequal split into 3 parts
parts = np.array_split(arr, 3)
print([len(p) for p in parts])  # [4, 3, 3]

for i, part in enumerate(parts):
    print(f"Part {i}: {part}")
# Part 0: [0 1 2 3]
# Part 1: [4 5 6]
# Part 2: [7 8 9]
```

**Related:** array_split, equal split

---

### V

#### Vsplit
Split array vertically (along axis 0).

```python
arr = np.arange(12).reshape(4, 3)
print(arr)
# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]
#  [ 9 10 11]]

# Split into 2 vertical parts
parts = np.vsplit(arr, 2)
print(parts[0])
# [[0 1 2]
#  [3 4 5]]
print(parts[1])
# [[ 6  7  8]
#  [ 9 10 11]]

# Split at specific row index
parts = np.vsplit(arr, [1, 3])
print([p.shape for p in parts])  # [(1, 3), (2, 3), (1, 3)]
```

**Related:** hsplit, split, axis

---

## Split Methods Comparison

| Method | Axis | Equal Only | Use Case |
|--------|------|------------|----------|
| `np.split()` | any | Yes* | Exact split points |
| `np.array_split()` | any | No | Uneven division |
| `np.vsplit()` | 0 | Yes* | Split rows |
| `np.hsplit()` | 1 | Yes* | Split columns |
| `np.dsplit()` | 2 | Yes* | Split depth |

*Can split at indices for unequal parts

## Split at Indices

```python
arr = np.arange(20)

# Split at specific points
parts = np.split(arr, [5, 10, 15])
print([len(p) for p in parts])  # [5, 5, 5, 5]

# Unequal split at points
parts = np.split(arr, [3, 8, 15])
print([len(p) for p in parts])  # [3, 5, 7, 5]
```
