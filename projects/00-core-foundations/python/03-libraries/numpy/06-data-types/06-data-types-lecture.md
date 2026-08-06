# NumPy Lecture 06: Data Types

## 🎯 Topic Overview

NumPy arrays are homogeneous — all elements share the same data type (dtype). Understanding dtypes is crucial for memory efficiency, precision control, and avoiding subtle bugs. This lecture covers NumPy's type system, type casting, type promotion, and practical dtype management.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Identify and use NumPy's numeric data types
2. Control array dtype at creation time
3. Cast arrays between different dtypes
4. Understand type promotion rules
5. Choose appropriate dtypes for memory and precision
6. Handle special types (strings, booleans, complex)
7. Debug dtype-related issues

---

## 1. NumPy Data Types Overview

### 1.1 Integer Types

```python
import numpy as np

# Signed integers (can be negative)
i8 = np.array([1, 2, 3], dtype=np.int8)     # -128 to 127
i16 = np.array([1, 2, 3], dtype=np.int16)   # -32768 to 32767
i32 = np.array([1, 2, 3], dtype=np.int32)   # -2^31 to 2^31-1
i64 = np.array([1, 2, 3], dtype=np.int64)   # -2^63 to 2^63-1

print(f"int8:  {i8.dtype}, size: {i8.itemsize}")    # int8, 1 byte
print(f"int16: {i16.dtype}, size: {i16.itemsize}")   # int16, 2 bytes
print(f"int32: {i32.dtype}, size: {i32.itemsize}")   # int32, 4 bytes
print(f"int64: {i64.dtype}, size: {i64.itemsize}")   # int64, 8 bytes

# Unsigned integers (0 and positive only)
u8 = np.array([1, 2, 3], dtype=np.uint8)    # 0 to 255
u16 = np.array([1, 2, 3], dtype=np.uint16)  # 0 to 65535
u32 = np.array([1, 2, 3], dtype=np.uint32)  # 0 to 2^32-1
u64 = np.array([1, 2, 3], dtype=np.uint64)  # 0 to 2^64-1
```

### 1.2 Float Types

```python
# Floating-point types
f16 = np.array([1.5, 2.5], dtype=np.float16)   # Half precision
f32 = np.array([1.5, 2.5], dtype=np.float32)   # Single precision
f64 = np.array([1.5, 2.5], dtype=np.float64)   # Double precision (default!)

print(f"float16: {f16.dtype}, size: {f16.itemsize}")   # 2 bytes
print(f"float32: {f32.dtype}, size: {f32.itemsize}")   # 4 bytes
print(f"float64: {f64.dtype}, size: {f64.itemsize}")   # 8 bytes

# Precision comparison
print(f"float16 max: {np.finfo(np.float16).max}")   # 65504
print(f"float32 max: {np.finfo(np.float32).max}")   # 3.4028235e+38
print(f"float64 max: {np.finfo(np.float64).max}")   # 1.7976931348623157e+308
```

### 1.3 Complex Types

```python
# Complex numbers
c64 = np.array([1+2j, 3+4j], dtype=np.complex64)
c128 = np.array([1+2j, 3+4j], dtype=np.complex128)

print(f"complex64:  {c64.dtype}, size: {c64.itemsize}")   # 8 bytes
print(f"complex128: {c128.dtype}, size: {c128.itemsize}") # 16 bytes
```

### 1.4 Boolean and String Types

```python
# Boolean
bool_arr = np.array([True, False, True], dtype=np.bool_)
print(f"bool: {bool_arr.dtype}, size: {bool_arr.itemsize}")  # 1 byte

# String (Unicode)
str_arr = np.array(["hello", "world"], dtype=np.str_)
print(f"str: {str_arr.dtype}")  # <U5

# Fixed-width string
bytes_arr = np.array([b"hello", b"world"], dtype=np.bytes_)
print(f"bytes: {bytes_arr.dtype}")  # |S5
```

### 1.5 Object Type

```python
# Object type — stores Python objects (slow, avoid when possible)
obj_arr = np.array([1, "hello", [1, 2, 3]], dtype=np.object_)
print(f"object: {obj_arr.dtype}")  # object
```

---

## 2. Specifying dtype at Creation

### 2.1 Using dtype Parameter

```python
# Explicit dtype
arr_int8 = np.array([1, 2, 3], dtype=np.int8)
arr_float32 = np.array([1, 2, 3], dtype=np.float32)

# Using strings
arr = np.array([1, 2, 3], dtype="int32")
arr = np.array([1, 2, 3], dtype="float64")
arr = np.array([1, 2, 3], dtype="complex128")

# Using Python types
arr = np.array([1, 2, 3], dtype=int)
arr = np.array([1, 2, 3], dtype=float)
arr = np.array([1, 2, 3], dtype=complex)
```

### 2.2 dtype Aliases

```python
# NumPy provides many aliases
arr = np.array([1, 2, 3], dtype=np.int_)      # Platform integer
arr = np.array([1, 2, 3], dtype=np.float_)    # Platform float
arr = np.array([1, 2, 3], dtype=np.complex_)  # Platform complex
arr = np.array([1, 2, 3], dtype=np.bool_)     # Boolean
arr = np.array([1, 2, 3], dtype=np.str_)      # String
arr = np.array([1, 2, 3], dtype=np.object_)   # Object

# Character codes (legacy, but still works)
arr = np.array([1, 2, 3], dtype='i')   # int
arr = np.array([1, 2, 3], dtype='f')   # float
arr = np.array([1, 2, 3], dtype='d')   # double
arr = np.array([1, 2, 3], dtype='b')   # byte (int8)
```

---

## 3. Type Casting (astype)

### 3.1 Basic Casting

```python
arr = np.array([1, 2, 3, 4, 5], dtype=np.int64)

# Cast to different types
arr_float = arr.astype(np.float32)
print(arr_float.dtype)  # float32
print(arr_float)        # [1. 2. 3. 4. 5.]

arr_int8 = arr.astype(np.int8)
print(arr_int8.dtype)   # int8

# Using string
arr_str = arr.astype("float64")
print(arr_str.dtype)    # float64
```

### 3.2 Casting with Copy vs View

```python
arr = np.array([1, 2, 3], dtype=np.int64)

# astype returns a COPY (new array)
arr_float = arr.astype(np.float32)
print(np.shares_memory(arr, arr_float))  # False

# To avoid copy, use view (only works for compatible types)
arr_view = arr.view(np.float64)  # Only works if memory compatible!
print(np.shares_memory(arr, arr_view))  # True (but data may be wrong!)
```

### 3.3 Casting Rules

```python
# Integers to floats
arr_int = np.array([1, 2, 3], dtype=np.int32)
arr_float = arr_int.astype(np.float64)
print(arr_float.dtype)  # float64

# Floats to integers (truncates!)
arr_float = np.array([1.7, 2.3, 3.9], dtype=np.float64)
arr_int = arr_float.astype(np.int32)
print(arr_int)  # [1 2 3] — truncated, not rounded!

# Safe casting
try:
    arr = np.array([1000], dtype=np.int8)  # Overflow!
    print(arr)  # [-24] — unexpected!
except:
    pass

# Use safe casting
from numpy import result_type
dt = np.result_type(np.int8, np.int32)
print(dt)  # int32
```

---

## 4. Type Promotion Rules

### 4.1 NumPy's Type Hierarchy

```
bool → int8 → int16 → int32 → int64
                   ↓
float16 → float32 → float64 → longdouble
                   ↓
complex64 → complex128 → clongdouble
```

### 4.2 Promotion in Operations

```python
# Int + Float → Float
a = np.array([1, 2, 3], dtype=np.int32)
b = np.array([1.0, 2.0, 3.0], dtype=np.float64)
c = a + b
print(c.dtype)  # float64 — promoted to larger type

# Int8 + Int64 → Int64
a = np.array([1, 2], dtype=np.int8)
b = np.array([1, 2], dtype=np.int64)
c = a + b
print(c.dtype)  # int64

# Float32 + Float64 → Float64
a = np.array([1.0, 2.0], dtype=np.float32)
b = np.array([1.0, 2.0], dtype=np.float64)
c = a + b
print(c.dtype)  # float64

# Bool + Int → Int
a = np.array([True, False], dtype=np.bool_)
b = np.array([1, 2], dtype=np.int32)
c = a + b
print(c.dtype)  # int32
```

### 4.3 np.result_type

```python
# Determine result type without computing
dt = np.result_type(np.int8, np.float32)
print(dt)  # float32

dt = np.result_type(np.int32, np.int64, np.float32)
print(dt)  # float64

dt = np.result_type(np.bool_, np.int32)
print(dt)  # int32
```

---

## 5. Memory and Precision Trade-offs

### 5.1 Memory Usage

```python
import sys

# Compare memory usage
n = 1000000

arr_int8 = np.zeros(n, dtype=np.int8)
arr_int32 = np.zeros(n, dtype=np.int32)
arr_int64 = np.zeros(n, dtype=np.int64)
arr_float32 = np.zeros(n, dtype=np.float32)
arr_float64 = np.zeros(n, dtype=np.float64)

print(f"int8:   {arr_int8.nbytes:>10,} bytes ({arr_int8.nbytes/1024/1024:.1f} MB)")
print(f"int32:  {arr_int32.nbytes:>10,} bytes ({arr_int32.nbytes/1024/1024:.1f} MB)")
print(f"int64:  {arr_int64.nbytes:>10,} bytes ({arr_int64.nbytes/1024/1024:.1f} MB)")
print(f"float32: {arr_float32.nbytes:>10,} bytes ({arr_float32.nbytes/1024/1024:.1f} MB)")
print(f"float64: {arr_float64.nbytes:>10,} bytes ({arr_float64.nbytes/1024/1024:.1f} MB)")
```

### 5.2 Precision Limits

```python
# float16 precision
print(np.finfo(np.float16))  # 3-4 decimal digits precision

# float32 precision
print(np.finfo(np.float32))  # 7-8 decimal digits precision

# float64 precision
print(np.finfo(np.float64))  # 15-16 decimal digits precision

# Example: precision loss
arr_f16 = np.array([1.123456789], dtype=np.float16)
arr_f32 = np.array([1.123456789], dtype=np.float32)
arr_f64 = np.array([1.123456789], dtype=np.float64)

print(f"float16: {arr_f16[0]}")  # 1.123
print(f"float32: {arr_f32[0]}")  # 1.1234568
print(f"float64: {arr_f64[0]}")  # 1.123456789
```

---

## 6. Special Types

### 6.1 Datetime and Timedelta

```python
# Datetime
dates = np.array(['2024-01-01', '2024-01-02', '2024-01-03'], dtype='datetime64')
print(dates)  # ['2024-01-01' '2024-01-02' '2024-01-03']
print(dates.dtype)  # datetime64[D]

# Timedelta
deltas = np.array([1, 2, 3], dtype='timedelta64[D]')
print(deltas)  # [1 2 3] days
print(deltas.dtype)  # timedelta64[D]

# Date arithmetic
tomorrow = dates[0] + np.timedelta64(1, 'D')
print(tomorrow)  # 2024-01-02
```

### 6.2 Structured Arrays

```python
# Structured array with named fields
dt = np.dtype([('name', 'U10'), ('age', 'i4'), ('salary', 'f8')])
employees = np.array([
    ('Alice', 30, 75000.0),
    ('Bob', 25, 65000.0),
    ('Charlie', 35, 85000.0)
], dtype=dt)

print(employees['name'])      # ['Alice' 'Bob' 'Charlie']
print(employees['salary'])    # [75000. 65000. 85000.]
```

---

## 7. Common Mistakes to Avoid

### Mistake 1: Overflow with Small dtypes
```python
# BAD — overflow
arr = np.array([128], dtype=np.int8)
print(arr)  # [-128] — overflow!

# GOOD — use appropriate dtype
arr = np.array([128], dtype=np.int16)
print(arr)  # [128]
```

### Mistake 2: Truncation When Casting Float to Int
```python
# BAD — truncation
arr_float = np.array([1.7, 2.3, 3.9])
arr_int = arr_float.astype(np.int32)
print(arr_int)  # [1 2 3] — truncated, not rounded!

# GOOD — round first
arr_int = np.round(arr_float).astype(np.int32)
print(arr_int)  # [2 2 4]
```

### Mistake 3: Precision Loss in float16
```python
# BAD — precision loss
arr = np.array([1.123456789], dtype=np.float16)
print(arr[0])  # 1.123 — lost precision

# GOOD — use float32 or float64
arr = np.array([1.123456789], dtype=np.float32)
print(arr[0])  # 1.1234568
```

### Mistake 4: Comparing Floats for Equality
```python
# BAD — floating point comparison
a = np.array([0.1 + 0.2])
b = np.array([0.3])
print(a == b)  # [False] — due to floating point precision!

# GOOD — use np.isclose()
print(np.isclose(a, b))  # [True]
```

---

## 8. Best Practices

1. **Use `np.float32`** for most ML/deep learning (saves memory, GPU-optimized)
2. **Use `np.float64`** when precision matters (scientific computing)
3. **Use `np.int32`** as default integer type (good balance)
4. **Use `np.int8`/`np.uint8`** for image data (0-255 range)
5. **Always check dtype** before operations: `print(arr.dtype)`
6. **Use `np.result_type()`** to determine result type without computation
7. **Use `np.isclose()`** for float comparison, never `==`
8. **Round before casting** float to int to avoid truncation
9. **Avoid `np.object_`** — it's slow and defeats NumPy's optimizations

---

## 9. Practice Exercises

### Exercise 1: dtype Identification
```python
import numpy as np

# What dtype does each array have? Why?
arr1 = np.array([1, 2, 3])
arr2 = np.array([1.0, 2.0, 3.0])
arr3 = np.array([1, 2.0, 3])
arr4 = np.array([True, False, True])
arr5 = np.array(["a", "b", "c"])
arr6 = np.array([1+2j, 3+4j])

# Print dtypes and sizes
for i, arr in enumerate([arr1, arr2, arr3, arr4, arr5, arr6], 1):
    print(f"arr{i}: dtype={arr.dtype}, size={arr.itemsize} bytes")
```

### Exercise 2: Type Casting
```python
# Create an array of floats and cast to different types
arr = np.array([1.5, 2.7, 3.14, 4.99, 5.0])

# a) Cast to int32 — what happens?
# b) Cast to int32 after rounding — what happens?
# c) Cast to float16 — compare precision
# d) Cast to string

# Solutions:
arr_int = arr.astype(np.int32)
print(f"int32 (truncated): {arr_int}")  # [1 2 3 4 5]

arr_int_round = np.round(arr).astype(np.int32)
print(f"int32 (rounded): {arr_int_round}")  # [2 3 3 5 5]

arr_f16 = arr.astype(np.float16)
print(f"float16: {arr_f16}")  # Precision loss

arr_str = arr.astype(str)
print(f"string: {arr_str}")
```

### Exercise 3: Memory Comparison
```python
import sys

# Compare memory for 1M elements
n = 1000000

dtypes = [np.int8, np.int16, np.int32, np.int64,
          np.float16, np.float32, np.float64]

for dt in dtypes:
    arr = np.zeros(n, dtype=dt)
    print(f"{str(dt):>10}: {arr.nbytes:>12,} bytes ({arr.nbytes/1024/1024:.1f} MB)")
```

### Exercise 4: Type Promotion
```python
# Predict the result dtype of these operations
a_int32 = np.array([1, 2, 3], dtype=np.int32)
b_float64 = np.array([1.0, 2.0, 3.0], dtype=np.float64)

c = a_int32 + b_float64
print(f"int32 + float64 = {c.dtype}")  # float64

a_int8 = np.array([1, 2], dtype=np.int8)
b_int64 = np.array([1, 2], dtype=np.int64)
c = a_int8 + b_int64
print(f"int8 + int64 = {c.dtype}")  # int64

a_bool = np.array([True, False], dtype=np.bool_)
b_int = np.array([1, 2], dtype=np.int32)
c = a_bool + b_int
print(f"bool + int32 = {c.dtype}")  # int32
```

---

## 10. Summary

| Type | NumPy Type | Bytes | Range/Precision |
|------|------------|-------|-----------------|
| Int8 | `np.int8` | 1 | -128 to 127 |
| Int16 | `np.int16` | 2 | -32768 to 32767 |
| Int32 | `np.int32` | 4 | ±2.1 billion |
| Int64 | `np.int64` | 8 | ±9.2×10^18 |
| UInt8 | `np.uint8` | 1 | 0 to 255 |
| Float16 | `np.float16` | 2 | ~3 decimal digits |
| Float32 | `np.float32` | 4 | ~7 decimal digits |
| Float64 | `np.float64` | 8 | ~15 decimal digits |
| Complex64 | `np.complex64` | 8 | 2× float32 |
| Complex128 | `np.complex128` | 16 | 2× float64 |
| Bool | `np.bool_` | 1 | True/False |
| String | `np.str_` | varies | Unicode |

### Key Takeaways

1. NumPy arrays are homogeneous — all elements share the same dtype
2. Default integer is `int64`, default float is `float64`
3. Use `astype()` to cast between types (returns a copy)
4. Type promotion: smaller type → larger type in operations
5. Choose appropriate dtypes: `float32` for ML, `float64` for precision
6. Avoid overflow with small integer types
7. Round before casting float to int (truncate vs round)
8. Use `np.isclose()` for float comparison

---

## 🔗 Next Lecture

→ [07-copy-vs-view-lecture.md](./07-copy-vs-view-lecture.md) — Copy vs View
