# Glossary 01: Introduction to Pandas

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| Pandas | Python library for data analysis built on NumPy | `import pandas as pd` |
| Series | 1D labeled array | `pd.Series([1, 2, 3])` |
| DataFrame | 2D labeled data structure | `pd.DataFrame(data)` |
| Panel Data | Econometrics term — multidimensional structured datasets | Origin of "Pandas" name |
| Vectorized Operation | Operation applied to entire array without explicit loops | `df["a"] + df["b"]` |
| Index | Label for each row in a Series or DataFrame | `index=["a", "b", "c"]` |
| Alias | Short name used for imports | `pd` is the alias for pandas |
| Dtypes | Data types of each column | `df.dtypes` |
| NumPy | Fundamental package for numerical computing in Python | Foundation of Pandas |
| Open Source | Software with publicly available source code | Pandas is BSD-licensed |

---

## Alphabetical Definitions

### A

**Alias**
A shorthand name assigned to a module during import. The universal convention for Pandas is `pd`.

```python
import pandas as pd  # pd is the alias
```

**Array**
A collection of elements stored in contiguous memory. NumPy arrays are the foundation of Pandas.

```python
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
```

### B

**Broadcasting**
NumPy's ability to perform operations on arrays of different shapes automatically. Pandas inherits this behavior.

```python
import pandas as pd
s = pd.Series([1, 2, 3])
print(s * 2)  # Broadcasting: each element multiplied by 2
# 0    2
# 1    4
# 2    6
```

### C

**CSV (Comma-Separated Values)**
A plain-text file format for tabular data. Pandas can read and write CSV files natively.

```python
df = pd.read_csv("data.csv")
df.to_csv("output.csv", index=False)
```

**Column**
A vertical array of data in a DataFrame. Each column is a Series.

```python
print(df["Name"])  # Accesses the "Name" column
```

### D

**DataFrame**
The primary 2D data structure in Pandas — a table with labeled rows and columns.

```python
import pandas as pd
df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Age": [28, 35]
})
```

**Data Types (dtypes)**
The type of data stored in each column (e.g., int64, float64, object, bool).

```python
print(df.dtypes)
# Name    object
# Age      int64
```

### H

**Head**
The first n rows of a DataFrame. Default is 5.

```python
print(df.head(10))  # First 10 rows
```

### I

**Index**
A labeled axis for rows in a Series or DataFrame. Labels can be strings, integers, or dates.

```python
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s["b"])  # 20
```

### M

**Missing Data**
Data that is absent or not recorded. Pandas represents missing values as `NaN` (Not a Number).

```python
import numpy as np
s = pd.Series([1, np.nan, 3])
print(s.isnull())  # Detects missing values
```

### N

**NumPy**
Numerical Python — a library for efficient array operations. Pandas is built on top of NumPy.

```python
import numpy as np
arr = np.array([1, 2, 3])
```

### O

**Object**
The Pandas dtype used for string/text columns and mixed-type columns.

```python
print(df.dtypes)
# Name    object  # String column
```

### P

**Panel Data**
An econometrics term for multidimensional structured datasets. The name "Pandas" is derived from this term.

**Pip**
Python's package installer. Used to install Pandas and other libraries.

```bash
pip install pandas
```

### S

**Series**
A one-dimensional labeled array. The building block of DataFrames.

```python
s = pd.Series([1, 2, 3], index=["x", "y", "z"])
```

**Shape**
A tuple representing the dimensions of a DataFrame (rows, columns).

```python
print(df.shape)  # (4, 3) — 4 rows, 3 columns
```

### V

**Vectorized Operation**
An operation that applies to an entire array at once, without explicit Python loops. Much faster than looping.

```python
# Slow — Python loop
for i in range(len(df)):
    df.loc[i, "total"] = df.loc[i, "price"] * df.loc[i, "quantity"]

# Fast — vectorized
df["total"] = df["price"] * df["quantity"]
```

---

## Code Examples

### Example 1: Creating a Series

```python
import pandas as pd

# From a list
s1 = pd.Series([10, 20, 30, 40])
print(s1)

# With custom index
s2 = pd.Series([72, 68, 75], index=["Mon", "Tue", "Wed"])
print(s2["Tue"])  # 68
```

### Example 2: Creating a DataFrame

```python
import pandas as pd

data = {
    "Product": ["Laptop", "Phone", "Tablet"],
    "Price": [999, 699, 449],
    "In Stock": [True, False, True]
}
df = pd.DataFrame(data)
print(df)
```

### Example 3: Basic Exploration

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Head:\n", df.head())
print("Describe:\n", df.describe())
print("Null counts:\n", df.isnull().sum())
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| DataFrame | Series | DataFrame is a collection of Series |
| NumPy | Pandas | Pandas is built on NumPy |
| CSV | read_csv | File format Pandas reads natively |
| Index | DataFrame | Labels for each row |
| Dtypes | DataFrame | Data type of each column |
| Vectorized | Operations | Fast element-wise operations |
| Missing Data | NaN | How Pandas represents absent values |
| Conda | Pip | Alternative package manager |

---

## Key Formulas and Patterns

```
DataFrame Shape:    df.shape          -> (rows, columns)
Column Access:      df["column_name"] -> Series
Row Count:          len(df)           -> int
Null Count:         df.isnull().sum() -> Series
Data Types:         df.dtypes         -> Series
Statistics:         df.describe()     -> DataFrame
```

---

## Self-Test Questions

1. What is the standard alias for importing Pandas?
2. What is the difference between a Series and a DataFrame?
3. How do you check the shape of a DataFrame?
4. What dtype does Pandas use for string columns?
5. Why is vectorized operation preferred over Python loops?
