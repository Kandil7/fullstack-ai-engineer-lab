"""
DSA Tutorial 12 - Linear Search
================================

Linear Search: Check each element one by one until found.

Time Complexity: O(n)
Space Complexity: O(1)

When to use:
- Small arrays
- Unsorted arrays
- Single search needed
"""

# =============================================================================
# 1. BASIC LINEAR SEARCH
# =============================================================================

def linear_search(arr, target):
    """Search for target in array. Returns index or -1."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

print("=== Basic Linear Search ===")
arr = [10, 23, 45, 70, 11, 15]
target = 70
result = linear_search(arr, target)
print(f"Array: {arr}")
print(f"Search {target}: index {result}")

target = 99
result = linear_search(arr, target)
print(f"Search {target}: index {result}")


# =============================================================================
# 2. SENTINEL LINEAR SEARCH
# =============================================================================

def sentinel_search(arr, target):
    """Linear search with sentinel - eliminates boundary check"""
    n = len(arr)
    last = arr[n - 1]
    arr[n - 1] = target  # Place sentinel

    i = 0
    while arr[i] != target:
        i += 1

    arr[n - 1] = last  # Restore last element

    if i < n - 1 or arr[n - 1] == target:
        return i
    return -1

print("\n=== Sentinel Search ===")
arr = [10, 23, 45, 70, 11, 15]
target = 70
result = sentinel_search(arr, target)
print(f"Sentinel search {target}: index {result}")


# =============================================================================
# 3. SEARCH IN SORTED ARRAY (LINEAR)
# =============================================================================

def linear_search_sorted(arr, target):
    """Optimized for sorted arrays - stop early"""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
        if arr[i] > target:
            return -1  # Not found, passed target
    return -1

print("\n=== Linear Search in Sorted Array ===")
sorted_arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(f"Search 23: {linear_search_sorted(sorted_arr, 23)}")
print(f"Search 10: {linear_search_sorted(sorted_arr, 10)}")


# =============================================================================
# 4. FIND MIN AND MAX
# =============================================================================

def find_min(arr):
    """Find minimum using linear search. O(n)"""
    if not arr:
        return None
    min_val = arr[0]
    for val in arr[1:]:
        if val < min_val:
            min_val = val
    return min_val

def find_max(arr):
    """Find maximum using linear search. O(n)"""
    if not arr:
        return None
    max_val = arr[0]
    for val in arr[1:]:
        if val > max_val:
            max_val = val
    return max_val

def find_min_max(arr):
    """Find both min and max in single pass. O(n)"""
    if not arr:
        return None, None

    if len(arr) == 1:
        return arr[0], arr[0]

    min_val, max_val = (arr[0], arr[1]) if arr[0] < arr[1] else (arr[1], arr[0])

    for i in range(2, len(arr), 2):
        if i + 1 < len(arr):
            local_min = min(arr[i], arr[i + 1])
            local_max = max(arr[i], arr[i + 1])
        else:
            local_min = local_max = arr[i]

        min_val = min(min_val, local_min)
        max_val = max(max_val, local_max)

    return min_val, max_val

print("\n=== Find Min and Max ===")
arr = [38, 27, 43, 3, 9, 82, 10]
print(f"Array: {arr}")
print(f"Min: {find_min(arr)}")
print(f"Max: {find_max(arr)}")
min_val, max_val = find_min_max(arr)
print(f"Min-Max (single pass): {min_val}, {max_val}")


# =============================================================================
# 5. SEARCH FOR MULTIPLE OCCURRENCES
# =============================================================================

def find_all_occurrences(arr, target):
    """Find all indices of target. O(n)"""
    indices = []
    for i, val in enumerate(arr):
        if val == target:
            indices.append(i)
    return indices

def count_occurrences(arr, target):
    """Count occurrences of target. O(n)"""
    count = 0
    for val in arr:
        if val == target:
            count += 1
    return count

print("\n=== Multiple Occurrences ===")
arr = [1, 3, 5, 3, 7, 3, 9, 3]
print(f"Array: {arr}")
print(f"All indices of 3: {find_all_occurrences(arr, 3)}")
print(f"Count of 3: {count_occurrences(arr, 3)}")


# =============================================================================
# 6. SEARCH IN 2D ARRAY
# =============================================================================

def search_2d(matrix, target):
    """Search in 2D array. O(m*n)"""
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == target:
                return (i, j)
    return None

def search_2d_sorted(matrix, target):
    """Search in row-sorted 2D array. O(m + n)"""
    if not matrix:
        return None

    rows, cols = len(matrix), len(matrix[0])
    row, col = 0, cols - 1  # Start top-right

    while row < rows and col >= 0:
        if matrix[row][col] == target:
            return (row, col)
        elif matrix[row][col] > target:
            col -= 1
        else:
            row += 1

    return None

print("\n=== Search in 2D Array ===")
matrix = [
    [10, 20, 30, 40],
    [15, 25, 35, 45],
    [27, 29, 37, 48],
    [32, 33, 39, 50]
]
print(f"Matrix:")
for row in matrix:
    print(f"  {row}")

target = 29
print(f"Search {target}: {search_2d(matrix, target)}")
print(f"Search {target} (sorted): {search_2d_sorted(matrix, target)}")


# =============================================================================
# 7. SEARCH STRING IN TEXT
# =============================================================================

def find_substring(text, pattern):
    """Find first occurrence of pattern in text. O(n*m)"""
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            return i
    return -1

def find_all_substrings(text, pattern):
    """Find all occurrences of pattern. O(n*m)"""
    indices = []
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            indices.append(i)
    return indices

print("\n=== String Search ===")
text = "ababcabcababc"
pattern = "abc"
print(f"Text: '{text}'")
print(f"Pattern: '{pattern}'")
print(f"First occurrence: {find_substring(text, pattern)}")
print(f"All occurrences: {find_all_substrings(text, pattern)}")


# =============================================================================
# 8. INTERPOLATION SEARCH
# =============================================================================

def interpolation_search(arr, target):
    """Improved linear search for uniformly distributed data. O(log log n) avg"""
    low, high = 0, len(arr) - 1

    while low <= high and arr[low] <= target <= arr[high]:
        if low == high:
            return low if arr[low] == target else -1

        # Estimate position
        pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1

print("\n=== Interpolation Search ===")
uniform_arr = [10, 12, 13, 16, 18, 19, 20, 21, 22, 23, 24, 33, 35, 42, 47]
print(f"Uniform array: {uniform_arr}")
print(f"Search 18: {interpolation_search(uniform_arr, 18)}")
print(f"Search 33: {interpolation_search(uniform_arr, 33)}")


# =============================================================================
# 9. TERNARY SEARCH
# =============================================================================

def ternary_search(arr, target):
    """Divide array into 3 parts. O(log3 n)"""
    low, high = 0, len(arr) - 1

    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3

        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2

        if target < arr[mid1]:
            high = mid1 - 1
        elif target > arr[mid2]:
            low = mid2 + 1
        else:
            low = mid1 + 1
            high = mid2 - 1

    return -1

print("\n=== Ternary Search ===")
sorted_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
print(f"Search 7: {ternary_search(sorted_data, 7)}")
print(f"Search 12: {ternary_search(sorted_data, 12)}")


# =============================================================================
# 10. COMPARISON OF SEARCH ALGORITHMS
# =============================================================================

def compare_searches():
    """Compare performance of different search algorithms"""
    import time
    import random

    sizes = [100, 1000, 10000, 100000]

    print("\n=== Search Algorithm Comparison ===")
    print(f"{'Size':<10} {'Linear':<12} {'Sentinel':<12} {'Binary':<12}")
    print("-" * 46)

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        # Linear
        start = time.time()
        for _ in range(1000):
            linear_search(arr, target)
        linear_time = (time.time() - start) / 1000

        # Sentinel
        start = time.time()
        for _ in range(1000):
            sentinel_search(arr.copy(), target)
        sentinel_time = (time.time() - start) / 1000

        # Binary
        start = time.time()
        for _ in range(1000):
            low, high = 0, len(arr) - 1
            while low <= high:
                mid = (low + high) // 2
                if arr[mid] == target:
                    break
                elif arr[mid] < target:
                    low = mid + 1
                else:
                    high = mid - 1
        binary_time = (time.time() - start) / 1000

        print(f"{size:<10} {linear_time*1000:<12.4f} {sentinel_time*1000:<12.4f} {binary_time*1000:<12.4f}")

compare_searches()


# =============================================================================
# 11. PRACTICAL APPLICATIONS
# =============================================================================

print("\n=== Practical Applications ===")

# Find duplicate
def find_duplicates(arr):
    """Find all duplicates. O(n) time, O(n) space"""
    seen = set()
    duplicates = set()
    for val in arr:
        if val in seen:
            duplicates.add(val)
        seen.add(val)
    return list(duplicates)

# Find missing number
def find_missing(arr, n):
    """Find missing number in 1..n. O(n)"""
    total = n * (n + 1) // 2
    return total - sum(arr)

# First non-repeating
def first_non_repeating(arr):
    """Find first non-repeating element. O(n)"""
    from collections import Counter
    count = Counter(arr)
    for val in arr:
        if count[val] == 1:
            return val
    return None

arr = [1, 2, 3, 2, 4, 3, 5]
print(f"Duplicates in {arr}: {find_duplicates(arr)}")
print(f"Missing in [1,2,4,5] from 1..5: {find_missing([1, 2, 4, 5], 5)}")

arr = [4, 5, 1, 2, 1, 4]
print(f"First non-repeating in {arr}: {first_non_repeating(arr)}")


# =============================================================================
# 12. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Linear Search - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Linear search checks each element sequentially")
    print("2. O(n) time complexity - works on any array")
    print("3. Sentinel search reduces boundary checks")
    print("4. Interpolation search optimizes for uniform data")
    print("5. Use binary search for sorted arrays when possible")
