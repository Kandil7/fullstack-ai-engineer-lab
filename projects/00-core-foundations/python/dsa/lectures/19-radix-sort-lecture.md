# Lecture 19: Radix Sort

> A non-comparison-based sorting algorithm that sorts integers by processing individual digits

## Learning Objectives

By the end of this lecture, you will be able to:
1. Understand the radix sort algorithm and its digit-by-digit approach
2. Implement radix sort using both LSD and MSD variants
3. Analyze time and space complexity
4. Know when radix sort is optimal versus when to use other algorithms
5. Understand the relationship between radix sort and counting sort

## Key Concepts

### What is Radix Sort?

Radix sort is a non-comparison-based sorting algorithm that sorts integers by processing individual digits. It processes digits from least significant to most significant (LSD) or vice versa (MSD), using a stable subroutine (typically counting sort) for each digit.

**Key Insight:** Instead of comparing whole numbers, radix sort sorts by individual digits, achieving O(d × (n + b)) time complexity where d is the number of digits, n is the input size, and b is the base.

### Core Principle

1. **Digit Extraction:** Extract the digit at a specific position
2. **Stable Sort:** Sort elements based on that digit using counting sort
3. **Repeat:** Process all digits from least to most significant

### Why Radix Sort?

- **Speed:** O(d × (n + b)) time complexity
- **Stability:** Maintains relative order of equal elements
- **Simplicity:** Uses counting sort as a subroutine
- **Predictable:** Performance depends on number of digits, not input order

### Limitations

- **Integer Keys Only:** Works with integer (or integer-mapped) keys
- **Base Dependent:** Performance depends on the base used
- **Space:** Requires O(n + b) extra space for counting sort subroutine
- **Digit Processing:** Overhead of extracting and processing digits

## Algorithm Walkthrough

### LSD (Least Significant Digit) Radix Sort

1. **Find Maximum:** Determine the maximum number to know the number of digits
2. **Process Digits:** For each digit position (units, tens, hundreds, ...):
   - Extract the digit at current position
   - Sort elements based on this digit using counting sort
3. **Repeat:** Continue until all digits have been processed

### MSD (Most Significant Digit) Radix Sort

1. **Sort by Most Significant Digit First**
2. **Recursively Sort Subarrays:** For each digit value, recursively sort elements with that prefix
3. **Base Case:** When considering 0 digits or single elements

## Code Examples

### LSD Radix Sort (Base 10)

```python
def radix_sort_lsd(arr):
    """
    LSD Radix Sort for non-negative integers.
    
    Time Complexity: O(d × (n + b)) where d = digits, b = base
    Space Complexity: O(n + b)
    
    Args:
        arr: List of non-negative integers to sort
    
    Returns:
        Sorted list
    """
    if not arr:
        return arr
    
    # Find maximum to determine number of digits
    max_val = max(arr)
    
    # Process each digit position
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr

def counting_sort_by_digit(arr, exp):
    """
    Counting sort subroutine for a specific digit position.
    
    Args:
        arr: Array to sort (modified in-place)
        exp: Current digit position (1, 10, 100, ...)
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # Base 10 digits
    
    # Count occurrences of each digit
    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1
    
    # Compute cumulative counts
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output (backward for stability)
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    # Copy back to original array
    for i in range(n):
        arr[i] = output[i]

# Example usage
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print("Original array:", arr)
sorted_arr = radix_sort_lsd(arr)
print("Sorted array:", sorted_arr)
```

### Radix Sort with Custom Base

```python
def radix_sort_custom_base(arr, base=16):
    """
    Radix sort with configurable base (e.g., hexadecimal).
    
    Args:
        arr: List of non-negative integers to sort
        base: Number base to use (default 16 for hex)
    
    Returns:
        Sorted list
    """
    if not arr:
        return arr
    
    max_val = max(arr)
    
    exp = 1
    while max_val // exp > 0:
        counting_sort_base(arr, exp, base)
        exp *= base
    
    return arr

def counting_sort_base(arr, exp, base):
    """
    Counting sort for specific digit in given base.
    
    Args:
        arr: Array to sort
        exp: Current digit position
        base: Number base
    """
    n = len(arr)
    output = [0] * n
    count = [0] * base
    
    # Count digit occurrences
    for num in arr:
        digit = (num // exp) % base
        count[digit] += 1
    
    # Cumulative counts
    for i in range(1, base):
        count[i] += count[i - 1]
    
    # Build output (backward for stability)
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % base
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    # Copy back
    for i in range(n):
        arr[i] = output[i]

# Example usage
arr = [255, 16, 128, 64, 32, 1, 8, 4]
print("Original array:", arr)
sorted_arr = radix_sort_custom_base(arr, base=16)
print("Sorted array (base 16):", sorted_arr)
```

### MSD Radix Sort

```python
def radix_sort_msd(arr):
    """
    MSD Radix Sort for non-negative integers.
    
    Processes digits from most significant to least significant.
    
    Args:
        arr: List of non-negative integers to sort
    
    Returns:
        Sorted list
    """
    if not arr:
        return arr
    
    max_val = max(arr)
    max_digits = len(str(max_val))
    
    msd_sort(arr, 0, len(arr), max_digits - 1)
    return arr

def msd_sort(arr, start, end, digit_pos):
    """
    Recursive MSD sort for a specific digit position.
    
    Args:
        arr: Array to sort
        start: Starting index
        end: Ending index (exclusive)
        digit_pos: Current digit position (0 = most significant)
    """
    if start >= end - 1 or digit_pos < 0:
        return
    
    # Counting sort for current digit
    count = [0] * 10
    output = [0] * (end - start)
    
    # Count occurrences
    for i in range(start, end):
        digit = (arr[i] // (10 ** digit_pos)) % 10
        count[digit] += 1
    
    # Cumulative counts
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output
    for i in range(end - 1, start - 1, -1):
        digit = (arr[i] // (10 ** digit_pos)) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    # Copy back
    for i in range(start, end):
        arr[i] = output[i - start]
    
    # Recursively sort subarrays
    for i in range(9):
        msd_sort(arr, start + count[i], start + count[i + 1], digit_pos - 1)

# Example usage
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print("Original array:", arr)
sorted_arr = radix_sort_msd(arr)
print("Sorted array:", sorted_arr)
```

### Radix Sort for Negative Numbers

```python
def radix_sort_negative(arr):
    """
    Radix sort that handles negative numbers.
    
    Separates negative and non-negative numbers, sorts each,
    then combines results.
    
    Args:
        arr: List of integers (including negatives) to sort
    
    Returns:
        Sorted list
    """
    if not arr:
        return []
    
    # Separate negative and non-negative
    negatives = [-x for x in arr if x < 0]
    non_negatives = [x for x in arr if x >= 0]
    
    # Sort absolute values of negatives (in reverse)
    if negatives:
        negatives = radix_sort_lsd(negatives)
        negatives = [-x for x in reversed(negatives)]
    
    # Sort non-negatives
    if non_negatives:
        non_negatives = radix_sort_lsd(non_negatives)
    
    return negatives + non_negatives

# Example usage
arr = [-5, -1, -3, 2, 4, -2, 1, 0]
print("Original array:", arr)
sorted_arr = radix_sort_negative(arr)
print("Sorted array:", sorted_arr)
```

### Optimized Radix Sort

```python
def radix_sort_optimized(arr, base=256):
    """
    Optimized radix sort using larger base for fewer passes.
    
    Args:
        arr: List of non-negative integers to sort
        base: Base for sorting (256 for byte-level sorting)
    
    Returns:
        Sorted list
    """
    if not arr:
        return arr
    
    max_val = max(arr)
    
    # Calculate number of passes needed
    passes = 0
    temp = max_val
    while temp > 0:
        passes += 1
        temp //= base
    
    # Process each digit
    exp = 1
    for _ in range(passes):
        counting_sort_base(arr, exp, base)
        exp *= base
    
    return arr

def counting_sort_base(arr, exp, base):
    """Counting sort for specific digit in given base."""
    n = len(arr)
    output = [0] * n
    count = [0] * base
    
    for num in arr:
        digit = (num // exp) % base
        count[digit] += 1
    
    for i in range(1, base):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % base
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    for i in range(n):
        arr[i] = output[i]

# Example usage
arr = [1000000, 500000, 100000, 50000, 10000, 5000, 1000]
print("Original array:", arr)
sorted_arr = radix_sort_optimized(arr, base=256)
print("Sorted array:", sorted_arr)
```

### Radix Sort with String Keys

```python
def radix_sort_strings(arr, max_len=None):
    """
    Radix sort for strings of equal length.
    
    Sorts lexicographically by processing characters from right to left.
    
    Args:
        arr: List of strings to sort
        max_len: Maximum string length (if None, uses max length in array)
    
    Returns:
        Sorted list
    """
    if not arr:
        return []
    
    if max_len is None:
        max_len = max(len(s) for s in arr)
    
    # Pad strings to equal length
    arr = [s.ljust(max_len) for s in arr]
    
    # Process each character position
    for pos in range(max_len - 1, -1, -1):
        counting_sort_by_char(arr, pos)
    
    # Remove padding
    return [s.rstrip() for s in arr]

def counting_sort_by_char(arr, pos):
    """Counting sort by character at specific position."""
    n = len(arr)
    output = [0] * n
    count = [0] * 256  # ASCII characters
    
    # Count occurrences
    for s in arr:
        char_code = ord(s[pos])
        count[char_code] += 1
    
    # Cumulative counts
    for i in range(1, 256):
        count[i] += count[i - 1]
    
    # Build output (backward for stability)
    for i in range(n - 1, -1, -1):
        char_code = ord(arr[i][pos])
        output[count[char_code] - 1] = arr[i]
        count[char_code] -= 1
    
    # Copy back
    for i in range(n):
        arr[i] = output[i]

# Example usage
arr = ["banana", "apple", "cherry", "date", "fig"]
print("Original array:", arr)
sorted_arr = radix_sort_strings(arr)
print("Sorted array:", sorted_arr)
```

## Common Mistakes

### Mistake 1: Not Using Stable Sort
```python
# WRONG: Using unstable sort breaks radix sort
def radix_sort_wrong(arr):
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        # Unstable sort will break the algorithm
        arr.sort(key=lambda x: (x // exp) % 10)  # Python's sort is stable, but...
        exp *= 10
    return arr

# CORRECT: Always use stable sort (counting sort)
def radix_sort_correct(arr):
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)  # Stable counting sort
        exp *= 10
    return arr
```

### Mistake 2: Wrong Digit Extraction
```python
# WRONG: Incorrect digit extraction
digit = (num // exp) % 10  # If exp is not power of 10

# CORRECT: Ensure exp is always power of base
exp = 1
while max_val // exp > 0:
    digit = (num // exp) % base
    exp *= base
```

### Mistake 3: Not Handling Zero Correctly
```python
# WRONG: Assuming all numbers have same number of digits
# This works but is inefficient

# CORRECT: Process only necessary digits
max_val = max(arr)
exp = 1
while max_val // exp > 0:  # Stop when no more digits
    counting_sort_by_digit(arr, exp)
    exp *= 10
```

### Mistake 4: Forgetting to Copy Back
```python
# WRONG: Not copying output back to original array
def counting_sort_wrong(arr, exp):
    output = [0] * len(arr)
    count = [0] * 10
    # ... counting and placing logic ...
    # Missing: for i in range(len(arr)): arr[i] = output[i]

# CORRECT: Always copy output back
def counting_sort_correct(arr, exp):
    output = [0] * len(arr)
    count = [0] * 10
    # ... counting and placing logic ...
    for i in range(len(arr)):
        arr[i] = output[i]
```

## Best Practices

1. **Use Stable Sort:** Always use counting sort as the subroutine
2. **Choose Right Base:** Larger base (256) means fewer passes but more space
3. **Handle Edge Cases:** Empty arrays, single elements, already sorted
4. **Optimize for Range:** Use appropriate base based on value range
5. **Consider MSD vs LSD:** MSD can be faster for certain data patterns
6. **Test Thoroughly:** Include edge cases and performance tests
7. **Document Assumptions:** Clearly state input requirements

## Complexity Analysis

| Case | Time | Space | Notes |
|------|------|-------|-------|
| Best | O(d × (n + b)) | O(n + b) | d = digits, b = base |
| Average | O(d × (n + b)) | O(n + b) | Consistent performance |
| Worst | O(d × (n + b)) | O(n + b) | Performance depends on digit count |

- **n** = number of elements
- **d** = number of digits in maximum element
- **b** = base (10 for decimal, 256 for byte-level)

**When to use radix sort:**
- Integer keys with bounded number of digits
- Need stable sorting
- Large datasets where O(n log n) is too slow
- When parallelization is possible

**When NOT to use radix sort:**
- Floating-point numbers (without conversion)
- Very large ranges with few elements
- Memory is severely constrained
- String keys with variable length

## Exercises

### Exercise 1: LSD Radix Sort Implementation
**Problem:** Implement LSD radix sort from scratch without using Python's built-in sort.

### Exercise 2: MSD Radix Sort
**Problem:** Implement MSD radix sort and compare performance with LSD version.

### Exercise 3: Custom Base Radix Sort
**Problem:** Implement radix sort with base 2 (binary) and test with large numbers.

### Exercise 4: Radix Sort for Floats
**Problem:** Adapt radix sort to handle floating-point numbers by converting to integers.

### Exercise 5: Performance Benchmark
**Problem:** Benchmark radix sort against quick sort and merge sort on various input sizes.

## Summary

Radix sort is a powerful non-comparison-based sorting algorithm that processes digits individually. Key takeaways:

- **Best for:** Integer keys with bounded digit count
- **Time complexity:** O(d × (n + b)) where d = digits, b = base
- **Space complexity:** O(n + b)
- **Stability:** Yes, when using stable subroutine
- **Variants:** LSD (least significant digit) and MSD (most significant digit)

Understanding radix sort provides insight into digit-based sorting and is fundamental for understanding more advanced algorithms like burstsort.

## Next Steps

- **Lecture 20:** Merge Sort (comparison-based but stable and O(n log n))
- **Practice:** Implement both LSD and MSD variants
- **Explore:** Burstsort and other string sorting algorithms
