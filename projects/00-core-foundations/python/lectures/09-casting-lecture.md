# Python Type Casting - Lecture Notes

## 1. Topic Overview
This lecture covers type casting (type conversion) in Python. Casting is the process of converting one data type to another. We'll explore explicit and implicit type conversion, when to use each method, and common pitfalls.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Perform explicit type casting (int(), float(), str(), bool())
- Understand implicit type conversion (coercion)
- Know when and why to use type conversion
- Avoid common casting errors
- Use type conversion in practical scenarios

## 3. Key Concepts

### 3.1 What is Type Casting?
Type casting is converting a value from one data type to another. Python supports both explicit (manual) and implicit (automatic) conversion.

### 3.2 Explicit Type Casting
You manually convert types using constructor functions:

```python
# String to integer
x = int("10")  # 10

# Integer to string
y = str(10)  # "10"

# Integer to float
z = float(10)  # 10.0

# Float to integer (truncates decimal)
a = int(3.99)  # 3

# String to float
b = float("3.14")  # 3.14
```

### 3.3 Implicit Type Conversion (Coercion)
Python automatically converts types in expressions:

```python
# Automatic conversion
result = 10 + 3.14  # int + float = float (13.14)
print(type(result))  # <class 'float'>

# Boolean to number
print(True + 1)  # 2
print(False * 10)  # 0
```

### 3.4 Type Conversion Rules

**Valid conversions:**
- String → Number (if valid number string)
- Number → String (always works)
- Number → Boolean (0/0.0 → False, others → True)
- Boolean → Number (True → 1, False → 0)

**Invalid conversions:**
- Non-numeric string → Number (raises ValueError)
- Complex → int/float (raises TypeError)

## 4. Code Examples

### Example 1: Basic Type Casting
```python
# String to number
num_str = "42"
num_int = int(num_str)
num_float = float(num_str)

print(f"String: '{num_str}'")
print(f"Integer: {num_int}")
print(f"Float: {num_float}")

# Number to string
age = 25
age_str = str(age)
print(f"Age: {age_str} (string)")
print(f"Length: {len(age_str)}")
```

### Example 2: Float to Integer
```python
# Truncating vs rounding
pi = 3.14159
print(f"Original: {pi}")
print(f"int(pi): {int(pi)}")  # Truncates: 3
print(f"round(pi): {round(pi)}")  # Rounds: 3
print(f"math.floor(pi): {math.floor(pi)}")  # Floor: 3
print(f"math.ceil(pi): {math.ceil(pi)}")  # Ceiling: 4
```

### Example 3: Boolean Conversion
```python
# Number to boolean
print(bool(0))     # False
print(bool(1))     # True
print(bool(-1))    # True
print(bool(3.14))  # True

# String to boolean
print(bool(""))      # False (empty string)
print(bool("hello")) # True (non-empty string)

# Other types to boolean
print(bool(None))    # False
print(bool([]))      # False (empty list)
print(bool([1, 2]))  # True (non-empty list)
```

### Example 4: Practical Examples
```python
# User input conversion
user_age = int(input("Enter your age: "))
user_height = float(input("Enter your height (m): "))

# Calculate with proper types
total = user_age + user_height  # Works (both numbers)
print(f"Sum: {total}")

# Building strings with numbers
name = "Alice"
age = 25
print("Hello, " + name + "! You are " + str(age) + " years old.")
print(f"Hello, {name}! You are {age} years old.")  # Better with f-strings
```

## 5. Common Mistakes to Avoid

### Mistake 1: Converting Non-Numeric Strings
```python
# Wrong - non-numeric string
num = int("hello")  # ValueError!

# Right - ensure valid conversion
num = int("42")
```

### Mistake 2: Float Precision in int()
```python
# Wrong - unexpected truncation
x = int(3.99)
print(x)  # 3, not 4!

# Right - use round() if needed
x = round(3.99)
print(x)  # 4
```

### Mistake 3: Forgetting str() for Concatenation
```python
# Wrong - type error
age = 25
print("Age: " + age)  # TypeError!

# Right - convert to string
print("Age: " + str(age))
print(f"Age: {age}")  # Better with f-strings
```

### Mistake 4: Converting Complex Numbers
```python
# Wrong - can't convert complex to int
z = 3 + 4j
x = int(z)  # TypeError!

# Right - extract parts first
x = int(z.real)  # 3
y = int(z.imag)  # 4
```

## 6. Best Practices

1. **Use f-strings** instead of concatenation with str()
2. **Validate input** before conversion
3. **Use round()** instead of int() for rounding
4. **Handle conversion errors** with try/except
5. **Be explicit** about type expectations
6. **Use type hints** to document expected types

## 7. Practice Exercises

### Exercise 1: Input Converter
Create a program that takes user input and converts it to different types (int, float, str, bool).

### Exercise 2: Safe Converter
Write a function that safely converts values with error handling.

### Exercise 3: Type Calculator
Build a calculator that handles different input types and converts appropriately.

## 8. Summary

**Key takeaways:**
- Use int(), float(), str(), bool() for explicit casting
- Python does implicit conversion in expressions
- Be careful with float to int conversion (truncates)
- Handle conversion errors with try/except
- Use f-strings for cleaner string building
- Type hints help document expected types

**Next Lecture:** We'll explore strings in detail.

---

**Quick Reference:**
- Type Conversion: https://docs.python.org/3/library/functions.html#int
- Built-in Functions: https://docs.python.org/3/library/functions.html