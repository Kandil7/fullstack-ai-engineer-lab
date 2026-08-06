# Lecture 08: Data Selecting

## 🎯 Learning Objectives

By the end of this lecture, you will be able to:

- Select columns by name and position
- Select rows by label and position
- Use boolean indexing to filter data
- Combine multiple conditions
- Select specific cells using loc and iloc
- Understand the differences between [], loc, and iloc

---

## 📖 1. Column Selection

### Single Column (Returns Series)

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "City": ["New York", "London", "Paris", "Tokyo"],
    "Salary": [75000, 82000, 95000, 68000]
})

# Bracket notation (recommended)
print(df["Name"])
# 0      Alice
# 1        Bob
# 2    Charlie
# 3      Diana

# Dot notation (only for valid identifiers)
print(df.Name)
```

### Multiple Columns (Returns DataFrame)

```python
# Select multiple columns
print(df[["Name", "Age"]])
#       Name  Age
# 0    Alice   28
# 1      Bob   35
# 2  Charlie   42
# 3    Diana   31

# Order matters
print(df[["Age", "Name"]])
#    Age     Name
# 0   28    Alice
# 1   35      Bob
# 2   42  Charlie
# 3   31    Diana
```

### Column Selection with loc

```python
# Select all rows for specific columns
print(df.loc[:, ["Name", "Salary"]])
```

---

## 📖 2. Row Selection

### By Label (loc)

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31]
}, index=["emp1", "emp2", "emp3", "emp4"])

# Single row by label
print(df.loc["emp2"])
# Name    Bob
# Age      35

# Multiple rows
print(df.loc[["emp1", "emp3"]])
#       Name  Age
# emp1  Alice   28
# emp3 Charlie  42

# Slice (inclusive end)
print(df.loc["emp1":"emp3"])
#       Name  Age
# emp1  Alice   28
# emp2    Bob   35
# emp3 Charlie  42
```

### By Position (iloc)

```python
# Single row by position
print(df.iloc[0])
# Name    Alice
# Age        28

# Multiple rows
print(df.iloc[[0, 2]])
#       Name  Age
# emp1  Alice   28
# emp3 Charlie  42

# Slice (exclusive end)
print(df.iloc[0:2])
#      Name  Age
# emp1 Alice   28
# emp2   Bob   35

# Negative indexing
print(df.iloc[-1])  # Last row
print(df.iloc[-2:]) # Last 2 rows
```

---

## 📖 3. Boolean Indexing

### Basic Filtering

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Age": [28, 35, 42, 31, 29],
    "Salary": [75000, 82000, 95000, 68000, 71000]
})

# Create boolean mask
mask = df["Age"] > 30
print(mask)
# 0    False
# 1     True
# 2     True
# 3     True
# 4    False

# Apply mask
print(df[mask])
#       Name  Age  Salary
# 1      Bob   35   82000
# 2  Charlie   42   95000
# 3    Diana   31   68000

# Or inline
print(df[df["Age"] > 30])
```

### Multiple Conditions

```python
# AND condition (&)
print(df[(df["Age"] >= 30) & (df["Salary"] >= 70000)])
#       Name  Age  Salary
# 1      Bob   35   82000
# 2  Charlie   42   95000
# 3    Diana   31   68000

# OR condition (|)
print(df[(df["Age"] < 30) | (df["Salary"] > 80000)])
#       Name  Age  Salary
# 0    Alice   28   75000
# 1      Bob   35   82000
# 2  Charlie   42   95000

# NOT condition (~)
print(df[~(df["Age"] > 30)])
#     Name  Age  Salary
# 0  Alice   28   75000
# 4    Eve   29   71000
```

### Using .isin()

```python
print(df[df["Name"].isin(["Alice", "Charlie"])])
#       Name  Age  Salary
# 0    Alice   28   75000
# 2  Charlie   42   95000
```

### Using .between()

```python
print(df[df["Age"].between(30, 40)])
#     Name  Age  Salary
# 1    Bob   35   82000
# 3  Diana   31   68000
```

---

## 📖 4. Cell Selection

### Using loc (Label-based)

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42],
    "City": ["New York", "London", "Paris"]
}, index=["emp1", "emp2", "emp3"])

# Single cell
print(df.loc["emp2", "Name"])  # Bob

# Row and column slice
print(df.loc["emp1":"emp2", "Name":"Age"])
#      Name  Age
# emp1 Alice   28
# emp2   Bob   35
```

### Using iloc (Position-based)

```python
# Single cell
print(df.iloc[1, 0])  # Bob

# Row and column slice
print(df.iloc[0:2, 0:2])
#       Name  Age
# emp1  Alice   28
# emp2    Bob   35
```

---

## 📖 5. Conditional Selection

### Using query()

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "Department": ["Eng", "Mkt", "Eng", "Sales"]
})

# Using query method
print(df.query("Age > 30"))
print(df.query("Department == 'Eng'"))
print(df.query("Age > 30 and Department == 'Eng'"))

# Using variables
min_age = 30
print(df.query("Age > @min_age"))
```

### Using where()

```python
# Returns DataFrame with NaN where condition is False
print(df.where(df["Age"] > 30))
#       Name   Age Department
# 0      NaN   NaN        NaN
# 1      Bob  35.0        Mkt
# 2  Charlie  42.0        Eng
# 3    Diana  31.0      Sales
```

### Using mask()

```python
# Opposite of where — returns NaN where condition is True
print(df.mask(df["Age"] > 30))
#       Name   Age Department
# 0    Alice  28.0        Eng
# 1      NaN   NaN        NaN
# 2      NaN   NaN        NaN
# 3      NaN   NaN        NaN
```

---

## 📖 6. Random Access

### Using sample()

```python
# Random 5 rows
print(df.sample(5))

# Random 20% of rows
print(df.sample(frac=0.2))

# Sample with replacement
print(df.sample(5, replace=True))

# Random column selection
print(df.sample(axis=1, n=2))
```

### Using nsmallest() and nlargest()

```python
import pandas as pd

df = pd.DataFrame({
    "Product": ["A", "B", "C", "D", "E"],
    "Sales": [100, 250, 150, 300, 200]
})

# Top 3 by sales
print(df.nlargest(3, "Sales"))
#   Product  Sales
# 3       D    300
# 1       B    250
# 4       E    200

# Bottom 2 by sales
print(df.nsmallest(2, "Sales"))
#   Product  Sales
# 0       A    100
# 2       C    150
```

---

## 📖 7. Real-World Example

```python
import pandas as pd

# Load dataset
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
df = pd.read_csv(url)

# Select specific columns
passengers = df[["Name", "Age", "Pclass", "Survived"]]

# Filter survivors
survivors = df[df["Survived"] == 1]

# Filter by class and age
first_class_adults = df[(df["Pclass"] == 1) & (df["Age"] >= 18)]

# Find youngest and oldest
youngest = df.nsmallest(1, "Age")
oldest = df.nlargest(1, "Age")

# Filter by name pattern
smiths = df[df["Name"].str.contains("Smith", na=False)]

# Multiple conditions with query
result = df.query("Pclass == 1 and Age > 30 and Survived == 1")
```

---

## ❌ 8. Common Mistakes

### Mistake 1: Using & instead of and

```python
# Bad — syntax error
# df[(df["Age"] > 30) and (df["Salary"] > 70000)]

# Good — use & operator
df[(df["Age"] > 30) & (df["Salary"] > 70000)]
```

### Mistake 2: Forgetting Parentheses

```python
# Bad — wrong precedence
# df[df["Age"] > 30 & df["Salary"] > 70000]

# Good — explicit parentheses
df[(df["Age"] > 30) & (df["Salary"] > 70000)]
```

### Mistake 3: Using loc with Integer Position

```python
# Bad — loc is label-based
# df.loc[0]  # May work if index is 0, but confusing

# Good — use iloc for position
df.iloc[0]
```

### Mistake 4: Modifying a View

```python
# Bad — may raise SettingWithCopyWarning
# df[df["Age"] > 30]["Name"] = "Unknown"

# Good — use .loc
df.loc[df["Age"] > 30, "Name"] = "Unknown"
```

---

## ✅ 9. Best Practices

1. **Use `.loc` for label-based** — explicit and clear
2. **Use `.iloc` for position-based** — unambiguous
3. **Use parentheses** — for complex boolean conditions
4. **Use `&` and `|`** — not `and` and `or`
5. **Use `.isin()`** — for multiple value matching
6. **Use `.query()`** — for readable complex conditions
7. **Check dtypes** — before filtering on numeric columns
8. **Use `.copy()`** — when modifying filtered data

---

## 🏋️ 10. Exercises

### Exercise 1: Column Selection

```python
import pandas as pd

# TODO: Create a DataFrame with 5 columns
# TODO: Select a single column (returns Series)
# TODO: Select 3 columns (returns DataFrame)
# TODO: Select columns by position using iloc
```

### Exercise 2: Row Filtering

```python
import pandas as pd

# TODO: Create a DataFrame with numeric columns
# TODO: Filter rows where column A > 50
# TODO: Filter rows where column A > 50 AND column B < 100
# TODO: Filter rows where column C is in ["X", "Y", "Z"]
```

### Exercise 3: Complex Selection

```python
import pandas as pd

# TODO: Load the Titanic dataset
# TODO: Select female passengers in first class
# TODO: Find passengers aged 20-30
# TODO: Get the top 10% by fare
```

---

## 📝 11. Summary

| Method | Purpose |
|---|---|
| `df["col"]` | Single column |
| `df[["col1", "col2"]]` | Multiple columns |
| `df.loc[label]` | Row by label |
| `df.iloc[pos]` | Row by position |
| `df.loc[row, col]` | Cell by label |
| `df.iloc[row, col]` | Cell by position |
| `df[condition]` | Boolean filtering |
| `df.query("expr")` | Query string filtering |
| `df.isin([...])` | Value matching |
| `df.between(a, b)` | Range filtering |
| `df.nlargest(n, col)` | Top n by column |
| `df.nsmallest(n, col)` | Bottom n by column |

### Next Lecture

In [Lecture 09: Data loc and iloc](./09-data-loc-lecture.md), we will dive deeper into the loc and iloc indexers for precise data selection.

---

## 📚 Further Reading

- [Pandas Indexing Documentation](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [Pandas Selection Documentation](https://pandas.pydata.org/docs/reference/frame.html#selection-by-label)
- [Pandas Boolean Indexing](https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing)
