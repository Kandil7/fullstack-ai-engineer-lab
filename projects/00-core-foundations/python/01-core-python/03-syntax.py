"""
W3Schools Python Tutorial - 03: Python Syntax
===============================================
Topics: Indentation, comments, case sensitivity

Run: python 03-syntax.py
Reference: https://www.w3schools.com/python/python_syntax.asp
"""

# ============================================================
# Python Indentation
# ============================================================
# Python uses indentation to define code blocks (scopes).
# Most other languages use curly braces {} or keywords like 'begin/end'.
# Indentation is NOT optional in Python - it's required!

# Example 1: Indentation defines code blocks
if 10 > 5:
    print("10 is greater than 5")
    print("This is still inside the if block")
print("This is outside the if block")

# Output:
# 10 is greater than 5
# This is still inside the if block
# This is outside the if block

# ============================================================
# Example 2: Indentation in nested structures
# ============================================================
x = 10
y = 20

if x > 5:
    print("x is greater than 5")
    if y > 15:
        print("y is greater than 15")
        print("Both conditions are true")
    print("Back to the outer if block")

# Output:
# x is greater than 5
# y is greater than 15
# Both conditions are true
# Back to the outer if block

# ============================================================
# Example 3: Common indentation error
# ============================================================
# The standard is 4 spaces per indentation level.
# You can also use tabs, but NEVER mix them!

# This would cause an IndentationError:
# if 10 > 5:
#     print("correct")
#   print("wrong - different indentation")  # Error!

# Python is strict about consistent indentation.

# ============================================================
# Python Comments
# ============================================================
# Comments are used to explain code. Python ignores them.

# Example 4: Single-line comments
# This is a comment
x = 5  # This is also a comment (inline)

# Example 5: Multi-line comments using triple quotes
"""
This is a multi-line comment (actually a docstring).
It can span multiple lines.
Python treats triple-quoted strings as docstrings when placed
at the beginning of modules, functions, or classes.
"""
y = 10

# Example 6: Multi-line strings as comments
'''
Another way to write multi-line comments.
This is technically a string literal, not a true comment,
but it's commonly used for longer explanations.
'''

# ============================================================
# Python is Case-Sensitive
# ============================================================
# Example 7: Variable name cases matter
myVar = "lowercase"
MyVar = "Capitalized"
MYVAR = "ALL CAPS"

print(f"myVar = {myVar}")   # Output: myVar = lowercase
print(f"MyVar = {MyVar}")   # Output: MyVar = Capitalized
print(f"MYVAR = {MYVAR}")   # Output: MYVAR = ALL CAPS

# Function names are also case-sensitive
def my_function():
    return "lowercase function"

def My_Function():
    return "Capitalized function"

print(my_function())    # Output: lowercase function
print(My_Function())    # Output: Capitalized function

# ============================================================
# Python Naming Conventions (PEP 8)
# ============================================================
# - Variables and functions: snake_case (my_variable)
# - Classes: PascalCase (MyClass)
# - Constants: UPPER_SNAKE_CASE (MAX_SIZE)
# - Private: leading underscore (_private)

# Examples of valid variable names:
user_name = "Alice"
_user_id = 123
maxSize = 100
temp2 = 98.6

# Examples of INVALID variable names (would cause SyntaxError):
# 2names = "bad"       # Can't start with a number
# my-name = "bad"      # Hyphens not allowed
# my name = "bad"      # Spaces not allowed
# class = "bad"        # Reserved keyword

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Python uses INDENTATION (not braces) to define code blocks")
print("2. Standard indent is 4 spaces - never mix tabs and spaces!")
print("3. Single-line comments use: # this is a comment")
print("4. Multi-line comments use: ''' or \"\"\" triple quotes")
print("5. Python is case-sensitive: Var != var != VAR")
