"""
DSA Tutorial 13 - Binary Search
================================

Binary Search: Efficiently find an item in a SORTED array.
Divides search space in half each iteration.

Time Complexity: O(log n)
Space Complexity: O(1) iterative, O(log n) recursive

Prerequisites: Array must be SORTED
"""

# =============================================================================
# 1. BASIC BINARY SEARCH
# =============================================================================

def binary_search_iterative(arr, target):
    """Iterative binary search. O(log n) time, O(1) space"""
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1

def binary_search_recursive(arr, target, low=0, high=None):
    """Recursive binary search. O(log n) time, O(log n) space"""
    if high is None:
        high = len(arr) - 1

    if low > high:
        return -1

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)

print("=== Basic Binary Search ===")
arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(f"Array: {arr}")

target = 23
print(f"Iterative search {target}: index {binary_search_iterative(arr, target)}")
print(f"Recursive search {target}: index {binary_search_recursive(arr, target)}")

target = 100
print(f"Search {target}: index {binary_search_iterative(arr, target)}")


# =============================================================================
# 2. FIND FIRST AND LAST OCCURRENCE
# =============================================================================

def find_first_occurrence(arr, target):
    """Find first occurrence of target. O(log n)"""
    low, high = 0, len(arr) - 1
    result = -1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            result = mid
            high = mid - 1  # Continue searching left
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return result

def find_last_occurrence(arr, target):
    """Find last occurrence of target. O(log n)"""
    low, high = 0, len(arr) - 1
    result = -1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            result = mid
            low = mid + 1  # Continue searching right
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return result

def count_occurrences(arr, target):
    """Count occurrences using first and last. O(log n)"""
    first = find_first_occurrence(arr, target)
    if first == -1:
        return 0
    last = find_last_occurrence(arr, target)
    return last - first + 1

print("\n=== First and Last Occurrence ===")
arr = [1, 2, 2, 2, 3, 3, 5, 5, 5, 5, 7]
print(f"Array: {arr}")
print(f"First occurrence of 5: {find_first_occurrence(arr, 5)}")
print(f"Last occurrence of 5: {find_last_occurrence(arr, 5)}")
print(f"Count of 5: {count_occurrences(arr, 5)}")
print(f"Count of 4: {count_occurrences(arr, 4)}")


# =============================================================================
# 3. FIND CEILING AND FLOOR
# =============================================================================

def find_floor(arr, target):
    """Largest element <= target. O(log n)"""
    low, high = 0, len(arr) - 1
    result = -1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return arr[mid]
        elif arr[mid] < target:
            result = arr[mid]
            low = mid + 1
        else:
            high = mid - 1

    return result

def find_ceiling(arr, target):
    """Smallest element >= target. O(log n)"""
    low, high = 0, len(arr) - 1
    result = -1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return arr[mid]
        elif arr[mid] > target:
            result = arr[mid]
            high = mid - 1
        else:
            low = mid + 1

    return result

print("\n=== Floor and Ceiling ===")
arr = [2, 5, 8, 12, 16, 23, 38]
print(f"Array: {arr}")
print(f"Floor of 10: {find_floor(arr, 10)}")
print(f"Ceiling of 10: {find_ceiling(arr, 10)}")
print(f"Floor of 2: {find_floor(arr, 2)}")
print(f"Ceiling of 40: {find_ceiling(arr, 40)}")


# =============================================================================
# 4. SEARCH IN ROTATED SORTED ARRAY
# =============================================================================

def search_rotated(arr, target):
    """Search in rotated sorted array. O(log n)"""
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid

        # Left half is sorted
        if arr[low] <= arr[mid]:
            if arr[low] <= target < arr[mid]:
                high = mid - 1
            else:
                low = mid + 1
        # Right half is sorted
        else:
            if arr[mid] < target <= arr[high]:
                low = mid + 1
            else:
                high = mid - 1

    return -1

print("\n=== Search in Rotated Array ===")
rotated = [4, 5, 6, 7, 0, 1, 2]
print(f"Array: {rotated}")
print(f"Search 0: {search_rotated(rotated, 0)}")
print(f"Search 5: {search_rotated(rotated, 5)}")


# =============================================================================
# 5. FIND PEAK ELEMENT
# =============================================================================

def find_peak_element(arr):
    """Find a peak element (greater than neighbors). O(log n)"""
    low, high = 0, len(arr) - 1

    while low < high:
        mid = (low + high) // 2

        if arr[mid] < arr[mid + 1]:
            low = mid + 1
        else:
            high = mid

    return low

print("\n=== Find Peak Element ===")
arr = [1, 3, 5, 4, 2]
print(f"Array: {arr}")
print(f"Peak at index: {find_peak_element(arr)} (value: {arr[find_peak_element(arr)]})")


# =============================================================================
# 6. FIND MINIMUM IN ROTATED ARRAY
# =============================================================================

def find_min_rotated(arr):
    """Find minimum in rotated sorted array. O(log n)"""
    low, high = 0, len(arr) - 1

    while low < high:
        mid = (low + high) // 2

        if arr[mid] > arr[high]:
            low = mid + 1
        else:
            high = mid

    return low

print("\n=== Find Minimum in Rotated Array ===")
rotated = [4, 5, 6, 7, 0, 1, 2]
print(f"Array: {rotated}")
min_idx = find_min_rotated(rotated)
print(f"Minimum at index: {min_idx} (value: {rotated[min_idx]})")


# =============================================================================
# 7. SQUARE ROOT using BINARY SEARCH
# =============================================================================

def sqrt_binary_search(n):
    """Find integer square root. O(log n)"""
    if n == 0:
        return 0

    low, high = 1, n
    result = 1

    while low <= high:
        mid = (low + high) // 2
        if mid * mid <= n:
            result = mid
            low = mid + 1
        else:
            high = mid - 1

    return result

print("\n=== Square Root ===")
for n in [0, 1, 4, 8, 16, 27, 100]:
    print(f"sqrt({n}) = {sqrt_binary_search(n)}")


# =============================================================================
# 8. SEARCH IN INFINITE SORTED ARRAY
# =============================================================================

def search_infinite(arr, target):
    """Search in effectively infinite sorted array"""
    # Find boundaries first
    low, high = 0, 1

    while high < len(arr) and arr[high] < target:
        low = high
        high *= 2

    high = min(high, len(arr) - 1)

    # Binary search in range
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1

print("\n=== Search in Infinite Array ===")
arr = list(range(0, 1000, 2))  # Even numbers
print(f"Search 500: {search_infinite(arr, 500)}")
print(f"Search 501: {search_infinite(arr, 501)}")


# =============================================================================
# 9. BINARY SEARCH ON ANSWER
# =============================================================================

def split_array_largest_sum(arr, m):
    """Minimize largest sum when splitting array into m parts"""
    def can_split(max_sum):
        cuts = 1
        current_sum = 0
        for num in arr:
            current_sum += num
            if current_sum > max_sum:
                cuts += 1
                current_sum = num
                if cuts > m:
                    return False
        return True

    low, high = max(arr), sum(arr)
    result = high

    while low <= high:
        mid = (low + high) // 2
        if can_split(mid):
            result = mid
            high = mid - 1
        else:
            low = mid + 1

    return result

print("\n=== Binary Search on Answer ===")
arr = [7, 2, 5, 10, 8]
m = 2
print(f"Array: {arr}, m = {m}")
print(f"Minimize largest sum: {split_array_largest_sum(arr, m)}")


# =============================================================================
# 10. MEDIAN OF TWO SORTED ARRAYS
# =============================================================================

def median_two_sorted(nums1, nums2):
    """Find median of two sorted arrays. O(log(min(m,n)))"""
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    low, high = 0, m

    while low <= high:
        i = (low + high) // 2
        j = (m + n + 1) // 2 - i

        max_left_1 = float('-inf') if i == 0 else nums1[i - 1]
        min_right_1 = float('inf') if i == m else nums1[i]
        max_left_2 = float('-inf') if j == 0 else nums2[j - 1]
        min_right_2 = float('inf') if j == n else nums2[j]

        if max_left_1 <= min_right_2 and max_left_2 <= min_right_1:
            if (m + n) % 2 == 1:
                return max(max_left_1, max_left_2)
            else:
                return (max(max_left_1, max_left_2) +
                        min(min_right_1, min_right_2)) / 2
        elif max_left_1 > min_right_2:
            high = i - 1
        else:
            low = i + 1

    return -1

print("\n=== Median of Two Sorted Arrays ===")
print(f"nums1=[1,3], nums2=[2]: {median_two_sorted([1, 3], [2])}")
print(f"nums1=[1,2], nums2=[3,4]: {median_two_sorted([1, 2], [3, 4])}")


# =============================================================================
# 11. NEXT LETTER (CEILING)
# =============================================================================

def next_letter(arr, target):
    """Find smallest letter greater than target. O(log n)"""
    low, high = 0, len(arr) - 1

    # Wrap around
    if target >= arr[-1] or target < arr[0]:
        return arr[0]

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] <= target:
            low = mid + 1
        else:
            high = mid - 1

    return arr[low % len(arr)]

print("\n=== Next Letter ===")
letters = ['a', 'c', 'f', 'h']
for target in ['b', 'f', 'h', 'z']:
    print(f"Next letter after '{target}': '{next_letter(letters, target)}'")


# =============================================================================
# 12. SEARCH MATRIX
# =============================================================================

def search_matrix(matrix, target):
    """Search in row-sorted, col-sorted matrix. O(log(m*n))"""
    if not matrix:
        return False

    rows, cols = len(matrix), len(matrix[0])
    low, high = 0, rows * cols - 1

    while low <= high:
        mid = (low + high) // 2
        row, col = mid // cols, mid % cols

        if matrix[row][col] == target:
            return True
        elif matrix[row][col] < target:
            low = mid + 1
        else:
            high = mid - 1

    return False

print("\n=== Search Matrix ===")
matrix = [
    [1, 3, 5, 7],
    [10, 11, 16, 20],
    [23, 30, 34, 60]
]
print(f"Search 3: {search_matrix(matrix, 3)}")
print(f"Search 13: {search_matrix(matrix, 13)}")


# =============================================================================
# 13. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Binary Search - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Binary search requires SORTED data")
    print("2. O(log n) time complexity - extremely efficient")
    print("3. Variants: first/last occurrence, ceiling/floor")
    print("4. Works on rotated arrays with modifications")
    print("5. 'Binary search on answer' solves optimization problems")
