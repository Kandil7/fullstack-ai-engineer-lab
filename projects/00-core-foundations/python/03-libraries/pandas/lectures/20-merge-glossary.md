# Glossary 20: Merge

## Quick Reference

| Method / Function | Purpose | Returns |
|-------------------|---------|---------|
| `pd.merge()` | SQL-style join | DataFrame |
| `how='inner'` | Only matching rows (default) | — |
| `how='left'` | All left + matching right | — |
| `how='right'` | All right + matching left | — |
| `how='outer'` | All rows from both | — |
| `on='col'` | Merge key (same name in both) | — |
| `left_on` / `right_on` | Different key column names | — |
| `left_index` / `right_index` | Merge on index | — |
| `suffixes` | Handle overlapping columns | tuple |
| `indicator=True` | Show merge source | column |
| `validate` | Check merge integrity | str |

---

## Alphabetical Definitions

### D

**Duplicate Keys**
When the merge key has duplicate values in one or both DataFrames. Causes row explosion (cartesian product) if both sides have duplicates.
```python
# Check before merging
print(f"Duplicates: {df['key'].duplicated().sum()}")
```

### I

**Inner Join**
Returns only rows where the key exists in both DataFrames. Excludes non-matching rows from either side.
```python
pd.merge(df1, df2, on='key', how='inner')  # Default
```

**Indicator**
Adds a `_merge` column showing whether each row came from left_only, right_only, or both.
```python
merged = pd.merge(df1, df2, on='key', how='outer', indicator=True)
print(merged['_merge'].value_counts())
```

### L

**Left Join**
Returns all rows from the left DataFrame. Matching right rows are included; non-matching get NaN.
```python
pd.merge(customers, orders, on='customer_id', how='left')
```

**left_on / right_on**
Specify different column names to merge on when the key columns don't have the same name.
```python
pd.merge(df1, df2, left_on='cust_id', right_on='customer_id')
```

**left_index / right_index**
Merge on the DataFrame index instead of a column.
```python
pd.merge(df1, df2, left_index=True, right_on='id')
```

### M

**Many-to-Many**
Both sides have duplicate keys. Creates a cartesian product. Use `validate='many_to_many'` to allow.
```python
pd.merge(df1, df2, on='key', validate='many_to_many')
```

**Many-to-One / One-to-Many**
One side has unique keys, the other has duplicates. Most common in practice (e.g., customers → orders).
```python
pd.merge(customers, orders, on='id', validate='one_to_many')
```

**merge()**
The primary function for combining DataFrames based on shared keys. Equivalent to SQL JOIN.
```python
pd.merge(df1, df2, on='key', how='inner')
```

### O

**One-to-One**
Both sides have unique keys. Simplest merge type.
```python
pd.merge(df1, df2, on='id', validate='one_to_one')
```

**Outer Join**
Returns all rows from both DataFrames. NaN fills in where there's no match.
```python
pd.merge(df1, df2, on='key', how='outer')
```

### R

**Right Join**
Returns all rows from the right DataFrame. Matching left rows are included; non-matching get NaN.
```python
pd.merge(df1, df2, on='key', how='right')
```

### S

**Suffixes**
Tuple of strings appended to overlapping column names. Default is `('_x', '_y')`.
```python
pd.merge(df1, df2, on='key', suffixes=('_left', '_right'))
```

### V

**validate**
Checks merge key integrity before performing the merge. Raises error if condition is violated.
```python
pd.merge(df1, df2, on='key', validate='one_to_many')
# Options: 'one_to_one', 'one_to_many', 'many_to_one', 'many_to_many'
```

---

## Code Examples

### Example 1: Complete Merge Workflow

```python
import pandas as pd

# Create sample data
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'email': ['alice@mail.com', 'bob@mail.com', 'charlie@mail.com', 'diana@mail.com']
})

orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105],
    'customer_id': [1, 2, 2, 5, 6],
    'product': ['Laptop', 'Phone', 'Tablet', 'Watch', 'Camera'],
    'amount': [1200, 800, 400, 250, 600]
})

# Step 1: Check duplicates
print(f"Customer duplicates: {customers['customer_id'].duplicated().sum()}")
print(f"Order customer duplicates: {orders['customer_id'].duplicated().sum()}")

# Step 2: Inner merge (only matching)
inner = pd.merge(customers, orders, on='customer_id', how='inner', validate='one_to_many')
print(f"\nInner merge shape: {inner.shape}")

# Step 3: Left merge (all customers)
left = pd.merge(customers, orders, on='customer_id', how='left')
print(f"Left merge shape: {left.shape}")
print(f"Customers without orders: {left['order_id'].isna().sum()}")

# Step 4: Indicator merge
outer = pd.merge(customers, orders, on='customer_id', how='outer', indicator=True)
print(f"\nMerge indicator:\n{outer['_merge'].value_counts()}")
```

### Example 2: Multi-Key Merge with Suffixes

```python
# Product sales data with overlapping column names
products = pd.DataFrame({
    'product_id': [1, 2, 3],
    'category': ['Electronics', 'Clothing', 'Food'],
    'price': [99.99, 49.99, 9.99]
})

product_sales = pd.DataFrame({
    'product_id': [1, 2, 3],
    'category': ['Electronics', 'Clothing', 'Food'],
    'units_sold': [150, 300, 500]
})

# Merge with custom suffixes
merged = pd.merge(
    products, product_sales,
    on='product_id',
    suffixes=('_catalog', '_sales')
)
print(merged)
#    product_id category_catalog  price category_sales  units_sold
# 0           1      Electronics  99.99    Electronics         150
# 1           2         Clothing  49.99       Clothing         300
# 2           3             Food   9.99           Food         500
```

### Example 3: Cascading Merges

```python
# Multiple related tables
departments = pd.DataFrame({
    'dept_id': [1, 2, 3],
    'dept_name': ['Engineering', 'Sales', 'HR']
})

employees = pd.DataFrame({
    'emp_id': [101, 102, 103, 104],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'dept_id': [1, 1, 2, 3]
})

salaries = pd.DataFrame({
    'emp_id': [101, 102, 103, 104],
    'salary': [120000, 110000, 95000, 90000]
})

# Cascade: departments → employees → salaries
result = (employees
    .merge(departments, on='dept_id', how='left')
    .merge(salaries, on='emp_id', how='left')
)
print(result)
#    emp_id     name  dept_id   dept_name  salary
# 0     101    Alice        1  Engineering  120000
# 1     102      Bob        1  Engineering  110000
# 2     103  Charlie        2       Sales    95000
# 3     104    Diana        3          HR    90000
```

---

## Related Terms

| Term | Related To | Connection |
|------|-----------|------------|
| `how` | Join type | inner/left/right/outer |
| `on` | Key column | Shared column name |
| `suffixes` | Overlapping columns | Name collision handling |
| `indicator` | Debugging | Shows merge source |
| `validate` | Data integrity | Key uniqueness check |
| `concat()` | Stacking | Vertical/horizontal append (no keys) |
| `join()` | Index merge | Merge on index (method) |

---

*See also: [Lecture 20](20-merge-lecture.md) | [Lecture 21 – Concat](21-concat-lecture.md)*
