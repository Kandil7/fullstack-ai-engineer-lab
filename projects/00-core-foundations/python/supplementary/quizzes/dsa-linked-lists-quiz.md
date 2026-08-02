# DSA: Linked Lists - Quiz

## Topic Overview
Linked lists are linear data structures where elements (nodes) are connected via pointers. Unlike arrays, they allow efficient insertions and deletions but lack random access. This quiz covers singly linked lists, doubly linked lists, circular linked lists, and common operations.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is the time complexity of inserting a node at the beginning of a singly linked list?
- **A)** O(n)
- **B)** O(1)
- **C)** O(log n)
- **D)** O(n²)

**Correct Answer: B** — Inserting at the head only requires updating the new node's next pointer and the head reference, which is O(1).

---

### Q2. What is the primary advantage of a linked list over an array?
- **A)** Faster random access
- **B)** Less memory usage
- **C)** Efficient insertions and deletions at arbitrary positions
- **D)** Better cache performance

**Correct Answer: C** — Linked lists excel at O(1) insertions/deletions (given a pointer to the position), while arrays require O(n) shifting for middle operations.

---

### Q3. What is the time complexity of searching for an element in an unsorted singly linked list?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n²)

**Correct Answer: C** — You must traverse from the head to find an element, checking each node. Worst case visits all n nodes.

---

### Q4. Which of the following correctly defines a node in a singly linked list?
- **A)** A node contains data and a pointer to the next node
- **B)** A node contains data and pointers to both next and previous nodes
- **C)** A node contains only data
- **D)** A node contains an array of elements

**Correct Answer: A** — A singly linked list node has `data` and a `next` pointer. Doubly linked list nodes have both `next` and `prev` pointers.

---

### Q5. What is the time complexity of reversing a singly linked list iteratively?
- **A)** O(n²)
- **B)** O(n log n)
- **C)** O(n)
- **D)** O(1)

**Correct Answer: C** — Iterative reversal traverses the list once, adjusting pointers. Each node is visited exactly once: O(n) time, O(1) space.

---

### Q6. In a doubly linked list, what is the space overhead per node compared to a singly linked list?
- **A)** No extra space
- **B)** One extra pointer (prev)
- **C)** Two extra pointers
- **D)** One extra integer

**Correct Answer: B** — Each doubly linked list node stores an additional `prev` pointer, increasing space by one pointer per node.

---

### Q7. What is the time complexity of deleting the last node in a singly linked list without a tail pointer?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n²)

**Correct Answer: C** — Without a tail pointer, you must traverse to the second-to-last node (O(n)), then update its next pointer.

---

### Q8. What is a circular linked list?
- **A)** A linked list where the last node points back to the first node
- **B)** A linked list with a cycle caused by a bug
- **C)** A linked list that is always sorted
- **D)** A linked list with duplicate elements

**Correct Answer: A** — In a circular linked list, the last node's next pointer references the head node, forming a cycle. This is by design, not a bug.

---

### Q9. Which technique detects a cycle in a linked list?
- **A)** Binary search
- **B)** Floyd's cycle detection (tortoise and hare)
- **C)** Depth-first search
- **D)** Breadth-first search

**Correct Answer: B** — Floyd's algorithm uses two pointers (slow and fast). If they meet, a cycle exists. Time: O(n), Space: O(1).

---

### Q10. What is the output of this code?
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

a = Node(1)
b = Node(2)
c = Node(3)
a.next = b
b.next = c

current = a
while current:
    print(current.data, end=" ")
    current = current.next
```
- **A)** 1 2 3
- **B)** 3 2 1
- **C)** 1 3 2
- **D)** 2 1 3

**Correct Answer: A** — The traversal starts at a (1), follows next to b (2), then c (3), then None terminates the loop. Output: "1 2 3".

---

### Q11. What is the time complexity of finding the middle element of a singly linked list?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n²)

**Correct Answer: C** — Using the slow/fast pointer technique, slow moves one step while fast moves two. When fast reaches the end, slow is at the middle: O(n) time.

---

### Q12. Which data structure would you use to implement a queue with O(1) enqueue and dequeue?
- **A)** Array
- **B)** Singly linked list with tail pointer
- **C)** Stack
- **D)** Binary search tree

**Correct Answer: B** — A singly linked list with both head and tail pointers allows O(1) enqueue (at tail) and O(1) dequeue (from head).

---

### Q13. What is the difference between a singly linked list and a circular doubly linked list?
- **A)** No difference
- **B)** Circular doubly has both prev/next pointers and last node points to first
- **C)** Singly linked list has prev pointers
- **D)** Circular doubly is always sorted

**Correct Answer: B** — A circular doubly linked list has nodes with both `next` and `prev` pointers, and the last node's `next` points to the first while the first's `prev` points to the last.

---

### Q14. What is the time complexity of merging two sorted linked lists?
- **A)** O(n × m)
- **B)** O(n + m)
- **C)** O(n log m)
- **D)** O(n²)

**Correct Answer: B** — Merging two sorted linked lists compares heads of both lists and picks the smaller one, similar to merge sort's merge step: O(n + m).

---

### Q15. What problem does the "two-pointer" technique solve efficiently on linked lists?
- **A)** Finding the intersection of two lists
- **B)** Finding the cycle start point
- **C)** Reversing the list
- **D)** All of the above

**Correct Answer: D** — Two-pointer techniques are versatile: Floyd's for cycle detection, fast/slow for middle finding, and offset pointers for intersection detection.

---

### Q16. What is the time complexity of inserting a node after a given node in a singly linked list?
- **A)** O(n)
- **B)** O(1)
- **C)** O(log n)
- **D)** O(n²)

**Correct Answer: B** — If you already have a pointer to the node, inserting after it only requires updating two pointers: O(1).

---

### Q17. What is the main disadvantage of a linked list compared to an array?
- **A)** Uses more memory
- **B)** No random access; must traverse sequentially
- **C)** Cannot store heterogeneous data
- **D)** Fixed size

**Correct Answer: B** — Linked lists don't support O(1) indexed access. Accessing the k-th element requires O(k) traversal from the head.

---

### Q18. Which of the following is true about a linked list's memory allocation?
- **A)** All nodes are stored in contiguous memory
- **B)** Nodes can be scattered in memory, connected by pointers
- **C)** Nodes must be allocated on the stack
- **D)** Memory is allocated in blocks of 1024 bytes

**Correct Answer: B** — Unlike arrays, linked list nodes are dynamically allocated and can reside anywhere in memory, connected via pointer references.

---

### Q19. What is the output?
```python
def reverse(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev
```
- **A)** Reverses the list in O(n) time and O(1) space
- **B)** Reverses the list in O(n) time and O(n) space
- **C)** Creates a copy of the list
- **D)** Does nothing

**Correct Answer: A** — This is the classic iterative reversal: O(n) time (single pass), O(1) space (only pointer variables used).

---

### Q20. What is a sentinel node (dummy head) in linked lists used for?
- **A)** Storing extra data
- **B)** Simplifying edge cases like empty lists and head insertions
- **C)** Making the list circular
- **D)** Increasing search speed

**Correct Answer: B** — A sentinel/dummy head simplifies code by eliminating special cases for empty lists or operations at the head position.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 11 | C |
| 2 | C | 12 | B |
| 3 | C | 13 | B |
| 4 | A | 14 | B |
| 5 | C | 15 | D |
| 6 | B | 16 | B |
| 7 | C | 17 | B |
| 8 | A | 18 | B |
| 9 | B | 19 | A |
| 10 | A | 20 | B |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong linked list knowledge
