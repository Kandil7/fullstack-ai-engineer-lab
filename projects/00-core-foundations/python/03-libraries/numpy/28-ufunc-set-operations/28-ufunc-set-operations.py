"""
Ufunc Set Operations
W3Schools: https://www.w3schools.com/python/numpy_ufunc_set_operations.asp

Set operations on arrays (unique, intersection, union, etc.).
"""

import numpy as np

# ============================================================
# Example 1: unique()
# Find unique elements in an array.
# ============================================================

arr = np.array([1, 2, 3, 2, 4, 3, 5, 1, 6, 5])
print("Original:", arr)

# Get unique values
unique_vals = np.unique(arr)
print("Unique:", unique_vals)  # [1 2 3 4 5 6]

# Get unique values and counts
unique_vals, counts = np.unique(arr, return_counts=True)
print("\nUnique with counts:")
for val, count in zip(unique_vals, counts):
    print(f"  {val}: {count}")

# Get unique with indices
unique_vals, indices = np.unique(arr, return_index=True)
print("\nUnique with first indices:", dict(zip(unique_vals, indices)))

# 2D unique
arr2d = np.array([[1, 2, 1], [2, 3, 2], [1, 2, 3]])
unique_2d = np.unique(arr2d)
print("\n2D unique:", unique_2d)

# Unique along axis
unique_rows = np.unique(arr2d, axis=0)
print("Unique rows:\n", unique_rows)
# Output:
# Unique: [1 2 3 4 5 6]
#
# Unique with counts:
#   1: 2
#   2: 2
#   3: 2
#   4: 1
#   5: 2
#   6: 1

# ============================================================
# Example 2: intersection1d()
# Find common elements between arrays.
# ============================================================

arr1 = np.array([1, 2, 3, 4, 5, 6])
arr2 = np.array([4, 5, 6, 7, 8, 9])

# Basic intersection
common = np.intersect1d(arr1, arr2)
print("\nIntersection:", common)  # [4 5 6]

# Intersection with indices
common, idx1, idx2 = np.intersect1d(arr1, arr2, return_indices=True)
print("Common values:", common)
print("Indices in arr1:", idx1)  # [3 4 5]
print("Indices in arr2:", idx2)  # [0 1 2]

# Multiple arrays (intersect1d takes exactly two arrays; chain for more)
arr3 = np.array([5, 6, 7, 10])
common_all = np.intersect1d(np.intersect1d(arr1, arr2), arr3)
print("\nCommon in all 3:", common_all)  # [5 6]

# Practical: find common customers
customers_a = np.array(["Alice", "Bob", "Charlie", "David"])
customers_b = np.array(["Bob", "David", "Eve", "Frank"])
common_customers = np.intersect1d(customers_a, customers_b)
print(f"\nCommon customers: {common_customers}")
# Output:
# Intersection: [4 5 6]

# ============================================================
# Example 3: union1d()
# Combine elements from arrays (like SQL UNION).
# ============================================================

arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([3, 4, 5, 6])

# Basic union (removes duplicates)
union = np.union1d(arr1, arr2)
print("\nUnion:", union)  # [1 2 3 4 5 6]

# Practical: merge unique categories
cat_a = np.array(["electronics", "clothing", "food"])
cat_b = np.array(["clothing", "furniture", "electronics", "toys"])
all_categories = np.union1d(cat_a, cat_b)
print(f"All categories: {all_categories}")

# Union of multiple arrays
arr3 = np.array([6, 7, 8])
union_all = np.union1d(np.union1d(arr1, arr2), arr3)
print(f"Union of 3 arrays: {union_all}")
# Output:
# Union: [1 2 3 4 5 6]

# ============================================================
# Example 4: setdiff1d() and setxor1d()
# Difference and symmetric difference.
# ============================================================

arr1 = np.array([1, 2, 3, 4, 5, 6])
arr2 = np.array([4, 5, 6, 7, 8, 9])

# setdiff1d: elements in arr1 but NOT in arr2
diff = np.setdiff1d(arr1, arr2)
print("\nDifference (arr1 - arr2):", diff)  # [1 2 3]

# Reverse difference
diff_rev = np.setdiff1d(arr2, arr1)
print("Difference (arr2 - arr1):", diff_rev)  # [7 8 9]

# setxor1d: elements in either but NOT in both
sym_diff = np.setxor1d(arr1, arr2)
print("Symmetric difference:", sym_diff)  # [1 2 3 7 8 9]

# Practical: find unique to each group
team_a = np.array(["Alice", "Bob", "Charlie"])
team_b = np.array(["Bob", "David", "Charlie"])
only_a = np.setdiff1d(team_a, team_b)
only_b = np.setdiff1d(team_b, team_a)
print(f"\nOnly in team A: {only_a}")
print(f"Only in team B: {only_b}")
print(f"Unique to each: {np.setxor1d(team_a, team_b)}")
# Output:
# Difference (arr1 - arr2): [1 2 3]
# Symmetric difference: [1 2 3 7 8 9]

# ============================================================
# Example 5: in1d() and isin()
# Check membership of elements.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
test_values = np.array([2, 5, 11])

# in1d (deprecated) has been replaced by isin; use isin instead
mask = np.isin(arr, test_values)
print("\nin1d (now isin):", mask)  # [False True False False True False False False False False]
print("Matches:", arr[mask])  # [2 5]

# isin (modern version)
mask = np.isin(arr, test_values)
print("\nisin:", mask)

# 2D membership
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
mask = np.isin(arr2d, [2, 5, 8])
print("\n2D isin:\n", mask)
print("Matching values:", arr2d[mask])  # [2 5 8]

# Practical: filter by category
categories = np.array(["A", "B", "C", "A", "D", "B", "E"])
valid_categories = np.array(["A", "B", "C"])
mask = np.isin(categories, valid_categories)
print(f"\nCategories: {categories}")
print(f"Valid: {categories[mask]}")

# Count occurrences of test values
arr = np.array([1, 2, 3, 2, 4, 2, 5, 3])
test = np.array([2, 3])
counts = np.array([np.sum(arr == val) for val in test])
print(f"\nTest values: {test}")
print(f"Counts: {counts}")
# Output:
# isin: [False  True False False  True False False False False False]
# Matches: [2 5]
