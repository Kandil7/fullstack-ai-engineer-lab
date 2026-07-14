"""
W3Schools Python Tutorial - 07: Python Data Types
==================================================
Topics: Built-in data types, type() function

Run: python 07-data-types.py
Reference: https://www.w3schools.com/python/python_datatypes.asp
"""

# ============================================================
# Python Built-in Data Types
# ============================================================
# Text Type:      str
# Numeric Types:  int, float, complex
# Sequence Types: list, tuple, range
# Mapping Type:   dict
# Set Types:      set, frozenset
# Boolean Type:   bool
# Binary Types:   bytes, bytearray, memoryview

# ============================================================
# Example 1: Text Type - str
# ============================================================
name = "Alice"
greeting = 'Hello, World!'
multi_line = """This is a
multi-line string"""

print(f"String: {name}")
print(f"Type: {type(name)}")
# Output:
# String: Alice
# Type: <class 'str'>

# ============================================================
# Example 2: Numeric Types
# ============================================================
# Integer - whole numbers (no decimal point)
age = 25
negative = -10
big_number = 1_000_000  # Underscores for readability

print(f"\nInteger: {age}")
print(f"Type: {type(age)}")

# Float - decimal numbers
pi = 3.14159
temperature = -40.0
scientific = 1.5e10  # Scientific notation: 1.5 × 10^10

print(f"Float: {pi}")
print(f"Type: {type(pi)}")

# Complex numbers
complex_num = 3 + 4j
print(f"Complex: {complex_num}")
print(f"Type: {type(complex_num)}")
print(f"Real part: {complex_num.real}")
print(f"Imaginary part: {complex_num.imag}")

# Output:
# Integer: 25
# Type: <class 'int'>
# Float: 3.14159
# Type: <class 'float'>
# Complex: (3+4j)
# Type: <class 'complex'>
# Real part: 3.0
# Imaginary part: 4.0

# ============================================================
# Example 3: Sequence Types
# ============================================================
# List - ordered, mutable, allows duplicates
fruits = ["apple", "banana", "cherry"]
print(f"\nList: {fruits}")
print(f"Type: {type(fruits)}")

# Tuple - ordered, immutable, allows duplicates
colors = ("red", "green", "blue")
print(f"Tuple: {colors}")
print(f"Type: {type(colors)}")

# Range - sequence of numbers
numbers = range(5)
print(f"Range: {numbers}")
print(f"Type: {type(numbers)}")
print(f"List from range: {list(numbers)}")

# Output:
# List: ['apple', 'banana', 'cherry']
# Type: <class 'list'>
# Tuple: ('red', 'green', 'blue')
# Type: <class 'tuple'>
# Range: range(0, 5)
# Type: <class 'range'>
# List from range: [0, 1, 2, 3, 4]

# ============================================================
# Example 4: Mapping Type - dict
# ============================================================
# Dictionary - key-value pairs, ordered (Python 3.7+), mutable
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

print(f"\nDict: {person}")
print(f"Type: {type(person)}")
# Output:
# Dict: {'name': 'Alice', 'age': 30, 'city': 'New York'}
# Type: <class 'dict'>

# ============================================================
# Example 5: Set Types
# ============================================================
# Set - unordered, no duplicates, mutable
unique_numbers = {1, 2, 3, 4, 5}
print(f"\nSet: {unique_numbers}")
print(f"Type: {type(unique_numbers)}")

# Frozenset - immutable set
frozen = frozenset([1, 2, 3])
print(f"Frozenset: {frozen}")
print(f"Type: {type(frozen)}")

# Output:
# Set: {1, 2, 3, 4, 5}
# Type: <class 'set'>
# Frozenset: frozenset({1, 2, 3})
# Type: <class 'frozenset'>

# ============================================================
# Example 6: Boolean Type
# ============================================================
is_active = True
is_empty = False

print(f"\nBool: {is_active}")
print(f"Type: {type(is_active)}")
# Output:
# Bool: True
# Type: <class 'bool'>

# Note: bool is a subclass of int!
print(f"True + 1 = {True + 1}")   # Output: True + 1 = 2
print(f"False * 5 = {False * 5}") # Output: False * 5 = 0

# ============================================================
# Example 7: Binary Types
# ============================================================
# Bytes - immutable byte sequence
byte_data = b"Hello"
print(f"\nBytes: {byte_data}")
print(f"Type: {type(byte_data)}")

# ByteArray - mutable byte sequence
byte_array = bytearray([65, 66, 67])
print(f"ByteArray: {byte_array}")
print(f"Type: {type(byte_array)}")

# MemoryView - view of binary data
mv = memoryview(bytes(b"Hello"))
print(f"MemoryView: {mv}")
print(f"Type: {type(mv)}")

# Output:
# Bytes: b'Hello'
# Type: <class 'bytes'>
# ByteArray: bytearray(b'ABC')
# Type: <class 'bytearray'>
# MemoryView: <memory at 0x...>
# Type: <class 'memoryview'>

# ============================================================
# Example 8: Getting the type with type()
# ============================================================
print("\n--- Type Checking ---")
test_values = [
    42, 3.14, "hello", True, None,
    [1, 2], (1, 2), {1, 2}, {"a": 1}
]

for val in test_values:
    print(f"{str(val):20s} -> {type(val).__name__}")
# Output:
# 42                   -> int
# 3.14                 -> float
# hello                -> str
# True                 -> bool
# None                 -> NoneType
# [1, 2]               -> list
# (1, 2)               -> tuple
# {1, 2}               -> set
# {'a': 1}             -> dict

# ============================================================
# Example 9: isinstance() for type checking
# ============================================================
print("\n--- isinstance() ---")
x = 42
print(f"Is {x} an int? {isinstance(x, int)}")          # True
print(f"Is {x} a float? {isinstance(x, float)}")        # False
print(f"Is {x} a number? {isinstance(x, (int, float))}") # True

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. str - text data (strings)")
print("2. int, float, complex - numeric types")
print("3. list - ordered, mutable sequence")
print("4. tuple - ordered, immutable sequence")
print("5. dict - key-value mapping")
print("6. set - unordered collection of unique items")
print("7. bool - True or False")
print("8. Use type() to check, isinstance() to test")
