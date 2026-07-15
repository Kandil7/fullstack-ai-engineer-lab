# Lecture 26: Difference Ufuncs in NumPy

## Topic Overview

The difference operation (discrete derivative) calculates the difference between consecutive elements in an array. NumPy's `np.diff()` function is essential for analyzing changes, detecting edges, computing velocities from positions, and performing discrete calculus. This lecture covers diff operations along axes, higher-order differences, and practical applications in data analysis.

Understanding diff operations is crucial for time series analysis, signal processing, and numerical computations.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `np.diff()` to calculate first-order differences
2. Apply `n` parameter for higher-order differences
3. Use `axis` parameter for multi-dimensional arrays
4. Use `prepend` and `append` to control diff output
5. Reconstruct arrays from their differences
6. Apply diff to velocity and acceleration calculations
7. Detect edges and transitions in data
8. Use diff for price change analysis
9. Understand the relationship between diff and cumsum
10. Apply diff operations to practical scenarios

---

## Key Concepts

### 1. Basic Difference

```python
import numpy as np

arr = np.array([10, 15, 25, 40, 60])

# First order difference
print("Original:", arr)
print("diff():", np.diff(arr))  # [ 5 10 15 20]
# Explanation: [15-10, 25-15, 40-25, 60-40]

# Second order difference (diff of diff)
print("diff(2):", np.diff(arr, n=2))  # [5 5 5]

# Verify: second diff is constant for quadratic sequence
arr2 = np.array([1, 4, 9, 16, 25])  # n^2
print("\nn^2 sequence:", arr2)
print("First diff:", np.diff(arr2))    # [3 5 7 9]
print("Second diff:", np.diff(arr2, n=2))  # [2 2 2]
```

**Key points:**
- `np.diff(arr)` returns array of length `len(arr) - 1`
- `n=2` applies diff twice
- Second diff of quadratic sequence is constant

### 2. Differences Along Axis

```python
import numpy as np

arr2d = np.array([[1, 2, 3, 4],
                  [5, 7, 9, 11],
                  [10, 14, 18, 22]])

print("\n2D Array:\n", arr2d)

# Diff along rows (axis=1)
print("\nDiff axis=1 (columns):\n", np.diff(arr2d, axis=1))
# [[1 1 1]
#  [2 2 2]
#  [4 4 4]]

# Diff along columns (axis=0)
print("\nDiff axis=0 (rows):\n", np.diff(arr2d, axis=0))
# [[4 5 6 7]
#  [5 7 9 11]]

# Second order diff
print("\nSecond diff axis=1:\n", np.diff(arr2d, n=2, axis=1))
# [[0 0]
#  [0 0]
#  [0 0]]
```

### 3. Differences with Prepend/Append

```python
import numpy as np

arr = np.array([10, 20, 35, 55, 80])

# Basic diff
print("\nOriginal:", arr)
print("diff():", np.diff(arr))  # [10 15 20 25]

# Prepend a value to diff
diff_with_start = np.diff(arr, prepend=0)
print("diff(prepend=0):", diff_with_start)  # [10 10 15 20 25]

# Append a value
diff_with_end = np.diff(arr, append=100)
print("diff(append=100):", diff_with_end)  # [10 15 20 25 20]

# Both prepend and append
diff_both = np.diff(arr, prepend=0, append=100)
print("diff(prepend=0, append=100):", diff_both)

# Practical: reconstruct array from diff
original = np.array([10, 20, 35, 55, 80])
diffs = np.diff(original)
reconstructed = np.concatenate([[original[0]], np.cumsum(diffs)])
print("\nOriginal:", original)
print("Diff:", diffs)
print("Reconstructed:", reconstructed)
print("Match:", np.array_equal(original, reconstructed))
```

### 4. Practical Applications

```python
import numpy as np

# Velocity from position
time = np.array([0, 1, 2, 3, 4, 5])  # seconds
position = np.array([0, 5, 20, 45, 80, 125])  # meters

velocity = np.diff(position) / np.diff(time)
print("\nPosition:", position)
print("Velocity (m/s):", velocity)  # [5 15 25 35 45]

# Acceleration from velocity
acceleration = np.diff(velocity) / np.diff(time[:-1])
print("Acceleration (m/s^2):", acceleration)  # [10 10 10 10]

# Daily price changes
prices = np.array([100, 102, 101, 105, 103, 108])
changes = np.diff(prices)
percent_changes = np.diff(prices) / prices[:-1] * 100
print("\nPrices:", prices)
print("Changes:", changes)
print("Percent changes:", percent_changes.round(2))
```

### 5. Edge Detection with diff

```python
import numpy as np

# Step function
signal = np.array([0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0])
print("\nSignal:", signal)
print("diff:", np.diff(signal))
# [0 0 1 0 0 0 -1 0 0 1 0 -1 0]

# Find transitions
diff_signal = np.diff(signal)
rise_edges = np.where(diff_signal == 1)[0] + 1
fall_edges = np.where(diff_signal == -1)[0] + 1
print("Rise edges at:", rise_edges)  # [3 10]
print("Fall edges at:", fall_edges)  # [7 12]

# Cumulative sum to reconstruct
print("\nCumulative sum:", np.concatenate([[0], np.cumsum(diff_signal)]))
# [0 0 0 1 1 1 1 0 0 0 1 1 0 0]

# Detect monotonic increase
data = np.array([1, 2, 3, 4, 5, 4, 3, 2, 3, 4, 5, 6])
diffs = np.diff(data)
is_increasing = np.all(diffs > 0)
print(f"\nData: {data}")
print(f"Is monotonically increasing: {is_increasing}")
```

---

## Code Examples with Explanations

### Example 1: Higher-Order Differences

```python
import numpy as np

# Polynomial sequences
n = np.arange(6)

# Linear: n
linear = n.copy()
# Quadratic: n^2
quadratic = n ** 2
# Cubic: n^3
cubic = n ** 3

print("Sequence | 1st diff | 2nd diff | 3rd diff")
print("-" * 50)

for name, seq in [("Linear", linear), ("Quadratic", quadratic), ("Cubic", cubic)]:
    d1 = np.diff(seq)
    d2 = np.diff(seq, n=2)
    d3 = np.diff(seq, n=3)
    print(f"{name:<10} | {str(d1):<10} | {str(d2):<10} | {str(d3)}")
```

### Example 2: Time Series Analysis

```python
import numpy as np

# Daily stock prices
prices = np.array([100, 102, 101, 105, 108, 103, 110, 115, 112, 118])

# Calculate changes
daily_change = np.diff(prices)
percent_change = np.diff(prices) / prices[:-1] * 100

print("Prices:", prices)
print("Daily changes:", daily_change)
print("Percent changes:", percent_change.round(2))

# Detect trends
increasing_days = np.sum(daily_change > 0)
decreasing_days = np.sum(daily_change < 0)
print(f"\nIncreasing days: {increasing_days}")
print(f"Decreasing days: {decreasing_days}")
```

### Example 3: Velocity and Acceleration

```python
import numpy as np

# Position data (meters)
time = np.array([0, 1, 2, 3, 4, 5])
position = np.array([0, 10, 25, 45, 70, 100])

# Calculate velocity (first derivative)
velocity = np.diff(position) / np.diff(time)

# Calculate acceleration (second derivative)
acceleration = np.diff(velocity) / np.diff(time[:-1])

print("Time:", time)
print("Position:", position)
print("Velocity (m/s):", velocity)
print("Acceleration (m/s^2):", acceleration)
```

### Example 4: Signal Processing

```python
import numpy as np

# Noisy signal
np.random.seed(42)
clean_signal = np.sin(np.linspace(0, 4*np.pi, 100))
noisy_signal = clean_signal + np.random.randn(100) * 0.3

# Edge detection using diff
edges = np.diff(noisy_signal)
threshold = 0.1
edge_points = np.where(np.abs(edges) > threshold)[0]

print(f"Signal length: {len(noisy_signal)}")
print(f"Edge points detected: {len(edge_points)}")
```

### Example 5: Reconstructing Arrays

```python
import numpy as np

# Given diff and first element, reconstruct original
first_element = 5
diffs = np.array([3, 5, 7, 9, 11])

# Reconstruct using cumsum
reconstructed = np.concatenate([[first_element], np.cumsum(diffs)])

print("First element:", first_element)
print("Diffs:", diffs)
print("Reconstructed:", reconstructed)

# Verify
original = np.array([5, 8, 13, 20, 29, 40])
print("Original:", original)
print("Match:", np.array_equal(original, reconstructed))
```

---

## Common Mistakes to Avoid

### Mistake 1: Length Mismatch

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# diff returns shorter array!
diff = np.diff(arr)
print(f"Original length: {len(arr)}")
print(f"Diff length: {len(diff)}")
# Output: Original length: 5, Diff length: 4
```

### Mistake 2: Forgetting Axis in 2D

```python
import numpy as np

arr2d = np.array([[1, 2, 3], [4, 5, 6]])

# Default axis is -1 (last axis, i.e., columns)
print("Default diff:\n", np.diff(arr2d))
# Explicit axis=1 (same as default)
print("Axis=1:\n", np.diff(arr2d, axis=1))
# Axis=0 (rows)
print("Axis=0:\n", np.diff(arr2d, axis=0))
```

### Mistake 3: Not Handling Edge Cases

```python
import numpy import np

# Empty array
empty = np.array([])
# diff(empty) would fail

# Single element
single = np.array([5])
# diff(single) returns empty array

# Handle gracefully
if len(arr) > 1:
    diffs = np.diff(arr)
```

---

## Best Practices

### 1. Use Prepend/Append for Same Length

```python
import numpy as np

arr = np.array([10, 20, 35, 55, 80])

# Same length as original
diff_same_length = np.diff(arr, prepend=0)
```

### 2. Use n Parameter for Higher Orders

```python
import numpy as np

arr = np.array([1, 4, 9, 16, 25])

# Second order diff directly
second_diff = np.diff(arr, n=2)
```

### 3. Combine with Other Operations

```python
import numpy as np

prices = np.array([100, 102, 101, 105, 103, 108])

# Percent changes
pct_changes = np.diff(prices) / prices[:-1] * 100

# Cumulative returns
cumulative = np.cumprod(1 + pct_changes/100) - 1
```

---

## Practice Exercises

### Exercise 1: Basic Differences

```python
import numpy as np

arr = np.array([10, 15, 25, 40, 60])

# TODO: Calculate first difference
first_diff = np.diff(arr)
print("First diff:", first_diff)

# TODO: Calculate second difference
second_diff = np.diff(arr, n=2)
print("Second diff:", second_diff)
```

### Exercise 2: Velocity Calculation

```python
import numpy as np

time = np.array([0, 1, 2, 3, 4])
position = np.array([0, 10, 30, 60, 100])

# TODO: Calculate velocity
velocity = np.diff(position) / np.diff(time)
print("Velocity:", velocity)
```

### Exercise 3: Price Analysis

```python
import numpy as np

prices = np.array([100, 105, 103, 110, 108, 115])

# TODO: Calculate daily changes
changes = np.diff(prices)
print("Changes:", changes)

# TODO: Calculate percent changes
pct = np.diff(prices) / prices[:-1] * 100
print("Percent:", pct.round(2))
```

---

## Summary

| Function | Description |
|----------|-------------|
| **np.diff()** | Calculate n-th discrete difference |
| **n** | Order of difference |
| **axis** | Axis along which to diff |
| **prepend** | Values to prepend to diff |
| **append** | Values to append to diff |

---

**Next Lecture:** [27 - Trigonometric Ufuncs](27-ufunc-trigonometric-lecture.md)
