# Glossary: Trees — General Concepts

> Quick reference for all terms introduced in Lecture 07.

---

## B

### Balanced Tree
- **Definition:** A tree where the height difference between left and right subtrees is at most 1 (for AVL) or logarithmic height is maintained.
- **Related:** AVL Tree, Height-Balanced, Unbalanced

```python
# Balanced:          Unbalanced:
#     3                  1
#    / \                  \
#   1   4                  2
#  /                        \
# 0                          3
```

### BFS (Breadth-First Search)
- **Definition:** A traversal method that visits nodes level by level, left to right, using a queue.
- **Also Known As:** Level-order traversal.
- **Time:** O(n), **Space:** O(w) where w = max width.
- **Related:** DFS, Level-Order, Queue

```python
from collections import deque

def bfs(root):
    if not root:
        return []
    queue = deque([root])
    result = []
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left: queue.append(node.left)
        if node.right: queue.append(node.right)
    return result
```

### Binary Tree
- **Definition:** A tree where each node has at most two children (left and right).
- **Related:** Tree, Binary Search Tree, Complete Binary Tree

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

## D

### Degree (of a Node)
- **Definition:** The number of children a node has.
- **Example:** A leaf has degree 0; a root with 3 children has degree 3.
- **Related:** Node, Leaf, Internal Node

### DFS (Depth-First Search)
- **Definition:** A traversal method that explores as far as possible along each branch before backtracking.
- **Variants:** Preorder, inorder, postorder.
- **Uses:** Stack (explicit or recursive call stack).
- **Related:** BFS, Preorder, Inorder, Postorder

```python
def dfs(node):
    if not node:
        return
    print(node.val)    # Preorder: process first
    dfs(node.left)
    dfs(node.right)
```

### Depth (of a Node)
- **Definition:** The number of edges from the root to that node.
- **Root depth:** 0.
- **Related:** Height, Level

---

## H

### Height (of a Tree)
- **Definition:** The number of edges on the longest path from the root to a leaf.
- **Height of a single node:** 0 (or 1 by some conventions).
- **Related:** Depth, Diameter, Balanced

```python
def height(node):
    if not node:
        return -1
    if not node.left and not node.right:
        return 0
    return 1 + max(height(node.left), height(node.right))
```

### Height-Balanced Tree
- **Definition:** A tree where the height difference between left and right subtrees of every node is at most 1.
- **Related:** AVL Tree, Balanced Tree

---

## I

### Inorder Traversal
- **Definition:** Visiting nodes in order: Left → Root → Right.
- **For BST:** Returns elements in sorted order.
- **Related:** Preorder, Postorder

```python
def inorder(node):
    if not node:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)
```

### Internal Node
- **Definition:** Any node that has at least one child (not a leaf).
- **Related:** Leaf, Root, Degree

---

## L

### Leaf (Leaf Node)
- **Definition:** A node with no children (degree 0).
- **Also Known As:** Terminal node.
- **Related:** Internal Node, Degree

---

## N

### N-ary Tree
- **Definition:** A tree where each node can have up to N children.
- **Example:** A binary tree is a 2-ary tree.
- **Related:** Binary Tree, General Tree

```python
class NaryNode:
    def __init__(self, val=None):
        self.val = val
        self.children = []
```

### Node
- **Definition:** The basic building block of a tree, containing data and references to child nodes.
- **Related:** Root, Leaf, Parent, Child

---

## P

### Parent
- **Definition:** The node directly above a given node in the tree (connected by an edge).
- **Related:** Child, Root, Sibling

### Postorder Traversal
- **Definition:** Visiting nodes in order: Left → Right → Root.
- **Use Case:** Deleting a tree (children before parent), postfix expression evaluation.
- **Related:** Preorder, Inorder

```python
def postorder(node):
    if not node:
        return []
    return postorder(node.left) + postorder(node.right) + [node.val]
```

### Preorder Traversal
- **Definition:** Visiting nodes in order: Root → Left → Right.
- **Use Case:** Copying/serializing a tree, prefix expression evaluation.
- **Related:** Inorder, Postorder

```python
def preorder(node):
    if not node:
        return []
    return [node.val] + preorder(node.left) + preorder(node.right)
```

---

## R

### Root
- **Definition:** The topmost node of a tree — the only node with no parent.
- **Related:** Leaf, Depth, Height

---

## S

### Subtree
- **Definition:** A tree consisting of a node and all its descendants.
- **Example:** In a binary tree, each node's left and right children define subtrees.
- **Related:** Tree, Node, Recursive Structure

---

## T

### Tree
- **Definition:** A hierarchical data structure consisting of nodes connected by edges, with a single root and no cycles.
- **Properties:** Connected, acyclic, n nodes have n-1 edges.
- **Related:** Graph, Binary Tree, Root

### Traversal
- **Definition:** The process of visiting each node in a tree exactly once.
- **Types:** Preorder, inorder, postorder (DFS), level-order (BFS).
- **Related:** DFS, BFS, Visit Order

---

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Root | Topmost node (no parent) | A in [A→B,C] |
| Leaf | Node with no children | D, E, F, G |
| Height | Longest root-to-leaf path | 3 (for our example) |
| Depth | Distance from root to node | B has depth 1 |
| Degree | Number of children | A has degree 2 |
| Preorder | Root → Left → Right | Top-down |
| Inorder | Left → Root → Right | Sorted for BST |
| Postorder | Left → Right → Root | Bottom-up |
| Level-order | Level by level | BFS with queue |

| Traversal | Order | Use Case | Algorithm |
|-----------|-------|----------|-----------|
| Preorder | Root, Left, Right | Copy tree, prefix expr | DFS (stack) |
| Inorder | Left, Root, Right | Sorted output (BST) | DFS (stack) |
| Postorder | Left, Right, Root | Delete tree, postfix expr | DFS (stack) |
| Level-order | Level by level | BFS, shortest path | Queue |

| Property | Formula |
|----------|---------|
| Max nodes at depth d | 2^d (binary tree) |
| Min height for n nodes | ⌊log₂(n)⌋ |
| Max height for n nodes | n - 1 (skewed tree) |
| Edges in tree | n - 1 |
| Height of empty tree | -1 (or 0) |
