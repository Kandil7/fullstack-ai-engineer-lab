# 📐 NumPy — Numerical Computing

34 self-contained topic directories covering NumPy from basics through advanced topics like linear algebra and advanced indexing.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

```
numpy/
├── 01-introduction/
│   ├── 01-introduction.py
│   ├── 01-introduction-lecture.md
│   └── 01-introduction-glossary.md
├── 02-getting-started/
└── ... (34 topics)
```

## 📚 Topics

### Getting Started (01-03)
| # | Topic | Description |
|---|-------|-------------|
| 01 | Introduction | What is NumPy, array vs list, performance |
| 02 | Getting Started | Installation, first arrays, operations |
| 03 | Creating Arrays | zeros, ones, arange, linspace, random |

### Array Basics (04-07)
| # | Topic | Description |
|---|-------|-------------|
| 04 | Array Indexing | Access elements, 2D/3D indexing |
| 05 | Array Slicing | Slicing syntax, fancy indexing |
| 06 | Data Types | dtypes, astype, overflow, precision |
| 07 | Copy vs View | Copies vs views, base attribute |

### Shape Manipulation (08-10)
| # | Topic | Description |
|---|-------|-------------|
| 08 | Array Shape | shape, ndim, size, transpose |
| 09 | Array Reshape | reshape, flatten, ravel, resize |
| 10 | Array Iterating | for loops, nditer, ndenumerate |

### Array Operations (11-15)
| # | Topic | Description |
|---|-------|-------------|
| 11 | Array Join | concatenate, stack, hstack, vstack |
| 12 | Array Split | split, array_split, hsplit, vsplit |
| 13 | Array Search | where, searchsorted, argmax, argmin |
| 14 | Array Sort | sort, argsort, lexsort |
| 15 | Array Filter | Boolean indexing, where, extract |

### Random Numbers (16-18)
| # | Topic | Description |
|---|-------|-------------|
| 16 | Random Intro | random, randint, randn, seed |
| 17 | Data Distribution | uniform, normal, binomial, poisson |
| 18 | Random Permutation | shuffle, permutation, choice |

### Universal Functions (19-28)
| # | Topic | Description |
|---|-------|-------------|
| 19 | Ufunc Intro | What are ufuncs, types, reduce |
| 20 | Ufunc Create | frompyfunc, custom ufuncs |
| 21 | Ufunc Arithmetic | add, subtract, multiply, divide |
| 22 | Ufunc Rounding | round, floor, ceil, trunc |
| 23 | Ufunc Logs | log, log2, log10, exp, power |
| 24 | Ufunc Summations | sum, cumsum, where-based sums |
| 25 | Ufunc Products | prod, cumprod |
| 26 | Ufunc Differences | diff, cumulative differences |
| 27 | Ufunc Trigonometric | sin, cos, tan, inverse |
| 28 | Ufunc Set Operations | unique, intersect, union, diff |

### Advanced Topics (29-34)
| # | Topic | Description |
|---|-------|-------------|
| 29 | Broadcasting Deep | Broadcasting rules and patterns |
| 30 | Vectorization | Vectorized operations vs loops |
| 31 | Memory and Strides | Memory layout, strides, contiguous |
| 32 | Dtypes and Precision | dtype selection, precision |
| 33 | Linear Algebra | Matrix operations, decompositions |
| 34 | Advanced Indexing | Fancy indexing, boolean masks |

## 🚀 Quick Start

```bash
# Run any topic
python 01-introduction/01-introduction.py

# Run all topics
for d in [0-9]*/; do
    py=$(ls "$d"/*.py 2>/dev/null | head -1)
    [ -n "$py" ] && echo "=== $d ===" && python "$py"
done
```

## 📖 Recommended Learning Order

1. **Fundamentals** (01-03): Introduction, setup, creating arrays
2. **Core Operations** (04-07): Indexing, slicing, types, memory
3. **Shape & Structure** (08-10): Reshaping, iterating
4. **Array Manipulation** (11-15): Joining, splitting, searching, sorting
5. **Random Numbers** (16-18): Generation and distributions
6. **Universal Functions** (19-28): Math, stats, and set operations
7. **Advanced Topics** (29-34): Broadcasting, vectorization, linear algebra

---

*Last updated: August 2026*
