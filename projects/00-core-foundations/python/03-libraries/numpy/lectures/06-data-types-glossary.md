# NumPy Lecture 06: Data Types — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| dtype | Data type of array elements | `np.float64`, `np.int32` |
| int8 | Signed 8-bit integer (-128 to 127) | `np.array([1], dtype=np.int8)` |
| int16 | Signed 16-bit integer | `np.array([1], dtype=np.int16)` |
| int32 | Signed 32-bit integer | `np.array([1], dtype=np.int32)` |
| int64 | Signed 64-bit integer | `np.array([1], dtype=np.int64)` |
| uint8 | Unsigned 8-bit integer (0-255) | `np.array([1], dtype=np.uint8)` |
| float16 | Half precision float | `np.array([1.0], dtype=np.float16)` |
| float32 | Single precision float | `np.array([1.0], dtype=np.float32)` |
| float64 | Double precision float | `np.array([1.0], dtype=np.float64)` |
| complex64 | Complex float32 | `np.array([1+2j], dtype=np.complex64)` |
| complex128 | Complex float64 | `np.array([1+2j], dtype=np.complex128)` |
| bool | Boolean type | `np.array([True], dtype=np.bool_)` |
| str | Unicode string | `np.array(["hi"], dtype=np.str_)` |
| object | Python object | `np.array([1, "hi"], dtype=np.object_)` |
| astype | Cast to different dtype | `arr.astype(np.float32)` |
| result_type | Determine result dtype | `np.result_type(int8, float32)` |
| promote | Automatic type widening | `int32 + float64 = float64` |
| finfo | Float type information | `np.finfo(np.float32)` |
| iinfo | Integer type information | `np.iinfo(np.int32)` |
| overflow | Exceeding type range | `np.int8(128)` → error |
| truncation | Losing decimal part | `float→int` drops decimals |

---

## Alphabetical Glossary

### A

#### astype
Cast an array to a different data type (returns a copy).

```python
import numpy as np

arr = np.array([1, 2, 3], dtype=np.int64)

# Cast to float
arr_float = arr.astype(np.float32)
print(arr_float.dtype)  # float32

# Cast to string
arr_str = arr.astype(str)
print(arr_str.dtype)  # <U21

# Round before casting float to int
arr_float = np.array([1.7, 2.3, 3.9])
arr_int = np.round(arr_float).astype(np.int32)
print(arr_int)  # [2 2 4]
```

**Note:** `astype()` returns a new array (copy), not a view.

**Related:** dtype, type promotion, casting rules

---

### B

#### Bool (np.bool_)
Boolean data type — True or False.

```python
arr = np.array([True, False, True], dtype=np.bool_)
print(arr.dtype)    # bool
print(arr.itemsize)  # 1 byte

# From comparison
arr = np.array([1, 2, 3, 4, 5])
mask = arr > 3
print(mask.dtype)   # bool
```

**Related:** dtype, boolean indexing

---

### C

#### Casting
Converting array from one dtype to another.

```python
arr = np.array([1, 2, 3], dtype=np.int32)

# Implicit casting in operations
float_arr = np.array([1.0, 2.0, 3.0], dtype=np.float64)
result = arr + float_arr
print(result.dtype)  # float64 — promoted

# Explicit casting
arr_f32 = arr.astype(np.float32)
print(arr_f32.dtype)  # float32
```

**Related:** type promotion, astype, result_type

---

#### Complex64
Complex number type with float32 real and imaginary parts.

```python
arr = np.array([1+2j, 3+4j], dtype=np.complex64)
print(arr.dtype)    # complex64
print(arr.itemsize)  # 8 bytes
```

**Related:** complex128, float32

---

#### Complex128
Complex number type with float64 real and imaginary parts.

```python
arr = np.array([1+2j, 3+4j], dtype=np.complex128)
print(arr.dtype)    # complex128
print(arr.itemsize)  # 16 bytes
```

**Related:** complex64, float64

---

### D

#### Dtype
The data type of array elements. Controls memory allocation and operations.

```python
arr = np.array([1, 2, 3], dtype=np.float64)
print(arr.dtype)    # float64
print(arr.itemsize)  # 8 bytes

# Common dtypes
np.int8, np.int16, np.int32, np.int64  # Integers
np.uint8, np.uint16, np.uint32, np.uint64  # Unsigned
np.float16, np.float32, np.float64  # Floats
np.complex64, np.complex128  # Complex
np.bool_, np.str_, np.object_  # Special
```

**Related:** astype, type promotion, itemsize

---

### F

#### Float16
Half-precision floating point (16 bits).

```python
arr = np.array([1.123456789], dtype=np.float16)
print(arr[0])       # 1.123 — precision loss!
print(arr.itemsize)  # 2 bytes

# Range
print(np.finfo(np.float16).max)  # 65504
print(np.finfo(np.float16).min)  # -65504
```

**Note:** Only 3-4 decimal digits of precision. Use for memory-critical applications.

**Related:** float32, float64, finfo

---

#### Float32
Single-precision floating point (32 bits).

```python
arr = np.array([1.123456789], dtype=np.float32)
print(arr[0])       # 1.1234568 — good precision
print(arr.itemsize)  # 4 bytes

# Range
print(np.finfo(np.float32).max)  # 3.4028235e+38
```

**Note:** 7-8 decimal digits of precision. Standard for ML/deep learning.

**Related:** float16, float64, finfo

---

#### Float64
Double-precision floating point (64 bits). NumPy's default float type.

```python
arr = np.array([1.123456789], dtype=np.float64)
print(arr[0])       # 1.123456789 — full precision
print(arr.itemsize)  # 8 bytes

# Range
print(np.finfo(np.float64).max)  # 1.7976931348623157e+308
```

**Note:** 15-16 decimal digits of precision. Default for scientific computing.

**Related:** float16, float32, finfo

---

#### Finfo
Get information about floating-point types.

```python
info = np.finfo(np.float32)
print(info.dtype)    # float32
print(info.bits)     # 32
print(info.max)      # 3.4028235e+38
print(info.min)      # -3.4028235e+38
print(info.precision)  # 7
print(info.resolution)  # 1e-05
```

**Related:** iinfo, dtype

---

### I

#### Iinfo
Get information about integer types.

```python
info = np.iinfo(np.int32)
print(info.dtype)    # int32
print(info.bits)     # 32
print(info.max)      # 2147483647
print(info.min)      # -2147483648
```

**Related:** finfo, dtype

---

#### Int8
Signed 8-bit integer (-128 to 127).

```python
arr = np.array([100, 127, -128], dtype=np.int8)
print(arr.dtype)    # int8
print(arr.itemsize)  # 1 byte

# Overflow example
arr = np.array([128], dtype=np.int8)
print(arr)  # [-128] — overflow!
```

**Related:** int16, uint8, iinfo

---

#### Int16
Signed 16-bit integer (-32768 to 32767).

```python
arr = np.array([32767, -32768], dtype=np.int16)
print(arr.dtype)    # int16
print(arr.itemsize)  # 2 bytes
```

**Related:** int8, int32, iinfo

---

#### Int32
Signed 32-bit integer (±2.1 billion).

```python
arr = np.array([2147483647, -2147483648], dtype=np.int32)
print(arr.dtype)    # int32
print(arr.itemsize)  # 4 bytes
```

**Related:** int16, int64, iinfo

---

#### Int64
Signed 64-bit integer (±9.2×10^18). NumPy's default integer type.

```python
arr = np.array([1, 2, 3], dtype=np.int64)
print(arr.dtype)    # int64
print(arr.itemsize)  # 8 bytes

# Default type
arr = np.array([1, 2, 3])
print(arr.dtype)    # int64 (default)
```

**Related:** int32, iinfo

---

### O

#### Object (np.object_)
Stores Python objects (slow, avoid when possible).

```python
arr = np.array([1, "hello", [1, 2, 3]], dtype=np.object_)
print(arr.dtype)    # object
print(arr.itemsize)  # platform-dependent

# Slow operations — no vectorization
```

**Note:** Use only when you must store mixed types. Defeats NumPy's performance advantages.

**Related:** dtype, str

---

#### Overflow
Exceeding the range of a data type.

```python
# int8 can only hold -128 to 127
arr = np.array([128], dtype=np.int8)
print(arr)  # [-128] — wraps around!

# int16 can hold larger values
arr = np.array([128], dtype=np.int16)
print(arr)  # [128] — no overflow

# Check range before creating
print(np.iinfo(np.int8).max)   # 127
print(np.iinfo(np.int16).max)  # 32767
```

**Related:** int8, int16, iinfo

---

### R

#### Result_type
Determine the result type of operations without computing.

```python
dt = np.result_type(np.int8, np.float32)
print(dt)  # float32

dt = np.result_type(np.int32, np.int64)
print(dt)  # int64

dt = np.result_type(np.bool_, np.int32, np.float64)
print(dt)  # float64
```

**Related:** type promotion, dtype

---

### S

#### Str (np.str_)
Unicode string data type.

```python
arr = np.array(["hello", "world"], dtype=np.str_)
print(arr.dtype)    # <U5
print(arr.itemsize)  # 20 bytes (5 chars × 4 bytes each)

# Fixed-width strings
arr = np.array(["hi", "hello"], dtype='U5')
print(arr)  # ['hi' 'hello']
```

**Related:** bytes_, object_

---

### T

#### Truncation
Losing the decimal part when converting float to integer.

```python
arr_float = np.array([1.7, 2.3, 3.9])

# Truncation (drops decimals)
arr_int = arr_float.astype(np.int32)
print(arr_int)  # [1 2 3] — truncated!

# Round first to avoid truncation
arr_int = np.round(arr_float).astype(np.int32)
print(arr_int)  # [2 2 4]
```

**Related:** astype, type casting

---

#### Type Promotion
Automatic widening of types in operations to prevent data loss.

```python
# Int + Float → Float
a = np.array([1, 2], dtype=np.int32)
b = np.array([1.0, 2.0], dtype=np.float64)
c = a + b
print(c.dtype)  # float64

# Int8 + Int64 → Int64
a = np.array([1, 2], dtype=np.int8)
b = np.array([1, 2], dtype=np.int64)
c = a + b
print(c.dtype)  # int64

# Bool + Int → Int
a = np.array([True, False], dtype=np.bool_)
b = np.array([1, 2], dtype=np.int32)
c = a + b
print(c.dtype)  # int32
```

**Hierarchy:** bool → int → float → complex

**Related:** result_type, dtype, casting

---

### U

#### Uint8
Unsigned 8-bit integer (0 to 255). Common for image data.

```python
arr = np.array([0, 128, 255], dtype=np.uint8)
print(arr.dtype)    # uint8
print(arr.itemsize)  # 1 byte

# Image data example
img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
```

**Related:** int8, uint16, dtype

---

## Type Size Comparison

| Type | Bytes | Range (approx) | Precision |
|------|-------|----------------|-----------|
| int8 | 1 | -128 to 127 | — |
| int16 | 2 | ±32K | — |
| int32 | 4 | ±2.1B | — |
| int64 | 8 | ±9.2×10^18 | — |
| uint8 | 1 | 0 to 255 | — |
| uint16 | 2 | 0 to 65535 | — |
| uint32 | 4 | 0 to 4.3B | — |
| uint64 | 8 | 0 to 1.8×10^19 | — |
| float16 | 2 | ±65504 | ~3 digits |
| float32 | 4 | ±3.4×10^38 | ~7 digits |
| float64 | 8 | ±1.8×10^308 | ~15 digits |
| complex64 | 8 | — | 2×float32 |
| complex128 | 16 | — | 2×float64 |
| bool | 1 | True/False | — |
| str | varies | Unicode | — |
