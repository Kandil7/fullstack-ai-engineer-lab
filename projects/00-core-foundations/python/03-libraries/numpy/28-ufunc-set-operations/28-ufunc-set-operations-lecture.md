# Lecture 28: Set Operations in NumPy

## Topic Overview

Set operations are essential for finding common elements, unique values, and performing logical comparisons between arrays. NumPy provides comprehensive set operations: `np.unique()` for finding unique elements, `np.intersect1d()` for intersections, `np.union1d()` for unions, `np.setdiff1d()` for differences, and `np.setxor1d()` for symmetric differences. These operations are crucial for data analysis, data cleaning, and comparing datasets.

Understanding set operations helps you efficiently compare datasets, find duplicates, merge categories, and perform logical operations on array data.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `np.unique()` to find unique elements with counts and indices
2. Use `np.intersect1d()` to find common elements between arrays
3. Use `np.union1d()` to combine arrays without duplicates
4. Use `np.setdiff1d()` to find elements in one array but not another
5. Use `np.setxor1d()` for symmetric difference
6. Use `np.isin()` to check element membership
7. Apply set operations to data analysis scenarios
8. Work with string arrays using set operations
9. Handle 2D arrays with set operations
10. Combine multiple set operations for complex queries

---

## Key Concepts

### 1. unique()

```python
import numpy as np

arr = np.array([1, 2, 3, 2, 4, 3, 5, 1, 6, 5])
print("Original:", arr)

# Get unique values
unique_vals = np.unique(arr)
print("Unique:", unique_vals)  # [1 2 3 4 5 6]

# Get unique values and counts
unique_vals, counts = np.unique(arr, return_counts=True)
print("\nUnique with counts:")
for val, count in zip(unique_vals, counts):
    print(f"  {val}: {count}")

# Get unique with indices
unique_vals, indices = np.unique(arr, return_index=True)
print("\nUnique with first indices:", dict(zip(unique_vals, indices)))

# 2D unique
arr2d = np.array([[1, 2, 1], [2, 3, 2], [1, 2, 3]])
unique_2d = np.unique(arr2d)
print("\n2D unique:", unique_2d)

# Unique along axis
unique_rows = np.unique(arr2d, axis=0)
print("Unique rows:\n", unique_rows)
```

### 2. intersect1d()

```python
import numpy as np

arr1 = np.array([1, 2, 3, 4, 5, 6])
arr2 = np.array([4, 5, 6, 7, 8, 9])

# Basic intersection
common = np.intersect1d(arr1, arr2)
print("\nIntersection:", common)  # [4 5 6]

# Intersection with indices
common, idx1, idx2 = np.intersect1d(arr1, arr2, return_indices=True)
print("Common values:", common)
print("Indices in arr1:", idx1)  # [3 4 5]
print("Indices in arr2:", idx2)  # [0 1 2]

# Multiple arrays
arr3 = np.array([5, 6, 7, 10])
common_all = np.intersect1d(arr1, arr2, arr3)
print("\nCommon in all 3:", common_all)  # [5 6]

# Practical: find common customers
customers_a = np.array(["Alice", "Bob", "Charlie", "David"])
customers_b = np.array(["Bob", "David", "Eve", "Frank"])
common_customers = np.intersect1d(customers_a, customers_b)
print(f"\nCommon customers: {common_customers}")
```

### 3. union1d()

```python
import numpy as np

arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([3, 4, 5, 6])

# Basic union (removes duplicates)
union = np.union1d(arr1, arr2)
print("\nUnion:", union)  # [1 2 3 4 5 6]

# Practical: merge unique categories
cat_a = np.array(["electronics", "clothing", "food"])
cat_b = np.array(["clothing", "furniture", "electronics", "toys"])
all_categories = np.union1d(cat_a, cat_b)
print(f"All categories: {all_categories}")

# Union of multiple arrays
arr3 = np.array([6, 7, 8])
union_all = np.union1d(np.union1d(arr1, arr2), arr3)
print(f"Union of 3 arrays: {union_all}")
```

### 4. setdiff1d() and setxor1d()

```python
import numpy as np

arr1 = np.array([1, 2, 3, 4, 5, 6])
arr2 = np.array([4, 5, 6, 7, 8, 9])

# setdiff1d: elements in arr1 but NOT in arr2
diff = np.setdiff1d(arr1, arr2)
print("\nDifference (arr1 - arr2):", diff)  # [1 2 3]

# Reverse difference
diff_rev = np.setdiff1d(arr2, arr1)
print("Difference (arr2 - arr1):", diff_rev)  # [7 8 9]

# setxor1d: elements in either but NOT in both
sym_diff = np.setxor1d(arr1, arr2)
print("Symmetric difference:", sym_diff)  # [1 2 3 7 8 9]

# Practical: find unique to each group
team_a = np.array(["Alice", "Bob", "Charlie"])
team_b = np.array(["Bob", "David", "Charlie"])
only_a = np.setdiff1d(team_a, team_b)
only_b = np.setdiff1d(team_b, team_a)
print(f"\nOnly in team A: {only_a}")
print(f"Only in team B: {only_b}")
print(f"Unique to each: {np.setxor1d(team_a, team_b)}")
```

### 5. in1d() and isin()

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
test_values = np.array([2, 5, 11])

# in1d (deprecated, use isin)
mask = np.in1d(arr, test_values)
print("\nin1d:", mask)  # [False True False False True False False False False False]
print("Matches:", arr[mask])  # [2 5]

# isin (modern version)
mask = np.isin(arr, test_values)
print("\nisin:", mask)

# 2D membership
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
mask = np.isin(arr2d, [2, 5, 8])
print("\n2D isin:\n", mask)
print("Matching values:", arr2d[mask])  # [2 5 8]

# Practical: filter by category
categories = np.array(["A", "B", "C", "A", "D", "B", "E"])
valid_categories = np.array(["A", "B", "C"])
mask = np.isin(categories, valid_categories)
print(f"\nCategories: {categories}")
print(f"Valid: {categories[mask]}")

# Count occurrences of test values
arr = np.array([1, 2, 3, 2, 4, 2, 5, 3])
test = np.array([2, 3])
counts = np.array([np.sum(arr == val) for val in test])
print(f"\nTest values: {test}")
print(f"Counts: {counts}")
```

---

## Code Examples with Explanations

### Example 1: Data Cleaning with Unique

```python
import numpy as np

# Messy data with duplicates and variations
raw_data = np.array(["apple", "Apple", "banana", "BANANA", "apple", "cherry"])

# Normalize and find unique
normalized = np.char.lower(raw_data)
unique_fruits = np.unique(normalized)

print("Raw data:", raw_data)
print("Unique (normalized):", unique_fruits)

# Count occurrences
unique, counts = np.unique(normalized, return_counts=True)
print("\nCounts:")
for fruit, count in zip(unique, counts):
    print(f"  {fruit}: {count}")
```

### Example 2: Comparing Datasets

```python
import numpy as np

# Two customer lists
customers_2023 = np.array(["Alice", "Bob", "Charlie", "David", "Eve"])
customers_2024 = np.array(["Bob", "David", "Frank", "Grace", "Alice"])

# Find common customers (retained)
retained = np.intersect1d(customers_2023, customers_2024)
print("Retained customers:", retained)

# Find churned customers
churned = np.setdiff1d(customers_2023, customers_2024)
print("Churned customers:", churned)

# Find new customers
new = np.setdiff1d(customers_2024, customers_2023)
print("New customers:", new)

# All unique customers
all_customers = np.union1d(customers_2023, customers_2024)
print("All unique customers:", all_customers)
```

### Example 3: Product Category Analysis

```python
import numpy as np

# Products from different stores
store_a = np.array(["electronics", "clothing", "food", "toys"])
store_b = np.array(["clothing", "furniture", "electronics", "books"])
store_c = np.array(["food", "toys", "books", "electronics"])

# Categories in all stores
common = np.intersect1d(np.intersect1d(store_a, store_b), store_c)
print("Categories in all stores:", common)

# Categories unique to each store
unique_a = np.setdiff1d(store_a, np.union1d(store_b, store_c))
unique_b = np.setdiff1d(store_b, np.union1d(store_a, store_c))
unique_c = np.setdiff1d(store_c, np.union1d(store_a, store_b))

print("\nUnique to each store:")
print(f"  Store A: {unique_a}")
print(f"  Store B: {unique_b}")
print(f"  Store C: {unique_c}")

# All categories
all_cats = np.union1d(np.union1d(store_a, store_b), store_c)
print(f"\nAll categories: {all_cats}")
```

### Example 4: Member Tracking System

```python
import numpy as np

# Membership data
current_members = np.array([101, 102, 103, 104, 105])
new_signups = np.array([103, 106, 107, 108])
cancelled = np.array([102, 104])

# Update membership
still_members = np.setdiff1d(current_members, cancelled)
final_members = np.union1d(still_members, new_signups)

print("Current members:", current_members)
print("New signups:", new_signups)
print("Cancelled:", cancelled)
print("Final members:", final_members)

# Check specific membership
is_member = np.isin([101, 103, 106, 109], final_members)
print("\nMembership status:", is_member)
```

### Example 5: Data Validation

```python
import numpy as np

# Valid values for a field
valid_values = np.array(["A", "B", "C", "D", "E"])

# Incoming data (may contain invalid values)
incoming_data = np.array(["A", "B", "X", "C", "Y", "D", "Z"])

# Check validity
is_valid = np.isin(incoming_data, valid_values)
valid_data = incoming_data[is_valid]
invalid_data = incoming_data[~is_valid]

print("Incoming data:", incoming_data)
print("Valid entries:", valid_data)
print("Invalid entries:", invalid_data)

# Get all unique values
all_values = np.union1d(incoming_data, valid_values)
print("All unique values:", all_values)
```

---

## Common Mistakes to Avoid

### Mistake 1: Assuming Order is Preserved

```python
import numpy as np

arr1 = np.array([3, 1, 2])
arr2 = np.array([2, 3, 1])

# Result is sorted, not in original order
print("Union:", np.union1d(arr1, arr2))  # [1 2 3]
print("Intersection:", np.intersect1d(arr1, arr2))  # [1 2 3]
```

### Mistake 2: Not Handling Duplicates

```python
import numpy as np

arr = np.array([1, 1, 2, 2, 3, 3])

# unique removes duplicates
print("Unique:", np.unique(arr))  # [1 2 3]

# If you need to keep duplicates, don't use unique
print("Original:", arr)
```

### Mistake 3: Forgetting 1D Requirement

```python
import numpy import np

# Most set operations require 1D arrays
arr2d = np.array([[1, 2], [3, 4]])

# WRONG - This flattens the array
# np.intersect1d(arr2d, other)  # Flattens to 1D

# CORRECT - Flatten first if needed
flat = arr2d.flatten()
```

---

## Best Practices

### 1. Use isin Instead of in1d

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
test = np.array([2, 4])

# Recommended
mask = np.isin(arr, test)

# Deprecated
# mask = np.in1d(arr, test)
```

### 2. Return Indices When Needed

```python
import numpy as np

arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([4, 5, 6, 7, 8])

# Get indices along with intersection
common, idx1, idx2 = np.intersect1d(arr1, arr2, return_indices=True)
print("Common:", common)
print("Indices in arr1:", idx1)
print("Indices in arr2:", idx2)
```

### 3. Chain Operations for Complex Queries

```python
import numpy as np

# Find elements in A but not in B or C
A = np.array([1, 2, 3, 4, 5])
B = np.array([2, 3])
C = np.array([4, 5])

result = np.setdiff1d(A, np.union1d(B, C))
print("In A but not in B or C:", result)  # [1]
```

---

## Practice Exercises

### Exercise 1: Finding Unique Elements

```python
import numpy as np

arr = np.array([5, 3, 5, 2, 3, 1, 4, 2, 5, 3])

# TODO: Find unique values
unique_vals = np.unique(arr)
print("Unique:", unique_vals)

# TODO: Find unique values with counts
unique_vals, counts = np.unique(arr, return_counts=True)
print("Counts:", dict(zip(unique_vals, counts)))
```

### Exercise 2: Set Comparisons

```python
import numpy as np

set_a = np.array([1, 2, 3, 4, 5])
set_b = np.array([4, 5, 6, 7, 8])

# TODO: Find intersection
intersection = np.intersect1d(set_a, set_b)
print("Intersection:", intersection)

# TODO: Find union
union = np.union1d(set_a, set_b)
print("Union:", union)

# TODO: Find difference (A - B)
diff = np.setdiff1d(set_a, set_b)
print("A - B:", diff)
```

### Exercise 3: Membership Testing

```python
import numpy as np

products = np.array(["A", "B", "C", "D", "E"])
available = np.array(["A", "C", "E"])

# TODO: Check which products are available
is_available = np.isin(products, available)
print("Available mask:", is_available)
print("Available:", products[is_available])
```

---

## Summary

| Function | Description |
|----------|-------------|
| **np.unique()** | Find unique elements |
| **np.intersect1d()** | Find common elements |
| **np.union1d()** | Combine without duplicates |
| **np.setdiff1d()** | Elements in A but not B |
| **np.setxor1d()** | Elements in either but not both |
| **np.isin()** | Check membership |

---

## Quick Reference

```python
import numpy as np

# Unique elements
unique, counts = np.unique(arr, return_counts=True)

# Intersection (AND)
common = np.intersect1d(arr1, arr2)

# Union (OR)
combined = np.union1d(arr1, arr2)

# Difference (A - B)
diff = np.setdiff1d(arr1, arr2)

# Symmetric difference (XOR)
sym_diff = np.setxor1d(arr1, arr2)

# Membership testing
mask = np.isin(arr, test_values)
```

---

**Congratulations!** You've completed all 28 NumPy lectures!
