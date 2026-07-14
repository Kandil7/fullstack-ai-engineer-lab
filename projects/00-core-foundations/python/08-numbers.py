"""
W3Schools Python Tutorial - 08: Python Numbers
===============================================
Topics: Integers, floats, complex, type conversion, random

Run: python 08-numbers.py
Reference: https://www.w3schools.com/python/python_numbers.asp
"""

# ============================================================
# Integers
# ============================================================
# Example 1: Integer basics
x = 1
y = 35656222554887711
z = -3255522

print(f"x = {x}, type: {type(x).__name__}")
print(f"y = {y}, type: {type(y).__name__}")
print(f"z = {z}, type: {type(z).__name__}")

# Integers have unlimited precision in Python!
huge = 10 ** 100  # A googol
print(f"Huge number: {huge}")
print(f"Digits: {len(str(huge))}")

# Underscores for readability (Python 3.6+)
population = 7_900_000_000
print(f"Population: {population}")

# Different bases
binary = 0b1010      # Binary (base 2)
octal = 0o17         # Octal (base 8)
hexadecimal = 0xFF   # Hexadecimal (base 16)

print(f"\nBinary 0b1010 = {binary}")
print(f"Octal 0o17 = {octal}")
print(f"Hex 0xFF = {hexadecimal}")

# Output:
# x = 1, type: int
# y = 35656222554887711, type: int
# z = -3255522, type: int
# Huge number: 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# Digits: 101
# Population: 7900000000
#
# Binary 0b1010 = 10
# Octal 0o17 = 15
# Hex 0xFF = 255

# ============================================================
# Floats (Floating Point Numbers)
# ============================================================
# Example 2: Float basics
x = 1.10
y = 1.0
z = -35.59

print(f"\nx = {x}")
print(f"y = {y}")
print(f"z = {z}")

# Floats can also be in scientific notation
a = 35e3    # 35 * 10^3 = 35000.0
b = 12E4    # 12 * 10^4 = 120000.0

print(f"35e3 = {a}")
print(f"12E4 = {b}")

# ⚠️ Floating point precision issue
print(f"\n0.1 + 0.2 = {0.1 + 0.2}")
# Output: 0.1 + 0.2 = 0.30000000000000004

# Fix with round()
print(f"rounded: {round(0.1 + 0.2, 1)}")
# Output: rounded: 0.3

# ============================================================
# Complex Numbers
# ============================================================
# Example 3: Complex numbers
x = 3 + 5j
y = 2 + 4j

print(f"\nComplex: {x}")
print(f"Real part: {x.real}")
print(f"Imaginary part: {x.imag}")

# Operations
print(f"\n{x} + {y} = {x + y}")
print(f"{x} * {y} = {x * y}")
print(f"Conjugate of {x}: {x.conjugate()}")

# Output:
# Complex: (3+5j)
# Real part: 3.0
# Imaginary part: 5.0

# (3+5j) + (2+4j) = (5+9j)
# (3+5j) * (2+4j) = (-14+22j)
# Conjugate of (3+5j): (3-5j)

# ============================================================
# Type Conversion (Casting)
# ============================================================
# Example 4: Converting between number types

# int to float
x = 10
y = float(x)
print(f"\nint {x} -> float {y}")

# float to int (truncates, doesn't round!)
x = 5.9
y = int(x)
print(f"float {x} -> int {y}")  # Output: 5 (not 6!)

# String to number
x = int("123")
y = float("3.14")
z = complex("1+2j")
print(f"str '123' -> int {x}")
print(f"str '3.14' -> float {y}")
print(f"str '1+2j' -> complex {z}")

# Number to string
x = str(123)
y = str(3.14)
print(f"int 123 -> str '{x}'")
print(f"float 3.14 -> str '{y}'")

# ============================================================
# Math Functions
# ============================================================
# Example 5: Built-in math operations
print("\n--- Built-in Math ---")
print(f"abs(-15) = {abs(-15)}")
print(f"pow(2, 10) = {pow(2, 10)}")
print(f"round(3.7) = {round(3.7)}")
print(f"round(3.14159, 2) = {round(3.14159, 2)}")
print(f"min(5, 3, 8, 1) = {min(5, 3, 8, 1)}")
print(f"max(5, 3, 8, 1) = {max(5, 3, 8, 1)}")

# ============================================================
# The math Module
# ============================================================
# Example 6: Using the math module
import math

print("\n--- math Module ---")
print(f"pi = {math.pi}")
print(f"e = {math.e}")
print(f"sqrt(144) = {math.sqrt(144)}")
print(f"ceil(4.3) = {math.ceil(4.3)}")
print(f"floor(4.7) = {math.floor(4.7)}")
print(f"factorial(5) = {math.factorial(5)}")
print(f"log(100, 10) = {math.log(100, 10)}")
print(f"sin(pi/2) = {math.sin(math.pi / 2)}")

# ============================================================
# Random Numbers
# ============================================================
# Example 7: Using the random module
import random

print("\n--- Random Numbers ---")
print(f"random() = {random.random()}")  # 0.0 to 1.0
print(f"randint(1, 10) = {random.randint(1, 10)}")  # 1 to 10
print(f"randrange(0, 10, 2) = {random.randrange(0, 10, 2)}")  # 0,2,4,6,8

# Random choice from a list
colors = ["red", "green", "blue", "yellow"]
print(f"choice = {random.choice(colors)}")

# Shuffle a list
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(f"shuffled = {numbers}")

# Random float in range
print(f"uniform(1.5, 6.5) = {random.uniform(1.5, 6.5):.2f}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. int: whole numbers with unlimited precision")
print("2. float: decimal numbers (watch for precision issues!)")
print("3. complex: numbers with real and imaginary parts")
print("4. Use int(), float(), str() for type conversion")
print("5. import math for advanced math functions")
print("6. import random for random number generation")
