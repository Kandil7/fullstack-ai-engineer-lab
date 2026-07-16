# Glossary 08: Data Selecting

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| Column Selection | Select by name | `df["col"]` |
| Row Selection | Select by label/position | `df.loc["a"]`, `df.iloc[0]` |
| Boolean Indexing | Filter by condition | `df[df["A"] > 5]` |
| loc | Label-based indexer | `df.loc["row", "col"]` |
| iloc | Position-based indexer | `df.iloc[0, 1]` |
| query | Filter with string expression | `df.query("A > 5")` |
| isin | Match multiple values | `df[df["A"].isin([1,2,3])]` |
| between | Range filter | `df[df["A"].between(1,10)]` |
| where | Keep rows where True | `df.where(df["A"] > 5)` |
| mask | Replace rows where True | `df.mask(df["A"] > 5)` |
| nlargest | Top n rows by column | `df.nlargest(5, "A")` |
| nsmallest | Bottom n rows by column | `df.nsmallest(5, "A")` |
| & | AND condition | `(df["A"] > 5) & (df["B"] < 10)` |
| \| | OR condition | `(df["A"] > 5) \| (df["B"] < 10)` |
| ~ | NOT condition | `~(df["A"] > 5)` |

---

## Alphabetical Definitions

### B

**Between**
Filters rows where a column value falls within a range (inclusive).

```python
df[df["Age"].between(25, 35)]
```

**Boolean Indexing**
Filtering rows using a boolean mask (True/False conditions).

```python
df[df["Age"] > 30]
df[(df["Age"] > 25) & (df["Salary"] > 70000)]
```

### C

**Column Selection**
Selecting specific columns from a DataFrame.

```python
df["Name"]              # Single column (Series)
df[["Name", "Age"]]     # Multiple columns (DataFrame)
```

### I

**Iloc**
Position-based indexer — selects by integer position (0-indexed).

```python
df.iloc[0]              # First row
df.iloc[0:5]            # First 5 rows
df.iloc[0, 1]           # Row 0, column 1
```

**Isin**
Filters rows where a column value is in a list of values.

```python
df[df["City"].isin(["New York", "London"])]
```

### L

**Loc**
Label-based indexer — selects by index label.

```python
df.loc["emp1"]          # Row with label "emp1"
df.loc["emp1", "Name"]  # Row and column
df.loc["emp1":"emp3"]   # Slice (inclusive)
```

### M

**Mask**
Replaces rows with NaN where the condition is True (opposite of where).

```python
df.mask(df["Age"] > 30)
```

### N

**Nlargest**
Returns the top n rows by a column value.

```python
df.nlargest(5, "Sales")
```

**Nsmallest**
Returns the bottom n rows by a column value.

```python
df.nsmallest(3, "Price")
```

### Q

**Query**
Filters rows using a string expression.

```python
df.query("Age > 30 and Department == 'Engineering'")
df.query("Age > @min_age")  # Using variables
```

### R

**Row Selection**
Selecting specific rows from a DataFrame.

```python
df.loc["label"]         # By label
df.iloc[0]              # By position
df[condition]           # By boolean mask
```

### W

**Where**
Keeps rows where the condition is True; replaces others with NaN.

```python
df.where(df["Age"] > 30)
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

# Single column
print(df["Name"])

# Multiple columns
print(df[["Name", "Age"]])

# By position
print(df.iloc[:, 0])     # First column
print(df.iloc[:, 0:2])   # First two columns
```

### Example 2: Boolean Filtering

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "Salary": [75000, 82000, 95000, 68000]
})

# Simple filter
print(df[df["Age"] > 30])

# Multiple conditions
print(df[(df["Age"] > 30) & (df["Salary"] > 70000)])

# Using isin
print(df[df["Name"].isin(["Alice", "Charlie"])])
```

### Example 3: loc and iloc

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42]
}, index=["emp1", "emp2", "emp3"])

# loc — label-based
print(df.loc["emp2"])
print(df.loc["emp1":"emp3"])
print(df.loc["emp2", "Name"])

# iloc — position-based
print(df.iloc[1])
print(df.iloc[0:2])
print(df.iloc[1, 0])
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| loc | DataFrame | Label-based selection |
| iloc | DataFrame | Position-based selection |
| Boolean Indexing | DataFrame | Filter by condition |
| query | DataFrame | String-based filtering |
| isin | Series | Match multiple values |
| between | Series | Range filtering |
| where | DataFrame | Conditional replacement |
| nlargest | DataFrame | Top n rows |

---

## Selection Methods Comparison

```
[]:
  df["col"]            -> Column by name
  df[["col1","col2"]]  -> Multiple columns
  df[condition]        -> Boolean filtering

loc:
  df.loc[label]        -> Row by label
  df.loc[label, col]   -> Cell by label
  df.loc[start:end]    -> Slice (inclusive)

iloc:
  df.iloc[pos]         -> Row by position
  df.iloc[row, col]    -> Cell by position
  df.iloc[start:end]   -> Slice (exclusive)
```

---

## Operator Reference

```
&   -> AND (both conditions must be True)
|   -> OR  (at least one condition must be True)
~   -> NOT (inverts the condition)
==  -> Equal to
!=  -> Not equal to
>   -> Greater than
<   -> Less than
>=  -> Greater than or equal
<=  -> Less than or equal
```

---

## Self-Test Questions

1. What is the difference between `[]`, `loc`, and `iloc`?
2. How do you filter rows with multiple conditions?
3. What does `.query("Age > 30")` do?
4. How do you select the top 5 rows by a column value?
5. What is the difference between `.where()` and `.mask()`?
