# Lecture 20: Merge in Pandas

## Learning Objectives

By the end of this lecture, you will be able to:
- Perform inner, outer, left, and right merges
- Merge on single and multiple keys
- Handle merge conflicts with suffixes
- Use indicator and validate parameters
- Merge on index vs columns
- Troubleshoot common merge issues
- Choose the right merge type for your use case

---

## 1. Why Merge?

Data rarely lives in one table. Customer info is in one database, orders in another, products in a third. Merging combines DataFrames based on shared keys — similar to SQL JOIN operations.

---

## 2. Sample Data

```python
import pandas as pd

# Customers table
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'city': ['NYC', 'LA', 'NYC', 'Chicago', 'LA']
})

# Orders table
orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105],
    'customer_id': [1, 2, 2, 6, 7],
    'amount': [250, 180, 320, 95, 140]
})

print("Customers:")
print(customers)
print("\nOrders:")
print(orders)
```

---

## 3. Types of Merges

### 3.1 Inner Merge (Default)

Returns only rows with matching keys in BOTH DataFrames.

```python
inner = pd.merge(customers, orders, on='customer_id', how='inner')
print(inner)
#    customer_id   name   city  order_id  amount
# 0            1  Alice    NYC       101     250
# 1            2    Bob     LA       102     180
# 2            2    Bob     LA       103     320
# Note: customer_id 6,7 (no customer) and 4,5 (no orders) are excluded
```

### 3.2 Left Merge

Returns ALL rows from the left DataFrame, matching rows from the right (NaN where no match).

```python
left = pd.merge(customers, orders, on='customer_id', how='left')
print(left)
#    customer_id     name     city  order_id  amount
# 0            1    Alice      NYC     101.0   250.0
# 1            2      Bob       LA     102.0   180.0
# 2            2      Bob       LA     103.0   320.0
# 3            3  Charlie      NYC       NaN     NaN
# 4            4    Diana  Chicago       NaN     NaN
# 5            5      Eve       LA       NaN     NaN
```

### 3.3 Right Merge

Returns ALL rows from the right DataFrame, matching rows from the left.

```python
right = pd.merge(customers, orders, on='customer_id', how='right')
print(right)
#    customer_id   name   city  order_id  amount
# 0          1.0  Alice    NYC       101     250
# 1          2.0    Bob     LA       102     180
# 2          2.0    Bob     LA       103     320
# 3          6.0    NaN    NaN       104      95
# 4          7.0    NaN    NaN       105     140
```

### 3.4 Outer Merge

Returns ALL rows from BOTH DataFrames (NaN where no match).

```python
outer = pd.merge(customers, orders, on='customer_id', how='outer')
print(outer)
#    customer_id     name     city  order_id  amount
# 0            1    Alice      NYC     101.0   250.0
# 1            2      Bob       LA     102.0   180.0
# 2            2      Bob       LA     103.0   320.0
# 3            3  Charlie      NYC       NaN     NaN
# 4            4    Diana  Chicago       NaN     NaN
# 5            5      Eve       LA       NaN     NaN
# 6            6      NaN      NaN     104.0    95.0
# 7            7      NaN      NaN     105.0   140.0
```

---

## 4. Merge Visualization

```
Inner Join:          Left Join:           Outer Join:
  A ∩ B                A ∪ (A ∩ B)          A ∪ B
┌─────┐              ┌─────┐              ┌─────┐
│  A  │              │█████│              │█████│
│█████│              │█████│              │█████│
│  B  │              │  B  │              │█████│
└─────┘              └─────┘              └─────┘
```

---

## 5. Merging on Different Keys

### 5.1 Different Column Names

```python
# When the key column has different names
pd.merge(
    customers, orders,
    left_on='customer_id', right_on='customer_id',
    how='inner'
)

# If names differ:
pd.merge(
    df_customers, df_orders,
    left_on='cust_id', right_on='customer_id',
    how='inner'
)
```

### 5.2 Multiple Keys

```python
# Merge on multiple columns
pd.merge(
    df1, df2,
    on=['customer_id', 'date'],
    how='inner'
)

# Different names for multiple keys
pd.merge(
    df1, df2,
    left_on=['cust_id', 'order_date'],
    right_on=['customer_id', 'date'],
    how='left'
)
```

---

## 6. Suffixes for Overlapping Columns

```python
# When both DataFrames have columns with the same name (not the key)
products = pd.DataFrame({
    'product_id': [1, 2, 3],
    'name': ['Widget', 'Gadget', 'Doohickey'],
    'price': [25.00, 50.00, 15.00]
})

sales = pd.DataFrame({
    'product_id': [1, 2, 3],
    'name': ['Widget', 'Gadget', 'Doohickey'],
    'quantity': [100, 50, 200]
})

merged = pd.merge(products, sales, on='product_id')
print(merged.columns)
# Index(['product_id', 'name_x', 'price', 'name_y', 'quantity'], dtype='object')

# Custom suffixes
merged = pd.merge(products, sales, on='product_id', suffixes=('_product', '_sales'))
print(merged.columns)
# Index(['product_id', 'name_product', 'price', 'name_sales', 'quantity'], dtype='object')
```

---

## 7. Indicator Parameter

```python
# Shows which DataFrame each row came from
merged = pd.merge(
    customers, orders,
    on='customer_id',
    how='outer',
    indicator=True
)
print(merged['_merge'].value_counts())
# both          3
# left_only     3
# right_only    2
```

---

## 8. Validate Parameter

```python
# Check merge integrity
# one_to_one: Each key appears at most once in both DataFrames
pd.merge(df1, df2, on='id', validate='one_to_one')

# one_to_many: Each key appears at most once in left, many times in right
pd.merge(customers, orders, on='customer_id', validate='one_to_many')

# many_to_one: Each key appears many times in left, at most once in right
pd.merge(orders, customers, on='customer_id', validate='many_to_one')

# many_to_many: Default — no validation
pd.merge(df1, df2, on='id', validate='many_to_many')
```

---

## 9. Merging on Index

```python
# Set index and merge on index
customers_idx = customers.set_index('customer_id')
orders_idx = orders.set_index('customer_id')

merged = pd.merge(
    customers_idx, orders_idx,
    left_index=True, right_index=True,
    how='inner'
)

# Or merge column on index
merged = pd.merge(
    customers, orders_idx,
    left_on='customer_id', right_index=True,
    how='inner'
)
```

---

## 10. Common Mistakes

1. **Forgetting `how` parameter** — Default is inner; you may lose rows unintentionally.
2. **Duplicate keys cause row explosion** — If both sides have duplicates, you get a cartesian product.
3. **Not checking for duplicates before merge** — Always `df.duplicated(subset=[key]).sum()` first.
4. **Merging on wrong columns** — Verify column names match exactly (case-sensitive).
5. **Ignoring suffixes** — Overlapping column names create `_x` and `_y` suffixes silently.

---

## 11. Best Practices

1. **Check shape before and after** — `print(df.shape)` to verify merge didn't explode or shrink unexpectedly.
2. **Use `validate=` parameter** — Catches data integrity issues early.
3. **Use `indicator=True`** — Helps debug which rows matched.
4. **Merge on the smaller DataFrame first** — For performance.
5. **Document merge logic** — Future you will forget why you did a left vs inner join.

---

## 12. Exercises

### Exercise 1: Basic Merge
Given a `students` DataFrame and a `grades` DataFrame, perform an inner merge on `student_id`. Then do a left merge and count how many students have no grades.

### Exercise 2: Multi-Key Merge
Merge two DataFrames on both `product_id` and `region`. Handle overlapping column names with custom suffixes.

### Exercise 3: Integrity Check
Before merging, check for duplicates in the key column. Merge with `validate='one_to_many'` and handle any validation errors.

---

## 13. Summary

| Merge Type | Rows Included | Use Case |
|-----------|--------------|----------|
| `inner` | Only matching rows | Default, safest |
| `left` | All left + matching right | Keep all primary records |
| `right` | All right + matching left | Keep all secondary records |
| `outer` | All rows from both | Complete union |

**Key takeaway**: Merging is the primary way to combine related DataFrames. Always verify merge results by checking shapes and using `indicator=True`.

---

*Next: [21 – Concat](21-concat-lecture.md)*
