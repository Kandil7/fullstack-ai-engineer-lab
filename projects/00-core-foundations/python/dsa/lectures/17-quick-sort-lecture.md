# Lecture 17: Quick Sort

## Learning Objectives

By the end of this lecture, you will be able to:
- Understand the divide-and-conquer principle behind quick sort
- Implement quick sort with different pivot selection strategies
- Analyze time and space complexity including worst-case scenarios
- Understand the importance of pivot selection for performance
- Compare quick sort with merge sort and other O(n log n) algorithms
- Implement randomized and median-of-three pivot strategies

---

## 1. Introduction

Quick sort is one of the most efficient and widely used sorting algorithms. Developed by Tony Hoare in 1960, it uses a divide-and-conquer approach to sort elements by partitioning the array around a pivot element. Despite its O(n²) worst case, quick sort is often faster in practice than merge sort and heapsort due to better cache performance and lower constant factors.

**The Core Idea**: Pick a pivot, partition the array so elements less than the pivot are on the left and elements greater are on the right, then recursively sort the sub-arrays.

**Why Study It**:
- O(n log n) average case with small constant factors
- In-place sorting (O(log n) stack space)
- Excellent cache performance
- Most practical general-purpose sorting algorithm
- Foundation for understanding partitioning-based algorithms
- Used in many standard library implementations

---

## 2. How Quick Sort Works

### The Algorithm

```
1. Choose a pivot element from the array
2. Partition: rearrange so elements < pivot are left, elements > pivot are right
3. Recursively apply to left sub-array
4. Recursively apply to right sub-array
```

### Visual Walkthrough

Sorting `[3, 6, 8, 10, 1, 2, 1]` with pivot = 1 (Lomuto partition):

```
Initial: [3, 6, 8, 10, 1, 2, 1]
Pivot = 1 (last element)

Partition:
  Compare 3 > 1 → no swap
  Compare 6 > 1 → no swap
  Compare 8 > 1 → no swap
  Compare 10 > 1 → no swap
  Compare 1 ≤ 1 → swap with index 0 → [1, 6, 8, 10, 3, 2, 1]
  Compare 2 > 1 → no swap
  Compare 1 ≤ 1 → swap with index 1 → [1, 1, 8, 10, 3, 2, 6]
  Swap pivot with partition point → [1, 1, 6, 10, 3, 2, 8]
  
Result: [1, 1, 6, 10, 3, 2, 8] with pivot 8 in final position
       Left: [1, 1, 6, 3, 2]  Right: [10]

Recursively sort left and right sub-arrays.
```

---

## 3. Lomuto Partition Scheme

```python
def quicksort_lomuto(arr, low=0, high=None):
    """
    Quick sort using Lomuto partition scheme.
    
    Pivot is always the last element.
    Simpler to implement but less efficient with duplicates.
    
    Time Complexity: O(n log n) average, O(n²) worst
    Space Complexity: O(log n) — recursion stack
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_idx = partition_lomuto(arr, low, high)
        quicksort_lomuto(arr, low, pivot_idx - 1)
        quicksort_lomuto(arr, pivot_idx + 1, high)


def partition_lomuto(arr, low, high):
    """
    Lomuto partition: pivot is last element.
    
    Returns final position of pivot.
    """
    pivot = arr[high]
    i = low - 1  # Index of smaller element
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Example
data = [3, 6, 8, 10, 1, 2, 1]
quicksort_lomuto(data)
print(data)  # Output: [1, 1, 2, 3, 6, 8, 10]
```

---

## 4. Hoare Partition Scheme

```python
def quicksort_hoare(arr, low=0, high=None):
    """
    Quick sort using Hoare partition scheme.
    
    More efficient than Lomuto: fewer swaps on average.
    Uses two pointers moving toward each other.
    
    Time Complexity: O(n log n) average, O(n²) worst
    Space Complexity: O(log n)
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_idx = partition_hoare(arr, low, high)
        quicksort_hoare(arr, low, pivot_idx)
        quicksort_hoare(arr, pivot_idx + 1, high)


def partition_hoare(arr, low, high):
    """
    Hoare partition: two pointers moving toward each other.
    
    Returns the partition point (elements <= pivot are left, > pivot are right).
    """
    pivot = arr[low]
    i = low - 1
    j = high + 1
    
    while True:
        # Move right pointer to find element <= pivot
        j -= 1
        while arr[j] > pivot:
            j -= 1
        
        # Move left pointer to find element >= pivot
        i += 1
        while arr[i] < pivot:
            i += 1
        
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
        else:
            return j


# Example
data = [3, 6, 8, 10, 1, 2, 1]
quicksort_hoare(data)
print(data)  # Output: [1, 1, 2, 3, 6, 8, 10]
```

**Hoare vs Lomuto**:
- Hoare makes fewer swaps (about n/3 vs up to n)
- Hoare is faster in practice
- Lomuto is simpler and more intuitive
- Both have same time complexity

---

## 5. Randomized Quick Sort

```python
import random

def quicksort_randomized(arr, low=0, high=None):
    """
    Quick sort with random pivot selection.
    
    Avoids worst-case on sorted/nearly sorted data.
    Expected time: O(n log n)
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_idx = random_partition(arr, low, high)
        quicksort_randomized(arr, low, pivot_idx - 1)
        quicksort_randomized(arr, pivot_idx + 1, high)


def random_partition(arr, low, high):
    """Randomly select pivot and partition."""
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
    return partition_lomuto(arr, low, high)
```

---

## 6. Median-of-Three Pivot

```python
def median_of_three(arr, low, high):
    """Select median of first, middle, and last elements as pivot."""
    mid = (low + high) // 2
    
    # Sort low, mid, high
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    
    # Place median at high-1 position
    arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
    return arr[high - 1]


def quicksort_median_of_three(arr, low=0, high=None):
    """
    Quick sort with median-of-three pivot selection.
    
    Better pivot selection reduces worst-case probability.
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        if high - low + 1 <= 3:
            # Use insertion sort for small subarrays
            insertion_sort_subarray(arr, low, high)
        else:
            pivot = median_of_three(arr, low, high)
            i = low
            j = high - 1
            
            while True:
                i += 1
                while arr[i] < pivot:
                    i += 1
                j -= 1
                while arr[j] > pivot:
                    j -= 1
                
                if i < j:
                    arr[i], arr[j] = arr[j], arr[i]
                else:
                    break
            
            arr[i], arr[high - 1] = arr[high - 1], arr[i]
            
            quicksort_median_of_three(arr, low, i - 1)
            quicksort_median_of_three(arr, i + 1, high)


def insertion_sort_subarray(arr, low, high):
    """Insertion sort for small subarrays."""
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

---

## 7. Common Mistakes and Pitfalls

### Mistake 1: Using Wrong Pivot Index

```python
# WRONG: Not placing pivot in correct position after partition
def partition_wrong(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    # BUG: Not swapping pivot into position!
    return i  # Wrong return value

# CORRECT: Swap pivot into position and return its index
def partition_correct(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

### Mistake 2: Infinite Recursion

```python
# WRONG: Not handling base case correctly
def quicksort_wrong(arr, low, high):
    if low < high:  # BUG: Should be if low < high
        pivot_idx = partition_lomuto(arr, low, high)
        quicksort_wrong(arr, low, pivot_idx)  # BUG: Should be pivot_idx - 1
        quicksort_wrong(arr, pivot_idx, high)  # BUG: Should be pivot_idx + 1

# CORRECT: Proper base case and recursive calls
def quicksort_correct(arr, low, high):
    if low < high:
        pivot_idx = partition_lomuto(arr, low, high)
        quicksort_correct(arr, low, pivot_idx - 1)
        quicksort_correct(arr, pivot_idx + 1, high)
```

### Mistake 3: Not Handling Duplicates

```python
# WRONG: Lomuto with many duplicates causes unbalanced partitions
# [1, 1, 1, 1, 1] → pivot 1, everything goes left → O(n²)

# CORRECT: Three-way partition for duplicates
def three_way_partition(arr, low, high):
    """Partition into < pivot, == pivot, > pivot."""
    if low >= high:
        return
    
    pivot = arr[low]
    lt = low      # arr[low..lt-1] < pivot
    gt = high     # arr[gt+1..high] > pivot
    i = low       # arr[lt..i-1] == pivot
    
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1
    
    # Recursively sort elements < pivot and > pivot
    three_way_partition(arr, low, lt - 1)
    three_way_partition(arr, gt + 1, high)
```

### Mistake 4: Stack Overflow on Sorted Data

```python
# WRONG: Sorted data causes O(n) recursion depth
def quicksort_bad_pivot(arr, low, high):
    if low < high:
        pivot_idx = partition_lomuto(arr, low, high)  # Pivot is last!
        # On sorted data: pivot is largest → unbalanced → O(n) depth

# CORRECT: Use randomized or median-of-three pivot
def quicksort_good_pivot(arr, low, high):
    if low < high:
        rand_idx = random.randint(low, high)
        arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
        pivot_idx = partition_lomuto(arr, low, high)
        quicksort_good_pivot(arr, low, pivot_idx - 1)
        quicksort_good_pivot(arr, pivot_idx + 1, high)
```

---

## 8. Tail Recursion Optimization

```python
def quicksort_tail_recursive(arr, low=0, high=None):
    """
    Quick sort with tail recursion optimization.
    
    Recurses on smaller partition first, iterates on larger.
    Guarantees O(log n) stack space.
    """
    if high is None:
        high = len(arr) - 1
    
    while low < high:
        pivot_idx = partition_lomuto(arr, low, high)
        
        # Recurse on smaller partition, iterate on larger
        if pivot_idx - low < high - pivot_idx:
            quicksort_tail_recursive(arr, low, pivot_idx - 1)
            low = pivot_idx + 1
        else:
            quicksort_tail_recursive(arr, pivot_idx + 1, high)
            high = pivot_idx - 1
```

---

## 9. Performance Analysis

| Case | Time | Space | Pivot Strategy |
|------|------|-------|----------------|
| Best | O(n log n) | O(log n) | Balanced partitions |
| Average | O(n log n) | O(log n) | Random pivot |
| Worst | O(n²) | O(n) | Already sorted + bad pivot |

**Why O(n log n) Average**:
- Each level of recursion does O(n) work
- Expected depth is O(log n) with good pivot selection
- Total: O(n) × O(log n) = O(n log n)

**Why O(n²) Worst**:
- Always picks smallest/largest as pivot
- Creates maximally unbalanced partitions
- Recursion depth becomes O(n)

**Space Complexity**:
- O(log n) for recursion stack (average)
- O(n) for recursion stack (worst case)
- In-place: no extra array needed

---

## 10. Quick Sort vs Merge Sort

| Aspect | Quick Sort | Merge Sort |
|--------|-----------|------------|
| Time (avg) | O(n log n) | O(n log n) |
| Time (worst) | O(n²) | O(n log n) |
| Space | O(log n) | O(n) |
| Stable | No | Yes |
| In-place | Yes | No |
| Cache | Better | Worse |
| Practical | Faster | More predictable |

**When to Choose Quick Sort**:
- Memory is constrained
- Average-case performance matters more than worst-case
- Stability isn't required
- Data fits in cache

**When to Choose Merge Sort**:
- Guaranteed O(n log n) is required
- Stability is needed
- Working with linked lists
- External sorting (data on disk)

---

## 11. Exercises

### Exercise 1: Quick Select
Implement quick select to find the k-th smallest element.

```python
def quick_select(arr, k):
    """Find k-th smallest element (0-indexed)."""
    # Your code here
    pass
```

### Exercise 2: Three-Way Partition
Implement quick sort with three-way partitioning for handling duplicates.

```python
def quicksort_three_way(arr):
    """Quick sort that handles duplicates efficiently."""
    # Your code here
    pass
```

### Exercise 3: Count Comparisons
Implement quick sort that counts the number of comparisons made.

```python
def quicksort_counting(arr):
    """Return (sorted_array, comparison_count)."""
    # Your code here
    pass
```

### Exercise 4: Iterative Quick Sort
Implement quick sort iteratively using a stack.

```python
def quicksort_iterative(arr):
    """Quick sort without recursion."""
    # Your code here
    pass
```

---

## 12. Summary

**Key Takeaways**:
1. Quick sort uses divide-and-conquer with partitioning around a pivot
2. Average case O(n log n) with small constant factors
3. Worst case O(n²) occurs with bad pivot selection on sorted data
4. Randomized or median-of-three pivot avoids worst case in practice
5. In-place with O(log n) stack space; not stable

**Algorithm Properties**:

| Property | Value |
|----------|-------|
| Time (best) | O(n log n) |
| Time (average) | O(n log n) |
| Time (worst) | O(n²) |
| Space | O(log n) |
| Stable | No |
| In-place | Yes |
| Cache-friendly | Yes |

**When to Use Quick Sort**:
- General-purpose sorting
- Memory is constrained
- Average performance matters more than worst-case
- Stability is not required

---

## Next Lecture

In the next lecture, we'll explore **Counting Sort**, a non-comparison-based sorting algorithm that achieves O(n+k) time for integer data.
