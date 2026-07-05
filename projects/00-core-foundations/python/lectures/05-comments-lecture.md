# Python Comments - Lecture Notes

## 1. Topic Overview
This lecture covers Python comments and documentation. Comments are essential for making code readable and maintainable. We'll explore different types of comments, docstrings, and best practices for documenting Python code.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Write single-line and multi-line comments
- Use docstrings effectively
- Understand when and how to comment code
- Follow PEP 8 comment guidelines
- Write documentation strings for modules, classes, and functions

## 3. Key Concepts

### 3.1 Single-Line Comments
Single-line comments start with `#` and extend to the end of the line.

```python
# This is a comment
x = 10  # This is an inline comment

# Multiple single-line comments
# Line 1
# Line 2
# Line 3
```

### 3.2 Multi-Line Comments
Python doesn't have a specific multi-line comment syntax, but there are two common approaches:

**Triple-quoted strings (docstrings):**
```python
"""
This is a multi-line
comment using docstrings
"""
```

**Multiple # comments:**
```python
# Line 1
# Line 2
# Line 3
```

### 3.3 Docstrings
Docstrings are string literals as the first statement in modules, classes, or functions.

```python
def greet(name):
    """Greet a person by name."""
    return f"Hello, {name}!"

class User:
    """A class to represent a user."""
    
    def __init__(self, name, age):
        """Initialize user with name and age."""
        self.name = name
        self.age = age
```

### 3.4 When to Comment

**Good times to comment:**
- Explaining complex logic
- Clarifying non-obvious code
- Documenting algorithms
- Noting workarounds or limitations
- Explaining business rules

**Bad times to comment:**
- Restating what code does
- Commenting obvious code
- Leaving outdated comments
- Commenting out code (use version control)

### 3.5 PEP 8 Comment Guidelines

**Block comments:**
```python
# Block comments explain a section of code.
# They should start with # and a single space.
# Each line should start with # and a single space.
# They should be separated from code by a blank line.
```

**Inline comments:**
```python
x = 10  # Inline comment (2+ spaces before #)
```

**Docstrings:**
```python
"""Summary line.

Extended description.

Args:
    param1: Description of param1.
    param2: Description of param2.

Returns:
    Description of return value.

Raises:
    ValueError: Description of when ValueError is raised.
"""
```

## 4. Code Examples

### Example 1: Basic Comments
```python
# Calculate the area of a rectangle
def calculate_area(length, width):
    """Calculate and return the area of a rectangle."""
    # Multiply length by width
    area = length * width
    return area

# Example usage
result = calculate_area(5, 3)
print(f"Area: {result}")  # Output: Area: 15
```

### Example 2: Docstrings
```python
def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers (list): A list of numerical values.
    
    Returns:
        float: The average of the numbers.
    
    Raises:
        ValueError: If the list is empty.
        TypeError: If input is not a list.
    
    Example:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0
    """
    if not numbers:
        raise ValueError("List cannot be empty")
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    
    return sum(numbers) / len(numbers)
```

### Example 3: Module Documentation
```python
"""
calculator.py - A simple calculator module.

This module provides basic arithmetic operations
for educational purposes.

Author: Your Name
Date: 2024
Version: 1.0
"""

def add(a, b):
    """Return the sum of a and b."""
    return a + b

def subtract(a, b):
    """Return the difference of a and b."""
    return a - b
```

### Example 4: Class Documentation
```python
class BankAccount:
    """
    A class to represent a bank account.
    
    Attributes:
        owner (str): The name of the account owner.
        balance (float): The current balance.
    
    Methods:
        deposit(amount): Add money to the account.
        withdraw(amount): Remove money from the account.
        get_balance(): Return the current balance.
    
    Example:
        >>> account = BankAccount("Alice", 1000)
        >>> account.deposit(500)
        >>> account.get_balance()
        1500
    """
    
    def __init__(self, owner, balance=0):
        """Initialize the bank account."""
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        """Add money to the account."""
        self.balance += amount
    
    def withdraw(self, amount):
        """Remove money from the account."""
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    
    def get_balance(self):
        """Return the current balance."""
        return self.balance
```

## 5. Common Mistakes to Avoid

### Mistake 1: Commenting Obvious Code
```python
# Bad - comments that restate the code
x = 10  # Set x to 10
y = 20  # Set y to 20
sum_result = x + y  # Add x and y

# Good - comments that explain why
x = 10  # Initial value from config
y = 20  # Default multiplier
sum_result = x + y  # Calculate base total
```

### Mistake 2: Outdated Comments
```python
# Bad - outdated comment
# Calculate tax at 5%
tax = amount * 0.08  # Tax is actually 8% now!

# Good - accurate comment
# Calculate tax at 8% (updated 2024)
tax = amount * 0.08
```

### Mistake 3: Commenting Out Code
```python
# Bad - commented out code
# def old_function():
#     pass

# def new_function():
#     pass

# Good - use version control
def new_function():
    pass
```

### Mistake 4: Too Many Comments
```python
# Bad - over-commenting
# This function adds two numbers
def add(a, b):
    # Add a and b
    result = a + b  # Store result
    # Return result
    return result  # Return the result

# Good - concise comments
def add(a, b):
    """Return the sum of two numbers."""
    return a + b
```

## 6. Best Practices

1. **Use docstrings** for all public functions, classes, and modules
2. **Write clear, concise** comments that explain why, not what
3. **Keep comments updated** when code changes
4. **Follow PEP 8** comment formatting
5. **Use inline comments** sparingly (2+ spaces before #)
6. **Remove commented-out code** (use version control)

## 7. Practice Exercises

### Exercise 1: Document a Function
Write a function to calculate the factorial of a number with proper docstring.

### Exercise 2: Comment Your Code
Take an existing program and add appropriate comments and docstrings.

### Exercise 3: Module Documentation
Create a module with proper module-level documentation.

## 8. Summary

**Key takeaways:**
- Single-line comments use `#`
- Docstrings are triple-quoted strings for documentation
- Comments explain why, not what
- Keep comments updated and accurate
- Follow PEP 8 comment guidelines
- Use version control instead of commenting out code

**Next Lecture:** We'll learn about variables and assignment.

---

**Quick Reference:**
- PEP 257 (Docstring Conventions): https://peps.python.org/pep-0257/
- PEP 8 Comments: https://peps.python.org/pep-0008/#comments
- Python Documentation: https://docs.python.org/3/tutorial/classes.html#documentation-strings