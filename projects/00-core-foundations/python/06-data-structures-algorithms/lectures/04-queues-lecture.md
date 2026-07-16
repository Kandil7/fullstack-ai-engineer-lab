# Lecture 04: Queues

## Topic Overview

A **queue** is a linear data structure that follows the **FIFO (First In, First Out)** principle. The first element added is the first one removed. Think of a line at a store — the first person in line is served first.

Queues are essential for:
- **Breadth-First Search (BFS)** — level-by-level graph traversal
- **Task scheduling** — OS process scheduling, print queues
- **Buffering** — I/O buffers, streaming data
- **Message queues** — producer-consumer patterns
- **Sliding window maximum/minimum**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Implement** a queue using arrays and linked lists
2. **Use** Python's `collections.deque` and `queue` module
3. **Apply** queues to BFS and scheduling problems
4. **Implement** specialized queues (circular queue, priority queue, deque)
5. **Analyze** time/space complexity of queue operations
6. **Solve** classic queue problems (sliding window, level-order traversal)

---

## Key Concepts

### 1. Queue Operations (ADT)

```
Queue ADT Operations:
┌──────────────┬───────────────────────────────────────────┐
│ Operation    │ Description                               │
├──────────────┼───────────────────────────────────────────┤
│ enqueue(item)│ Add item to the back (rear) of the queue  │
│ dequeue()    │ Remove and return the front item          │
│ peek/front() │ Return the front item without removing    │
│ is_empty()   │ Check if the queue is empty               │
│ size()       │ Return the number of elements             │
└──────────────┴───────────────────────────────────────────┘

Visual representation:
enqueue(A) → enqueue(B) → enqueue(C) → dequeue()
    
    [A]        [A,B]      [A,B,C]     [B,C]
    rear→A     rear→C     rear→C     rear→C
    front→A    front→A    front→A    front→B
```

### 2. Queue Implementations

#### Using Python List (Inefficient)
```python
class ListQueue:
    """Queue using list — O(n) dequeue due to shifting."""
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)       # O(1) amortized
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self.items.pop(0)      # O(n) — shifts all elements!
    
    def is_empty(self):
        return len(self.items) == 0
```

#### Using collections.deque (Recommended)
```python
from collections import deque

class DequeQueue:
    """Queue using deque — O(1) for both enqueue and dequeue."""
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        self.items.append(item)       # O(1)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self.items.popleft()   # O(1)
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Peek at empty queue")
        return self.items[0]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

#### Using Linked List
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedQueue:
    """Queue using linked list — O(1) enqueue and dequeue."""
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0
    
    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self._size -= 1
        return data
    
    def is_empty(self):
        return self.front is None
    
    def size(self):
        return self._size
```

### 3. Circular Queue

A circular queue reuses empty spaces at the front by wrapping around:

```
Circular Queue (capacity=5):
Initial:  [_, _, _, _, _]
Enqueue A: [A, _, _, _, _]  front=0, rear=0
Enqueue B: [A, B, _, _, _]  front=0, rear=1
Enqueue C: [A, B, C, _, _]  front=0, rear=2
Dequeue:   [_, B, C, _, _]  front=1, rear=2
Enqueue D: [_, B, C, D, _]  front=1, rear=3
Enqueue E: [_, B, C, D, E]  front=1, rear=4
Enqueue F: [F, B, C, D, E]  front=1, rear=0  (wrapped!)
```

```python
class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = [None] * capacity
        self.front = 0
        self.rear = -1
        self._size = 0
    
    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("Queue is full")
        self.rear = (self.rear + 1) % self.capacity
        self.items[self.rear] = item
        self._size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self.items[self.front]
        self.items[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self._size -= 1
        return item
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[self.front]
    
    def is_empty(self):
        return self._size == 0
    
    def is_full(self):
        return self._size == self.capacity
    
    def size(self):
        return self._size
```

### 4. Priority Queue

A priority queue serves elements based on priority, not insertion order.

```python
import heapq

class PriorityQueue:
    """Min-heap based priority queue."""
    def __init__(self):
        self.heap = []
        self.counter = 0  # For tie-breaking
    
    def enqueue(self, item, priority):
        heapq.heappush(self.heap, (priority, self.counter, item))
        self.counter += 1
    
    def dequeue(self):
        if not self.heap:
            raise IndexError("Dequeue from empty priority queue")
        priority, _, item = heapq.heappop(self.heap)
        return item
    
    def peek(self):
        if not self.heap:
            raise IndexError("Peek at empty priority queue")
        return self.heap[0][2]
    
    def is_empty(self):
        return len(self.heap) == 0

# Usage
pq = PriorityQueue()
pq.enqueue("low priority", 5)
pq.enqueue("high priority", 1)
pq.enqueue("medium priority", 3)
print(pq.dequeue())  # "high priority" (priority 1)
print(pq.dequeue())  # "medium priority" (priority 3)
```

### 5. Time Complexity Comparison

| Operation | Python List | deque | Linked List | Circular Array |
|-----------|------------|-------|-------------|----------------|
| Enqueue (back) | O(1)* | O(1) | O(1) | O(1) |
| Dequeue (front) | O(n) | O(1) | O(1) | O(1) |
| Peek (front) | O(1) | O(1) | O(1) | O(1) |
| Space | O(n) | O(n) | O(n) + pointers | O(n) fixed |

*Amortized

---

## Complete Code Examples

### Example 1: BFS Using a Queue

```python
"""
Breadth-First Search — explore graph level by level.
Time: O(V + E), Space: O(V)
"""

from collections import deque

def bfs(graph, start):
    """BFS traversal returning visited order."""
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []
    
    while queue:
        node = queue.popleft()   # Dequeue from front
        order.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # Enqueue to back
    
    return order

# Example graph (adjacency list)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print(bfs(graph, 'A'))  # ['A', 'B', 'C', 'D', 'E', 'F']
```

### Example 2: Sliding Window Maximum

```python
"""
Find the maximum in every window of size k.
Input: [1, 3, -1, -3, 5, 3, 6, 7], k=3
Output: [3, 3, 5, 5, 6, 7]

Uses a deque to maintain indices of useful elements.
Time: O(n), Space: O(k)
"""

from collections import deque

def sliding_window_max(nums, k):
    dq = deque()  # Stores indices, front = max of current window
    result = []
    
    for i in range(len(nums)):
        # Remove elements outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements from back (they're useless)
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Test
print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
# Output: [3, 3, 5, 5, 6, 7]
```

### Example 3: Level-Order Tree Traversal

```python
"""
Level-order traversal of a binary tree using a queue.
Time: O(n), Space: O(n)
"""

from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result

# Build tree:      3
#                 / \
#                9   20
#                   /  \
#                  15   7
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

print(level_order(root))  # [[3], [9, 20], [15, 7]]
```

### Example 4: Queue Using Two Stacks

```python
"""
Implement a queue using two stacks.
Idea: One stack for enqueue, one for dequeue.
When dequeue stack is empty, transfer from enqueue stack.

Amortized O(1) per operation.
"""

class QueueWithStacks:
    def __init__(self):
        self.stack_in = []    # For enqueue
        self.stack_out = []   # For dequeue
    
    def enqueue(self, item):
        self.stack_in.append(item)
    
    def dequeue(self):
        self._transfer()
        if not self.stack_out:
            raise IndexError("Dequeue from empty queue")
        return self.stack_out.pop()
    
    def peek(self):
        self._transfer()
        if not self.stack_out:
            raise IndexError("Peek at empty queue")
        return self.stack_out[-1]
    
    def _transfer(self):
        """Move elements from in-stack to out-stack when needed."""
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
    
    def is_empty(self):
        return not self.stack_in and not self.stack_out

# Usage
q = QueueWithStacks()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print(q.dequeue())  # 1 (FIFO)
print(q.dequeue())  # 2
q.enqueue(4)
print(q.dequeue())  # 3
print(q.dequeue())  # 4
```

### Example 5: Hot Potato (Josephus Problem)

```python
"""
Classic queue simulation: Children stand in a circle,
every k-th child is eliminated until one remains.

Time: O(n × k)
"""

from collections import deque

def hot_potato(names, k):
    queue = deque(names)
    
    while len(queue) > 1:
        # Rotate k-1 times (move first to end)
        for _ in range(k - 1):
            queue.append(queue.popleft())
        # Eliminate the k-th person
        eliminated = queue.popleft()
        print(f"Eliminated: {eliminated}")
    
    return queue[0]

# Test
winner = hot_potato(["Alice", "Bob", "Charlie", "David", "Eve"], 3)
print(f"Winner: {winner}")
# Eliminated: Charlie, Alice, Eve, Bob
# Winner: David
```

---

## Common Mistakes to Avoid

### Mistake 1: Using `list.pop(0)` for Queue
```python
# WRONG: O(n) — shifts all elements
queue = [1, 2, 3]
queue.pop(0)  # O(n) — bad!

# RIGHT: Use deque
from collections import deque
queue = deque([1, 2, 3])
queue.popleft()  # O(1) — good!
```

### Mistake 2: Forgetting the FIFO Order
```python
# WRONG: Thinking append/pop gives FIFO
stack = []
stack.append(1)  # Push
stack.append(2)  # Push
stack.pop()      # Returns 2 — this is LIFO!

# RIGHT: Use popleft for FIFO
from collections import deque
queue = deque()
queue.append(1)    # Enqueue
queue.append(2)    # Enqueue
queue.popleft()    # Returns 1 — this is FIFO!
```

### Mistake 3: Infinite Loop in BFS
```python
# WRONG: Forgetting to mark visited
def bfs_infinite(graph, start):
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            queue.append(neighbor)  # Infinite loop! Never marks visited

# RIGHT: Always mark when enqueuing
def bfs_correct(graph, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

---

## Best Practices

1. **Always use `collections.deque`** for queue operations — O(1) at both ends
2. **Use `queue.SimpleQueue`** or `queue.Queue` for thread-safe queues
3. **For BFS**, mark nodes as visited when enqueuing, not when dequeuing
4. **For priority queues**, use Python's `heapq` module
5. **For sliding window problems**, use a monotonic deque
6. **Circular queues** are useful when buffer size is fixed
7. **Two-stack queues** are a common interview pattern

---

## Practice Exercises

### Exercise 1: Implement Stack Using Two Queues
```python
class StackWithQueues:
    """Implement a stack using two queues."""
    def __init__(self):
        from collections import deque
        self.q1 = deque()
        self.q2 = deque()
    
    def push(self, item):
        # Your solution here
        pass
    
    def pop(self):
        # Your solution here
        pass
```

### Exercise 2: First Non-Repeating Character in Stream
```python
def first_non_repeating(stream):
    """
    Given a stream of characters, find the first non-repeating
    character at each point.
    Input: "aabxbxc"
    Output: "a#bxbxc"
    """
    # Your solution here — use a queue and a count dict
    pass
```

### Exercise 3: Rotting Oranges (BFS)
```python
def oranges_rotting(grid):
    """
    Given a grid of fresh (1) and rotten (2) oranges,
    find minimum minutes until all oranges are rotten.
    Each minute, rotten oranges rot adjacent fresh ones.
    """
    # Your solution here — multi-source BFS
    pass
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **FIFO Principle** | First in, first out |
| **deque** | O(1) enqueue and dequeue at both ends |
| **BFS** | Queue-based level-by-level traversal |
| **Priority Queue** | Serves by priority, not insertion order |
| **Circular Queue** | Reuses space in a fixed-size buffer |
| **Sliding Window** | Deque maintains useful elements efficiently |

**Key Insight:** Whenever you need to process items in the order they arrived, or explore something level-by-level, think queue.

**Next Lecture:** Linked Lists — dynamic data structures with O(1) insertions/deletions at any position.
