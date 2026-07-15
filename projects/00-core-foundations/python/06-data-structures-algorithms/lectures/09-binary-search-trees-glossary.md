# Glossary: Binary Search Trees

> Quick reference for all terms introduced in Lecture 09.

---

## B

### BST (Binary Search Tree)
- **Definition:** A binary tree where for every node, all values in the left subtree are less and all values in the right subtree are greater.
- **Property:** Inorder traversal yields sorted order.
- **Time:** O(log n) average, O(n) worst.
- **Related:** Binary Tree, AVL Tree, Balanced Tree

```python
class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
```

### BST Property
- **Definition:** For any node N: all left subtree values < N.val < all right subtree values.
- **Related:** Inorder Traversal, Sorted Order

---

## D

### Degenerate Tree
- **Definition:** A BST where each node has only one child, effectively becoming a linked list.
- **Cause:** Inserting already-sorted data into a BST.
- **Performance:** O(n) for all operations (worst case).
- **Related:** Balanced Tree, Skewed Tree

```
Degenerate BST (sorted insertion: 1,2,3,4,5):
1
 \
  2
   \
    3
     \
      4
       \
        5
```

---

## F

### Floor and Ceiling
- **Definition:** Floor = largest value ≤ target; Ceiling = smallest value ≥ target in the BST.
- **Time:** O(h)
- **Related:** Search, Range Query

```python
def floor(node, target):
    """Find largest value ≤ target."""
    if not node:
        return None
    if node.val == target:
        return node.val
    if node.val > target:
        return floor(node.left, target)
    right_floor = floor(node.right, target)
    return right_floor if right_floor else node.val
```

---

## I

### Inorder Successor
- **Definition:** The node with the next largest value after a given node in BST.
- **Time:** O(h)
- **Related:** Inorder Predecessor, BST Property

```python
def inorder_successor(root, p):
    successor = None
    while root:
        if p.val < root.val:
            successor = root
            root = root.left
        else:
            root = root.right
    return successor
```

### Inorder Traversal (BST)
- **Definition:** Visiting nodes in Left → Root → Right order. For a BST, this yields sorted order.
- **Related:** BST Property, Sorted Order

```python
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)
```

---

## K

### Kth Smallest / Largest
- **Definition:** Finding the kth element in sorted order using BST traversal.
- **Time:** O(h + k) using inorder traversal with counter.
- **Related:** Inorder, Rank

```python
def kth_smallest(root, k):
    count = 0
    result = None
    
    def inorder(node):
        nonlocal count, result
        if not node or count >= k:
            return
        inorder(node.left)
        count += 1
        if count == k:
            result = node.val
            return
        inorder(node.right)
    
    inorder(root)
    return result
```

---

## L

### Lowest Common Ancestor (BST)
- **Definition:** The deepest node that is an ancestor of both p and q in a BST. Simpler than general tree LCA — use BST ordering.
- **Time:** O(h)
- **Related:** LCA, BST Property

```python
def lca_bst(root, p, q):
    if p.val < root.val and q.val < root.val:
        return lca_bst(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lca_bst(root.right, p, q)
    return root
```

---

## R

### Range Query
- **Definition:** Finding all nodes (or their sum/count) within a value range [low, high].
- **Time:** O(k + log n) where k = number of results.
- **Pruning:** Skip subtrees that are entirely outside the range.
- **Related:** BST Property, Pruning

```python
def range_query(root, low, high):
    if not root:
        return []
    if root.val > high:
        return range_query(root.left, low, high)  # Prune right
    if root.val < low:
        return range_query(root.right, low, high)  # Prune left
    return (range_query(root.left, low, high) + 
            [root.val] + 
            range_query(root.right, low, high))
```

---

## S

### Search (BST)
- **Definition:** Finding a value in BST by comparing with current node and going left/right.
- **Time:** O(log n) average, O(n) worst.
- **Related:** Insert, Delete, BST Property

```python
def search(root, val):
    if not root:
        return False
    if val == root.val:
        return True
    elif val < root.val:
        return search(root.left, val)
    else:
        return search(root.right, val)
```

### Sorted Array to BST
- **Definition:** Converting a sorted array to a height-balanced BST using the middle element as root.
- **Time:** O(n)
- **Related:** Balanced BST, Array to Tree

```python
def sorted_array_to_bst(nums):
    if not nums:
        return None
    mid = len(nums) // 2
    root = BSTNode(nums[mid])
    root.left = sorted_array_to_bst(nums[:mid])
    root.right = sorted_array_to_bst(nums[mid+1:])
    return root
```

### Successor
- **Definition:** See Inorder Successor. The next larger node.
- **Related:** Predecessor, Inorder

---

## T

### Two Sum in BST
- **Definition:** Finding two nodes whose values sum to a target.
- **Approach:** Use a set during inorder traversal, or two-pointer on sorted inorder list.
- **Time:** O(n), **Space:** O(n)
- **Related:** Two Sum, Inorder

```python
def find_target(root, k):
    seen = set()
    
    def dfs(node):
        if not node:
            return False
        if k - node.val in seen:
            return True
        seen.add(node.val)
        return dfs(node.left) or dfs(node.right)
    
    return dfs(root)
```

---

## V

### Validate BST
- **Definition:** Checking if a binary tree satisfies the BST property at every node.
- **Method:** Pass min/max constraints down during recursion.
- **Time:** O(n), **Space:** O(h)
- **Related:** BST Property, Range Constraints

```python
def is_valid_bst(root, low=float('-inf'), high=float('inf')):
    if not root:
        return True
    if root.val <= low or root.val >= high:
        return False
    return (is_valid_bst(root.left, low, root.val) and
            is_valid_bst(root.right, root.val, high))
```

---

## Quick Reference Table

| Operation | Average | Worst | Note |
|-----------|---------|-------|------|
| Search | O(log n) | O(n) | Degenerate tree |
| Insert | O(log n) | O(n) | Same as search |
| Delete | O(log n) | O(n) | Find successor |
| Find min | O(log n) | O(n) | Go left |
| Find max | O(log n) | O(n) | Go right |
| Inorder | O(n) | O(n) | Sorted output |
| Kth smallest | O(h + k) | O(n + k) | Inorder with counter |
| Range query | O(k + log n) | O(n) | With pruning |
| Validate | O(n) | O(n) | Check all nodes |
| LCA | O(h) | O(n) | Use BST property |

| BST vs Array vs Hash Table | BST | Sorted Array | Hash Table |
|---------------------------|-----|-------------|-----------|
| Search | O(log n) | O(log n) | O(1) avg |
| Insert | O(log n) | O(n) | O(1) avg |
| Delete | O(log n) | O(n) | O(1) avg |
| Sorted order | O(n) | Already sorted | Not sorted |
| Range query | O(k + log n) | O(log n + k) | O(n) |
| Space | O(n) | O(n) | O(n) |
