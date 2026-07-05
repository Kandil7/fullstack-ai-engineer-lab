# Lecture 22: Rounding Ufuncs in NumPy

## Topic Overview

Rounding operations are essential for controlling numerical precision in data processing. NumPy provides several rounding ufuncs: `round()` / `around()` for standard rounding, `floor()` for rounding down, `ceil()` for rounding up, and `trunc()` / `fix()` for truncation toward zero. Understanding the differences between these methods, especially for negative numbers, is crucial for accurate computations.

Rounding is commonly used in financial calculations, data visualization, reporting, and any scenario where numerical precision needs to be controlled.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `np.round()` / `np.around()` to round to nearest integer or decimal places
2. Use `np.floor()` to round down to nearest integer
3. Use `np.ceil()` to round up to nearest integer
4. Use `np.trunc()` / `np.fix()` to truncate toward zero
5. Understand Banker's rounding (round half to even)
6. Apply rounding to specific decimal places
7. Round to nearest 10, 100, etc. using negative decimals
8. Handle rounding differences between positive and negative numbers
9. Apply rounding in practical scenarios (currency, percentages, data binning)
10. Choose the appropriate rounding method for different use cases

---

## Key Concepts

### 1. Rounding to Nearest Integer

```python
import numpy as np

arr = np.array([1.2, 2.5, 3.7, 4.1, 5.5, 6.9])

print("Original:", arr)
print("round():", np.round(arr))       # [1. 2. 4. 4. 6. 7.]
print("around():", np.around(arr))     # [1. 2. 4. 4. 6. 7.]
```

**Key points:**
- `np.round()` and `np.around()` are identical
- Default rounds to 0 decimal places (nearest integer)
- Returns float array (not int)

### 2. Rounding to Specific Decimals

```python
import numpy as np

arr = np.array([1.2345, 2.3456, 3.4567])

print("\nRound to 2 decimals:", np.round(arr, 2))  # [1.23 2.35 3.46]
print("Round to 1 decimal:", np.round(arr, 1))    # [1.2 2.3 3.5]
print("Round to 0 decimals:", np.round(arr, 0))   # [1. 2. 3.]
```

### 3. Round to Nearest 10, 100

```python
import numpy as np

arr = np.array([12, 27, 33, 48, 55])

print("\nRound to nearest 10:", np.round(arr, -1))  # [10 30 30 50 60]

# Round to nearest 100
print("Round to nearest 100:", np.round(arr, -2))  # [  0   0   0   0 100]
```

### 4. Floor and Ceil

```python
import numpy as np

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
```

### 5. Truncation

```python
import numpy as np

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
```

### 6. Banker's Rounding

```python
import numpy as np

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
```

---

## Code Examples with Explanations

### Example 1: Rounding Methods Comparison

```python
import numpy as np

arr = np.array([1.5, 2.5, 3.5, 4.5, -1.5, -2.5])

print("Original:", arr)
print("round():", np.round(arr))
print("floor():", np.floor(arr))
print("ceil():", np.ceil(arr))
print("trunc():", np.trunc(arr))

# Show differences for negative numbers
neg = np.array([-1.1, -1.5, -1.9, -2.1, -2.5, -2.9])
print("\nNegative numbers:", neg)
print("round():", np.round(neg))
print("floor():", np.floor(neg))
print("ceil():", np.ceil(neg))
print("trunc():", np.trunc(neg))
```

### Example 2: Currency Rounding

```python
import numpy as np

# Prices with many decimals
prices = np.array([19.999, 29.995, 49.994, 99.991])

print("Original prices:", prices)
print("Rounded to 2 decimals:", np.round(prices, 2))

# Total calculation
total = prices.sum()
print(f"\nExact total: {total}")
print(f"Rounded total: {np.round(total, 2)}")
```

### Example 3: Percentage Rounding

```python
import numpy as np

scores = np.array([85.67, 92.34, 78.91, 95.00])

print("Scores:", scores)
print("Grades (rounded):", np.round(scores).astype(int))

# Calculate percentages
total = 100
percentages = scores / total * 100
print("\nPercentages:", np.round(percentages, 1))
```

### Example 4: Data Binning

```python
import numpy as np

# Round to nearest bin
data = np.array([1.2, 2.7, 3.4, 4.8, 5.1, 6.9])
bins = np.round(data / 2) * 2  # Round to nearest 2
print("Data:", data)
print("Binned to nearest 2:", bins)

# Round to nearest 5
data2 = np.array([12, 27, 33, 48, 55])
binned5 = np.round(data2 / 5) * 5
print("\nData:", data2)
print("Binned to nearest 5:", binned5)
```

### Example 5: Temperature Rounding

```python
import numpy as np

temps = np.array([20.4, 21.6, 22.5, 23.1])

print("Temperatures:", temps)
print("Rounded:", np.round(temps).astype(int))

# Different rounding strategies
print("\nFloor (conservative):", np.floor(temps).astype(int))
print("Ceil (aggressive):", np.ceil(temps).astype(int))
```

---

## Common Mistakes to Avoid

### Mistake 1: Assuming round() Always Rounds Up

```python
import numpy as np

# Banker's rounding rounds 0.5 to even
print("round(0.5):", np.round(0.5))  # 0.0, not 1.0!
print("round(1.5):", np.round(1.5))  # 2.0
print("round(2.5):", np.round(2.5))  # 2.0, not 3.0!
```

### Mistake 2: Confusing Floor and Trunc for Negatives

```python
import numpy as np

# For negative numbers, floor and trunc differ
print("floor(-1.7):", np.floor(-1.7))  # -2.0 (toward -inf)
print("trunc(-1.7):", np.trunc(-1.7))  # -1.0 (toward 0)
```

### Mistake 3: Forgetting Return Type

```python
import numpy as np

arr = np.array([1.2, 2.7, 3.5])

# round() returns float
result = np.round(arr)
print(result.dtype)  # float64

# Convert to int if needed
result_int = np.round(arr).astype(int)
```

---

## Best Practices

### 1. Choose the Right Rounding Method

```python
import numpy as np

arr = np.array([1.5, 2.5, 3.5, 4.5])

# For general rounding
print("round():", np.round(arr))

# For floor/ceiling
print("floor():", np.floor(arr))
print("ceil():", np.ceil(arr))

# For truncation
print("trunc():", np.trunc(arr))
```

### 2. Specify Decimal Places

```python
import numpy as np

arr = np.array([1.23456, 2.34567, 3.45678])

print("2 decimals:", np.round(arr, 2))
print("3 decimals:", np.round(arr, 3))
```

### 3. Convert to Int After Rounding

```python
import numpy as np

arr = np.array([1.2, 2.7, 3.5])

# Round then convert
result = np.round(arr).astype(int)
print(result)
```

---

## Practice Exercises

### Exercise 1: Basic Rounding

```python
import numpy as np

arr = np.array([1.2, 2.5, 3.7, 4.1, 5.5, 6.9])

# TODO: Round to nearest integer
rounded = np.round(arr)
print("Rounded:", rounded)

# TODO: Round to 1 decimal place
rounded_1 = np.round(arr, 1)
print("1 decimal:", rounded_1)
```

### Exercise 2: Floor and Ceil

```python
import numpy as np

arr = np.array([1.2, 2.5, 3.7, -1.3, -2.8, 4.0])

# TODO: Apply floor
floored = np.floor(arr)
print("Floor:", floored)

# TODO: Apply ceil
ceiled = np.ceil(arr)
print("Ceil:", ceiled)
```

### Exercise 3: Truncation

```python
import numpy as np

arr = np.array([1.9, 2.1, -3.7, -4.2, 5.5])

# TODO: Apply trunc
truncated = np.trunc(arr)
print("Trunc:", truncated)

# TODO: Compare with floor for negative numbers
print("Floor:", np.floor(arr))
```

---

## Summary

| Function | Description | Negative Behavior |
|----------|-------------|-------------------|
| **round()** | Round to nearest (Banker's) | 0.5 rounds to even |
| **floor()** | Round down | Toward -infinity |
| **ceil()** | Round up | Toward +infinity |
| **trunc()** | Truncate | Toward zero |
| **fix()** | Alias for trunc | Toward zero |

---

**Next Lecture:** [23 - Logarithmic Ufuncs](23-ufunc-logs-lecture.md)
