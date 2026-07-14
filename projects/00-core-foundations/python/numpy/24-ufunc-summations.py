"""
Ufunc Summations
W3Schools: https://www.w3schools.com/python/numpy_ufunc_summations.asp

Summation operations on arrays.
"""

import numpy as np

# ============================================================
# Example 1: Basic Sum
# sum() adds all elements.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Total sum
print("sum():", np.sum(arr))       # 55
print("arr.sum():", arr.sum())     # 55

# Sum along axis
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\n2D Array:\n", arr2d)
print("Sum all:", arr2d.sum())           # 45
print("Sum rows (axis=1):", arr2d.sum(axis=1))  # [ 6 15 24]
print("Sum cols (axis=0):", arr2d.sum(axis=0))  # [12 15 18]

# Cumulative sum
print("\ncumsum():", np.cumsum(arr))  # [ 1  3  6 10 15 21 28 36 45 55]
# Output:
# sum(): 55
# arr.sum(): 55
#
# Sum all: 45
# Sum rows (axis=1): [ 6 15 24]
# Sum cols (axis=0): [12 15 18]

# ============================================================
# Example 2: Sum with Mask
# Sum elements that meet a condition.
# ============================================================

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# Sum of elements > 50
mask = arr > 50
print("\nSum of elements > 50:", arr[mask].sum())  # 400

# Sum using where parameter
print("Sum where > 50:", np.sum(arr, where=arr > 50))  # 400

# Conditional sum
even_sum = np.sum(arr[arr % 2 == 0])
print("Sum of even numbers:", even_sum)

# Sum with condition on 2D
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\nSum of elements > 5:", np.sum(arr2d[arr2d > 5]))  # 30
# Output:
# Sum of elements > 50: 400
# Sum where > 50: 400

# ============================================================
# Example 3: Cumulative Sum
# Running total along an axis.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# 1D cumulative sum
print("\nOriginal:", arr)
print("cumsum():", np.cumsum(arr))  # [ 1  3  6 10 15]

# 2D cumulative sum
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print("\n2D Array:\n", arr2d)
print("cumsum():", np.cumsum(arr2d))
# [ 1  3  6 10 15 21]

# Cumsum along axis
print("cumsum(axis=0):\n", np.cumsum(arr2d, axis=0))
# [[1 2 3]
#  [5 7 9]]

print("cumsum(axis=1):\n", np.cumsum(arr2d, axis=1))
# [[ 1  3  6]
#  [ 4  9 15]]

# Practical: calculate running balance
deposits = np.array([1000, 500, -200, 300, -100])
balance = np.cumsum(deposits)
print("\nDeposits:", deposits)
print("Running balance:", balance)
# Output:
# Original: [1 2 3 4 5]
# cumsum(): [ 1  3  6 10 15]

# ============================================================
# Example 4: Summation with Initial and Where
# Control where summation occurs.
# ============================================================

arr = np.array([10, 20, 30, 40, 50])

# Sum with initial value
print("\nSum with initial=100:", np.sum(arr, initial=100))  # 250

# Sum only positive elements
arr2 = np.array([-5, 10, -15, 20, -25])
print("\nArray:", arr2)
print("Sum positives:", np.sum(arr2, where=arr2 > 0))  # 30

# Cumulative sum with initial
print("\ncumsum with initial=0:", np.cumsum(arr, initial=0))
# [  0   1   3   6  10  15]

# Sum with axis and initial
arr2d = np.array([[1, 2], [3, 4], [5, 6]])
print("\n2D Array:\n", arr2d)
print("cumsum(axis=1, initial=0):\n", np.cumsum(arr2d, axis=1, initial=0))
# [[ 0  1  3]
#  [ 0  3  7]
#  [ 0  5 11]]
# Output:
# Sum with initial=100: 250
# Sum positives: 30

# ============================================================
# Example 5: Practical Summation Examples
# Real-world use cases.
# ============================================================

# Running total of sales
daily_sales = np.array([1200, 1500, 800, 2200, 1800, 900, 1100])
print("\nDaily sales:", daily_sales)
print("Weekly total:", daily_sales.sum())
print("Running total:", np.cumsum(daily_sales))

# Moving average (using cumsum)
def moving_average(arr, window):
    cumsum = np.cumsum(arr)
    cumsum = np.insert(cumsum, 0, 0)
    return (cumsum[window:] - cumsum[:-window]) / window

prices = np.array([100, 102, 101, 103, 105, 104, 106, 108, 107, 109])
ma3 = moving_average(prices, 3)
print(f"\nPrices: {prices}")
print(f"3-day MA: {ma3.round(2)}")

# Cumulative percentage
values = np.array([30, 25, 20, 15, 10])
total = values.sum()
cumulative = np.cumsum(values) / total * 100
print(f"\nValues: {values}")
print(f"Cumulative %: {cumulative.round(1)}")
