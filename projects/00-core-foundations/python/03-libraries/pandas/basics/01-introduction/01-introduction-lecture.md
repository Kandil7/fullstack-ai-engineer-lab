# Lecture 01: Introduction to Pandas

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Understand what Pandas is and why it matters for data science
- Install and verify Pandas in your environment
- Import Pandas and explore its core components
- Understand the relationship between Pandas and NumPy
- Recognize when to use Pandas over plain Python

---

## 📖 1. What is Pandas?

Pandas is an open-source Python library built on top of NumPy. It provides high-performance, easy-to-use data structures and data analysis tools. The name "Pandas" is derived from "panel data," an econometrics term for multidimensional structured datasets.

### Key Features

| Feature | Description |
|---|---|
| DataFrame | 2D labeled data structure (like a spreadsheet) |
| Series | 1D labeled array (like a column) |
| Data I/O | Read/write CSV, Excel, SQL, JSON, Parquet, and more |
| Data Cleaning | Handle missing data, duplicates, type conversion |
| Data Transformation | Filter, group, aggregate, merge, reshape |
| Time Series | Built-in support for dates, ranges, and frequencies |
| Visualization | Integration with Matplotlib for quick plots |

### Why Pandas?

```python
# Without Pandas — manual CSV parsing
import csv

with open("data.csv") as f:
    reader = csv.DictReader(f)
    sales = []
    for row in reader:
        if row["region"] == "East":
            sales.append(float(row["amount"]))

total = sum(sales)
print(f"East region total: {total}")
```

```python
# With Pandas — concise and fast
import pandas as pd

df = pd.read_csv("data.csv")
total = df[df["region"] == "East"]["amount"].sum()
print(f"East region total: {total}")
```

The Pandas version is shorter, faster, and more readable.

---

## 📦 2. Installing Pandas

### Using pip

```bash
pip install pandas
```

### Using conda

```bash
conda install pandas
```

### Verify Installation

```python
import pandas as pd
print(pd.__version__)
# Output: 2.2.2 (or similar)
```

### Common Extras

```bash
pip install pandas[excel]    # For Excel support (openpyxl)
pip install pandas[sql]      # For SQL support (sqlalchemy)
pip install pandas[parquet]  # For Parquet support (pyarrow)
```

---

## 🔧 3. Importing Pandas

The universal convention is to import Pandas with the alias `pd`:

```python
import pandas as pd
```

This alias is recognized by virtually every data science tutorial, textbook, and codebase. Breaking this convention creates confusion.

### Also Useful: NumPy

```python
import numpy as np
import pandas as pd

# Pandas builds on NumPy — they work together seamlessly
arr = np.array([1, 2, 3, 4, 5])
series = pd.Series(arr)
print(series)
# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: int64
```

---

## 🧱 4. Core Data Structures

Pandas provides two primary data structures:

### Series

A one-dimensional labeled array. Think of it as a single column from a spreadsheet.

```python
import pandas as pd

# Creating a Series
temperatures = pd.Series([72, 68, 75, 80, 65], index=["Mon", "Tue", "Wed", "Thu", "Fri"])
print(temperatures)

# Mon    72
# Tue    68
# Wed    75
# Thu    80
# Fri    65
# dtype: int64
```

### DataFrame

A two-dimensional labeled data structure with columns of potentially different types. Think of it as an entire spreadsheet or SQL table.

```python
import pandas as pd

# Creating a DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "City": ["New York", "London", "Paris", "Tokyo"]
}
df = pd.DataFrame(data)
print(df)

#       Name  Age      City
# 0    Alice   28  New York
# 1      Bob   35    London
# 2  Charlie   42     Paris
# 3    Diana   31     Tokyo
```

### Relationship Between Series and DataFrame

```python
# A DataFrame is a collection of Series
print(type(df["Name"]))
# <class 'pandas.core.series.Series'>

# Each column is a Series
print(df["Age"])
# 0    28
# 1    35
# 2    42
# 3    31
# Name: Age, dtype: int64
```

---

## 📊 5. Pandas vs NumPy

| Aspect | NumPy | Pandas |
|---|---|---|
| Primary Structure | ndarray | DataFrame / Series |
| Data Types | Homogeneous | Heterogeneous |
| Labels | Positional (integer) | Labeled (index + columns) |
| Missing Data | Limited support | First-class support |
| Use Case | Numerical computing | Data analysis & manipulation |

```python
import numpy as np
import pandas as pd

# NumPy — homogeneous
arr = np.array([1, 2, 3])
print(type(arr[0]))  # <class 'numpy.int64'>

# Pandas — heterogeneous via DataFrame
df = pd.DataFrame({
    "name": ["Alice"],
    "age": [28],
    "active": [True]
})
print(df.dtypes)
# name      object
# age        int64
# active      bool
# dtype: object
```

---

## 🧹 6. Real-World Example: Quick Data Exploration

```python
import pandas as pd

# Load a dataset
df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")

# First look at the data
print("Shape:", df.shape)          # (244, 7)
print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nBasic statistics:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())
```

This five-line exploration tells you the size, structure, statistics, and data quality of any dataset.

---

## ❌ 7. Common Mistakes

### Mistake 1: Not Importing with Standard Alias

```python
# Bad — breaks convention
import pandas as pnd

# Good — standard alias
import pandas as pd
```

### Mistake 2: Confusing Index with Position

```python
import pandas as pd

s = pd.Series([10, 20, 30], index=["a", "b", "c"])

# This uses label-based indexing
print(s["a"])  # 10

# This uses positional indexing
print(s.iloc[0])  # 10
```

### Mistake 3: Modifying a View Instead of a Copy

```python
import pandas as pd

df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

# This may trigger a SettingWithCopyWarning
# df[df["A"] > 1]["B"] = 99

# Use .loc instead
df.loc[df["A"] > 1, "B"] = 99
```

---

## ✅ 8. Best Practices

1. **Always import as `pd`** — the convention is universal
2. **Start with `.head()`** — always inspect data before processing
3. **Check dtypes** — ensure columns have expected types
4. **Check for nulls** — use `.isnull().sum()` early
5. **Use vectorized operations** — avoid Python loops over rows
6. **Chain operations carefully** — use method chaining for readability
7. **Set meaningful indexes** — use `.set_index()` when appropriate

---

## 🏋️ 9. Exercises

### Exercise 1: Install and Verify

```python
# TODO: Install pandas, then run:
import pandas as pd
print("Pandas version:", pd.__version__)
```

### Exercise 2: Create Your First DataFrame

```python
import pandas as pd

# TODO: Create a DataFrame with these columns:
# - product: ["Laptop", "Phone", "Tablet"]
# - price: [999, 699, 449]
# - in_stock: [True, False, True]

# TODO: Print the DataFrame
# TODO: Print the shape
# TODO: Print the data types
```

### Exercise 3: Quick Exploration

```python
import pandas as pd

# TODO: Load the Iris dataset
# URL: "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

# TODO: Print shape, head, dtypes, and describe()
```

---

## 📝 10. Summary

| Concept | What You Learned |
|---|---|
| What is Pandas | Open-source data analysis library built on NumPy |
| Core structures | Series (1D) and DataFrame (2D) |
| Installation | `pip install pandas` or `conda install pandas` |
| Import convention | `import pandas as pd` |
| Pandas vs NumPy | Pandas handles heterogeneous, labeled data |
| First steps | `.head()`, `.dtypes`, `.describe()`, `.shape` |

### Next Lecture

In [Lecture 02: Getting Started with Pandas](./02-getting-started-lecture.md), we will dive deeper into creating Series and DataFrames, exploring their attributes, and performing basic operations.

---

## 📚 Further Reading

- [Pandas Official Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Pandas Cookbook](https://pandas.pydata.org/docs/user_guide/cookbook.html)
- [Python for Data Analysis (Wes McKinney)](https://wesmckinney.com/book/)
