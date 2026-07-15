# Lecture 09: Binary Search Trees (BST)

## Topic Overview

A **Binary Search Tree (BST)** is a binary tree with an ordering property: for every node, all values in its left subtree are less than the node's value, and all values in its right subtree are greater. This property enables efficient searching, insertion, and deletion.

**Key property:** Inorder traversal of a BST yields elements in sorted order.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Implement** a BST with insert, search, and delete operations
2. **Explain** the BST property and why it enables O(log n) operations
3. **Perform** range queries and find kth smallest/largest elements
4. **Understand** the problem of unbalanced BSTs (degenerate trees)
5. **Solve** BST validation and conversion problems
6. **Compare** BST with sorted arrays and hash tables

---

## Key Concepts

### 1. BST Property

```
BST Property: For every node N:
  - All nodes in N's LEFT subtree have values < N.val
  - All nodes in N's RIGHT subtree have values > N.val

Example BST:
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13

Inorder traversal: 1, 3, 4, 6, 7, 8, 10, 13, 14 (sorted!)
```

### 2. BST Implementation

```python
class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        """Insert a value. O(h) time, O(h) space (recursive)."""
        self.root = self._insert(self.root, val)
    
    def _insert(self, node, val):
        if not node:
            return BSTNode(val)
        
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        # Duplicate values are ignored
        
        return node
    
    def search(self, val):
        """Search for a value. O(h) time."""
        return self._search(self.root, val)
    
    def _search(self, node, val):
        if not node:
            return False
        
        if val == node.val:
            return True
        elif val < node.val:
            return self._search(node.left, val)
        else:
            return self._search(node.right, val)
    
    def delete(self, val):
        """Delete a value. O(h) time."""
        self.root = self._delete(self.root, val)
    
    def _delete(self, node, val):
        if not node:
            return None
        
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # Found the node to delete
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
                # Find inorder successor (smallest in right subtree)
                successor = self._find_min(node.right)
                node.val = successor.val
                node.right = self._delete(node.right, successor.val)
        
        return node
    
    def _find_min(self, node):
        """Find the minimum value node in subtree."""
        while node.left:
            node = node.left
        return node
    
    def _find_max(self, node):
        """Find the maximum value node in subtree."""
        while node.right:
            node = node.right
        return node
    
    def inorder(self):
        """Return sorted list of values."""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)
    
    def kth_smallest(self, k):
        """Find kth smallest element. O(h + k)"""
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
            self.result = node.val
            return
        self._kth_smallest(node.right, k)
```

### 3. BST Operations Complexity

| Operation | Average | Worst (unbalanced) |
|-----------|---------|-------------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Inorder traversal | O(n) | O(n) |
| Find min/max | O(log n) | O(n) |

**Worst case O(n)** occurs when BST degenerates into a linked list:
```
Degenerate BST (essentially a linked list):
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

## Complete Code Examples

### Example 1: Validate BST

```python
"""
Check if a binary tree is a valid BST.
Time: O(n), Space: O(h)
"""

def is_valid_bst(root):
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node:
            return True
        if node.val <= low or node.val >= high:
            return False
        return (validate(node.left, low, node.val) and 
                validate(node.right, node.val, high))
    
    return validate(root)
```

### Example 2: Range Sum of BST

```python
"""
Sum all nodes with values between low and high (inclusive).
Time: O(n), Space: O(h)
"""

def range_sum_bst(root, low, high):
    if not root:
        return 0
    
    # Prune: if current value > high, only check left
    if root.val > high:
        return range_sum_bst(root.left, low, high)
    
    # Prune: if current value < low, only check right
    if root.val < low:
        return range_sum_bst(root.right, low, high)
    
    # Current node is in range, check both subtrees
    return (root.val + 
            range_sum_bst(root.left, low, high) + 
            range_sum_bst(root.right, low, high))
```

### Example 3: Lowest Common Ancestor in BST

```python
"""
LCA in BST is simpler than in a general binary tree.
Use BST property to navigate.
Time: O(h), Space: O(h)
"""

def lca_bst(root, p, q):
    # Both in left subtree
    if p.val < root.val and q.val < root.val:
        return lca_bst(root.left, p, q)
    
    # Both in right subtree
    if p.val > root.val and q.val > root.val:
        return lca_bst(root.right, p, q)
    
    # Split point — this is the LCA
    return root
```

### Example 4: Kth Largest Element

```python
"""
Find kth largest element in BST.
Use reverse inorder traversal (Right → Root → Left).
Time: O(h + k), Space: O(h)
"""

def kth_largest(root, k):
    count = 0
    result = None
    
    def reverse_inorder(node):
        nonlocal count, result
        if not node or count >= k:
            return
        
        reverse_inorder(node.right)  # Visit largest first
        count += 1
        if count == k:
            result = node.val
            return
        reverse_inorder(node.left)
    
    reverse_inorder(root)
    return result
```

### Example 5: BST from Sorted Array

```python
"""
Convert sorted array to height-balanced BST.
Time: O(n), Space: O(n)
"""

def sorted_array_to_bst(nums):
    if not nums:
        return None
    
    mid = len(nums) // 2
    root = BSTNode(nums[mid])
    root.left = sorted_array_to_bst(nums[:mid])
    root.right = sorted_array_to_bst(nums[mid + 1:])
    
    return root

# This creates a balanced BST — height = log(n)
```

### Example 6: Inorder Successor

```python
"""
Find the inorder successor of a given node in BST.
The successor is the node with the next largest value.
Time: O(h), Space: O(1) iterative
"""

def inorder_successor(root, p):
    successor = None
    
    while root:
        if p.val < root.val:
            successor = root  # Candidate
            root = root.left  # Go left for smaller
        else:
            root = root.right  # Go right for larger
    
    return successor
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Validating BST Correctly
```python
# WRONG: Only checking immediate children
def is_valid_bst_wrong(root):
    if not root:
        return True
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False
    return is_valid_bst_wrong(root.left) and is_valid_bst_wrong(root.right)

# This misses: left subtree's right child could be > root!

# RIGHT: Pass range constraints
def is_valid_bst(root, low=float('-inf'), high=float('inf')):
    if not root:
        return True
    if root.val <= low or root.val >= high:
        return False
    return (is_valid_bst(root.left, low, root.val) and
            is_valid_bst(root.right, root.val, high))
```

### Mistake 2: Confusing BST with Binary Tree
```python
# In a BST: left < root < right (ALWAYS)
# In a general binary tree: no ordering guaranteed
# Don't assume BST property unless explicitly stated!
```

### Mistake 3: Deleting Node with Two Children Incorrectly
```python
# WRONG: Just removing the node
# RIGHT: Replace with inorder successor (or predecessor),
# then delete the successor/predecessor
```

---

## Best Practices

1. **Always validate BST** property if the problem doesn't guarantee it
2. **Use BST property** to prune search space (don't visit unnecessary subtrees)
3. **For balanced BST needs**, consider using a self-balancing tree (AVL, Red-Black)
4. **Inorder traversal** gives sorted order — use it for range queries
5. **For kth element**, use inorder with counter
6. **For LCA in BST**, use the ordering property — much simpler than general tree LCA

---

## Practice Exercises

### Exercise 1: Two Sum IV — Input BST
```python
def find_target(root, k):
    """
    Check if BST has two elements that sum to k.
    Time: O(n), Space: O(n) using a set
    """
    # Your solution here
    pass
```

### Exercise 2: Convert BST to Greater Tree
```python
def convert_bst(root):
    """
    Convert BST to greater tree where each node's value is
    replaced by the sum of all values >= it.
    """
    # Your solution here — reverse inorder traversal
    pass
```

### Exercise 3: Recover BST
```python
def recover_tree(root):
    """
    Two nodes in BST were swapped. Find and fix them.
    Time: O(n), Space: O(h)
    """
    # Your solution here — use inorder to find violations
    pass
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **BST Property** | left < root < right |
| **Search** | O(log n) average, O(n) worst |
| **Inorder** | Returns sorted order |
| **Delete 2 children** | Replace with inorder successor |
| **Validate BST** | Pass min/max constraints |
| **Degenerate tree** | BST becomes linked list → O(n) |
| **Balanced BST** | Always O(log n) — see AVL trees |

**Key Insight:** BSTs combine the advantages of arrays (sorted order) and linked lists (dynamic size). The key weakness is that without balancing, performance degrades to O(n).

**Next Lecture:** AVL Trees — self-balancing BSTs that guarantee O(log n) for all operations.
