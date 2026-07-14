# Lecture 11: Rename Columns

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Rename columns using various methods
- Rename index labels
- Clean column names (lowercase, remove spaces, etc.)
- Handle multi-level column indices
- Use rename with functions for bulk renaming

---

## 📖 1. Basic Renaming

### Rename Specific Columns

```python
import pandas as pd

df = pd.DataFrame({
    "first name": ["Alice", "Bob"],
    "last name": ["Smith", "Jones"],
    "age yrs": [28, 35]
})

# Rename using rename()
df_renamed = df.rename(columns={
    "first name": "first_name",
    "last name": "last_name",
    "age yrs": "age"
})
print(df_renamed)
#   first_name last_name  age
# 0      Alice     Smith   28
# 1        Bob     Jones   35
```

### Rename with inplace

```python
# Modifies original DataFrame
df.rename(columns={
    "first name": "first_name",
    "last name": "last_name"
}, inplace=True)
```

---

## 📖 2. Rename All Columns

### Direct Assignment

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Age": [28, 35],
    "City": ["New York", "London"]
})

# Rename all columns at once
df.columns = ["name", "age", "city"]
print(df)
#      name  age      city
# 0   Alice   28  New York
# 1     Bob   35    London
```

### Using a List

```python
# Must match the number of columns
df.columns = ["employee_name", "employee_age", "employee_city"]
```

---

## 📖 3. Bulk Renaming with Functions

### Lowercase All Columns

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Age": [28, 35],
    "City": ["New York", "London"]
})

# Using str methods
df.columns = df.columns.str.lower()
print(df)
#    name  age      city
# 0  Alice   28  New York
# 1    Bob   35    London
```

### Replace Spaces with Underscores

```python
df = pd.DataFrame({
    "First Name": ["Alice", "Bob"],
    "Last Name": ["Smith", "Jones"],
    "Age Yrs": [28, 35]
})

df.columns = df.columns.str.replace(" ", "_").str.lower()
print(df)
#   first_name last_name  age_yrs
# 0      Alice     Smith       28
# 1        Bob     Jones       35
```

### Using apply()

```python
df.columns = df.columns.apply(lambda x: x.lower().replace(" ", "_"))
```

### Using map()

```python
df.columns = df.columns.map(lambda x: x.strip().lower())
```

---

## 📖 4. Rename with rename() Method

### Using a Dictionary

```python
import pandas as pd

df = pd.DataFrame({
    "A": [1, 2],
    "B": [3, 4],
    "C": [5, 6]
})

df_renamed = df.rename(columns={"A": "Alpha", "B": "Beta", "C": "Gamma"})
print(df_renamed)
#    Alpha  Beta  Gamma
# 0      1     3      5
# 1      2     4      6
```

### Using a Function

```python
# Rename all columns with a function
df_renamed = df.rename(columns=lambda x: f"col_{x}")
print(df_renamed)
#    col_A  col_B  col_C
# 0      1      3      5
# 1      2      4      6
```

### Rename Both Columns and Index

```python
df_renamed = df.rename(
    columns={"A": "Alpha"},
    index={0: "row_0", 1: "row_1"}
)
```

---

## 📖 5. Rename Index Labels

### Rename Index

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42]
}, index=["emp_1", "emp_2", "emp_3"])

# Rename specific index labels
df_renamed = df.rename(index={
    "emp_1": "employee_1",
    "emp_2": "employee_2"
})
print(df_renamed)
#              Name  Age
# employee_1  Alice   28
# employee_2    Bob   35
# emp_3    Charlie   42
```

### Rename Index with Function

```python
df_renamed = df.rename(index=lambda x: x.upper())
print(df_renamed)
#       Name  Age
# EMP_1  Alice   28
# EMP_2    Bob   35
# EMP_3  Charlie  42
```

---

## 📖 6. Cleaning Column Names

### Common Cleaning Operations

```python
import pandas as pd

df = pd.DataFrame({
    " First Name ": ["Alice", "Bob"],
    "Last Name": ["Smith", "Jones"],
    "AGE (years)": [28, 35],
    "  City  ": ["New York", "London"]
})

# Strip whitespace
df.columns = df.columns.str.strip()

# Lowercase
df.columns = df.columns.str.lower()

# Replace spaces with underscores
df.columns = df.columns.str.replace(" ", "_")

# Remove special characters
df.columns = df.columns.str.replace(r"[^a-z0-9_]", "", regex=True)

print(df)
#   first_name last_name  ageyears     city
# 0      Alice     Smith        28  New York
# 1        Bob     Jones        35   London
```

### Complete Cleaning Pipeline

```python
def clean_column_names(df):
    """Clean all column names in a DataFrame."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df

df_clean = clean_column_names(df)
```

---

## 📖 7. Multi-Level Columns

### Rename Multi-Level Columns

```python
import pandas as pd

# Create multi-level columns
arrays = [
    ["A", "A", "B", "B"],
    ["one", "two", "one", "two"]
]
columns = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])

df = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8]], columns=columns)
print(df)
# first   A       B      
# second one two one two
# 0      1   2   3   4
# 1      5   6   7   8

# Rename level
df.columns = df.columns.rename("level_0", level=0)
```

---

## 📖 8. Real-World Example

```python
import pandas as pd

# Messy column names from real data
df = pd.DataFrame({
    " Customer ID ": [1001, 1002, 1003],
    "Customer Name": ["Alice Smith", "Bob Jones", "Charlie Brown"],
    " Order Date": ["2024-01-15", "2024-02-20", "2024-03-10"],
    "Total Amount ($)": [250.50, 180.75, 320.00],
    "  Status  ": ["Shipped", "Pending", "Delivered"]
})

print("Original columns:")
print(df.columns.tolist())
# [' Customer ID ', 'Customer Name', ' Order Date', 'Total Amount ($)', '  Status  ']

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)

print("\nCleaned columns:")
print(df.columns.tolist())
# ['customer_id', 'customer_name', 'order_date', 'total_amount', 'status']
```

---

## ❌ 9. Common Mistakes

### Mistake 1: Wrong Number of Columns

```python
import pandas as pd

df = pd.DataFrame({"A": [1], "B": [2], "C": [3]})

# Bad — wrong number of columns
# df.columns = ["X", "Y"]

# Good — match the number
df.columns = ["X", "Y", "Z"]
```

### Mistake 2: Not Preserving Data

```python
# Bad — loses the data connection
df.columns = ["new_a", "new_b"]

# Good — use rename for safety
df = df.rename(columns={"A": "new_a", "B": "new_b"})
```

### Mistake 3: Forgetting inplace

```python
# Bad — doesn't modify df
df.rename(columns={"A": "Alpha"})

# Good — assign or use inplace
df = df.rename(columns={"A": "Alpha"})
```

---

## ✅ 10. Best Practices

1. **Use `rename()` for safety** — preserves data connection
2. **Clean column names early** — normalize before processing
3. **Use `.str` methods** — for bulk renaming
4. **Document renames** — keep a mapping dictionary
5. **Check dtypes after rename** — ensure no data loss
6. **Use descriptive names** — avoid abbreviations
7. **Follow naming conventions** — lowercase_underscore
8. **Use `inplace=False`** — default and safer

---

## 🏋️ 11. Exercises

### Exercise 1: Basic Renaming

```python
import pandas as pd

# TODO: Create a DataFrame with messy column names
# TODO: Rename specific columns
# TODO: Rename all columns to lowercase
# TODO: Replace spaces with underscores
```

### Exercise 2: Bulk Renaming

```python
import pandas as pd

# TODO: Create a DataFrame with 5 columns
# TODO: Rename all columns using a function
# TODO: Add prefix to all columns
# TODO: Add suffix to all columns
```

### Exercise 3: Cleaning Pipeline

```python
import pandas as pd

# TODO: Create a DataFrame with messy names
# TODO: Write a function to clean all column names
# TODO: Apply the function
# TODO: Verify the result
```

---

## 📝 12. Summary

| Method | Purpose |
|---|---|
| `df.rename(columns={...})` | Rename specific columns |
| `df.columns = [...]` | Rename all columns |
| `df.columns.str.lower()` | Bulk lowercase |
| `df.columns.str.replace(...)` | Bulk replace |
| `df.rename(index={...})` | Rename index labels |
| `df.rename(columns=func)` | Rename with function |

### Next Lecture

In [Lecture 12: Iterating](./12-iterating-lecture.md), we will explore techniques for iterating over DataFrames and Series.

---

## 📚 Further Reading

- [Pandas rename Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html)
- [Pandas DataFrame.columns Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.columns.html)
- [Pandas String Methods](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html)
