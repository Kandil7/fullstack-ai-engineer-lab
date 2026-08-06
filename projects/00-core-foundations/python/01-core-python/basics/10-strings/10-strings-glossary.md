# Python Strings - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| str | Type | Immutable sequence of characters |
| String Literal | Syntax | Text enclosed in quotes |
| f-string | Formatting | String with embedded expressions |
| Slice | Operation | Extracting substring using indices |
| Method | Function | Function that belongs to an object |
| Immutability | Property | Cannot be changed after creation |
| Escape Sequence | Character | Special character representation (\n, \t) |
| Raw String | Type | String ignoring escape sequences |
| Unicode | Encoding | Character encoding standard |
| String Methods | Functions | Built-in string manipulation functions |

## Detailed Definitions

### C

**Concatenation**
- **Definition**: Joining strings using + operator
- **Example**: `"Hello" + " " + "World"`
- **Related terms**: + Operator, String, Join
```python
# String concatenation
first = "Hello"
second = "World"
result = first + " " + second
print(result)  # Hello World

# Concatenation with variables
name = "Alice"
age = 25
print("Name: " + name + ", Age: " + str(age))
```

**Conversion**
- **Definition**: Converting other types to string
- **Example**: `str(10)` → "10"
- **Related terms**: str(), Type Casting, String
```python
# Type to string conversion
num = 42
num_str = str(num)
print(num_str)  # "42"
print(type(num_str))  # <class 'str'>

# Boolean to string
is_true = True
print(str(is_true))  # "True"
```

### D

**Delimiter**
- **Definition**: Character used to separate values
- **Example**: Comma in CSV, space in sentences
- **Related terms**: Separator, Split, Join
```python
# Using delimiters
csv_line = "Alice,25,alice@email.com"
fields = csv_line.split(",")
print(fields)  # ['Alice', '25', 'alice@email.com']

# Reconstruct with delimiter
reconstructed = " | ".join(fields)
print(reconstructed)  # "Alice | 25 | alice@email.com"
```

### E

**Escape Sequence**
- **Definition**: Special character represented by backslash + character
- **Example**: `\n` (newline), `\t` (tab), `\"` (quote)
- **Related terms**: Raw String, Special Character, Backslash
```python
# Common escape sequences
print("Hello\nWorld")    # Newline
print("Name\tAge")       # Tab
print("Quote: \"Hi\"")   # Double quote
print("Backslash: \\")   # Backslash
```

### F

**f-string**
- **Definition**: String literal with embedded expressions using f prefix
- **Example**: `f"Name: {name}"`
- **Related terms**: String Formatting, Expression, Format Specification
```python
name = "Alice"
age = 25
print(f"Hello, {name}!")  # Hello, Alice!
print(f"Age: {age}")      # Age: 25
print(f"Next year: {age + 1}")  # Next year: 26
```

**Format Specification**
- **Definition**: Code controlling how values are formatted
- **Example**: `:.2f`, `:,`, `:<10`
- **Related terms**: Format Mini-Language, Formatting, Precision
```python
pi = 3.14159
print(f"Pi: {pi:.2f}")    # 2 decimal places
print(f"Number: {1234:,}")  # With commas
print(f"Text: {'hi':^10}") # Centered
```

### I

**Immutability**
- **Definition**: Property that value cannot be changed after creation
- **Example**: Strings, tuples, integers are immutable
- **Related terms**: Mutable, Immutable, Change
```python
# Strings are immutable
text = "Hello"
# text[0] = "h"  # TypeError!

# Create new string instead
text = "h" + text[1:]  # "hello"
```

**Indexing**
- **Definition**: Accessing single character by position
- **Example**: `text[0]`, `text[-1]`
- **Related terms**: Slicing, Position, Zero-based
```python
text = "Hello"
print(text[0])   # H (first character)
print(text[-1])  # o (last character)
print(text[1])   # e (second character)
```

### J

**join()**
- **Definition**: Method to concatenate iterable elements into string
- **Example**: `", ".join(["a", "b", "c"])`
- **Related terms**: Split, Concatenation, Iterable
```python
# join() method
fruits = ['apple', 'banana', 'cherry']
text = ", ".join(fruits)
print(text)  # "apple, banana, cherrry"

# Join with different delimiter
words = ['Hello', 'World']
sentence = " ".join(words)
print(sentence)  # "Hello World"
```

### M

**Method**
- **Definition**: Function that belongs to an object
- **Example**: `text.upper()`, `text.split()`
- **Related terms**: Function, Object, String Methods
```python
# String methods
text = "Hello, World!"
print(text.upper())      # HELLO, WORLD!
print(text.lower())      # hello, world!
print(text.find("World"))  # 7
print(text.replace("World", "Python"))  # "Hello, Python!"
```

**Multi-line String**
- **Definition**: String spanning multiple lines
- **Example**: `"""Line 1\nLine 2\nLine 3"""`
- **Related terms**: Triple Quotes, Docstring, Newline
```python
# Multi-line string
multi = """Line 1
Line 2
Line 3"""
print(multi)
# Line 1
# Line 2
# Line 3
```

### P

**Prefix**
- **Definition**: Characters at start of string
- **Example**: `"Hello".startswith("He")`
- **Related terms**: Suffix, startswith(), endswith()
```python
# Check prefix
text = "Hello, World!"
print(text.startswith("Hello"))  # True
print(text.startswith("World"))  # False
```

**Pythonic**
- **Definition**: Idiomatic Python way of doing things
- **Example**: Using f-strings instead of concatenation
- **Related terms**: Best Practices, Idiom, Style
```python
# Non-Pythonic
print("Hello, " + name + "!")

# Pythonic
print(f"Hello, {name}!")
```

### R

**Raw String**
- **Definition**: String with r prefix ignoring escape sequences
- **Example**: `r"C:\new\folder"`
- **Related terms**: Escape Sequence, Backslash, String Literal
```python
# Raw string - literal backslashes
print(r"C:\new\folder")  # C:\new\folder

# Regular string - interprets escape sequences
print("C:\new\folder")  # C:
                        # ew
                        # older
```

**Replace**
- **Definition**: Method to substitute parts of string
- **Example**: `"hello".replace("l", "L")`
- **Related terms**: Substitute, Method, String Manipulation
```python
# replace() method
text = "Hello, World!"
print(text.replace("World", "Python"))  # "Hello, Python!"
print(text.replace("l", "L"))  # "HeLLo, WorLd!"
print(text.replace("l", "L", 2))  # "HeLLo, World!" (replace first 2)
```

### S

**Slicing**
- **Definition**: Extracting substring using indices
- **Example**: `text[0:5]`, `text[::2]`
- **Related terms**: Indexing, Substring, Range
```python
text = "Hello, World!"
print(text[0:5])   # Hello
print(text[7:12])  # World
print(text[:5])    # Hello (start to index 5)
print(text[7:])    # World! (index 7 to end)
print(text[::2])   # Hlo ol! (every 2nd character)
```

**split()**
- **Definition**: Method to divide string into list
- **Example**: `"a,b,c".split(",")`
- **Related terms**: Join, Delimiter, List
```python
# split() method
text = "apple,banana,cherry"
fruits = text.split(",")
print(fruits)  # ['apple', 'banana', 'cherry']

# Split by whitespace
sentence = "Hello World Python"
words = sentence.split()
print(words)  # ['Hello', 'World', 'Python']

# Split with maxsplit
text = "a,b,c,d"
print(text.split(",", 2))  # ['a', 'b', 'c,d']
```

**String Literal**
- **Definition**: Text enclosed in quotes
- **Example**: `"Hello"`, `'World'`, `"""Multi-line"""`
- **Related terms**: Quote, Delimiter, Syntax
```python
# String literals
single = 'Hello'
double = "Hello"
multi = """Hello
World"""
```

**str()**
- **Definition**: Function to convert value to string
- **Example**: `str(10)` → "10"
- **Related terms**: Type Conversion, Casting, String
```python
# str() conversion
num = 42
print(str(num))  # "42"

is_true = True
print(str(is_true))  # "True"

my_list = [1, 2, 3]
print(str(my_list))  # "[1, 2, 3]"
```

**Strip**
- **Definition**: Method to remove whitespace from both ends
- **Example**: `"  hello  ".strip()` → "hello"
- **Related terms**: lstrip(), rstrip(), Whitespace
```python
# strip() methods
text = "  Hello, World!  "
print(text.strip())     # "Hello, World!"
print(text.lstrip())    # "Hello, World!  "
print(text.rstrip())    # "  Hello, World!"

# Strip specific characters
text = "###Hello###"
print(text.strip("#"))  # "Hello"
```

**Suffix**
- **Definition**: Characters at end of string
- **Example**: `"Hello".endswith("lo")`
- **Related terms**: Prefix, endswith(), startswith()
```python
# Check suffix
text = "Hello, World!"
print(text.endswith("!"))    # True
print(text.endswith("World"))  # False
```

### T

**Title Case**
- **Definition**: First letter of each word capitalized
- **Example**: `"hello world".title()` → "Hello World"
- **Related terms**: capitalize(), upper(), lower()
```python
# Title case
text = "hello world"
print(text.title())  # "Hello World"

# capitalize() - first letter only
print(text.capitalize())  # "Hello world"
```

### U

**Unicode**
- **Definition**: Standard for encoding characters
- **Example**: `"Hello"` is Unicode string
- **Related terms**: Encoding, ASCII, Character Set
```python
# Unicode strings
text = "Hello, 世界!"
print(text)  # Works with any Unicode character

# Check Unicode code point
print(ord('A'))  # 65
print(chr(65))   # A
```

**Upper/Lower**
- **Definition**: Methods to change case
- **Example**: `"hello".upper()` → "HELLO"
- **Related terms**: casefold(), title(), swapcase()
```python
# Case methods
text = "Hello, World!"
print(text.upper())      # HELLO, WORLD!
print(text.lower())      # hello, world!
print(text.title())      # Hello, World!
print(text.capitalize()) # Hello, world!
print(text.swapcase())   # hELLO, wORLD!
```

## Key Concepts Summary

### String Operations
| Operation | Example | Result |
|-----------|---------|--------|
| Concatenation | `"a" + "b"` | `"ab"` |
| Repetition | `"a" * 3` | `"aaa"` |
| Indexing | `"hello"[0]` | `"h"` |
| Slicing | `"hello"[1:3]` | `"el"` |
| Length | `len("hello")` | `5` |
| Membership | `"l" in "hello"` | `True` |

### String Methods
| Method | Description | Example |
|--------|-------------|---------|
| upper() | Convert to uppercase | `"hello".upper()` → `"HELLO"` |
| lower() | Convert to lowercase | `"HELLO".lower()` → `"hello"` |
| strip() | Remove whitespace | `" hi ".strip()` → `"hi"` |
| split() | Split into list | `"a,b".split(",")` → `["a","b"]` |
| join() | Join list into string | `",".join(["a","b"])` → `"a,b"` |
| replace() | Replace substring | `"hi".replace("i","e")` → `"he"` |
| find() | Find substring index | `"hello".find("ll")` → `2` |
| count() | Count occurrences | `"hello".count("l")` → `2` |
| startswith() | Check start | `"hello".startswith("he")` → `True` |
| endswith() | Check end | `"hello".endswith("lo")` → `True` |

### String Formatting
| Method | Syntax | Example |
|--------|--------|---------|
| f-string | `f"...{expr}"` | `f"Name: {name}"` |
| str.format() | `"...{}".format()` | `"Name: {}".format(name)` |
| % formatting | `"..." % values` | `"Name: %s" % name` |

### Escape Sequences
| Sequence | Description | Example |
|----------|-------------|---------|
| `\n` | Newline | `"Line1\nLine2"` |
| `\t` | Tab | `"Name\tAge"` |
| `\\` | Backslash | `"C:\\path"` |
| `\"` | Double quote | `"He said \"Hi\""` |
| `\'` | Single quote | `'It\'s'` |

## Practice Terms

Match these terms to their definitions:
1. f-string - ?
2. slice - ?
3. immutable - ?
4. join() - ?
5. strip() - ?

**Answers:**
1. String with embedded expressions using f prefix
2. Extracting substring using indices
3. Cannot be changed after creation
4. Method to concatenate iterable elements into string
5. Method to remove whitespace from both ends