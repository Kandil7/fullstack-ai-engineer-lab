# DSA Trees Interview Practice

## Topic Overview

Trees are hierarchical data structures with a root node and child nodes. Binary trees have at most two children. Binary Search Trees (BSTs) maintain sorted order. Tree problems test **recursion**, **traversals**, and **divide-and-conquer** thinking.

**Key Properties:**
- Root node has no parent
- Leaf node has no children
- Height = longest path from root to leaf
- Depth = distance from root to a node
- A tree with n nodes has n-1 edges

**Tree Types:**
- **Binary tree:** Each node has 0-2 children
- **BST:** Left < Root < Right
- **Complete binary tree:** All levels full except possibly last, filled left to right
- **Balanced BST:** Height is O(log n)
- **Full binary tree:** Each node has 0 or 2 children

---

## Interview Questions (with Answers)

### Q1: What are the different tree traversal methods?

**Answer:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

**Inorder (Left → Root → Right):** BST gives sorted order
```python
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)
```

**Preorder (Root → Left → Right):** Used for tree serialization
```python
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)
```

**Postorder (Left → Right → Root):** Used for deletion, expression evaluation
```python
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]
```

**Level-order (BFS):** Uses a queue
```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

**Iterative Inorder (using stack):**
```python
def inorder_iterative(root):
    result = []
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result
```

---

### Q2: What is a Binary Search Tree (BST)?

**Answer:**
A BST is a binary tree where for every node:
- All nodes in left subtree have values < node's value
- All nodes in right subtree have values > node's value

**Operations:**
- Search: O(log n) average, O(n) worst
- Insert: O(log n) average, O(n) worst
- Delete: O(log n) average, O(n) worst

**BST Operations:**
```python
def search(root, val):
    if not root or root.val == val:
        return root
    if val < root.val:
        return search(root.left, val)
    return search(root.right, val)

def insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root

def delete(root, val):
    if not root:
        return root
    if val < root.val:
        root.left = delete(root.left, val)
    elif val > root.val:
        root.right = delete(root.right, val)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        # Find inorder successor (smallest in right subtree)
        successor = find_min(root.right)
        root.val = successor.val
        root.right = delete(root.right, successor.val)
    return root

def find_min(root):
    while root.left:
        root = root.left
    return root
```

---

### Q3: How do you find the lowest common ancestor (LCA) of two nodes?

**Answer:**
**Binary Tree (O(n) time):**
```python
def lowest_common_ancestor(root, p, q):
    if not root or root == p or root == q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left and right:
        return root  # p and q are in different subtrees
    return left or right

# Test
#       3
#      / \
#     5   1
#    / \ / \
#   6  2 0  8
#     / \
#    7   4
root = TreeNode(3)
root.left = TreeNode(5)
root.right = TreeNode(1)
root.left.left = TreeNode(6)
root.left.right = TreeNode(2)
root.left.right.left = TreeNode(7)
root.left.right.right = TreeNode(4)
root.right.left = TreeNode(0)
root.right.right = TreeNode(8)

assert lowest_common_ancestor(root, root.left, root.right) == root  # LCA of 5 and 1 is 3
assert lowest_common_ancestor(root, root.left, root.left.right.right) == root.left  # LCA of 5 and 4 is 5
```

**BST (O(log n) time):**
```python
def lca_bst(root, p, q):
    if p.val < root.val and q.val < root.val:
        return lca_bst(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lca_bst(root.right, p, q)
    return root
```

---

### Q4: How do you check if a binary tree is balanced?

**Answer:**
```python
def is_balanced(root):
    def check_height(node):
        if not node:
            return 0

        left_height = check_height(node.left)
        if left_height == -1:
            return -1

        right_height = check_height(node.right)
        if right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1

        return max(left_height, right_height) + 1

    return check_height(root) != -1
```

**Time: O(n), Space: O(h)** where h is tree height.

---

### Q5: How do you serialize and deserialize a binary tree?

**Answer:**
```python
class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string."""
        if not root:
            return "null"

        return f"{root.val},{self.serialize(root.left)},{self.serialize(root.right)}"

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        def helper(nodes):
            val = next(nodes)
            if val == 'null':
                return None
            node = TreeNode(int(val))
            node.left = helper(nodes)
            node.right = helper(nodes)
            return node

        return helper(iter(data.split(',')))

# Test
codec = Codec()
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.right.left = TreeNode(4)
root.right.right = TreeNode(5)

serialized = codec.serialize(root)
deserialized = codec.deserialize(serialized)
assert codec.serialize(deserialized) == serialized
```

---

### Q6: How do you find the maximum depth of a binary tree?

**Answer:**
**Recursive:**
```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

**Iterative (BFS):**
```python
def max_depth_bfs(root):
    if not root:
        return 0
    queue = deque([root])
    depth = 0
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth
```

**Time: O(n), Space: O(h) recursive, O(n) iterative**

---

### Q7: How do you construct a binary tree from preorder and inorder traversals?

**Answer:**
```python
def build_tree(preorder, inorder):
    if not preorder or not inorder:
        return None

    root_val = preorder[0]
    root = TreeNode(root_val)

    mid = inorder.index(root_val)

    root.left = build_tree(preorder[1:mid+1], inorder[:mid])
    root.right = build_tree(preorder[mid+1:], inorder[mid+1:])

    return root

# Test
preorder = [3, 9, 20, 15, 7]
inorder = [9, 3, 15, 20, 7]
root = build_tree(preorder, inorder)
#       3
#      / \
#     9  20
#        / \
#       15  7
```

**Time: O(n), Space: O(n)**

---

### Q8: How do you find the diameter of a binary tree?

**Answer:**
The diameter is the longest path between any two nodes (number of edges).

```python
def diameter_of_binary_tree(root):
    diameter = 0

    def depth(node):
        nonlocal diameter
        if not node:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        diameter = max(diameter, left + right)
        return 1 + max(left, right)

    depth(root)
    return diameter
```

**Time: O(n), Space: O(h)**

---

### Q9: How do you flatten a binary tree to a linked list?

**Answer:**
```python
def flatten(root):
    """Flatten to right-only linked list in preorder."""
    if not root:
        return

    stack = [root]
    while stack:
        node = stack.pop()

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

        if stack:
            node.right = stack[-1]
        node.left = None

# Alternative: Morris traversal O(1) space
def flatten_morris(root):
    curr = root
    while curr:
        if curr.left:
            # Find rightmost node in left subtree
            prev = curr.left
            while prev.right:
                prev = prev.right
            prev.right = curr.right
            curr.right = curr.left
            curr.left = None
        curr = curr.right
```

---

### Q10: How do you find all root-to-leaf paths that sum to a target?

**Answer:**
```python
def path_sum(root, target):
    result = []

    def dfs(node, remaining, path):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right and remaining == node.val:
            result.append(path[:])
        else:
            dfs(node.left, remaining - node.val, path)
            dfs(node.right, remaining - node.val, path)
        path.pop()

    dfs(root, target, [])
    return result

# Test
#       5
#      / \
#     4   8
#    /   / \
#   11  13  4
#  / \      / \
# 7   2    5   1
root = TreeNode(5)
root.left = TreeNode(4)
root.right = TreeNode(8)
root.left.left = TreeNode(11)
root.left.left.left = TreeNode(7)
root.left.left.right = TreeNode(2)
root.right.left = TreeNode(13)
root.right.right = TreeNode(4)
root.right.right.left = TreeNode(5)
root.right.right.right = TreeNode(1)

assert path_sum(root, 22) == [[5,4,11,2],[5,8,4,5]]
```

---

### Q11: How do you find the kth smallest element in a BST?

**Answer:**
```python
def kth_smallest(root, k):
    stack = []
    curr = root

    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right

# Alternative: Recursive with counter
def kth_smallest_recursive(root, k):
    def inorder(node):
        if not node:
            return []
        return inorder(node.left) + [node.val] + inorder(node.right)
    return inorder(root)[k-1]
```

---

### Q12: How do you validate a BST?

**Answer:**
```python
def is_valid_bst(root):
    def validate(node, low, high):
        if not node:
            return True
        if node.val <= low or node.val >= high:
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)

    return validate(root, float('-inf'), float('inf'))
```

**Common mistake:** Only checking `node.left.val < node.val` is wrong. Must check against all ancestors.

---

### Q13: How do you invert a binary tree?

**Answer:**
```python
def invert_tree(root):
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)
    return root
```

**Iterative:**
```python
def invert_tree_iterative(root):
    if not root:
        return None
    queue = deque([root])
    while queue:
        node = queue.popleft()
        node.left, node.right = node.right, node.left
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return root
```

---

### Q14: How do you find the right side view of a binary tree?

**Answer:**
```python
def right_side_view(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_length = len(queue)
        for i in range(level_length):
            node = queue.popleft()
            if i == level_length - 1:
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result
```

---

### Q15: How do you find the vertical order traversal of a binary tree?

**Answer:**
```python
from collections import defaultdict

def vertical_order(root):
    if not root:
        return []

    column_table = defaultdict(list)
    min_col = max_col = 0

    queue = deque([(root, 0)])

    while queue:
        node, col = queue.popleft()
        if node:
            column_table[col].append(node.val)
            min_col = min(min_col, col)
            max_col = max(max_col, col)
            queue.append((node.left, col - 1))
            queue.append((node.right, col + 1))

    return [column_table[col] for col in range(min_col, max_col + 1)]
```

---

## Coding Challenges

### Challenge 1: Maximum Depth of Binary Tree
```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Test
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)
assert max_depth(root) == 3
```
**Time: O(n), Space: O(h)**

---

### Challenge 2: Symmetric Tree
```python
def is_symmetric(root):
    def is_mirror(t1, t2):
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False
        return (t1.val == t2.val and
                is_mirror(t1.left, t2.right) and
                is_mirror(t1.right, t2.left))

    return is_mirror(root.left, root.right) if root else True
```
**Time: O(n), Space: O(h)**

---

### Challenge 3: Invert Binary Tree
```python
def invert_tree(root):
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)
    return root
```
**Time: O(n), Space: O(h)**

---

### Challenge 4: Binary Tree Level Order Traversal
```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```
**Time: O(n), Space: O(n)**

---

### Challenge 5: Validate BST
```python
def is_valid_bst(root):
    def validate(node, low, high):
        if not node:
            return True
        if node.val <= low or node.val >= high:
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
    return validate(root, float('-inf'), float('inf'))
```
**Time: O(n), Space: O(h)**

---

### Challenge 6: Lowest Common Ancestor
```python
def lowest_common_ancestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right
```
**Time: O(n), Space: O(h)**

---

### Challenge 7: Path Sum II (All root-to-leaf paths with given sum)
```python
def path_sum(root, target):
    result = []
    def dfs(node, remaining, path):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right and remaining == node.val:
            result.append(path[:])
        else:
            dfs(node.left, remaining - node.val, path)
            dfs(node.right, remaining - node.val, path)
        path.pop()
    dfs(root, target, [])
    return result
```
**Time: O(n²), Space: O(n)**

---

### Challenge 8: Binary Tree Zigzag Level Order Traversal
```python
def zigzag_level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level = deque()
        for _ in range(len(queue)):
            node = queue.popleft()
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(list(level))
        left_to_right = not left_to_right

    return result
```
**Time: O(n), Space: O(n)**

---

### Challenge 9: Serialize and Deserialize Binary Tree
```python
class Codec:
    def serialize(self, root):
        if not root:
            return "null"
        return f"{root.val},{self.serialize(root.left)},{self.serialize(root.right)}"

    def deserialize(self, data):
        def helper(nodes):
            val = next(nodes)
            if val == 'null':
                return None
            node = TreeNode(int(val))
            node.left = helper(nodes)
            node.right = helper(nodes)
            return node
        return helper(iter(data.split(',')))
```
**Time: O(n), Space: O(n)**

---

### Challenge 10: Kth Smallest Element in BST
```python
def kth_smallest(root, k):
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
```
**Time: O(h + k), Space: O(h)**

---

## Common Follow-Up Questions

1. **"Can you do it iteratively?"** — Yes, use an explicit stack (for DFS) or queue (for BFS). Mention Morris traversal for O(1) space.
2. **"What about a balanced BST?"** — Use AVL or Red-Black tree for guaranteed O(log n).
3. **"How would you handle very deep trees?"** — Iterative approaches avoid stack overflow.
4. **"What's the difference between BST and heap?"** — BST: sorted, efficient search. Heap: efficient min/max, no search.
5. **"Can you use this for a Trie?"** — Yes, Trie is a special tree for string operations.

---

## Tips for Answering Tree Questions

1. **Think recursively:** Most tree problems have elegant recursive solutions.
2. **Base cases:** Empty tree, single node, leaf node.
3. **Return values:** What should each recursive call return? (node, value, boolean, list)
4. **Traversal order:** Inorder for BST (sorted), preorder for construction, postorder for deletion.
5. **Use helper functions:** Pass extra state (current path, remaining sum, etc.) through helpers.
6. **Draw the tree:** Visualize before coding.

---

## Complexity Cheat Sheet

| Problem | Time | Space |
|---------|------|-------|
| Traversals (in/pre/post) | O(n) | O(h) |
| Level-order | O(n) | O(n) |
| Search in BST | O(h) | O(h) |
| Insert/Delete BST | O(h) | O(h) |
| LCA | O(n) | O(h) |
| Max Depth | O(n) | O(h) |
| Diameter | O(n) | O(h) |
| Serialize/Deserialize | O(n) | O(n) |
| Validate BST | O(n) | O(h) |
| Kth Smallest BST | O(h + k) | O(h) |
| Path Sum | O(n²) | O(n) |
| Invert Tree | O(n) | O(h) |
