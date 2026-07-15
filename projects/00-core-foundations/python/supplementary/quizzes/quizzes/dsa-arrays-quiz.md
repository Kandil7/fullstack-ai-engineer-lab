# DSA: Arrays - Quiz

## Topic Overview
Arrays are the most fundamental data structure, storing elements in contiguous memory locations. This quiz covers array operations, traversal, manipulation, two-pointer techniques, and sliding window patterns essential for coding interviews and competitive programming.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is the time complexity of accessing an element by index in an array?
- **A)** O(n)
- **B)** O(log n)
- **C)** O(1)
- **D)** O(n log n)

**Correct Answer: C** — Arrays provide O(1) random access because elements are stored in contiguous memory. The address is computed as `base_address + index * element_size`.

---

### Q2. What is the worst-case time complexity of searching for an element in an unsorted array?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n²)

**Correct Answer: C** — In an unsorted array, you must check each element sequentially (linear search), giving O(n) worst case.

---

### Q3. Which of the following is NOT a valid way to create an array in Python?
- **A)** `arr = [1, 2, 3]`
- **B)** `arr = list()`
- **C)** `arr = array.array('i', [1, 2, 3])`
- **D)** `arr = dict()`

**Correct Answer: D** — `dict()` creates a dictionary, not an array. Lists and the `array` module create array-like structures in Python.

---

### Q4. What is the time complexity of inserting an element at the end of a dynamic array (when capacity is sufficient)?
- **A)** O(n)
- **B)** O(1)
- **C)** O(log n)
- **D)** O(n²)

**Correct Answer: B** — Appending to the end of a dynamic array with available capacity is O(1) amortized. When resizing is needed, it becomes O(n) occasionally.

---

### Q5. What is the space complexity of a 2D array with M rows and N columns?
- **A)** O(M)
- **B)** O(N)
- **C)** O(M + N)
- **D)** O(M × N)

**Correct Answer: D** — A 2D array of M rows and N columns stores M*N elements, giving O(M × N) space complexity.

---

### Q6. In the two-pointer technique, when is it most commonly used?
- **A)** Searching in a sorted array
- **B)** Finding pairs with a specific sum in a sorted array
- **C)** Traversing a binary tree
- **D)** Hashing elements

**Correct Answer: B** — Two pointers are ideal for sorted arrays when finding pairs, triplets, or solving problems like container with most water. Pointers move from both ends.

---

### Q7. What is the time complexity of removing an element from the middle of an array?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n²)

**Correct Answer: C** — Removing from the middle requires shifting all subsequent elements to fill the gap, giving O(n) time complexity.

---

### Q8. What is the sliding window technique primarily used for?
- **A)** Sorting arrays
- **B)** Finding subarrays/substrings meeting a condition
- **C)** Binary search
- **D)** Graph traversal

**Correct Answer: B** — Sliding window maintains a window over a portion of the array/string and slides it to find optimal subarrays or substrings, reducing brute-force O(n²) to O(n).

---

### Q9. Given `arr = [1, 2, 3, 4, 5]`, what does `arr[1:3]` return?
- **A)** [1, 2, 3]
- **B)** [2, 3]
- **C)** [2, 3, 4]
- **D)** [1, 2]

**Correct Answer: B** — Python slicing `[1:3]` returns elements at indices 1 and 2 (start inclusive, end exclusive), giving [2, 3].

---

### Q10. Which technique reduces the search space by half in each step?
- **A)** Linear search
- **B)** Binary search
- **C)** Two-pointer
- **D)** Sliding window

**Correct Answer: B** — Binary search compares the target with the middle element and eliminates half the remaining elements each iteration, achieving O(log n).

---

### Q11. What is the amortized time complexity of dynamic array resizing (doubling strategy)?
- **A)** O(n)
- **B)** O(n log n)
- **C)** O(1)
- **D)** O(log n)

**Correct Answer: C** — With the doubling strategy, occasional O(n) resizes are amortized over many O(1) insertions, giving O(1) amortized per insertion.

---

### Q12. What is the output of the following code?
```python
arr = [3, 1, 4, 1, 5, 9, 2, 6]
arr.sort()
print(arr[::2])
```
- **A)** [9, 5, 3, 1]
- **B)** [1, 1, 2, 3]
- **C)** [1, 2, 4, 6]
- **D)** [1, 4, 5, 9]

**Correct Answer: C** — After sorting: [1, 1, 2, 3, 4, 5, 6, 9]. `arr[::2]` takes every 2nd element starting from index 0: [1, 2, 4, 6].

---

### Q13. Which approach is best for finding the maximum subarray sum?
- **A)** Brute force checking all subarrays
- **B)** Kadane's algorithm
- **C)** Binary search
- **D)** Sorting and picking the largest

**Correct Answer: B** — Kadane's algorithm tracks the maximum sum ending at each position, achieving O(n) time and O(1) space — far better than O(n³) brute force.

---

### Q14. What is the time complexity of rotating an array by k positions?
- **A)** O(k)
- **B)** O(n)
- **C)** O(n log n)
- **D)** O(n²)

**Correct Answer: B** — Array rotation can be done in O(n) time using the reversal algorithm: reverse the entire array, then reverse the first k elements, then reverse the rest.

---

### Q15. In Python, what is the difference between a list and an array from the `array` module?
- **A)** Lists store homogeneous data; arrays store heterogeneous
- **B)** Lists are dynamic; arrays are fixed-size
- **C)** Arrays are type-restricted; lists can hold any type
- **D)** There is no difference

**Correct Answer: C** — The `array` module creates type-restricted arrays (e.g., all integers), while Python lists can hold mixed types. Lists are also more flexible with built-in methods.

---

### Q16. What is the time complexity of merging two sorted arrays of sizes m and n?
- **A)** O(m + n)
- **B)** O(m × n)
- **C)** O(m log n)
- **D)** O(n log m)

**Correct Answer: A** — Merging two sorted arrays uses the two-pointer technique: compare elements from both arrays and place the smaller one, resulting in O(m + n) time.

---

### Q17. Which problem is an example of the prefix sum technique?
- **A)** Finding duplicate elements
- **B)** Range sum queries on an array
- **C)** Sorting an array
- **D)** Finding the median

**Correct Answer: B** — Prefix sums allow O(1) range sum queries after O(n) preprocessing. `prefix[i] = arr[0] + arr[1] + ... + arr[i-1]`.

---

### Q18. What is the worst-case time complexity of inserting at the beginning of an array?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n²)

**Correct Answer: C** — Inserting at the beginning requires shifting all n elements to make room, giving O(n) time complexity.

---

### Q19. What is the output of this code?
```python
arr = [1, 2, 3, 4, 5]
arr.insert(2, 10)
print(len(arr))
```
- **A)** 5
- **B)** 6
- **C)** 7
- **D)** Error

**Correct Answer: B** — `insert(2, 10)` adds 10 at index 2, shifting elements right. The array becomes [1, 2, 10, 3, 4, 5] with length 6.

---

### Q20. Which technique is used to find the majority element that appears more than n/2 times?
- **A)** Boyer-Moore Voting Algorithm
- **B)** Quickselect
- **C)** Merge Sort
- **D)** Breadth-First Search

**Correct Answer: A** — Boyer-Moore Voting Algorithm finds the majority element in O(n) time and O(1) space by maintaining a candidate and counter.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | C | 11 | C |
| 2 | C | 12 | C |
| 3 | D | 13 | B |
| 4 | B | 14 | B |
| 5 | D | 15 | C |
| 6 | B | 16 | A |
| 7 | C | 17 | B |
| 8 | B | 18 | C |
| 9 | B | 19 | B |
| 10 | B | 20 | A |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong arrays knowledge
