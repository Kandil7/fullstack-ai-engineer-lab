"""
DSA Tutorial 05 - Linked Lists
===============================

Linked List: Linear data structure where elements are stored in nodes.
Each node contains data and a pointer to the next node.

Types:
- Singly Linked List
- Doubly Linked List
- Circular Linked List

Advantages over arrays:
- Dynamic size
- Efficient insertion/deletion (O(1) at known positions)
- No memory waste

Disadvantages:
- No random access (O(n) traversal)
- Extra memory for pointers
"""

# =============================================================================
# 1. SINGLY LINKED LIST
# =============================================================================

class Node:
    """A node in a linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"

class SinglyLinkedList:
    """Singly Linked List implementation"""

    def __init__(self):
        self.head = None
        self._size = 0

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size

    # ---- INSERTION ----

    def prepend(self, data):
        """Insert at beginning. O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def append(self, data):
        """Insert at end. O(n)"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def insert_after(self, prev_node, data):
        """Insert after given node. O(1)"""
        if not prev_node:
            raise ValueError("Previous node must be in the list")
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node
        self._size += 1

    def insert_at_index(self, index, data):
        """Insert at specific index. O(n)"""
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")
        if index == 0:
            self.prepend(data)
            return
        current = self.head
        for _ in range(index - 1):
            current = current.next
        self.insert_after(current, data)

    # ---- DELETION ----

    def delete_first(self):
        """Delete first node. O(1)"""
        if self.is_empty():
            raise IndexError("List is empty")
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data

    def delete_last(self):
        """Delete last node. O(n)"""
        if self.is_empty():
            raise IndexError("List is empty")
        if self.head.next is None:
            return self.delete_first()
        current = self.head
        while current.next.next:
            current = current.next
        data = current.next.data
        current.next = None
        self._size -= 1
        return data

    def delete_by_value(self, data):
        """Delete first occurrence of value. O(n)"""
        if self.is_empty():
            return False
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def delete_at_index(self, index):
        """Delete at specific index. O(n)"""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        if index == 0:
            return self.delete_first()
        current = self.head
        for _ in range(index - 1):
            current = current.next
        data = current.next.data
        current.next = current.next.next
        self._size -= 1
        return data

    # ---- SEARCH ----

    def search(self, data):
        """Search for value. O(n)"""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def get(self, index):
        """Get element at index. O(n)"""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    # ---- UTILITIES ----

    def reverse(self):
        """Reverse the list in-place. O(n)"""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self):
        """Convert to Python list. O(n)"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __str__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes) + " -> None"


print("=== Singly Linked List ===")
sll = SinglyLinkedList()
for i in [1, 2, 3, 4, 5]:
    sll.append(i)
print(f"List: {sll}")
print(f"Size: {sll.size()}")

sll.prepend(0)
print(f"Prepend 0: {sll}")

sll.insert_at_index(3, 99)
print(f"Insert 99 at index 3: {sll}")

print(f"Delete first: {sll.delete_first()}")
print(f"Delete last: {sll.delete_last()}")
print(f"After deletes: {sll}")

print(f"Search 3: index {sll.search(3)}")
print(f"Get index 2: {sll.get(2)}")

sll.reverse()
print(f"Reversed: {sll}")


# =============================================================================
# 2. DOUBLY LINKED LIST
# =============================================================================

class DNode:
    """Node for doubly linked list"""
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """Doubly Linked List implementation"""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size

    def prepend(self, data):
        """Insert at beginning. O(1)"""
        new_node = DNode(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def append(self, data):
        """Insert at end. O(1)"""
        new_node = DNode(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def delete_first(self):
        """Delete first node. O(1)"""
        if self.is_empty():
            raise IndexError("List is empty")
        data = self.head.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self._size -= 1
        return data

    def delete_last(self):
        """Delete last node. O(1)"""
        if self.is_empty():
            raise IndexError("List is empty")
        data = self.tail.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self._size -= 1
        return data

    def forward_traversal(self):
        """Traverse from head to tail. O(n)"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def backward_traversal(self):
        """Traverse from tail to head. O(n)"""
        result = []
        current = self.tail
        while current:
            result.append(current.data)
            current = current.prev
        return result

    def __str__(self):
        return " <-> ".join(str(x) for x in self.forward_traversal())


print("\n=== Doubly Linked List ===")
dll = DoublyLinkedList()
for i in [10, 20, 30, 40]:
    dll.append(i)
print(f"List: {dll}")
dll.prepend(5)
print(f"Prepend 5: {dll}")
print(f"Forward: {dll.forward_traversal()}")
print(f"Backward: {dll.backward_traversal()}")
print(f"Delete first: {dll.delete_first()}")
print(f"Delete last: {dll.delete_last()}")
print(f"After deletes: {dll}")


# =============================================================================
# 3. CIRCULAR LINKED LIST
# =============================================================================

class CircularLinkedList:
    """Circular Linked List - last node points to first"""

    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, data):
        """Add to end. O(n)"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head
        self._size += 1

    def prepend(self, data):
        """Add to beginning. O(n)"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            new_node.next = self.head
            current.next = new_node
            self.head = new_node
        self._size += 1

    def delete(self, data):
        """Delete first occurrence. O(n)"""
        if not self.head:
            return False

        if self.head.data == data:
            if self.head.next == self.head:
                self.head = None
            else:
                current = self.head
                while current.next != self.head:
                    current = current.next
                current.next = self.head.next
                self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next != self.head:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def to_list(self):
        """Convert to Python list. O(n)"""
        if not self.head:
            return []
        result = []
        current = self.head
        while True:
            result.append(current.data)
            current = current.next
            if current == self.head:
                break
        return result

    def __str__(self):
        items = self.to_list()
        return " -> ".join(str(x) for x in items) + " -> (back to head)"


print("\n=== Circular Linked List ===")
cll = CircularLinkedList()
for i in [1, 2, 3, 4]:
    cll.append(i)
print(f"List: {cll}")
cll.prepend(0)
print(f"Prepend 0: {cll}")
cll.delete(2)
print(f"Delete 2: {cll}")
print(f"As list: {cll.to_list()}")


# =============================================================================
# 4. MERGE TWO SORTED LISTS
# =============================================================================

def merge_sorted_lists(l1, l2):
    """Merge two sorted linked lists. O(n + m) time."""
    dummy = Node(0)
    current = dummy

    while l1 and l2:
        if l1.data <= l2.data:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 if l1 else l2
    return dummy.next

def list_to_linked(lst):
    """Convert Python list to linked list"""
    if not lst:
        return None
    head = Node(lst[0])
    current = head
    for val in lst[1:]:
        current.next = Node(val)
        current = current.next
    return head

def linked_to_list(head):
    """Convert linked list to Python list"""
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result

print("\n=== Merge Sorted Lists ===")
l1 = list_to_linked([1, 3, 5, 7])
l2 = list_to_linked([2, 4, 6, 8])
merged = merge_sorted_lists(l1, l2)
print(f"Merged: {linked_to_list(merged)}")


# =============================================================================
# 5. DETECT CYCLE (FLOYD'S ALGORITHM)
# =============================================================================

def has_cycle(head):
    """Detect cycle using Floyd's tortoise and hare. O(n) time, O(1) space."""
    if not head or not head.next:
        return False
    slow = head
    fast = head.next
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
    return True

# Create list with cycle for testing
cycle_node = Node(3)
cycle_list = Node(1)
cycle_list.next = Node(2)
cycle_list.next.next = cycle_node
cycle_node.next = Node(4)
cycle_node.next.next = cycle_node  # Cycle!

print(f"\n=== Cycle Detection ===")
print(f"Has cycle: {has_cycle(cycle_list)}")
print(f"Normal list has cycle: {has_cycle(list_to_linked([1, 2, 3, 4]))}")


# =============================================================================
# 6. FIND MIDDLE ELEMENT
# =============================================================================

def find_middle(head):
    """Find middle using slow/fast pointers. O(n) time."""
    if not head:
        return None
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow.data

print("\n=== Find Middle ===")
test = list_to_linked([1, 2, 3, 4, 5])
print(f"Middle of [1,2,3,4,5]: {find_middle(test)}")

test2 = list_to_linked([1, 2, 3, 4, 5, 6])
print(f"Middle of [1,2,3,4,5,6]: {find_middle(test2)}")


# =============================================================================
# 7. REMOVE NTH NODE FROM END
# =============================================================================

def remove_nth_from_end(head, n):
    """Remove nth node from end. O(n) time, one pass."""
    dummy = Node(0)
    dummy.next = head
    fast = slow = dummy

    for _ in range(n):
        fast = fast.next

    while fast.next:
        fast = fast.next
        slow = slow.next

    slow.next = slow.next.next
    return dummy.next

print("\n=== Remove Nth from End ===")
test = list_to_linked([1, 2, 3, 4, 5])
result = remove_nth_from_end(test, 2)
print(f"Remove 2nd from end of [1,2,3,4,5]: {linked_to_list(result)}")


# =============================================================================
# 8. FLATTEN A MULTI-LEVEL LIST
# =============================================================================

class MultiLevelNode:
    """Node with child pointer"""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.child = None

def flatten_list(head):
    """Flatten multi-level linked list. O(n) time."""
    if not head:
        return None

    current = head
    while current:
        if current.child:
            next_node = current.next
            current.next = flatten_list(current.child)
            current.child = None

            tail = current.next
            while tail.next:
                tail = tail.next
            tail.next = next_node

        current = current.next
    return head


# =============================================================================
# 9. ROTATE LIST
# =============================================================================

def rotate_right(head, k):
    """Rotate list to the right by k places. O(n) time."""
    if not head or not head.next or k == 0:
        return head

    # Find length and tail
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1

    k = k % length
    if k == 0:
        return head

    # Make it circular
    tail.next = head

    # Find new tail (length - k steps from head)
    new_tail = head
    for _ in range(length - k - 1):
        new_tail = new_tail.next

    new_head = new_tail.next
    new_tail.next = None

    return new_head

print("\n=== Rotate List ===")
test = list_to_linked([1, 2, 3, 4, 5])
rotated = rotate_right(test, 2)
print(f"Rotate [1,2,3,4,5] right by 2: {linked_to_list(rotated)}")


# =============================================================================
# 10. PALINDROME LINKED LIST
# =============================================================================

def is_palindrome_linked(head):
    """Check if linked list is palindrome. O(n) time, O(1) space."""
    if not head or not head.next:
        return True

    # Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    prev = None
    while slow:
        next_node = slow.next
        slow.next = prev
        prev = slow
        slow = next_node

    # Compare both halves
    left, right = head, prev
    while right:
        if left.data != right.data:
            return False
        left = left.next
        right = right.next

    return True

print("\n=== Palindrome Check ===")
test1 = list_to_linked([1, 2, 3, 2, 1])
test2 = list_to_linked([1, 2, 3, 4, 5])
print(f"[1,2,3,2,1] palindrome: {is_palindrome_linked(test1)}")
print(f"[1,2,3,4,5] palindrome: {is_palindrome_linked(test2)}")


# =============================================================================
# 11. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Linked Lists - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Linked lists provide O(1) insertion/deletion at known positions")
    print("2. No random access - must traverse O(n)")
    print("3. Doubly linked list allows backward traversal")
    print("4. Circular linked list is useful for round-robin scheduling")
    print("5. Fast/slow pointer technique solves many linked list problems")
