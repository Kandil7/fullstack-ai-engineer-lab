"""
W3Schools Python Tutorial - 31: Python String Formatting
=========================================================
Topics: f-strings, .format(), % operator, template strings

Run: python 31-string-formatting.py
Reference: https://www.w3schools.com/python/python_string_formatting.asp
"""

# ============================================================
# f-Strings (Python 3.6+) - Recommended
# ============================================================
# Example 1: Basic f-string usage
print("--- f-Strings ---")

name = "Alice"
age = 30
height = 5.7

# Basic interpolation
print(f"Name: {name}")
print(f"Age: {age}")

# Expressions
print(f"Next year: {age + 1}")
print(f"Uppercase: {name.upper()}")

# Variables
print(f"{name} is {age} years old and {height} feet tall")

# Output:
# Name: Alice
# Age: 30
# Next year: 31
# Uppercase: ALICE
# Alice is 30 years old and 5.7 feet tall

# ============================================================
# f-String Formatting
# ============================================================
# Example 2: Formatting numbers
print("\n--- Number Formatting ---")

pi = 3.141592653589793

print(f"Default: {pi}")
print(f"2 decimal places: {pi:.2f}")
print(f"4 decimal places: {pi:.4f}")

# Width and alignment
print(f"\nWidth 10: {'hello':>10}")
print(f"Left align: {'hello':<10}")
print(f"Center: {'hello':^10}")
print(f"Fill with *: {'hello':*^10}")

# Number formatting
big_num = 1234567890
print(f"\nWith comma: {big_num:,}")
print(f"With underscore: {big_num:_}")

# Percentage
rate = 0.856
print(f"Percentage: {rate:.1%}")
print(f"Percentage: {rate:.2%}")

# Binary, octal, hex
num = 42
print(f"\nBinary: {num:b}")
print(f"Octal: {num:o}")
print(f"Hex (lower): {num:x}")
print(f"Hex (upper): {num:X}")

# Scientific notation
big = 1234567890.123
print(f"Scientific: {big:e}")
print(f"Scientific (2 places): {big:.2e}")

# ============================================================
# Debug Format (Python 3.8+)
# ============================================================
# Example 3: f-string debug syntax
print("\n--- Debug Format ---")

x = 42
name = "Alice"

print(f"{x = }")        # x = 42
print(f"{name = }")     # name = 'Alice'
print(f"{x + 1 = }")    # x + 1 = 43
print(f"{x * 2 = }")    # x * 2 = 84

# ============================================================
# .format() Method
# ============================================================
# Example 4: Basic .format() usage
print("\n--- .format() Method ---")

# Positional arguments
print("Hello, {}! You are {} years old.".format("Alice", 30))

# Numbered arguments
print("{0} is {1}, and {0} is a name.".format("Alice", "female"))

# Named arguments
print("{name} is {age} years old.".format(name="Bob", age=25))

# Accessing attributes and items
person = {"name": "Charlie", "age": 35}
print("Name: {0[name]}, Age: {0[age]}".format(person))

# ============================================================
# .format() Formatting
# ============================================================
# Example 5: Formatting with .format()
print("\n--- .format() Formatting ---")

# Number formatting
pi = 3.14159
print("Pi = {:.2f}".format(pi))
print("Pi = {:.4f}".format(pi))

# Width and alignment
print("{:>10}".format("right"))
print("{:<10}".format("left"))
print("{:^10}".format("center"))
print("{:*^10}".format("center"))

# Number formatting
print("{:,}".format(1234567890))
print("{:.1%}".format(0.856))

# ============================================================
# % Operator (Old Style)
# ============================================================
# Example 6: printf-style formatting
print("\n--- % Operator ---")

# Basic usage
name = "Alice"
age = 30
print("Hello, %s! You are %d years old." % (name, age))

# Number formatting
pi = 3.14159
print("Pi = %.2f" % pi)
print("Pi = %.4f" % pi)

# Width
print("%10s" % "right")
print("%-10s" % "left")

# Dictionary
person = {"name": "Bob", "age": 25}
print("%(name)s is %(age)d years old." % person)

# Multiple values
print("Name: %s, Age: %d, Score: %.1f" % ("Charlie", 35, 95.5))

# ============================================================
# Template Strings
# ============================================================
# Example 7: Template strings (safe substitution)
print("\n--- Template Strings ---")

from string import Template

# Basic template
template = Template("Hello, $name! You are $age years old.")
result = template.substitute(name="Alice", age=30)
print(result)

# Safe substitution (no error for missing values)
template = Template("$name is $age years old.")
result = template.safe_substitute(name="Bob")
print(f"Safe sub: {result}")  # $age remains

# Using $$ for literal $
template = Template("Price: $$${price}")
result = template.substitute(price=19.99)
print(f"Price: {result}")

# ============================================================
# Comparison of Methods
# ============================================================
# Example 8: Same result, different methods
print("\n--- Comparison ---")

name = "Alice"
age = 30
score = 95.5

# f-string
print(f"f-string: {name} is {age} with score {score:.1f}")

# .format()
print("format(): {} is {} with score {:.1f}".format(name, age, score))

# % operator
print("%% operator: %s is %d with score %.1f" % (name, age, score))

# Template
t = Template("$name is $age with score $score")
print(f"Template: {t.substitute(name=name, age=age, score=f'{score:.1f}')}")

# ============================================================
# Multi-line f-strings
# ============================================================
# Example 9: Multi-line formatting
print("\n--- Multi-line f-strings ---")

name = "Alice"
age = 30
city = "New York"

# Using triple quotes
info = f"""
Name: {name}
Age: {age}
City: {city}
"""
print(info)

# Using backslash in f-string (Python 3.12+)
# In older versions, use variables
line1 = f"Name: {name}"
line2 = f"Age: {age}"
info = line1 + "\n" + line2
print(info)

# ============================================================
# Practical Examples
# ============================================================
# Example 10: Real-world formatting
print("\n--- Practical Examples ---")

# Currency formatting
price = 1234.56
print(f"Price: ${price:,.2f}")
print(f"Price: {price:,.2f} EUR")

# Table formatting
print("\n--- Table ---")
products = [
    ("Apple", 1.50, 10),
    ("Banana", 0.75, 25),
    ("Cherry", 3.00, 5),
]

print(f"{'Product':<10} {'Price':>8} {'Qty':>5} {'Total':>10}")
print("-" * 35)
for name, price, qty in products:
    total = price * qty
    print(f"{name:<10} ${price:>7.2f} {qty:>5} ${total:>9.2f}")

# Padding and truncation
text = "Hello, World!"
print(f"\nTruncated: {text:.5}")
print(f"Padded: {text:_>20}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. f-strings: f\"{variable}\" - most readable and Pythonic")
print("2. .format(): \"{}\".format(value) - flexible and powerful")
print("3. % operator: \"%s\" % value - old style, still works")
print("4. Template: Template(\"$\").safe_substitute() - safe for user input")
print("5. f-strings support expressions: f\"{2+2}\"")
print("6. Format specifiers: :.2f, :>, :<, :^, :, :b, :x, :%")
print("7. Debug format (3.8+): f\"{variable = }\"")
