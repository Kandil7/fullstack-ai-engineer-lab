# Lecture 06: Reading JSON Data

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Understand JSON structure (objects, arrays, nested data)
- Read JSON files with different orientations
- Handle nested JSON and flatten it
- Parse JSON from APIs
- Convert between JSON and DataFrames

---

## 📖 1. What is JSON?

JSON (JavaScript Object Notation) is a lightweight data interchange format. It is the most common format for web APIs and configuration files.

### JSON Structure

```json
{
  "name": "Alice",
  "age": 28,
  "city": "New York",
  "hobbies": ["reading", "hiking", "coding"],
  "address": {
    "street": "123 Main St",
    "zip": "10001"
  }
}
```

### JSON vs CSV

| Aspect | JSON | CSV |
|---|---|---|
| Structure | Nested/hierarchical | Flat/tabular |
| Readability | Good | Good |
| Size | Larger (verbose) | Smaller |
| Types | Native (string, number, bool, null) | All strings |
| Nesting | Supported | Not supported |

---

## 📖 2. Basic JSON Reading

### From a File

```python
import pandas as pd

# Simple JSON (records format)
df = pd.read_json("data.json")
print(df)
```

### From a JSON String

```python
import pandas as pd
import json

json_string = '''
[
    {"Name": "Alice", "Age": 28, "City": "New York"},
    {"Name": "Bob", "Age": 35, "City": "London"},
    {"Name": "Charlie", "Age": 42, "City": "Paris"}
]
'''

df = pd.read_json(json_string)
print(df)
#       Name  Age      City
# 0    Alice   28  New York
# 1      Bob   35    London
# 2  Charlie   42     Paris
```

### From a URL

```python
import pandas as pd

# JSON API endpoint
df = pd.read_json("https://api.example.com/data")
```

---

## 📖 3. JSON Orientations

JSON can store data in different structures. Pandas uses the `orient` parameter to understand the structure.

### Orient: "records" (Default)

Array of objects — each object is a row.

```json
[
    {"Name": "Alice", "Age": 28},
    {"Name": "Bob", "Age": 35}
]
```

```python
import pandas as pd

df = pd.read_json('''
[
    {"Name": "Alice", "Age": 28},
    {"Name": "Bob", "Age": 35}
]
''', orient="records")
```

### Orient: "columns"

Object of objects — outer keys are column names.

```json
{
    "Name": {"0": "Alice", "1": "Bob"},
    "Age": {"0": 28, "1": 35}
}
```

```python
df = pd.read_json('''
{
    "Name": {"0": "Alice", "1": "Bob"},
    "Age": {"0": 28, "1": 35}
}
''', orient="columns")
```

### Orient: "index"

Object of objects — outer keys are row indices.

```json
{
    "0": {"Name": "Alice", "Age": 28},
    "1": {"Name": "Bob", "Age": 35}
}
```

```python
df = pd.read_json('''
{
    "0": {"Name": "Alice", "Age": 28},
    "1": {"Name": "Bob", "Age": 35}
}
''', orient="index")
```

### Orient: "values"

Array of arrays — no headers or indices.

```json
[
    ["Alice", 28],
    ["Bob", 35]
]
```

```python
df = pd.read_json('''
[
    ["Alice", 28],
    ["Bob", 35]
]
''', orient="values", columns=["Name", "Age"])
```

### Orient: "split"

Separated keys for index, columns, and data.

```json
{
    "index": [0, 1],
    "columns": ["Name", "Age"],
    "data": [["Alice", 28], ["Bob", 35]]
}
```

```python
df = pd.read_json('''
{
    "index": [0, 1],
    "columns": ["Name", "Age"],
    "data": [["Alice", 28], ["Bob", 35]]
}
''', orient="split")
```

---

## 📖 4. Nested JSON

Real-world JSON often has nested structures. We need to flatten it.

### Example: Nested JSON

```json
{
    "results": [
        {
            "id": 1,
            "name": "Alice",
            "contact": {
                "email": "alice@example.com",
                "phone": "555-1234"
            },
            "scores": [92, 85, 88]
        },
        {
            "id": 2,
            "name": "Bob",
            "contact": {
                "email": "bob@example.com",
                "phone": "555-5678"
            },
            "scores": [78, 90, 82]
        }
    ]
}
```

### Flattening Nested JSON

```python
import pandas as pd
import json

data = {
    "results": [
        {
            "id": 1,
            "name": "Alice",
            "contact": {"email": "alice@example.com", "phone": "555-1234"},
            "scores": [92, 85, 88]
        },
        {
            "id": 2,
            "name": "Bob",
            "contact": {"email": "bob@example.com", "phone": "555-5678"},
            "scores": [78, 90, 82]
        }
    ]
}

# Extract the records
df = pd.json_normalize(data["results"])
print(df)
#    id   name                              contact       scores
# 0   1  Alice  {'email': 'alice@example.com', ...}  [92, 85, 88]
# 1   2    Bob  {'email': 'bob@example.com', ...}    [78, 90, 82]
```

### Deep Flattening

```python
# Flatten nested objects with dot notation
df = pd.json_normalize(data["results"], sep="_")
print(df)
#    id   name contact_email    contact_phone      scores
# 0   1  Alice  alice@example.com  555-1234    [92, 85, 88]
# 1   2    Bob  bob@example.com    555-5678    [78, 90, 82]

# Fully flatten (expand lists)
df = pd.json_normalize(
    data["results"],
    sep="_",
    record_path=None
)
```

### Handling Arrays in JSON

```python
import pandas as pd

# JSON with array field
json_data = '''
[
    {
        "id": 1,
        "name": "Alice",
        "scores": [92, 85, 88]
    },
    {
        "id": 2,
        "name": "Bob",
        "scores": [78, 90, 82]
    }
]
'''

df = pd.read_json(json_data, orient="records")
print(df)
#    id   name        scores
# 0   1  Alice  [92, 85, 88]
# 1   2    Bob  [78, 90, 82]

# Explode array column into rows
df_exploded = df.explode("scores")
print(df_exploded)
#    id   name scores
# 0   1  Alice     92
# 0   1  Alice     85
# 0   1  Alice     88
# 1   2    Bob     78
# 1   2    Bob     90
# 1   2    Bob     82
```

---

## 📖 5. Writing JSON

### Basic Writing

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42]
})

# Save with different orientations
df.to_json("output_records.json", orient="records", indent=2)
df.to_json("output_columns.json", orient="columns")
df.to_json("output_index.json", orient="index")
df.to_json("output_split.json", orient="split")
df.to_json("output_values.json", orient="values")
```

### Pretty Print

```python
import json

# Save with pretty formatting
df.to_json("output.json", orient="records", indent=2, force_ascii=False)

# Or use json module for more control
data = df.to_dict(orient="records")
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

---

## 📖 6. JSON from APIs

### Using requests + pandas

```python
import pandas as pd
import requests

# Fetch JSON from API
response = requests.get("https://api.example.com/data")
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data)
# or
df = pd.json_normalize(data)
```

### Real API Example

```python
import pandas as pd
import requests

# GitHub API
response = requests.get("https://api.github.com/repos/pandas-dev/pandas/issues")
issues = response.json()

df = pd.json_normalize(issues)
print(df[["title", "state", "created_at", "user.login"]])
```

---

## 📖 7. Common JSON Patterns

### Pattern 1: API Response Wrapper

```json
{
    "status": "success",
    "data": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ],
    "count": 2
}
```

```python
import pandas as pd
import json

response = json.loads(json_string)
df = pd.DataFrame(response["data"])
```

### Pattern 2: Paginated Results

```python
import pandas as pd
import requests

all_data = []
page = 1

while True:
    response = requests.get(f"https://api.example.com/data?page={page}")
    data = response.json()
    
    if not data["results"]:
        break
    
    all_data.extend(data["results"])
    page += 1

df = pd.DataFrame(all_data)
```

### Pattern 3: Grouped Data

```json
{
    "group1": [{"id": 1}, {"id": 2}],
    "group2": [{"id": 3}, {"id": 4}]
}
```

```python
import pandas as pd

data = json.loads(json_string)
records = []
for group_name, items in data.items():
    for item in items:
        item["group"] = group_name
        records.append(item)

df = pd.DataFrame(records)
```

---

## 📖 8. Real-World Example

```python
import pandas as pd
import json

# Sample nested JSON data
json_data = '''
{
    "employees": [
        {
            "id": 1,
            "name": "Alice",
            "department": "Engineering",
            "skills": ["Python", "SQL", "Pandas"],
            "address": {
                "city": "New York",
                "state": "NY"
            }
        },
        {
            "id": 2,
            "name": "Bob",
            "department": "Marketing",
            "skills": ["SEO", "Analytics"],
            "address": {
                "city": "London",
                "state": null
            }
        }
    ]
}
'''

# Parse and flatten
data = json.loads(json_data)
df = pd.json_normalize(data["employees"], sep="_")

print("Flattened DataFrame:")
print(df)

# Explode skills
df_skills = df.explode("skills")
print("\nSkills Exploded:")
print(df_skills)

# Group by department
print("\nEmployees by Department:")
print(df.groupby("department")["name"].apply(list))
```

---

## ❌ 9. Common Mistakes

### Mistake 1: Wrong Orient

```python
import pandas as pd

# Bad — wrong orient
# df = pd.read_json("data.json", orient="columns")  # If data is records

# Good — match the actual structure
df = pd.read_json("data.json", orient="records")
```

### Mistake 2: Not Flattening Nested Data

```python
# Bad — nested data in DataFrame
df = pd.read_json("nested.json")
print(df["contact"])  # Returns dict, not columns

# Good — flatten first
df = pd.json_normalize(data["results"])
```

### Mistake 3: Not Handling Null Values

```python
import pandas as pd

# JSON null becomes NaN in pandas
df = pd.read_json("data.json")
print(df.isnull().sum())  # Check for nulls
```

---

## ✅ 10. Best Practices

1. **Identify the orient** — check JSON structure before reading
2. **Use `json_normalize`** — for nested JSON
3. **Check for nulls** — JSON nulls become NaN
4. **Validate after loading** — check shape, dtypes, nulls
5. **Use `indent`** — for human-readable output
6. **Handle encoding** — use `force_ascii=False` for unicode
7. **Cache API responses** — avoid repeated requests

---

## 🏋️ 11. Exercises

### Exercise 1: Basic JSON

```python
import pandas as pd

# TODO: Create this JSON string and read it:
# [
#     {"product": "Laptop", "price": 999, "specs": {"ram": "16GB", "storage": "512GB"}},
#     {"product": "Phone", "price": 699, "specs": {"ram": "8GB", "storage": "256GB"}}
# ]

# TODO: Flatten the nested "specs" column
# TODO: Calculate average price
```

### Exercise 2: API Data

```python
import pandas as pd
import requests

# TODO: Fetch this API and create a DataFrame:
# https://jsonplaceholder.typicode.com/posts

# TODO: Print shape, head, and dtypes
# TODO: Find the user with most posts
```

### Exercise 3: Nested JSON

```python
import pandas as pd
import json

# TODO: Create nested JSON with orders:
# - order_id
# - customer name
# - items (array of {product, quantity, price})
# - shipping address (nested object)

# TODO: Flatten to get one row per item
# TODO: Calculate total per order
```

---

## 📝 12. Summary

| Concept | What You Learned |
|---|---|
| JSON Structure | Objects, arrays, nesting |
| Orientations | records, columns, index, split, values |
| Reading | `pd.read_json()` with orient parameter |
| Nested JSON | `pd.json_normalize()` to flatten |
| Writing | `df.to_json()` with orient and indent |
| APIs | `requests.get().json()` + DataFrame |
| Exploding | `.explode()` for array columns |

### Next Lecture

In [Lecture 07: Data Viewing](./07-data-viewing-lecture.md), we will explore techniques for viewing and inspecting data in DataFrames.

---

## 📚 Further Reading

- [Pandas read_json Documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_json.html)
- [Pandas json_normalize Documentation](https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html)
- [JSON.org Specification](https://www.json.org/)
