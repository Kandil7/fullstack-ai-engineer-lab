# Python Dictionaries — Glossary 16

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| Dictionary | Collection of key-value pairs | `{"name": "Alice", "age": 30}` |
| Key | Immutable identifier for a dictionary entry | `"name"`, `1`, `(2, 3)` |
| Value | Data associated with a key | `"Alice"`, `30`, `[1, 2]` |
| Key-Error | Exception raised when accessing a missing key | `d["missing"]` |
| Get | Safe access with default value | `d.get("key", default)` |
| Setdefault | Get value or set default if key missing | `d.setdefault("key", default)` |
| Update | Modify or add multiple entries | `d.update({"a": 1, "b": 2})` |
| Pop | Remove and return a value | `d.pop("key")` |
| Popitem | Remove and return last inserted pair | `d.popitem()` |
| Items | View of all key-value pairs | `d.items()` |
| Keys | View of all keys | `d.keys()` |
| Values | View of all values | `d.values()` |
| Dictionary Comprehension | Create dict with comprehension syntax | `{k: v for k, v in items}` |
| Nested Dict | Dict containing other dicts | `{"a": {"b": 1}}` |
| Merge | Combine two dictionaries | `d1 | d2` or `{**d1, **d2}` |
| Default Dict | Dict with automatic default values | `defaultdict(list)` |
| Counter | Dict subclass for counting | `Counter("abc")` |
| OrderedDict | Dict that remembers insertion order | `OrderedDict()` |
| Hashable | Type that can be a dictionary key | `int`, `str`, `tuple` |
| Shallow Copy | Copy of dict (not deep) | `d.copy()` |

---

## Definitions

### Counter
**Definition**: A dictionary subclass from the `collections` module designed for counting hashable objects. Elements are stored as dictionary keys and their counts as values.

**Example**:
```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
count = Counter(words)
print(count)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(count.most_common(2))  # [('apple', 3), ('banana', 2)]
```

**Related**: `collections`, frequency counting, `most_common()`

---

### Default Dict
**Definition**: A dictionary subclass from `collections` that calls a factory function to supply a default value when a key is not found, eliminating KeyError.

**Example**:
```python
from collections import defaultdict

# Group items by category
d = defaultdict(list)
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
for word in words:
    d[word[0]].append(word)
print(dict(d))  # {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}
```

**Related**: `dict.setdefault()`, `collections`, factory function

---

### Dict Comprehension
**Definition**: A concise syntax for creating dictionaries using the pattern `{key_expr: value_expr for item in iterable if condition}`.

**Example**:
```python
# Square numbers
squares = {x: x**2 for x in range(6)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Filter and transform
scores = {"Alice": 85, "Bob": 62, "Charlie": 91}
passed = {k: v for k, v in scores.items() if v >= 70}
print(passed)  # {'Alice': 85, 'Charlie': 91}
```

**Related**: list comprehension, set comprehension, generator expression

---

### Dictionary
**Definition**: An unordered (ordered since Python 3.7), mutable collection of key-value pairs. Keys must be unique and hashable; values can be any type.

**Example**:
```python
person = {"name": "Alice", "age": 30, "hobbies": ["reading", "coding"]}
print(person["name"])  # Alice
person["email"] = "alice@example.com"
```

**Related**: `dict()`, hashable, key, value, mutable

---

### Get
**Definition**: A method that returns the value for a key if it exists, otherwise returns a default value (or `None` if no default is specified). Does not raise KeyError.

**Example**:
```python
d = {"a": 1, "b": 2}
print(d.get("a"))       # 1
print(d.get("c"))       # None
print(d.get("c", 0))    # 0
```

**Related**: `__getitem__`, KeyError, `setdefault()`

---

### Hashable
**Definition**: An object is hashable if it has a `__hash__()` method that returns the same value during its lifetime. Hashable objects can be used as dictionary keys.

**Example**:
```python
# Hashable — can be dict keys
{1: "number", "hello": "string", (1, 2): "tuple"}

# Unhashable — cannot be dict keys
# {[1, 2]: "list"}  # TypeError
# {{'a': 1}: "dict"}  # TypeError
```

**Related**: `__hash__`, dictionary keys, set elements, immutable

---

### Items
**Definition**: A method that returns a view object displaying a list of a dictionary's key-value tuple pairs.

**Example**:
```python
d = {"a": 1, "b": 2, "c": 3}
for key, value in d.items():
    print(f"{key}: {value}")

# Convert to list of tuples
pairs = list(d.items())
print(pairs)  # [('a', 1), ('b', 2), ('c', 3)]
```

**Related**: `keys()`, `values()`, iteration

---

### Key
**Definition**: A unique identifier for a value in a dictionary. Keys must be immutable (hashable) types like strings, numbers, or tuples.

**Example**:
```python
d = {
    "string_key": "value1",
    42: "value2",
    (1, 2): "value3"
}
print(d["string_key"])  # value1
print(d[42])            # value2
```

**Related**: hashable, value, dictionary, `__hash__`

---

### Key-Error
**Definition**: An exception raised when trying to access a dictionary key that doesn't exist using square bracket notation `d[key]`.

**Example**:
```python
d = {"a": 1}
# print(d["b"])  # KeyError: 'b'

# Avoid with get()
d.get("b", "default")  # Returns "default"
```

**Related**: `get()`, `setdefault()`, `pop()`, safe access

---

### Keys
**Definition**: A method that returns a view object displaying all keys in the dictionary.

**Example**:
```python
d = {"name": "Alice", "age": 30, "city": "NYC"}
print(list(d.keys()))  # ['name', 'age', 'city']

# Check if key exists
if "name" in d.keys():  # or just: if "name" in d:
    print("Name found")
```

**Related**: `values()`, `items()`, `in` operator

---

### Merge
**Definition**: The operation of combining two dictionaries. In Python 3.9+, use `|` operator. In older versions, use `{**d1, **d2}` or `d1.update(d2)`.

**Example**:
```python
# Python 3.9+
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = d1 | d2
print(merged)  # {'a': 1, 'b': 3, 'c': 4}

# Older Python
merged = {**d1, **d2}
```

**Related**: `update()`, unpacking, `|` operator

---

### Nested Dict
**Definition**: A dictionary that contains other dictionaries as values, enabling hierarchical data structures.

**Example**:
```python
students = {
    "alice": {
        "age": 20,
        "grades": {"math": 90, "english": 85}
    },
    "bob": {
        "age": 22,
        "grades": {"math": 78, "english": 92}
    }
}
print(students["alice"]["grades"]["math"])  # 90
```

**Related**: dictionary, nested data structures, JSON

---

### OrderedDict
**Definition**: A dictionary subclass from `collections` that remembers the order in which keys were first inserted. Standard dicts preserve order since Python 3.7, but OrderedDict has extra methods like `move_to_end()`.

**Example**:
```python
from collections import OrderedDict

od = OrderedDict()
od["first"] = 1
od["second"] = 2
od["third"] = 3

od.move_to_end("first")
print(od)  # OrderedDict([('second', 2), ('third', 3), ('first', 1)])
```

**Related**: `collections`, insertion order, `move_to_end()`

---

### Pop
**Definition**: A method that removes a key from the dictionary and returns its value. Can provide a default to avoid KeyError.

**Example**:
```python
d = {"a": 1, "b": 2, "c": 3}
val = d.pop("b")
print(val)   # 2
print(d)     # {'a': 1, 'c': 3}

val = d.pop("z", "missing")
print(val)   # "missing"
```

**Related**: `popitem()`, `del`, `clear()`

---

### Popitem
**Definition**: A method that removes and returns the last inserted key-value pair as a tuple.

**Example**:
```python
d = {"a": 1, "b": 2, "c": 3}
item = d.popitem()
print(item)  # ('c', 3)
print(d)     # {'a': 1, 'b': 2}
```

**Related**: `pop()`, `clear()`, `del`

---

### Setdefault
**Definition**: A method that returns the value of a key if it exists. If the key doesn't exist, it inserts the key with a specified default value and returns that default.

**Example**:
```python
d = {"a": 1}

# Key exists — returns value
val = d.setdefault("a", 10)
print(val)  # 1
print(d)    # {'a': 1}

# Key doesn't exist — inserts and returns default
val = d.setdefault("b", 20)
print(val)  # 20
print(d)    # {'a': 1, 'b': 20}
```

**Related**: `get()`, `update()`, initialization patterns

---

### Shallow Copy
**Definition**: A copy of a dictionary where nested objects are referenced, not copied. Changes to nested objects in the copy affect the original.

**Example**:
```python
original = {"a": [1, 2, 3], "b": 4}
copy_d = original.copy()

copy_d["b"] = 10
print(original["b"])  # 4 (unchanged — independent for top-level)

copy_d["a"].append(4)
print(original["a"])  # [1, 2, 3, 4] (changed — shared nested object)
```

**Related**: `copy()`, deep copy, `copy.deepcopy()`

---

### Update
**Definition**: A method that updates the dictionary with key-value pairs from another dictionary or iterable. Existing keys are overwritten.

**Example**:
```python
d = {"a": 1, "b": 2}
d.update({"b": 3, "c": 4})
print(d)  # {'a': 1, 'b': 3, 'c': 4}

# From list of tuples
d.update([("d", 5), ("e", 6)])
print(d)  # {'a': 1, 'b': 3, 'c': 4, 'd': 5, 'e': 6}
```

**Related**: `|=`, merge, `{**d1, **d2}`

---

### Values
**Definition**: A method that returns a view object displaying all values in the dictionary.

**Example**:
```python
d = {"name": "Alice", "age": 30, "city": "NYC"}
print(list(d.values()))  # ['Alice', 30, 'NYC']

# Check if value exists
if 30 in d.values():
    print("Found value 30")
```

**Related**: `keys()`, `items()`, `in` operator

---

## Code Examples

### Example 1: Count Word Frequency
```python
from collections import Counter

text = "the cat sat on the mat the cat"
words = text.split()
freq = Counter(words)
print(freq.most_common(2))  # [('the', 3), ('cat', 2)]
```

### Example 2: Build a Lookup Table
```python
# Create a fast lookup from ID to name
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]
lookup = {user["id"]: user["name"] for user in users}
print(lookup)  # {1: 'Alice', 2: 'Bob', 3: 'Charlie'}
print(lookup[2])  # Bob
```

### Example 3: Group Items
```python
from collections import defaultdict

students = [
    ("Alice", "Engineering"),
    ("Bob", "Marketing"),
    ("Charlie", "Engineering"),
    ("Diana", "Marketing"),
    ("Eve", "Engineering")
]

groups = defaultdict(list)
for name, dept in students:
    groups[dept].append(name)

print(dict(groups))
# {'Engineering': ['Alice', 'Charlie', 'Eve'], 'Marketing': ['Bob', 'Diana']}
```

---

## Related Concepts

- **JSON**: Python dictionaries map directly to JSON objects
- **kwargs: `**kwargs` passes dictionaries as keyword arguments
- **dataclasses**: Modern alternative to dictionaries for structured data
- **namedtuple**: Lightweight immutable alternative for fixed keys
- **attrs**: Third-party library for class-based data structures
