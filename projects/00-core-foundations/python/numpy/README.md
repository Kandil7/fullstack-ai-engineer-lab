# NumPy Tutorial - Complete Exercise Set

A comprehensive collection of 28 NumPy exercise scripts based on the [W3Schools NumPy Tutorial](https://www.w3schools.com/python/numpy/default.asp).

Each script contains **3-5 complete working examples** with output comments, covering every topic in the W3Schools NumPy curriculum.

## Quick Start

```bash
# Install NumPy (if not already installed)
pip install numpy

# Run any exercise file
python 01-introduction.py

# Run all files sequentially
for f in *.py; do echo "=== $f ==="; python "$f"; echo; done
```

## Files Index

### Getting Started
| File | Topic | W3Schools Link |
|------|-------|----------------|
| `01-introduction.py` | What is NumPy, array vs list, performance | [Intro](https://www.w3schools.com/python/numpy_intro.asp) |
| `02-getting-started.py` | Installation, first arrays, operations | [Getting Started](https://www.w3schools.com/python/numpy_getting_started.asp) |
| `03-creating-arrays.py` | zeros, ones, arange, linspace, random | [Creating Arrays](https://www.w3schools.com/python/numpy_creating_arrays.asp) |

### Array Basics
| File | Topic | W3Schools Link |
|------|-------|----------------|
| `04-array-indexing.py` | Access elements, 2D/3D indexing, negative indices | [Indexing](https://www.w3schools.com/python/numpy_array_indexing.asp) |
| `05-array-slicing.py` | Slicing syntax, fancy indexing, boolean indexing | [Slicing](https://www.w3schools.com/python/numpy_array_slicing.asp) |
| `06-data-types.py` | dtypes, astype, overflow, precision | [Data Types](https://www.w3schools.com/python/numpy_data_types.asp) |
| `07-copy-vs-view.py` | Copies vs views, base attribute, memory | [Copy vs View](https://www.w3schools.com/python/numpy_copy_vs_view.asp) |

### Shape Manipulation
| File | Topic | W3Schools Link |
|------|-------|----------------|
| `08-array-shape.py` | shape, ndim, size, transpose | [Array Shape](https://www.w3schools.com/python/numpy_array_shape.asp) |
| `09-array-reshape.py` | reshape, flatten, ravel, resize, squeeze | [Array Reshape](https://www.w3schools.com/python/numpy_array_reshape.asp) |
| `10-array-iterating.py` | for loops, nditer, ndenumerate, flags | [Array Iterating](https://www.w3schools.com/python/numpy_array_iterating.asp) |

### Array Operations
| File | Topic | W3Schools Link |
|------|-------|----------------|
| `11-array-join.py` | concatenate, stack, hstack, vstack | [Array Join](https://www.w3schools.com/python/numpy_array_join.asp) |
| `12-array-split.py` | split, array_split, hsplit, vsplit | [Array Split](https://www.w3schools.com/python/numpy_array_split.asp) |
| `13-array-search.py` | where, searchsorted, argmax, argmin, nonzero | [Array Search](https://www.w3schools.com/python/numpy_array_search.asp) |
| `14-array-sort.py` | sort, argsort, lexsort, sorting algorithms | [Array Sort](https://www.w3schools.com/python/numpy_array_sort.asp) |
| `15-array-filter.py` | Boolean indexing, where, extract, masking | [Array Filter](https://www.w3schools.com/python/numpy_array_filter.asp) |

### Random Numbers
| File | Topic | W3Schools Link |
|------|-------|----------------|
| `16-random-intro.py` | random, randint, randn, seed, Generator | [Random Intro](https://www.w3schools.com/python/numpy_random_intro.asp) |
| `17-data-distribution.py` | uniform, normal, binomial, poisson, exponential | [Data Distribution](https://www.w3schools.com/python/numpy_random_distribution.asp) |
| `18-random-permutation.py` | shuffle, permutation, choice | [Random Permutation](https://www.w3schools.com/python/numpy_random_permutation.asp) |

### Universal Functions (ufuncs)
| File | Topic | W3Schools Link |
|------|-------|----------------|
| `19-ufunc-intro.py` | What are ufuncs, types, reduce, accumulate | [Ufunc Intro](https://www.w3schools.com/python/numpy_ufunc_intro.asp) |
| `20-ufunc-create.py` | frompyfunc, custom ufuncs | [Ufunc Create](https://www.w3schools.com/python/numpy_ufunc_create.asp) |
| `21-ufunc-arithmetic.py` | add, subtract, multiply, divide, power | [Ufunc Arithmetic](https://www.w3schools.com/python/numpy_ufunc_arithmetic.asp) |
| `22-ufunc-rounding.py` | round, floor, ceil, trunc | [Ufunc Rounding](https://www.w3schools.com/python/numpy_ufunc_rounding.asp) |
| `23-ufunc-logs.py` | log, log2, log10, exp, power | [Ufunc Logs](https://www.w3schools.com/python/numpy_ufunc_logs.asp) |
| `24-ufunc-summations.py` | sum, cumsum, where-based sums | [Ufunc Summations](https://www.w3schools.com/python/numpy_ufunc_summations.asp) |
| `25-ufunc-products.py` | prod, cumprod | [Ufunc Products](https://www.w3schools.com/python/numpy_ufunc_products.asp) |
| `26-ufunc-differences.py` | diff, cumulative differences | [Ufunc Differences](https://www.w3schools.com/python/numpy_ufunc_differences.asp) |
| `27-ufunc-trigonometric.py` | sin, cos, tan, inverse, hyperbolic | [Ufunc Trig](https://www.w3schools.com/python/numpy_ufunc_trigonometric.asp) |
| `28-ufunc-set-operations.py` | unique, intersect, union, diff, isin | [Ufunc Set Ops](https://www.w3schools.com/python/numpy_ufunc_set_operations.asp) |

## Learning Path

**Recommended order:**

1. **Fundamentals** (01-03): Introduction, setup, creating arrays
2. **Core Operations** (04-07): Indexing, slicing, types, memory
3. **Shape & Structure** (08-10): Reshaping, iterating
4. **Array Manipulation** (11-15): Joining, splitting, searching, sorting, filtering
5. **Random Numbers** (16-18): Generation and distributions
6. **Universal Functions** (19-28): Math, stats, and set operations

## Key Concepts

### Array Creation
```python
import numpy as np

# From list
arr = np.array([1, 2, 3, 4, 5])

# Common patterns
zeros = np.zeros((3, 4))           # 3x4 zeros
ones = np.ones(5)                   # 5 ones
rng = np.random.default_rng(42)     # Modern RNG
rand_arr = rng.random((3, 3))       # 3x3 random [0,1)
```

### Indexing & Slicing
```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

arr[0, 1]       # Element: 2
arr[1]          # Row 1: [4 5 6]
arr[:, 0]       # Column 0: [1 4 7]
arr[0:2, 1:3]   # Sub-matrix
arr[arr > 5]    # Boolean filter: [6 7 8 9]
```

### Broadcasting
```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
row = np.array([10, 20, 30])

# Broadcasting: add row to each row
result = arr + row  # [[11 22 33], [14 25 36]]
```

### Vectorization
```python
# Slow: Python loop
result = []
for x in arr:
    result.append(x * 2)

# Fast: NumPy vectorization
result = arr * 2  # 10-100x faster!
```

## Running Individual Examples

Each script is self-contained. Run any file directly:

```bash
python 01-introduction.py      # ~50 lines
python 28-ufunc-set-operations.py  # ~150 lines
```

All output is printed with comments showing expected values.

## Resources

- [W3Schools NumPy Tutorial](https://www.w3schools.com/python/numpy/default.asp)
- [NumPy Official Documentation](https://numpy.org/doc/)
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy API Reference](https://numpy.org/doc/stable/reference/)

## License

Educational use. Based on W3Schools NumPy tutorial concepts.
