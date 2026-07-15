"""
DSA Tutorial 07 - Trees (General)
==================================

Tree: Hierarchical data structure with nodes.

Terminology:
- Root: Top node
- Parent/Child: Directly connected nodes
- Siblings: Nodes with same parent
- Leaf: Node with no children
- Height: Longest path from root to leaf
- Depth: Distance from root to node
"""

# =============================================================================
# 1. GENERAL TREE IMPLEMENTATION
# =============================================================================

class TreeNode:
    """A node in a general tree"""
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children = [c for c in self.children if c != child]

    def __str__(self):
        return str(self.data)


class Tree:
    """General tree implementation"""

    def __init__(self, root=None):
        self.root = root

    def is_empty(self):
        return self.root is None

    # ---- TRAVERSALS ----

    def dfs_preorder(self, node, result=None):
        """Depth-First Search: Root -> Children"""
        if result is None:
            result = []
        if node:
            result.append(node.data)
            for child in node.children:
                self.dfs_preorder(child, result)
        return result

    def dfs_postorder(self, node, result=None):
        """Depth-First Search: Children -> Root"""
        if result is None:
            result = []
        if node:
            for child in node.children:
                self.dfs_postorder(child, result)
            result.append(node.data)
        return result

    def bfs_level_order(self):
        """Breadth-First Search: Level by level"""
        if not self.root:
            return []

        result = []
        queue = [self.root]

        while queue:
            node = queue.pop(0)
            result.append(node.data)
            queue.extend(node.children)

        return result

    # ---- UTILITIES ----

    def height(self, node):
        """Calculate height of tree. O(n)"""
        if not node:
            return -1
        if not node.children:
            return 0
        return 1 + max(self.height(child) for child in node.children)

    def count_nodes(self, node):
        """Count total nodes. O(n)"""
        if not node:
            return 0
        return 1 + sum(self.count_nodes(child) for child in node.children)

    def count_leaves(self, node):
        """Count leaf nodes. O(n)"""
        if not node:
            return 0
        if not node.children:
            return 1
        return sum(self.count_leaves(child) for child in node.children)

    def find(self, node, target):
        """Find node with given value. O(n)"""
        if not node:
            return None
        if node.data == target:
            return node
        for child in node.children:
            result = self.find(child, target)
            if result:
                return result
        return None

    def display(self, node, level=0, prefix="Root: "):
        """Pretty print the tree"""
        if node:
            print(" " * (level * 4) + prefix + str(node.data))
            for i, child in enumerate(node.children):
                if i == len(node.children) - 1:
                    self.display(child, level + 1, "└── ")
                else:
                    self.display(child, level + 1, "├── ")


print("=== General Tree ===")

# Build a tree
root = TreeNode("CEO")
tree = Tree(root)

vp1 = TreeNode("VP Engineering")
vp2 = TreeNode("VP Marketing")
root.add_child(vp1)
root.add_child(vp2)

eng1 = TreeNode("Dev Lead")
eng2 = TreeNode("QA Lead")
vp1.add_child(eng1)
vp1.add_child(eng2)

dev1 = TreeNode("Dev 1")
dev2 = TreeNode("Dev 2")
eng1.add_child(dev1)
eng1.add_child(dev2)

mkt1 = TreeNode("Mktg Manager")
mkt2 = TreeNode("Sales Lead")
vp2.add_child(mkt1)
vp2.add_child(mkt2)

print("Tree structure:")
tree.display(root)

print(f"\nPreorder:  {tree.dfs_preorder(root)}")
print(f"Postorder: {tree.dfs_postorder(root)}")
print(f"Level order: {tree.bfs_level_order()}")
print(f"Height: {tree.height(root)}")
print(f"Total nodes: {tree.count_nodes(root)}")
print(f"Leaf nodes: {tree.count_leaves(root)}")


# =============================================================================
# 2. N-ARY TREE
# =============================================================================

class NaryTreeNode:
    """Node for N-ary tree (up to N children)"""

    def __init__(self, data, max_children=3):
        self.data = data
        self.children = []
        self.max_children = max_children

    def add_child(self, child):
        if len(self.children) >= self.max_children:
            raise ValueError(f"Node can have at most {self.max_children} children")
        self.children.append(child)

    def is_leaf(self):
        return len(self.children) == 0

    def __str__(self):
        return str(self.data)


print("\n=== N-ary Tree (max 3 children) ===")
root = NaryTreeNode("A", max_children=3)
b = NaryTreeNode("B", max_children=3)
c = NaryTreeNode("C", max_children=3)
d = NaryTreeNode("D", max_children=3)
e = NaryTreeNode("E", max_children=3)

root.add_child(b)
root.add_child(c)
root.add_child(d)
b.add_child(e)

print(f"Root: {root}, Children: {[str(c) for c in root.children]}")
print(f"B's children: {[str(c) for c in b.children]}")


# =============================================================================
# 3. TREE SERIALIZATION
# =============================================================================

def serialize_tree(node):
    """Serialize tree to string. O(n) time."""
    if not node:
        return "None"
    result = [str(node.data)]
    for child in node.children:
        result.append(serialize_tree(child))
    return "(" + " ".join(result) + ")"

def deserialize_tree(data):
    """Deserialize string to tree. O(n) time."""
    if data == "None":
        return None
    # Simple parser for format: (data child1 child2 ...)
    data = data.strip("()")
    parts = data.split()
    if not parts:
        return None

    root = TreeNode(parts[0])
    stack = [(root, 1)]

    i = 1
    while i < len(parts):
        if parts[i] == "None":
            i += 1
            continue

        child = TreeNode(parts[i])
        parent, _ = stack[-1]
        parent.add_child(child)
        stack.append((child, 0))
        i += 1

    return root

print("\n=== Tree Serialization ===")
serialized = serialize_tree(root)
print(f"Serialized: {serialized}")


# =============================================================================
# 4. TREE HEIGHT AND DEPTH
# =============================================================================

def tree_height(root):
    """Calculate height using BFS. O(n)"""
    if not root:
        return -1

    height = -1
    queue = [root]

    while queue:
        height += 1
        level_size = len(queue)
        for _ in range(level_size):
            node = queue.pop(0)
            queue.extend(node.children)

    return height

def node_depth(root, target, depth=0):
    """Find depth of a specific node. O(n)"""
    if not root:
        return -1
    if root.data == target:
        return depth

    for child in root.children:
        result = node_depth(child, target, depth + 1)
        if result != -1:
            return result
    return -1

print("\n=== Height and Depth ===")
print(f"Tree height: {tree_height(root)}")
print(f"Depth of 'E': {node_depth(root, 'E')}")


# =============================================================================
# 5. TREE PATH
# =============================================================================

def find_path(root, target, path=None):
    """Find path from root to target node. O(n)"""
    if path is None:
        path = []

    if not root:
        return None

    path.append(root.data)

    if root.data == target:
        return path

    for child in root.children:
        result = find_path(child, target, path.copy())
        if result:
            return result

    return None

print("\n=== Find Path ===")
print(f"Path to 'Dev 1': {find_path(root, 'Dev 1')}")
print(f"Path to 'Sales Lead': {find_path(root, 'Sales Lead')}")


# =============================================================================
# 6. COPY/MIRROR TREE
# =============================================================================

def copy_tree(node):
    """Create deep copy of tree. O(n)"""
    if not node:
        return None
    new_node = TreeNode(node.data)
    for child in node.children:
        new_node.add_child(copy_tree(child))
    return new_node

def are_identical(t1, t2):
    """Check if two trees are identical. O(n)"""
    if not t1 and not t2:
        return True
    if not t1 or not t2:
        return False
    if t1.data != t2.data:
        return False
    if len(t1.children) != len(t2.children):
        return False
    return all(are_identical(c1, c2) for c1, c2 in zip(t1.children, t2.children))

def mirror_tree(node):
    """Create mirror of tree. O(n)"""
    if not node:
        return None
    mirrored = TreeNode(node.data)
    for child in reversed(node.children):
        mirrored.add_child(mirror_tree(child))
    return mirrored

print("\n=== Copy and Mirror ===")
copy = copy_tree(root)
print(f"Copy identical to original: {are_identical(root, copy)}")
mirrored = mirror_tree(root)
print(f"Mirrored root children: {[str(c) for c in mirrored.children]}")


# =============================================================================
# 7. ANCESTOR AND DESCENDANT
# =============================================================================

def is_ancestor(root, ancestor, descendant):
    """Check if ancestor is ancestor of descendant. O(n)"""
    if not root:
        return False
    if root.data == ancestor:
        return _has_descendant(root, descendant)
    return any(is_ancestor(child, ancestor, descendant) for child in root.children)

def _has_descendant(node, target):
    """Check if node has descendant with target value"""
    for child in node.children:
        if child.data == target or _has_descendant(child, target):
            return True
    return False

print("\n=== Ancestor/Descendant ===")
print(f"'CEO' is ancestor of 'Dev 1': {is_ancestor(root, 'CEO', 'Dev 1')}")
print(f"'Dev 1' is ancestor of 'CEO': {is_ancestor(root, 'Dev 1', 'CEO')}")


# =============================================================================
# 8. COMMON ANCESTOR
# =============================================================================

def lowest_common_ancestor(root, p, q):
    """Find lowest common ancestor. O(n)"""
    if not root or root.data == p or root.data == q:
        return root

    for child in root.children:
        result = lowest_common_ancestor(child, p, q)
        if result:
            if result.data == p or result.data == q:
                if any(c.data == (q if result.data == p else p)
                       for c in child.children):
                    return result
                return result
            return result
    return None


# =============================================================================
# 9. TREE SIZE
# =============================================================================

def tree_size_bfs(root):
    """Count nodes using BFS. O(n)"""
    if not root:
        return 0

    count = 0
    queue = [root]

    while queue:
        node = queue.pop(0)
        count += 1
        queue.extend(node.children)

    return count

print("\n=== Tree Size (BFS) ===")
print(f"Tree size: {tree_size_bfs(root)}")


# =============================================================================
# 10. TREE TO LIST
# =============================================================================

def tree_to_level_lists(root):
    """Convert tree to list of lists by level. O(n)"""
    if not root:
        return []

    result = []
    queue = [root]

    while queue:
        level = []
        level_size = len(queue)
        for _ in range(level_size):
            node = queue.pop(0)
            level.append(node.data)
            queue.extend(node.children)
        result.append(level)

    return result

print("\n=== Tree to Level Lists ===")
levels = tree_to_level_lists(root)
for i, level in enumerate(levels):
    print(f"Level {i}: {level}")


# =============================================================================
# 11. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("General Trees - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Trees are hierarchical data structures")
    print("2. DFS explores depth-first, BFS explores breadth-first")
    print("3. Trees can be serialized/deserialized for storage")
    print("4. Common operations: height, depth, path finding")
    print("5. Trees are used in: file systems, DOM, organization charts")
