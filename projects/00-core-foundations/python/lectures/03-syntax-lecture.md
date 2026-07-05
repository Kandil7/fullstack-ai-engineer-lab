# Python Syntax Fundamentals - Lecture Notes

## 1. Topic Overview
This lecture covers Python's syntax rules, including indentation, statements, and the fundamental structure of Python code. Python's syntax is designed for readability, making it one of the cleanest languages to write and understand.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Understand Python's indentation rules
- Write proper Python statements and expressions
- Use line continuation and multi-line statements
- Understand Python's naming conventions
- Write syntactically correct Python code

## 3. Key Concepts

### 3.1 Indentation
Python uses **indentation** instead of braces `{}` to define code blocks. This is Python's most distinctive syntax feature.

**Standard indentation:** 4 spaces (recommended by PEP 8)

```python
# Correct indentation
if True:
    print("Indented block")
    print("Still in block")
print("Outside block")
```

**Common indentation mistakes:**
```python
# Wrong - mixing tabs and spaces
if True:
	print("Tab")  # 1 tab
    print("Space")  # 4 spaces - IndentationError!

# Wrong - inconsistent indentation
if True:
    print("4 spaces")
        print("8 spaces") - IndentationError!

# Correct - consistent 4 spaces
if True:
    print("4 spaces")
    print("Still 4 spaces")
```

### 3.2 Statements and Expressions

**Statement**: An instruction that Python can execute
```python
# Assignment statement
x = 10

# Print statement
print("Hello")

# Conditional statement
if x > 5:
    print("Greater than 5")
```

**Expression**: A combination of values and operators that produces a result
```python
# Expressions
2 + 3          # Arithmetic expression
"Hello" * 3    # String expression
x > 5          # Comparison expression
True and False # Boolean expression
```

### 3.3 Line Structure

**One statement per line (recommended):**
```python
# Recommended
x = 10
y = 20
print(x + y)
```

**Multiple statements per line (use semicolons):**
```python
# Allowed but not recommended
x = 10; y = 20; print(x + y)
```

### 3.4 Line Continuation

**Implicit continuation (inside brackets):**
```python
# Inside parentheses, brackets, or braces
total = (10 +
         20 +
         30)

numbers = [1,
           2,
           3,
           4]

person = {"name": "Alice",
          "age": 25}
```

**Explicit continuation (backslash):**
```python
# Using backslash
total = 10 + \
        20 + \
        30

# Better to use parentheses instead
total = (10 +
         20 +
         30)
```

### 3.5 Comments

**Single-line comments:**
```python
# This is a comment
x = 10  # Inline comment
```

**Multi-line comments (using triple quotes):
```python
"""
This is a multi-line
comment block
"""
x = 10
```

### 3.6 Naming Conventions (PEP 8)

**Variables and functions:**
```python
# Use snake_case
user_name = "Alice"
def calculate_total():
    pass
```

**Classes:**
```python
# Use PascalCase
class UserAccount:
    pass
```

**Constants:**
```python
# Use UPPER_SNAKE_CASE
MAX_CONNECTIONS = 100
PI = 3.14159
```

## 4. Code Examples

### Example 1: Basic Program Structure
```python
# Program structure example
def main():
    """Main function"""
    # Variable assignment
    name = "Alice"
    age = 25
    
    # Conditional
    if age >= 18:
        print(f"{name} is an adult")
    else:
        print(f"{name} is a minor")
    
    # Loop
    for i in range(3):
        print(f"Count: {i}")

# Entry point
if __name__ == "__main__":
    main()
```

### Example 2: Indentation Practice
```python
# Nested indentation
def process_data(data):
    """Process data with nested structures"""
    if data:
        for item in data:
            if item > 0:
                print(f"Positive: {item}")
                if item > 10:
                    print(f"  Large: {item}")
            else:
                print(f"Non-positive: {item}")
    else:
        print("No data")
```

### Example 3: Line Continuation
```python
# Multiple ways to continue lines
result = (10 + 20 + 30 + 
          40 + 50)

# Function call continuation
very_long_function_name(
    argument1,
    argument2,
    argument3
)

# Dictionary continuation
config = {
    "host": "localhost",
    "port": 8080,
    "debug": True
}
```

### Example 4: Naming Conventions
```python
# Variables (snake_case)
user_name = "Alice"
is_active = True

# Functions (snake_case)
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# Classes (PascalCase)
class UserAccount:
    def __init__(self, name):
        self.name = name

# Constants (UPPER_SNAKE_CASE)
MAX_RETRY_ATTEMPTS = 3
API_VERSION = "2.0"
```

## 5. Common Mistakes to Avoid

### Mistake 1: Inconsistent Indentation
```python
# Wrong - mixing indentation
if True:
    print("4 spaces")
	print("Tab")  # IndentationError!

# Correct - consistent indentation
if True:
    print("4 spaces")
    print("4 spaces")
```

### Mistake 2: Missing Colon
```python
# Wrong - missing colon
if x > 5
    print("Greater")

# Correct - colon required
if x > 5:
    print("Greater")
```

### Mistake 3: Case Sensitivity
```python
# Wrong - Python is case-sensitive
Name = "Alice"
print(name)  # NameError: name 'name' is not defined

# Correct - consistent casing
name = "Alice"
print(name)  # Works
```

### Mistake 4: Using Reserved Words
```python
# Wrong - using reserved words as variables
class = "Math"  # SyntaxError!
for = 5         # SyntaxError!

# Correct - use descriptive names
subject = "Math"
count = 5
```

## 6. Best Practices

1. **Always use 4 spaces** for indentation (never tabs)
2. **One statement per line** for readability
3. **Use parentheses** for line continuation instead of backslashes
4. **Follow PEP 8** naming conventions
5. **Add comments** for complex logic
6. **Use blank lines** to separate logical sections

## 7. Practice Exercises

### Exercise 1: Indentation Practice
Write a program that demonstrates proper indentation with nested `if` statements.

### Exercise 2: Naming Conventions
Create variables, functions, and a class following PEP 8 naming conventions.

### Exercise 3: Line Continuation
Write a long mathematical expression using line continuation.

## 8. Summary

**Key takeaways:**
- Python uses indentation instead of braces
- Standard indentation is 4 spaces
- Statements are instructions, expressions produce values
- Follow PEP 8 naming conventions
- Use parentheses for line continuation
- Python is case-sensitive

**Next Lecture:** We'll learn about output and the `print()` function.

---

**Quick Reference:**
- PEP 8 Style Guide: https://peps.python.org/pep-0008/
- Python Tutorial: https://docs.python.org/3/tutorial/
- Indentation in Python: https://docs.python.org/3/reference/lexical_analysis.html#indentation