# Glossary 06: Reading JSON Data

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| JSON | JavaScript Object Notation | `{"key": "value"}` |
| Orient | JSON structure format | `pd.read_json(orient="records")` |
| json_normalize | Flatten nested JSON | `pd.json_normalize(data)` |
| records | Array of objects (default orient) | `[{"a": 1}, {"a": 2}]` |
| columns | Object of objects | `{"a": {"0": 1}}` |
| index | Object of objects (keys are indices) | `{"0": {"a": 1}}` |
| split | Separated index/columns/data | `{"index": [], "columns": [], "data": []}` |
| values | Array of arrays | `[[1, 2], [3, 4]]` |
| Nested JSON | JSON with nested objects/arrays | `{"a": {"b": 1}}` |
| Flatten | Convert nested to flat structure | `pd.json_normalize()` |
| Explode | Expand array column to rows | `df.explode("col")` |
| Null | JSON null value (becomes NaN) | `{"key": null}` |

---

## Alphabetical Definitions

### C

**Columns Orient**
JSON structure where outer keys are column names and inner keys are row indices.

```json
{
    "Name": {"0": "Alice", "1": "Bob"},
    "Age": {"0": 28, "1": 35}
}
```

```python
pd.read_json(data, orient="columns")
```

### E

**Explode**
Transforms each element of an array column into a separate row.

```python
df = pd.DataFrame({"Name": ["Alice"], "Skills": [["Python", "SQL"]]})
df_exploded = df.explode("Skills")
#    Name  Skills
# 0  Alice  Python
# 0  Alice     SQL
```

### I

**Index Orient**
JSON structure where outer keys are row indices and inner keys are column names.

```json
{
    "0": {"Name": "Alice", "Age": 28},
    "1": {"Name": "Bob", "Age": 35}
}
```

```python
pd.read_json(data, orient="index")
```

### J

**JSON (JavaScript Object Notation)**
A lightweight data interchange format using key-value pairs and arrays.

```json
{
    "name": "Alice",
    "age": 28,
    "hobbies": ["reading", "coding"]
}
```

**json_normalize**
Pandas function to flatten nested JSON into a flat DataFrame.

```python
df = pd.json_normalize(data, sep="_")
```

### N

**Nested JSON**
JSON data containing objects within objects or arrays within objects.

```json
{
    "user": {
        "name": "Alice",
        "address": {"city": "NYC", "zip": "10001"}
    }
}
```

**Null**
JSON's representation of no value. Becomes NaN in Pandas.

```json
{"name": "Alice", "email": null}
```

### O

**Orient**
The structure/format of the JSON data.

```python
pd.read_json(data, orient="records")  # Default
```

### P

**Pretty Print**
Formatted JSON output with indentation for readability.

```python
df.to_json("out.json", indent=2)
```

### R

**Records Orient**
Array of objects where each object is a row. Most common format.

```json
[
    {"Name": "Alice", "Age": 28},
    {"Name": "Bob", "Age": 35}
]
```

```python
pd.read_json(data, orient="records")  # Default
```

### S

**Split Orient**
JSON with separate keys for index, columns, and data.

```json
{
    "index": [0, 1],
    "columns": ["Name", "Age"],
    "data": [["Alice", 28], ["Bob", 35]]
}
```

```python
pd.read_json(data, orient="split")
```

### V

**Values Orient**
Array of arrays with no headers or indices.

```json
[
    ["Alice", 28],
    ["Bob", 35]
]
```

```python
pd.read_json(data, orient="values", columns=["Name", "Age"])
```

---

## Code Examples

### Example 1: Basic JSON Reading

```python
import pandas as pd

# From string
json_str = '[{"Name": "Alice", "Age": 28}, {"Name": "Bob", "Age": 35}]'
df = pd.read_json(json_str, orient="records")
print(df)
```

### Example 2: Nested JSON

```python
import pandas as pd
import json

data = {
    "users": [
        {"id": 1, "name": "Alice", "address": {"city": "NYC"}},
        {"id": 2, "name": "Bob", "address": {"city": "London"}}
    ]
}

df = pd.json_normalize(data["users"], sep="_")
print(df)
#    id   name address_city
# 0   1  Alice         NYC
# 1   2    Bob      London
```

### Example 3: Explode Arrays

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Skills": [["Python", "SQL"], ["Java", "Go"]]
})

df_exploded = df.explode("Skills")
print(df_exploded)
#    Name  Skills
# 0  Alice  Python
# 0  Alice     SQL
# 1    Bob    Java
# 1    Bob      Go
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| JSON | read_json | File format |
| orient | read_json | Structure specification |
| json_normalize | Nested JSON | Flattening function |
| explode | Array columns | Expand to rows |
| null | Missing data | Becomes NaN |
| records | orient | Default structure |
| API | JSON | Common data source |

---

## Orient Comparison

```
records (default):
  Structure: Array of objects
  Use when: Each object is a row
  Example: [{"a": 1}, {"a": 2}]

columns:
  Structure: Object of objects
  Use when: Outer keys are columns
  Example: {"a": {"0": 1, "1": 2}}

index:
  Structure: Object of objects
  Use when: Outer keys are row indices
  Example: {"0": {"a": 1}, "1": {"a": 2}}

split:
  Structure: Separated keys
  Use when: Need to preserve index/columns
  Example: {"index": [0,1], "columns": ["a"], "data": [[1],[2]]}

values:
  Structure: Array of arrays
  Use when: No headers or indices
  Example: [[1, 2], [3, 4]]
```

---

## Self-Test Questions

1. What is the default orient for `pd.read_json()`?
2. How do you flatten nested JSON?
3. What happens to JSON null values in Pandas?
4. How do you expand an array column into rows?
5. When would you use `orient="columns"` vs `orient="records"`?
