# Glossary: Linked Lists

> Quick reference for all terms introduced in Lecture 05.

---

## C

### Cycle Detection
- **Definition:** Determining whether a linked list contains a cycle (a node that points back to a previous node).
- **Algorithm:** Floyd's Tortoise and Hare — O(n) time, O(1) space.
- **Related:** Fast/Slow Pointers, Floyd's Algorithm

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

---

## D

### Dummy Node
- **Definition:** A placeholder node added temporarily to simplify edge cases in linked list operations (e.g., inserting at head).
- **Example:** `dummy = Node(0); dummy.next = head`
- **Related:** Sentinel Node, Head

```python
def remove_head(head, target):
    dummy = Node(0)
    dummy.next = head
    prev = dummy
    while prev.next:
        if prev.next.data == target:
            prev.next = prev.next.next
            break
        prev = prev.next
    return dummy.next
```

---

## F

### Fast/Slow Pointers (Floyd's Algorithm)
- **Definition:** A two-pointer technique where one pointer moves at double the speed of the other, used for cycle detection and finding the middle node.
- **Also Known As:** Tortoise and Hare algorithm.
- **Time:** O(n), **Space:** O(1)
- **Related:** Cycle Detection, Middle of Linked List

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # At middle
```

---

## H

### Head
- **Definition:** The first node in a linked list. The entry point for traversal.
- **Related:** Tail, Node, Null Terminator

```python
class LinkedList:
    def __init__(self):
        self.head = None  # No nodes yet
```

---

## I

### In-Place Reversal
- **Definition:** Reversing a linked list by modifying pointers without creating new nodes.
- **Time:** O(n), **Space:** O(1)
- **Related:** Reversal, Pointer Manipulation

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

---

## L

### Linked List
- **Definition:** A linear data structure where elements (nodes) are stored in non-contiguous memory, connected by pointers.
- **Types:** Singly linked, doubly linked, circular.
- **Related:** Node, Pointer, Array

```
Singly:   A → B → C → None
Doubly:   None ← A ⇄ B ⇄ C → None
Circular: A → B → C → A (last points to first)
```

---

## M

### Middle Node
- **Definition:** The center node of a linked list, found using the fast/slow pointer technique.
- **For even length:** The second middle node (by convention).
- **Related:** Fast/Slow Pointers

---

## N

### Node
- **Definition:** The basic building block of a linked list, containing data and a pointer (or pointers) to other nodes.
- **In singly linked list:** `data` + `next` pointer.
- **In doubly linked list:** `data` + `next` + `prev` pointers.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
```

### Null Terminator
- **Definition:** The `None` (or `null`) reference at the end of a singly linked list, indicating no more nodes.
- **Related:** Head, Tail, End

---

## P

### Pointer
- **Definition:** A reference (memory address) to another node in a linked list.
- **In Python:** An object reference (all variables are essentially pointers).
- **Related:** Node, Reference, Link

### Pointer Manipulation
- **Definition:** Changing the `next` (and `prev`) references to restructure a linked list.
- **Example:** Reversal, insertion, deletion, splitting.
- **Related:** In-Place Reversal, Dummy Node

---

## R

### Reversal
- **Definition:** Flipping the direction of all pointers in a linked list so the last node becomes the first.
- **Time:** O(n), **Space:** O(1) for in-place reversal.
- **Related:** In-Place Reversal, Two-Pointer

```python
def reverse_list(head):
    prev, current = None, head
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    return prev
```

---

## S

### Sentinel Node
- **Definition:** See Dummy Node. A placeholder node that simplifies boundary conditions.
- **Related:** Dummy Node, Head

### Singly Linked List
- **Definition:** A linked list where each node has only a `next` pointer, allowing traversal in one direction only.
- **Related:** Doubly Linked List, Circular Linked List

```python
class SinglyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
```

---

## T

### Tail
- **Definition:** The last node in a linked list (its `next` pointer is `None`).
- **Related:** Head, Null Terminator

---

## Quick Reference Table

| Term | Definition | Time | Example |
|------|-----------|------|---------|
| Prepend | Add to head | O(1) | `node.next = head; head = node` |
| Append | Add to tail | O(n)* | Traverse to end, link |
| Insert at index | Add at position | O(n) | Traverse to index-1 |
| Delete by value | Remove first match | O(n) | Search + relink |
| Search | Find by value | O(n) | Traverse and compare |
| Reverse | Flip all pointers | O(n) | In-place pointer swap |
| Find Middle | Locate center | O(n) | Fast/slow pointers |
| Detect Cycle | Check for loop | O(n) | Floyd's algorithm |

*O(1) with tail pointer

| Singly | Doubly | Description |
|--------|--------|-------------|
| `next` only | `next` + `prev` | Traversal direction |
| O(n) delete at node | O(1) delete at node | With direct reference |
| Less memory per node | More memory per node | Pointer overhead |
| One-directional | Bidirectional | Flexibility |

| Technique | Use Case | Complexity |
|-----------|----------|-----------|
| Fast/Slow Pointers | Cycle detection, middle node | O(n) time, O(1) space |
| Two-Pointer | Intersection, nth from end | O(n) time, O(1) space |
| Dummy Node | Edge case simplification | O(1) extra space |
| In-Place Reversal | Reverse list/group | O(n) time, O(1) space |
| Runner Technique | Find kth from end | O(n) time, O(1) space |
