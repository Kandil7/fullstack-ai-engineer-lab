# Lecture 07: Data Viewing

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- View and inspect DataFrames using various methods
- Use head(), tail(), and sample() effectively
- Display detailed information with info() and describe()
- Control display options for better readability
- Handle large DataFrames without overwhelming output

---

## 📖 1. Basic Viewing Methods

### head() — First Rows

```python
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")

# First 5 rows (default)
print(df.head())

# First 10 rows
print(df.head(10))
```

### tail() — Last Rows

```python
# Last 5 rows (default)
print(df.tail())

# Last 10 rows
print(df.tail(10))
```

### sample() — Random Rows

```python
# 5 random rows
print(df.sample(5))

# 10% of rows (random)
print(df.sample(frac=0.1))

# Sample without replacement
print(df.sample(5, replace=False))
```

---

## 📖 2. Shape and Dimensions

### Shape

```python
# Tuple of (rows, columns)
print(df.shape)
# (244, 7)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
```

### Size

```python
# Total number of elements
print(df.size)
# 1708 (244 * 7)
```

### Number of Dimensions

```python
# Always 2 for DataFrame
print(df.ndim)
# 2
```

---

## 📖 3. Column and Index Info

### Columns

```python
# List of column names
print(df.columns.tolist())
# ['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size']

# Number of columns
print(len(df.columns))
# 7

# Column data types
print(df.dtypes)
# total_bill    float64
# tip           float64
# sex            object
# smoker         object
# day            object
# time           object
# size            int64
```

### Index

```python
# Index info
print(df.index)
# RangeIndex(start=0, stop=244, step=1)

# Index values
print(df.index.tolist())
# [0, 1, 2, ..., 243]
```

---

## 📖 4. Detailed Information

### info() — Concise Summary

```python
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 244 entries, 0 to 243
# Data columns (total 7 columns):
#  #   Column      Non-Null Count  Dtype  
# ---  ------      --------------  -----  
#  0   total_bill  244 non-null    float64
#  1   tip         244 non-null    float64
#  2   sex         244 non-null    object 
#  3   smoker      244 non-null    object 
#  4   day         244 non-null    object 
#  5   time        244 non-null    object 
#  6   size        244 non-null    int64  
# dtypes: float64(2), int64(1), object(4)
# memory usage: 13.5+ KB
```

### info() with Memory Usage

```python
# Detailed memory usage
df.info(memory_usage="deep")
```

---

## 📖 5. Descriptive Statistics

### describe() — Numeric Columns

```python
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
```

### describe() — All Columns

```python
print(df.describe(include="all"))
```

### describe() — Specific Percentiles

```python
print(df.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]))
```

### describe() — Specific Columns

```python
print(df[["total_bill", "tip"]].describe())
```

---

## 📖 6. Unique Values and Counts

### unique() — Distinct Values

```python
print(df["day"].unique())
# ['Sun' 'Sat' 'Thur' 'Fri']

print(df["time"].unique())
# ['Dinner' 'Lunch']
```

### nunique() — Count of Distinct Values

```python
print(df["day"].nunique())
# 4

print(df.nunique())
# total_bill    224
# tip           123
# sex             2
# smoker          2
# day             4
# time            2
# size            6
```

### value_counts() — Frequency Count

```python
print(df["day"].value_counts())
# Sat     87
# Sun     76
# Thur    62
# Fri     19

# With percentages
print(df["day"].value_counts(normalize=True))
# Sat     0.356557
# Sun     0.311475
# Thur    0.254098
# Fri     0.077869

# Top 2 most frequent
print(df["day"].value_counts().head(2))
```

---

## 📖 7. Display Options

### Setting Display Options

```python
import pandas as pd

# Show all columns
pd.set_option("display.max_columns", None)

# Show all rows
pd.set_option("display.max_rows", None)

# Set column width
pd.set_option("display.max_colwidth", 50)

# Set float format
pd.set_option("display.float_format", "{:.2f}".format)

# Show more rows
pd.set_option("display.min_rows", 20)

# Reset options
pd.reset_option("display.max_columns")
pd.reset_option("display.max_rows")
pd.reset_option("display.max_colwidth")
pd.reset_option("display.float_format")
```

### Context Manager

```python
# Temporary display settings
with pd.option_context("display.max_rows", 100, "display.float_format", "{:.4f}".format):
    print(df.head(50))
```

---

## 📖 8. Transpose and Rotation

### Transpose

```python
# Swap rows and columns
print(df.head().T)
```

### Rotated View

```python
# For small DataFrames
print(df.head().transpose())
```

---

## 📖 9. Memory Usage

### Check Memory

```python
# Memory usage per column
print(df.memory_usage())
# Index          128
# total_bill    1952
# tip           1952
# sex           1952
# smoker        1952
# day           1952
# time          1952
# size          1952
# dtype: int64

# Total memory
print(df.memory_usage(deep=True).sum())
# 16232 (approximate)

# With percentages
print(df.memory_usage(deep=True, index=False) / df.memory_usage(deep=True).sum() * 100)
```

---

## 📖 10. Real-World Example

```python
import pandas as pd

# Load dataset
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
df = pd.read_csv(url)

# Comprehensive inspection
print("=" * 60)
print("SHAPE")
print("=" * 60)
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)
print(df.head())

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)
print(df.dtypes)

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
print(pd.DataFrame({"Count": missing, "Percentage": missing_pct}))

print("\n" + "=" * 60)
print("UNIQUE VALUES")
print("=" * 60)
for col in df.select_dtypes(include=["object"]).columns:
    print(f"{col}: {df[col].nunique()} unique - {df[col].unique()[:5]}...")

print("\n" + "=" * 60)
print("STATISTICS")
print("=" * 60)
print(df.describe())
```

---

## ❌ 11. Common Mistakes

### Mistake 1: Overwhelming Output

```python
# Bad — prints everything
# print(df)

# Good — use head
print(df.head())
```

### Mistake 2: Not Checking dtypes

```python
# Bad — may have wrong types
df = pd.read_csv("data.csv")
# Process without checking types

# Good — check first
print(df.dtypes)
```

### Mistake 3: Ignoring Missing Data

```python
# Bad — may have hidden nulls
df.describe()

# Good — check nulls first
print(df.isnull().sum())
print(df.describe())
```

---

## ✅ 12. Best Practices

1. **Start with `.head()`** — always inspect first 5 rows
2. **Check `.info()`** — understand structure and missing data
3. **Check `.dtypes`** — ensure correct types
4. **Check `.isnull().sum()`** — identify missing data
5. **Use `.describe()`** — get statistical summary
6. **Set display options** — for better readability
7. **Check `.shape`** — understand dataset size
8. **Use `.sample()`** — for random inspection

---

## 🏋️ 13. Exercises

### Exercise 1: Basic Inspection

```python
import pandas as pd

# TODO: Load the Titanic dataset
# URL: "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"

# TODO: Print shape, head, dtypes, info
# TODO: Count missing values per column
# TODO: Print unique values for categorical columns
```

### Exercise 2: Display Options

```python
import pandas as pd

# TODO: Load a dataset with many columns
# TODO: Set display options to show all columns
# TODO: Print the DataFrame with formatted floats
# TODO: Reset display options
```

### Exercise 3: Statistical Summary

```python
import pandas as pd

# TODO: Load the tips dataset
# TODO: Print describe() for all columns
# TODO: Print describe() for specific columns only
# TODO: Calculate custom percentiles (10th, 90th)
```

---

## 📝 14. Summary

| Method | Purpose |
|---|---|
| `df.head(n)` | First n rows |
| `df.tail(n)` | Last n rows |
| `df.sample(n)` | Random n rows |
| `df.shape` | (rows, columns) |
| `df.info()` | Column info, types, nulls |
| `df.dtypes` | Data types per column |
| `df.describe()` | Statistical summary |
| `df.unique()` | Distinct values |
| `df.nunique()` | Count of distinct values |
| `df.value_counts()` | Frequency count |
| `df.memory_usage()` | Memory per column |
| `df.T` | Transpose |

### Next Lecture

In [Lecture 08: Data Selecting](./08-data-selecting-lecture.md), we will dive deep into techniques for selecting specific rows and columns from DataFrames.

---

## 📚 Further Reading

- [Pandas DataFrame Visualization](https://pandas.pydata.org/docs/user_guide/style.html)
- [Pandas Options and Settings](https://pandas.pydata.org/docs/user_guide/options.html)
- [Pandas DataFrame Attributes](https://pandas.pydata.org/docs/reference/frame.html)
