"""
Array Search
W3Schools: https://www.w3schools.com/python/numpy_array_search.asp

Searching for values and their indices in arrays.
"""

import numpy as np

# ============================================================
# Example 1: where() - Find Indices of Conditions
# Returns indices where condition is True.
# ============================================================

arr = np.array([10, 20, 30, 40, 50, 30, 20, 10])

# Find where value equals 30
indices = np.where(arr == 30)
print("Indices where arr == 30:", indices[0])  # [2 5]
# Output: Indices where arr == 30: [2 5]

# Find where value > 25
indices = np.where(arr > 25)
print("Indices where arr > 25:", indices[0])  # [2 3 4 5]
# Output: Indices where arr > 25: [2 3 4 5]

# Find where value is even
indices = np.where(arr % 2 == 0)
print("Indices of even numbers:", indices[0])  # [0 1 2 3 4 5 6 7]

# Get the actual values
values = arr[np.where(arr > 25)]
print("Values > 25:", values)  # [30 40 50 30]
# Output:
# Indices where arr == 30: [2 5]
# Indices where arr > 25: [2 3 4 5]
# Indices of even numbers: [0 1 2 3 4 5 6 7]
# Values > 25: [30 40 50 30]

# ============================================================
# Example 2: where() with x and y
# Select values from x where True, from y where False.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])

# Replace values: keep if > 4, else replace with 0
result = np.where(arr > 4, arr, 0)
print("\nWhere arr > 4, else 0:", result)  # [0 0 0 0 5 6 7 8]

# Replace with different values
result = np.where(arr % 2 == 0, "even", "odd")
print("Where even/odd:", result)
# Output: ['odd' 'even' 'odd' 'even' 'odd' 'even' 'odd' 'even']

# Replace values based on condition
arr = np.array([10, 25, 30, 45, 50])
result = np.where(arr < 30, arr * 2, arr // 2)
print("Double if < 30, else halve:", result)
# Output: [20 50 15 22 25]

# ============================================================
# Example 3: searchsorted()
# Find indices where elements should be inserted to maintain order.
# ============================================================

arr = np.array([10, 20, 30, 40, 50])

# Find index for value 25
idx = np.searchsorted(arr, 25)
print("\nIndex for 25:", idx)  # 2 (between 20 and 30)

# Find index for value 35
idx = np.searchsorted(arr, 35)
print("Index for 35:", idx)  # 3 (between 30 and 40)

# Find index for value 5
idx = np.searchsorted(arr, 5)
print("Index for 5:", idx)  # 0 (before all elements)

# Find index for value 55
idx = np.searchsorted(arr, 55)
print("Index for 55:", idx)  # 5 (after all elements)

# Right side insertion
idx = np.searchsorted(arr, 30, side='right')
print("Index for 30 (right):", idx)  # 3

idx = np.searchsorted(arr, 30, side='left')
print("Index for 30 (left):", idx)   # 2
# Output:
# Index for 25: 2
# Index for 35: 3
# Index for 5: 0
# Index for 55: 5
# Index for 30 (right): 3
# Index for 30 (left): 2

# ============================================================
# Example 4: argmax() and argmin()
# Find indices of maximum and minimum values.
# ============================================================

arr = np.array([10, 25, 30, 45, 50, 15, 35])

# Find index of maximum
max_idx = np.argmax(arr)
print("\nIndex of max:", max_idx)     # 4
print("Max value:", arr[max_idx])     # 50

# Find index of minimum
min_idx = np.argmin(arr)
print("Index of min:", min_idx)       # 0
print("Min value:", arr[min_idx])     # 10

# For 2D arrays, argmax/argmin flatten by default
arr2d = np.array([[1, 5, 3], [4, 2, 6]])
print("\n2D array:\n", arr2d)
print("Index of max (flattened):", np.argmax(arr2d))  # 5

# Along specific axis
print("Index of max in each row:", np.argmax(arr2d, axis=1))  # [1 2]
print("Index of max in each col:", np.argmax(arr2d, axis=0))  # [1 0 1]
# Output:
# Index of max: 4
# Max value: 50
# Index of min: 0
# Min value: 10
#
# 2D array:
#  [[1 5 3]
#   [4 2 6]]
# Index of max (flattened): 5
# Index of max in each row: [1 2]
# Index of max in each col: [1 0 1]

# ============================================================
# Example 5: nonzero() and Extracting Values
# Find indices of non-zero elements.
# ============================================================

arr = np.array([0, 1, 0, 3, 0, 5, 0, 7])

# Get indices of non-zero elements
indices = np.nonzero(arr)
print("\nNon-zero indices:", indices[0])  # [1 3 5 7]

# Get non-zero values
values = arr[np.nonzero(arr)]
print("Non-zero values:", values)  # [1 3 5 7]

# Using np.extract
mask = arr > 2
extracted = np.extract(mask, arr)
print("Values > 2:", extracted)  # [3 5 7]

# Finding multiple conditions
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
indices = np.where((arr > 3) & (arr < 7))
print("\nIndices where 3 < arr < 7:")
print("  Rows:", indices[0])  # [1 1 1]
print("  Cols:", indices[1])  # [0 1 2]
print("  Values:", arr[indices])  # [4 5 6]
# Output:
# Non-zero indices: [1 3 5 7]
# Non-zero values: [1 3 5 7]
# Values > 2: [3 5 7]
#
# Indices where 3 < arr < 7:
#   Rows: [1 1 1]
#   Cols: [0 1 2]
#   Values: [4 5 6]
