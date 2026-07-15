"""
Array Join
W3Schools: https://www.w3schools.com/python/numpy_array_join.asp

Joining arrays together using concatenation and stacking.
"""

import numpy as np

# ============================================================
# Example 1: Concatenate 1D Arrays
# Join arrays along an existing axis.
# ============================================================

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Concatenate along axis 0 (default)
arr_concat = np.concatenate((arr1, arr2))
print("Concatenate 1D:", arr_concat)  # [1 2 3 4 5 6]

# Same as using np.hstack
arr_hstack = np.hstack((arr1, arr2))
print("hstack 1D:", arr_hstack)  # [1 2 3 4 5 6]

# Using np.append (creates new array)
arr_append = np.append(arr1, arr2)
print("append:", arr_append)  # [1 2 3 4 5 6]
# Output:
# Concatenate 1D: [1 2 3 4 5 6]
# hstack 1D: [1 2 3 4 5 6]
# append: [1 2 3 4 5 6]

# ============================================================
# Example 2: Concatenate 2D Arrays
# Join arrays along rows or columns.
# ============================================================

arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

# Concatenate along rows (axis=0) - stack vertically
arr_v = np.concatenate((arr1, arr2), axis=0)
print("Vertical concat (axis=0):\n", arr_v)
# Output:
# Vertical concat (axis=0):
#  [[1 2]
#   [3 4]
#   [5 6]
#   [7 8]]

# Concatenate along columns (axis=1) - stack horizontally
arr_h = np.concatenate((arr1, arr2), axis=1)
print("\nHorizontal concat (axis=1):\n", arr_h)
# Output:
# Horizontal concat (axis=1):
#  [[1 2 5 6]
#   [3 4 7 8]]

# Using hstack and vstack
print("\nvstack:\n", np.vstack((arr1, arr2)))  # Same as axis=0
print("\nhstack:\n", np.hstack((arr1, arr2)))  # Same as axis=1
# Output:
# vstack:
#  [[1 2]
#   [3 4]
#   [5 6]
#   [7 8]]
#
# hstack:
#  [[1 2 5 6]
#   [3 4 7 8]]

# ============================================================
# Example 3: Stack Arrays
# Stack arrays along a new axis.
# ============================================================

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Stack along new axis 0
arr_stack0 = np.stack((arr1, arr2), axis=0)
print("Stack axis=0:\n", arr_stack0)
print("Shape:", arr_stack0.shape)  # (2, 3)
# Output:
# Stack axis=0:
#  [[1 2 3]
#   [4 5 6]]
# Shape: (2, 3)

# Stack along new axis 1
arr_stack1 = np.stack((arr1, arr2), axis=1)
print("\nStack axis=1:\n", arr_stack1)
print("Shape:", arr_stack1.shape)  # (3, 2)
# Output:
# Stack axis=1:
#  [[1 4]
#   [2 5]
#   [3 6]]
# Shape: (3, 2)

# Stack along new axis 2 (for 2D arrays)
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])
arr_stack2 = np.stack((arr1, arr2), axis=2)
print("\nStack axis=2:\n", arr_stack2)
print("Shape:", arr_stack2.shape)  # (2, 2, 2)

# ============================================================
# Example 4: Column Stack and Row Stack
# Convenience functions for 2D stacking.
# ============================================================

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Column stack - stack as columns
arr_cstack = np.column_stack((arr1, arr2))
print("Column stack:\n", arr_cstack)
print("Shape:", arr_cstack.shape)  # (3, 2)
# Output:
# Column stack:
#  [[1 4]
#   [2 5]
#   [3 6]]
# Shape: (3, 2)

# Row stack - stack as rows
arr_rstack = np.row_stack((arr1, arr2))
print("\nRow stack:\n", arr_rstack)
print("Shape:", arr_rstack.shape)  # (2, 3)
# Output:
# Row stack:
#  [[1 2 3]
#   [4 5 6]]
# Shape: (2, 3)

# With 2D arrays
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

print("\nColumn stack 2D:\n", np.column_stack((arr1, arr2)))
print("\nRow stack 2D:\n", np.row_stack((arr1, arr2)))
# Output:
# Column stack 2D:
#  [[1 2 5 6]
#   [3 4 7 8]]
#
# Row stack 2D:
#  [[1 2]
#   [3 4]
#   [5 6]
#   [7 8]]

# ============================================================
# Example 5: Concatenate with More Than Two Arrays
# Join multiple arrays at once.
# ============================================================

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr3 = np.array([7, 8, 9])

# Concatenate three arrays
arr_all = np.concatenate((arr1, arr2, arr3))
print("Three arrays:", arr_all)  # [1 2 3 4 5 6 7 8 9]

# Stack three arrays
arr_stacked = np.stack((arr1, arr2, arr3))
print("\nStacked:\n", arr_stacked)
print("Shape:", arr_stacked.shape)  # (3, 3)

# With 2D arrays
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])
arr3 = np.array([[9, 10], [11, 12]])

arr_v = np.vstack((arr1, arr2, arr3))
print("\nVstack 3 arrays:\n", arr_v)
print("Shape:", arr_v.shape)  # (6, 2)

arr_h = np.hstack((arr1, arr2, arr3))
print("\nHstack 3 arrays:\n", arr_h)
print("Shape:", arr_h.shape)  # (2, 6)
# Output:
# Three arrays: [1 2 3 4 5 6 7 8 9]
#
# Stacked:
#  [[1 2 3]
#   [4 5 6]
#   [7 8 9]]
# Shape: (3, 3)
#
# Vstack 3 arrays:
#  [[ 1  2]
#   [ 3  4]
#   [ 5  6]
#   [ 7  8]
#   [ 9 10]
#   [11 12]]
# Shape: (6, 2)
#
# Hstack 3 arrays:
#  [[ 1  2  5  6  9 10]
#   [ 3  4  7  8 11 12]]
# Shape: (2, 6)
