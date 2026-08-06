# Glossary 09: Data loc and iloc

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| loc | Label-based indexer | `df.loc["row1"]` |
| iloc | Position-based indexer | `df.iloc[0]` |
| Label | Index value for rows | `df.loc["emp1"]` |
| Position | Integer position (0-indexed) | `df.iloc[0]` |
| Slice (loc) | Inclusive end | `df.loc["a":"c"]` |
| Slice (iloc) | Exclusive end | `df.iloc[0:3]` |
| Boolean Mask | True/False condition | `df.loc[df["A"] > 5]` |
| Cell Selection | Row and column | `df.loc["r", "c"]` |
| All Rows | Using colon | `df.loc[:, "col"]` |
| All Columns | Using colon | `df.loc["row", :]` |
| Negative Index | Count from end (iloc) | `df.iloc[-1]` |
| Setting Values | Modify with loc/iloc | `df.loc[mask, "col"] = val` |

---

## Alphabetical Definitions

### B

**Boolean Mask**
A Series of True/False values used to filter rows.

```python
mask = df["Age"] > 30
print(df.loc[mask])
```

### C

**Cell Selection**
Selecting a specific value at the intersection of a row and column.

```python
df.loc["emp1", "Name"]    # Label-based
df.iloc[0, 1]             # Position-based
```

### I

**Iloc**
Position-based indexer — selects by integer position (0-indexed).

```python
df.iloc[0]           # First row
df.iloc[0:5]         # First 5 rows (exclusive end)
df.iloc[0, 1]        # Row 0, column 1
```

**Index**
Labels for rows in a DataFrame.

```python
print(df.index)
# Index(['emp1', 'emp2', 'emp3'], dtype='object')
```

### L

**Label**
The index value that identifies a row.

```python
df.loc["emp1"]   # Selects row with label "emp1"
```

**Loc**
Label-based indexer — selects by index label.

```python
df.loc["emp1"]           # Row by label
df.loc["emp1":"emp3"]    # Slice (inclusive)
df.loc["emp1", "Name"]   # Cell by label
```

### N

**Negative Index**
Position from the end (only works with iloc).

```python
df.iloc[-1]    # Last row
df.iloc[-2:]   # Last 2 rows
```

### S

**Slice**
A range of rows or columns.

```python
# loc — inclusive end
df.loc["a":"c"]

# iloc — exclusive end
df.iloc[0:3]
```

**Setting Values**
Modifying DataFrame values using loc or iloc.

```python
df.loc[df["Age"] > 30, "Name"] = "Senior"
df.iloc[0, 1] = 29
```

---

## Code Examples

### Example 1: loc Basics

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42]
}, index=["emp1", "emp2", "emp3"])

# Single row
print(df.loc["emp1"])

# Multiple rows
print(df.loc[["emp1", "emp3"]])

# Slice
print(df.loc["emp1":"emp2"])

# Cell
print(df.loc["emp2", "Name"])
```

### Example 2: iloc Basics

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [28, 35, 42]
})

# Single row
print(df.iloc[0])

# Multiple rows
print(df.iloc[[0, 2]])

# Slice (exclusive)
print(df.iloc[0:2])

# Cell
print(df.iloc[1, 0])

# Negative
print(df.iloc[-1])
```

### Example 3: Boolean with loc

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 35, 42, 31],
    "Salary": [75000, 82000, 95000, 68000]
})

# Filter and select columns
print(df.loc[df["Age"] > 30, ["Name", "Salary"]])

# Set values
df.loc[df["Age"] > 30, "Name"] = "Senior"
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| loc | DataFrame | Label-based indexing |
| iloc | DataFrame | Position-based indexing |
| Index | DataFrame | Row labels |
| Position | iloc | Integer location |
| Slice | loc/iloc | Range selection |
| Boolean Mask | loc | Conditional filtering |
| Cell | loc/iloc | Single value |

---

## loc vs iloc Comparison

```
loc:
  - Label-based
  - Inclusive end in slices
  - Can use boolean masks
  - Can modify values
  - Works with index labels

iloc:
  - Position-based
  - Exclusive end in slices
  - Cannot use boolean masks directly
  - Can modify values
  - Works with integer positions only
```

---

## Slice Behavior

```
loc["a":"c"]   -> Includes "c" (inclusive)
iloc[0:3]      -> Excludes position 3 (exclusive)

Example:
  Index: ["a", "b", "c", "d"]
  
  loc["a":"c"]   -> ["a", "b", "c"]  (3 rows)
  iloc[0:3]      -> ["a", "b"]       (2 rows)
```

---

## Self-Test Questions

1. What is the difference between `loc` and `iloc`?
2. Is `loc` slice inclusive or exclusive?
3. How do you select a single cell?
4. How do you modify values using `loc`?
5. How do you select the last row using `iloc`?
