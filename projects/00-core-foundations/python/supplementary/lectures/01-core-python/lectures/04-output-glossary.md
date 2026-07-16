# Python Output - Glossary

## Quick Reference Table
| Term | Category | Brief Definition |
|------|----------|------------------|
| print() | Function | Outputs text/data to console |
| f-string | Formatting | String with embedded expressions (Python 3.6+) |
| str.format() | Formatting | String formatting method |
| Escape Sequence | Character | Special character representation (\n, \t, etc.) |
| Raw String | String Type | String ignoring escape sequences |
| sep | Parameter | Separator between print() values |
| end | Parameter | Character to end print() output |
| Format Specification | Syntax | Controls how values are formatted |
| stdout | Concept | Standard output stream |
| Formatting | Process | Converting values to readable strings |

## Detailed Definitions

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
print("Bell: \a")        # Alert sound
```

**Expression**
- **Definition**: Code that evaluates to a value
- **Example**: `{name}`, `{age + 1}`, `{x:.2f}`
- **Related terms**: f-string, Evaluation, Value
```python
name = "Alice"
age = 25
print(f"Name: {name}")      # Variable expression
print(f"Age: {age + 1}")    # Arithmetic expression
print(f"PI: {3.14159:.2f}") # Function call expression
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
print(f"Pi: {pi:.4f}")    # 4 decimal places
print(f"Number: {1234:,}")  # With commas
print(f"Text: {'hi':^10}") # Centered
```

**Format Mini-Language**
- **Definition**: Mini-language for string formatting specifications
- **Example**: `[[fill]align][sign][#][0][width][grouping][.precision][type]`
- **Related terms**: Format Specification, Formatting, Syntax
```python
# Format mini-language components
# fill: character to fill with
# align: < (left), > (right), ^ (center), = (pad after sign)
# sign: +, -, or space
# width: minimum field width
# .precision: digits after decimal
# type: f (float), d (integer), s (string), etc.
```

### N

**Newline Character**
- **Definition**: Character that moves cursor to next line
- **Example**: `\n`
- **Related terms**: Escape Sequence, Line Break, End Parameter
```python
print("Line 1\nLine 2")
# Output:
# Line 1
# Line 2
```

### P

**Parameter**
- **Definition**: Variable in function definition
- **Example**: `sep`, `end` in print()
- **Related terms**: Argument, Function, print()
```python
# print() parameters
print("a", "b", sep="-")    # Separator
print("Hello", end=" ")     # End character
print("World")              # Output: Hello World
```

**print()**
- **Definition**: Built-in function to output data
- **Example**: `print("Hello")`
- **Related terms**: Output, Console, Standard Output
```python
# Basic print usage
print("Hello, World!")
print(42)
print(3.14)
print("Name:", "Alice")
```

**Precision**
- **Definition**: Number of digits after decimal point
- **Example**: `:.2f` (2 decimal places)
- **Related terms**: Format Specification, Decimal Places
```python
pi = 3.141592653589793
print(f"Pi: {pi:.2f}")  # 3.14
print(f"Pi: {pi:.4f}")  # 3.1416
print(f"Pi: {pi:.0f}")  # 3
```

### R

**Raw String**
- **Definition**: String with r prefix ignoring escape sequences
- **Example**: `r"C:\new\folder"`
- **Related terms**: Escape Sequence, Backslash, String Literal
```python
# Regular string - interprets escape sequences
print("C:\new\folder")  # C:
                        # ew
                        # older

# Raw string - literal backslashes
print(r"C:\new\folder")  # C:\new\folder
```

### S

**sep (Separator)**
- **Definition**: String placed between print() values
- **Example**: `sep=", "` or `sep="-"`
- **Related terms**: print(), Parameter, Delimiter
```python
# Default separator (space)
print("a", "b", "c")  # a b c

# Custom separators
print("a", "b", "c", sep=", ")  # a, b, c
print("2024", "01", "15", sep="-")  # 2024-01-15
print("a", "b", "c", sep="")  # abc
```

**String Concatenation**
- **Definition**: Joining strings using + operator
- **Example**: `"Hello" + " " + "World"`
- **Related terms**: + Operator, String, Join
```python
# String concatenation
first = "Hello"
second = "World"
result = first + " " + second
print(result)  # Hello World
```

**String Formatting**
- **Definition**: Embedding values in strings
- **Example**: f-strings, str.format(), % formatting
- **Related terms**: f-string, format(), % Operator
```python
name = "Alice"
age = 25

# f-string (recommended)
print(f"Name: {name}, Age: {age}")

# str.format()
print("Name: {}, Age: {}".format(name, age))

# % formatting (old style)
print("Name: %s, Age: %d" % (name, age))
```

### T

**Tab Character**
- **Definition**: Character that moves cursor to next tab stop
- **Example**: `\t`
- **Related terms**: Escape Sequence, Whitespace, Alignment
```python
# Using tabs for alignment
print("Name\tAge\tCity")
print("Alice\t25\tNew York")
print("Bob\t30\tBoston")
# Output:
# Name    Age     City
# Alice   25      New York
# Bob     30      Boston
```

### W

**Width**
- **Definition**: Minimum number of characters in formatted output
- **Example**: `{:10}` (10 characters minimum)
- **Related terms**: Format Specification, Alignment, Padding
```python
name = "Alice"
print(f"{'Name':<10}")  # "Name      "
print(f"{name:<10}")    # "Alice     "
print(f"{name:>10}")    # "     Alice"
print(f"{name:^10}")    # "  Alice   "
print(f"{name:*^10}")   # "**Alice***"
```

## Key Concepts Summary

### print() Function Parameters
| Parameter | Default | Description | Example |
|-----------|---------|-------------|---------|
| *objects | (required) | Values to print | `print("a", "b")` |
| sep | `' '` | Separator between values | `sep=","` |
| end | `'\n'` | End character | `end=" "` |
| file | `sys.stdout` | Output destination | `file=sys.stderr` |
| flush | `False` | Flush buffer | `flush=True` |

### String Formatting Methods
| Method | Syntax | Version | Example |
|--------|--------|---------|---------|
| f-string | `f"...{expr}"` | 3.6+ | `f"Name: {name}"` |
| str.format() | `"...{}".format()` | 2.6+ | `"Name: {}".format(name)` |
| % formatting | `"..." % values` | All | `"Name: %s" % name` |

### Format Specifications
| Spec | Description | Example | Output |
|------|-------------|---------|--------|
| `:.2f` | 2 decimal places | `{3.14:.2f}` | `3.14` |
| `:,` | With commas | `{1234:,}` | `1,234` |
| `:<10` | Left align | `{'hi':<10}` | `hi        ` |
| `:>10` | Right align | `{'hi':>10}` | `        hi` |
| `:^10` | Center align | `{'hi':^10}` | `    hi    ` |
| `:.1%` | Percentage | `{0.75:.1%}` | `75.0%` |
| `:.2e` | Scientific | `{1234:.2e}` | `1.23e+03` |

### Escape Sequences Reference
| Sequence | Description | Example |
|----------|-------------|---------|
| `\n` | Newline | `"Line1\nLine2"` |
| `\t` | Tab | `"Name\tAge"` |
| `\\` | Backslash | `"C:\\path"` |
| `\"` | Double quote | `"He said \"Hi\""` |
| `\'` | Single quote | `'It\'s'` |
| `\a` | Alert/bell | `"\a"` |
| `\b` | Backspace | `"Hello\bWorld"` |
| `\r` | Carriage return | `"Hello\rHi"` |
| `\0` | Null | `"\0"` |

## Practice Terms

Match these terms to their definitions:
1. f-string - ?
2. sep - ?
3. end - ?
4. escape sequence - ?
5. raw string - ?

**Answers:**
1. String with embedded expressions using f prefix
2. Separator between print() values
3. Character to end print() output
4. Special character representation (\n, \t, etc.)
5. String ignoring escape sequences (r prefix)