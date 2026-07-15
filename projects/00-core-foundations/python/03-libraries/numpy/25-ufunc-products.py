"""
Ufunc Products
W3Schools: https://www.w3schools.com/python/numpy_ufunc_products.asp

Product (multiplication) operations on arrays.
"""

import numpy as np

# ============================================================
# Example 1: Basic Product
# prod() multiplies all elements.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# Total product
print("prod():", np.prod(arr))       # 120
print("arr.prod():", arr.prod())     # 120

# Product along axis
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\n2D Array:\n", arr2d)
print("Product all:", arr2d.prod())              # 362880
print("Product rows (axis=1):", arr2d.prod(axis=1))  # [  6 120 504]
print("Product cols (axis=0):", arr2d.prod(axis=0))  # [ 28  80 162]

# Cumulative product
print("\ncumprod():", np.cumprod(arr))  # [  1   2   6  24 120]
# Output:
# prod(): 120
# arr.prod(): 120
#
# Product all: 362880
# Product rows (axis=1): [  6 120 504]
# Product cols (axis=0): [ 28  80 162]

# ============================================================
# Example 2: Cumulative Product
# Running product along an axis.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

print("\nOriginal:", arr)
print("cumprod():", np.cumprod(arr))  # [  1   2   6  24 120]

# 2D cumulative product
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print("\n2D Array:\n", arr2d)
print("cumprod():", np.cumprod(arr2d))
# [  1   2   6  24 120 720]

# Along axis
print("cumprod(axis=0):\n", np.cumprod(arr2d, axis=0))
# [[ 1  2  3]
#  [ 4 10 18]]

print("cumprod(axis=1):\n", np.cumprod(arr2d, axis=1))
# [[  1   2   6]
#  [  4  20 120]]

# Practical: compound growth
rates = np.array([1.05, 1.03, 1.07, 1.02, 1.06])
growth = np.cumprod(rates)
print(f"\nGrowth rates: {rates}")
print(f"Cumulative growth: {growth.round(4)}")
print(f"Final value: ${1000 * growth[-1]:.2f}")
# Output:
# cumprod(): [  1   2   6  24 120]

# ============================================================
# Example 3: Product with Mask
# Multiply specific elements.
# ============================================================

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Product of elements > 5
mask = arr > 5
product_gt5 = arr[mask].prod()
print("\nProduct of elements > 5:", product_gt5)  # 30240

# Product of even numbers
even_product = arr[arr % 2 == 0].prod()
print("Product of even numbers:", even_product)  # 3840

# Product using where
product = np.prod(arr, where=arr > 3)
print("Product where > 3:", product)  # 6720

# Product of diagonal
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
diag_product = np.prod(np.diag(arr2d))
print("\nDiagonal product:", diag_product)  # 45
# Output:
# Product of elements > 5: 30240
# Product of even numbers: 3840

# ============================================================
# Example 4: Product with Initial and Where
# Control product operations.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# Product with initial value
print("\nProduct with initial=2:", np.prod(arr, initial=2))  # 240

# Cumprod with initial
print("cumprod with initial=1:", np.cumprod(arr, initial=1))
# [  1   1   2   6  24 120]

# Product along axis with initial
arr2d = np.array([[1, 2], [3, 4], [5, 6]])
print("\n2D Array:\n", arr2d)
print("cumprod(axis=1, initial=1):\n", np.cumprod(arr2d, axis=1, initial=1))
# [[ 1  1  2]
#  [ 1  3 12]
#  [ 1  5 30]]
# Output:
# Product with initial=2: 240
# cumprod with initial=1: [  1   1   2   6  24 120]

# ============================================================
# Example 5: Practical Product Examples
# Real-world use cases.
# ============================================================

# Compound interest
principal = 1000
quarterly_rates = np.array([1.02, 1.015, 1.025, 1.01])  # Quarterly returns
final = principal * np.prod(quarterly_rates)
print(f"\nPrincipal: ${principal}")
print(f"Quarterly rates: {quarterly_rates}")
print(f"Final amount: ${final:.2f}")

# Portfolio returns
stock_returns = np.array([1.10, 0.95, 1.05, 1.08, 0.98])
portfolio_return = np.prod(stock_returns)
print(f"\nStock returns: {stock_returns}")
print(f"Total return: {portfolio_return:.4f} ({(portfolio_return-1)*100:.2f}%)")

# Probability of independent events
event_probs = np.array([0.8, 0.9, 0.7, 0.85])
combined_prob = np.prod(event_probs)
print(f"\nEvent probabilities: {event_probs}")
print(f"Combined probability: {combined_prob:.4f}")

# Factorial using cumprod
n = 10
factorial = np.cumprod(np.arange(1, n + 1))[-1]
print(f"\n{n}! = {factorial}")

# Geometric mean
data = np.array([10, 100, 1000])
geometric_mean = np.prod(data) ** (1/len(data))
print(f"\nData: {data}")
print(f"Geometric mean: {geometric_mean:.2f}")
print(f"Using log: {np.exp(np.mean(np.log(data))):.2f}")
