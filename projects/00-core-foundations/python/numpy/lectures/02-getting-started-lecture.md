# NumPy Lecture 02: Getting Started with NumPy

## 🎯 Topic Overview

This lecture covers the practical setup and first steps with NumPy. You'll learn how to install NumPy, create arrays, explore array attributes, and perform basic operations. This is your hands-on introduction to working with NumPy arrays.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Install and verify NumPy installation
2. Import NumPy with the standard convention
3. Create arrays from Python lists, tuples, and other iterables
4. Inspect array attributes (shape, dtype, size, ndim)
5. Perform basic element-wise operations
6. Use built-in array creation functions
7. Debug common import and creation errors

---

## 1. Installing NumPy

### Using pip (Standard)

```bash
# Basic installation
pip install numpy

# Upgrade to latest version
pip install --upgrade numpy

# Install specific version
pip install numpy==1.26.4
```

### Using conda

```bash
# Create a conda environment first (recommended)
conda create -n numpy-env python=3.11
conda activate numpy-env

# Install numpy
conda install numpy

# Or install from conda-forge (community channel)
conda install -c conda-forge numpy
```

### Verifying Installation

```python
import numpy as np

# Check version
print(f"NumPy version: {np.__version__}")

# Check configuration (BLAS, LAPACK info)
np.show_config()
```

### System Information

```python
import numpy as np

# Check what's under the hood
print(np.__config__.show())  # Detailed BLAS/LAPACK info
```

---

## 2. Importing NumPy

### Standard Import (Universal Convention)

```python
# ALWAYS use this import — it's THE universal convention
import numpy as np
```

### Why `np`?

The `np` alias is:
- Short and memorable
- Universal across the entire Python data science community
- Used in every NumPy tutorial, textbook, and documentation
- Expected by tools like Jupyter, IDEs, and linters

### Alternative Imports (Don't Do This)

```python
# DON'T use these in production code:
from numpy import *          # Pollutes namespace
import numpy as num         # Non-standard
import numpy                # Too verbose
from numpy import array, zeros  # Only for specific small scripts
```

---

## 3. Creating Arrays

### 3.1 From Python Lists

```python
import numpy as np

# 1D array (vector)
arr_1d = np.array([1, 2, 3, 4, 5])
print(arr_1d)        # [1 2 3 4 5]
print(arr_1d.shape)  # (5,)

# 2D array (matrix)
arr_2d = np.array([[1, 2, 3],
                   [4, 5, 6]])
print(arr_2d)
# [[1 2 3]
#  [4 5 6]]
print(arr_2d.shape)  # (2, 3)

# 3D array (tensor)
arr_3d = np.array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]]])
print(arr_3d.shape)  # (2, 2, 2)
```

### 3.2 From Python Tuples

```python
# Tuples work exactly like lists
arr = np.array((1, 2, 3, 4, 5))
print(arr)  # [1 2 3 4 5]
```

### 3.3 From Mixed Types (Type Coercion)

```python
# NumPy will upcast to a common type
arr = np.array([1, 2.5, 3, 4.0])
print(arr.dtype)  # float64 — int promoted to float

arr = np.array([1, "hello", 3])
print(arr.dtype)  # <U21 — everything becomes string

arr = np.array([1, 2, True])
print(arr.dtype)  # int64 — True becomes 1
```

### 3.4 From Nested Lists (Multi-dimensional)

```python
# 2D — nested lists
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
print(matrix.shape)  # (3, 3)
print(matrix)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]
```

---

## 4. Array Creation Functions

NumPy provides many built-in functions for creating arrays without manually specifying every element.

### 4.1 Zeros and Ones

```python
# Array of all zeros
zeros_1d = np.zeros(5)
print(zeros_1d)  # [0. 0. 0. 0. 0.]

zeros_2d = np.zeros((3, 4))
print(zeros_2d)
# [[0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]]

# Array of all ones
ones_1d = np.ones(5)
print(ones_1d)  # [1. 1. 1. 1. 1.]

# With specific dtype
zeros_int = np.zeros((2, 3), dtype=int)
print(zeros_int.dtype)  # int64
```

### 4.2 Empty and Full

```python
# Empty array (uninitialized — random memory values)
empty_arr = np.empty(5)
print(empty_arr)  # Values are undefined!

# Array filled with a specific value
full_arr = np.full((3, 3), fill_value=7)
print(full_arr)
# [[7 7 7]
#  [7 7 7]
#  [7 7 7]]
```

### 4.3 Arange and Linspace

```python
# arange — like range() but returns ndarray
arr = np.arange(0, 10, 2)
print(arr)  # [0 2 4 6 8]

# With float step
arr_float = np.arange(0, 1, 0.2)
print(arr_float)  # [0.  0.2 0.4 0.6 0.8]

# linspace — evenly spaced numbers over a range
arr_lin = np.linspace(0, 1, 5)
print(arr_lin)  # [0.   0.25 0.5  0.75 1.  ]

# linspace includes the endpoint (arange does not by default)
```

### 4.4 Identity and Diagonal

```python
# Identity matrix
eye_3 = np.eye(3)
print(eye_3)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]

# Identity matrix with offset
eye_offset = np.eye(4, k=1)
print(eye_offset)
# [[0. 1. 0. 0.]
#  [0. 0. 1. 0.]
#  [0. 0. 0. 1.]
#  [0. 0. 0. 0.]]
```

### 4.5 Random Arrays

```python
# Random floats in [0, 1)
random_arr = np.random.rand(5)
print(random_arr)  # e.g., [0.5488 0.7152 0.6028 0.5449 0.4237]

# Random 2D
random_2d = np.random.rand(3, 3)
print(random_2d)

# Random integers
rand_int = np.random.randint(0, 100, size=(3, 4))
print(rand_int)

# Standard normal distribution
normal = np.random.randn(5)
print(normal)  # e.g., [-0.2  1.4 -0.7  0.9 -1.3]

# Reproducible randomness with seed
np.random.seed(42)
arr1 = np.random.rand(3)
np.random.seed(42)
arr2 = np.random.rand(3)
print(np.array_equal(arr1, arr2))  # True
```

---

## 5. Inspecting Array Attributes

```python
arr = np.array([[1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0]])

# Shape — dimensions as tuple
print(arr.shape)        # (3, 3)

# Dtype — data type of elements
print(arr.dtype)        # float64

# ndim — number of dimensions
print(arr.ndim)         # 2

# Size — total number of elements
print(arr.size)         # 9

# Itemsize — bytes per element
print(arr.itemsize)     # 8

# nbytes — total bytes consumed
print(arr.nbytes)       # 72

# T — transpose
print(arr.T.shape)      # (3, 3)

# flags — memory information
print(arr.flags)
```

---

## 6. Basic Operations

### 6.1 Element-wise Arithmetic

```python
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print(a + b)     # [11 22 33 44 55]
print(a - b)     # [-9 -18 -27 -36 -45]
print(a * b)     # [10 40 90 160 250]
print(b / a)     # [10. 10. 10. 10. 10.]
print(a ** 2)    # [1 4 9 16 25]
print(a % 3)     # [1 2 0 1 2]
```

### 6.2 Scalar Operations (Broadcasting)

```python
arr = np.array([1, 2, 3, 4, 5])

print(arr + 10)    # [11 12 13 14 15]
print(arr * 3)     # [3 6 9 12 15]
print(arr ** 2)    # [1 4 9 16 25]
print(arr / 2)     # [0.5 1.  1.5 2.  2.5]
```

### 6.3 Comparison Operations

```python
arr = np.array([1, 2, 3, 4, 5])

print(arr > 3)     # [False False False  True  True]
print(arr == 3)    # [False False  True False False]
print(arr <= 2)    # [ True  True False False False]
```

### 6.4 Aggregate Operations

```python
arr = np.array([1, 2, 3, 4, 5, 6])

print(arr.sum())    # 21
print(arr.mean())   # 3.5
print(arr.min())    # 1
print(arr.max())    # 6
print(arr.std())    # 1.7078...
print(arr.var())    # 2.9166...
```

---

## 7. Common Mistakes to Avoid

### Mistake 1: Forgetting the Import
```python
# NameError: name 'np' is not defined
arr = np.array([1, 2, 3])  # Forgot: import numpy as np
```

### Mistake 2: Using Python Lists After Creating Arrays
```python
# This will error
python_list = [1, 2, 3]
python_list * 2  # [1, 2, 3, 1, 2, 3] — concatenation

# NumPy does what you probably want
arr = np.array([1, 2, 3])
arr * 2  # [2, 4, 6] — element-wise
```

### Mistake 3: Wrong Shape for Operations
```python
a = np.array([1, 2, 3])       # shape (3,)
b = np.array([[1, 2, 3]])     # shape (1, 3)
# a + b  — broadcasting works but may be confusing
```

### Mistake 4: Using Float Indices
```python
arr = np.array([10, 20, 30, 40, 50])
# arr[1.5]  — IndexError: only integers can be used for indexing
arr[1]  # Correct — returns 20
```

### Mistake 5: Modifying a View
```python
a = np.array([1, 2, 3, 4])
b = a[1:3]     # View into a
b[0] = 99
print(a)       # [ 1 99  3  4] — a is modified!
```

---

## 8. Best Practices

1. **Always verify your array shape** after creation: `print(arr.shape)`
2. **Use vectorized operations** — never use Python loops for element-wise math
3. **Be explicit about dtype** — `np.zeros(5, dtype=np.float32)` instead of just `np.zeros(5)`
4. **Use `np.arange()` and `np.linspace()`** for sequences instead of `range()`
5. **Set random seeds** for reproducibility: `np.random.seed(42)`
6. **Check array attributes** before operations: `arr.shape`, `arr.dtype`
7. **Use `np.info()`** to inspect unfamiliar arrays: `np.info(arr)`

---

## 9. Practice Exercises

### Exercise 1: Array Creation
```python
# Create the following arrays and print their shapes:
import numpy as np

# a) A 1D array of 10 zeros
zeros = np.zeros(10)
print(f"Shape: {zeros.shape}")

# b) A 3x3 identity matrix
identity = np.eye(3)
print(f"Shape: {identity.shape}")

# c) A 2D array of 4x6 ones
ones = np.ones((4, 6))
print(f"Shape: {ones.shape}")

# d) An array of integers from 0 to 20 (exclusive) with step 3
arr = np.arange(0, 20, 3)
print(f"Values: {arr}")

# e) 5 evenly spaced numbers from 0 to 1
arr_lin = np.linspace(0, 1, 5)
print(f"Linspace: {arr_lin}")
```

### Exercise 2: Array Attributes
```python
# Create this array and print ALL attributes
arr = np.array([[1.0, 2.0, 3.0, 4.0],
                [5.0, 6.0, 7.0, 8.0]])

# Print: shape, dtype, ndim, size, itemsize, nbytes
print(f"Shape: {arr.shape}")
print(f"Dtype: {arr.dtype}")
print(f"Ndim: {arr.ndim}")
print(f"Size: {arr.size}")
print(f"Itemsize: {arr.itemsize}")
print(f"Nbytes: {arr.nbytes}")
```

### Exercise 3: Operations
```python
# Perform these operations and verify results
a = np.array([10, 20, 30, 40, 50])
b = np.array([1, 2, 3, 4, 5])

# a) Element-wise addition
print(f"a + b = {a + b}")

# b) Element-wise multiplication
print(f"a * b = {a * b}")

# c) a divided by b
print(f"a / b = {a / b}")

# d) a raised to power of b
print(f"a ** b = {a ** b}")

# e) Sum, mean, min, max of a
print(f"Sum: {a.sum()}, Mean: {a.mean()}, Min: {a.min()}, Max: {a.max()}")
```

### Exercise 4: Random Arrays
```python
# Create random arrays with fixed seed
np.random.seed(123)

# a) 4x4 array of random floats [0, 1)
random_floats = np.random.rand(4, 4)
print("Random floats:")
print(random_floats)

# b) 3x3 array of random integers [0, 50)
random_ints = np.random.randint(0, 50, size=(3, 3))
print("\nRandom integers:")
print(random_ints)

# c) Verify reproducibility by resetting seed
np.random.seed(123)
arr1 = np.random.rand(3)
np.random.seed(123)
arr2 = np.random.rand(3)
print(f"\nReproducible: {np.array_equal(arr1, arr2)}")
```

---

## 10. Summary

| Topic | Key Takeaway |
|-------|-------------|
| **Import** | Always `import numpy as np` |
| **From Lists** | `np.array([1, 2, 3])` |
| **Zeros/Ones** | `np.zeros()`, `np.ones()` |
| **Range** | `np.arange()`, `np.linspace()` |
| **Identity** | `np.eye(n)` |
| **Random** | `np.random.rand()`, `np.random.randint()` |
| **Attributes** | `.shape`, `.dtype`, `.ndim`, `.size` |
| **Operations** | Element-wise: `+`, `-`, `*`, `/`, `**` |
| **Aggregates** | `.sum()`, `.mean()`, `.min()`, `.max()` |

### Key Takeaways

1. NumPy installation is straightforward with `pip install numpy`
2. The `np` alias is universal and mandatory in practice
3. Arrays can be created from lists, tuples, or built-in functions
4. Built-in functions (`zeros`, `ones`, `arange`, `linspace`) are essential
5. Array attributes (`shape`, `dtype`, `ndim`) are your debugging tools
6. Element-wise operations replace Python loops for performance
7. Broadcasting lets you operate on arrays and scalars together

---

## 🔗 Next Lecture

→ [03-creating-arrays-lecture.md](./03-creating-arrays-lecture.md) — Creating Arrays in Detail
