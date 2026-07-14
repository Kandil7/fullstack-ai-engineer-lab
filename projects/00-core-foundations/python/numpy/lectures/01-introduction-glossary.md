# NumPy Lecture 01: Introduction — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| ndarray | N-dimensional array — NumPy's core data structure | `np.array([1, 2, 3])` |
| NumPy | Numerical Python — library for numerical computing | `import numpy as np` |
| Vectorization | Element-wise operations without explicit loops | `arr * 2` |
| Broadcasting | Automatic shape alignment for array operations | `arr + scalar` |
| Homogeneous | All elements share the same data type | `np.array([1, 2, 3]).dtype` |
| dtype | Data type of array elements | `np.float64`, `np.int32` |
| Shape | Tuple of array dimensions | `(3, 4)` for 3×4 matrix |
| Axis | Dimension along which operations occur | `axis=0` (rows), `axis=1` (columns) |
| Scalar | Single value (0-dimensional) | `5`, `3.14` |
| ufunc | Universal function — element-wise operations | `np.add()`, `np.sqrt()` |
| contiguous | Elements stored in adjacent memory blocks | Default for `np.array()` |
| strides | Bytes to move along each dimension | `arr.strides` |
| BLAS | Basic Linear Algebra Subprograms — low-level math | Used under the hood |
| LAPACK | Linear Algebra PACKage — matrix algorithms | Used under the hood |

---

## Alphabetical Glossary

### A

#### Array
A collection of elements stored at contiguous memory locations with the same data type. In NumPy, arrays are instances of the `ndarray` class.

```python
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(type(arr))  # <class 'numpy.ndarray'>
```

**Related:** ndarray, dtype, shape

---

#### Array Interface
A protocol that allows objects to expose their data as NumPy arrays. Implemented via `__array__()` or `__array_interface__` attributes.

```python
class MyArray:
    def __array__(self):
        return np.array([1, 2, 3])
```

**Related:** ndarray, buffer protocol

---

#### Axis
A dimension of an array. A 2D array has two axes: axis 0 (rows) and axis 1 (columns). Operations can be applied along specific axes.

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
arr.sum(axis=0)  # [5, 7, 9] — sum along rows
arr.sum(axis=1)  # [6, 15] — sum along columns
```

**Related:** ndarray, shape, ufunc

---

### B

#### Broadcasting
NumPy's method of performing operations on arrays of different shapes by automatically expanding dimensions.

```python
# Scalar broadcasting
arr = np.array([1, 2, 3])
result = arr + 5  # [6, 7, 8]

# Array broadcasting
a = np.array([[1], [2], [3]])  # shape (3, 1)
b = np.array([10, 20, 30])     # shape (3,)
result = a + b  # shape (3, 3) — a expands columns, b expands rows
```

**Related:** ndarray, shape, ufunc

---

### D

#### dtype (Data Type)
The type of data stored in array elements. NumPy supports many numeric types, strings, objects, and more.

```python
arr_float = np.array([1.0, 2.0], dtype=np.float64)
arr_int = np.array([1, 2], dtype=np.int32)
arr_complex = np.array([1+2j, 3+4j], dtype=np.complex128)
```

**Related:** ndarray, type promotion, casting

---

### E

#### Element-wise Operation
An operation applied independently to each element of an array.

```python
arr = np.array([1, 4, 9, 16])
np.sqrt(arr)  # [1.0, 2.0, 3.0, 4.0]
```

**Related:** ufunc, broadcasting, vectorization

---

### F

#### Fortran Order
Memory layout where elements are stored column-first (as in Fortran). Contrast with C order (row-first).

```python
arr_c = np.array([[1, 2], [3, 4]], order='C')    # Row-major
arr_f = np.array([[1, 2], [3, 4]], order='F')    # Column-major
```

**Related:** strides, contiguous, memory layout

---

### M

#### Memory Layout
How array data is organized in physical memory. NumPy supports C-contiguous (row-major) and Fortran-contiguous (column-major) layouts.

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.flags['C_CONTIGUOUS'])    # True
print(arr.flags['F_CONTIGUOUS'])    # False
```

**Related:** strides, contiguous, order

---

### N

#### ndim
The number of dimensions (axes) of an array.

```python
arr_0d = np.array(5)
arr_1d = np.array([1, 2, 3])
arr_2d = np.array([[1, 2], [3, 4]])

print(arr_0d.ndim)  # 0
print(arr_1d.ndim)  # 1
print(arr_2d.ndim)  # 2
```

**Related:** ndarray, shape, axis

---

#### ndarray
The fundamental N-dimensional array class in NumPy. It provides fast, memory-efficient operations on homogeneous data.

```python
arr = np.ndarray(shape=(2, 3), dtype=np.float64)
# or more commonly:
arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
```

**Related:** dtype, shape, ndim, strides, contiguous

---

#### NumPy
Numerical Python — the foundational library for scientific computing. Provides ndarray, mathematical functions, linear algebra, and more.

```python
import numpy as np
print(np.__version__)
```

**Related:** ndarray, scipy, pandas

---

### S

#### Scalar
A 0-dimensional array (single value). NumPy treats scalars as 0-d arrays.

```python
scalar = np.array(42)
print(scalar.ndim)    # 0
print(scalar.shape)   # ()
```

**Related:** ndarray, broadcasting

---

#### Size
The total number of elements in an array.

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.size)  # 6
```

**Related:** shape, ndim, ndarray

---

#### Strides
The number of bytes to move to the next element along each dimension.

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.strides)  # (24, 8) — 24 bytes to next row, 8 bytes to next column
```

**Related:** memory layout, contiguous, itemsize

---

### T

#### Type Promotion
When operations involve different dtypes, NumPy automatically promotes to a common type.

```python
a = np.array([1, 2, 3])         # int64
b = np.array([1.0, 2.0, 3.0])  # float64
c = a + b                       # float64 (promoted from int)
print(c.dtype)                   # float64
```

**Related:** dtype, casting, ufunc

---

### U

#### ufunc (Universal Function)
Functions that operate element-wise on arrays. They are implemented in C and are highly optimized.

```python
arr = np.array([1, 4, 9, 16, 25])
np.sqrt(arr)    # [1. 2. 3. 4. 5.]
np.add(arr, 1)  # [ 2  5 10 17 26]
np.sin(arr)     # element-wise sine
```

**Related:** broadcasting, vectorization, dtype

---

### V

#### Vectorization
The process of converting element-wise operations into array-level operations, eliminating Python loops.

```python
# WITHOUT vectorization (slow)
result = []
for x in range(1000000):
    result.append(x ** 2)

# WITH vectorization (fast)
arr = np.arange(1000000)
result = arr ** 2
```

**Related:** ufunc, broadcasting, ndarray

---

## Related Concepts Map

```
ndarray
├── dtype (data type)
├── shape (dimensions)
├── ndim (number of dimensions)
├── strides (memory stepping)
├── size (total elements)
├── itemsize (bytes per element)
├── contiguous (memory layout)
│
├── Operations
│   ├── Vectorization (loop elimination)
│   ├── Broadcasting (shape alignment)
│   └── ufuncs (element-wise functions)
│
└── Memory
    ├── C order (row-major)
    ├── Fortran order (column-major)
    └── strides (byte stepping)
```
