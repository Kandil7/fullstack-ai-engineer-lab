# Python JSON — Lecture 28

## Topic Overview

**JSON** (JavaScript Object Notation) is a lightweight data interchange format that's easy for humans to read and write, and easy for machines to parse and generate. Python's built-in `json` module provides functions for encoding (serializing) Python objects to JSON strings and decoding (deserializing) JSON strings back to Python objects.

JSON is the standard format for APIs, configuration files, and data exchange between systems.

---

## Learning Objectives

By the end of this lecture, you will be able to:

- Convert Python objects to JSON strings (dumps/dump)
- Convert JSON strings to Python objects (loads/load)
- Handle common data type conversions
- Format and pretty-print JSON
- Work with JSON files
- Handle errors in JSON parsing
- Apply JSON to real-world scenarios

---

## Key Concepts

### 1. JSON Basics

```python
import json

# Python dict → JSON string
data = {"name": "Alice", "age": 30, "city": "New York"}
json_string = json.dumps(data)
print(json_string)  # {"name": "Alice", "age": 30, "city": "New York"}
print(type(json_string))  # <class 'str'>

# JSON string → Python dict
parsed = json.loads(json_string)
print(parsed)       # {'name': 'Alice', 'age': 30, 'city': 'New York'}
print(type(parsed))  # <class 'dict'>
```

### 2. Python to JSON (Encoding)

```python
import json

# Data type conversions
print(json.dumps(42))          # "42"
print(json.dumps(3.14))        # "3.14"
print(json.dumps("hello"))     # "\"hello\""
print(json.dumps(True))        # "true"
print(json.dumps(None))        # "null"

# Collections
print(json.dumps([1, 2, 3]))          # "[1, 2, 3]"
print(json.dumps({"a": 1, "b": 2}))   # "{\"a\": 1, \"b\": 2}"
print(json.dumps((1, 2, 3)))          # "[1, 2, 3]" — tuples → arrays
print(json.dumps({1, 2, 3}))          # TypeError — sets not supported
```

### 3. JSON to Python (Decoding)

```python
import json

# JSON types → Python types
# "string"  → str
# 123       → int
# 1.23      → float
# true      → True
# false     → False
# null      → None
# [array]   → list
# {object}  → dict

json_str = '{"name": "Alice", "active": true, "score": null}'
data = json.loads(json_str)
print(data)  # {'name': 'Alice', 'active': True, 'score': None}
```

### 4. Pretty Printing

```python
import json

data = {
    "name": "Alice",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY"
    },
    "hobbies": ["reading", "coding", "hiking"]
}

# Compact (default)
compact = json.dumps(data)
print(compact)

# Pretty printed with indentation
pretty = json.dumps(data, indent=4)
print(pretty)

# Sorted keys
sorted_json = json.dumps(data, indent=2, sort_keys=True)
print(sorted_json)
```

### 5. Working with JSON Files

```python
import json

# Writing JSON to file
data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Reading JSON from file
with open("data.json", "r") as f:
    loaded_data = json.load(f)

print(loaded_data)  # {'users': [{'name': 'Alice'}, {'name': 'Bob'}]}
```

### 6. Handling Non-Serializable Types

```python
import json
from datetime import datetime, date

# Custom encoder for non-serializable types
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

# Usage
data = {
    "date": datetime.now(),
    "tags": {"python", "json", "data"}
}

json_str = json.dumps(data, cls=CustomEncoder, indent=2)
print(json_str)

# Custom decoder
def custom_hook(dct):
    if "date" in dct:
        dct["date"] = datetime.fromisoformat(dct["date"])
    return dct

parsed = json.loads(json_str, object_hook=custom_hook)
```

### 7. JSON with Nested Data

```python
import json

# Complex nested structure
data = {
    "company": "TechCorp",
    "employees": [
        {
            "name": "Alice",
            "department": "Engineering",
            "skills": ["Python", "JavaScript", "SQL"]
        },
        {
            "name": "Bob",
            "department": "Marketing",
            "skills": ["SEO", "Analytics"]
        }
    ],
    "metadata": {
        "founded": 2010,
        "public": True
    }
}

# Pretty print
print(json.dumps(data, indent=2))

# Access nested data
parsed = json.loads(json.dumps(data))
for emp in parsed["employees"]:
    print(f"{emp['name']}: {', '.join(emp['skills'])}")
```

### 8. Error Handling

```python
import json

# Invalid JSON
try:
    result = json.loads("{invalid json}")
except json.JSONDecodeError as e:
    print(f"JSON parse error: {e}")

# File not found
try:
    with open("nonexistent.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("File not found!")
except json.JSONDecodeError as e:
    print(f"Invalid JSON in file: {e}")
```

---

## Code Examples

### Example 1: JSON API Response Handler

```python
import json

def parse_api_response(response_text):
    """Parse and validate API response."""
    try:
        data = json.loads(response_text)
        
        # Validate required fields
        required = ["status", "data"]
        for field in required:
            if field not in data:
                return {"error": f"Missing field: {field}"}
        
        return data
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {e}"}

# Test
response = '{"status": "success", "data": {"users": 42}}'
result = parse_api_response(response)
print(result)
```

### Example 2: JSON Config Manager

```python
import json
import os

class ConfigManager:
    def __init__(self, filename):
        self.filename = filename
        self.config = self.load()
    
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return {}
    
    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save()

# Usage
config = ConfigManager("app_config.json")
config.set("theme", "dark")
config.set("language", "en")
print(config.get("theme"))  # dark
```

### Example 3: JSON Data Transformer

```python
import json

def flatten_json(nested_json, prefix=""):
    """Flatten nested JSON into dot-notation keys."""
    flat = {}
    for key, value in nested_json.items():
        new_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten_json(value, new_key))
        else:
            flat[new_key] = value
    return flat

# Test
nested = {
    "name": "Alice",
    "address": {
        "street": "123 Main St",
        "city": "NYC"
    }
}
flat = flatten_json(nested)
print(flat)  # {'name': 'Alice', 'address.street': '123 Main St', 'address.city': 'NYC'}
```

---

## Common Mistakes to Avoid

### Mistake 1: Using `json.dumps()` on Non-Serializable Types
```python
import json
from datetime import datetime

# WRONG
# json.dumps(datetime.now())  # TypeError

# CORRECT — use custom encoder
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps({"date": datetime.now()}, cls=DateEncoder)
```

### Mistake 2: Single vs. Double Quotes
```python
import json

# WRONG — Python uses single quotes
# json.loads("{'key': 'value'}")  # JSONDecodeError

# CORRECT — JSON requires double quotes
json.loads('{"key": "value"}')  # Works!
```

### Mistake 3: Forgetting `json.load()` vs `json.loads()`
```python
import json

# loads() — from string
data = json.loads('{"name": "Alice"}')

# load() — from file
with open("data.json") as f:
    data = json.load(f)

# dumps() — to string
json_str = json.dumps(data)

# dump() — to file
with open("output.json", "w") as f:
    json.dump(data, f)
```

### Mistake 4: Set Not Serializable
```python
import json

# WRONG
# json.dumps({1, 2, 3})  # TypeError: set is not JSON serializable

# CORRECT — convert to list
json.dumps(list({1, 2, 3}))  # "[1, 2, 3]"
```

---

## Best Practices

1. **Use `indent` parameter** for human-readable output
2. **Use `sort_keys=True`** for consistent key ordering
3. **Handle `JSONDecodeError`** when parsing user input
4. **Use custom encoders** for non-standard types
5. **Use `load()`/`dump()`** for file operations
6. **Use `loads()`/`dumps()`** for string operations
7. **Validate JSON structure** after parsing
8. **Use `ensure_ascii=False`** for Unicode characters

---

## Practice Exercises

### Exercise 1: JSON to CSV
Write a function that converts a JSON array of objects to CSV format.

### Exercise 2: JSON Merger
Write a function that deep-merges two JSON objects.

### Exercise 3: JSON Validator
Write a function that validates a JSON string against a schema.

---

## Summary

- **`json.dumps()`**: Python object → JSON string
- **`json.loads()`**: JSON string → Python object
- **`json.dump()`**: Python object → JSON file
- **`json.load()`**: JSON file → Python object
- **Type mapping**: `dict`↔`object`, `list`↔`array`, `str`↔`string`, `int/float`↔`number`, `True`↔`true`, `None`↔`null`
- **Pretty print**: `json.dumps(data, indent=2)`
- **Custom encoder**: Override `default()` method
- **Error handling**: Catch `JSONDecodeError`
- **Sets and tuples** need conversion before serialization
