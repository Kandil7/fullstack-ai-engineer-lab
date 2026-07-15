# DSA: Trees - Quiz

## Topic Overview
Trees are hierarchical data structures with a root node and child nodes forming a parent-child relationship. This quiz covers binary trees, binary search trees (BST), tree traversals, balanced trees, and common tree problems essential for interviews.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is a binary tree?
- **A)** A tree where each node has at most two children
- **B)** A tree with exactly two nodes
- **C)** A tree with two levels
- **D)** A sorted tree

**Correct Answer: A** — A binary tree is a tree data structure where each node has at most two children, typically called left and right.

---

### Q2. What is the difference between a binary tree and a binary search tree (BST)?
- **A)** No difference
- **B)** BST maintains sorted order: left child < parent < right child
- **C)** BST has more levels
- **D)** Binary tree is always balanced

**Correct Answer: B** — A BST is a binary tree with an ordering property: for any node, all left descendants are smaller and all right descendants are larger.

---

### Q3. What are the three main depth-first traversal orders?
- **A)** Preorder, Inorder, Postorder
- **B)** Top-down, Bottom-up, Level-order
- **C)** Left, Right, Center
- **D)** Forward, Backward, Random

**Correct Answer: A** — Preorder (root→left→right), Inorder (left→root→right), Postorder (left→right→root) are the three DFS traversal orders.

---

### Q4. What traversal of a BST gives elements in sorted order?
- **A)** Preorder
- **B)** Postorder
- **C)** Inorder
- **D)** Level-order

**Correct Answer: C** — Inorder traversal (left→root→right) of a BST produces elements in ascending sorted order due to the BST property.

---

### Q5. What is the time complexity of searching in a balanced BST?
- **A)** O(n)
- **B)** O(log n)
- **C)** O(n log n)
- **D)** O(1)

**Correct Answer: B** — A balanced BST has height O(log n), so search, insert, and delete all run in O(log n) time.

---

### Q6. What is the height of a tree with a single node?
- **A)** 0
- **B)** 1
- **C)** 2
- **D)** Undefined

**Correct Answer: A** — The height is the number of edges on the longest path from root to leaf. A single node has height 0.

---

### Q7. Which data structure is commonly used to implement level-order traversal?
- **A)** Stack
- **B)** Queue
- **C)** Priority Queue
- **D)** Linked List

**Correct Answer: B** — Level-order (BFS) traversal uses a queue: enqueue the root, then repeatedly dequeue and enqueue children.

---

### Q8. What is a complete binary tree?
- **A)** A tree where all levels are fully filled except possibly the last, which is filled from left to right
- **B)** A tree with no missing nodes
- **C)** A tree with equal left and right subtrees
- **D)** A tree with only one level

**Correct Answer: A** — A complete binary tree has all levels full except possibly the last, which is filled left to right. Heaps are complete binary trees.

---

### Q9. What is the time complexity of finding the lowest common ancestor (LCA) in a BST?
- **A)** O(n)
- **B)** O(log n) for balanced BST
- **C)** O(n log n)
- **D)** O(1)

**Correct Answer: B** — In a balanced BST, LCA can be found in O(log n) by traversing from root: if both values are smaller, go left; if both larger, go right; otherwise, current node is LCA.

---

### Q10. What is the output of this inorder traversal?
```python
#      4
#     / \
#    2   6
#   / \ / \
#  1  3 5  7
def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)
```
- **A)** [4, 2, 6, 1, 3, 5, 7]
- **B)** [1, 2, 3, 4, 5, 6, 7]
- **C)** [1, 3, 2, 5, 7, 6, 4]
- **D)** [4, 2, 1, 3, 6, 5, 7]

**Correct Answer: B** — Inorder traversal (left→root→right) on this BST gives sorted order: [1, 2, 3, 4, 5, 6, 7].

---

### Q11. What is the maximum number of nodes in a binary tree of height h?
- **A)** 2h
- **B)** 2^h - 1
- **C)** 2^(h+1) - 1
- **D)** h²

**Correct Answer: C** — A perfect binary tree of height h has 2^(h+1) - 1 nodes (sum of geometric series: 1 + 2 + 4 + ... + 2^h).

---

### Q12. What is an AVL tree?
- **A)** A binary tree with no balance requirement
- **B)** A self-balancing BST where the height difference of subtrees is at most 1
- **C)** A tree with exactly 2 children per node
- **D)** A tree that stores data in arrays

**Correct Answer: B** — An AVL tree maintains a balance factor (|height(left) - height(right)| ≤ 1) for every node, ensuring O(log n) operations.

---

### Q13. Which traversal uses a stack (or recursion)?
- **A)** Level-order
- **B)** Depth-first search (preorder/inorder/postorder)
- **C)** Breadth-first search
- **D)** All of the above

**Correct Answer: B** — DFS traversals (preorder, inorder, postorder) can be implemented iteratively using an explicit stack. Level-order uses a queue.

---

### Q14. What is a trie?
- **A)** A binary search tree for numbers
- **B)** A tree-like data structure for storing strings where each node represents a character
- **C)** A tree with three children per node
- **D)** A balanced binary tree

**Correct Answer: B** — A trie (prefix tree) stores strings character by character, enabling efficient prefix-based searches. Commonly used in autocomplete.

---

### Q15. What is the space complexity of storing a binary tree with n nodes?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n)
- **D)** O(n²)

**Correct Answer: C** — Each node requires space for data and pointers. Total space for n nodes is O(n).

---

### Q16. What is a segment tree used for?
- **A)** Searching for an element
- **B)** Efficient range queries and updates on an array
- **C)** Sorting elements
- **D)** Hashing data

**Correct Answer: B** — A segment tree supports range queries (sum, min, max) and point updates in O(log n) time, built over an array.

---

### Q17. What is the output of this preorder traversal?
```python
#      1
#     / \
#    2   3
#   / \
#  4   5
def preorder(node):
    if node is None:
        return []
    return [node.val] + preorder(node.left) + preorder(node.right)
```
- **A)** [4, 2, 5, 1, 3]
- **B)** [1, 2, 4, 5, 3]
- **C)** [4, 5, 2, 3, 1]
- **D)** [1, 3, 2, 4, 5]

**Correct Answer: B** — Preorder traversal (root→left→right): visit 1, then left subtree (2, 4, 5), then right subtree (3). Result: [1, 2, 4, 5, 3].

---

### Q18. What is the time complexity of inserting into a BST in the worst case?
- **A)** O(1)
- **B)** O(log n)
- **C)** O(n) for unbalanced BST
- **D)** O(n log n)

**Correct Answer: C** — An unbalanced BST (essentially a linked list) has height O(n), making insertion O(n). Balanced BSTs guarantee O(log n).

---

### Q19. What is a red-black tree?
- **A)** A tree colored with red and black markers
- **B)** A self-balancing BST with color properties ensuring O(log n) operations
- **C)** A tree with only two levels
- **D)** A tree that stores data in a hash table

**Correct Answer: B** — A red-black tree is a self-balancing BST with color constraints (root is black, no two red nodes adjacent, etc.) guaranteeing O(log n) height.

---

### Q20. Which algorithm uses a tree data structure internally?
- **A)** Dijkstra's algorithm
- **B)** Heap sort
- **C)** Merge sort
- **D)** Both B and C

**Correct Answer: B** — Heap sort uses a binary heap (complete binary tree stored in an array). Merge sort uses divide-and-conquer but doesn't use a tree data structure explicitly.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | A | 11 | C |
| 2 | B | 12 | B |
| 3 | A | 13 | B |
| 4 | C | 14 | B |
| 5 | B | 15 | C |
| 6 | A | 16 | B |
| 7 | B | 17 | B |
| 8 | A | 18 | C |
| 9 | B | 19 | B |
| 10 | B | 20 | B |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong tree knowledge
