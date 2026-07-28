# Python Match Statements — Glossary 18

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| Match | Structural pattern matching keyword | `match value:` |
| Case | Pattern in a match statement | `case 1:` |
| Literal Pattern | Matches a specific value | `case 42:` |
| Capture Pattern | Captures matched value into variable | `case x:` |
| Class Pattern | Matches against a class type | `case Point(x, y):` |
| Sequence Pattern | Matches lists/tuples | `case [a, b, *rest]:` |
| Mapping Pattern | Matches dictionaries | `case {"key": value}:` |
| Wildcard Pattern | Matches anything (default) | `case _:` |
| OR Pattern | Matches multiple patterns | `case 1 \| 2 \| 3:` |
| Guard | Additional if condition on a case | `case x if x > 0:` |
| As Pattern | Captures while matching | `case Point() as p:` |
| Star Pattern | Captures remaining items | `case [first, *rest]:` |
| Keyword Pattern | Matches class attribute values | `case Point(x=0):` |
| Positional Pattern | Matches by position in class | `case Point(0, y):` |
| Open Pattern | Matches with any remaining args | `case Point(_, y):` |
| Value Pattern | Matches a named constant | `case RED:` |
| Host Subject | The value being matched | `match subject:` |
| PEP 634 | Python Enhancement Proposal for match | Python 3.10+ |
| Structural Matching | Pattern matching with destructuring | `case [x, y]:` |
| Exhaustive Matching | All cases covered | Always include `case _:` |

---

## Definitions

### As Pattern
**Definition**: A pattern that captures the matched value into a variable while also matching against a sub-pattern. Uses the `as` keyword.

**Example**:
```python
match command:
    case ["quit"] as cmd:
        print(f"Got quit command: {cmd}")
    case ["move", str(direction)] as cmd:
        print(f"Moving command: {cmd}")
```

**Related**: capture pattern, case, as keyword

---

### Case
**Definition**: A keyword that defines a pattern to match against the subject of a `match` statement. Each case contains a pattern and an indented block of code.

**Example**:
```python
match day:
    case "Monday":
        print("Start of week")
    case "Friday":
        print("TGIF!")
    case str() as d:
        print(f"Another day: {d}")
```

**Related**: `match`, pattern, guard, wildcard

---

### Capture Pattern
**Definition**: A pattern that captures the matched value into a variable. The variable name becomes a binding that can be used in the case body and guard.

**Example**:
```python
match value:
    case int():
        print(f"Got integer: {value}")  # 'value' captures the int
    case str(text):
        print(f"Got string: {text}")    # 'text' captures the string
```

**Related**: as pattern, binding, variable capture

---

### Class Pattern
**Definition**: A pattern that matches against an object's class and optionally its attributes. Can use keyword or positional arguments.

**Example**:
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

match point:
    case Point(x=0, y=0):
        print("Origin")
    case Point(x=x, y=y) if x == y:
        print(f"Diagonal: {x}")
    case Point(x, y):
        print(f"General point: ({x}, {y})")
```

**Related**: keyword pattern, positional pattern, data classes

---

### Guard
**Definition**: An additional `if` condition appended to a `case` pattern. The case only matches if the pattern matches AND the guard condition is true.

**Example**:
```python
match number:
    case int(n) if n > 0:
        print(f"Positive: {n}")
    case int(n) if n < 0:
        print(f"Negative: {n}")
    case int():
        print("Zero")
```

**Related**: `case`, condition, if clause

---

### Host Subject
**Definition**: The expression or value that appears after the `match` keyword. This is the value that all subsequent `case` patterns are compared against.

**Example**:
```python
# 'color' is the host subject
color = "red"
match color:
    case "red":
        print("Stop")
    case "green":
        print("Go")
```

**Related**: `match`, expression, value being matched

---

### Keyword Pattern
**Definition**: A pattern in a class match that specifies attribute names and their expected values. Uses `ClassName(attr=value)` syntax.

**Example**:
```python
match event:
    case {"type": "click", "x": x, "y": y}:
        print(f"Click at ({x}, {y})")

match point:
    case Point(x=0, y=y):
        print(f"On Y-axis at {y}")
```

**Related**: class pattern, positional pattern, mapping pattern

---

### Literal Pattern
**Definition**: A pattern that matches against a specific literal value (number, string, boolean, None).

**Example**:
```python
match status:
    case 200:
        return "OK"
    case 404:
        return "Not Found"
    case "success":
        return "It worked!"
    case None:
        return "No data"
    case True:
        return "Confirmed"
```

**Related**: constant, value matching, `case`

---

### Mapping Pattern
**Definition**: A pattern that matches against dictionary-like objects using `{key: pattern}` syntax. Extra keys are ignored.

**Example**:
```python
match data:
    case {"name": str(name), "age": int(age)}:
        print(f"{name} is {age}")
    case {"error": msg}:
        print(f"Error: {msg}")
    case {}:
        print("Empty dict")
```

**Related**: dictionary, key-value matching, structural matching

---

### Match
**Definition**: A keyword (Python 3.10+) that begins a structural pattern matching block. The expression after `match` is compared against each `case` pattern in order.

**Example**:
```python
def describe(value):
    match value:
        case int():
            return "integer"
        case str():
            return "string"
        case list():
            return "list"
        case _:
            return "unknown"
```

**Related**: `case`, PEP 634, pattern matching, Python 3.10

---

### Open Pattern
**Definition**: A pattern that matches a class instance without specifying all attributes. Uses `ClassName(*, attr=value)` or just `ClassName()` for any instance.

**Example**:
```python
match point:
    case Point(x=0):       # Matches any Point where x=0
        print("On Y-axis")
    case Point():           # Matches any Point
        print(f"Any point")
```

**Related**: class pattern, keyword pattern

---

### OR Pattern
**Definition**: A pattern that matches if any of the specified sub-patterns match. Uses the `|` (pipe) separator.

**Example**:
```python
match status:
    case 200 | 201 | 202:
        return "Success"
    case 400 | 401 | 403:
        return "Client error"
    case 500 | 502 | 503:
        return "Server error"

match command:
    case "quit" | "exit" | "q":
        return "Exiting"
```

**Related**: case, alternative patterns, pipe separator

---

### PEP 634
**Definition**: Python Enhancement Proposal that introduced structural pattern matching to Python 3.10. Defines the syntax and semantics for `match` and `case` statements.

**Example**:
```python
# PEP 634 introduced:
match subject:
    case pattern1:  # Structural pattern matching
        ...
    case pattern2:
        ...
```

**Related**: Python 3.10, match, case, pattern matching

---

### Positional Pattern
**Definition**: A pattern in a class match that specifies attribute values by their position rather than by name. Uses `ClassName(arg1, arg2)` syntax.

**Example**:
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

match point:
    case Point(0, 0):
        print("Origin")
    case Point(x, 0):
        print(f"X-axis: {x}")
    case Point(0, y):
        print(f"Y-axis: {y}")
```

**Related**: keyword pattern, class pattern, attribute matching

---

### Star Pattern
**Definition**: A pattern using `*` that captures remaining items in a sequence into a list. Used in sequence patterns.

**Example**:
```python
match items:
    case [first, *rest]:
        print(f"First: {first}, Rest: {rest}")
    case []:
        print("Empty")

match items:
    case [*_, last]:
        print(f"Last item: {last}")
    case []:
        print("Empty")
```

**Related**: sequence pattern, unpacking, *args

---

### Structural Matching
**Definition**: Pattern matching that goes beyond simple value comparison to destructure and match against the structure of data (lists, dicts, objects).

**Example**:
```python
# Simple value matching
match x:
    case 1:  # Just checks if x == 1

# Structural matching
match data:
    case [1, [2, 3]]:  # Matches structure: list starting with 1, containing [2, 3]
```

**Related**: match, case, destructuring, pattern

---

### Value Pattern
**Definition**: A pattern that matches against a named constant or variable. The name must be a dotted path to avoid confusion with capture patterns.

**Example**:
```python
RED = "red"
GREEN = "green"
BLUE = "blue"

match color:
    case RED:
        print("Stop")
    case GREEN:
        print("Go")
    case BLUE:
        print("Sky")
```

**Related**: literal pattern, named constant, dotted name

---

### Wildcard Pattern
**Definition**: The `_` pattern that matches anything without capturing the value. Used as the default/catch-all case.

**Example**:
```python
match command:
    case "quit":
        return "Exiting"
    case "help":
        return "Help text"
    case _:
        return f"Unknown command: {command}"

# Multiple wildcards in sequence
match items:
    case [first, _, last]:  # Middle item ignored
        print(f"First: {first}, Last: {last}")
```

**Related**: default case, catch-all, underscore

---

## Code Examples

### Example 1: Command Parser
```python
def parse_command(command):
    match command.split():
        case ["quit"]:
            return ("exit",)
        case ["help", topic]:
            return ("help", topic)
        case ["move", direction, str(steps)] if steps.isdigit():
            return ("move", direction, int(steps))
        case ["set", key, "=", value]:
            return ("set", key, value)
        case _:
            return ("unknown", command)

print(parse_command("quit"))              # ('exit',)
print(parse_command("help python"))       # ('help', 'python')
print(parse_command("move north 5"))      # ('move', 'north', 5)
print(parse_command("set color = red"))   # ('set', 'color', 'red')
```

### Example 2: JSON Schema Validator
```python
def validate_schema(data, schema):
    match (data, schema):
        case (int(), "integer"):
            return True
        case (str(), "string"):
            return True
        case (list(), "array"):
            return True
        case (dict(), {"type": "object", "required": keys}):
            return all(k in data for k in keys)
        case _:
            return False

print(validate_schema(42, "integer"))                     # True
print(validate_schema({"a": 1}, {"type": "object", "required": ["a"]}))  # True
```

---

## Related Concepts

- **Switch/Case**: Traditional multi-way branching (limited in Python before 3.10)
- **If/Elif/Else**: Simpler conditional branching
- **Pattern Matching**: Concept from functional programming languages
- **Destructuring**: Extracting values from complex data structures
- **Visitor Pattern**: OOP alternative for processing different types
- **Algebraic Data Types**: Typed patterns (more common in functional languages)
