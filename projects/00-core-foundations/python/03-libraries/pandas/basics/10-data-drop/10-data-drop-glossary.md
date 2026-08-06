# Glossary 10: Data Drop

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| drop | Remove rows or columns | `df.drop(columns=["A"])` |
| dropna | Remove rows with NaN | `df.dropna()` |
| drop_duplicates | Remove duplicate rows | `df.drop_duplicates()` |
| axis | 0=row, 1=column | `df.drop("A", axis=1)` |
| inplace | Modify original DataFrame | `df.drop(inplace=True)` |
| subset | Specific columns to check | `df.dropna(subset=["A"])` |
| thresh | Minimum non-null count | `df.dropna(thresh=3)` |
| how | all=drop if all NaN, any=drop if any | `df.dropna(how="all")` |
| keep | first, last, or False | `df.drop_duplicates(keep="first")` |
| reset_index | Reset index after dropping | `df.reset_index(drop=True)` |

---

## Alphabetical Definitions

### D

**Drop**
Removes specified rows or columns from a DataFrame.

```python
df.drop(columns=["A"])       # Drop column
df.drop(index=["row1"])      # Drop row by label
df.drop(df.index[[0, 2]])    # Drop rows by position
```

**Drop Duplicates**
Removes duplicate rows from a DataFrame.

```python
df.drop_duplicates()                    # Exact duplicates
df.drop_duplicates(subset=["Name"])     # By specific column
df.drop_duplicates(keep="last")         # Keep last occurrence
```

**Drop NA**
Removes rows or columns with missing values.

```python
df.dropna()                           # Any NaN in row
df.dropna(how="all")                  # All values NaN
df.dropna(subset=["Age"])             # Check specific column
df.dropna(thresh=3)                   # At least 3 non-null
df.dropna(axis=1)                     # Drop columns with NaN
```

### H

**How**
Parameter for dropna — determines when to drop.

```python
df.dropna(how="any")    # Drop if ANY value is NaN (default)
df.dropna(how="all")    # Drop if ALL values are NaN
```

### I

**Inplace**
When True, modifies the original DataFrame instead of returning a new one.

```python
df.drop(columns=["A"], inplace=True)  # Modifies df directly
```

### K

**Keep**
Parameter for drop_duplicates — which duplicates to keep.

```python
df.drop_duplicates(keep="first")   # Keep first occurrence
df.drop_duplicates(keep="last")    # Keep last occurrence
df.drop_duplicates(keep=False)     # Remove all duplicates
```

### R

**Reset Index**
Resets the index to default integers after dropping.

```python
df.drop(index=[0, 2]).reset_index(drop=True)
```

### S

**Subset**
Specific columns to check for NaN or duplicates.

```python
df.dropna(subset=["Age", "Salary"])
df.drop_duplicates(subset=["Name", "Email"])
```

### T

**Thresh**
Minimum number of non-null values required to keep a row.

```python
df.dropna(thresh=3)  # Keep rows with at least 3 non-null values
```

---

## Code Examples

### Example 1: Drop Columns

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob"],
    "Age": [28, 35],
    "City": ["NYC", "London"]
})

# Drop one column
df1 = df.drop(columns=["City"])

# Drop multiple columns
df2 = df.drop(columns=["Age", "City"])

# Using axis
df3 = df.drop("City", axis=1)
```

### Example 2: Drop Rows

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42]
}, index=["emp1", "emp2", "emp3"])

# Drop by label
df1 = df.drop(index=["emp2"])

# Drop by position
df2 = df.drop(df.index[[0, 2]])

# Drop by condition
df3 = df[df["Age"] > 30]
```

### Example 3: Drop Missing/Duplicates

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Alice", "Charlie"],
    "Age": [28, np.nan, 28, 42]
})

# Drop NaN
print(df.dropna())
print(df.dropna(subset=["Age"]))

# Drop duplicates
print(df.drop_duplicates())
print(df.drop_duplicates(subset=["Name"], keep="last"))
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| drop | DataFrame | Remove rows/columns |
| dropna | DataFrame | Remove missing data |
| drop_duplicates | DataFrame | Remove duplicates |
| inplace | Methods | Modify original |
| reset_index | DataFrame | Fix index after dropping |
| subset | dropna | Columns to check |
| thresh | dropna | Minimum non-null count |

---

## Drop Methods Reference

```
Columns:
  df.drop(columns=["col"])      -> Drop by name
  df.drop("col", axis=1)        -> Drop by name
  df.drop(df.columns[0:2])      -> Drop by position

Rows:
  df.drop(index=["label"])      -> Drop by label
  df.drop(df.index[[0, 2]])     -> Drop by position
  df[df["A"] > 5]               -> Drop by condition

Missing:
  df.dropna()                   -> Drop rows with any NaN
  df.dropna(how="all")          -> Drop if all NaN
  df.dropna(subset=["col"])     -> Check specific column
  df.dropna(thresh=3)           -> Require min non-null

Duplicates:
  df.drop_duplicates()          -> Exact duplicates
  df.drop_duplicates(subset=["col"])  -> By column
  df.drop_duplicates(keep="first")    -> Keep strategy
```

---

## Self-Test Questions

1. How do you drop a column by name?
2. What does `dropna(how="all")` do?
3. How do you drop rows with NaN in a specific column?
4. What is the difference between `keep="first"` and `keep="last"`?
5. Why should you reset the index after dropping rows?
