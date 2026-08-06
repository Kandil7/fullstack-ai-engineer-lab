"""
DSA Tutorial 04 - Queues
========================

Queue: First In, First Out (FIFO)
Think of a line at a store - first person in line gets served first.

Operations:
- enqueue: Add to rear    O(1)
- dequeue: Remove from front O(1)
- peek: View front        O(1)
- is_empty: Check         O(1)
- size: Count elements    O(1)
"""

# =============================================================================
# 1. BASIC QUEUE IMPLEMENTATION
# =============================================================================

class Queue:
    """Queue implementation using Python list"""

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Add to rear. O(n) for list, O(1) amortized for deque."""
        self.items.insert(0, item)  # Insert at front for O(1)

    def dequeue(self):
        """Remove from front. O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.pop()

    def peek(self):
        """View front item. O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return f"Queue({self.items})"


print("=== Basic Queue ===")
queue = Queue()
queue.enqueue("A")
queue.enqueue("B")
queue.enqueue("C")
print(f"Enqueue A, B, C: {queue}")
print(f"Peek: {queue.peek()}")
print(f"Dequeue: {queue.dequeue()}")
print(f"After dequeue: {queue}")


# =============================================================================
# 2. QUEUE USING COLLECTIONS.DEQUE (OPTIMAL)
# =============================================================================

from collections import deque

class DequeQueue:
    """Queue using deque - O(1) for both ends"""

    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.popleft()

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return f"DequeQueue({list(self.items)})"


print("\n=== Queue Using Deque ===")
dq = DequeQueue()
dq.enqueue(1)
dq.enqueue(2)
dq.enqueue(3)
print(f"Enqueue 1, 2, 3: {dq}")
print(f"Dequeue: {dq.dequeue()}")
print(f"After dequeue: {dq}")


# =============================================================================
# 3. CIRCULAR QUEUE
# =============================================================================

class CircularQueue:
    """Circular queue using fixed-size array"""

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("Queue is full")
        self.rear = (self.rear + 1) % self.capacity
        self.items[self.rear] = item
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self.items[self.front]
        self.items[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[self.front]

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def __str__(self):
        if self.is_empty():
            return "CircularQueue([])"
        items = []
        i = self.front
        for _ in range(self.size):
            items.append(str(self.items[i]))
            i = (i + 1) % self.capacity
        return f"CircularQueue([{', '.join(items)}])"


print("\n=== Circular Queue ===")
circular = CircularQueue(5)
circular.enqueue(10)
circular.enqueue(20)
circular.enqueue(30)
print(f"Enqueue 10, 20, 30: {circular}")
circular.dequeue()
circular.enqueue(40)
circular.enqueue(50)
print(f"After operations: {circular}")


# =============================================================================
# 4. QUEUE USING LINKED LIST
# =============================================================================

class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedQueue:
    """Queue using linked list - no capacity limit"""

    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def enqueue(self, item):
        new_node = QueueNode(item)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self._size -= 1
        return data

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.front.data

    def is_empty(self):
        return self.front is None

    def size(self):
        return self._size

    def __str__(self):
        items = []
        current = self.front
        while current:
            items.append(str(current.data))
            current = current.next
        return " <- ".join(items)


print("\n=== Queue Using Linked List ===")
linked_q = LinkedQueue()
linked_q.enqueue("X")
linked_q.enqueue("Y")
linked_q.enqueue("Z")
print(f"Queue: {linked_q}")
print(f"Dequeue: {linked_q.dequeue()}")
print(f"After dequeue: {linked_q}")


# =============================================================================
# 5. DEQUE (DOUBLE-ENDED QUEUE)
# =============================================================================

class Deque:
    """Double-ended queue - add/remove from both ends"""

    def __init__(self):
        self.items = deque()

    def add_front(self, item):
        self.items.appendleft(item)

    def add_rear(self, item):
        self.items.append(item)

    def remove_front(self):
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.items.popleft()

    def remove_rear(self):
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.items.pop()

    def peek_front(self):
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.items[0]

    def peek_rear(self):
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return f"Deque({list(self.items)})"


print("\n=== Deque ===")
d = Deque()
d.add_rear(1)
d.add_rear(2)
d.add_front(0)
print(f"After adds: {d}")
print(f"Remove rear: {d.remove_rear()}")
print(f"Remove front: {d.remove_front()}")
print(f"After removes: {d}")


# =============================================================================
# 6. PRIORITY QUEUE
# =============================================================================

import heapq

class PriorityQueue:
    """Priority queue using heap. O(log n) enqueue/dequeue"""

    def __init__(self):
        self.heap = []
        self.counter = 0  # For stable ordering

    def enqueue(self, item, priority):
        heapq.heappush(self.heap, (-priority, self.counter, item))
        self.counter += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        priority, _, item = heapq.heappop(self.heap)
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.heap[0][2]

    def is_empty(self):
        return len(self.heap) == 0

    def __str__(self):
        items = [(-p, item) for p, _, item in sorted(self.heap, reverse=True)]
        return f"PriorityQueue({items})"


print("\n=== Priority Queue ===")
pq = PriorityQueue()
pq.enqueue("Low priority task", 1)
pq.enqueue("High priority task", 10)
pq.enqueue("Medium priority task", 5)
print(f"Queue: {pq}")
print(f"Dequeue: {pq.dequeue()}")
print(f"Dequeue: {pq.dequeue()}")


# =============================================================================
# 7. QUEUE REVERSAL
# =============================================================================

def reverse_queue(queue):
    """Reverse a queue using recursion. O(n) time, O(n) space."""
    if queue.is_empty():
        return

    item = queue.dequeue()
    reverse_queue(queue)
    queue.enqueue(item)
    return queue

print("\n=== Queue Reversal ===")
q = Queue()
for i in range(1, 6):
    q.enqueue(i)
print(f"Original: {q}")
reverse_queue(q)
print(f"Reversed: {q}")


# =============================================================================
# 8. STACK USING TWO QUEUES
# =============================================================================

class StackUsingQueues:
    """Stack implementation using two queues"""

    def __init__(self):
        self.q1 = deque()
        self.q2 = deque()

    def push(self, item):
        self.q2.append(item)
        while self.q1:
            self.q2.append(self.q1.popleft())
        self.q1, self.q2 = self.q2, self.q1

    def pop(self):
        if not self.q1:
            raise IndexError("Stack is empty")
        return self.q1.popleft()

    def peek(self):
        if not self.q1:
            raise IndexError("Stack is empty")
        return self.q1[0]

    def is_empty(self):
        return not self.q1

    def __str__(self):
        return f"StackUsingQueues({list(self.q1)})"


print("\n=== Stack Using Two Queues ===")
sq = StackUsingQueues()
sq.push(1)
sq.push(2)
sq.push(3)
print(f"Push 1, 2, 3: {sq}")
print(f"Pop: {sq.pop()}")
print(f"Peek: {sq.peek()}")


# =============================================================================
# 9. QUEUE USING STACKS
# =============================================================================

class QueueUsingStacks:
    """Queue implementation using two stacks"""

    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def enqueue(self, item):
        self.stack_in.append(item)

    def dequeue(self):
        if not self.stack_out:
            if not self.stack_in:
                raise IndexError("Queue is empty")
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        return self.stack_out.pop()

    def peek(self):
        if not self.stack_out:
            if not self.stack_in:
                raise IndexError("Queue is empty")
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        return self.stack_out[-1]

    def is_empty(self):
        return not self.stack_in and not self.stack_out

    def __str__(self):
        out = list(reversed(self.stack_out))
        return f"QueueUsingStacks({out + self.stack_in})"


print("\n=== Queue Using Two Stacks ===")
qs = QueueUsingStacks()
qs.enqueue(10)
qs.enqueue(20)
qs.enqueue(30)
print(f"Enqueue 10, 20, 30: {qs}")
print(f"Dequeue: {qs.dequeue()}")
print(f"After dequeue: {qs}")


# =============================================================================
# 10. BOUNDED BUFFER (PRODUCER-CONSUMER)
# =============================================================================

import threading
import time

class BoundedBuffer:
    """Thread-safe bounded buffer (producer-consumer problem)"""

    def __init__(self, capacity):
        self.buffer = deque()
        self.capacity = capacity
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def produce(self, item):
        with self.not_full:
            while len(self.buffer) >= self.capacity:
                self.not_full.wait()
            self.buffer.append(item)
            print(f"  Produced: {item} (buffer size: {len(self.buffer)})")
            self.not_empty.notify()

    def consume(self):
        with self.not_empty:
            while not self.buffer:
                self.not_empty.wait()
            item = self.buffer.popleft()
            print(f"  Consumed: {item} (buffer size: {len(self.buffer)})")
            self.not_full.notify()
            return item

print("\n=== Bounded Buffer (Producer-Consumer) ===")
buffer = BoundedBuffer(3)

def producer():
    for i in range(5):
        time.sleep(0.1)
        buffer.produce(i)

def consumer():
    for _ in range(5):
        time.sleep(0.15)
        buffer.consume()

# Note: In real usage, these would run in separate threads
# For demo, we run producer and consumer in REAL threads to demonstrate
# the blocking behavior correctly - capacity 3 means producer blocks after 3 items
print("(Real producer-consumer with threading)")
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

print("(Producer-consumer completed successfully)")


# =============================================================================
# 11. QUEUE APPLICATIONS
# =============================================================================

print("\n=== Queue Applications ===")

# BFS using queue
def bfs_example(graph, start):
    """Breadth-first search using queue"""
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []

    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order

# Graph representation
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print(f"BFS from A: {bfs_example(graph, 'A')}")


# =============================================================================
# 12. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Queues - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Queue is FIFO (First In, First Out)")
    print("2. Deque provides O(1) operations at both ends")
    print("3. Priority queue serves highest-priority first")
    print("4. Circular queue efficiently uses fixed space")
    print("5. Used in: BFS, scheduling, producer-consumer, buffers")
