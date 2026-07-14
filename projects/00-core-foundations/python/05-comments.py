"""
W3Schools Python Tutorial - 05: Python Comments
================================================
Topics: Single-line comments, multi-line comments, best practices

Run: python 05-comments.py
Reference: https://www.w3schools.com/python/python_comments.asp
"""

# ============================================================
# Single-Line Comments
# ============================================================
# Comments start with a hash character (#)
# Everything after # on that line is ignored by Python

# This is a comment
x = 5  # This is an inline comment

# Example 1: Using comments to explain code
# Calculate the area of a circle
radius = 7
pi = 3.14159
area = pi * radius ** 2
print(f"Area of circle with radius {radius}: {area:.2f}")
# Output: Area of circle with radius 7: 153.94

# Example 2: Using comments to prevent execution
# print("This line will NOT execute")
# x = 10
# y = 20
# print(x + y)

# ============================================================
# Multi-Line Comments
# ============================================================
# Python doesn't technically have multi-line comments,
# but you can use triple-quoted strings (''' or """)

# Example 3: Triple-quoted strings as comments
"""
This is a multi-line comment.
It can span multiple lines.
Python treats it as a string literal, but since it's not
assigned to anything, it's effectively ignored.
"""
x = 10  # This still runs fine

# Example 4: Using single triple quotes
'''
Another multi-line comment style.
Useful for longer explanations.
'''
y = 20

# ============================================================
# Docstrings (Special Multi-Line Comments)
# ============================================================
# Docstrings are special comments that describe what a
# module, function, or class does.

# Example 5: Function docstring
def calculate_bmi(weight_kg, height_m):
    """
    Calculate Body Mass Index (BMI).
    
    Parameters:
        weight_kg (float): Weight in kilograms
        height_m (float): Height in meters
    
    Returns:
        float: BMI value
    
    Example:
        >>> calculate_bmi(70, 1.75)
        22.86
    """
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

result = calculate_bmi(70, 1.75)
print(f"BMI: {result}")
# Output: BMI: 22.86

# Example 6: Class docstring
class Dog:
    """
    A simple Dog class to demonstrate class docstrings.
    
    Attributes:
        name (str): The name of the dog
        breed (str): The breed of the dog
    """
    
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
    
    def bark(self):
        """Return the dog's bark sound."""
        return f"{self.name} says Woof!"

dog = Dog("Rex", "Labrador")
print(dog.bark())
# Output: Rex says Woof!

# ============================================================
# Best Practices for Comments
# ============================================================

# DO: Comment WHY, not WHAT
# BAD: Increment counter by 1
counter = 0
counter += 1

# GOOD: Skip the first item because headers start at index 0
items = ["header", "item1", "item2"]
for i in range(1, len(items)):
    print(items[i])

# DO: Keep comments up to date
total_price = 100
discount = 10
final_price = total_price - discount
# Note: No tax applied for educational content
print(f"Final price: {final_price}")

# DON'T: State the obvious
# BAD:
x = 5  # This is a variable
name = "Alice"  # This is a string

# DO: Use comments to mark TODOs
# TODO: Add input validation for weight
# FIXME: Rounding precision needs improvement
# HACK: Temporary workaround for edge case

# ============================================================
# Commenting Out Code for Debugging
# ============================================================
# Example 7: Useful for debugging
debug_mode = True

# Temporary debug output
if debug_mode:
    print("[DEBUG] Variables:", {"x": x, "y": y})

# You can temporarily disable code by commenting it out:
# import pdb; pdb.set_trace()  # Debugger breakpoint

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Single-line comments use: # this is a comment")
print("2. Multi-line comments use: ''' or \"\"\" triple quotes")
print("3. Docstrings (''') describe modules, functions, and classes")
print("4. Best practice: Comment WHY, not WHAT")
print("5. Use TODO/FIXME to mark items needing attention")
