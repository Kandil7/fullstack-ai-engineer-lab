# Glossary: Summation Ufuncs (Lecture 24)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| sum() | `np.sum(arr)` | Total sum of array |
| cumsum() | `np.cumsum(arr)` | Cumulative sum |
| nansum() | `np.nansum(arr)` | Sum ignoring NaN |
| axis | Parameter | Sum along axis (0=rows, 1=cols) |
| where | Parameter | Sum where condition True |
| initial | Parameter | Starting value for cumsum |
| Moving Average | Calculation | Rolling window average |
| Running Total | cumsum result | Cumulative sum |
| Weighted Sum | `np.average(arr, weights=w)` | Weighted average |

---

## Detailed Definitions

### axis

**Definition:** A parameter that specifies the direction along which to perform summation. axis=0 operates along rows, axis=1 along columns.

**Example:**
```python
import numpy as np

arr2d = np.array([[1, 2, 3], [4, 5, 6]])

print("Sum axis=0:", arr2d.sum(axis=0))  # [5 7 9]
print("Sum axis=1:", arr2d.sum(axis=1))  # [6 15]
```

**Related Terms:** Broadcasting, Shape

---

### cumsum()

**Definition:** Calculates the cumulative sum of array elements. Returns an array of the same size with running totals.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(np.cumsum(arr))
# Output: [ 1  3  6 10 15]
```

**Related Terms:** sum(), cumprod()

---

### initial

**Definition:** A parameter that specifies the starting value for cumulative operations. Prepended to the result.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(np.cumsum(arr, initial=0))
# Output: [ 0  1  3  6 10 15]

print(np.cumsum(arr, initial=100))
# Output: [100 101 103 106 110 115]
```

**Related Terms:** cumsum(), where

---

### Moving Average

**Definition:** A calculation that creates a series of averages of different subsets of the full dataset. Used for smoothing time series data.

**Example:**
```python
import numpy as np

def moving_average(arr, window):
    cumsum = np.cumsum(arr)
    cumsum = np.insert(cumsum, 0, 0)
    return (cumsum[window:] - cumsum[:-window]) / window

data = np.array([10, 12, 11, 13, 14, 12, 15])
ma3 = moving_average(data, 3)
print("3-day MA:", ma3.round(2))
```

**Related Terms:** cumsum(), Rolling Window

---

### nansum()

**Definition:** Calculates the sum of array elements, ignoring NaN values.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, np.nan, 4, 5])
print("sum:", np.sum(arr))        # nan
print("nansum:", np.nansum(arr))  # 12.0
```

**Related Terms:** sum(), nanmean()

---

### Rolling Window

**Definition:** A fixed-size window that moves across data, used for calculating rolling statistics like moving averages.

**Example:**
```python
import numpy as np

def rolling_mean(arr, window):
    cumsum = np.cumsum(arr)
    cumsum = np.insert(cumsum, 0, 0)
    return (cumsum[window:] - cumsum[:-window]) / window

data = np.array([1, 2, 3, 4, 5, 6, 7])
print("Rolling mean (window=3):", rolling_mean(data, 3))
```

**Related Terms:** Moving Average, cumsum()

---

### Running Total

**Definition:** A cumulative sum that shows the total at each point in a sequence.

**Example:**
```python
import numpy as np

sales = np.array([100, 150, 120, 180, 90])
running_total = np.cumsum(sales)
print("Running total:", running_total)
# Output: [100 250 370 550 640]
```

**Related Terms:** cumsum(), Total

---

### sum()

**Definition:** Calculates the total sum of all array elements along a specified axis.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print("Total:", np.sum(arr))  # 15

arr2d = np.array([[1, 2], [3, 4]])
print("Sum axis=0:", arr2d.sum(axis=0))  # [4 6]
print("Sum axis=1:", arr2d.sum(axis=1))  # [3 7]
```

**Related Terms:** cumsum(), mean()

---

### Total

**Definition:** The sum of all elements in an array.

**Example:**
```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])
total = np.sum(arr)
print(f"Total: {total}")  # 150
```

**Related Terms:** sum(), Average

---

### where

**Definition:** A parameter that specifies a condition for conditional summation. Only elements where the condition is True are included in the sum.

**Example:**
```python
import numpy as np

arr = np.array([-5, 10, -15, 20, -25])
print("Sum where positive:", np.sum(arr, where=arr > 0))
# Output: 30
```

**Related Terms:** Boolean Indexing, Conditional

---

### Weighted Average

**Definition:** An average where different values contribute differently based on their weights.

**Example:**
```python
import numpy as np

values = np.array([85, 92, 78, 95])
weights = np.array([0.2, 0.3, 0.2, 0.3])

weighted_avg = np.average(values, weights=weights)
print("Weighted average:", weighted_avg)
```

**Related Terms:** average(), weights

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| axis | Direction of operation | `arr.sum(axis=0)` |
| cumsum() | Cumulative sum | `np.cumsum(arr)` |
| initial | Starting value | `np.cumsum(arr, initial=0)` |
| Moving Average | Rolling window average | `moving_average(data, 3)` |
| nansum() | Sum ignoring NaN | `np.nansum(arr)` |
| Rolling Window | Fixed-size subset | Rolling statistics |
| Running Total | Cumulative sum | `np.cumsum(sales)` |
| sum() | Total sum | `np.sum(arr)` |
| where | Conditional sum | `np.sum(arr, where=cond)` |
| Weighted Average | Weighted mean | `np.average(arr, weights=w)` |

---

**Back to Lecture:** [24 - Summation Ufuncs](24-ufunc-summations-lecture.md)
