# Glossary: Arithmetic Ufuncs (Lecture 21)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| add() | `np.add(a, b)` | Element-wise addition |
| subtract() | `np.subtract(a, b)` | Element-wise subtraction |
| multiply() | `np.multiply(a, b)` | Element-wise multiplication |
| divide() | `np.divide(a, b)` | Element-wise division |
| floor_divide() | `np.floor_divide(a, b)` | Integer division |
| mod() | `np.mod(a, b)` | Modulo (remainder) |
| power() | `np.power(a, b)` | Exponentiation |
| negative() | `np.negative(a)` | Negate elements |
| sqrt() | `np.sqrt(arr)` | Square root |
| cbrt() | `np.cbrt(arr)` | Cube root |
| matmul() | `np.matmul(a, b)` | Matrix multiplication |
| dot() | `np.dot(a, b)` | Dot product |

---

## Detailed Definitions

### add()

**Definition:** Element-wise addition of two arrays. Equivalent to the `+` operator.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print(np.add(a, b))
# Output: [11 22 33 44 55]

# With scalar
print(np.add(a, 10))
# Output: [11 12 13 14 15]
```

**Related Terms:** subtract(), multiply(), Broadcasting

---

### Broadcasting

**Definition:** NumPy's ability to perform operations on arrays of different shapes by automatically expanding the smaller array to match the larger one.

**Example:**
```python
import numpy as np

arr2d = np.array([[1, 2, 3],
                  [4, 5, 6]])
arr1d = np.array([10, 20, 30])

# Broadcasting: 1D added to each row
result = arr2d + arr1d
print(result)
# Output:
# [[11 22 33]
#  [14 25 36]]
```

**Related Terms:** add(), Scalar Operations

---

### cbrt()

**Definition:** Calculates the cube root of each element.

**Example:**
```python
import numpy as np

arr = np.array([1, 8, 27, 64, 125])
print(np.cbrt(arr))
# Output: [1. 2. 3. 4. 5.]
```

**Related Terms:** sqrt(), power()

---

### divide()

**Definition:** Element-wise true division, always returning float results.

**Example:**
```python
import numpy as np

a = np.array([10, 20, 30])
b = np.array([3, 4, 5])

print(np.divide(a, b))
# Output: [3.333 5.    6.   ]
```

**Related Terms:** floor_divide(), mod()

---

### Dot Product

**Definition:** The sum of element-wise products of two arrays. For 1D arrays, it's the scalar product.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(np.dot(a, b))
# Output: 32 (1*4 + 2*5 + 3*6)
```

**Related Terms:** matmul(), multiply()

---

### Element-wise Operation

**Definition:** An operation that applies a function to each corresponding element of arrays independently.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(a + b)  # [5 7 9]
print(a * b)  # [4 10 18]
```

**Related Terms:** Broadcasting, Vectorization

---

### floor_divide()

**Definition:** Element-wise floor division, truncating toward negative infinity. Returns integer results.

**Example:**
```python
import numpy as np

a = np.array([7, 15, 23])
b = np.array([2, 4, 5])

print(np.floor_divide(a, b))
# Output: [3 3 4]
```

**Related Terms:** divide(), mod()

---

### matmul()

**Definition:** Matrix multiplication. Computes the matrix product of two arrays.

**Example:**
```python
import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

print(np.matmul(a, b))
# Output:
# [[19 22]
#  [43 50]]
```

**Related Terms:** dot(), @ operator

---

### mod()

**Definition:** Element-wise modulo operation. Returns the remainder after division.

**Example:**
```python
import numpy as np

a = np.array([10, 15, 20])
b = np.array([3, 4, 6])

print(np.mod(a, b))
# Output: [1 3 2]
```

**Related Terms:** floor_divide(), remainder()

---

### multiply()

**Definition:** Element-wise multiplication of two arrays. Equivalent to the `*` operator.

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

### negative()

**Definition:** Negates each element (multiplies by -1).

**Example:**
```python
import numpy as np

arr = np.array([1, -2, 3, -4, 5])
print(np.negative(arr))
# Output: [-1  2 -3  4 -5]
```

**Related Terms:** absolute(), sign()

---

### Power

**Definition:** Element-wise exponentiation. Raises each element to the specified power.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(np.power(arr, 2))
# Output: [ 1  4  9 16 25]

print(np.power(arr, 3))
# Output: [  1   8  27  64 125]
```

**Related Terms:** sqrt(), square()

---

### remainder()

**Definition:** Alias for mod(). Returns the remainder after division.

**Example:**
```python
import numpy as np

a = np.array([10, 15, 20])
b = np.array([3, 4, 6])

print(np.remainder(a, b))
# Output: [1 3 2]
```

**Related Terms:** mod(), floor_divide()

---

### Scalar Operations

**Definition:** Operations between an array and a single value (scalar). The scalar is applied to each element.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print(arr + 10)   # [11 12 13 14 15]
print(arr * 2)    # [ 2  4  6  8 10]
print(arr ** 2)   # [ 1  4  9 16 25]
```

**Related Terms:** Broadcasting, Element-wise Operation

---

### sqrt()

**Definition:** Calculates the square root of each element.

**Example:**
```python
import numpy as np

arr = np.array([1, 4, 9, 16, 25])
print(np.sqrt(arr))
# Output: [1. 2. 3. 4. 5.]
```

**Related Terms:** cbrt(), power()

---

### subtract()

**Definition:** Element-wise subtraction of two arrays. Equivalent to the `-` operator.

**Example:**
```python
import numpy as np

a = np.array([10, 20, 30])
b = np.array([1, 2, 3])

print(np.subtract(a, b))
# Output: [ 9 18 27]
```

**Related Terms:** add(), multiply()

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
result1 = [x * 2 for x in arr]
loop_time = time.time() - start

# Fast: vectorized
start = time.time()
result2 = arr * 2
vector_time = time.time() - start

print(f"Loop: {loop_time:.4f}s, Vectorized: {vector_time:.4f}s")
```

**Related Terms:** ufunc, Element-wise Operation

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| add() | Element-wise addition | `np.add(a, b)` |
| Broadcasting | Auto-expand smaller array | `arr2d + arr1d` |
| cbrt() | Cube root | `np.cbrt(arr)` |
| divide() | Element-wise division | `np.divide(a, b)` |
| Dot Product | Sum of element-wise products | `np.dot(a, b)` |
| Element-wise | Per-element operation | `a + b` |
| floor_divide() | Integer division | `np.floor_divide(a, b)` |
| matmul() | Matrix multiplication | `np.matmul(a, b)` |
| mod() | Remainder | `np.mod(a, b)` |
| multiply() | Element-wise multiplication | `np.multiply(a, b)` |
| negative() | Negate elements | `np.negative(arr)` |
| Power | Exponentiation | `np.power(a, 2)` |
| remainder() | Alias for mod | `np.remainder(a, b)` |
| Scalar Operations | Array + scalar | `arr * 2` |
| sqrt() | Square root | `np.sqrt(arr)` |
| subtract() | Element-wise subtraction | `np.subtract(a, b)` |
| Vectorization | Loop to array conversion | `arr * 2` |

---

**Back to Lecture:** [21 - Arithmetic Ufuncs](21-ufunc-arithmetic-lecture.md)
