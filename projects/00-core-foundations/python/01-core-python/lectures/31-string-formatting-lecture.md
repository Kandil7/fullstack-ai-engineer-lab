# String Formatting in Python

## Topic 31: Creating Dynamic Strings

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use the `%` operator for old-style formatting
2. Use `str.format()` method for positional and keyword arguments
3. Master f-strings (formatted string literals) - the modern approach
4. Apply format specifications for numbers, alignment, and precision
5. Use Template strings for simple substitution
6. Choose the right formatting method for each situation

---

## 1. Why String Formatting?

String formatting allows you to **embed dynamic values** into strings.

```python
name = "Alice"
age = 30

# Without formatting - manual concatenation
message = "Hello, " + name + "! You are " + str(age) + " years old."

# With formatting - cleaner and more readable
message = f"Hello, {name}! You are {age} years old."
```

---

## 2. %-Formatting (Old Style)

The original Python string formatting method (C-style).

### Basic Syntax

```python
# %s - string
# %d - integer
# %f - float
# %x - hexadecimal
# %o - octal

name = "Alice"
age = 30
price = 19.99

# Basic substitution
print("Hello, %s!" % name)  # Hello, Alice!

# Multiple values
print("%s is %d years old" % (name, age))  # Alice is 30 years old

# Float formatting
print("Price: $%.2f" % price)  # Price: $19.99
```

### Format Specifiers

```python
# Width and alignment
print("%10s" % "hi")       #         hi (right-aligned, width 10)
print("%-10s" % "hi")      # hi         (left-aligned, width 10)
print("%010d" % 42)        # 0000000042 (zero-padded)

# Precision
print("%.3f" % 3.14159)    # 3.142
print("%.10s" % "Hello World")  # Hello Worl (truncated)

# Named placeholders
print("%(name)s is %(age)d" % {"name": "Alice", "age": 30})
```

### Limitations

```python
# BAD - complex expressions don't work well
# print("%s" % (name.upper(),))  # Need tuple wrapper

# GOOD - f-strings handle this better
print(f"{name.upper()}")
```

---

## 3. str.format() Method

More powerful and flexible than %-formatting.

### Basic Usage

```python
# Positional arguments
print("Hello, {}!".format("Alice"))  # Hello, Alice!
print("{} is {} years old".format("Alice", 30))

# Multiple values
print("{0} {1} {0}".format("hello", "world"))  # hello world hello

# Named arguments
print("{name} is {age}".format(name="Alice", age=30))

# Using variables
name = "Alice"
age = 30
print("{name} is {age}".format(name=name, age=age))
```

### Accessing Attributes and Items

```python
# Object attributes
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print("{0.name} is {0.age}".format(p))  # Alice is 30

# Dictionary items
data = {"name": "Alice", "age": 30}
print("{name} is {age}".format(**data))  # Alice is 30
```

### Format Specifications

```python
# Width
print("{:10}".format("hi"))      #         hi
print("{:<10}".format("hi"))     # hi
print("{:>10}".format("hi"))     #         hi
print("{:^10}".format("hi"))     #     hi

# Fill character
print("{:*=10}".format("hi"))    # ********hi
print("{:.<10}".format("hi"))    # hi........

# Number formatting
print("{:.2f}".format(3.14159))  # 3.14
print("{:,}".format(1000000))    # 1,000,000
print("{:.2%}".format(0.15))     # 15.00%
print("{:b}".format(10))         # 1010 (binary)
print("{:x}".format(255))        # ff (hex)
```

---

## 4. F-Strings (Formatted String Literals)

**The modern, preferred approach** (Python 3.6+).

### Basic Syntax

```python
name = "Alice"
age = 30

# Simple substitution
print(f"Hello, {name}!")  # Hello, Alice!

# Expressions
print(f"Next year you'll be {age + 1}")  # Next year you'll be 31

# Function calls
print(f"Name upper: {name.upper()}")  # Name upper: ALICE

# Format specifications
print(f"Pi is approximately {3.14159:.2f}")  # Pi is approximately 3.14
```

### Multi-line F-Strings

```python
# Using triple quotes
message = f"""
Hello, {name}!
You are {age} years old.
Double age: {age * 2}
"""
print(message)

# Backslash restriction
# f"New line: {name\n}"  # SyntaxError - no backslashes in expressions
# Use temporary variable instead
nl = "\n"
print(f"New line:{nl}")
```

### Debugging with F-Strings

```python
# = specifier shows expression and value
name = "Alice"
age = 30
print(f"{name=}")        # name='Alice'
print(f"{age=}")         # age=30
print(f"{age * 2=}")     # age * 2=60

# Great for debugging
def calculate(x, y):
    result = x + y
    print(f"{x=}, {y=}, {result=}")
    return result
```

### Conversion Flags

```python
# !s - str()
# !r - repr()
# !a - ascii()

print(f"{name!s}")   # Alice
print(f"{name!r}")   # 'Alice'
print(f"{'hello'!r}")  # 'hello'

# Useful for debugging strings with special characters
text = "Hello\nWorld"
print(f"{text!r}")   # 'Hello\nWorld'
```

---

## 5. Format Specification Mini-Language

### Syntax

```
[[fill]align][sign][#][0][width][grouping][.precision][type]
```

### Alignment Options

```python
# < left-align
# > right-align
# ^ center-align
# = pad after sign

print(f"{'left':<10}|")     # left      |
print(f"{'right':>10}|")    #      right|
print(f"{'center':^10}|")   #   center  |
print(f"{'pad':*^10}|")     # ***pad****|

# With numbers
print(f"{42:>10}")          #         42
print(f"{42:<10}")          # 42
print(f"{42:^10}")          #    42
```

### Number Formatting

```python
# Integer
print(f"{1234567:,}")       # 1,234,567
print(f"{1234567:_}")       # 1_234_567

# Float precision
print(f"{3.14159:.2f}")     # 3.14
print(f"{3.14159:.4f}")     # 3.1416

# Scientific notation
print(f"{123456:.2e}")      # 1.23e+05

# Percentage
print(f"{0.15:.1%}")        # 15.0%
print(f"{0.15:.2%}")        # 15.00%

# Binary, Octal, Hex
print(f"{42:b}")            # 101010
print(f"{42:o}")            # 52
print(f"{42:x}")            # 2a
print(f"{42:#x}")           # 0x2a
print(f"{42:#b}")           # 0b101010
```

### Sign and Padding

```python
# Sign options
print(f"{42:+d}")           # +42
print(f"{-42:+d}")          # -42
print(f"{42: d}")           #  42 (space for positive)

# Zero-padding
print(f"{42:05d}")          # 00042
print(f"{-42:05d}")         # -0042
print(f"{42:+06d}")         # +00042
```

---

## 6. Template Strings

Simple substitution using `string.Template`.

```python
from string import Template

# Basic usage
t = Template("Hello, $name!")
print(t.substitute(name="Alice"))  # Hello, Alice!

# With dictionary
data = {"name": "Alice", "age": 30}
t = Template("$name is $age years old")
print(t.safe_substitute(data))  # Alice is 30 years old

# Delimiter customization
t = Template("Hello, ${name}!")
print(t.substitute({"name": "Alice"}))  # Hello, Alice!
```

### When to Use Templates

```python
# GOOD - user-provided templates (safer)
user_template = Template("Dear $customer, your order $order_id is ready")
result = user_template.safe_substitute(
    customer="Alice",
    order_id="12345"
)

# NOT recommended - f-strings are more powerful for code
# But templates are safer when formatting user-supplied patterns
```

---

## 7. Comparison Table

| Feature | %-formatting | str.format() | F-strings |
|---------|--------------|--------------|-----------|
| **Syntax** | `"Hello %s" % name` | `"Hello {}".format(name)` | `f"Hello {name}"` |
| **Readability** | Low | Medium | High |
| **Performance** | Fast | Slower | Fastest |
| **Debugging** | Manual | Manual | Built-in (`=`) |
| **Complex expressions** | Limited | Limited | Full support |
| **Python version** | All | 2.6+ | 3.6+ |

---

## 8. Common Mistakes to Avoid

### 1. Forgetting the `f` Prefix

```python
name = "Alice"
# BAD - treats as literal text
print("Hello {name}")  # Hello {name}

# GOOD - includes f prefix
print(f"Hello {name}")  # Hello Alice
```

### 2. Quote Mismatch

```python
name = "Alice"
# BAD - quotes conflict
# print(f"Hello " + name + "!")

# GOOD - use different quotes
print(f'Hello {name}!')
print(f"Hello {name}!")
```

### 3. Escaping Issues in F-Strings

```python
# BAD - backslashes not allowed in expressions
# print(f"Newline: {name\n}")  # SyntaxError

# GOOD - use variable or different approach
nl = "\n"
print(f"Newline:{nl}")
```

### 4. Overcomplicating Expressions

```python
name = "Alice"
age = 30

# BAD - too complex inside f-string
# result = f"{'Adult' if age >= 18 else 'Minor'}: {name.upper().strip()}"

# GOOD - extract to variable
status = "Adult" if age >= 18 else "Minor"
clean_name = name.upper().strip()
result = f"{status}: {clean_name}"
```

---

## 9. Best Practices

1. **Use f-strings** as your default - they're fast and readable
2. **Use `=` for debugging** - `print(f"{variable=}")`
3. **Keep expressions simple** in f-strings
4. **Use `:` for formatting** - `f"{value:.2f}"`
5. **Use templates** when formatting user-provided patterns
6. **Use `repr()`** (`!r`) for debugging strings
7. **Be consistent** - pick one style for your project

---

## 10. Practice Exercises

### Exercise 1: Receipt Generator

```python
def generate_receipt(items, tax_rate=0.08):
    """Generate a formatted receipt."""
    print("=" * 40)
    print(f"{'ITEMS':^40}")
    print("=" * 40)
    
    subtotal = 0
    for item, price, qty in items:
        total = price * qty
        subtotal += total
        print(f"{item:<25} {qty:>2} x ${price:>6.2f} = ${total:>8.2f}")
    
    print("-" * 40)
    tax = subtotal * tax_rate
    grand_total = subtotal + tax
    
    print(f"{'Subtotal:':<30} ${subtotal:>8.2f}")
    print(f"{'Tax (8%):':<30} ${tax:>8.2f}")
    print(f"{'TOTAL:':<30} ${grand_total:>8.2f}")
    print("=" * 40)

# Test
items = [
    ("Widget", 9.99, 2),
    ("Gadget", 24.99, 1),
    ("Thingamajig", 4.99, 3)
]
generate_receipt(items)
```

### Exercise 2: Data Table Formatter

```python
def format_table(headers, rows, col_widths=None):
    """Format data as a nice table."""
    if col_widths is None:
        col_widths = [max(len(str(h)), max(len(str(r[i])) for r in rows)) 
                      for i, h in enumerate(headers)]
    
    # Header
    header_line = " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
    separator = "-+-".join("-" * w for w in col_widths)
    
    print(header_line)
    print(separator)
    
    # Rows
    for row in rows:
        row_line = " | ".join(f"{str(v):<{w}}" for v, w in zip(row, col_widths))
        print(row_line)

# Test
headers = ["Name", "Age", "City"]
rows = [
    ["Alice", 30, "New York"],
    ["Bob", 25, "Boston"],
    ["Charlie", 35, "Chicago"]
]
format_table(headers, rows)
```

### Exercise 3: Number Formatter

```python
def format_number(value, style="default"):
    """Format numbers in various styles."""
    formats = {
        "default": f"{value:,}",
        "currency": f"${value:,.2f}",
        "percent": f"{value:.1%}",
        "scientific": f"{value:.2e}",
        "binary": f"{value:#b}",
        "hex": f"{value:#x}",
        "padded": f"{value:010d}",
    }
    
    return formats.get(style, f"{value}")

# Test
print(format_number(1234567))        # 1,234,567
print(format_number(1234.56, "currency"))  # $1,234.56
print(format_number(0.15, "percent"))       # 15.0%
print(format_number(1234567, "scientific")) # 1.23e+06
print(format_number(255, "hex"))            # 0xff
```

---

## 11. Summary

| Method | Syntax | Best For |
|--------|--------|----------|
| **%** | `"Hello %s" % name` | Legacy code |
| **str.format()** | `"Hello {}".format(name)` | Python 2.6+ compat |
| **F-strings** | `f"Hello {name}"` | Modern Python (3.6+) |
| **Template** | `Template("$name").substitute()` | User patterns |

### Key Points

- **F-strings** are the fastest and most readable
- Use **`=`** for debugging: `f"{x=}"`
- Use **format specifiers** for numbers: `f"{x:.2f}"`
- **Templates** are safest for user-provided formats
- Keep **expressions simple** inside formatting

---

## Next Steps

- Learn about internationalization (i18n) with string formatting
- Explore format specification for dates and times
- Study custom formatters for complex objects
