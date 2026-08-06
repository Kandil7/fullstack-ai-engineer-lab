# Glossary: Product Ufuncs (Lecture 25)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| prod() | `np.prod(arr)` | Total product |
| cumprod() | `np.cumprod(arr)` | Cumulative product |
| nprod() | `np.nprod(arr)` | Product ignoring NaN |
| axis | Parameter | Product along axis |
| where | Parameter | Conditional product |
| initial | Parameter | Starting value for cumprod |
| Factorial | n! calculation | Product of 1 to n |
| Geometric Mean | (x1*x2*...*xn)^(1/n) | Central tendency for ratios |
| Compound Interest | Principal * ∏rates | Exponential growth |

---

## Detailed Definitions

### Compound Growth

**Definition:** Growth where gains are added to the principal, creating exponential growth. Calculated using product of growth factors.

**Example:**
```python
import numpy as np

# Investment returns
returns = np.array([1.08, 1.12, 1.05])
cumulative = np.cumprod(returns)
print(f"Cumulative growth: {cumulative[-1]:.4f}x")
```

**Related Terms:** Compound Interest, Growth Factor

---

### Compound Interest

**Definition:** Interest calculated on the principal and accumulated interest. Formula: A = P * ∏(1 + rate).

**Example:**
```python
import numpy as np

principal = 1000
rates = np.array([0.05, 0.04, 0.06])
final = principal * np.prod(1 + rates)
print(f"Final amount: ${final:.2f}")
```

**Related Terms:** Principal, Rate, Compound Growth

---

### cumprod()

**Definition:** Calculates the cumulative product of array elements. Returns an array of running products.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(np.cumprod(arr))
# Output: [  1   2   6  24 120]
```

**Related Terms:** cumsum(), prod()

---

### Factorial

**Definition:** The product of all positive integers up to n. Denoted as n!. Can be calculated using cumulative product.

**Example:**
```python
import numpy as np

n = 5
factorial = np.prod(np.arange(1, n + 1))
print(f"{n}! = {factorial}")  # 5! = 120

# Using cumprod
factorials = np.cumprod(np.arange(1, 11))
print("Factorials:", factorials)
```

**Related Terms:** prod(), Permutation

---

### Geometric Mean

**Definition:** The nth root of the product of n values. Used as a measure of central tendency for rates and ratios.

**Example:**
```python
import numpy as np

data = np.array([2, 8, 4])

# Direct calculation
geo_mean = np.prod(data) ** (1/len(data))

# Using logarithms (more stable)
geo_mean_log = np.exp(np.mean(np.log(data)))

print(f"Geometric mean: {geo_mean:.4f}")
print(f"Geometric mean (log): {geo_mean_log:.4f}")
```

**Related Terms:** Arithmetic Mean, Logarithm

---

### Growth Factor

**Definition:** A multiplier representing growth. A value of 1.05 means 5% growth, 0.95 means 5% decline.

**Example:**
```python
import numpy as np

growth_factors = np.array([1.05, 0.98, 1.03])
cumulative_growth = np.prod(growth_factors)
print(f"Total growth: {cumulative_growth:.4f}x")
```

**Related Terms:** Compound Growth, Rate of Return

---

### Initial

**Definition:** A parameter specifying the starting value for cumulative operations. For products, typically set to 1 (multiplicative identity).

**Example:**
```python
import numpy as np

arr = np.array([2, 3, 4])
print(np.cumprod(arr, initial=1))
# Output: [ 1  2  6 24]
```

**Related Terms:** cumprod(), Identity Element

---

### Permutation

**Definition:** The number of ways to arrange r items from n items. Formula: P(n,r) = n! / (n-r)!. Uses factorials.

**Example:**
```python
import numpy as np

def permutation(n, r):
    return np.prod(np.arange(n - r + 1, n + 1))

print("P(5,3):", permutation(5, 3))  # 60
```

**Related Terms:** Factorial, Combination

---

### Principal

**Definition:** The initial amount of money invested or borrowed, before interest is applied.

**Example:**
```python
import numpy as np

principal = 10000
rate = 0.05
years = 10

final = principal * np.prod(np.ones(years) * (1 + rate))
print(f"Final: ${final:.2f}")
```

**Related Terms:** Compound Interest, Rate

---

### prod()

**Definition:** Calculates the total product of all array elements along a specified axis.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print("Product:", np.prod(arr))  # 120

arr2d = np.array([[1, 2], [3, 4]])
print("Product axis=0:", arr2d.prod(axis=0))  # [3 8]
print("Product axis=1:", arr2d.prod(axis=1))  # [2 12]
```

**Related Terms:** cumprod(), sum()

---

### Rate of Return

**Definition:** The gain or loss of an investment over a period, expressed as a percentage. Growth factor = 1 + rate.

**Example:**
```python
import numpy as np

returns = np.array([0.05, -0.02, 0.08])  # 5%, -2%, 8%
growth_factors = 1 + returns
total_return = np.prod(growth_factors) - 1
print(f"Total return: {total_return:.2%}")
```

**Related Terms:** Growth Factor, Compound Interest

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| Compound Growth | Exponential growth | `np.cumprod(returns)` |
| Compound Interest | Interest on interest | `P * ∏(1+r)` |
| cumprod() | Cumulative product | `np.cumprod(arr)` |
| Factorial | Product of 1 to n | `np.prod(np.arange(1, n+1))` |
| Geometric Mean | nth root of product | `np.prod(x)**(1/n)` |
| Growth Factor | Multiplier for growth | `1 + rate` |
| Initial | Starting value | `np.cumprod(arr, initial=1)` |
| Permutation | Arrangement count | `n! / (n-r)!` |
| Principal | Initial investment | Starting amount |
| prod() | Total product | `np.prod(arr)` |
| Rate of Return | Investment gain/loss | `final/initial - 1` |

---

**Back to Lecture:** [25 - Product Ufuncs](25-ufunc-products-lecture.md)
