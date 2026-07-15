# Lecture 08: Binary Trees

## Topic Overview

A **binary tree** is a tree data structure where each node has at most two children, referred to as the **left child** and the **right child**. Binary trees are the most commonly used tree type and form the basis for BSTs, heaps, and many other structures.

This lecture covers binary tree implementation, traversals (iterative and recursive), and classic binary tree problems.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Implement** a binary tree with insert, delete, and search operations
2. **Perform** all four traversals (preorder, inorder, postorder, level-order)
3. **Implement** traversals both iteratively and recursively
4. **Solve** classic problems: max depth, path sum, invert tree, serialize
5. **Understand** complete, full, and perfect binary trees
6. **Apply** DFS and BFS patterns to binary tree problems

---

## Key Concepts

### 1. Binary Tree Node

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left    # Left child
        self.right = right  # Right child
    
    def __repr__(self):
        return f"TreeNode({self.val})"

# Build example tree:
#        1
#       / \
#      2   3
#     / \   \
#    4   5   6

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.right = TreeNode(6)
```

### 2. Types of Binary Trees

```
Full Binary Tree:        Complete Binary Tree:     Perfect Binary Tree:
Every node has 0 or 2    All levels full except    All levels completely
children                 last, filled left-to-right filled

      1                       1                       1
     / \                     / \                     / \
    2   3                   2   3                   2   3
   /   / \                 / \                     / \ / \
  4   5   6               4   5                   4  5 6  7
```

### 3. Four Traversals

```python
# ============= RECURSIVE TRAVERSALS =============

def preorder_recursive(root):
    """Root → Left → Right"""
    if not root:
        return []
    return [root.val] + preorder_recursive(root.left) + preorder_recursive(root.right)

def inorder_recursive(root):
    """Left → Root → Right"""
    if not root:
        return []
    return inorder_recursive(root.left) + [root.val] + inorder_recursive(root.right)

def postorder_recursive(root):
    """Left → Right → Root"""
    if not root:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.val]

# ============= ITERATIVE TRAVERSALS =============

def preorder_iterative(root):
    """Using a stack — O(n) time, O(n) space."""
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Push right first so left is processed first (LIFO)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result

def inorder_iterative(root):
    """Using a stack — O(n) time, O(n) space."""
    result = []
    stack = []
    current = root
    
    while current or stack:
        # Go as far left as possible
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        result.append(current.val)
        
        # Visit right subtree
        current = current.right
    
    return result

def postorder_iterative(root):
    """Two-stack approach — O(n) time, O(n) space."""
    if not root:
        return []
    
    stack1 = [root]
    stack2 = []
    
    while stack1:
        node = stack1.pop()
        stack2.append(node.val)
        
        if node.left:
            stack1.append(node.left)
        if node.right:
            stack1.append(node.right)
    
    return stack2[::-1]  # Reverse for postorder

def level_order(root):
    """BFS using a queue — O(n) time, O(n) space."""
    if not root:
        return []
    
    from collections import deque
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

### 4. Core Binary Tree Properties

```python
def max_depth(root):
    """Maximum depth of the tree. O(n)."""
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def min_depth(root):
    """Minimum depth (shortest root-to-leaf path). O(n)."""
    if not root:
        return 0
    if not root.left:
        return 1 + min_depth(root.right)
    if not root.right:
        return 1 + min_depth(root.left)
    return 1 + min(min_depth(root.left), min_depth(root.right))

def is_balanced(root):
    """Check if tree is height-balanced. O(n)."""
    def check(node):
        if not node:
            return 0
        left = check(node.left)
        right = check(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)
    
    return check(root) != -1

def count_nodes(root):
    """Count total nodes. O(n)."""
    if not root:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)

def is_same_tree(p, q):
    """Check if two trees are identical. O(n)."""
    if not p and not q:
        return True
    if not p or not q:
        return False
    return (p.val == q.val and 
            is_same_tree(p.left, q.left) and 
            is_same_tree(p.right, q.right))
```

---

## Complete Code Examples

### Example 1: Invert (Mirror) Binary Tree

```python
"""
Invert a binary tree (mirror it).
Time: O(n), Space: O(h)
"""

def invert_tree(root):
    if not root:
        return None
    
    # Swap left and right
    root.left, root.right = root.right, root.left
    
    # Recursively invert subtrees
    invert_tree(root.left)
    invert_tree(root.right)
    
    return root
```

### Example 2: Path Sum

```python
"""
Check if tree has a root-to-leaf path with given sum.
Time: O(n), Space: O(h)
"""

def has_path_sum(root, target_sum):
    if not root:
        return False
    
    # Leaf node — check if remaining sum matches
    if not root.left and not root.right:
        return root.val == target_sum
    
    # Recurse with reduced sum
    remaining = target_sum - root.val
    return (has_path_sum(root.left, remaining) or 
            has_path_sum(root.right, remaining))
```

### Example 3: Serialize and Deserialize Binary Tree

```python
"""
Convert binary tree to/from string representation.
Time: O(n), Space: O(n)
"""

def serialize(root):
    """Serialize tree to string using preorder."""
    if not root:
        return "null"
    
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"

def deserialize(data):
    """Deserialize string back to tree."""
    def helper(nodes):
        val = next(nodes)
        if val == "null":
            return None
        node = TreeNode(int(val))
        node.left = helper(nodes)
        node.right = helper(nodes)
        return node
    
    return helper(iter(data.split(",")))

# Test
tree_str = serialize(root)
print(tree_str)  # "1,2,4,null,null,5,null,null,3,null,6,null,null"
restored = deserialize(tree_str)
```

### Example 4: Lowest Common Ancestor (LCA)

```python
"""
Find LCA of two nodes in a binary tree.
Time: O(n), Space: O(h)
"""

def lowest_common_ancestor(root, p, q):
    if not root or root == p or root == q:
        return root
    
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    if left and right:
        return root  # p and q are in different subtrees
    
    return left if left else right
```

### Example 5: Maximum Path Sum

```python
"""
Find the maximum path sum in a binary tree (path can start and end at any node).
Time: O(n), Space: O(h)
"""

def max_path_sum(root):
    max_sum = float('-inf')
    
    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0
        
        # Get max contribution from children (ignore negative)
        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)
        
        # Path through this node as the highest point
        current_path_sum = node.val + left_gain + right_gain
        max_sum = max(max_sum, current_path_sum)
        
        # Return max contribution to parent
        return node.val + max(left_gain, right_gain)
    
    dfs(root)
    return max_sum
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting to Handle Null
```python
# WRONG: Crashes on empty tree
def max_depth(root):
    return 1 + max(max_depth(root.left), max_depth(root.right))

# RIGHT: Check for None first
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

### Mistake 2: Incorrect Traversal Order
```python
# For preorder iterative, push RIGHT first:
# This ensures LEFT is processed first (stack is LIFO)
stack.append(node.right)  # Push right first
stack.append(node.left)   # Then left — popped first!
```

### Mistake 3: Confusing BST Property
```python
# In a general binary tree, left < root < right is NOT guaranteed
# Only in Binary Search Trees!
# Don't assume order unless it's specifically a BST
```

---

## Best Practices

1. **Draw the tree** on paper before coding
2. **Start with recursive solution** — convert to iterative if needed
3. **Use a helper function** for recursion with extra parameters
4. **For iterative traversals**, think about the stack/queue state at each step
5. **Handle edge cases:** empty tree, single node, skewed tree
6. **Understand the return value** — what should the function return?

---

## Practice Exercises

### Exercise 1: Right Side View
```python
def right_side_view(root):
    """
    Return values of nodes visible from the right side.
    Input: [1,2,3,null,5,null,4]
    Output: [1,3,4]
    """
    # Your solution here — BFS, take last node at each level
    pass
```

### Exercise 2: Binary Tree Zigzag Level Order
```python
def zigzag_level_order(root):
    """
    Return zigzag level order traversal.
    Level 0: left to right
    Level 1: right to left
    Level 2: left to right
    """
    # Your solution here
    pass
```

### Exercise 3: Construct Binary Tree from Preorder and Inorder
```python
def build_tree(preorder, inorder):
    """
    Construct binary tree from preorder and inorder traversals.
    preorder = [3,9,20,15,7]
    inorder = [9,3,15,20,7]
    """
    # Your solution here — O(n) using hash map
    pass
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Binary Tree** | Each node has at most 2 children |
| **Preorder** | Root → Left → Right (top-down) |
| **Inorder** | Left → Root → Right (sorted for BST) |
| **Postorder** | Left → Right → Root (bottom-up) |
| **Level-order** | BFS with queue (level by level) |
| **Recursive DFS** | Clean but uses call stack O(h) |
| **Iterative DFS** | Uses explicit stack, same complexity |

**Key Insight:** Most binary tree problems can be solved with a simple recursive pattern: process the current node, then recursively solve for left and right subtrees.

**Next Lecture:** Binary Search Trees — ordered binary trees enabling O(log n) operations.
