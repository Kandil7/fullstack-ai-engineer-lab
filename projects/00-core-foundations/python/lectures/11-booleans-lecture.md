# Python Booleans - Lecture Notes

## 1. Topic Overview
This lecture covers Python booleans and logical operations. Booleans represent truth values (True and False) and are fundamental for conditional logic, comparisons, and control flow in Python programs.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Understand boolean values (True/False)
- Use comparison operators
- Apply logical operators (and, or, not)
- Understand truthiness and falsiness
- Use booleans in conditional statements
- Convert between booleans and other types

## 3. Key Concepts

### 3.1 Boolean Values
Python has two boolean values: `True` and `False` (case-sensitive).

```python
# Boolean values
is_active = True
is_admin = False

# Boolean expressions
x = 10
is_positive = x > 0  # True
is_negative = x < 0  # False
```

### 3.2 Comparison Operators
These operators return boolean values:

```python
x = 10
y = 20

print(x == y)   # Equal: False
print(x != y)   # Not equal: True
print(x > y)    # Greater than: False
print(x < y)    # Less than: True
print(x >= 10)  # Greater or equal: True
print(x <= 5)   # Less or equal: False
```

### 3.3 Logical Operators

**and** - True if both conditions are True:
```python
x = 15
print(x > 10 and x < 20)  # True (both True)
print(x > 10 and x > 20)  # False (one False)
```

**or** - True if at least one condition is True:
```python
x = 15
print(x > 10 or x > 20)  # True (one True)
print(x > 20 or x > 30)  # False (both False)
```

**not** - Reverses the boolean value:
```python
x = 10
print(not (x > 5))   # False (not True)
print(not (x > 15))  # True (not False)
```

### 3.4 Truthiness and Falsiness
In Python, many values can be treated as booleans:

**Falsy values:**
```python
# All these evaluate to False
print(bool(0))      # False
print(bool(0.0))    # False
print(bool(""))     # False
print(bool([]))     # False
print(bool({}))     # False
print(bool(None))   # False
```

**Truthy values:**
```python
# All these evaluate to True
print(bool(1))      # True
print(bool(-1))     # True
print(bool("hi"))   # True
print(bool([1, 2])) # True
print(bool({"a": 1}))  # True
```

### 3.5 Boolean Context
Booleans are used in:
- Conditional statements (if, elif, else)
- Loop conditions (while)
- Function return values
- Data validation

```python
# Conditional statements
if is_active:
    print("User is active")

# While loop
while not done:
    process()

# Function return
def is_valid(data):
    return len(data) > 0
```

## 4. Code Examples

### Example 1: Basic Boolean Operations
```python
# Boolean variables
is_sunny = True
is_weekend = False

# Logical operations
if is_sunny and is_weekend:
    print("Perfect day for park!")

if is_sunny or is_weekend:
    print("At least one condition met!")

if not is_weekend:
    print("It's a workday")
```

### Example 2: Comparison Operations
```python
# Comparing values
age = 25
score = 85

# Multiple conditions
if age >= 18 and age <= 65:
    print("Working age adult")

if score >= 90 or score >= 80:
    print("Good score!")

# Chained comparisons (Pythonic)
if 18 <= age <= 65:
    print("Working age adult (chained)")
```

### Example 3: Truthiness in Practice
```python
# Using truthiness for简洁 checks
name = ""
if not name:
    print("Name is empty")

items = []
if not items:
    print("No items found")

# Using truthiness for default values
user_input = ""
display_name = user_input or "Anonymous"
print(display_name)  # Anonymous
```

### Example 4: Boolean Functions
```python
def is_even(number):
    """Check if number is even."""
    return number % 2 == 0

def is_adult(age):
    """Check if person is adult."""
    return age >= 18

# Using boolean functions
print(is_even(4))    # True
print(is_even(7))    # False
print(is_adult(25))  # True
print(is_adult(15))  # False
```

## 5. Common Mistakes to Avoid

### Mistake 1: Confusing = and ==
```python
# Wrong - assignment instead of comparison
if x = 10:  # SyntaxError!
    print("x is 10")

# Right - use == for comparison
if x == 10:
    print("x is 10")
```

### Mistake 2: Not Using Parentheses
```python
# Wrong - precedence issues
if x > 5 and y > 5 or z > 5:  # Ambiguous
    print("Something")

# Right - use parentheses for clarity
if (x > 5 and y > 5) or z > 5:
    print("Something")
```

### Mistake 3: Comparing to True/False
```python
# Wrong - redundant comparison
if is_active == True:  # Redundant
    print("Active")

# Right - direct boolean check
if is_active:
    print("Active")
```

### Mistake 4: Forgetting Short-circuit Evaluation
```python
# Be careful with short-circuit
def check():
    print("Checking...")
    return True

# This won't print "Checking..." if x is False
if x and check():
    print("Passed")
```

## 6. Best Practices

1. **Use descriptive names**: `is_valid` instead of `flag`
2. **Direct boolean checks**: `if is_valid:` instead of `if is_valid == True:`
3. **Use parentheses** for complex conditions
4. **Leverage truthiness** for简洁 code
5. **Return booleans** from comparison functions
6. **Document** boolean parameters

## 7. Practice Exercises

### Exercise 1: Age Validator
Write a function that checks if a person is a child (0-12), teenager (13-19), adult (20-64), or senior (65+).

### Exercise 2: Password Checker
Create a function that validates a password (at least 8 chars, contains digit, contains uppercase).

### Exercise 3: Login System
Build a simple login system that checks username and password with boolean logic.

## 8. Summary

**Key takeaways:**
- Booleans represent True/False values
- Comparison operators return booleans
- Logical operators combine conditions
- Many values have truthiness/falsiness
- Use booleans for conditional logic
- Follow best practices for readable boolean code

**Next Lecture:** We'll explore operators in detail.

---

**Quick Reference:**
- Boolean Type: https://docs.python.org/3/library/stdtypes.html#boolean-type-bool
- Logical Operators: https://docs.python.org/3/reference/expressions.html#boolean-operations
- Truth Value Testing: https://docs.python.org/3/library/stdtypes.html#truth-value-testing