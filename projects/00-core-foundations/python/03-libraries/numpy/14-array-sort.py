"""
Array Sort
W3Schools: https://www.w3schools.com/python/numpy_array_sort.asp

Sorting arrays using various algorithms and parameters.
"""

import numpy as np

# ============================================================
# Example 1: Basic Sorting
# sort() returns a sorted copy without modifying original.
# ============================================================

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print("Original:", arr)

# Sort (returns new sorted array)
sorted_arr = np.sort(arr)
print("Sorted:", sorted_arr)   # [1 1 2 3 4 5 6 9]
print("Original:", arr)        # [3 1 4 1 5 9 2 6] (unchanged)

# Sort in place with .sort()
arr_copy = arr.copy()
arr_copy.sort()
print("In-place sorted:", arr_copy)
# Output:
# Original: [3 1 4 1 5 9 2 6]
# Sorted: [1 1 2 3 4 5 6 9]
# Original: [3 1 4 1 5 9 2 6]
# In-place sorted: [1 1 2 3 4 5 6 9]

# ============================================================
# Example 2: Sorting 2D Arrays
# Sort along specific axes.
# ============================================================

arr = np.array([[3, 1, 2], [6, 4, 5]])
print("\nOriginal:\n", arr)

# Sort each row (axis=1, default)
sorted_rows = np.sort(arr, axis=1)
print("\nSorted rows (axis=1):\n", sorted_rows)
# Output:
# Sorted rows (axis=1):
#  [[1 2 3]
#   [4 5 6]]

# Sort each column (axis=0)
sorted_cols = np.sort(arr, axis=0)
print("\nSorted columns (axis=0):\n", sorted_cols)
# Output:
# Sorted columns (axis=0):
#  [[3 1 2]
#   [6 4 5]]

# Sort all elements (flatten first)
sorted_all = np.sort(arr, axis=None)
print("\nSorted all elements:", sorted_all)
# Output: [1 2 3 4 5 6]

# ============================================================
# Example 3: Sort Order (Ascending/Descending)
# Reverse sorted array for descending order.
# ============================================================

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# Ascending (default)
asc = np.sort(arr)
print("\nAscending:", asc)

# Descending - sort then flip
desc = np.sort(arr)[::-1]
print("Descending:", desc)

# Or use the negation trick for descending on numeric arrays
arr_nums = np.array([3, 1, 4, 1, 5, 9, 2, 6])
desc_neg = -np.sort(-arr_nums)
print("Descending via neg:", desc_neg)

# For string arrays
arr_str = np.array(["banana", "apple", "cherry", "date"])
print("\nSorted strings:", np.sort(arr_str))
# Output:
# Ascending: [1 1 2 3 4 5 6 9]
# Descending: [9 6 5 4 3 2 1 1]

# ============================================================
# Example 4: Sorting Algorithms
# Different sort algorithms with different performance.
# ============================================================

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])

# Quick sort (default) - O(n log n) average
print("\nQuicksort:", np.sort(arr, kind='quicksort'))

# Merge sort - O(n log n), stable
print("Mergesort:", np.sort(arr, kind='mergesort'))

# Heap sort - O(n log n), not stable
print("Heapsort:", np.sort(arr, kind='heapsort'))

# Stable sort preserves order of equal elements
arr2 = np.array([('Alice', 25), ('Bob', 20), ('Charlie', 25)],
                dtype=[('name', 'U10'), ('age', int)])
# Sort by age (stable)
sorted_by_age = np.sort(arr2, order='age')
print("\nStable sort by age:", sorted_by_age)
# Output: [('Bob', 20) ('Alice', 25) ('Charlie', 25)]

# ============================================================
# Example 5: argsort and lexsort
# Find indices that would sort the array.
# ============================================================

arr = np.array([30, 10, 50, 20, 40])

# argsort returns indices that would sort the array
sort_indices = np.argsort(arr)
print("\nOriginal:", arr)
print("argsort:", sort_indices)    # [1 3 0 4 2]
print("Sorted by indices:", arr[sort_indices])  # [10 20 30 40 50]

# Use argsort for fancy indexing
print("Using argsort:", arr[sort_indices])

# lexsort - sort by multiple keys
names = np.array(['Charlie', 'Alice', 'Bob', 'Alice'])
ages = np.array([25, 30, 20, 25])

# Sort by age, then by name
sorted_idx = np.lexsort((names, ages))
print("\nLexsort (age, then name):")
for i in sorted_idx:
    print(f"  {names[i]}, age {ages[i]}")
# Output:
# Original: [30 10 50 20 40]
# argsort: [1 3 0 4 2]
# Sorted by indices: [10 20 30 40 50]
#
# Lexsort (age, then name):
#   Bob, age 20
#   Alice, age 25
#   Charlie, age 25
#   Alice, age 30
