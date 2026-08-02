"""
DSA Tutorial 08 - Binary Trees
===============================

Binary Tree: Each node has at most 2 children (left and right).

Types:
- Full Binary Tree: Every node has 0 or 2 children
- Complete Binary Tree: All levels filled except possibly last
- Perfect Binary Tree: All internal nodes have 2 children
- Balanced Binary Tree: Height difference of subtrees <= 1

Properties:
- Maximum nodes at level l: 2^l
- Maximum nodes in tree of height h: 2^(h+1) - 1
"""

from collections import deque

# =============================================================================
# 1. BINARY TREE IMPLEMENTATION
# =============================================================================

class TreeNode:
    """A node in a binary tree"""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.data)


class BinaryTree:
    """Binary tree implementation"""

    def __init__(self, root=None):
        self.root = root

    # ---- INSERTION ----

    def insert_level_order(self, arr):
        """Insert from array using level order. O(n)"""
        if not arr:
            return None

        root = TreeNode(arr[0])
        queue = deque([root])
        i = 1

        while i < len(arr):
            node = queue.popleft()

            if i < len(arr) and arr[i] is not None:
                node.left = TreeNode(arr[i])
                queue.append(node.left)
            i += 1

            if i < len(arr) and arr[i] is not None:
                node.right = TreeNode(arr[i])
                queue.append(node.right)
            i += 1

        self.root = root
        return root

    # ---- TRAVERSALS ----

    def preorder(self, node, result=None):
        """Root -> Left -> Right. O(n)"""
        if result is None:
            result = []
        if node:
            result.append(node.data)
            self.preorder(node.left, result)
            self.preorder(node.right, result)
        return result

    def inorder(self, node, result=None):
        """Left -> Root -> Right. O(n)"""
        if result is None:
            result = []
        if node:
            self.inorder(node.left, result)
            result.append(node.data)
            self.inorder(node.right, result)
        return result

    def postorder(self, node, result=None):
        """Left -> Right -> Root. O(n)"""
        if result is None:
            result = []
        if node:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            result.append(node.data)
        return result

    def level_order(self):
        """BFS traversal. O(n)"""
        if not self.root:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            node = queue.popleft()
            result.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def reverse_level_order(self):
        """Bottom-up level order: bottom level first, left->right within each level. O(n)"""
        if not self.root:
            return []

        levels = []
        queue = deque([self.root])

        while queue:
            level_size = len(queue)
            level = []
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.data)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            levels.append(level)

        # Reverse the list of levels (bottom to top), then flatten
        return [data for level in reversed(levels) for data in level]

    # ---- UTILITIES ----

    def height(self, node):
        """Height of tree. O(n)"""
        if not node:
            return -1
        return 1 + max(self.height(node.left), self.height(node.right))

    def size(self, node):
        """Number of nodes. O(n)"""
        if not node:
            return 0
        return 1 + self.size(node.left) + self.size(node.right)

    def count_leaves(self, node):
        """Count leaf nodes. O(n)"""
        if not node:
            return 0
        if not node.left and not node.right:
            return 1
        return self.count_leaves(node.left) + self.count_leaves(node.right)

    def is_balanced(self, node):
        """Check if tree is balanced. O(n)"""
        def check_height(n):
            if not n:
                return 0
            left = check_height(n.left)
            right = check_height(n.right)
            if left == -1 or right == -1:
                return -1
            if abs(left - right) > 1:
                return -1
            return 1 + max(left, right)
        return check_height(node) != -1

    def is_complete(self, root):
        """Check if tree is complete. O(n)"""
        if not root:
            return True
        queue = deque([root])
        reached_end = False
        while queue:
            node = queue.popleft()
            if node is None:
                reached_end = True
            else:
                if reached_end:
                    return False
                queue.append(node.left)
                queue.append(node.right)
        return True

    def is_perfect(self, root, depth=None, level=0):
        """Check if tree is perfect. O(n)"""
        if root is None:
            return True
        if depth is None:
            depth = self.height(root)
        if not root.left and not root.right:
            return depth == level
        if not root.left or not root.right:
            return False
        return (self.is_perfect(root.left, depth, level + 1) and
                self.is_perfect(root.right, depth, level + 1))

    # ---- DISPLAY ----

    def display(self, node, level=0, prefix="Root: "):
        """Pretty print the tree"""
        if node:
            print(" " * (level * 4) + prefix + str(node.data))
            if node.left or node.right:
                if node.left:
                    self.display(node.left, level + 1, "L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")
                if node.right:
                    self.display(node.right, level + 1, "R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")


print("=== Binary Tree ===")

# Build tree
tree = BinaryTree()
tree.root = TreeNode(1)
tree.root.left = TreeNode(2)
tree.root.right = TreeNode(3)
tree.root.left.left = TreeNode(4)
tree.root.left.right = TreeNode(5)
tree.root.right.left = TreeNode(6)
tree.root.right.right = TreeNode(7)

print("Tree structure:")
tree.display(tree.root)

print(f"\nPreorder:  {tree.preorder(tree.root)}")
print(f"Inorder:   {tree.inorder(tree.root)}")
print(f"Postorder: {tree.postorder(tree.root)}")
print(f"Level:     {tree.level_order()}")
print(f"Reverse level: {tree.reverse_level_order()}")
print(f"Height:    {tree.height(tree.root)}")
print(f"Size:      {tree.size(tree.root)}")
print(f"Leaves:    {tree.count_leaves(tree.root)}")
print(f"Balanced:  {tree.is_balanced(tree.root)}")
print(f"Complete:  {tree.is_complete(tree.root)}")
print(f"Perfect:   {tree.is_perfect(tree.root)}")


# =============================================================================
# 2. BUILD TREE FROM TRAVERSALS
# =============================================================================

def build_from_pre_in(preorder, inorder):
    """Build tree from preorder and inorder traversals. O(n)"""
    if not preorder or not inorder:
        return None

    root = TreeNode(preorder[0])
    mid = inorder.index(preorder[0])

    root.left = build_from_pre_in(preorder[1:mid + 1], inorder[:mid])
    root.right = build_from_pre_in(preorder[mid + 1:], inorder[mid + 1:])

    return root

def build_from_post_in(postorder, inorder):
    """Build tree from postorder and inorder traversals. O(n)"""
    if not postorder or not inorder:
        return None

    root = TreeNode(postorder[-1])
    mid = inorder.index(postorder[-1])

    root.left = build_from_post_in(postorder[:mid], inorder[:mid])
    root.right = build_from_post_in(postorder[mid:-1], inorder[mid + 1:])

    return root

print("\n=== Build Tree from Traversals ===")
preorder = [1, 2, 4, 5, 3, 6, 7]
inorder = [4, 2, 5, 1, 6, 3, 7]

tree2 = BinaryTree(build_from_pre_in(preorder, inorder))
print(f"From preorder {preorder} + inorder {inorder}:")
print(f"  Preorder: {tree2.preorder(tree2.root)}")
print(f"  Inorder: {tree2.inorder(tree2.root)}")


# =============================================================================
# 3. MORRIS TRAVERSAL (O(1) space)
# =============================================================================

def morris_inorder(root):
    """Inorder traversal using Morris method. O(n) time, O(1) space"""
    result = []
    current = root

    while current:
        if current.left is None:
            result.append(current.data)
            current = current.right
        else:
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right

            if predecessor.right is None:
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None
                result.append(current.data)
                current = current.right

    return result

print("\n=== Morris Traversal ===")
print(f"Morris inorder: {morris_inorder(tree.root)}")


# =============================================================================
# 4. ZIGZAG TRAVERSAL
# =============================================================================

def zigzag_traversal(root):
    """Zigzag level order traversal. O(n)"""
    if not root:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level = []
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()
            if left_to_right:
                level.append(node.data)
            else:
                level.insert(0, node.data)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)
        left_to_right = not left_to_right

    return result

print("\n=== Zigzag Traversal ===")
print(f"Zigzag: {zigzag_traversal(tree.root)}")


# =============================================================================
# 5. BOUNDARY TRAVERSAL
# =============================================================================

def boundary_traversal(root):
    """Boundary traversal: left boundary + leaves + right boundary. O(n)"""
    if not root:
        return []

    result = [root.data]

    def left_boundary(node):
        if not node or (not node.left and not node.right):
            return
        result.append(node.data)
        if node.left:
            left_boundary(node.left)
        else:
            left_boundary(node.right)

    def leaves(node):
        if not node:
            return
        if not node.left and not node.right:
            result.append(node.data)
            return
        leaves(node.left)
        leaves(node.right)

    def right_boundary(node):
        if not node or (not node.left and not node.right):
            return
        if node.right:
            right_boundary(node.right)
        else:
            right_boundary(node.left)
        result.append(node.data)

    left_boundary(root.left)
    leaves(root.left)
    leaves(root.right)
    right_boundary(root.right)

    return result

print("\n=== Boundary Traversal ===")
print(f"Boundary: {boundary_traversal(tree.root)}")


# =============================================================================
# 6. DIAMETER OF TREE
# =============================================================================

def diameter(root):
    """Diameter: longest path between any two nodes. O(n)"""
    max_diameter = [0]

    def height(node):
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        max_diameter[0] = max(max_diameter[0], left + right)
        return 1 + max(left, right)

    height(root)
    return max_diameter[0]

print("\n=== Diameter ===")
print(f"Diameter: {diameter(tree.root)}")


# =============================================================================
# 7. VERTICAL ORDER TRAVERSAL
# =============================================================================

def vertical_order(root):
    """Vertical order traversal. O(n log n)"""
    if not root:
        return []

    column_table = {}
    min_col = max_col = 0
    queue = deque([(root, 0)])

    while queue:
        node, col = queue.popleft()

        if col not in column_table:
            column_table[col] = []
        column_table[col].append(node.data)

        if node.left:
            queue.append((node.left, col - 1))
            min_col = min(min_col, col - 1)
        if node.right:
            queue.append((node.right, col + 1))
            max_col = max(max_col, col + 1)

    return [column_table[col] for col in range(min_col, max_col + 1)]

print("\n=== Vertical Order ===")
print(f"Vertical: {vertical_order(tree.root)}")


# =============================================================================
# 8. TOP VIEW AND BOTTOM VIEW
# =============================================================================

def top_view(root):
    """Top view of tree. O(n)"""
    if not root:
        return []

    column_table = {}
    queue = deque([(root, 0)])

    while queue:
        node, col = queue.popleft()
        if col not in column_table:
            column_table[col] = node.data

        if node.left:
            queue.append((node.left, col - 1))
        if node.right:
            queue.append((node.right, col + 1))

    return [column_table[k] for k in sorted(column_table.keys())]

def bottom_view(root):
    """Bottom view of tree. O(n)"""
    if not root:
        return []

    column_table = {}
    queue = deque([(root, 0)])

    while queue:
        node, col = queue.popleft()
        column_table[col] = node.data  # Overwrite with last seen

        if node.left:
            queue.append((node.left, col - 1))
        if node.right:
            queue.append((node.right, col + 1))

    return [column_table[k] for k in sorted(column_table.keys())]

print("\n=== Top and Bottom View ===")
print(f"Top view:    {top_view(tree.root)}")
print(f"Bottom view: {bottom_view(tree.root)}")


# =============================================================================
# 9. RIGHT/LEFT VIEW
# =============================================================================

def right_view(root):
    """Right side view of tree. O(n)"""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:
                result.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result

def left_view(root):
    """Left side view of tree. O(n)"""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == 0:
                result.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result

print("\n=== Right and Left View ===")
print(f"Right view: {right_view(tree.root)}")
print(f"Left view:  {left_view(tree.root)}")


# =============================================================================
# 10. TREE PATH SUM
# =============================================================================

def has_path_sum(root, target_sum):
    """Check if any root-to-leaf path sums to target. O(n)"""
    if not root:
        return False
    if not root.left and not root.right:
        return root.data == target_sum
    return (has_path_sum(root.left, target_sum - root.data) or
            has_path_sum(root.right, target_sum - root.data))

def all_path_sums(root, target_sum, path=None, result=None):
    """Find all root-to-leaf paths with given sum. O(n^2)"""
    if path is None:
        path = []
    if result is None:
        result = []

    if not root:
        return result

    path.append(root.data)

    if not root.left and not root.right and sum(path) == target_sum:
        result.append(path.copy())

    all_path_sums(root.left, target_sum, path, result)
    all_path_sums(root.right, target_sum, path, result)
    path.pop()

    return result

print("\n=== Path Sum ===")
print(f"Has path sum 18: {has_path_sum(tree.root, 18)}")
print(f"Has path sum 100: {has_path_sum(tree.root, 100)}")


# =============================================================================
# 11. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Binary Trees - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Each node has at most 2 children")
    print("2. Pre/In/Post order traversals are DFS-based")
    print("3. Level order is BFS-based")
    print("4. Many problems use recursive height calculations")
    print("5. Used in: expression parsing, file systems, databases")
