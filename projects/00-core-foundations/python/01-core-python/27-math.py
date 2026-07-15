"""
W3Schools Python Tutorial - 27: Python Math
============================================
Topics: Math module, min(), max(), abs(), pow(), sqrt(), round()

Run: python 27-math.py
Reference: https://www.w3schools.com/python/python_math.asp
"""

# ============================================================
# Built-in Math Functions
# ============================================================
# Example 1: Basic math functions
print("--- Built-in Math Functions ---")

print(f"abs(-15) = {abs(-15)}")          # 15
print(f"abs(-3.14) = {abs(-3.14)}")      # 3.14
print(f"abs(10) = {abs(10)}")            # 10

print(f"\npow(2, 10) = {pow(2, 10)}")    # 1024.0
print(f"pow(3, 3) = {pow(3, 3)}")        # 27.0
print(f"pow(4, 0.5) = {pow(4, 0.5)}")    # 2.0 (square root)

print(f"\n2 ** 10 = {2 ** 10}")           # 1024
print(f"3 ** 3 = {3 ** 3}")              # 27

# ============================================================
# min() and max()
# ============================================================
# Example 2: Finding min and max
print("\n--- min() and max() ---")

# With multiple arguments
print(f"min(5, 3, 8, 1) = {min(5, 3, 8, 1)}")  # 1
print(f"max(5, 3, 8, 1) = {max(5, 3, 8, 1)}")  # 8

# With strings (alphabetical order)
print(f"min('apple', 'banana') = {min('apple', 'banana')}")
print(f"max('apple', 'banana') = {max('apple', 'banana')}")

# With lists
numbers = [45, 12, 89, 23, 67]
print(f"min(numbers) = {min(numbers)}")   # 12
print(f"max(numbers) = {max(numbers)}")   # 89

# With key function
words = ["banana", "apple", "cherry", "date"]
print(f"min by length: {min(words, key=len)}")  # date
print(f"max by length: {max(words, key=len)}")  # banana

# ============================================================
# round()
# ============================================================
# Example 3: Rounding numbers
print("\n--- round() ---")

print(f"round(3.7) = {round(3.7)}")      # 4
print(f"round(3.2) = {round(3.2)}")      # 3
print(f"round(3.5) = {round(3.5)}")      # 4 (banker's rounding)
print(f"round(2.5) = {round(2.5)}")      # 2 (banker's rounding!)

# Rounding to decimal places
print(f"round(3.14159, 2) = {round(3.14159, 2)}")  # 3.14
print(f"round(3.14159, 3) = {round(3.14159, 3)}")  # 3.142

# Rounding negative numbers
print(f"round(-3.7) = {round(-3.7)}")    # -4
print(f"round(-3.2) = {round(-3.2)}")    # -3

# ============================================================
# The math Module
# ============================================================
# Example 4: Math module constants
import math

print("\n--- math Module Constants ---")
print(f"pi = {math.pi}")        # 3.141592653589793
print(f"e = {math.e}")          # 2.718281828459045
print(f"inf = {math.inf}")      # inf (infinity)
print(f"tau = {math.tau}")      # 6.283185307179586 (2 * pi)

# ============================================================
# Power and Root Functions
# ============================================================
# Example 5: Power and root operations
print("\n--- Power and Root ---")

print(f"sqrt(144) = {math.sqrt(144)}")    # 12.0
print(f"sqrt(2) = {math.sqrt(2)}")        # 1.4142135623730951
print(f"cbrt(27) = {math.cbrt(27)}")      # 3.0 (Python 3.11+)
print(f"pow(2, 10) = {math.pow(2, 10)}")  # 1024.0

# ============================================================
# Logarithmic Functions
# ============================================================
# Example 6: Logarithms
print("\n--- Logarithmic Functions ---")

print(f"log(100) = {math.log(100)}")          # Natural log (ln)
print(f"log(100, 10) = {math.log(100, 10)}")  # Log base 10
print(f"log2(8) = {math.log2(8)}")             # Log base 2
print(f"log10(1000) = {math.log10(1000)}")    # Log base 10

# exp() - e^x
print(f"exp(1) = {math.exp(1)}")   # e^1 = 2.71828...
print(f"exp(0) = {math.exp(0)}")   # e^0 = 1.0

# ============================================================
# Trigonometric Functions
# ============================================================
# Example 7: Trigonometry
print("\n--- Trigonometric Functions ---")

# Angles in radians
print(f"sin(pi/2) = {math.sin(math.pi/2)}")  # 1.0
print(f"cos(0) = {math.cos(0)}")              # 1.0
print(f"tan(pi/4) = {math.tan(math.pi/4)}")  # ~1.0

# Convert degrees to radians
angle_degrees = 45
angle_radians = math.radians(angle_degrees)
print(f"\n{angle_degrees}° = {angle_radians} radians")
print(f"sin({angle_degrees}°) = {math.sin(angle_radians):.4f}")

# Convert radians to degrees
radians = math.pi / 4
degrees = math.degrees(radians)
print(f"{radians} radians = {degrees}°")

# ============================================================
# Rounding Functions
# ============================================================
# Example 8: Different rounding methods
print("\n--- Rounding Functions ---")

print(f"ceil(4.3) = {math.ceil(4.3)}")      # 5 (round up)
print(f"ceil(-4.3) = {math.ceil(-4.3)}")    # -4 (toward infinity)
print(f"floor(4.7) = {math.floor(4.7)}")    # 4 (round down)
print(f"floor(-4.7) = {math.floor(-4.7)}")  # -5 (toward -infinity)
print(f"trunc(4.7) = {math.trunc(4.7)}")    # 4 (truncate toward zero)
print(f"trunc(-4.7) = {math.trunc(-4.7)}")  # -4 (truncate toward zero)

# ============================================================
# Combinatorics
# ============================================================
# Example 9: Factorial and GCD
print("\n--- Combinatorics ---")

print(f"factorial(5) = {math.factorial(5)}")      # 120
print(f"factorial(10) = {math.factorial(10)}")    # 3628800
print(f"factorial(0) = {math.factorial(0)}")      # 1

print(f"gcd(48, 18) = {math.gcd(48, 18)}")       # 6
print(f"gcd(100, 75) = {math.gcd(100, 75)}")     # 25

# ============================================================
# Hyperbolic Functions
# ============================================================
# Example 10: Hyperbolic functions
print("\n--- Hyperbolic Functions ---")

print(f"sinh(1) = {math.sinh(1)}")
print(f"cosh(1) = {math.cosh(1)}")
print(f"tanh(1) = {math.tanh(1)}")

# ============================================================
# Practical Examples
# ============================================================
# Example 11: Real-world math applications
print("\n--- Practical Examples ---")

# Distance between two points
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

d = distance(0, 0, 3, 4)
print(f"Distance (0,0) to (3,4): {d}")

# Circle area and circumference
radius = 5
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius
print(f"\nCircle (r={radius}):")
print(f"  Area: {area:.2f}")
print(f"  Circumference: {circumference:.2f}")

# Compound interest
principal = 1000
rate = 0.05
years = 10
amount = principal * (1 + rate) ** years
print(f"\nCompound Interest:")
print(f"  Principal: ${principal}")
print(f"  Rate: {rate * 100}%")
print(f"  Years: {years}")
print(f"  Amount: ${amount:.2f}")

# Standard deviation
def stdev(data):
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return math.sqrt(variance)

data = [2, 4, 4, 4, 5, 5, 7, 9]
print(f"\nData: {data}")
print(f"Mean: {sum(data) / len(data)}")
print(f"Std Dev: {stdev(data):.4f}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Built-in: abs(), pow(), round(), min(), max()")
print("2. math.sqrt(): square root")
print("3. math.ceil()/floor(): round up/down")
print("4. math.log(): logarithms (natural, base 10, base 2)")
print("5. Trig: sin(), cos(), tan() (use radians!)")
print("6. math.radians()/degrees(): angle conversion")
print("7. math.factorial(): factorial calculation")
print("8. math.gcd(): greatest common divisor")
