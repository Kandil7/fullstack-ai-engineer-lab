# Python Operators - Lecture Notes

## 1. Topic Overview
This lecture covers Python operators in detail. Operators are special symbols that perform operations on values. We'll explore arithmetic, comparison, logical, assignment, and other operator types.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Use arithmetic operators for calculations
- Apply comparison operators for logic
- Use logical operators for conditions
- Understand assignment operators
- Work with identity and membership operators
- Know operator precedence

## 3. Key Concepts

### 3.1 Arithmetic Operators
Perform mathematical calculations:

```python
a = 10
b = 3

print(a + b)   # Addition: 13
print(a - b)   # Subtraction: 7
print(a * b)   # Multiplication: 30
print(a / b)   # Division: 3.333...
print(a // b)  # Floor Division: 3
print(a % b)   # Modulus: 1
print(a ** b)  # Exponent: 1000
```

### 3.2 Comparison Operators
Compare values and return booleans:

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
Combine boolean expressions:

```python
x = 15

# and - both must be True
print(x > 10 and x < 20)  # True
print(x > 10 and x > 20)  # False

# or - at least one must be True
print(x > 10 or x > 20)   # True
print(x > 20 or x > 30)   # False

# not - reverses boolean
print(not (x > 5))   # False
print(not (x > 15))  # True
```

### 3.4 Assignment Operators
Assign and modify values:

```python
x = 10       # Basic assignment
x += 5       # x = x + 5 (15)
x -= 3       # x = x - 3 (12)
x *= 2       # x = x * 2 (24)
x /= 4       # x = x / 4 (6.0)
x //= 2      # x = x // 2 (3.0)
x %= 2       # x = x % 2 (1.0)
x **= 3      # x = x ** 3 (1.0)
```

### 3.5 Identity Operators
Compare object identity (memory location):

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a is b)      # False (different objects)
print(a is c)      # True (same object)
print(a is not b)  # True
```

### 3.6 Membership Operators
Check if value is in sequence:

```python
fruits = ["apple", "banana", "cherry"]

print("apple" in fruits)      # True
print("orange" in fruits)     # False
print("orange" not in fruits) # True
```

### 3.7 Operator Precedence
Order of operations (highest to lowest):

```python
# 1. Parentheses ()
# 2. Exponentiation **
# 3. Unary +, -, ~
# 4. *, /, //, %
# 5. +, -
# 6. <<, >>
# 7. &
# 8. ^
# 9. |
# 10. ==, !=, >, <, >=, <=, is, is not, in, not in
# 11. not
# 12. and
# 13. or
```

## 4. Code Examples

### Example 1: Calculator Program
```python
def calculator():
    """Simple calculator using operators"""
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    op = input("Enter operator (+, -, *, /): ")
    
    if op == '+':
        result = num1 + num2
    elif op == '-':
        result = num1 - num2
    elif op == '*':
        result = num1 * num2
    elif op == '/':
        if num2 != 0:
            result = num1 / num2
        else:
            return "Error: Division by zero"
    else:
        return "Invalid operator"
    
    return f"{num1} {op} {num2} = {result}"

print(calculator())
```

### Example 2: Logical Operations
```python
# User authentication
username = input("Username: ")
password = input("Password: ")

# Check credentials
is_valid_user = username == "admin"
is_valid_pass = password == "1234"

if is_valid_user and is_valid_pass:
    print("Login successful!")
elif is_valid_user or is_valid_pass:
    print("Invalid credentials")
else:
    print("Access denied")
```

### Example 3: Membership Testing
```python
# Check if element exists
numbers = [1, 2, 3, 4, 5]
text = "Hello, World!"

print(3 in numbers)           # True
print(6 in numbers)           # False
print("World" in text)        # True
print("Python" not in text)   # True
```

### Example 4: Operator Precedence
```python
# Understanding precedence
result1 = 2 + 3 * 4     # 14 (not 20)
result2 = (2 + 3) * 4   # 20
result3 = 2 ** 3 ** 2   # 512 (right-associative)
result4 = (2 ** 3) ** 2 # 64

print(f"2 + 3 * 4 = {result1}")
print(f"(2 + 3) * 4 = {result2}")
print(f"2 ** 3 ** 2 = {result3}")
print(f"(2 ** 3) ** 2 = {result4}")
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

### Mistake 2: Division by Zero
```python
# Wrong - division by zero
result = 10 / 0  # ZeroDivisionError!

# Right - check for zero
if denominator != 0:
    result = numerator / denominator
else:
    print("Cannot divide by zero")
```

### Mistake 3: Integer Division vs Float Division
```python
# Unexpected results
print(10 / 2)   # 5.0 (float)
print(10 // 2)  # 5 (int)

# Use // for integer division
result = 10 // 3  # 3
```

### Mistake 4: Forgetting Precedence
```python
# Wrong - unexpected result
result = 2 + 3 * 4  # 14, not 20

# Right - use parentheses for clarity
result = (2 + 3) * 4  # 20
```

## 6. Best Practices

1. **Use parentheses** for complex expressions
2. **Check for zero** before division
3. **Use descriptive variable names**
4. **Understand operator precedence**
5. **Use `is` for None comparisons**
6. **Use `in` for membership tests**

## 7. Practice Exercises

### Exercise 1: Scientific Calculator
Build a calculator that handles basic and advanced operations (sqrt, power, etc.).

### Exercise 2: Grade Calculator
Create a program that calculates grades based on scores using comparison operators.

### Exercise 3: Password Validator
Build a password validator using logical operators.

## 8. Summary

**Key takeaways:**
- Arithmetic operators perform calculations
- Comparison operators return booleans
- Logical operators combine conditions
- Assignment operators modify values
- Identity operators compare objects
- Membership operators check sequences
- Understand operator precedence

**Next Lecture:** We'll explore lists in detail.

---

**Quick Reference:**
- Operators: https://docs.python.org/3/reference/expressions.html#operators
- Operator Precedence: https://docs.python.org/3/reference/expressions.html#operator-precedence