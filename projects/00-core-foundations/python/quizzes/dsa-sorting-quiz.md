# DSA: Sorting Algorithms - Quiz

## Topic Overview
Sorting algorithms arrange elements in a specific order (ascending/descending). This quiz covers comparison-based sorts (bubble, selection, insertion, merge, quick, heap), non-comparison sorts (counting, radix), and their complexities, trade-offs, and use cases.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is the best-case time complexity of Bubble Sort?
- **A)** O(n)
- **B)** O(n log n)
- **C)** O(n²)
- **D)** O(log n)

**Correct Answer: A** — With an optimization flag (detecting no swaps), Bubble Sort's best case is O(n) when the array is already sorted.

---

### Q2. What is the average time complexity of Quick Sort?
- **A)** O(n)
- **B)** O(n log n)
- **C)** O(n²)
- **D)** O(n log n) average, O(n²) worst

**Correct Answer: D** — Quick Sort averages O(n log n) but has O(n²) worst case (e.g., already sorted array with poor pivot selection).

---

### Q3. Which sorting algorithm is guaranteed O(n log n) in ALL cases?
- **A)** Quick Sort
- **B)** Bubble Sort
- **C)** Merge Sort
- **D)** Selection Sort

**Correct Answer: C** — Merge Sort always divides the array in half and merges, guaranteeing O(n log n) in best, average, and worst cases.

---

### Q4. Which sorting algorithm is NOT stable?
- **A)** Bubble Sort
- **B)** Merge Sort
- **C)** Quick Sort
- **D)** Insertion Sort

**Correct Answer: C** — Standard Quick Sort is not stable because partitioning can change the relative order of equal elements.

---

### Q5. What is the time complexity of Selection Sort?
- **A)** O(n)
- **B)** O(n log n)
- **C)** O(n²)
- **D)** O(log n)

**Correct Answer: C** — Selection Sort always performs n(n-1)/2 comparisons, giving O(n²) in all cases regardless of input.

---

### Q6. What is the space complexity of Merge Sort?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n²)

**Correct Answer: C** — Merge Sort requires O(n) auxiliary space for the temporary arrays used during merging.

---

### Q7. Which sorting algorithm works best for nearly sorted data?
- **A)** Quick Sort
- **B)** Bubble Sort
- **C)** Insertion Sort
- **D)** Heap Sort

**Correct Answer: C** — Insertion Sort is O(n) for nearly sorted data (adaptive), as each element only needs a few shifts to reach its position.

---

### Q8. What is the worst-case time complexity of Quick Sort?
- **A)** O(n log n)
- **B)** O(n²)
- **C)** O(n)
- **D)** O(log n)

**Correct Answer: B** — Quick Sort's worst case occurs when the pivot is always the smallest or largest element, degrading to O(n²).

---

### Q9. Which sorting algorithm uses a heap data structure?
- **A)** Quick Sort
- **B)** Merge Sort
- **C)** Heap Sort
- **D)** Bubble Sort

**Correct Answer: C** — Heap Sort builds a max-heap from the array, then repeatedly extracts the maximum element, achieving O(n log n) time.

---

### Q10. What is the time complexity of Counting Sort?
- **A)** O(n log n)
- **B)** O(n + k) where k is the range of input
- **C)** O(n²)
- **D)** O(k log n)

**Correct Answer: B** — Counting Sort runs in O(n + k) time, making it efficient when k (range of values) is small relative to n.

---

### Q11. What is a stable sorting algorithm?
- **A)** An algorithm that sorts in O(n log n)
- **B)** An algorithm that preserves the relative order of equal elements
- **C)** An algorithm that always uses O(1) space
- **D)** An algorithm that sorts in-place

**Correct Answer: B** — Stability means equal elements maintain their original relative order after sorting.

---

### Q12. What is the output of this sorting algorithm?
```python
arr = [64, 34, 25, 12, 22, 11, 90]
# After one pass of bubble sort (without optimization):
```
- **A)** [34, 25, 12, 22, 11, 64, 90]
- **B)** [11, 12, 22, 25, 34, 64, 90]
- **C)** [64, 34, 25, 12, 22, 11, 90]
- **D)** [90, 64, 34, 25, 22, 12, 11]

**Correct Answer: A** — After one pass of bubble sort, the largest element (90) bubbles to the end. Comparisons swap adjacent elements: [34, 25, 12, 22, 11, 64, 90].

---

### Q13. What is Radix Sort's time complexity?
- **A)** O(n log n)
- **B)** O(d × (n + b)) where d = digits, b = base
- **C)** O(n²)
- **D)** O(n)

**Correct Answer: B** — Radix Sort processes d digits using a stable sort (like counting sort) for each digit, giving O(d × (n + b)).

---

### Q14. Which sorting algorithm is best for sorting linked lists?
- **A)** Quick Sort
- **B)** Merge Sort
- **C)** Heap Sort
- **D)** Selection Sort

**Correct Answer: B** — Merge Sort works well for linked lists because it doesn't require random access. It achieves O(n log n) without extra space for linked lists.

---

### Q15. What is the worst-case space complexity of Quick Sort?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n log n)

**Correct Answer: C** — Quick Sort's recursion stack can go O(n) deep in the worst case (unbalanced partitions), though good pivot selection (median-of-three) limits it to O(log n).

---

### Q16. What is the lower bound for comparison-based sorting?
- **A)** O(n)
- **B)** O(n log n)
- **C)** O(n²)
- **D)** O(log n)

**Correct Answer: B** — Information theory proves that any comparison-based sort must perform at least O(n log n) comparisons in the worst case.

---

### Q17. Which of these is a non-comparison sort?
- **A)** Merge Sort
- **B)** Quick Sort
- **C)** Counting Sort
- **D)** Heap Sort

**Correct Answer: C** — Counting Sort (and Radix/Bucket Sort) don't compare elements directly. They use properties of the data (like integer range) to sort.

---

### Q18. What is the time complexity of insertion sort for a reverse-sorted array?
- **A)** O(n)
- **B)** O(n log n)
- **C)** O(n²)
- **D)** O(1)

**Correct Answer: C** — For reverse-sorted input, insertion sort must shift all previous elements for each insertion, giving O(n²) worst case.

---

### Q19. What makes Tim Sort efficient for real-world data?
- **A)** It's always O(n log n)
- **B)** It detects and exploits existing runs (sorted subsequences) in the data
- **C)** It uses no extra space
- **D)** It's the fastest comparison sort

**Correct Answer: B** — Tim Sort (Python's built-in sort) finds existing sorted runs and merges them efficiently, achieving O(n) for nearly sorted data.

---

### Q20. What is the space complexity of Heap Sort?
- **A)** O(n)
- **B)** O(log n)
- **C)** O(1)
- **D)** O(n log n)

**Correct Answer: C** — Heap Sort sorts in-place by building the heap within the original array, requiring only O(1) auxiliary space.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | A | 11 | B |
| 2 | D | 12 | A |
| 3 | C | 13 | B |
| 4 | C | 14 | B |
| 5 | C | 15 | C |
| 6 | C | 16 | B |
| 7 | C | 17 | C |
| 8 | B | 18 | C |
| 9 | C | 19 | B |
| 10 | B | 20 | C |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong sorting algorithm knowledge
