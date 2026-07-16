# NumPy Lecture 03: Creating Arrays — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| array | N-dimensional data container | `np.array([1, 2, 3])` |
| zeros | Array of all zeros | `np.zeros(5)` |
| ones | Array of all ones | `np.ones((3, 3))` |
| empty | Uninitialized array | `np.empty(5)` |
| full | Fill array with value | `np.full((3, 3), 7)` |
| arange | Evenly spaced values | `np.arange(0, 10, 2)` |
| linspace | Evenly spaced over interval | `np.linspace(0, 1, 5)` |
| logspace | Log-spaced values | `np.logspace(0, 3, 4)` |
| eye | Identity matrix | `np.eye(3)` |
| diag | Diagonal array | `np.diag([1, 2, 3])` |
| tril | Lower triangular | `np.tril(arr)` |
| triu | Upper triangular | `np.triu(arr)` |
| meshgrid | Coordinate grids | `np.meshgrid(x, y)` |
| fromiter | Create from iterator | `np.fromiter(gen, int)` |
| frombuffer | Create from bytes | `np.frombuffer(data, uint8)` |
| loadtxt | Load from text file | `np.loadtxt("data.txt")` |
| genfromtxt | Load with missing data | `np.genfromtxt("data.csv")` |
| savetxt | Save to text file | `np.savetxt("out.txt", arr)` |
| rand | Uniform random [0, 1) | `np.random.rand(3)` |
| randn | Standard normal random | `np.random.randn(3)` |
| randint | Random integers | `np.random.randint(0, 10, 5)` |
| seed | Initialize RNG | `np.random.seed(42)` |
| default_rng | Modern RNG generator | `np.random.default_rng(42)` |
| dtype | Element data type | `np.float64`, `np.int32` |
| order | Memory layout (C or F) | `order='C'`, `order='F'` |
| fill | Fill existing array | `arr.fill(5)` |

---

## Alphabetical Glossary

### A

#### Arange
Return evenly spaced values within a given interval. Like Python's `range()` but returns an ndarray.

```python
import numpy as np

# Basic: [0, 10)
arr = np.arange(10)
print(arr)  # [0 1 2 3 4 5 6 7 8 9]

# With start, stop, step
arr = np.arange(0, 10, 2)
print(arr)  # [0 2 4 6 8]

# With float step
arr = np.arange(0, 1, 0.25)
print(arr)  # [0.   0.25 0.5  0.75]
```

**Warning:** Float steps can cause precision issues. Use `np.linspace()` for float sequences.

**Related:** linspace, zeros, array

---

#### Array
The fundamental NumPy data structure. Creates an ndarray from data.

```python
arr = np.array([1, 2, 3])
print(type(arr))  # <class 'numpy.ndarray'>

# 2D
matrix = np.array([[1, 2], [3, 4]])

# With dtype
arr = np.array([1, 2, 3], dtype=np.float64)

# From tuple
arr = np.array((1, 2, 3))
```

**Related:** ndarray, dtype, zeros, ones

---

### C

#### Contiguous
Memory layout where elements are stored in a single continuous block.

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.flags['C_CONTIGUOUS'])  # True (row-major)

# Fortran-contiguous
arr_f = np.asfortranarray(arr)
print(arr_f.flags['F_CONTIGUOUS'])  # True
```

**Related:** order, strides, memory layout

---

### D

#### Default_rng
Modern random number generator (recommended over legacy API).

```python
rng = np.random.default_rng(seed=42)
arr = rng.random(5)
ints = rng.integers(0, 100, size=5)
normal = rng.normal(0, 1, size=5)
```

**Related:** seed, rand, randint

---

#### Diag
Create a diagonal array or extract diagonal from matrix.

```python
# Create diagonal matrix
D = np.diag([1, 2, 3, 4])
print(D)
# [[1 0 0 0]
#  [0 2 0 0]
#  [0 0 3 0]
#  [0 0 0 4]]

# Extract diagonal from matrix
M = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
d = np.diag(M)
print(d)  # [1 5 9]

# k parameter for off-diagonal
D_upper = np.diag([1, 2, 3], k=1)
```

**Related:** eye, tril, triu

---

#### Dtype
Data type of array elements. Controls memory allocation and operations.

```python
arr = np.array([1, 2, 3], dtype=np.float32)
print(arr.dtype)  # float32

# Common types:
np.int8, np.int16, np.int32, np.int64  # Integers
np.float16, np.float32, np.float64     # Floats
np.complex64, np.complex128            # Complex
np.bool_                               # Boolean
np.str_                                # String
np.object_                             # Python objects
```

**Related:** type promotion, casting, astype

---

### E

#### Empty
Create an array without initializing values (contains random memory).

```python
arr = np.empty(5)
print(arr)  # Undefined garbage values!
```

**Warning:** Always initialize before use. Prefer `np.zeros()` or `np.ones()`.

**Related:** zeros, ones, full

---

#### Eye
Create an identity matrix (2D) with ones on diagonal.

```python
I = np.eye(3)
print(I)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]

# Rectangular
I_rect = np.eye(3, 5)

# With offset
I_upper = np.eye(4, k=1)  # Superdiagonal
I_lower = np.eye(4, k=-1)  # Subdiagonal

# With dtype
I_int = np.eye(3, dtype=int)
```

**Related:** diag, zeros, ones

---

### F

#### Fill
Fill an existing array with a scalar value (in-place).

```python
arr = np.zeros(5)
arr.fill(7)
print(arr)  # [7. 7. 7. 7. 7.]

# Different from np.full (which creates new array)
arr_new = np.full(5, 7)  # Creates new array
```

**Related:** zeros, ones, full

---

#### Frombuffer
Create array from a buffer (bytes object).

```python
data = bytes(range(10))
arr = np.frombuffer(data, dtype=np.uint8)
print(arr)  # [0 1 2 3 4 5 6 7 8 9]
```

**Related:** fromiter, array

---

#### Fromiter
Create array from an iterator or generator.

```python
gen = (x**2 for x in range(5))
arr = np.fromiter(gen, dtype=int, count=5)
print(arr)  # [ 0  1  4  9 16]

# Without count (slower, reads until exhausted)
arr = np.fromiter((x for x in range(5)), dtype=int)
```

**Related:** array, frombuffer

---

### G

#### Genfromtxt
Load data from text file, handling missing values.

```python
# Save some data first
np.savetxt("data.csv", [[1, 2, 3], [4, 5, 6]], delimiter=",")

# Load with genfromtxt
arr = np.genfromtxt("data.csv", delimiter=",")
print(arr)
# [[1. 2. 3.]
#  [4. 5. 6.]]

# With missing values
arr = np.genfromtxt("data.csv", delimiter=",", filling_values=0)
```

**Related:** loadtxt, savetxt

---

### L

#### Linspace
Return evenly spaced numbers over a specified interval.

```python
# 5 numbers from 0 to 10 (inclusive)
arr = np.linspace(0, 10, 5)
print(arr)  # [ 0.   2.5  5.   7.5 10. ]

# Without endpoint
arr = np.linspace(0, 10, 5, endpoint=False)
print(arr)  # [0. 2. 4. 6. 8.]

# With retstep
arr, step = np.linspace(0, 10, 5, retstep=True)
print(f"Step: {step}")  # 2.5

# Log-spaced
arr = np.logspace(0, 3, 4)
print(arr)  # [1. 10. 100. 1000.]
```

**Note:** `linspace` includes endpoint by default, unlike `arange`.

**Related:** arange, logspace

---

#### Loadtxt
Load data from a text file.

```python
# Save data
np.savetxt("data.txt", [[1, 2, 3], [4, 5, 6]], delimiter=",")

# Load
arr = np.loadtxt("data.txt", delimiter=",")
print(arr)
# [[1. 2. 3.]
#  [4. 5. 6.]]
```

**Related:** genfromtxt, savetxt

---

#### Logspace
Return evenly spaced numbers on a log scale.

```python
arr = np.logspace(0, 3, 4)
print(arr)  # [1. 10. 100. 1000.]

# Custom base
arr = np.logspace(0, 3, 4, base=2)
print(arr)  # [1. 2. 4. 8.]
```

**Related:** linspace, arange

---

### M

#### Meshgrid
Create coordinate matrices from coordinate vectors.

```python
x = np.array([1, 2, 3])
y = np.array([4, 5])

X, Y = np.meshgrid(x, y)
print(X)
# [[1 2 3]
#  [1 2 3]]
print(Y)
# [[4 4 4]
#  [5 5 5]]

# With indexing='ij' (matrix indexing)
X, Y = np.meshgrid(x, y, indexing='ij')
```

**Related:** linspace, arange

---

### O

#### Order
Memory layout of array: 'C' (row-major) or 'F' (column-major).

```python
# C order (row-major, default)
arr_c = np.array([[1, 2, 3], [4, 5, 6]], order='C')

# F order (column-major)
arr_f = np.array([[1, 2, 3], [4, 5, 6]], order='F')

# Convert
arr_f = np.asfortranarray(arr_c)
arr_c = np.ascontiguousarray(arr_f)
```

**Related:** contiguous, strides, memory layout

---

#### Ones
Create array filled with ones.

```python
arr = np.ones(5)
print(arr)  # [1. 1. 1. 1. 1.]

# 2D
arr_2d = np.ones((3, 4), dtype=int)
print(arr_2d)
# [[1 1 1 1]
#  [1 1 1 1]
#  [1 1 1 1]]

# From shape of another array
arr = np.array([[1, 2, 3], [4, 5, 6]])
ones_like = np.ones_like(arr)
```

**Related:** zeros, full, empty

---

### R

#### Rand
Generate random floats in [0, 1).

```python
arr = np.random.rand(5)
print(arr)  # e.g., [0.5488 0.7152 0.6028 0.5449 0.4237]

# 2D
arr_2d = np.random.rand(3, 4)

# With seed
np.random.seed(42)
arr = np.random.rand(5)
```

**Related:** randn, randint, seed

---

#### Randint
Generate random integers.

```python
arr = np.random.randint(0, 100, size=10)
print(arr)  # e.g., [51 92 14 71 60]

# 2D
arr_2d = np.random.randint(0, 10, size=(3, 4))

# Single integer
single = np.random.randint(0, 10)
```

**Related:** rand, randn, seed

---

#### Randn
Generate random numbers from standard normal distribution.

```python
arr = np.random.randn(5)
print(arr)  # e.g., [-0.204  1.437 -0.716  0.872 -1.297]

# 2D
arr_2d = np.random.randn(3, 4)

# Custom mean and std
arr = np.random.randn(1000) * 15 + 100  # mean=100, std=15
```

**Related:** rand, normal, seed

---

### S

#### Savetxt
Save array to text file.

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
np.savetxt("output.txt", arr, delimiter=",", fmt="%d")
```

**Related:** loadtxt, genfromtxt

---

#### Seed
Initialize random number generator.

```python
np.random.seed(42)
arr = np.random.rand(5)

# Same seed = same results
np.random.seed(42)
arr2 = np.random.rand(5)
print(np.array_equal(arr, arr2))  # True
```

**Related:** rand, randint, default_rng

---

#### Tril
Extract lower triangular matrix.

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
L = np.tril(arr)
print(L)
# [[1 0 0]
#  [4 5 0]
#  [7 8 9]]

# With offset
L = np.tril(arr, k=-1)
print(L)
# [[0 0 0]
#  [4 0 0]
#  [7 8 0]]
```

**Related:** triu, diag, eye

---

#### Triu
Extract upper triangular matrix.

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
U = np.triu(arr)
print(U)
# [[1 2 3]
#  [0 5 6]
#  [0 0 9]]

# With offset
U = np.triu(arr, k=1)
print(U)
# [[0 2 3]
#  [0 0 6]
#  [0 0 0]]
```

**Related:** tril, diag, eye

---

### Z

#### Zeros
Create array filled with zeros.

```python
arr = np.zeros(5)
print(arr)  # [0. 0. 0. 0. 0.]

# 2D
arr_2d = np.zeros((3, 4), dtype=int)

# From shape of another array
arr = np.array([[1, 2], [3, 4]])
zeros_like = np.zeros_like(arr)
```

**Related:** ones, full, empty

---

## Creation Method Comparison

| Method | Use Case | Returns |
|--------|----------|---------|
| `np.array()` | From Python data | ndarray |
| `np.zeros()` | Initialize zeros | ndarray |
| `np.ones()` | Initialize ones | ndarray |
| `np.empty()` | Uninitialized | ndarray |
| `np.full()` | Fill with value | ndarray |
| `np.arange()` | Integer sequence | ndarray |
| `np.linspace()` | Float sequence | ndarray |
| `np.logspace()` | Log sequence | ndarray |
| `np.eye()` | Identity matrix | ndarray |
| `np.diag()` | Diagonal matrix | ndarray |
| `np.tril()` | Lower triangular | ndarray |
| `np.triu()` | Upper triangular | ndarray |
| `np.meshgrid()` | Coordinate grids | tuple of ndarrays |
| `np.fromiter()` | From iterator | ndarray |
| `np.frombuffer()` | From bytes | ndarray |
| `np.loadtxt()` | From text file | ndarray |
| `np.genfromtxt()` | From file with missing | ndarray |
| `np.random.rand()` | Uniform random | ndarray |
| `np.random.randn()` | Normal random | ndarray |
| `np.random.randint()` | Random integers | ndarray |
