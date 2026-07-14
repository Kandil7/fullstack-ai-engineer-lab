# DSA Searching Interview Practice

## Topic Overview

Searching algorithms find elements or determine properties of data. **Binary search** is the most important searching technique, with many variations. Interviews test your ability to identify when binary search applies and handle edge cases.

**Key Concepts:**
- Linear search: O(n) — check each element
- Binary search: O(log n) — divide and conquer on sorted data
- Binary search on answer space — optimization problems
- Two-dimensional search — matrix patterns

---

## Interview Questions (with Answers)

### Q1: Explain binary search. What are the preconditions?

**Answer:**
Binary search finds a target in a sorted collection by repeatedly dividing the search space in half.

**Preconditions:**
1. Data must be sorted (or have a monotonic predicate)
2. Random access (array, not linked list)

**Classic Binary Search:**
```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

**Key points:**
- `left <= right` (not `<`) — allows searching the full range
- `left = mid + 1` and `right = mid - 1` — avoid infinite loops
- `mid = left + (right - left) // 2` — prevents integer overflow

---

### Q2: What are the two common binary search templates?

**Answer:**
**Template 1 — Find exact match or insertion point:**
```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return left  # Insertion point
```

**Template 2 — Find boundary (first/last occurrence):**
```python
def find_first(nums, target):
    left, right = 0, len(nums) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

def find_last(nums, target):
    left, right = 0, len(nums) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            left = mid + 1  # Continue searching right
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
```

---

### Q3: How do you search in a rotated sorted array?

**Answer:**
```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1

# Test
assert search_rotated([4,5,6,7,0,1,2], 0) == 4
assert search_rotated([4,5,6,7,0,1,2], 3) == -1
assert search_rotated([1], 0) == -1
```
**Time: O(log n), Space: O(1)**

---

### Q4: How do you search in a 2D matrix?

**Answer:**
**Approach 1 — Treat as sorted 1D array:**
```python
def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = left + (right - left) // 2
        mid_val = matrix[mid // n][mid % n]

        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False
```

**Approach 2 — Staircase search (for matrices sorted row-wise and column-wise):**
```python
def search_matrix_2(matrix, target):
    if not matrix:
        return False

    row, col = 0, len(matrix[0]) - 1

    while row < len(matrix) and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1
        else:
            row += 1

    return False
```

**Time: O(log(m*n)) for Approach 1, O(m+n) for Approach 2**

---

### Q5: How do you find the median of two sorted arrays?

**Answer:**
Binary search on the smaller array to find the correct partition.

```python
def find_median_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    left, right = 0, m

    while left <= right:
        i = (left + right) // 2
        j = (m + n + 1) // 2 - i

        max_left_1 = float('-inf') if i == 0 else nums1[i - 1]
        min_right_1 = float('inf') if i == m else nums1[i]
        max_left_2 = float('-inf') if j == 0 else nums2[j - 1]
        min_right_2 = float('inf') if j == n else nums2[j]

        if max_left_1 <= min_right_2 and max_left_2 <= min_right_1:
            if (m + n) % 2 == 1:
                return max(max_left_1, max_left_2)
            else:
                return (max(max_left_1, max_left_2) + min(min_right_1, min_right_2)) / 2
        elif max_left_1 > min_right_2:
            right = i - 1
        else:
            left = i + 1

# Test
assert find_median_sorted_arrays([1, 3], [2]) == 2.0
assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5
```
**Time: O(log(min(m, n))), Space: O(1)**

---

### Q6: How do you find the first bad version?

**Answer:**
```python
def first_bad_version(n):
    left, right = 1, n

    while left < right:
        mid = left + (right - left) // 2
        if is_bad_version(mid):
            right = mid
        else:
            left = mid + 1

    return left

# is_bad_version is provided by the system
```

**Key difference:** Uses `left < right` (not `<=`) because we're looking for a boundary, not an exact match.

---

### Q7: How do you find the square root of a number using binary search?

**Answer:**
```python
def sqrt_binary_search(x):
    if x < 2:
        return x

    left, right = 1, x // 2

    while left <= right:
        mid = left + (right - left) // 2
        if mid * mid == x:
            return mid
        elif mid * mid < x:
            left = mid + 1
        else:
            right = mid - 1

    return right  # Return floor of sqrt

# Test
assert sqrt_binary_search(8) == 2
assert sqrt_binary_search(4) == 2
assert sqrt_binary_search(0) == 0
```

---

### Q8: How do you find the peak element in an array?

**Answer:**
A peak element is greater than its neighbors. Binary search works because if `nums[mid] < nums[mid+1]`, a peak exists on the right.

```python
def find_peak_element(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return left

# Test
assert find_peak_element([1, 2, 3, 1]) == 2
assert find_peak_element([1, 2, 1, 3, 5, 6, 4]) in [1, 5]
```

---

### Q9: How do you search in a sorted array with duplicates?

**Answer:**
Find the first and last occurrence using modified binary search.

```python
def search_range(nums, target):
    def find_first():
        left, right = 0, len(nums) - 1
        result = -1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                result = mid
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    def find_last():
        left, right = 0, len(nums) - 1
        result = -1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                result = mid
                left = mid + 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    return [find_first(), find_last()]

# Test
assert search_range([5,7,7,8,8,10], 8) == [3, 4]
assert search_range([5,7,7,8,8,10], 6) == [-1, -1]
```

---

### Q10: What is binary search on answer space?

**Answer:**
Binary search on answer space applies binary search to optimization problems where we binary search on the possible answer values.

**Example — Split Array Largest Sum:**
Given an array and m subarrays, minimize the largest sum.

```python
def split_array(nums, m):
    def can_split(max_sum):
        count = 1
        current_sum = 0
        for num in nums:
            current_sum += num
            if current_sum > max_sum:
                count += 1
                current_sum = num
                if count > m:
                    return False
        return True

    left, right = max(nums), sum(nums)

    while left < right:
        mid = left + (right - left) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1

    return left

# Test
assert split_array([7,2,5,10,8], 2) == 18
```

**Pattern:** Binary search on the answer, check if it's feasible.

---

### Q11: How do you find the minimum in a rotated sorted array?

**Answer:**
```python
def find_min(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]

# Test
assert find_min([3,4,5,1,2]) == 1
assert find_min([4,5,6,7,0,1,2]) == 0
assert find_min([11,13,15,17]) == 11
```

**Logic:** If `nums[mid] > nums[right]`, the minimum is in the right half. Otherwise, it's in the left half (including mid).

---

### Q12: How do you find the smallest letter greater than target?

**Answer:**
```python
def next_greatest_letter(letters, target):
    left, right = 0, len(letters)

    while left < right:
        mid = left + (right - left) // 2
        if letters[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return letters[left % len(letters)]

# Test
assert next_greatest_letter(["c","f","j"], "a") == "c"
assert next_greatest_letter(["c","f","j"], "c") == "f"
assert next_greatest_letter(["c","f","j"], "d") == "f"
```

---

### Q13: How do you find the maximum in a bitonic array?

**Answer:**
A bitonic array increases then decreases.

```python
def find_peak_bitonic(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return nums[left]

# Test
assert find_peak_bitonic([1, 3, 8, 12, 4, 2]) == 12
```

---

### Q14: How do you search in an infinite sorted array?

**Answer:**
Find the bounds first, then binary search.

```python
def search_infinite(nums, target):
    # Find bounds
    left, right = 0, 1
    while right < len(nums) and nums[right] < target:
        left = right
        right *= 2

    # Binary search
    while left <= right:
        mid = left + (right - left) // 2
        if mid >= len(nums) or nums[mid] > target:
            right = mid - 1
        elif nums[mid] < target:
            left = mid + 1
        else:
            return mid

    return -1
```

---

### Q15: How do you find the intersection of two sorted arrays?

**Answer:**
Two pointers approach:

```python
def intersection(nums1, nums2):
    result = []
    i, j = 0, 0

    while i < len(nums1) and j < len(nums2):
        if nums1[i] == nums2[j]:
            if not result or result[-1] != nums1[i]:
                result.append(nums1[i])
            i += 1
            j += 1
        elif nums1[i] < nums2[j]:
            i += 1
        else:
            j += 1

    return result

# Test
assert intersection([1, 2, 2, 1], [2, 2]) == [2]
assert intersection([4, 9, 5], [9, 4, 9, 8, 4]) == [4, 9]
```

---

## Coding Challenges

### Challenge 1: Binary Search
```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# Test
assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
```
**Time: O(log n), Space: O(1)**

---

### Challenge 2: Search Insert Position
```python
def search_insert(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return left

# Test
assert search_insert([1, 3, 5, 6], 5) == 2
assert search_insert([1, 3, 5, 6], 2) == 1
assert search_insert([1, 3, 5, 6], 7) == 4
```
**Time: O(log n), Space: O(1)**

---

### Challenge 3: Find First and Last Position
```python
def search_range(nums, target):
    def find_first():
        left, right = 0, len(nums) - 1
        result = -1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                result = mid
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    def find_last():
        left, right = 0, len(nums) - 1
        result = -1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                result = mid
                left = mid + 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    return [find_first(), find_last()]

# Test
assert search_range([5,7,7,8,8,10], 8) == [3, 4]
assert search_range([5,7,7,8,8,10], 6) == [-1, -1]
```
**Time: O(log n), Space: O(1)**

---

### Challenge 4: Search in Rotated Sorted Array
```python
def search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1

# Test
assert search([4,5,6,7,0,1,2], 0) == 4
assert search([4,5,6,7,0,1,2], 3) == -1
```
**Time: O(log n), Space: O(1)**

---

### Challenge 5: Find Minimum in Rotated Sorted Array
```python
def find_min(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]

# Test
assert find_min([3,4,5,1,2]) == 1
assert find_min([4,5,6,7,0,1,2]) == 0
```
**Time: O(log n), Space: O(1)**

---

### Challenge 6: Median of Two Sorted Arrays
```python
def find_median_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    left, right = 0, m

    while left <= right:
        i = (left + right) // 2
        j = (m + n + 1) // 2 - i

        max_left_1 = float('-inf') if i == 0 else nums1[i - 1]
        min_right_1 = float('inf') if i == m else nums1[i]
        max_left_2 = float('-inf') if j == 0 else nums2[j - 1]
        min_right_2 = float('inf') if j == n else nums2[j]

        if max_left_1 <= min_right_2 and max_left_2 <= min_right_1:
            if (m + n) % 2 == 1:
                return max(max_left_1, max_left_2)
            else:
                return (max(max_left_1, max_left_2) + min(min_right_1, min_right_2)) / 2
        elif max_left_1 > min_right_2:
            right = i - 1
        else:
            left = i + 1

# Test
assert find_median_sorted_arrays([1, 3], [2]) == 2.0
assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5
```
**Time: O(log(min(m, n))), Space: O(1)**

---

### Challenge 7: Peak Index in a Mountain Array
```python
def peak_index_in_mountain_array(arr):
    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return left

# Test
assert peak_index_in_mountain_array([0, 1, 0]) == 1
assert peak_index_in_mountain_array([0, 2, 1, 0]) == 1
assert peak_index_in_mountain_array([0, 10, 5, 2]) == 1
```
**Time: O(log n), Space: O(1)**

---

### Challenge 8: Capacity To Ship Packages Within D Days
```python
def ship_within_days(weights, days):
    def can_ship(capacity):
        days_needed = 1
        current = 0
        for w in weights:
            current += w
            if current > capacity:
                days_needed += 1
                current = w
        return days_needed <= days

    left, right = max(weights), sum(weights)

    while left < right:
        mid = left + (right - left) // 2
        if can_ship(mid):
            right = mid
        else:
            left = mid + 1

    return left

# Test
assert ship_within_days([1,2,3,4,5,6,7,8,9,10], 5) == 15
assert ship_within_days([3,2,2,4,1,4], 3) == 6
```
**Time: O(n * log(sum - max)), Space: O(1)**

---

### Challenge 9: Split Array Largest Sum
```python
def split_array(nums, m):
    def can_split(max_sum):
        count = 1
        current_sum = 0
        for num in nums:
            current_sum += num
            if current_sum > max_sum:
                count += 1
                current_sum = num
                if count > m:
                    return False
        return True

    left, right = max(nums), sum(nums)

    while left < right:
        mid = left + (right - left) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1

    return left

# Test
assert split_array([7,2,5,10,8], 2) == 18
```
**Time: O(n * log(sum)), Space: O(1)**

---

### Challenge 10: Find in Mountain Array
```python
def find_in_mountain_array(target, mountain_arr):
    length = mountain_arr.length()

    # Find peak
    left, right = 0, length - 1
    while left < right:
        mid = left + (right - left) // 2
        if mountain_arr.get(mid) < mountain_arr.get(mid + 1):
            left = mid + 1
        else:
            right = mid
    peak = left

    # Search left side (ascending)
    left, right = 0, peak
    while left <= right:
        mid = left + (right - left) // 2
        val = mountain_arr.get(mid)
        if val == target:
            return mid
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1

    # Search right side (descending)
    left, right = peak, length - 1
    while left <= right:
        mid = left + (right - left) // 2
        val = mountain_arr.get(mid)
        if val == target:
            return mid
        elif val > target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```
**Time: O(log n), Space: O(1)**

---

## Common Follow-Up Questions

1. **"Can you do it in O(1) space?"** — Binary search is O(1) space. If you need extra space, explain why.
2. **"What if the array is not sorted?"** — You can't use binary search. Consider sorting first (O(n log n)) or using hash map (O(n)).
3. **"What about duplicates?"** — Modified binary search for first/last occurrence.
4. **"What if the array is infinite?"** — Exponential search (find bounds, then binary search).
5. **"Can you use binary search on a linked list?"** — Not directly (no random access). Use skip list or convert to array.
6. **"What about 2D matrices?"** — Treat as 1D if row-sorted. Use staircase search for row+column sorted.

---

## Tips for Answering Searching Questions

1. **Identify the search space:** Is it an array, a range of values, or an answer space?
2. **Define the predicate:** What condition divides the search space?
3. **Handle edge cases:** Empty array, single element, all same elements, target not found.
4. **Choose the right template:** Exact match vs. boundary vs. answer space.
5. **Watch for off-by-one errors:** `left <= right` vs. `left < right`.
6. **Consider the constraints:** If O(log n) is required, binary search is likely the answer.

---

## Complexity Cheat Sheet

| Problem | Time | Space |
|---------|------|-------|
| Binary Search | O(log n) | O(1) |
| First/Last Occurrence | O(log n) | O(1) |
| Search in Rotated Array | O(log n) | O(1) |
| Find Minimum Rotated | O(log n) | O(1) |
| Median of Two Arrays | O(log(min(m,n))) | O(1) |
| 2D Matrix Search | O(log(m*n)) | O(1) |
| Peak Element | O(log n) | O(1) |
| Square Root | O(log x) | O(1) |
| Split Array Largest Sum | O(n * log(sum)) | O(1) |
| Ship Within Days | O(n * log(sum)) | O(1) |
| Infinite Array Search | O(log n) | O(1) |
| Mountain Array Search | O(log n) | O(1) |
