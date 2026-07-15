# Python Data Types - Lecture Notes

## 1. Topic Overview
This lecture covers Python's built-in data types. Understanding data types is crucial because they determine what operations you can perform on data. Python has several core data types including numbers, strings, booleans, and collections.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Identify and use Python's built-in data types
- Understand type conversion and type checking
- Choose appropriate data types for different scenarios
- Use type hints for better code documentation
- Work with complex data structures

## 3. Key Concepts

### 3.1 Overview of Data Types

Python has these core data types:

**Numeric Types:**
- `int` - Integer numbers (no decimal)
- `float` - Floating-point numbers (decimal)
- `complex` - Complex numbers

**Sequence Types:**
- `str` - Strings (text)
- `list` - Lists (ordered, mutable)
- `tuple` - Tuples (ordered, immutable)
- `range` - Range of numbers

**Mapping Type:**
- `dict` - Dictionaries (key-value pairs)

**Set Types:**
- `set` - Sets (unordered, unique)
- `frozenset` - Immutable sets

**Boolean Type:**
- `bool` - Boolean (True/False)

**Binary Types:**
- `bytes` - Immutable byte sequences
- `bytearray` - Mutable byte sequences
- `memoryview` - Memory view objects

### 3.2 Checking Data Types

**Using type() function:**
```python
x = 10
print(type(x))  # <class 'int'>

y = 3.14
print(type(y))  # <class 'float'>

z = "Hello"
print(type(z))  # <class 'str'>
```

**Using isinstance():**
```python
x = 10
print(isinstance(x, int))  # True
print(isinstance(x, float))  # False
```

### 3.3 Type Conversion (Casting)

**Explicit conversion:**
```python
# String to integer
x = int("10")

# Integer to string
y = str(10)

# Integer to float
z = float(10)

# Float to integer (truncates decimal)
a = int(3.99)  # Result: 3
```

**Automatic conversion:**
```python
# Python automatically converts in expressions
result = 10 + 3.14  # int + float = float (13.14)
print(type(result))  # <class 'float'>
```

### 3.4 Type Hints (Python 3.5+)

**Basic type hints:**
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(x: int, y: int) -> int:
    return x + y
```

**Complex type hints:**
```python
from typing import List, Dict, Optional

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Alice"
    return None
```

## 4. Code Examples

### Example 1: Numeric Types
```python
# Integer
age = 25
large_number = 1_000_000  # Underscores for readability
negative = -42

# Float
pi = 3.14159
scientific = 1.6e-19  # 1.6 × 10^-19
infinity = float('inf')

# Complex
complex_num = 3 + 4j
print(complex_num.real)  # 3.0
print(complex_num.imag)  # 4.0
```

### Example 2: String Type
```python
# String creation
name = "Alice"
greeting = 'Hello, World!'
multi_line = """This is a
multi-line string"""

# String operations
print(len(name))  # 5
print(name.upper())  # ALICE
print(name.lower())  # alice
print(name[0])  # A
```

### Example 3: Boolean Type
```python
# Boolean values
is_active = True
is_admin = False

# Boolean expressions
x = 10
is_positive = x > 0  # True
is_negative = x < 0  # False

# Boolean in conditions
if is_active:
    print("User is active")

# Boolean values are subclasses of int
print(True + True)  # 2
print(True * 10)    # 10
```

### Example 4: Type Conversion
```python
# String to number
num_str = "42"
num_int = int(num_str)
num_float = float(num_str)

print(num_int)    # 42
print(num_float)  # 42.0

# Number to string
age = 25
age_str = str(age)
print("Age: " + age_str)  # Works now

# Float to int (truncates)
pi = 3.14159
print(int(pi))  # 3
```

## 5. Common Mistakes to Avoid

### Mistake 1: Confusing Type Conversion
```python
# Wrong - can't convert non-numeric string
num = int("hello")  # ValueError!

# Right - ensure valid conversion
num = int("42")
```

### Mistake 2: Float Precision Issues
```python
# Wrong - float precision
print(0.1 + 0.2)  # 0.30000000000000004

# Right - use decimal module for precision
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2'))  # 0.3
```

### Mistake 3: Mutable Default Arguments
```python
# Wrong - mutable default
def append_to(item, lst=[]):
    lst.append(item)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] - Bug!

# Right - use None
def append_to(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### Mistake 4: Type Checking with == vs isinstance()
```python
# Wrong - using ==
print(type(x) == int)  # Works but not recommended

# Right - using isinstance()
print(isinstance(x, int))  # Recommended
```

## 6. Best Practices

1. **Choose appropriate types** for your data
2. **Use type hints** for better documentation
3. **Check types** with isinstance() when needed
4. **Be careful** with float precision
5. **Use Decimal** for financial calculations
6. **Document** expected types in functions

## 7. Practice Exercises

### Exercise 1: Type Explorer
Write a program that takes user input and determines its data type.

### Exercise 2: Type Converter
Create a program that converts between different number types and shows the results.

### Exercise 3: Type Checker
Build a function that checks if a value is a specific type and handles conversions.

## 8. Summary

**Key takeaways:**
- Python has several built-in data types
- Use `type()` to check types, `isinstance()` to verify
- Type conversion (casting) converts between types
- Type hints improve code documentation
- Be careful with float precision
- Choose appropriate types for your data

**Next Lecture:** We'll dive deeper into numbers and arithmetic.

---

**Quick Reference:**
- Built-in Types: https://docs.python.org/3/library/stdtypes.html
- Type Hints: https://docs.python.org/3/library/typing.html
- Decimal Module: https://docs.python.org/3/library/decimal.html