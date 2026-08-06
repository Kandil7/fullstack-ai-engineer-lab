# Merge Sort — Glossary

> **Quick Reference Table**

| Term | Definition |
|------|-----------|
| Merge Sort | A divide-and-conquer sorting algorithm that splits, sorts, and merges |
| Divide and Conquer | Algorithm paradigm that splits problems into subproblems, solves them, and combines results |
| Merge | The process of combining two sorted arrays into one sorted array |
| Stable Sort | A sorting algorithm that preserves relative order of equal elements |
| In-place Sorting | Sorting without requiring additional memory proportional to input size |
| Recursion | A function that calls itself to solve smaller instances of the problem |
| Base Case | The condition that stops recursion |
| Subarray | A contiguous portion of an array |
| Temporary Array | Auxiliary array used during merge operation |
| Time Complexity | A measure of how algorithm runtime grows with input size |
| Space Complexity | A measure of how memory usage grows with input size |
| O(n log n) | Time complexity of merge sort in all cases |
| O(n) | Space complexity of merge sort for temporary arrays |
| Bottom-Up Merge Sort | Iterative version that avoids recursion |
| Top-Down Merge Sort | Recursive version that divides from top |
| Linked List Sorting | Merge sort adapted for linked list data structure |
| External Sorting | Sorting data that doesn't fit in memory |
| Inversion | A pair of elements that are out of order |
| Two-Pointer Technique | Using two indices to traverse arrays during merge |
| Already Sorted Check | Optimization to skip merge when halves are sorted |
| Insertion Sort Hybrid | Using insertion sort for small subarrays |
| Parallel Merge Sort | Merge sort that processes subarrays concurrently |
| Cache-Friendly | Algorithm that works well with CPU cache |
| Auxiliary Space | Extra memory used beyond input and output |
| Comparison Sort | A sort that uses comparisons to determine order |
| Lower Bound | Theoretical minimum comparisons needed for sorting |
| Tim Sort | Hybrid sort combining merge sort and insertion sort |
| Natural Merge Sort | Merge sort that identifies existing sorted runs |
| Run | A contiguous sorted subsequence |
| Monotonic | Consistently increasing or decreasing sequence |
| Merge Policy | Strategy for choosing which runs to merge |
| Way Merge | Number of arrays being merged simultaneously |
| k-Way Merge | Merging k sorted arrays |
| Tournament Tree | Tree structure used for k-way merging |
| Priority Queue | Data structure for efficient minimum extraction |
| Heap | Complete binary tree with heap property |
| Min-Heap | Heap where parent ≤ children |
| Max-Heap | Heap where parent ≥ children |
| Binary Search | Efficient search in sorted arrays |
| Divide Point | The midpoint where array is split |
| Left Subarray | First half of divided array |
| Right Subarray | Second half of divided array |
| Merge Pointer | Index tracking position in each subarray during merge |
| Result Array | Array containing merged sorted elements |
| Remaining Elements | Elements left after main merge loop |
| Copy Operation | Duplicating array contents |
| Array Slicing | Creating subarrays from original array |
| Recursion Depth | Maximum nested recursive calls |
| Call Stack | Stack tracking active function calls |
| Tail Recursion | Recursion where recursive call is last action |
| Iterative Version | Non-recursive implementation |
| Hybrid Algorithm | Combining multiple algorithms for optimization |
| Performance Benchmarking | Measuring algorithm speed |
| Worst Case | Scenario with maximum operations |
| Best Case | Scenario with minimum operations |
| Average Case | Expected performance over inputs |
| Algorithm Optimization | Improving efficiency without changing correctness |

## Alphabetical Definitions

### A

**Algorithm Optimization** — Improving efficiency without changing correctness. Merge sort optimizations include insertion sort for small arrays and checking if already sorted.

**Already Sorted Check** — Optimization to skip merge when halves are already in order. Reduces unnecessary operations.

**Auxiliary Space** — Extra memory used beyond input and output. Merge sort requires O(n) auxiliary space.

### B

**Base Case** — The condition that stops recursion. For merge sort, this is when the array has 0 or 1 elements.

**Binary Search** — Efficient search in sorted arrays. Can be used with merge sort for efficient searching.

**Bottom-Up Merge Sort** — Iterative version that avoids recursion. Merges subarrays of increasing size.

### C

**Cache-Friendly** — Algorithm that works well with CPU cache. Merge sort is less cache-friendly than in-place algorithms.

**Call Stack** — Stack tracking active function calls. Each recursive merge sort call adds a frame.

**Comparison Sort** — A sort using comparisons. Merge sort is a comparison-based sort.

### D

**Divide and Conquer** — Algorithm paradigm that splits problems into subproblems. Merge sort exemplifies this approach.

**Divide Point** — The midpoint where array is split. Usually at len(arr) // 2.

### E

**External Sorting** — Sorting data that doesn't fit in memory. Merge sort is commonly used for external sorting.

### I

**In-place Sorting** — Sorting without significant extra memory. Merge sort is NOT in-place (requires O(n) space).

**Insertion Sort Hybrid** — Using insertion sort for small subarrays. Improves merge sort performance on small inputs.

**Inversion** — A pair of elements that are out of order. Merge sort can count inversions efficiently.

**Iterative Version** — Non-recursive implementation. Bottom-up merge sort is iterative.

### K

**k-Way Merge** — Merging k sorted arrays simultaneously. Used in external sorting and multiway merge sort.

### L

**Lower Bound** — Theoretical minimum comparisons needed for sorting. Merge sort achieves this bound.

### M

**Merge** — The process of combining two sorted arrays into one. Core operation of merge sort.

**Merge Pointer** — Index tracking position in each subarray during merge.

**Merge Policy** — Strategy for choosing which runs to merge in natural merge sort.

**Min-Heap** — Heap where parent ≤ children. Can be used for k-way merging.

**Monotonic** — Consistently increasing or decreasing sequence. Runs in natural merge sort are monotonic.

### N

**Natural Merge Sort** — Merge sort that identifies existing sorted runs. More efficient on partially sorted data.

### P

**Parallel Merge Sort** — Merge sort that processes subarrays concurrently. Takes advantage of multiple processors.

**Priority Queue** — Data structure for efficient minimum extraction. Can be used for k-way merging.

### R

**Recursion** — A function calling itself. Merge sort uses recursion to sort subarrays.

**Recursion Depth** — Maximum nested recursive calls. Merge sort has O(log n) depth.

**Remaining Elements** — Elements left after main merge loop. Must be appended to result.

**Result Array** — Array containing merged sorted elements.

**Run** — A contiguous sorted subsequence. Natural merge sort identifies and merges runs.

### T

**Tail Recursion** — Recursion where recursive call is last action. Can optimize merge sort space.

**Temporary Array** — Auxiliary array used during merge. Required for O(n) merge operation.

**Time Complexity** — Measure of runtime growth. Merge sort is O(n log n) in all cases.

**Tim Sort** — Hybrid sort combining merge sort and insertion sort. Python's built-in sort.

**Top-Down Merge Sort** — Recursive version that divides from top. Standard merge sort implementation.

**Two-Pointer Technique** — Using two indices to traverse arrays during merge.

### W

**Worst Case** — Scenario with maximum operations. Merge sort is O(n log n) even in worst case.

**Way Merge** — Number of arrays being merged simultaneously. Standard merge is 2-way.

## Code Examples

### Basic Merge Sort

```python
def merge_sort(arr):
    """
    Basic merge sort implementation.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        arr: List to sort
    
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

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
arr = [38, 27, 43, 3, 9, 82, 10]
print("Sorted:", merge_sort(arr))
```

### In-Place Merge Sort

```python
def merge_sort_inplace(arr, left=0, right=None):
    """In-place merge sort."""
    if right is None:
        right = len(arr)
    
    if right - left > 1:
        mid = (left + right) // 2
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid, right)
        merge_inplace(arr, left, mid, right)

def merge_inplace(arr, left, mid, right):
    """Merge two sorted subarrays in-place."""
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
merge_sort_inplace(arr)
print("Sorted:", arr)
```

### Bottom-Up Merge Sort

```python
def merge_sort_bottom_up(arr):
    """Bottom-up merge sort (iterative)."""
    n = len(arr)
    size = 1
    
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(left + size, n)
            right = min(left + 2 * size, n)
            
            if mid < right:
                merge_inplace(arr, left, mid, right)
        
        size *= 2
    
    return arr

# Example usage
arr = [38, 27, 43, 3, 9, 82, 10]
print("Sorted:", merge_sort_bottom_up(arr))
```

### Merge Sort for Linked Lists

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_sort_linked_list(head):
    """Merge sort for linked lists."""
    if not head or not head.next:
        return head
    
    # Find middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    mid = slow.next
    slow.next = None
    
    # Sort halves
    left = merge_sort_linked_list(head)
    right = merge_sort_linked_list(mid)
    
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
```

### Count Inversions

```python
def count_inversions(arr):
    """
    Count inversions using merge sort.
    
    Inversion: pair (i,j) where i < j and arr[i] > arr[j]
    
    Args:
        arr: List to count inversions
    
    Returns:
        Tuple (sorted_array, inversion_count)
    """
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, left_inv = count_inversions(arr[:mid])
    right, right_inv = count_inversions(arr[mid:])
    merged, split_inv = merge_count(left, right)
    
    return merged, left_inv + right_inv + split_inv

def merge_count(left, right):
    """Merge and count split inversions."""
    result = []
    i = j = 0
    inversions = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            inversions += len(left) - i
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result, inversions

# Example usage
arr = [2, 4, 1, 3, 5]
sorted_arr, inversions = count_inversions(arr)
print("Inversions:", inversions)  # Output: 3
```

## Related Terms

- **Quick Sort** — Comparison-based sort with O(n log n) average but O(n²) worst case
- **Heap Sort** — In-place O(n log n) sort using heap data structure
- **Insertion Sort** — O(n²) sort efficient for small or nearly sorted arrays
- **Selection Sort** — Simple O(n²) sort that repeatedly selects minimum
- **Bubble Sort** — Simple O(n²) sort with repeated swaps
- **Shell Sort** — Generalization of insertion sort for distant elements
- **Tim Sort** — Hybrid sort combining merge sort and insertion sort
- **Intro Sort** — Hybrid sort combining quicksort, heapsort, and insertion sort
- **Counting Sort** — Non-comparison sort using element counts
- **Radix Sort** — Non-comparison sort processing digits
- **Bucket Sort** — Distribution-based sort using buckets
- **Divide and Conquer** — Algorithm paradigm underlying merge sort
- **Recursion** — Programming technique used by merge sort
- **Stable Sort** — Preserves relative order of equal elements
- **In-place Algorithm** — Uses constant extra space
- **Auxiliary Space** — Extra memory beyond input
- **Time Complexity** — Growth rate of runtime with input size
- **Space Complexity** — Growth rate of memory usage with input size
- **O(n log n)** — Time complexity of merge sort
- **O(n)** — Space complexity of merge sort
- **Base Case** — Condition that stops recursion
- **Subarray** — Contiguous portion of array
- **Two-Pointer Technique** — Using two indices for traversal
- **External Sorting** — Sorting data that doesn't fit in memory
- **Inversion** — Pair of out-of-order elements
- **Linked List Sorting** — Merge sort for linked data structures
- **Bottom-Up Merge Sort** — Iterative version without recursion
- **Top-Down Merge Sort** — Recursive version
- **Natural Merge Sort** — Identifies existing sorted runs
- **Run** — Contiguous sorted subsequence
- **k-Way Merge** — Merging k sorted arrays
- **Way Merge** — Number of arrays being merged
- **Merge Policy** — Strategy for choosing runs to merge
- **Tournament Tree** — Tree structure for k-way merging
- **Priority Queue** — Data structure for minimum extraction
- **Heap** — Complete binary tree with heap property
- **Min-Heap** — Heap where parent ≤ children
- **Max-Heap** — Heap where parent ≥ children
- **Binary Search** — Efficient search in sorted arrays
- **Divide Point** — Midpoint where array is split
- **Left Subarray** — First half of divided array
- **Right Subarray** — Second half of divided array
- **Merge Pointer** — Index tracking position during merge
- **Result Array** — Array containing merged elements
- **Remaining Elements** — Elements left after merge loop
- **Copy Operation** — Duplicating array contents
- **Array Slicing** — Creating subarrays from original
- **Recursion Depth** — Maximum nested recursive calls
- **Call Stack** — Stack tracking active function calls
- **Tail Recursion** — Recursion where call is last action
- **Iterative Version** — Non-recursive implementation
- **Hybrid Algorithm** — Combining multiple algorithms
- **Performance Benchmarking** — Measuring algorithm speed
- **Worst Case** — Scenario with maximum operations
- **Best Case** — Scenario with minimum operations
- **Average Case** — Expected performance over inputs
- **Algorithm Optimization** — Improving efficiency
