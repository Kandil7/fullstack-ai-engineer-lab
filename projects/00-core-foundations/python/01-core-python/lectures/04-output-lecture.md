# Python Output - Lecture Notes

## 1. Topic Overview
This lecture covers Python's output capabilities, focusing on the `print()` function and various ways to format and display information. We'll explore different output methods, formatting options, and best practices for displaying data.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Use the `print()` function effectively
- Format output using different methods
- Control output with special characters
- Display multiple values and data types
- Use escape sequences and raw strings
- Write clean, readable output code

## 3. Key Concepts

### 3.1 The print() Function
The `print()` function is Python's primary way to output text and data to the console.

**Basic syntax:**
```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

**Parameters:**
- `*objects`: Values to print (multiple values allowed)
- `sep`: Separator between values (default: space)
- `end`: Character to end output (default: newline)
- `file`: Output destination (default: stdout)
- `flush`: Whether to flush output buffer (default: False)

### 3.2 Basic Output Examples

**Simple text:**
```python
print("Hello, World!")
print('This also works')
```

**Numbers:**
```python
print(42)
print(3.14159)
print(2 + 3)
```

**Multiple values:**
```python
print("Name:", "Alice", "Age:", 25)
```

### 3.3 String Formatting Methods

**f-strings (Python 3.6+):**
```python
name = "Alice"
age = 25
print(f"Name: {name}, Age: {age}")
print(f"Next year you'll be {age + 1}")
```

**str.format():**
```python
print("Name: {}, Age: {}".format("Alice", 25))
print("Name: {0}, Age: {1}".format("Alice", 25))
print("Name: {n}, Age: {a}".format(n="Alice", a=25))
```

**String concatenation:**
```python
print("Name: " + "Alice" + ", Age: " + str(25))
```

### 3.4 Formatting Specifications

**Number formatting:**
```python
pi = 3.141592653589793
print(f"Pi: {pi:.2f}")  # 2 decimal places
print(f"Pi: {pi:.4f}")  # 4 decimal places
print(f"Percentage: {0.756:.1%}")  # 75.6%
print(f"Scientific: {1234567:.2e}")  # 1.23e+06
```

**String formatting:**
```python
name = "Alice"
print(f"Left aligned: {name:<10}")  # "Alice     "
print(f"Right aligned: {name:>10}") # "     Alice"
print(f"Centered: {name:^10}")      # "  Alice   "
print(f"Filled: {name:*^10}")       # "**Alice***"
```

**Integer formatting:**
```python
number = 1234567
print(f"With commas: {number:,}")  # 1,234,567
print(f"With underscores: {number:_}")  # 1_234_567
print(f"Binary: {42:b}")  # 101010
print(f"Octal: {42:o}")   # 52
print(f"Hex: {42:x}")     # 2a
```

### 3.5 Special Characters and Escape Sequences

**Common escape sequences:**
```python
print("Line1\nLine2")      # Newline
print("Column1\tColumn2")  # Tab
print("Quote: \"Hello\"")  # Double quote
print("Backslash: \\")     # Backslash
print("Bell: \a")          # Alert/bell
print("Backspace: \b")     # Backspace
```

**Raw strings (ignore escape sequences):**
```python
print(r"C:\new\folder")  # Prints literal backslashes
print(r"Line1\nLine2")   # Prints \n literally
```

### 3.6 print() Parameters in Detail

**Using sep parameter:**
```python
print("2024", "01", "15", sep="-")  # 2024-01-15
print("a", "b", "c", sep="")        # abc
print("a", "b", "c", sep=", ")      # a, b, c
```

**Using end parameter:**
```python
print("Hello", end=" ")
print("World")  # Output: Hello World

print("Loading", end="...\n")  # Loading...
```

## 4. Code Examples

### Example 1: Basic Output
```python
# Simple output
print("Hello, World!")
print("Python is awesome!")

# Numbers
print(42)
print(3.14)

# Multiple values
print("Name:", "Alice", "Age:", 25)
```

### Example 2: String Formatting
```python
name = "Bob"
age = 30
height = 1.75

# f-string (recommended)
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height:.2f}m")

# str.format()
print("Name: {}".format(name))
print("Age: {}".format(age))

# String concatenation
print("Name: " + name)
```

### Example 3: Number Formatting
```python
# Number formatting
pi = 3.141592653589793
print(f"Pi: {pi:.2f}")  # 3.14
print(f"Pi: {pi:.4f}")  # 3.1416

# Large numbers
population = 789456123
print(f"Population: {population:,}")  # 789,456,123

# Percentages
tax_rate = 0.0825
print(f"Tax rate: {tax_rate:.1%}")  # 8.2%

# Scientific notation
avogadro = 6.022e23
print(f"Avogadro: {avogadro:.3e}")  # 6.022e+23
```

### Example 4: Special Characters
```python
# Escape sequences
print("Hello\nWorld")  # Newline
print("Name\tAge")     # Tab
print("Quote: \"Hi\"") # Quote

# Raw strings
print(r"C:\new\folder")  # Literal backslashes
```

## 5. Common Mistakes to Avoid

### Mistake 1: Forgetting str() for Non-Strings
```python
age = 25
# Wrong - concatenation error
print("Age: " + age)  # TypeError!

# Correct - use f-string or str()
print("Age: " + str(age))
print(f"Age: {age}")
```

### Mistake 2: Incorrect Format Specifications
```python
pi = 3.14159
# Wrong - missing format spec
print(f"Pi: {pi:.2}")  # ValueError!

# Correct - include f for float
print(f"Pi: {pi:.2f}")
```

### Mistake 3: Unnecessary Escape Characters
```python
# Wrong - unnecessary escaping
print("Hello\n")  # Extra newline

# Correct - if you want just "Hello\n"
print("Hello")
```

### Mistake 4: Mixing Formatting Styles
```python
# Inconsistent (works but confusing)
print(f"Name: {name}, Age: {}".format(age))  # Wrong!

# Use one style consistently
print(f"Name: {name}, Age: {age}")
```

## 6. Best Practices

1. **Use f-strings** for most formatting (Python 3.6+)
2. **Be consistent** with formatting style
3. **Use meaningful** variable names in output
4. **Format numbers** appropriately (decimals, commas)
5. **Use escape sequences** for special characters
6. **Consider output** readability for users

## 7. Practice Exercises

### Exercise 1: Personal Information Card
Create a program that outputs a formatted personal information card with name, age, email, and address.

### Exercise 2: Number Formatter
Write a program that formats numbers in different ways: currency, percentage, scientific notation.

### Exercise 3: Table Printer
Create a program that outputs a formatted table with headers and aligned columns.

## 8. Summary

**Key takeaways:**
- `print()` is Python's primary output function
- f-strings are the most readable formatting method
- Use format specifications for numbers and strings
- Escape sequences handle special characters
- Raw strings ignore escape sequences
- Consistent formatting improves code readability

**Next Lecture:** We'll learn about comments and documentation.

---

**Quick Reference:**
- print() documentation: https://docs.python.org/3/library/functions.html#print
- String formatting: https://docs.python.org/3/library/string.html#format-specification-mini-language
- f-strings: https://docs.python.org/3/reference/lexical_analysis.html#f-strings