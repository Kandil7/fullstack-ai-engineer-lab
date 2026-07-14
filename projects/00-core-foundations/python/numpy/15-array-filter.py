"""
Array Filter
W3Schools: https://www.w3schools.com/python/numpy_array_filter.asp

Filtering arrays using boolean indexing and conditions.
"""

import numpy as np

# ============================================================
# Example 1: Boolean Filtering
# Use boolean arrays to select elements.
# ============================================================

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# Create boolean mask
mask = arr > 50
print("Boolean mask:", mask)
# Output: [False False False False False  True  True  True  True  True]

# Apply filter
filtered = arr[mask]
print("Filtered (arr > 50):", filtered)  # [60 70 80 90 100]

# Direct boolean indexing
filtered = arr[arr > 50]
print("Direct filter:", filtered)  # [60 70 80 90 100]

# Multiple conditions
filtered = arr[(arr > 30) & (arr < 70)]
print("30 < arr < 70:", filtered)  # [40 50 60]
# Output:
# Boolean mask: [False False False False False  True  True  True  True  True]
# Filtered (arr > 50): [ 60  70  80  90 100]
# Direct filter: [ 60  70  80  90 100]
# 30 < arr < 70: [40 50 60]

# ============================================================
# Example 2: Filter with where()
# More flexible conditional selection.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Get indices where condition is true
indices = np.where(arr % 2 == 0)
print("\nEven number indices:", indices[0])  # [1 3 5 7 9]

# Get actual values
even_values = arr[indices]
print("Even values:", even_values)  # [ 2  4  6  8 10]

# Using np.extract
mask = arr > 5
extracted = np.extract(mask, arr)
print("\nExtracted (> 5):", extracted)  # [ 6  7  8  9 10]

# Extract with complex condition
mask = (arr % 3 == 0) & (arr > 4)
extracted = np.extract(mask, arr)
print("Divisible by 3 and > 4:", extracted)  # [6 9]
# Output:
# Even number indices: [1 3 5 7 9]
# Even values: [ 2  4  6  8 10]
#
# Extracted (> 5): [ 6  7  8  9 10]
# Divisible by 3 and > 4: [6 9]

# ============================================================
# Example 3: Filter 2D Arrays
# Filter rows and columns.
# ============================================================

arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 16]])

print("\nOriginal:\n", arr)

# Filter rows where sum > 20
row_sums = arr.sum(axis=1)
print("Row sums:", row_sums)  # [10 26 42 58]

filtered_rows = arr[row_sums > 20]
print("Rows with sum > 20:\n", filtered_rows)
# Output:
# Rows with sum > 20:
#  [[ 5  6  7  8]
#   [ 9 10 11 12]
#   [13 14 15 16]]

# Filter columns where mean > 8
col_means = arr.mean(axis=0)
print("Column means:", col_means)  # [ 7.  8.  9. 10.]

filtered_cols = arr[:, col_means > 8]
print("Columns with mean > 8:\n", filtered_cols)
# Output:
# Columns with mean > 8:
#  [[ 3  4]
#   [ 7  8]
#   [11 12]
#   [15 16]]

# Filter specific elements
mask = arr > 10
print("Elements > 10:", arr[mask])  # [11 12 13 14 15 16]

# ============================================================
# Example 4: Filter with Fancy Indexing
# Select elements at specific positions.
# ============================================================

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80])

# Select specific indices
indices = [0, 2, 4, 6]
filtered = arr[indices]
print("\nFancy indexing:", filtered)  # [10 30 50 70]

# Select random indices
random_indices = np.random.choice(len(arr), size=4, replace=False)
print("Random indices:", random_indices)
print("Random selection:", arr[random_indices])

# Select with replacement
random_indices = np.random.choice(len(arr), size=5, replace=True)
print("With replacement:", arr[random_indices])

# 2D fancy indexing
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
rows = np.array([0, 2])
cols = np.array([1, 2])
print("\n2D fancy indexing:", arr2d[rows, cols])  # [2 9]
# Output:
# Fancy indexing: [10 30 50 70]

# ============================================================
# Example 5: Filter and Modify
# Combine filtering with assignment.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("\nOriginal:", arr)

# Replace elements meeting condition
arr[arr > 5] = 0
print("After arr>5=0:", arr)  # [1 2 3 4 5 0 0 0 0 0]

# Replace with calculated values
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
arr[arr % 2 == 0] *= -1
print("Negate evens:", arr)  # [ 1 -2  3 -4  5 -6  7 -8  9 -10]

# Conditional replacement
arr = np.array([10, 25, 30, 45, 50])
result = np.where(arr > 30, arr * 2, arr)
print("Double if > 30:", result)  # [10 25 30 90 100]

# Clip values
arr = np.array([1, 5, 10, 15, 20, 25, 30])
clipped = np.clip(arr, 5, 20)
print("Clipped [5,20]:", clipped)  # [ 5  5 10 15 20 20 20]

# Masked array approach
arr = np.array([1, 2, 3, 4, 5])
masked = np.ma.masked_where(arr > 3, arr)
print("Masked:", masked)  # [1 2 3 -- --]
print("Masked data:", masked.compressed())  # [1 2 3]
