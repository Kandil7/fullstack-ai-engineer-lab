# Lecture 03: Stacks

## Topic Overview

A **stack** is a linear data structure that follows the **LIFO (Last In, First Out)** principle. The last element added is the first one removed. Think of a stack of plates — you always add to and remove from the top.

Stacks are fundamental in computing:
- **Function call stack** — manages function calls and local variables
- **Expression evaluation** — parsing and evaluating mathematical expressions
- **Backtracking** — undo operations, navigation history
- **Depth-first search** — graph/tree traversal

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Implement** a stack using both arrays and linked lists
2. **Perform** push, pop, peek, and is_empty operations
3. **Apply** stacks to solve practical problems (balanced brackets, postfix evaluation)
4. **Convert** between infix, prefix, and postfix notations
5. **Analyze** time and space complexity of stack operations
6. **Use** Python's `list` and `collections.deque` as stacks
7. **Recognize** stack-based patterns in algorithms

---

## Key Concepts

### 1. Stack Operations (ADT)

```
Stack ADT Operations:
┌─────────────┬────────────────────────────────────────────┐
│ Operation   │ Description                                │
├─────────────┼────────────────────────────────────────────┤
│ push(item)  │ Add item to the top of the stack           │
│ pop()       │ Remove and return the top item             │
│ peek/top()  │ Return the top item without removing it    │
│ is_empty()  │ Check if the stack is empty                │
│ size()      │ Return the number of elements              │
└─────────────┴────────────────────────────────────────────┘

Visual representation:
    push(3)  →  push(5)  →  push(7)  →  pop()
    
    [  3  ]    [  5  ]    [  7  ]    [  5  ]
    [     ]    [  3  ]    [  5  ]    [  3  ]
    [     ]    [     ]    [  3  ]    [     ]
    ← TOP      ← TOP      ← TOP      ← TOP
```

### 2. Stack Implementation Using a Python List

```python
class Stack:
    """Stack implementation using a Python list."""
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Add item to top. O(1) amortized."""
        self.items.append(item)
    
    def pop(self):
        """Remove and return top item. O(1)."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.items.pop()
    
    def peek(self):
        """Return top item without removing. O(1)."""
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self.items[-1]
    
    def is_empty(self):
        """Check if stack is empty. O(1)."""
        return len(self.items) == 0
    
    def size(self):
        """Return number of items. O(1)."""
        return len(self.items)
    
    def __str__(self):
        return f"Stack({self.items})"

# Usage
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(stack)          # Stack([1, 2, 3])
print(stack.pop())    # 3
print(stack.peek())   # 2
print(stack.size())   # 2
```

### 3. Stack Implementation Using a Linked List

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedStack:
    """Stack implementation using a singly linked list."""
    
    def __init__(self):
        self.top = None
        self._size = 0
    
    def push(self, item):
        """Add item to top. O(1)."""
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self._size += 1
    
    def pop(self):
        """Remove and return top item. O(1)."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data
    
    def peek(self):
        """Return top item without removing. O(1)."""
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self.top.data
    
    def is_empty(self):
        return self.top is None
    
    def size(self):
        return self._size
```

### 4. Time Complexity Analysis

| Operation | Array-based | Linked List-based |
|-----------|------------|-------------------|
| push | O(1) amortized | O(1) |
| pop | O(1) | O(1) |
| peek | O(1) | O(1) |
| is_empty | O(1) | O(1) |
| size | O(1) | O(1) |
| search | O(n) | O(n) |
| Space | O(n) | O(n) + pointer overhead |

**Why O(1) for push/pop?**
- Array-based: `append()` and `pop()` operate on the end — no shifting needed
- Linked list: Adding/removing at the head is O(1)

---

## Complete Code Examples

### Example 1: Balanced Parentheses

```python
"""
Check if a string has balanced brackets: (), [], {}
Time: O(n), Space: O(n)
"""

def is_balanced(expression):
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}
    
    for char in expression:
        if char in '([{':           # Opening bracket
            stack.append(char)
        elif char in ')]}':         # Closing bracket
            if not stack or stack[-1] != matching[char]:
                return False
            stack.pop()
    
    return len(stack) == 0  # Stack should be empty if balanced

# Tests
print(is_balanced("({[()]})"))      # True
print(is_balanced("({[()]})"))      # True
print(is_balanced("({[()]"))        # False — missing closing
print(is_balanced("({[()]}"))       # False — wrong order
print(is_balanced(""))              # True — empty is balanced
```

### Example 2: Postfix Expression Evaluation

```python
"""
Evaluate a postfix (Reverse Polish Notation) expression.
Example: "3 4 + 2 *" → (3 + 4) * 2 = 14

Algorithm:
1. Scan left to right
2. If number → push to stack
3. If operator → pop two operands, compute, push result
4. Final result is the only item on stack

Time: O(n), Space: O(n)
"""

def evaluate_postfix(expression):
    stack = []
    tokens = expression.split()
    
    for token in tokens:
        if token.lstrip('-').isdigit():  # Handle negative numbers
            stack.append(int(token))
        else:
            # Pop two operands (note order!)
            b = stack.pop()  # Second operand (popped first)
            a = stack.pop()  # First operand
            
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(int(a / b))  # Integer division
    
    return stack[0]

# Tests
print(evaluate_postfix("3 4 +"))            # 7
print(evaluate_postfix("3 4 + 2 *"))        # 14
print(evaluate_postfix("5 1 2 + 4 * + 3 -"))  # 14
```

### Example 3: Infix to Postfix Conversion

```python
"""
Convert infix expression to postfix (Shunting-Yard Algorithm).
Example: "3 + 4 * 2" → "3 4 2 * +"

Operator precedence:
  * / : precedence 2 (high)
  + - : precedence 1 (low)

Algorithm:
1. If number → output directly
2. If '(' → push to stack
3. If ')' → pop and output until '('
4. If operator → pop higher/equal precedence operators, then push
5. At end → pop all remaining operators

Time: O(n), Space: O(n)
"""

def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []
    output = []
    
    tokens = expression.replace('(', '( ').replace(')', ' )').split()
    
    for token in tokens:
        if token.lstrip('-').isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remove '('
        else:  # Operator
            while (stack and stack[-1] != '(' and
                   stack[-1] in precedence and
                   precedence[stack[-1]] >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)
    
    while stack:
        output.append(stack.pop())
    
    return ' '.join(output)

# Tests
print(infix_to_postfix("3 + 4"))              # "3 4 +"
print(infix_to_postfix("3 + 4 * 2"))          # "3 4 2 * +"
print(infix_to_postfix("( 3 + 4 ) * 2"))      # "3 4 + 2 *"
print(infix_to_postfix("3 + 4 * 2 - 6 / 3"))  # "3 4 2 * + 6 3 / -"
```

### Example 4: Min Stack (Constant-Time Minimum)

```python
"""
Design a stack that supports push, pop, top, and retrieving
the minimum element in O(1) time.

Use two stacks: main stack and min stack.
Min stack tracks the minimum at each level.

Time: O(1) for all operations, Space: O(n)
"""

class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # Tracks minimums
    
    def push(self, val):
        self.stack.append(val)
        # Push to min_stack if it's empty or val <= current min
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self):
        if not self.stack:
            return None
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()
        return val
    
    def top(self):
        return self.stack[-1] if self.stack else None
    
    def get_min(self):
        return self.min_stack[-1] if self.min_stack else None

# Usage
ms = MinStack()
ms.push(5)
ms.push(3)
ms.push(7)
print(ms.get_min())  # 3
ms.pop()
print(ms.get_min())  # 3
ms.pop()
print(ms.get_min())  # 5
```

### Example 5: Valid Parentheses with Multiple Types

```python
"""
Advanced bracket validation with different bracket types
and error reporting.
"""

def validate_brackets(s):
    """Returns (is_valid, error_position) tuple."""
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    brackets = set('()[]{}')
    
    for i, char in enumerate(s):
        if char in '([{':
            stack.append((char, i))
        elif char in ')]}':
            if not stack:
                return False, i  # Unmatched closing bracket
            top, _ = stack.pop()
            if top != pairs[char]:
                return False, i  # Mismatched brackets
    
    if stack:
        return False, stack[-1][1]  # Unclosed opening bracket
    
    return True, -1

# Tests
tests = ["{[()]}", "((())", "([)]", ""]
for test in tests:
    valid, pos = validate_brackets(test)
    if valid:
        print(f"'{test}' → Valid ✓")
    else:
        print(f"'{test}' → Invalid at position {pos}")
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting to Check Empty Stack
```python
# WRONG: May raise IndexError
def pop_unsafe(stack):
    return stack.pop()  # Crashes if stack is empty!

# RIGHT: Always check first
def pop_safe(stack):
    if not stack:
        return None  # Or raise a meaningful exception
    return stack.pop()
```

### Mistake 2: Wrong Operand Order in Postfix
```python
# WRONG: Subtraction and division are not commutative
b = stack.pop()  # This is the SECOND operand
a = stack.pop()  # This is the FIRST operand
result = b - a   # WRONG: Should be a - b

# RIGHT
b = stack.pop()  # Second operand
a = stack.pop()  # First operand
result = a - b   # Correct: first - second
```

### Mistake 3: Using `insert(0, x)` for Stack Push
```python
# WRONG: O(n) — shifts all elements
stack.insert(0, item)  # Terrible for stack!

# RIGHT: Use append/pop — O(1) at the end
stack.append(item)
stack.pop()
```

### Mistake 4: Confusing Stack and Queue
```python
# Stack: LIFO — last in, first out
stack = [1, 2, 3]
stack.pop()  # Returns 3 (last added)

# Queue: FIFO — first in, first out
from collections import deque
queue = deque([1, 2, 3])
queue.popleft()  # Returns 1 (first added)
```

---

## Best Practices

1. **Use Python's `list`** as a stack — `append()` and `pop()` are O(1)
2. **Use `collections.deque`** if you need O(1) operations at both ends
3. **Always check for empty stack** before pop/peek operations
4. **For min-stack problems**, use a辅助 (auxiliary) stack
5. **For expression problems**, remember operator precedence and associativity
6. **Think recursively** — recursion implicitly uses the call stack
7. **Use stack for DFS** — iterative DFS avoids recursion depth limits

---

## Practice Exercises

### Exercise 1: Implement Queue Using Two Stacks
```python
class QueueFromStacks:
    """Implement a queue using two stacks."""
    def __init__(self):
        self.stack_in = []    # For enqueue
        self.stack_out = []   # For dequeue
    
    def enqueue(self, item):
        # Your solution here
        pass
    
    def dequeue(self):
        # Your solution here
        pass
```

### Exercise 2: Next Greater Element
```python
def next_greater_elements(arr):
    """
    For each element, find the next greater element to its right.
    Input: [4, 5, 2, 25]
    Output: [5, 25, 25, -1]
    
    Hint: Use a monotonic stack — O(n) time.
    """
    # Your solution here
    pass
```

### Exercise 3: Daily Temperatures
```python
def daily_temperatures(temperatures):
    """
    Given daily temperatures, find how many days until warmer.
    Input: [73, 74, 75, 71, 69, 72, 76, 73]
    Output: [1, 1, 4, 2, 1, 1, 0, 0]
    """
    # Your solution here — use monotonic stack
    pass
```

### Exercise 4: Implement a Circular Stack
```python
class CircularStack:
    """
    Stack with fixed capacity that wraps around.
    When full, pushing a new element overwrites the oldest.
    """
    def __init__(self, capacity):
        # Your solution here
        pass
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **LIFO Principle** | Last in, first out |
| **Push/Pop** | O(1) at the top |
| **Expression Evaluation** | Stack-based postfix evaluation |
| **Balanced Brackets** | Classic stack application |
| **Min Stack** | Auxiliary stack for O(1) min |
| **Recursion** | Implicitly uses the call stack |

**Key Insight:** Any problem involving "nested" or "matching" structures (brackets, nested function calls, undo/redo) is a candidate for stack-based solutions.

**Next Lecture:** Queues — the FIFO counterpart to stacks, essential for BFS, scheduling, and buffering.
