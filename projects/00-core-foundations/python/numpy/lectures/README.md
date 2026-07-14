# NumPy Lectures Directory

## Overview

This directory contains comprehensive lecture notes and glossaries for NumPy topics 15-28, covering array filtering, random numbers, data distributions, permutations, and universal functions (ufuncs). Each lecture includes detailed explanations, code examples, common mistakes, best practices, and exercises.

## Directory Structure

```
lectures/
├── 15-array-filter-lecture.md
├── 15-array-filter-glossary.md
├── 16-random-intro-lecture.md
├── 16-random-intro-glossary.md
├── 17-data-distribution-lecture.md
├── 17-data-distribution-glossary.md
├── 18-random-permutation-lecture.md
├── 18-random-permutation-glossary.md
├── 19-ufunc-intro-lecture.md
├── 19-ufunc-intro-glossary.md
├── 20-ufunc-create-lecture.md
├── 20-ufunc-create-glossary.md
├── 21-ufunc-arithmetic-lecture.md
├── 21-ufunc-arithmetic-glossary.md
├── 22-ufunc-rounding-lecture.md
├── 22-ufunc-rounding-glossary.md
├── 23-ufunc-logs-lecture.md
├── 23-ufunc-logs-glossary.md
├── 24-ufunc-summations-lecture.md
├── 24-ufunc-summations-glossary.md
├── 25-ufunc-products-lecture.md
├── 25-ufunc-products-glossary.md
├── 26-ufunc-differences-lecture.md
├── 26-ufunc-differences-glossary.md
├── 27-ufunc-trigonometric-lecture.md
├── 27-ufunc-trigonometric-glossary.md
├── 28-ufunc-set-operations-lecture.md
├── 28-ufunc-set-operations-glossary.md
└── README.md
```

## Lecture Topics

### Array Filtering (Topic 15)
| Lecture | Topic | Description |
|---------|-------|-------------|
| [15-lecture](15-array-filter-lecture.md) | Array Filtering | Boolean indexing, masks, conditional selection |
| [15-glossary](15-array-filter-glossary.md) | Terms | Boolean mask, where, extract, clip |

### Random Numbers (Topics 16-18)
| Lecture | Topic | Description |
|---------|-------|-------------|
| [16-lecture](16-random-intro-lecture.md) | Random Introduction | random, randint, randn, seed, Generator |
| [16-glossary](16-random-intro-glossary.md) | Terms | Random, seed, reproducibility, distributions |
| [17-lecture](17-data-distribution-lecture.md) | Data Distributions | uniform, normal, binomial, Poisson, exponential |
| [17-glossary](17-data-distribution-glossary.md) | Terms | Distribution, mean, std, variance, percentile |
| [18-lecture](18-random-permutation-lecture.md) | Random Permutation | shuffle, permutation, choice, train/test split |
| [18-glossary](18-random-permutation-glossary.md) | Terms | Shuffle, permutation, in-place, copy |

### Universal Functions (Topics 19-28)
| Lecture | Topic | Description |
|---------|-------|-------------|
| [19-lecture](19-ufunc-intro-lecture.md) | Ufunc Introduction | What are ufuncs, types, reduce, accumulate |
| [19-glossary](19-ufunc-intro-glossary.md) | Terms | Ufunc, vectorization, reduce, accumulate |
| [20-lecture](20-ufunc-create-lecture.md) | Creating Ufuncs | frompyfunc, custom functions, string operations |
| [20-glossary](20-ufunc-create-glossary.md) | Terms | frompyfunc, nin, nout, dtype conversion |
| [21-lecture](21-ufunc-arithmetic-lecture.md) | Arithmetic | add, subtract, multiply, divide, power |
| [21-glossary](21-ufunc-arithmetic-glossary.md) | Terms | Arithmetic, broadcasting, matrix multiply |
| [22-lecture](22-ufunc-rounding-lecture.md) | Rounding | round, floor, ceil, trunc, Banker's rounding |
| [22-glossary](22-ufunc-rounding-glossary.md) | Terms | Round, floor, ceil, trunc, decimal places |
| [23-lecture](23-ufunc-logs-lecture.md) | Logarithms | log, log2, log10, exp, power functions |
| [23-glossary](23-ufunc-logs-glossary.md) | Terms | Logarithm, exponential, entropy, decibels |
| [24-lecture](24-ufunc-summations-lecture.md) | Summations | sum, cumsum, axis, where, initial |
| [24-glossary](24-ufunc-summations-glossary.md) | Terms | Sum, cumsum, axis, moving average |
| [25-lecture](25-ufunc-products-lecture.md) | Products | prod, cumprod, compound interest, factorial |
| [25-glossary](25-ufunc-products-glossary.md) | Terms | Product, cumprod, geometric mean, factorial |
| [26-lecture](26-ufunc-differences-lecture.md) | Differences | diff, prepend, append, edge detection |
| [26-glossary](26-ufunc-differences-glossary.md) | Terms | Diff, first/second difference, velocity |
| [27-lecture](27-ufunc-trigonometric-lecture.md) | Trigonometric | sin, cos, tan, arcsin, hyperbolic |
| [27-glossary](27-ufunc-trigonometric-glossary.md) | Terms | Trig, radians, degrees, unit circle |
| [28-lecture](28-ufunc-set-operations-lecture.md) | Set Operations | unique, intersect, union, setdiff, isin |
| [28-glossary](28-ufunc-set-operations-glossary.md) | Terms | Unique, intersection, union, difference |

## Recommended Learning Order

### Track 1: Array Filtering & Random (Prerequisites for ML)
1. **15 - Array Filtering** - Essential for data selection
2. **16 - Random Introduction** - Basic random generation
3. **17 - Data Distributions** - Statistical distributions
4. **18 - Random Permutation** - Shuffling and sampling

### Track 2: Universal Functions (Core Operations)
5. **19 - Ufunc Introduction** - Understanding ufuncs
6. **20 - Creating Ufuncs** - Custom functions
7. **21 - Arithmetic** - Basic math operations
8. **22 - Rounding** - Precision control

### Track 3: Advanced Ufuncs (Specialized Math)
9. **23 - Logarithms** - Exponential and log functions
10. **24 - Summations** - Sum and cumulative sum
11. **25 - Products** - Product and cumulative product
12. **26 - Differences** - Discrete differences

### Track 4: Trig & Set Operations (Applied Math)
13. **27 - Trigonometric** - Trig functions
14. **28 - Set Operations** - Set theory operations

## How to Use Lectures + Glossaries Together

### For Learning
1. **Read the lecture first** for conceptual understanding
2. **Study the glossary** for quick reference and definitions
3. **Run the code examples** in the corresponding `.py` file
4. **Complete the exercises** to test your understanding
5. **Review common mistakes** to avoid pitfalls

### For Reference
1. **Use the glossary** to look up unfamiliar terms
2. **Check the quick reference table** for function syntax
3. **Review related terms** to understand connections

## Study Schedule

### Week 1: Array Filtering & Random Basics
- Day 1-2: Lecture 15 (Array Filtering)
- Day 3-4: Lecture 16 (Random Introduction)
- Day 5: Review and exercises

### Week 2: Distributions & Permutations
- Day 1-2: Lecture 17 (Data Distributions)
- Day 3-4: Lecture 18 (Random Permutation)
- Day 5: Review and exercises

### Week 3: Ufunc Fundamentals
- Day 1: Lecture 19 (Ufunc Introduction)
- Day 2: Lecture 20 (Creating Ufuncs)
- Day 3-4: Lecture 21 (Arithmetic)
- Day 5: Lecture 22 (Rounding)

### Week 4: Advanced Ufuncs
- Day 1: Lecture 23 (Logarithms)
- Day 2: Lecture 24 (Summations)
- Day 3: Lecture 25 (Products)
- Day 4: Lecture 26 (Differences)
- Day 5: Review and exercises

### Week 5: Applied Math & Final Review
- Day 1-2: Lecture 27 (Trigonometric)
- Day 3-4: Lecture 28 (Set Operations)
- Day 5: Comprehensive review

## Prerequisites

- Python basics (variables, loops, functions)
- Basic NumPy array creation (topics 01-14)
- Understanding of array indexing and slicing
- Basic mathematical concepts

## Key Concepts Across All Lectures

### Vectorization
All ufuncs operate element-wise on arrays, leveraging NumPy's vectorized operations for performance.

### Broadcasting
Arithmetic operations automatically handle arrays of different shapes through broadcasting.

### Axis Semantics
- `axis=0`: Operations along rows (down columns)
- `axis=1`: Operations along columns (across rows)

### Memory Efficiency
- Use in-place operations when possible
- Understand views vs copies
- Use appropriate data types

## Quick Reference Card

### Array Filtering
```python
arr[arr > threshold]           # Boolean indexing
np.where(condition, x, y)      # Conditional selection
np.extract(condition, arr)     # Extract elements
np.clip(arr, min, max)         # Limit range
```

### Random Numbers
```python
np.random.random(n)            # Floats [0,1)
np.random.randint(low, high, n) # Integers
np.random.normal(μ, σ, n)      # Normal distribution
np.random.seed(42)             # Reproducibility
```

### Arithmetic Ufuncs
```python
np.add(a, b)                   # a + b
np.subtract(a, b)              # a - b
np.multiply(a, b)              # a * b
np.divide(a, b)                # a / b
np.power(a, b)                 # a ** b
```

### Summation & Products
```python
np.sum(arr)                    # Total sum
np.cumsum(arr)                 # Cumulative sum
np.prod(arr)                   # Total product
np.cumprod(arr)                # Cumulative product
```

### Differences
```python
np.diff(arr)                   # First difference
np.diff(arr, n=2)              # Second difference
np.diff(arr, prepend=0)        # With initial value
```

### Trigonometric
```python
np.sin(arr)                    # Sine (radians)
np.cos(arr)                    # Cosine (radians)
np.tan(arr)                    # Tangent (radians)
np.radians(arr)                # Degrees to radians
np.degrees(arr)                # Radians to degrees
```

### Set Operations
```python
np.unique(arr)                 # Unique elements
np.intersect1d(a, b)           # Common elements
np.union1d(a, b)               # All unique elements
np.setdiff1d(a, b)             # In A not B
np.isin(arr, test)             # Membership test
```

## Resources

- [W3Schools NumPy Tutorial](https://www.w3schools.com/python/numpy/default.asp)
- [NumPy Official Documentation](https://numpy.org/doc/)
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)

## License

Educational use. Based on W3Schools NumPy tutorial concepts.
