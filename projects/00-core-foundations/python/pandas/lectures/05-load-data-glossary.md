# Glossary 05: Loading Data

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| read_csv | Load CSV file into DataFrame | `pd.read_csv("data.csv")` |
| read_excel | Load Excel file into DataFrame | `pd.read_excel("data.xlsx")` |
| read_json | Load JSON file into DataFrame | `pd.read_json("data.json")` |
| read_sql | Load SQL query into DataFrame | `pd.read_sql(query, engine)` |
| read_parquet | Load Parquet file into DataFrame | `pd.read_parquet("data.parquet")` |
| to_csv | Save DataFrame as CSV | `df.to_csv("out.csv")` |
| to_excel | Save DataFrame as Excel | `df.to_excel("out.xlsx")` |
| to_json | Save DataFrame as JSON | `df.to_json("out.json")` |
| to_parquet | Save DataFrame as Parquet | `df.to_parquet("out.parquet")` |
| chunksize | Read file in chunks | `pd.read_csv("f.csv", chunksize=1000)` |
| encoding | Character encoding | `pd.read_csv("f.csv", encoding="latin-1")` |
| sep | Field delimiter | `pd.read_csv("f.tsv", sep="\t")` |
| usecols | Select specific columns | `pd.read_csv("f.csv", usecols=["A","B"])` |
| dtype | Specify column data types | `pd.read_csv("f.csv", dtype={"id": str})` |
| parse_dates | Parse date columns | `pd.read_csv("f.csv", parse_dates=["date"])` |

---

## Alphabetical Definitions

### C

**Chunksize**
The number of rows to read at a time when reading large files. Returns an iterator.

```python
for chunk in pd.read_csv("large.csv", chunksize=10000):
    process(chunk)
```

**CSV (Comma-Separated Values)**
A plain-text file format for tabular data where values are separated by commas.

```python
df = pd.read_csv("data.csv")
df.to_csv("output.csv", index=False)
```

### D

**Delimiter**
The character used to separate values in a text file. Default is comma for CSV.

```python
df = pd.read_csv("data.tsv", sep="\t")       # Tab-separated
df = pd.read_csv("data.csv", sep=";")         # Semicolon-separated
```

**Dtypes**
Data types to assign to specific columns when reading.

```python
df = pd.read_csv("data.csv", dtype={
    "id": "int32",
    "category": "category",
    "amount": "float32"
})
```

### E

**Encoding**
Character encoding of the file (UTF-8, latin-1, cp1252, etc.).

```python
df = pd.read_csv("data.csv", encoding="utf-8")
df = pd.read_csv("data.csv", encoding="latin-1")
```

**Excel**
Microsoft Excel spreadsheet format (.xlsx, .xls).

```python
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df.to_excel("output.xlsx", index=False)
```

### H

**HDF5**
Hierarchical Data Format version 5 — a file format for storing large numerical datasets.

```python
df.to_hdf("data.h5", key="df", mode="w")
df = pd.read_hdf("data.h5", key="df")
```

### I

**Index Col**
Specifies which column to use as the row index.

```python
df = pd.read_csv("data.csv", index_col="id")
```

### J

**JSON (JavaScript Object Notation)**
A lightweight data interchange format. Common for APIs.

```python
df = pd.read_json("data.json")
df.to_json("output.json", orient="records", indent=2)
```

### N

**Na Values**
Custom values to recognize as missing/NaN.

```python
df = pd.read_csv("data.csv", na_values=["N/A", "missing", "-"])
```

**Nrows**
Number of rows to read from the file.

```python
df = pd.read_csv("data.csv", nrows=1000)
```

### P

**Parquet**
A columnar storage format optimized for analytics. Efficient compression and encoding.

```python
df = pd.read_parquet("data.parquet")
df.to_parquet("output.parquet", compression="snappy")
```

**Pickle**
Python's native serialization format. Fast but not portable across languages.

```python
df.to_pickle("data.pkl")
df = pd.read_pickle("data.pkl")
```

### R

**Read Functions**
Pandas functions to load data from various formats.

```
pd.read_csv()      -> CSV
pd.read_excel()     -> Excel
pd.read_json()      -> JSON
pd.read_sql()       -> SQL
pd.read_parquet()   -> Parquet
pd.read_hdf()       -> HDF5
pd.read_pickle()    -> Pickle
```

### S

**Sep (Separator)**
The delimiter character for text files.

```python
df = pd.read_csv("data.csv", sep=",")     # Comma (default)
df = pd.read_csv("data.tsv", sep="\t")    # Tab
```

**Sheet Name**
Specifies which sheet to read from an Excel file.

```python
df = pd.read_excel("data.xlsx", sheet_name="Revenue")
sheets = pd.read_excel("data.xlsx", sheet_name=None)  # All sheets
```

### U

**Use Cols**
Selects specific columns to load from the file.

```python
df = pd.read_csv("data.csv", usecols=["Name", "Age", "City"])
```

---

## Code Examples

### Example 1: CSV with Options

```python
import pandas as pd

df = pd.read_csv(
    "data.csv",
    sep=",",
    header=0,
    index_col=None,
    usecols=["Name", "Age", "City"],
    dtype={"Age": int},
    parse_dates=["Date"],
    na_values=["N/A", "missing"],
    nrows=1000,
    encoding="utf-8"
)
```

### Example 2: Multiple Sheets Excel

```python
import pandas as pd

# Read all sheets
sheets = pd.read_excel("data.xlsx", sheet_name=None)
for name, sheet_df in sheets.items():
    print(f"Sheet: {name}, Shape: {sheet_df.shape}")

# Write multiple sheets
with pd.ExcelWriter("output.xlsx") as writer:
    df1.to_excel(writer, sheet_name="Sales", index=False)
    df2.to_excel(writer, sheet_name="Inventory", index=False)
```

### Example 3: Large File Processing

```python
import pandas as pd

# Process in chunks
total_rows = 0
for chunk in pd.read_csv("large.csv", chunksize=10000):
    # Filter and process
    filtered = chunk[chunk["amount"] > 100]
    total_rows += len(filtered)

print(f"Total rows matching filter: {total_rows}")
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| CSV | read_csv | File format |
| Excel | read_excel | File format |
| JSON | read_json | File format |
| Parquet | read_parquet | File format |
| Encoding | read_csv | Character set |
| Chunksize | read_csv | Memory management |
| Dtype | read_csv | Column types |
| Index Col | read_csv | Row index |

---

## Format Comparison

```
CSV:
  Pros: Universal, human-readable, simple
  Cons: No type info, large files slow, no compression
  Best for: Small-medium datasets, data exchange

Excel:
  Pros: Familiar, multiple sheets, formatting
  Cons: Slow, large files, licensing
  Best for: Business users, small datasets

JSON:
  Pros: Nested data, web APIs, flexible
  Cons: Verbose, slower to parse
  Best for: APIs, nested/hierarchical data

Parquet:
  Pros: Fast, compressed, columnar, typed
  Cons: Not human-readable, requires library
  Best for: Large analytical datasets

SQL:
  Pros: Direct database access, complex queries
  Cons: Requires connection, SQL knowledge
  Best for: Production data pipelines
```

---

## Self-Test Questions

1. How do you read a CSV file with a tab delimiter?
2. What does `chunksize` do in `pd.read_csv()`?
3. How do you read all sheets from an Excel file?
4. What encoding should you use for legacy Windows CSV files?
5. When would you use Parquet over CSV?
