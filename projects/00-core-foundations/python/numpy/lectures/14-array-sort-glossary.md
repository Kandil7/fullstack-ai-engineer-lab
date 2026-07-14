# NumPy Lecture 14: Array Sort — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| sort | Sort array elements | `np.sort(arr)` |
| argsort | Indices that sort array | `np.argsort(arr)` |
| partition | Partial sort around k | `np.partition(arr, k)` |
| lexsort | Multi-key sorting | `np.lexsort((key2, key1))` |
| axis | Dimension to sort along | `axis=0`, `axis=1` |
| kind | Sorting algorithm | `'quicksort'`, `'mergesort'` |
| stable | Preserves equal element order | `kind='stable'` |
| ascending | Smallest to largest | Default |
| descending | Largest to smallest | `np.sort(arr)[::-1]` |
| In-place | Modifies original array | `arr.sort()` |
| Out-of-place | Returns new array | `np.sort(arr)` |
| take_along_axis | Sort with indices | `np.take_along_axis()` |

---

## Alphabetical Glossary

### A

#### Argsort
Return indices that would sort the array.

```python
import numpy as np

arr = np.array([30, 10, 50, 20, 40])

# Indices that sort the array
indices = np.argsort(arr)
print(indices)  # [1 3 0 4 2]

# Use indices to sort
sorted_arr = arr[indices]
print(sorted_arr)  # [10 20 30 40 50]

# Descending order
indices_desc = np.argsort(-arr)
print(arr[indices_desc])  # [50 40 30 20 10]

# 2D argsort
matrix = np.array([[3, 1, 4], [1, 5, 9]])
indices = np.argsort(matrix, axis=1)
print(indices)
# [[1 0 2]
#  [0 1 2]]
```

**Related:** sort, partition, take_along_axis

---

#### Axis
Dimension along which to sort.

```python
matrix = np.array([[3, 1, 4],
                   [1, 5, 9],
                   [2, 6, 5]])

# Sort along axis 0 (columns)
print(np.sort(matrix, axis=0))
# [[1 1 4]
#  [2 5 5]
#  [3 6 9]]

# Sort along axis 1 (rows)
print(np.sort(matrix, axis=1))
# [[1 3 4]
#  [1 5 9]
#  [2 5 6]]

# Sort all elements
print(np.sort(matrix, axis=None))
# [1 1 2 3 4 5 5 6 9]
```

**Related:** sort, argsort, shape

---

### D

#### Descending
Sort from largest to smallest.

```python
arr = np.array([30, 10, 50, 20, 40])

# Descending sort
sorted_desc = np.sort(arr)[::-1]
print(sorted_desc)  # [50 40 30 20 10]

# Alternative using negative
sorted_desc = -np.sort(-arr)
print(sorted_desc)  # [50 40 30 20 10]
```

**Related:** ascending, sort

---

### K

#### Kind
Sorting algorithm parameter: 'quicksort', 'mergesort', 'heapsort', 'stable'.

```python
arr = np.random.rand(1000000)

# QuickSort (default)
sorted_arr = np.sort(arr, kind='quicksort')

# MergeSort (stable)
sorted_arr = np.sort(arr, kind='mergesort')

# HeapSort
sorted_arr = np.sort(arr, kind='heapsort')

# Stable sort
sorted_arr = np.sort(arr, kind='stable')
```

**Related:** sort, stable, performance

---

### L

#### Lexsort
Sort by multiple keys (lexicographic sorting).

```python
names = np.array(['Alice', 'Bob', 'Charlie', 'David'])
ages = np.array([30, 25, 35, 25])

# Sort by age (primary), then name (secondary)
indices = np.lexsort((names, ages))
print(f"Names: {names[indices]}")
# ['Bob' 'David' 'Alice' 'Charlie']

print(f"Ages: {ages[indices]}")
# [25 25 30 35]
```

**Related:** sort, argsort, multiple keys

---

### P

#### Partition
Partial sort: places k-th element in correct position.

```python
arr = np.array([30, 10, 50, 20, 40])

# Partition around index 2
partitioned = np.partition(arr, 2)
print(partitioned)  # [20 10 30 50 40]

# Find k smallest
k = 3
smallest = np.partition(arr, k)[:k]
print(f"Smallest {k}: {np.sort(smallest)}")  # [10 20 30]

# Find k largest
largest = np.partition(arr, -k)[-k:]
print(f"Largest {k}: {np.sort(largest)}")  # [30 40 50]
```

**Note:** Faster than full sort when you only need k smallest/largest.

**Related:** sort, argsort, k-th element

---

### S

#### Sort
Return a sorted copy of the array.

```python
arr = np.array([30, 10, 50, 20, 40])

# Returns new array (out-of-place)
sorted_arr = np.sort(arr)
print(sorted_arr)  # [10 20 30 40 50]
print(arr)         # [30 10 50 20 40] — unchanged

# In-place sort
arr.sort()
print(arr)  # [10 20 30 40 50]
```

**Related:** argsort, partition, .sort()

---

#### Stable
Sorting algorithm that preserves order of equal elements.

```python
arr = np.array([3, 1, 2, 1, 3])

# Unstable sort (may change order of 1s and 3s)
sorted_unstable = np.sort(arr, kind='quicksort')

# Stable sort (preserves order of 1s and 3s)
sorted_stable = np.sort(arr, kind='stable')

# For structured arrays
dt = np.dtype([('name', 'U10'), ('age', 'i4')])
data = np.array([('Alice', 30), ('Bob', 25), ('Charlie', 30)], dtype=dt)

# Stable sort by age preserves original order of equal ages
sorted_data = np.sort(data, order='age', kind='stable')
print(sorted_data)
# [('Bob', 25) ('Alice', 30) ('Charlie', 30)]
```

**Related:** kind, sort, equal elements

---

#### Sort indices
Indices that would sort the array.

```python
arr = np.array([30, 10, 50, 20, 40])
indices = np.argsort(arr)
print(indices)  # [1 3 0 4 2]
```

**Related:** argsort

---

### T

#### Take_along_axis
Gather elements along axis using indices.

```python
matrix = np.array([[3, 1, 4],
                   [1, 5, 9]])

# Sort each row
indices = np.argsort(matrix, axis=1)
sorted_matrix = np.take_along_axis(matrix, indices, axis=1)
print(sorted_matrix)
# [[1 3 4]
#  [1 5 9]]

# Sort each column
indices = np.argsort(matrix, axis=0)
sorted_matrix = np.take_along_axis(matrix, indices, axis=0)
print(sorted_matrix)
# [[1 1 4]
#  [1 5 9]]
```

**Related:** argsort, sort, axis

---

## Sorting Methods Comparison

| Method | Returns | In-place | Use Case |
|--------|---------|----------|----------|
| `np.sort()` | New array | No | General sorting |
| `arr.sort()` | None | Yes | Memory efficient |
| `np.argsort()` | Indices | No | Get sort order |
| `np.partition()` | New array | No | k smallest/largest |
| `np.lexsort()` | Indices | No | Multi-key sorting |
| `np.take_along_axis()` | New array | No | Sort with indices |

## Sorting Algorithms

| Algorithm | Time | Space | Stable | Best For |
|-----------|------|-------|--------|----------|
| QuickSort | O(n log n) | O(log n) | No | General purpose |
| MergeSort | O(n log n) | O(n) | Yes | Stable sort |
| HeapSort | O(n log n) | O(1) | No | Memory constrained |
| Stable | O(n log n) | O(n) | Yes | Equal elements |

## Quick Sort Patterns

```python
import numpy as np

arr = np.array([30, 10, 50, 20, 40])

# Basic sort
sorted_arr = np.sort(arr)

# Descending
sorted_desc = np.sort(arr)[::-1]

# Get indices
indices = np.argsort(arr)

# K smallest
k = 3
smallest = np.partition(arr, k)[:k]

# K largest
largest = np.partition(arr, -k)[-k:]

# Sort 2D by row
matrix = np.array([[3, 1, 4], [1, 5, 9]])
sorted_rows = np.sort(matrix, axis=1)

# Sort 2D by column
sorted_cols = np.sort(matrix, axis=0)
```
