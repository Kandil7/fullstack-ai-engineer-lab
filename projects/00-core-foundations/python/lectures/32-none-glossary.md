# None and Null Values Glossary

## Topic 32: Quick Reference Guide

---

## Glossary Terms

### F

#### Falsy
**Definition:** Values that evaluate to `False` in boolean context (including `None`).
```python
# None is falsy
if None:
    print("Won't run")

# All falsy values
print(bool(None))    # False
print(bool(0))       # False
print(bool(""))      # False
print(bool([]))      # False
```
**Related:** None, truthiness, boolean conversion

---

### N

#### None
**Definition:** Python's singleton representing absence of a value (null).
```python
x = None
print(x)         # None
print(type(x))   # <class 'NoneType'>
```
**Related:** NoneType, null, void

#### NoneType
**Definition:** The type of the `None` object.
```python
print(type(None))  # <class 'NoneType'>
```
**Related:** None, type checking

#### Null (concept)
**Definition:** General term for "no value"; Python uses `None` for this.
```python
# Other languages use null, NULL, nil, etc.
# Python uses None
```
**Related:** None, optional, nullable

---

### O

#### Optional
**Definition:** Type hint indicating a value can be `None` or the specified type.
```python
from typing import Optional

def greet(name: Optional[str]) -> str:
    if name is None:
        return "Hello, stranger!"
    return f"Hello, {name}!"
```
**Related:** None, type hints, Union

---

### T

#### Truthiness
**Definition:** Whether a value evaluates to `True` or `False` in boolean context.
```python
# None is falsy
print(bool(None))  # False

# Truthy values
print(bool(1))        # True
print(bool("hello"))  # True
```
**Related:** Falsy, truthiness, bool()

---

## Quick Reference Table

| Term | Category | Description |
|------|----------|-------------|
| **None** | Value | Absence of value (null) |
| **NoneType** | Type | Type of None object |
| **is None** | Check | Identity check for None |
| **is not None** | Check | Identity check (not None) |
| **Optional** | Type hint | Value can be None or type |
| **Falsy** | Boolean | Evaluates to False |
| **Truthiness** | Boolean | Boolean evaluation |
| **Null** | Concept | No value (Python uses None) |
| **Null pointer** | Error | Reference to null (doesn't exist in Python) |

---

## None Patterns

### Pattern 1: Default Parameter
```python
def func(data=None):
    if data is None:
        data = []
    return data
```

### Pattern 2: Guard Clause
```python
def process(value):
    if value is None:
        raise ValueError("Value cannot be None")
    # Continue processing
```

### Pattern 3: Sentinel
```python
_MISSING = object()

def get(key, default=_MISSING):
    if default is _MISSING:
        raise KeyError(key)
    return default
```

### Pattern 4: Optional Return
```python
def find_item(items, target):
    for item in items:
        if item == target:
            return item
    return None  # Not found
```

---

## None vs Other Languages

| Language | Null Value |
|----------|------------|
| **Python** | `None` |
| **JavaScript** | `null`, `undefined` |
| **Java** | `null` |
| **C#** | `null` |
| **Ruby** | `nil` |
| **Go** | `nil` |
| **PHP** | `null` |

---

## Common Mistakes

### Wrong: Using `==`
```python
x = None
if x == None:  # BAD
    pass
```

### Right: Using `is`
```python
x = None
if x is None:  # GOOD
    pass
```

### Wrong: Mutable Default
```python
def func(data=[]):  # BAD
    data.append(1)
    return data
```

### Right: None Default
```python
def func(data=None):  # GOOD
    if data is None:
        data = []
    data.append(1)
    return data
```
