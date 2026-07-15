# Lecture 18: Random Permutation and Shuffling in NumPy

## Topic Overview

Random permutation involves rearranging elements in a random order. NumPy provides `shuffle()` and `permutation()` functions for shuffling arrays, and `choice()` for random selection with or without replacement. These operations are essential for data preprocessing in machine learning (train/test splits), games, simulations, and any scenario requiring randomization.

Understanding the difference between in-place modification and returning new arrays is crucial when working with these functions.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `np.random.shuffle()` to shuffle arrays in-place
2. Use `np.random.permutation()` to return a new shuffled array
3. Understand the difference between in-place and copy operations
4. Apply shuffling to 2D arrays (shuffling rows while maintaining row integrity)
5. Use `np.random.choice()` for random selection with/without replacement
6. Create weighted random selections
7. Implement reproducible shuffling with seeds
8. Create random train/test splits for machine learning
9. Apply permutation operations to real-world scenarios
10. Understand when to use each shuffling method

---

## Key Concepts

### 1. shuffle() — Modify In Place

`np.random.shuffle()` modifies the array directly. The original array is changed.

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("Original:", arr)

# Shuffle in place
np.random.shuffle(arr)
print("Shuffled:", arr)  # Different order each time

# 2D array - shuffles rows only
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
print("\nOriginal 2D:\n", arr2d)

np.random.shuffle(arr2d)
print("Shuffled rows:\n", arr2d)
# Rows are shuffled, columns stay together
```

**Key points:**
- Modifies the array in place (no return value)
- For 2D arrays, only rows are shuffled (columns stay together)
- Original data is lost (unless you made a copy first)

### 2. permutation() — Returns New Array

`np.random.permutation()` returns a new shuffled array, leaving the original unchanged.

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("Original:", arr)

# Get permuted copy (original unchanged)
permuted = np.random.permutation(arr)
print("Permuted:", permuted)  # New array
print("Original:", arr)       # Still [1 2 3 4 5 6 7 8 9 10]

# Permutation of 2D - shuffles rows
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
permuted_2d = np.random.permutation(arr2d)
print("\nOriginal 2D:\n", arr2d)
print("Permuted 2D:\n", permuted_2d)
```

**Key points:**
- Returns a new array (original unchanged)
- More memory efficient than copying then shuffling
- For 2D arrays, shuffles rows

### 3. permutation() with Integer

When passed an integer `n`, returns a random permutation of `range(n)`.

```python
import numpy as np

# Random permutation of indices
perm = np.random.permutation(10)
print("Permutation of 0-9:", perm)

# Use for random indexing
arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
indices = np.random.permutation(len(arr))
print("Random indices:", indices)
print("Shuffled array:", arr[indices])

# Create random train/test split indices
n_samples = 100
indices = np.random.permutation(n_samples)
train_size = 80
train_idx = indices[:train_size]
test_idx = indices[train_size:]
print(f"\nTrain size: {len(train_idx)}, Test size: {len(test_idx)}")
```

### 4. Random Choice

`np.random.choice()` selects random elements with or without replacement.

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Random choice (single element)
choice = np.random.choice(arr)
print("Random choice:", choice)

# Multiple choices (with replacement - can repeat)
choices = np.random.choice(arr, size=10, replace=True)
print("10 choices (replace=True):", choices)

# Multiple choices (without replacement - unique)
choices = np.random.choice(arr, size=3, replace=False)
print("3 choices (replace=False):", choices)

# With probabilities
probs = [0.1, 0.1, 0.1, 0.1, 0.6]  # 50 most likely
choices = np.random.choice(arr, size=20, p=probs)
print("Weighted choices:", choices)
print("Counts:", {x: np.sum(choices == x) for x in arr})
```

### 5. Practical Shuffling Examples

```python
import numpy as np

# Shuffle training data
X = np.arange(100).reshape(20, 5)  # 20 samples, 5 features
y = np.arange(20)                   # 20 labels

# Shuffle together
indices = np.random.permutation(len(y))
X_shuffled = X[indices]
y_shuffled = y[indices]

print("Original first 5 labels:", y[:5])
print("Shuffled first 5 labels:", y_shuffled[:5])

# Random train/test split
n = len(y)
split = int(0.8 * n)
X_train, X_test = X_shuffled[:split], X_shuffled[split:]
y_train, y_test = y_shuffled[:split], y_shuffled[split:]

print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")

# Random sample without replacement
data = np.arange(1000)
sample = np.random.choice(data, size=100, replace=False)
print(f"\nRandom sample of 100 from 1000:")
print(f"  Min: {sample.min()}, Max: {sample.max()}")
print(f"  Unique: {len(np.unique(sample))} (should be 100)")
```

---

## Code Examples with Explanations

### Example 1: In-Place vs Copy Shuffling

```python
import numpy as np

# Demonstrate the difference
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([1, 2, 3, 4, 5])

print("Before shuffle:")
print("  arr1:", arr1)
print("  arr2:", arr2)

# shuffle() modifies in place
np.random.shuffle(arr1)

# permutation() returns new array
arr2_permuted = np.random.permutation(arr2)

print("\nAfter shuffle/permutation:")
print("  arr1 (shuffled):", arr1)  # Modified!
print("  arr2 (original):", arr2)  # Unchanged!
print("  arr2_permuted:", arr2_permuted)  # New array

# Verify arr2 unchanged
print("\narr2 unchanged:", np.array_equal(arr2, np.array([1, 2, 3, 4, 5])))
```

### Example 2: Shuffling 2D Arrays

```python
import numpy as np

# Create dataset
X = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              [10, 11, 12]])
y = np.array([0, 1, 0, 1])

print("Original X:\n", X)
print("Original y:", y)

# Shuffle both together
indices = np.random.permutation(len(y))
X_shuffled = X[indices]
y_shuffled = y[indices]

print("\nShuffled X:\n", X_shuffled)
print("Shuffled y:", y_shuffled)

# Verify row integrity
print("\nRow integrity maintained:")
for i, (orig, shuf) in enumerate(zip(X, X_shuffled)):
    # Check if each original row exists in shuffled
    exists = any(np.array_equal(orig, row) for row in X_shuffled)
    print(f"  Row {i} exists: {exists}")
```

### Example 3: Random Train/Test Split

```python
import numpy as np

np.random.seed(42)

# Create sample dataset
n_samples = 1000
X = np.random.randn(n_samples, 10)  # 10 features
y = np.random.randint(0, 2, n_samples)  # Binary labels

print(f"Original dataset: {X.shape[0]} samples")

# Shuffle indices
indices = np.random.permutation(n_samples)

# Split 80/20
train_size = int(0.8 * n_samples)
train_idx = indices[:train_size]
test_idx = indices[train_size:]

X_train, X_test = X[train_idx], X[test_idx]
y_train, y_test = y[train_idx], y[test_idx]

print(f"\nTrain set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Verify no overlap
train_set = set(train_idx)
test_set = set(test_idx)
overlap = train_set.intersection(test_set)
print(f"Overlap: {len(overlap)} (should be 0)")

# Verify labels are shuffled
print(f"\nOriginal label distribution: {np.bincount(y)}")
print(f"Train label distribution: {np.bincount(y_train)}")
print(f"Test label distribution: {np.bincount(y_test)}")
```

### Example 4: Weighted Random Selection

```python
import numpy as np

np.random.seed(42)

# Product categories with different sales volumes
products = np.array(["A", "B", "C", "D", "E"])
sales_weights = np.array([0.4, 0.25, 0.15, 0.12, 0.08])

print("Products and weights:")
for prod, weight in zip(products, sales_weights):
    print(f"  {prod}: {weight:.0%}")

# Simulate 1000 purchases
purchases = np.random.choice(products, size=1000, p=sales_weights)

# Count and compare
unique, counts = np.unique(purchases, return_counts=True)
print("\nSimulated purchases:")
for prod, count in zip(unique, counts):
    actual = count / 1000
    expected = sales_weights[products == prod][0]
    print(f"  {prod}: {count} ({actual:.1%}, expected {expected:.0%})")
```

### Example 5: Reproducible Shuffling

```python
import numpy as np

# Without seed - different each time
arr = np.array([1, 2, 3, 4, 5])
np.random.shuffle(arr)
print("Without seed:", arr)

# With seed - reproducible
np.random.seed(42)
arr = np.array([1, 2, 3, 4, 5])
np.random.shuffle(arr)
print("Seed 42 (first):", arr)

np.random.seed(42)
arr = np.array([1, 2, 3, 4, 5])
np.random.shuffle(arr)
print("Seed 42 (second):", arr)  # Same!

# Using permutation for reproducible shuffling
np.random.seed(42)
arr = np.array([1, 2, 3, 4, 5])
permuted = np.random.permutation(arr)
print("Permutation:", permuted)
```

---

## Common Mistakes to Avoid

### Mistake 1: Confusing shuffle() and permutation()

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# WRONG - Trying to get return value from shuffle()
# result = np.random.shuffle(arr)  # Returns None!

# CORRECT - Use shuffle for in-place modification
np.random.shuffle(arr)
print("Shuffled in-place:", arr)

# Or use permutation to get new array
arr = np.array([1, 2, 3, 4, 5])
permuted = np.random.permutation(arr)
print("Permutation (new):", permuted)
print("Original unchanged:", arr)
```

### Mistake 2: Not Shuffling X and y Together

```python
import numpy as np

X = np.array([[1, 2], [3, 4], [5, 6]])
y = np.array([0, 1, 0])

# WRONG - Shuffling independently
np.random.shuffle(X)
np.random.shuffle(y)  # Labels don't match X anymore!

# CORRECT - Shuffle indices together
indices = np.random.permutation(len(y))
X_shuffled = X[indices]
y_shuffled = y[indices]
```

### Mistake 3: Using replace=True When You Need Unique

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# WRONG - Getting duplicates
selected = np.random.choice(arr, size=10, replace=True)
print("With replacement:", selected)  # May have duplicates!

# CORRECT - No duplicates
selected = np.random.choice(arr, size=5, replace=False)
print("Without replacement:", selected)  # All unique
```

### Mistake 4: Forgetting about Memory

```python
import numpy as np

# For large arrays, this creates a copy
large_arr = np.random.randn(1000000, 100)

# This creates another copy
shuffled = np.random.permutation(large_arr)  # 2x memory!

# Better for memory-critical situations
indices = np.random.permutation(len(large_arr))
shuffled = large_arr[indices]  # Still creates copy, but clearer intent
```

---

## Best Practices

### 1. Always Use Seeds for Reproducibility

```python
import numpy as np

# In scripts and experiments
np.random.seed(42)

# In functions, accept seed parameter
def create_train_test_split(X, y, test_size=0.2, seed=None):
    if seed is not None:
        np.random.seed(seed)
    indices = np.random.permutation(len(y))
    split = int((1 - test_size) * len(y))
    return X[indices[:split]], X[indices[split:]], y[indices[:split]], y[indices[split:]]
```

### 2. Use permutation() When You Need the Original

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# When original is needed
permuted = np.random.permutation(arr)
print("Original:", arr)
print("Permuted:", permuted)
```

### 3. Use shuffle() for In-Place Efficiency

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# When you don't need the original
np.random.shuffle(arr)
print("Shuffled:", arr)
```

### 4. Document Your Random Seed

```python
import numpy as np

# Document the seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Your code here
```

### 5. Consider Using sklearn for ML Splits

```python
# For machine learning, sklearn provides more features
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

---

## Practice Exercises

### Exercise 1: Basic Shuffling

```python
import numpy as np

# TODO: Create array and shuffle in-place
arr = np.arange(10)
print("Original:", arr)
np.random.shuffle(arr)
print("Shuffled:", arr)

# TODO: Create array and get permutation (original unchanged)
arr2 = np.arange(10)
permuted = np.random.permutation(arr2)
print("Original:", arr2)
print("Permuted:", permuted)
```

### Exercise 2: 2D Array Shuffling

```python
import numpy as np

# TODO: Shuffle rows of 2D array
data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9],
                 [10, 11, 12]])

indices = np.random.permutation(len(data))
shuffled = data[indices]
print("Shuffled rows:\n", shuffled)
```

### Exercise 3: Train/Test Split

```python
import numpy as np

# TODO: Create and split dataset
np.random.seed(42)
X = np.random.randn(100, 5)
y = np.random.randint(0, 2, 100)

# TODO: Split 70/30
indices = np.random.permutation(100)
train_size = 70
X_train = X[indices[:train_size]]
X_test = X[indices[train_size:]]
y_train = y[indices[:train_size]]
y_test = y[indices[train_size:]]

print(f"Train: {len(X_train)}, Test: {len(X_test)}")
```

### Exercise 4: Random Selection

```python
import numpy as np

# TODO: Random selection with replacement
choices = np.array(["red", "blue", "green", "yellow"])
selected = np.random.choice(choices, size=10, replace=True)
print("With replacement:", selected)

# TODO: Random selection without replacement
selected_unique = np.random.choice(choices, size=3, replace=False)
print("Without replacement:", selected_unique)

# TODO: Weighted selection
weights = [0.5, 0.2, 0.2, 0.1]
weighted = np.random.choice(choices, size=10, p=weights)
print("Weighted:", weighted)
```

---

## Summary

| Function | Behavior | Use Case |
|----------|----------|----------|
| **shuffle()** | Modifies in-place | When you don't need original |
| **permutation()** | Returns new array | When you need original |
| **permutation(n)** | Returns shuffled indices | Index-based shuffling |
| **choice()** | Random selection | Sampling with/without replacement |

---

## Quick Reference

```python
import numpy as np

# In-place shuffle
np.random.shuffle(arr)

# New shuffled array
permuted = np.random.permutation(arr)

# Shuffled indices
indices = np.random.permutation(len(arr))

# Random selection
selected = np.random.choice(arr, size=n, replace=True/False)

# Weighted selection
selected = np.random.choice(arr, size=n, p=probabilities)

# Reproducible shuffling
np.random.seed(42)
np.random.shuffle(arr)
```

---

**Next Lecture:** [19 - Ufunc Introduction](19-ufunc-intro-lecture.md)
