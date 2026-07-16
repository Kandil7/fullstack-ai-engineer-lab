# Lecture 24: Summation Ufuncs in NumPy

## Topic Overview

Summation operations are fundamental in data analysis, statistics, and mathematics. NumPy provides `np.sum()` for total summation and `np.cumsum()` for cumulative summation, along with parameters like `axis`, `where`, and `initial` for fine-grained control. These operations are essential for calculating totals, running averages, cumulative statistics, and more.

Understanding axis-based summation is crucial for working with multi-dimensional arrays effectively.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `np.sum()` to calculate total sums of arrays
2. Apply summation along specific axes in 2D+ arrays
3. Use `np.cumsum()` for cumulative summation
4. Filter summation using boolean masks
5. Use `where` parameter to sum only certain elements
6. Use `initial` parameter to add starting values
7. Calculate running totals and moving averages
8. Apply summation to practical data analysis scenarios
9. Handle NaN values with `np.nansum()`
10. Understand axis semantics for multi-dimensional arrays

---

## Key Concepts

### 1. Basic Sum

```python
import numpy as np

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
```

**Axis semantics:**
- `axis=0`: Sum along rows (result has same columns)
- `axis=1`: Sum along columns (result has same rows)

### 2. Sum with Mask

```python
import numpy as np

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
```

### 3. Cumulative Sum

```python
import numpy as np

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
```

### 4. Summation with Initial and Where

```python
import numpy as np

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
```

### 5. Practical Summation Examples

```python
import numpy as np

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
```

---

## Code Examples with Explanations

### Example 1: Axis-based Summation

```python
import numpy as np

# 3D array example
arr3d = np.array([[[1, 2], [3, 4]],
                  [[5, 6], [7, 8]],
                  [[9, 10], [11, 12]]])

print("3D Array shape:", arr3d.shape)
print(arr3d)

# Sum along different axes
print("\nSum all:", arr3d.sum())
print("Sum axis=0:", arr3d.sum(axis=0))  # Sum across layers
print("Sum axis=1:", arr3d.sum(axis=1))  # Sum across rows
print("Sum axis=2:", arr3d.sum(axis=2))  # Sum across columns

# Multiple axes
print("\nSum axes 0,1:", arr3d.sum(axis=(0, 1)))
```

### Example 2: Weighted Summation

```python
import numpy as np

# Calculate weighted average
grades = np.array([85, 92, 78, 95, 88])
weights = np.array([0.2, 0.25, 0.15, 0.25, 0.15])

# Weighted sum
weighted_sum = np.sum(grades * weights)
print(f"Weighted sum: {weighted_sum}")

# Weighted average
weighted_avg = np.average(grades, weights=weights)
print(f"Weighted average: {weighted_avg:.2f}")

# Using sum for verification
print(f"Verification: {np.sum(grades * weights) / np.sum(weights):.2f}")
```

### Example 3: Moving Average with cumsum

```python
import numpy as np

def moving_average(data, window_size):
    """Calculate moving average using cumsum for efficiency."""
    cumsum = np.cumsum(data)
    cumsum = np.insert(cumsum, 0, 0)
    return (cumsum[window_size:] - cumsum[:-window_size]) / window_size

# Stock prices
prices = np.array([100, 102, 101, 103, 105, 104, 106, 108, 107, 109])

# Calculate different moving averages
ma3 = moving_average(prices, 3)
ma5 = moving_average(prices, 5)

print("Prices:", prices)
print(f"3-day MA: {ma3.round(2)}")
print(f"5-day MA: {ma5.round(2)}")
```

### Example 4: Running Statistics

```python
import numpy as np

np.random.seed(42)
data = np.random.randn(100).cumsum()

# Calculate running statistics
running_sum = np.cumsum(data)
running_mean = running_sum / np.arange(1, len(data) + 1)

print(f"Final sum: {data.sum():.2f}")
print(f"Final mean: {data.mean():.2f}")
print(f"Running mean (first 10): {running_mean[:10].round(2)}")
```

### Example 5: Conditional Cumulative Sum

```python
import numpy as np

# Sales data with promotions
sales = np.array([100, 120, 80, 150, 90, 200, 110])
promotions = np.array([0, 1, 0, 1, 0, 1, 0])  # 1 = promoted

# Cumulative sales during promotions
promo_sales = np.where(promotions, sales, 0)
cumulative_promo = np.cumsum(promo_sales)

print("Sales:", sales)
print("Promotions:", promotions)
print("Promo sales:", promo_sales)
print("Cumulative promo sales:", cumulative_promo)
```

---

## Common Mistakes to Avoid

### Mistake 1: Confusing Axis Semantics

```python
import numpy as np

arr2d = np.array([[1, 2, 3], [4, 5, 6]])

# axis=0 sums DOWN columns
print("axis=0:", arr2d.sum(axis=0))  # [5 7 9]

# axis=1 sums ACROSS rows
print("axis=1:", arr2d.sum(axis=1))  # [6 15]
```

### Mistake 2: Not Handling NaN

```python
import numpy as np

arr = np.array([1, 2, np.nan, 4, 5])

# NaN propagates
print("sum:", np.sum(arr))  # nan

# Use nansum
print("nansum:", np.nansum(arr))  # 12.0
```

### Mistake 3: Forgetting Initial Value

```python
import numpy as np

# Want cumulative sum starting from 0
arr = np.array([1, 2, 3, 4, 5])

# WRONG - Missing initial 0
print(np.cumsum(arr))  # [ 1  3  6 10 15]

# CORRECT - Include initial 0
print(np.cumsum(arr, initial=0))  # [ 0  1  3  6 10 15]
```

---

## Best Practices

### 1. Use Axis Parameter for Multi-dimensional Arrays

```python
import numpy as np

arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Sum along specific axis
row_sums = arr2d.sum(axis=1)
col_sums = arr2d.sum(axis=0)
```

### 2. Use nansum for Data with Missing Values

```python
import numpy as np

arr = np.array([1, 2, np.nan, 4, 5])
total = np.nansum(arr)  # 12.0
```

### 3. Use cumsum for Running Totals

```python
import numpy as np

arr = np.array([100, 200, 150, 300, 250])
running_total = np.cumsum(arr)
```

### 4. Use where for Conditional Summation

```python
import numpy as np

arr = np.array([-5, 10, -15, 20, -25])
positive_sum = np.sum(arr, where=arr > 0)
```

---

## Practice Exercises

### Exercise 1: Basic Summation

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# TODO: Calculate total sum
total = np.sum(arr)
print("Total:", total)

# TODO: Calculate sum of even numbers
even_sum = np.sum(arr[arr % 2 == 0])
print("Even sum:", even_sum)
```

### Exercise 2: Axis Summation

```python
import numpy as np

arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# TODO: Sum along rows (axis=1)
row_sums = arr2d.sum(axis=1)
print("Row sums:", row_sums)

# TODO: Sum along columns (axis=0)
col_sums = arr2d.sum(axis=0)
print("Col sums:", col_sums)
```

### Exercise 3: Cumulative Sum

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# TODO: Calculate cumulative sum
cumsum = np.cumsum(arr)
print("Cumsum:", cumsum)

# TODO: Calculate cumulative sum with initial 0
cumsum_init = np.cumsum(arr, initial=0)
print("Cumsum with 0:", cumsum_init)
```

---

## Summary

| Function | Description |
|----------|-------------|
| **np.sum()** | Total sum of array |
| **np.cumsum()** | Cumulative sum |
| **np.nansum()** | Sum ignoring NaN |
| **axis** | Sum along specific axis |
| **where** | Sum only where condition True |
| **initial** | Starting value for cumsum |

---

**Next Lecture:** [25 - Product Ufuncs](25-ufunc-products-lecture.md)
