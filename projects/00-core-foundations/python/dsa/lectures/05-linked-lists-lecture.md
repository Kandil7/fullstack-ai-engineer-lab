# Lecture 05: Linked Lists

## Topic Overview

A **linked list** is a linear data structure where elements (nodes) are stored in non-contiguous memory locations. Each node contains data and a reference (pointer) to the next node. Unlike arrays, linked lists allow efficient insertion and deletion without shifting elements.

Types of linked lists:
- **Singly Linked List** — each node points to the next
- **Doubly Linked List** — each node points to both next and previous
- **Circular Linked List** — the last node points back to the first

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Implement** singly and doubly linked lists from scratch
2. **Perform** insert, delete, search, and reverse operations
3. **Use** the two-pointer technique (fast/slow) for linked list problems
4. **Compare** linked lists with arrays (trade-offs)
5. **Solve** classic problems (detect cycle, merge lists, find middle)
6. **Analyze** time and space complexity of linked list operations

---

## Key Concepts

### 1. Node Structure

```python
class Node:
    """A single node in a linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None  # Pointer to next node

# Creating nodes
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)

# Linking nodes
node1.next = node2
node2.next = node3

# Visual: 1 → 2 → 3 → None
```

### 2. Singly Linked List Implementation

```python
class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self._size = 0
    
    def append(self, data):
        """Add node to end. O(n) — must traverse to end."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1
    
    def prepend(self, data):
        """Add node to beginning. O(1)."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def insert_at(self, index, data):
        """Insert at specific position. O(n)."""
        if index < 0 or index > self._size:
            raise IndexError("Index out of range")
        
        if index == 0:
            self.prepend(data)
            return
        
        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self._size += 1
    
    def delete(self, data):
        """Delete first occurrence of data. O(n)."""
        if not self.head:
            return
        
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return
            current = current.next
    
    def search(self, data):
        """Find node with given data. O(n)."""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1
    
    def get(self, index):
        """Get element at index. O(n)."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data
    
    def reverse(self):
        """Reverse the linked list in-place. O(n)."""
        prev = None
        current = self.head
        while current:
            next_node = current.next  # Save next
            current.next = prev       # Reverse link
            prev = current            # Move prev forward
            current = next_node       # Move current forward
        self.head = prev
    
    def to_list(self):
        """Convert to Python list for easy visualization."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def __len__(self):
        return self._size
    
    def __str__(self):
        return " → ".join(str(x) for x in self.to_list()) + " → None"
```

### 3. Doubly Linked List

```python
class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0
    
    def append(self, data):
        """Add to end. O(1) with tail pointer."""
        new_node = DoublyNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
    
    def prepend(self, data):
        """Add to beginning. O(1)."""
        new_node = DoublyNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1
    
    def delete(self, node):
        """Delete a given node. O(1) — direct access!"""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next  # Deleting head
        
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev  # Deleting tail
        
        self._size -= 1
    
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
```

### 4. Time Complexity Comparison

| Operation | Array | Linked List |
|-----------|-------|-------------|
| Access by index | O(1) | O(n) |
| Search | O(n) | O(n) |
| Insert at beginning | O(n) | O(1) |
| Insert at end | O(1) amortized | O(1) with tail, O(n) without |
| Insert at middle | O(n) | O(1) if at known node |
| Delete at beginning | O(n) | O(1) |
| Delete at end | O(1) | O(1) with tail, O(n) without |
| Delete at middle | O(n) | O(1) if at known node |
| Space efficiency | High (no pointers) | Lower (pointer overhead) |

---

## Complete Code Examples

### Example 1: Detect Cycle (Floyd's Algorithm)

```python
"""
Detect if a linked list has a cycle.
Floyd's Tortoise and Hare — O(n) time, O(1) space.

Two pointers: slow moves 1 step, fast moves 2 steps.
If they meet, there's a cycle.
"""

def has_cycle(head):
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while slow != fast:
        if not fast or not fast.next:
            return False  # Reached end — no cycle
        slow = slow.next
        fast = fast.next.next
    
    return True  # They met — cycle exists

# To find the cycle start:
def detect_cycle_start(head):
    if not head or not head.next:
        return None
    
    slow = fast = head
    
    # Phase 1: Detect if cycle exists
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle
    
    # Phase 2: Find cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow  # Start of cycle
```

### Example 2: Find Middle of Linked List

```python
"""
Find the middle node using fast/slow pointers.
If even length, return the second middle node.
Time: O(n), Space: O(1)
"""

def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # slow is at the middle

# Test
lst = SinglyLinkedList()
for x in [1, 2, 3, 4, 5]:
    lst.append(x)
print(find_middle(lst.head).data)  # 3

lst2 = SinglyLinkedList()
for x in [1, 2, 3, 4, 5, 6]:
    lst2.append(x)
print(find_middle(lst2.head).data)  # 4 (second middle)
```

### Example 3: Merge Two Sorted Linked Lists

```python
"""
Merge two sorted linked lists into one sorted list.
Time: O(n + m), Space: O(1)
"""

def merge_sorted_lists(l1, l2):
    dummy = Node(0)  # Dummy node to simplify edge cases
    current = dummy
    
    while l1 and l2:
        if l1.data <= l2.data:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # Attach remaining nodes
    current.next = l1 if l1 else l2
    
    return dummy.next  # Skip dummy node
```

### Example 4: Remove Nth Node From End

```python
"""
Remove the nth node from the end of a linked list.
Time: O(n), Space: O(1)

Two-pointer technique: advance first pointer n steps,
then move both until first reaches end.
"""

def remove_nth_from_end(head, n):
    dummy = Node(0)
    dummy.next = head
    
    fast = slow = dummy
    
    # Advance fast pointer n+1 steps
    for _ in range(n + 1):
        fast = fast.next
    
    # Move both until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next
    
    # Slow is now at the node before the one to remove
    slow.next = slow.next.next
    
    return dummy.next
```

### Example 5: Intersection of Two Linked Lists

```python
"""
Find the node where two linked lists intersect.
If no intersection, return None.

Two-pointer technique: when a pointer reaches the end,
redirect it to the head of the other list.
If they intersect, they'll meet at the intersection node.
Time: O(n + m), Space: O(1)
"""

def get_intersection_node(headA, headB):
    if not headA or not headB:
        return None
    
    pointerA = headA
    pointerB = headB
    
    # When pointerA reaches end, redirect to headB
    # When pointerB reaches end, redirect to headA
    # They will meet at intersection (or both become None)
    while pointerA is not pointerB:
        pointerA = pointerA.next if pointerA else headB
        pointerB = pointerB.next if pointerB else headA
    
    return pointerA  # Either intersection node or None
```

---

## Common Mistakes to Avoid

### Mistake 1: Losing Reference to Remaining List
```python
# WRONG: Lost the rest of the list!
current = head
head = head.next
head.next = None  # Oops! Broke the entire chain

# RIGHT: Work with the current node
current = head
head = head.next
current.next = None  # Only disconnected current node
```

### Mistake 2: Forgetting to Handle Empty List
```python
# WRONG: May crash on empty list
def get_data(head):
    return head.data  # AttributeError if head is None

# RIGHT: Check for None
def get_data(head):
    if not head:
        return None
    return head.data
```

### Mistake 3: Not Using Dummy Nodes
```python
# WRONG: Complex edge case handling for head insertion
def add_node(head, data):
    new_node = Node(data)
    if not head:
        return new_node  # Special case
    # ... handle insertion ...

# RIGHT: Dummy node eliminates special cases
def add_node(head, data):
    dummy = Node(0)
    dummy.next = head
    # ... always works, even for empty list ...
    return dummy.next
```

---

## Best Practices

1. **Use a dummy node** to eliminate edge cases at the head
2. **Draw the pointers** on paper before coding linked list problems
3. **Always handle None** — empty list, end of list, null pointers
4. **Use fast/slow pointers** for cycle detection and middle finding
5. **Two-pointer technique** — advance one pointer n steps ahead, then move both
6. **For reversal**, save `next` before modifying the link
7. **For doubly linked lists**, update both `next` and `prev` pointers

---

## Practice Exercises

### Exercise 1: Reverse a Linked List in Groups of K
```python
def reverse_in_groups(head, k):
    """
    Reverse every k consecutive nodes.
    Input: 1→2→3→4→5, k=2
    Output: 2→1→4→3→5
    """
    # Your solution here
    pass
```

### Exercise 2: Palindrome Linked List
```python
def is_palindrome(head):
    """
    Check if a linked list is a palindrome.
    Input: 1→2→1
    Output: True
    """
    # Your solution here — O(n) time, O(1) space
    pass
```

### Exercise 3: Flatten a Multilevel Doubly Linked List
```python
def flatten(head):
    """
    Flatten a multilevel doubly linked list where child
    pointers create sub-lists.
    """
    # Your solution here
    pass
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Node** | Data + pointer to next node |
| **Singly Linked** | One-directional traversal |
| **Doubly Linked** | Bidirectional traversal, O(1) delete at known node |
| **No Random Access** | Must traverse from head — O(n) access |
| **Fast/Slow Pointers** | Cycle detection, middle finding — O(n) |
| **Two-Pointer** | Many list problems solved in one pass |
| **Dummy Node** | Simplifies edge case handling |

**Key Insight:** Linked lists trade fast random access for fast insertions/deletions. They're the foundation for stacks, queues, and hash table chaining.

**Next Lecture:** Hash Tables — O(1) average-time lookup, insertion, and deletion.
