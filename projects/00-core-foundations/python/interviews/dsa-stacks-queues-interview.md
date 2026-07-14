# DSA Stacks & Queues Interview Practice

## Topic Overview

Stacks (LIFO) and queues (FIFO) are linear data structures with constrained access patterns. They're fundamental for BFS/DFS, expression evaluation, scheduling, and monotonic patterns. Mastering **monotonic stack/queue** unlocks many "next greater/smaller element" problems.

**Core Properties:**

| Operation | Stack | Queue |
|-----------|-------|-------|
| Add | push O(1) | enqueue O(1) |
| Remove | pop O(1) | dequeue O(1) |
| Peek | top O(1) | front O(1) |
| Access middle | O(n) | O(n) |
| Search | O(n) | O(n) |

**Python implementations:**
- Stack: `list` with `append()` and `pop()`
- Queue: `collections.deque` with `append()` and `popleft()`
- Priority Queue: `heapq` (min-heap)

---

## Interview Questions (with Answers)

### Q1: What is a stack? Give three real-world applications.

**Answer:**
A stack is a LIFO (Last In, First Out) data structure. Operations: push (add to top), pop (remove from top), peek (view top).

**Applications:**
1. **Function call stack** — Recursion uses the call stack to track function calls
2. **Undo/Redo** — Text editors push changes to a stack
3. **Expression evaluation** — Converting infix to postfix, evaluating postfix expressions
4. **Browser back button** — Navigation history
5. **Balanced parentheses** — Matching brackets in compilers

---

### Q2: What is a queue? Give three real-world applications.

**Answer:**
A queue is a FIFO (First In, First Out) data structure. Operations: enqueue (add to rear), dequeue (remove from front), peek (view front).

**Applications:**
1. **BFS traversal** — Level-order tree/graph traversal
2. **Task scheduling** — OS process scheduling
3. **Print queue** — Documents printed in order
4. **Sliding window maximum** — Using deque
5. **Message queues** — RabbitMQ, Kafka (distributed systems)

---

### Q3: How do you implement a stack using a queue?

**Answer:**
**Using one queue:**
```python
from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x):
        self.q.append(x)
        # Rotate to make last pushed element the front
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self):
        return self.q.popleft()

    def top(self):
        return self.q[0]

    def empty(self):
        return len(self.q) == 0
```
**Time:** Push O(n), Pop O(1), Top O(1)

---

### Q4: How do you implement a queue using a stack?

**Answer:**
**Using two stacks:**
```python
class MyQueue:
    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def push(self, x):
        self.stack_in.append(x)

    def _transfer(self):
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())

    def pop(self):
        self._transfer()
        return self.stack_out.pop()

    def peek(self):
        self._transfer()
        return self.stack_out[-1]

    def empty(self):
        return not self.stack_in and not self.stack_out
```
**Time:** Amortized O(1) per operation

---

### Q5: How do you validate balanced parentheses?

**Answer:**
```python
def is_valid(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)

    return not stack

# Test
assert is_valid("()[]{}") == True
assert is_valid("(]") == False
assert is_valid("([)]") == False
assert is_valid("{[]}") == True
```
**Time: O(n), Space: O(n)**

---

### Q6: What is a monotonic stack? Explain with an example.

**Answer:**
A monotonic stack maintains elements in either increasing or decreasing order. It's used for "next greater/smaller element" problems.

**Next Greater Element:**
```python
def next_greater_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)

    return result

# Test
assert next_greater_element([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
```

**How it works:** We iterate through the array. For each element, we pop all stack elements that are smaller (they found their next greater). The remaining stack elements keep waiting.

---

### Q7: How do you implement a monotonic queue for sliding window maximum?

**Answer:**
```python
from collections import deque

def max_sliding_window(nums, k):
    result = []
    dq = deque()  # Stores indices, front is max

    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements (they're useless)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# Test
assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
```
**Time: O(n), Space: O(k)**

---

### Q8: How do you evaluate a postfix expression?

**Answer:**
```python
def eval_postfix(tokens):
    stack = []

    for token in tokens:
        if token in '+-*/':
            b = stack.pop()
            a = stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(int(a / b))  # truncate toward 0
        else:
            stack.append(int(token))

    return stack[0]

# Test
assert eval_postfix(["2", "1", "+", "3", "*"]) == 9  # (2+1)*3
assert eval_postfix(["4", "13", "5", "/", "+"]) == 6  # 4+(13/5)
```
**Time: O(n), Space: O(n)**

---

### Q9: How do you convert infix to postfix?

**Answer:**
Using the Shunting Yard algorithm:

```python
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output = []
    stack = []

    tokens = expression.split()

    for token in tokens:
        if token.isalnum():
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

# Test
assert infix_to_postfix("A + B * C") == "A B C * +"
assert infix_to_postfix("( A + B ) * C") == "A B + C *"
```

---

### Q10: How do you find the largest rectangle in a histogram?

**Answer:**
Monotonic stack approach:

```python
def largest_rectangle_area(heights):
    stack = []
    max_area = 0
    heights.append(0)  # Sentinel

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    heights.pop()  # Restore
    return max_area

# Test
assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
```
**Time: O(n), Space: O(n)**

---

### Q11: What is a deque? How does it differ from a stack and queue?

**Answer:**
A deque (double-ended queue) allows insertion and removal from both ends.

```python
from collections import deque

dq = deque()
dq.append(1)      # Add to right
dq.appendleft(2)  # Add to left
dq.pop()          # Remove from right
dq.popleft()      # Remove from left
dq[0]             # Access front (O(1))
dq[-1]            # Access back (O(1))
```

**Difference from stack/queue:**
- Stack: push/pop from one end only
- Queue: add to one end, remove from the other
- Deque: add/remove from both ends

---

### Q12: How do you implement a min stack (stack that supports getMin in O(1))?

**Answer:**
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def get_min(self):
        return self.min_stack[-1]
```

**Alternative without extra space:**
Store difference between current value and min. Reconstruct original when needed.

---

### Q13: How do you use a queue for BFS?

**Answer:**
```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order

# Test
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
assert bfs(graph, 'A') == ['A', 'B', 'C', 'D', 'E', 'F']
```

---

### Q14: How do you implement a stack that supports push, pop, top, and getMin in O(1)?

**Answer:**
Using a single stack with tuples:

```python
class MinStack:
    def __init__(self):
        self.stack = []

    def push(self, val):
        if not self.stack:
            self.stack.append((val, val))
        else:
            current_min = self.stack[-1][1]
            self.stack.append((val, min(val, current_min)))

    def pop(self):
        return self.stack.pop()[0]

    def top(self):
        return self.stack[-1][0]

    def get_min(self):
        return self.stack[-1][1]
```

---

### Q15: What is the difference between a stack and recursion?

**Answer:**
Recursion uses the call stack implicitly. Any recursive algorithm can be converted to an iterative one using an explicit stack.

**Recursion:**
```python
def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)
```

**Iterative with stack:**
```python
def factorial_iterative(n):
    stack = [n]
    result = 1
    while stack:
        val = stack.pop()
        result *= val
        if val > 1:
            stack.append(val - 1)
    return result
```

**When to use which:** Recursion is cleaner for tree/graph problems. Iterative is better for deep recursion (avoid stack overflow).

---

## Coding Challenges

### Challenge 1: Valid Parentheses
```python
def is_valid(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)

    return not stack

# Test
assert is_valid("()") == True
assert is_valid("()[]{}") == True
assert is_valid("(]") == False
assert is_valid("([)]") == False
assert is_valid("{[]}") == True
```
**Time: O(n), Space: O(n)**

---

### Challenge 2: Min Stack
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

    def top(self):
        return self.stack[-1]

    def get_min(self):
        return self.min_stack[-1]

# Test
ms = MinStack()
ms.push(-2)
ms.push(0)
ms.push(-3)
assert ms.get_min() == -3
ms.pop()
assert ms.top() == 0
assert ms.get_min() == -2
```
**Time: O(1) for all operations, Space: O(n)**

---

### Challenge 3: Daily Temperatures
Given daily temperatures, find how many days until a warmer temperature.

```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []  # Stack of indices

    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev = stack.pop()
            result[prev] = i - prev
        stack.append(i)

    return result

# Test
assert daily_temperatures([73,74,75,71,69,72,76,73]) == [1,1,4,2,1,1,0,0]
```
**Time: O(n), Space: O(n)**

---

### Challenge 4: Implement Queue Using Stacks
```python
class MyQueue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x):
        self.in_stack.append(x)

    def _transfer(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def pop(self):
        self._transfer()
        return self.out_stack.pop()

    def peek(self):
        self._transfer()
        return self.out_stack[-1]

    def empty(self):
        return not self.in_stack and not self.out_stack

# Test
q = MyQueue()
q.push(1)
q.push(2)
assert q.peek() == 1
assert q.pop() == 1
assert q.empty() == False
```
**Time: Amortized O(1), Space: O(n)**

---

### Challenge 5: Next Greater Element
```python
def next_greater_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)

    return result

# Test
assert next_greater_element([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
```
**Time: O(n), Space: O(n)**

---

### Challenge 6: Largest Rectangle in Histogram
```python
def largest_rectangle_area(heights):
    stack = []
    max_area = 0
    heights.append(0)

    for i in range(len(heights)):
        while stack and heights[stack[-1]] > heights[i]:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    heights.pop()
    return max_area

# Test
assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
assert largest_rectangle_area([2, 4]) == 4
```
**Time: O(n), Space: O(n)**

---

### Challenge 7: Decode String (LeetCode 394)
Given `s = "3[a2[c]]"`, return `"accaccacc"`.

```python
def decode_string(s):
    stack = []
    current_string = ""
    current_num = 0

    for char in s:
        if char.isdigit():
            current_num = current_num * 10 + int(char)
        elif char == '[':
            stack.append((current_string, current_num))
            current_string = ""
            current_num = 0
        elif char == ']':
            prev_string, num = stack.pop()
            current_string = prev_string + current_string * num
        else:
            current_string += char

    return current_string

# Test
assert decode_string("3[a2[c]]") == "accaccacc"
assert decode_string("2[abc]3[cd]ef") == "abcabccdcdcdef"
```
**Time: O(n), Space: O(n)**

---

### Challenge 8: Simplify Path
Simplify Unix-style file path.

```python
def simplify_path(path):
    stack = []
    components = path.split('/')

    for component in components:
        if component == '' or component == '.':
            continue
        elif component == '..':
            if stack:
                stack.pop()
        else:
            stack.append(component)

    return '/' + '/'.join(stack)

# Test
assert simplify_path("/home//foo/") == "/home/foo"
assert simplify_path("/home/user/Documents/../Pictures") == "/home/user/Pictures"
assert simplify_path("/a/./b/../../c/") == "/c"
```
**Time: O(n), Space: O(n)**

---

### Challenge 9: Basic Calculator II
Evaluate expression with +, -, *, /.

```python
def calculate(s):
    stack = []
    current_num = 0
    operation = '+'

    for i, char in enumerate(s):
        if char.isdigit():
            current_num = current_num * 10 + int(char)

        if char in '+-*/' or i == len(s) - 1:
            if operation == '+':
                stack.append(current_num)
            elif operation == '-':
                stack.append(-current_num)
            elif operation == '*':
                stack.append(stack.pop() * current_num)
            elif operation == '/':
                stack.append(int(stack.pop() / current_num))

            operation = char
            current_num = 0

    return sum(stack)

# Test
assert calculate("3+2*2") == 7
assert calculate(" 3/2 ") == 1
assert calculate(" 3+5 / 2 ") == 5
```
**Time: O(n), Space: O(n)**

---

### Challenge 10: Valid Parentheses - Generate All Combinations
Generate all valid parentheses combinations for n pairs.

```python
def generate_parenthesis(n):
    result = []

    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)

    backtrack("", 0, 0)
    return result

# Test
assert generate_parenthesis(3) == ["((()))","(()())","(())()","()(())","()()()"]
```
**Time: O(4^n / √n) Catalan number, Space: O(n)**

---

## Common Follow-Up Questions

1. **"Can you implement it without extra space?"** — For stacks, sometimes you can use the input itself. For queues with two stacks, amortized O(1) is achievable.
2. **"What about thread safety?"** — Use locks, or thread-safe collections like `queue.Queue`.
3. **"Can you make it O(1) for all operations?"** — Usually yes, but sometimes you need auxiliary space (e.g., min stack).
4. **"What's the difference between a stack and recursion?"** — Stack avoids recursion depth limits. Any recursive algorithm can be made iterative with a stack.
5. **"How would you handle very large inputs?"** — Use streaming/chunked processing. Monotonic stack/queue patterns are memory-efficient.

---

## Tips for Answering Stack/Queue Questions

1. **Identify the pattern:** Valid parentheses → stack, BFS → queue, next greater → monotonic stack.
2. **Trace through examples:** Walk through the algorithm with 3-5 elements.
3. **Consider edge cases:** Empty input, single element, all same elements, no valid answer.
4. **Think about the data structure:** Stack is for "matching" problems. Queue is for "order" problems.
5. **Use deques:** Python's `collections.deque` is O(1) for both ends, unlike `list.pop(0)`.
6. **Monotonic patterns:** If you need "next greater/smaller," think monotonic stack/queue.

---

## Complexity Cheat Sheet

| Problem | Time | Space |
|---------|------|-------|
| Valid Parentheses | O(n) | O(n) |
| Min Stack | O(1) all ops | O(n) |
| Next Greater Element | O(n) | O(n) |
| Daily Temperatures | O(n) | O(n) |
| Sliding Window Max | O(n) | O(k) |
| Largest Rectangle Histogram | O(n) | O(n) |
| Queue via Stacks | O(1) amortized | O(n) |
| Evaluate Postfix | O(n) | O(n) |
| Infix to Postfix | O(n) | O(n) |
| Decode String | O(n) | O(n) |
| Simplify Path | O(n) | O(n) |
| Basic Calculator | O(n) | O(n) |
