# Lecture 04: DataFrames Deep Dive

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Create DataFrames from multiple data sources
- Perform advanced row and column operations
- Use loc and iloc for precise data selection
- Apply transformations to DataFrames
- Handle missing data in DataFrames
- Perform aggregation and grouping

---

## 📖 1. Creating DataFrames

### From a Dictionary of Lists

```python
import pandas as pd

data = {
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Department": ["Engineering", "Marketing", "Engineering", "Sales", "Marketing"],
    "Salary": [95000, 72000, 88000, 65000, 71000],
    "Years": [5, 3, 8, 2, 4]
}
df = pd.DataFrame(data)
print(df)
#       Name    Department  Salary  Years
# 0    Alice  Engineering   95000      5
# 1      Bob    Marketing   72000      3
# 2  Charlie  Engineering   88000      8
# 3    Diana        Sales   65000      2
# 4      Eve    Marketing   71000      4
```

### From a List of Dictionaries

```python
import pandas as pd

records = [
    {"Name": "Alice", "Score": 92},
    {"Name": "Bob", "Score": 85},
    {"Name": "Charlie", "Score": 78}
]
df = pd.DataFrame(records)
```

### From a 2D NumPy Array

```python
import numpy as np
import pandas as pd

arr = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])
df = pd.DataFrame(arr, columns=["A", "B", "C"], index=["x", "y", "z"])
```

### From a CSV File

```python
import pandas as pd

df = pd.read_csv("data.csv")
df = pd.read_csv("data.csv", index_col=0)  # First column as index
df = pd.read_csv("data.csv", parse_dates=["date_col"])  # Parse dates
```

---

## 📖 2. Selecting Columns

### Single Column (Returns Series)

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42],
    "City": ["New York", "London", "Paris"]
})

# Returns a Series
print(df["Name"])
# 0      Alice
# 1        Bob
# 2    Charlie

# Also works with dot notation (only for valid Python identifiers)
print(df.Name)
```

### Multiple Columns (Returns DataFrame)

```python
# Returns a DataFrame
print(df[["Name", "Age"]])
#       Name  Age
# 0    Alice   28
# 1      Bob   35
# 2  Charlie   42
```

---

## 📖 3. Selecting Rows

### By Label (loc)

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "City": ["New York", "London", "Paris", "Tokyo"]
}, index=["emp1", "emp2", "emp3", "emp4"])

# Single row by label
print(df.loc["emp2"])
# Name      Bob
# Age        35
# City    London

# Multiple rows
print(df.loc[["emp1", "emp3"]])

# Slice (inclusive end)
print(df.loc["emp1":"emp3"])

# Row and column
print(df.loc["emp1", "Name"])  # Alice
```

### By Position (iloc)

```python
# Single row by position
print(df.iloc[0])

# Multiple rows
print(df.iloc[[0, 2]])

# Slice (exclusive end)
print(df.iloc[0:2])

# Row and column
print(df.iloc[0, 1])  # 28
```

### Boolean Indexing

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31]
})

# Filter rows
adults = df[df["Age"] >= 30]
print(adults)
#       Name  Age
# 1      Bob   35
# 2  Charlie   42
# 3    Diana   31

# Multiple conditions
result = df[(df["Age"] >= 30) & (df["Age"] <= 40)]
```

---

## 📖 4. Adding and Removing

### Adding Columns

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42]
})

# Add a constant column
df["Country"] = "USA"

# Add computed column
df["Age_Group"] = df["Age"].apply(
    lambda x: "Senior" if x >= 35 else "Junior"
)

# Using assign (returns new DataFrame)
df_new = df.assign(Bonus=df["Age"] * 100)

print(df)
#       Name  Age Country Age_Group
# 0    Alice   28     USA    Junior
# 1      Bob   35     USA    Senior
# 2  Charlie   42     USA    Senior
```

### Removing Columns

```python
# Drop columns
df_dropped = df.drop(columns=["Country"])

# Drop multiple columns
df_dropped = df.drop(columns=["Country", "Age_Group"])

# Drop by axis
df_dropped = df.drop("Country", axis=1)
```

### Adding Rows

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Age": [28, 35]
})

# Add a single row
new_row = pd.DataFrame({"Name": ["Charlie"], "Age": [42]})
df = pd.concat([df, new_row], ignore_index=True)

# Add multiple rows
new_rows = pd.DataFrame({
    "Name": ["Diana", "Eve"],
    "Age": [31, 29]
})
df = pd.concat([df, new_rows], ignore_index=True)
```

### Removing Rows

```python
# Drop by index
df_dropped = df.drop(index=[0])  # Drop first row

# Drop multiple rows
df_dropped = df.drop(index=[0, 2])

# Drop by condition
df_dropped = df[df["Age"] >= 30]
```

---

## 📖 5. Renaming

### Rename Columns

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

# Rename all columns
df.columns = ["first_name", "last_name", "age"]

# Using a function
df.columns = df.columns.str.replace(" ", "_").str.lower()
```

### Rename Index

```python
df_renamed = df.rename(index={0: "emp1", 1: "emp2"})
```

---

## 📖 6. Sorting

### Sort by Values

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "Salary": [75000, 82000, 95000, 68000]
})

# Sort by single column
print(df.sort_values("Age"))
#       Name  Age  Salary
# 0    Alice   28   75000
# 3    Diana   31   68000
# 1      Bob   35   82000
# 2  Charlie   42   95000

# Sort descending
print(df.sort_values("Salary", ascending=False))

# Sort by multiple columns
print(df.sort_values(["Age", "Salary"], ascending=[True, False]))
```

### Sort by Index

```python
df_sorted = df.set_index("Name").sort_index()
```

---

## 📖 7. Handling Missing Data

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, np.nan, 42, 31],
    "Salary": [75000, 82000, np.nan, 68000],
    "City": ["New York", None, "Paris", "Tokyo"]
})

# Check for missing values
print(df.isnull())
#     Name    Age  Salary   City
# 0  False  False   False  False
# 1  False   True   False   True
# 2  False  False    True  False
# 3  False  False   False  False

print(df.isnull().sum())
# Name      0
# Age       1
# Salary    1
# City      1
# dtype: int64

# Drop rows with any missing values
print(df.dropna())

# Drop rows with all missing values
print(df.dropna(how="all"))

# Drop rows with missing values in specific columns
print(df.dropna(subset=["Age"]))

# Fill missing values
print(df.fillna(0))
print(df.fillna({"Age": df["Age"].mean(), "Salary": 0}))

# Forward fill
print(df.fillna(method="ffill"))

# Backward fill
print(df.fillna(method="bfill"))
```

---

## 📖 8. Grouping and Aggregation

```python
import pandas as pd

df = pd.DataFrame({
    "Department": ["Engineering", "Marketing", "Engineering", "Sales", "Marketing"],
    "Employee": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Salary": [95000, 72000, 88000, 65000, 71000]
})

# Group by a single column
dept_stats = df.groupby("Department")["Salary"].agg(["mean", "sum", "count"])
print(dept_stats)
#                 mean    sum  count
# Department
# Engineering    91500  183000      2
# Marketing      71500  143000      2
# Sales          65000   65000      1

# Group by multiple columns
df.groupby(["Department"]).agg(
    avg_salary=("Salary", "mean"),
    total_salary=("Salary", "sum"),
    headcount=("Employee", "count")
)
```

---

## 📖 9. Real-World Example

```python
import pandas as pd
import numpy as np

# Simulated sales data
np.random.seed(42)
df = pd.DataFrame({
    "Date": pd.date_range("2024-01-01", periods=100),
    "Region": np.random.choice(["North", "South", "East", "West"], 100),
    "Product": np.random.choice(["Laptop", "Phone", "Tablet"], 100),
    "Sales": np.random.randint(1000, 10000, 100),
    "Quantity": np.random.randint(1, 20, 100)
})

# Quick exploration
print("Shape:", df.shape)
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())
print("\nBasic stats:")
print(df.describe())

# Group analysis
print("\nSales by Region:")
print(df.groupby("Region")["Sales"].sum())

print("\nSales by Product:")
print(df.groupby("Product")["Sales"].mean())
```

---

## ❌ 10. Common Mistakes

### Mistake 1: Using `[]` for Row Selection

```python
import pandas as pd

df = pd.DataFrame({"A": [1, 2, 3]}, index=["a", "b", "c"])

# Bad — ambiguous
# print(df["a"])  # May work, but confusing

# Good — use .loc
print(df.loc["a"])
```

### Mistake 2: Modifying a View

```python
# Bad — may raise SettingWithCopyWarning
# df[df["Age"] > 30]["Name"] = "Unknown"

# Good — use .loc
df.loc[df["Age"] > 30, "Name"] = "Unknown"
```

### Mistake 3: Forgetting `ignore_index`

```python
import pandas as pd

df1 = pd.DataFrame({"A": [1, 2]})
df2 = pd.DataFrame({"A": [3, 4]})

# Bad — index is duplicated
df_bad = pd.concat([df1, df2])

# Good — reset index
df_good = pd.concat([df1, df2], ignore_index=True)
```

---

## ✅ 11. Best Practices

1. **Use `.loc` and `.iloc`** — avoid ambiguous indexing
2. **Check missing values early** — `.isnull().sum()` before processing
3. **Use `.assign()` for chaining** — keeps transformations readable
4. **Avoid `inplace=True`** — prefer assignment for clarity
5. **Use `.copy()`** when modifying subsets
6. **Group and aggregate** — use `.groupby()` instead of loops
7. **Reset index after operations** — use `.reset_index(drop=True)`

---

## 🏋️ 12. Exercises

### Exercise 1: Data Manipulation

```python
import pandas as pd
import numpy as np

# TODO: Create a DataFrame with 100 rows:
# - student_id: 1-100
# - name: random names
# - score: random 0-100
# - grade: A/B/C/D/F based on score

# TODO: Add a "pass" column (score >= 60)
# TODO: Remove students with score < 30
# TODO: Calculate pass rate by grade
```

### Exercise 2: Missing Data

```python
import pandas as pd
import numpy as np

# TODO: Create a DataFrame with intentional missing values
# TODO: Calculate missing percentage per column
# TODO: Fill missing numeric values with column mean
# TODO: Drop rows where all values are missing
```

### Exercise 3: Grouping

```python
import pandas as pd

# TODO: Using the sales dataset above
# TODO: Find top 3 products by total sales
# TODO: Find average sales per region per product
# TODO: Find the day with highest total sales
```

---

## 📝 13. Summary

| Concept | What You Learned |
|---|---|
| Column Selection | `df["col"]`, `df[["col1", "col2"]]` |
| Row Selection | `.loc[]`, `.iloc[]`, boolean indexing |
| Adding Columns | Direct assignment, `.assign()` |
| Removing Columns | `.drop(columns=[...])` |
| Adding Rows | `pd.concat()` |
| Removing Rows | `.drop(index=[...])`, boolean filtering |
| Renaming | `.rename()`, direct `.columns` assignment |
| Sorting | `.sort_values()`, `.sort_index()` |
| Missing Data | `.isnull()`, `.dropna()`, `.fillna()` |
| Grouping | `.groupby().agg()` |

### Next Lecture

In [Lecture 05: Loading Data](./05-load-data-lecture.md), we will explore how to load data from various file formats into DataFrames.

---

## 📚 Further Reading

- [Pandas DataFrame Documentation](https://pandas.pydata.org/docs/reference/frame.html)
- [Pandas User Guide: Indexing and Selecting Data](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [Pandas User Guide: Missing Data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
