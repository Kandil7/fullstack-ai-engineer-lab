"""
W3Schools Python Tutorial - 12: Python Operators
=================================================
Topics: Arithmetic, assignment, comparison, logical, identity, membership

Run: python 12-operators.py
Reference: https://www.w3schools.com/python/python_operators.asp
"""

# ============================================================
# Arithmetic Operators
# ============================================================
# Example 1: Basic arithmetic
x = 15
y = 4

print("--- Arithmetic Operators ---")
print(f"{x} + {y} = {x + y}")     # 19 - Addition
print(f"{x} - {y} = {x - y}")     # 11 - Subtraction
print(f"{x} * {y} = {x * y}")     # 60 - Multiplication
print(f"{x} / {y} = {x / y}")     # 3.75 - Division (always float)
print(f"{x} // {y} = {x // y}")   # 3 - Floor division (rounds down)
print(f"{x} % {y} = {x % y}")     # 3 - Modulus (remainder)
print(f"{x} ** {y} = {x ** y}")   # 50625 - Exponentiation

# Output:
# 15 + 4 = 19
# 15 - 4 = 11
# 15 * 4 = 60
# 15 / 4 = 3.75
# 15 // 4 = 3
# 15 % 4 = 3
# 15 ** 4 = 50625

# ============================================================
# Assignment Operators
# ============================================================
# Example 2: Assignment operators
x = 10
print(f"\n--- Assignment Operators ---")
print(f"x = {x}")

x += 5   # x = x + 5
print(f"x += 5 -> {x}")  # 15

x -= 3   # x = x - 3
print(f"x -= 3 -> {x}")  # 12

x *= 2   # x = x * 2
print(f"x *= 2 -> {x}")  # 24

x /= 4   # x = x / 4
print(f"x /= 4 -> {x}")  # 6.0

x //= 2  # x = x // 2
print(f"x //= 2 -> {x}")  # 3.0

x **= 3  # x = x ** 3
print(f"x **= 3 -> {x}")  # 27.0

x %= 5   # x = x % 5
print(f"x %= 5 -> {x}")  # 2.0

# Other assignment operators
x = 60
x &= 12   # Bitwise AND
print(f"\n60 &= 12 -> {x}")  # 12

x |= 8    # Bitwise OR
print(f"12 |= 8 -> {x}")  # 28

x ^= 5    # Bitwise XOR
print(f"28 ^= 5 -> {x}")  # 25

x >>= 1   # Right shift
print(f"25 >>= 1 -> {x}")  # 12

x <<= 2   # Left shift
print(f"12 <<= 2 -> {x}")  # 48

# ============================================================
# Comparison Operators
# ============================================================
# Example 3: Comparison operators
x = 10
y = 20

print(f"\n--- Comparison Operators ---")
print(f"{x} == {y}: {x == y}")   # False - Equal
print(f"{x} != {y}: {x != y}")   # True - Not equal
print(f"{x} > {y}: {x > y}")     # False - Greater than
print(f"{x} < {y}: {x < y}")     # True - Less than
print(f"{x} >= {y}: {x >= y}")   # False - Greater or equal
print(f"{x} <= {y}: {x <= y}")   # True - Less or equal

# Chained comparisons (Pythonic!)
z = 15
print(f"\n10 < 15 < 20: {10 < 15 < 20}")  # True
print(f"10 < 5 < 20: {10 < 5 < 20}")      # False

# ============================================================
# Logical Operators
# ============================================================
# Example 4: Logical operators
print(f"\n--- Logical Operators ---")
x = True
y = False

print(f"True and True: {True and True}")    # True
print(f"True and False: {True and False}")  # False
print(f"True or False: {True or False}")    # True
print(f"not True: {not True}")              # False

# Practical example
age = 25
income = 50000
print(f"\nAge: {age}, Income: {income}")
print(f"Eligible for loan: {age >= 18 and income >= 30000}")
# Output: True

# Short-circuit evaluation
# 'and' returns the first falsy value, or the last value
print(f"\nShort-circuit and: {5 and 3}")    # 3 (both truthy, returns last)
print(f"Short-circuit and: {0 and 3}")      # 0 (first falsy)
print(f"Short-circuit or: {5 or 3}")        # 5 (first truthy)
print(f"Short-circuit or: {0 or 3}")        # 3 (first falsy, returns last)

# ============================================================
# Identity Operators
# ============================================================
# Example 5: Identity operators (is, is not)
# 'is' checks if two variables point to the SAME OBJECT in memory
# '==' checks if two variables have the SAME VALUE

print(f"\n--- Identity Operators ---")
x = [1, 2, 3]
y = [1, 2, 3]
z = x

print(f"x == y: {x == y}")      # True (same value)
print(f"x is y: {x is y}")      # False (different objects!)
print(f"x is z: {x is z}")      # True (same object)

# Common use: check for None
value = None
print(f"\nvalue is None: {value is None}")          # True
print(f"value is not None: {value is not None}")    # False

# Small integer caching (CPython optimization)
a = 256
b = 256
print(f"\n256 is 256: {a is b}")  # True (cached)

a = 257
b = 257
print(f"257 is 257: {a is b}")    # May be True or False (implementation dependent)

# ============================================================
# Membership Operators
# ============================================================
# Example 6: Membership operators (in, not in)
print(f"\n--- Membership Operators ---")

# In a string
text = "Hello, World!"
print(f"'Hello' in text: {'Hello' in text}")        # True
print(f"'Python' not in text: {'Python' not in text}")  # True

# In a list
fruits = ["apple", "banana", "cherry"]
print(f"\n'apple' in fruits: {'apple' in fruits}")      # True
print(f"'grape' in fruits: {'grape' in fruits}")        # False
print(f"'grape' not in fruits: {'grape' not in fruits}")  # True

# In a tuple
colors = ("red", "green", "blue")
print(f"\n'red' in colors: {'red' in colors}")  # True

# In a dictionary (checks KEYS)
person = {"name": "Alice", "age": 30}
print(f"\n'name' in person: {'name' in person}")          # True
print(f"'Alice' in person: {'Alice' in person}")          # False
print(f"'Alice' in person.values(): {'Alice' in person.values()}")  # True

# In a set
unique = {1, 2, 3, 4, 5}
print(f"\n3 in unique: {3 in unique}")  # True

# ============================================================
# Bitwise Operators
# ============================================================
# Example 7: Bitwise operators
a = 60   # 0011 1100
b = 13   # 0000 1101

print(f"\n--- Bitwise Operators ---")
print(f"a = {a} ({bin(a)})")
print(f"b = {b} ({bin(b)})")
print(f"a & b = {a & b} ({bin(a & b)})")     # 12 - AND
print(f"a | b = {a | b} ({bin(a | b)})")     # 61 - OR
print(f"a ^ b = {a ^ b} ({bin(a ^ b)})")     # 49 - XOR
print(f"~a = {~a}")                          # -61 - NOT
print(f"a << 2 = {a << 2} ({bin(a << 2)})")  # 240 - Left shift
print(f"a >> 2 = {a >> 2} ({bin(a >> 2)})")  # 15 - Right shift

# ============================================================
# Operator Precedence
# ============================================================
# Example 8: Order of operations
print(f"\n--- Operator Precedence ---")
print(f"2 + 3 * 4 = {2 + 3 * 4}")       # 14 (not 20!)
print(f"(2 + 3) * 4 = {(2 + 3) * 4}")   # 20
print(f"2 ** 3 ** 2 = {2 ** 3 ** 2}")   # 512 (right to left: 2**(3**2))
print(f"(2 ** 3) ** 2 = {(2 ** 3) ** 2}")  # 64

# Precedence order (highest to lowest):
# 1. ** (exponentiation)
# 2. ~, +, - (unary)
# 3. *, /, //, % (multiplication)
# 4. +, - (addition)
# 5. >>, << (bitwise shift)
# 6. & (bitwise AND)
# 7. ^, | (bitwise XOR, OR)
# 8. ==, !=, >, <, >=, <=, is, in (comparisons)
# 9. not (logical NOT)
# 10. and (logical AND)
# 11. or (logical OR)

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Arithmetic: + - * / // % **")
print("2. Assignment: = += -= *= /= //= %= **= &= |= ^= >>= <<=")
print("3. Comparison: == != > < >= <=")
print("4. Logical: and or not")
print("5. Identity: is, is not (checks object identity)")
print("6. Membership: in, not in (checks membership)")
print("7. Bitwise: & | ^ ~ << >>")
