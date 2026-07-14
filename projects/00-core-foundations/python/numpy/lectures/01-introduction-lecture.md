# NumPy Lecture 01: Introduction to NumPy

## 🎯 Topic Overview

NumPy (Numerical Python) is the foundational library for scientific computing in Python. It provides a powerful N-dimensional array object, sophisticated broadcasting functions, and tools for integrating C/C++ and Fortran code. NumPy is the backbone of the entire Python data science ecosystem, underpinning libraries like Pandas, SciPy, Matplotlib, scikit-learn, and TensorFlow.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what NumPy is and why it matters
2. Explain the advantages of NumPy over Python lists
3. Recognize the core components of the NumPy ecosystem
4. Install and import NumPy correctly
5. Understand NumPy's role in the data science stack
6. Identify when to use NumPy vs. pure Python

---

## 1. What is NumPy?

NumPy is an open-source library created in 2005 by Travis Oliphant. It is the spiritual successor to the older Numeric and numarray libraries and provides:

- **N-dimensional array objects** (`ndarray`) — fast, memory-efficient containers for homogeneous data
- **Broadcasting** — vectorized operations that eliminate explicit loops
- **Mathematical functions** — linear algebra, statistics, Fourier transforms, random number generation
- **Interoperability** — bridges between Python, C, C++, and Fortran code

### Core Philosophy

NumPy's design is guided by three principles:

1. **Vectorization over iteration** — operations on entire arrays instead of element-by-element loops
2. **Homogeneous data** — all elements in an array share the same type, enabling memory efficiency
3. **Broadcasting** — operations automatically handle arrays of different shapes

---

## 2. Why NumPy? — Performance Comparison

### Python Lists vs NumPy Arrays

```python
import time
import sys

# Python list
python_list = list(range(1000000))
print(f"Python list size: {sys.getsizeof(python_list)} bytes")  # ~8 MB

# NumPy array
import numpy as np
numpy_array = np.arange(1000000)
print(f"NumPy array size: {numpy_array.nbytes} bytes")  # ~8 MB

# But the key difference is speed:
start = time.time()
result_list = [x * 2 for x in python_list]
print(f"Python list: {time.time() - start:.4f}s")

start = time.time()
result_array = numpy_array * 2
print(f"NumPy array: {time.time() - start:.4f}s")
```

### Why is NumPy Faster?

| Factor | Python List | NumPy Array |
|--------|-------------|-------------|
| Memory layout | Array of pointers to objects | Contiguous block of raw bytes |
| Type checking | Every element checked at runtime | Type determined once at creation |
| Operations | Python loop (interpreted) | SIMD vectorized (compiled C) |
| Caching | Poor cache locality | Excellent cache locality |

---

## 3. The NumPy Ecosystem

NumPy is the foundation upon which the entire scientific Python stack is built:

```
┌─────────────────────────────────────────────────┐
│            Application Layer                     │
│  (Data Science, ML, Scientific Research)         │
├─────────────────────────────────────────────────┤
│         High-Level Libraries                     │
│  Pandas │ SciPy │ Matplotlib │ scikit-learn      │
├─────────────────────────────────────────────────┤
│              NumPy                               │
│  ndarray │ ufuncs │ linear algebra │ linalg      │
├─────────────────────────────────────────────────┤
│         Low-Level Languages                      │
│  C │ C++ │ Fortran │ BLAS │ LAPACK              │
├─────────────────────────────────────────────────┤
│              Hardware                            │
│  CPU │ GPU │ Memory │ SIMD Instructions          │
└─────────────────────────────────────────────────┘
```

### Key Ecosystem Partners

- **Pandas** — DataFrames built on top of NumPy arrays
- **SciPy** — Scientific algorithms extending NumPy
- **Matplotlib** — Visualization that consumes NumPy arrays
- **scikit-learn** — Machine learning with NumPy as input format
- **TensorFlow/PyTorch** — Deep learning frameworks using NumPy-compatible arrays

---

## 4. Installation and Import

### Installation

```bash
# Using pip
pip install numpy

# Using conda
conda install numpy

# With optional accelerated BLAS/LAPACK
pip install numpy[accelerate]
```

### Standard Import Convention

```python
# THE universal convention — always import as np
import numpy as np

# Verify installation
print(np.__version__)  # e.g., 1.26.4
```

> ⚠️ **Convention Alert**: The community universally uses `np` as the alias. Never deviate from this in production code.

---

## 5. Creating Your First Array

```python
import numpy as np

# From a Python list
arr = np.array([1, 2, 3, 4, 5])
print(arr)        # [1 2 3 4 5]
print(type(arr))  # <class 'numpy.ndarray'>

# 2D array (matrix)
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix)
# [[1 2 3]
#  [4 5 6]]

# Inspecting an array
print(arr.shape)    # (5,)      — dimensions
print(arr.dtype)    # int64     — data type
print(arr.size)     # 5         — total elements
print(arr.ndim)     # 1         — number of dimensions
print(arr.itemsize) # 8         — bytes per element
```

---

## 6. Key Concepts — ndarray

The `ndarray` (N-dimensional array) is NumPy's core data structure.

### Attributes of an ndarray

```python
arr = np.array([[1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0]])

# Shape: (rows, columns)
print(arr.shape)      # (2, 3)

# Data type
print(arr.dtype)      # float64

# Number of dimensions
print(arr.ndim)       # 2

# Total elements
print(arr.size)       # 6

# Bytes per element
print(arr.itemsize)   # 8

# Total bytes consumed
print(arr.nbytes)     # 48

# strides — bytes to step in each dimension
print(arr.strides)    # (24, 8)
```

### Homogeneous Data

```python
# NumPy arrays store ONE type — this is what makes them fast
arr_int = np.array([1, 2, 3])       # int64
arr_float = np.array([1.0, 2.0])    # float64
arr_mixed = np.array([1, 2.5, 3])   # float64 (upcast!)
print(arr_mixed.dtype)               # float64

# You can force a specific type
arr_str = np.array([1, 2, 3], dtype=str)
print(arr_str.dtype)                 # <U11
```

---

## 7. Common Mistakes to Avoid

### Mistake 1: Confusing Lists and Arrays
```python
# WRONG — list operations don't work as expected
[1, 2, 3] + [4, 5, 6]  # [1, 2, 3, 4, 5, 6] — concatenation

# RIGHT — NumPy does element-wise addition
np.array([1, 2, 3]) + np.array([4, 5, 6])  # [5, 7, 9]
```

### Mistake 2: Forgetting NumPy is 0-indexed
```python
arr = np.array([10, 20, 30, 40, 50])
arr[0]   # 10 (first element)
arr[5]   # IndexError!
```

### Mistake 3: Modifying a view unintentionally
```python
a = np.array([1, 2, 3])
b = a[:2]       # This is a VIEW, not a copy!
b[0] = 99
print(a)        # [99  2  3] — a is modified!
```

---

## 8. Best Practices

1. **Always use `import numpy as np`** — the universal convention
2. **Use vectorized operations** — avoid Python `for` loops on arrays
3. **Be explicit about dtype** — `np.array(data, dtype=np.float64)` prevents surprises
4. **Check array shapes before operations** — shape mismatches cause cryptic errors
5. **Use `np.newaxis`** for dimension expansion — clearer than reshape
6. **Prefer `np.arange()` over `range()`** — returns an ndarray directly
7. **Memory awareness** — large arrays consume significant RAM; use appropriate dtypes

---

## 9. Practice Exercises

### Exercise 1: Basic Array Creation
```python
# Create arrays from these Python structures and print their properties
import numpy as np

# a) A 1D array from [10, 20, 30, 40, 50]
# Print: shape, dtype, size, ndim

# b) A 2D array from [[1, 2], [3, 4], [5, 6]]
# Print: shape, dtype, size, ndim

# c) An array of 10 zeros
# Print the array and its type
```

### Exercise 2: Type Coercion
```python
# What dtype do these arrays have? Why?
arr1 = np.array([1, 2, 3])
arr2 = np.array([1.0, 2, 3])
arr3 = np.array([1, 2, "hello"])
arr4 = np.array([True, False, True])
arr5 = np.array([1+2j, 3+4j])
```

### Exercise 3: Performance Comparison
```python
# Time the difference between summing 1M numbers with:
# a) Python's built-in sum()
# b) np.sum() on a NumPy array
# Print the speedup factor
```

---

## 10. Summary

| Concept | Key Takeaway |
|---------|-------------|
| **What** | NumPy = N-dimensional array library for Python |
| **Why** | 10-100x faster than Python lists for numerical work |
| **Core** | `ndarray` — fast, homogeneous, contiguous memory |
| **Import** | Always `import numpy as np` |
| **Convention** | 0-indexed, vectorized operations, broadcasting |
| **Ecosystem** | Foundation for Pandas, SciPy, ML frameworks |

### Key Takeaways

1. NumPy provides the `ndarray` — the most important data structure in Python data science
2. Homogeneous typing + contiguous memory = massive performance gains
3. Broadcasting eliminates the need for element-wise loops
4. The `np` alias is universal — never deviate
5. NumPy is the foundation of the entire scientific Python ecosystem

---

## 🔗 Next Lecture

→ [02-getting-started-lecture.md](./02-getting-started-lecture.md) — Getting Started with NumPy
