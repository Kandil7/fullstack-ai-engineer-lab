"""
Reading JSON Data with Pandas
W3Schools: https://www.w3schools.com/python/pandas_json.asp

JSON (JavaScript Object Notation) is a lightweight data-interchange format
that is easy for humans to read and write. Pandas can easily read and
parse JSON data.
"""
import pandas as pd
import json
import io
import os
import tempfile

# ---------------------------------------------------------------------------
# Example 1: Reading JSON from a dictionary
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 1: DataFrame from Dictionary (JSON-like)")
print("=" * 60)

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "London", "Paris"],
}
df = pd.DataFrame(data)
print(df)
print()

# ---------------------------------------------------------------------------
# Example 2: Reading a JSON file
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 2: Read JSON File")
print("=" * 60)

json_data = [
    {"id": 1, "product": "Laptop", "price": 999.99, "category": "Electronics"},
    {"id": 2, "product": "Book", "price": 19.99, "category": "Education"},
    {"id": 3, "product": "Headphones", "price": 79.99, "category": "Electronics"},
    {"id": 4, "product": "Backpack", "price": 49.99, "category": "Travel"},
    {"id": 5, "product": "Keyboard", "price": 129.99, "category": "Electronics"},
]

json_path = os.path.join(tempfile.gettempdir(), "pandas_ex06_data.json")
with open(json_path, "w") as f:
    json.dump(json_data, f, indent=2)

df_products = pd.read_json(json_path)
print("Products from JSON:")
print(df_products)
print()

# ---------------------------------------------------------------------------
# Example 3: JSON with nested data
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 3: Nested JSON")
print("=" * 60)

nested_data = {
    "employees": [
        {
            "name": "Alice",
            "details": {"department": "Engineering", "level": "Senior"},
            "skills": ["Python", "SQL", "AWS"],
        },
        {
            "name": "Bob",
            "details": {"department": "Marketing", "level": "Junior"},
            "skills": ["SEO", "Content"],
        },
        {
            "name": "Charlie",
            "details": {"department": "Engineering", "level": "Lead"},
            "skills": ["Python", "Go", "Docker"],
        },
    ]
}

# Use json_normalize to flatten nested structures
from pandas import json_normalize

df_nested = json_normalize(
    nested_data["employees"],
    sep="_"
)
print("Flattened nested JSON:")
print(df_nested)
print()

# ---------------------------------------------------------------------------
# Example 4: Different JSON orientations
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 4: JSON Orientations")
print("=" * 60)

df_demo = pd.DataFrame({
    "fruit": ["apple", "banana", "cherry"],
    "count": [10, 25, 15],
})

# records (list of objects) – most common
records_json = df_demo.to_json(orient="records", indent=2)
print("Orient 'records':")
print(records_json)
print()

# columns (dict of column lists)
columns_json = df_demo.to_json(orient="columns", indent=2)
print("Orient 'columns':")
print(columns_json)
print()

# index (dict of row dicts)
index_json = df_demo.to_json(orient="index", indent=2)
print("Orient 'index':")
print(index_json)
print()

# Split
split_json = df_demo.to_json(orient="split", indent=2)
print("Orient 'split':")
print(split_json)
print()

# ---------------------------------------------------------------------------
# Example 5: Reading JSON from a URL-like string
# ---------------------------------------------------------------------------

print("=" * 60)
print("Example 5: Inline JSON String")
print("=" * 60)

json_str = '[{"city":"Rome","pop":2873000},{"city":"Berlin","pop":3645000}]'
df_cities = pd.read_json(io.StringIO(json_str))
print("Cities from inline JSON:")
print(df_cities)
print()

# Clean up
os.remove(json_path)
print("Done!")
