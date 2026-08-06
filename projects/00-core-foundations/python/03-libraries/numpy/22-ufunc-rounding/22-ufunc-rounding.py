"""
Ufunc Rounding
W3Schools: https://www.w3schools.com/python/numpy_ufunc_rounding.asp

Rounding, truncating, and ceiling/floor operations.
"""

import numpy as np

# ============================================================
# Example 1: Rounding to Nearest Integer
# around() and round().
# ============================================================

arr = np.array([1.2, 2.5, 3.7, 4.1, 5.5, 6.9])

print("Original:", arr)
print("round():", np.round(arr))       # [1. 2. 4. 4. 6. 7.]
print("around():", np.around(arr))     # [1. 2. 4. 4. 6. 7.]

# Round to specific decimal places
arr2 = np.array([1.2345, 2.3456, 3.4567])
print("\nRound to 2 decimals:", np.round(arr2, 2))  # [1.23 2.35 3.46]
print("Round to 1 decimal:", np.round(arr2, 1))    # [1.2 2.3 3.5]
print("Round to 0 decimals:", np.round(arr2, 0))   # [1. 2. 3.]

# Round to nearest 10
arr3 = np.array([12, 27, 33, 48, 55])
print("\nRound to nearest 10:", np.round(arr3, -1))  # [10 30 30 50 60]

# Round to nearest 100
print("Round to nearest 100:", np.round(arr3, -2))  # [  0   0   0   0 100]
# Output:
# Original: [1.2 2.5 3.7 4.1 5.5 6.9]
# round(): [1. 2. 4. 4. 6. 7.]
# around(): [1. 2. 4. 4. 6. 7.]

# ============================================================
# Example 2: Floor and Ceil
# floor() rounds down, ceil() rounds up.
# ============================================================

arr = np.array([1.2, 2.5, 3.7, -1.3, -2.8, 4.0])

print("\nOriginal:", arr)
print("floor():", np.floor(arr))    # [ 1.  2.  3. -2. -3.  4.]
print("ceil():", np.ceil(arr))      # [ 2.  3.  4. -1. -2.  4.]

# Floor is always <= value, ceil is always >= value
print("\nFloor check:", np.all(np.floor(arr) <= arr))  # True
print("Ceil check:", np.all(np.ceil(arr) >= arr))      # True

# Practical example: ceiling division
a = np.array([10, 11, 12, 13])
b = np.array([3, 3, 3, 3])
ceiling_div = np.ceil(a / b).astype(int)
print("\nCeiling division:", a, "//", b, "=", ceiling_div)
# Output:
# Original: [ 1.2  2.5  3.7 -1.3 -2.8  4. ]
# floor(): [ 1.  2.  3. -2. -3.  4.]
# ceil(): [ 2.  3.  4. -1. -2.  4.]

# ============================================================
# Example 3: Truncation
# trunc() and fix() truncate toward zero.
# ============================================================

arr = np.array([1.9, 2.1, -3.7, -4.2, 5.5])

print("\nOriginal:", arr)
print("trunc():", np.trunc(arr))    # [ 1.  2. -3. -4.  5.]
print("fix():", np.fix(arr))        # [ 1.  2. -3. -4.  5.]

# trunc vs floor for negative numbers
print("\nFor -3.7:")
print("  trunc:", np.trunc(-3.7))   # -3.0 (toward zero)
print("  floor:", np.floor(-3.7))   # -4.0 (toward -inf)

# Practical: integer part extraction
arr2 = np.array([3.14, 2.72, 1.41, 0.00])
print("\nInteger parts:", np.trunc(arr2).astype(int))  # [3 2 1 0]
# Output:
# trunc(): [ 1.  2. -3. -4.  5.]
# fix(): [ 1.  2. -3. -4.  5.]
#
# For -3.7:
#   trunc: -3.0
#   floor: -4.0

# ============================================================
# Example 4: Rounding Methods Compared
# Different rounding strategies for same values.
# ============================================================

arr = np.array([1.5, 2.5, 3.5, 4.5, -1.5, -2.5])

print("\nOriginal:", arr)
print("round():", np.round(arr))      # [2. 2. 4. 4. -2. -2.]
print("floor():", np.floor(arr))      # [ 1.  2.  3.  4. -2. -3.]
print("ceil():", np.ceil(arr))        # [2. 3. 4. 5. -1. -2.]
print("trunc():", np.trunc(arr))      # [ 1.  2.  3.  4. -1. -2.]

# Banker's rounding (round half to even)
print("\nBanker's rounding:")
print("  round(0.5):", np.round(0.5))    # 0.0 (rounds to even)
print("  round(1.5):", np.round(1.5))    # 2.0 (rounds to even)
print("  round(2.5):", np.round(2.5))    # 2.0 (rounds to even)
print("  round(3.5):", np.round(3.5))    # 4.0 (rounds to even)
# Output:
# round(): [ 2.  2.  4.  4. -2. -2.]
# floor(): [ 1.  2.  3.  4. -2. -3.]
# ceil(): [ 2.  3.  4.  5. -1. -2.]

# ============================================================
# Example 5: Practical Rounding Examples
# Real-world use cases.
# ============================================================

# Currency rounding
prices = np.array([19.999, 29.995, 49.994, 99.991])
print("\nOriginal prices:", prices)
print("Rounded to 2 decimals:", np.round(prices, 2))

# Percentage rounding
scores = np.array([85.67, 92.34, 78.91, 95.00])
print("\nScores:", scores)
print("Grades:", np.round(scores).astype(int))

# Temperature rounding
temps = np.array([20.4, 21.6, 22.5, 23.1])
print("\nTemperatures:", temps)
print("Rounded:", np.round(temps).astype(int))

# Data binning using rounding
data = np.array([1.2, 2.7, 3.4, 4.8, 5.1, 6.9])
bins = np.round(data / 2) * 2  # Round to nearest 2
print("\nData:", data)
print("Binned to nearest 2:", bins)
# Output:
# Original prices: [19.999 29.995 49.994 99.991]
# Rounded to 2 decimals: [20.   30.   49.99 99.99]
