# NumPy Lecture 14: Array Sort

## 🎯 Topic Overview

Sorting is a fundamental operation for data analysis and processing. This lecture covers `np.sort()`, `np.argsort()`, `np.lexsort()`, `np.partition()`, and sorting along different axes. Understanding sorting is essential for data preparation and analysis.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Sort arrays with `np.sort()`
2. Get sorting indices with `np.argsort()`
3. Sort along specific axes
4. Use `np.partition()` for partial sorting
5. Handle structured array sorting
6. Understand sorting algorithms and performance

---

## 1. Basic Sorting with `np.sort()`

### 1.1 1D Array Sorting

```python
import numpy as np

arr = np.array([30, 10, 50, 20, 40])
print(f"Original: {arr}")  # [30 10 50 20 40]

# Sort (returns new array)
sorted_arr = np.sort(arr)
print(f"Sorted: {sorted_arr}")  # [10 20 30 40 50]

# Original unchanged
print(f"Original: {arr}")  # [30 10 50 20 40]

# In-place sort (modifies original)
arr.sort()
print(f"In-place sorted: {arr}")  # [10 20 30 40 50]
```

### 1.2 Sorting Order

```python
arr = np.array([30, 10, 50, 20, 40])

# Ascending (default)
print(np.sort(arr))  # [10 20 30 40 50]

# Descending
print(np.sort(arr)[::-1])  # [50 40 30 20 10]

# Or use negative values
print(-np.sort(-arr))  # [50 40 30 20 10]
```

---

## 2. Sorting 2D Arrays

### 2.1 Sort Along Axis

```python
matrix = np.array([[3, 1, 4],
                   [1, 5, 9],
                   [2, 6, 5]])
print("Original:")
print(matrix)
# [[3 1 4]
#  [1 5 9]
#  [2 6 5]]

# Sort along axis 0 (columns)
sorted_axis0 = np.sort(matrix, axis=0)
print("Sorted along axis 0:")
print(sorted_axis0)
# [[1 1 4]
#  [2 5 5]
#  [3 6 9]]

# Sort along axis 1 (rows)
sorted_axis1 = np.sort(matrix, axis=1)
print("Sorted along axis 1:")
print(sorted_axis1)
# [[1 3 4]
#  [1 5 9]
#  [2 5 6]]

# Sort all elements (flattened)
sorted_all = np.sort(matrix, axis=None)
print("Sorted all: ", sorted_all)
# [1 1 2 3 4 5 5 6 9]
```

---

## 3. `np.argsort()` — Sorting Indices

### 3.1 Basic argsort

```python
arr = np.array([30, 10, 50, 20, 40])

# Get indices that would sort the array
indices = np.argsort(arr)
print(f"Indices: {indices}")  # [1 3 0 4 2]

# Use indices to sort
sorted_arr = arr[indices]
print(f"Sorted: {sorted_arr}")  # [10 20 30 40 50]

# Descending order
indices_desc = np.argsort(-arr)
print(f"Desc indices: {indices_desc}")  # [2 4 0 3 1]
print(f"Desc sorted: {arr[indices_desc]}")  # [50 40 30 20 10]
```

### 3.2 argsort with 2D Arrays

```python
matrix = np.array([[3, 1, 4],
                   [1, 5, 9]])

# Sort along axis 1 (rows)
indices = np.argsort(matrix, axis=1)
print(f"Indices:\n{indices}")
# [[1 0 2]
#  [0 1 2]]

# Get sorted values
sorted_matrix = np.take_along_axis(matrix, indices, axis=1)
print(f"Sorted:\n{sorted_matrix}")
# [[1 3 4]
#  [1 5 9]]
```

---

## 4. `np.partition()` — Partial Sorting

### 4.1 Basic Partition

```python
arr = np.array([30, 10, 50, 20, 40])

# Partition around 3rd element (index 2)
partitioned = np.partition(arr, 2)
print(f"Partitioned: {partitioned}")
# [20 10 30 50 40] — first 3 elements are smallest (not sorted)

# Find k smallest elements
k = 3
smallest = np.partition(arr, k)[:k]
print(f"Smallest {k}: {np.sort(smallest)}")  # [10 20 30]

# Find k largest elements
largest = np.partition(arr, -k)[-k:]
print(f"Largest {k}: {np.sort(largest)}")  # [30 40 50]
```

### 4.2 Partition vs Sort

```python
import time

arr = np.random.rand(1000000)

# Partition (faster for small k)
start = time.time()
_ = np.partition(arr, 10)[:10]
print(f"Partition: {time.time() - start:.4f}s")

# Sort (slower but fully sorted)
start = time.time()
_ = np.sort(arr)[:10]
print(f"Sort: {time.time() - start:.4f}s")
```

---

## 5. `np.lexsort()` — Multiple Key Sorting

```python
# Sort by multiple keys
names = np.array(['Alice', 'Bob', 'Charlie', 'David'])
ages = np.array([30, 25, 35, 25])

# Sort by age first, then by name
# lexsort sorts by last key first
sorted_indices = np.lexsort((names, ages))
print(f"Names: {names[sorted_indices]}")
# ['Bob' 'David' 'Alice' 'Charlie']

# Sort by age (primary), then name (secondary)
print(f"Ages: {ages[sorted_indices]}")
print(f"Names: {names[sorted_indices]}")
```

---

## 6. Sorting Structured Arrays

```python
# Create structured array
dt = np.dtype([('name', 'U10'), ('age', 'i4')])
employees = np.array([
    ('Alice', 30),
    ('Bob', 25),
    ('Charlie', 35),
    ('David', 25)
], dtype=dt)

# Sort by age
sorted_by_age = np.sort(employees, order='age')
print(sorted_by_age)
# [('Bob', 25) ('David', 25) ('Alice', 30) ('Charlie', 35)]

# Sort by name
sorted_by_name = np.sort(employees, order='name')
print(sorted_by_name)
```

---

## 7. Sorting Algorithms

### 7.1 Available Algorithms

```python
arr = np.random.rand(1000000)

# QuickSort (default, O(n log n))
sorted_arr = np.sort(arr, kind='quicksort')

# MergeSort (stable, O(n log n))
sorted_arr = np.sort(arr, kind='mergesort')

# HeapSort (O(n log n))
sorted_arr = np.sort(arr, kind='heapsort')

# Stable sort (preserves order of equal elements)
sorted_arr = np.sort(arr, kind='stable')
```

### 7.2 Performance Comparison

```python
import time

arr = np.random.rand(1000000)

for kind in ['quicksort', 'mergesort', 'heapsort', 'stable']:
    start = time.time()
    _ = np.sort(arr, kind=kind)
    print(f"{kind}: {time.time() - start:.4f}s")
```

---

## 8. Common Mistakes to Avoid

### Mistake 1: Forgetting sort Returns New Array
```python
arr = np.array([30, 10, 50, 20, 40])

# sort() returns new array
sorted_arr = np.sort(arr)
print(arr)        # [30 10 50 20 40] — unchanged!
print(sorted_arr) # [10 20 30 40 50]

# Use .sort() for in-place
arr.sort()
print(arr)        # [10 20 30 40 50]
```

### Mistake 2: Wrong Axis for Sorting
```python
matrix = np.array([[3, 1, 4],
                   [1, 5, 9]])

# axis=1 sorts rows
sorted_rows = np.sort(matrix, axis=1)
print(sorted_rows)
# [[1 3 4]
#  [1 5 9]]

# axis=0 sorts columns
sorted_cols = np.sort(matrix, axis=0)
print(sorted_cols)
# [[1 1 4]
#  [1 5 9]]
```

### Mistake 3: Not Using argsort When Indices Needed
```python
arr = np.array([30, 10, 50, 20, 40])

# Wrong: sorting twice
sorted_arr = np.sort(arr)
# How to get indices? Need to search again!

# Right: use argsort
indices = np.argsort(arr)
print(indices)  # [1 3 0 4 2]
```

---

## 9. Best Practices

1. **Use `np.sort()`** for returning new sorted array
2. **Use `.sort()`** for in-place sorting
3. **Use `np.argsort()`** when you need sorting indices
4. **Use `np.partition()`** for finding k smallest/largest
5. **Use `axis=None`** to sort all elements
6. **Use `kind='stable'`** when preserving order matters
7. **Use `np.lexsort()`** for multi-key sorting

---

## 10. Practice Exercises

### Exercise 1: Basic Sorting
```python
import numpy as np

arr = np.array([64, 25, 12, 22, 11])

# a) Sort in ascending order
# b) Sort in descending order
# c) Get indices that would sort the array
# d) Sort using argsort

sorted_asc = np.sort(arr)
sorted_desc = np.sort(arr)[::-1]
indices = np.argsort(arr)

print(f"Original: {arr}")
print(f"Ascending: {sorted_asc}")
print(f"Descending: {sorted_desc}")
print(f"Indices: {indices}")
print(f"Using argsort: {arr[indices]}")
```

### Exercise 2: 2D Sorting
```python
matrix = np.array([[3, 1, 4, 1],
                   [5, 9, 2, 6],
                   [5, 3, 5, 8]])

# a) Sort each row
# b) Sort each column
# c) Sort all elements

sorted_rows = np.sort(matrix, axis=1)
sorted_cols = np.sort(matrix, axis=0)
sorted_all = np.sort(matrix, axis=None)

print("Sorted rows:\n", sorted_rows)
print("Sorted columns:\n", sorted_cols)
print("Sorted all:", sorted_all)
```

### Exercise 3: argsort
```python
scores = np.array([85, 92, 78, 95, 88])
names = np.array(['Alice', 'Bob', 'Charlie', 'David', 'Eve'])

# Sort names by scores
indices = np.argsort(scores)[::-1]  # Descending
print("Ranking:")
for i, idx in enumerate(indices):
    print(f"{i+1}. {names[idx]}: {scores[idx]}")
```

### Exercise 4: Partition
```python
arr = np.random.rand(20)

# a) Find 5 smallest elements
# b) Find 5 largest elements
# c) Find median

smallest = np.partition(arr, 5)[:5]
largest = np.partition(arr, -5)[-5:]
median = np.partition(arr, len(arr)//2)[len(arr)//2]

print(f"5 smallest: {np.sort(smallest)}")
print(f"5 largest: {np.sort(largest)}")
print(f"Median: {median}")
```

---

## 11. Summary

| Function | Description | Returns | Use Case |
|----------|-------------|---------|----------|
| `np.sort()` | Sort array | New array | General sorting |
| `.sort()` | In-place sort | None | Memory efficient |
| `np.argsort()` | Sort indices | Indices | Get order |
| `np.partition()` | Partial sort | Array | k smallest/largest |
| `np.lexsort()` | Multi-key sort | Indices | Complex sorting |
| `np.take_along_axis()` | Sort with indices | Array | 2D+ sorting |

### Key Takeaways

1. `np.sort()` returns a new array; `.sort()` sorts in-place
2. Use `axis` parameter to control sort direction
3. `np.argsort()` returns indices that would sort the array
4. `np.partition()` is faster for finding k smallest/largest
5. `np.lexsort()` sorts by multiple keys
6. Use `kind='stable'` when preserving order matters
7. `np.take_along_axis()` combines argsort with sorting

---

## 🔗 End of NumPy Lectures

Congratulations! You've completed all 14 NumPy lectures. You now have a solid foundation in:

- Array creation and manipulation
- Indexing and slicing
- Data types and memory
- Shape and reshaping
- Joining and splitting
- Searching and sorting

**Next Steps:**
- Practice with real datasets
- Learn Pandas (built on NumPy)
- Explore SciPy for scientific computing
- Study machine learning libraries (scikit-learn, TensorFlow, PyTorch)
