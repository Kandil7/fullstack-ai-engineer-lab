# Python JSON — Glossary 28

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| JSON | JavaScript Object Notation | `{"key": "value"}` |
| dumps | Serialize Python object to string | `json.dumps(data)` |
| loads | Deserialize string to Python object | `json.loads(string)` |
| dump | Serialize Python object to file | `json.dump(data, f)` |
| load | Deserialize file to Python object | `json.load(f)` |
| Serialization | Converting object to string/bytes | `json.dumps()` |
| Deserialization | Converting string/bytes to object | `json.loads()` |
| Pretty Print | Formatted JSON with indentation | `json.dumps(data, indent=2)` |
| Encoder | Custom serializer for non-JSON types | `json.JSONEncoder` |
| Decoder | Custom deserializer | `object_hook` |
| JSON Decode Error | Invalid JSON syntax | `json.JSONDecodeError` |
| JSON Object | Key-value pairs `{}` | `{"name": "Alice"}` |
| JSON Array | Ordered list `[]` | `[1, 2, 3]` |
| JSON String | Double-quoted text | `"hello"` |
| JSON Number | Integer or float | `42`, `3.14` |
| JSON Boolean | true/false | `true`, `false` |
| JSON Null | Null value | `null` |
| MIME Type | JSON content type | `application/json` |
| API | Application Programming Interface | REST APIs |
| Schema | JSON structure definition | Validation |
| JSONL | JSON Lines (newline-delimited) | Big data |
| Minify | Remove whitespace from JSON | Compact |
| Escaping | Special character handling | `\"`, `\\` |

---

## Definitions

### Decoder
**Definition**: A function or class that converts JSON strings back into Python objects. Can be customized using `object_hook` or `object_pairs_hook` parameters.

**Example**:
```python
import json

# Default decoder
data = json.loads('{"name": "Alice", "age": 30}')

# Custom decoder
def custom_decode(dct):
    if "date" in dct:
        from datetime import datetime
        dct["date"] = datetime.fromisoformat(dct["date"])
    return dct

data = json.loads(json_str, object_hook=custom_decode)
```

**Related**: `loads()`, `object_hook`, deserialization

---

### Deserialization
**Definition**: The process of converting a JSON string or bytes into a Python object (dict, list, etc.).

**Example**:
```python
import json

json_string = '{"name": "Alice", "active": true}'
data = json.loads(json_string)  # Deserialization
print(data)  # {'name': 'Alice', 'active': True}
```

**Related**: serialization, `loads()`, `load()`, parsing

---

### Dump
**Definition**: A function that serializes a Python object and writes it directly to a file object.

**Example**:
```python
import json

data = {"name": "Alice", "age": 30}

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# File now contains:
# {
#   "name": "Alice",
#   "age": 30
# }
```

**Related**: `dumps()`, `load()`, file I/O

---

### Dumps
**Definition**: A function that serializes a Python object and returns it as a JSON-formatted string. The "s" stands for "string".

**Example**:
```python
import json

data = {"name": "Alice", "hobbies": ["reading", "coding"]}
json_string = json.dumps(data, indent=2)
print(json_string)
# {
#   "name": "Alice",
#   "hobbies": ["reading", "coding"]
# }
```

**Related**: `dump()`, `loads()`, serialization

---

### Encoder
**Definition**: A class that controls how Python objects are serialized to JSON. Override the `default()` method to handle non-serializable types.

**Example**:
```python
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

data = {"timestamp": datetime.now()}
json_str = json.dumps(data, cls=DateTimeEncoder)
```

**Related**: `dumps()`, `default()`, custom serialization

---

### Escaping
**Definition**: The process of replacing special characters with escape sequences to ensure valid JSON strings (e.g., `"` becomes `\"`).

**Example**:
```python
import json

# Special characters are escaped
text = 'He said "Hello"\nand \\ backslash'
data = {"text": text}
json_str = json.dumps(data)
print(json_str)  # {"text": "He said \"Hello\"\nand \\\\ backslash"}

# Ensure ASCII off for Unicode
data = {"name": "José"}
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)  # {"name": "José"}
```

**Related**: `ensure_ascii`, special characters, Unicode

---

### File I/O
**Definition**: Input/Output operations for reading from and writing to files. JSON provides `load()` and `dump()` for file operations.

**Example**:
```python
import json

# Write to file
data = {"config": {"theme": "dark", "lang": "en"}}
with open("config.json", "w") as f:
    json.dump(data, f, indent=2)

# Read from file
with open("config.json", "r") as f:
    config = json.load(f)

print(config)  # {'config': {'theme': 'dark', 'lang': 'en'}}
```

**Related**: `dump()`, `load()`, file handling

---

### JSON
**Definition**: JavaScript Object Notation — a lightweight, text-based data interchange format. Uses key-value pairs and arrays, readable by both humans and machines.

**Example**:
```json
{
  "name": "Alice",
  "age": 30,
  "active": true,
  "address": {
    "street": "123 Main St",
    "city": "New York"
  },
  "hobbies": ["reading", "coding"]
}
```

**Related**: API, serialization, data exchange, REST

---

### JSON Array
**Definition**: An ordered collection of values enclosed in square brackets `[]`. Can contain any JSON value type.

**Example**:
```python
import json

# JSON array
json_array = '[1, "hello", true, null, [1, 2, 3]]'
data = json.loads(json_array)
print(data)  # [1, 'hello', True, None, [1, 2, 3]]
```

**Related**: JSON object, list, serialization

---

### JSON Boolean
**Definition**: A JSON literal representing true or false. Maps to Python's `True` and `False`.

**Example**:
```python
import json

json_str = '{"active": true, "deleted": false}'
data = json.loads(json_str)
print(data)  # {'active': True, 'deleted': False}

# Python to JSON
print(json.dumps({"flag": True}))  # {"flag": true}
```

**Related**: JSON null, boolean, true/false

---

### JSON Decode Error
**Definition**: An exception raised when trying to parse invalid JSON syntax.

**Example**:
```python
import json

try:
    data = json.loads('{"name": "Alice"')  # Missing closing brace
except json.JSONDecodeError as e:
    print(f"Error: {e}")
    print(f"Line: {e.lineno}, Column: {e.colno}")
```

**Related**: `loads()`, error handling, validation

---

### JSON Lines
**Definition**: A format where each line is a separate JSON object (JSONL). Used for streaming and big data processing.

**Example**:
```python
import json

# JSONL file format:
# {"name": "Alice", "age": 30}
# {"name": "Bob", "age": 25}
# {"name": "Charlie", "age": 35}

def read_jsonl(filename):
    with open(filename, "r") as f:
        for line in f:
            yield json.loads(line.strip())

for record in read_jsonl("data.jsonl"):
    print(record)
```

**Related**: JSON, streaming, newline-delimited

---

### JSON Null
**Definition**: A JSON literal representing null/none. Maps to Python's `None`.

**Example**:
```python
import json

json_str = '{"name": "Alice", "score": null}'
data = json.loads(json_str)
print(data)  # {'name': 'Alice', 'score': None}

# Python to JSON
print(json.dumps({"value": None}))  # {"value": null}
```

**Related**: JSON boolean, None, null

---

### JSON Number
**Definition**: A JSON numeric value (integer or float). Maps to Python's `int` or `float`.

**Example**:
```python
import json

json_str = '{"count": 42, "price": 19.99}'
data = json.loads(json_str)
print(data)  # {'count': 42, 'price': 19.99}

print(type(data["count"]))  # <class 'int'>
print(type(data["price"]))  # <class 'float'>
```

**Related**: int, float, numeric types

---

### JSON Object
**Definition**: A collection of key-value pairs enclosed in curly braces `{}`. Keys must be strings, values can be any JSON type.

**Example**:
```python
import json

json_obj = '{"name": "Alice", "age": 30, "active": true}'
data = json.loads(json_obj)
print(data)  # {'name': 'Alice', 'age': 30, 'active': True}

# Python dict to JSON object
print(json.dumps({"x": 1, "y": 2}))  # {"x": 1, "y": 2}
```

**Related**: dict, JSON array, key-value

---

### JSON String
**Definition**: A sequence of characters enclosed in double quotes. The only acceptable quote character in JSON.

**Example**:
```python
import json

json_str = '{"message": "Hello, World!"}'
data = json.loads(json_str)
print(data["message"])  # Hello, World!

# Python string to JSON
print(json.dumps({"text": "Hello"}))  # {"text": "Hello"}
```

**Related**: string, double quotes, escaping

---

### Load
**Definition**: A function that reads JSON from a file object and deserializes it into a Python object.

**Example**:
```python
import json

with open("data.json", "r") as f:
    data = json.load(f)

print(data)
```

**Related**: `loads()`, `dump()`, file I/O

---

### Loads
**Definition**: A function that deserializes a JSON string into a Python object. The "s" stands for "string".

**Example**:
```python
import json

json_string = '{"name": "Alice", "age": 30}'
data = json.loads(json_string)
print(data)  # {'name': 'Alice', 'age': 30}
```

**Related**: `load()`, `dumps()`, parsing

---

### Minify
**Definition**: Removing all unnecessary whitespace from JSON to create the smallest possible representation.

**Example**:
```python
import json

data = {"name": "Alice", "hobbies": ["reading", "coding"]}

# Pretty printed
pretty = json.dumps(data, indent=2)
print(pretty)

# Minified (compact)
compact = json.dumps(data, separators=(',', ':'))
print(compact)  # {"name":"Alice","hobbies":["reading","coding"]}
```

**Related**: compact, whitespace, optimization

---

### MIME Type
**Definition**: The content type for JSON data in HTTP requests/responses: `application/json`.

**Example**:
```python
# In HTTP requests
headers = {"Content-Type": "application/json"}

# In API responses
response.headers["Content-Type"] = "application/json"
```

**Related**: HTTP, API, Content-Type

---

### Pretty Print
**Definition**: Formatting JSON with indentation and line breaks for human readability.

**Example**:
```python
import json

data = {"name": "Alice", "address": {"city": "NYC"}}

# Compact (no whitespace)
compact = json.dumps(data)
print(compact)  # {"name": "Alice", "address": {"city": "NYC"}}

# Pretty printed
pretty = json.dumps(data, indent=4)
print(pretty)
# {
#     "name": "Alice",
#     "address": {
#         "city": "NYC"
#     }
# }
```

**Related**: indent, formatting, readability

---

### Schema
**Definition**: A structure definition for JSON data, specifying required fields, data types, and constraints. Used for validation.

**Example**:
```python
# JSON Schema example
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0}
    },
    "required": ["name"]
}

# Validation with jsonschema library
from jsonschema import validate
validate(instance={"name": "Alice"}, schema=schema)
```

**Related**: validation, jsonschema, structure

---

### Serialization
**Definition**: The process of converting a Python object into a JSON string or bytes for storage or transmission.

**Example**:
```python
import json

data = {"name": "Alice", "scores": [85, 92, 78]}
json_string = json.dumps(data)  # Serialization
print(json_string)

# Write to file
with open("data.json", "w") as f:
    json.dump(data, f)  # Serialization to file
```

**Related**: deserialization, `dumps()`, `dump()`, encoding

---

## Code Examples

### Example 1: API Response Handler
```python
import json

def handle_api_response(response_text):
    """Parse and validate API response."""
    try:
        data = json.loads(response_text)
        if "error" in data:
            raise ValueError(data["error"])
        return data
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {e}"}

response = '{"status": "ok", "data": [1, 2, 3]}'
result = handle_api_response(response)
print(result)  # {'status': 'ok', 'data': [1, 2, 3]}
```

### Example 2: JSON Transformer
```python
import json

def transform_json(data, key_map):
    """Rename keys in JSON data."""
    if isinstance(data, dict):
        return {key_map.get(k, k): transform_json(v, key_map) 
                for k, v in data.items()}
    elif isinstance(data, list):
        return [transform_json(item, key_map) for item in data]
    return data

data = {"firstName": "Alice", "lastName": "Smith", "age": 30}
mapping = {"firstName": "first_name", "lastName": "last_name"}
result = transform_json(data, mapping)
print(json.dumps(result, indent=2))
```

---

## Related Concepts

- **XML**: Alternative data format (more verbose)
- **YAML**: Human-readable alternative to JSON
- **CSV**: Tabular data format
- **Protocol Buffers**: Binary serialization format
- **MessagePack**: Binary JSON alternative
- **Avro**: Data serialization system
