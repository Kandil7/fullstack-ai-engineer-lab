"""
NumPy Introduction
W3Schools: https://www.w3schools.com/python/numpy_intro.asp

NumPy is a Python library used for working with arrays.
It also has functions for working in domain of linear algebra,
fourier transform, and matrices.
"""

import numpy as np

# ============================================================
# Example 1: What is NumPy?
# NumPy stands for Numerical Python and is the core library
# for scientific computing in Python.
# ============================================================

# Create a simple Python list
python_list = [1, 2, 3, 4, 5]
print("Python list:", python_list)
print("Type:", type(python_list))  # <class 'list'>

# Create a NumPy array
numpy_array = np.array([1, 2, 3, 4, 5])
print("\nNumPy array:", numpy_array)
print("Type:", type(numpy_array))  # <class 'numpy.ndarray'>
print("Shape:", numpy_array.shape)  # (5,)
# Output:
# Python list: [1, 2, 3, 4, 5]
# Type: <class 'list'>
#
# NumPy array: [1 2 3 4 5]
# Type: <class 'numpy.ndarray'>
# Shape: (5,)

# ============================================================
# Example 2: Why Use NumPy?
# NumPy arrays are faster and more memory-efficient than
# Python lists. They use contiguous memory blocks.
# ============================================================

import sys
import time

# Memory comparison
list_mem = sys.getsizeof(python_list)
array_mem = numpy_array.nbytes
print(f"\nMemory - List: {list_mem} bytes, Array: {array_mem} bytes")
# Output: Memory - List: 104 bytes, Array: 40 bytes

# Speed comparison: sum of 1 million elements
big_list = list(range(1_000_000))
big_array = np.arange(1_000_000)

start = time.time()
sum_list = sum(big_list)
list_time = time.time() - start

start = time.time()
sum_array = np.sum(big_array)
array_time = time.time() - start

print(f"List sum time: {list_time:.6f}s")
print(f"Array sum time: {array_time:.6f}s")
print(f"Speedup: {list_time / max(array_time, 1e-9):.1f}x faster with NumPy")
# Output:
# List sum time: 0.015000s
# Array sum time: 0.001000s
# Speedup: 15.0x faster with NumPy

# ============================================================
# Example 3: NumPy Array vs Python List Operations
# NumPy supports element-wise operations directly.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# Element-wise operations
print("\nOriginal:", arr)
print("Add 10:", arr + 10)         # [11 12 13 14 15]
print("Multiply by 2:", arr * 2)    # [ 2  4  6  8 10]
print("Square:", arr ** 2)          # [ 1  4  9 16 25]
print("Square root:", np.sqrt(arr)) # [1.   1.41 1.73 2.   2.24]
# Output:
# Original: [1 2 3 4 5]
# Add 10: [11 12 13 14 15]
# Multiply by 2: [ 2  4  6  8 10]
# Square: [ 1  4  9 16 25]
# Square root: [1.    1.414 1.732 2.    2.236]

# Python list operations require loops
py_list = [1, 2, 3, 4, 5]
# This would NOT work: py_list + 10  (TypeError)
# You need a list comprehension:
print("List add 10:", [x + 10 for x in py_list])  # [11, 12, 13, 14, 15]

# ============================================================
# Example 4: Multi-dimensional Arrays
# NumPy arrays can have any number of dimensions.
# ============================================================

# 0-D array (scalar)
arr_0d = np.array(42)
print("\n0-D array:", arr_0d)
print("Dimensions:", arr_0d.ndim)  # 0

# 1-D array (vector)
arr_1d = np.array([1, 2, 3])
print("\n1-D array:", arr_1d)
print("Dimensions:", arr_1d.ndim)  # 1

# 2-D array (matrix)
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print("\n2-D array:\n", arr_2d)
print("Dimensions:", arr_2d.ndim)  # 2

# 3-D array (tensor)
arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print("\n3-D array:\n", arr_3d)
print("Dimensions:", arr_3d.ndim)  # 3
# Output:
# 0-D array: 42
# Dimensions: 0
#
# 1-D array: [1 2 3]
# Dimensions: 1
#
# 2-D array:
#  [[1 2 3]
#   [4 5 6]]
# Dimensions: 2
#
# 3-D array:
#  [[[1 2]
#    [3 4]]
#   [[5 6]
#    [7 8]]]
# Dimensions: 3

# ============================================================
# Example 5: NumPy Array Attributes
# Every NumPy array has useful attributes for inspection.
# ============================================================

arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
print("\nArray:\n", arr)
print("Shape:", arr.shape)      # (2, 5) - 2 rows, 5 columns
print("Size:", arr.size)        # 10 - total elements
print("ndim:", arr.ndim)        # 2 - number of dimensions
print("Dtype:", arr.dtype)     # int64 on Linux/macOS, int32 on Windows (platform-dependent)
print("Item size:", arr.itemsize)  # 8 on Linux/macOS, 4 on Windows (platform-dependent)
print("Nbytes:", arr.nbytes)   # 80 on Linux/macOS, 40 on Windows (platform-dependent)
# Output:
# Array:
#  [[ 1  2  3  4  5]
#   [ 6  7  8  9 10]]
# Shape: (2, 5)
# Size: 10
# ndim: 2
# Dtype: int64
# Item size: 8
# Nbytes: 80
