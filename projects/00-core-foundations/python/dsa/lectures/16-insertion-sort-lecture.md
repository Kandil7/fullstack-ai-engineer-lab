# Lecture 16: Insertion Sort

## Learning Objectives

By the end of this lecture, you will be able to:
- Understand the insertion sort algorithm and its mechanics
- Implement insertion sort in Python
- Analyze time and space complexity
- Recognize when insertion sort outperforms other O(n²) algorithms
- Use insertion sort as a building block for hybrid algorithms
- Compare insertion sort with bubble sort and selection sort

---

## 1. Introduction

Insertion sort is one of the simplest and most practical O(n²) sorting algorithms. Unlike bubble sort (which bubbles large elements to the end) or selection sort (which selects the minimum), insertion sort builds the sorted array one element at a time by inserting each element into its correct position.

**The Core Idea**: Similar to how you sort playing cards in your hand—pick up each card and insert it into the correct position among the cards you've already sorted.

**Why Study It**:
- Best performance among O(n²) sorts on small or nearly sorted data
- Stable sort (preserves relative order of equal elements)
- In-place and adaptive (O(n) best case)
- Foundation for more advanced algorithms (Timsort, introsort)
- Simple to implement and understand
- Excellent for online sorting (can sort as data arrives)

---

## 2. How Insertion Sort Works

### The Algorithm

```
1. Start with the first element (trivially sorted)
2. Take the next element (the "key")
3. Compare it with elements in the sorted portion
4. Shift larger elements to the right
5. Insert the key in the correct position
6. Repeat until all elements are processed
```

### Visual Walkthrough

Sorting `[5, 2, 4, 6, 1, 3]`:

```
Step 1: [5, 2, 4, 6, 1, 3]
         ^ sorted portion
        
Step 2: [5, 2, 4, 6, 1, 3]  key = 2
         Compare 2 with 5 → shift 5 right
         Insert 2 at beginning
         Result: [2, 5, 4, 6, 1, 3]

Step 3: [2, 5, 4, 6, 1, 3]  key = 4
         Compare 4 with 5 → shift 5 right
         Compare 4 with 2 → stop (4 > 2)
         Insert 4 after 2
         Result: [2, 4, 5, 6, 1, 3]

Step 4: [2, 4, 5, 6, 1, 3]  key = 6
         Compare 6 with 5 → stop (6 > 5)
         Insert 6 after 5
         Result: [2, 4, 5, 6, 1, 3]

Step 5: [2, 4, 5, 6, 1, 3]  key = 1
         Compare 1 with 6 → shift 6 right
         Compare 1 with 5 → shift 5 right
         Compare 1 with 4 → shift 4 right
         Compare 1 with 2 → shift 2 right
         Insert 1 at beginning
         Result: [1, 2, 4, 5, 6, 3]

Step 6: [1, 2, 4, 5, 6, 3]  key = 3
         Compare 3 with 6 → shift 6 right
         Compare 3 with 5 → shift 5 right
         Compare 3 with 4 → shift 4 right
         Compare 3 with 2 → stop (3 > 2)
         Insert 3 after 2
         Result: [1, 2, 3, 4, 5, 6]
```

**Key Insight**: At each step, the left portion is always sorted. We're inserting the next element into its correct position within this sorted portion.

---

## 3. Implementation

```python
def insertion_sort(arr):
    """
    Insertion sort implementation.
    
    Args:
        arr: List of comparable elements
    
    Returns:
        None (sorts in-place)
    
    Time Complexity: O(n²) worst/average, O(n) best
    Space Complexity: O(1)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Shift elements greater than key to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        # Insert key in correct position
        arr[j + 1] = key


# Example
data = [5, 2, 4, 6, 1, 3]
insertion_sort(data)
print(data)  # Output: [1, 2, 3, 4, 5, 6]
```

**Complexity Analysis**:
- **Time**: O(n²) worst/average, O(n) best (already sorted)
- **Space**: O(1) — in-place sorting

---

## 4. Binary Insertion Sort

```python
def binary_insertion_sort(arr):
    """
    Insertion sort with binary search for finding insertion point.
    
    Reduces comparisons from O(n) to O(log n) per element.
    Shifts are still O(n) per element.
    
    Time Complexity: O(n²) overall, but fewer comparisons
    """
    for i in range(1, len(arr)):
        key = arr[i]
        
        # Binary search for insertion point
        left, right = 0, i
        while left < right:
            mid = (left + right) // 2
            if arr[mid] <= key:
                left = mid + 1
            else:
                right = mid
        
        # Shift elements to make room
        for j in range(i, left, -1):
            arr[j] = arr[j - 1]
        
        # Insert key
        arr[left] = key
```

**Trade-off**: Fewer comparisons but same number of shifts. Useful when comparisons are expensive.

---

## 5. Optimized Version with Sentinel

```python
def insertion_sort_sentinel(arr):
    """
    Insertion sort using sentinel to eliminate bounds check.
    
    Places minimum element at position 0 as sentinel.
    Removes the j >= 0 check in inner loop.
    """
    n = len(arr)
    
    # Find and place minimum at position 0 (sentinel)
    min_idx = 0
    for i in range(1, n):
        if arr[i] < arr[min_idx]:
            min_idx = i
    arr[0], arr[min_idx] = arr[min_idx], arr[0]
    
    # Standard insertion sort (no bounds check needed)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while arr[j] > key:  # No j >= 0 check needed!
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

---

## 6. Common Mistakes and Pitfalls

### Mistake 1: Starting from Index 0

```python
# WRONG: Starting from index 0
for i in range(len(arr)):  # BUG: arr[i-1] when i=0 is arr[-1]
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = key

# CORRECT: Start from index 1
for i in range(1, len(arr)):  # First element is trivially sorted
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = key
```

### Mistake 2: Not Shifting Before Inserting

```python
# WRONG: Overwriting without shifting
while j >= 0 and arr[j] > key:
    arr[j] = arr[j + 1]  # BUG: Overwrites arr[j]!
    j -= 1

# CORRECT: Shift right, then insert
while j >= 0 and arr[j] > key:
    arr[j + 1] = arr[j]  # Shift right
    j -= 1
arr[j + 1] = key  # Insert in correct position
```

### Mistake 3: Using `>=` Instead of `>`

```python
# WRONG: Unnecessarily shifts equal elements
while j >= 0 and arr[j] >= key:  # Shifts equal elements (unstable!)
    arr[j + 1] = arr[j]
    j -= 1

# CORRECT: Only shift when strictly greater
while j >= 0 and arr[j] > key:  # Preserves stability
    arr[j + 1] = arr[j]
    j -= 1
```

### Mistake 4: Forgetting to Store Key

```python
# WRONG: Overwriting key before insertion
for i in range(1, len(arr)):
    j = i - 1
    while j >= 0 and arr[j] > arr[i]:  # BUG: arr[i] changes during shifts!
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = arr[i]

# CORRECT: Store key before shifting
for i in range(1, len(arr)):
    key = arr[i]  # Store the value
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = key  # Insert stored value
```

---

## 7. Stability and Properties

**Stability**: Insertion sort is a stable sorting algorithm. Equal elements maintain their relative order because we only shift when `arr[j] > key` (strictly greater).

**In-Place**: Yes, O(1) extra space. Only uses a temporary variable for the key.

**Adaptive**: Yes, O(n) best case. Already sorted arrays require no shifts.

**Online**: Yes, can sort elements as they are received. Each new element is inserted into the correct position in the already-sorted portion.

```python
# Online sorting demonstration
class OnlineSorter:
    def __init__(self):
        self.sorted_data = []
    
    def insert(self, value):
        """Insert a new value while maintaining sorted order."""
        self.sorted_data.append(value)
        # Insertion sort on the last element
        i = len(self.sorted_data) - 1
        key = self.sorted_data[i]
        j = i - 1
        while j >= 0 and self.sorted_data[j] > key:
            self.sorted_data[j + 1] = self.sorted_data[j]
            j -= 1
        self.sorted_data[j + 1] = key
    
    def get_sorted(self):
        return self.sorted_data

# Usage
sorter = OnlineSorter()
for value in [5, 2, 8, 1, 9]:
    sorter.insert(value)
    print(f"After inserting {value}: {sorter.get_sorted()}")
```

---

## 8. Performance Analysis

| Case | Time | Shifts | Comparisons |
|------|------|--------|-------------|
| Best (sorted) | O(n) | 0 | n-1 |
| Average | O(n²) | n²/4 | n²/4 |
| Worst (reverse) | O(n²) | n(n-1)/2 | n(n-1)/2 |

**Key Insight**: Insertion sort is the only O(n²) sort that achieves O(n) best case. This makes it excellent for nearly sorted data.

**Real-World Performance**: For small arrays (n < 50), insertion sort often outperforms quicksort due to lower overhead.

```python
# Performance comparison
import time
import random

def benchmark_sort(sort_func, data, name):
    start = time.time()
    sort_func(data.copy())
    end = time.time()
    print(f"{name}: {end - start:.6f} seconds")

# Generate test data
n = 1000
random_data = [random.randint(0, n) for _ in range(n)]
nearly_sorted = list(range(n))
# Swap a few elements
for _ in range(10):
    i, j = random.randint(0, n-1), random.randint(0, n-1)
    nearly_sorted[i], nearly_sorted[j] = nearly_sorted[j], nearly_sorted[i]

print("Random data:")
benchmark_sort(insertion_sort, random_data, "Insertion Sort")
benchmark_sort(bubble_sort_optimized, random_data, "Bubble Sort")

print("\nNearly sorted data:")
benchmark_sort(insertion_sort, nearly_sorted, "Insertion Sort")
benchmark_sort(bubble_sort_optimized, nearly_sorted, "Bubble Sort")
```

---

## 9. Insertion Sort in Hybrid Algorithms

Insertion sort is used as a subroutine in more advanced algorithms:

**Timsort** (Python's built-in sort): Uses insertion sort for small runs (< 64 elements).

**Introsort**: Switches to insertion sort for small partitions.

**Shell Sort**: Generalization of insertion sort with gap sequences.

```python
# Timsort-like hybrid approach
def hybrid_sort(arr, threshold=32):
    """
    Use insertion sort for small arrays, quicksort for larger ones.
    """
    if len(arr) <= threshold:
        insertion_sort(arr)
    else:
        # Simplified quicksort partition
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        hybrid_sort(left, threshold)
        hybrid_sort(right, threshold)
        arr[:] = left + middle + right
```

---

## 10. When to Use Insertion Sort

**Use Insertion Sort When**:
- Data is small (< 50 elements)
- Data is nearly sorted
- Stability is required
- Online sorting is needed (data arrives one element at a time)
- Implementing a hybrid algorithm
- Memory is constrained (O(1) space)

**Avoid Insertion Sort When**:
- Data is large and random (use quicksort or mergesort)
- Performance is critical (O(n²) is too slow)

---

## 11. Exercises

### Exercise 1: Insertion Sort Descending
Modify insertion sort to sort in descending order.

```python
def insertion_sort_descending(arr):
    """Sort array in descending order using insertion sort."""
    # Your code here
    pass
```

### Exercise 2: Count Shifts
Implement insertion sort that returns the number of shifts performed.

```python
def insertion_sort_count_shifts(arr):
    """Return (sorted_array, shift_count)."""
    # Your code here
    pass
```

### Exercise 3: Insertion Sort for Linked List
Implement insertion sort for a singly linked list.

```python
def insertion_sort_linked_list(head):
    """Sort a singly linked list using insertion sort."""
    # Your code here
    pass
```

### Exercise 4: Binary Insertion Sort
Implement binary insertion sort and compare its performance with standard insertion sort.

```python
def binary_insertion_sort(arr):
    """Insertion sort using binary search for insertion point."""
    # Your code here
    pass
```

---

## 12. Summary

**Key Takeaways**:
1. Insertion sort builds the sorted array by inserting each element into position
2. O(n²) worst/average case, but O(n) best case (already sorted)
3. Stable, in-place, adaptive, and online
4. Best among O(n²) sorts for small or nearly sorted data
5. Foundation for hybrid algorithms like Timsort

**Algorithm Properties**:

| Property | Value |
|----------|-------|
| Time (best) | O(n) — already sorted |
| Time (average) | O(n²) |
| Time (worst) | O(n²) — reverse sorted |
| Space | O(1) |
| Stable | Yes |
| In-place | Yes |
| Adaptive | Yes |
| Online | Yes |

**Comparison with Other O(n²) Sorts**:

| Algorithm | Best | Average | Worst | Stable | Adaptive |
|-----------|------|---------|-------|--------|----------|
| Bubble Sort | O(n) | O(n²) | O(n²) | Yes | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | No | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | Yes | Yes |

---

## Next Lecture

In the next lecture, we'll explore **Quick Sort**, one of the most efficient general-purpose sorting algorithms with O(n log n) average case.
