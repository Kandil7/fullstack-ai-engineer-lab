# Lecture 07: Trees — General Concepts

## Topic Overview

A **tree** is a hierarchical (non-linear) data structure consisting of nodes connected by edges. It has a single root node and zero or more child nodes, forming a parent-child relationship. Trees are fundamental to many algorithms and data structures.

Key properties:
- **Root:** The topmost node (no parent)
- **Leaf:** A node with no children
- **Height:** The longest path from root to leaf
- **Depth:** The distance from root to a specific node

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Define** tree terminology (root, leaf, height, depth, degree)
2. **Implement** a general tree using node objects
3. **Traverse** trees using DFS (preorder, inorder, postorder) and BFS (level-order)
4. **Calculate** tree height, size, and depth
5. **Solve** classic tree problems
6. **Understand** the relationship between trees and recursion

---

## Key Concepts

### 1. Tree Terminology

```
            A          ← Root (depth 0, height 3)
           / \
          B   C        ← Depth 1
         / \   \
        D   E   F      ← Depth 2 (D, E are leaves of subtree)
             \
              G        ← Depth 3 (G is a leaf)

Height of tree: 3 (path A→B→E→G)
Degree of node A: 2 (two children)
Degree of node B: 2
Degree of node C: 1
Degree of node D, E, F, G: 0 (leaves)
```

### 2. General Tree Node

```python
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def remove_child(self, child):
        self.children = [c for c in self.children if c != child]
    
    def __repr__(self):
        return f"TreeNode({self.data})"

# Build a tree
root = TreeNode("A")
b = TreeNode("B")
c = TreeNode("C")
d = TreeNode("D")
e = TreeNode("E")
f = TreeNode("F")

root.add_child(b)
root.add_child(c)
b.add_child(d)
b.add_child(e)
c.add_child(f)
```

### 3. Tree Traversals

#### Depth-First Search (DFS)

```python
def preorder(node):
    """Visit: Root → Left → Right (top-down)"""
    if node is None:
        return []
    result = [node.data]
    for child in node.children:
        result.extend(preorder(child))
    return result

def postorder(node):
    """Visit: Left → Right → Root (bottom-up)"""
    if node is None:
        return []
    result = []
    for child in node.children:
        result.extend(postorder(child))
    result.append(node.data)
    return result

def inorder_binary(node):
    """Visit: Left → Root → Right (in-order for BST)"""
    if node is None:
        return []
    result = []
    result.extend(inorder_binary(node.left))
    result.append(node.data)
    result.extend(inorder_binary(node.right))
    return result

# For general trees, "inorder" is less defined
# Focus on preorder and postorder
```

#### Breadth-First Search (BFS)

```python
from collections import deque

def level_order(root):
    """Visit level by level, left to right."""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.data)
            
            for child in node.children:
                queue.append(child)
        
        result.append(level)
    
    return result
```

### 4. Tree Properties

```python
def tree_height(node):
    """Maximum depth of any leaf. O(n)."""
    if not node:
        return -1  # or 0, depending on convention
    if not node.children:
        return 0
    return 1 + max(tree_height(child) for child in node.children)

def tree_size(node):
    """Total number of nodes. O(n)."""
    if not node:
        return 0
    return 1 + sum(tree_size(child) for child in node.children)

def tree_depth(node, target, current_depth=0):
    """Find depth of target node. O(n)."""
    if node.data == target:
        return current_depth
    for child in node.children:
        result = tree_depth(child, target, current_depth + 1)
        if result != -1:
            return result
    return -1  # Not found

def count_leaves(node):
    """Count leaf nodes. O(n)."""
    if not node:
        return 0
    if not node.children:
        return 1
    return sum(count_leaves(child) for child in node.children)
```

---

## Complete Code Examples

### Example 1: N-ary Tree Serialization

```python
"""
Serialize and deserialize an N-ary tree.
Uses preorder with a marker for null children.
"""

class NaryNode:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children or []

def serialize(root):
    """Serialize tree to list."""
    if not root:
        return []
    result = [root.val]
    for child in root.children:
        result.extend(serialize(child))
    result.append(None)  # Marker for end of children
    return result

def deserialize(data):
    """Deserialize list back to tree."""
    if not data:
        return None
    
    def helper(index):
        if index[0] >= len(data) or data[index[0]] is None:
            index[0] += 1
            return None
        
        node = NaryNode(data[index[0]])
        index[0] += 1
        
        while index[0] < len(data) and data[index[0]] is not None:
            node.children.append(helper(index))
        
        index[0] += 1  # Skip the None marker
        return node
    
    return helper([0])
```

### Example 2: Find Lowest Common Ancestor (LCA)

```python
"""
Find the lowest common ancestor of two nodes in a tree.
Time: O(n), Space: O(h) where h = height
"""

def find_lca(root, node1, node2):
    """Find LCA in a general tree."""
    if root is None:
        return None
    
    if root.data == node1 or root.data == node2:
        return root
    
    for child in root.children:
        lca = find_lca(child, node1, node2)
        if lca:
            # If both found in different subtrees, root is LCA
            # Count how many of node1, node2 we've found
            pass
    
    # Simplified approach: find path from root to each node
    path1 = find_path(root, node1)
    path2 = find_path(root, node2)
    
    if not path1 or not path2:
        return None
    
    # LCA is the last common node in both paths
    lca = None
    for a, b in zip(path1, path2):
        if a == b:
            lca = a
        else:
            break
    
    return lca

def find_path(root, target):
    """Find path from root to target node."""
    if root is None:
        return None
    
    if root.data == target:
        return [root]
    
    for child in root.children:
        path = find_path(child, target)
        if path:
            return [root] + path
    
    return None
```

### Example 3: Tree Diameter

```python
"""
Find the diameter of a tree (longest path between any two nodes).
Time: O(n²) for general tree, O(n) for binary tree
"""

def tree_diameter(root):
    """Diameter = longest path between any two leaves."""
    if not root:
        return 0
    
    # Height of each subtree
    heights = [tree_height(child) for child in root.children]
    
    # Diameter through this node: sum of two tallest subtrees + 2
    max_diameter = 0
    if len(heights) >= 2:
        sorted_heights = sorted(heights, reverse=True)
        max_diameter = sorted_heights[0] + sorted_heights[1] + 2
    
    # Diameter in subtrees
    for child in root.children:
        max_diameter = max(max_diameter, tree_diameter(child))
    
    return max_diameter
```

### Example 4: Mirror Tree

```python
"""
Check if two trees are mirror images of each other.
Time: O(n), Space: O(h)
"""

def are_mirrors(root1, root2):
    if not root1 and not root2:
        return True
    if not root1 or not root2:
        return False
    if root1.data != root2.data:
        return False
    
    # Children of root1 reversed should match children of root2
    if len(root1.children) != len(root2.children):
        return False
    
    for c1, c2 in zip(root1.children, reversed(root2.children)):
        if not are_mirrors(c1, c2):
            return False
    
    return True
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting Base Case in Recursion
```python
# WRONG: Infinite recursion
def tree_height(node):
    return 1 + max(tree_height(child) for child in node.children)

# RIGHT: Handle None and leaves
def tree_height(node):
    if not node:
        return -1
    if not node.children:
        return 0
    return 1 + max(tree_height(child) for child in node.children)
```

### Mistake 2: Confusing Height and Depth
```python
# Height: longest path from node DOWN to a leaf
# Depth: distance from root DOWN to this node

# Height of root = 3 (in our example tree)
# Depth of node G = 3
# Height of node B = 2
# Depth of node B = 1
```

### Mistake 3: Not Handling Empty Trees
```python
# WRONG: Crashes on empty tree
def traverse(root):
    result = [root.data]  # AttributeError if root is None
    ...

# RIGHT: Always check
def traverse(root):
    if not root:
        return []
    ...
```

---

## Best Practices

1. **Think recursively** — most tree problems have elegant recursive solutions
2. **Draw the tree** before solving — visualization helps enormously
3. **Always handle base cases** — None nodes and leaf nodes
4. **Choose the right traversal** — pre/post/level-order depending on the problem
5. **For iterative DFS**, use an explicit stack
6. **For BFS**, use a queue
7. **Understand the trade-off** — recursion is clean but uses stack space; iterative is more complex but O(1) extra space

---

## Practice Exercises

### Exercise 1: Count Nodes at Each Level
```python
def nodes_at_levels(root):
    """
    Return a list where index i contains the number of nodes at depth i.
    """
    # Your solution here — use BFS
    pass
```

### Exercise 2: Tree to Linked List
```python
def flatten_tree(root):
    """
    Flatten a tree to a linked list following preorder traversal.
    """
    # Your solution here
    pass
```

### Exercise 3: Maximum Width of Tree
```python
def max_width(root):
    """
    Find the maximum number of nodes at any level.
    """
    # Your solution here — use BFS
    pass
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Tree** | Hierarchical structure with root and children |
| **Root** | Topmost node (no parent) |
| **Leaf** | Node with no children |
| **Height** | Longest path from node to leaf |
| **Depth** | Distance from root to node |
| **DFS** | Preorder, inorder, postorder — uses recursion/stack |
| **BFS** | Level-order — uses queue |

**Key Insight:** Trees naturally represent hierarchical data (file systems, DOM, organizational charts). Understanding tree traversals unlocks solutions for most tree problems.

**Next Lecture:** Binary Trees — the most common tree type with at most two children per node.
