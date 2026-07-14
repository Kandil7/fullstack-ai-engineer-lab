# Glossary: Introduction to Universal Functions (Lecture 19)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| ufunc | Universal Function | Element-wise array function |
| add() | `np.add(a, b)` | Element-wise addition |
| subtract() | `np.subtract(a, b)` | Element-wise subtraction |
| multiply() | `np.multiply(a, b)` | Element-wise multiplication |
| divide() | `np.divide(a, b)` | Element-wise division |
| power() | `np.power(a, b)` | Element-wise power |
| sqrt() | `np.sqrt(arr)` | Square root |
| log() | `np.log(arr)` | Natural logarithm |
| exp() | `np.exp(arr)` | Exponential (e^x) |
| sin() | `np.sin(arr)` | Sine function |
| reduce() | `ufunc.reduce(arr)` | Reduce to single value |
| accumulate() | `ufunc.accumulate(arr)` | Running operation |
| outer() | `ufunc.outer(a, b)` | Outer product |

---

## Detailed Definitions

### Absolute Value

**Definition:** A ufunc that returns the absolute (non-negative) value of each element. Works with real and complex numbers.

**Example:**
```python
import numpy as np

arr = np.array([-3, -2, -1, 0, 1, 2, 3])
print(np.abs(arr))
# Output: [3 2 1 0 1 2 3]

# Complex numbers
complex_arr = np.array([1+2j, 3-4j])
print(np.abs(complex_arr))
# Output: [2.236 5.   ]
```

**Related Terms:** negate(), sign()

---

### Accumulate

**Definition:** A ufunc method that applies the operation cumulatively, returning an array of intermediate results. Similar to cumulative sum/product.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Cumulative sum
print(np.add.accumulate(arr))
# Output: [ 1  3  6 10 15]

# Cumulative product
print(np.multiply.accumulate(arr))
# Output: [  1   2   6  24 120]
```

**Related Terms:** reduce(), cumsum(), cumprod()

---

### Arithmetic Ufunc

**Definition:** A ufunc that performs basic mathematical operations (addition, subtraction, multiplication, division) on arrays element-wise.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print("Add:", np.add(a, b))
print("Subtract:", np.subtract(a, b))
print("Multiply:", np.multiply(a, b))
print("Divide:", np.divide(a, b))
```

**Related Terms:** Comparison Ufunc, Math Ufunc

---

### Comparison Ufunc

**Definition:** A ufunc that compares arrays element-wise and returns boolean arrays.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([5, 4, 3, 2, 1])

print("Greater:", np.greater(a, b))
print("Less:", np.less(a, b))
print("Equal:", np.equal(a, b))
print("Not equal:", np.not_equal(a, b))
```

**Related Terms:** Arithmetic Ufunc, Boolean Array

---

### Divide

**Definition:** Element-wise division of two arrays. Returns float results.

**Example:**
```python
import numpy as np

a = np.array([10, 20, 30])
b = np.array([2, 4, 5])

print(np.divide(a, b))
# Output: [5. 5. 6.]
```

**Related Terms:** floor_divide(), true_divide(), mod()

---

### Element-wise Operation

**Definition:** An operation that applies a function to each corresponding element of two or more arrays independently.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Element-wise addition
print(a + b)
# Output: [5 7 9]

# Element-wise multiplication
print(a * b)
# Output: [ 4 10 18]
```

**Related Terms:** Broadcasting, Vectorization

---

### Exponential

**Definition:** A ufunc that calculates e raised to the power of each element. Inverse of natural logarithm.

**Example:**
```python
import numpy as np

arr = np.array([0, 1, 2, 3, 4])
print(np.exp(arr))
# Output: [ 1.     2.718  7.389 20.086 54.598]
```

**Related Terms:** log(), exp2(), expm1()

---

### Floor

**Definition:** A ufunc that rounds each element down to the nearest integer. Always returns the largest integer less than or equal to the input.

**Example:**
```python
import numpy as np

arr = np.array([1.2, 2.5, 3.7, -1.3, -2.8])
print(np.floor(arr))
# Output: [ 1.  2.  3. -2. -3.]
```

**Related Terms:** ceil(), trunc(), round()

---

### Logarithm

**Definition:** A ufunc that calculates the logarithm of each element. Supports different bases (natural, base-2, base-10).

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 4, 8, 16])
print("Natural log:", np.log(arr))
print("Log base 2:", np.log2(arr))
print("Log base 10:", np.log10(arr))
```

**Related Terms:** exp(), log2(), log10(), log1p()

---

### Math Ufunc

**Definition:** A ufunc that performs mathematical functions (sqrt, log, exp, trigonometric) on arrays element-wise.

**Example:**
```python
import numpy as np

arr = np.array([1, 4, 9, 16, 25])
print("Square root:", np.sqrt(arr))
print("Natural log:", np.log(arr))
print("Sine:", np.sin(arr))
```

**Related Terms:** Arithmetic Ufunc, Trigonometric Ufunc

---

### Multiply

**Definition:** Element-wise multiplication of two arrays.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print(np.multiply(a, b))
# Output: [ 10  40  90 160 250]
```

**Related Terms:** add(), divide(), dot()

---

### Negate

**Definition:** A ufunc that negates each element (multiplies by -1).

**Example:**
```python
import numpy as np

arr = np.array([1, -2, 3, -4, 5])
print(np.negative(arr))
# Output: [-1  2 -3  4 -5]
```

**Related Terms:** absolute(), sign()

---

### Outer

**Definition:** A ufunc method that computes the operation between all pairs of elements from two arrays, producing a result array with shape (len(a), len(b)).

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5])

print("Outer add:\n", np.add.outer(a, b))
# Output:
# [[5 6]
#  [6 7]
#  [7 8]]

print("Outer multiply:\n", np.multiply.outer(a, b))
# Output:
# [[ 4  5]
#  [ 8 10]
#  [12 15]]
```

**Related Terms:** reduce(), accumulate(), dot()

---

### Power

**Definition:** Element-wise exponentiation of arrays.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
print(np.power(a, 2))
# Output: [ 1  4  9 16 25]

print(np.power(a, 3))
# Output: [  1   8  27  64 125]
```

**Related Terms:** sqrt(), square(), cube()

---

### Reduce

**Definition:** A ufunc method that applies the operation repeatedly to reduce the array to a single value.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print("Sum:", np.add.reduce(arr))
# Output: 15

print("Product:", np.multiply.reduce(arr))
# Output: 120

print("Max:", np.maximum.reduce(arr))
# Output: 5
```

**Related Terms:** accumulate(), sum(), prod()

---

### Rounding

**Definition:** Ufuncs that round numbers to specified precision. Includes round, floor, ceil, and trunc.

**Example:**
```python
import numpy as np

arr = np.array([1.2, 2.5, 3.7, -1.3, -2.8])

print("Round:", np.round(arr))
print("Floor:", np.floor(arr))
print("Ceil:", np.ceil(arr))
print("Trunc:", np.trunc(arr))
```

**Related Terms:** floor(), ceil(), trunc()

---

### Square Root

**Definition:** A ufunc that calculates the square root of each element.

**Example:**
```python
import numpy as np

arr = np.array([1, 4, 9, 16, 25])
print(np.sqrt(arr))
# Output: [1. 2. 3. 4. 5.]
```

**Related Terms:** power(), square(), cbrt()

---

### Subtract

**Definition:** Element-wise subtraction of two arrays.

**Example:**
```python
import numpy as np

a = np.array([10, 20, 30])
b = np.array([1, 2, 3])

print(np.subtract(a, b))
# Output: [ 9 18 27]
```

**Related Terms:** add(), multiply(), divide()

---

### Trigonometric Ufunc

**Definition:** A ufunc that performs trigonometric operations (sin, cos, tan, etc.) on arrays.

**Example:**
```python
import numpy as np

angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
print("Sin:", np.sin(angles))
print("Cos:", np.cos(angles))
print("Tan:", np.tan(angles))
```

**Related Terms:** arcsin(), arccos(), arctan(), radians(), degrees()

---

### Vectorization

**Definition:** The process of converting operations from element-by-element loops to array operations, leveraging ufuncs for performance.

**Example:**
```python
import numpy as np
import time

arr = np.arange(1000000)

# Slow: loop
start = time.time()
result1 = [x ** 2 for x in arr]
loop_time = time.time() - start

# Fast: vectorized
start = time.time()
result2 = arr ** 2
vector_time = time.time() - start

print(f"Loop: {loop_time:.4f}s, Vectorized: {vector_time:.4f}s")
```

**Related Terms:** Broadcasting, ufunc, Element-wise Operation

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| Absolute Value | Non-negative value | `np.abs(arr)` |
| Accumulate | Cumulative operation | `np.add.accumulate(arr)` |
| Arithmetic Ufunc | Basic math operations | `np.add(a, b)` |
| Comparison Ufunc | Element-wise comparison | `np.greater(a, b)` |
| Divide | Element-wise division | `np.divide(a, b)` |
| Element-wise | Per-element operation | `a + b` |
| Exponential | e^x calculation | `np.exp(arr)` |
| Floor | Round down | `np.floor(arr)` |
| Logarithm | Log calculation | `np.log(arr)` |
| Math Ufunc | Mathematical functions | `np.sqrt(arr)` |
| Multiply | Element-wise multiplication | `np.multiply(a, b)` |
| Negate | Multiply by -1 | `np.negative(arr)` |
| Outer | All pairs operation | `np.add.outer(a, b)` |
| Power | Element-wise exponentiation | `np.power(a, 2)` |
| Reduce | Reduce to single value | `np.add.reduce(arr)` |
| Rounding | Round to precision | `np.round(arr, 2)` |
| Square Root | √x calculation | `np.sqrt(arr)` |
| Subtract | Element-wise subtraction | `np.subtract(a, b)` |
| Trigonometric | Trig functions | `np.sin(arr)` |
| Vectorization | Loop to array conversion | `arr ** 2` |

---

**Back to Lecture:** [19 - Ufunc Introduction](19-ufunc-intro-lecture.md)
