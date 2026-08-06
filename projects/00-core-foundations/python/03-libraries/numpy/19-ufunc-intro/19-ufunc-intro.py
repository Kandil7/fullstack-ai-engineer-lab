"""
Ufunc Intro
W3Schools: https://www.w3schools.com/python/numpy_ufunc_intro.asp

Introduction to Universal Functions (ufuncs) in NumPy.
"""

import numpy as np

# ============================================================
# Example 1: What is a ufunc?
# Universal functions operate element-wise on arrays.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# Math operations are ufuncs
print("sqrt:", np.sqrt(arr))        # [1.   1.41 1.73 2.   2.24]
print("log:", np.log(arr))          # [0.   0.69 1.10 1.39 1.61]
print("exp:", np.exp(arr))          # [ 2.72  7.39 20.09 54.60 148.41]
print("sin:", np.sin(arr))          # [ 0.84  0.91  0.14 -0.76 -0.96]

# Compare with Python math
import math
print("\nPython math.sqrt(4):", math.sqrt(4))  # 2.0
print("NumPy np.sqrt(4):", np.sqrt(4))         # 2.0
print("NumPy np.sqrt(arr):", np.sqrt(arr))     # [1. 1.41 1.73 2. 2.24]
# Output:
# sqrt: [1.    1.414 1.732 2.    2.236]
# log: [0.    0.693 1.099 1.386 1.609]

# ============================================================
# Example 2: ufunc Types
# ufuncs include trigonometric, arithmetic, comparison, etc.
# ============================================================

arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([5, 4, 3, 2, 1])

# Arithmetic ufuncs
print("\nadd:", np.add(arr1, arr2))        # [6 6 6 6 6]
print("subtract:", np.subtract(arr1, arr2)) # [-4 -2  0  2  4]
print("multiply:", np.multiply(arr1, arr2)) # [5 8 9 8 5]
print("divide:", np.divide(arr1, arr2))     # [0.2 0.5 1.0 2.0 5.0]
print("power:", np.power(arr1, 2))          # [ 1  4  9 16 25]
print("mod:", np.mod(arr1, 2))              # [1 0 1 0 1]

# Comparison ufuncs
print("\ngreater:", np.greater(arr1, arr2))       # [False False False True True]
print("less:", np.less(arr1, arr2))               # [True True False False False]
print("equal:", np.equal(arr1, arr2))             # [False False True False False]
print("not_equal:", np.not_equal(arr1, arr2))     # [True True False True True]
# Output:
# add: [6 6 6 6 6]
# subtract: [-4 -2  0  2  4]
# multiply: [5 8 9 8 5]
# greater: [False False False  True  True]

# ============================================================
# Example 3: Absolute Values
# abs() and absolute() for absolute values.
# ============================================================

arr = np.array([-3, -2, -1, 0, 1, 2, 3])

# Absolute values
print("\nabs():", np.abs(arr))           # [3 2 1 0 1 2 3]
print("absolute():", np.absolute(arr))  # [3 2 1 0 1 2 3]

# With complex numbers
arr_complex = np.array([1+2j, 3-4j, -5+0j])
print("abs(complex):", np.abs(arr_complex))  # [2.24 5.   5.  ]
# Output:
# abs(): [3 2 1 0 1 2 3]
# absolute(): [3 2 1 0 1 2 3]
# abs(complex): [2.236 5.    5.   ]

# ============================================================
# Example 4: Rounding Functions
# Round, ceil, floor, and trunc.
# ============================================================

arr = np.array([1.2, 2.5, 3.7, -1.3, -2.8, 4.0])

print("\nOriginal:", arr)
print("round():", np.round(arr))        # [ 1.  2.  4. -1. -3.  4.]
print("ceil():", np.ceil(arr))          # [ 2.  3.  4. -1. -2.  4.]
print("floor():", np.floor(arr))        # [ 1.  2.  3. -2. -3.  4.]
print("trunc():", np.trunc(arr))        # [ 1.  2.  3. -1. -2.  4.]

# Round to specific decimals
arr2 = np.array([1.2345, 2.3456, 3.4567])
print("\nRound to 2 decimals:", np.round(arr2, 2))  # [1.23 2.35 3.46]
print("Round to 1 decimal:", np.round(arr2, 1))    # [1.2 2.3 3.5]
# Output:
# Original: [ 1.2  2.5  3.7 -1.3 -2.8  4. ]
# round(): [ 1.  2.  4. -1. -3.  4.]
# ceil(): [ 2.  3.  4. -1. -2.  4.]
# floor(): [ 1.  2.  3. -2. -3.  4.]

# ============================================================
# Example 5: ufunc Methods
# reduce, accumulate, reduceat, outer, at.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# reduce - apply operation to reduce array to single value
print("\nreduce (add):", np.add.reduce(arr))   # 15 (1+2+3+4+5)
print("reduce (multiply):", np.multiply.reduce(arr))  # 120

# accumulate - running total
print("\naccumulate (add):", np.add.accumulate(arr))  # [ 1  3  6 10 15]
print("accumulate (multiply):", np.multiply.accumulate(arr))  # [  1   2   6  24 120]

# outer - outer product
a = np.array([1, 2, 3])
b = np.array([4, 5])
print("\nouter (add):\n", np.add.outer(a, b))
# [[5 6]
#  [6 7]
#  [7 8]]

print("\nouter (multiply):\n", np.multiply.outer(a, b))
# [[ 4  5]
#  [ 8 10]
#  [12 15]]
# Output:
# reduce (add): 15
# reduce (multiply): 120
#
# accumulate (add): [ 1  3  6 10 15]
# accumulate (multiply): [  1   2   6  24 120]
#
# outer (add):
#  [[5 6]
#   [6 7]
#   [7 8]]
