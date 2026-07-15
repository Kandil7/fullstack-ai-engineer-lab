# Glossary 11: Rename Columns

## Quick Reference

| Term | Definition | Example |
|---|---|---|
| rename | Change column/index labels | `df.rename(columns={...})` |
| columns | Column labels attribute | `df.columns` |
| str.lower | Lowercase strings | `df.columns.str.lower()` |
| str.replace | Replace substrings | `df.columns.str.replace(" ", "_")` |
| str.strip | Remove whitespace | `df.columns.str.strip()` |
| inplace | Modify original DataFrame | `df.rename(inplace=True)` |
| MultiIndex | Multi-level column index | `pd.MultiIndex.from_arrays(...)` |
| prefix | Add prefix to columns | `df.add_prefix("col_")` |
| suffix | Add suffix to columns | `df.add_suffix("_col")` |

---

## Alphabetical Definitions

### A

**Add Prefix**
Adds a prefix to all column names.

```python
df = df.add_prefix("data_")
# A -> data_A, B -> data_B
```

**Add Suffix**
Adds a suffix to all column names.

```python
df = df.add_suffix("_2024")
# A -> A_2024, B -> B_2024
```

### C

**Columns**
The vertical labels of a DataFrame.

```python
print(df.columns)
# Index(['Name', 'Age', 'City'], dtype='object')
```

### I

**Inplace**
When True, modifies the original DataFrame instead of returning a new one.

```python
df.rename(columns={"A": "Alpha"}, inplace=True)
```

### M

**MultiIndex**
A multi-level index for rows or columns.

```python
arrays = [["A", "A", "B"], ["one", "two", "one"]]
columns = pd.MultiIndex.from_arrays(arrays)
```

### R

**Rename**
Changes column or index labels.

```python
df.rename(columns={"old": "new"})
df.rename(index={0: "first"})
df.rename(columns=lambda x: x.lower())
```

### S

**Str Methods**
String methods for bulk operations on column names.

```python
df.columns.str.lower()
df.columns.str.upper()
df.columns.str.replace(" ", "_")
df.columns.str.strip()
df.columns.str.contains("pattern")
```

---

## Code Examples

### Example 1: Basic Rename

```python
import pandas as pd

df = pd.DataFrame({
    "First Name": ["Alice", "Bob"],
    "Last Name": ["Smith", "Jones"],
    "Age Yrs": [28, 35]
})

# Rename specific columns
df_renamed = df.rename(columns={
    "First Name": "first_name",
    "Last Name": "last_name",
    "Age Yrs": "age"
})
```

### Example 2: Bulk Rename

```python
import pandas as pd

df = pd.DataFrame({
    "Column A": [1, 2],
    "Column B": [3, 4],
    "Column C": [5, 6]
})

# Lowercase and replace spaces
df.columns = df.columns.str.lower().str.replace(" ", "_")
```

### Example 3: Clean Pipeline

```python
import pandas as pd

def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df
```

---

## Related Terms

| Term | Related To | Relationship |
|---|---|---|
| rename | DataFrame | Change labels |
| columns | DataFrame | Column labels |
| index | DataFrame | Row labels |
| str methods | Series | String operations |
| MultiIndex | DataFrame | Multi-level columns |

---

## String Methods Reference

```
str.lower()      -> Lowercase
str.upper()      -> Uppercase
str.title()      -> Title case
str.strip()      -> Remove whitespace
str.replace(a,b) -> Replace substring
str.contains(p)  -> Check if contains pattern
str.split(d)     -> Split by delimiter
str.len()        -> String length
str.cat()        -> Concatenate strings
str.startswith(p) -> Check start
str.endswith(p)   -> Check end
```

---

## Self-Test Questions

1. How do you rename a single column?
2. How do you lowercase all column names?
3. How do you replace spaces with underscores?
4. What is the difference between `rename()` and direct assignment?
5. How do you add a prefix to all columns?
