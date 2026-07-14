# Quick Sort — Glossary

> **Quick Reference Table**

| Term | Definition |
|------|-----------|
| Quick Sort | A divide-and-conquer sorting algorithm that selects a pivot and partitions elements around it |
| Pivot | The element used to partition the array into sub-arrays |
| Partition | The process of dividing elements into groups less than, equal to, and greater than the pivot |
| In-place Sorting | Sorting without requiring additional memory proportional to input size |
| Stable Sort | A sort that preserves the relative order of equal elements |
| Unstable Sort | A sort that may change the relative order of equal elements |
| Divide and Conquer | Algorithm paradigm that splits problems into subproblems, solves them, and combines results |
| Recursion | A function that calls itself to solve smaller instances of the problem |
| Time Complexity | A measure of how the runtime of an algorithm grows with input size |
| Space Complexity | A measure of how the memory usage of an algorithm grows with input size |
| Best Case | The scenario where the algorithm performs the minimum number of operations |
| Average Case | The expected performance over all possible inputs |
| Worst Case | The scenario where the algorithm performs the maximum number of operations |
| Tail Recursion | Recursion where the recursive call is the last action in the function |
| Hoare Partition | A two-pointer partitioning scheme that converges from both ends |
| Lomuto Partition | A single-pointer partitioning scheme that scans from left to right |
| Pivot Selection | The strategy for choosing the element to partition around |
| Median of Three | A pivot selection strategy that uses the median of the first, middle, and last elements |
| Random Pivot | A pivot selection strategy that randomly selects an element from the array |
| Already Sorted Input | An input where elements are in non-decreasing order |
| Reverse Sorted Input | An input where elements are in non-increasing order |
| Duplicate Elements | Multiple elements with the same value in the array |
| Three-Way Partitioning | Partitioning into less than, equal to, and greater than the pivot |
| Dutch National Flag | Dijkstra's three-way partitioning algorithm |
| Stack Overflow | Error when recursion depth exceeds the system limit |
| Recursion Depth | The number of nested recursive calls at any point |
| Call Stack | The stack that tracks active function calls during execution |
| Base Case | The condition that stops recursion |
| Inductive Hypothesis | The assumption that the algorithm works for smaller inputs |
| Subarray | A contiguous portion of an array |
| Comparison Sort | A sort that uses comparisons to determine element order |
| Lower Bound | The theoretical minimum number of comparisons needed to sort |
| O(n log n) | The time complexity of efficient comparison-based sorting algorithms |
| O(n²) | The time complexity of inefficient sorting algorithms on worst-case input |
| Quadratic Time | Growth rate proportional to the square of input size |
| Logarithmic Time | Growth rate proportional to the logarithm of input size |
| Linear Time | Growth rate proportional to input size |
| Amortized Analysis | Average performance per operation over a worst-case sequence |
| In-place Algorithm | An algorithm that uses constant extra space |
| Extra Space | Additional memory used beyond the input and output |
| Unsorted Array | An array where elements are not in the desired order |
| Sorted Array | An array where elements are in non-decreasing order |
| Ascending Order | Elements arranged from smallest to largest |
| Descending Order | Elements arranged from largest to smallest |
| Algorithm Efficiency | How well an algorithm uses time and space resources |
| Benchmarking | Measuring algorithm performance through timed execution |
| Profiling | Analyzing program performance to identify bottlenecks |
| Optimization | Improving algorithm efficiency without changing correctness |
| Tail Call Optimization | Compiler optimization that reuses stack frames for tail recursion |

## Alphabetical Definitions

### A

**Algorithm Efficiency** — A measure of how well an algorithm utilizes time and space resources to solve a problem. Quick Sort achieves O(n log n) average time with O(log n) space.

**Already Sorted Input** — Data where all elements are in non-decreasing order. This is the worst case for basic Quick Sort implementations that always choose the first element as pivot.

### B

**Base Case** — The condition in a recursive function that stops further recursion. For Quick Sort, this is when the subarray has zero or one elements.

**Benchmarking** — The process of measuring algorithm performance by running timed executions. Useful for comparing Quick Sort against other sorting algorithms.

### C

**Call Stack** — The stack data structure that tracks active function calls during program execution. Each recursive Quick Sort call adds a frame to the call stack.

**Comparison Sort** — A sorting algorithm that determines element order using comparisons. Quick Sort is a comparison-based sort with O(n log n) average complexity.

### D

**Divide and Conquer** — An algorithm paradigm that breaks a problem into smaller subproblems, solves each recursively, and combines the results. Quick Sort exemplifies this approach.

**Dutch National Flag** — Dijkstra's three-way partitioning algorithm that divides elements into three groups: less than, equal to, and greater than the pivot. Useful for handling duplicate elements.

### H

**Hoare Partition** — A two-pointer partitioning scheme where pointers start at opposite ends and converge. Generally more efficient than Lomuto partitioning with fewer swaps.

### I

**Inductive Hypothesis** — The assumption that Quick Sort correctly sorts smaller subarrays. If we assume it works for arrays of size n-1, we prove it works for size n.

**In-place Algorithm** — An algorithm that uses constant extra memory beyond the input. Quick Sort is in-place with O(log n) space for recursion stack.

**In-place Sorting** — Sorting without allocating additional arrays. Quick Sort partitions elements within the original array.

### L

**Logarithmic Time** — Time complexity O(log n) where the number of operations grows logarithmically with input size. Quick Sort achieves this for each partition level.

**Lomuto Partition** — A single-pointer partitioning scheme that scans left to right, maintaining an invariant about elements less than the pivot.

### O

**O(n log n)** — The average-case time complexity of Quick Sort. This is the theoretical lower bound for comparison-based sorting.

**O(n²)** — The worst-case time complexity of Quick Sort, occurring when the pivot selection is consistently poor.

**Optimization** — The process of improving algorithm efficiency. Quick Sort optimizations include better pivot selection, tail recursion, and insertion sort for small subarrays.

### P

**Pivot** — The element chosen to partition the array. Good pivot selection (e.g., median of three) is crucial for Quick Sort performance.

**Pivot Selection** — The strategy for choosing the partition element. Random or median-of-three selection avoids worst-case behavior.

**Profiling** — Analyzing program execution to identify performance bottlenecks. Useful for determining if Quick Sort is the optimal choice for a specific use case.

### Q

**Quadratic Time** — Time complexity O(n²) where operations grow proportionally to the square of input size. This is Quick Sort's worst case.

### R

**Random Pivot** — A pivot selection strategy that chooses a random element from the array. Eliminates worst-case behavior on sorted inputs.

**Recursion** — A function calling itself with a smaller input. Quick Sort recursively sorts subarrays on each side of the pivot.

**Recursion Depth** — The maximum number of nested recursive calls. Quick Sort's depth is O(log n) on average, O(n) worst case.

**Reverse Sorted Input** — Data where elements are in non-increasing order. This can be worst case for naive pivot selection.

### S

**Space Complexity** — The amount of memory an algorithm uses relative to input size. Quick Sort uses O(log n) space for the recursion stack.

**Stack Overflow** — An error that occurs when recursion depth exceeds the call stack limit. Happens with O(n) recursion depth in worst-case Quick Sort.

**Stable Sort** — A sorting algorithm that preserves the relative order of equal elements. Quick Sort is not naturally stable but can be made stable with modifications.

**Subarray** — A contiguous portion of an array. Quick Sort recursively sorts subarrays on each side of the pivot.

### T

**Tail Call Optimization** — A compiler optimization that reuses the stack frame for tail-recursive calls. Can reduce Quick Sort's space complexity to O(1).

**Tail Recursion** — Recursion where the recursive call is the last action. Quick Sort can be implemented with tail recursion for one partition.

**Three-Way Partitioning** — Partitioning elements into three groups: less than, equal to, and greater than the pivot. Handles duplicate elements efficiently.

**Time Complexity** — A measure of how algorithm runtime grows with input size. Quick Sort has O(n log n) average and O(n²) worst case.

### U

**Unstable Sort** — A sorting algorithm that may change the relative order of equal elements. Quick Sort is naturally unstable due to partitioning swaps.

### W

**Worst Case** — The scenario where the algorithm performs the maximum operations. For Quick Sort, this is O(n²) with poor pivot selection.

## Code Examples

### Basic Quick Sort Implementation

```python
def quick_sort(arr, low, high):
    """
    Basic Quick Sort implementation.
    
    Time Complexity: O(n log n) average, O(n²) worst case
    Space Complexity: O(log n) average, O(n) worst case
    
    Args:
        arr: List to sort
        low: Starting index
        high: Ending index
    """
    if low < high:
        # Partition the array and get pivot position
        pivot_index = partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)

def partition(arr, low, high):
    """
    Lomuto partition scheme.
    
    Selects last element as pivot and partitions array
    so elements less than pivot are on the left.
    
    Args:
        arr: Array to partition
        low: Starting index
        high: Ending index
    
    Returns:
        Final position of pivot element
    """
    pivot = arr[high]  # Choose last element as pivot
    i = low - 1        # Index of smaller element
    
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Example usage
arr = [10, 7, 8, 9, 1, 5]
print("Original array:", arr)
quick_sort(arr, 0, len(arr) - 1)
print("Sorted array:", arr)
```

### Median of Three Pivot Selection

```python
def median_of_three(arr, low, high):
    """
    Select pivot as median of first, middle, and last elements.
    
    This improves pivot selection to avoid worst-case scenarios
    on already sorted or reverse sorted arrays.
    
    Args:
        arr: Array to select pivot from
        low: Starting index
        high: Ending index
    
    Returns:
        Index of median element
    """
    mid = (low + high) // 2
    
    # Sort low, mid, high elements
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    
    # Place median at high-1 position for partitioning
    arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
    return arr[high - 1]

def quick_sort_median(arr, low, high):
    """
    Quick Sort with median-of-three pivot selection.
    
    Args:
        arr: Array to sort
        low: Starting index
        high: Ending index
    """
    if low < high:
        if high - low + 1 < 10:
            # Use insertion sort for small subarrays
            insertion_sort(arr, low, high)
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
            
            quick_sort_median(arr, low, i - 1)
            quick_sort_median(arr, i + 1, high)

def insertion_sort(arr, low, high):
    """Helper insertion sort for small subarrays."""
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Example usage
arr = [3, 6, 8, 10, 1, 2, 1]
print("Original array:", arr)
quick_sort_median(arr, 0, len(arr) - 1)
print("Sorted array:", arr)
```

### Random Pivot Quick Sort

```python
import random

def random_partition(arr, low, high):
    """
    Partition using a random pivot element.
    
    Randomly selects pivot and swaps it with the last element
    before using standard Lomuto partition.
    
    Args:
        arr: Array to partition
        low: Starting index
        high: Ending index
    
    Returns:
        Final position of pivot
    """
    # Select random pivot and move to end
    random_idx = random.randint(low, high)
    arr[random_idx], arr[high] = arr[high], arr[random_idx]
    
    return partition(arr, low, high)

def quick_sort_random(arr, low, high):
    """
    Quick Sort with random pivot selection.
    
    Expected time complexity: O(n log n)
    Eliminates worst-case behavior on sorted inputs.
    
    Args:
        arr: Array to sort
        low: Starting index
        high: Ending index
    """
    if low < high:
        pi = random_partition(arr, low, high)
        quick_sort_random(arr, low, pi - 1)
        quick_sort_random(arr, pi + 1, high)

def partition(arr, low, high):
    """Standard Lomuto partition."""
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Example usage
arr = [10, 7, 8, 9, 1, 5, 3, 4, 2, 6]
print("Original array:", arr)
quick_sort_random(arr, 0, len(arr) - 1)
print("Sorted array:", arr)
```

### Three-Way Partition Quick Sort

```python
def three_way_partition(arr, low, high):
    """
    Three-way partition (Dutch National Flag) for handling duplicates.
    
    Partitions array into three regions:
    - Elements less than pivot
    - Elements equal to pivot
    - Elements greater than pivot
    
    Args:
        arr: Array to partition
        low: Starting index
        high: Ending index
    
    Returns:
        Tuple (lt, gt) where:
        - arr[low:lt] < pivot
        - arr[lt:gt+1] == pivot
        - arr[gt+1:high+1] > pivot
    """
    if low > high:
        return low, high
    
    pivot = arr[low]
    lt = low      # arr[low:lt] < pivot
    gt = high     # arr[gt+1:high+1] > pivot
    i = low       # arr[lt:i] == pivot
    
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
    
    return lt, gt

def quick_sort_three_way(arr, low, high):
    """
    Quick Sort with three-way partitioning.
    
    Efficient for arrays with many duplicate elements.
    
    Args:
        arr: Array to sort
        low: Starting index
        high: Ending index
    """
    if low < high:
        lt, gt = three_way_partition(arr, low, high)
        quick_sort_three_way(arr, low, lt - 1)
        quick_sort_three_way(arr, gt + 1, high)

# Example usage
arr = [4, 9, 4, 4, 1, 9, 4, 4, 9, 4, 4, 1, 4]
print("Original array:", arr)
quick_sort_three_way(arr, 0, len(arr) - 1)
print("Sorted array:", arr)
```

### Tail Recursive Quick Sort

```python
def quick_sort_tail_recursive(arr, low, high):
    """
    Quick Sort with tail recursion optimization.
    
    Reduces worst-case space complexity from O(n) to O(log n)
    by recursing only on the smaller partition.
    
    Args:
        arr: Array to sort
        low: Starting index
        high: Ending index
    """
    while low < high:
        pi = partition(arr, low, high)
        
        # Recurse on smaller partition, iterate on larger
        if pi - low < high - pi:
            quick_sort_tail_recursive(arr, low, pi - 1)
            low = pi + 1
        else:
            quick_sort_tail_recursive(arr, pi + 1, high)
            high = pi - 1

def partition(arr, low, high):
    """Standard Lomuto partition."""
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Example usage
arr = [3, 3, 5, 2, 1, 4, 2, 3]
print("Original array:", arr)
quick_sort_tail_recursive(arr, 0, len(arr) - 1)
print("Sorted array:", arr)
```

## Related Terms

- **Merge Sort** — Another divide-and-conquer sort with guaranteed O(n log n) but requires O(n) extra space
- **Heap Sort** — An in-place O(n log n) sort that uses a heap data structure
- **Insertion Sort** — O(n²) sort that's efficient for small or nearly sorted arrays
- **Selection Sort** — Simple O(n²) sort that repeatedly selects the minimum element
- **Bubble Sort** — O(n²) sort that repeatedly swaps adjacent elements
- **Shell Sort** — A generalization of insertion sort that allows exchange of far elements
- **Tim Sort** — A hybrid stable sort combining merge sort and insertion sort
- **Intro Sort** — A hybrid sort combining quick sort, heap sort, and insertion sort
- **Partition** — The core operation that divides the array around a pivot element
- **Recursion** — The programming technique used by Quick Sort for subproblem decomposition
- **Divide and Conquer** — The algorithm paradigm underlying Quick Sort
- **In-place Sorting** — Sorting without significant extra memory allocation
- **Unstable Sort** — A sort that may change relative order of equal elements
- **Pivot Selection** — The strategy for choosing the partition element
- **Median of Three** — A pivot selection strategy using the median of first, middle, and last elements
- **Random Pivot** — A pivot selection strategy that randomly selects an element
- **Three-Way Partitioning** — Partitioning into less than, equal to, and greater than pivot
- **Tail Recursion** — Recursion where the recursive call is the last action
- **Stack Overflow** — Error when recursion depth exceeds system limit
- **Call Stack** — Stack tracking active function calls during execution
- **Base Case** — The condition that stops recursion
- **Amortized Analysis** — Average performance per operation over worst-case sequence
- **Lower Bound** — Theoretical minimum comparisons needed for sorting
- **Comparison Sort** — A sort using comparisons to determine order
- **Worst Case** — Scenario with maximum algorithm operations
- **Best Case** — Scenario with minimum algorithm operations
- **Average Case** — Expected performance over all possible inputs
- **Algorithm Efficiency** — How well an algorithm uses time and space resources
- **Benchmarking** — Measuring algorithm performance through timed execution
- **Profiling** — Analyzing program performance to identify bottlenecks
- **Optimization** — Improving algorithm efficiency without changing correctness
