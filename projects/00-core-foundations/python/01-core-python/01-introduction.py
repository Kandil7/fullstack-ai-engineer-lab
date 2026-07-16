"""
W3Schools Python Tutorial - 01: Introduction
=============================================
Topics: What Python is, print() function, case sensitivity

Run: python 01-introduction.py
Reference: https://www.w3schools.com/python/python_intro.asp
"""

# ============================================================
# What is Python?
# ============================================================
# Python is a popular programming language created by Guido van Rossum.
# It was released in 1991 and is used for:
#   - Web development (server-side)
#   - Software development
#   - Mathematics
#   - System scripting

# ============================================================
# Example 1: Hello, World! - The classic first program
# ============================================================
print("Hello, World!")
# Output: Hello, World!

# ============================================================
# Example 2: What can Python do?
# ============================================================
# Python can be used to create web applications, work with databases,
# read and modify files, handle big data, perform math/science,
# build prototypes, and automate tasks.

print("Python is versatile and beginner-friendly!")
# Output: Python is versatile and beginner-friendly!

# ============================================================
# Example 3: Python Syntax compared to other languages
# ============================================================
# Python uses new lines to complete a statement (no semicolons needed).
# Python uses indentation to define blocks (no curly braces).

if 5 > 2:
    print("Five is greater than two!")
# Output: Five is greater than two!

# ============================================================
# Example 4: Python is Case-Sensitive
# ============================================================
a = 4
A = 5  # This is a DIFFERENT variable from 'a'
print(f"a = {a}")   # Output: a = 4
print(f"A = {A}")   # Output: A = 5

# Variable names are case-sensitive
firstname = "John"
Firstname = "Jane"
print(f"{firstname} and {Firstname} are different variables")
# Output: John and Jane are different variables

# ============================================================
# Example 5: Python uses indentation, not braces
# ============================================================
# Unlike Java, C++, or JavaScript which use braces {} to define blocks,
# Python uses indentation (whitespace).

# WRONG (would cause IndentationError in Python):
# if 5 > 2:
# print("Five is greater than two!")  # This would fail!

# CORRECT:
if 5 > 2:
    print("Five is greater than two!")
    print("This line is also part of the if block.")

# Output:
# Five is greater than two!
# This line is also part of the if block.

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. Python is a powerful, beginner-friendly language")
print("2. print() is used to output text to the console")
print("3. Python is case-sensitive (myVar != MyVar != myvar)")
print("4. Python uses indentation instead of braces for code blocks")
print("5. Python statements end at the end of the line (no semicolons)")
