# Python Math — Glossary 27

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| `math.pi` | Pi constant (3.14159...) | `math.pi` |
| `math.e` | Euler's number (2.71828...) | `math.e` |
| `math.inf` | Infinity | `math.inf` |
| `math.nan` | Not a Number | `math.nan` |
| `math.sqrt()` | Square root | `math.sqrt(16)` → 4.0 |
| `math.pow()` | Power function | `math.pow(2, 10)` → 1024.0 |
| `math.exp()` | e raised to power | `math.exp(1)` → 2.718... |
| `math.log()` | Natural logarithm | `math.log(100)` |
| `math.log2()` | Log base 2 | `math.log2(8)` → 3.0 |
| `math.log10()` | Log base 10 | `math.log10(100)` → 2.0 |
| `math.sin()` | Sine (radians) | `math.sin(math.pi/2)` → 1.0 |
| `math.cos()` | Cosine (radians) | `math.cos(0)` → 1.0 |
| `math.tan()` | Tangent (radians) | `math.tan(math.pi/4)` → 1.0 |
| `math.radians()` | Degrees to radians | `math.radians(180)` → π |
| `math.degrees()` | Radians to degrees | `math.degrees(math.pi)` → 180 |
| `math.ceil()` | Round up | `math.ceil(4.3)` → 5 |
| `math.floor()` | Round down | `math.floor(4.7)` → 4 |
| `math.trunc()` | Truncate toward zero | `math.trunc(4.7)` → 4 |
| `math.factorial()` | Factorial | `math.factorial(5)` → 120 |
| `math.gcd()` | Greatest common divisor | `math.gcd(12, 8)` → 4 |
| `math.lcm()` | Least common multiple | `math.lcm(4, 6)` → 12 |
| `math.hypotenuse()` | Pythagorean hypotenuse | `math.hypot(3, 4)` → 5.0 |
| `math.isclose()` | Approximate equality | `math.isclose(0.1+0.2, 0.3)` |
| `math.comb()` | Combinations (n choose k) | `math.comb(10, 3)` → 120 |
| `math.perm()` | Permutations | `math.perm(10, 3)` → 720 |
| `random.random()` | Float 0.0-1.0 | `random.random()` |
| `random.randint()` | Random integer | `random.randint(1, 10)` |
| `random.choice()` | Random selection | `random.choice(lst)` |
| `random.shuffle()` | Shuffle in-place | `random.shuffle(lst)` |
| `random.seed()` | Set random seed | `random.seed(42)` |
| `random.sample()` | Random sample | `random.sample(range(10), 3)` |

---

## Definitions

### Combinations
**Definition**: The number of ways to choose k items from n items without order. Calculated as n! / (k! * (n-k)!).

**Example**:
```python
import math

# 10 choose 3
print(math.comb(10, 3))  # 120

# 5 choose 5
print(math.comb(5, 5))   # 1

# 5 choose 0
print(math.comb(5, 0))   # 1
```

**Related**: permutations, factorial, binomial coefficient

---

### Decimal
**Definition**: A module for decimal floating-point arithmetic with arbitrary precision. Avoids floating-point rounding errors for financial calculations.

**Example**:
```python
from decimal import Decimal, getcontext

# Set precision
getcontext().prec = 10

# Precise decimal arithmetic
a = Decimal("0.1")
b = Decimal("0.2")
print(a + b)  # 0.3 — exactly 0.3!

# vs float
print(0.1 + 0.2)  # 0.30000000000000004
```

**Related**: float, precision, financial calculations

---

### Factorial
**Definition**: The product of all positive integers up to n. Written as n! where n! = n × (n-1) × ... × 1.

**Example**:
```python
import math

print(math.factorial(0))   # 1 (by definition)
print(math.factorial(1))   # 1
print(math.factorial(5))   # 120 (5*4*3*2*1)
print(math.factorial(10))  # 3628800
```

**Related**: permutations, combinations, combinatorics

---

### Float
**Definition**: A floating-point number representing real numbers with decimal points. Python uses double precision (64-bit) floats.

**Example**:
```python
# Float operations
x = 3.14
y = 2.0

print(x + y)  # 5.14
print(x * y)  # 6.28

# Float precision issues
print(0.1 + 0.2)  # 0.30000000000000004
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

**Related**: decimal, precision, math.isclose()

---

### GCD
**Definition**: Greatest Common Divisor — the largest positive integer that divides both numbers without remainder.

**Example**:
```python
import math

print(math.gcd(12, 8))    # 4
print(math.gcd(12, 8, 6)) # 2
print(math.gcd(7, 13))    # 1 (coprime)
```

**Related**: LCM, coprime, number theory

---

### Hypotenuse
**Definition**: The longest side of a right triangle, calculated using the Pythagorean theorem: √(a² + b²).

**Example**:
```python
import math

# 3-4-5 triangle
print(math.hypot(3, 4))     # 5.0

# 5-12-13 triangle
print(math.hypot(5, 12))    # 13.0

# Works with more dimensions
print(math.hypot(1, 2, 3))  # 3.7416573867739413
```

**Related**: Pythagorean theorem, distance, trigonometry

---

### Infinity
**Definition**: A value representing mathematical infinity. Used for comparisons and as a sentinel value.

**Example**:
```python
import math

print(math.inf > 1000000)    # True
print(-math.inf < -1000000)  # True
print(math.inf == math.inf)  # True
print(math.inf + 1)          # inf

# Useful for finding minimum
def find_minimum(values):
    minimum = math.inf
    for v in values:
        if v < minimum:
            minimum = v
    return minimum
```

**Related**: NaN, comparison, sentinel value

---

### LCM
**Definition**: Least Common Multiple — the smallest positive integer divisible by both numbers.

**Example**:
```python
import math

print(math.lcm(4, 6))     # 12
print(math.lcm(4, 6, 8))  # 24
print(math.lcm(3, 5))     # 15
```

**Related**: GCD, multiples, number theory

---

### Logarithm
**Definition**: The power to which a base must be raised to get a number. Common bases: e (natural), 10 (common), 2 (binary).

**Example**:
```python
import math

print(math.log(100))        # 4.605... (natural log, base e)
print(math.log(100, 10))    # 2.0 (log base 10)
print(math.log(8, 2))       # 3.0 (log base 2)
print(math.log2(8))         # 3.0
print(math.log10(100))      # 2.0
```

**Related**: exp(), inverse, exponential

---

### NaN
**Definition**: Not a Number — represents undefined or unrepresentable results (0/0, inf-inf, etc.).

**Example**:
```python
import math

print(math.nan)              # nan
print(math.nan == math.nan)  # False (NaN != NaN!)
print(math.isnan(math.nan))  # True (use this to check)

# NaN propagates
print(math.nan + 1)          # nan
print(math.nan * 0)          # nan
```

**Related**: infinity, undefined, comparison

---

### Permutations
**Definition**: The number of ways to arrange k items from n items where order matters. Calculated as n! / (n-k)!.

**Example**:
```python
import math

# 10 permute 3
print(math.perm(10, 3))  # 720

# 5 permute 5
print(math.perm(5, 5))   # 120 (same as 5!)
```

**Related**: combinations, factorial, ordering

---

### Pi
**Definition**: The mathematical constant π ≈ 3.141592653589793, the ratio of a circle's circumference to its diameter.

**Example**:
```python
import math

print(math.pi)  # 3.141592653589793

# Circle calculations
radius = 5
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius

print(f"Area: {area:.2f}")  # 78.54
print(f"Circumference: {circumference:.2f}")  # 31.42
```

**Related**: circle, tau, trigonometry

---

### Pythagorean Theorem
**Definition**: In a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides: a² + b² = c².

**Example**:
```python
import math

def is_right_triangle(a, b, c):
    sides = sorted([a, b, c])
    return math.isclose(sides[0]**2 + sides[1]**2, sides[2]**2)

print(is_right_triangle(3, 4, 5))   # True
print(is_right_triangle(5, 12, 13)) # True
print(is_right_triangle(3, 4, 6))   # False
```

**Related**: hypotenuse, trigonometry, geometry

---

### Radians
**Definition**: The standard unit of angular measure. 180° = π radians. Trig functions in Python use radians.

**Example**:
```python
import math

# Degrees to radians
print(math.radians(90))   # π/2 ≈ 1.5708
print(math.radians(180))  # π ≈ 3.1416

# Radians to degrees
print(math.degrees(math.pi))      # 180.0
print(math.degrees(math.pi / 2))  # 90.0
```

**Related**: degrees, trigonometry, conversion

---

### Random
**Definition**: The `random` module provides functions for generating random numbers and making random selections.

**Example**:
```python
import random

# Random float 0.0 to 1.0
print(random.random())

# Random integer in range (inclusive)
print(random.randint(1, 100))

# Random choice
colors = ["red", "green", "blue"]
print(random.choice(colors))

# Random sample (no repeats)
print(random.sample(range(100), 5))

# Shuffle in-place
lst = [1, 2, 3, 4, 5]
random.shuffle(lst)
print(lst)
```

**Related**: seed, choice, shuffle, sample

---

### Square Root
**Definition**: A value that, when multiplied by itself, gives the original number. √x is the square root of x.

**Example**:
```python
import math

print(math.sqrt(16))   # 4.0
print(math.sqrt(2))    # 1.4142135623730951
print(math.sqrt(0))    # 0.0

# Or use exponent
print(16 ** 0.5)       # 4.0
```

**Related**: power, exponent, Pythagorean theorem

---

## Code Examples

### Example 1: Distance Between Points
```python
import math

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

print(euclidean_distance((0, 0), (3, 4)))  # 5.0
print(euclidean_distance((1, 1), (4, 5)))  # 5.0
```

### Example 2: Compound Interest
```python
import math

def compound_interest(principal, rate, years, n=12):
    """Calculate compound interest."""
    return principal * (1 + rate/n) ** (n * years)

final = compound_interest(10000, 0.05, 10)
print(f"Final: ${final:,.2f}")  # $16,470.09
```

### Example 3: Normal Distribution PDF
```python
import math

def normal_pdf(x, mu=0, sigma=1):
    """Normal distribution probability density function."""
    coefficient = 1 / (sigma * math.sqrt(2 * math.pi))
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    return coefficient * math.exp(exponent)

for x in range(-3, 4):
    print(f"x={x}: {normal_pdf(x):.4f}")
```

---

## Related Concepts

- **NumPy**: Numerical computing library for arrays and math
- **statistics**: Standard library for statistical calculations
- **decimal**: Precise decimal arithmetic
- **fractions**: Rational number arithmetic
- **cmath**: Complex number math
- **math.isclose()**: Safe float comparison
