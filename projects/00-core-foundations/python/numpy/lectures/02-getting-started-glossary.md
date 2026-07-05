# NumPy Lecture 02: Getting Started — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| pip | Python package installer | `pip install numpy` |
| conda | Cross-platform package manager | `conda install numpy` |
| import | Bring a module into the namespace | `import numpy as np` |
| alias | Alternative name for a module | `np` is the alias for `numpy` |
| zeros | Array of all zeros | `np.zeros(5)` |
| ones | Array of all ones | `np.ones((3, 3))` |
| empty | Uninitialized array | `np.empty(5)` |
| full | Array filled with a value | `np.full((3, 3), 7)` |
| arange | Like range() but returns ndarray | `np.arange(0, 10, 2)` |
| linspace | Evenly spaced numbers | `np.linspace(0, 1, 5)` |
| eye | Identity matrix | `np.eye(3)` |
| rand | Random floats [0, 1) | `np.random.rand(3, 3)` |
| randint | Random integers | `np.random.randint(0, 100, 5)` |
| seed | Initialize random state | `np.random.seed(42)` |
| dtype | Data type of array | `arr.dtype` |
| shape | Array dimensions tuple | `arr.shape` |
| ndim | Number of dimensions | `arr.ndim` |
| size | Total element count | `arr.size` |
| itemsize | Bytes per element | `arr.itemsize` |
| nbytes | Total bytes in array | `arr.nbytes` |
| aggregate | Operation reducing to scalar | `arr.sum()`, `arr.mean()` |

---

## Alphabetical Glossary

### A

#### Arange
Create an array with evenly spaced values within a given interval. Like Python's `range()` but returns an ndarray.

```python
import numpy as np

arr = np.arange(0, 10, 2)
print(arr)  # [0 2 4 6 8]

# With float step
arr_f = np.arange(0, 1, 0.25)
print(arr_f)  # [0.   0.25 0.5  0.75]
```

**Note:** When using float steps, prefer `np.linspace()` to avoid floating point precision issues.

**Related:** linspace, zeros, ones

---

### B

#### Basic Operations
Element-wise operations on arrays: addition, subtraction, multiplication, division, and exponentiation.

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(a + b)    # [5 7 9]
print(a * b)    # [4 10 18]
print(a ** b)   # [1 32 729]
print(a / b)    # [0.25 0.4  0.5]
```

**Related:** broadcasting, ufunc, vectorization

---

### C

#### Conda
Cross-platform package and environment manager. Alternative to pip for installing NumPy.

```bash
conda install numpy
conda install -c conda-forge numpy
```

**Related:** pip, environment

---

### D

#### Dtype (Data Type)
The type of data stored in array elements. Can be specified at creation time.

```python
arr_int = np.zeros(5, dtype=np.int32)
arr_float = np.ones(5, dtype=np.float32)

print(arr_int.dtype)    # int32
print(arr_float.dtype)  # float32
```

**Common dtypes:** `np.int8`, `np.int16`, `np.int32`, `np.int64`, `np.float32`, `np.float64`, `np.complex64`, `np.complex128`, `np.bool_`, `np.str_`

**Related:** type promotion, casting

---

### E

#### Empty
Create an array without initializing values (contains whatever was in memory).

```python
arr = np.empty(5)
print(arr)  # Random garbage values!
```

**Warning:** Never rely on `np.empty()` values — always initialize before use.

**Related:** zeros, ones, full

---

#### Eye
Create an identity matrix (diagonal of ones, rest zeros).

```python
# 3x3 identity
I = np.eye(3)
print(I)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]

# With offset k (k>0 upper diagonal, k<0 lower diagonal)
I_offset = np.eye(4, k=1)
print(I_offset)
# [[0. 1. 0. 0.]
#  [0. 0. 1. 0.]
#  [0. 0. 0. 1.]
#  [0. 0. 0. 0.]]
```

**Related:** zeros, ones, full

---

### F

#### Full
Create an array filled with a specified value.

```python
arr = np.full((3, 4), fill_value=7)
print(arr)
# [[7 7 7 7]
#  [7 7 7 7]
#  [7 7 7 7]]

# With specific dtype
arr_str = np.full(3, "hello", dtype=object)
print(arr_str)  # ['hello' 'hello' 'hello']
```

**Related:** zeros, ones, empty

---

### I

#### Import
Bring a Python module into the current namespace.

```python
# Standard import
import numpy as np

# From import (avoid in production)
from numpy import array, zeros, ones

# Wildcard import (NEVER do this)
from numpy import *
```

**Related:** alias, module

---

### L

#### Linspace
Create an array with evenly spaced numbers over a specified interval.

```python
arr = np.linspace(0, 10, 5)
print(arr)  # [ 0.   2.5  5.   7.5 10. ]

# Without endpoint
arr_no_end = np.linspace(0, 10, 5, endpoint=False)
print(arr_no_end)  # [0. 2. 4. 6. 8.]

# With retstep=True to get the step size
arr_step, step = np.linspace(0, 10, 5, retstep=True)
print(f"Step size: {step}")  # 2.5
```

**Note:** `linspace` includes the endpoint by default, unlike `arange`.

**Related:** arange, zeros, ones

---

### N

#### Ndim
The number of dimensions (axes) of an array.

```python
arr_0d = np.array(5)
arr_1d = np.array([1, 2, 3])
arr_2d = np.array([[1, 2], [3, 4]])
arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])

print(arr_0d.ndim)  # 0
print(arr_1d.ndim)  # 1
print(arr_2d.ndim)  # 2
print(arr_3d.ndim)  # 3
```

**Related:** shape, size, ndarray

---

#### Nbytes
Total number of bytes consumed by the array.

```python
arr = np.zeros((3, 3), dtype=np.float64)
print(arr.nbytes)  # 72 (9 elements × 8 bytes each)
```

**Related:** itemsize, size, dtype

---

#### Numpy
Numerical Python — the fundamental library for scientific computing.

```python
import numpy as np
print(np.__version__)  # e.g., 1.26.4
```

**Related:** ndarray, scipy, pandas

---

### O

#### Ones
Create an array filled with ones.

```python
arr = np.ones(5)
print(arr)  # [1. 1. 1. 1. 1.]

# 2D
arr_2d = np.ones((3, 4), dtype=int)
print(arr_2d)
# [[1 1 1 1]
#  [1 1 1 1]
#  [1 1 1 1]]
```

**Related:** zeros, full, empty

---

### P

#### Pip
Python's standard package installer. Used to install NumPy from PyPI.

```bash
pip install numpy
pip install numpy==1.26.4
pip install --upgrade numpy
```

**Related:** conda, package

---

### R

#### Rand
Generate random floats in the half-open interval [0.0, 1.0).

```python
# 1D array of 5 random floats
arr = np.random.rand(5)
print(arr)  # e.g., [0.5488 0.7152 0.6028 0.5449 0.4237]

# 2D array
arr_2d = np.random.rand(3, 3)
print(arr_2d)

# With seed for reproducibility
np.random.seed(42)
arr1 = np.random.rand(3)
np.random.seed(42)
arr2 = np.random.rand(3)
print(np.array_equal(arr1, arr2))  # True
```

**Related:** randint, randn, seed

---

#### Randint
Generate random integers from a range.

```python
# Random integers from 0 to 99
arr = np.random.randint(0, 100, size=10)
print(arr)  # e.g., [51 92 14 71 60]

# 2D array
arr_2d = np.random.randint(0, 10, size=(3, 4))
print(arr_2d)

# Single random integer
single = np.random.randint(0, 10)
print(single)
```

**Related:** rand, randn, seed

---

### S

#### Seed
Initialize the random number generator for reproducibility.

```python
np.random.seed(42)
arr1 = np.random.rand(5)

np.random.seed(42)
arr2 = np.random.rand(5)

print(np.array_equal(arr1, arr2))  # True
```

**Best Practice:** Always set a seed when debugging or sharing results.

**Related:** rand, randint, random state

---

#### Shape
Tuple of array dimensions.

```python
arr_1d = np.array([1, 2, 3])
print(arr_1d.shape)  # (3,)

arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print(arr_2d.shape)  # (2, 3)

arr_3d = np.zeros((2, 3, 4))
print(arr_3d.shape)  # (2, 3, 4)
```

**Related:** ndim, size, strides

---

#### Size
Total number of elements in the array.

```python
arr = np.zeros((3, 4))
print(arr.size)  # 12

# For 1D
arr_1d = np.arange(10)
print(arr_1d.size)  # 10
```

**Related:** shape, ndim, nbytes

---

### Z

#### Zeros
Create an array filled with zeros.

```python
# 1D
arr = np.zeros(5)
print(arr)  # [0. 0. 0. 0. 0.]

# 2D
arr_2d = np.zeros((3, 4))
print(arr_2d)
# [[0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]]

# With specific dtype
arr_int = np.zeros(5, dtype=int)
print(arr_int.dtype)  # int64
```

**Related:** ones, full, empty

---

## Common Patterns Quick Reference

```python
import numpy as np

# All zeros
np.zeros(5)              # 1D: 5 zeros
np.zeros((3, 4))         # 2D: 3×4 zeros
np.zeros((2, 3, 4))      # 3D: 2×3×4 zeros

# All ones
np.ones(5)               # 1D: 5 ones
np.ones((3, 4))          # 2D: 3×4 ones

# Filled with value
np.full((3, 3), 7)       # 3×3 filled with 7

# Identity matrix
np.eye(3)                # 3×3 identity
np.eye(4, k=1)           # 4×4 with ones on first superdiagonal

# Sequences
np.arange(0, 10, 2)      # [0, 2, 4, 6, 8]
np.linspace(0, 1, 5)     # [0, 0.25, 0.5, 0.75, 1]

# Random
np.random.rand(3, 3)     # Uniform [0, 1)
np.random.randn(3, 3)    # Standard normal
np.random.randint(0, 10, (3, 3))  # Random ints
```
