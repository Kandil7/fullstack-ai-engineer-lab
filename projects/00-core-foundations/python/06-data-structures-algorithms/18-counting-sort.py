"""
DSA Tutorial 18 - Counting Sort
================================

Counting Sort: Non-comparison based sort for integers.
Count occurrences of each element, then place them in order.

Time Complexity: O(n + k) where k = range of input
Space Complexity: O(n + k)
Stable: Yes
When to use: Small range of integer values
"""

# =============================================================================
# 1. BASIC COUNTING SORT
# =============================================================================

def counting_sort(arr):
    """Basic counting sort for non-negative integers"""
    if not arr:
        return arr

    max_val = max(arr)
    count = [0] * (max_val + 1)

    # Count occurrences
    for num in arr:
        count[num] += 1

    # Build sorted array
    sorted_arr = []
    for i, c in enumerate(count):
        sorted_arr.extend([i] * c)

    return sorted_arr

print("=== Basic Counting Sort ===")
arr = [4, 2, 2, 8, 3, 3, 1]
print(f"Original: {arr}")
print(f"Sorted: {counting_sort(arr)}")


# =============================================================================
# 2. COUNTING SORT WITH NEGATIVES
# =============================================================================

def counting_sort_with_negatives(arr):
    """Counting sort handling negative numbers"""
    if not arr:
        return arr

    min_val = min(arr)
    max_val = max(arr)
    range_val = max_val - min_val + 1

    count = [0] * range_val
    output = [0] * len(arr)

    # Count occurrences
    for num in arr:
        count[num - min_val] += 1

    # Cumulative count
    for i in range(1, range_val):
        count[i] += count[i - 1]

    # Build output (stable - traverse backwards)
    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1

    return output

print("\n=== Counting Sort with Negatives ===")
arr = [-5, -1, 3, -3, 0, 4, 2, -2]
print(f"Original: {arr}")
print(f"Sorted: {counting_sort_with_negatives(arr)}")


# =============================================================================
# 3. STABLE COUNTING SORT
# =============================================================================

def counting_sort_stable(arr):
    """Stable counting sort - preserves relative order"""
    if not arr:
        return arr

    max_val = max(arr)
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1

    # Cumulative count
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    output = [0] * len(arr)

    # Traverse backwards for stability
    for num in reversed(arr):
        output[count[num] - 1] = num
        count[num] -= 1

    return output

print("\n=== Stable Counting Sort ===")
arr = [4, 2, 2, 8, 3, 3, 1]
print(f"Original: {arr}")
print(f"Stable sorted: {counting_sort_stable(arr)}")


# =============================================================================
# 4. COUNTING SORT FOR RANGE [0, k]
# =============================================================================

def counting_sort_range(arr, k):
    """Counting sort for range [0, k]"""
    count = [0] * (k + 1)

    for num in arr:
        if 0 <= num <= k:
            count[num] += 1

    sorted_arr = []
    for i, c in enumerate(count):
        sorted_arr.extend([i] * c)

    return sorted_arr

print("\n=== Counting Sort with Range ===")
arr = [2, 1, 1, 0, 3, 2, 3, 0]
print(f"Original: {arr}")
print(f"Sorted: {counting_sort_range(arr, 3)}")


# =============================================================================
# 5. SORT STRINGS USING COUNTING SORT
# =============================================================================

def counting_sort_strings(strings):
    """Sort strings by first character using counting sort"""
    if not strings:
        return strings

    # Count by first character
    count = {}
    for s in strings:
        char = s[0].lower()
        count[char] = count.get(char, 0) + 1

    # Sort by first character
    sorted_strings = sorted(strings, key=lambda s: s[0].lower())
    return sorted_strings

print("\n=== Counting Sort Strings ===")
strings = ["banana", "apple", "cherry", "avocado", "blueberry"]
print(f"Original: {strings}")
print(f"Sorted: {counting_sort_strings(strings)}")


# =============================================================================
# 6. FREQUENCY SORT
# =============================================================================

def frequency_sort(arr):
    """Sort elements by frequency (most frequent first)"""
    from collections import Counter

    count = Counter(arr)

    # Sort by frequency (descending), then by value
    return sorted(arr, key=lambda x: (-count[x], x))

print("\n=== Frequency Sort ===")
arr = [2, 3, 5, 3, 7, 9, 5, 3, 7]
print(f"Original: {arr}")
print(f"Frequency sorted: {frequency_sort(arr)}")


# =============================================================================
# 7. COUNTING SORT WITH KEY
# =============================================================================

def counting_sort_by_key(arr, key_func):
    """Counting sort with custom key function"""
    if not arr:
        return arr

    keys = [key_func(x) for x in arr]
    min_key = min(keys)
    max_key = max(keys)
    range_val = max_key - min_key + 1

    count = [0] * range_val
    for k in keys:
        count[k - min_key] += 1

    # Cumulative count
    for i in range(1, range_val):
        count[i] += count[i - 1]

    output = [None] * len(arr)
    for x in reversed(arr):
        k = key_func(x)
        output[count[k - min_key] - 1] = x
        count[k - min_key] -= 1

    return output

print("\n=== Counting Sort by Key ===")
students = [
    ("Alice", 85),
    ("Bob", 92),
    ("Charlie", 78),
    ("Diana", 92),
    ("Eve", 85)
]
print(f"Original: {students}")
sorted_students = counting_sort_by_key(students, lambda x: x[1])
print(f"Sorted by grade: {sorted_students}")


# =============================================================================
# 8. RADIX SORT USING COUNTING SORT
# =============================================================================

def counting_sort_by_digit(arr, exp):
    """Counting sort used as subroutine for radix sort"""
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        index = (num // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    return output

def radix_sort(arr):
    """Radix sort using counting sort as subroutine"""
    if not arr:
        return arr

    max_val = max(arr)
    exp = 1

    while max_val // exp > 0:
        arr = counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr

print("\n=== Radix Sort ===")
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print(f"Original: {arr}")
print(f"Sorted: {radix_sort(arr.copy())}")


# =============================================================================
# 9. COUNTING SORT PERFORMANCE
# =============================================================================

def compare_sorting_algorithms():
    """Compare counting sort with comparison sorts"""
    import time
    import random

    print("\n=== Performance Comparison ===")

    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    def merge(left, right):
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

    sizes = [1000, 5000, 10000]
    max_vals = [100, 1000, 10000]

    for size in sizes:
        for max_val in max_vals:
            arr = [random.randint(0, max_val) for _ in range(size)]

            # Counting
            test = arr.copy()
            start = time.time()
            counting_sort(test)
            count_time = time.time() - start

            # Merge
            test = arr.copy()
            start = time.time()
            merge_sort(test)
            merge_time = time.time() - start

            # Bubble (only for small sizes)
            if size <= 1000:
                test = arr.copy()
                start = time.time()
                bubble_sort(test)
                bubble_time = time.time() - start
                bubble_str = f"{bubble_time*1000:.2f}ms"
            else:
                bubble_str = "N/A"

            print(f"\nn={size}, max={max_val}:")
            print(f"  Counting: {count_time*1000:.2f}ms")
            print(f"  Merge:    {merge_time*1000:.2f}ms")
            print(f"  Bubble:   {bubble_str}")

compare_sorting_algorithms()


# =============================================================================
# 10. PRACTICAL APPLICATIONS
# =============================================================================

print("\n=== Practical Applications ===")

# Sort colors (Dutch National Flag problem)
def sort_colors(arr):
    """Sort array of 0s, 1s, and 2s"""
    count = [0, 0, 0]
    for num in arr:
        count[num] += 1

    idx = 0
    for color in range(3):
        for _ in range(count[color]):
            arr[idx] = color
            idx += 1

    return arr

arr = [2, 0, 2, 1, 1, 0]
print(f"Sort colors {arr}: {sort_colors(arr.copy())}")

# Find missing number
def find_missing(arr, n):
    """Find missing number in 1..n using counting"""
    present = [False] * (n + 1)
    for num in arr:
        if num <= n:
            present[num] = True

    for i in range(1, n + 1):
        if not present[i]:
            return i
    return -1

print(f"Missing in [1,2,4,5] from 1..5: {find_missing([1, 2, 4, 5], 5)}")

# Sort by absolute value
def sort_by_absolute(arr):
    """Sort by absolute value"""
    max_val = max(abs(x) for x in arr)
    count = [0] * (2 * max_val + 1)

    for num in arr:
        count[num + max_val] += 1

    sorted_arr = []
    for i, c in enumerate(count):
        sorted_arr.extend([i - max_val] * c)

    return sorted_arr

arr = [-3, -1, 4, -2, 5, 0]
print(f"Sort by absolute value {arr}: {sort_by_absolute(arr)}")


# =============================================================================
# 11. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Counting Sort - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Counting sort is O(n + k) - linear time!")
    print("2. Only works for integer/range-limited data")
    print("3. Stable sort when implemented correctly")
    print("4. Used as subroutine in Radix Sort")
    print("5. Efficient when k (range) is not much larger than n")
