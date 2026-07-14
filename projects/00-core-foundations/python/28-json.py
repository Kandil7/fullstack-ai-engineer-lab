"""
W3Schools Python Tutorial - 28: Python JSON
============================================
Topics: JSON to Python, Python to JSON, formatting, parsing

Run: python 28-json.py
Reference: https://www.w3schools.com/python/python_json.asp
"""

# ============================================================
# What is JSON?
# ============================================================
# JSON (JavaScript Object Notation) is a lightweight data format.
# It's widely used for data exchange between servers and clients.
# Python has a built-in json module to work with JSON.

import json

# ============================================================
# Python to JSON (Serialize)
# ============================================================
# Example 1: Convert Python objects to JSON
print("--- Python to JSON ---")

# Python dict to JSON string
python_dict = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "is_student": False
}

json_string = json.dumps(python_dict)
print(f"JSON string: {json_string}")
print(f"Type: {type(json_string)}")

# Output:
# JSON string: {"name": "Alice", "age": 30, "city": "New York", "is_student": false}
# Type: <class 'str'>

# ============================================================
# Type Mapping (Python to JSON)
# ============================================================
# Example 2: How Python types map to JSON
print("\n--- Type Mapping ---")

python_data = {
    "string": "hello",
    "integer": 42,
    "float": 3.14,
    "boolean_true": True,
    "boolean_false": False,
    "none_value": None,
    "list": [1, 2, 3],
    "tuple": (4, 5, 6),  # Tuples become JSON arrays
    "dict": {"key": "value"}
}

json_data = json.dumps(python_data, indent=2)
print(json_data)

# Output:
# {
#   "string": "hello",
#   "integer": 42,
#   "float": 3.14,
#   "boolean_true": true,
#   "boolean_false": false,
#   "none_value": null,
#   "list": [1, 2, 3],
#   "tuple": [4, 5, 6],
#   "dict": {"key": "value"}
# }

# Note: True becomes true, False becomes false, None becomes null

# ============================================================
# JSON to Python (Deserialize)
# ============================================================
# Example 3: Convert JSON string to Python objects
print("\n--- JSON to Python ---")

json_string = '{"name": "Bob", "age": 25, "active": true, "scores": [90, 85, 92]}'
python_obj = json.loads(json_string)

print(f"Python object: {python_obj}")
print(f"Type: {type(python_obj)}")
print(f"Name: {python_obj['name']}")
print(f"Age: {python_obj['age']}")
print(f"Active: {python_obj['active']}")
print(f"Scores: {python_obj['scores']}")

# Output:
# Python object: {'name': 'Bob', 'age': 25, 'active': True, 'scores': [90, 85, 92]}
# Type: <class 'dict'>
# Name: Bob
# Age: 25
# Active: True
# Scores: [90, 85, 92]

# ============================================================
# Type Mapping (JSON to Python)
# ============================================================
# Example 4: How JSON types map to Python
print("\n--- JSON to Python Mapping ---")

json_data = '''
{
    "string": "hello",
    "integer": 42,
    "float": 3.14,
    "boolean_true": true,
    "boolean_false": false,
    "null_value": null,
    "array": [1, 2, 3],
    "object": {"key": "value"}
}
'''

python_data = json.loads(json_data)
for key, value in python_data.items():
    print(f"{key}: {value} (type: {type(value).__name__})")

# Output:
# string: hello (type: str)
# integer: 42 (type: int)
# float: 3.14 (type: float)
# boolean_true: True (type: bool)
# boolean_false: False (type: bool)
# null_value: None (type: NoneType)
# array: [1, 2, 3] (type: list)
# object: {'key': 'value'} (type: dict)

# ============================================================
# Pretty Printing
# ============================================================
# Example 5: Formatting JSON output
print("\n--- Pretty Printing ---")

data = {"users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]}

# Default (compact)
compact = json.dumps(data)
print(f"Compact: {compact}")

# Pretty print with indent
pretty = json.dumps(data, indent=2)
print(f"\nPretty:\n{pretty}")

# Custom indent
custom = json.dumps(data, indent=4)
print(f"\nCustom indent:\n{custom}")

# ============================================================
# Working with Files
# ============================================================
# Example 6: Reading and writing JSON files
print("\n--- JSON Files ---")

# Write JSON to file
data = {
    "employees": [
        {"name": "Alice", "department": "Engineering", "salary": 95000},
        {"name": "Bob", "department": "Marketing", "salary": 75000},
        {"name": "Charlie", "department": "Engineering", "salary": 105000}
    ]
}

# Write to file
with open("employees.json", "w") as f:
    json.dump(data, f, indent=2)
print("Written to employees.json")

# Read from file
with open("employees.json", "r") as f:
    loaded_data = json.load(f)

print(f"Loaded: {loaded_data['employees'][0]['name']}")

# Clean up
import os
os.remove("employees.json")

# ============================================================
# Advanced Options
# ============================================================
# Example 7: JSON options
print("\n--- Advanced Options ---")

data = {"name": "Alice", "scores": [90, 85, 92]}

# sort_keys - sort dictionary keys
print(json.dumps(data, sort_keys=True))

# separators - custom separators
print(json.dumps(data, separators=(",", ":")))

# ensure_ascii - handle non-ASCII characters
data_unicode = {"name": "José", "city": "München"}
print(json.dumps(data_unicode, ensure_ascii=False))
print(json.dumps(data_unicode, ensure_ascii=True))

# default - handle non-serializable objects
def custom_serializer(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

from datetime import datetime
data_with_date = {
    "event": "Meeting",
    "date": datetime.now()
}

# This would fail:
# json.dumps(data_with_date)  # TypeError

# With custom serializer:
print(json.dumps(data_with_date, default=custom_serializer, indent=2))

# ============================================================
# Practical Examples
# ============================================================
# Example 8: Real-world JSON usage
print("\n--- Practical Examples ---")

# API response simulation
api_response = '''
{
    "status": "success",
    "data": {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ],
        "total": 2,
        "page": 1
    }
}
'''

response = json.loads(api_response)
print(f"Status: {response['status']}")
print(f"Total users: {response['data']['total']}")

for user in response['data']['users']:
    print(f"  - {user['name']} ({user['email']})")

# Configuration file
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp"
    },
    "debug": True,
    "log_level": "INFO"
}

# Save config
config_json = json.dumps(config, indent=2)
print(f"\nConfig:\n{config_json}")

# Parse config
loaded_config = json.loads(config_json)
print(f"\nDB Host: {loaded_config['database']['host']}")

# ============================================================
# Error Handling
# ============================================================
# Example 9: Handling JSON errors
print("\n--- Error Handling ---")

# Invalid JSON
invalid_json = '{"name": "Alice", age: 25}'  # age not quoted!

try:
    json.loads(invalid_json)
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")

# Type error
try:
    json.dumps({1, 2, 3})  # Sets aren't JSON serializable
except TypeError as e:
    print(f"Type Error: {e}")

# ============================================================
# Summary
# ============================================================
print("\n--- Summary ---")
print("1. json.dumps(): Python object to JSON string")
print("2. json.loads(): JSON string to Python object")
print("3. json.dump(): Python object to JSON file")
print("4. json.load(): JSON file to Python object")
print("5. indent parameter: pretty print JSON")
print("6. sort_keys: sort dictionary keys alphabetically")
print("7. Handle errors with try/except")
print("8. JSON types: object=dict, array=list, null=None")
