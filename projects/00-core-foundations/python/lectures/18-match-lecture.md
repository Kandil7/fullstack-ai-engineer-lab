# Python Match Statements — Lecture 18

## Topic Overview

The `match` statement, introduced in **Python 3.10** (PEP 634), provides **structural pattern matching** — a powerful way to compare a value against multiple patterns and execute code based on which pattern matches. Unlike `if/elif` chains, match statements can destructure data, match sequences, and apply guards.

Think of it as a supercharged switch statement that can match against complex data structures, not just simple values.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Understand the syntax and structure of match/case statements
- Match against literal values, sequences, and mappings
- Use capture patterns to extract values
- Apply guards (if conditions) to patterns
- Use wildcard patterns for default cases
- Destructure complex data structures
- Understand when to use match vs. if/elif

---

## Key Concepts

### 1. Basic Syntax

```python
# match statement structure
match subject:
    case pattern1:
        # code if pattern1 matches
    case pattern2:
        # code if pattern2 matches
    case _:
        # default case (wildcard)
```

### 2. Literal Patterns

```python
# Match against specific values
def http_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return f"Unknown: {status}"

print(http_status(200))  # OK
print(http_status(418))  # Unknown: 418

# Multiple literals with | (OR pattern)
match status:
    case 400 | 401 | 403:
        return "Client error"
    case 500 | 502 | 503:
        return "Server error"
```

### 3. Capture Patterns

```python
# Capture the matched value into a variable
def describe(value):
    match value:
        case int():
            print(f"Integer: {value}")
        case float():
            print(f"Float: {value}")
        case str():
            print(f"String: {value}")
        case list():
            print(f"List of {len(value)} items")

describe(42)           # Integer: 42
describe(3.14)         # Float: 3.14
describe("hello")      # String: hello
describe([1, 2, 3])    # List of 3 items
```

### 4. Class Patterns

```python
# Match against class types
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def classify_point(point):
    match point:
        case Point(x=0, y=0):
            return "Origin"
        case Point(x=0, y=y):
            return f"On Y-axis at {y}"
        case Point(x=x, y=0):
            return f"On X-axis at {x}"
        case Point(x=x, y=y) if x == y:
            return f"On diagonal at ({x}, {y})"
        case Point(x=x, y=y):
            return f"Point at ({x}, {y})"

print(classify_point(Point(0, 0)))      # Origin
print(classify_point(Point(0, 5)))      # On Y-axis at 5
print(classify_point(Point(3, 3)))      # On diagonal at (3, 3)
print(classify_point(Point(2, 4)))      # Point at (2, 4)
```

### 5. Sequence Patterns

```python
# Match against lists/tuples
def describe_list(items):
    match items:
        case []:
            print("Empty list")
        case [x]:
            print(f"Single item: {x}")
        case [x, y]:
            print(f"Two items: {x} and {y}")
        case [x, *rest]:
            print(f"First: {x}, rest: {rest}")

describe_list([])              # Empty list
describe_list([42])            # Single item: 42
describe_list([1, 2])          # Two items: 1 and 2
describe_list([1, 2, 3, 4])    # First: 1, rest: [2, 3, 4]

# Tuple matching
def process_point(point):
    match point:
        case (0, 0):
            return "Origin"
        case (x, 0):
            return f"X-axis: {x}"
        case (0, y):
            return f"Y-axis: {y}"
        case (x, y):
            return f"Point: ({x}, {y})"

print(process_point((0, 0)))  # Origin
print(process_point((5, 0)))  # X-axis: 5
print(process_point((3, 4)))  # Point: (3, 4)
```

### 6. Mapping Patterns (Dictionaries)

```python
# Match against dictionaries
def handle_event(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            print(f"Click at ({x}, {y})")
        case {"type": "keypress", "key": key}:
            print(f"Key pressed: {key}")
        case {"type": "scroll", "direction": dir}:
            print(f"Scrolling {dir}")
        case {"type": unknown}:
            print(f"Unknown event type: {unknown}")
        case _:
            print("Invalid event")

handle_event({"type": "click", "x": 100, "y": 200})   # Click at (100, 200)
handle_event({"type": "keypress", "key": "enter"})      # Key pressed: enter
handle_event({"type": "scroll", "direction": "up"})     # Scrolling up

# Extra keys are ignored
handle_event({"type": "click", "x": 10, "y": 20, "button": "left"})
# Click at (10, 20)
```

### 7. Guards (If Conditions)

```python
# Add conditions to patterns
def categorize_number(n):
    match n:
        case x if x < 0:
            return f"Negative: {x}"
        case x if x == 0:
            return "Zero"
        case x if x % 2 == 0:
            return f"Positive even: {x}"
        case x:
            return f"Positive odd: {x}"

print(categorize_number(-5))  # Negative: -5
print(categorize_number(0))   # Zero
print(categorize_number(4))   # Positive even: 4
print(categorize_number(7))   # Positive odd: 7
```

### 8. Complex Nested Patterns

```python
# Nested pattern matching
def process_command(command):
    match command:
        case ["quit"]:
            return "Exiting"
        case ["help", topic]:
            return f"Help for: {topic}"
        case ["move", direction, steps] if steps > 0:
            return f"Moving {direction} by {steps} steps"
        case ["set", key, value]:
            return f"Setting {key} = {value}"
        case ["get", key]:
            return f"Getting {key}"
        case _:
            return f"Unknown command: {command}"

print(process_command(["quit"]))                        # Exiting
print(process_command(["help", "python"]))              # Help for: python
print(process_command(["move", "north", 5]))            # Moving north by 5 steps
print(process_command(["set", "color", "red"]))         # Setting color = red
print(process_command(["delete", "file.txt"]))          # Unknown command: [...]
```

---

## Code Examples

### Example 1: JSON Parser Helper

```python
def parse_json_value(value):
    match value:
        case None:
            return "null"
        case bool():
            return "true" if value else "false"
        case int() | float():
            return str(value)
        case str():
            return f'"{value}"'
        case list():
            items = ", ".join(parse_json_value(item) for item in value)
            return f"[{items}]"
        case dict():
            pairs = ", ".join(f'"{k}": {parse_json_value(v)}' for k, v in value.items())
            return f"{{{pairs}}}"
        case _:
            return str(value)

print(parse_json_value(None))              # null
print(parse_json_value(True))              # true
print(parse_json_value(42))                # 42
print(parse_json_value("hello"))           # "hello"
print(parse_json_value([1, "two", None]))  # [1, "two", null]
```

### Example 2: State Machine

```python
def process_state(state, action):
    match (state, action):
        case ("idle", "start"):
            return "running"
        case ("running", "pause"):
            return "paused"
        case ("running", "stop"):
            return "idle"
        case ("paused", "resume"):
            return "running"
        case ("paused", "stop"):
            return "idle"
        case _:
            return state  # No change

print(process_state("idle", "start"))    # running
print(process_state("running", "pause")) # paused
print(process_state("paused", "stop"))   # idle
```

### Example 3: Data Validation

```python
def validate_user(data):
    match data:
        case {"name": str(name), "age": int(age), "email": str(email)}:
            if age < 0 or age > 150:
                return "Invalid age"
            if "@" not in email:
                return "Invalid email"
            return f"Valid user: {name}"
        case {"name": _}:
            return "Missing age or email"
        case _:
            return "Invalid data format"

print(validate_user({"name": "Alice", "age": 30, "email": "alice@test.com"}))
# Valid user: Alice
print(validate_user({"name": "Bob"}))
# Missing age or email
print(validate_user("invalid"))
# Invalid data format
```

### Example 4: AST Node Processing

```python
# Simulating expression evaluation
class Number:
    def __init__(self, value):
        self.value = value

class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

def evaluate(expr):
    match expr:
        case Number(value=v):
            return v
        case Add(left=l, right=r):
            return evaluate(l) + evaluate(r)
        case Multiply(left=l, right=r):
            return evaluate(l) * evaluate(r)
        case _:
            raise ValueError(f"Unknown expression: {expr}")

# (3 + 4) * 5
expr = Multiply(Add(Number(3), Number(4)), Number(5))
print(evaluate(expr))  # 35
```

---

## Common Mistakes to Avoid

### Mistake 1: Using match Before Python 3.10
```python
# match is only available in Python 3.10+
# Check your Python version: python --version

# For older Python, use if/elif
import sys
if sys.version_info >= (3, 10):
    # Can use match
    pass
else:
    # Must use if/elif
    pass
```

### Mistake 2: Forgetting the Colon
```python
# WRONG
# match value
#     case 1:
#         print("one")

# CORRECT
match value:
    case 1:
        print("one")
```

### Mistake 3: Confusing Capture with Value Patterns
```python
# This captures ANY value into variable 'x'
match value:
    case x:
        print(f"Captured: {x}")

# To match a specific value, use the value directly
match value:
    case 42:
        print("It's 42!")
```

### Mistake 4: Not Using Wildcard for Default
```python
# If no wildcard, unmatched values do nothing
match value:
    case 1:
        print("one")
    # No default — silently ignores other values

# Always add wildcard for completeness
match value:
    case 1:
        print("one")
    case _:
        print("something else")
```

---

## Best Practices

1. **Use match for complex pattern matching** — if/elif is simpler for basic equality checks
2. **Always include a wildcard case** `_` for unexpected values
3. **Use capture patterns** to extract values cleanly
4. **Add guards** for conditions that depend on captured values
5. **Use OR patterns** `|` to group related cases
6. **Keep patterns readable** — don't make them too complex
7. **Consider match** for state machines, event handling, and AST processing
8. **Use `as` keyword** to capture while matching a pattern: `case Point() as p:`

---

## Practice Exercises

### Exercise 1: Color Parser
Write a function that parses color strings ("red", "rgb(255,0,0)", "#FF0000") into normalized RGB tuples.

```python
def parse_color(color_str):
    # Your code here using match
    pass

# Expected: (255, 0, 0)
print(parse_color("red"))
print(parse_color("rgb(255, 0, 0)"))
print(parse_color("#FF0000"))
```

### Exercise 2: Shape Area Calculator
Write a function that calculates the area of different shapes given as tuples: ("circle", radius), ("rectangle", width, height), ("triangle", base, height).

```python
def shape_area(shape):
    import math
    # Your code here using match
    pass

# Expected: ~78.54
print(shape_area(("circle", 5)))
print(shape_area(("rectangle", 4, 6)))
print(shape_area(("triangle", 3, 8)))
```

### Exercise 3: Calculator
Write a function that evaluates expressions given as tuples: ("add", a, b), ("multiply", a, b), ("power", a, b).

```python
def calculate(expr):
    # Your code here using match
    pass

# Expected: 8
print(calculate(("add", 3, 5)))
print(calculate(("multiply", 4, 7)))
print(calculate(("power", 2, 10)))
```

---

## Summary

- **Match statements** (Python 3.10+) provide structural pattern matching
- **Literal patterns**: match against specific values
- **Capture patterns**: extract values into variables
- **Class patterns**: match against object types and attributes
- **Sequence patterns**: match lists/tuples with destructuring
- **Mapping patterns**: match dictionaries with key-value patterns
- **OR patterns**: `case 1 | 2 | 3:` matches multiple values
- **Guards**: `case x if x > 0:` add conditions to patterns
- **Wildcard**: `case _:` matches anything (default case)
- More powerful than if/elif for complex data matching
