# DSA: Stacks & Queues - Quiz

## Topic Overview
Stacks and queues are linear data structures with specific access patterns. Stacks follow LIFO (Last In, First Out) while queues follow FIFO (First In, First Out). This quiz covers stack/queue operations, implementations, applications, and related problems.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What does LIFO stand for in the context of stacks?
- **A)** Last In, First Out
- **B)** Last In, Fast Output
- **C)** Linear Input, Fixed Output
- **D)** Linked Input, Functional Output

**Correct Answer: A** — LIFO means the last element pushed onto the stack is the first one removed (popped).

---

### Q2. What is the time complexity of push and pop operations on a stack?
- **A)** O(n)
- **B)** O(log n)
- **C)** O(1)
- **D)** O(n²)

**Correct Answer: C** — Both push and pop operate at the top of the stack, requiring O(1) time.

---

### Q3. Which operation is NOT valid for a stack?
- **A)** push
- **B)** pop
- **C)** peek
- **D)** enqueue

**Correct Answer: D** — Enqueue is a queue operation. Stacks use push, pop, peek/top, and isEmpty.

---

### Q4. What is FIFO in the context of queues?
- **A)** First In, First Out
- **B)** Fast In, Fast Output
- **C)** Fixed Input, Fixed Output
- **D)** First Index, First Output

**Correct Answer: A** — FIFO means the first element enqueued is the first one dequeued.

---

### Q5. What is the time complexity of enqueue and dequeue in a well-implemented queue?
- **A)** O(n)
- **B)** O(log n)
- **C)** O(1)
- **D)** O(n²)

**Correct Answer: C** — A properly implemented queue (with head and tail pointers or circular buffer) provides O(1) enqueue and dequeue.

---

### Q6. Which of the following is a common application of stacks?
- **A)** Print job scheduling
- **B)** Function call management (call stack)
- **C)** CPU scheduling
- **D)** Network packet routing

**Correct Answer: B** — The call stack manages function calls: each call pushes a frame, each return pops it. This is the primary use of stacks in programming.

---

### Q7. What data structure is used to implement a recursive function's local variables?
- **A)** Queue
- **B)** Array
- **C)** Stack
- **D)** Hash table

**Correct Answer: C** — Recursion uses the call stack to store return addresses, parameters, and local variables for each function call.

---

### Q8. What is a balanced parentheses problem?
- **A)** Checking if all opening parentheses have matching closing ones
- **B)** Counting total parentheses
- **C)** Converting infix to postfix
- **D)** Both A and C

**Correct Answer: A** — The balanced parentheses problem uses a stack: push opening brackets, pop on closing brackets, and verify the stack is empty at the end.

---

### Q9. What is a priority queue?
- **A)** A queue where elements are served in FIFO order
- **B)** A queue where elements are served based on priority, not insertion order
- **C)** A queue that only stores one element
- **D)** A queue with two ends

**Correct Answer: B** — A priority queue dequeues the highest-priority element first. It's commonly implemented with a heap.

---

### Q10. What is the output of this code?
```python
stack = [1, 2, 3, 4]
stack.append(5)
stack.pop()
print(stack[-1])
```
- **A)** 5
- **B)** 4
- **C)** 3
- **D)** Error

**Correct Answer: B** — After append(5): [1, 2, 3, 4, 5]. After pop(): [1, 2, 3, 4]. `stack[-1]` is 4.

---

### Q11. What is a circular queue?
- **A)** A queue that wraps around using modular arithmetic
- **B)** A queue that only allows one traversal
- **C)** A queue with no size limit
- **D)** A queue that sorts elements

**Correct Answer: A** — A circular queue uses modular arithmetic (`index % size`) to wrap around, efficiently reusing space in a fixed-size array.

---

### Q12. Which of the following uses a stack?
- **A)** Undo functionality in text editors
- **B)** Browser back button
- **C)** Expression evaluation
- **D)** All of the above

**Correct Answer: D** — Stacks power undo/redo, browser history navigation, expression evaluation (postfix), and many other features.

---

### Q13. What is the time complexity of reversing a queue using a stack?
- **A)** O(n)
- **B)** O(n log n)
- **C)** O(n²)
- **D)** O(1)

**Correct Answer: A** — Dequeue all elements and push onto stack (O(n)), then pop all and enqueue (O(n)). Total: O(n).

---

### Q14. What is a monotonic stack?
- **A)** A stack that only stores unique elements
- **B)** A stack where elements are in strictly increasing or decreasing order
- **C)** A stack that never shrinks
- **D)** A stack with a fixed maximum size

**Correct Answer: B** — A monotonic stack maintains elements in sorted order (increasing or decreasing), useful for problems like "next greater element."

---

### Q15. Which of the following correctly implements a queue using two stacks?
- **A)** Push to stack 1; pop from stack 2 (refill from stack 1 when empty)
- **B)** Push to both stacks simultaneously
- **C)** Pop from stack 1 and push to stack 2
- **D)** Use only one stack

**Correct Answer: A** — The two-stack queue: enqueue pushes to stack1. Dequeue pops from stack2; if empty, transfer all from stack1 to stack2 first.

---

### Q16. What is the output of this code?
```python
from collections import deque
queue = deque([1, 2, 3])
queue.append(4)
queue.popleft()
print(list(queue))
```
- **A)** [1, 2, 3, 4]
- **B)** [2, 3, 4]
- **C)** [1, 2, 4]
- **D)** [4, 3, 2]

**Correct Answer: B** — After append(4): [1, 2, 3, 4]. After popleft(): [2, 3, 4]. The deque provides O(1) popleft.

---

### Q17. What is the next greater element problem?
- **A)** Finding the smallest element in an array
- **B)** For each element, finding the next element that is greater than it
- **C)** Finding the maximum element
- **D)** Sorting the array

**Correct Answer: B** — The next greater element for each element is the first element to its right that is greater. A monotonic stack solves this in O(n).

---

### Q18. What is a deque (double-ended queue)?
- **A)** A queue that allows insertion and removal from both ends
- **B)** A queue with two separate data stores
- **C)** A priority queue with two priorities
- **D)** A queue that stores duplicates

**Correct Answer: A** — A deque supports O(1) insertion and removal at both the front and rear ends, making it more flexible than a standard queue.

---

### Q19. What is the time complexity of converting infix to postfix using a stack?
- **A)** O(n)
- **B)** O(n log n)
- **C)** O(n²)
- **D)** O(log n)

**Correct Answer: A** — The Shunting-Yard algorithm processes each token once (O(n)) and uses a stack for operators. Total: O(n).

---

### Q20. Which data structure is used in BFS (Breadth-First Search)?
- **A)** Stack
- **B)** Queue
- **C)** Priority Queue
- **D)** Heap

**Correct Answer: B** — BFS explores nodes level by level using a queue. Enqueue neighbors, dequeue the next node to visit.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | A | 11 | A |
| 2 | C | 12 | D |
| 3 | D | 13 | A |
| 4 | A | 14 | B |
| 5 | C | 15 | A |
| 6 | B | 16 | B |
| 7 | C | 17 | B |
| 8 | A | 18 | A |
| 9 | B | 19 | A |
| 10 | B | 20 | B |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong stacks and queues knowledge
