# Glossary: Binary Trees

> Quick reference for all terms introduced in Lecture 08.

---

## B

### Balanced Binary Tree
- **Definition:** A binary tree where the height difference between left and right subtrees of every node is at most 1.
- **Related:** AVL Tree, Height, Unbalanced

```python
def is_balanced(root):
    def check(node):
        if not node:
            return 0
        left = check(node.left)
        right = check(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)
    return check(root) != -1
```

### Binary Tree
- **Definition:** A tree where each node has at most two children (left and right).
- **Related:** Tree, Binary Search Tree, Complete Binary Tree

---

## C

### Complete Binary Tree
- **Definition:** A binary tree where all levels are completely filled except possibly the last, which is filled from left to right.
- **Related:** Perfect Binary Tree, Heap

```
Complete:           NOT Complete:
      1                   1
     / \                 / \
    2   3               2   3
   / \                 /   /
  4   5               4   6
```

### Construct (from traversals)
- **Definition:** Building a binary tree from two traversal sequences (typically preorder+inorder or postorder+inorder).
- **Related:** Preorder, Inorder, Tree Construction

---

## D

### DFS (Depth-First Search)
- **Definition:** Traversal that explores deep into each branch before backtracking.
- **Variants:** Preorder, inorder, postorder.
- **Uses:** Stack (explicit or recursive call stack).
- **Related:** BFS, Traversal

---

## F

### Full Binary Tree
- **Definition:** A binary tree where every node has either 0 or 2 children (no node has exactly 1 child).
- **Related:** Complete Binary Tree, Perfect Binary Tree

```
Full Binary Tree:
      1
     / \
    2   3
   / \
  4   5
(No node has only 1 child)
```

---

## H

### Height (of Binary Tree)
- **Definition:** The number of edges on the longest path from root to leaf.
- **Time to compute:** O(n)
- **Related:** Depth, Diameter

```python
def height(root):
    if not root:
        return -1
    return 1 + max(height(root.left), height(root.right))
```

---

## I

### Inorder Traversal
- **Definition:** Left → Root → Right
- **For BST:** Returns elements in sorted (ascending) order.
- **Related:** Preorder, Postorder

```python
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# For BST, this gives sorted output!
```

### Invert (Mirror) Tree
- **Definition:** Flipping a binary tree so left and right children are swapped at every node.
- **Related:** Symmetric Tree, Mirror

```python
def invert(root):
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invert(root.left)
    invert(root.right)
    return root
```

---

## L

### Leaf Node
- **Definition:** A node with no children (both left and right are None).
- **Related:** Internal Node, Degree

```python
def is_leaf(node):
    return node and not node.left and not node.right
```

### Level-Order Traversal
- **Definition:** Visiting nodes level by level, left to right (BFS).
- **Uses:** Queue.
- **Related:** BFS, DFS

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

### Lowest Common Ancestor (LCA)
- **Definition:** The deepest node that is an ancestor of both given nodes.
- **Related:** Ancestor, Descendant, Binary Tree

```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root
    return left or right
```

---

## M

### Maximum Depth
- **Definition:** The number of nodes on the longest path from root to a leaf.
- **Related:** Height, Minimum Depth

```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

### Mirror Tree
- **Definition:** See Invert Tree. A tree that is a mirror image of another.
- **Related:** Symmetric Tree

---

## N

### Node
- **Definition:** A basic element of a binary tree containing a value and references to left and right children.
- **Related:** TreeNode, Left Child, Right Child

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

## P

### Path Sum
- **Definition:** Checking if a root-to-leaf path exists with a given sum.
- **Related:** DFS, Recursion

```python
def has_path_sum(root, target):
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target
    return (has_path_sum(root.left, target - root.val) or
            has_path_sum(root.right, target - root.val))
```

### Perfect Binary Tree
- **Definition:** A binary tree where all interior nodes have two children and all leaves are at the same level.
- **Properties:** n nodes, height h, total nodes = 2^(h+1) - 1.
- **Related:** Complete Binary Tree, Full Binary Tree

```
Perfect Binary Tree:
      1
     / \
    2   3
   / \ / \
  4  5 6  7
```

### Postorder Traversal
- **Definition:** Left → Right → Root
- **Use Case:** Deleting tree, evaluating postfix expressions.
- **Related:** Preorder, Inorder

```python
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]
```

### Preorder Traversal
- **Definition:** Root → Left → Right
- **Use Case:** Copying tree, prefix expression, serialization.
- **Related:** Inorder, Postorder

```python
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)
```

---

## S

### Serialize / Deserialize
- **Definition:** Converting a tree to a string (serialize) and back (deserialize).
- **Related:** Preorder, Tree Construction

```python
def serialize(root):
    if not root:
        return "null"
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"
```

### Symmetric Tree
- **Definition:** A tree that is a mirror of itself (left subtree is mirror of right subtree).
- **Related:** Mirror, Invert Tree

```python
def is_symmetric(root):
    def mirror(a, b):
        if not a and not b:
            return True
        if not a or not b:
            return False
        return (a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left))
    return mirror(root.left, root.right) if root else True
```

---

## Quick Reference Table

| Traversal | Order | Use Case | Stack/Queue |
|-----------|-------|----------|------------|
| Preorder | Root → Left → Right | Copy/serialize tree | Stack |
| Inorder | Left → Root → Right | Sorted output (BST) | Stack |
| Postorder | Left → Right → Root | Delete tree, evaluate | Stack |
| Level-order | Level by level | BFS | Queue |

| Tree Type | Property | Nodes at Height h |
|-----------|----------|-------------------|
| Full | 0 or 2 children per node | Varies |
| Complete | All levels full except last, filled L→R | Varies |
| Perfect | All levels completely full | 2^(h+1) - 1 |
| Balanced | Height diff ≤ 1 for all nodes | ~2^h |

| Operation | Time | Space |
|-----------|------|-------|
| Traverse all | O(n) | O(h) recursive, O(w) BFS |
| Search (unsorted) | O(n) | O(h) |
| Insert | O(h) | O(h) |
| Delete | O(h) | O(h) |
| Height | O(n) | O(h) |
| Count nodes | O(n) | O(h) |
