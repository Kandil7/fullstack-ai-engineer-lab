# Glossary 04: DataFrames Deep Dive

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| DataFrame | 2D labeled data structure | `pd.DataFrame(data)` |
| loc | Label-based indexing | `df.loc["row1"]` |
| iloc | Position-based indexing | `df.iloc[0]` |
| Boolean Indexing | Filter rows by condition | `df[df["A"] > 5]` |
| drop | Remove rows or columns | `df.drop(columns=["A"])` |
| rename | Change column or index labels | `df.rename(columns={...})` |
| sort_values | Sort by column values | `df.sort_values("A")` |
| sort_index | Sort by index labels | `df.sort_index()` |
| isnull | Detect missing values | `df.isnull().sum()` |
| dropna | Remove missing values | `df.dropna()` |
| fillna | Fill missing values | `df.fillna(0)` |
| groupby | Group by column values | `df.groupby("A")` |
| agg | Aggregate grouped data | `df.groupby("A").agg(...)` |
| concat | Concatenate DataFrames | `pd.concat([df1, df2])` |
| assign | Add columns (returns new df) | `df.assign(new_col=...)` |

---

## Alphabetical Definitions

### A

**Aggregation (agg)**
Reducing grouped data to summary statistics using functions like sum, mean, count.

```python
df.groupby("Department").agg(
    avg_salary=("Salary", "mean"),
    count=("Employee", "count")
)
```

**Assign**
Adds new columns to a DataFrame and returns a new DataFrame (does not modify original).

```python
df_new = df.assign(bonus=df["Salary"] * 0.1)
```

### B

**Boolean Indexing**
Filtering rows using a boolean mask (True/False conditions).

```python
df[df["Age"] > 30]
df[(df["Age"] > 25) & (df["Salary"] > 70000)]
```

### C

**Columns**
The vertical labels of a DataFrame.

```python
print(df.columns)
# Index(['Name', 'Age', 'Salary'], dtype='object')
```

**Concat**
Combines two or more DataFrames vertically or horizontally.

```python
df_combined = pd.concat([df1, df2], ignore_index=True)
```

### D

**DataFrame**
A 2D labeled data structure with rows and columns.

```python
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
```

**Drop**
Removes specified rows or columns from a DataFrame.

```python
df.drop(columns=["A"])       # Drop column
df.drop(index=[0, 1])        # Drop rows
```

**Dtypes**
Data types of each column.

```python
print(df.dtypes)
# A    int64
# B    object
```

### F

**Fillna**
Replaces missing values with a specified value or strategy.

```python
df.fillna(0)                          # Fill with 0
df.fillna({"A": 0, "B": "Unknown"})   # Fill per column
df.fillna(method="ffill")             # Forward fill
```

### G

**Groupby**
Groups rows by column values for aggregation.

```python
df.groupby("Department")["Salary"].mean()
```

### H

**Head**
Returns the first n rows (default 5).

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
Prints a concise summary of the DataFrame.

```python
df.info()
```

**Iloc**
Position-based indexing (integer positions).

```python
df.iloc[0]           # First row
df.iloc[0:5]         # First 5 rows
df.iloc[0, 1]        # Row 0, column 1
```

**Isnull**
Returns a boolean DataFrame indicating missing values.

```python
print(df.isnull().sum())
```

### L

**Loc**
Label-based indexing (index labels).

```python
df.loc["emp1"]              # Row with label "emp1"
df.loc["emp1", "Name"]      # Row and column
df.loc["emp1":"emp3"]       # Slice
```

### R

**Rename**
Changes column or index labels.

```python
df.rename(columns={"old": "new"})
df.rename(index={0: "first"})
```

**Reset Index**
Resets the index to default integers.

```python
df.reset_index(drop=True)
```

### S

**Set Index**
Sets a column as the index.

```python
df.set_index("Name")
```

**Shape**
Tuple of (rows, columns).

```python
print(df.shape)  # (100, 5)
```

**Sort Index**
Sorts by index labels.

```python
df.sort_index()
```

**Sort Values**
Sorts by column values.

```python
df.sort_values("Age", ascending=False)
```

### T

**Tail**
Returns the last n rows (default 5).

```python
print(df.tail(3))
```

---

## Code Examples

### Example 1: Column Selection

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42],
    "City": ["New York", "London", "Paris"]
})

# Single column (Series)
print(df["Name"])

# Multiple columns (DataFrame)
print(df[["Name", "Age"]])
```

### Example 2: Row Selection

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31]
}, index=["emp1", "emp2", "emp3", "emp4"])

# loc — label-based
print(df.loc["emp2"])
print(df.loc["emp1":"emp3"])

# iloc — position-based
print(df.iloc[0])
print(df.iloc[0:2])

# Boolean
print(df[df["Age"] > 30])
```

### Example 3: Grouping

```python
import pandas as pd

df = pd.DataFrame({
    "Department": ["Eng", "Mkt", "Eng", "Sales"],
    "Employee": ["Alice", "Bob", "Charlie", "Diana"],
    "Salary": [95000, 72000, 88000, 65000]
})

print(df.groupby("Department")["Salary"].agg(["mean", "sum", "count"]))
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| loc | DataFrame | Label-based row/column selection |
| iloc | DataFrame | Position-based row/column selection |
| drop | DataFrame | Remove rows/columns |
| rename | DataFrame | Change labels |
| sort_values | DataFrame | Sort by values |
| isnull | DataFrame | Detect missing data |
| fillna | DataFrame | Handle missing data |
| groupby | DataFrame | Group for aggregation |
| concat | DataFrame | Combine DataFrames |
| assign | DataFrame | Add columns |

---

## Key Operations Reference

```
Column Selection:
  df["col"]             -> Series
  df[["col1", "col2"]]  -> DataFrame

Row Selection:
  df.loc[label]         -> Label-based
  df.iloc[pos]          -> Position-based
  df[condition]         -> Boolean filtering

Add/Remove:
  df["new_col"] = val   -> Add column
  df.drop(columns=[...]) -> Remove column
  df.drop(index=[...])   -> Remove row

Sorting:
  df.sort_values("col") -> Sort by column
  df.sort_index()       -> Sort by index

Missing Data:
  df.isnull().sum()     -> Count missing
  df.dropna()           -> Remove missing
  df.fillna(val)        -> Fill missing

Grouping:
  df.groupby("col")     -> Group
  .agg(func)            -> Aggregate
```

---

## Self-Test Questions

1. What is the difference between `.loc` and `.iloc`?
2. How do you select multiple columns?
3. How do you drop rows with missing values?
4. What does `.groupby().agg()` do?
5. How do you add a new column without modifying the original?
