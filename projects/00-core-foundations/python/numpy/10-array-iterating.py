"""
Array Iterating
W3Schools: https://www.w3schools.com/python/numpy_array_iterating.asp

Iterating through arrays using loops and NumPy functions.
"""

import numpy as np

# ============================================================
# Example 1: Iterating 1D Arrays
# Basic for loop iteration over arrays.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# Standard for loop
print("1D Array iteration:")
for x in arr:
    print(x, end=" ")
print()
# Output: 1 2 3 4 5

# Using enumerate for index and value
print("\nWith index:")
for i, x in enumerate(arr):
    print(f"arr[{i}] = {x}")
# Output:
# arr[0] = 1
# arr[1] = 2
# arr[2] = 3
# arr[3] = 4
# arr[4] = 5

# Using nditer for element-wise access
print("\nUsing nditer:")
for x in np.nditer(arr):
    print(x, end=" ")
print()
# Output: 1 2 3 4 5

# ============================================================
# Example 2: Iterating 2D Arrays
# Iterating over rows and elements.
# ============================================================

arr2d = np.array([[1, 2, 3], [4, 5, 6]])

# Iterating over rows
print("\nIterating rows:")
for row in arr2d:
    print(row)
# Output:
# [1 2 3]
# [4 5 6]

# Iterating over all elements
print("\nAll elements:")
for x in arr2d:
    for y in x:
        print(y, end=" ")
print()
# Output: 1 2 3 4 5 6

# Using nditer for 2D
print("\nUsing nditer:")
for x in np.nditer(arr2d):
    print(x, end=" ")
print()
# Output: 1 2 3 4 5 6

# With index using ndindex
print("\nUsing ndindex:")
for idx in np.ndindex(arr2d.shape):
    print(f"arr2d{idx} = {arr2d[idx]}")
# Output:
# arr2d(0, 0) = 1
# arr2d(0, 1) = 2
# arr2d(0, 2) = 3
# arr2d(1, 0) = 4
# arr2d(1, 1) = 5
# arr2d(1, 2) = 6

# ============================================================
# Example 3: nditer with Flags
# Control iteration behavior with flags.
# ============================================================

arr = np.array([[1, 2, 3], [4, 5, 6]])

# C-style (row-major) iteration
print("C-style iteration:")
for x in np.nditer(arr, flags=["c_index"]):
    print(f"  {x} at index {x.index}")
# Output:
#   1 at index 0
#   2 at index 1
#   3 at index 2
#   4 at index 3
#   5 at index 4
#   6 at index 5

# F-style (column-major) iteration
print("\nF-style iteration:")
for x in np.nditer(arr, flags=["f_index"]):
    print(f"  {x} at index {x.index}")
# Output:
#   1 at index 0
#   4 at index 1
#   2 at index 2
#   5 at index 3
#   3 at index 4
#   6 at index 5

# With multi_index
print("\nMulti-index iteration:")
for x in np.nditer(arr, flags=["multi_index"]):
    print(f"  {x} at {x.multi_index}")
# Output:
#   1 at (0, 0)
#   2 at (0, 1)
#   3 at (0, 2)
#   4 at (1, 0)
#   5 at (1, 1)
#   6 at (1, 2)

# ============================================================
# Example 4: nditer with Casting
# Control type casting during iteration.
# ============================================================

arr_int = np.array([[1, 2, 3], [4, 5, 6]], dtype=int)
arr_float = np.array([[1.1, 2.2, 3.3], [4.4, 5.5, 6.6]], dtype=float)

# Default: type promotion
print("Default iteration (mixed types):")
for x, y in np.nditer([arr_int, arr_float]):
    print(f"  {x} ({x.dtype}) + {y} ({y.dtype})")

# With casting="same_kind"
print("\nSame_kind casting:")
for x, y in np.nditer([arr_int, arr_float], casting="same_kind"):
    print(f"  {x} + {y}")

# With op_dtypes
print("\nWith op_dtypes (float output):")
for x in np.nditer(arr_int, op_dtypes=["float64"]):
    print(f"  {x} ({x.dtype})", end=" ")
print()
# Output:
# Default iteration (mixed types):
#   1 (int64) + 1.1 (float64)
#   2 (int64) + 2.2 (float64)
#   ...
#
# Same_kind casting:
#   1 + 1.1
#   2 + 2.2
#   ...
#
# With op_dtypes (float output):
#   1.0 (float64) 2.0 (float64) 3.0 (float64) 4.0 (float64) 5.0 (float64) 6.0 (float64)

# ============================================================
# Example 5: Iterating with zip-like Access
# Using ndenumerate for index-element pairs.
# ============================================================

arr = np.array([[10, 20, 30], [40, 50, 60]])

# ndenumerate gives (index, value) pairs
print("\nndenumerate:")
for index, value in np.ndenumerate(arr):
    print(f"  {index}: {value}")
# Output:
#   (0, 0): 10
#   (0, 1): 20
#   (0, 2): 30
#   (1, 0): 40
#   (1, 1): 50
#   (1, 2): 60

# Practical: find all elements > 25
print("\nElements > 25:")
for index, value in np.ndenumerate(arr):
    if value > 25:
        print(f"  arr{index} = {value}")
# Output:
#   arr(0, 2) = 30
#   arr(1, 0) = 40
#   arr(1, 1) = 50
#   arr(1, 2) = 60

# Using np.ndenumerate for 3D
arr3d = np.arange(8).reshape(2, 2, 2)
print("\n3D ndenumerate:")
for index, value in np.ndenumerate(arr3d):
    print(f"  {index}: {value}", end="")
print()
# Output:
#   (0, 0, 0): 0  (0, 0, 1): 1  (0, 1, 0): 2  (0, 1, 1): 3
#   (1, 0, 0): 4  (1, 0, 1): 5  (1, 1, 0): 6  (1, 1, 1): 7
