# Lecture 25: Product Ufuncs in NumPy

## Topic Overview

Product operations are essential for calculating compound effects, factorials, probabilities, and growth rates. NumPy provides `np.prod()` for total product and `np.cumprod()` for cumulative product. These functions are commonly used in financial calculations (compound interest), probability (independent events), and mathematical computations.

Understanding when to use product vs. sum operations is crucial for accurate calculations.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `np.prod()` to calculate total products of arrays
2. Apply product operations along specific axes
3. Use `np.cumprod()` for cumulative products
4. Filter product operations using boolean masks
5. Use `where` parameter for conditional products
6. Apply products to compound interest calculations
7. Calculate factorials using cumulative products
8. Compute geometric means using products
9. Handle edge cases (zeros, overflow)
10. Apply product operations to probability calculations

---

## Key Concepts

### 1. Basic Product

```python
import numpy as np

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
```

### 2. Cumulative Product

```python
import numpy as np

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
```

### 3. Product with Mask

```python
import numpy as np

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
```

### 4. Product with Initial and Where

```python
import numpy as np

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
```

### 5. Practical Product Examples

```python
import numpy as np

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
```

---

## Code Examples with Explanations

### Example 1: Compound Growth Calculation

```python
import numpy as np

# Investment returns over 5 years
annual_returns = np.array([1.08, 1.12, 0.95, 1.10, 1.07])

# Calculate cumulative growth
cumulative_growth = np.cumprod(annual_returns)

print("Annual returns:", annual_returns)
print("Cumulative growth:", cumulative_growth.round(4))

# Initial investment of $10000
initial = 10000
final_values = initial * cumulative_growth

print(f"\nInitial investment: ${initial}")
for year, (growth, value) in enumerate(zip(cumulative_growth, final_values), 1):
    print(f"Year {year}: {growth:.4f}x (${value:,.2f})")
```

### Example 2: Probability Calculations

```python
import numpy as np

# Probability of multiple independent events
# All must occur: multiply probabilities
event_a_prob = 0.8
event_b_prob = 0.9
event_c_prob = 0.7

# Combined probability (all events)
all_events = np.prod([event_a_prob, event_b_prob, event_c_prob])
print(f"P(all events): {all_events:.4f}")

# At least one event (1 - P(none))
none_prob = np.prod([1 - event_a_prob, 1 - event_b_prob, 1 - event_c_prob])
at_least_one = 1 - none_prob
print(f"P(at least one): {at_least_one:.4f}")
```

### Example 3: Factorial Calculation

```python
import numpy as np

def factorial(n):
    """Calculate factorial using cumulative product."""
    if n == 0 or n == 1:
        return 1
    return np.prod(np.arange(2, n + 1))

# Calculate factorials
for n in range(11):
    print(f"{n}! = {factorial(n)}")

# Using cumprod for all factorials
factorials = np.cumprod(np.arange(1, 11))
print("\nFactorials (cumprod):", factorials)
```

### Example 4: Geometric Mean

```python
import numpy as np

# Geometric mean using products
data = np.array([2, 8, 4])

# Method 1: Direct calculation
geo_mean_direct = np.prod(data) ** (1/len(data))

# Method 2: Using logarithms (more numerically stable)
geo_mean_log = np.exp(np.mean(np.log(data)))

print("Data:", data)
print(f"Geometric mean (direct): {geo_mean_direct:.4f}")
print(f"Geometric mean (log): {geo_mean_log:.4f}")

# Compare with arithmetic mean
print(f"Arithmetic mean: {np.mean(data):.4f}")
```

### Example 5: Portfolio Returns

```python
import numpy as np

# Stock portfolio returns
stocks = np.array(["AAPL", "GOOGL", "MSFT", "AMZN"])
returns = np.array([1.15, 0.92, 1.08, 1.22])  # 15%, -8%, 8%, 22%
weights = np.array([0.3, 0.25, 0.25, 0.2])

# Calculate portfolio return
portfolio_return = np.prod(returns ** weights)
print("Stock returns:", returns)
print("Weights:", weights)
print(f"Portfolio return: {portfolio_return:.4f} ({(portfolio_return-1)*100:.2f}%)")

# Multi-period returns
period_returns = np.array([1.05, 0.98, 1.02, 1.07, 0.99])
total_return = np.prod(period_returns)
print(f"\nPeriod returns: {period_returns}")
print(f"Total return: {total_return:.4f} ({(total_return-1)*100:.2f}%)")
```

---

## Common Mistakes to Avoid

### Mistake 1: Overflow with Large Products

```python
import numpy as np

# WARNING: Large factorials overflow!
large_factorial = np.prod(np.arange(1, 171))  # 170! overflows float64
print(f"170! = {large_factorial}")  # inf

# Use log space for large products
log_factorial = np.sum(np.log(np.arange(1, 171)))
print(f"log(170!) = {log_factorial:.2f}")
```

### Mistake 2: Product with Zeros

```python
import numpy as np

arr = np.array([1, 2, 0, 4, 5])
print("Product with zero:", np.prod(arr))  # 0!

# If zeros are meaningful, consider excluding them
non_zero = arr[arr > 0]
print("Product (no zeros):", np.prod(non_zero))
```

### Mistake 3: Confusing Product and Sum

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Different operations
print("Sum:", np.sum(arr))      # 15
print("Product:", np.prod(arr))  # 120
```

---

## Best Practices

### 1. Use Log Space for Large Products

```python
import numpy as np

# For very large products, work in log space
large_data = np.random.randint(1, 100, size=1000)

# Direct product may overflow
# product = np.prod(large_data)  # May be inf!

# Log space is safer
log_product = np.sum(np.log(large_data))
product_from_log = np.exp(log_product)
```

### 2. Handle Zeros Explicitly

```python
import numpy as np

arr = np.array([1, 2, 0, 4, 5])

# Check for zeros before product
if np.any(arr == 0):
    print("Warning: array contains zeros")
```

### 3. Use Initial for Identity Element

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Cumulative product starting from 1 (multiplicative identity)
print(np.cumprod(arr, initial=1))
```

---

## Practice Exercises

### Exercise 1: Basic Product

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# TODO: Calculate total product
total = np.prod(arr)
print("Total product:", total)

# TODO: Calculate cumulative product
cumulative = np.cumprod(arr)
print("Cumulative product:", cumulative)
```

### Exercise 2: Compound Interest

```python
import numpy as np

# TODO: Calculate compound interest
principal = 1000
rates = np.array([1.05, 1.03, 1.07, 1.02])

final = principal * np.prod(rates)
print(f"Final amount: ${final:.2f}")
```

### Exercise 3: Probability

```python
import numpy as np

# TODO: Calculate probability of all events
probs = np.array([0.8, 0.9, 0.7])
all_prob = np.prod(probs)
print(f"P(all): {all_prob:.4f}")
```

---

## Summary

| Function | Description |
|----------|-------------|
| **np.prod()** | Total product of array |
| **np.cumprod()** | Cumulative product |
| **axis** | Product along specific axis |
| **where** | Conditional product |
| **initial** | Starting value for cumprod |

---

**Next Lecture:** [26 - Difference Ufuncs](26-ufunc-differences-lecture.md)
