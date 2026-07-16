# Lecture 23: Logarithmic and Exponential Ufuncs

## Topic Overview

Logarithmic and exponential functions are fundamental in mathematics, science, and engineering. NumPy provides comprehensive support for logarithms (natural, base-2, base-10) and exponentials, along with related power functions. These operations are essential for data transformation, scaling, information theory, and many scientific applications.

Understanding when to use different logarithmic bases and their properties is crucial for data analysis and machine learning.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `np.log()` for natural logarithm (base e)
2. Use `np.log2()` for base-2 logarithm
3. Use `np.log10()` for base-10 logarithm
4. Use `np.log1p()` for log(1+x) with better precision
5. Use `np.exp()` for e^x and `np.exp2()` for 2^x
6. Use `np.expm1()` for exp(x)-1 with better precision
7. Apply power functions: `np.power()`, `np.square()`, `np.sqrt()`
8. Verify logarithmic identities
9. Apply logarithmic functions in practical scenarios (information theory, decibels, compound interest)
10. Handle edge cases (log of zero, negative numbers)

---

## Key Concepts

### 1. Logarithm Functions

```python
import numpy as np

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
```

**When to use each:**
- `np.log()`: Natural logarithm (most common in mathematics)
- `np.log2()`: Binary logarithm (information theory, computing)
- `np.log10()`: Common logarithm (decibels, pH scale)
- `np.log1p()`: When x is close to 0 (numerical stability)

### 2. Exponential Functions

```python
import numpy as np

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
```

### 3. Power Functions

```python
import numpy as np

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
```

### 4. Logarithmic Identities

```python
import numpy as np

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
```

### 5. Practical Applications

```python
import numpy as np

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
```

---

## Code Examples with Explanations

### Example 1: Comparing Logarithmic Bases

```python
import numpy as np

arr = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])

print("Value | log (base e) | log2 (base 2) | log10 (base 10)")
print("-" * 60)
for val in arr:
    print(f"{val:>5} | {np.log(val):>12.4f} | {np.log2(val):>13.4f} | {np.log10(val):>14.4f}")
```

### Example 2: Numerical Stability with log1p and expm1

```python
import numpy as np

x = 1e-10

# For very small x, log(1+x) loses precision
print("log(1 + x):", np.log(1 + x))        # May be 0.0
print("log1p(x):", np.log1p(x))            # More accurate

# Similarly for exp(x) - 1
print("exp(x) - 1:", np.exp(x) - 1)        # May be 0.0
print("expm1(x):", np.expm1(x))            # More accurate

# Verify they're equivalent for larger values
arr = np.array([0.1, 1.0, 10.0, 100.0])
print("\nlog1p vs log(1+x):", np.allclose(np.log1p(arr), np.log(1 + arr)))
print("expm1 vs exp(x)-1:", np.allclose(np.expm1(arr), np.exp(arr) - 1))
```

### Example 3: Information Theory

```python
import numpy as np

# Calculate Shannon entropy
def shannon_entropy(probs):
    """Calculate Shannon entropy in bits."""
    # Remove zero probabilities to avoid log(0)
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

# Different probability distributions
distributions = {
    "Fair coin": np.array([0.5, 0.5]),
    "Biased coin": np.array([0.9, 0.1]),
    "Fair die": np.array([1/6] * 6),
    "Skewed die": np.array([0.5, 0.1, 0.1, 0.1, 0.1, 0.1]),
}

print("Shannon Entropy:")
for name, probs in distributions.items():
    entropy = shannon_entropy(probs)
    print(f"  {name}: {entropy:.4f} bits")
```

### Example 4: Decibel Scale

```python
import numpy as np

# Power ratio to decibels
def power_to_db(power_ratio):
    return 10 * np.log10(power_ratio)

# Amplitude ratio to decibels
def amplitude_to_db(amplitude_ratio):
    return 20 * np.log10(amplitude_ratio)

# Examples
power_ratios = np.array([1, 2, 5, 10, 100, 1000])
print("Power ratios to dB:")
for ratio in power_ratios:
    print(f"  {ratio}x → {power_to_db(ratio):.1f} dB")

# Audio volume levels
volumes = np.array([0.1, 0.5, 1.0, 2.0, 5.0])
print("\nVolume levels to dB:")
for vol in volumes:
    print(f"  {vol}x → {amplitude_to_db(vol):.1f} dB")
```

### Example 5: Financial Applications

```python
import numpy as np

# Continuous compounding
principal = 10000
annual_rate = 0.05
years = np.array([1, 5, 10, 20, 30])

# Future value with continuous compounding
fv = principal * np.exp(annual_rate * years)

print("Continuous Compounding:")
print(f"Principal: ${principal}")
print(f"Rate: {annual_rate:.0%}")
print("-" * 30)
for t, value in zip(years, fv):
    print(f"  {t:>2} years: ${value:>10.2f}")

# Log returns for stock analysis
prices = np.array([100, 105, 102, 110, 108, 115])
log_returns = np.diff(np.log(prices))
percent_returns = np.exp(log_returns) - 1

print("\nStock Returns:")
print(f"Prices: {prices}")
print(f"Log returns: {log_returns.round(4)}")
print(f"Percent returns: {(percent_returns * 100).round(2)}%")
```

---

## Common Mistakes to Avoid

### Mistake 1: Log of Zero or Negative Numbers

```python
import numpy as np

# WRONG - log of 0 or negative
# np.log(0)    # -inf
# np.log(-1)   # nan

# CORRECT - Handle edge cases
arr = np.array([-1, 0, 1, 2, 3])
safe_log = np.where(arr > 0, np.log(arr), np.nan)
print("Safe log:", safe_log)
```

### Mistake 2: Using Wrong Base

```python
import numpy as np

# WRONG - Assuming base 10
# result = np.log(100)  # Returns 4.605, not 2!

# CORRECT - Use appropriate function
print("log(100):", np.log(100))      # 4.605 (base e)
print("log2(100):", np.log2(100))    # 6.644 (base 2)
print("log10(100):", np.log10(100))  # 2.0 (base 10)
```

### Mistake 3: Precision Loss with Small Values

```python
import numpy as np

x = 1e-15

# WRONG - Precision loss
result1 = np.log(1 + x)

# CORRECT - Use log1p
result2 = np.log1p(x)
print(f"log(1+x): {result1}")
print(f"log1p(x): {result2}")
```

---

## Best Practices

### 1. Use Appropriate Base

```python
import numpy as np

# Natural log for mathematical operations
result = np.log(arr)

# Base 2 for information theory
entropy = -np.sum(probs * np.log2(probs))

# Base 10 for decibels, pH
db = 10 * np.log10(power_ratio)
```

### 2. Use log1p/expm1 for Small Values

```python
import numpy as np

x = np.array([1e-10, 1e-8, 1e-6])

# For numerical stability
log_result = np.log1p(x)
exp_result = np.expm1(x)
```

### 3. Handle Edge Cases

```python
import numpy as np

arr = np.array([-1, 0, 0.5, 1, 2])

# Safe logarithm
safe_log = np.where(arr > 0, np.log(arr), np.nan)
```

---

## Practice Exercises

### Exercise 1: Basic Logarithms

```python
import numpy as np

arr = np.array([1, 10, 100, 1000, 10000])

# TODO: Calculate natural log
natural = np.log(arr)
print("Natural log:", natural.round(4))

# TODO: Calculate base-10 log
base10 = np.log10(arr)
print("Base-10 log:", base10)

# TODO: Calculate base-2 log
base2 = np.log2(arr)
print("Base-2 log:", base2.round(4))
```

### Exercise 2: Exponentials

```python
import numpy as np

arr = np.array([0, 1, 2, 3, 4, 5])

# TODO: Calculate e^x
exp_result = np.exp(arr)
print("e^x:", exp_result.round(4))

# TODO: Calculate 2^x
exp2_result = np.exp2(arr)
print("2^x:", exp2_result)

# TODO: Verify exp(log(x)) = x
x = np.array([1, 2, 3, 4, 5])
print("exp(log(x)):", np.exp(np.log(x)))
```

### Exercise 3: Practical Applications

```python
import numpy as np

# TODO: Calculate decibels for power ratios
power_ratios = np.array([1, 10, 100, 1000])
db = 10 * np.log10(power_ratios)
print("Decibels:", db)

# TODO: Calculate entropy
probs = np.array([0.25, 0.25, 0.25, 0.25])
entropy = -np.sum(probs * np.log2(probs))
print("Entropy:", entropy, "bits")
```

---

## Summary

| Function | Base | Use Case |
|----------|------|----------|
| **np.log()** | e (2.718) | Mathematics, calculus |
| **np.log2()** | 2 | Information theory, computing |
| **np.log10()** | 10 | Decibels, pH, scientific notation |
| **np.log1p()** | e | log(1+x), numerical stability |
| **np.exp()** | e | e^x |
| **np.exp2()** | 2 | 2^x |
| **np.expm1()** | e | exp(x)-1, numerical stability |
| **np.power()** | any | x^n |
| **np.square()** | 2 | x^2 |
| **np.sqrt()** | 0.5 | √x |

---

**Next Lecture:** [24 - Summation Ufuncs](24-ufunc-summations-lecture.md)
