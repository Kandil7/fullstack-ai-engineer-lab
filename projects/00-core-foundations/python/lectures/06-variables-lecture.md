# Python Variables - Lecture Notes

## 1. Topic Overview
This lecture covers Python variables, including how to create, name, and use them. Variables are fundamental building blocks in programming - they store data that your program can manipulate. We'll explore variable assignment, naming rules, and best practices.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Create and assign variables
- Understand Python's dynamic typing
- Follow proper naming conventions
- Use multiple assignment techniques
- Understand variable scope basics
- Avoid common variable mistakes

## 3. Key Concepts

### 3.1 What is a Variable?
A variable is a named container that stores data in memory. Think of it as a labeled box where you can put values.

```python
# Variable assignment
name = "Alice"      # String variable
age = 25            # Integer variable
height = 1.65       # Float variable
is_student = True   # Boolean variable
```

### 3.2 Variable Assignment
In Python, assignment uses the `=` operator. The variable name goes on the left, and the value goes on the right.

```python
# Basic assignment
x = 10
y = 3.14
name = "Hello"
```

**Key points:**
- Variables don't need explicit type declaration
- Python determines type automatically (dynamic typing)
- Assignment creates the variable if it doesn't exist

### 3.3 Dynamic Typing
Python is **dynamically typed** - variables can change type during execution.

```python
x = 10          # x is an integer
print(type(x))  # <class 'int'>

x = "hello"     # Now x is a string
print(type(x))  # <class 'str'>

x = [1, 2, 3]   # Now x is a list
print(type(x))  # <class 'list'>
```

### 3.4 Naming Rules

**Must follow:**
- Start with letter or underscore (`_`)
- Can contain letters, numbers, underscores
- Case-sensitive (`name` ≠ `Name`)
- Cannot be Python keywords

```python
# Valid variable names
user_name = "Alice"
_private = "hidden"
count2 = 5
MAX_SIZE = 100

# Invalid variable names
# 2count = 5      # Can't start with number
# user-name = "A" # Can't use hyphen
# class = "Math"  # Can't use keywords
```

### 3.5 Multiple Assignment

**Simultaneous assignment:**
```python
# Multiple variables at once
x, y, z = 1, 2, 3

# Same value to multiple variables
a = b = c = 0

# Swap variables
x, y = y, x
```

### 3.6 Variable Scope

**Local variables:**
```python
def my_function():
    x = 10  # Local variable
    print(x)  # Accessible here

my_function()
# print(x)  # Error! x not accessible here
```

**Global variables:**
```python
x = 10  # Global variable

def my_function():
    global x  # Declare global
    x = 20    # Modify global

my_function()
print(x)  # 20
```

## 4. Code Examples

### Example 1: Basic Variable Assignment
```python
# Different data types
name = "Alice"          # String
age = 25                # Integer
height = 1.65           # Float
is_student = True       # Boolean
grades = [90, 85, 92]   # List

# Print variables
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height}")
print(f"Student: {is_student}")
print(f"Grades: {grades}")
```

### Example 2: Multiple Assignment
```python
# Assign multiple values
x, y, z = 10, 20, 30
print(f"x={x}, y={y}, z={z}")

# Same value to multiple variables
a = b = c = 100
print(f"a={a}, b={b}, c={c}")

# Swap variables
x, y = 5, 10
print(f"Before swap: x={x}, y={y}")
x, y = y, x
print(f"After swap: x={x}, y={y}")
```

### Example 3: Dynamic Typing
```python
# Variable can change type
data = 42
print(f"Initial: {data} (type: {type(data).__name__})")

data = "Hello"
print(f"Now: {data} (type: {type(data).__name__})")

data = [1, 2, 3]
print(f"Now: {data} (type: {type(data).__name__})")
```

### Example 4: Variable Scope
```python
# Global vs local scope
global_var = "I'm global"

def function():
    local_var = "I'm local"
    print(global_var)  # Can access global
    print(local_var)   # Can access local

function()
print(global_var)  # Can access global
# print(local_var)  # Error! Can't access local
```

## 5. Common Mistakes to Avoid

### Mistake 1: Using Keywords as Variables
```python
# Wrong - using reserved words
class = "Math"  # SyntaxError!
for = 5         # SyntaxError!

# Correct - use descriptive names
subject = "Math"
count = 5
```

### Mistake 2: Starting with Number
```python
# Wrong - can't start with number
2count = 5  # SyntaxError!

# Correct - start with letter or underscore
count2 = 5
_count = 5
```

### Mistake 3: Using Special Characters
```python
# Wrong - invalid characters
user-name = "Alice"  # SyntaxError!
user name = "Alice"  # SyntaxError!

# Correct - use underscores
user_name = "Alice"
```

### Mistake 4: Case Sensitivity
```python
# Wrong - case matters
name = "Alice"
Name = "Bob"
NAME = "Charlie"
# These are three different variables!

# Correct - be consistent
name = "Alice"
```

## 6. Best Practices

1. **Use descriptive names**: `user_age` instead of `x`
2. **Follow PEP 8**: snake_case for variables
3. **Use UPPER_CASE for constants**: `MAX_SIZE = 100`
4. **Avoid single letters** (except loop counters)
5. **Initialize variables** before use
6. **Use meaningful names** that describe purpose

## 7. Practice Exercises

### Exercise 1: Personal Information
Create variables for your name, age, height, and hobbies. Print them in a formatted output.

### Exercise 2: Variable Swapping
Write a program that swaps two variables without using a third variable.

### Exercise 3: Type Changing
Create a variable and change its type multiple times. Print the type each time.

## 8. Summary

**Key takeaways:**
- Variables store data in named containers
- Python uses dynamic typing (no type declaration needed)
- Follow naming rules: letters, numbers, underscores
- Use snake_case for variables, UPPER_CASE for constants
- Variables have scope (local vs global)
- Descriptive names improve code readability

**Next Lecture:** We'll explore Python's data types in detail.

---

**Quick Reference:**
- PEP 8 Naming: https://peps.python.org/pep-0008/#naming-conventions
- Python Variables: https://docs.python.org/3/tutorial/classes.html#variable-annotations
- Dynamic Typing: https://docs.python.org/3/reference/compound_stmts.html#the-simple-assignment-statement