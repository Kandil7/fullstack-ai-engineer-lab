"""
W3Schools Python Tutorial - 04: Python Output
==============================================
Topics: print() function, multiple values, separator, end parameter

Run: python 04-output.py
Reference: https://www.w3schools.com/python/python_strings_insert.asp
"""

# ============================================================
# The print() Function
# ============================================================
# The print() function outputs text to the screen/console.

# Example 1: Basic print
print("Hello, World!")
# Output: Hello, World!

# Example 2: Printing numbers
print(42)
print(3.14159)
# Output:
# 42
# 3.14159

# Example 3: Printing expressions
print(5 + 3)
print("5 + 3 =", 5 + 3)
# Output:
# 8
# 5 + 3 = 8

# ============================================================
# Printing Multiple Values
# ============================================================
# Example 4: Multiple arguments are separated by spaces by default
print("Name:", "Alice", "Age:", 30)
# Output: Name: Alice Age: 30

# Example 5: Mixing strings and numbers
x = 10
y = 20
print("The sum of", x, "and", y, "is", x + y)
# Output: The sum of 10 and 20 is 30

# ============================================================
# The sep Parameter (Separator)
# ============================================================
# Example 6: Custom separator
print("Apple", "Banana", "Cherry", sep=", ")
# Output: Apple, Banana, Cherry

print("2024", "01", "15", sep="-")
# Output: 2024-01-15

print("one", "two", "three", sep=" | ")
# Output: one | two | three

# Example 7: No separator
print("Hello", "World", sep="")
# Output: HelloWorld

# ============================================================
# The end Parameter
# ============================================================
# Example 8: Default end is newline '\n'
print("Line 1")
print("Line 2")
# Output:
# Line 1
# Line 2

# Example 9: Custom end parameter
print("Hello", end=" ")
print("World")
# Output: Hello World

# Example 10: Building output on the same line
for i in range(5):
    print(i, end=" ")
print()  # Final newline
# Output: 0 1 2 3 4

# ============================================================
# Printing Special Characters
# ============================================================
# Example 11: Escape characters
print("Line1\nLine2")        # \n = newline
print("Column1\tColumn2")    # \t = tab
print("She said \"hello\"")  # \" = double quote
print('It\'s a day')         # \' = single quote
print("Backslash: \\")       # \\ = backslash

# Output:
# Line1
# Line2
# Column1	Column2
# She said "hello"
# It's a day
# Backslash: \

# ============================================================
# Printing with f-strings (Python 3.6+)
# ============================================================
# Example 12: f-strings for formatted output
name = "Bob"
age = 25
print(f"My name is {name} and I am {age} years old.")
# Output: My name is Bob and I am 25 years old.

# Example 13: Expressions in f-strings
print(f"10 + 5 = {10 + 5}")
print(f"Uppercase: {'hello'.upper()}")
# Output:
# 10 + 5 = 15
# Uppercase: HELLO

# ============================================================
# Print without newline (joining)
# ============================================================
# Example 14: Using join to print list items
fruits = ["apple", "banana", "cherry"]
print(", ".join(fruits))
# Output: apple, banana, cherry

# Example 15: Print with flush (useful for progress)
import time
for i in range(3):
    print(".", end="", flush=True)
    time.sleep(0.3)
print(" Done!")
# Output: ... Done!

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. print() outputs text to the console")
print("2. Multiple values are separated by spaces by default")
print("3. sep parameter changes the separator (default: ' ')")
print("4. end parameter changes the ending (default: '\\n')")
print("5. f-strings provide the cleanest way to format output")
