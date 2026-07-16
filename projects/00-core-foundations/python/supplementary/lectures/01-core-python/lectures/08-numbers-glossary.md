# Python Numbers - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| int | Type | Integer numbers (whole numbers) |
| float | Type | Floating-point numbers (decimal) |
| complex | Type | Complex numbers (real + imaginary) |
| Arithmetic | Operation | Basic math operations (+, -, *, /) |
| Floor Division | Operation | Division that rounds down (//) |
| Modulus | Operation | Remainder after division (%) |
| Exponent | Operation | Power operation (**) |
| Math Module | Library | Advanced mathematical functions |
| Decimal Module | Library | Precise decimal arithmetic |
| Precision | Concept | Accuracy of decimal representation |

## Detailed Definitions

### A

**Arbitrary Precision**
- **Definition**: Integers can be as large as memory allows
- **Example**: `10 ** 100` (googol) works fine
- **Related terms**: Integer, Overflow, Memory
```python
# No overflow for integers!
huge = 10 ** 1000
print(huge)
# Python handles arbitrarily large integers
```

**Arithmetic Operations**
- **Definition**: Basic mathematical operations
- **Example**: Addition (+), Subtraction (-), Multiplication (*), Division (/)
- **Related terms**: Operator, Operand, Expression
```python
a = 10
b = 3

print(a + b)   # 13 (addition)
print(a - b)   # 7 (subtraction)
print(a * b)   # 30 (multiplication)
print(a / b)   # 3.333... (division)
print(a // b)  # 3 (floor division)
print(a % b)   # 1 (modulus)
print(a ** b)  # 1000 (exponent)
```

### B

**Base Conversion**
- **Definition**: Converting numbers between different bases
- **Example**: Binary (base 2), Octal (base 8), Hexadecimal (base 16)
- **Related terms**: Binary, Octal, Hexadecimal
```python
# Base conversion functions
print(bin(42))   # '0b101010' (binary)
print(oct(42))   # '0o52' (octal)
print(hex(42))   # '0x2a' (hexadecimal)

# Convert from base
print(int('101010', 2))  # 42 (from binary)
print(int('52', 8))      # 42 (from octal)
print(int('2a', 16))     # 42 (from hexadecimal)
```

### C

**Ceiling**
- **Definition**: Smallest integer greater than or equal to number
- **Example**: `math.ceil(3.2)` → 4
- **Related terms**: Floor, Rounding, Math Module
```python
import math

print(math.ceil(3.2))   # 4
print(math.ceil(3.8))   # 4
print(math.ceil(-3.2))  # -3
```

**Complex Number**
- **Definition**: Number with real and imaginary parts
- **Example**: `3 + 4j`, `complex(3, 4)`
- **Related terms**: Real, Imaginary, j notation
```python
# Complex number creation
z = 3 + 4j
z = complex(3, 4)

# Access parts
print(z.real)  # 3.0
print(z.imag)  # 4.0

# Operations
z1 = 1 + 2j
z2 = 3 + 4j
print(z1 + z2)  # (4+6j)
print(z1 * z2)  # (-5+10j)
```

### D

**Decimal Module**
- **Definition**: Module for precise decimal arithmetic
- **Example**: `Decimal('0.1') + Decimal('0.2')`
- **Related terms**: Precision, Float, Financial Calculations
```python
from decimal import Decimal

# Float precision issue
print(0.1 + 0.2)  # 0.30000000000000004

# Decimal solution
print(Decimal('0.1') + Decimal('0.2'))  # 0.3

# Financial calculations
price = Decimal('19.99')
tax = Decimal('0.08')
total = price * (1 + tax)
print(total)  # 21.5892
```

**Division**
- **Definition**: Operation that divides one number by another
- **Example**: `10 / 2` → 5.0
- **Related terms**: Float Division, Floor Division, Quotient
```python
# Regular division (always returns float)
print(10 / 2)   # 5.0
print(10 / 3)   # 3.333...
print(10 / 4)   # 2.5

# Floor division (returns integer)
print(10 // 2)  # 5
print(10 // 3)  # 3
```

### F

**Float**
- **Definition**: Floating-point number (decimal)
- **Example**: `3.14`, `-0.5`, `1.0`
- **Related terms**: Precision, IEEE 754, Scientific Notation
```python
# Float creation
pi = 3.14159
negative = -0.5
scientific = 1.6e-19  # 1.6 × 10^-19

# Float precision
print(0.1 + 0.2)  # 0.30000000000000004
```

**Floor**
- **Definition**: Largest integer less than or equal to number
- **Example**: `math.floor(3.7)` → 3
- **Related terms**: Ceiling, Rounding, Math Module
```python
import math

print(math.floor(3.7))   # 3
print(math.floor(3.2))   # 3
print(math.floor(-3.2))  # -4
```

**Floor Division**
- **Definition**: Division that rounds down to nearest integer
- **Example**: `10 // 3` → 3
- **Related terms**: Modulus, Integer Division, Operator
```python
# Floor division
print(10 // 3)   # 3
print(10 // 2)   # 5
print(-10 // 3)  # -4 (rounds down, not towards zero)

# Floor division with floats
print(10.0 // 3)  # 3.0
```

### H

**Hexadecimal**
- **Definition**: Base-16 number system (0-9, A-F)
- **Example**: `0x2A` (42 in decimal)
- **Related terms**: Binary, Octal, Base Conversion
```python
# Hexadecimal conversion
print(hex(42))   # '0x2a'
print(int('2a', 16))  # 42

# Hex literals
x = 0x2A  # 42 in decimal
print(x)  # 42
```

### I

**IEEE 754**
- **Definition**: Standard for floating-point arithmetic
- **Example**: Python floats follow this standard
- **Related terms**: Float, Precision, Binary Representation
```python
# IEEE 754 double precision
# - 64 bits total
# - 1 sign bit
# - 11 exponent bits
# - 52 mantissa bits
# - ~15-17 decimal digits precision
```

**Integer**
- **Definition**: Whole number (positive, negative, or zero)
- **Example**: `42`, `-10`, `0`
- **Related terms**: Float, Arbitrary Precision, Type
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
print(10 // 3)  # 3 (floor division)
print(10 % 3)   # 1 (modulus)
print(10 ** 2)  # 100 (exponent)
```

### M

**Math Module**
- **Definition**: Module for advanced mathematical functions
- **Example**: `math.sqrt()`, `math.pi`, `math.sin()`
- **Related terms**: Function, Library, Import
```python
import math

print(math.pi)        # 3.141592653589793
print(math.e)         # 2.718281828459045
print(math.sqrt(16))  # 4.0
print(math.pow(2, 3)) # 8.0
print(math.floor(3.7)) # 3
print(math.ceil(3.2))  # 4
print(math.log(100, 10)) # 2.0
```

**Modulus**
- **Definition**: Remainder after division
- **Example**: `10 % 3` → 1
- **Related terms**: Floor Division, Remainder, Operator
```python
# Modulus operation
print(10 % 3)   # 1
print(10 % 2)   # 0 (even)
print(11 % 2)   # 1 (odd)

# Use cases
# Check if even/odd
if num % 2 == 0:
    print("Even")
else:
    print("Odd")
```

### O

**Octal**
- **Definition**: Base-8 number system (0-7)
- **Example**: `0o52` (42 in decimal)
- **Related terms**: Binary, Hexadecimal, Base Conversion
```python
# Octal conversion
print(oct(42))   # '0o52'
print(int('52', 8))  # 42

# Octal literals
x = 0o52  # 42 in decimal
print(x)  # 42
```

**Overflow**
- **Definition**: When number exceeds maximum representable value
- **Example**: Doesn't happen with Python integers!
- **Related terms**: Arbitrary Precision, Float, Integer
```python
# Python integers don't overflow!
huge = 10 ** 1000
print(huge)  # Works fine!

# Floats can overflow
import sys
print(sys.float_info.max)  # 1.7976931348623157e+308
```

### P

**Precision**
- **Definition**: Accuracy of decimal representation
- **Example**: Floats have ~15-17 decimal digits precision
- **Related terms**: Float, Decimal, IEEE 754
```python
# Float precision
print(0.1 + 0.2)  # 0.30000000000000004

# Decimal precision
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2'))  # 0.3
```

### R

**Rounding**
- **Definition**: Adjusting number to specified precision
- **Example**: `round(3.14159, 2)` → 3.14
- **Related terms**: Floor, Ceiling, Precision
```python
# Rounding
pi = 3.141592653589793
print(round(pi, 2))  # 3.14
print(round(pi, 4))  # 3.1416

# Rounding to integer
print(round(3.7))  # 4
print(round(3.2))  # 3
```

### S

**Scientific Notation**
- **Definition**: Number format using exponent (e notation)
- **Example**: `1.6e-19` (1.6 × 10^-19)
- **Related terms**: Float, Exponent, Notation
```python
# Scientific notation
avogadro = 6.022e23
speed_of_light = 3e8
electron_mass = 9.109e-31

# Convert to float
print(float('1.6e-19'))  # 1.6e-19
```

## Key Concepts Summary

### Numeric Types
| Type | Example | Precision | Range |
|------|---------|-----------|-------|
| int | 42 | Unlimited | Unlimited |
| float | 3.14 | ~15-17 digits | ±1.8e308 |
| complex | 3+4j | Same as float | Same as float |

### Arithmetic Operations
| Operation | Symbol | Example | Result |
|-----------|--------|---------|--------|
| Addition | + | `10 + 3` | 13 |
| Subtraction | - | `10 - 3` | 7 |
| Multiplication | * | `10 * 3` | 30 |
| Division | / | `10 / 3` | 3.333... |
| Floor Division | // | `10 // 3` | 3 |
| Modulus | % | `10 % 3` | 1 |
| Exponent | ** | `10 ** 3` | 1000 |

### Math Module Functions
| Function | Description | Example |
|----------|-------------|---------|
| sqrt(x) | Square root | `math.sqrt(16)` → 4.0 |
| pow(x, y) | Power | `math.pow(2, 3)` → 8.0 |
| floor(x) | Round down | `math.floor(3.7)` → 3 |
| ceil(x) | Round up | `math.ceil(3.2)` → 4 |
| log(x, base) | Logarithm | `math.log(100, 10)` → 2.0 |
| sin(x) | Sine | `math.sin(math.pi/2)` → 1.0 |
| cos(x) | Cosine | `math.cos(0)` → 1.0 |

### Float Precision Solutions
| Method | Use Case | Example |
|--------|----------|---------|
| round() | Simple rounding | `round(0.1+0.2, 1)` |
| math.isclose() | Float comparison | `math.isclose(a, b)` |
| Decimal | Financial calculations | `Decimal('0.1') + Decimal('0.2')` |

### Base Conversion
| Function | Base | Example |
|----------|------|---------|
| bin(x) | 2 (binary) | `bin(42)` → `'0b101010'` |
| oct(x) | 8 (octal) | `oct(42)` → `'0o52'` |
| hex(x) | 16 (hex) | `hex(42)` → `'0x2a'` |
| int(s, base) | Any | `int('101010', 2)` → 42 |

## Practice Terms

Match these terms to their definitions:
1. int - ?
2. float - ?
3. floor division - ?
4. modulus - ?
5. math module - ?

**Answers:**
1. Whole numbers (42, -10, 0)
2. Decimal numbers (3.14, -0.5)
3. Division that rounds down (//)
4. Remainder after division (%)
5. Advanced mathematical functions