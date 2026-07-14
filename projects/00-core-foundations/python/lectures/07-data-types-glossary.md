# Python Data Types - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| int | Type | Integer numbers (whole numbers) |
| float | Type | Floating-point numbers (decimal) |
| str | Type | Strings (text data) |
| bool | Type | Boolean values (True/False) |
| list | Type | Ordered, mutable collection |
| tuple | Type | Ordered, immutable collection |
| dict | Type | Key-value pair mapping |
| set | Type | Unordered, unique collection |
| type() | Function | Returns the type of an object |
| isinstance() | Function | Checks if object is instance of type |

## Detailed Definitions

### B

**bool (Boolean)**
- **Definition**: Data type with two values: True and False
- **Example**: `is_active = True`, `is_admin = False`
- **Related terms**: True, False, Logical Operators
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
```

**bytes**
- **Definition**: Immutable sequence of bytes
- **Example**: `b"hello"`, `bytes([65, 66, 67])`
- **Related terms**: bytearray, memoryview, Binary Data
```python
# bytes creation
data = b"hello"
data = bytes([65, 66, 67])  # ASCII for ABC

# bytes operations
print(data[0])  # 65 (A)
print(len(data))  # 3
```

**bytearray**
- **Definition**: Mutable sequence of bytes
- **Example**: `bytearray(b"hello")`
- **Related terms**: bytes, memoryview, Binary Data
```python
# bytearray creation
data = bytearray(b"hello")

# bytearray operations
data[0] = 72  # Change first byte
print(data)  # bytearray(b'Hello')
```

### C

**Casting**
- **Definition**: Explicit conversion between data types
- **Example**: `int("10")`, `str(10)`, `float(10)`
- **Related terms**: Type Conversion, Type Coercion
```python
# String to integer
x = int("10")

# Integer to string
y = str(10)

# Integer to float
z = float(10)

# Float to integer (truncates)
a = int(3.99)  # Result: 3
```

**Complex**
- **Definition**: Data type for complex numbers
- **Example**: `3 + 4j`, `complex(3, 4)`
- **Related terms**: Real, Imaginary, j notation
```python
# Complex number creation
z = 3 + 4j
z = complex(3, 4)

# Access parts
print(z.real)  # 3.0
print(z.imag)  # 4.0
```

### D

**dict (Dictionary)**
- **Definition**: Unordered collection of key-value pairs
- **Example**: `{"name": "Alice", "age": 25}`
- **Related terms**: Key, Value, Mapping
```python
# Dictionary creation
person = {"name": "Alice", "age": 25}

# Access values
print(person["name"])  # Alice

# Add/update
person["email"] = "alice@example.com"

# Dictionary methods
print(person.keys())   # dict_keys(['name', 'age', 'email'])
print(person.values()) # dict_values(['Alice', 25, 'alice@example.com'])
```

### F

**float**
- **Definition**: Floating-point numbers (decimal numbers)
- **Example**: `3.14`, `-0.5`, `1.0`
- **Related terms**: int, Precision, Scientific Notation
```python
# Float creation
pi = 3.14159
negative = -0.5
scientific = 1.6e-19  # 1.6 × 10^-19

# Float operations
print(pi + 1)  # 4.14159
print(pi * 2)  # 6.28318
```

**frozenset**
- **Definition**: Immutable version of set
- **Example**: `frozenset([1, 2, 3])`
- **Related terms**: set, Immutable, Hashable
```python
# frozenset creation
fs = frozenset([1, 2, 3])

# Cannot modify
# fs.add(4)  # AttributeError!

# Can use in sets or as dict keys
my_set = {fs, frozenset([4, 5])}
```

### I

**int (Integer)**
- **Definition**: Whole numbers (positive, negative, or zero)
- **Example**: `42`, `-10`, `0`
- **Related terms**: float, Arithmetic, Type Conversion
```python
# Integer creation
age = 25
negative = -42
zero = 0
large = 1_000_000  # Underscores for readability

# Integer operations
print(10 + 5)   # 15
print(10 - 5)   # 5
print(10 * 5)   # 50
print(10 / 5)   # 2.0 (float division)
print(10 // 3)  # 3 (integer division)
print(10 % 3)   # 1 (modulus)
print(10 ** 2)  # 100 (exponent)
```

**isinstance()**
- **Definition**: Function to check if object is instance of type
- **Example**: `isinstance(10, int)` → True
- **Related terms**: type(), Type Checking, Inheritance
```python
x = 10
print(isinstance(x, int))    # True
print(isinstance(x, float))  # False

# Can check multiple types
print(isinstance(x, (int, float)))  # True
```

### L

**list**
- **Definition**: Ordered, mutable collection
- **Example**: `[1, 2, 3]`, `["a", "b", "c"]`
- **Related terms**: tuple, Mutable, Index
```python
# List creation
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# List operations
numbers.append(6)  # Add to end
numbers.insert(0, 0)  # Insert at index 0
numbers.remove(3)  # Remove first occurrence of 3
numbers.pop()  # Remove and return last element

# List indexing
print(numbers[0])   # First element
print(numbers[-1])  # Last element
print(numbers[1:3])  # Slice
```

### M

**memoryview**
- **Definition**: Object that provides access to binary data buffer
- **Example**: `memoryview(bytes_data)`
- **Related terms**: bytes, bytearray, Buffer Protocol
```python
# memoryview creation
data = b"hello"
mv = memoryview(data)

# Access bytes without copying
print(mv[0])  # 104 (h)
print(mv[1:3])  # memoryview at b"el"
```

### N

**NoneType**
- **Definition**: Data type for None (absence of value)
- **Example**: `x = None`
- **Related terms**: None, Null, Void
```python
# None creation
x = None

# Check for None
if x is None:
    print("x is None")

# Function returning None
def greet():
    print("Hello")
    # Implicitly returns None
```

### R

**range**
- **Definition**: Immutable sequence of numbers
- **Example**: `range(5)`, `range(1, 10, 2)`
- **Related terms**: Sequence, Iterator, Loop
```python
# range creation
r1 = range(5)      # 0, 1, 2, 3, 4
r2 = range(1, 10)  # 1, 2, 3, 4, 5, 6, 7, 8, 9
r3 = range(0, 10, 2)  # 0, 2, 4, 6, 8

# Using range in loops
for i in range(5):
    print(i)

# Converting to list
print(list(range(5)))  # [0, 1, 2, 3, 4]
```

### S

**set**
- **Definition**: Unordered collection of unique elements
- **Example**: `{1, 2, 3}`, `set([1, 2, 2, 3])`
- **Related terms**: frozenset, Unique, Unordered
```python
# Set creation
numbers = {1, 2, 3, 4, 5}
from_list = set([1, 2, 2, 3, 3])  # Removes duplicates

# Set operations
numbers.add(6)        # Add element
numbers.remove(3)     # Remove element
numbers.discard(10)   # Remove if exists (no error)

# Set math
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)  # Union: {1, 2, 3, 4, 5}
print(a & b)  # Intersection: {3}
print(a - b)  # Difference: {1, 2}
```

**str (String)**
- **Definition**: Immutable sequence of characters
- **Example**: `"hello"`, `'world'`, `"""multi-line"""`
- **Related terms**: Text, Immutable, Unicode
```python
# String creation
name = "Alice"
greeting = 'Hello, World!'
multi = """This is
a multi-line string"""

# String operations
print(len(name))      # 5
print(name.upper())   # ALICE
print(name.lower())   # alice
print(name[0])        # A
print(name[1:3])      # li

# String methods
print(name.replace("A", "B"))  # Blice
print(name.startswith("A"))    # True
print(name.endswith("e"))      # True
```

### T

**tuple**
- **Definition**: Ordered, immutable collection
- **Example**: `(1, 2, 3)`, `("a", "b")`
- **Related terms**: list, Immutable, Unpacking
```python
# Tuple creation
coordinates = (10, 20)
single = (5,)  # Single element tuple (note comma)
empty = ()

# Tuple operations
print(coordinates[0])  # 10
print(coordinates[1])  # 20

# Tuple unpacking
x, y = coordinates
print(x, y)  # 10 20

# Cannot modify
# coordinates[0] = 5  # TypeError!
```

**type()**
- **Definition**: Function that returns the type of an object
- **Example**: `type(10)` → `<class 'int'>`
- **Related terms**: isinstance(), Type Checking, Data Type
```python
x = 10
print(type(x))  # <class 'int'>

y = "hello"
print(type(y))  # <class 'str'>

z = [1, 2, 3]
print(type(z))  # <class 'list'>
```

### U

**Union Type**
- **Definition**: Type hint indicating multiple possible types
- **Example**: `Union[int, str]` or `int | str` (Python 3.10+)
- **Related terms**: Type Hints, Optional, Any
```python
from typing import Union

def process(value: Union[int, str]) -> str:
    return str(value)

# Python 3.10+ syntax
def process(value: int | str) -> str:
    return str(value)
```

## Key Concepts Summary

### Data Type Categories
| Category | Types | Mutability |
|----------|-------|------------|
| Numeric | int, float, complex | Immutable |
| Text | str | Immutable |
| Sequence | list, tuple, range | list: Mutable, tuple/range: Immutable |
| Mapping | dict | Mutable |
| Set | set, frozenset | set: Mutable, frozenset: Immutable |
| Boolean | bool | Immutable |
| Binary | bytes, bytearray | bytes: Immutable, bytearray: Mutable |

### Type Conversion Table
| From → To | int | float | str | bool |
|-----------|-----|-------|-----|------|
| int | - | `float(x)` | `str(x)` | `bool(x)` |
| float | `int(x)` | - | `str(x)` | `bool(x)` |
| str | `int(s)` | `float(s)` | - | `bool(s)` |
| bool | `int(b)` | `float(b)` | `str(b)` | - |

### Type Checking Methods
| Method | Example | Returns |
|--------|---------|---------|
| type() | `type(10)` | `<class 'int'>` |
| isinstance() | `isinstance(10, int)` | `True` |
| type() == | `type(10) == int` | `True` |

### When to Use Each Type
| Use Case | Recommended Type |
|----------|------------------|
| Whole numbers | int |
| Decimal numbers | float |
| Text | str |
| True/False | bool |
| Ordered collection | list |
| Immutable sequence | tuple |
| Key-value pairs | dict |
| Unique elements | set |
| Binary data | bytes |

## Practice Terms

Match these terms to their definitions:
1. int - ?
2. float - ?
3. str - ?
4. list - ?
5. dict - ?

**Answers:**
1. Whole numbers (42, -10, 0)
2. Decimal numbers (3.14, -0.5)
3. Text data ("hello", 'world')
4. Ordered, mutable collection ([1, 2, 3])
5. Key-value pairs ({"name": "Alice"})