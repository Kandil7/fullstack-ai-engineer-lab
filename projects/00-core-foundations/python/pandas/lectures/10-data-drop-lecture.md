# Lecture 10: Data Drop

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Drop rows and columns from DataFrames
- Drop based on labels, positions, and conditions
- Handle missing data with dropna()
- Drop duplicate rows
- Use the inplace parameter correctly
- Combine drop operations with other transformations

---

## 📖 1. Dropping Columns

### Drop Single Column

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42],
    "City": ["New York", "London", "Paris"],
    "Salary": [75000, 82000, 95000]
})

# Drop single column
df_dropped = df.drop(columns=["City"])
print(df_dropped)
#       Name  Age  Salary
# 0    Alice   28   75000
# 1      Bob   35   82000
# 2  Charlie   42   95000
```

### Drop Multiple Columns

```python
df_dropped = df.drop(columns=["City", "Salary"])
print(df_dropped)
#       Name  Age
# 0    Alice   28
# 1      Bob   35
# 2  Charlie   42
```

### Using axis Parameter

```python
# axis=1 means columns
df_dropped = df.drop("City", axis=1)
df_dropped = df.drop(["City", "Salary"], axis=1)
```

---

## 📖 2. Dropping Rows

### Drop Single Row

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31]
}, index=["emp1", "emp2", "emp3", "emp4"])

# Drop by label
df_dropped = df.drop(index=["emp2"])
print(df_dropped)
#          Name  Age
# emp1    Alice   28
# emp3  Charlie   42
# emp4    Diana   31
```

### Drop Multiple Rows

```python
df_dropped = df.drop(index=["emp1", "emp3"])
print(df_dropped)
#       Name  Age
# emp2    Bob   35
# emp4  Diana   31
```

### Drop by Position (Using iloc)

```python
# Drop first row
df_dropped = df.iloc[1:]

# Drop last row
df_dropped = df.iloc[:-1]

# Drop specific positions
df_dropped = df.drop(df.index[[0, 2]])
```

---

## 📖 3. Dropping Missing Data

### dropna() — Remove Rows with NaN

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, np.nan, 42, 31],
    "Salary": [75000, 82000, np.nan, 68000],
    "City": ["New York", None, "Paris", "Tokyo"]
})

# Drop rows with any NaN
print(df.dropna())
#     Name   Age  Salary      City
# 0  Alice  28.0  75000  New York
# 3  Diana  31.0  68000     Tokyo

# Drop rows with all NaN
print(df.dropna(how="all"))
#       Name   Age  Salary      City
# 0    Alice  28.0  75000  New York
# 1      Bob   NaN  82000      None
# 2  Charlie  42.0     NaN     Paris
# 3    Diana  31.0  68000     Tokyo
```

### Drop Rows with NaN in Specific Columns

```python
# Drop rows where "Age" is NaN
print(df.dropna(subset=["Age"]))
#       Name   Age  Salary      City
# 0    Alice  28.0  75000  New York
# 2  Charlie  42.0     NaN     Paris
# 3    Diana  31.0  68000     Tokyo

# Drop rows where "Age" OR "Salary" is NaN
print(df.dropna(subset=["Age", "Salary"]))
#     Name   Age  Salary      City
# 0  Alice  28.0  75000  New York
# 3  Diana  31.0  68000     Tokyo
```

### Drop Rows with Threshold

```python
# Drop rows with less than 3 non-null values
print(df.dropna(thresh=3))
#       Name   Age  Salary      City
# 0    Alice  28.0  75000  New York
# 2  Charlie  42.0     NaN     Paris
# 3    Diana  31.0  68000     Tokyo
```

### Drop Columns with NaN

```python
# Drop columns with any NaN
print(df.dropna(axis=1))
#       Name
# 0    Alice
# 1      Bob
# 2  Charlie
# 3    Diana
```

---

## 📖 4. Dropping Duplicates

### Drop Duplicate Rows

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
    "Age": [28, 35, 28, 42, 35],
    "City": ["New York", "London", "New York", "Paris", "London"]
})

# Drop exact duplicates
print(df.drop_duplicates())
#       Name  Age      City
# 0    Alice   28  New York
# 1      Bob   35    London
# 3  Charlie   42     Paris

# Count duplicates
print(df.duplicated().sum())  # 2
```

### Drop Duplicates Based on Specific Columns

```python
# Keep first occurrence
print(df.drop_duplicates(subset=["Name"]))
#       Name  Age      City
# 0    Alice   28  New York
# 1      Bob   35    London
# 3  Charlie   42     Paris

# Keep last occurrence
print(df.drop_duplicates(subset=["Name"], keep="last"))
#       Name  Age    City
# 2    Alice   28  New York
# 4      Bob   35  London
# 3  Charlie   42   Paris
```

### Drop All Duplicates

```python
# Remove all duplicate rows (keep none)
print(df.drop_duplicates(keep=False))
#       Name  Age      City
# 3  Charlie   42     Paris
```

---

## 📖 5. Dropping Based on Conditions

### Drop Rows Where Condition is True

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "Active": [True, False, True, False]
})

# Drop inactive users
df_active = df[df["Active"] == True]

# Or using ~ for opposite
df_active = df[~(df["Active"] == False)]

# Drop rows where Age > 35
df_young = df[df["Age"] <= 35]
```

### Drop Rows by Multiple Conditions

```python
# Keep only rows that meet ALL conditions
df_filtered = df[(df["Age"] >= 30) & (df["Active"] == True)]
```

---

## 📖 6. Using inplace Parameter

### inplace=True vs Assignment

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42]
})

# Method 1: Assignment (recommended)
df_new = df.drop(columns=["Age"])

# Method 2: inplace (modifies original)
df.drop(columns=["Age"], inplace=True)
```

### Recommendation

```python
# Preferred — creates new DataFrame
df_new = df.drop(columns=["col"])

# Avoid — modifies original
# df.drop(columns=["col"], inplace=True)
```

---

## 📖 7. Real-World Example

```python
import pandas as pd
import numpy as np

# Sample dataset with issues
np.random.seed(42)
df = pd.DataFrame({
    "ID": range(1, 101),
    "Name": [f"User_{i}" for i in range(1, 101)],
    "Age": np.random.choice([25, 30, 35, np.nan, 40], 100),
    "Email": np.random.choice(["a@test.com", "b@test.com", None, "d@test.com"], 100),
    "Score": np.random.randint(0, 100, 100),
    "Category": np.random.choice(["A", "B", "C"], 100)
})

print("Original shape:", df.shape)
print("Missing values:\n", df.isnull().sum())

# Step 1: Drop rows with missing critical data
df_clean = df.dropna(subset=["Name", "Email"])

# Step 2: Drop duplicate emails
df_clean = df_clean.drop_duplicates(subset=["Email"], keep="first")

# Step 3: Drop unnecessary columns
df_clean = df_clean.drop(columns=["ID"])

# Step 4: Drop outliers (e.g., Age > 50)
df_clean = df_clean[df_clean["Age"] <= 50]

# Step 5: Reset index
df_clean = df_clean.reset_index(drop=True)

print("\nCleaned shape:", df_clean.shape)
print("Missing values:\n", df_clean.isnull().sum())
```

---

## ❌ 8. Common Mistakes

### Mistake 1: Not Assigning the Result

```python
# Bad — doesn't change df
df.drop(columns=["Age"])

# Good — assign the result
df = df.drop(columns=["Age"])
# or
df_new = df.drop(columns=["Age"])
```

### Mistake 2: Dropping the Wrong Axis

```python
# Bad — drops row "Age" instead of column
df.drop("Age", axis=0)

# Good — drops column "Age"
df.drop("Age", axis=1)
df.drop(columns=["Age"])
```

### Mistake 3: Dropping All Rows with dropna()

```python
# Bad — may drop too many rows
df.dropna()

# Good — be specific about columns
df.dropna(subset=["critical_column"])
```

### Mistake 4: Forgetting to Reset Index

```python
# Bad — index has gaps
df_dropped = df.drop(index=[0, 2, 4])

# Good — reset index
df_dropped = df.drop(index=[0, 2, 4]).reset_index(drop=True)
```

---

## ✅ 9. Best Practices

1. **Assign the result** — don't rely on inplace
2. **Be specific with dropna()** — use subset parameter
3. **Check duplicates first** — use `.duplicated().sum()`
4. **Reset index after dropping** — use `.reset_index(drop=True)`
5. **Use columns= parameter** — more readable than axis=1
6. **Create new DataFrame** — preserve original
7. **Validate after dropping** — check shape and contents
8. **Document what was dropped** — for reproducibility

---

## 🏋️ 10. Exercises

### Exercise 1: Column Dropping

```python
import pandas as pd

# TODO: Create a DataFrame with 5 columns
# TODO: Drop one column
# TODO: Drop two columns
# TODO: Drop columns by position using iloc
```

### Exercise 2: Missing Data

```python
import pandas as pd
import numpy as np

# TODO: Create a DataFrame with missing values
# TODO: Drop rows with any NaN
# TODO: Drop rows with all NaN
# TODO: Drop rows where specific column is NaN
# TODO: Drop columns with any NaN
```

### Exercise 3: Duplicates

```python
import pandas as pd

# TODO: Create a DataFrame with duplicates
# TODO: Count exact duplicates
# TODO: Drop duplicates keeping first
# TODO: Drop duplicates based on specific column
```

---

## 📝 11. Summary

| Method | Purpose |
|---|---|
| `df.drop(columns=["col"])` | Drop columns |
| `df.drop(index=["label"])` | Drop rows by label |
| `df.dropna()` | Drop rows with NaN |
| `df.dropna(subset=["col"])` | Drop rows with NaN in specific columns |
| `df.dropna(thresh=n)` | Drop rows with less than n non-null |
| `df.dropna(axis=1)` | Drop columns with NaN |
| `df.drop_duplicates()` | Drop duplicate rows |
| `df.drop_duplicates(subset=["col"])` | Drop duplicates by column |
| `df[condition]` | Drop rows by condition |

### Next Lecture

In [Lecture 11: Rename Columns](./11-rename-columns-lecture.md), we will explore techniques for renaming columns and index labels.

---

## 📚 Further Reading

- [Pandas drop Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html)
- [Pandas dropna Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html)
- [Pandas drop_duplicates Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html)
