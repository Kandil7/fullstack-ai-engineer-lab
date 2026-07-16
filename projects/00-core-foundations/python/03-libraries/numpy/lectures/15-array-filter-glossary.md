# Glossary: Array Filtering in NumPy (Lecture 15)

## Quick Reference Table

| Term | Function | Description |
|------|----------|-------------|
| Boolean Mask | `arr > value` | Array of True/False from comparisons |
| Boolean Indexing | `arr[mask]` | Select elements where mask is True |
| np.where() | `np.where(cond, x, y)` | Conditional element selection |
| np.extract() | `np.extract(cond, arr)` | Extract matching elements |
| np.clip() | `np.clip(arr, min, max)` | Limit values to range |
| Fancy Indexing | `arr[indices]` | Select by index array |
| Masked Array | `np.ma.masked_where()` | Array with masked values |
| np.isin() | `np.isin(arr, test)` | Check membership |
| np.all() | `np.all(condition)` | Check if all elements True |
| np.any() | `np.any(condition)` | Check if any element True |

---

## Detailed Definitions

### AND Operator (`&`)

**Definition:** Bitwise AND operator used to combine two boolean conditions. Both conditions must be True for the result to be True.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Elements greater than 3 AND less than 8
filtered = arr[(arr > 3) & (arr < 8)]
print(filtered)
# Output: [4 5 6 7]
```

**Related Terms:** OR (`|`), NOT (`~`), Boolean Mask

---

### Boolean Indexing

**Definition:** A method of selecting array elements using a boolean array (mask) of the same shape. Elements at positions where the mask is True are selected.

**Example:**
```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])
mask = np.array([True, False, True, False, True])

# Select elements where mask is True
filtered = arr[mask]
print(filtered)
# Output: [10 30 50]

# Direct boolean indexing
filtered = arr[arr > 25]
print(filtered)
# Output: [30 40 50]
```

**Related Terms:** Boolean Mask, Fancy Indexing, np.where()

---

### Boolean Mask

**Definition:** An array of boolean (True/False) values produced by applying comparison operators to NumPy arrays. Has the same shape as the original array.

**Example:**
```python
import numpy as np

arr = np.array([1, 5, 10, 15, 20])

# Create boolean mask
mask = arr > 8
print(mask)
# Output: [False False  True  True  True]

print("Shape matches:", arr.shape == mask.shape)
# Output: Shape matches: True
```

**Related Terms:** Boolean Indexing, Comparison Operators, np.where()

---

### Clip

**Definition:** A function that limits array values to a specified range. Values below `min` become `min`, values above `max` become `max`.

**Example:**
```python
import numpy as np

arr = np.array([-5, 0, 10, 50, 100, 150])

# Clip to range [0, 100]
clipped = np.clip(arr, 0, 100)
print(clipped)
# Output: [  0   0  10  50 100 100]
```

**Related Terms:** np.where(), Comparison Operators

---

### Comparison Operators

**Definition:** Operators that compare array elements element-wise and return boolean arrays. Includes `>`, `<`, `>=`, `<=`, `==`, `!=`.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print(arr > 3)      # [False False False  True  True]
print(arr <= 2)     # [ True  True False False False]
print(arr == 3)     # [False False  True False False]
print(arr != 4)     # [ True  True  True False  True]
```

**Related Terms:** Boolean Mask, Boolean Indexing

---

### Fancy Indexing

**Definition:** A method of selecting array elements using integer arrays as indices. Allows non-contiguous element selection.

**Example:**
```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50, 60])

# Select elements at indices 0, 2, 4
indices = np.array([0, 2, 4])
result = arr[indices]
print(result)
# Output: [10 30 50]

# 2D fancy indexing
arr2d = np.array([[1, 2], [3, 4], [5, 6]])
rows = np.array([0, 2])
cols = np.array([1, 0])
print(arr2d[rows, cols])
# Output: [2 5]
```

**Related Terms:** Boolean Indexing, Integer Array Indexing

---

### Masked Array

**Definition:** A special NumPy array type that allows marking certain elements as invalid or missing. Created using `np.ma` module.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Create masked array (mask elements > 3)
masked = np.ma.masked_where(arr > 3, arr)
print(masked)
# Output: [1 2 3 -- --]

# Get unmasked values
print(masked.compressed())
# Output: [1 2 3]
```

**Related Terms:** Boolean Mask, np.where()

---

### np.all()

**Definition:** Tests whether all elements along an axis evaluate to True. Returns a single boolean value.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Check if all elements are positive
print(np.all(arr > 0))
# Output: True

# Check if all elements in a row are positive
arr2d = np.array([[1, 2], [3, -4]])
print(np.all(arr2d > 0, axis=1))
# Output: [ True False]
```

**Related Terms:** np.any(), Boolean Mask

---

### np.any()

**Definition:** Tests whether any element along an axis evaluates to True. Returns a single boolean value.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Check if any element is greater than 4
print(np.any(arr > 4))
# Output: True

# Check if any element in each row is negative
arr2d = np.array([[1, 2], [-3, 4]])
print(np.any(arr2d < 0, axis=1))
# Output: [False  True]
```

**Related Terms:** np.all(), Boolean Mask

---

### np.extract()

**Definition:** Extracts elements from an array that satisfy a given condition. Always returns a flattened 1D array.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Extract elements greater than 5
extracted = np.extract(arr > 5, arr)
print(extracted)
# Output: [ 6  7  8  9 10]

# Complex condition
mask = (arr % 3 == 0) & (arr > 4)
extracted = np.extract(mask, arr)
print(extracted)
# Output: [6 9]
```

**Related Terms:** Boolean Indexing, np.where()

---

### np.isin()

**Definition:** Tests whether each element of an array is contained in a test array. Returns a boolean array of the same shape.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
test_values = np.array([2, 5, 11])

# Check membership
mask = np.isin(arr, test_values)
print(mask)
# Output: [False  True False False  True False False False False False]

# Get matching elements
print(arr[mask])
# Output: [2 5]
```

**Related Terms:** Boolean Mask, np.in1d()

---

### np.where()

**Definition:** Returns elements chosen from `x` or `y` based on condition. Can also return indices where condition is True.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Get indices where condition is True
indices = np.where(arr > 3)
print(indices)
# Output: (array([3, 4]),)

# Conditional replacement
result = np.where(arr > 3, arr * 10, arr)
print(result)
# Output: [ 1  2  3 40 50]
```

**Related Terms:** Boolean Indexing, np.extract()

---

### NOT Operator (`~`)

**Definition:** Bitwise NOT operator that negates a boolean condition. Flips True to False and vice versa.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Elements NOT greater than 3
filtered = arr[~(arr > 3)]
print(filtered)
# Output: [1 2 3]
```

**Related Terms:** AND (`&`), OR (`|`), Boolean Mask

---

### OR Operator (`|`)

**Definition:** Bitwise OR operator used to combine two boolean conditions. Either condition can be True for the result to be True.

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Elements less than 3 OR greater than 7
filtered = arr[(arr < 3) | (arr > 7)]
print(filtered)
# Output: [ 1  2  8  9 10]
```

**Related Terms:** AND (`&`), NOT (`~`), Boolean Mask

---

### np.clip()

**Definition:** Limits array values to a specified range. Values below min become min, values above max become max.

**Example:**
```python
import numpy as np

arr = np.array([-10, 0, 50, 100, 200])

# Clip to [0, 100]
clipped = np.clip(arr, 0, 100)
print(clipped)
# Output: [  0   0  50 100 100]
```

**Related Terms:** np.where(), Comparison Operators

---

### Integer Array Indexing

**Definition:** Selecting array elements using arrays of integers as indices. Also known as fancy indexing.

**Example:**
```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Integer array indexing
indices = np.array([0, 2, 4])
print(arr[indices])
# Output: [10 30 50]
```

**Related Terms:** Fancy Indexing, Boolean Indexing

---

### np.in1d()

**Definition:** Tests whether each element of a 1D array is contained in another 1D array. Deprecated in favor of np.isin().

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
test = np.array([2, 4, 6])

# Check membership (deprecated)
mask = np.in1d(arr, test)
print(mask)
# Output: [False  True False  True False]

# Modern equivalent
mask = np.isin(arr, test)
print(mask)
# Output: [False  True False  True False]
```

**Related Terms:** np.isin(), Boolean Mask

---

### Conditional Replacement

**Definition:** Replacing array elements based on a condition using np.where().

**Example:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Replace elements > 3 with 0
result = np.where(arr > 3, 0, arr)
print(result)
# Output: [1 2 3 0 0]

# Replace based on two arrays
x = np.array([10, 20, 30, 40, 50])
y = np.array([100, 200, 300, 400, 500])
result = np.where(arr > 3, x, y)
print(result)
# Output: [100 200 300  10  20]
```

**Related Terms:** np.where(), Boolean Indexing

---

## Summary Table

| Term | Definition | Example |
|------|------------|---------|
| AND (`&`) | Both conditions must be True | `arr[(arr > 2) & (arr < 5)]` |
| Boolean Indexing | Select elements using boolean mask | `arr[arr > 3]` |
| Boolean Mask | Array of True/False from comparisons | `mask = arr > 3` |
| Clip | Limit values to range | `np.clip(arr, 0, 100)` |
| Comparison Operators | Element-wise comparisons | `arr > 3`, `arr == 5` |
| Fancy Indexing | Select by index array | `arr[[0, 2, 4]]` |
| Masked Array | Array with masked values | `np.ma.masked_where(arr > 3, arr)` |
| np.all() | Check if all True | `np.all(arr > 0)` |
| np.any() | Check if any True | `np.any(arr > 5)` |
| np.extract() | Extract matching elements | `np.extract(arr > 5, arr)` |
| np.isin() | Check membership | `np.isin(arr, test)` |
| np.where() | Conditional selection | `np.where(arr > 3, 0, arr)` |
| NOT (`~`) | Negate condition | `arr[~(arr > 3)]` |
| OR (`\|`) | Either condition True | `arr[(arr < 2) \| (arr > 8)]` |

---

**Back to Lecture:** [15 - Array Filter](15-array-filter-lecture.md)
