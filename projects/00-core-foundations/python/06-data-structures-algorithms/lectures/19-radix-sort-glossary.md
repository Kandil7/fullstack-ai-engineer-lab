# Radix Sort — Glossary

> **Quick Reference Table**

| Term | Definition |
|------|-----------|
| Radix Sort | A non-comparison-based sorting algorithm that sorts by processing individual digits |
| LSD Radix Sort | Least Significant Digit radix sort - processes digits from right to left |
| MSD Radix Sort | Most Significant Digit radix sort - processes digits from left to right |
| Base | The number of unique digits in the number system used for sorting |
| Digit | A single symbol in a number system |
| Digit Position | The place value of a digit (units, tens, hundreds, etc.) |
| Stable Sort | A sorting algorithm that preserves relative order of equal elements |
| Non-Comparison Sort | A sorting algorithm that doesn't compare elements to determine order |
| Counting Sort | A subroutine used by radix sort for each digit position |
| Digit Extraction | The process of isolating a specific digit from a number |
| Place Value | The value of a digit based on its position in a number |
| Number System | A system for representing numbers (binary, decimal, hexadecimal) |
| Binary | Base-2 number system with digits 0 and 1 |
| Decimal | Base-10 number system with digits 0-9 |
| Hexadecimal | Base-16 number system with digits 0-9 and A-F |
| Byte | 8-bit binary number (base-256 possible values) |
| Pass | One complete processing of all elements for a specific digit position |
| Digit Count | The number of digits in the maximum element |
| Range | The difference between maximum and minimum values |
| Non-Negative Integers | Whole numbers greater than or equal to zero |
| Negative Numbers | Numbers less than zero |
| String Sorting | Sorting strings lexicographically using character codes |
| ASCII | American Standard Code for Information Interchange |
| Character Code | Numeric representation of a character |
| In-place Sorting | Sorting without significant extra memory |
| Auxiliary Space | Extra memory used by an algorithm |
| Linear Time | Time complexity O(n) where operations grow proportionally |
| Digit-based Sort | Sorting algorithm that processes individual digits |
| Prefix Sort | MSD radix sort approach |
| Suffix Sort | LSD radix sort approach |
| Bucket | Container for elements with same digit value |
| Stable Subroutine | A sorting algorithm used by radix sort that preserves order |
| Digit Processing | Extracting and using individual digits for sorting |
| Number Representation | How numbers are expressed in different bases |
| Bit Manipulation | Operations on individual binary digits |
| Modular Arithmetic | Operations using modulo to extract digits |
| Integer Division | Division that discards remainder, used for digit extraction |
| Overflow | When a number exceeds the maximum representable value |
| Underflow | When a number is too small to represent accurately |
| Performance Optimization | Improving algorithm efficiency |
| Benchmarking | Measuring algorithm performance |
| Algorithm Complexity | Growth rate of runtime or space with input size |
| Input Validation | Checking that input meets algorithm requirements |
| Edge Cases | Special input cases requiring special handling |
| Empty Array | An array with zero elements |
| Single Element | An array with exactly one element |
| Already Sorted | Elements in non-decreasing order |
| Reverse Sorted | Elements in non-increasing order |
| Duplicate Elements | Multiple elements with the same value |

## Alphabetical Definitions

### B

**Base** — The number of unique digits in a number system. Radix sort uses base-10 (decimal) by default, but can use any base (2 for binary, 16 for hex, 256 for byte-level).

**Binary** — Base-2 number system with digits 0 and 1. Radix sort can use base-2 for bit-level sorting.

**Bit Manipulation** — Operations on individual binary digits. Can be used to optimize digit extraction.

**Bucket** — Container for elements with the same digit value at a specific position. Each digit value maps to a bucket.

**Byte** — 8-bit binary number representing values 0-255. Base-256 radix sort processes one byte at a time.

### D

**Decimal** — Base-10 number system with digits 0-9. The most common base for human-readable numbers.

**Digit** — A single symbol in a number system. Radix sort processes numbers digit by digit.

**Digit Count** — The number of digits in the maximum element. Determines how many passes radix sort needs.

**Digit Extraction** — The process of isolating a specific digit from a number. Done using division and modulo operations.

**Digit Position** — The place value of a digit (units, tens, hundreds, etc.). LSD starts from position 0.

**Digit-based Sort** — A sorting algorithm that processes individual digits rather than comparing whole numbers. Radix sort is a digit-based sort.

### H

**Hexadecimal** — Base-16 number system with digits 0-9 and A-F. Useful for compact representation of binary data.

### I

**In-place Sorting** — Sorting without significant extra memory. Radix sort is NOT in-place (requires O(n + b) space).

**Input Validation** — Checking that input meets algorithm requirements. Radix sort requires non-negative integers.

**Integer Division** — Division that discards remainder. Used to shift digit position: `num // exp`.

**Integer Sorting** — Sorting algorithms designed for integer keys. Radix sort is an integer sorting algorithm.

### L

**Least Significant Digit** — The rightmost digit in a number (units place). LSD radix sort processes from right to left.

**Linear Time** — Time complexity O(n). Radix sort is O(d × (n + b)) which is linear when d and b are constants.

### M

**Most Significant Digit** — The leftmost digit in a number. MSD radix sort processes from left to right.

**Modular Arithmetic** — Operations using modulo to extract digits: `num % base` gives the last digit.

### N

**Non-Comparison Sort** — A sorting algorithm that doesn't compare elements. Radix sort uses digit-based placement instead.

**Non-Negative Integers** — Whole numbers ≥ 0. Basic radix sort requires these.

**Number Representation** — How numbers are expressed in different bases. Affects digit extraction logic.

**Number System** — A system for representing numbers (binary, decimal, hexadecimal). Determines the base for radix sort.

### P

**Pass** — One complete processing of all elements for a specific digit position. Radix sort makes d passes for d digits.

**Place Value** — The value of a digit based on its position. Position i has value base^i.

**Prefix Sort** — Another name for MSD radix sort. Sorts by processing from most significant digit first.

### R

**Radix Sort** — A non-comparison-based sorting algorithm that sorts by processing individual digits from least to most significant.

**Range** — The difference between maximum and minimum values. Affects the efficiency of radix sort.

**Reverse Sorted** — Elements in non-increasing order. Radix sort handles this efficiently.

### S

**String Sorting** — Sorting strings lexicographically using character codes. Radix sort can sort strings by processing characters.

**Stable Sort** — A sorting algorithm that preserves relative order of equal elements. Radix sort requires a stable subroutine.

**Stable Subroutine** — A sorting algorithm used by radix sort that preserves order. Counting sort is typically used.

**Suffix Sort** — Another name for LSD radix sort. Sorts by processing from least significant digit first.

### U

**Underflow** — When a number is too small to represent accurately. Not typically an issue for integer radix sort.

### V

**Value Range** — The span from minimum to maximum value. Affects count array size in the counting sort subroutine.

## Code Examples

### Basic LSD Radix Sort

```python
def radix_sort_lsd(arr):
    """
    LSD Radix Sort for non-negative integers.
    
    Time Complexity: O(d × (n + b))
    Space Complexity: O(n + b)
    
    Args:
        arr: List of non-negative integers
    
    Returns:
        Sorted list
    """
    if not arr:
        return arr
    
    max_val = max(arr)
    exp = 1
    
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr

def counting_sort_by_digit(arr, exp):
    """Counting sort for a specific digit position."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    for i in range(n):
        arr[i] = output[i]

# Example usage
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print("Sorted:", radix_sort_lsd(arr))
```

### MSD Radix Sort

```python
def radix_sort_msd(arr):
    """MSD Radix Sort for non-negative integers."""
    if not arr:
        return arr
    
    max_val = max(arr)
    max_digits = len(str(max_val))
    
    msd_sort(arr, 0, len(arr), max_digits - 1)
    return arr

def msd_sort(arr, start, end, digit_pos):
    """Recursive MSD sort for specific digit position."""
    if start >= end - 1 or digit_pos < 0:
        return
    
    count = [0] * 10
    output = [0] * (end - start)
    
    for i in range(start, end):
        digit = (arr[i] // (10 ** digit_pos)) % 10
        count[digit] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(end - 1, start - 1, -1):
        digit = (arr[i] // (10 ** digit_pos)) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    for i in range(start, end):
        arr[i] = output[i - start]
    
    for i in range(9):
        msd_sort(arr, start + count[i], start + count[i + 1], digit_pos - 1)

# Example usage
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print("Sorted:", radix_sort_msd(arr))
```

### Custom Base Radix Sort

```python
def radix_sort_custom_base(arr, base=16):
    """Radix sort with configurable base (e.g., hexadecimal)."""
    if not arr:
        return arr
    
    max_val = max(arr)
    exp = 1
    
    while max_val // exp > 0:
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
arr = [255, 16, 128, 64, 32, 1, 8, 4]
print("Sorted (base 16):", radix_sort_custom_base(arr, 16))
```

### Radix Sort for Negative Numbers

```python
def radix_sort_negative(arr):
    """Radix sort that handles negative numbers."""
    if not arr:
        return []
    
    negatives = [-x for x in arr if x < 0]
    non_negatives = [x for x in arr if x >= 0]
    
    if negatives:
        negatives = radix_sort_lsd(negatives)
        negatives = [-x for x in reversed(negatives)]
    
    if non_negatives:
        non_negatives = radix_sort_lsd(non_negatives)
    
    return negatives + non_negatives

# Example usage
arr = [-5, -1, -3, 2, 4, -2, 1, 0]
print("Sorted:", radix_sort_negative(arr))
```

## Related Terms

- **Counting Sort** — Subroutine used by radix sort for each digit
- **Bucket Sort** — Another distribution-based sorting algorithm
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
- **Base** — Number of unique digits in number system
- **Digit** — Single symbol in number system
- **Digit Position** — Place value of digit
- **Digit Extraction** — Isolating specific digit
- **Place Value** — Value based on position
- **Number System** — System for representing numbers
- **Binary** — Base-2 system
- **Decimal** — Base-10 system
- **Hexadecimal** — Base-16 system
- **Byte** — 8-bit binary number
- **Pass** — Complete processing for one digit
- **Digit Count** — Number of digits in max element
- **Range** — Difference between max and min
- **LSD Radix Sort** — Least significant digit first
- **MSD Radix Sort** — Most significant digit first
- **Prefix Sort** — MSD approach
- **Suffix Sort** — LSD approach
- **Bucket** — Container for same-digit elements
- **Stable Subroutine** — Sorting algorithm preserving order
- **Digit Processing** — Extracting and using digits
- **Number Representation** — Expressing numbers in bases
- **Bit Manipulation** — Operations on binary digits
- **Modular Arithmetic** — Operations using modulo
- **Integer Division** — Division discarding remainder
- **Overflow** — Exceeding maximum value
- **Underflow** — Too small to represent
- **Performance Optimization** — Improving efficiency
- **Benchmarking** — Measuring performance
- **Algorithm Complexity** — Growth rate of runtime/space
- **Input Validation** — Checking requirements
- **Edge Cases** — Special input cases
- **Empty Array** — Array with zero elements
- **Single Element** — Array with one element
- **Already Sorted** — Elements in order
- **Reverse Sorted** — Elements in reverse order
- **Duplicate Elements** — Multiple same values
