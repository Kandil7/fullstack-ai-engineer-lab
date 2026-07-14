# Python Type Casting - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| Type Casting | Process | Converting one data type to another |
| Explicit Conversion | Method | Manual type conversion using functions |
| Implicit Conversion | Method | Automatic type conversion by Python |
| Coercion | Process | Automatic type promotion in expressions |
| int() | Function | Convert to integer |
| float() | Function | Convert to floating-point |
| str() | Function | Convert to string |
| bool() | Function | Convert to boolean |
| ValueError | Error | Raised when conversion fails |
| TypeError | Error | Raised for invalid type operation |

## Detailed Definitions

### B

**bool()**
- **Definition**: Convert value to boolean (True/False)
- **Example**: `bool(0)` → False, `bool(1)` → True
- **Related terms**: Boolean, Truthiness, Falsy Values
```python
# bool() conversion
print(bool(0))      # False
print(bool(1))      # True
print(bool(-1))     # True
print(bool(""))     # False
print(bool("hi"))   # True
print(bool([]))     # False
print(bool([1]))    # True
print(bool(None))   # False
```

**Built-in Function**
- **Definition**: Function provided by Python core
- **Example**: `int()`, `float()`, `str()`, `bool()`
- **Related terms**: Constructor, Type Conversion, Python Core
```python
# Built-in type conversion functions
x = int("10")      # String to int
y = float("3.14")  # String to float
z = str(10)        # Int to string
w = bool(0)        # Int to bool
```

### C

**Casting**
- **Definition**: Converting value from one type to another
- **Example**: `int("10")`, `str(10)`, `float(10)`
- **Related terms**: Type Conversion, Explicit Conversion, Implicit Conversion
```python
# Type casting examples
num_str = "42"
num_int = int(num_str)  # Cast string to int
num_float = float(num_str)  # Cast string to float
num_str2 = str(num_int)  # Cast int to string
```

**Coercion**
- **Definition**: Automatic type conversion in expressions
- **Example**: `10 + 3.14` → 13.14 (int coerced to float)
- **Related terms**: Implicit Conversion, Type Promotion, Operator
```python
# Coercion in expressions
result = 10 + 3.14  # int + float = float
print(type(result))  # <class 'float'>

# Boolean coercion
print(True + 1)  # 2 (True coerced to 1)
print(False * 10)  # 0 (False coerced to 0)
```

### E

**Explicit Conversion**
- **Definition**: Manual type conversion using constructor functions
- **Example**: `int("10")`, `float(10)`, `str(10)`
- **Related terms**: Type Casting, Constructor, Manual
```python
# Explicit conversion
x = int("42")      # Explicit: string to int
y = float(42)      # Explicit: int to float
z = str(42)        # Explicit: int to string
w = bool(42)       # Explicit: int to bool
```

### F

**float()**
- **Definition**: Convert value to floating-point number
- **Example**: `float(10)` → 10.0, `float("3.14")` → 3.14
- **Related terms**: Float, Decimal, Number
```python
# float() conversion
print(float(10))      # 10.0
print(float("3.14"))  # 3.14
print(float(True))    # 1.0
print(float(False))   # 0.0

# Invalid conversion
# float("hello")  # ValueError!
```

### I

**Implicit Conversion**
- **Definition**: Automatic type conversion by Python interpreter
- **Example**: `10 + 3.14` automatically converts int to float
- **Related terms**: Coercion, Type Promotion, Automatic
```python
# Implicit conversion
result = 10 + 3.14  # Python converts int to float
print(type(result))  # <class 'float'>

# In function arguments
def greet(name: str, age: int):
    print(f"Hello {name}, age {age}")

# Python handles type conversion automatically
greet("Alice", 25.0)  # float converted to int? No!
# Actually this would raise TypeError if type hints enforced
```

**int()**
- **Definition**: Convert value to integer
- **Example**: `int("10")` → 10, `int(3.99)` → 3
- **Related terms**: Integer, Truncation, Conversion
```python
# int() conversion
print(int("42"))      # 42
print(int(3.99))      # 3 (truncates, doesn't round)
print(int(True))      # 1
print(int(False))     # 0
print(int("3.14"))    # ValueError!

# With base parameter
print(int("1010", 2))  # 10 (binary to decimal)
print(int("ff", 16))   # 255 (hex to decimal)
```

### T

**Type Casting**
- **Definition**: Process of converting one data type to another
- **Example**: `int("10")`, `str(10)`, `float("3.14")`
- **Related terms**: Conversion, Explicit, Implicit
```python
# Type casting in action
user_input = "42"  # String from input()

# Cast to number for calculations
age = int(user_input)
next_year_age = age + 1

# Cast back to string for display
print("Next year you'll be " + str(next_year_age))
```

**TypeError**
- **Definition**: Error raised for invalid type operation
- **Example**: `int("hello")` raises ValueError, `int(None)` raises TypeError
- **Related terms**: ValueError, Exception, Error Handling
```python
# TypeError examples
# int(None)  # TypeError: int() argument must be a string...
# "hello" + 1  # TypeError: can only concatenate str to str

# ValueError examples
# int("hello")  # ValueError: invalid literal for int()
```

**Type Conversion**
- **Definition**: Changing data type of a value
- **Example**: Converting string "42" to integer 42
- **Related terms**: Type Casting, Conversion, Explicit, Implicit
```python
# Type conversion functions
x = int("42")      # String to int
y = float(42)      # Int to float
z = str(42)        # Int to string
w = bool(0)        # Int to bool
```

### V

**ValueError**
- **Definition**: Error raised when function receives correct type but wrong value
- **Example**: `int("hello")` raises ValueError
- **Related terms**: TypeError, Exception, Error Handling
```python
# ValueError examples
try:
    num = int("hello")  # ValueError: invalid literal
except ValueError as e:
    print(f"Conversion error: {e}")

# TypeError examples
try:
    num = int(None)  # TypeError: int() argument must be a string
except TypeError as e:
    print(f"Type error: {e}")
```

## Key Concepts Summary

### Type Conversion Functions
| Function | Input → Output | Example |
|----------|----------------|---------|
| int(x) | string/float → int | `int("42")` → 42 |
| float(x) | string/int → float | `float("3.14")` → 3.14 |
| str(x) | any → string | `str(42)` → "42" |
| bool(x) | any → bool | `bool(0)` → False |

### Conversion Rules
| From → To | Works? | Notes |
|-----------|--------|-------|
| string → int | ✓ | Must be valid integer string |
| string → float | ✓ | Must be valid float string |
| int → string | ✓ | Always works |
| float → int | ✓ | Truncates decimal |
| int → float | ✓ | Always works |
| bool → int | ✓ | True=1, False=0 |
| int → bool | ✓ | 0=False, others=True |
| complex → int | ✗ | Raises TypeError |

### Error Handling
```python
# Safe conversion with try/except
def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

result = safe_int("hello")  # Returns None
result = safe_int("42")     # Returns 42
```

### Common Patterns
```python
# User input conversion
age = int(input("Enter age: "))

# String building
print("Age: " + str(age))
print(f"Age: {age}")  # Better with f-strings

# Boolean checks
if bool(user_input):
    process(user_input)

# Safe conversion
def convert_to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0
```

## Practice Terms

Match these terms to their definitions:
1. Type Casting - ?
2. Explicit Conversion - ?
3. Implicit Conversion - ?
4. ValueError - ?
5. int() - ?

**Answers:**
1. Process of converting one data type to another
2. Manual type conversion using functions
3. Automatic type conversion by Python
4. Error raised when conversion fails
5. Convert value to integer