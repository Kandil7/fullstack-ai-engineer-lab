# None and Null Values in Python

## Topic 32: Understanding Python's Null Value

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what `None` is and how it differs from other languages
2. Check for `None` correctly using `is` vs `==`
3. Use `None` as default values in functions
4. Work with Optional types
5. Understand None's role in data structures
6. Implement None-safe patterns

---

## 1. What is None?

`None` is Python's way of representing the **absence of a value** or a **null value**.

```python
# None is a singleton - only one instance exists
x = None
y = None

print(x is y)      # True (same object)
print(type(None))   # <class 'NoneType'>
```

### NoneType

```python
# None is its own type
print(type(None))   # <class 'NoneType'>

# Only one None exists
print(None)         # None
```

---

## 2. Checking for None

### Use `is` not `==`

```python
x = None

# CORRECT - identity check
if x is None:
    print("x is None")

# Also correct
if x is not None:
    print("x is not None")

# AVOID - equality check (works but not Pythonic)
if x == None:
    print("Don't do this")
```

### Why `is` is Better

```python
class BadEquals:
    def __eq__(self, other):
        return True  # Always equal!

obj = BadEquals()

# Equality check fails
print(obj == None)   # True (wrong!)

# Identity check works correctly
print(obj is None)   # False (correct!)
```

---

## 3. None in Functions

### Default Parameters

```python
# BAD - mutable default!
def append_to_list(item, lst=[]):
    lst.append(item)
    return lst

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] - Bug! Same list!

# GOOD - None as default
def append_to_list(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [2] - Correct!
```

### Return Values

```python
def find_user(user_id):
    """Return user or None if not found."""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)  # Returns None if not found

user = find_user(1)
if user is not None:
    print(f"Found: {user}")

user = find_user(999)
if user is None:
    print("User not found")
```

---

## 4. None in Conditional Expressions

### Truthiness of None

```python
# None is falsy
if None:
    print("This won't execute")

if not None:
    print("This will execute")

# Truthy/Falsy summary
print(bool(None))     # False
print(bool(0))        # False
print(bool(""))       # False
print(bool([]))       # False
print(bool({}))       # False
print(bool(1))        # True
print(bool("hello"))  # True
```

### Ternary with None

```python
name = None

# Set default if None
display_name = name if name is not None else "Anonymous"
print(display_name)  # Anonymous

# Short-circuit
display_name = name or "Anonymous"
print(display_name)  # Anonymous
```

---

## 5. None in Data Structures

### Lists

```python
my_list = [1, None, 3, None, 5]

# Count None occurrences
print(my_list.count(None))  # 2

# Filter out Nones
filtered = [x for x in my_list if x is not None]
print(filtered)  # [1, 3, 5]
```

### Dictionaries

```python
# Missing keys return None (or default)
config = {"host": "localhost", "port": 8080}

# .get() returns None if key missing
value = config.get("timeout")  # None

# Explicit default
value = config.get("timeout", 30)  # 30
```

### Sets

```python
my_set = {1, None, 3}
print(None in my_set)  # True
```

---

## 6. None vs Other Falsy Values

| Value | Type | `is None` | `not value` |
|-------|------|-----------|-------------|
| `None` | NoneType | `True` | `True` |
| `0` | int | `False` | `True` |
| `0.0` | float | `False` | `True` |
| `""` | str | `False` | `True` |
| `[]` | list | `False` | `True` |
| `{}` | dict | `False` | `True` |
| `set()` | set | `False` | `True` |
| `False` | bool | `False` | `True` |

```python
# Important distinction
value = 0

# These are different!
print(value is None)    # False
print(value == None)    # False (but works)
print(not value)        # True

# Use 'is None' when you specifically mean None
# Use 'not value' when you want any falsy value
```

---

## 7. Optional Type Hinting

### Basic Optional

```python
from typing import Optional

def greet(name: Optional[str]) -> str:
    if name is None:
        return "Hello, stranger!"
    return f"Hello, {name}!"

print(greet("Alice"))  # Hello, Alice!
print(greet(None))     # Hello, stranger!
```

### Optional with Default

```python
from typing import Optional

def process_data(data: list, 
                 callback: Optional[callable] = None) -> list:
    if callback is None:
        return data
    return [callback(x) for x in data]
```

---

## 8. None Patterns

### Guard Clauses

```python
def process_order(order):
    if order is None:
        raise ValueError("Order cannot be None")
    
    if order.items is None:
        raise ValueError("Order must have items")
    
    # Process order...
```

### Default Values Pattern

```python
class Config:
    def __init__(self, host=None, port=None, debug=None):
        self.host = host or "localhost"
        self.port = port or 8080
        self.debug = debug or False
```

### Sentinel Pattern

```python
_MISSING = object()  # Unique sentinel

def get_value(key, default=_MISSING):
    if default is _MISSING:
        raise KeyError(f"Key {key} not found")
    return default
```

---

## 9. Common Mistakes to Avoid

### 1. Using `==` Instead of `is`

```python
x = None

# BAD
if x == None:
    print("Don't do this")

# GOOD
if x is None:
    print("Do this")
```

### 2. Mutable Default Arguments

```python
# BAD - shared mutable default
def func(data=[]):
    data.append(1)
    return data

# GOOD - None as default
def func(data=None):
    if data is None:
        data = []
    data.append(1)
    return data
```

### 3. Returning None Unnecessarily

```python
# BAD - implicit None
def do_something():
    result = perform_operation()
    # Forgot to return result!

# GOOD - explicit return
def do_something():
    result = perform_operation()
    return result
```

---

## 10. Best Practices

1. **Use `is None`** and `is not None` for comparisons
2. **Use `None`** as default parameter for mutable arguments
3. **Return `None` explicitly** when no value to return
4. **Document** when functions can return `None`
5. **Use type hints** with `Optional[X]` for nullable values
6. **Check for `None`** before operating on potentially null values
7. **Use `.get()`** for dictionary lookups that may fail

---

## 11. Practice Exercises

### Exercise 1: Safe Dictionary Access

```python
def safe_get_nested(data, *keys):
    """Safely access nested dictionary values."""
    current = data
    for key in keys:
        if current is None or not isinstance(current, dict):
            return None
        current = current.get(key)
    return current

# Test
data = {"a": {"b": {"c": 42}}}
print(safe_get_nested(data, "a", "b", "c"))  # 42
print(safe_get_nested(data, "a", "x"))       # None
print(safe_get_nested(data, "x"))            # None
```

### Exercise 2: None-Safe List Processing

```python
def filter_and_transform(items, transform=None, filter_fn=None):
    """Filter and transform a list, handling None values."""
    result = items
    
    # Apply filter
    if filter_fn is not None:
        result = [x for x in result if filter_fn(x)]
    
    # Apply transform
    if transform is not None:
        result = [transform(x) for x in result]
    
    return result

# Test
numbers = [1, None, 2, None, 3, 4, None, 5]

# Filter Nones and double
result = filter_and_transform(
    numbers,
    filter_fn=lambda x: x is not None,
    transform=lambda x: x * 2
)
print(result)  # [2, 4, 6, 8, 10]
```

---

## 12. Summary

| Concept | Key Points |
|---------|------------|
| **None** | Python's null value, singleton |
| **is None** | Correct way to check for None |
| **NoneType** | Type of None object |
| **Default params** | Use None for mutable defaults |
| **Optional** | Type hint for nullable values |
| **Truthiness** | None is falsy |
| **Sentinel** | Use for "no value provided" |

---

## Next Steps

- Learn about `typing.Optional` and `typing.Union`
- Explore null object pattern in OOP
- Study async/await with None return values
