# Lecture 02: Getting Started with Pandas

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Create Series and DataFrames from various data sources
- Understand the anatomy of a DataFrame (index, columns, values)
- Explore DataFrame attributes and methods
- Use basic data inspection techniques
- Perform simple operations on Series and DataFrames

---

## 📖 1. Creating a Series

A Series is a one-dimensional array with labels. There are multiple ways to create one.

### From a List

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40, 50])
print(s)
# 0    10
# 1    20
# 2    30
# 3    40
# 4    50
# dtype: int64
```

### From a Dictionary

```python
import pandas as pd

population = pd.Series({
    "Tokyo": 13960000,
    "Delhi": 11030000,
    "Shanghai": 24870000,
    "Sao Paulo": 12330000
})
print(population)
# Tokyo       13960000
# Delhi       11030000
# Shanghai    24870000
# Sao Paulo   12330000
# dtype: int64
```

### From a NumPy Array

```python
import numpy as np
import pandas as pd

arr = np.array([1.5, 2.7, 3.9, 4.1])
s = pd.Series(arr)
print(s)
# 0    1.5
# 1    2.7
# 2    3.9
# 3    4.1
# dtype: float64
```

### With Custom Index

```python
import pandas as pd

temps = pd.Series(
    [72, 68, 75, 80, 65],
    index=["Mon", "Tue", "Wed", "Thu", "Fri"],
    name="Temperature"
)
print(temps)
# Mon    72
# Tue    68
# Wed    75
# Thu    80
# Fri    65
# Name: Temperature, dtype: int64
```

---

## 📖 2. Creating a DataFrame

A DataFrame is a two-dimensional table. You can create one from dictionaries, lists, Series, or other DataFrames.

### From a Dictionary of Lists

```python
import pandas as pd

data = {
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "City": ["New York", "London", "Paris", "Tokyo"],
    "Salary": [75000, 82000, 95000, 68000]
}
df = pd.DataFrame(data)
print(df)
#       Name  Age      City  Salary
# 0    Alice   28  New York   75000
# 1      Bob   35    London   82000
# 2  Charlie   42     Paris   95000
# 3    Diana   31     Tokyo   68000
```

### From a List of Dictionaries

```python
import pandas as pd

records = [
    {"product": "Laptop", "price": 999, "quantity": 5},
    {"product": "Phone", "price": 699, "quantity": 12},
    {"product": "Tablet", "price": 449, "quantity": 8}
]
df = pd.DataFrame(records)
print(df)
#   product  price  quantity
# 0  Laptop    999         5
# 1   Phone    699        12
# 2  Tablet    449         8
```

### From a 2D NumPy Array

```python
import numpy as np
import pandas as pd

arr = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
df = pd.DataFrame(
    arr,
    columns=["A", "B", "C"],
    index=["row1", "row2", "row3"]
)
print(df)
#       A  B  C
# row1  1  2  3
# row2  4  5  6
# row3  7  8  9
```

### From Another DataFrame

```python
import pandas as pd

df_original = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Age": [28, 35]
})

# Create a copy
df_copy = df_original.copy()

# Create a slice
df_slice = df_original[["Name"]]
```

---

## 📖 3. Anatomy of a DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Age": [28, 35]
})
```

### Key Components

| Component | Access | Description |
|---|---|---|
| Index | `df.index` | Row labels |
| Columns | `df.columns` | Column labels |
| Values | `df.values` | Raw NumPy array |
| Shape | `df.shape` | (rows, columns) |
| Dtypes | `df.dtypes` | Data types per column |
| Size | `df.size` | Total number of elements |

### Accessing Components

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42],
    "City": ["New York", "London", "Paris"]
})

# Index
print("Index:", df.index.tolist())
# Index: [0, 1, 2]

# Columns
print("Columns:", df.columns.tolist())
# Columns: ['Name', 'Age', 'City']

# Values (returns NumPy array)
print("Values:\n", df.values)
# [['Alice' 28 'New York']
#  ['Bob' 35 'London']
#  ['Charlie' 42 'Paris']]

# Shape
print("Shape:", df.shape)
# Shape: (3, 3)

# Size
print("Size:", df.size)
# Size: 9
```

---

## 📖 4. Essential DataFrame Attributes

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "Salary": [75000.50, 82000.75, 95000.00, 68000.25]
})
```

### Data Types

```python
print(df.dtypes)
# Name      object
# Age        int64
# Salary   float64
# dtype: object
```

### Memory Usage

```python
print(df.memory_usage(deep=True))
# Index     128
# Name      328
# Age        32
# Salary     32
# dtype: int64
```

### Transpose

```python
print(df.T)
#           0      1        2      3
# Name  Alice    Bob  Charlie  Diana
# Age      28     35       42     31
# Salary 75000  82000    95000  68000
```

---

## 📖 5. Data Inspection Methods

### Quick Overview

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")

# First and last rows
print("Head:\n", df.head())         # First 5 rows
print("Tail:\n", df.tail(3))        # Last 3 rows

# Random sample
print("Sample:\n", df.sample(5))    # 5 random rows

# Dimensions
print("Shape:", df.shape)
print("Size:", df.size)
print("ndim:", df.ndim)

# Info
print(df.info())
```

### Descriptive Statistics

```python
# Summary statistics for numeric columns
print(df.describe())
#        total_bill         tip        size
# count  244.000000  244.000000  244.000000
# mean    19.785943    2.998279    2.569672
# std      8.902412    1.383638    0.951100
# min      3.070000    1.000000    1.000000
# 25%     13.347500    2.000000    2.000000
# 50%     17.795000    2.900000    2.000000
# 75%     24.127500    3.562500    3.000000
# max     50.810000   10.000000    6.000000

# Summary for all columns (including strings)
print(df.describe(include="all"))

# Summary for specific columns
print(df[["total_bill", "tip"]].describe())
```

### Value Counts

```python
# Count unique values in a column
print(df["day"].value_counts())
# Sat     87
# Sun     76
# Thur    62
# Fri     19
```

---

## 📖 6. Basic Operations

### Column Selection

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42],
    "City": ["New York", "London", "Paris"]
})

# Single column (returns Series)
print(df["Name"])

# Multiple columns (returns DataFrame)
print(df[["Name", "Age"]])
```

### Adding a Column

```python
# Add a new column with a scalar value
df["Country"] = "Unknown"

# Add a new column with computed values
df["Age_in_10_years"] = df["Age"] + 10

print(df)
#       Name  Age      City Country  Age_in_10_years
# 0    Alice   28  New York Unknown               38
# 1      Bob   35    London Unknown               45
# 2  Charlie   42     Paris Unknown               52
```

### Removing a Column

```python
df_dropped = df.drop(columns=["Country"])
# or
df_dropped = df.drop("Country", axis=1)
```

### Filtering Rows

```python
# Boolean indexing
adults = df[df["Age"] >= 30]
print(adults)
#       Name  Age    City
# 1      Bob   35  London
# 2  Charlie   42   Paris
```

---

## 📖 7. Setting and Resetting Index

### Setting an Index

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42],
    "SSN": ["123-45-6789", "234-56-7890", "345-67-8901"]
})

# Set SSN as index
df_indexed = df.set_index("SSN")
print(df_indexed)
#              Name  Age
# SSN
# 123-45-6789  Alice   28
# 234-56-7890    Bob   35
# 345-67-8901 Charlie  42
```

### Resetting an Index

```python
df_reset = df_indexed.reset_index()
print(df_reset)
#             SSN     Name  Age
# 0  123-45-6789    Alice   28
# 1  234-56-7890      Bob   35
# 2  345-67-8901  Charlie   42
```

---

## 📖 8. Renaming Columns

```python
import pandas as pd

df = pd.DataFrame({
    "first name": ["Alice", "Bob"],
    "last name": ["Smith", "Jones"],
    "age yrs": [28, 35]
})

# Rename specific columns
df_renamed = df.rename(columns={
    "first name": "first_name",
    "last name": "last_name",
    "age yrs": "age"
})

# Rename all columns at once
df.columns = ["first_name", "last_name", "age"]
```

---

## ❌ 9. Common Mistakes

### Mistake 1: Confusing `loc` and `iloc`

```python
import pandas as pd

df = pd.DataFrame({"A": [10, 20, 30]}, index=["a", "b", "c"])

# loc uses labels
print(df.loc["a"])     # Works

# iloc uses integer positions
print(df.iloc[0])      # Works
print(df.iloc["a"])    # ERROR
```

### Mistake 2: Modifying the Original DataFrame

```python
# This modifies the original
df["new_col"] = 1

# This creates a new DataFrame (safer)
df_new = df.assign(new_col=1)
```

### Mistake 3: Forgetting `inplace` Parameter

```python
# This returns a new DataFrame
df_sorted = df.sort_values("Age")

# This modifies in place
df.sort_values("Age", inplace=True)
```

### Mistake 4: Chaining Indexing

```python
# Bad — may raise SettingWithCopyWarning
# df[df["Age"] > 30]["Name"] = "Unknown"

# Good — use .loc
df.loc[df["Age"] > 30, "Name"] = "Unknown"
```

---

## ✅ 10. Best Practices

1. **Inspect first** — always call `.head()`, `.info()`, `.describe()` before processing
2. **Use meaningful index** — set_index on meaningful identifiers when appropriate
3. **Check dtypes** — ensure columns have expected types
4. **Use `.assign()` for chaining** — keeps transformations readable
5. **Avoid `inplace=True`** — prefer assignment for clarity
6. **Copy when needed** — use `.copy()` to avoid modifying originals
7. **Name your Series** — gives context when printing

---

## 🏋️ 11. Exercises

### Exercise 1: Create and Explore

```python
import pandas as pd

# TODO: Create a DataFrame with employees:
# - name: ["Alice", "Bob", "Charlie", "Diana", "Eve"]
# - department: ["Engineering", "Marketing", "Engineering", "Sales", "Marketing"]
# - salary: [95000, 72000, 88000, 65000, 71000]
# - years经验: [5, 3, 8, 2, 4]

# TODO: Print shape, dtypes, head, describe
```

### Exercise 2: Column Operations

```python
# TODO: Add a column "bonus" that is 10% of salary
# TODO: Add a column "level" that is "Senior" if years >= 5, else "Junior"
# TODO: Remove the "years经验" column
```

### Exercise 3: Index Manipulation

```python
# TODO: Set "name" as the index
# TODO: Print the DataFrame
# TODO: Reset the index back to default
```

---

## 📝 12. Summary

| Concept | What You Learned |
|---|---|
| Creating Series | From lists, dicts, NumPy arrays |
| Creating DataFrames | From dicts, lists of dicts, 2D arrays |
| DataFrame Anatomy | Index, columns, values, shape, dtypes |
| Inspection | `.head()`, `.info()`, `.describe()`, `.shape` |
| Column Operations | Select, add, remove, rename |
| Index Operations | `set_index()`, `reset_index()` |
| Basic Filtering | Boolean indexing with conditions |

### Next Lecture

In [Lecture 03: Series Deep Dive](./03-series-lecture.md), we will explore Series in depth — indexing, slicing, operations, and methods.

---

## 📚 Further Reading

- [Pandas User Guide: 10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Pandas DataFrame Documentation](https://pandas.pydata.org/docs/reference/frame.html)
- [Pandas Series Documentation](https://pandas.pydata.org/docs/reference/series.html)
