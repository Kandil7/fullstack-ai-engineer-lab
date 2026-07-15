"""
Ufunc Logs
W3Schools: https://www.w3schools.com/python/numpy_ufunc_logs.asp

Logarithmic and exponential functions.
"""

import numpy as np

# ============================================================
# Example 1: Logarithm Functions
# log(), log2(), log10(), log1p().
# ============================================================

arr = np.array([1, 2, 4, 8, 16, 32, 64, 128])

# Natural logarithm (base e)
print("log():", np.log(arr))
# [0.    0.693 1.386 2.079 2.773 3.466 4.159 4.852]

# Base-2 logarithm
print("log2():", np.log2(arr))
# [0. 1. 2. 3. 4. 5. 6. 7.]

# Base-10 logarithm
print("log10():", np.log10(arr))
# [0.    0.301 0.602 0.903 1.204 1.505 1.806 2.107]

# log1p(x) = log(1 + x) - more accurate for small x
arr_small = np.array([1e-10, 1e-8, 1e-6, 1e-4])
print("\nlog1p():", np.log1p(arr_small))
# Output:
# log(): [0.    0.693 1.386 2.079 2.773 3.466 4.159 4.852]
# log2(): [0. 1. 2. 3. 4. 5. 6. 7.]
# log10(): [0.    0.301 0.602 0.903 1.204 1.505 1.806 2.107]

# ============================================================
# Example 2: Exponential Functions
# exp(), exp2(), expm1().
# ============================================================

arr = np.array([0, 1, 2, 3, 4, 5])

# e^x
print("\nexp():", np.exp(arr))
# [ 1.     2.718  7.389 20.086 54.598 148.413]

# 2^x
print("exp2():", np.exp2(arr))
# [ 1.  2.  4.  8. 16. 32.]

# expm1(x) = exp(x) - 1 - more accurate for small x
arr_small = np.array([0.001, 0.01, 0.1])
print("\nexpm1():", np.expm1(arr_small))
# [0.0010005 0.0100502 0.1051709]

# Inverse of log
arr = np.array([1, 2, 3, 4, 5])
print("\nlog then exp:", np.exp(np.log(arr)))  # [1. 2. 3. 4. 5.]
print("log2 then exp2:", np.exp2(np.log2(arr)))  # [1. 2. 3. 4. 5.]
# Output:
# exp(): [  1.       2.718    7.389   20.086   54.598  148.413]
# exp2(): [ 1.  2.  4.  8. 16. 32.]

# ============================================================
# Example 3: Power Functions
# power() and square/sqrt/cbrt.
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# Power
print("\npower(x, 2):", np.power(arr, 2))    # [ 1  4  9 16 25]
print("power(x, 3):", np.power(arr, 3))      # [  1   8  27  64 125]
print("power(x, 0.5):", np.power(arr, 0.5))  # [1.   1.41 1.73 2.   2.24]

# Square and square root
print("\nsquare():", np.square(arr))    # [ 1  4  9 16 25]
print("sqrt():", np.sqrt(arr))          # [1.   1.41 1.73 2.   2.24]

# Cube root
print("cbrt():", np.cbrt(arr))          # [1.    1.26 1.44 1.59 1.71]

# Inverse square root
print("1/sqrt:", 1 / np.sqrt(arr))      # [1.    0.707 0.577 0.5   0.447]
# Output:
# power(x, 2): [ 1  4  9 16 25]
# sqrt(): [1.    1.414 1.732 2.    2.236]

# ============================================================
# Example 4: Logarithmic Identities
# Verify mathematical properties.
# ============================================================

a = np.array([2.0, 3.0, 4.0, 5.0])
b = np.array([3.0, 2.0, 5.0, 2.0])

# log(a * b) = log(a) + log(b)
lhs = np.log(a * b)
rhs = np.log(a) + np.log(b)
print("\nlog(a*b) = log(a) + log(b):", np.allclose(lhs, rhs))

# log(a / b) = log(a) - log(b)
lhs = np.log(a / b)
rhs = np.log(a) - np.log(b)
print("log(a/b) = log(a) - log(b):", np.allclose(lhs, rhs))

# log(a^n) = n * log(a)
n = 3
lhs = np.log(a ** n)
rhs = n * np.log(a)
print("log(a^n) = n*log(a):", np.allclose(lhs, rhs))

# log_b(x) = log(x) / log(b)
x = 100
base = 10
lhs = np.log10(x)
rhs = np.log(x) / np.log(base)
print("log_10(100) = ln(100)/ln(10):", np.allclose(lhs, rhs))
# Output:
# log(a*b) = log(a) + log(b): True
# log(a/b) = log(a) - log(b): True
# log(a^n) = n*log(a): True
# log_10(100) = ln(100)/ln(10): True

# ============================================================
# Example 5: Practical Applications
# Use cases for logarithmic functions.
# ============================================================

# Information theory: entropy
probs = np.array([0.25, 0.25, 0.25, 0.25])  # Uniform
entropy = -np.sum(probs * np.log2(probs))
print(f"\nEntropy (uniform): {entropy:.4f} bits")  # 2.0

probs = np.array([0.9, 0.05, 0.03, 0.02])  # Skewed
entropy = -np.sum(probs * np.log2(probs))
print(f"Entropy (skewed): {entropy:.4f} bits")    # ~1.0

# Signal strength: decibels
power_ratio = np.array([1, 10, 100, 1000])
db = 10 * np.log10(power_ratio)
print(f"\nDecibels: {db}")  # [0. 10. 20. 30.]

# Compound interest: continuous compounding
principal = 1000
rate = 0.05
time = np.array([1, 5, 10, 20, 30])
future_value = principal * np.exp(rate * time)
print(f"\nContinuous compounding:")
for t, fv in zip(time, future_value):
    print(f"  {t} years: ${fv:.2f}")

# Growth rate from log differences
values = np.array([100, 110, 121, 133, 146])
log_returns = np.diff(np.log(values))
print(f"\nLog returns: {log_returns.round(4)}")
print(f"Approx growth rate: {log_returns.mean():.4f}")
