# Lecture 10: AVL Trees

## Topic Overview

An **AVL tree** (Adelson-Velsky and Landis tree) is a self-balancing binary search tree where the height difference between left and right subtrees of any node is at most 1. After every insertion or deletion, the tree performs **rotations** to maintain balance, guaranteeing O(log n) time for all operations.

AVL trees solve the degenerate BST problem where operations degrade to O(n).

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** the balance factor and AVL property
2. **Perform** the four rotation types (LL, RR, LR, RL)
3. **Implement** an AVL tree with insert and delete
4. **Understand** why AVL trees guarantee O(log n) operations
5. **Compare** AVL trees with regular BSTs and Red-Black trees
6. **Analyze** rotations and their impact on performance

---

## Key Concepts

### 1. Balance Factor

```
Balance Factor = Height(Left Subtree) - Height(Right Subtree)

AVL Property: For every node, -1 ≤ balance_factor ≤ 1

Balance Factors:
  -1, 0, +1  →  Balanced (OK)
  -2 or +2    →  Unbalanced (needs rotation)

Example:
        30 (BF=+1)         30 (BF=+2) ← UNBALANCED!
       / \                 / \
    (20)  40             (10)  40
    / \                    \
   10  25                  20
                            \
                            25
```

### 2. The Four Rotation Cases

#### Case 1: Left-Left (LL) — Right Rotation
```
Before:          After:
    z (BF=+2)       y (BF=0)
   / \             / \
  y   T4          x   z
 / \             / \ / \
x   T3          T1 T2 T3 T4
/ \
T1 T2

Right rotate around z
```

#### Case 2: Right-Right (RR) — Left Rotation
```
Before:          After:
  z (BF=-2)         y (BF=0)
 / \               / \
T1   y            z   x
    / \           / \ / \
   T2  x         T1 T2 T3 T4
      / \
     T3 T4

Left rotate around z
```

#### Case 3: Left-Right (LR) — Left then Right Rotation
```
Before:
    z (BF=+2)
   / \
  y   T4
 / \
T1   x
    / \
   T2 T3

Step 1: Left rotate y → LR case becomes LL
Step 2: Right rotate z
```

#### Case 4: Right-Left (RL) — Right then Left Rotation
```
Before:
  z (BF=-2)
 / \
T1   y
    / \
   x   T4
  / \
 T2 T3

Step 1: Right rotate y → RL case becomes RR
Step 2: Left rotate z
```

### 3. AVL Tree Implementation

```python
class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1  # Height of node (leaf = 1)

class AVLTree:
    def __init__(self):
        self.root = None
    
    def get_height(self, node):
        """Get height of node. O(1)."""
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        """Get balance factor. O(1)."""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def update_height(self, node):
        """Update height after modification. O(1)."""
        node.height = 1 + max(
            self.get_height(node.left),
            self.get_height(node.right)
        )
    
    # ============= ROTATIONS =============
    
    def right_rotate(self, z):
        """Right rotation around z. O(1)."""
        y = z.left
        T3 = y.right
        
        # Perform rotation
        y.right = z
        z.left = T3
        
        # Update heights
        self.update_height(z)
        self.update_height(y)
        
        return y  # New root of this subtree
    
    def left_rotate(self, z):
        """Left rotation around z. O(1)."""
        y = z.right
        T2 = y.left
        
        # Perform rotation
        y.left = z
        z.right = T2
        
        # Update heights
        self.update_height(z)
        self.update_height(y)
        
        return y  # New root of this subtree
    
    # ============= INSERT =============
    
    def insert(self, val):
        """Insert value and rebalance. O(log n)."""
        self.root = self._insert(self.root, val)
    
    def _insert(self, node, val):
        # Step 1: Standard BST insert
        if not node:
            return AVLNode(val)
        
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        else:
            return node  # Duplicate, no insert
        
        # Step 2: Update height
        self.update_height(node)
        
        # Step 3: Get balance factor
        balance = self.get_balance(node)
        
        # Step 4: Rebalance if needed
        
        # Left-Left case
        if balance > 1 and val < node.left.val:
            return self.right_rotate(node)
        
        # Right-Right case
        if balance < -1 and val > node.right.val:
            return self.left_rotate(node)
        
        # Left-Right case
        if balance > 1 and val > node.left.val:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        # Right-Left case
        if balance < -1 and val < node.right.val:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node
    
    # ============= DELETE =============
    
    def delete(self, val):
        """Delete value and rebalance. O(log n)."""
        self.root = self._delete(self.root, val)
    
    def _delete(self, node, val):
        # Step 1: Standard BST delete
        if not node:
            return node
        
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # Node found
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            # Two children: get inorder successor
            successor = self._get_min(node.right)
            node.val = successor.val
            node.right = self._delete(node.right, successor.val)
        
        if not node:
            return node
        
        # Step 2: Update height
        self.update_height(node)
        
        # Step 3: Get balance factor
        balance = self.get_balance(node)
        
        # Step 4: Rebalance (4 cases)
        
        # Left-Left
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        
        # Left-Right
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        # Right-Right
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        
        # Right-Left
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node
    
    def _get_min(self, node):
        """Find minimum node in subtree."""
        while node.left:
            node = node.left
        return node
    
    # ============= UTILITIES =============
    
    def search(self, val):
        """Search for value. O(log n)."""
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
    
    def is_balanced(self):
        """Check if tree is AVL-balanced."""
        return self._is_balanced(self.root)
    
    def _is_balanced(self, node):
        if not node:
            return True
        balance = self.get_balance(node)
        if abs(balance) > 1:
            return False
        return self._is_balanced(node.left) and self._is_balanced(node.right)
```

### 4. Why AVL Guarantees O(log n)

```
The Fibonacci connection:
  Height of AVL tree with n nodes ≤ 1.44 * log₂(n + 2)

Why? Minimum nodes for height h:
  N(0) = 1  (empty)
  N(1) = 1  (single node)
  N(h) = N(h-1) + N(h-2) + 1  (like Fibonacci!)

This means:
  - Even worst case is still O(log n)
  - The tree can never degenerate to a linked list
  - Rotations maintain the invariant

Example:
  n = 1,000,000 nodes
  Max height ≈ 1.44 * log₂(1,000,000) ≈ 28.7
  vs. degenerate BST: height = 999,999
```

### 5. Time Complexity

| Operation | AVL Tree | Regular BST (avg) | BST (worst) |
|-----------|----------|-------------------|-------------|
| Search | O(log n) | O(log n) | O(n) |
| Insert | O(log n) | O(log n) | O(n) |
| Delete | O(log n) | O(log n) | O(n) |
| Space | O(n) | O(n) | O(n) |

**Rotation cost:** Each rotation is O(1), and at most O(log n) rotations per operation.

---

## Complete Code Examples

### Example 1: Visualize AVL Tree

```python
def print_tree(node, level=0, prefix="Root: "):
    """Pretty print AVL tree."""
    if node is not None:
        print(" " * (level * 4) + prefix + str(node.val) + 
              f" (h={node.height}, bf={get_balance(node)})")
        if node.left is not None or node.right is not None:
            print_tree(node.left, level + 1, "L--- ")
            print_tree(node.right, level + 1, "R--- ")

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)

def get_height(node):
    if not node:
        return 0
    return node.height

# Build AVL tree
avl = AVLTree()
for val in [10, 20, 30, 40, 50, 25]:
    avl.insert(val)
    print(f"\nAfter inserting {val}:")
    print_tree(avl.root)
```

### Example 2: Kth Smallest in AVL

```python
"""
Find kth smallest element in AVL tree.
Uses enhanced nodes with subtree size.
"""

class AVLNodeWithSize:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1  # Number of nodes in subtree

def kth_smallest(root, k):
    """Find kth smallest using subtree sizes. O(log n)."""
    left_size = root.left.size if root.left else 0
    
    if k <= left_size:
        return kth_smallest(root.left, k)
    elif k == left_size + 1:
        return root.val
    else:
        return kth_smallest(root.right, k - left_size - 1)
```

### Example 3: Range Count in AVL

```python
"""
Count number of elements in range [low, high].
Uses BST property for pruning.
Time: O(log n + k) where k = number of elements in range
"""

def range_count(node, low, high):
    if not node:
        return 0
    
    if node.val < low:
        return range_count(node.right, low, high)
    if node.val > high:
        return range_count(node.left, low, high)
    
    return (1 + 
            range_count(node.left, low, high) + 
            range_count(node.right, low, high))
```

---

## Common Mistakes to Avoid

### Mistake 1: Wrong Rotation Case
```python
# WRONG: Using the same rotation for all cases
# RIGHT: Determine the case first:
#   LL → Right rotate
#   RR → Left rotate
#   LR → Left rotate child, then Right rotate
#   RL → Right rotate child, then Left rotate
```

### Mistake 2: Forgetting to Update Heights
```python
# WRONG: Rotating without updating heights
def right_rotate(z):
    y = z.left
    z.left = y.right
    y.right = z
    return y  # Heights are wrong!

# RIGHT: Update heights after rotation
def right_rotate(z):
    y = z.left
    z.left = y.right
    y.right = z
    update_height(z)  # Update z first (it's now lower)
    update_height(y)  # Then y (it's now higher)
    return y
```

### Mistake 3: Using Balance Factor Wrong
```python
# The balance factor is LEFT height - RIGHT height
# BF > 0: left-heavy
# BF < 0: right-heavy
# BF = 0: balanced

# Wrong rotation conditions will break the tree!
```

---

## Best Practices

1. **Always update heights** after any structural change
2. **Check balance factor** after insert/delete to decide rotation type
3. **Draw the tree** before and after rotations
4. **Use iterative insertion** for better space efficiency
5. **For range queries**, AVL's balance guarantees consistent performance
6. **Understand the four cases** — they cover all possible imbalances
7. **For practice**, manually trace through insertions and verify rotations

---

## Practice Exercises

### Exercise 1: AVL Tree from Array
```python
def build_avl_from_array(arr):
    """
    Build a balanced AVL tree from a sorted array.
    Hint: Use middle element as root, recurse on halves.
    """
    # Your solution here
    pass
```

### Exercise 2: Merge Two AVL Trees
```python
def merge_avl(t1, t2):
    """
    Merge two AVL trees into one.
    Time: O(n log(n/m)) where m = size of smaller tree.
    """
    # Your solution here
    pass
```

### Exercise 3: Check if Tree is AVL
```python
def is_avl(root):
    """
    Check if a binary tree is a valid AVL tree.
    Returns (is_valid, height).
    """
    # Your solution here
    pass
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **AVL Property** | Balance factor ∈ {-1, 0, 1} for all nodes |
| **Rotations** | 4 types: LL, RR, LR, RL |
| **Insert** | BST insert + rebalance up to root |
| **Delete** | BST delete + rebalance up to root |
| **Guaranteed O(log n)** | Height ≤ 1.44 × log₂(n) |
| **Space** | O(n) |

**Key Insight:** AVL trees are the simplest self-balancing BST. They guarantee O(log n) for all operations at the cost of slightly more complex insertion/deletion. For most applications, they're the go-to choice when you need guaranteed performance.

**Next Topics:** Red-Black trees (less strict balancing, better for frequent insertions), B-trees (for disk-based storage), and Skip Lists (probabilistic alternative).
