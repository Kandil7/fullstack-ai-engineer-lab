"""
W3Schools Python Tutorial - 25: Python Modules
===============================================
Topics: Importing, from import, math, random, datetime modules

Run: python 25-modules.py
Reference: https://www.w3schools.com/python/python_modules.asp
"""

# ============================================================
# What is a Module?
# ============================================================
# A module is a file containing Python code (functions, classes, variables).
# Modules help organize code and promote reuse.
# Python comes with many built-in modules.

# ============================================================
# Importing Modules
# ============================================================
# Example 1: Different ways to import

# Method 1: Import entire module
import math
print(f"pi = {math.pi}")
print(f"sqrt(144) = {math.sqrt(144)}")

# Method 2: Import with alias
import datetime as dt
today = dt.date.today()
print(f"\nToday: {today}")

# Method 3: Import specific items
from random import randint, choice
print(f"\nRandom int: {randint(1, 100)}")
print(f"Random choice: {choice(['a', 'b', 'c'])}")

# Method 4: Import all (NOT recommended - can cause naming conflicts)
# from math import *
# print(sqrt(144))  # Works, but unclear where sqrt comes from

# ============================================================
# The math Module
# ============================================================
# Example 2: Math module functions
import math

print("\n--- math Module ---")
print(f"pi = {math.pi}")
print(f"e = {math.e}")
print(f"inf = {math.inf}")
print(f"nan = {math.nan}")

# Rounding
print(f"\nceil(4.3) = {math.ceil(4.3)}")      # 5
print(f"floor(4.7) = {math.floor(4.7)}")     # 4
print(f"trunc(4.7) = {math.trunc(4.7)}")     # 4

# Power and logarithmic
print(f"\npow(2, 10) = {math.pow(2, 10)}")   # 1024.0
print(f"sqrt(144) = {math.sqrt(144)}")        # 12.0
print(f"log(100, 10) = {math.log(100, 10)}")  # 2.0
print(f"log2(8) = {math.log2(8)}")            # 3.0
print(f"log10(1000) = {math.log10(1000)}")    # 3.0

# Trigonometry
print(f"\nsin(pi/2) = {math.sin(math.pi/2)}")
print(f"cos(0) = {math.cos(0)}")
print(f"tan(pi/4) = {math.tan(math.pi/4)}")
print(f"degrees(pi) = {math.degrees(math.pi)}")
print(f"radians(180) = {math.radians(180)}")

# Combinatorics
print(f"\nfactorial(5) = {math.factorial(5)}")
print(f"gcd(48, 18) = {math.gcd(48, 18)}")

# ============================================================
# The random Module
# ============================================================
# Example 3: Random module functions
import random

print("\n--- random Module ---")
print(f"random() = {random.random()}")          # 0.0 to 1.0
print(f"randint(1, 10) = {random.randint(1, 10)}")  # 1 to 10
print(f"randrange(0, 10, 2) = {random.randrange(0, 10, 2)}")  # Even numbers 0-8
print(f"uniform(1.5, 6.5) = {random.uniform(1.5, 6.5):.2f}")  # Float in range

# Random choice
colors = ["red", "green", "blue", "yellow"]
print(f"\nchoice: {random.choice(colors)}")
print(f"choices (3): {random.choices(colors, k=3)}")

# Random sample (no duplicates)
print(f"sample (2): {random.sample(colors, k=2)}")

# Shuffle list
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(f"shuffled: {numbers}")

# Seed for reproducibility
random.seed(42)
print(f"\nSeeded random: {random.random()}")
random.seed(42)
print(f"Same seed: {random.random()}")  # Same value!

# ============================================================
# The datetime Module
# ============================================================
# Example 4: DateTime module
from datetime import datetime, date, time, timedelta

print("\n--- datetime Module ---")

# Current date and time
now = datetime.now()
print(f"Current datetime: {now}")
print(f"Year: {now.year}")
print(f"Month: {now.month}")
print(f"Day: {now.day}")
print(f"Hour: {now.hour}")
print(f"Minute: {now.minute}")

# Today's date
today = date.today()
print(f"\nToday: {today}")

# Formatting
print(f"Formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Day name: {now.strftime('%A')}")
print(f"Month name: {now.strftime('%B')}")

# Timedelta
print("\n--- timedelta ---")
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(weeks=1)
print(f"Tomorrow: {tomorrow}")
print(f"Next week: {next_week}")

# Age calculation
birthday = date(1990, 1, 1)
age = today - birthday
print(f"\nDays since {birthday}: {age.days}")
print(f"Years (approx): {age.days // 365}")

# ============================================================
# Creating Your Own Module
# ============================================================
# Example 5: You can create your own modules!
# Create a file called mymodule.py with:
#
# def greet(name):
#     return f"Hello, {name}!"
#
# PI = 3.14159
#
# Then import it:
# import mymodule
# print(mymodule.greet("Alice"))
# print(mymodule.PI)

# ============================================================
# The __name__ Variable
# ============================================================
# Example 6: Understanding __name__
print("\n--- __name__ Variable ---")
print(f"__name__ in this script: {__name__}")
# Output: __name__ in this script: __main__

# When you run a file directly, __name__ == "__main__"
# When imported, __name__ == the module name

# Common pattern:
if __name__ == "__main__":
    print("This code only runs when the file is executed directly!")
    print("Not when imported as a module.")

# ============================================================
# Useful Built-in Modules
# ============================================================
# Example 7: Quick overview of useful modules
print("\n--- Useful Modules ---")

# os - operating system interface
import os
print(f"Current dir: {os.getcwd()}")
print(f"List dir: {os.listdir('.')[:3]}...")

# sys - system parameters
import sys
print(f"Python version: {sys.version_info[:2]}")
print(f"Platform: {sys.platform}")

# json - JSON handling
import json
data = {"name": "Alice", "age": 30}
json_str = json.dumps(data)
print(f"JSON: {json_str}")

# collections - specialized containers
from collections import Counter, defaultdict
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
print(f"Counter: {Counter(words)}")

# itertools - iterator utilities
import itertools
print(f"Chain: {list(itertools.chain([1, 2], [3, 4]))}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. import module: import entire module")
print("2. from module import func: import specific items")
print("3. import module as alias: use short name")
print("4. math: mathematical functions (sqrt, ceil, floor, etc.)")
print("5. random: random number generation")
print("6. datetime: date and time handling")
print("7. Create modules: save code in .py files")
print("8. __name__ == '__main__': code that runs only when executed")
