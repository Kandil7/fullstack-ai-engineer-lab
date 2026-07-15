# DSA Arrays Interview Practice

## Topic Overview

Arrays are the most fundamental data structure. Master array manipulation is critical for technical interviews. Key techniques include **two pointers**, **sliding window**, **prefix sum**, and **Kadane's algorithm**. Problems often test your ability to optimize from brute force O(n²) to linear or O(n log n) solutions.

**Core Properties:**
- Contiguous memory allocation
- O(1) random access by index
- O(n) insertion/deletion in the middle
- Fixed or dynamic sizing (Python lists are dynamic)

---

## Interview Questions (with Answers)

### Q1: What is the time complexity of accessing, inserting, and deleting elements in an array?

**Answer:**
- Access by index: **O(1)** — direct memory offset calculation
- Insert at end (amortized): **O(1)** for dynamic arrays, **O(n)** for fixed-size
- Insert at beginning/middle: **O(n)** — requires shifting elements
- Delete at end: **O(1)** amortized
- Delete at beginning/middle: **O(n)** — requires shifting elements
- Search in unsorted: **O(n)**
- Search in sorted: **O(log n)** via binary search

---

### Q2: Explain the two pointers technique. When would you use it?

**Answer:**
Two pointers use two indices to traverse an array (or linked list), typically from opposite ends or at different speeds. Common patterns:

- **Opposite ends**: Two sum on sorted array, palindrome check, container with most water
- **Same direction (fast/slow)**: Remove duplicates, partition array
- **Converging**: Valid palindrome, trapping rain water

Example — Two Sum (Sorted Array):
```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        curr = nums[left] + nums[right]
        if curr == target:
            return [left, right]
        elif curr < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]
```
**Time: O(n), Space: O(1)**

---

### Q3: What is the sliding window technique? Give an example.

**Answer:**
Sliding window maintains a "window" (subset) of elements and slides it across the array. It's used for problems involving contiguous subarrays.

**Fixed-size window** — Maximum sum of k consecutive elements:
```python
def max_sum_k(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

**Variable-size window** — Longest subarray with sum ≤ k:
```python
def longest_subarray_sum(nums, k):
    left = 0
    curr_sum = 0
    max_len = 0
    for right in range(len(nums)):
        curr_sum += nums[right]
        while curr_sum > k:
            curr_sum -= nums[left]
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len
```
**Time: O(n), Space: O(1)**

---

### Q4: Explain prefix sum and when to use it.

**Answer:**
Prefix sum precomputes cumulative sums so that the sum of any subarray `nums[i..j]` can be answered in O(1).

```python
def build_prefix(nums):
    prefix = [0] * (len(nums) + 1)
    for i in range(len(nums)):
        prefix[i + 1] = prefix[i] + nums[i]
    return prefix

# Range sum query: sum of nums[i..j]
def range_sum(prefix, i, j):
    return prefix[j + 1] - prefix[i]
```

**When to use:**
- Frequent range sum queries on the same array
- Subarray sum equals k (combined with hash map)
- Counting subarrays with certain sum properties
- 2D prefix sums for matrix region queries

---

### Q5: What is Kadane's algorithm? Explain it with code.

**Answer:**
Kadane's algorithm finds the maximum subarray sum in O(n) time. It tracks the maximum sum ending at the current position.

```python
def max_subarray(nums):
    max_sum = nums[0]
    curr_sum = nums[0]
    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)
    return max_sum
```

**Key insight:** At each position, decide whether to extend the current subarray or start a new one. If `curr_sum < 0`, starting fresh is better.

**Variations:**
- Maximum product subarray: track both min and max (negative × negative = positive)
- Return the subarray itself: track start/end indices
- Circular array variant: total sum - min subarray sum

---

### Q6: How would you rotate an array by k positions?

**Answer:**
Three approaches:

**Approach 1 — Extra array (O(n) time, O(n) space):**
```python
def rotate(nums, k):
    n = len(nums)
    result = [0] * n
    for i in range(n):
        result[(i + k) % n] = nums[i]
    return result
```

**Approach 2 — Reversal trick (O(n) time, O(1) space):**
```python
def rotate_inplace(nums, k):
    n = len(nums)
    k %= n
    nums.reverse()
    nums[:k] = reversed(nums[:k])
    nums[k:] = reversed(nums[k:])
```
Steps for `[1,2,3,4,5,6,7]` with k=3: reverse all → `[7,6,5,4,3,2,1]`, reverse first 3 → `[5,6,7,4,3,2,1]`, reverse last 4 → `[5,6,7,1,2,3,4]`

**Approach 3 — Cyclic replacement (O(n) time, O(1) space):**
Move each element to its correct position, handling cycles.

---

### Q7: How do you find the intersection of two sorted arrays?

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
```

**Time: O(n + m), Space: O(1)** excluding output

---

### Q8: What is the difference between a list and an array in Python?

**Answer:**
- Python `list` is a dynamic array of pointers to objects
- `array.array` stores homogeneous C-type values (more memory efficient)
- `numpy.ndarray` is optimized for numerical operations

In interview contexts, "array" usually means Python list. Key differences:
- Lists store any type; arrays store one type
- Lists have O(1) amortized append; arrays may need reallocation
- NumPy arrays support vectorized operations (O(n) without Python loops)

---

### Q9: How would you find the majority element in an array?

**Answer:**
**Boyer-Moore Voting Algorithm (O(n) time, O(1) space):**

```python
def majority_element(nums):
    candidate = None
    count = 0
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    return candidate
```

**Why it works:** The majority element appears more than n/2 times. Non-majority elements can at most cancel out the majority element, leaving it as the final candidate.

---

### Q10: How do you merge two sorted arrays in-place?

**Answer:**
Start from the end of both arrays and fill from the back:

```python
def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while i >= 0 and j >= 0:
        if nums1[i] >= nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1
```
**Time: O(m + n), Space: O(1)**

---

### Q11: What is the Dutch National Flag problem?

**Answer:**
Sort an array of 0s, 1s, and 2s in a single pass (O(n) time, O(1) space):

```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

**Invariant:** `nums[0..low-1]` = 0s, `nums[low..mid-1]` = 1s, `nums[high+1..n-1]` = 2s, `nums[mid..high]` = unsorted.

---

### Q12: How would you find all pairs in an array that sum to a target?

**Answer:**
**Hash map approach (O(n) time, O(n) space):**

```python
def two_sum_all(nums, target):
    seen = {}
    pairs = []
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            pairs.append((seen[complement], i))
        seen[num] = i
    return pairs
```

**For sorted array — two pointers (O(n) time, O(1) space):**
```python
def two_sum_sorted_pairs(nums, target):
    left, right = 0, len(nums) - 1
    pairs = []
    while left < right:
        curr = nums[left] + nums[right]
        if curr == target:
            pairs.append((left, right))
            left += 1
            right -= 1
        elif curr < target:
            left += 1
        else:
            right -= 1
    return pairs
```

---

### Q13: What is the difference between shallow and deep copy of an array?

**Answer:**
- **Shallow copy:** Copies the reference to nested objects. Modifications to nested objects affect both copies.
  ```python
  import copy
  shallow = copy.copy(nested_list)  # or list(nested_list) or nested_list[:]
  ```
- **Deep copy:** Recursively copies all nested objects. Fully independent.
  ```python
  deep = copy.deepcopy(nested_list)
  ```

**In interviews:** If the question says "modify the array in-place," don't copy. If it says "return a new array," clarify whether nested structures need independence.

---

### Q14: How do you find the missing number in an array of 0 to n?

**Answer:**
**Math approach (O(n) time, O(1) space):**
```python
def missing_number(nums):
    n = len(nums)
    expected = n * (n + 1) // 2
    return expected - sum(nums)
```

**XOR approach (O(n) time, O(1) space, no overflow risk):**
```python
def missing_number_xor(nums):
    xor = len(nums)
    for i, num in enumerate(nums):
        xor ^= i ^ num
    return xor
```

---

### Q15: Explain the concept of a monotonic array.

**Answer:**
A monotonic array is entirely non-increasing or non-decreasing:
- **Monotonically increasing:** `a[i] <= a[i+1]` for all i
- **Monotonically decreasing:** `a[i] >= a[i+1]` for all i

```python
def is_monotonic(nums):
    increasing = decreasing = True
    for i in range(1, len(nums)):
        if nums[i] > nums[i-1]:
            decreasing = False
        if nums[i] < nums[i-1]:
            increasing = False
    return increasing or decreasing
```

---

## Coding Challenges

### Challenge 1: Two Sum
Given an array of integers and a target, return indices of two numbers that add up to target.

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return [-1, -1]

# Test
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
```
**Time: O(n), Space: O(n)**

---

### Challenge 2: Best Time to Buy and Sell Stock
Given prices[i] = price on day i, find the maximum profit from one buy and one sell.

```python
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit

# Test
assert max_profit([7, 1, 5, 3, 6, 4]) == 5  # buy@1, sell@6
assert max_profit([7, 6, 4, 3, 1]) == 0
```
**Time: O(n), Space: O(1)**

---

### Challenge 3: Maximum Subarray (Kadane's Algorithm)
Find the contiguous subarray with the largest sum.

```python
def max_subarray(nums):
    max_sum = curr_sum = nums[0]
    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)
    return max_sum

# Test
assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6  # [4, -1, 2, 1]
```
**Time: O(n), Space: O(1)**

---

### Challenge 4: Container With Most Water
Given heights[i], find two lines that together with the x-axis form a container holding the most water.

```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        area = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, area)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water

# Test
assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
```
**Time: O(n), Space: O(1)**

---

### Challenge 5: Product of Array Except Self
Return an array where each element is the product of all other elements (no division allowed).

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n

    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]

    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]

    return result

# Test
assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
```
**Time: O(n), Space: O(1)** (excluding output array)

---

### Challenge 6: Trapping Rain Water
Given heights of bars, compute how much water can be trapped.

```python
def trap(height):
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]

    return water

# Test
assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
```
**Time: O(n), Space: O(1)**

---

### Challenge 7: Merge Intervals
Merge all overlapping intervals.

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged

# Test
assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
```
**Time: O(n log n), Space: O(n)**

---

### Challenge 8: Spiral Matrix
Return all elements of a matrix in spiral order.

```python
def spiral_order(matrix):
    if not matrix:
        return []
    result = []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1

        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1

        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1

        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1

    return result

# Test
assert spiral_order([[1,2,3],[4,5,6],[7,8,9]]) == [1,2,3,6,9,8,7,4,5]
```
**Time: O(m*n), Space: O(1)** excluding output

---

### Challenge 9: Subarray Sum Equals K
Count the number of contiguous subarrays whose sum equals k.

```python
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    seen = {0: 1}

    for num in nums:
        prefix_sum += num
        if prefix_sum - k in seen:
            count += seen[prefix_sum - k]
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1

    return count

# Test
assert subarray_sum([1, 1, 1], 2) == 2
assert subarray_sum([1, 2, 3], 3) == 2
```
**Time: O(n), Space: O(n)**

---

### Challenge 10: Next Permutation
Implement next permutation — rearranges numbers into the lexicographically next greater permutation.

```python
def next_permutation(nums):
    # Step 1: Find the first decreasing element from the right
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    # Step 2: Find the element to swap with
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]

    # Step 3: Reverse the suffix
    nums[i + 1:] = reversed(nums[i + 1:])

# Test
nums = [1, 2, 3]
next_permutation(nums)
assert nums == [1, 3, 2]
```
**Time: O(n), Space: O(1)**

---

## Common Follow-Up Questions

1. **"Can you do it in O(1) space?"** — Often yes, using in-place swaps or the input array for bookkeeping.
2. **"What if the array is very large and doesn't fit in memory?"** — Process in chunks, use external sort, or streaming algorithms.
3. **"What if the array is sorted?"** — Binary search, two pointers become more efficient.
4. **"Can you handle duplicates?"** — Use hash maps with counts, or handle duplicates explicitly in pointer logic.
5. **"What about negative numbers?"** — Most techniques (two pointers, sliding window) still work. Prefix sum + hash map works for subarray sums.
6. **"How would you parallelize this?"** — Split array into chunks, process in parallel, merge results (e.g., reduce pattern).

---

## Tips for Answering Array Questions

1. **Clarify constraints:** Ask about duplicates, empty arrays, negative numbers, sorted/unsorted.
2. **Start with brute force:** State the O(n²) or O(n³) approach, then optimize.
3. **Identify the pattern:** Is it two pointers? Sliding window? Prefix sum? Hash map?
4. **Edge cases:** Empty array, single element, all same elements, no valid answer.
5. **In-place vs. new array:** Check if the problem requires modifying the input.
6. **Python specifics:** Lists are dynamic arrays. Use `collections.Counter` for frequency problems. `enumerate()` is preferred over index-based loops.

---

## Complexity Cheat Sheet

| Problem | Time | Space |
|---------|------|-------|
| Two Sum (hash) | O(n) | O(n) |
| Two Sum (sorted, pointers) | O(n) | O(1) |
| Kadane's Algorithm | O(n) | O(1) |
| Sliding Window Max | O(n) | O(k) |
| Prefix Sum | O(n) precompute, O(1) query | O(n) |
| Rotate Array | O(n) | O(1) |
| Merge Sorted Arrays | O(m+n) | O(1) |
| Trapping Rain Water | O(n) | O(1) |
| Container With Most Water | O(n) | O(1) |
| Product Except Self | O(n) | O(1) |
