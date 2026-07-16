# Python Math — Lecture 27

## Topic Overview

Python's `math` module provides access to mathematical functions and constants. It includes functions for basic arithmetic, trigonometry, logarithms, number theory, and more. While Python has built-in operators for simple math, the `math` module offers advanced functions not available through operators.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Use built-in math operators and functions
- Import and use the `math` module
- Apply trigonometric and logarithmic functions
- Work with constants (pi, e, inf, nan)
- Implement statistical calculations
- Use the `random` module for random numbers
- Apply math to real-world scenarios

---

## Key Concepts

### 1. Built-in Math Operations

```python
# Basic arithmetic
print(5 + 3)      # Addition: 8
print(5 - 3)      # Subtraction: 2
print(5 * 3)      # Multiplication: 15
print(5 / 3)      # Division: 1.666...
print(5 // 3)     # Floor division: 1
print(5 % 3)      # Modulo: 2
print(5 ** 3)     # Exponent: 125

# Built-in functions
print(abs(-5))     # Absolute value: 5
print(round(3.7))  # Round: 4
print(round(3.14159, 2))  # Round to 2 decimals: 3.14
print(min(1, 2, 3))  # Minimum: 1
print(max(1, 2, 3))  # Maximum: 3
print(sum([1, 2, 3]))  # Sum: 6
```

### 2. Math Module Basics

```python
import math

# Constants
print(math.pi)       # 3.141592653589793
print(math.e)        # 2.718281828459045
print(math.tau)      # 6.283185307179586 (2*pi)
print(math.inf)      # Infinity
print(math.nan)      # Not a Number

# Power and roots
print(math.pow(2, 10))     # 1024.0
print(math.sqrt(16))       # 4.0
print(math.exp(1))         # 2.718281828459045 (e^1)
print(math.log(100, 10))   # 2.0 (log base 10)
print(math.log(math.e))    # 1.0 (natural log)
print(math.log2(8))        # 3.0 (log base 2)
```

### 3. Rounding Functions

```python
import math

print(math.ceil(4.3))    # 5 — round up
print(math.ceil(-4.3))   # -4 — round toward infinity
print(math.floor(4.7))   # 4 — round down
print(math.floor(-4.7))  # -5 — round toward negative infinity

print(math.trunc(4.7))   # 4 — truncate toward zero
print(math.trunc(-4.7))  # -4 — truncate toward zero

# factorial and combinatorics
print(math.factorial(5))  # 120 (5! = 5*4*3*2*1)
print(math.comb(10, 3))  # 120 (10 choose 3)
print(math.perm(10, 3))  # 720 (10 permute 3)
```

### 4. Trigonometric Functions

```python
import math

# Convert degrees to radians
radians = math.radians(45)
print(radians)  # 0.7853981633974483

# Convert radians to degrees
degrees = math.degrees(math.pi / 4)
print(degrees)  # 45.0

# Trig functions (use radians!)
print(math.sin(math.pi / 2))   # 1.0
print(math.cos(0))              # 1.0
print(math.tan(math.pi / 4))   # 1.0

# Inverse trig
print(math.asin(1))      # 1.5707963267948966 (pi/2)
print(math.acos(1))      # 0.0
print(math.atan(1))      # 0.7853981633974483 (pi/4)

# Hyperbolic
print(math.sinh(1))      # 1.1752011936438014
print(math.cosh(1))      # 1.5430806348152437
```

### 5. Logarithmic Functions

```python
import math

print(math.log(100))         # 4.605170185988092 (natural log)
print(math.log(100, 10))     # 2.0 (log base 10)
print(math.log(8, 2))        # 3.0 (log base 2)
print(math.log2(8))          # 3.0
print(math.log10(100))       # 2.0
print(math.log1p(1e-10))     # Very precise for small numbers

# Exponential
print(math.exp(0))           # 1.0 (e^0)
print(math.exp(1))           # 2.718281828459045 (e^1)
print(math.expm1(0))         # 0.0 (precise for small values)
```

### 6. Number Theory

```python
import math

# GCD (Greatest Common Divisor)
print(math.gcd(12, 8))    # 4
print(math.gcd(12, 8, 6)) # 2

# LCM (Least Common Multiple) — Python 3.9+
print(math.lcm(4, 6))     # 12
print(math.lcm(4, 6, 8))  # 24

# Coprime check
def are_coprime(a, b):
    return math.gcd(a, b) == 1

print(are_coprime(14, 15))  # True
print(are_coprime(14, 21))  # False

# Hypotenuse
print(math.hypot(3, 4))     # 5.0
print(math.hypot(5, 12))    # 13.0
```

### 7. Statistical Functions

```python
import math

def mean(data):
    return sum(data) / len(data)

def variance(data):
    avg = mean(data)
    return sum((x - avg) ** 2 for x in data) / len(data)

def std_dev(data):
    return math.sqrt(variance(data))

data = [10, 20, 30, 40, 50]
print(f"Mean: {mean(data)}")       # 30.0
print(f"Variance: {variance(data)}") # 200.0
print(f"Std Dev: {std_dev(data)}")  # 14.142135623730951
```

### 8. The Random Module

```python
import random

# Random float 0.0 to 1.0
print(random.random())

# Random integer in range
print(random.randint(1, 10))  # 1-10 inclusive

# Random choice from list
fruits = ["apple", "banana", "cherry"]
print(random.choice(fruits))

# Random sample (no repeats)
print(random.sample(range(100), 5))  # 5 unique random numbers

# Shuffle list in-place
cards = list(range(1, 53))
random.shuffle(cards)
print(cards[:5])  # First 5 cards

# Random with seed (reproducible)
random.seed(42)
print(random.randint(1, 100))  # Always same number
```

---

## Code Examples

### Example 1: Distance Calculator

```python
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates (km)."""
    R = 6371  # Earth's radius in km
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

# Distance: NYC to London
dist = haversine_distance(40.7128, -74.0060, 51.5074, -0.1278)
print(f"Distance: {dist:.0f} km")  # ~5570 km
```

### Example 2: Compound Interest Calculator

```python
import math

def compound_interest(principal, rate, years, n=12):
    """Calculate compound interest."""
    A = principal * (1 + rate/n) ** (n * years)
    return A

# $10,000 at 5% for 10 years, compounded monthly
final = compound_interest(10000, 0.05, 10)
print(f"Final amount: ${final:,.2f}")  # $16,470.09
```

### Example 3: Normal Distribution

```python
import math

def normal_pdf(x, mu, sigma):
    """Probability density function of normal distribution."""
    coefficient = 1 / (sigma * math.sqrt(2 * math.pi))
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    return coefficient * math.exp(exponent)

# Bell curve values
for x in range(-3, 4):
    y = normal_pdf(x, 0, 1)
    print(f"x={x:2d}: {y:.4f}")
```

### Example 4: Prime Number Generator

```python
import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def primes_up_to(limit):
    return [n for n in range(2, limit + 1) if is_prime(n)]

print(primes_up_to(50))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

---

## Common Mistakes to Avoid

### Mistake 1: Using Degrees Instead of Radians
```python
import math

# WRONG — sin expects radians
# math.sin(90)  # Wrong!

# CORRECT — convert degrees to radians
print(math.sin(math.radians(90)))  # 1.0
print(math.sin(math.pi / 2))       # 1.0
```

### Mistake 2: Integer Division Surprise
```python
# Python 3: / always returns float
print(5 / 2)   # 2.5

# Python 2: / does integer division
# 5 / 2  # 2 (Python 2)

# Use // for floor division
print(5 // 2)  # 2
```

### Mistake 3: Floating Point Precision
```python
# WRONG — floating point issues
print(0.1 + 0.2 == 0.3)  # False!

# CORRECT — use math.isclose()
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

### Mistake 4: Dividing by Zero
```python
# WRONG — raises ZeroDivisionError
# result = 10 / 0

# CORRECT — check first
def safe_divide(a, b):
    if b == 0:
        return None
    return a / b
```

---

## Best Practices

1. **Use `math.isclose()`** for float comparison
2. **Convert degrees to radians** for trig functions
3. **Use `math.sqrt()`** for square roots (faster than `** 0.5`)
4. **Use `math.gcd()` and `math.lcm()`** for number theory
5. **Use `random.seed()`** for reproducible results
6. **Use `decimal` module** for precise financial calculations
7. **Use `statistics` module** for statistical calculations
8. **Check for `math.inf` and `math.nan`** in calculations

---

## Practice Exercises

### Exercise 1: Circle Calculator
Write functions to calculate area, circumference, and diameter of a circle.

### Exercise 2: Pythagorean Theorem
Write a function that checks if three sides form a right triangle.

### Exercise 3: Matrix Determinant
Write a function to calculate the determinant of a 2x2 matrix.

---

## Summary

- **Built-in**: `abs()`, `round()`, `min()`, `max()`, `sum()`
- **Math module**: `pi`, `e`, `sqrt()`, `pow()`, `log()`
- **Rounding**: `ceil()`, `floor()`, `trunc()`
- **Trig**: `sin()`, `cos()`, `tan()` (use radians!)
- **Logarithmic**: `log()`, `log2()`, `log10()`, `exp()`
- **Number theory**: `gcd()`, `lcm()`, `factorial()`
- **Random**: `random()`, `randint()`, `choice()`, `shuffle()`
- **Float comparison**: Use `math.isclose()`
- **Precision**: Use `decimal` for financial calculations
