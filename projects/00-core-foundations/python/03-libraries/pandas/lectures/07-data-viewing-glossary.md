# Glossary 07: Data Viewing

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| head | First n rows | `df.head(5)` |
| tail | Last n rows | `df.tail(5)` |
| sample | Random n rows | `df.sample(5)` |
| shape | Dimensions (rows, columns) | `df.shape` |
| info | Concise summary | `df.info()` |
| dtypes | Data types per column | `df.dtypes` |
| describe | Statistical summary | `df.describe()` |
| unique | Distinct values | `df["col"].unique()` |
| nunique | Count of distinct values | `df["col"].nunique()` |
| value_counts | Frequency count | `df["col"].value_counts()` |
| memory_usage | Memory per column | `df.memory_usage()` |
| T | Transpose (swap rows/cols) | `df.T` |
| columns | Column labels | `df.columns` |
| index | Row labels | `df.index` |
| ndim | Number of dimensions | `df.ndim` |
| size | Total elements | `df.size` |

---

## Alphabetical Definitions

### C

**Columns**
The vertical labels of a DataFrame.

```python
print(df.columns.tolist())
# ['Name', 'Age', 'City']
```

### D

**Describe**
Returns summary statistics (count, mean, std, min, max, quartiles) for numeric columns.

```python
print(df.describe())
#         Age
# count   5.0
# mean   32.0
# std     6.5
```

**Dtypes**
Data type of each column in a DataFrame.

```python
print(df.dtypes)
# Name    object
# Age      int64
# City    object
```

### H

**Head**
Returns the first n rows. Default is 5.

```python
print(df.head(10))
```

### I

**Index**
Row labels of a DataFrame.

```python
print(df.index)
# RangeIndex(start=0, stop=100, step=1)
```

**Info**
Prints a concise summary: column names, non-null counts, dtypes, memory usage.

```python
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 100 entries, 0 to 99
# Data columns (total 3 columns):
```

### M

**Memory Usage**
The amount of memory consumed by each column.

```python
print(df.memory_usage(deep=True))
# Index     128
# Name      512
# Age        80
# dtype: int64
```

### N

**Ndims**
Number of dimensions. DataFrame is always 2.

```python
print(df.ndim)  # 2
```

**Nunique**
Count of unique values in a column.

```python
print(df["city"].nunique())  # 3
```

### S

**Sample**
Returns random rows from the DataFrame.

```python
print(df.sample(5))    # 5 random rows
print(df.sample(frac=0.1))  # 10% of rows
```

**Shape**
A tuple of (number of rows, number of columns).

```python
print(df.shape)  # (100, 5)
```

**Size**
Total number of elements in the DataFrame (rows × columns).

```python
print(df.size)  # 500
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

**Value Counts**
Counts occurrences of each unique value in a column.

```python
print(df["city"].value_counts())
# New York    40
# London      35
# Paris       25
```

**Values**
Returns the raw data as a NumPy array.

```python
print(df.values)
```

---

## Code Examples

### Example 1: Basic Inspection

```python
import pandas as pd

df = pd.read_csv("data.csv")

print("Shape:", df.shape)
print("First 5 rows:\n", df.head())
print("Data types:\n", df.dtypes)
print("Info:")
df.info()
```

### Example 2: Statistics

```python
import pandas as pd

df = pd.read_csv("data.csv")

print("Numeric stats:\n", df.describe())
print("All columns:\n", df.describe(include="all"))
print("Specific cols:\n", df[["Age", "Salary"]].describe())
```

### Example 3: Unique Values

```python
import pandas as pd

df = pd.read_csv("data.csv")

print("Unique days:", df["day"].unique())
print("Number of days:", df["day"].nunique())
print("Day counts:\n", df["day"].value_counts())
print("Day percentages:\n", df["day"].value_counts(normalize=True))
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| head/tail | DataFrame | Quick row inspection |
| describe | DataFrame | Summary statistics |
| info | DataFrame | Column metadata |
| dtypes | DataFrame | Column data types |
| shape | DataFrame | Dimensions |
| unique | Series | Distinct values |
| value_counts | Series | Frequency distribution |
| memory_usage | DataFrame | Memory consumption |

---

## Display Options Reference

```
pd.set_option("display.max_columns", None)      # Show all columns
pd.set_option("display.max_rows", None)          # Show all rows
pd.set_option("display.max_colwidth", 50)        # Max column width
pd.set_option("display.float_format", "{:.2f}")  # Float format
pd.set_option("display.min_rows", 20)            # Min rows to show
pd.reset_option("display.max_columns")           # Reset to default
```

---

## Self-Test Questions

1. What does `.info()` tell you that `.dtypes` doesn't?
2. How do you check for missing values?
3. What is the difference between `.unique()` and `.nunique()`?
4. How do you display all columns in a wide DataFrame?
5. What does `.describe(include="all")` do differently from `.describe()`?
