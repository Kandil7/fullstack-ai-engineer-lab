"""
Array Indexing
W3Schools: https://www.w3schools.com/python/numpy_array_indexing.asp

Accessing and modifying array elements using indexing.
"""

import numpy as np

# ============================================================
# Example 1: Basic Indexing
# Access elements using zero-based integer indices.
# ============================================================

arr = np.array([10, 20, 30, 40, 50])
print("Array:", arr)
print("First element:", arr[0])     # 10
print("Second element:", arr[1])    # 20
print("Last element:", arr[-1])     # 50
print("Second to last:", arr[-2])   # 40
# Output:
# Array: [10 20 30 40 50]
# First element: 10
# Second element: 20
# Last element: 50
# Second to last: 40

# ============================================================
# Example 2: 2D Array Indexing
# Access rows and individual elements in 2D arrays.
# ============================================================

arr2d = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12]])
print("\n2D Array:\n", arr2d)

# Access rows
print("\nFirst row:", arr2d[0])      # [1 2 3 4]
print("Second row:", arr2d[1])      # [5 6 7 8]
print("Last row:", arr2d[-1])       # [ 9 10 11 12]

# Access individual element (row, col)
print("\nElement [0,0]:", arr2d[0, 0])    # 1
print("Element [1,2]:", arr2d[1, 2])     # 7
print("Element [2,3]:", arr2d[2, 3])     # 12
# Output:
# 2D Array:
#  [[ 1  2  3  4]
#   [ 5  6  7  8]
#   [ 9 10 11 12]]
#
# First row: [1 2 3 4]
# Second row: [5 6 7 8]
# Last row: [ 9 10 11 12]
#
# Element [0,0]: 1
# Element [1,2]: 7
# Element [2,3]: 12

# ============================================================
# Example 3: 3D Array Indexing
# Accessing elements in higher-dimensional arrays.
# ============================================================

arr3d = np.array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]],
                   [[9, 10], [11, 12]]])
print("\n3D Array shape:", arr3d.shape)  # (3, 2, 2)

# Access first block
print("Block 0:\n", arr3d[0])
# [[1 2]
#  [3 4]]

# Access element across dimensions
print("\nElement [1, 0, 1]:", arr3d[1, 0, 1])  # 6
print("Element [2, 1, 0]:", arr3d[2, 1, 0])  # 11
# Output:
# 3D Array shape: (3, 2, 2)
# Block 0:
#  [[1 2]
#   [3 4]]
#
# Element [1, 0, 1]: 6
# Element [2, 1, 0]: 11

# ============================================================
# Example 4: Negative Indexing
# Negative indices count from the end.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("\nArray:", arr)
print("Last element:", arr[-1])      # 10
print("3rd from end:", arr[-3])      # 8
print("First element:", arr[-10])    # 1

# 2D negative indexing
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print("\nLast row:", arr2d[-1])       # [4 5 6]
print("Last element:", arr2d[-1, -1]) # 6
# Output:
# Array: [ 1  2  3  4  5  6  7  8  9 10]
# Last element: 10
# 3rd from end: 8
# First element: 1
#
# Last row: [4 5 6]
# Last element: 6

# ============================================================
# Example 5: Modifying Elements with Indexing
# Assign new values using indexing.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])
print("\nOriginal:", arr)  # [1 2 3 4 5]

# Modify single element
arr[0] = 100
print("After arr[0]=100:", arr)  # [100   2   3   4   5]

# Modify with negative index
arr[-1] = 500
print("After arr[-1]=500:", arr)  # [100   2   3   4 500]

# Modify multiple elements at once
arr[1:4] = 999
print("After arr[1:4]=999:", arr)  # [100 999 999 999 500]

# Modify 2D array elements
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
arr2d[0, 0] = 10
arr2d[1, 2] = 60
print("\nModified 2D:\n", arr2d)
# Output:
# Original: [1 2 3 4 5]
# After arr[0]=100: [100   2   3   4   5]
# After arr[-1]=500: [100   2   3   4 500]
# After arr[1:4]=999: [100 999 999 999 500]
#
# Modified 2D:
#  [[10  2  3]
#   [ 4  5 60]]
