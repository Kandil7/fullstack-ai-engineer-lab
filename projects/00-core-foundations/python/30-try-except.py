"""
W3Schools Python Tutorial - 30: Python Try Except
==================================================
Topics: try/except, else, finally, raising exceptions, exception types

Run: python 30-try-except.py
Reference: https://www.w3schools.com/python/python_try_except.asp
"""

# ============================================================
# What are Exceptions?
# ============================================================
# Exceptions are errors that occur during program execution.
# Python uses try/except to handle these errors gracefully.

# ============================================================
# Basic try/except
# ============================================================
# Example 1: Handling a ZeroDivisionError
print("--- Basic try/except ---")

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Output: Cannot divide by zero!

# ============================================================
# Handling Multiple Exceptions
# ============================================================
# Example 2: Different exception types
print("\n--- Multiple Exceptions ---")

def divide_numbers(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print(f"Error: Cannot divide {a} by zero!")
    except TypeError:
        print(f"Error: Invalid types for division!")
    else:
        print(f"{a} / {b} = {result}")
    finally:
        print("Operation completed.")

divide_numbers(10, 2)    # Works
divide_numbers(10, 0)    # ZeroDivisionError
divide_numbers("10", 2)  # TypeError

# Output:
# 10 / 2 = 5.0
# Operation completed.
# Error: Cannot divide 10 by zero!
# Operation completed.
# Error: Invalid types for division!
# Operation completed.

# ============================================================
# The else Clause
# ============================================================
# Example 3: Code that runs only if no exception occurs
print("\n--- else Clause ---")

try:
    number = int("42")
except ValueError:
    print("Could not convert to integer!")
else:
    print(f"Successfully converted: {number}")
    # Code here runs only if try succeeded

# Output: Successfully converted: 42

# ============================================================
# The finally Clause
# ============================================================
# Example 4: Code that always runs
print("\n--- finally Clause ---")

def read_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File '{filename}' not found!")
    finally:
        print("Cleanup: File operation attempted.")

read_file("nonexistent.txt")

# Output:
# File 'nonexistent.txt' not found!
# Cleanup: File operation attempted.

# ============================================================
# Raising Exceptions
# ============================================================
# Example 5: Manually raising exceptions
print("\n--- Raising Exceptions ---")

def set_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer!")
    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150!")
    return age

# Test valid age
try:
    age = set_age(25)
    print(f"Age set to: {age}")
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

# Test invalid age
try:
    age = set_age(-5)
    print(f"Age set to: {age}")
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

# Test wrong type
try:
    age = set_age("twenty-five")
    print(f"Age set to: {age}")
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

# Output:
# Age set to: 25
# Error: Age must be between 0 and 150!
# Error: Age must be an integer!

# ============================================================
# Common Exception Types
# ============================================================
# Example 6: Different exception types
print("\n--- Common Exceptions ---")

# SyntaxError (can't catch - happens at parse time)
# if True  # SyntaxError

# ValueError
try:
    int("hello")
except ValueError as e:
    print(f"ValueError: {e}")

# TypeError
try:
    "hello" + 42
except TypeError as e:
    print(f"TypeError: {e}")

# IndexError
try:
    [1, 2, 3][10]
except IndexError as e:
    print(f"IndexError: {e}")

# KeyError
try:
    {"name": "Alice"}["age"]
except KeyError as e:
    print(f"KeyError: {e}")

# AttributeError
try:
    "hello".nonexistent_method()
except AttributeError as e:
    print(f"AttributeError: {e}")

# FileNotFoundError
try:
    open("nonexistent.txt")
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")

# ImportError
try:
    import nonexistent_module
except ImportError as e:
    print(f"ImportError: {e}")

# Output:
# ValueError: invalid literal for int() with base 10: 'hello'
# TypeError: can only concatenate str (not "int") to str
# IndexError: list index out of range
# KeyError: 'age'
# AttributeError: 'str' object has no attribute 'nonexistent_method'
# FileNotFoundError: [Errno 2] No such file or directory: 'nonexistent.txt'
# ImportError: No module named 'nonexistent_module'

# ============================================================
# Catching Multiple Exceptions
# ============================================================
# Example 7: Different ways to catch multiple exceptions
print("\n--- Catching Multiple ---")

# Method 1: Tuple of exceptions
try:
    value = int("hello")
except (ValueError, TypeError) as e:
    print(f"Catched: {type(e).__name__}: {e}")

# Method 2: Multiple except blocks
try:
    result = 10 / "2"
except ZeroDivisionError:
    print("Division by zero!")
except TypeError as e:
    print(f"Type error: {e}")

# ============================================================
# Exception Chaining
# ============================================================
# Example 8: Chaining exceptions
print("\n--- Exception Chaining ---")

def process_data(data):
    try:
        value = int(data)
    except ValueError as e:
        raise RuntimeError("Failed to process data") from e

try:
    process_data("not a number")
except RuntimeError as e:
    print(f"RuntimeError: {e}")
    print(f"Original cause: {e.__cause__}")

# ============================================================
# Practical Examples
# ============================================================
# Example 9: Real-world error handling
print("\n--- Practical Examples ---")

# Safe division
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    except TypeError:
        return None

print(f"10 / 3 = {safe_divide(10, 3)}")
print(f"10 / 0 = {safe_divide(10, 0)}")
print(f"'10' / 3 = {safe_divide('10', 3)}")

# Safe dictionary access
def safe_get(d, key, default=None):
    try:
        return d[key]
    except (KeyError, TypeError):
        return default

data = {"name": "Alice", "age": 30}
print(f"\nName: {safe_get(data, 'name')}")
print(f"Phone: {safe_get(data, 'phone', 'N/A')}")

# Input validation loop
def get_valid_number(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(f"{prompt}: "))
            if min_val is not None and value < min_val:
                print(f"Must be >= {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Must be <= {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number!")

# Uncomment to test interactively:
# age = get_valid_number("Enter your age", 0, 150)
# print(f"Your age: {age}")

# ============================================================
# Custom Exceptions
# ============================================================
# Example 10: Creating custom exceptions
print("\n--- Custom Exceptions ---")

class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Cannot withdraw ${amount}. Balance: ${balance}")

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance

account = BankAccount(100)

try:
    account.withdraw(50)
    print(f"After withdrawal: ${account.balance}")
    account.withdraw(75)  # Will raise exception
except InsufficientFundsError as e:
    print(f"Error: {e}")

# Output:
# After withdrawal: $50
# Error: Cannot withdraw $75. Balance: $50

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. try/except: catch and handle exceptions")
print("2. else: runs if no exception occurred")
print("3. finally: always runs (cleanup code)")
print("4. raise: manually throw an exception")
print("5. except Type as e: catch specific exception with variable")
print("6. Common exceptions: ValueError, TypeError, IndexError, KeyError")
print("7. Custom exceptions: inherit from Exception class")
print("8. Best practice: catch specific exceptions, not all!")
