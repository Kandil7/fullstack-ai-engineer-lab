# Glossary: Set Operations (Lecture 28)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| unique() | `np.unique(arr)` | Find unique elements |
| intersect1d() | `np.intersect1d(a, b)` | Common elements |
| union1d() | `np.union1d(a, b)` | Combine without duplicates |
| setdiff1d() | `np.setdiff1d(a, b)` | Elements in A not in B |
| setxor1d() | `np.setxor1d(a, b)` | Elements in either, not both |
| isin() | `np.isin(arr, test)` | Check membership |
| in1d() | `np.in1d(arr, test)` | Check membership (deprecated) |
| return_counts | Parameter | Get counts with unique |
| return_index | Parameter | Get indices with unique |
| Symmetric Difference | XOR operation | Exclusive or |
| Intersection | AND operation | Common elements |
| Union | OR operation | All unique elements |

---

## Detailed Definitions

### Difference

**Definition:** Elements that are in one set but not in another. In set theory: A \ B = {x | x ∈ A and x ∉ B}.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([4, 5, 6, 7, 8])

print("A - B:", np.setdiff1d(a, b))  # [1 2 3]
print("B - A:", np.setdiff1d(b, a))  # [6 7 8]
```

**Related Terms:** Symmetric Difference, Complement

---

### Disjoint Sets

**Definition:** Two sets are disjoint if they have no elements in common. Their intersection is empty.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Check if disjoint
is_disjoint = len(np.intersect1d(a, b)) == 0
print("Are disjoint:", is_disjoint)  # True
```

**Related Terms:** Intersection, Empty Set

---

### Element Membership

**Definition:** Testing whether an element belongs to a set. In NumPy, done with `np.isin()`.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
test = np.array([2, 4, 6])

mask = np.isin(arr, test)
print("Membership:", mask)
# Output: [False True False True False]
```

**Related Terms:** isin(), in1d()

---

### in1d()

**Definition:** Tests whether each element of a 1D array is contained in another 1D array. Deprecated in favor of `np.isin()`.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
test = np.array([2, 4])

# Deprecated
mask = np.in1d(arr, test)
print("in1d:", mask)
# Output: [False True False True False]
```

**Related Terms:** isin(), Membership

---

### Intersection

**Definition:** Elements that are common to two or more sets. In set theory: A ∩ B = {x | x ∈ A and x ∈ B}.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([4, 5, 6, 7, 8])

print("Intersection:", np.intersect1d(a, b))
# Output: [4 5]
```

**Related Terms:** Union, Difference

---

### isin()

**Definition:** Tests whether each element of an array is contained in a test array. Returns a boolean array.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
test = np.array([2, 4, 6])

mask = np.isin(arr, test)
print("isin:", mask)
# Output: [False True False True False]

print("Matches:", arr[mask])
# Output: [2 4]
```

**Related Terms:** in1d(), Membership

---

### Membership

**Definition:** The relationship of an element belonging to a set. Tested using `np.isin()`.

**Example:**
```python
import numpy as np

products = np.array(["A", "B", "C", "D"])
available = np.array(["A", "C"])

is_member = np.isin(products, available)
print("Available:", products[is_member])
# Output: ['A' 'C']
```

**Related Terms:** isin(), Set

---

### Multiset

**Definition:** A collection that allows duplicate elements. NumPy arrays are multisets by default.

**Example:**
```python
import numpy as np

arr = np.array([1, 1, 2, 2, 3, 3])
unique, counts = np.unique(arr, return_counts=True)
print("Unique:", unique)
print("Counts:", counts)
# Output: [1 2 3], [2 2 2]
```

**Related Terms:** unique(), Duplicate

---

### return_counts

**Definition:** Parameter in `np.unique()` that returns the number of occurrences of each unique value.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 2, 3, 3, 3])
unique, counts = np.unique(arr, return_counts=True)
print("Unique:", unique)
print("Counts:", counts)
# Output: [1 2 3], [1 2 3]
```

**Related Terms:** unique(), return_index

---

### return_index

**Definition:** Parameter in `np.unique()` that returns the indices of the first occurrences of unique values.

**Example:**
```python
import numpy as np

arr = np.array([3, 1, 2, 1, 3, 2])
unique, indices = np.unique(arr, return_index=True)
print("Unique:", unique)
print("Indices:", indices)
# Output: [1 2 3], [1 2 0]
```

**Related Terms:** unique(), return_counts

---

### Set

**Definition:** A collection of distinct elements. In NumPy, represented by arrays with `np.unique()` to ensure distinctness.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 2, 3, 3, 3])
set_arr = np.unique(arr)
print("Set:", set_arr)
# Output: [1 2 3]
```

**Related Terms:** unique(), Distinct

---

### Symmetric Difference

**Definition:** Elements that are in either set but not in both. In set theory: A △ B = (A \ B) ∪ (B \ A).

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([4, 5, 6, 7, 8])

print("Symmetric difference:", np.setxor1d(a, b))
# Output: [1 2 3 6 7 8]
```

**Related Terms:** Union, Difference, XOR

---

### Union

**Definition:** All unique elements from two or more sets. In set theory: A ∪ B = {x | x ∈ A or x ∈ B}.

**Example:**
```python
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([3, 4, 5, 6])

print("Union:", np.union1d(a, b))
# Output: [1 2 3 4 5 6]
```

**Related Terms:** Intersection, Difference

---

### Union1d

**Definition:** Function that returns the unique union of two arrays. Elements are sorted and duplicates removed.

**Example:**
```python
import numpy import np

a = np.array([1, 2, 3])
b = np.array([2, 3, 4])

print("Union1d:", np.union1d(a, b))
# Output: [1 2 3 4]
```

**Related Terms:** union(), Union

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| Difference | In A but not B | `np.setdiff1d(A, B)` |
| Disjoint | No common elements | `len(intersect) == 0` |
| Element Membership | Belongs to set | `np.isin(arr, test)` |
| in1d() | Membership test (deprecated) | `np.in1d(arr, test)` |
| Intersection | Common elements | `np.intersect1d(A, B)` |
| isin() | Membership test | `np.isin(arr, test)` |
| Membership | Belonging relationship | `np.isin()` |
| Multiset | Allows duplicates | Original array |
| return_counts | Get occurrence counts | `np.unique(arr, return_counts=True)` |
| return_index | Get first indices | `np.unique(arr, return_index=True)` |
| Set | Distinct collection | `np.unique(arr)` |
| Symmetric Diff | In either, not both | `np.setxor1d(A, B)` |
| Union | All unique elements | `np.union1d(A, B)` |

---

**Back to Lecture:** [28 - Set Operations](28-ufunc-set-operations-lecture.md)
