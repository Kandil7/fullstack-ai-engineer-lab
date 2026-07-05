"""
W3Schools Python Tutorial - 09: Python Casting
===============================================
Topics: int(), float(), str() conversion, common scenarios

Run: python 09-casting.py
Reference: https://www.w3schools.com/python/python_casting.asp
"""

# ============================================================
# What is Casting?
# ============================================================
# Casting is the process of converting a value from one type to another.
# Python is dynamically typed, but sometimes you need explicit conversion.

# ============================================================
# int() - Convert to Integer
# ============================================================
# Example 1: int() conversions

# From float (truncates, does NOT round!)
x = int(3.7)
print(f"int(3.7) = {x}")  # Output: 3 (not 4!)

x = int(3.2)
print(f"int(3.2) = {x}")  # Output: 3

# From negative float
x = int(-3.7)
print(f"int(-3.7) = {x}")  # Output: -3 (truncates toward zero)

# From string
x = int("42")
print(f"int('42') = {x}")  # Output: 42

# From string with base
x = int("1010", 2)   # Binary
print(f"int('1010', 2) = {x}")  # Output: 10

x = int("FF", 16)    # Hexadecimal
print(f"int('FF', 16) = {x}")  # Output: 255

x = int("77", 8)     # Octal
print(f"int('77', 8) = {x}")  # Output: 63

# From boolean
x = int(True)
print(f"int(True) = {x}")  # Output: 1

x = int(False)
print(f"int(False) = {x}")  # Output: 0

# ⚠️ These would cause ValueError:
# int("hello")     # ValueError: invalid literal
# int("3.14")      # ValueError: can't convert string to int
# int(None)        # TypeError

# ============================================================
# float() - Convert to Float
# ============================================================
# Example 2: float() conversions

x = float(3)
print(f"\nfloat(3) = {x}")  # Output: 3.0

x = float("3.14")
print(f"float('3.14') = {x}")  # Output: 3.14

x = float("-42")
print(f"float('-42') = {x}")  # Output: -42.0

x = float("inf")
print(f"float('inf') = {x}")  # Output: inf (infinity)

x = float("-inf")
print(f"float('-inf') = {x}")  # Output: -inf

x = float(True)
print(f"float(True) = {x}")  # Output: 1.0

x = float(False)
print(f"float(False) = {x}")  # Output: 0.0

# ⚠️ These would cause ValueError:
# float("hello")
# float("3.14.15")

# ============================================================
# str() - Convert to String
# ============================================================
# Example 3: str() conversions

x = str(42)
print(f"\nstr(42) = '{x}', type: {type(x).__name__}")

x = str(3.14)
print(f"str(3.14) = '{x}', type: {type(x).__name__}")

x = str(True)
print(f"str(True) = '{x}', type: {type(x).__name__}")

x = str([1, 2, 3])
print(f"str([1,2,3]) = '{x}', type: {type(x).__name__}")

x = str({"a": 1})
print(f"str({{'a': 1}}) = '{x}', type: {type(x).__name__}")

# Output:
# str(42) = '42', type: str
# str(3.14) = '3.14', type: str
# str(True) = 'True', type: str
# str([1,2,3]) = '[1, 2, 3]', type: str
# str({'a': 1}) = "{'a': 1}", type: str

# ============================================================
# Common Conversion Scenarios
# ============================================================
# Example 4: User input is always a string
user_input = "42"  # Simulating input() which returns string
number = int(user_input)
print(f"\nUser input: '{user_input}' (string)")
print(f"Converted: {number} (integer)")
print(f"Doubled: {number * 2}")

# Example 5: Math with mixed types
x = 10      # int
y = 3.14    # float
result = x + y
print(f"\n{x} (int) + {y} (float) = {result} (float)")
print(f"Type: {type(result).__name__}")

# Python automatically promotes int to float for mixed operations
x = 5
y = 2.0
print(f"\n{x} / {y} = {x / y}")  # Always returns float
print(f"{x} // {y} = {x // y}")  # Floor division

# ============================================================
# String to Number and Back
# ============================================================
# Example 6: Converting strings to numbers for calculations
price_str = "19.99"
quantity_str = "5"

price = float(price_str)
quantity = int(quantity_str)
total = price * quantity

print(f"\nPrice: ${price}")
print(f"Quantity: {quantity}")
print(f"Total: ${total:.2f}")

# Converting result back to string for display
total_str = f"${total:.2f}"
print(f"Total as string: {total_str}")

# ============================================================
# Safe Conversion with try/except
# ============================================================
# Example 7: Handling conversion errors
def safe_int(value, default=0):
    """Safely convert a value to int, returning default on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """Safely convert a value to float, returning default on failure."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

print("\n--- Safe Conversion ---")
print(f"safe_int('42') = {safe_int('42')}")      # 42
print(f"safe_int('abc') = {safe_int('abc')}")    # 0 (default)
print(f"safe_int(None) = {safe_int(None)}")      # 0 (default)
print(f"safe_float('3.14') = {safe_float('3.14')}")  # 3.14
print(f"safe_float('abc') = {safe_float('abc')}")    # 0.0 (default)

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. int() converts to integer (truncates, doesn't round)")
print("2. float() converts to floating-point number")
print("3. str() converts to string")
print("4. input() always returns a string - cast before math!")
print("5. Python auto-promotes int to float in mixed operations")
print("6. Use try/except for safe conversion of uncertain input")
