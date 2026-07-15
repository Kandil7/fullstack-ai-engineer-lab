"""
DSA Tutorial 03 - Stacks
========================

Stack: Last In, First Out (LIFO)
Think of a stack of plates - you add/remove from the top.

Operations:
- push: Add to top    O(1)
- pop: Remove from top  O(1)
- peek: View top       O(1)
- is_empty: Check       O(1)
- size: Count elements  O(1)
"""

# =============================================================================
# 1. STACK IMPLEMENTATION USING LIST
# =============================================================================

class Stack:
    """Stack implementation using Python list"""

    def __init__(self):
        self.items = []

    def push(self, item):
        """Add item to top. O(1)"""
        self.items.append(item)

    def pop(self):
        """Remove and return top item. O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()

    def peek(self):
        """View top item without removing. O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]

    def is_empty(self):
        """Check if stack is empty. O(1)"""
        return len(self.items) == 0

    def size(self):
        """Return number of items. O(1)"""
        return len(self.items)

    def __str__(self):
        return f"Stack({self.items})"

    def __repr__(self):
        return self.__str__()


print("=== Stack Using List ===")
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(f"Push 1, 2, 3: {stack}")
print(f"Peek: {stack.peek()}")
print(f"Pop: {stack.pop()}")
print(f"After pop: {stack}")
print(f"Size: {stack.size()}")


# =============================================================================
# 2. STACK IMPLEMENTATION USING LINKED LIST
# =============================================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedStack:
    """Stack using linked list - no capacity limit"""

    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, item):
        """Add to top. O(1)"""
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self):
        """Remove from top. O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self):
        """View top. O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.top.data

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size

    def __str__(self):
        items = []
        current = self.top
        while current:
            items.append(str(current.data))
            current = current.next
        return " -> ".join(items) + " -> None"


print("\n=== Stack Using Linked List ===")
linked_stack = LinkedStack()
linked_stack.push(10)
linked_stack.push(20)
linked_stack.push(30)
print(f"Stack: {linked_stack}")
print(f"Pop: {linked_stack.pop()}")
print(f"After pop: {linked_stack}")


# =============================================================================
# 3. BRACKET MATCHING
# =============================================================================

def is_balanced_brackets(expression):
    """Check if brackets are balanced. O(n) time."""
    stack = Stack()
    matching = {')': '(', ']': '[', '}': '{'}

    for char in expression:
        if char in '([{':
            stack.push(char)
        elif char in ')]}':
            if stack.is_empty() or stack.pop() != matching[char]:
                return False
    return stack.is_empty()

print("\n=== Bracket Matching ===")
tests = [
    "((1 + 2) * 3)",
    "{[a + b] * (c - d)}",
    "((a + b)",
    "a + b]",
    "[{()}]",
    ""
]
for expr in tests:
    result = is_balanced_brackets(expr)
    print(f"'{expr}': {'Balanced' if result else 'Not balanced'}")


# =============================================================================
# 4. PREFIX EVALUATION
# =============================================================================

def evaluate_prefix(expression):
    """Evaluate prefix expression. O(n) time."""
    stack = Stack()
    tokens = expression.split()

    for token in reversed(tokens):
        if token in '+-*/':
            a = stack.pop()
            b = stack.pop()
            if token == '+':
                stack.push(a + b)
            elif token == '-':
                stack.push(a - b)
            elif token == '*':
                stack.push(a * b)
            elif token == '/':
                stack.push(a / b)
        else:
            stack.push(float(token))

    return stack.pop()

print("\n=== Prefix Evaluation ===")
print(f"+ 3 * 4 5 = {evaluate_prefix('+ 3 * 4 5')}")  # 3 + (4 * 5) = 23
print(f"* + 3 4 5 = {evaluate_prefix('* + 3 4 5')}")  # (3 + 4) * 5 = 35


# =============================================================================
# 5. POSTFIX EVALUATION
# =============================================================================

def evaluate_postfix(expression):
    """Evaluate postfix expression. O(n) time."""
    stack = Stack()
    tokens = expression.split()

    for token in tokens:
        if token in '+-*/':
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.push(a + b)
            elif token == '-':
                stack.push(a - b)
            elif token == '*':
                stack.push(a * b)
            elif token == '-':
                stack.push(a / b)
        else:
            stack.push(float(token))

    return stack.pop()

print("\n=== Postfix Evaluation ===")
print(f"3 4 5 * + = {evaluate_postfix('3 4 5 * +')}")  # 3 + (4 * 5) = 23
print(f"3 4 + 5 * = {evaluate_postfix('3 4 + 5 *')}")  # (3 + 4) * 5 = 35


# =============================================================================
# 6. INFIX TO POSTFIX CONVERSION
# =============================================================================

def infix_to_postfix(expression):
    """Convert infix to postfix. O(n) time."""
    stack = Stack()
    output = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    right_associative = {'^'}

    tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()

    for token in tokens:
        if token.isalnum():
            output.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                output.append(stack.pop())
            if not stack.is_empty():
                stack.pop()  # Remove '('
        else:  # Operator
            while (not stack.is_empty() and
                   stack.peek() != '(' and
                   stack.peek() in precedence and
                   (precedence[stack.peek()] > precedence[token] or
                    (precedence[stack.peek()] == precedence[token] and
                     token not in right_associative))):
                output.append(stack.pop())
            stack.push(token)

    while not stack.is_empty():
        output.append(stack.pop())

    return ' '.join(output)

print("\n=== Infix to Postfix ===")
expressions = [
    "A + B * C",
    "( A + B ) * C",
    "A + B * C - D / E",
    "( A + B ) * ( C - D )",
]
for expr in expressions:
    postfix = infix_to_postfix(expr)
    print(f"{expr} -> {postfix}")


# =============================================================================
# 7. REVERSE A STRING USING STACK
# =============================================================================

def reverse_string(s):
    """Reverse string using stack. O(n) time, O(n) space."""
    stack = Stack()
    for char in s:
        stack.push(char)

    reversed_str = ""
    while not stack.is_empty():
        reversed_str += stack.pop()
    return reversed_str

print("\n=== Reverse String ===")
print(f"reverse('Hello World') = '{reverse_string('Hello World')}'")


# =============================================================================
# 8. NEXT GREATER ELEMENT
# =============================================================================

def next_greater_element(arr):
    """Find next greater element for each item. O(n) time."""
    n = len(arr)
    result = [-1] * n
    stack = Stack()

    for i in range(n):
        while not stack.is_empty() and arr[stack.peek()] < arr[i]:
            result[stack.pop()] = arr[i]
        stack.push(i)

    return result

print("\n=== Next Greater Element ===")
arr = [4, 5, 2, 25, 7, 8]
print(f"Array: {arr}")
print(f"Next greater: {next_greater_element(arr)}")


# =============================================================================
# 9. MINIMUM STACK
# =============================================================================

class MinStack:
    """Stack that supports getMin in O(1)"""

    def __init__(self):
        self.stack = Stack()
        self.min_stack = Stack()

    def push(self, item):
        self.stack.push(item)
        if self.min_stack.is_empty() or item <= self.min_stack.peek():
            self.min_stack.push(item)

    def pop(self):
        if self.stack.is_empty():
            raise IndexError("Stack is empty")
        item = self.stack.pop()
        if item == self.min_stack.peek():
            self.min_stack.pop()
        return item

    def get_min(self):
        if self.min_stack.is_empty():
            raise IndexError("Stack is empty")
        return self.min_stack.peek()

print("\n=== Minimum Stack ===")
min_stack = MinStack()
min_stack.push(5)
min_stack.push(3)
min_stack.push(7)
min_stack.push(1)
print(f"Push 5, 3, 7, 1")
print(f"Current min: {min_stack.get_min()}")
min_stack.pop()
print(f"After pop: min = {min_stack.get_min()}")


# =============================================================================
# 10. STACK SORT
# =============================================================================

def sort_stack(stack):
    """Sort a stack using another stack. O(n^2) time."""
    temp_stack = Stack()

    while not stack.is_empty():
        temp = stack.pop()
        while not temp_stack.is_empty() and temp_stack.peek() > temp:
            stack.push(temp_stack.pop())
        temp_stack.push(temp)

    while not temp_stack.is_empty():
        stack.push(temp_stack.pop())

    return stack

print("\n=== Stack Sort ===")
unsorted_stack = Stack()
for val in [34, 3, 31, 98, 92, 23]:
    unsorted_stack.push(val)

print("Before sort (top to bottom):", end=" ")
temp = Stack()
items = []
while not unsorted_stack.is_empty():
    items.append(str(unsorted_stack.pop()))
print(" ".join(items))

# Re-push for sorting
for val in [34, 3, 31, 98, 92, 23]:
    unsorted_stack.push(val)

sorted_stack = sort_stack(unsorted_stack)
items = []
while not sorted_stack.is_empty():
    items.append(str(sorted_stack.pop()))
print(f"After sort (top to bottom): {' '.join(items)}")


# =============================================================================
# 11. DECIMAL TO BINARY
# =============================================================================

def decimal_to_binary(n):
    """Convert decimal to binary using stack. O(log n) time."""
    if n == 0:
        return "0"

    stack = Stack()
    while n > 0:
        stack.push(n % 2)
        n //= 2

    binary = ""
    while not stack.is_empty():
        binary += str(stack.pop())
    return binary

print("\n=== Decimal to Binary ===")
for num in [10, 25, 100, 255]:
    print(f"{num} -> {decimal_to_binary(num)}")


# =============================================================================
# 12. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Stacks - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Stack is LIFO (Last In, First Out)")
    print("2. All operations are O(1)")
    print("3. Great for: bracket matching, undo/redo, expression evaluation")
    print("4. Used in: DFS, backtracking, function call stack")
    print("5. MinStack supports O(1) minimum lookup")
