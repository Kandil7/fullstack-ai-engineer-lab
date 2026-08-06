"""
W3Schools Python Tutorial - 10: Python Strings
===============================================
Topics: String literals, accessing, slicing, methods, f-strings

Run: python 10-strings.py
Reference: https://www.w3schools.com/python/python_strings.asp
"""

# ============================================================
# String Literals
# ============================================================
# Example 1: Different ways to create strings
s1 = "Hello, World!"
s2 = 'Hello, World!'
s3 = """This is
a multi-line
string"""
s4 = '''Another
multi-line
string'''

print(s1)
print(s3)
# Output:
# Hello, World!
# This is
# a multi-line
# string

# Escape characters
print("She said \"hello\"")   # \" = double quote
print('It\'s a day')          # \' = single quote
print("Line1\nLine2")         # \n = newline
print("Col1\tCol2")           # \t = tab
print("Backslash: \\")        # \\ = backslash

# Raw strings (ignore escape characters)
print(r"C:\new\folder")       # Output: C:\new\folder
print(R"Also raw \n string")  # Output: Also raw \n string

# ============================================================
# Accessing Characters
# ============================================================
# Example 2: String indexing (0-based)
text = "Hello, Python!"
print(f"\nText: {text}")
print(f"First char: {text[0]}")    # Output: H
print(f"Second char: {text[1]}")   # Output: e
print(f"Last char: {text[-1]}")    # Output: !
print(f"Second to last: {text[-2]}")  # Output: n

# Strings are IMMUTABLE
# text[0] = "h"  # TypeError: 'str' object does not support item assignment

# ============================================================
# Slicing
# ============================================================
# Example 3: String slicing [start:stop:step]
text = "Hello, World!"
print(f"\nFull string: {text}")
print(f"First 5: {text[0:5]}")     # Output: Hello
print(f"From index 7: {text[7:]}")  # Output: World!
print(f"To index 5: {text[:5]}")    # Output: Hello
print(f"Skip every 2: {text[::2]}")  # Output: Hlo ol!
print(f"Reverse: {text[::-1]}")     # Output: !dlroW ,olleH

# Negative slicing
print(f"Last 6 chars: {text[-6:]}")  # Output:orld!

# ============================================================
# String Methods
# ============================================================
# Example 4: Common string methods
text = "  Hello, World!  "

print(f"\nOriginal: '{text}'")
print(f"upper(): '{text.upper()}'")         # HELLO, WORLD!
print(f"lower(): '{text.lower()}'")         # hello, world!
print(f"strip(): '{text.strip()}'")         # Hello, World!
print(f"lstrip(): '{text.lstrip()}'")       # Hello, World!  
print(f"rstrip(): '{text.rstrip()}'")       #   Hello, World!
print(f"title(): '{text.strip().title()}'") # Hello, World!
print(f"capitalize(): '{text.strip().capitalize()}'")  # Hello, world!
print(f"swapcase(): '{text.strip().swapcase()}'")  # hELLO, wORLD!

# ============================================================
# Search and Replace Methods
# ============================================================
# Example 5: Finding and replacing
text = "Hello, World! Hello, Python!"

print(f"\nOriginal: {text}")
print(f"find('Hello'): {text.find('Hello')}")      # 0
print(f"find('Hello', 5): {text.find('Hello', 5)}") # 14
print(f"rfind('Hello'): {text.rfind('Hello')}")     # 14
print(f"index('World'): {text.index('World')}")     # 7
print(f"count('Hello'): {text.count('Hello')}")     # 2

# Replace
new_text = text.replace("Hello", "Hi")
print(f"replace: {new_text}")  # Hi, World! Hi, Python!

# Startswith / Endswith
print(f"startswith('Hello'): {text.startswith('Hello')}")  # True
print(f"endswith('Python!'): {text.endswith('Python!')}")  # True

# ============================================================
# Split and Join
# ============================================================
# Example 6: Splitting and joining strings
sentence = "Python is awesome and fun"
words = sentence.split()
print(f"\nsplit(): {words}")
# Output: ['Python', 'is', 'awesome', 'and', 'fun']

csv_data = "apple,banana,cherry"
fruits = csv_data.split(",")
print(f"split(','): {fruits}")
# Output: ['apple', 'banana', 'cherry']

# Join
joined = " - ".join(words)
print(f"join(): {joined}")
# Output: Python - is - awesome - and - fun

joined = ", ".join(fruits)
print(f"join(): {joined}")
# Output: apple, banana, cherry

# ============================================================
# String Testing Methods
# ============================================================
# Example 7: Boolean string methods
print("\n--- String Testing ---")
tests = [
    ("Hello123", "isalnum"),   # Alphanumeric
    ("Hello", "isalpha"),      # Alphabetical
    ("12345", "isdigit"),      # Digits
    ("  ", "isspace"),         # Whitespace
    ("hello", "islower"),      # All lowercase
    ("HELLO", "isupper"),      # All uppercase
]

for s, method in tests:
    result = getattr(s, method)()
    print(f"'{s}'.{method}() = {result}")

# Output:
# 'Hello123'.isalnum() = True
# 'Hello'.isalpha() = True
# '12345'.isdigit() = True
# '  '.isspace() = True
# 'hello'.islower() = True
# 'HELLO'.isupper() = True

# ============================================================
# String Concatenation
# ============================================================
# Example 8: Different ways to concatenate strings
first = "Hello"
second = "World"

# Method 1: + operator
result = first + " " + second
print(f"\nConcatenation: {result}")

# Method 2: join()
result = " ".join([first, second])
print(f"join(): {result}")

# Method 3: f-string
result = f"{first} {second}"
print(f"f-string: {result}")

# Method 4: format()
result = "{} {}".format(first, second)
print(f"format(): {result}")

# Method 5: * operator (repetition)
result = "Ha" * 3
print(f"Repetition: {result}")  # HaHaHa

# ============================================================
# f-strings (Formatted String Literals)
# ============================================================
# Example 9: f-string formatting
name = "Alice"
age = 30
pi = 3.14159

print(f"\n--- f-string Examples ---")
print(f"Name: {name}, Age: {age}")
print(f"Pi rounded: {pi:.2f}")
print(f"Left aligned: {'hello':<20}")
print(f"Right aligned: {'hello':>20}")
print(f"Centered: {'hello':^20}")
print(f"Zero-padded: {42:05d}")
print(f"With comma: {1000000:,}")
print(f"Percentage: {0.856:.1%}")
print(f"Binary: {42:b}")
print(f"Hex: {255:x}")
print(f"Octal: {42:o}")
print(f"Expression: {2 + 3 = }")  # Python 3.8+ debug format

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Strings are created with ' or \" (single or double quotes)")
print("2. Strings are IMMUTABLE - can't change individual characters")
print("3. Access characters with text[index] (0-based)")
print("4. Slice with text[start:stop:step]")
print("5. Methods: upper, lower, strip, split, replace, find, count")
print("6. f-strings (f\"...\") are the modern way to format strings")
