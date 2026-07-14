# Lecture 21: Arithmetic Ufuncs in NumPy

## Topic Overview

Arithmetic ufuncs are the mathematical building blocks of NumPy, providing element-wise operations for addition, subtraction, multiplication, division, and power. These operations are fundamental to array computations and leverage NumPy's vectorization for optimal performance. Understanding arithmetic ufuncs is essential for performing mathematical operations on arrays efficiently.

This lecture covers all arithmetic ufuncs, their operators, broadcasting behavior, and practical applications in data processing and mathematical computations.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use addition ufuncs (`np.add()`) and the `+` operator
2. Use subtraction ufuncs (`np.subtract()`) and the `-` operator
3. Use multiplication ufuncs (`np.multiply()`) and the `*` operator
4. Use division ufuncs (`np.divide()`, `np.floor_divide()`) and operators
5. Use power ufuncs (`np.power()`) and the `**` operator
6. Apply modulo operations (`np.mod()`, `np.remainder()`)
7. Use square root and cube root functions
8. Handle division by zero and special values
9. Apply arithmetic operations with broadcasting
10. Use matrix multiplication (`np.matmul()`, `np.dot()`)

---

## Key Concepts

### 1. Addition

```python
import numpy as np

arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([10, 20, 30, 40, 50])

# Using ufunc
print("add():", np.add(arr1, arr2))       # [11 22 33 44 55]

# Using operator
print("arr1 + arr2:", arr1 + arr2)        # [11 22 33 44 55]

# Scalar addition
print("arr1 + 10:", arr1 + 10)            # [11 12 13 14 15]
print("np.add(arr1, 10):", np.add(arr1, 10))

# With different shapes (broadcasting)
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
arr_1d = np.array([10, 20, 30])
print("\n2D + 1D:\n", arr_2d + arr_1d)
# Output:
# [[11 22 33]
#  [14 25 36]]
```

### 2. Subtraction

```python
import numpy as np

arr1 = np.array([10, 20, 30, 40, 50])
arr2 = np.array([1, 2, 3, 4, 5])

# Using ufunc
print("\nsubtract():", np.subtract(arr1, arr2))  # [ 9 18 27 36 45]

# Using operator
print("arr1 - arr2:", arr1 - arr2)                # [ 9 18 27 36 45]

# Scalar subtraction
print("arr1 - 5:", arr1 - 5)                      # [ 5 15 25 35 45]

# Negation
print("negative:", np.negative(arr1))             # [-10 -20 -30 -40 -50]
print("-arr1:", -arr1)                            # [-10 -20 -30 -40 -50]
```

### 3. Multiplication

```python
import numpy as np

arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([10, 20, 30, 40, 50])

# Using ufunc
print("\nmultiply():", np.multiply(arr1, arr2))   # [ 10  40  90 160 250]

# Using operator
print("arr1 * arr2:", arr1 * arr2)                # [ 10  40  90 160 250]

# Scalar multiplication
print("arr1 * 3:", arr1 * 3)                      # [ 3  6  9 12 15]

# Matrix multiplication
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print("\nMatrix multiply:\n", np.matmul(a, b))
# [[19 22]
#  [43 50]]

# Dot product
print("Dot product:", np.dot(arr1, arr2))  # 550 (1*10 + 2*20 + ...)
```

### 4. Division

```python
import numpy as np

arr1 = np.array([10, 20, 30, 40, 50])
arr2 = np.array([2, 4, 5, 8, 10])

# True division (float result)
print("\ndivide():", np.divide(arr1, arr2))     # [5. 5. 6. 5. 5.]
print("arr1 / arr2:", arr1 / arr2)              # [5. 5. 6. 5. 5.]

# Floor division (integer result)
print("floor_divide():", np.floor_divide(arr1, arr2))  # [5 5 6 5 5]
print("arr1 // arr2:", arr1 // arr2)                    # [5 5 6 5 5]

# Modulus
print("mod():", np.mod(arr1, arr2))             # [0 0 0 0 0]
print("arr1 % arr2:", arr1 % arr2)              # [0 0 0 0 0]

# Remainder
print("remainder():", np.remainder(arr1, arr2))

# Division by zero handling
arr_zero = np.array([1, 0, 1])
with np.errstate(divide='ignore', invalid='ignore'):
    result = np.divide(arr1[:3], arr_zero)
    print("\nDivision by zero:", result)  # [10. inf nan]
```

### 5. Power and Modulo

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Power
print("\npower():", np.power(arr, 2))     # [ 1  4  9 16 25]
print("arr ** 2:", arr ** 2)              # [ 1  4  9 16 25]
print("power(3):", np.power(arr, 3))      # [  1   8  27  64 125]

# Square root
print("sqrt():", np.sqrt(arr))            # [1.   1.41 1.73 2.   2.24]

# Cube root
print("cbrt():", np.cbrt(arr))            # [1.    1.26 1.44 1.59 1.71]

# Modulo
arr1 = np.array([10, 15, 20, 25, 30])
arr2 = np.array([3, 4, 6, 7, 8])
print("\nmod():", np.mod(arr1, arr2))      # [1 3 2 4 6]
print("arr1 % arr2:", arr1 % arr2)        # [1 3 2 4 6]

# Practical: check even/odd
print("\nEven/odd:", np.where(arr % 2 == 0, "even", "odd"))
```

---

## Code Examples with Explanations

### Example 1: Element-wise Operations

```python
import numpy as np

# Two arrays
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print("Array a:", a)
print("Array b:", b)

# All arithmetic operations
print("\nAddition (a + b):", a + b)
print("Subtraction (a - b):", a - b)
print("Multiplication (a * b):", a * b)
print("Division (a / b):", a / b)
print("Floor Division (a // b):", a // b)
print("Modulo (a % b):", a % b)
print("Power (a ** 2):", a ** 2)
```

### Example 2: Scalar Operations

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print("Original:", arr)
print("Add 10:", arr + 10)
print("Subtract 5:", arr - 5)
print("Multiply by 3:", arr * 3)
print("Divide by 2:", arr / 2)
print("Power of 2:", arr ** 2)
print("Modulo 2:", arr % 2)
```

### Example 3: Broadcasting

```python
import numpy as np

# 2D array + 1D array
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
arr1d = np.array([10, 20, 30])

print("2D array:\n", arr2d)
print("1D array:", arr1d)

# Broadcasting: 1D added to each row
result = arr2d + arr1d
print("\n2D + 1D:\n", result)
# Output:
# [[11 22 33]
#  [14 25 36]
#  [17 28 39]]

# Broadcasting: scalar
result = arr2d * 2
print("\n2D * 2:\n", result)
```

### Example 4: Division by Zero Handling

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
zero_arr = np.array([1, 0, 1, 0, 1])

# Default behavior - raises warning
# result = arr / zero_arr

# Suppress warnings and handle special values
with np.errstate(divide='ignore', invalid='ignore'):
    result = arr / zero_arr
    print("Division by zero:", result)
    # Output: [ 1. inf  3. inf  5.]
    
    # Replace inf and nan
    result_clean = np.where(np.isinf(result), 0, result)
    result_clean = np.where(np.isnan(result_clean), 0, result_clean)
    print("Cleaned:", result_clean)
```

### Example 5: Matrix Operations

```python
import numpy as np

# Matrix multiplication
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

print("Matrix A:\n", a)
print("Matrix B:\n", b)

# Different ways to do matrix multiplication
print("\nnp.matmul(A, B):\n", np.matmul(a, b))
print("np.dot(A, B):\n", np.dot(a, b))
print("A @ B:\n", a @ b)

# Vector dot product
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
print("\nDot product:", np.dot(x, y))  # 32
```

---

## Common Mistakes to Avoid

### Mistake 1: Confusing Element-wise and Matrix Multiplication

```python
import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# WRONG - Element-wise multiplication
print("Element-wise:", a * b)
# [[ 5 12]
#  [21 32]]

# CORRECT - Matrix multiplication
print("Matrix multiply:", np.matmul(a, b))
# [[19 22]
#  [43 50]]
```

### Mistake 2: Integer Division Truncation

```python
import numpy as np

a = np.array([7, 15, 23])
b = np.array([2, 4, 5])

# Integer division truncates
print("Floor division:", a // b)  # [3 3 4]

# True division gives float
print("True division:", a / b)    # [3.5 3.75 4.6]
```

### Mistake 3: Not Handling Division by Zero

```python
import numpy as np

arr = np.array([1, 2, 3])
zero = np.array([1, 0, 1])

# CORRECT - Handle explicitly
with np.errstate(divide='ignore', invalid='ignore'):
    result = np.divide(arr, zero)
    result = np.where(np.isinf(result), np.nan, result)
```

---

## Best Practices

### 1. Use Operators for Simple Operations

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Simple operations - use operators
sum_result = a + b
diff_result = a - b
prod_result = a * b
```

### 2. Use Ufuncs When You Need Additional Parameters

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Ufunc form allows where parameter
result = np.add(a, b, where=a > 1)
```

### 3. Use errstate for Division

```python
import numpy as np

# Safely handle division by zero
with np.errstate(divide='ignore', invalid='ignore'):
    result = np.divide(arr1, arr2)
    result = np.where(np.isinf(result), np.nan, result)
```

### 4. Document Matrix vs Element-wise

```python
import numpy as np

# Element-wise multiplication
element_wise = a * b

# Matrix multiplication
matrix_product = a @ b  # or np.matmul(a, b)
```

---

## Practice Exercises

### Exercise 1: Basic Arithmetic

```python
import numpy as np

a = np.array([10, 20, 30, 40, 50])
b = np.array([5, 10, 15, 20, 25])

# TODO: Add arrays
add_result = a + b
print("Add:", add_result)

# TODO: Subtract arrays
sub_result = a - b
print("Subtract:", sub_result)

# TODO: Multiply arrays
mul_result = a * b
print("Multiply:", mul_result)
```

### Exercise 2: Division Operations

```python
import numpy as np

a = np.array([10, 20, 25, 30])
b = np.array([3, 4, 5, 6])

# TODO: True division
true_div = a / b
print("True division:", true_div)

# TODO: Floor division
floor_div = a // b
print("Floor division:", floor_div)

# TODO: Modulo
mod_result = a % b
print("Modulo:", mod_result)
```

### Exercise 3: Power Operations

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# TODO: Square each element
squares = arr ** 2
print("Squares:", squares)

# TODO: Cube each element
cubes = arr ** 3
print("Cubes:", cubes)

# TODO: Square root
sqrt_arr = np.sqrt(arr)
print("Square roots:", sqrt_arr.round(2))
```

---

## Summary

| Operation | Ufunc | Operator | Description |
|-----------|-------|----------|-------------|
| Addition | `np.add()` | `+` | Element-wise sum |
| Subtraction | `np.subtract()` | `-` | Element-wise difference |
| Multiplication | `np.multiply()` | `*` | Element-wise product |
| Division | `np.divide()` | `/` | Element-wise division |
| Floor Divide | `np.floor_divide()` | `//` | Integer division |
| Modulo | `np.mod()` | `%` | Remainder |
| Power | `np.power()` | `**` | Exponentiation |
| Negative | `np.negative()` | `-` | Negate elements |
| Square Root | `np.sqrt()` | - | √x |
| Cube Root | `np.cbrt()` | - | ∛x |
| Matrix Multiply | `np.matmul()` | `@` | Matrix product |
| Dot Product | `np.dot()` | - | Vector dot product |

---

**Next Lecture:** [22 - Rounding Ufuncs](22-ufunc-rounding-lecture.md)
