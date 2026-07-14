"""
DSA Tutorial 10 - AVL Trees
============================

AVL Tree: Self-balancing BST where the height difference
between left and right subtrees (balance factor) is at most 1.

Guarantees O(log n) for all operations through rotations.

Balance Factor = height(left) - height(right)
Valid values: -1, 0, 1
"""

# =============================================================================
# 1. AVL TREE IMPLEMENTATION
# =============================================================================

class AVLNode:
    """Node in an AVL tree"""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """AVL Tree implementation"""

    def __init__(self):
        self.root = None

    def get_height(self, node):
        """Get height of node"""
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        """Get balance factor"""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        """Update height after modification"""
        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))

    # ---- ROTATIONS ----

    def right_rotate(self, y):
        """Right rotation (LL case)"""
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        self.update_height(y)
        self.update_height(x)

        return x

    def left_rotate(self, x):
        """Left rotation (RR case)"""
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        self.update_height(x)
        self.update_height(y)

        return y

    # ---- INSERTION ----

    def insert(self, key):
        """Insert key and rebalance. O(log n)"""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        # Standard BST insert
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # Duplicate keys not allowed

        # Update height
        self.update_height(node)

        # Get balance factor
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # ---- DELETION ----

    def delete(self, key):
        """Delete key and rebalance. O(log n)"""
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
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Two children: get inorder successor
            successor = self._min_value_node(node.right)
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)

        if not node:
            return node

        # Update height
        self.update_height(node)

        # Get balance factor
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # Left Right Case
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # Right Left Case
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # ---- SEARCH ----

    def search(self, key):
        """Search for key. O(log n)"""
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    # ---- TRAVERSALS ----

    def inorder(self):
        """Inorder traversal. O(n)"""
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

    def level_order(self):
        """Level order traversal. O(n)"""
        if not self.root:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    # ---- UTILITIES ----

    def height(self):
        """Get tree height. O(1)"""
        return self.get_height(self.root)

    def is_balanced(self):
        """Check if tree is balanced. O(n)"""
        return self._is_balanced(self.root)

    def _is_balanced(self, node):
        if not node:
            return True
        balance = self.get_balance(node)
        if abs(balance) > 1:
            return False
        return self._is_balanced(node.left) and self._is_balanced(node.right)

    def display(self, node=None, level=0, prefix="Root: "):
        """Pretty print the tree"""
        if node is None:
            node = self.root
        if node:
            balance = self.get_balance(node)
            print(" " * (level * 4) + prefix + str(node.key) +
                  f" (h={node.height}, b={balance})")
            if node.left or node.right:
                if node.left:
                    self.display(node.left, level + 1, "L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")
                if node.right:
                    self.display(node.right, level + 1, "R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")


print("=== AVL Tree ===")

avl = AVLTree()
for key in [10, 20, 30, 40, 50, 25]:
    avl.insert(key)
    print(f"Insert {key}: inorder={avl.inorder()}")

print("\nTree structure:")
avl.display()
print(f"\nHeight: {avl.height()}")
print(f"Balanced: {avl.is_balanced()}")
print(f"Inorder: {avl.inorder()}")
print(f"Preorder: {avl.preorder()}")
print(f"Level: {avl.level_order()}")

# Delete
avl.delete(30)
print(f"\nAfter deleting 30:")
avl.display()
print(f"Height: {avl.height()}, Balanced: {avl.is_balanced()}")


# =============================================================================
# 2. AVL ROTATION VISUALIZATION
# =============================================================================

print("\n=== AVL Rotation Cases ===")

# LL Case
ll = AVLTree()
for k in [30, 20, 10]:
    ll.insert(k)
print("LL Case (insert 30,20,10):")
ll.display()

# RR Case
rr = AVLTree()
for k in [10, 20, 30]:
    rr.insert(k)
print("\nRR Case (insert 10,20,30):")
rr.display()

# LR Case
lr = AVLTree()
for k in [30, 10, 20]:
    lr.insert(k)
print("\nLR Case (insert 30,10,20):")
lr.display()

# RL Case
rl = AVLTree()
for k in [10, 30, 20]:
    rl.insert(k)
print("\nRL Case (insert 10,30,20):")
rl.display()


# =============================================================================
# 3. AVL TREE HEIGHT PROOF
# =============================================================================

def demonstrate_height_bound():
    """Show AVL tree height is O(log n)"""
    print("\n=== Height Bound Demonstration ===")

    avl = AVLTree()
    import random

    sizes = [10, 100, 1000, 10000]
    for n in sizes:
        avl = AVLTree()
        keys = list(range(n))
        random.shuffle(keys)
        for key in keys:
            avl.insert(key)

        import math
        theoretical_max = 1.44 * math.log2(n + 2) - 0.328
        actual_height = avl.height()

        print(f"n={n:>5}: actual_height={actual_height:>3}, "
              f"theoretical_max={theoretical_max:.1f}, "
              f"log2(n)={math.log2(n):.1f}")

demonstrate_height_bound()


# =============================================================================
# 4. RANGE QUERY
# =============================================================================

def range_query_avl(root, low, high):
    """Find all keys in range [low, high]. O(log n + k)"""
    result = []

    def traverse(node):
        if not node:
            return
        if node.key > low:
            traverse(node.left)
        if low <= node.key <= high:
            result.append(node.key)
        if node.key < high:
            traverse(node.right)

    traverse(root)
    return result

print("\n=== Range Query ===")
avl2 = AVLTree()
for k in range(1, 21):
    avl2.insert(k)
print(f"All keys: {avl2.inorder()}")
print(f"Range [5, 15]: {range_query_avl(avl2.root, 5, 15)}")


# =============================================================================
# 5. KTH SMALLEST ELEMENT
# =============================================================================

def kth_smallest_avl(root, k):
    """Find kth smallest using inorder. O(k)"""
    count = [0]
    result = [None]

    def inorder(node):
        if not node or count[0] >= k:
            return
        inorder(node.left)
        count[0] += 1
        if count[0] == k:
            result[0] = node.key
            return
        inorder(node.right)

    inorder(root)
    return result[0]

print("\n=== Kth Smallest ===")
print(f"5th smallest: {kth_smallest_avl(avl2.root, 5)}")
print(f"10th smallest: {kth_smallest_avl(avl2.root, 10)}")


# =============================================================================
# 6. CLOSEST VALUE
# =============================================================================

def closest_value_avl(root, target):
    """Find closest value to target. O(log n)"""
    if not root:
        return None

    closest = root.key
    current = root

    while current:
        if abs(current.key - target) < abs(closest - target):
            closest = current.key
        if target < current.key:
            current = current.left
        elif target > current.key:
            current = current.right
        else:
            return current.key

    return closest

print("\n=== Closest Value ===")
print(f"Closest to 23: {closest_value_avl(avl2.root, 23)}")
print(f"Closest to 100: {closest_value_avl(avl2.root, 100)}")


# =============================================================================
# 7. CEILING AND FLOOR
# =============================================================================

def ceiling_avl(root, key):
    """Find smallest element >= key. O(log n)"""
    ceiling = None
    current = root

    while current:
        if current.key == key:
            return current.key
        elif current.key > key:
            ceiling = current.key
            current = current.left
        else:
            current = current.right

    return ceiling

def floor_avl(root, key):
    """Find largest element <= key. O(log n)"""
    floor_val = None
    current = root

    while current:
        if current.key == key:
            return current.key
        elif current.key < key:
            floor_val = current.key
            current = current.right
        else:
            current = current.left

    return floor_val

print("\n=== Ceiling and Floor ===")
print(f"Ceiling of 17: {ceiling_avl(avl2.root, 17)}")
print(f"Floor of 17: {floor_avl(avl2.root, 17)}")


# =============================================================================
# 8. MERGE TWO AVL TREES
# =============================================================================

def merge_avl_trees(t1, t2):
    """Merge two AVL trees. O(n + m)"""
    # Get all elements from both trees
    elements = t1.inorder() + t2.inorder()
    elements.sort()

    # Build balanced BST from sorted elements
    def build_balanced(arr, start, end):
        if start > end:
            return None
        mid = (start + end) // 2
        node = AVLNode(arr[mid])
        node.left = build_balanced(arr, start, mid - 1)
        node.right = build_balanced(arr, mid + 1, end)
        node.height = 1 + max(
            node.left.height if node.left else 0,
            node.right.height if node.right else 0
        )
        return node

    merged = AVLTree()
    merged.root = build_balanced(elements, 0, len(elements) - 1)
    return merged

print("\n=== Merge AVL Trees ===")
avl3 = AVLTree()
for k in [1, 3, 5]:
    avl3.insert(k)
avl4 = AVLTree()
for k in [2, 4, 6]:
    avl4.insert(k)
merged = merge_avl_trees(avl3, avl4)
print(f"Merged: {merged.inorder()}")


# =============================================================================
# 9. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AVL Trees - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. AVL trees are self-balancing BSTs")
    print("2. Height difference between subtrees <= 1")
    print("3. Four rotation types: LL, RR, LR, RL")
    print("4. Guaranteed O(log n) for all operations")
    print("5. Height <= 1.44 * log2(n+2) - 0.328")
