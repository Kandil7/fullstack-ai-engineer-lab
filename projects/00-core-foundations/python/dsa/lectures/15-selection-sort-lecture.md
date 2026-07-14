# Lecture 15: Selection Sort

## Learning Objectives

By the end of this lecture, you will be able to:
- Understand the selection sort algorithm and its mechanics
- Implement selection sort in Python
- Analyze time and space complexity
- Compare selection sort with bubble sort and insertion sort
- Recognize that selection sort is not stable
- Understand when selection sort might be preferred despite O(n²)

---

## 1. Introduction

Selection sort is a simple, intuitive sorting algorithm that works by repeatedly finding the minimum element from the unsorted portion and placing it at the beginning. Unlike bubble sort which swaps adjacent elements, selection sort makes at most one swap per pass.

**The Core Idea**: Select the smallest remaining element and put it in its correct position.

**Why Study It**:
- Simple to understand and implement
- Minimal number of swaps (O(n)) — useful when write operations are expensive
- In-place sorting with O(1) extra space
- Good for understanding the trade-offs between comparison count and swap count
- Foundation for understanding more efficient selection-based algorithms

---

## 2. How Selection Sort Works

### The Algorithm

```
1. Find the minimum element in the unsorted portion
2. Swap it with the first unsorted element
3. Move the boundary between sorted and unsorted one position right
4. Repeat until the entire array is sorted
```

### Visual Walkthrough

Sorting `[64, 25, 12, 22, 11]`:

```
Initial: [64, 25, 12, 22, 11]

Pass 1:
  Find min in [64, 25, 12, 22, 11] → 11 at index 4
  Swap 64 and 11 → [11, 25, 12, 22, 64]
  Sorted: [11] | Unsorted: [25, 12, 22, 64]

Pass 2:
  Find min in [25, 12, 22, 64] → 12 at index 2
  Swap 25 and 12 → [11, 12, 25, 22, 64]
  Sorted: [11, 12] | Unsorted: [25, 22, 64]

Pass 3:
  Find min in [25, 22, 64] → 22 at index 3
  Swap 25 and 22 → [11, 12, 22, 25, 64]
  Sorted: [11, 12, 22] | Unsorted: [25, 64]

Pass 4:
  Find min in [25, 64] → 25 at index 3
  No swap needed (already in place)
  Sorted: [11, 12, 22, 25, 64]

Result: [11, 12, 22, 25, 64] — sorted!
```

**Key Observation**: Each pass makes at most one swap, regardless of array size. This is fewer swaps than bubble sort.

---

## 3. Implementation

```python
def selection_sort(arr):
    """
    Selection sort implementation.
    
    Args:
        arr: List of comparable elements
    
    Returns:
        None (sorts in-place)
    
    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    n = len(arr)
    
    for i in range(n - 1):
        # Find the minimum element in unsorted portion
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap the minimum element with the first unsorted element
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]


# Example
data = [64, 25, 12, 22, 11]
selection_sort(data)
print(data)  # Output: [11, 12, 22, 25, 64]
```

**Complexity Analysis**:
- **Time**: O(n²) in all cases — always scans the remaining unsorted portion
- **Space**: O(1) — only uses a temporary variable for swapping

---

## 4. Optimizations

### Early Termination

```python
def selection_sort_optimized(arr):
    """
    Optimized selection sort with early termination.
    
    Stops if minimum is already in correct position.
    Still O(n²) but saves the swap when possible.
    """
    n = len(arr)
    
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Only swap if needed
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
```

###双向选择排序 (Bidirectional Selection Sort)

```python
def bidirectional_selection_sort(arr):
    """
    Find both min and max in each pass.
    Places min at beginning and max at end.
    Reduces passes by half.
    """
    left = 0
    right = len(arr) - 1
    
    while left < right:
        min_idx = left
        max_idx = right
        
        for i in range(left, right + 1):
            if arr[i] < arr[min_idx]:
                min_idx = i
            if arr[i] > arr[max_idx]:
                max_idx = i
        
        # Place minimum at left
        arr[left], arr[min_idx] = arr[min_idx], arr[left]
        
        # If maximum was at left, it got swapped to min_idx
        if max_idx == left:
            max_idx = min_idx
        
        # Place maximum at right
        arr[right], arr[max_idx] = arr[max_idx], arr[right]
        
        left += 1
        right -= 1
```

---

## 5. Comparison with Bubble Sort

| Aspect | Selection Sort | Bubble Sort |
|--------|---------------|-------------|
| Comparisons | Always O(n²) | Always O(n²) |
| Swaps | O(n) | O(n²) worst |
| Stability | Not stable | Stable |
| Best case | O(n²) | O(n) with optimization |
| Adaptive | No | Yes |
| Writes | Fewer | More |

**When Selection Sort Wins**:
- Write operations are expensive (e.g., flash memory)
- Minimizing total data movement matters
- Simplicity is more important than best-case performance

**When Bubble Sort Wins**:
- Data is nearly sorted (adaptive O(n))
- Stability is required
- Teaching sorting concepts (more intuitive)

```python
# Demonstration: Selection sort does fewer swaps
def selection_sort_counting(arr):
    """Count comparisons and swaps."""
    comparisons = 0
    swaps = 0
    n = len(arr)
    
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    
    return comparisons, swaps

# For array of 1000 elements:
# Selection sort: 499,500 comparisons, at most 999 swaps
# Bubble sort: 499,500 comparisons, up to 499,500 swaps
```

---

## 6. Common Mistakes and Pitfalls

### Mistake 1: Not Finding True Minimum

```python
# WRONG: Only comparing with adjacent elements
for i in range(n - 1):
    if arr[i] > arr[i + 1]:
        arr[i], arr[i + 1] = arr[i + 1], arr[i]  # This is bubble sort!

# CORRECT: Finding minimum in entire unsorted portion
for i in range(n - 1):
    min_idx = i
    for j in range(i + 1, n):  # Scan entire unsorted portion
        if arr[j] < arr[min_idx]:
            min_idx = j
    arr[i], arr[min_idx] = arr[min_idx], arr[i]
```

### Mistake 2: Assuming Stability

```python
# Selection sort is NOT stable!
# Consider: [(1, 'a'), (1, 'b'), (2, 'c')]
# After sorting by first element:
# [(1, 'b'), (1, 'a'), (2, 'c')] — 'a' and 'b' swapped!

# If stability matters, use insertion sort or merge sort
```

### Mistake 3: Extra Swaps Per Pass

```python
# WRONG: Swapping during the search
for i in range(n - 1):
    for j in range(i + 1, n):
        if arr[j] < arr[i]:
            arr[i], arr[j] = arr[j], arr[i]  # Multiple swaps per pass!

# CORRECT: Find minimum first, then swap once
for i in range(n - 1):
    min_idx = i
    for j in range(i + 1, n):
        if arr[j] < arr[min_idx]:
            min_idx = j
    arr[i], arr[min_idx] = arr[min_idx], arr[i]  # One swap per pass
```

---

## 7. Properties

**Stability**: Selection sort is NOT stable. The swapping of distant elements can change the relative order of equal elements.

**In-Place**: Yes, O(1) extra space. Only uses a temporary variable for swapping.

**Adaptive**: No, selection sort always scans the entire unsorted portion regardless of input order.

**Online**: Can sort elements as they arrive, but not commonly used this way.

**Comparison Count**: Always n(n-1)/2 — same as bubble sort.

**Swap Count**: At most n-1 — much better than bubble sort's O(n²) swaps.

```python
# Instability demonstration
def demonstrate_instability():
    data = [(3, 'apple'), (1, 'banana'), (3, 'cherry'), (2, 'date')]
    
    # Sort by first element using selection sort
    n = len(data)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if data[j][0] < data[min_idx][0]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    
    print(data)
    # May output: [(1, 'banana'), (2, 'date'), (3, 'cherry'), (3, 'apple')]
    # Note: 'cherry' came before 'apple' — order changed!

demonstrate_instability()
```

---

## 8. When to Use Selection Sort

**Use Selection Sort When**:
- Write operations are expensive (minimize swaps)
- Memory is extremely constrained (O(1) space)
- Data structure doesn't support efficient swaps
- Educational purposes (simple to understand)
- Small datasets (< 20 elements)

**Avoid Selection Sort When**:
- Performance matters (use quicksort, mergesort, or timsort)
- Stability is required (use insertion sort or merge sort)
- Data is nearly sorted (bubble or insertion sort are better)
- Data is large (O(n²) is too slow)

```python
# Practical example: Minimizing writes to flash memory
def flash_friendly_sort(data):
    """
    Selection sort is good when writes are expensive.
    Each element is written at most once.
    """
    selection_sort(data)
    return data
```

---

## 9. Performance Analysis

| Case | Time | Swaps | Comparisons |
|------|------|-------|-------------|
| Best | O(n²) | 0 | n(n-1)/2 |
| Average | O(n²) | n/2 | n(n-1)/2 |
| Worst | O(n²) | n-1 | n(n-1)/2 |

**Space Complexity**: O(1) — in-place sorting

**Key Insight**: Selection sort always makes the same number of comparisons regardless of input. This makes it predictable but never fast.

---

## 10. Exercises

### Exercise 1: Maximum Selection Sort
Modify selection sort to sort in descending order by finding the maximum instead of minimum.

```python
def selection_sort_descending(arr):
    """Sort array in descending order using selection sort."""
    # Your code here
    pass
```

### Exercise 2: Count Operations
Implement selection sort that returns the number of comparisons and swaps performed.

```python
def selection_sort_counting(arr):
    """Return (sorted_array, comparisons, swaps)."""
    # Your code here
    pass
```

### Exercise 3: Stable Selection Sort
Implement a stable version of selection sort (hint: use insertion instead of swapping).

```python
def stable_selection_sort(arr):
    """Stable selection sort using insertion for equal elements."""
    # Your code here
    pass
```

### Exercise 4: Selection Sort on Linked List
Implement selection sort for a singly linked list.

```python
def selection_sort_linked_list(head):
    """Sort a singly linked list using selection sort."""
    # Your code here
    pass
```

---

## 11. Summary

**Key Takeaways**:
1. Selection sort finds the minimum and swaps it to the front
2. O(n²) time in all cases, but only O(n) swaps
3. Not stable — equal elements may change relative order
4. Good when write operations are expensive
5. Simpler than bubble sort but less adaptive

**Algorithm Properties**:

| Property | Value |
|----------|-------|
| Time (all cases) | O(n²) |
| Space | O(1) |
| Stable | No |
| In-place | Yes |
| Adaptive | No |
| Swaps | O(n) |
| Comparisons | O(n²) |

**When to Choose Selection Sort**:
- Minimizing writes is critical
- Simplicity outweighs performance
- Educational demonstration
- Very small datasets

---

## Next Lecture

In the next lecture, we'll explore **Insertion Sort**, which is often the most practical of the O(n²) sorts for small or nearly sorted datasets.
