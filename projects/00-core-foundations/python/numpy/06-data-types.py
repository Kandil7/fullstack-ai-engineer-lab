"""
Data Types
W3Schools: https://www.w3schools.com/python/numpy_data_types.asp

NumPy data types, type checking, and conversion.
"""

import numpy as np

# ============================================================
# Example 1: NumPy Data Types
# Common dtypes and how to specify them.
# ============================================================

# Integer types
arr_i8 = np.array([1, 2, 3], dtype=np.int8)
arr_i16 = np.array([1, 2, 3], dtype=np.int16)
arr_i32 = np.array([1, 2, 3], dtype=np.int32)
arr_i64 = np.array([1, 2, 3], dtype=np.int64)

print("int8:", arr_i8.dtype, "- Bytes:", arr_i8.nbytes)   # int8, 3 bytes
print("int16:", arr_i16.dtype, "- Bytes:", arr_i16.nbytes) # int16, 6 bytes
print("int32:", arr_i32.dtype, "- Bytes:", arr_i32.nbytes) # int32, 12 bytes
print("int64:", arr_i64.dtype, "- Bytes:", arr_i64.nbytes) # int64, 24 bytes

# Float types
arr_f16 = np.array([1.5, 2.5], dtype=np.float16)
arr_f32 = np.array([1.5, 2.5], dtype=np.float32)
arr_f64 = np.array([1.5, 2.5], dtype=np.float64)

print("\nfloat16:", arr_f16.dtype, "- Bytes:", arr_f16.nbytes)  # 4
print("float32:", arr_f32.dtype, "- Bytes:", arr_f32.nbytes)  # 8
print("float64:", arr_f64.dtype, "- Bytes:", arr_f64.nbytes)  # 16

# Boolean and string types
arr_bool = np.array([True, False, True])
arr_str = np.array(["hello", "world"])
print("\nbool:", arr_bool.dtype)
print("str:", arr_str.dtype)
# Output:
# int8: int8 - Bytes: 3
# int16: int16 - Bytes: 6
# int32: int32 - Bytes: 12
# int64: int64 - Bytes: 24
#
# float16: float16 - Bytes: 4
# float32: float32 - Bytes: 8
# float64: float64 - Bytes: 16
#
# bool: bool
# str: <U5

# ============================================================
# Example 2: Default Data Types
# NumPy defaults to int64 and float64.
# ============================================================

arr_int = np.array([1, 2, 3])
arr_float = np.array([1.0, 2.0, 3.0])
arr_complex = np.array([1+2j, 3+4j])
arr_bool = np.array([True, False])
arr_str = np.array(["a", "b", "c"])

print("\nDefault int dtype:", arr_int.dtype)      # int64
print("Default float dtype:", arr_float.dtype)    # float64
print("Complex dtype:", arr_complex.dtype)        # complex128
print("Bool dtype:", arr_bool.dtype)              # bool
print("String dtype:", arr_str.dtype)             # <U1
# Output:
# Default int dtype: int64
# Default float dtype: float64
# Complex dtype: complex128
# Bool dtype: bool
# String dtype: <U1

# ============================================================
# Example 3: Type Conversion (astype)
# Convert between data types using astype().
# ============================================================

arr = np.array([1.7, 2.3, 3.9, 4.1])
print("\nOriginal float64:", arr)
print("Dtype:", arr.dtype)  # float64

# Convert to integer (truncates, not rounds)
arr_int = arr.astype(int)
print("\nAs int:", arr_int)
print("Dtype:", arr_int.dtype)  # int64
# Output: As int: [1 2 3 4]

# Convert to float32 for memory savings
arr_f32 = arr.astype(np.float32)
print("\nAs float32:", arr_f32)
print("Dtype:", arr_f32.dtype)
print("Bytes:", arr_f32.nbytes)  # 16 vs 32 for float64
# Output: Bytes: 16

# Convert int to float
arr_int = np.array([1, 2, 3, 4])
arr_float = arr_int.astype(float)
print("\nInt to float:", arr_float)
print("Dtype:", arr_float.dtype)  # float64
# Output: Int to float: [1. 2. 3. 4.]

# Convert to complex
arr_complex = arr_int.astype(complex)
print("As complex:", arr_complex)  # [1.+0.j 2.+0.j 3.+0.j 4.+0.j]

# ============================================================
# Example 4: Overflow and Underflow
# Data type limits affect calculations.
# ============================================================

# int8 range: -128 to 127
arr = np.array([127], dtype=np.int8)
print("\nint8 max:", arr)  # 127
arr += 1
print("int8 max + 1:", arr)  # -128 (overflow!)
# Output:
# int8 max: [127]
# int8 max + 1: [-128]

# Safe conversion with where and clipping
arr = np.array([1.9, 2.3, 3.7, 4.1])

# Using np.round before converting
arr_rounded = np.round(arr).astype(int)
print("\nRounded and converted:", arr_rounded)  # [2 2 4 4]

# Using clip to stay within bounds
arr_clip = np.clip(arr, 0, 3).astype(int)
print("Clipped and converted:", arr_clip)  # [1 2 3 3]

# Float precision
arr32 = np.array([1.123456789012345], dtype=np.float32)
arr64 = np.array([1.123456789012345], dtype=np.float64)
print("\nfloat32 precision:", arr32)  # 1.1234568
print("float64 precision:", arr64)  # 1.123456789012345
# Output:
# float32 precision: [1.1234568]
# float64 precision: [1.123456789012345]

# ============================================================
# Example 5: Type Conversion with astype and Python Types
# ============================================================

arr = np.array([1, 2, 3, 4, 5])

# Convert to Python list
python_list = arr.tolist()
print("\nTo list:", python_list)
print("Type:", type(python_list))  # <class 'list'>

# Convert list back to array
arr2 = np.array(python_list)
print("Back to array:", arr2)

# Convert to specific types
arr_float = arr.astype(np.float32)
arr_str = arr.astype(str)
arr_bytes = arr.astype(bytes)

print("\nAs float32:", arr_float, arr_float.dtype)
print("As string:", arr_str, arr_str.dtype)
print("As bytes:", arr_bytes, arr_bytes.dtype)

# Using Python type objects
arr_from_float = np.array([1.0, 2.0]).astype(int)
arr_from_int = np.array([1, 2]).astype(float)
print("\nFloat to int:", arr_from_float)
print("Int to float:", arr_from_int)
# Output:
# To list: [1, 2, 3, 4, 5]
# Type: <class 'list'>
# Back to array: [1 2 3 4 5]
#
# As float32: [1. 2. 3. 4. 5.] float32
# As string: ['1' '2' '3' '4' '5'] <U21
# As bytes: [b'1' b'2' b'3' b'4' b'5'] |S21
#
# Float to int: [1 2]
# Int to float: [1. 2.]
