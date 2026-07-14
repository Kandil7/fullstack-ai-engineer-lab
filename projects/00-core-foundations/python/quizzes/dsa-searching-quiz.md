# DSA: Searching Algorithms - Quiz

## Topic Overview
Searching algorithms find specific elements or determine their absence in a data structure. This quiz covers linear search, binary search, variations of binary search, hash-based searching, and search-related problem-solving patterns.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is the time complexity of linear search?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n²)

**Correct Answer: C** — Linear search checks each element sequentially, requiring up to n comparisons in the worst case.

---

### Q2. What is the prerequisite for binary search?
- **A)** The array must be sorted
- **B)** The array must be a linked list
- **C)** The array must be unsorted
- **D)** The array must have even length

**Correct Answer: A** — Binary search requires sorted data to determine which half to discard based on comparison with the middle element.

---

### Q3. What is the time complexity of binary search?
- **A)** O(n)
- **B)** O(log n)
- **C)** O(n log n)
- **D)** O(1)

**Correct Answer: B** — Binary search halves the search space each step, giving O(log n) time complexity.

---

### Q4. What is the space complexity of iterative binary search?
- **A)** O(n)
- **B)** O(log n)
- **C)** O(1)
- **D)** O(n²)

**Correct Answer: C** — Iterative binary search uses only a few pointer variables (low, high, mid), requiring O(1) space.

---

### Q5. What is the space complexity of recursive binary search?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n log n)

**Correct Answer: B** — Recursive binary search uses O(log n) stack space due to the recursion depth equal to the number of halvings.

---

### Q6. What is the output of binary search for target=7 in `[1, 3, 5, 7, 9, 11]`?
- **A)** Index 0
- **B)** Index 2
- **C)** Index 3
- **D)** Index 4

**Correct Answer: C** — Binary search: mid=(0+5)//2=2, arr[2]=5 < 7, search right. mid=(3+5)//2=4, arr[4]=9 > 7, search left. mid=(3+3)//2=3, arr[3]=7 found at index 3.

---

### Q7. What is a hash table's average-case search time?
- **A)** O(n)
- **B)** O(log n)
- **C)** O(1)
- **D)** O(n log n)

**Correct Answer: C** — Hash tables provide O(1) average-case search by computing a hash to directly access the bucket. Worst case is O(n) with collisions.

---

### Q8. What causes worst-case O(n) search in a hash table?
- **A)** Large table size
- **B)** All keys hash to the same bucket (collision)
- **C)** Small key values
- **D)** Using a good hash function

**Correct Answer: B** — When all keys collide (same bucket), the hash table degrades to a linked list, requiring O(n) search.

---

### Q9. What is the sentinel linear search technique?
- **A)** Using a binary tree for search
- **B)** Placing the target at the end of the array to eliminate bounds checking
- **C)** Using recursion for search
- **D)** Searching from both ends simultaneously

**Correct Answer: B** — Sentinel search places the target value at the end of the array, eliminating the need to check for array bounds in each iteration.

---

### Q10. What is the output of this code?
```python
def binary_search(arr, target):
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

print(binary_search([2, 4, 6, 8, 10], 6))
```
- **A)** 0
- **B)** 1
- **C)** 2
- **D)** -1

**Correct Answer: C** — mid=(0+4)//2=2, arr[2]=6==6, returns index 2.

---

### Q11. What is the difference between lower_bound and upper_bound in binary search?
- **A)** lower_bound finds first position ≤ target; upper_bound finds first position > target
- **B)** They are the same
- **C)** lower_bound finds first position ≥ target; upper_bound finds first position > target
- **D)** lower_bound is for arrays; upper_bound is for linked lists

**Correct Answer: C** — lower_bound returns the first index where element ≥ target (first occurrence). upper_bound returns the first index where element > target.

---

### Ternary Search
### Q12. What is ternary search's time complexity?
- **A)** O(log n)
- **B)** O(log₃ n)
- **C)** O(n/3)
- **D)** O(n)

**Correct Answer: B** — Ternary search divides the search space into three parts, giving O(log₃ n) which is equivalent to O(log n) asymptotically.

---

### Q13. What is exponential search useful for?
- **A)** Searching in unsorted arrays
- **B)** Searching in arrays with unknown bounds or infinite arrays
- **C)** Searching in trees
- **D)** Searching in graphs

**Correct Answer: B** — Exponential search first finds a range by doubling the index, then applies binary search. Ideal for unbounded/infinite arrays.

---

### Q14. What is the time complexity of interpolation search on uniformly distributed sorted data?
- **A)** O(log n)
- **B)** O(1) average
- **C)** O(log log n) average
- **D)** O(n)

**Correct Answer: C** — Interpolation search estimates the position based on value distribution, achieving O(log log n) average for uniform data (O(n) worst case).

---

### Q15. What is the output of this code?
```python
def find_first(arr, target):
    low, high = 0, len(arr) - 1
    result = -1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            result = mid
            high = mid - 1
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return result

print(find_first([1, 2, 2, 2, 3, 4], 2))
```
- **A)** 3
- **B)** 1
- **C)** 2
- **D)** -1

**Correct Answer: B** — This finds the first occurrence of target. It finds 2 at index 2, then continues searching left, finding the first occurrence at index 1.

---

### Q16. What is the jump search technique?
- **A)** Jumping to random positions
- **B)** Jumping ahead by fixed blocks (√n), then doing linear search within the block
- **C)** Using a hash table
- **D)** Binary search with recursion

**Correct Answer: B** — Jump search jumps √n steps at a time, then does linear search in the identified block. Time: O(√n).

---

### Q17. What is the time complexity of Fibonacci search?
- **A)** O(n)
- **B)** O(log n)
- **C)** O(√n)
- **D)** O(n log n)

**Correct Answer: B** — Fibonacci search uses Fibonacci numbers to divide the array, achieving O(log n) time, similar to binary search.

---

### Q18. In which scenario does binary search outperform linear search?
- **A)** Unsorted data
- **B)** Small datasets (n < 10)
- **C)** Large sorted datasets
- **D)** When data changes frequently

**Correct Answer: C** — Binary search's O(log n) advantage is significant for large sorted datasets. For small n or unsorted data, linear search is often better.

---

### Q19. What is the time complexity of searching in a balanced BST?
- **A)** O(n)
- **B)** O(log n)
- **C)** O(1)
- **D)** O(n log n)

**Correct Answer: B** — A balanced BST has height O(log n), so search follows a single root-to-leaf path: O(log n).

---

### Q20. What is the advantage of using a hash set over binary search for membership testing?
- **A)** Hash set uses less memory
- **B)** Hash set provides O(1) average lookup vs O(log n) for binary search
- **C)** Hash set maintains sorted order
- **D)** Hash set is always faster

**Correct Answer: B** — Hash sets provide O(1) average-case lookup. Binary search requires O(log n) and sorted data. Hash sets don't maintain order.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | C | 11 | C |
| 2 | A | 12 | B |
| 3 | B | 13 | B |
| 4 | C | 14 | C |
| 5 | B | 15 | B |
| 6 | C | 16 | B |
| 7 | C | 17 | B |
| 8 | B | 18 | C |
| 9 | B | 19 | B |
| 10 | C | 20 | B |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong searching algorithm knowledge
