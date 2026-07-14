# Python Booleans - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| bool | Type | Boolean data type (True/False) |
| True | Value | Boolean true value |
| False | Value | Boolean false value |
| Comparison Operator | Operator | Compares values, returns boolean |
| Logical Operator | Operator | Combines boolean expressions |
| Truthiness | Concept | Values evaluated as True |
| Falsiness | Concept | Values evaluated as False |
| Short-circuit | Behavior | Logical operators stop early |
| Chained Comparison | Syntax | Multiple comparisons in one expression |
| Boolean Context | Context | Where booleans are expected |

## Detailed Definitions

### B

**Boolean**
- **Definition**: Data type with two values: True and False
- **Example**: `is_active = True`, `is_admin = False`
- **Related terms**: bool, True, False, Logical Operations
```python
# Boolean values
is_active = True
is_admin = False

# Boolean expressions
x = 10
is_positive = x > 0  # True
is_negative = x < 0  # False
```

**bool()**
- **Definition**: Function to convert value to boolean
- **Example**: `bool(0)` → False, `bool(1)` → True
- **Related terms**: Truthiness, Falsiness, Type Conversion
```python
# bool() conversion
print(bool(0))      # False
print(bool(1))      # True
print(bool(-1))     # True
print(bool(""))     # False
print(bool("hi"))   # True
print(bool([]))     # False
print(bool([1, 2])) # True
```

### C

**Chained Comparison**
- **Definition**: Multiple comparisons in one expression
- **Example**: `1 < x < 10`, `a == b == c`
- **Related terms**: Comparison Operator, Syntax, Pythonic
```python
# Chained comparisons
x = 15
if 10 < x < 20:
    print("x is between 10 and 20")

# Equivalent to
if x > 10 and x < 20:
    print("x is between 10 and 20")
```

**Comparison Operator**
- **Definition**: Operator that compares values, returns boolean
- **Example**: `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Related terms**: Equality, Relational, Boolean
```python
# Comparison operators
x = 10
y = 20

print(x == y)   # Equal: False
print(x != y)   # Not equal: True
print(x > y)    # Greater than: False
print(x < y)    # Less than: True
print(x >= 10)  # Greater or equal: True
print(x <= 5)   # Less or equal: False
```

### F

**False**
- **Definition**: Boolean false value
- **Example**: `is_admin = False`
- **Related terms**: True, bool, Boolean
```python
# False value
is_admin = False
print(is_admin)  # False
print(type(is_admin))  # <class 'bool'>
```

**Falsiness**
- **Definition**: Values that evaluate to False in boolean context
- **Example**: `0`, `0.0`, `""`, `[]`, `{}`, `None`
- **Related terms**: Truthiness, bool(), Boolean Context
```python
# Falsy values
print(bool(0))      # False
print(bool(0.0))    # False
print(bool(""))     # False
print(bool([]))     # False
print(bool({}))     # False
print(bool(None))   # False
```

### L

**Logical Operator**
- **Definition**: Operator that combines boolean expressions
- **Example**: `and`, `or`, `not`
- **Related terms**: Boolean, Short-circuit, Truth Table
```python
# Logical operators
x = 15

# and - both must be True
print(x > 10 and x < 20)  # True
print(x > 10 and x > 20)  # False

# or - at least one must be True
print(x > 10 or x > 20)   # True
print(x > 20 or x > 30)   # False

# not - reverses boolean
print(not (x > 5))   # False
print(not (x > 15))  # True
```

### S

**Short-circuit Evaluation**
- **Definition**: Logical operators stop when result is determined
- **Example**: `False and ...` returns False without evaluating right side
- **Related terms**: Logical Operator, Performance, Lazy Evaluation
```python
# Short-circuit with and
def check():
    print("Checking...")
    return True

# This won't print "Checking..." if x is False
x = False
if x and check():
    print("Passed")

# Short-circuit with or
y = True
if y or check():  # check() not called
    print("Passed")
```

**Truthiness**
- **Definition**: Values that evaluate to True in boolean context
- **Example**: Non-zero numbers, non-empty strings, non-empty collections
- **Related terms**: Falsiness, bool(), Boolean Context
```python
# Truthy values
print(bool(1))      # True
print(bool(-1))     # True
print(bool("hi"))   # True
print(bool([1, 2])) # True
print(bool({"a": 1}))  # True
```

### T

**Truth Table**
- **Definition**: Table showing all possible outputs of logical operators
- **Example**: Truth table for and, or, not
```python
# Truth table for and
# True and True = True
# True and False = False
# False and True = False
# False and False = False

# Truth table for or
# True or True = True
# True or False = True
# False or True = True
# False or False = False

# Truth table for not
# not True = False
# not False = True
```

**True**
- **Definition**: Boolean true value
- **Example**: `is_active = True`
- **Related terms**: False, bool, Boolean
```python
# True value
is_active = True
print(is_active)  # True
print(type(is_active))  # <class 'bool'>
```

### V

**Value Comparison**
- **Definition**: Comparing values for equality or inequality
- **Example**: `x == y`, `x != y`
- **Related terms**: Equality, Identity, Comparison Operator
```python
# Value comparison
x = 10
y = 10
print(x == y)  # True (values equal)

# Identity comparison
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)   # True (values equal)
print(a is b)   # False (different objects)
```

## Key Concepts Summary

### Boolean Values
| Value | Meaning | Example |
|-------|---------|---------|
| True | Logical true | `is_active = True` |
| False | Logical false | `is_admin = False` |

### Comparison Operators
| Operator | Description | Example |
|----------|-------------|---------|
| == | Equal | `10 == 10` → True |
| != | Not equal | `10 != 5` → True |
| > | Greater than | `10 > 5` → True |
| < | Less than | `5 < 10` → True |
| >= | Greater or equal | `10 >= 10` → True |
| <= | Less or equal | `5 <= 10` → True |

### Logical Operators
| Operator | Description | Example |
|----------|-------------|---------|
| and | Both True | `True and False` → False |
| or | At least one True | `True or False` → True |
| not | Reverses | `not True` → False |

### Truthiness Rules
| Falsy Values | Truthy Values |
|--------------|---------------|
| `0` | Non-zero numbers |
| `0.0` | Non-empty strings |
| `""` | Non-empty collections |
| `[]` | Objects with `__bool__` returning True |
| `{}` | |
| `None` | |

### Short-circuit Behavior
| Expression | Result | Notes |
|------------|--------|-------|
| `True and X` | X | Evaluates X |
| `False and X` | False | Stops, doesn't evaluate X |
| `False or X` | X | Evaluates X |
| `True or X` | True | Stops, doesn't evaluate X |

## Practice Terms

Match these terms to their definitions:
1. True - ?
2. False - ?
3. and - ?
4. or - ?
5. not - ?

**Answers:**
1. Boolean true value
2. Boolean false value
3. Logical operator requiring both conditions True
4. Logical operator requiring at least one condition True
5. Logical operator reversing boolean value