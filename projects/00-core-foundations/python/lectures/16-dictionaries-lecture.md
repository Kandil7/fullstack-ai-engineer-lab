# Python Dictionaries — Lecture 16

## Topic Overview

A **dictionary** is a collection of key-value pairs. Unlike lists and tuples, dictionaries are indexed by keys rather than numeric positions. Keys must be unique and immutable (strings, numbers, tuples), while values can be of any type. Dictionaries are one of the most versatile and frequently used data structures in Python.

Dictionaries are defined using curly braces `{}` with `key: value` pairs, or the `dict()` constructor. They are ordered (as of Python 3.7+), mutable, and optimized for fast lookups by key.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Create dictionaries using different methods
- Access, add, modify, and delete dictionary entries
- Use dictionary methods for iteration and manipulation
- Implement nested dictionaries
- Use dictionary comprehensions
- Understand when to use dictionaries vs. other data structures
- Apply dictionaries to real-world scenarios

---

## Key Concepts

### 1. Creating Dictionaries

```python
# Using curly braces
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}
print(person)  # {'name': 'Alice', 'age': 30, 'city': 'New York'}

# Using the dict() constructor
person = dict(name="Alice", age=30, city="New York")
print(person)  # {'name': 'Alice', 'age': 30, 'city': 'New York'}

# From a list of tuples
person = dict([("name", "Alice"), ("age", 30)])
print(person)  # {'name': 'Alice', 'age': 30}

# Empty dictionary
empty = {}
empty = dict()
```

### 2. Accessing Values

```python
person = {"name": "Alice", "age": 30, "city": "New York"}

# Using square brackets
print(person["name"])  # Alice

# Using get() — returns None (or default) if key doesn't exist
print(person.get("name"))       # Alice
print(person.get("phone"))      # None
print(person.get("phone", "N/A"))  # N/A

# Using square brackets with missing key raises KeyError
# print(person["phone"])  # KeyError: 'phone'
```

### 3. Adding and Modifying Entries

```python
person = {"name": "Alice", "age": 30}

# Add new key-value pair
person["email"] = "alice@example.com"
print(person)  # {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}

# Modify existing value
person["age"] = 31
print(person)  # {'name': 'Alice', 'age': 31, 'email': 'alice@example.com'}

# Using update() — add or modify multiple entries
person.update({"phone": "555-1234", "age": 32})
print(person)  # includes phone and updated age

# Using setdefault() — add if key doesn't exist
person.setdefault("country", "USA")
print(person["country"])  # USA
person.setdefault("name", "Bob")  # Won't change — "name" already exists
print(person["name"])  # Alice
```

### 4. Removing Entries

```python
person = {"name": "Alice", "age": 30, "email": "alice@example.com"}

# pop() — remove and return value
age = person.pop("age")
print(age)     # 30
print(person)  # {'name': 'Alice', 'email': 'alice@example.com'}

# pop() with default — no error if key missing
phone = person.pop("phone", "N/A")
print(phone)  # N/A

# popitem() — remove and return last inserted pair
last = person.popitem()
print(last)   # ('email', 'alice@example.com')

# del statement
del person["name"]
print(person)  # {}

# clear() — remove all entries
person.clear()
print(person)  # {}
```

### 5. Iterating Over Dictionaries

```python
person = {"name": "Alice", "age": 30, "city": "New York"}

# Iterate over keys (default)
for key in person:
    print(key, person[key])

# Explicitly iterate over keys
for key in person.keys():
    print(key)

# Iterate over values
for value in person.values():
    print(value)

# Iterate over key-value pairs
for key, value in person.items():
    print(f"{key}: {value}")
```

### 6. Nested Dictionaries

```python
# Dictionaries can contain other dictionaries
company = {
    "employees": {
        "alice": {"age": 30, "department": "Engineering"},
        "bob": {"age": 25, "department": "Marketing"},
        "charlie": {"age": 35, "department": "Engineering"}
    },
    "departments": {
        "engineering": {"budget": 500000, "headcount": 2},
        "marketing": {"budget": 200000, "headcount": 1}
    }
}

# Accessing nested values
print(company["employees"]["alice"]["department"])  # Engineering
print(company["departments"]["engineering"]["budget"])  # 500000

# Adding to nested dictionary
company["employees"]["diana"] = {"age": 28, "department": "HR"}
```

### 7. Dictionary Comprehensions

```python
# Create a dictionary from a list
names = ["Alice", "Bob", "Charlie"]
name_lengths = {name: len(name) for name in names}
print(name_lengths)  # {'Alice': 5, 'Bob': 3, 'Charlie': 7}

# Filter a dictionary
scores = {"Alice": 85, "Bob": 62, "Charlie": 91, "Diana": 78}
passed = {name: score for name, score in scores.items() if score >= 70}
print(passed)  # {'Alice': 85, 'Charlie': 91, 'Diana': 78}

# Transform values
scores = {"Alice": 85, "Bob": 62, "Charlie": 91}
grades = {name: "A" if score >= 90 else "B" if score >= 80 else "C" 
          for name, score in scores.items()}
print(grades)  # {'Alice': 'B', 'Bob': 'C', 'Charlie': 'A'}
```

### 8. Useful Dictionary Methods

```python
d = {"a": 1, "b": 2, "c": 3}

# keys() — view of all keys
print(list(d.keys()))  # ['a', 'b', 'c']

# values() — view of all values
print(list(d.values()))  # [1, 2, 3]

# items() — view of all key-value pairs
print(list(d.items()))  # [('a', 1), ('b', 2), 'c', 3)]

# copy() — shallow copy
d_copy = d.copy()

# merge using | operator (Python 3.9+)
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = d1 | d2
print(merged)  # {'a': 1, 'b': 3, 'c': 4} — d2 overwrites d1

# fromkeys() — create dict with same value
keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)
print(d)  # {'a': 0, 'b': 0, 'c': 0}
```

---

## Code Examples

### Example 1: Word Frequency Counter

```python
def word_frequency(text):
    words = text.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

text = "the cat sat on the mat the cat ate the rat"
result = word_frequency(text)
# {'the': 4, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1, 'ate': 1, 'rat': 1}

# Sort by frequency
sorted_freq = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
print(sorted_freq)
```

### Example 2: Merge Two Dictionaries

```python
def merge_dicts(dict1, dict2):
    """Merge two dictionaries, with dict2 values taking precedence."""
    return {**dict1, **dict2}

# Or using | operator (Python 3.9+)
def merge_dicts(dict1, dict2):
    return dict1 | dict2

a = {"x": 1, "y": 2}
b = {"y": 3, "z": 4}
print(merge_dicts(a, b))  # {'x': 1, 'y': 3, 'z': 4}
```

### Example 3: Invert a Dictionary

```python
def invert_dict(d):
    """Swap keys and values."""
    return {v: k for k, v in d.items()}

original = {"a": 1, "b": 2, "c": 3}
inverted = invert_dict(original)
print(inverted)  # {1: 'a', 2: 'b', 3: 'c'}
```

### Example 4: Group by Category

```python
def group_by_category(items, key_func):
    """Group items into categories based on a key function."""
    groups = {}
    for item in items:
        category = key_func(item)
        groups.setdefault(category, []).append(item)
    return groups

words = ["apple", "banana", "avocado", "blueberry", "cherry", "apricot"]
result = group_by_category(words, key_func=lambda w: w[0])
# {'a': ['apple', 'avocado', 'apricot'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}
print(result)
```

---

## Common Mistakes to Avoid

### Mistake 1: Accessing Missing Keys
```python
# WRONG — raises KeyError
d = {"a": 1}
# print(d["b"])  # KeyError

# CORRECT — use get() with default
print(d.get("b", 0))  # 0
```

### Mistake 2: Modifying Dict While Iterating
```python
# WRONG
d = {"a": 1, "b": 2, "c": 3}
# for key in d:
#     if d[key] < 2:
#         del d[key]  # RuntimeError!

# CORRECT — iterate over a copy of keys
d = {"a": 1, "b": 2, "c": 3}
for key in list(d.keys()):
    if d[key] < 2:
        del d[key]
```

### Mistake 3: Using Mutable Values as Keys
```python
# WRONG
# d = {[1, 2]: "value"}  # TypeError: unhashable type: 'list'

# CORRECT — use tuples instead
d = {(1, 2): "value"}
```

### Mistake 4: Assuming Order (Pre-3.7)
```python
# In Python 3.7+, dicts maintain insertion order
# In older Python, dict order was undefined
# If supporting older Python, don't rely on order
```

---

## Best Practices

1. **Use `get()` for safe access** — avoids KeyError
2. **Use `setdefault()`** for initialization patterns
3. **Use dictionary comprehensions** for concise transformations
4. **Use `items()` for iteration** — clean and Pythonic
5. **Use `**unpacking`** for merging dicts (Python 3.5+) or `|` (Python 3.9+)
6. **Use `Counter` from collections** for frequency counting
7. **Consider `defaultdict`** for automatic default values
8. **Validate keys exist** before accessing in critical code paths

---

## Practice Exercises

### Exercise 1: Character Counter
Write a function that counts the frequency of each character in a string (ignoring spaces).

```python
def char_frequency(text):
    # Your code here
    pass

# Expected: {'h': 2, 'e': 1, 'l': 3, 'o': 2}
print(char_frequency("hello hello"))
```

### Exercise 2: Dictionary Merge
Write a function that deeply merges two nested dictionaries.

```python
def deep_merge(dict1, dict2):
    # Your code here — recursive merge
    pass

a = {"x": {"a": 1}, "y": 2}
b = {"x": {"b": 3}, "z": 4}
# Expected: {"x": {"a": 1, "b": 3}, "y": 2, "z": 4}
print(deep_merge(a, b))
```

### Exercise 3: Sort by Value
Write a function that returns a dictionary sorted by its values.

```python
def sort_by_value(d, reverse=False):
    # Your code here
    pass

data = {"alice": 85, "bob": 62, "charlie": 91}
# Expected: {'charlie': 91, 'alice': 85, 'bob': 62}
print(sort_by_value(data, reverse=True))
```

### Exercise 4: Flatten Nested Dictionary
Write a function that flattens a nested dictionary with dot notation keys.

```python
def flatten_dict(d, parent_key="", sep="."):
    # Your code here
    pass

data = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
# Expected: {"a": 1, "b.c": 2, "b.d.e": 3}
print(flatten_dict(data))
```

---

## Summary

- **Dictionaries** map unique keys to values using `{key: value}` syntax
- Keys must be **immutable** (strings, numbers, tuples); values can be anything
- **Access**: `d[key]` (raises KeyError) or `d.get(key, default)` (safe)
- **Modify**: `d[key] = value`, `d.update()`, `d.setdefault()`
- **Remove**: `d.pop()`, `del d[key]`, `d.clear()`
- **Iterate**: `d.keys()`, `d.values()`, `d.items()`
- **Nested dicts** enable complex data structures
- **Dictionary comprehensions** `{k: v for k, v in iterable}` create dicts concisely
- **Order is preserved** in Python 3.7+
