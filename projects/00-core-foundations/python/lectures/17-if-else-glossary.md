# Python If/Else Statements — Glossary 17

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| If | Executes code when condition is True | `if x > 0:` |
| Elif | Else-if: additional condition check | `elif x == 0:` |
| Else | Catches all unmatched conditions | `else:` |
| Condition | Expression that evaluates to True or False | `x > 5`, `name == "Alice"` |
| Comparison Operator | Compares two values | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| Logical Operator | Combines boolean expressions | `and`, `or`, `not` |
| Truthy | Value that evaluates to True in boolean context | `"hello"`, `[1]`, `42` |
| Falsy | Value that evaluates to False in boolean context | `""`, `[]`, `0`, `None` |
| Ternary Expression | Inline if-else for simple assignments | `"yes" if x else "no"` |
| Chained Comparison | Multiple comparisons in one expression | `1 < x < 10` |
| Identity Test | Checks if two objects are the same instance | `x is None` |
| Membership Test | Checks if element exists in collection | `"a" in my_list` |
| Nested Conditional | if/elif/else inside another if block | `if a: if b:` |
| Short-Circuit | Logical operators stop early | `x and y` stops if x is False |
| Match Statement | Structural pattern matching (3.10+) | `match x: case 1:` |
| Case | Pattern in a match statement | `case "quit":` |
| Wildcard Pattern | Matches anything (default case) | `case _:` |
| Guard | Additional condition in a case | `case x if x > 0:` |
| Boolean Context | Where a value is evaluated as True/False | `if value:`, `while items:` |
| FizzBuzz | Classic programming problem using conditionals | Divisibility by 3 and 5 |

---

## Definitions

### And
**Definition**: A logical operator that returns `True` if both operands are `True`. Uses short-circuit evaluation — if the first operand is `False`, the second is not evaluated.

**Example**:
```python
x = 5
if x > 0 and x < 10:
    print("x is a positive single digit")

# Short-circuit: second condition not evaluated if first is False
if False and expensive_function():  # expensive_function() never called
    print("Never reached")
```

**Related**: `or`, `not`, short-circuit evaluation

---

### Boolean Context
**Definition**: A place in code where a value is interpreted as `True` or `False`. Includes `if` statements, `while` loops, `and`/`or`/`not` operators, and `bool()` function.

**Example**:
```python
# Boolean context in if statement
name = "Alice"
if name:  # "Alice" is truthy
    print("Name exists")

# Boolean context in while loop
items = [1, 2, 3]
while items:  # Non-empty list is truthy
    items.pop()

# Boolean context in and/or
result = value and "default"  # Returns value if truthy, else "default"
```

**Related**: truthy, falsy, `bool()`

---

### Case
**Definition**: A keyword used in `match` statements to define a pattern to match against. Each `case` specifies a pattern and optional guard.

**Example**:
```python
command = "quit"

match command:
    case "quit":           # Pattern: literal string
        print("Exiting")
    case "help":           # Pattern: literal string
        print("Help")
    case str() as cmd:     # Pattern: any string, captured as cmd
        print(f"Unknown: {cmd}")
```

**Related**: `match`, guard, pattern matching, wildcard

---

### Chained Comparison
**Definition**: Python allows multiple comparison operators in a single expression, connected by `and`. Equivalent to `a < b and b < c`.

**Example**:
```python
x = 5
print(1 < x < 10)      # True — (1 < 5) and (5 < 10)
print(1 < x < 3)       # False — (1 < 5) and (5 < 3)
print(1 < 2 < 3 < 4)   # True

# More complex chains
print(1 <= x <= 10 <= 100)  # True
```

**Related**: comparison operators, `and`, Pythonic style

---

### Condition
**Definition**: An expression that evaluates to `True` or `False`. Used in `if` statements, `while` loops, and logical operations to control program flow.

**Example**:
```python
x = 10
if x > 5:            # x > 5 is a condition (True)
    print("Big")

name = "Alice"
if len(name) > 3:    # len(name) > 3 is a condition (True)
    print("Long name")
```

**Related**: `if`, `elif`, `else`, boolean, expression

---

### Elif
**Definition**: A keyword (short for "else if") that adds additional conditions to an `if` chain. Checked only if all previous conditions were `False`.

**Example**:
```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:  # Only checked if score < 90
    grade = "B"
elif score >= 70:  # Only checked if score < 80
    grade = "C"
else:
    grade = "F"
```

**Related**: `if`, `else`, conditional chain

---

### Else
**Definition**: A keyword that defines a code block to execute when all preceding `if` and `elif` conditions are `False`.

**Example**:
```python
age = 15

if age >= 18:
    print("Adult")
else:  # Executes because age < 18
    print("Minor")
```

**Related**: `if`, `elif`, catch-all, default case

---

### Falsy
**Definition**: A value that evaluates to `False` in a boolean context. Python has specific falsy values that are commonly encountered.

**Example**:
```python
# All falsy values
falsy_values = [False, None, 0, 0.0, "", [], {}, set(), frozenset(), b"", range(0)]

for val in falsy_values:
    print(f"{repr(val):>10} -> {bool(val)}")
# False -> False
# None -> False
# 0 -> False
# 0.0 -> False
# '' -> False
# [] -> False
# {} -> False
# set() -> False
```

**Related**: truthy, `bool()`, boolean context

---

### Guard
**Definition**: An additional condition in a `match` case that must also be satisfied for the case to match. Written with `if` after the pattern.

**Example**:
```python
def check_value(x):
    match x:
        case int() if x > 0:
            return "Positive integer"
        case int() if x < 0:
            return "Negative integer"
        case int():
            return "Zero"
        case _:
            return "Not an integer"

print(check_value(5))   # Positive integer
print(check_value(-3))  # Negative integer
print(check_value(0))   # Zero
print(check_value("hi"))# Not an integer
```

**Related**: `match`, `case`, pattern matching

---

### Identity Test
**Definition**: An operation that checks whether two variables reference the same object in memory, using `is` or `is not`. Different from equality (`==`) which checks if values are the same.

**Example**:
```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True — same value
print(a is b)   # False — different objects
print(a is c)   # True — same object

# Always use 'is' for None
x = None
if x is None:   # Correct
    print("None")
# if x == None:  # Works but not Pythonic
```

**Related**: `is`, `is not`, `==`, `!=`, memory identity

---

### If
**Definition**: A keyword that begins a conditional block. The code inside the block executes only if the condition evaluates to `True`.

**Example**:
```python
temperature = 80

if temperature > 75:
    print("It's hot!")      # Executes
    print("Turn on AC!")    # Also executes
```

**Related**: `elif`, `else`, condition, indentation

---

### Match Statement
**Definition**: A structural pattern matching statement introduced in Python 3.10. Compares a value against multiple patterns and executes the matching case. More powerful than if/elif chains.

**Example**:
```python
def describe(command):
    match command:
        case "quit":
            return "Exiting program"
        case "help":
            return "Showing help"
        case ["move", direction]:
            return f"Moving {direction}"
        case _:
            return f"Unknown: {command}"

print(describe("quit"))           # Exiting program
print(describe(["move", "north"]))# Moving north
print(describe("foo"))            # Unknown: foo
```

**Related**: `case`, guard, pattern, wildcard, Python 3.10

---

### Membership Test
**Definition**: An operation that checks whether an element exists within a collection (list, tuple, set, string, dict), using `in` or `not in`.

**Example**:
```python
# List membership
fruits = ["apple", "banana", "cherry"]
if "apple" in fruits:
    print("We have apples!")

# String membership
if "py" in "python":
    print("Contains 'py'")

# Dict membership (checks keys)
person = {"name": "Alice", "age": 30}
if "name" in person:
    print("Has name key")

# Set membership (very fast)
valid_users = {"alice", "bob"}
if "alice" in valid_users:
    print("Valid user!")
```

**Related**: `in`, `not in`, O(1) lookup (sets)

---

### Not
**Definition**: A logical operator that inverts a boolean value. `True` becomes `False` and vice versa.

**Example**:
```python
is_active = True
if not is_active:
    print("Account is inactive")

# Double negation (confusing — avoid)
if not not True:  # True
    print("Still True")

# Useful with membership tests
if "mango" not in fruits:
    print("No mangoes!")
```

**Related**: `and`, `or`, boolean inversion

---

### Nested Conditional
**Definition**: An `if`, `elif`, or `else` block inside another conditional block. Creates hierarchical decision trees but can become hard to read if deeply nested.

**Example**:
```python
has_ticket = True
age = 20

if has_ticket:
    if age >= 18:
        print("Welcome! Enjoy the show.")
    else:
        print("Welcome! Enjoy the kids' section.")
else:
    print("Please buy a ticket first.")
```

**Related**: `if`, `elif`, `else`, flattening, early returns

---

### Or
**Definition**: A logical operator that returns `True` if at least one operand is `True`. Uses short-circuit evaluation — if the first operand is `True`, the second is not evaluated.

**Example**:
```python
age = 25
if age < 13 or age > 65:
    print("Discount!")

# Short-circuit: second not evaluated if first is True
if True or expensive_function():  # expensive_function() never called
    print("Always True")
```

**Related**: `and`, `not`, short-circuit evaluation

---

### Ternary Expression
**Definition**: A one-line conditional expression that evaluates to one of two values based on a condition. Syntax: `value_if_true if condition else value_if_false`.

**Example**:
```python
age = 20
status = "adult" if age >= 18 else "minor"
print(status)  # adult

# Nested ternary
score = 85
grade = "A" if score >= 90 else "B" if score >= 80 else "C"
print(grade)  # B

# In function arguments
print("Even" if x % 2 == 0 else "Odd")
```

**Related**: `if`/`else`, inline conditional, conditional expression

---

### Truthy
**Definition**: A value that evaluates to `True` in a boolean context. Most non-empty, non-zero values in Python are truthy.

**Example**:
```python
# Common truthy values
truthy_values = [True, 1, -1, 3.14, "hello", [1], {"a": 1}, (1,), {1}, object()]

for val in truthy_values:
    print(f"{repr(val):>20} -> {bool(val)}")
# True -> True
# 1 -> True
# -1 -> True
# 3.14 -> True
# 'hello' -> True
```

**Related**: falsy, `bool()`, boolean context

---

### Wildcard Pattern
**Definition**: The `_` pattern in a `match` statement that matches anything. Used as the default/catch-all case, similar to `else` in if/elif chains.

**Example**:
```python
def response(code):
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return f"Unknown code: {code}"

print(response(200))  # OK
print(response(418))  # Unknown code: 418
```

**Related**: `match`, `case`, default case

---

## Code Examples

### Example 1: BMI Calculator
```python
def bmi_category(weight_kg, height_m):
    bmi = weight_kg / (height_m ** 2)
    
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

print(bmi_category(70, 1.75))  # Normal weight
```

### Example 2: Tiered Pricing
```python
def calculate_price(quantity):
    if quantity < 10:
        return quantity * 10.00     # $10 each
    elif quantity < 50:
        return quantity * 8.50      # $8.50 each
    elif quantity < 100:
        return quantity * 7.00      # $7 each
    else:
        return quantity * 5.50      # $5.50 each

print(calculate_price(5))    # $50.00
print(calculate_price(25))   # $212.50
print(calculate_price(150))  # $825.00
```

### Example 3: Pattern Matching with Match Statement
```python
def handle_http_status(status):
    match status:
        case 200:
            return "Success"
        case 301 | 302:
            return "Redirect"
        case 404:
            return "Not Found"
        case 500 | 502 | 503:
            return "Server Error"
        case int() if 400 <= status < 500:
            return "Client Error"
        case _:
            return f"Unknown status: {status}"

print(handle_http_status(200))  # Success
print(handle_http_status(418))  # Client Error
```

---

## Related Concepts

- **Boolean Algebra**: AND, OR, NOT operations
- **Short-Circuit Evaluation**: Logical operators stop early
- **Truthiness**: Python's implicit boolean conversion
- **Pattern Matching**: Structural matching (Python 3.10+)
- **Early Returns**: Flattening nested conditionals
- **Guard Clauses**: Pre-conditions that exit early
