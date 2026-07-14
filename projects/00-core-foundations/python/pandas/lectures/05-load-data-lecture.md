# Lecture 05: Loading Data

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Load data from CSV, Excel, JSON, and other formats
- Understand common read parameters (header, index_col, dtype)
- Handle encoding issues and large files
- Validate data after loading
- Save DataFrames to various formats

---

## 📖 1. CSV Files

CSV (Comma-Separated Values) is the most common data format.

### Basic CSV Reading

```python
import pandas as pd

# From a local file
df = pd.read_csv("data.csv")

# From a URL
df = pd.read_csv("https://raw.githubusercontent.com/example/data.csv")
```

### Common Parameters

```python
import pandas as pd

# Specify delimiter (for tab-separated, semicolon, etc.)
df = pd.read_csv("data.tsv", sep="\t")
df = pd.read_csv("data.csv", sep=";")

# Use a column as index
df = pd.read_csv("data.csv", index_col=0)

# Parse dates
df = pd.read_csv("data.csv", parse_dates=["date_column"])

# Specify data types
df = pd.read_csv("data.csv", dtype={"id": str, "amount": float})

# Skip rows
df = pd.read_csv("data.csv", skiprows=3)        # Skip first 3 rows
df = pd.read_csv("data.csv", skiprows=[1, 3])    # Skip specific rows

# Select columns
df = pd.read_csv("data.csv", usecols=["Name", "Age", "City"])

# Handle missing values
df = pd.read_csv("data.csv", na_values=["N/A", "missing", ""])

# Limit rows
df = pd.read_csv("data.csv", nrows=100)          # Read only 100 rows
```

### Writing CSV

```python
# Save to CSV
df.to_csv("output.csv", index=False)

# Save with specific encoding
df.to_csv("output.csv", encoding="utf-8-sig")

# Save with specific separator
df.to_csv("output.tsv", sep="\t", index=False)
```

---

## 📖 2. Excel Files

### Reading Excel

```python
import pandas as pd

# Basic read
df = pd.read_excel("data.xlsx")

# Read specific sheet
df = pd.read_excel("data.xlsx", sheet_name="Sheet2")

# Read by sheet index
df = pd.read_excel("data.xlsx", sheet_name=0)

# Read multiple sheets
sheets = pd.read_excel("data.xlsx", sheet_name=None)  # Returns dict of DataFrames
print(sheets.keys())  # dict_keys(['Sheet1', 'Sheet2'])

# Specify header row
df = pd.read_excel("data.xlsx", header=1)

# Use column as index
df = pd.read_excel("data.xlsx", index_col=0)

# Parse dates
df = pd.read_excel("data.xlsx", parse_dates=["Date"])
```

### Writing Excel

```python
# Save to Excel
df.to_excel("output.xlsx", index=False)

# Save to specific sheet
df.to_excel("output.xlsx", sheet_name="Data", index=False)

# Save multiple DataFrames to one file
with pd.ExcelWriter("output.xlsx") as writer:
    df1.to_excel(writer, sheet_name="Sheet1", index=False)
    df2.to_excel(writer, sheet_name="Sheet2", index=False)
```

### Required Package

```bash
pip install openpyxl  # For .xlsx files
```

---

## 📖 3. JSON Files

### Reading JSON

```python
import pandas as pd

# Basic JSON (records format)
df = pd.read_json("data.json")

# Nested JSON
df = pd.read_json("data.json", orient="records")

# Different orientations
df = pd.read_json("data.json", orient="columns")
df = pd.read_json("data.json", orient="index")
df = pd.read_json("data.json", orient="values")
```

### Writing JSON

```python
# Save to JSON
df.to_json("output.json", orient="records", indent=2)

# Different orientations
df.to_json("output.json", orient="columns")
df.to_json("output.json", orient="index")
```

---

## 📖 4. SQL Databases

### Reading from SQL

```python
import pandas as pd
from sqlalchemy import create_engine

# Create engine
engine = create_engine("sqlite:///database.db")
# engine = create_engine("postgresql://user:pass@host:5432/db")
# engine = create_engine("mysql://user:pass@host:3306/db")

# Read entire table
df = pd.read_sql("SELECT * FROM users", engine)

# Read with query
df = pd.read_sql("SELECT * FROM users WHERE age > 30", engine)

# Read with parameters
df = pd.read_sql(
    "SELECT * FROM users WHERE age > :min_age",
    engine,
    params={"min_age": 30}
)

# Read table by name
df = pd.read_sql_table("users", engine)
```

### Writing to SQL

```python
# Write DataFrame to SQL
df.to_sql("users", engine, if_exists="replace", index=False)

# Append to existing table
df.to_sql("users", engine, if_exists="append", index=False)
```

---

## 📖 5. Parquet Files

Parquet is a columnar storage format optimized for analytics.

### Reading Parquet

```python
import pandas as pd

df = pd.read_parquet("data.parquet")

# Read specific columns
df = pd.read_parquet("data.parquet", columns=["Name", "Age"])
```

### Writing Parquet

```python
df.to_parquet("output.parquet", index=False)

# With compression
df.to_parquet("output.parquet", compression="snappy")
```

### Required Package

```bash
pip install pyarrow  # or fastparquet
```

---

## 📖 6. Other Formats

### HDF5

```python
# Write
df.to_hdf("data.h5", key="df", mode="w")

# Read
df = pd.read_hdf("data.h5", key="df")
```

### Pickle

```python
# Write
df.to_pickle("data.pkl")

# Read
df = pd.read_pickle("data.pkl")
```

### Clipboard

```python
# Read from clipboard (e.g., copied from Excel)
df = pd.read_clipboard()

# Copy DataFrame to clipboard
df.to_clipboard()
```

---

## 📖 7. Handling Large Files

### Read in Chunks

```python
import pandas as pd

# Process large file in chunks
chunk_size = 10000
chunks = []

for chunk in pd.read_csv("large_file.csv", chunksize=chunk_size):
    # Process each chunk
    filtered = chunk[chunk["amount"] > 100]
    chunks.append(filtered)

# Combine results
result = pd.concat(chunks, ignore_index=True)
```

### Process and Write Incrementally

```python
import pandas as pd

# Write header first
first_chunk = True

for chunk in pd.read_csv("large_file.csv", chunksize=10000):
    processed = chunk[chunk["amount"] > 100]
    
    processed.to_csv(
        "filtered_output.csv",
        mode="a" if not first_chunk else "w",
        header=first_chunk,
        index=False
    )
    first_chunk = False
```

### Memory Optimization

```python
import pandas as pd

# Optimize data types to reduce memory
df = pd.read_csv("data.csv", dtype={
    "id": "int32",           # Instead of int64
    "category": "category",  # Instead of object
    "flag": "bool"           # Instead of int
})

# Check memory usage
print(df.memory_usage(deep=True).sum())

# Optimize automatically
df = pd.read_csv("data.csv")
df = df.convert_dtypes()
```

---

## 📖 8. Encoding Issues

```python
import pandas as pd

# Common encodings
df = pd.read_csv("data.csv", encoding="utf-8")
df = pd.read_csv("data.csv", encoding="latin-1")  # Common for legacy data
df = pd.read_csv("data.csv", encoding="cp1252")   # Windows encoding
df = pd.read_csv("data.csv", encoding="utf-8-sig") # BOM handling

# Detect encoding
# pip install chardet
import chardet

with open("data.csv", "rb") as f:
    result = chardet.detect(f.read())
    print(result)
# {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
```

---

## 📖 9. Validating Data After Loading

```python
import pandas as pd

df = pd.read_csv("data.csv")

# Check shape
print("Shape:", df.shape)

# Check data types
print("\nData types:")
print(df.dtypes)

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check for duplicates
print("\nDuplicate rows:", df.duplicated().sum())

# Check unique values in key columns
print("\nUnique values:")
for col in df.select_dtypes(include=["object"]).columns:
    print(f"{col}: {df[col].nunique()} unique")

# Check basic statistics
print("\nStatistics:")
print(df.describe())

# Check for outliers
print("\nOutlier check:")
for col in df.select_dtypes(include=["number"]).columns:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    outliers = ((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)).sum()
    print(f"{col}: {outliers} outliers")
```

---

## 📖 10. Real-World Example

```python
import pandas as pd

# Load a public dataset
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
df = pd.read_csv(url)

# Initial validation
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())
print("\nBasic statistics:")
print(df.describe())

# Save to multiple formats
df.to_csv("tips.csv", index=False)
df.to_json("tips.json", orient="records", indent=2)
```

---

## ❌ 11. Common Mistakes

### Mistake 1: Not Specifying Index Column

```python
# Bad — creates a redundant index column
df = pd.read_csv("data.csv")
# Output CSV will have an extra index column

# Good — skip index when saving
df.to_csv("output.csv", index=False)
```

### Mistake 2: Not Handling Encoding

```python
# Bad — may fail on non-UTF-8 files
# df = pd.read_csv("legacy_data.csv")

# Good — specify encoding
df = pd.read_csv("legacy_data.csv", encoding="latin-1")
```

### Mistake 3: Reading Entire Large File

```python
# Bad — memory error on large files
# df = pd.read_csv("huge_file.csv")

# Good — read in chunks
for chunk in pd.read_csv("huge_file.csv", chunksize=10000):
    process(chunk)
```

---

## ✅ 12. Best Practices

1. **Validate after loading** — check shape, dtypes, nulls, duplicates
2. **Specify dtypes** — prevent memory waste and type errors
3. **Use `usecols`** — load only needed columns
4. **Handle encoding** — specify encoding for non-UTF-8 files
5. **Chunk large files** — avoid memory errors
6. **Use Parquet** — for large analytical datasets
7. **Always check `head()`** — verify data loaded correctly
8. **Skip index when saving** — avoid redundant index columns

---

## 🏋️ 13. Exercises

### Exercise 1: CSV Loading

```python
import pandas as pd

# TODO: Load this CSV with all common parameters:
# URL: "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"

# TODO: Specify dtypes for key columns
# TODO: Parse the "date" column (if exists)
# TODO: Select only relevant columns
```

### Exercise 2: Multiple Formats

```python
import pandas as pd

# TODO: Load the tips dataset
# TODO: Save it as CSV, JSON, and Excel
# TODO: Reload each format and verify they match
```

### Exercise 3: Large File Simulation

```python
import pandas as pd
import numpy as np

# TODO: Create a large DataFrame (1M rows)
# TODO: Save to CSV
# TODO: Read it back in chunks of 100K
# TODO: Verify the result matches the original
```

---

## 📝 14. Summary

| Format | Read | Write |
|---|---|---|
| CSV | `pd.read_csv()` | `df.to_csv()` |
| Excel | `pd.read_excel()` | `df.to_excel()` |
| JSON | `pd.read_json()` | `df.to_json()` |
| SQL | `pd.read_sql()` | `df.to_sql()` |
| Parquet | `pd.read_parquet()` | `df.to_parquet()` |
| HDF5 | `pd.read_hdf()` | `df.to_hdf()` |
| Pickle | `pd.read_pickle()` | `df.to_pickle()` |

### Next Lecture

In [Lecture 06: Reading JSON Data](./06-reading-json-lecture.md), we will dive deeper into JSON data handling with Pandas.

---

## 📚 Further Reading

- [Pandas IO Documentation](https://pandas.pydata.org/docs/user_guide/io.html)
- [Pandas Read CSV Reference](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [Pandas to_csv Reference](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html)
