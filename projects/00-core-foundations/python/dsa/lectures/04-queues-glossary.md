# Glossary: Queues

> Quick reference for all terms introduced in Lecture 04.

---

## B

### BFS (Breadth-First Search)
- **Definition:** A graph traversal algorithm that explores all neighbors at the current depth before moving deeper. Uses a queue.
- **Time Complexity:** O(V + E)
- **Related:** Queue, DFS, Level-Order Traversal

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### Back
- **Definition:** The end of a queue where new elements are added (also called "rear" or "tail").
- **Related:** Front, Enqueue, Rear

---

## C

### Circular Queue
- **Definition:** A queue where the last position connects back to the first position, reusing freed space.
- **Example:** Buffer with fixed capacity that wraps around.
- **Related:** Ring Buffer, Queue

```
Circular Queue (capacity=4):
[_, A, B, C]  front=1, rear=3
Enqueue D:
[D, A, B, C]  front=1, rear=0  (wrapped)
Dequeue:
[D, _, B, C]  front=2, rear=0
```

```python
class CircularQueue:
    def __init__(self, capacity):
        self.items = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0
        self.capacity = capacity
    
    def enqueue(self, item):
        if self.size == self.capacity:
            raise OverflowError("Queue full")
        self.rear = (self.rear + 1) % self.capacity
        self.items[self.rear] = item
        self.size += 1
    
    def dequeue(self):
        if self.size == 0:
            raise IndexError("Queue empty")
        item = self.items[self.front]
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item
```

---

## D

### Dequeue (Data Structure)
- **Definition:** Double-Ended Queue — allows insertion and deletion at both ends in O(1).
- **Example:** Python `collections.deque`.
- **Related:** Queue, Stack, FIFO, LIFO

```python
from collections import deque
dq = deque([1, 2, 3])
dq.append(4)      # Add to right: [1, 2, 3, 4]
dq.appendleft(0)  # Add to left: [0, 1, 2, 3, 4]
dq.pop()           # Remove right: [0, 1, 2, 3]
dq.popleft()       # Remove left: [1, 2, 3]
```

### Dequeue (Operation)
- **Definition:** Removing and returning the front element of a queue.
- **Time Complexity:** O(1) for linked list and deque implementations.
- **Related:** Enqueue, Peek, FIFO

```python
from collections import deque
queue = deque(["A", "B", "C"])
item = queue.popleft()  # Returns "A"
```

---

## E

### Enqueue
- **Definition:** Adding an element to the back (rear) of a queue.
- **Time Complexity:** O(1) for linked list and deque implementations.
- **Related:** Dequeue, Peek, Rear

```python
from collections import deque
queue = deque()
queue.append("first")   # Enqueue
queue.append("second")  # Enqueue
```

### Empty Queue
- **Definition:** A queue containing no elements. Calling dequeue or peek raises an error.
- **Related:** Underflow, Is Empty

```python
queue = deque()
if not queue:
    print("Queue is empty")
```

---

## F

### FIFO (First In, First Out)
- **Definition:** The principle that the first element added is the first to be removed.
- **Example:** A line at a store — first person in line gets served first.
- **Related:** LIFO, Queue, Stack

```python
from collections import deque
queue = deque(["Alice", "Bob", "Charlie"])
print(queue.popleft())  # "Alice" — first in, first out
```

### Front
- **Definition:** The element at the beginning of a queue — the one to be dequeued next.
- **Related:** Rear, Peek, Dequeue

```python
queue = deque(["A", "B", "C"])
front = queue[0]  # "A"
```

---

## H

### Heap
- **Definition:** A complete binary tree where each node satisfies the heap property (min-heap or max-heap).
- **Example:** Used to implement priority queues.
- **Related:** Priority Queue, Min-Heap, Max-Heap

```python
import heapq

heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
print(heapq.heappop(heap))  # 1 (smallest first — min-heap)
```

---

## L

### Level-Order Traversal
- **Definition:** Visiting nodes of a tree level by level, left to right. Uses a queue.
- **Example:** BFS on a tree.
- **Related:** BFS, Queue, Tree Traversal

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

---

## M

### Monotonic Deque
- **Definition:** A deque maintained in sorted order (increasing or decreasing) to solve sliding window problems.
- **Example:** Finding max in every window of size k.
- **Related:** Sliding Window, Dequeue

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()  # Stores indices of decreasing values
    result = []
    for i in range(len(nums)):
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

---

## P

### Peek / Front
- **Definition:** Viewing the front element of a queue without removing it.
- **Time Complexity:** O(1)
- **Related:** Dequeue, Front

```python
queue = deque([1, 2, 3])
front = queue[0]  # Peek: returns 1 without removing
```

### Priority Queue
- **Definition:** A queue where each element has a priority, and elements are served in priority order (not insertion order).
- **Implementation:** Typically using a heap.
- **Related:** Heap, Min-Heap, Max-Heap

```python
import heapq

class PriorityQueue:
    def __init__(self):
        self._heap = []
    def push(self, item, priority):
        heapq.heappush(self._heap, (priority, item))
    def pop(self):
        return heapq.heappop(self._heap)[1]
    
pq = PriorityQueue()
pq.push("low", 5)
pq.push("high", 1)
print(pq.pop())  # "high" — lowest priority number = highest priority
```

---

## Q

### Queue
- **Definition:** A FIFO (First In, First Out) data structure — elements are added at the back and removed from the front.
- **Operations:** enqueue, dequeue, peek, is_empty.
- **Related:** FIFO, Dequeue, Stack

```python
from collections import deque
queue = deque()
queue.append("A")   # Enqueue
queue.append("B")   # Enqueue
queue.popleft()     # Dequeue: returns "A"
```

### Queue Overflow
- **Definition:** Error when trying to enqueue into a full fixed-size queue.
- **Related:** Circular Queue, Overflow, Full

---

## R

### Rear
- **Definition:** The end of a queue where new elements are added (also called "back" or "tail").
- **Related:** Front, Enqueue

---

## S

### Simple Queue
- **Definition:** A basic FIFO queue with enqueue, dequeue, and peek operations.
- **Related:** Queue, FIFO

```python
from queue import SimpleQueue
q = SimpleQueue()
q.put(1)
q.put(2)
print(q.get())  # 1
```

### Sliding Window
- **Definition:** A technique using a queue/deque to maintain a "window" of elements over a sequence.
- **Example:** Maximum of every k consecutive elements.
- **Related:** Dequeue, Monotonic Dequeue

```python
from collections import deque

def first_negative_in_window(arr, k):
    """Find first negative number in every window of size k."""
    result = []
    dq = deque()  # Stores indices of negative numbers
    for i in range(len(arr)):
        if arr[i] < 0:
            dq.append(i)
        # Remove out-of-window indices
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        if i >= k - 1:
            result.append(arr[dq[0]] if dq else 0)
    return result
```

---

## U

### Underflow
- **Definition:** Error when trying to dequeue from an empty queue.
- **Related:** Queue, Empty Queue, Overflow

---

## Quick Reference Table

| Term | Definition | Time | Example |
|------|-----------|------|---------|
| Enqueue | Add to back | O(1) | `queue.append(x)` |
| Dequeue | Remove from front | O(1) | `queue.popleft()` |
| Peek/Front | View front | O(1) | `queue[0]` |
| Is Empty | Check if empty | O(1) | `len(queue) == 0` |
| Size | Count elements | O(1) | `len(queue)` |
| BFS | Level-by-level traversal | O(V+E) | Graph/tree traversal |
| Priority Queue | Serve by priority | O(log n) | `heapq` operations |
| Sliding Window | Window-based processing | O(n) | Max in window of k |
| Circular Queue | Wrapping buffer | O(1) | Fixed-size queue |

| Implementation | Enqueue | Dequeue | Peek | Space |
|---------------|---------|---------|------|-------|
| Python list | O(1)* | O(n) | O(1) | O(n) |
| deque | O(1) | O(1) | O(1) | O(n) |
| Linked list | O(1) | O(1) | O(1) | O(n) + pointers |
| Circular array | O(1) | O(1) | O(1) | O(n) fixed |

*Amortized
