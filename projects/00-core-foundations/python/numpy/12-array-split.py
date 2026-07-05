"""
Array Split
W3Schools: https://www.w3schools.com/python/numpy_array_split.asp

Splitting arrays into multiple sub-arrays.
"""

import numpy as np

# ============================================================
# Example 1: Split 1D Array
# Split array into equal parts.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Split into 3 equal parts
parts = np.split(arr, 3)
print("Split into 3:")
for i, part in enumerate(parts):
    print(f"  Part {i}: {part}")
# Output:
# Split into 3:
#   Part 0: [1 2 3 4]
#   Part 1: [5 6 7 8]
#   Part 2: [ 9 10]

# Split into 5 parts
parts = np.split(arr, 5)
print("\nSplit into 5:")
for i, part in enumerate(parts):
    print(f"  Part {i}: {part}")
# Output:
# Split into 5:
#   Part 0: [1 2]
#   Part 1: [3 4]
#   Part 2: [5 6]
#   Part 3: [7 8]
#   Part 4: [ 9 10]

# Split at specific indices
parts = np.split(arr, [3, 7])
print("\nSplit at [3, 7]:")
for i, part in enumerate(parts):
    print(f"  Part {i}: {part}")
# Output:
# Split at [3, 7]:
#   Part 0: [1 2 3]
#   Part 1: [4 5 6 7]
#   Part 2: [ 8  9 10]

# ============================================================
# Example 2: Split 2D Array
# Split along rows or columns.
# ============================================================

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
print("\nOriginal:\n", arr)
print("Shape:", arr.shape)  # (4, 3)

# Split into 2 equal parts along rows (axis=0)
parts = np.split(arr, 2, axis=0)
print("\nSplit rows into 2:")
for i, part in enumerate(parts):
    print(f"  Part {i}:\n{part}\n")
# Output:
# Split rows into 2:
#   Part 0:
# [[1 2 3]
#  [4 5 6]]
#
#   Part 1:
# [[ 7  8  9]
#  [10 11 12]]

# Split into 3 equal parts along columns (axis=1)
parts = np.split(arr, 3, axis=1)
print("Split columns into 3:")
for i, part in enumerate(parts):
    print(f"  Part {i}:\n{part}\n")
# Output:
# Split columns into 3:
#   Part 0:
# [[ 1]
#  [ 4]
#  [ 7]
#  [10]]
#
#   Part 1:
# [[ 2]
#  [ 5]
#  [ 8]
#  [11]]
#
#   Part 2:
# [[ 3]
#  [ 6]
#  [ 9]
#  [12]]

# ============================================================
# Example 3: hsplit, vsplit, dsplit
# Convenience functions for different split directions.
# ============================================================

arr = np.arange(16).reshape(4, 4)
print("Original:\n", arr)

# hsplit - horizontal split (along columns)
parts = np.hsplit(arr, 2)
print("\nhsplit into 2:")
for i, part in enumerate(parts):
    print(f"  Part {i}:\n{part}\n")

# vsplit - vertical split (along rows)
parts = np.vsplit(arr, 2)
print("vsplit into 2:")
for i, part in enumerate(parts):
    print(f"  Part {i}:\n{part}\n")
# Output:
# Original:
#  [[ 0  1  2  3]
#   [ 4  5  6  7]
#   [ 8  9 10 11]
#   [12 13 14 15]]
#
# hsplit into 2:
#   Part 0:
# [[ 0  1]
#   [ 4  5]
#   [ 8  9]
#   [12 13]]
#
#   Part 1:
# [[ 2  3]
#   [ 6  7]
#   [10 11]
#   [14 15]]
#
# vsplit into 2:
#   Part 0:
# [[ 0  1  2  3]
#   [ 4  5  6  7]]
#
#   Part 1:
# [[ 8  9 10 11]
#   [12 13 14 15]]

# ============================================================
# Example 4: Split at Specific Indices
# Split at custom positions.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Split at indices [2, 5, 8]
parts = np.split(arr, [2, 5, 8])
print("\nSplit at [2, 5, 8]:")
for i, part in enumerate(parts):
    print(f"  Part {i}: {part}")
# Output:
# Split at [2, 5, 8]:
#   Part 0: [1 2]
#   Part 1: [3 4 5]
#   Part 2: [6 7 8]
#   Part 3: [ 9 10]

# 2D split at specific row indices
arr = np.arange(20).reshape(4, 5)
print("\n2D Array:\n", arr)

parts = np.split(arr, [1, 3], axis=0)
print("\nSplit rows at [1, 3]:")
for i, part in enumerate(parts):
    print(f"  Part {i}:\n{part}\n")

# Split at specific column indices
parts = np.split(arr, [2, 4], axis=1)
print("Split columns at [2, 4]:")
for i, part in enumerate(parts):
    print(f"  Part {i}:\n{part}\n")
# Output:
# 2D Array:
#  [[ 0  1  2  3  4]
#   [ 5  6  7  8  9]
#   [10 11 12 13 14]
#   [15 16 17 18 19]]
#
# Split rows at [1, 3]:
#   Part 0:
# [[0 1 2 3 4]]
#
#   Part 1:
# [[ 5  6  7  8  9]
#  [10 11 12 13 14]]
#
#   Part 2:
# [[15 16 17 18 19]]

# ============================================================
# Example 5: Array Split vs Equal Split
# When split doesn't produce equal parts.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7])

# np.array_split - allows unequal splits
parts = np.array_split(arr, 3)
print("\narray_split into 3:")
for i, part in enumerate(parts):
    print(f"  Part {i}: {part}")
# Output:
# array_split into 3:
#   Part 0: [1 2 3]
#   Part 1: [4 5]
#   Part 2: [6 7]

# Compare with split (would fail with 7 elements)
try:
    np.split(arr, 3)
except ValueError as e:
    print(f"\nsplit(3) fails: {e}")

# Unequal split at specific indices
parts = np.array_split(arr, [2, 5])
print("\narray_split at [2, 5]:")
for i, part in enumerate(parts):
    print(f"  Part {i}: {part}")
# Output:
# array_split at [2, 5]:
#   Part 0: [1 2]
#   Part 1: [3 4 5]
#   Part 2: [6 7]

# 2D array_split
arr = np.arange(20).reshape(4, 5)
parts = np.array_split(arr, 3, axis=0)
print("\n2D array_split into 3 rows:")
for i, part in enumerate(parts):
    print(f"  Part {i} shape: {part.shape}")
    print(f"  Part {i}:\n{part}\n")
