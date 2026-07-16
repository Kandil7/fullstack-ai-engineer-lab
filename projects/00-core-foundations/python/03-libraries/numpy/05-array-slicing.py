"""
Array Slicing
W3Schools: https://www.w3schools.com/python/numpy_array_slicing.asp

Extracting portions of arrays using slice notation.
"""

import numpy as np

# ============================================================
# Example 1: Basic Slicing (1D)
# Syntax: array[start:stop:step]
# ============================================================

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
print("Array:", arr)

# Slice from index 1 to 5 (stop is exclusive)
print("\narr[1:5]:", arr[1:5])      # [20 30 40 50]
# Output: arr[1:5]: [20 30 40 50]

# Slice from beginning
print("arr[:4]:", arr[:4])          # [10 20 30 40]

# Slice from end
print("arr[6:]:", arr[6:])          # [70 80 90 100]

# Every other element
print("arr[::2]:", arr[::2])        # [10 30 50 70 90]

# Reversed array
print("arr[::-1]:", arr[::-1])      # [100 90 80 70 60 50 40 30 20 10]

# Negative step
print("arr[8:2:-2]:", arr[8:2:-2])  # [90 70 50]
# Output:
# arr[:4]: [10 20 30 40]
# arr[6:]: [70 80 90 100]
# arr[::2]: [10 30 50 70 90]
# arr[::-1]: [100  90  80  70  60  50  40  30  20  10]
# arr[8:2:-2]: [90 70 50]

# ============================================================
# Example 2: 2D Array Slicing
# Slicing rows and columns independently.
# ============================================================

arr2d = np.array([[1, 2, 3, 4, 5],
                   [6, 7, 8, 9, 10],
                   [11, 12, 13, 14, 15],
                   [16, 17, 18, 19, 20]])
print("\n2D Array:\n", arr2d)

# Slice first two rows
print("\nFirst 2 rows:\n", arr2d[:2])
# Output:
# First 2 rows:
#  [[ 1  2  3  4  5]
#   [ 6  7  8  9 10]]

# Slice last two rows
print("Last 2 rows:\n", arr2d[2:])

# Slice specific columns (all rows, columns 1-3)
print("Columns 1-3:\n", arr2d[:, 1:4])
# Output:
# Columns 1-3:
#  [[ 2  3  4]
#   [ 7  8  9]
#   [12 13 14]
#   [17 18 19]]

# First row, all columns
print("First row:", arr2d[0, :])      # [1 2 3 4 5]

# All rows, specific column
print("Second column:", arr2d[:, 1])  # [ 2  7 12 17]

# Specific element slice: rows 1-2, columns 0-2
print("Sub-matrix:\n", arr2d[1:3, 0:3])
# Output:
# Sub-matrix:
#  [[ 6  7  8]
#   [11 12 13]]

# ============================================================
# Example 3: Fancy Indexing (Integer Array Indexing)
# Pass arrays of indices to select elements.
# ============================================================

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80])

# Select specific elements by index array
indices = [0, 2, 4, 6]
print("\nFancy indexing:", arr[indices])  # [10 30 50 70]
# Output: Fancy indexing: [10 30 50 70]

# 2D fancy indexing
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Select rows 0 and 2
print("\nRows 0 and 2:\n", arr2d[[0, 2]])
# Output:
# Rows 0 and 2:
#  [[1 2 3]
#   [7 8 9]]

# Select specific elements: (0,1), (1,2), (2,0)
rows = np.array([0, 1, 2])
cols = np.array([1, 2, 0])
print("Specific elements:", arr2d[rows, cols])  # [2 6 7]
# Output: Specific elements: [2 6 7]

# ============================================================
# Example 4: Boolean Indexing
# Use boolean arrays to filter elements.
# ============================================================

arr = np.array([10, 25, 30, 45, 50, 65, 70])

# Create boolean mask
mask = arr > 30
print("\nBoolean mask:", mask)
# Output: Boolean mask: [False False False  True  True  True  True]

# Apply mask
print("Elements > 30:", arr[mask])  # [45 50 65 70]

# Direct boolean indexing
print("Elements > 30:", arr[arr > 30])  # [45 50 65 70]

# Multiple conditions (use & for AND, | for OR)
print("Elements between 20 and 60:", arr[(arr > 20) & (arr < 60)])
# Output: [25 30 45 50]

# Modify using boolean indexing
arr[arr > 50] = 0
print("After setting > 50 to 0:", arr)
# Output: After setting > 50 to 0: [10 25 30 45 50  0  0]
# ============================================================
# Example 5: Slicing and Assigning
# Modify multiple elements using slicing.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("\nOriginal:", arr)  # [ 1  2  3  4  5  6  7  8  9 10]

# Replace a slice with a scalar
arr[2:5] = 99
print("After arr[2:5]=99:", arr)  # [ 1  2 99 99 99  6  7  8  9 10]

# Replace a slice with an array of same shape
arr[5:8] = [600, 700, 800]
print("After arr[5:8]=[600,700,800]:", arr)
# Output: [  1   2  99  99  99 600 700 800   9  10]

# 2D slice assignment
arr2d = np.zeros((4, 4), dtype=int)
arr2d[1:3, 1:3] = 1
print("\n2D slice assignment:\n", arr2d)
# Output:
# 2D slice assignment:
#  [[0 0 0 0]
#   [0 1 1 0]
#   [0 1 1 0]
#   [0 0 0 0]]

# Replace entire column
arr2d[:, 0] = 5
print("After setting first column to 5:\n", arr2d)
# Output:
# After setting first column to 5:
#  [[5 0 0 0]
#   [5 1 1 0]
#   [5 1 1 0]
#   [5 0 0 0]]
