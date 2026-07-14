# Lecture 20: Merge Sort

> A divide-and-conquer sorting algorithm that splits, sorts, and merges

## Learning Objectives

By the end of this lecture, you will be able to:
1. Understand the merge sort algorithm and its divide-and-conquer approach
2. Implement merge sort from scratch
3. Analyze time and space complexity
4. Know when merge sort is optimal versus when to use other algorithms
5. Understand the relationship between merge sort and other sorting algorithms

## Key Concepts

### What is Merge Sort?

Merge sort is a divide-and-conquer sorting algorithm that divides the input array into two halves, recursively sorts each half, and then merges the two sorted halves into a single sorted array.

**Key Insight:** By breaking the problem into smaller subproblems and combining solutions, merge sort achieves guaranteed O(n log n) time complexity with stable sorting.

### Core Principle

1. **Divide:** Split the array into two halves
2. **Conquer:** Recursively sort each half
3. **Combine:** Merge the two sorted halves

### Why Merge Sort?

- **Guaranteed Performance:** O(n log n) in all cases
- **Stability:** Preserves relative order of equal elements
- **Predictable:** Performance doesn't depend on input order
- **Parallelism:** Easy to parallelize due to independent subproblems

### Limitations

- **Space:** Requires O(n) extra space for merging
- **Not In-Place:** Cannot sort in constant extra space
- **Overhead:** Recursion and merging add constant factors
- **Cache:** Less cache-friendly than in-place algorithms

## Algorithm Walkthrough

### Step 1: Divide
Split the array into two halves at the midpoint.

### Step 2: Recurse
Recursively sort each half until reaching base case (single element).

### Step 3: Merge
Combine two sorted arrays into one sorted array using two pointers.

### Step 4: Base Case
When array has 0 or 1 elements, it's already sorted.

## Code Examples

### Basic Merge Sort

```python
def merge_sort(arr):
    """
    Basic merge sort implementation.
    
    Time Complexity: O(n log n) in all cases
    Space Complexity: O(n) for temporary arrays
    
    Args:
        arr: List to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer (merge)
    return merge(left, right)

def merge(left, right):
    """
    Merge two sorted arrays into one sorted array.
    
    Args:
        left: First sorted array
        right: Second sorted array
    
    Returns:
        Merged sorted array
    """
    result = []
    i = j = 0
    
    # Compare elements and merge
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

# Example usage
arr = [38, 27, 43, 3, 9, 82, 10]
print("Original array:", arr)
sorted_arr = merge_sort(arr)
print("Sorted array:", sorted_arr)
```

### In-Place Merge Sort

```python
def merge_sort_inplace(arr, left=0, right=None):
    """
    In-place merge sort that modifies the original array.
    
    Uses auxiliary space for merging but sorts in-place.
    
    Args:
        arr: Array to sort (modified in-place)
        left: Starting index
        right: Ending index (exclusive)
    """
    if right is None:
        right = len(arr)
    
    if right - left > 1:
        mid = (left + right) // 2
        
        # Sort halves in-place
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid, right)
        
        # Merge in-place
        merge_inplace(arr, left, mid, right)

def merge_inplace(arr, left, mid, right):
    """
    Merge two sorted subarrays in-place.
    
    Args:
        arr: Array containing subarrays
        left: Start of first subarray
        mid: End of first subarray / start of second
        right: End of second subarray
    """
    # Create temporary arrays
    left_arr = arr[left:mid]
    right_arr = arr[mid:right]
    
    i = j = 0
    k = left
    
    # Merge back into original array
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    # Copy remaining elements
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1

# Example usage
arr = [38, 27, 43, 3, 9, 82, 10]
print("Original array:", arr)
merge_sort_inplace(arr)
print("Sorted array:", arr)
```

### Optimized Merge Sort

```python
def merge_sort_optimized(arr):
    """
    Optimized merge sort with multiple improvements.
    
    1. Uses insertion sort for small subarrays
    2. Checks if array is already sorted
    3. Skips merge if halves are already in order
    
    Args:
        arr: List to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    # Use insertion sort for small arrays
    if len(arr) <= 10:
        return insertion_sort(arr)
    
    # Check if already sorted
    mid = len(arr) // 2
    if arr[mid - 1] <= arr[mid]:
        # Already sorted, no need to merge
        left = merge_sort_optimized(arr[:mid])
        right = merge_sort_optimized(arr[mid:])
        return left + right
    
    # Divide and conquer
    left = merge_sort_optimized(arr[:mid])
    right = merge_sort_optimized(arr[mid:])
    
    return merge(left, right)

def insertion_sort(arr):
    """Helper insertion sort for small arrays."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge(left, right):
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Example usage
arr = [38, 27, 43, 3, 9, 82, 10, 1, 5, 7]
print("Original array:", arr)
sorted_arr = merge_sort_optimized(arr)
print("Sorted array:", sorted_arr)
```

### Bottom-Up Merge Sort

```python
def merge_sort_bottom_up(arr):
    """
    Bottom-up merge sort (iterative version).
    
    Avoids recursion by merging subarrays of increasing size.
    
    Args:
        arr: List to sort
    
    Returns:
        Sorted list
    """
    n = len(arr)
    size = 1
    
    # Merge subarrays of increasing size
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(left + size, n)
            right = min(left + 2 * size, n)
            
            if mid < right:
                # Merge arr[left:mid] and arr[mid:right]
                merge_inplace(arr, left, mid, right)
        
        size *= 2
    
    return arr

def merge_inplace(arr, left, mid, right):
    """Merge two sorted subarrays."""
    left_arr = arr[left:mid]
    right_arr = arr[mid:right]
    
    i = j = 0
    k = left
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1

# Example usage
arr = [38, 27, 43, 3, 9, 82, 10]
print("Original array:", arr)
sorted_arr = merge_sort_bottom_up(arr)
print("Sorted array:", sorted_arr)
```

### Merge Sort for Linked Lists

```python
class ListNode:
    """Node for linked list."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_sort_linked_list(head):
    """
    Merge sort for linked lists.
    
    Efficient for linked lists due to O(1) merge operation.
    
    Args:
        head: Head of linked list
    
    Returns:
        Head of sorted linked list
    """
    if not head or not head.next:
        return head
    
    # Find middle using slow/fast pointers
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Split into two halves
    mid = slow.next
    slow.next = None
    
    # Recursively sort halves
    left = merge_sort_linked_list(head)
    right = merge_sort_linked_list(mid)
    
    # Merge sorted halves
    return merge_linked_lists(left, right)

def merge_linked_lists(l1, l2):
    """Merge two sorted linked lists."""
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    current.next = l1 or l2
    return dummy.next

# Helper function to create linked list from array
def create_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

# Helper function to convert linked list to array
def linked_list_to_array(head):
    arr = []
    while head:
        arr.append(head.val)
        head = head.next
    return arr

# Example usage
arr = [38, 27, 43, 3, 9, 82, 10]
print("Original array:", arr)
head = create_linked_list(arr)
sorted_head = merge_sort_linked_list(head)
sorted_arr = linked_list_to_array(sorted_head)
print("Sorted array:", sorted_arr)
```

### Merge Sort for Strings

```python
def merge_sort_strings(arr):
    """
    Merge sort for strings (lexicographic order).
    
    Args:
        arr: List of strings to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort_strings(arr[:mid])
    right = merge_sort_strings(arr[mid:])
    
    return merge_strings(left, right)

def merge_strings(left, right):
    """Merge two sorted string arrays."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Example usage
arr = ["banana", "apple", "cherry", "date", "fig"]
print("Original array:", arr)
sorted_arr = merge_sort_strings(arr)
print("Sorted array:", sorted_arr)
```

## Common Mistakes

### Mistake 1: Not Handling Base Case
```python
# WRONG: Missing base case causes infinite recursion
def merge_sort_wrong(arr):
    mid = len(arr) // 2
    left = merge_sort_wrong(arr[:mid])
    right = merge_sort_wrong(arr[mid:])
    return merge(left, right)

# CORRECT: Check for base case
def merge_sort_correct(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_correct(arr[:mid])
    right = merge_sort_correct(arr[mid:])
    return merge(left, right)
```

### Mistake 2: Incorrect Merge Logic
```python
# WRONG: Forgetting to add remaining elements
def merge_wrong(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result  # Missing remaining elements!

# CORRECT: Add remaining elements
def merge_correct(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### Mistake 3: Modifying Original Array During Merge
```python
# WRONG: Using original arrays during merge
def merge_wrong(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            left.pop(i)  # Modifying original!
            # ...
```

### Mistake 4: Not Using Stable Comparison
```python
# WRONG: Using unstable comparison
if left[i] < right[j]:  # May break stability
    result.append(left[i])
    i += 1

# CORRECT: Use <= for stability
if left[i] <= right[j]:
    result.append(left[i])
    i += 1
```

## Best Practices

1. **Handle Base Case:** Always check for single-element arrays
2. **Use Stable Comparison:** Use `<=` to preserve stability
3. **Optimize Small Arrays:** Use insertion sort for small subarrays
4. **Check Already Sorted:** Skip merge if halves are already in order
5. **Consider Bottom-Up:** Avoid recursion overhead for large arrays
6. **Memory Management:** Reuse temporary arrays when possible
7. **Test Thoroughly:** Include edge cases and performance tests

## Complexity Analysis

| Case | Time | Space | Notes |
|------|------|-------|-------|
| Best | O(n log n) | O(n) | Guaranteed performance |
| Average | O(n log n) | O(n) | Consistent behavior |
| Worst | O(n log n) | O(n) | No degradation |

- **n** = number of elements
- **log n** = number of divisions
- **n** = work per merge

**When to use merge sort:**
- Need guaranteed O(n log n) performance
- Stability is important
- Sorting linked lists (O(1) merge)
- External sorting (large data that doesn't fit in memory)
- Parallel processing is available

**When NOT to use merge sort:**
- Memory is severely constrained
- Need in-place sorting
- Small arrays (insertion sort is faster)
- Cache performance is critical

## Exercises

### Exercise 1: Merge Sort Implementation
**Problem:** Implement merge sort from scratch without using Python's built-in sort.

### Exercise 2: Count Inversions
**Problem:** Modify merge sort to count the number of inversions in an array.

### Exercise 3: External Merge Sort
**Problem:** Implement merge sort for files that don't fit in memory.

### Exercise 4: Three-Way Merge Sort
**Problem:** Implement merge sort that splits into three parts instead of two.

### Exercise 5: Parallel Merge Sort
**Problem:** Implement merge sort using Python's multiprocessing module.

## Summary

Merge sort is a fundamental divide-and-conquer sorting algorithm that provides guaranteed O(n log n) performance with stability. Key takeaways:

- **Best for:** When guaranteed performance and stability are needed
- **Time complexity:** O(n log n) in all cases
- **Space complexity:** O(n) for temporary arrays
- **Stability:** Yes, preserves relative order of equal elements
- **Variants:** In-place, bottom-up, and parallel versions

Understanding merge sort is essential for algorithm design and is used in many real-world applications like database systems and external sorting.

## Next Steps

- **Explore:** Tim Sort (Python's built-in sort combines merge sort and insertion sort)
- **Practice:** Implement merge sort variations
- **Study:** External sorting and large-scale data processing
- **Advanced:** Parallel and distributed merge sort algorithms
