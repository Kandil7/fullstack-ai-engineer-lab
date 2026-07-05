"""
Random Permutation
W3Schools: https://www.w3schools.com/python/numpy_random_permutation.asp

Shuffling and permuting arrays randomly.
"""

import numpy as np

# ============================================================
# Example 1: shuffle() - Modify in Place
# shuffle() modifies the array directly.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("Original:", arr)

# Shuffle in place
np.random.shuffle(arr)
print("Shuffled:", arr)  # Different order each time

# Shuffle is in place - original is modified
print("Same object:", arr)  # Modified!

# 2D array - shuffles rows only
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
print("\nOriginal 2D:\n", arr2d)

np.random.shuffle(arr2d)
print("Shuffled rows:\n", arr2d)  # Rows are shuffled, columns stay together
# Output:
# Original: [ 1  2  3  4  5  6  7  8  9 10]
# Shuffled: [ 3  7  1 10  5  2  9  4  8  6]
#
# Original 2D:
#  [[ 1  2  3]
#   [ 4  5  6]
#   [ 7  8  9]
#   [10 11 12]]
# Shuffled rows:
#  [[ 7  8  9]
#   [ 1  2  3]
#   [10 11 12]
#   [ 4  5  6]]

# ============================================================
# Example 2: permutation() - Returns New Array
# permutation() returns a new shuffled array.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("\nOriginal:", arr)

# Get permuted copy (original unchanged)
permuted = np.random.permutation(arr)
print("Permuted:", permuted)  # New array
print("Original:", arr)       # Still [1 2 3 4 5 6 7 8 9 10]

# Permutation of 2D - shuffles rows
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
permuted_2d = np.random.permutation(arr2d)
print("\nOriginal 2D:\n", arr2d)
print("Permuted 2D:\n", permuted_2d)
# Output:
# Original: [ 1  2  3  4  5  6  7  8  9 10]
# Permuted: [ 5  9  2  8  1  4 10  3  7  6]
# Original: [ 1  2  3  4  5  6  7  8  9 10]

# ============================================================
# Example 3: permutation() with Integer
# permutation(n) returns a random permutation of range(n).
# ============================================================

# Random permutation of indices
perm = np.random.permutation(10)
print("\nPermutation of 0-9:", perm)  # Random order of 0-9

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
# Output:
# Permutation of 0-9: [3 7 1 9 0 5 2 8 4 6]
# Random indices: [5 2 8 0 3 7 1 9 4 6]
# Shuffled array: [60 30 80 10 40 70 20 90 50 100]

# ============================================================
# Example 4: Random Choice
# Select random elements with or without replacement.
# ============================================================

arr = np.array([10, 20, 30, 40, 50])

# Random choice (single element)
choice = np.random.choice(arr)
print("\nRandom choice:", choice)

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
# Output:
# Random choice: 30
# 10 choices (replace=True): [20 50 20 10 30 50 40 20 10 50]
# 3 choices (replace=False): [40 10 30]

# ============================================================
# Example 5: Practical Shuffling Examples
# Common use cases for permutation and shuffle.
# ============================================================

# Shuffle training data
X = np.arange(100).reshape(20, 5)  # 20 samples, 5 features
y = np.arange(20)                   # 20 labels

# Shuffle together
indices = np.random.permutation(len(y))
X_shuffled = X[indices]
y_shuffled = y[indices]

print("\nOriginal first 5 labels:", y[:5])
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

# Reproducible shuffle
np.random.seed(42)
data = np.arange(10)
np.random.shuffle(data)
print(f"\nSeeded shuffle: {data}")  # Always same result

np.random.seed(42)
data = np.arange(10)
np.random.shuffle(data)
print(f"Seeded shuffle again: {data}")  # Same!
