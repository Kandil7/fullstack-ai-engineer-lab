# Lecture 15: Array Filtering in NumPy

## Topic Overview

Array filtering is the process of selecting specific elements from an array based on conditions or criteria. NumPy provides powerful tools for filtering arrays using boolean indexing, `np.where()`, `np.extract()`, and fancy indexing. This is one of the most frequently used operations in data analysis, enabling you to work with subsets of data that meet specific requirements.

Filtering is fundamental to data analysis workflows — you often need to select data points that meet certain thresholds, belong to specific categories, or satisfy multiple conditions simultaneously.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create boolean masks to filter array elements
2. Use boolean indexing to select elements based on conditions
3. Combine multiple conditions using logical operators (`&`, `|`, `~`)
4. Use `np.where()` for conditional element selection and replacement
5. Use `np.extract()` for complex filtering conditions
6. Apply filtering techniques to 2D arrays (rows and columns)
7. Use fancy indexing to select elements at specific positions
8. Combine filtering with element modification
9. Avoid common mistakes like using Python's `and`/`or` instead of `&`/`|`
10. Apply practical filtering patterns in data analysis

---

## Key Concepts

### 1. Boolean Masking

A **boolean mask** is an array of True/False values that corresponds element-wise to the original array. When you apply a comparison operator to a NumPy array, it returns a boolean array of the same shape.

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# Create a boolean mask
mask = arr > 50
print(mask)
# Output: [False False False False False  True  True  True  True  True]

# Apply mask to filter
filtered = arr[mask]
print(filtered)
# Output: [ 60  70  80  90 100]
```

**How it works:**
- The comparison `arr > 50` is applied element-wise
- Each element is compared to 50
- The result is a boolean array where `True` means the condition was met
- When used as an index, only `True` elements are selected

### 2. Boolean Indexing (Direct Filtering)

You can filter directly by embedding the condition inside the index brackets, without creating an intermediate mask variable.

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Direct boolean indexing
filtered = arr[arr > 5]
print(filtered)
# Output: [ 6  7  8  9 10]

# Works with any condition
even_filtered = arr[arr % 2 == 0]
print(even_filtered)
# Output: [ 2  4  6  8 10]
```

### 3. Combining Multiple Conditions

NumPy uses `&` for AND, `|` for OR, and `~` for NOT when combining conditions. **Important:** You must wrap each condition in parentheses due to operator precedence.

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# AND condition: both must be true
filtered = arr[(arr > 3) & (arr < 8)]
print(filtered)
# Output: [4 5 6 7]

# OR condition: either can be true
filtered = arr[(arr < 3) | (arr > 8)]
print(filtered)
# Output: [ 1  2  9 10]

# NOT condition: negates
filtered = arr[~(arr > 5)]
print(filtered)
# Output: [1 2 3 4 5]

# Multiple conditions
filtered = arr[(arr >= 2) & (arr <= 7) & (arr % 2 == 0)]
print(filtered)
# Output: [2 4 6]
```

### 4. np.where() — Conditional Selection

`np.where()` is a versatile function that returns elements chosen from `x` or `y` depending on `condition`.

**Three main use cases:**

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Use case 1: Get indices where condition is True
indices = np.where(arr % 2 == 0)
print(indices)
# Output: (array([1, 3, 5, 7, 9]),)

# Use case 2: Conditional replacement (ternary operator)
# Replace elements > 5 with 0, keep others
result = np.where(arr > 5, 0, arr)
print(result)
# Output: [ 1  2  3  4  5  0  0  0  0  0]

# Use case 3: Select from two arrays based on condition
x = np.array([10, 20, 30, 40, 50])
y = np.array([100, 200, 300, 400, 500])
result = np.where(arr > 5, x, y)
print(result)
# Output: [100 200 300 400 500  10  20  30  40  50]
```

### 5. np.extract() — Extract with Condition

`np.extract()` returns elements that satisfy a condition. It's similar to boolean indexing but always returns a 1D flattened array.

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Simple extraction
extracted = np.extract(arr > 5, arr)
print(extracted)
# Output: [ 6  7  8  9 10]

# Complex condition
mask = (arr % 3 == 0) & (arr > 4)
extracted = np.extract(mask, arr)
print(extracted)
# Output: [6 9]
```

### 6. Filtering 2D Arrays

Filtering 2D arrays can target rows, columns, or individual elements.

```python
arr2d = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 16]])

# Filter rows where sum > 20
row_sums = arr2d.sum(axis=1)
print("Row sums:", row_sums)
# Output: [10 26 42 58]

filtered_rows = arr2d[row_sums > 20]
print("Rows with sum > 20:\n", filtered_rows)
# Output:
# [[ 5  6  7  8]
#  [ 9 10 11 12]
#  [13 14 15 16]]

# Filter columns where mean > 8
col_means = arr2d.mean(axis=0)
print("Column means:", col_means)
# Output: [ 7.  8.  9. 10.]

filtered_cols = arr2d[:, col_means > 8]
print("Columns with mean > 8:\n", filtered_cols)
# Output:
# [[ 3  4]
#  [ 7  8]
#  [11 12]
#  [15 16]]

# Filter individual elements
mask = arr2d > 10
print("Elements > 10:", arr2d[mask])
# Output: [11 12 13 14 15 16]
```

### 7. Fancy Indexing

Fancy indexing allows you to select elements at specific positions using an array of indices.

```python
arr = np.array([10, 20, 30, 40, 50, 60, 70, 80])

# Select specific indices
indices = [0, 2, 4, 6]
filtered = arr[indices]
print(filtered)
# Output: [10 30 50 70]

# Random selection
random_indices = np.random.choice(len(arr), size=4, replace=False)
print("Random indices:", random_indices)
print("Random selection:", arr[random_indices])

# 2D fancy indexing
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
rows = np.array([0, 2])
cols = np.array([1, 2])
print("2D fancy indexing:", arr2d[rows, cols])
# Output: [2 9]
```

### 8. Filter and Modify

Combine filtering with assignment to modify elements that meet certain conditions.

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("Original:", arr)

# Replace elements meeting condition
arr[arr > 5] = 0
print("After arr>5=0:", arr)
# Output: [1 2 3 4 5 0 0 0 0 0]

# Replace with calculated values
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
arr[arr % 2 == 0] *= -1
print("Negate evens:", arr)
# Output: [ 1 -2  3 -4  5 -6  7 -8  9 -10]

# Conditional replacement with np.where
arr = np.array([10, 25, 30, 45, 50])
result = np.where(arr > 30, arr * 2, arr)
print("Double if > 30:", result)
# Output: [10 25 30 90 100]

# Clip values (limit range)
arr = np.array([1, 5, 10, 15, 20, 25, 30])
clipped = np.clip(arr, 5, 20)
print("Clipped [5,20]:", clipped)
# Output: [ 5  5 10 15 20 20 20]
```

---

## Code Examples with Explanations

### Example 1: Basic Boolean Filtering

```python
import numpy as np

# Create sample data
temperatures = np.array([18, 22, 25, 30, 35, 28, 20, 15, 32, 27])

# Find days with temperature above 25°C
hot_days = temperatures[temperatures > 25]
print("Hot days temperatures:", hot_days)
# Output: [30 35 28 32 27]

# Find days with comfortable temperature (18-25°C)
comfortable = temperatures[(temperatures >= 18) & (temperatures <= 25)]
print("Comfortable temperatures:", comfortable)
# Output: [18 22 25 20]

# Find extreme temperatures (below 18 or above 30)
extreme = temperatures[(temperatures < 18) | (temperatures > 30)]
print("Extreme temperatures:", extreme)
# Output: [35 15 32]
```

### Example 2: Using np.where for Conditional Operations

```python
import numpy as np

scores = np.array([85, 92, 78, 65, 45, 88, 72, 55])

# Assign grades based on scores
grades = np.where(scores >= 90, 'A',
         np.where(scores >= 80, 'B',
         np.where(scores >= 70, 'C',
         np.where(scores >= 60, 'D', 'F'))))
print("Grades:", grades)
# Output: ['B' 'A' 'C' 'D' 'F' 'B' 'C' 'F']

# Replace failing scores with 0
adjusted = np.where(scores >= 60, scores, 0)
print("Adjusted scores:", adjusted)
# Output: [85 92 78 65  0 88 72  0]

# Calculate bonus points for high scores
bonus = np.where(scores > 80, scores * 1.1, scores)
print("With bonus:", np.round(bonus, 1))
# Output: [ 85.  101.2  78.   65.   45.   96.8  72.   55. ]
```

### Example 3: Multi-Condition Filtering

```python
import numpy as np

# Student data: [name_id, score, attendance]
students = np.array([[1, 85, 90],
                     [2, 92, 95],
                     [3, 78, 85],
                     [4, 65, 70],
                     [5, 95, 88],
                     [6, 88, 92]])

scores = students[:, 1]
attendance = students[:, 2]

# Students with high scores AND good attendance
excellent = students[(scores >= 90) & (attendance >= 90)]
print("Excellent students:\n", excellent)
# Output:
# [[ 2 92 95]
#  [ 5 95 88]]

# Students who need improvement (low score OR low attendance)
needs_help = students[(scores < 80) | (attendance < 80)]
print("Need improvement:\n", needs_help)
# Output:
# [[ 4 65 70]]

# Students with good scores but poor attendance
good_but_absent = students[(scores >= 85) & (attendance < 85)]
print("Good scores, poor attendance:\n", good_but_absent)
# Output:
# [[ 5 95 88]]
```

### Example 4: Filtering 2D Arrays

```python
import numpy as np

# Sales data: [region, product, quantity, revenue]
sales = np.array([[1, 101, 50, 5000],
                  [1, 102, 30, 3600],
                  [2, 101, 70, 7000],
                  [2, 103, 45, 5400],
                  [3, 102, 60, 7200],
                  [3, 101, 25, 2500]])

# Filter by revenue > 5000
high_revenue = sales[sales[:, 3] > 5000]
print("High revenue sales:\n", high_revenue)
# Output:
# [[ 2 101   70 7000]
#  [ 3 102   60 7200]]

# Filter by multiple conditions
selected = sales[(sales[:, 0] == 1) & (sales[:, 3] > 4000)]
print("Region 1, revenue > 4000:\n", selected)
# Output:
# [[ 1 101   50 5000]]

# Calculate filtered statistics
region1_sales = sales[sales[:, 0] == 1]
print(f"Region 1 total revenue: {region1_sales[:, 3].sum()}")
# Output: Region 1 total revenue: 8600
```

---

## Common Mistakes to Avoid

### Mistake 1: Using Python `and`/`or` Instead of `&`/`|`

```python
# WRONG - This will raise an error
arr = np.array([1, 2, 3, 4, 5])
# filtered = arr[(arr > 2) and (arr < 4)]  # ValueError!

# CORRECT - Use & and | with parentheses
filtered = arr[(arr > 2) & (arr < 4)]
print(filtered)
# Output: [3]
```

### Mistake 2: Forgetting Parentheses Around Conditions

```python
# WRONG - Operator precedence issues
# filtered = arr[arr > 2 & arr < 4]  # Bitwise AND first!

# CORRECT - Wrap each condition in parentheses
filtered = arr[(arr > 2) & (arr < 4)]
print(filtered)
# Output: [3]
```

### Mistake 3: Modifying a View Instead of a Copy

```python
arr = np.array([1, 2, 3, 4, 5])

# This creates a view, not a copy
view = arr[arr > 2]
# view[0] = 100  # This would modify original array!

# If you need a modifiable copy
copy = arr[arr > 2].copy()
copy[0] = 100
print("Original:", arr)
print("Modified copy:", copy)
# Output:
# Original: [1 2 3 4 5]
# Modified copy: [100   4   5]
```

### Mistake 4: Using np.where Instead of Boolean Indexing for Simple Cases

```python
arr = np.array([1, 2, 3, 4, 5])

# Unnecessary use of np.where for simple filtering
# filtered = np.where(arr > 3)[0]  # Returns indices, not values

# Simpler and more direct
filtered = arr[arr > 3]
print(filtered)
# Output: [4 5]
```

### Mistake 5: Not Handling Empty Results

```python
arr = np.array([1, 2, 3, 4, 5])
filtered = arr[arr > 10]

# This could cause issues if you expect data
print("Filtered:", filtered)
print("Is empty:", len(filtered) == 0)

# Safe approach
if len(filtered) > 0:
    print("Mean:", filtered.mean())
else:
    print("No matching elements")
# Output:
# Filtered: []
# Is empty: True
# No matching elements
```

---

## Best Practices

### 1. Use Boolean Masks for Readability

```python
import numpy as np

data = np.random.randn(1000)

# Clear and readable
mask = data > 2
outliers = data[mask]

# Less readable (but works)
outliers = data[data > 2]
```

### 2. Store Complex Conditions in Variables

```python
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Clearer with named conditions
is_even = data % 2 == 0
in_range = (data >= 3) & (data <= 8)
filtered = data[is_even & in_range]
print(filtered)
# Output: [4 6 8]
```

### 3. Use np.where for Conditional Assignment

```python
arr = np.array([1, 2, 3, 4, 5])

# Use np.where when you need to assign different values
result = np.where(arr > 3, arr * 10, arr)
print(result)
# Output: [ 1  2  3 40 50]
```

### 4. Validate Filter Results

```python
arr = np.array([1, 2, 3, 4, 5])

# Always check if filter returned expected results
filtered = arr[arr > 10]
print(f"Expected non-empty, got {len(filtered)} elements")

# Use assertions for debugging
assert len(filtered) == 0, "Should be empty"
```

### 5. Consider Performance for Large Arrays

```python
import numpy as np
import time

# Create large array
large_arr = np.random.randn(1000000)

# Method 1: Boolean indexing (fast)
start = time.time()
result1 = large_arr[large_arr > 0]
print(f"Boolean indexing: {time.time() - start:.6f}s")

# Method 2: np.where (slightly slower for simple cases)
start = time.time()
result2 = large_arr[np.where(large_arr > 0)]
print(f"np.where: {time.time() - start:.6f}s")
```

---

## Practice Exercises

### Exercise 1: Basic Filtering

```python
import numpy as np

# Create array
arr = np.array([15, 22, 8, 42, 17, 35, 6, 28, 11, 50])

# TODO: Filter elements greater than 20
filtered = arr[arr > 20]
print("Elements > 20:", filtered)

# TODO: Filter even numbers
even = arr[arr % 2 == 0]
print("Even numbers:", even)

# TODO: Filter numbers between 10 and 30 (inclusive)
between = arr[(arr >= 10) & (arr <= 30)]
print("Between 10 and 30:", between)
```

### Exercise 2: Conditional Replacement

```python
import numpy as np

scores = np.array([85, 42, 91, 38, 76, 55, 88, 47, 63, 79])

# TODO: Replace failing scores (< 60) with 0
adjusted = np.where(scores >= 60, scores, 0)
print("Adjusted scores:", adjusted)

# TODO: Add 5 bonus points to scores > 80
with_bonus = np.where(scores > 80, scores + 5, scores)
print("With bonus:", with_bonus)

# TODO: Cap all scores at 100
capped = np.clip(scores, 0, 100)
print("Capped scores:", capped)
```

### Exercise 3: 2D Array Filtering

```python
import numpy as np

# Student data: [age, score, grade_points]
students = np.array([[20, 85, 3.5],
                     [22, 92, 3.8],
                     [19, 78, 3.0],
                     [21, 65, 2.5],
                     [23, 95, 3.9],
                     [20, 88, 3.6]])

# TODO: Find students with score > 85
high_scorers = students[students[:, 1] > 85]
print("High scorers:\n", high_scorers)

# TODO: Find students with GPA > 3.5
high_gpa = students[students[:, 2] > 3.5]
print("High GPA:\n", high_gpa)

# TODO: Find students aged 21 or younger with score > 80
young_high = students[(students[:, 0] <= 21) & (students[:, 1] > 80)]
print("Young high performers:\n", young_high)
```

### Exercise 4: Using np.where and np.extract

```python
import numpy as np

prices = np.array([19.99, 49.95, 12.50, 99.99, 25.00, 8.99])

# TODO: Replace prices > 50 with "expensive", others with "affordable"
labels = np.where(prices > 50, "expensive", "affordable")
print("Labels:", labels)

# TODO: Extract prices that are multiples of 5
# Hint: Use np.round to check divisibility
rounded = np.round(prices, 0)
multiples_of_5 = rounded[rounded % 5 == 0]
print("Multiples of 5:", multiples_of_5)

# TODO: Create a 10% discount for items under $20
discounted = np.where(prices < 20, prices * 0.9, prices)
print("Discounted prices:", np.round(discounted, 2))
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **Boolean Mask** | Array of True/False values from comparison operations |
| **Boolean Indexing** | `arr[mask]` or `arr[condition]` to filter elements |
| **AND (`&`)** | Both conditions must be true |
| **OR (`\|`)** | Either condition can be true |
| **NOT (`~`)** | Negates the condition |
| **np.where()** | Conditional selection: `np.where(condition, x, y)` |
| **np.extract()** | Extract elements matching condition (always 1D) |
| **Fancy Indexing** | Select elements at specific indices |
| **Clip** | `np.clip(arr, min, max)` limits values to range |
| **Masked Arrays** | `np.ma.masked_where()` for "transparent" masking |

---

## Quick Reference

```python
import numpy as np

# Basic filtering
filtered = arr[arr > threshold]

# Multiple conditions
filtered = arr[(cond1) & (cond2)]  # AND
filtered = arr[(cond1) | (cond2)]  # OR
filtered = arr[~(condition)]       # NOT

# Conditional replacement
result = np.where(condition, value_if_true, value_if_false)

# Extract elements
extracted = np.extract(condition, arr)

# Clip values
clipped = np.clip(arr, min_val, max_val)

# 2D filtering
filtered_rows = arr2d[row_mask]           # Filter rows
filtered_cols = arr2d[:, col_mask]        # Filter columns
filtered_elements = arr2d[element_mask]   # Filter elements
```

---

**Next Lecture:** [16 - Random Number Introduction](16-random-intro-lecture.md)
