"""
NumPy Getting Started
W3Schools: https://www.w3schools.com/python/numpy_getting_started.asp

How to install NumPy and get started with basic array operations.
"""

import numpy as np

# ============================================================
# Example 1: Installation and Import
# NumPy is installed via pip and imported as np (convention).
# ============================================================

# After installation: pip install numpy
# Import convention:
# import numpy as np

print("NumPy version:", np.__version__)
# Output: NumPy version: <your installed version, e.g. 2.x.x>

# ============================================================
# Example 2: Creating Your First Array
# Multiple ways to create NumPy arrays.
# ============================================================

# From a Python list
arr1 = np.array([1, 2, 3, 4, 5])
print("From list:", arr1)
print("Type:", type(arr1))
# Output:
# From list: [1 2 3 4 5]
# Type: <class 'numpy.ndarray'>

# From a nested list (2D)
arr2 = np.array([[1, 2, 3], [4, 5, 6]])
print("\n2D array:\n", arr2)
# Output:
# 2D array:
#  [[1 2 3]
#   [4 5 6]]

# Using array creation functions
arr_zeros = np.zeros(5)
print("\nZeros:", arr_zeros)
# Output: Zeros: [0. 0. 0. 0. 0.]

arr_ones = np.ones(3)
print("Ones:", arr_ones)
# Output: Ones: [1. 1. 1.]

arr_range = np.arange(0, 10, 2)
print("Range (0 to 10, step 2):", arr_range)
# Output: Range (0 to 10, step 2): [0 2 4 6 8]

arr_linspace = np.linspace(0, 1, 5)
print("Linspace (0 to 1, 5 points):", arr_linspace)
# Output: Linspace (0 to 1, 5 points): [0.   0.25 0.5  0.75 1.  ]

# ============================================================
# Example 3: Array Data Types
# NumPy automatically infers data types.
# ============================================================

# Integer array
arr_int = np.array([1, 2, 3])
print("\nInteger array dtype:", arr_int.dtype)  # int64 on Linux/macOS, int32 on Windows (platform-dependent)

# Float array
arr_float = np.array([1.0, 2.0, 3.0])
print("Float array dtype:", arr_float.dtype)    # float64

# String array
arr_str = np.array(["apple", "banana", "cherry"])
print("String array dtype:", arr_str.dtype)     # <U6

# Mixed types - NumPy upcasts to common type
arr_mixed = np.array([1, 2.5, "three"])
print("Mixed array dtype:", arr_mixed.dtype)    # <U32 (all become strings)
print("Mixed array:", arr_mixed)
# Output:
# Integer array dtype: int64
# Float array dtype: float64
# String array dtype: <U6
# Mixed array dtype: <U32
# Mixed array: ['1' '2.5' 'three']

# ============================================================
# Example 4: Array Indexing Basics
# Access elements using zero-based indexing.
# ============================================================

arr = np.array([10, 20, 30, 40, 50])

# Single element
print("\nFirst element:", arr[0])    # 10
print("Third element:", arr[2])     # 30
print("Last element:", arr[-1])     # 50

# 2D array indexing
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print("\nFirst row:", arr2d[0])         # [1 2 3]
print("Second row:", arr2d[1])         # [4 5 6]
print("Element (1,2):", arr2d[1, 2])  # 6
# Output:
# First element: 10
# Third element: 30
# Last element: 50
#
# First row: [1 2 3]
# Second row: [4 5 6]
# Element (1,2): 6

# ============================================================
# Example 5: Basic Array Operations
# NumPy supports vectorized operations.
# ============================================================

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Arithmetic operations
print("\nAddition:", a + b)          # [5 7 9]
print("Subtraction:", a - b)        # [-3 -3 -3]
print("Multiplication:", a * b)     # [ 4 10 18]
print("Division:", b / a)           # [4.  2.5 2. ]
print("Power:", a ** 2)             # [1 4 9]

# Aggregation functions
print("\nSum:", np.sum(a))           # 6
print("Mean:", np.mean(a))          # 2.0
print("Max:", np.max(a))            # 3
print("Min:", np.min(a))            # 1
print("Std:", np.std(a))            # 0.816...
# Output:
# Addition: [5 7 9]
# Subtraction: [-3 -3 -3]
# Multiplication: [ 4 10 18]
# Division: [4.   2.5  2.  ]
# Power: [1 4 9]
#
# Sum: 6
# Mean: 2.0
# Max: 3
# Min: 1
# Std: 0.816496580927726
