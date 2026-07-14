# Lecture 19: Introduction to Universal Functions (ufuncs)

## Topic Overview

Universal functions (ufuncs) are functions that operate element-wise on NumPy arrays. They are the backbone of NumPy's vectorized operations, providing fast, efficient computation without explicit Python loops. Ufuncs include mathematical operations (add, multiply, sqrt), comparison operations (greater, less), and many others.

Understanding ufuncs is essential for writing efficient NumPy code. They leverage low-level optimizations to perform operations much faster than equivalent Python loops.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what ufuncs are and why they're important
2. Use common ufuncs for mathematical operations
3. Apply ufuncs for element-wise operations on arrays
4. Use comparison ufuncs for array comparisons
5. Apply absolute value and rounding ufuncs
6. Understand ufunc methods: reduce, accumulate, outer
7. Distinguish between ufuncs and regular functions
8. Apply ufuncs to real-world data processing scenarios
9. Recognize the performance benefits of ufuncs over loops
10. Create arrays of ufunc results efficiently

---

## Key Concepts

### 1. What is a ufunc?

A **universal function** (ufunc) is a function that operates element-wise on an array. It takes one or more arrays as input and returns an array as output.

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Math operations are ufuncs
print("sqrt:", np.sqrt(arr))        # [1.   1.41 1.73 2.   2.24]
print("log:", np.log(arr))          # [0.   0.69 1.10 1.39 1.61]
print("exp:", np.exp(arr))          # [ 2.72  7.39 20.09 54.60 148.41]
print("sin:", np.sin(arr))          # [ 0.84  0.91  0.14 -0.76 -0.96]

# Compare with Python math
import math
print("\nPython math.sqrt(4):", math.sqrt(4))  # 2.0
print("NumPy np.sqrt(4):", np.sqrt(4))         # 2.0
print("NumPy np.sqrt(arr):", np.sqrt(arr))     # [1. 1.41 1.73 2. 2.24]
```

**Key points:**
- Ufuncs operate element-wise automatically
- They work on individual values OR entire arrays
- Much faster than Python loops (vectorization)

### 2. Types of Ufuncs

NumPy provides ufuncs in several categories:

```python
import numpy as np

arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([5, 4, 3, 2, 1])

# Arithmetic ufuncs
print("\nadd:", np.add(arr1, arr2))        # [6 6 6 6 6]
print("subtract:", np.subtract(arr1, arr2)) # [-4 -2  0  2  4]
print("multiply:", np.multiply(arr1, arr2)) # [5 8 9 8 5]
print("divide:", np.divide(arr1, arr2))     # [0.2 0.5 1.0 2.0 5.0]
print("power:", np.power(arr1, 2))          # [ 1  4  9 16 25]
print("mod:", np.mod(arr1, 2))              # [1 0 1 0 1]

# Comparison ufuncs
print("\ngreater:", np.greater(arr1, arr2))       # [False False False True True]
print("less:", np.less(arr1, arr2))               # [True True False False False]
print("equal:", np.equal(arr1, arr2))             # [False False True False False]
print("not_equal:", np.not_equal(arr1, arr2))     # [True True False True True]
```

### 3. Absolute Values

```python
import numpy as np

arr = np.array([-3, -2, -1, 0, 1, 2, 3])

# Absolute values
print("\nabs():", np.abs(arr))           # [3 2 1 0 1 2 3]
print("absolute():", np.absolute(arr))  # [3 2 1 0 1 2 3]

# With complex numbers
arr_complex = np.array([1+2j, 3-4j, -5+0j])
print("abs(complex):", np.abs(arr_complex))  # [2.24 5.   5.  ]
```

### 4. Rounding Functions

```python
import numpy as np

arr = np.array([1.2, 2.5, 3.7, -1.3, -2.8, 4.0])

print("\nOriginal:", arr)
print("round():", np.round(arr))        # [ 1.  2.  4. -1. -3.  4.]
print("ceil():", np.ceil(arr))          # [ 2.  3.  4. -1. -2.  4.]
print("floor():", np.floor(arr))        # [ 1.  2.  3. -2. -3.  4.]
print("trunc():", np.trunc(arr))        # [ 1.  2.  3. -1. -2.  4.]

# Round to specific decimals
arr2 = np.array([1.2345, 2.3456, 3.4567])
print("\nRound to 2 decimals:", np.round(arr2, 2))  # [1.23 2.35 3.46]
print("Round to 1 decimal:", np.round(arr2, 1))    # [1.2 2.3 3.5]
```

### 5. Ufunc Methods

Ufuncs have special methods for advanced operations:

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# reduce - apply operation to reduce array to single value
print("\nreduce (add):", np.add.reduce(arr))   # 15 (1+2+3+4+5)
print("reduce (multiply):", np.multiply.reduce(arr))  # 120

# accumulate - running total
print("\naccumulate (add):", np.add.accumulate(arr))  # [ 1  3  6 10 15]
print("accumulate (multiply):", np.multiply.accumulate(arr))  # [  1   2   6  24 120]

# outer - outer product
a = np.array([1, 2, 3])
b = np.array([4, 5])
print("\nouter (add):\n", np.add.outer(a, b))
# [[5 6]
#  [6 7]
#  [7 8]]

print("\nouter (multiply):\n", np.multiply.outer(a, b))
# [[ 4  5]
#  [ 8 10]
#  [12 15]]
```

---

## Code Examples with Explanations

### Example 1: Ufuncs vs Python Loops

```python
import numpy as np
import time

# Create large array
arr = np.arange(1000000)

# Method 1: Python loop (slow)
start = time.time()
result_loop = []
for x in arr:
    result_loop.append(np.sqrt(x))
loop_time = time.time() - start

# Method 2: NumPy ufunc (fast)
start = time.time()
result_ufunc = np.sqrt(arr)
ufunc_time = time.time() - start

print(f"Python loop: {loop_time:.4f}s")
print(f"NumPy ufunc: {ufunc_time:.4f}s")
print(f"Speedup: {loop_time/ufunc_time:.1f}x faster")
# Typical output:
# Python loop: 0.2500s
# NumPy ufunc: 0.0030s
# Speedup: ~80x faster
```

### Example 2: Arithmetic Operations

```python
import numpy as np

# Array arithmetic
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print("Addition:")
print(f"  a + b = {a + b}")
print(f"  np.add(a, b) = {np.add(a, b)}")

print("\nSubtraction:")
print(f"  a - b = {a - b}")
print(f"  np.subtract(a, b) = {np.subtract(a, b)}")

print("\nMultiplication:")
print(f"  a * b = {a * b}")
print(f"  np.multiply(a, b) = {np.multiply(a, b)}")

print("\nDivision:")
print(f"  a / b = {a / b}")
print(f"  np.divide(a, b) = {np.divide(a, b)}")

print("\nPower:")
print(f"  a ** 2 = {a ** 2}")
print(f"  np.power(a, 2) = {np.power(a, 2)}")
```

### Example 3: Comparison Operations

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Comparison operations
print("Array:", arr)
print("Greater than 25:", arr > 25)
print("Less than or equal 30:", arr <= 30)
print("Equal to 30:", arr == 30)
print("Not equal to 30:", arr != 30)

# Using ufunc form
print("\nUsing ufuncs:")
print("np.greater(arr, 25):", np.greater(arr, 25))
print("np.less_equal(arr, 30):", np.less_equal(arr, 30))

# Filtering with comparisons
filtered = arr[arr > 25]
print("\nElements > 25:", filtered)
```

### Example 4: Rounding Operations

```python
import numpy as np

prices = np.array([19.999, 29.995, 49.994, 99.991])

print("Original prices:", prices)
print("Rounded to 2 decimals:", np.round(prices, 2))
print("Rounded to integer:", np.round(prices).astype(int))

# Floor vs ceil
arr = np.array([1.1, 1.5, 1.9, -1.1, -1.5, -1.9])
print("\nOriginal:", arr)
print("floor():", np.floor(arr))  # Round down
print("ceil():", np.ceil(arr))    # Round up
print("trunc():", np.trunc(arr))  # Truncate toward zero
```

### Example 5: Ufunc Methods

```python
import numpy as np

# Reduce operation
arr = np.array([1, 2, 3, 4, 5])
print("Sum (reduce):", np.add.reduce(arr))        # 15
print("Product (reduce):", np.multiply.reduce(arr))  # 120

# Accumulate operation
print("\nCumulative sum:", np.add.accumulate(arr))      # [ 1  3  6 10 15]
print("Cumulative product:", np.multiply.accumulate(arr))  # [  1   2   6  24 120]

# Outer operation
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("\nOuter addition:\n", np.add.outer(a, b))
print("Outer multiplication:\n", np.multiply.outer(a, b))
```

---

## Common Mistakes to Avoid

### Mistake 1: Using Python Operators Instead of Ufuncs

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Both work, but ufuncs are more explicit
result1 = arr * 2
result2 = np.multiply(arr, 2)

# Ufuncs can have additional parameters
result3 = np.multiply(arr, 2, where=arr > 2)
```

### Mistake 2: Forgetting Element-wise Behavior

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# WRONG - Matrix multiplication
# result = np.dot(a, b)  # This is dot product, not element-wise

# CORRECT - Element-wise multiplication
result = np.multiply(a, b)
print(result)  # [ 4 10 18]
```

### Mistake 3: Not Handling NaN Values

```python
import numpy as np

arr = np.array([1, 2, np.nan, 4, 5])

# NaN propagates through operations
print("sum with NaN:", np.sum(arr))  # nan

# Use nan-safe versions
print("nansum:", np.nansum(arr))  # 12.0
```

---

## Best Practices

### 1. Use Ufuncs Instead of Loops

```python
import numpy as np

# Slow: Python loop
arr = np.arange(1000000)
result = []
for x in arr:
    result.append(x ** 2)

# Fast: NumPy ufunc
result = np.square(arr)  # or arr ** 2
```

### 2. Chain Ufunc Operations

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Chain operations
result = np.sqrt(np.abs(arr))  # Square root of absolute values
print(result)
```

### 3. Use Where for Conditional Operations

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Conditional operation
result = np.where(arr > 3, arr * 2, arr)
print(result)  # [1 2 3 8 10]
```

---

## Practice Exercises

### Exercise 1: Basic Ufuncs

```python
import numpy as np

arr = np.array([1, 4, 9, 16, 25])

# TODO: Calculate square root
sqrt_arr = np.sqrt(arr)
print("Square root:", sqrt_arr)

# TODO: Calculate natural log
log_arr = np.log(arr)
print("Natural log:", log_arr)

# TODO: Calculate exponential
exp_arr = np.exp(arr)
print("Exponential:", exp_arr)
```

### Exercise 2: Arithmetic Operations

```python
import numpy as np

a = np.array([10, 20, 30, 40, 50])
b = np.array([5, 10, 15, 20, 25])

# TODO: Add arrays
add_result = np.add(a, b)
print("Add:", add_result)

# TODO: Multiply arrays
mul_result = np.multiply(a, b)
print("Multiply:", mul_result)

# TODO: Calculate power
power_result = np.power(a, 2)
print("Power:", power_result)
```

### Exercise 3: Comparison Operations

```python
import numpy as np

arr = np.array([15, 25, 35, 45, 55])

# TODO: Find elements greater than 30
greater = arr[arr > 30]
print("Greater than 30:", greater)

# TODO: Count elements less than 40
count = np.sum(arr < 40)
print("Count < 40:", count)

# TODO: Check if any element equals 25
has_25 = np.any(arr == 25)
print("Has 25:", has_25)
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **ufunc** | Function that operates element-wise on arrays |
| **Arithmetic** | add, subtract, multiply, divide, power |
| **Comparison** | greater, less, equal, not_equal |
| **Math** | sqrt, log, exp, sin, cos |
| **Rounding** | round, floor, ceil, trunc |
| **Absolute** | abs, absolute |
| **Methods** | reduce, accumulate, outer |
| **Vectorization** | Element-wise operations without loops |

---

## Quick Reference

```python
import numpy as np

# Arithmetic
np.add(a, b)        # a + b
np.subtract(a, b)   # a - b
np.multiply(a, b)   # a * b
np.divide(a, b)     # a / b
np.power(a, b)      # a ** b
np.mod(a, b)        # a % b

# Comparison
np.greater(a, b)    # a > b
np.less(a, b)       # a < b
np.equal(a, b)      # a == b
np.not_equal(a, b)  # a != b

# Math
np.sqrt(arr)        # Square root
np.log(arr)         # Natural log
np.log2(arr)        # Log base 2
np.log10(arr)       # Log base 10
np.exp(arr)         # e^x
np.sin(arr)         # Sine
np.cos(arr)         # Cosine

# Rounding
np.round(arr, n)    # Round to n decimals
np.floor(arr)       # Round down
np.ceil(arr)        # Round up
np.trunc(arr)       # Truncate

# Absolute
np.abs(arr)         # Absolute value

# Methods
np.add.reduce(arr)           # Sum
np.multiply.reduce(arr)      # Product
np.add.accumulate(arr)       # Cumulative sum
np.add.outer(a, b)          # Outer sum
```

---

**Next Lecture:** [20 - Creating Custom Ufuncs](20-ufunc-create-lecture.md)
