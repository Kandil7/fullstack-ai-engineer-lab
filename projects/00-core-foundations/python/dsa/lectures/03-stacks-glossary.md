# Glossary: Stacks

> Quick reference for all terms introduced in Lecture 03.

---

## A

### Array-Based Stack
- **Definition:** A stack implemented using a contiguous array (Python list), with push/pop at the end.
- **Time Complexity:** O(1) amortized for push/pop.
- **Related:** Linked Stack, Dynamic Array

```python
class ArrayStack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
```

---

## B

### Balanced Parentheses
- **Definition:** A string where every opening bracket has a corresponding closing bracket in the correct order.
- **Example:** `"{[()]}"` is balanced; `"([)]"` is not.
- **Related:** Stack, Bracket Matching

```python
def is_balanced(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0
```

---

## D

### Deque (Double-Ended Queue)
- **Definition:** A data structure that allows insertion and deletion at both ends in O(1) time.
- **Example:** Python `collections.deque` — can serve as both stack and queue.
- **Related:** Stack, Queue, FIFO, LIFO

```python
from collections import deque
dq = deque([1, 2, 3])
dq.append(4)      # Add to right (stack push)
dq.appendleft(0)  # Add to left (queue front)
dq.pop()           # Remove from right (stack pop)
dq.popleft()       # Remove from left (queue dequeue)
```

---

## E

### Expression Evaluation
- **Definition:** Computing the result of a mathematical expression using stack-based parsing.
- **Example:** Evaluating `"3 4 + 2 *"` → `(3+4)*2 = 14`
- **Related:** Postfix, Infix, Prefix, Shunting-Yard

### Expression Tree
- **Definition:** A binary tree where leaves are operands and internal nodes are operators.
- **Example:** For `3 + 4 * 2`, the tree has `*` as root, `+` as left child, `2` as right child.
- **Related:** Postfix, Prefix, Inorder Traversal

---

## I

### Infix Notation
- **Definition:** The standard mathematical notation where operators are between operands.
- **Example:** `3 + 4 * 2` — operators between operands.
- **Related:** Postfix, Prefix, Operator Precedence

```
Infix:   3 + 4 * 2        → Requires precedence rules
Postfix: 3 4 2 * +        → No precedence needed (stack-based)
Prefix:  + 3 * 4 2        → No precedence needed (stack-based)
```

---

## L

### LIFO (Last In, First Out)
- **Definition:** The principle that the most recently added element is the first to be removed.
- **Example:** Stack of plates — you take from the top.
- **Related:** Stack, FIFO

```python
stack = []
stack.append("first")   # Bottom
stack.append("second")  # Middle
stack.append("third")   # Top
print(stack.pop())      # "third" — last in, first out
```

### Linked Stack
- **Definition:** A stack implemented using a linked list, with push/pop at the head.
- **Time Complexity:** O(1) for push/pop (no resizing needed).
- **Related:** Array-Based Stack, Linked List

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedStack:
    def __init__(self):
        self.top = None
    def push(self, item):
        node = Node(item)
        node.next = self.top
        self.top = node
    def pop(self):
        data = self.top.data
        self.top = self.top.next
        return data
```

---

## M

### Monotonic Stack
- **Definition:** A stack where elements are always in sorted order (increasing or decreasing).
- **Use Case:** Finding next greater/smaller element in O(n) time.
- **Related:** Next Greater Element, Stack

```python
def next_greater(arr):
    result = [-1] * len(arr)
    stack = []  # Monotonic decreasing stack (stores indices)
    for i, val in enumerate(arr):
        while stack and arr[stack[-1]] < val:
            result[stack.pop()] = val
        stack.append(i)
    return result
```

### Min Stack
- **Definition:** A stack that supports retrieving the minimum element in O(1) time.
- **Implementation:** Uses an auxiliary stack to track minimums.
- **Related:** Auxiliary Stack, Stack

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    def pop(self):
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()
        return val
    def get_min(self):
        return self.min_stack[-1]
```

---

## N

### Next Greater Element
- **Definition:** For each element in an array, the first element to its right that is greater.
- **Example:** In `[4, 5, 2, 25]`, next greater for 4 is 5, for 5 is 25, for 2 is 25.
- **Algorithm:** Monotonic stack in O(n).
- **Related:** Monotonic Stack

---

## O

### Operator Precedence
- **Definition:** The order in which operators are evaluated in an expression.
- **Example:** `*` and `/` have higher precedence than `+` and `-`.
- **Related:** Shunting-Yard, Postfix Conversion

```
Precedence (high to low):
  ^          (exponentiation)
  *, /       (multiplication, division)
  +, -       (addition, subtraction)
```

---

## P

### Peek / Top
- **Definition:** Viewing the top element of a stack without removing it.
- **Time Complexity:** O(1)
- **Related:** Pop, Push

```python
stack = [1, 2, 3]
top = stack[-1]  # Peek: returns 3 without removing
```

### Pop
- **Definition:** Removing and returning the top element of a stack.
- **Time Complexity:** O(1)
- **Related:** Push, Peek, LIFO

```python
stack = [1, 2, 3]
item = stack.pop()  # Returns 3, stack is now [1, 2]
```

### Postfix Notation (RPN)
- **Definition:** Notation where operators follow their operands. Also called Reverse Polish Notation.
- **Example:** `3 4 +` means `3 + 4 = 7`
- **Related:** Infix, Prefix, Expression Evaluation

```python
# Postfix evaluation using stack
def eval_postfix(expr):
    stack = []
    for token in expr.split():
        if token in '+-*/':
            b, a = stack.pop(), stack.pop()
            stack.append({'+' : a+b, '-': a-b, '*': a*b, '/': a//b}[token])
        else:
            stack.append(int(token))
    return stack[0]

print(eval_postfix("3 4 + 2 *"))  # 14
```

### Prefix Notation
- **Definition:** Notation where operators precede their operands. Also called Polish Notation.
- **Example:** `+ 3 4` means `3 + 4 = 7`
- **Related:** Postfix, Infix

---

## S

### Stack
- **Definition:** A LIFO (Last In, First Out) data structure — elements are added and removed from the same end (top).
- **Operations:** push, pop, peek, is_empty.
- **Related:** LIFO, Push, Pop, Queue

```python
stack = []
stack.push(10)  # [10]
stack.push(20)  # [10, 20]
stack.push(30)  # [10, 20, 30]
stack.pop()     # Returns 30 → [10, 20]
```

### Stack Overflow
- **Definition:** An error that occurs when a stack exceeds its maximum capacity (e.g., too many recursive calls).
- **Example:** Infinite recursion causes a stack overflow.
- **Related:** Recursion, Call Stack, Base Case

```python
# Causes stack overflow — no base case!
def infinite_recursion(n):
    return infinite_recursion(n + 1)  # Never stops
```

### Stack Underflow
- **Definition:** An error that occurs when trying to pop from an empty stack.
- **Related:** Stack, Pop, Underflow

### Shunting-Yard Algorithm
- **Definition:** An algorithm by Edsger Dijkstra for converting infix expressions to postfix notation.
- **Time Complexity:** O(n)
- **Related:** Infix, Postfix, Operator Precedence

```python
def shunting_yard(expression):
    """Convert infix to postfix using Shunting-Yard algorithm."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output, stack = [], []
    for token in expression.split():
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(token, 0):
                output.append(stack.pop())
            stack.append(token)
    output.extend(reversed(stack))
    return output
```

---

## T

### Top
- **Definition:** The element at the top of the stack — the most recently pushed element.
- **Related:** Peek, Push, Pop

---

## U

### Undo/Redo
- **Definition:** A pattern where operations are stored on stacks to allow reversing (undo) and reapplying (redo).
- **Example:** Text editor undo — each action is pushed to an undo stack.
- **Related:** Stack, Two-Stack Pattern

```python
class UndoRedo:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
    def do(self, action):
        self.undo_stack.append(action)
        self.redo_stack.clear()  # New action clears redo
    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            self.redo_stack.append(action)
            return action
    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
            return action
```

---

## Quick Reference Table

| Term | Definition | Time | Example |
|------|-----------|------|---------|
| Push | Add to top | O(1) | `stack.append(x)` |
| Pop | Remove from top | O(1) | `stack.pop()` |
| Peek/Top | View top without removing | O(1) | `stack[-1]` |
| Is Empty | Check if empty | O(1) | `len(stack) == 0` |
| Size | Count elements | O(1) | `len(stack)` |
| Min Stack | Get minimum | O(1) | Auxiliary stack |
| Infix to Postfix | Convert notation | O(n) | Shunting-Yard |
| Evaluate Postfix | Compute result | O(n) | Stack-based scan |
| Balanced Brackets | Validate pairs | O(n) | Matching push/pop |
| Next Greater Element | Find successor | O(n) | Monotonic stack |

| Stack Application | Description | Algorithm |
|-------------------|------------|-----------|
| Function calls | Manage scope and return | Call stack |
| Expression eval | Evaluate postfix | Stack scan |
| Bracket matching | Validate balanced pairs | Push/pop matching |
| Undo/Redo | Track actions | Two stacks |
| DFS traversal | Visit graph depth-first | Explicit/implicit stack |
| Backtracking | Explore and retreat | Push on explore, pop on retreat |
