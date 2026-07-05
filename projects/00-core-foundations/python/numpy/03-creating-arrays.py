"""
Creating Arrays
W3Schools: https://www.w3schools.com/python/numpy_creating_arrays.asp

Different ways to create NumPy arrays.
"""

import numpy as np

# ============================================================
# Example 1: Creating Arrays from Python Lists
# The most basic way to create arrays.
# ============================================================

# 1D array from list
arr = np.array([1, 2, 3, 4, 5])
print("1D array:", arr)
# Output: 1D array: [1 2 3 4 5]

# 2D array from nested list
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print("\n2D array:\n", arr2d)
# Output:
# 2D array:
#  [[1 2 3]
#   [4 5 6]]

# 3D array from nested list
arr3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print("\n3D array shape:", arr3d.shape)  # (2, 2, 2)
# Output: 3D array shape: (2, 2, 2)

# Specifying data type explicitly
arr_float = np.array([1, 2, 3], dtype=float)
print("\nFloat array:", arr_float)
print("Dtype:", arr_float.dtype)  # float64
# Output:
# Float array: [1. 2. 3.]
# Dtype: float64

# ============================================================
# Example 2: Array of Zeros
# Create arrays filled with zeros.
# ============================================================

# 1D zeros
arr_zero1 = np.zeros(5)
print("\n1D zeros:", arr_zero1)
# Output: 1D zeros: [0. 0. 0. 0. 0.]

# 2D zeros (3 rows, 4 columns)
arr_zero2 = np.zeros((3, 4))
print("\n2D zeros (3x4):\n", arr_zero2)
# Output:
# 2D zeros (3x4):
#  [[0. 0. 0. 0.]
#   [0. 0. 0. 0.]
#   [0. 0. 0. 0.]]

# Integer zeros
arr_zero_int = np.zeros(5, dtype=int)
print("Integer zeros:", arr_zero_int)  # [0 0 0 0 0]
# Output: Integer zeros: [0 0 0 0 0]

# ============================================================
# Example 3: Array of Ones
# Create arrays filled with ones.
# ============================================================

# 1D ones
arr_one1 = np.ones(5)
print("\n1D ones:", arr_one1)
# Output: 1D ones: [1. 1. 1. 1. 1.]

# 2D ones (2x3)
arr_one2 = np.ones((2, 3))
print("\n2D ones (2x3):\n", arr_one2)
# Output:
# 2D ones (2x3):
#  [[1. 1. 1.]
#   [1. 1. 1.]]

# Full array (fill with any value)
arr_full = np.full((3, 3), 7)
print("\nFull array (3x3 of 7s):\n", arr_full)
# Output:
# Full array (3x3 of 7s):
#  [[7 7 7]
#   [7 7 7]
#   [7 7 7]]

# ============================================================
# Example 4: Array of Evenly Spaced Values
# arange and linspace for creating sequences.
# ============================================================

# np.arange: like Python range but returns array
arr_arange = np.arange(0, 20, 5)
print("\narange(0, 20, 5):", arr_arange)  # [ 0  5 10 15]
# Output: arange(0, 20, 5): [ 0  5 10 15]

# np.linspace: specify number of points instead of step
arr_linspace = np.linspace(0, 10, 6)
print("linspace(0, 10, 6):", arr_linspace)
# Output: linspace(0, 10, 6): [ 0.  2.  4.  6.  8. 10.]

# With endpoint=False
arr_linspace2 = np.linspace(0, 10, 5, endpoint=False)
print("linspace(0, 10, 5, endpoint=False):", arr_linspace2)
# Output: linspace(0, 10, 5, endpoint=False): [0. 2. 4. 6. 8.]

# ============================================================
# Example 5: Random Arrays
# Arrays with random values.
# ============================================================

# Random floats between 0 and 1
arr_random = np.random.rand(5)
print("\nRandom (5):", arr_random)
# Output: Random (5): [0.548 0.715 0.603 0.545 0.424]

# Random 2D array
arr_random2d = np.random.rand(3, 3)
print("\nRandom 2D (3x3):\n", arr_random2d)

# Random integers
arr_randint = np.random.randint(0, 100, size=(3, 4))
print("\nRandom integers (3x4, 0-100):\n", arr_randint)

# Random with specific seed for reproducibility
np.random.seed(42)
arr_seed = np.random.rand(5)
print("\nSeeded random:", arr_seed)
# Always produces same output: [0.375 0.951 0.732 0.599 0.156]

# Standard normal distribution
arr_normal = np.random.randn(5)
print("Normal distribution:", arr_normal)

# Empty array (uninitialized values)
arr_empty = np.empty(5)
print("\nEmpty array:", arr_empty)  # Contains garbage values
# Output: Empty array: [0. 0. 0. 0. 0.]
