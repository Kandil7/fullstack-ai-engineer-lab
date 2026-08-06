# NumPy Lecture 03: Creating Arrays in Detail

## 🎯 Topic Overview

This lecture dives deep into every method for creating NumPy arrays. You'll master the art of array initialization with precise control over data types, shapes, memory layout, and content. Understanding these creation methods is fundamental to efficient NumPy usage.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Create arrays from Python data structures (lists, tuples, generators)
2. Use all built-in array creation functions
3. Control array dtype and memory layout
4. Create arrays from files and buffers
5. Use NumPy's random module for various distributions
6. Understand array memory allocation and initialization
7. Choose the right creation method for each use case

---

## 1. Creating Arrays from Python Data Structures

### 1.1 From Python Lists

```python
import numpy as np

# 1D array
arr = np.array([1, 2, 3, 4, 5])
print(arr)  # [1 2 3 4 5]

# 2D array — nested lists
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
print(matrix)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]

# 3D array
tensor = np.array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]]])
print(tensor.shape)  # (2, 2, 2)

# Explicit dtype
arr_float = np.array([1, 2, 3], dtype=np.float64)
arr_int = np.array([1.5, 2.5, 3.5], dtype=np.int32)
```

### 1.2 From Python Tuples

```python
# Tuples work identically to lists
arr = np.array((1, 2, 3, 4, 5))
print(arr)  # [1 2 3 4 5]

# Nested tuples
matrix = np.array(((1, 2, 3), (4, 5, 6)))
print(matrix)
```

### 1.3 From Generators and Iterators

```python
# From a generator
gen = (x**2 for x in range(5))
arr = np.fromiter(gen, dtype=int)
print(arr)  # [ 0  1  4  9 16]

# From a list comprehension
arr = np.array([x**2 for x in range(5)])
print(arr)  # [ 0  1  4  9 16]
```

### 1.4 Type Coercion Rules

```python
# All integers → int
arr = np.array([1, 2, 3])
print(arr.dtype)  # int64

# Mixed int/float → float
arr = np.array([1, 2.5, 3])
print(arr.dtype)  # float64

# Integers and strings → string
arr = np.array([1, "hello", 3])
print(arr.dtype)  # <U21

# Booleans stay bool
arr = np.array([True, False, True])
print(arr.dtype)  # bool

# Complex numbers
arr = np.array([1+2j, 3+4j])
print(arr.dtype)  # complex128
```

---

## 2. Built-in Array Creation Functions

### 2.1 Zeros, Ones, Empty, Full

```python
# Zeros — all elements = 0
z1 = np.zeros(5)           # [0. 0. 0. 0. 0.]
z2 = np.zeros((3, 4))      # 3×4 matrix of zeros
z3 = np.zeros(5, dtype=int) # Integer zeros

# Ones — all elements = 1
o1 = np.ones(5)            # [1. 1. 1. 1. 1.]
o2 = np.ones((3, 4))       # 3×4 matrix of ones
o3 = np.ones(5, dtype=bool) # Boolean True

# Empty — uninitialized (garbage values)
e = np.empty(5)            # Undefined values!

# Full — fill with a specific value
f1 = np.full(5, 7)          # [7 7 7 7 7]
f2 = np.full((3, 3), 3.14)  # 3×3 matrix of π
f3 = np.full((2, 3), "hi", dtype=object)
```

### 2.2 Arange — Like range() for Arrays

```python
# Basic arange
arr = np.arange(10)         # [0 1 2 3 4 5 6 7 8 9]

# With start, stop, step
arr = np.arange(0, 10, 2)   # [0 2 4 6 8]
arr = np.arange(10, 0, -1)  # [10 9 8 7 6 5 4 3 2 1]

# With float step
arr = np.arange(0, 1, 0.25) # [0.   0.25 0.5  0.75]

# WARNING: Float step can cause precision issues
arr = np.arange(0, 1, 0.1)
print(len(arr))  # Might be 9 or 10 due to floating point!
```

### 2.3 Linspace — Evenly Spaced Numbers

```python
# 5 numbers from 0 to 10 (inclusive)
arr = np.linspace(0, 10, 5)
print(arr)  # [ 0.   2.5  5.   7.5 10. ]

# Without endpoint
arr = np.linspace(0, 10, 5, endpoint=False)
print(arr)  # [0. 2. 4. 6. 8.]

# Get the step size
arr, step = np.linspace(0, 10, 5, retstep=True)
print(f"Step: {step}")  # 2.5

# Log-spaced (using formula)
arr = np.logspace(0, 3, 4)  # [1. 10. 100. 1000.]
```

### 2.4 Identity and Diagonal Arrays

```python
# Identity matrix
I = np.eye(3)
print(I)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]

# Rectangular identity
I_rect = np.eye(3, 5)
print(I_rect)
# [[1. 0. 0. 0. 0.]
#  [0. 1. 0. 0. 0.]
#  [0. 0. 1. 0. 0.]]

# With offset k
I_upper = np.eye(4, k=1)   # Upper diagonal
I_lower = np.eye(4, k=-1)  # Lower diagonal

# Diagonal from vector
v = np.array([1, 2, 3, 4])
D = np.diag(v)
print(D)
# [[1 0 0 0]
#  [0 2 0 0]
#  [0 0 3 0]
#  [0 0 0 4]]

# Extract diagonal from matrix
M = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
d = np.diag(M)
print(d)  # [1 5 9]
```

### 2.5 Triangular Arrays

```python
# Lower triangular
L = np.tril(np.ones((4, 4)))
print(L)
# [[1. 0. 0. 0.]
#  [1. 1. 0. 0.]
#  [1. 1. 1. 0.]
#  [1. 1. 1. 1.]]

# Upper triangular
U = np.triu(np.ones((4, 4)))
print(U)
# [[1. 1. 1. 1.]
#  [0. 1. 1. 1.]
#  [0. 0. 1. 1.]
#  [0. 0. 0. 1.]]

# With offset
L_offset = np.tril(np.ones((4, 4)), k=-1)
print(L_offset)
# [[0. 0. 0. 0.]
#  [1. 0. 0. 0.]
#  [1. 1. 0. 0.]
#  [1. 1. 1. 0.]]
```

---

## 3. Random Array Creation

### 3.1 Uniform Distribution

```python
# Random floats in [0, 1)
arr = np.random.rand(5)
print(arr)  # e.g., [0.5488 0.7152 0.6028 0.5449 0.4237]

# 2D
arr_2d = np.random.rand(3, 4)

# Custom range [low, high)
arr = np.random.uniform(10, 20, size=5)
print(arr)  # e.g., [15.488 17.152 16.028 15.449 14.237]

# Uniform with shape
arr = np.random.uniform(0, 1, size=(3, 3))
```

### 3.2 Normal (Gaussian) Distribution

```python
# Standard normal: mean=0, std=1
arr = np.random.randn(5)
print(arr)  # e.g., [-0.204  1.437 -0.716  0.872 -1.297]

# Custom mean and std
arr = np.random.normal(loc=100, scale=15, size=1000)
print(f"Mean: {arr.mean():.1f}")   # ~100
print(f"Std: {arr.std():.1f}")     # ~15
```

### 3.3 Integer Random

```python
# Random integers in [low, high)
arr = np.random.randint(0, 100, size=10)
print(arr)  # e.g., [51 92 14 71 60]

# 2D
arr_2d = np.random.randint(0, 10, size=(3, 4))
```

### 3.4 Random Sampling

```python
# Random choice from array
arr = np.array([10, 20, 30, 40, 50])
sample = np.random.choice(arr, size=3, replace=False)
print(sample)  # 3 unique values from arr

# With probabilities
sample = np.random.choice(arr, size=3, p=[0.1, 0.1, 0.1, 0.1, 0.6])
```

### 3.5 Reproducibility

```python
# ALWAYS set a seed for reproducible results
np.random.seed(42)

# Or use Generator (modern approach)
rng = np.random.default_rng(seed=42)
arr1 = rng.random(5)
arr2 = rng.random(5)

# Each Generator is independent
rng1 = np.random.default_rng(42)
rng2 = np.random.default_rng(42)
arr1 = rng1.random(5)
arr2 = rng2.random(5)
print(np.array_equal(arr1, arr2))  # True
```

---

## 4. Special Array Creation

### 4.1 From Buffer

```python
# Create array from bytes
data = bytes(range(10))
arr = np.frombuffer(data, dtype=np.uint8)
print(arr)  # [0 1 2 3 4 5 6 7 8 9]
```

### 4.2 From String

```python
# Parse string data
data = "1.5 2.5 3.5 4.5"
arr = np.fromstring(data, sep=' ')
print(arr)  # [1.5 2.5 3.5 4.5]
```

### 4.3 From File

```python
# Load from text file
arr = np.loadtxt("data.txt", delimiter=",")
arr = np.genfromtxt("data.csv", delimiter=",", filling_values=0)

# Save to file
np.savetxt("output.txt", arr, delimiter=",")
```

### 4.4 Meshgrid

```python
# Create coordinate grids
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

print(X.shape)  # (100, 100)
print(Y.shape)  # (100, 100)

# Useful for plotting
Z = X**2 + Y**2
```

---

## 5. Memory Layout and Contiguity

```python
# C-contiguous (row-major, default)
arr_c = np.array([[1, 2, 3], [4, 5, 6]], order='C')
print(arr_c.flags['C_CONTIGUOUS'])  # True

# Fortran-contiguous (column-major)
arr_f = np.array([[1, 2, 3], [4, 5, 6]], order='F')
print(arr_f.flags['F_CONTIGUOUS'])  # True

# Convert between layouts
arr_f = np.asfortranarray(arr_c)
arr_c = np.ascontiguousarray(arr_f)
```

### Why Memory Layout Matters

```python
# Column-major slicing is faster for column access
arr = np.random.rand(1000, 1000)

# Column access (Fortran order is faster)
col_f = arr_f[:, 500]  # Fast with Fortran layout
col_c = arr_c[:, 500]  # Slower with C layout

# Row access (C order is faster)
row_c = arr_c[500, :]  # Fast with C layout
row_f = arr_f[500, :]  # Slower with Fortran layout
```

---

## 6. Array Creation Best Practices

### Performance Tips

```python
# SLOW — Python loop
arr = np.zeros(1000000)
for i in range(1000000):
    arr[i] = i ** 2

# FAST — Vectorized
arr = np.arange(1000000) ** 2

# FAST — Preallocate with zeros
arr = np.zeros(1000000)
arr[:] = np.arange(1000000) ** 2
```

### Memory Efficiency

```python
# Use appropriate dtypes
small_int = np.zeros(1000000, dtype=np.int8)    # 1 MB
large_int = np.zeros(1000000, dtype=np.int64)   # 8 MB

# Use sparse arrays for mostly-zero data
from scipy import sparse
sparse_arr = sparse.csr_matrix((10000, 10000))  # Much less memory
```

---

## 7. Common Mistakes to Avoid

### Mistake 1: Uninitialized Arrays
```python
# BAD — garbage values
arr = np.empty(5)
# print(arr.sum())  # Undefined result!

# GOOD — always initialize
arr = np.zeros(5)
```

### Mistake 2: Float Step in Arange
```python
# BAD — precision issues
arr = np.arange(0, 1, 0.1)
print(len(arr))  # Might be 9 or 10!

# GOOD — use linspace
arr = np.linspace(0, 0.9, 10)
```

### Mistake 3: Forgetting dtype
```python
# BAD — unexpected type
arr = np.array([1, 2, 3])
# arr[0] = 1.5  # Truncates to 1!

# GOOD — explicit dtype
arr = np.array([1, 2, 3], dtype=float)
arr[0] = 1.5  # Works as expected
```

### Mistake 4: Creating Very Large Arrays Unnecessarily
```python
# BAD — wastes memory
huge = np.zeros((10000, 10000, 1000))  # 800 GB!

# GOOD — use chunks or generators
for i in range(10):
    chunk = np.zeros((10000, 10000))
    # process chunk...
```

---

## 8. Best Practices

1. **Use `np.zeros()` or `np.ones()`** for initialization — never `np.empty()`
2. **Set `dtype` explicitly** to avoid unexpected type coercion
3. **Prefer `np.linspace()`** over `np.arange()` for float sequences
4. **Use `np.random.default_rng()`** instead of `np.random.seed()`
5. **Check array shape** after creation: `print(arr.shape)`
6. **Use vectorized operations** instead of Python loops
7. **Consider memory layout** (C vs Fortran order) for large arrays
8. **Use appropriate dtypes** — don't use `float64` when `float32` suffices

---

## 9. Practice Exercises

### Exercise 1: Array Creation Methods
```python
import numpy as np

# Create these arrays:
# a) [0, 1, 2, ..., 19]
# b) 5×5 matrix of zeros with dtype=int
# c) 3×3 identity matrix
# d) 4×4 matrix of ones
# e) Array of 10 random floats between 0 and 1
# f) 100 evenly spaced numbers from 0 to 100

# Solutions:
a = np.arange(20)
b = np.zeros((5, 5), dtype=int)
c = np.eye(3)
d = np.ones((4, 4))
e = np.random.rand(10)
f = np.linspace(0, 100, 100)
```

### Exercise 2: Special Matrices
```python
# Create:
# a) Lower triangular 4×4 matrix of ones
# b) Upper triangular 4×4 matrix of ones
# c) Diagonal matrix with [10, 20, 30, 40] on diagonal
# d) 3×5 matrix with 7s in positions where row+col is even

# Solutions:
a = np.tril(np.ones((4, 4)))
b = np.triu(np.ones((4, 4)))
c = np.diag([10, 20, 30, 40])
d = np.zeros((3, 5), dtype=int)
d[::2, ::2] = 7  # Rows 0,2 and cols 0,2,4
```

### Exercise 3: Random Arrays
```python
# With seed=42:
# a) 10×10 matrix of random integers [0, 100)
# b) 1000 values from normal distribution (mean=50, std=10)
# c) Verify the mean is approximately 50

np.random.seed(42)
a = np.random.randint(0, 100, size=(10, 10))
b = np.random.normal(50, 10, size=1000)
c = np.abs(b.mean() - 50) < 1  # Should be True
```

### Exercise 4: Memory and Performance
```python
import sys

# Compare memory usage of:
# a) Python list of 1,000,000 integers
# b) NumPy array of 1,000,000 integers (int64)
# c) NumPy array of 1,000,000 integers (int8)

list_data = list(range(1000000))
arr_int64 = np.arange(1000000, dtype=np.int64)
arr_int8 = np.arange(1000000, dtype=np.int8)

print(f"Python list: {sys.getsizeof(list_data):,} bytes")
print(f"NumPy int64: {arr_int64.nbytes:,} bytes")
print(f"NumPy int8:  {arr_int8.nbytes:,} bytes")
```

---

## 10. Summary

| Method | Use Case | Example |
|--------|----------|---------|
| `np.array()` | From Python data | `np.array([1, 2, 3])` |
| `np.zeros()` | Initialize with zeros | `np.zeros((3, 3))` |
| `np.ones()` | Initialize with ones | `np.ones(5, dtype=int)` |
| `np.empty()` | Uninitialized (fast) | `np.empty(5)` |
| `np.full()` | Fill with specific value | `np.full((3, 3), 7)` |
| `np.arange()` | Integer sequences | `np.arange(0, 10, 2)` |
| `np.linspace()` | Float sequences | `np.linspace(0, 1, 5)` |
| `np.eye()` | Identity matrix | `np.eye(3)` |
| `np.diag()` | Diagonal matrix | `np.diag([1, 2, 3])` |
| `np.tril()` | Lower triangular | `np.tril(np.ones((3,3)))` |
| `np.triu()` | Upper triangular | `np.triu(np.ones((3,3)))` |
| `np.random.rand()` | Random floats | `np.random.rand(3, 3)` |
| `np.random.randint()` | Random integers | `np.random.randint(0, 10, 5)` |
| `np.fromiter()` | From generator | `np.fromiter(gen, int)` |
| `np.frombuffer()` | From bytes | `np.frombuffer(data, uint8)` |
| `np.loadtxt()` | From file | `np.loadtxt("data.txt")` |
| `np.meshgrid()` | Coordinate grids | `np.meshgrid(x, y)` |

---

## 🔗 Next Lecture

→ [04-array-indexing-lecture.md](./04-array-indexing-lecture.md) — Array Indexing
