# Glossary 02: Getting Started with Pandas

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| Series | 1D labeled array | `pd.Series([1, 2, 3])` |
| DataFrame | 2D labeled data structure | `pd.DataFrame(data)` |
| Index | Labels for each row | `df.index` |
| Columns | Labels for each column | `df.columns` |
| Shape | Tuple of (rows, columns) | `df.shape` |
| Dtypes | Data type of each column | `df.dtypes` |
| Head | First n rows of DataFrame | `df.head(5)` |
| Tail | Last n rows of DataFrame | `df.tail(5)` |
| Describe | Summary statistics | `df.describe()` |
| Info | DataFrame summary | `df.info()` |
| Transpose | Swap rows and columns | `df.T` |
| Value Counts | Count unique values | `df["col"].value_counts()` |

---

## Alphabetical Definitions

### C

**Columns**
The vertical labels of a DataFrame. Each column is a Series.

```python
print(df.columns)
# Index(['Name', 'Age', 'City'], dtype='object')
```

**Copy**
A duplicate of a DataFrame. Use `.copy()` to avoid modifying the original.

```python
df_new = df.copy()
```

### D

**DataFrame**
The primary 2D data structure — a table with labeled rows and columns.

```python
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
```

**Describe**
Returns summary statistics (count, mean, std, min, max, quartiles) for numeric columns.

```python
print(df.describe())
```

**Dtypes**
The data type of each column in a DataFrame.

```python
print(df.dtypes)
# Name    object
# Age      int64
```

### H

**Head**
Returns the first n rows. Default is 5.

```python
print(df.head(10))
```

### I

**Index**
Row labels. Can be integers, strings, or dates.

```python
print(df.index)
# RangeIndex(start=0, stop=3, step=1)
```

**Info**
Prints a concise summary: column names, non-null counts, dtypes, memory usage.

```python
df.info()
```

### M

**Memory Usage**
The amount of memory consumed by each column.

```python
print(df.memory_usage(deep=True))
```

### N

**Ndims**
Number of dimensions. DataFrame is always 2.

```python
print(df.ndim)  # 2
```

### R

**Records**
A list of dictionaries, where each dictionary represents a row.

```python
records = [{"name": "Alice", "age": 28}, {"name": "Bob", "age": 35}]
df = pd.DataFrame(records)
```

### S

**Sample**
Returns random rows from the DataFrame.

```python
print(df.sample(3))  # 3 random rows
```

**Shape**
A tuple of (number of rows, number of columns).

```python
print(df.shape)  # (3, 4)
```

**Size**
Total number of elements in the DataFrame (rows × columns).

```python
print(df.size)  # 12
```

### T

**Tail**
Returns the last n rows. Default is 5.

```python
print(df.tail(3))
```

**Transpose**
Swaps rows and columns.

```python
print(df.T)
```

### V

**Values**
Returns the raw data as a NumPy array.

```python
print(df.values)
```

**Value Counts**
Counts occurrences of each unique value in a column.

```python
print(df["city"].value_counts())
# New York    2
# London      1
```

---

## Code Examples

### Example 1: Creating a Series

```python
import pandas as pd

# From list
s = pd.Series([10, 20, 30])

# From dictionary
s = pd.Series({"a": 1, "b": 2, "c": 3})

# With custom index
s = pd.Series([72, 68, 75], index=["Mon", "Tue", "Wed"])
```

### Example 2: Creating a DataFrame

```python
import pandas as pd

# From dictionary of lists
df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Age": [28, 35]
})

# From list of dictionaries
df = pd.DataFrame([
    {"Name": "Alice", "Age": 28},
    {"Name": "Bob", "Age": 35}
])

# From NumPy array
import numpy as np
df = pd.DataFrame(np.array([[1, 2], [3, 4]]), columns=["A", "B"])
```

### Example 3: Inspecting a DataFrame

```python
import pandas as pd

df = pd.read_csv("data.csv")

print(df.head())        # First 5 rows
print(df.info())        # Column info
print(df.describe())    # Statistics
print(df.shape)         # Dimensions
print(df.dtypes)        # Data types
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| Series | DataFrame | Column of a DataFrame |
| Index | DataFrame | Row labels |
| Columns | DataFrame | Column labels |
| Head/Tail | DataFrame | Quick row inspection |
| Describe | DataFrame | Summary statistics |
| Info | DataFrame | Column metadata |
| Dtypes | DataFrame | Column data types |
| Shape | DataFrame | Dimensions (rows, columns) |

---

## DataFrame Creation Methods

```
pd.DataFrame(dict_of_lists)    -> DataFrame from dict of lists
pd.DataFrame(list_of_dicts)    -> DataFrame from list of dicts
pd.DataFrame(np_array)         -> DataFrame from 2D NumPy array
pd.DataFrame(series)           -> DataFrame from Series
pd.read_csv(file)              -> DataFrame from CSV file
pd.read_excel(file)            -> DataFrame from Excel file
pd.read_json(file)             -> DataFrame from JSON file
```

---

## Self-Test Questions

1. What is the difference between `.head()` and `.tail()`?
2. How do you check the data types of all columns?
3. What does `.describe()` return?
4. How do you create a DataFrame from a list of dictionaries?
5. What is the purpose of `.copy()`?
