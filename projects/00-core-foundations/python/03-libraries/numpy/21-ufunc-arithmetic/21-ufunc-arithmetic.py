"""
Ufunc Arithmetic
W3Schools: https://www.w3schools.com/python/numpy_ufunc_arithmetic.asp

Arithmetic operations on arrays using ufuncs.
"""

import numpy as np

# ============================================================
# Example 1: Addition
# add() and the + operator.
# ============================================================

arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([10, 20, 30, 40, 50])

# Using ufunc
print("add():", np.add(arr1, arr2))       # [11 22 33 44 55]

# Using operator
print("arr1 + arr2:", arr1 + arr2)        # [11 22 33 44 55]

# Scalar addition
print("arr1 + 10:", arr1 + 10)            # [11 12 13 14 15]
print("np.add(arr1, 10):", np.add(arr1, 10))

# With different shapes (broadcasting)
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
arr_1d = np.array([10, 20, 30])
print("\n2D + 1D:\n", arr_2d + arr_1d)
# Output:
# add(): [11 22 33 44 55]
# arr1 + arr2: [11 22 33 44 55]
#
# 2D + 1D:
#  [[11 22 33]
#   [14 25 36]]

# ============================================================
# Example 2: Subtraction
# subtract() and the - operator.
# ============================================================

arr1 = np.array([10, 20, 30, 40, 50])
arr2 = np.array([1, 2, 3, 4, 5])

# Using ufunc
print("\nsubtract():", np.subtract(arr1, arr2))  # [ 9 18 27 36 45]

# Using operator
print("arr1 - arr2:", arr1 - arr2)                # [ 9 18 27 36 45]

# Scalar subtraction
print("arr1 - 5:", arr1 - 5)                      # [ 5 15 25 35 45]

# Negation
print("negative:", np.negative(arr1))             # [-10 -20 -30 -40 -50]
print("-arr1:", -arr1)                            # [-10 -20 -30 -40 -50]
# Output:
# subtract(): [ 9 18 27 36 45]
# arr1 - arr2: [ 9 18 27 36 45]

# ============================================================
# Example 3: Multiplication
# multiply() and the * operator.
# ============================================================

arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([10, 20, 30, 40, 50])

# Using ufunc
print("\nmultiply():", np.multiply(arr1, arr2))   # [ 10  40  90 160 250]

# Using operator
print("arr1 * arr2:", arr1 * arr2)                # [ 10  40  90 160 250]

# Scalar multiplication
print("arr1 * 3:", arr1 * 3)                      # [ 3  6  9 12 15]

# Matrix multiplication
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print("\nMatrix multiply:\n", np.matmul(a, b))
# [[19 22]
#  [43 50]]

# Dot product
print("Dot product:", np.dot(arr1, arr2))  # 550 (1*10 + 2*20 + ...)
# Output:
# multiply(): [ 10  40  90 160 250]
# Matrix multiply:
#  [[19 22]
#   [43 50]]

# ============================================================
# Example 4: Division
# divide(), true_divide(), and the / operator.
# ============================================================

arr1 = np.array([10, 20, 30, 40, 50])
arr2 = np.array([2, 4, 5, 8, 10])

# True division (float result)
print("\ndivide():", np.divide(arr1, arr2))     # [5. 5. 6. 5. 5.]
print("arr1 / arr2:", arr1 / arr2)              # [5. 5. 6. 5. 5.]

# Floor division (integer result)
print("floor_divide():", np.floor_divide(arr1, arr2))  # [5 5 6 5 5]
print("arr1 // arr2:", arr1 // arr2)                    # [5 5 6 5 5]

# Modulus
print("mod():", np.mod(arr1, arr2))             # [0 0 0 0 0]
print("arr1 % arr2:", arr1 % arr2)              # [0 0 0 0 0]

# Remainder
print("remainder():", np.remainder(arr1, arr2))

# Division by zero handling
arr_zero = np.array([1, 0, 1])
with np.errstate(divide='ignore', invalid='ignore'):
    result = np.divide(arr1[:3], arr_zero)
    print("\nDivision by zero:", result)  # [10. inf nan]
# Output:
# divide(): [5. 5. 6. 5. 5.]
# floor_divide(): [5 5 6 5 5]
# mod(): [0 0 0 0 0]

# ============================================================
# Example 5: Power and Modulo
# power() and mod() operations.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# Power
print("\npower():", np.power(arr, 2))     # [ 1  4  9 16 25]
print("arr ** 2:", arr ** 2)              # [ 1  4  9 16 25]
print("power(3):", np.power(arr, 3))      # [  1   8  27  64 125]

# Square root
print("sqrt():", np.sqrt(arr))            # [1.   1.41 1.73 2.   2.24]

# Cube root
print("cbrt():", np.cbrt(arr))            # [1.    1.26 1.44 1.59 1.71]

# Modulo
arr1 = np.array([10, 15, 20, 25, 30])
arr2 = np.array([3, 4, 6, 7, 8])
print("\nmod():", np.mod(arr1, arr2))      # [1 3 2 4 6]
print("arr1 % arr2:", arr1 % arr2)        # [1 3 2 4 6]

# Practical: check even/odd
print("\nEven/odd:", np.where(arr % 2 == 0, "even", "odd"))
# Output:
# power(): [ 1  4  9 16 25]
# sqrt(): [1.    1.414 1.732 2.    2.236]
# mod(): [1 3 2 4 6]
