# Counting Sort — Glossary

> **Quick Reference Table**

| Term | Definition |
|------|-----------|
| Counting Sort | A non-comparison-based sorting algorithm that counts occurrences of each element |
| Non-Comparison Sort | A sorting algorithm that doesn't compare elements to determine order |
| Count Array | An auxiliary array that stores the frequency of each element |
| Cumulative Count | Running total of counts used to determine element positions |
| Prefix Sum | Cumulative sum of elements in an array |
| Range | The difference between maximum and minimum values in the input |
| Stable Sort | A sorting algorithm that preserves the relative order of equal elements |
| In-place Sorting | Sorting without requiring additional memory proportional to input size |
| Distribution Sort | A sorting algorithm that distributes elements into buckets based on values |
| Integer Sorting | Sorting algorithms designed specifically for integer keys |
| Key | The value used to determine the sort order of elements |
| Auxiliary Space | Extra memory used by an algorithm beyond the input |
| Linear Time | Time complexity O(n) where operations grow proportionally with input size |
| Non-Negative Integers | Whole numbers greater than or equal to zero |
| Negative Numbers | Numbers less than zero |
| Value Range | The span from minimum to maximum value in the dataset |
| Frequency | The number of times an element appears in the array |
| Stable Algorithm | An algorithm that maintains relative order of equal elements |
| Unstable Algorithm | An algorithm that may change relative order of equal elements |
| Digit | A single symbol in a number system |
| Base | The number of unique digits in a number system (e.g., base 10) |
| Radix | The base of a number system used in radix sort |
| Bucket | A container for elements with similar values |
| Array Indexing | Accessing elements by their position in an array |
| Backward Traversal | Iterating through an array from last to first element |
| Forward Traversal | Iterating through an array from first to last element |
| Edge Cases | Special input cases that require special handling |
| Empty Array | An array with zero elements |
| Single Element | An array with exactly one element |
| Already Sorted | An array where elements are in non-decreasing order |
| Duplicate Elements | Multiple elements with the same value |
| Memory Allocation | Reserving memory space for data structures |
| Time Complexity | A measure of how algorithm runtime grows with input size |
| Space Complexity | A measure of how memory usage grows with input size |
| Best Case | The scenario with minimum algorithm operations |
| Worst Case | The scenario with maximum algorithm operations |
| Average Case | Expected performance over all possible inputs |
| Input Validation | Checking that input meets algorithm requirements |
| Performance Optimization | Improving algorithm efficiency |
| Benchmarking | Measuring algorithm performance through timed execution |
| Algorithm Design | The process of creating step-by-step problem solutions |
| Data Structure | A way of organizing data for efficient access and modification |
| Sorting Algorithm | An algorithm that arranges elements in a specific order |
| Comparison-Based Sort | A sort using comparisons to determine element order |
| Lower Bound | Theoretical minimum comparisons needed for sorting |
| O(n log n) | Time complexity of efficient comparison-based sorts |
| O(n + k) | Time complexity of counting sort where k is value range |
| Integer Mapping | Converting non-integer keys to integer indices |
| Shift Operation | Adding a constant to convert negative numbers to non-negative |
| Cumulative Sum | Running total calculated by adding each element to the sum of predecessors |
| Output Array | The array containing sorted elements |
| Original Array | The input array before sorting |

## Alphabetical Definitions

### A

**Algorithm Design** — The process of creating step-by-step solutions to computational problems. Counting sort is designed for efficient integer sorting.

**Already Sorted** — An array where elements are in non-decreasing order. Counting sort handles this efficiently with O(n + k) time.

**Array Indexing** — Accessing elements by their position in an array. Counting sort uses values as indices in the count array.

### B

**Backward Traversal** — Iterating through an array from last to first element. Used in counting sort to preserve stability.

**Base** — The number of unique digits in a number system. Counting sort assumes base-10 integers by default.

**Best Case** — The scenario with minimum algorithm operations. For counting sort, this is always O(n + k) regardless of input order.

**Bucket** — A container for elements with similar values. Counting sort effectively creates buckets for each unique value.

### C

**Comparison-Based Sort** — A sorting algorithm that uses comparisons to determine element order. Counting sort is NOT comparison-based.

**Count Array** — An auxiliary array that stores the frequency of each element. Its size is determined by the value range.

**Counting Sort** — A non-comparison-based sorting algorithm that counts occurrences of each element to determine positions.

**Cumulative Count** — Running total of counts used to determine element positions. Transforms frequency counts into position information.

**Cumulative Sum** — Running total calculated by adding each element to the sum of predecessors. Same as cumulative count.

### D

**Digit** — A single symbol in a number system. Counting sort can be adapted for digit-level sorting.

**Distribution Sort** — A sorting algorithm that distributes elements into buckets based on values. Counting sort is a type of distribution sort.

### E

**Edge Cases** — Special input cases requiring special handling. Counting sort needs handling for empty arrays and single elements.

**Empty Array** — An array with zero elements. Counting sort should return immediately for empty input.

### F

**Forward Traversal** — Iterating through an array from first to last element. Forward traversal in counting sort may break stability.

**Frequency** — The number of times an element appears in the array. The count array stores frequencies.

### I

**In-place Sorting** — Sorting without significant extra memory. Counting sort is NOT in-place (requires O(n + k) space).

**Input Validation** — Checking that input meets algorithm requirements. Counting sort validates non-negative integers.

**Integer Mapping** — Converting non-integer keys to integer indices. Used to adapt counting sort for non-integer data.

**Integer Sorting** — Sorting algorithms designed specifically for integer keys. Counting sort is an integer sorting algorithm.

### L

**Linear Time** — Time complexity O(n) where operations grow proportionally with input size. Counting sort is O(n + k).

**Lower Bound** — Theoretical minimum comparisons needed for sorting. Counting sort bypasses this by not using comparisons.

### M

**Memory Allocation** — Reserving memory space for data structures. Counting sort allocates count and output arrays.

### N

**Negative Numbers** — Numbers less than zero. Counting sort can handle negatives by shifting the range.

**Non-Comparison Sort** — A sorting algorithm that doesn't compare elements. Counting sort uses arithmetic instead.

**Non-Negative Integers** — Whole numbers greater than or equal to zero. The basic version of counting sort requires these.

### O

**O(n + k)** — Time complexity of counting sort where n is input size and k is value range. Linear when k = O(n).

**O(n log n)** — Time complexity of comparison-based sorts. Counting sort can be faster when k is small.

### P

**Performance Optimization** — Improving algorithm efficiency. Counting sort optimizations include reusing arrays and early termination.

**Prefix Sum** — Cumulative sum of elements. Same as cumulative count in counting sort context.

### R

**Radix** — The base of a number system. Counting sort is used as a subroutine in radix sort.

**Range** — The difference between maximum and minimum values. Determines the size of the count array.

### S

**Shift Operation** — Adding a constant to convert negative numbers to non-negative. Enables counting sort for negative inputs.

**Single Element** — An array with exactly one element. Already sorted, can return immediately.

**Space Complexity** — The amount of memory an algorithm uses. Counting sort is O(n + k).

**Stable Algorithm** — An algorithm that maintains relative order of equal elements. Counting sort is stable when implemented correctly.

**Stable Sort** — A sorting algorithm that preserves relative order of equal elements. Important for multi-key sorting.

### T

**Time Complexity** — A measure of how algorithm runtime grows with input size. Counting sort is O(n + k).

### U

**Unstable Algorithm** — An algorithm that may change relative order of equal elements. Improper counting sort implementation can be unstable.

### V

**Value Range** — The span from minimum to maximum value. Determines count array size and algorithm efficiency.

## Code Examples

### Basic Counting Sort Implementation

```python
def counting_sort(arr):
    """
    Basic counting sort for non-negative integers.
    
    Time Complexity: O(n + k) where k is the range
    Space Complexity: O(n + k)
    
    Args:
        arr: List of non-negative integers
    
    Returns:
        Sorted list
    """
    if not arr:
        return []
    
    max_val = max(arr)
    count = [0] * (max_val + 1)
    
    # Count occurrences
    for num in arr:
        count[num] += 1
    
    # Build sorted array
    sorted_arr = []
    for i in range(len(count)):
        sorted_arr.extend([i] * count[i])
    
    return sorted_arr

# Example usage
arr = [4, 2, 2, 8, 3, 3, 1]
print("Original:", arr)
print("Sorted:", counting_sort(arr))
```

### Cumulative Count Version

```python
def counting_sort_cumulative(arr):
    """
    Counting sort using cumulative counts for direct placement.
    
    Args:
        arr: List of non-negative integers
    
    Returns:
        Sorted list
    """
    if not arr:
        return []
    
    max_val = max(arr)
    count = [0] * (max_val + 1)
    
    # Count occurrences
    for num in arr:
        count[num] += 1
    
    # Compute cumulative counts
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    # Build output (backward for stability)
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i]] - 1] = arr[i]
        count[arr[i]] -= 1
    
    return output

# Example usage
arr = [3, 1, 4, 1, 5, 9, 2, 6]
print("Sorted:", counting_sort_cumulative(arr))
```

### Handling Negative Numbers

```python
def counting_sort_negative(arr):
    """
    Counting sort that handles negative numbers.
    
    Args:
        arr: List of integers (including negatives)
    
    Returns:
        Sorted list
    """
    if not arr:
        return []
    
    min_val = min(arr)
    max_val = max(arr)
    shift = -min_val
    range_size = max_val - min_val + 1
    
    count = [0] * range_size
    for num in arr:
        count[num + shift] += 1
    
    sorted_arr = []
    for i in range(range_size):
        sorted_arr.extend([i - shift] * count[i])
    
    return sorted_arr

# Example usage
arr = [-3, -1, -4, 2, 0, -2, 1]
print("Sorted:", counting_sort_negative(arr))
```

### Stability Demonstration

```python
def counting_sort_stable(arr):
    """
    Stable counting sort implementation.
    
    Preserves relative order of equal elements.
    
    Args:
        arr: List of non-negative integers
    
    Returns:
        Sorted list (stable)
    """
    if not arr:
        return []
    
    max_val = max(arr)
    count = [0] * (max_val + 1)
    
    for num in arr:
        count[num] += 1
    
    # Cumulative counts
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    # Backward traversal for stability
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i]] - 1] = arr[i]
        count[arr[i]] -= 1
    
    return output

# Stability test
arr = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd')]
# Sort by first element
sorted_arr = counting_sort_stable([x[0] for x in arr])
print("Stable sort preserves order of equal elements")
```

## Related Terms

- **Radix Sort** — Uses counting sort as a subroutine for each digit
- **Bucket Sort** — Distributes elements into buckets, then sorts each bucket
- **Quick Sort** — Comparison-based sort with O(n log n) average time
- **Merge Sort** — Stable comparison-based sort with O(n log n) time
- **Insertion Sort** — Simple O(n²) sort for small arrays
- **Selection Sort** — Simple O(n²) sort that selects minimums
- **Bubble Sort** — Simple O(n²) sort with repeated swaps
- **Heap Sort** — In-place O(n log n) sort using heap data structure
- **Tim Sort** — Hybrid sort combining merge sort and insertion sort
- **Intro Sort** — Hybrid sort combining quicksort, heapsort, and insertion sort
- **Shell Sort** — Generalization of insertion sort for distant elements
- **Non-Comparison Sort** — Sorting without element comparisons
- **Distribution Sort** — Sorting by distributing into value-based buckets
- **Integer Sorting** — Algorithms designed for integer keys
- **Stable Sort** — Preserves relative order of equal elements
- **In-place Algorithm** — Uses constant extra space
- **Auxiliary Space** — Extra memory beyond input
- **Time Complexity** — Growth rate of runtime with input size
- **Space Complexity** — Growth rate of memory usage with input size
- **Linear Time** — O(n) complexity
- **Non-Negative Integers** — Whole numbers ≥ 0
- **Negative Numbers** — Numbers < 0
- **Value Range** — Span from min to max value
- **Frequency** — Count of element occurrences
- **Cumulative Count** — Running total of frequencies
- **Prefix Sum** — Cumulative sum of array elements
- **Count Array** — Stores element frequencies
- **Output Array** — Contains sorted results
- **Backward Traversal** — Iterating from end to start
- **Forward Traversal** — Iterating from start to end
- **Stable Algorithm** — Maintains equal element order
- **Unstable Algorithm** — May change equal element order
- **Edge Cases** — Special input requiring handling
- **Empty Array** — Array with zero elements
- **Single Element** — Array with one element
- **Already Sorted** — Elements in non-decreasing order
- **Duplicate Elements** — Multiple same-valued elements
- **Memory Allocation** — Reserving memory space
- **Input Validation** — Checking input requirements
- **Performance Optimization** — Improving efficiency
- **Benchmarking** — Measuring performance
- **Algorithm Design** — Creating problem solutions
- **Data Structure** — Organizing data efficiently
- **Sorting Algorithm** — Arranging elements in order
- **Comparison-Based Sort** — Uses comparisons for ordering
- **Lower Bound** — Minimum comparisons needed
- **O(n log n)** — Comparison sort complexity
- **O(n + k)** — Counting sort complexity
- **Integer Mapping** — Converting keys to indices
- **Shift Operation** — Converting negatives to non-negative
