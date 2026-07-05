"""
DSA Tutorial 02 - Arrays
========================

Arrays store elements in contiguous memory.
In Python, lists serve as dynamic arrays.

Key Properties:
- Fixed type (in traditional languages)
- Indexed access O(1)
- Fixed size (traditional) / Dynamic (Python)
"""

# =============================================================================
# 1. BASIC ARRAY OPERATIONS
# =============================================================================

print("=== Basic Array Operations ===")

# Creating arrays
arr1 = [10, 20, 30, 40, 50]
arr2 = [0] * 10  # Array of 10 zeros
arr3 = list(range(1, 11))  # [1, 2, ..., 10]

print(f"arr1: {arr1}")
print(f"arr2: {arr2}")
print(f"arr3: {arr3}")


# =============================================================================
# 2. ARRAY INSERTION
# =============================================================================

print("\n=== Array Insertion ===")

def insert_at_index(arr, index, value):
    """Insert value at specific index. O(n) time."""
    if index < 0 or index > len(arr):
        print("Index out of bounds")
        return arr
    # Create new array with one more space
    new_arr = arr[:index] + [value] + arr[index:]
    return new_arr

def insert_at_end(arr, value):
    """Append to end. O(1) amortized."""
    arr.append(value)
    return arr

def insert_at_beginning(arr, value):
    """Insert at start. O(n) - must shift all elements."""
    return [value] + arr

test = [1, 2, 3, 4, 5]
print(f"Original: {test}")

test = insert_at_end(test, 6)
print(f"After append 6: {test}")

test = insert_at_beginning(test, 0)
print(f"Insert 0 at start: {test}")

test = insert_at_index(test, 3, 99)
print(f"Insert 99 at index 3: {test}")


# =============================================================================
# 3. ARRAY DELETION
# =============================================================================

print("\n=== Array Deletion ===")

def delete_at_index(arr, index):
    """Delete element at index. O(n) time."""
    if index < 0 or index >= len(arr):
        return arr
    return arr[:index] + arr[index + 1:]

def delete_value(arr, value):
    """Delete first occurrence of value. O(n) time."""
    try:
        idx = arr.index(value)
        return arr[:idx] + arr[idx + 1:]
    except ValueError:
        return arr

def delete_at_beginning(arr):
    """Remove first element. O(n) shift."""
    return arr[1:] if arr else arr

test = [10, 20, 30, 40, 50]
print(f"Original: {test}")

test = delete_at_index(test, 2)
print(f"Delete at index 2: {test}")

test = delete_value(test, 40)
print(f"Delete value 40: {test}")

test = delete_at_beginning(test)
print(f"Delete at beginning: {test}")


# =============================================================================
# 4. ARRAY SEARCHING
# =============================================================================

print("\n=== Array Searching ===")

def linear_search(arr, target):
    """Search sequentially. O(n) time."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def binary_search(arr, target):
    """Search in sorted array. O(log n) time."""
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

def find_all_occurrences(arr, target):
    """Find all indices of target. O(n) time."""
    return [i for i, v in enumerate(arr) if v == target]

data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(f"Sorted array: {data}")
print(f"Linear search 23: index {linear_search(data, 23)}")
print(f"Binary search 23: index {binary_search(data, 23)}")

duplicates = [1, 3, 2, 3, 4, 3, 5]
print(f"All occurrences of 3 in {duplicates}: {find_all_occurrences(duplicates, 3)}")


# =============================================================================
# 5. ARRAY TRAVERSAL
# =============================================================================

print("\n=== Array Traversal ===")

def traverse_forward(arr):
    """O(n) traversal"""
    return [arr[i] for i in range(len(arr))]

def traverse_backward(arr):
    """O(n) reverse traversal"""
    return [arr[i] for i in range(len(arr) - 1, -1, -1)]

def traverse_by_step(arr, step=2):
    """Traverse with step. O(n/step)"""
    return [arr[i] for i in range(0, len(arr), step)]

sample = [10, 20, 30, 40, 50, 60, 70, 80]
print(f"Forward: {traverse_forward(sample)}")
print(f"Backward: {traverse_backward(sample)}")
print(f"Every 2nd: {traverse_by_step(sample, 2)}")


# =============================================================================
# 6. ARRAY REVERSAL
# =============================================================================

print("\n=== Array Reversal ===")

def reverse_iterative(arr):
    """Two-pointer approach. O(n) time, O(1) space."""
    result = arr.copy()
    left, right = 0, len(result) - 1
    while left < right:
        result[left], result[right] = result[right], result[left]
        left += 1
        right -= 1
    return result

def reverse_recursive(arr, start=0):
    """Recursive reversal. O(n) time, O(n) space."""
    if start >= len(arr) // 2:
        return arr
    arr[start], arr[len(arr) - 1 - start] = arr[len(arr) - 1 - start], arr[start]
    return reverse_recursive(arr, start + 1)

test = [1, 2, 3, 4, 5, 6, 7, 8]
print(f"Original: {test}")
print(f"Iterative reverse: {reverse_iterative(test)}")
print(f"Recursive reverse: {reverse_recursive(test.copy())}")


# =============================================================================
# 7. ARRAY ROTATION
# =============================================================================

print("\n=== Array Rotation ===")

def rotate_left(arr, k):
    """Rotate array left by k positions. O(n) time."""
    n = len(arr)
    k = k % n
    return arr[k:] + arr[:k]

def rotate_right(arr, k):
    """Rotate array right by k positions. O(n) time."""
    n = len(arr)
    k = k % n
    return arr[n - k:] + arr[:n - k]

def rotate_in_place(arr, k):
    """In-place rotation using reversal. O(n) time, O(1) space."""
    n = len(arr)
    k = k % n

    def reverse(start, end):
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1

    reverse(0, k - 1)
    reverse(k, n - 1)
    reverse(0, n - 1)
    return arr

original = [1, 2, 3, 4, 5, 6, 7]
print(f"Original: {original}")
print(f"Left by 2: {rotate_left(original, 2)}")
print(f"Right by 3: {rotate_right(original, 3)}")

in_place = original.copy()
rotate_in_place(in_place, 2)
print(f"In-place left by 2: {in_place}")


# =============================================================================
# 8. ARRAY SORTING
# =============================================================================

print("\n=== Array Sorting ===")

def insertion_sort(arr):
    """Insertion sort. O(n^2) time."""
    result = arr.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result

def merge_sort(arr):
    """Merge sort. O(n log n) time."""
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

unsorted = [64, 34, 25, 12, 22, 11, 90]
print(f"Unsorted: {unsorted}")
print(f"Insertion sort: {insertion_sort(unsorted)}")
print(f"Merge sort: {merge_sort(unsorted)}")


# =============================================================================
# 9. TWO POINTER TECHNIQUE
# =============================================================================

print("\n=== Two Pointer Technique ===")

def two_sum(arr, target):
    """Find two numbers that sum to target. O(n) with sorted array."""
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return (left, right)
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None

def is_pair_sum(arr, target):
    """Check if any pair sums to target. O(n)."""
    return two_sum(arr, target) is not None

sorted_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = two_sum(sorted_arr, 9)
print(f"Sorted array: {sorted_arr}")
if result:
    print(f"Pair summing to 9: indices {result} -> {sorted_arr[result[0]]} + {sorted_arr[result[1]]} = 9")


# =============================================================================
# 10. SLIDING WINDOW
# =============================================================================

print("\n=== Sliding Window Technique ===")

def max_subarray_sum(arr, k):
    """Maximum sum of subarray of size k. O(n)."""
    if len(arr) < k:
        return None

    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum

def max_subarray_kadane(arr):
    """Maximum subarray sum (Kadane's algorithm). O(n)."""
    if not arr:
        return 0
    max_sum = current_sum = arr[0]
    for num in arr[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum

data = [2, 1, 5, 1, 3, 2]
k = 3
print(f"Array: {data}, k = {k}")
print(f"Max sum of subarray size {k}: {max_subarray_sum(data, k)}")

mixed = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(f"Max subarray sum (Kadane): {max_subarray_kadane(mixed)}")


# =============================================================================
# 11. ARRAY UTILITIES
# =============================================================================

print("\n=== Array Utilities ===")

def remove_duplicates(arr):
    """Remove duplicates while preserving order. O(n) time."""
    seen = set()
    result = []
    for item in arr:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def find_second_largest(arr):
    """Find second largest element. O(n) time."""
    if len(arr) < 2:
        return None
    first = second = float('-inf')
    for num in arr:
        if num > first:
            second = first
            first = num
        elif num > second and num != first:
            second = num
    return second if second != float('-inf') else None

def flatten(arr):
    """Flatten nested arrays. O(n) time."""
    result = []
    for item in arr:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

test = [1, 2, 2, 3, 4, 4, 5, 5, 5]
print(f"Remove duplicates: {remove_duplicates(test)}")
print(f"Second largest: {find_second_largest(test)}")

nested = [1, [2, 3], [4, [5, 6]], 7]
print(f"Flatten {nested}: {flatten(nested)}")


# =============================================================================
# 12. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Arrays - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Arrays provide O(1) indexed access")
    print("2. Insertion/deletion at arbitrary positions is O(n)")
    print("3. Two pointer technique optimizes many array problems")
    print("4. Sliding window handles subarray problems efficiently")
    print("5. Python lists are dynamic arrays (amortized O(1) append)")
