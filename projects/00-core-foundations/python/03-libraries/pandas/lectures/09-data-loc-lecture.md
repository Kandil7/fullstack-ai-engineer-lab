# Lecture 09: Data loc and iloc Deep Dive

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Master loc for label-based selection
- Master iloc for position-based selection
- Use advanced slicing techniques
- Select cells, rows, and columns precisely
- Understand the differences between loc and iloc
- Avoid common indexing pitfalls

---

## 📖 1. Understanding loc vs iloc

| Feature | loc | iloc |
|---|---|---|
| Indexing Type | Label-based | Position-based |
| Inclusive End | Yes | No |
| Can Use Boolean | Yes | No |
| Works With | Index labels | Integer positions |

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31]
}, index=["emp1", "emp2", "emp3", "emp4"])

# loc — uses labels
print(df.loc["emp1"])       # Row with label "emp1"

# iloc — uses integer positions
print(df.iloc[0])           # First row (position 0)
```

---

## 📖 2. loc In Depth

### Select Single Row

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "City": ["New York", "London", "Paris", "Tokyo"]
}, index=["emp1", "emp2", "emp3", "emp4"])

print(df.loc["emp2"])
# Name      Bob
# Age        35
# City    London
```

### Select Multiple Rows

```python
print(df.loc[["emp1", "emp3"]])
#       Name  Age      City
# emp1  Alice   28  New York
# emp3 Charlie  42     Paris
```

### Select Row Slice (Inclusive)

```python
print(df.loc["emp1":"emp3"])
#       Name  Age      City
# emp1  Alice   28  New York
# emp2    Bob   35    London
# emp3 Charlie  42     Paris
```

### Select Row and Column

```python
# Single cell
print(df.loc["emp2", "Name"])  # Bob

# Multiple columns
print(df.loc["emp1", ["Name", "City"]])
# Name      Alice
# City    New York
```

### Select Multiple Rows and Columns

```python
print(df.loc["emp1":"emp3", "Name":"Age"])
#       Name  Age
# emp1  Alice   28
# emp2    Bob   35
# emp3 Charlie  42
```

### Select All Rows for Specific Columns

```python
print(df.loc[:, ["Name", "Age"]])
```

### Select All Columns for Specific Rows

```python
print(df.loc[["emp1", "emp3"], :])
```

---

## 📖 3. iloc In Depth

### Select Single Row

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "City": ["New York", "London", "Paris", "Tokyo"]
})

print(df.iloc[0])
# Name    Alice
# Age        28
# City    New York
```

### Select Multiple Rows

```python
print(df.iloc[[0, 2]])
#       Name  Age      City
# 0    Alice   28  New York
# 2  Charlie   42     Paris
```

### Select Row Slice (Exclusive End)

```python
print(df.iloc[0:2])
#     Name  Age      City
# 0  Alice   28  New York
# 1    Bob   35    London
```

### Select Row and Column

```python
# Single cell
print(df.iloc[1, 0])  # Bob

# Multiple columns
print(df.iloc[0, [0, 2]])
# Name      Alice
# City    New York
```

### Select Multiple Rows and Columns

```python
print(df.iloc[0:2, 0:2])
#     Name  Age
# 0  Alice   28
# 1    Bob   35
```

### Negative Indexing

```python
print(df.iloc[-1])      # Last row
print(df.iloc[-2:])     # Last 2 rows
print(df.iloc[::-1])    # Reverse order
```

---

## 📖 4. Advanced Slicing

### loc with Integer Index

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31]
})

# When index is integers, loc uses labels (integers)
print(df.loc[0:2])      # Rows 0, 1, 2 (inclusive!)
#       Name  Age
# 0    Alice   28
# 1      Bob   35
# 2  Charlie   42
```

### iloc with Integer Index

```python
# iloc always uses position
print(df.iloc[0:2])     # Rows at positions 0, 1 (exclusive end)
#     Name  Age
# 0  Alice   28
# 1    Bob   35
```

### Key Difference

```python
# loc[0:2] includes row with label 2
# iloc[0:2] excludes position 2

import pandas as pd

df = pd.DataFrame({"A": [10, 20, 30, 40]}, index=[0, 1, 2, 3])

print("loc[0:2]:")
print(df.loc[0:2])      # Returns 3 rows (0, 1, 2)

print("\niloc[0:2]:")
print(df.iloc[0:2])     # Returns 2 rows (position 0, 1)
```

---

## 📖 5. Boolean Selection with loc

### Filter Rows

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "Salary": [75000, 82000, 95000, 68000]
})

# Filter and select columns
print(df.loc[df["Age"] > 30, ["Name", "Salary"]])
#       Name  Salary
# 1      Bob   82000
# 2  Charlie   95000
# 3    Diana   68000
```

### Modify Values

```python
# Set values where condition is True
df.loc[df["Age"] > 30, "Name"] = "Senior"
print(df)
#       Name  Age  Salary
# 0    Alice   28   75000
# 1    Senior   35   82000
# 2    Senior   42   95000
# 3    Senior   31   68000
```

---

## 📖 6. Setting Values

### Using loc

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42]
}, index=["emp1", "emp2", "emp3"])

# Set a single value
df.loc["emp1", "Age"] = 29

# Set multiple values
df.loc["emp1":"emp2", "Age"] = 30

# Set with condition
df.loc[df["Age"] > 35, "Name"] = "Veteran"

print(df)
```

### Using iloc

```python
# Set by position
df.iloc[0, 1] = 29

# Set multiple values
df.iloc[0:2, 1] = 30
```

---

## 📖 7. Real-World Example

```python
import pandas as pd
import numpy as np

# Create sample data
np.random.seed(42)
df = pd.DataFrame({
    "Employee": [f"Emp_{i}" for i in range(100)],
    "Department": np.random.choice(["Eng", "Mkt", "Sales", "HR"], 100),
    "Salary": np.random.randint(50000, 120000, 100),
    "Years": np.random.randint(1, 20, 100),
    "Rating": np.random.choice([1, 2, 3, 4, 5], 100)
})
df = df.set_index("Employee")

# Get first 5 engineers
engineers = df[df["Department"] == "Eng"]
print("First 5 Engineers:")
print(engineers.iloc[:5])

# Get top 10% by salary
top earners = df.nlargest(10, "Salary")
print("\nTop 10 Earners:")
print(top earners)

# Get senior employees (10+ years) in engineering
senior_eng = df.loc[
    (df["Department"] == "Eng") & (df["Years"] >= 10),
    ["Salary", "Years", "Rating"]
]
print("\nSenior Engineers:")
print(senior_eng)

# Update ratings for low performers
df.loc[(df["Rating"] <= 2) & (df["Years"] >= 5), "Rating"] = 3
```

---

## ❌ 8. Common Mistakes

### Mistake 1: Confusing loc and iloc with Integer Index

```python
import pandas as pd

df = pd.DataFrame({"A": [10, 20, 30]}, index=[0, 1, 2])

# loc[0:2] includes index label 2 (3 rows!)
print(df.loc[0:2])
#     A
# 0  10
# 1  20
# 2  30

# iloc[0:2] excludes position 2 (2 rows)
print(df.iloc[0:2])
#     A
# 0  10
# 1  20
```

### Mistake 2: Using loc with Position

```python
# Bad — loc expects labels
# df.loc[0]  # May work if index is 0, but confusing

# Good — use iloc for position
df.iloc[0]
```

### Mistake 3: Modifying a View

```python
# Bad — may raise SettingWithCopyWarning
# df[df["Age"] > 30]["Name"] = "Senior"

# Good — use .loc
df.loc[df["Age"] > 30, "Name"] = "Senior"
```

---

## ✅ 9. Best Practices

1. **Use `.loc` for label-based** — explicit and clear
2. **Use `.iloc` for position-based** — unambiguous
3. **Understand inclusive vs exclusive** — loc is inclusive, iloc is not
4. **Use `.loc` for modification** — avoids SettingWithCopyWarning
5. **Check index type** — integer index can be confusing with loc
6. **Use `.copy()`** when modifying subsets
7. **Chain carefully** — loc/iloc work on the result
8. **Use `:` for all** — `df.loc[:, "col"]` or `df.iloc[:, 0]`

---

## 🏋️ 10. Exercises

### Exercise 1: loc Operations

```python
import pandas as pd

# TODO: Create a DataFrame with string index
# TODO: Select a single row by label
# TODO: Select multiple rows by label
# TODO: Select row and column by label
# TODO: Select a slice of rows (inclusive)
```

### Exercise 2: iloc Operations

```python
import pandas as pd

# TODO: Create a DataFrame with 10 rows
# TODO: Select first row by position
# TODO: Select last 3 rows
# TODO: Select specific cell by position
# TODO: Reverse row order
```

### Exercise 3: Combined Operations

```python
import pandas as pd

# TODO: Load the Titanic dataset
# TODO: Get first 5 rows of "Name" and "Age" columns
# TODO: Filter and select using loc
# TODO: Modify values based on condition
```

---

## 📝 11. Summary

| Method | Purpose | Inclusive? |
|---|---|---|
| `df.loc[label]` | Row by label | Yes (slices) |
| `df.iloc[pos]` | Row by position | No (slices) |
| `df.loc[label, col]` | Cell by label | Yes |
| `df.iloc[row, col]` | Cell by position | No |
| `df.loc[mask, col]` | Filtered selection | — |
| `df.loc[...] = val` | Set values | — |

### Next Lecture

In [Lecture 10: Data Drop](./10-data-drop-lecture.md), we will explore techniques for removing rows and columns from DataFrames.

---

## 📚 Further Reading

- [Pandas loc Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html)
- [Pandas iloc Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html)
- [Pandas Indexing Guide](https://pandas.pydata.org/docs/user_guide/indexing.html)
