# Python Operators - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| Arithmetic Operator | Operator | Mathematical operations (+, -, *, /) |
| Comparison Operator | Operator | Compare values (==, !=, >, <) |
| Logical Operator | Operator | Combine conditions (and, or, not) |
| Assignment Operator | Operator | Assign and modify values (=, +=) |
| Identity Operator | Operator | Compare object identity (is, is not) |
| Membership Operator | Operator | Check sequence membership (in, not in) |
| Operator Precedence | Concept | Order of operations |
| Operand | Concept | Value operated on by operator |
| Expression | Concept | Combination of values and operators |
| Unary Operator | Operator | Operates on one value |

## Detailed Definitions

### A

**Arithmetic Operator**
- **Definition**: Operator that performs mathematical calculations
- **Example**: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- **Related terms**: Addition, Subtraction, Multiplication
```python
# Arithmetic operators
a = 10
b = 3

print(a + b)   # Addition: 13
print(a - b)   # Subtraction: 7
print(a * b)   # Multiplication: 30
print(a / b)   # Division: 3.333...
print(a // b)  # Floor Division: 3
print(a % b)   # Modulus: 1
print(a ** b)  # Exponent: 1000
```

**Assignment Operator**
- **Definition**: Operator that assigns values to variables
- **Example**: `=`, `+=`, `-=`, `*=`, `/=`
- **Related terms**: Variable, Value, Compound Assignment
```python
# Assignment operators
x = 10       # Basic assignment
x += 5       # x = x + 5 (15)
x -= 3       # x = x - 3 (12)
x *= 2       # x = x * 2 (24)
x /= 4       # x = x / 4 (6.0)
x //= 2      # x = x // 2 (3.0)
x %= 2       # x = x % 2 (1.0)
x **= 3      # x = x ** 3 (1.0)
```

### B

**Bitwise Operator**
- **Definition**: Operator that operates on binary representations
- **Example**: `&`, `|`, `^`, `~`, `<<`, `>>`
- **Related terms**: Binary, Bit, Bitwise AND
```python
# Bitwise operators
a = 12  # 1100 in binary
b = 10  # 1010 in binary

print(a & b)   # Bitwise AND: 8 (1000)
print(a | b)   # Bitwise OR: 14 (1110)
print(a ^ b)   # Bitwise XOR: 6 (0110)
print(~a)      # Bitwise NOT: -13
print(a << 2)  # Left shift: 48 (110000)
print(a >> 2)  # Right shift: 3 (11)
```

### C

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

**Compound Assignment**
- **Definition**: Assignment operator that modifies variable in place
- **Example**: `+=`, `-=`, `*=`, `/=`
- **Related terms**: Assignment Operator, Shorthand
```python
# Compound assignment
x = 10
x += 5   # Same as x = x + 5
x -= 3   # Same as x = x - 3
x *= 2   # Same as x = x * 2
x /= 4   # Same as x = x / 4
```

### E

**Expression**
- **Definition**: Combination of values and operators that produces a result
- **Example**: `2 + 3`, `x > 5`, `"hello".upper()`
- **Related terms**: Operator, Value, Statement
```python
# Expressions
2 + 3          # Arithmetic expression
x > 5          # Comparison expression
True and False # Boolean expression
```

### I

**Identity Operator**
- **Definition**: Operator that compares object identity (memory location)
- **Example**: `is`, `is not`
- **Related terms**: Reference, Memory, Object
```python
# Identity operators
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a is b)      # False (different objects)
print(a is c)      # True (same object)
print(a is not b)  # True
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

### M

**Membership Operator**
- **Definition**: Operator that checks if value is in sequence
- **Example**: `in`, `not in`
- **Related terms**: Sequence, Containment, List
```python
# Membership operators
fruits = ["apple", "banana", "cherry"]

print("apple" in fruits)      # True
print("orange" in fruits)     # False
print("orange" not in fruits) # True

# Works with strings
text = "Hello, World!"
print("World" in text)        # True
```

### O

**Operator**
- **Definition**: Symbol that performs operation on values
- **Example**: `+`, `-`, `*`, `/`, `==`, `and`
- **Related terms**: Operand, Expression, Calculation
```python
# Operator examples
result = 10 + 5      # + is operator
is_greater = 10 > 5  # > is operator
x = 10               # = is operator
```

**Operator Precedence**
- **Definition**: Order in which operators are evaluated
- **Example**: `**` before `*` before `+`
- **Related terms**: Order of Operations, PEMDAS, BODMAS
```python
# Operator precedence
result1 = 2 + 3 * 4     # 14 (not 20)
result2 = (2 + 3) * 4   # 20
result3 = 2 ** 3 ** 2   # 512 (right-associative)
```

### P

**Precedence**
- **Definition**: Priority of operators in evaluation
- **Example**: `**` > `*` > `+`
- **Related terms**: Order of Operations, Parentheses
```python
# Precedence rules (highest to lowest):
# 1. Parentheses ()
# 2. Exponentiation **
# 3. Unary +, -, ~
# 4. *, /, //, %
# 5. +, -
# 6. ==, !=, >, <, >=, <=, is, is not, in, not in
# 7. not
# 8. and
# 9. or
```

### U

**Unary Operator**
- **Definition**: Operator that operates on one value
- **Example**: `+`, `-`, `~`, `not`
- **Related terms**: Binary Operator, Operand
```python
# Unary operators
x = 5
print(+x)   # Positive: 5
print(-x)   # Negative: -5
print(not True)  # Logical not: False
```

## Key Concepts Summary

### Operator Categories
| Category | Operators | Example |
|----------|-----------|---------|
| Arithmetic | +, -, *, /, //, %, ** | `10 + 5` |
| Comparison | ==, !=, >, <, >=, <= | `10 > 5` |
| Logical | and, or, not | `True and False` |
| Assignment | =, +=, -=, *=, /= | `x += 5` |
| Identity | is, is not | `a is b` |
| Membership | in, not in | `"a" in "abc"` |
| Bitwise | &, \|, ^, ~, <<, >> | `a & b` |

### Operator Precedence (High to Low)
| Precedence | Operator | Description |
|------------|----------|-------------|
| 1 | `()` | Parentheses |
| 2 | `**` | Exponentiation |
| 3 | `+x`, `-x`, `~x` | Unary operators |
| 4 | `*`, `/`, `//`, `%` | Multiplication, Division |
| 5 | `+`, `-` | Addition, Subtraction |
| 6 | `==`, `!=`, `>`, `<`, `>=`, `<=`, `is`, `is not`, `in`, `not in` | Comparisons |
| 7 | `not` | Logical NOT |
| 8 | `and` | Logical AND |
| 9 | `or` | Logical OR |

### Common Patterns
```python
# Range checking
if 18 <= age <= 65:
    print("Working age")

# Membership testing
if "admin" in user_roles:
    print("Admin access")

# Identity checking
if result is None:
    print("No result")
```

## Practice Terms

Match these terms to their definitions:
1. Arithmetic Operator - ?
2. Comparison Operator - ?
3. Logical Operator - ?
4. Identity Operator - ?
5. Membership Operator - ?

**Answers:**
1. Mathematical operations (+, -, *, /)
2. Compare values (==, !=, >, <)
3. Combine conditions (and, or, not)
4. Compare object identity (is, is not)
5. Check sequence membership (in, not in)