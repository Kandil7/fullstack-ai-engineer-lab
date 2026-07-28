# Python Numbers - Lecture Notes

## 1. Topic Overview
This lecture covers Python's numeric types in detail: integers, floating-point numbers, and complex numbers. We'll explore arithmetic operations, mathematical functions, and how to work with numbers effectively in Python.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Work with different numeric types (int, float, complex)
- Perform arithmetic operations
- Use mathematical functions from the math module
- Handle precision issues with floats
- Convert between numeric types
- Understand Python's arbitrary-precision integers

## 3. Key Concepts

### 3.1 Integer Numbers (int)
Integers are whole numbers without decimal points.

**Key features:**
- No size limit (arbitrary precision)
- Can use underscores for readability: `1_000_000`
- Support all standard arithmetic operations

```python
# Integer examples
age = 25
negative = -42
zero = 0
large = 999_999_999_999_999_999  # Underscores for readability

# Very large integers (no overflow!)
huge = 10 ** 100  # Googol
print(huge)
```

### 3.2 Floating-Point Numbers (float)
Floats are numbers with decimal points.

**Key features:**
- Based on IEEE 754 double precision
- Limited precision (~15-17 digits)
- Can use scientific notation: `1.6e-19`

```python
# Float examples
pi = 3.14159
temperature = -10.5
speed_of_light = 3e8  # 3 × 10^8

# Scientific notation
avogadro = 6.022e23
```

### 3.3 Complex Numbers
Complex numbers have real and imaginary parts.

```python
# Complex number examples
z = 3 + 4j
z = complex(3, 4)

# Access parts
print(z.real)  # 3.0
print(z.imag)  # 4.0

# Operations
z1 = 1 + 2j
z2 = 3 + 4j
print(z1 + z2)  # (4+6j)
```

### 3.4 Arithmetic Operations

**Basic operations:**
```python
a = 10
b = 3

print(a + b)   # Addition: 13
print(a - b)   # Subtraction: 7
print(a * b)   # Multiplication: 30
print(a / b)   # Division: 3.3333...
print(a // b)  # Floor Division: 3
print(a % b)   # Modulus: 1
print(a ** b)  # Exponent: 1000
```

### 3.5 Mathematical Functions

**Built-in functions:**
```python
x = -5
print(abs(x))     # Absolute value: 5
print(round(3.14159, 2))  # Round to 2 decimals: 3.14
print(min(1, 2, 3))  # Minimum: 1
print(max(1, 2, 3))  # Maximum: 3
```

**Math module functions:**
```python
import math

print(math.pi)        # 3.141592653589793
print(math.e)         # 2.718281828459045
print(math.sqrt(16))  # Square root: 4.0
print(math.pow(2, 3)) # Power: 8.0
print(math.floor(3.7)) # Floor: 3
print(math.ceil(3.2))  # Ceiling: 4
print(math.log(100, 10)) # Log base 10: 2.0
```

## 4. Code Examples

### Example 1: Basic Arithmetic
```python
# Calculator program
def calculator():
    """Simple calculator"""
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    
    print(f"Addition: {num1} + {num2} = {num1 + num2}")
    print(f"Subtraction: {num1} - {num2} = {num1 - num2}")
    print(f"Multiplication: {num1} * {num2} = {num1 * num2}")
    print(f"Division: {num1} / {num2} = {num1 / num2}")
    print(f"Floor Division: {num1} // {num2} = {num1 // num2}")
    print(f"Modulus: {num1} % {num2} = {num1 % num2}")
    print(f"Exponent: {num1} ** {num2} = {num1 ** num2}")

calculator()
```

### Example 2: Math Module Functions
```python
import math

# Circle calculations
radius = 5
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius

print(f"Radius: {radius}")
print(f"Area: {area:.2f}")
print(f"Circumference: {circumference:.2f}")

# Trigonometry
angle_degrees = 45
angle_radians = math.radians(angle_degrees)
print(f"Sine of {angle_degrees}°: {math.sin(angle_radians):.4f}")
print(f"Cosine of {angle_degrees}°: {math.cos(angle_radians):.4f}")
```

### Example 3: Float Precision
```python
# Float precision issues
print(0.1 + 0.2)  # 0.30000000000000004
print(0.1 + 0.2 == 0.3)  # False!

# Solution 1: Use round()
print(round(0.1 + 0.2, 1) == 0.3)  # True

# Solution 2: Use decimal module
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2') == Decimal('0.3'))  # True
```

### Example 4: Number Formatting
```python
# Number formatting
pi = 3.141592653589793

# Decimal places
print(f"Pi: {pi:.2f}")  # 3.14
print(f"Pi: {pi:.4f}")  # 3.1416

# Commas for thousands
population = 789456123
print(f"Population: {population:,}")  # 789,456,123

# Percentage
tax_rate = 0.0825
print(f"Tax rate: {tax_rate:.1%}")  # 8.2%

# Scientific notation
avogadro = 6.022e23
print(f"Avogadro: {avogadro:.3e}")  # 6.022e+23
```

## 5. Common Mistakes to Avoid

### Mistake 1: Float Precision
```python
# Wrong - comparing floats directly
print(0.1 + 0.2 == 0.3)  # False!

# Right - use tolerance or Decimal
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

### Mistake 2: Integer Division vs Float Division
```python
# Wrong - expecting float
result = 10 / 2  # 5.0 (float, not int)

# Right - use // for integer division
result = 10 // 2  # 5 (int)
```

### Mistake 3: Modulus with Floats
```python
# Unexpected results with floats
print(0.1 % 0.1)  # 0.0 (usually works)
print(0.7 % 0.1)  # 0.09999999999999964 (precision issue)

# Solution - use Decimal for precise calculations
from decimal import Decimal
print(Decimal('0.7') % Decimal('0.1'))  # 0.0
```

### Mistake 4: Missing Import
```python
# Wrong - math module not imported
print(math.sqrt(16))  # NameError!

# Right - import first
import math
print(math.sqrt(16))  # 4.0
```

## 6. Best Practices

1. **Use underscores** for large numbers: `1_000_000`
2. **Use Decimal** for financial calculations
3. **Use math.isclose()** for float comparisons
4. **Import math** when needed for advanced functions
5. **Choose appropriate type**: int for whole numbers, float for decimals
6. **Format numbers** for display: commas, decimal places

## 7. Practice Exercises

### Exercise 1: Calculator
Create a calculator that performs all basic arithmetic operations.

### Exercise 2: Math Functions
Write a program that uses math module functions to calculate circle area, circumference, and volume of a sphere.

### Exercise 3: Number Formatter
Create a program that formats numbers in different ways: currency, percentage, scientific notation.

## 8. Summary

**Key takeaways:**
- Python has three numeric types: int, float, complex
- Integers have arbitrary precision (no overflow)
- Floats have limited precision (~15-17 digits)
- Use math module for advanced mathematical functions
- Use Decimal for precise calculations
- Format numbers for display

**Next Lecture:** We'll learn about type conversion and casting.

---

**Quick Reference:**
- Math Module: https://docs.python.org/3/library/math.html
- Decimal Module: https://docs.python.org/3/library/decimal.html
- Numeric Types: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex