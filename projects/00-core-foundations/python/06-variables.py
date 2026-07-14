"""
W3Schools Python Tutorial - 06: Python Variables
=================================================
Topics: Creating variables, naming rules, multiple assignments, scope

Run: python 06-variables.py
Reference: https://www.w3schools.com/python/python_variables.asp
"""

# ============================================================
# Creating Variables
# ============================================================
# Variables are containers for storing data values.
# In Python, you don't need to declare the type - it's inferred.

# Example 1: Basic variable assignment
x = 5           # integer
y = "Hello"     # string
z = 3.14        # float
is_active = True  # boolean

print(f"x = {x}, type: {type(x).__name__}")
print(f"y = {y}, type: {type(y).__name__}")
print(f"z = {z}, type: {type(z).__name__}")
print(f"is_active = {is_active}, type: {type(is_active).__name__}")

# Output:
# x = 5, type: int
# y = Hello, type: str
# z = 3.14, type: float
# is_active = True, type: bool

# ============================================================
# Variable Naming Rules
# ============================================================
# Valid names:
my_var = 1          # snake_case (recommended)
_private = 2        # leading underscore
myVar2 = 3          # camelCase (not recommended but valid)
MAX_SIZE = 100      # UPPER_CASE for constants

# Invalid names (would cause SyntaxError):
# 2names = "bad"     # Can't start with number
# my-var = "bad"     # Hyphens not allowed
# my var = "bad"     # Spaces not allowed
# class = "bad"      # Reserved keyword

# Python keywords (cannot be used as variable names):
import keyword
print(f"\nPython has {len(keyword.kwlist)} reserved keywords")
print(f"Examples: {keyword.kwlist[:5]}...")

# ============================================================
# Assign Multiple Values
# ============================================================
# Example 2: Multiple assignment techniques

# Method 1: Multiple variables on one line
a, b, c = 1, 2, 3
print(f"\na={a}, b={b}, c={c}")  # Output: a=1, b=2, c=3

# Method 2: Same value to multiple variables
x = y = z = "same"
print(f"x={x}, y={y}, z={z}")  # Output: x=same, y=same, z=same

# Method 3: Unpacking a list or tuple
coordinates = [10, 20, 30]
x, y, z = coordinates
print(f"Coordinates: x={x}, y={y}, z={z}")
# Output: Coordinates: x=10, y=20, z=30

# Method 4: Unpacking with *
first, *rest = [1, 2, 3, 4, 5]
print(f"First: {first}, Rest: {rest}")
# Output: First: 1, Rest: [2, 3, 4, 5]

# ============================================================
# Output Variables
# ============================================================
# Example 3: Different ways to output variables

name = "Alice"
age = 30

# String concatenation (not recommended for mixed types)
print("Name: " + name + ", Age: " + str(age))

# Comma-separated (auto space)
print("Name:", name, "Age:", age)

# f-string (recommended)
print(f"Name: {name}, Age: {age}")

# .format() method
print("Name: {}, Age: {}".format(name, age))

# Output:
# Name: Alice, Age: 30
# Name: Alice Age: 30
# Name: Alice, Age: 30
# Name: Alice, Age: 30

# ============================================================
# Variable Reassignment
# ============================================================
# Example 4: Variables can change type
x = 10
print(f"\nx = {x}, type: {type(x).__name__}")
# Output: x = 10, type: int

x = "Now a string"
print(f"x = {x}, type: {type(x).__name__}")
# Output: x = Now a string, type: str

x = [1, 2, 3]
print(f"x = {x}, type: {type(x).__name__}")
# Output: x = [1, 2, 3], type: list

# ============================================================
# Global vs Local Variables
# ============================================================
# Example 5: Variable scope

global_var = "I am global"

def my_function():
    local_var = "I am local"
    print(f"Inside function: {global_var}")
    print(f"Inside function: {local_var}")

my_function()
print(f"Outside function: {global_var}")
# print(local_var)  # This would cause NameError!

# Output:
# Inside function: I am global
# Inside function: I am local
# Outside function: I am global

# Example 6: Using 'global' keyword
counter = 0

def increment():
    global counter
    counter += 1
    return counter

print(f"\nCounter: {increment()}")  # Output: Counter: 1
print(f"Counter: {increment()}")    # Output: Counter: 2
print(f"Counter: {increment()}")    # Output: Counter: 3

# ============================================================
# Deleting Variables
# ============================================================
# Example 7: Remove a variable
temp = "temporary"
print(f"\nBefore delete: {temp}")
del temp
# print(temp)  # Would cause NameError: name 'temp' is not defined
print("After delete: temp is removed")

# ============================================================
# Type of Variables
# ============================================================
# Example 8: Check variable types
name = "Alice"
age = 25
height = 5.7
is_student = True
grades = [90, 85, 92]
person = {"name": "Alice", "age": 25}

print(f"\n{name} is {type(name).__name__}")
print(f"{age} is {type(age).__name__}")
print(f"{height} is {type(height).__name__}")
print(f"{is_student} is {type(is_student).__name__}")
print(f"{grades} is {type(grades).__name__}")
print(f"{person} is {type(person).__name__}")

# Output:
# Alice is str
# 25 is int
# 5.7 is float
# True is bool
# [90, 85, 92] is list
# {'name': 'Alice', 'age': 25} is dict

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Variables are created when you assign a value")
print("2. No need to declare type - Python infers it")
print("3. Variable names: letters, numbers, underscores (no start with number)")
print("4. Use f-strings for clean variable output")
print("5. 'global' keyword lets you modify global variables inside functions")
print("6. 'del' keyword removes a variable")
