# Glossary: AVL Trees

> Quick reference for all terms introduced in Lecture 10.

---

## A

### AVL Tree
- **Definition:** A self-balancing binary search tree where the height difference between left and right subtrees of every node is at most 1.
- **Named After:** Georgy Adelson-Velsky and Evgenii Landis (1962).
- **Guarantee:** All operations O(log n).
- **Related:** BST, Balanced Tree, Rotation

```python
class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1
```

---

## B

### Balance Factor
- **Definition:** The difference between the heights of the left and right subtrees of a node. BF = height(left) - height(right).
- **AVL Constraint:** -1 ≤ BF ≤ 1 for all nodes.
- **Related:** Height, Rotation, AVL Property

```
Balance Factor = height(left) - height(right)

BF = +1: left-heavy (still balanced)
BF =  0: perfectly balanced
BF = -1: right-heavy (still balanced)
BF = +2 or -2: UNBALANCED — needs rotation!
```

---

## H

### Height (of AVL Tree)
- **Definition:** The number of edges on the longest path from root to leaf.
- **AVL Guarantee:** Height ≤ 1.44 × log₂(n + 2) ≈ 1.44 × log₂(n)
- **Related:** Balance Factor, Logarithmic Height

```python
# Minimum nodes for AVL height h:
# N(0) = 1, N(1) = 2
# N(h) = N(h-1) + N(h-2) + 1  (Fibonacci-like)
# This guarantees O(log n) height
```

### Height Update
- **Definition:** Recalculating a node's height after structural changes (insert, delete, rotation).
- **Formula:** height = 1 + max(height(left), height(right))
- **Related:** Rotation, AVL Property

```python
def update_height(node):
    node.height = 1 + max(get_height(node.left), get_height(node.right))
```

---

## I

### Insert (AVL)
- **Definition:** Adding a node to an AVL tree, followed by rebalancing via rotations.
- **Steps:** (1) Standard BST insert, (2) Update heights, (3) Check balance, (4) Rotate if needed.
- **Time:** O(log n)
- **Related:** Delete, Rotation, BST Insert

```python
def insert(node, val):
    # 1. BST insert
    if not node:
        return AVLNode(val)
    if val < node.val:
        node.left = insert(node.left, val)
    elif val > node.val:
        node.right = insert(node.right, val)
    else:
        return node
    
    # 2. Update height
    update_height(node)
    
    # 3. Check balance and rotate
    balance = get_balance(node)
    
    # 4 cases...
    return node
```

---

## L

### Left-Left (LL) Case
- **Definition:** Unbalanced node has balance factor +2, and the left child has balance factor ≥ 0.
- **Fix:** Single right rotation.
- **Related:** Right-Right, Left-Right, Right-Left

```
Before:      After (right rotate z):
   z              y
  / \            / \
 y   T4    →    x   z
/ \            / \ / \
x   T3        T1 T2 T3 T4
/ \
T1 T2
```

### Left-Right (LR) Case
- **Definition:** Unbalanced node has balance factor +2, and the left child has balance factor -1.
- **Fix:** Left rotate on left child, then right rotate on node.
- **Related:** Left-Left, Right-Right, Right-Left

```
Before:        After left rotate y:    After right rotate z:
   z               z                       y
  / \             / \                     / \
 y   T4    →     x   T4     →           x   z
/ \             / \                     / \ / \
T1  x          T1  y                   T1 T2 T3 T4
   / \             / \
  T2 T3           T2 T3
```

---

## R

### Right-Left (RL) Case
- **Definition:** Unbalanced node has balance factor -2, and the right child has balance factor +1.
- **Fix:** Right rotate on right child, then left rotate on node.
- **Related:** Left-Left, Right-Right, Left-Right

```
Before:        After right rotate y:    After left rotate z:
  z                z                       y
 / \              / \                     / \
T1   y     →    T1   x     →           z   x
    / \              / \               / \ / \
   x   T4          T2   y            T1 T2 T3 T4
  / \                  / \
 T2 T3                T3 T4
```

### Right-Right (RR) Case
- **Definition:** Unbalanced node has balance factor -2, and the right child has balance factor ≤ 0.
- **Fix:** Single left rotation.
- **Related:** Left-Left, Left-Right, Right-Left

```
Before:      After (left rotate z):
  z              y
 / \            / \
T1   y    →    z   x
    / \        / \ / \
   T2  x      T1 T2 T3 T4
      / \
     T3 T4
```

### Right Rotation
- **Definition:** A rotation that moves a node down to its left child's position, promoting the left child.
- **Time:** O(1)
- **Related:** Left Rotation, LL Case

```python
def right_rotate(z):
    y = z.left
    T3 = y.right
    
    y.right = z
    z.left = T3
    
    update_height(z)
    update_height(y)
    
    return y  # New root
```

### Root
- **Definition:** The topmost node of the AVL tree.
- **Related:** Node, Height

---

## T

### Tree Rotation
- **Definition:** A tree restructuring operation that changes the tree's structure while preserving the BST ordering property.
- **Purpose:** Restore balance after insertion or deletion.
- **Types:** Left rotation, right rotation, and combined (LR, RL).
- **Time:** O(1)
- **Related:** Balance Factor, AVL Property

```python
# Rotation preserves inorder traversal!
# Before rotation: inorder = [1, 2, 3, 4, 5]
# After rotation:  inorder = [1, 2, 3, 4, 5]  (same!)
```

---

## Quick Reference Table

| Case | Balance Factor | Child BF | Fix | Rotation Type |
|------|---------------|----------|-----|---------------|
| LL | +2 | ≥ 0 | Right rotate | Single |
| RR | -2 | ≤ 0 | Left rotate | Single |
| LR | +2 | -1 | Left then Right | Double |
| RL | -2 | +1 | Right then Left | Double |

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Search | O(log n) | O(h) | Same as BST |
| Insert | O(log n) | O(h) | BST insert + rotations |
| Delete | O(log n) | O(h) | BST delete + rotations |
| Rotation | O(1) | O(1) | At most O(log n) per op |
| Height update | O(1) | O(1) | After each rotation |

| AVL Tree | Regular BST | Red-Black Tree |
|----------|-------------|----------------|
| Strictly balanced (BF ±1) | May be unbalanced | Approximately balanced |
| O(log n) guaranteed | O(n) worst case | O(log n) guaranteed |
| More rotations | Fewer rotations | Fewer rotations |
| Better for lookup-heavy | Worse for degenerate | Better for insert-heavy |
| Height ≈ 1.44 log n | Height up to n | Height ≤ 2 log n |

| AVL vs Red-Black | AVL | Red-Black |
|-----------------|-----|-----------|
| Balance strictness | Stricter (BF ±1) | Looser (height ≤ 2×min) |
| Lookup speed | Faster (shorter tree) | Slightly slower |
| Insert/Delete rotations | More rotations | Fewer rotations |
| Use case | Read-heavy | Write-heavy |
| Implementation | Simpler | More complex |
| Memory per node | 1 int (height) | 1 bit (color) |
