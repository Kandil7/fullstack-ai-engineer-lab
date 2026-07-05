# NumPy Lecture 12: Array Split

## 🎯 Topic Overview

Splitting is the opposite of joining — it divides an array into multiple subarrays. This lecture covers `split()`, `hsplit()`, `vsplit()`, `dsplit()`, and `array_split()`. Understanding splitting is essential for data preprocessing and cross-validation.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Split arrays into equal and unequal parts
2. Use hsplit, vsplit, dsplit for convenience
3. Handle arrays that don't divide evenly
4. Understand axis requirements for splitting
5. Choose the right splitting method

---

## 1. Basic Splitting with `np.split()`

### 1.1 Equal Split

```python
import numpy as np

arr = np.arange(12)
print(arr)  # [ 0  1  2  3  4  5  6  7  8  9 10 11]

# Split into 3 equal parts
parts = np.split(arr, 3)
print(parts)
# [array([0, 1, 2, 3]), array([4, 5, 6, 7]), array([8, 9, 10, 11])]

for i, part in enumerate(parts):
    print(f"Part {i}: {part}")
# Part 0: [0 1 2 3]
# Part 1: [4 5 6 7]
# Part 2: [8 9 10 11]
```

### 1.2 Unequal Split

```python
arr = np.arange(10)
print(arr)  # [0 1 2 3 4 5 6 7 8 9]

# Split at specific indices
parts = np.split(arr, [3, 7])
print(parts)
# [array([0, 1, 2]), array([3, 4, 5, 6]), array([7, 8, 9])]

for i, part in enumerate(parts):
    print(f"Part {i}: {part}")
# Part 0: [0 1 2]
# Part 1: [3 4 5 6]
# Part 2: [7 8 9]
```

---

## 2. `np.array_split()` — Handles Uneven Division

### 2.1 Unequal Parts

```python
arr = np.arange(10)
print(arr)  # [0 1 2 3 4 5 6 7 8 9]

# Split into 3 parts (not equal!)
parts = np.array_split(arr, 3)
print(parts)
# [array([0, 1, 2, 3]), array([4, 5, 6]), array([7, 8, 9])]

for i, part in enumerate(parts):
    print(f"Part {i}: {part}")
# Part 0: [0 1 2 3]
# Part 1: [4 5 6]
# Part 2: [7 8 9]
```

### 2.2 Split vs array_split

```python
arr = np.arange(10)

# split requires equal division
# np.split(arr, 3)  # ValueError: array split does not result in an equal division

# array_split handles unequal division
parts = np.array_split(arr, 3)
print([len(p) for p in parts])  # [4, 3, 3]
```

---

## 3. Convenience Functions

### 3.1 `np.vsplit()` — Vertical Split

```python
arr = np.arange(12).reshape(4, 3)
print(arr)
# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]
#  [ 9 10 11]]

# Split into 2 vertical parts (along axis 0)
parts = np.vsplit(arr, 2)
print(parts[0])
# [[0 1 2]
#  [3 4 5]]
print(parts[1])
# [[ 6  7  8]
#  [ 9 10 11]]
```

### 3.2 `np.hsplit()` — Horizontal Split

```python
arr = np.arange(12).reshape(3, 4)
print(arr)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Split into 2 horizontal parts (along axis 1)
parts = np.hsplit(arr, 2)
print(parts[0])
# [[0 1]
#  [4 5]
#  [8 9]]
print(parts[1])
# [[ 2  3]
#  [ 6  7]
#  [10 11]]
```

### 3.3 `np.dsplit()` — Depth Split

```python
arr = np.arange(24).reshape(2, 3, 4)
print(arr.shape)  # (2, 3, 4)

# Split along depth (axis 2)
parts = np.dsplit(arr, 2)
print(parts[0].shape)  # (2, 3, 2)
print(parts[1].shape)  # (2, 3, 2)
```

---

## 4. Splitting at Specific Indices

### 4.1 Custom Split Points

```python
arr = np.arange(20)
print(arr)  # [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19]

# Split at indices 5 and 10
parts = np.split(arr, [5, 10])
print(parts)
# [array([0, 1, 2, 3, 4]),
#  array([5, 6, 7, 8, 9]),
#  array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])]

for i, part in enumerate(parts):
    print(f"Part {i}: {part}")
```

### 4.2 2D Split at Specific Points

```python
arr = np.arange(12).reshape(3, 4)
print(arr)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Split columns at index 2
parts = np.hsplit(arr, [2])
print(parts[0])
# [[0 1]
#  [4 5]
#  [8 9]]
print(parts[1])
# [[ 2  3]
#  [ 6  7]
#  [10 11]]
```

---

## 5. Common Splitting Patterns

### 5.1 Train/Test Split

```python
from sklearn.model_selection import train_test_split

X = np.arange(100).reshape(50, 2)
y = np.arange(50)

# Or manually
indices = np.random.permutation(50)
train_idx = indices[:40]
test_idx = indices[40:]

X_train = X[train_idx]
X_test = X[test_idx]
y_train = y[train_idx]
y_test = y[test_idx]
```

### 5.2 K-Fold Cross Validation

```python
arr = np.arange(100)
k = 5
folds = np.array_split(arr, k)

for i, fold in enumerate(folds):
    test = fold
    train = np.concatenate([folds[j] for j in range(k) if j != i])
    print(f"Fold {i}: train={len(train)}, test={len(test)}")
```

### 5.3 Splitting by Columns

```python
# Split features and target
data = np.random.rand(100, 5)  # 100 samples, 5 features

X = data[:, :-1]  # Features (first 4 columns)
y = data[:, -1]   # Target (last column)

print(f"X shape: {X.shape}")  # (100, 4)
print(f"y shape: {y.shape}")  # (100,)
```

---

## 6. Common Mistakes to Avoid

### Mistake 1: Using split with Unequal Division
```python
arr = np.arange(10)

# This will error
# np.split(arr, 3)  # ValueError: array split does not result in an equal division

# Use array_split instead
parts = np.array_split(arr, 3)
```

### Mistake 2: Wrong Axis for Splitting
```python
arr = np.arange(12).reshape(3, 4)

# vsplit: splits rows (axis 0)
parts = np.vsplit(arr, 2)
print(parts[0].shape)  # (1, 4) — not what you might expect!

# hsplit: splits columns (axis 1)
parts = np.hsplit(arr, 2)
print(parts[0].shape)  # (3, 2)
```

### Mistake 3: Confusing split indices
```python
arr = np.arange(10)

# Split at index 3 means:
# Part 0: arr[0:3]  (indices 0, 1, 2)
# Part 1: arr[3:]   (indices 3, 4, 5, 6, 7, 8, 9)
parts = np.split(arr, [3])
```

---

## 7. Best Practices

1. **Use `array_split()`** when division isn't equal
2. **Use `split()`** when you need exact split points
3. **Use `vsplit()`** for vertical (row) splitting
4. **Use `hsplit()`** for horizontal (column) splitting
5. **Check part sizes** after splitting to verify
6. **Use `np.concatenate()`** to rejoin split arrays
7. **Use for cross-validation** and data preprocessing

---

## 8. Practice Exercises

### Exercise 1: Basic Splitting
```python
import numpy as np

arr = np.arange(24)

# a) Split into 4 equal parts
# b) Split at indices [6, 12, 18]
# c) Split into 5 parts (unequal)

parts_4 = np.split(arr, 4)
parts_indices = np.split(arr, [6, 12, 18])
parts_5 = np.array_split(arr, 5)

print("4 equal parts:", [len(p) for p in parts_4])
print("Split at indices:", [len(p) for p in parts_indices])
print("5 unequal parts:", [len(p) for p in parts_5])
```

### Exercise 2: 2D Splitting
```python
arr = np.arange(12).reshape(3, 4)
print(arr)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# a) Split vertically into 3 parts
# b) Split horizontally into 2 parts
# c) Split columns at index 1

parts_v = np.vsplit(arr, 3)
parts_h = np.hsplit(arr, 2)
parts_col = np.hsplit(arr, [1])

print("Vertical parts:", [p.shape for p in parts_v])
print("Horizontal parts:", [p.shape for p in parts_h])
print("Column split:", [p.shape for p in parts_col])
```

### Exercise 3: Cross-Validation Split
```python
# Create 5-fold cross-validation splits
data = np.arange(100)
k = 5

# Split data into k folds
folds = np.array_split(data, k)

# For each fold: train on other folds, test on current
for i in range(k):
    test = folds[i]
    train = np.concatenate([folds[j] for j in range(k) if j != i])
    print(f"Fold {i}: train={len(train)}, test={len(test)}")
```

### Exercise 4: Split and Rejoin
```python
arr = np.arange(20)

# Split and rejoin
parts = np.split(arr, [5, 10, 15])
rejoined = np.concatenate(parts)

# Verify
print(np.array_equal(arr, rejoined))  # True
```

---

## 9. Summary

| Function | Description | Axis | Use Case |
|----------|-------------|------|----------|
| `np.split()` | Equal split or at indices | any | Exact split points |
| `np.array_split()` | Unequal split allowed | any | Uneven division |
| `np.vsplit()` | Vertical split | 0 | Split rows |
| `np.hsplit()` | Horizontal split | 1 | Split columns |
| `np.dsplit()` | Depth split | 2 | Split depth |

### Key Takeaways

1. `split()` requires equal division; `array_split()` allows unequal
2. Use split indices `[3, 7]` to split at specific points
3. `vsplit()` splits along axis 0 (rows)
4. `hsplit()` splits along axis 1 (columns)
5. `dsplit()` splits along axis 2 (depth)
6. Rejoin with `np.concatenate()`
7. Essential for train/test splits and cross-validation

---

## 🔗 Next Lecture

→ [13-array-search-lecture.md](./13-array-search-lecture.md) — Array Search
