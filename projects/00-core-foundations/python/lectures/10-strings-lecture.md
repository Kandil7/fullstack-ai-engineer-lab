# Python Strings - Lecture Notes

## 1. Topic Overview
This lecture covers Python strings in detail. Strings are sequences of characters used for text data. We'll explore string creation, manipulation, formatting, and methods. Strings are immutable in Python, meaning they cannot be changed after creation.

## 2. Learning Objectives
By the end of this lecture, you will be able to:
- Create strings using different methods
- Manipulate strings (slicing, concatenation, methods)
- Format strings using f-strings and other methods
- Work with string methods (upper, lower, split, etc.)
- Understand string immutability
- Handle special characters and escape sequences

## 3. Key Concepts

### 3.1 String Creation
Strings can be created using single quotes, double quotes, or triple quotes.

```python
# Single quotes
name = 'Alice'

# Double quotes
greeting = "Hello, World!"

# Triple quotes (multi-line)
multi_line = """This is a
multi-line string"""

# Triple single quotes
also_multi = '''This is also
multi-line'''
```

### 3.2 String Immutability
Strings cannot be changed after creation. Operations create new strings.

```python
name = "Alice"
# name[0] = "B"  # TypeError! Strings are immutable

# Create new string instead
name = "B" + name[1:]  # "Blice"
```

### 3.3 String Indexing and Slicing
Access characters using indices (0-based).

```python
text = "Hello, World!"

# Indexing
print(text[0])   # H
print(text[-1])  # ! (last character)

# Slicing
print(text[0:5])   # Hello
print(text[7:12])  # World
print(text[:5])    # Hello (start to index 5)
print(text[7:])    # World! (index 7 to end)
print(text[::2])   # Hlo ol! (every 2nd character)
```

### 3.4 String Methods

**Case methods:**
```python
text = "Hello, World!"
print(text.upper())      # HELLO, WORLD!
print(text.lower())      # hello, world!
print(text.title())      # Hello, World!
print(text.capitalize()) # Hello, world!
print(text.swapcase())   # hELLO, wORLD!
```

**Search methods:**
```python
text = "Hello, World!"
print(text.find("World"))    # 7
print(text.find("Python"))  # -1 (not found)
print(text.count("l"))      # 3
print(text.startswith("Hello"))  # True
print(text.endswith("!"))    # True
```

**Modify methods:**
```python
text = "  Hello, World!  "
print(text.strip())     # "Hello, World!" (removes whitespace)
print(text.lstrip())    # "Hello, World!  "
print(text.rstrip())    # "  Hello, World!"
print(text.replace("World", "Python"))  # "  Hello, Python!  "
```

### 3.5 String Splitting and Joining

**Splitting:**
```python
text = "apple,banana,cherry"
fruits = text.split(",")
print(fruits)  # ['apple', 'banana', 'cherry']

# Split by whitespace
sentence = "Hello World Python"
words = sentence.split()
print(words)  # ['Hello', 'World', 'Python']
```

**Joining:**
```python
fruits = ['apple', 'banana', 'cherry']
text = ", ".join(fruits)
print(text)  # "apple, banana, cherry"

words = ['Hello', 'World']
sentence = " ".join(words)
print(sentence)  # "Hello World"
```

### 3.6 String Formatting

**f-strings (Python 3.6+):**
```python
name = "Alice"
age = 25
print(f"Name: {name}, Age: {age}")
print(f"Next year: {age + 1}")
print(f"PI: {3.14159:.2f}")
```

**str.format():**
```python
print("Name: {}, Age: {}".format("Alice", 25))
print("Name: {0}, Age: {1}".format("Alice", 25))
print("Name: {n}, Age: {a}".format(n="Alice", a=25))
```

## 4. Code Examples

### Example 1: Basic String Operations
```python
# String creation
name = "Alice"
greeting = "Hello, " + name + "!"

# String length
print(len(greeting))  # 13

# String repetition
separator = "-" * 20
print(separator)  # --------------------

# String membership
print("Alice" in greeting)  # True
```

### Example 2: String Methods
```python
# Text processing
text = "  Hello, World!  "
print(text.strip())           # "Hello, World!"
print(text.strip().upper())   # "HELLO, WORLD!"
print(text.strip().lower())   # "hello, world!"

# Search and replace
email = "user@example.com"
print(email.replace("@", "[at]"))  # "user[at]example.com"
print(email.find("@"))            # 4
```

### Example 3: Split and Join
```python
# CSV processing
csv_line = "Alice,25,alice@email.com"
fields = csv_line.split(",")
print(fields)  # ['Alice', '25', 'alice@email.com']

# Reconstruct
reconstructed = " | ".join(fields)
print(reconstructed)  # "Alice | 25 | alice@email.com"
```

### Example 4: String Formatting
```python
# Product information
name = "Laptop"
price = 999.99
quantity = 3

# f-string formatting
print(f"Product: {name}")
print(f"Price: ${price:.2f}")
print(f"Quantity: {quantity}")
print(f"Total: ${price * quantity:.2f}")

# Alignment
print(f"{'Product':<15}{'Price':>10}{'Qty':>5}")
print(f"{name:<15}${price:>9.2f}{quantity:>5}")
```

## 5. Common Mistakes to Avoid

### Mistake 1: Trying to Modify Immutable Strings
```python
# Wrong - strings are immutable
text = "Hello"
# text[0] = "h"  # TypeError!

# Right - create new string
text = "h" + text[1:]
```

### Mistake 2: Forgetting split() Returns a List
```python
# Wrong - expecting string
text = "hello world"
result = text.split()
print(result)  # ['hello', 'world'] (list, not string)

# Right - join to get string back
result = " ".join(text.split())
```

### Mistake 3: Case Sensitivity in Searches
```python
# Wrong - case-sensitive
text = "Hello World"
print(text.find("hello"))  # -1 (not found)

# Right - convert case first
print(text.lower().find("hello"))  # 0
```

### Mistake 4: Not Stripping Input
```python
# Wrong - whitespace issues
user_input = input("Enter name: ")  # User types " Alice "
if user_input == "Alice":
    print("Match!")  # Never matches!

# Right - strip whitespace
if user_input.strip() == "Alice":
    print("Match!")  # Works!
```

## 6. Best Practices

1. **Use f-strings** for string formatting (Python 3.6+)
2. **Strip user input** before processing
3. **Use string methods** instead of manual manipulation
4. **Choose appropriate quotes** (single, double, triple)
5. **Be mindful** of string immutability
6. **Use join()** for building strings from lists

## 7. Practice Exercises

### Exercise 1: String Reverser
Write a function that reverses a string.

### Exercise 2: Word Counter
Create a program that counts words in a sentence.

### Exercise 3: Text Formatter
Build a program that formats text (center, left, right align).

## 8. Summary

**Key takeaways:**
- Strings are immutable sequences of characters
- Use indexing and slicing to access parts
- String methods provide powerful manipulation
- f-strings are the preferred formatting method
- split() and join() work together for text processing
- Always strip user input before processing

**Next Lecture:** We'll explore booleans and logical operations.

---

**Quick Reference:**
- String Methods: https://docs.python.org/3/library/stdtypes.html#string-methods
- String Formatting: https://docs.python.org/3/library/string.html#formatstrings
- f-strings: https://docs.python.org/3/reference/lexical_analysis.html#f-strings