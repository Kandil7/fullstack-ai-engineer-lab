"""
DSA Tutorial 09 - Binary Search Trees (BST)
=============================================

BST Property: For every node:
- Left subtree contains only smaller values
- Right subtree contains only larger values

Operations (average case):
- Search: O(log n)
- Insert: O(log n)
- Delete: O(log n)

Worst case (degenerate): O(n) - same as linked list
"""

# =============================================================================
# 1. BST IMPLEMENTATION
# =============================================================================

class BSTNode:
    """Node in a Binary Search Tree"""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # For AVL balancing

class BST:
    """Binary Search Tree implementation"""

    def __init__(self):
        self.root = None

    # ---- INSERTION ----

    def insert(self, key):
        """Insert a key. O(log n) average"""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def insert_iterative(self, key):
        """Insert using iteration. O(log n) average"""
        new_node = BSTNode(key)
        if not self.root:
            self.root = new_node
            return

        current = self.root
        while True:
            if key < current.key:
                if not current.left:
                    current.left = new_node
                    return
                current = current.left
            elif key > current.key:
                if not current.right:
                    current.right = new_node
                    return
                current = current.right
            else:
                return  # Duplicate keys not allowed

    # ---- SEARCH ----

    def search(self, key):
        """Search for a key. O(log n) average"""
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def search_iterative(self, key):
        """Search using iteration. O(log n) average"""
        current = self.root
        while current:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    # ---- DELETION ----

    def delete(self, key):
        """Delete a key. O(log n) average"""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node found
            # Case 1: Leaf node
            if not node.left and not node.right:
                return None
            # Case 2: One child
            elif not node.left:
                return node.right
            elif not node.right:
                return node.left
            # Case 3: Two children
            else:
                successor = self._min_value_node(node.right)
                node.key = successor.key
                node.right = self._delete(node.right, successor.key)

        return node

    def _min_value_node(self, node):
        """Find node with minimum value"""
        current = node
        while current.left:
            current = current.left
        return current

    # ---- TRAVERSALS ----

    def inorder(self):
        """Inorder traversal (sorted order). O(n)"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def preorder(self):
        """Preorder traversal. O(n)"""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.key)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        """Postorder traversal. O(n)"""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.key)

    # ---- UTILITIES ----

    def min_value(self):
        """Find minimum value. O(log n)"""
        if not self.root:
            return None
        return self._min_value_node(self.root).key

    def max_value(self):
        """Find maximum value. O(log n)"""
        if not self.root:
            return None
        current = self.root
        while current.right:
            current = current.right
        return current.key

    def height(self):
        """Calculate height. O(n)"""
        return self._height(self.root)

    def _height(self, node):
        if not node:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def count_nodes(self):
        """Count nodes. O(n)"""
        return self._count(self.root)

    def _count(self, node):
        if not node:
            return 0
        return 1 + self._count(node.left) + self._count(node.right)

    def is_valid_bst(self):
        """Validate BST property. O(n)"""
        return self._validate(self.root, float('-inf'), float('inf'))

    def _validate(self, node, min_val, max_val):
        if not node:
            return True
        if node.key <= min_val or node.key >= max_val:
            return False
        return (self._validate(node.left, min_val, node.key) and
                self._validate(node.right, node.key, max_val))

    def kth_smallest(self, k):
        """Find kth smallest element. O(k)"""
        self.count = 0
        self.result = None
        self._kth_smallest(self.root, k)
        return self.result

    def _kth_smallest(self, node, k):
        if not node or self.count >= k:
            return
        self._kth_smallest(node.left, k)
        self.count += 1
        if self.count == k:
            self.result = node.key
            return
        self._kth_smallest(node.right, k)

    def display(self, node=None, level=0, prefix="Root: "):
        """Pretty print the tree"""
        if node is None:
            node = self.root
        if node:
            print(" " * (level * 4) + prefix + str(node.key))
            if node.left or node.right:
                if node.left:
                    self.display(node.left, level + 1, "L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")
                if node.right:
                    self.display(node.right, level + 1, "R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")


print("=== Binary Search Tree ===")

bst = BST()
for key in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(key)

bst.display()
print(f"\nInorder (sorted): {bst.inorder()}")
print(f"Preorder: {bst.preorder()}")
print(f"Postorder: {bst.postorder()}")
print(f"Min: {bst.min_value()}, Max: {bst.max_value()}")
print(f"Height: {bst.height()}")
print(f"Count: {bst.count_nodes()}")
print(f"Valid BST: {bst.is_valid_bst()}")
print(f"3rd smallest: {bst.kth_smallest(3)}")

# Search
print(f"\nSearch 40: {'Found' if bst.search(40) else 'Not found'}")
print(f"Search 55: {'Found' if bst.search(55) else 'Not found'}")

# Delete
bst.delete(20)
print(f"\nAfter deleting 20: {bst.inorder()}")
bst.delete(30)
print(f"After deleting 30: {bst.inorder()}")
bst.delete(50)
print(f"After deleting 50: {bst.inorder()}")


# =============================================================================
# 2. BST FROM SORTED ARRAY
# =============================================================================

def sorted_array_to_bst(arr):
    """Convert sorted array to balanced BST. O(n)"""
    if not arr:
        return None

    mid = len(arr) // 2
    node = BSTNode(arr[mid])
    node.left = sorted_array_to_bst(arr[:mid])
    node.right = sorted_array_to_bst(arr[mid + 1:])
    return node

def inorder_list(node):
    if not node:
        return []
    return inorder_list(node.left) + [node.key] + inorder_list(node.right)

print("\n=== BST from Sorted Array ===")
sorted_arr = [1, 2, 3, 4, 5, 6, 7]
balanced_root = sorted_array_to_bst(sorted_arr)
print(f"From {sorted_arr}: {inorder_list(balanced_root)}")


# =============================================================================
# 3. LOWEST COMMON ANCESTOR
# =============================================================================

def lca_bst(root, p, q):
    """Find LCA in BST. O(log n)"""
    if not root:
        return None
    if p < root.key and q < root.key:
        return lca_bst(root.left, p, q)
    if p > root.key and q > root.key:
        return lca_bst(root.right, p, q)
    return root.key

print("\n=== Lowest Common Ancestor ===")
print(f"LCA of 20 and 40: {lca_bst(bst.root, 20, 40)}")
print(f"LCA of 20 and 80: {lca_bst(bst.root, 20, 80)}")


# =============================================================================
# 4. RANGE SUM QUERY
# =============================================================================

def range_sum_bst(root, low, high):
    """Sum of all keys in range [low, high]. O(n)"""
    if not root:
        return 0
    if root.key < low:
        return range_sum_bst(root.right, low, high)
    if root.key > high:
        return range_sum_bst(root.left, low, high)
    return (root.key +
            range_sum_bst(root.left, low, high) +
            range_sum_bst(root.right, low, high))

print("\n=== Range Sum ===")
print(f"Sum in range [30, 70]: {range_sum_bst(bst.root, 30, 70)}")


# =============================================================================
# 5. BST TO DOUBLY LINKED LIST
# =============================================================================

class DLLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def bst_to_dll(root):
    """Convert BST to sorted doubly linked list. O(n)"""
    if not root:
        return None

    # Convert left subtree
    left_head = bst_to_dll(root.left)

    # Create new DLL node for current BST node
    dll_node = DLLNode(root.key)

    # Connect left subtree
    if left_head:
        curr = left_head
        while curr.right:
            curr = curr.right
        curr.right = dll_node
        dll_node.left = curr

    # Convert right subtree
    right_head = bst_to_dll(root.right)
    if right_head:
        right_head.left = dll_node
        dll_node.right = right_head

    # Return head of the list
    head = left_head if left_head else dll_node
    return head

print("\n=== BST to Doubly Linked List ===")
dll_root = bst_to_dll(bst.root)
# Traverse forward
current = dll_root
forward = []
while current:
    forward.append(current.val)
    current = current.right
print(f"Forward: {forward}")


# =============================================================================
# 6. BST SUCCESSOR AND PREDECESSOR
# =============================================================================

def find_successor(root, key):
    """Find inorder successor. O(log n)"""
    successor = None
    current = root

    while current:
        if key < current.key:
            successor = current.key
            current = current.left
        else:
            current = current.right

    return successor

def find_predecessor(root, key):
    """Find inorder predecessor. O(log n)"""
    predecessor = None
    current = root

    while current:
        if key > current.key:
            predecessor = current.key
            current = current.right
        else:
            current = current.left

    return predecessor

print("\n=== Successor and Predecessor ===")
print(f"Successor of 40: {find_successor(bst.root, 40)}")
print(f"Predecessor of 40: {find_predecessor(bst.root, 40)}")


# =============================================================================
# 7. TWO SUM IN BST
# =============================================================================

def two_sum_bst(root, target):
    """Find two elements that sum to target. O(n)"""
    elements = []

    def inorder_collect(node):
        if not node:
            return
        inorder_collect(node.left)
        elements.append(node.key)
        inorder_collect(node.right)

    inorder_collect(root)

    # Two pointer on sorted list
    left, right = 0, len(elements) - 1
    while left < right:
        current_sum = elements[left] + elements[right]
        if current_sum == target:
            return (elements[left], elements[right])
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None

print("\n=== Two Sum in BST ===")
result = two_sum_bst(bst.root, 90)
print(f"Two elements summing to 90: {result}")


# =============================================================================
# 8. BST FROM PREORDER
# =============================================================================

def bst_from_preorder(preorder):
    """Construct BST from preorder traversal. O(n)"""
    index = [0]

    def helper(lower=float('-inf'), upper=float('inf')):
        if index[0] == len(preorder):
            return None

        val = preorder[index[0]]
        if val < lower or val > upper:
            return None

        node = BSTNode(val)
        index[0] += 1
        node.left = helper(lower, val)
        node.right = helper(val, upper)
        return node

    return helper()

print("\n=== BST from Preorder ===")
preorder = [10, 5, 1, 7, 40, 50]
new_root = bst_from_preorder(preorder)
print(f"Preorder {preorder}: {inorder_list(new_root)}")


# =============================================================================
# 9. FLATTEN BST TO SORTED ARRAY
# =============================================================================

def flatten_bst(root):
    """Flatten BST to sorted linked list in-place. O(n)"""
    if not root:
        return None

    dummy = BSTNode(0)
    current = dummy

    def inorder_flatten(node):
        nonlocal current
        if not node:
            return
        inorder_flatten(node.left)
        current.right = BSTNode(node.key)
        current = current.right
        inorder_flatten(node.right)

    inorder_flatten(root)
    return dummy.right


# =============================================================================
# 10. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Binary Search Trees - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. BST maintains sorted order for efficient search")
    print("2. Average case: O(log n) for search, insert, delete")
    print("3. Worst case: O(n) when tree is degenerate")
    print("4. Inorder traversal gives sorted order")
    print("5. Used in: databases, file systems, symbol tables")
