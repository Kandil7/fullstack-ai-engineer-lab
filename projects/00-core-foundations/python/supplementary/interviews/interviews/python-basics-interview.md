# Python Basics Interview Practice

## Overview

Python fundamentals form the backbone of any Python developer interview. This guide covers variables, data types, strings, collections, control flow, comprehensions, generators, and memory management. Master these concepts to ace technical screening rounds.

---

## Interview Questions

### Q1: What are the key differences between a list and a tuple in Python?

**Answer:**
Lists are mutable (can be modified after creation) while tuples are immutable (fixed after creation). Lists use square brackets `[]` and tuples use parentheses `()`. Because tuples are immutable, they are faster and can be used as dictionary keys. Lists consume more memory due to their dynamic nature.

```python
my_list = [1, 2, 3]
my_list[0] = 10  # Works - lists are mutable

my_tuple = (1, 2, 3)
my_tuple[0] = 10  # TypeError: 'tuple' does not support item assignment

# Tuples can be dict keys, lists cannot
my_dict = {(1, 2): "coordinates"}  # Valid
my_dict = {[1, 2]: "coordinates"}  # TypeError: unhashable type: 'list'
```

---

### Q2: Explain the difference between `==` and `is` operators.

**Answer:**
`==` checks for value equality (do the objects have the same value?), while `is` checks for identity (are they the exact same object in memory?).

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True - same values
print(a is b)  # False - different objects
print(a is c)  # True - same object

# Small integer caching (-5 to 256)
x = 256
y = 256
print(x is y)  # True - cached

x = 257
y = 257
print(x is y)  # May be False - depends on implementation
```

---

### Q3: What are Python's core data types?

**Answer:**
- **Numeric**: `int`, `float`, `complex`
- **Sequence**: `str`, `list`, `tuple`, `range`
- **Mapping**: `dict`
- **Set**: `set`, `frozenset`
- **Boolean**: `bool`
- **Binary**: `bytes`, `bytearray`, `memoryview`
- **None**: `NoneType`

```python
# Type checking
x = 42
print(type(x))        # <class 'int'>
print(isinstance(x, (int, float)))  # True
print(isinstance(x, str))           # False
```

---

### Q4: How does Python handle variable scoping (LEGB rule)?

**Answer:**
Python looks up variables in the following order: Local, Enclosing, Global, Built-in (LEGB).

```python
x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(x)      # local
    
    inner()
    print(x)          # enclosing

outer()
print(x)              # global

# Built-in example
print(len)            # <built-in function len>
```

---

### Q5: What are mutable and immutable types? Give examples.

**Answer:**
- **Immutable**: `int`, `float`, `str`, `tuple`, `frozenset`, `bytes` - cannot be modified after creation
- **Mutable**: `list`, `dict`, `set`, `bytearray` - can be modified in place

```python
# Immutable - creates new object
s = "hello"
s += " world"  # New string object created

# Mutable - modified in place
lst = [1, 2, 3]
lst.append(4)  # Same list object modified
```

---

### Q6: Explain string immutability and its implications.

**Answer:**
Strings in Python are immutable sequences of Unicode characters. Once created, they cannot be modified. Any "modification" creates a new string object.

```python
# String concatenation creates new objects
s1 = "hello"
s2 = s1 + " world"  # New string created

# String concatenation in loop is O(n^2)
result = ""
for s in ["a", "b", "c"]:
    result += s  # Creates new string each iteration - inefficient

# Better: use join()
result = "".join(["a", "b", "c"])  # O(n)
```

---

### Q7: What is the difference between `range()` and `xrange()` (Python 2)?

**Answer:**
In Python 2, `range()` returns a list, while `xrange()` returns an iterator (lazy evaluation). In Python 3, `range()` behaves like Python 2's `xrange()` - it's an iterator. This saves memory for large ranges.

```python
# Python 3 - range is an iterator
r = range(1000000)
print(type(r))    # <class 'range'>
print(sys.getsizeof(r))  # Small - doesn't store all values

# Use range() for iteration
for i in range(10):
    print(i)
```

---

### Q8: How do you swap two variables in Python?

**Answer:**
Python supports tuple unpacking, making variable swapping elegant and simple.

```python
# Method 1: Tuple unpacking (Pythonic)
a, b = 5, 10
a, b = b, a
print(a, b)  # 10 5

# Method 2: Using a temporary variable
a, b = 5, 10
temp = a
a = b
b = temp

# Method 3: XOR trick (for integers)
a, b = 5, 10
a ^= b
b ^= a
a ^= b
print(a, b)  # 10 5
```

---

### Q9: What are list comprehensions and when should you use them?

**Answer:**
List comprehensions provide a concise way to create lists. They are generally faster than equivalent for loops and are considered more Pythonic.

```python
# Basic syntax: [expression for item in iterable if condition]

# Traditional for loop
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x ** 2)

# List comprehension
squares = [x ** 2 for x in range(10) if x % 2 == 0]

# Nested comprehension
matrix = [[i * j for j in range(5)] for i in range(5)]

# Flatten matrix
flat = [x for row in matrix for x in row]
```

---

### Q10: Explain the difference between generators and iterators.

**Answer:**
An iterator is any object implementing `__iter__()` and `__next__()` methods. A generator is a special type of iterator created using a function with `yield` statements. Generators are lazy - they produce values on demand.

```python
# Iterator protocol
class CountDown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

# Generator function
def countdown(start):
    while start > 0:
        yield start
        start -= 1

# Generator expression
squares_gen = (x ** 2 for x in range(1000000))  # Memory efficient
```

---

### Q11: What are Python's truthy and falsy values?

**Answer:**
In Python, any object can be evaluated as True or False in a boolean context. Falsy values include: `False`, `None`, `0`, `0.0`, `""`, `()`, `[]`, `{}`, `set()`, `range(0)`. Everything else is truthy.

```python
# Falsy values
if not "":
    print("Empty string is falsy")

if not 0:
    print("Zero is falsy")

if not []:
    print("Empty list is falsy")

# Truthy values
if [0]:  # List with one element
    print("Non-empty list is truthy")

if " ":  # String with space
    print("Non-empty string is truthy")
```

---

### Q12: How does Python handle multiple assignments?

**Answer:**
Python supports simultaneous assignment, unpacking, and extended unpacking.

```python
# Multiple assignment
a = b = c = 0

# Unpacking
x, y, z = 1, 2, 3

# Extended unpacking with *
first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2, 3, 4], last=5

# Swapping with unpacking
a, b = b, a

# Unpacking in function calls
def func(a, b, c):
    return a + b + c

values = [1, 2, 3]
func(*values)  # Unpacks list as positional arguments
```

---

### Q13: What is the difference between `deepcopy` and `copy`?

**Answer:**
`copy` creates a shallow copy (new object but references to nested objects), while `deepcopy` recursively copies all nested objects.

```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

original[0][0] = 999
print(shallow)  # [[999, 2], [3, 4]] - affected
print(deep)     # [[1, 2], [3, 4]] - not affected

# For flat lists, shallow copy is sufficient
simple = [1, 2, 3]
shallow_simple = simple.copy()  # or simple[:]
```

---

### Q14: Explain Python's memory model for integers and string interning.

**Answer:**
Python caches small integers (-5 to 256) and interns some strings for optimization. This means identical immutable values may reference the same object in memory.

```python
# Integer caching
a = 256
b = 256
print(a is b)  # True - cached

a = 257
b = 257
print(a is b)  # False - not cached (implementation dependent)

# String interning
s1 = "hello"
s2 = "hello"
print(s1 is s2)  # True - interned

s1 = "hello world!"
s2 = "hello world!"
print(s1 is s2)  # May be False - not interned

# Force interning
import sys
s1 = sys.intern("hello world!")
s2 = sys.intern("hello world!")
print(s1 is s2)  # True
```

---

### Q15: What are walrus operator (`:=`) and its use cases?

**Answer:**
The walrus operator (:=) assigns a value to a variable as part of an expression. Introduced in Python 3.8, it's useful in list comprehensions and while loops.

```python
# Without walrus operator
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = []
for x in data:
    if x % 2 == 0:
        result.append(x ** 2)

# With walrus operator in list comprehension
result = [y for x in data if x % 2 == 0 and (y := x ** 2)]

# Useful in while loops
while (line := input("Enter: ")) != "quit":
    print(f"You entered: {line}")

# In if statements
if (n := len(data)) > 5:
    print(f"List has {n} elements")
```

---

## Coding Challenges

### Challenge 1: Reverse a String Without Slicing

**Problem:** Write a function that reverses a string without using slicing or the `reversed()` built-in.

**Solution:**
```python
def reverse_string(s):
    result = ""
    for char in s:
        result = char + result
    return result

# Or using join
def reverse_string_v2(s):
    return "".join(s[i] for i in range(len(s) - 1, -1, -1))

# Recursive approach
def reverse_string_v3(s):
    if len(s) <= 1:
        return s
    return reverse_string_v3(s[1:]) + s[0]
```

---

### Challenge 2: Find Duplicates in a List

**Problem:** Find all duplicate elements in a list.

**Solution:**
```python
def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)

# Alternative using Counter
from collections import Counter

def find_duplicates_v2(lst):
    counts = Counter(lst)
    return [item for item, count in counts.items() if count > 1]

# Test
print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))  # [2, 3]
```

---

### Challenge 3: Flatten a Nested List

**Problem:** Write a function to flatten arbitrarily nested lists.

**Solution:**
```python
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# Generator version (memory efficient)
def flatten_gen(lst):
    for item in lst:
        if isinstance(item, list):
            yield from flatten_gen(item)
        else:
            yield item

# Test
nested = [1, [2, 3], [4, [5, 6]], 7]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6, 7]
```

---

### Challenge 4: Implement a FizzBuzz Generator

**Problem:** Create a generator that yields FizzBuzz values for a given range.

**Solution:**
```python
def fizzbuzz(start, end):
    for i in range(start, end + 1):
        if i % 15 == 0:
            yield "FizzBuzz"
        elif i % 3 == 0:
            yield "Fizz"
        elif i % 5 == 0:
            yield "Buzz"
        else:
            yield i

# Alternative using tuple unpacking
def fizzbuzz_v2(start, end):
    for i in range(start, end + 1):
        result = ""
        if i % 3 == 0:
            result += "Fizz"
        if i % 5 == 0:
            result += "Buzz"
        yield result or i

# Test
for val in fizzbuzz(1, 15):
    print(val)
```

---

### Challenge 5: Word Frequency Counter

**Problem:** Count the frequency of each word in a sentence, ignoring case.

**Solution:**
```python
def word_frequency(sentence):
    words = sentence.lower().split()
    freq = {}
    for word in words:
        # Remove punctuation
        word = word.strip(".,!?;:")
        freq[word] = freq.get(word, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

# Using collections.Counter
from collections import Counter

def word_frequency_v2(sentence):
    words = sentence.lower().split()
    words = [w.strip(".,!?;:") for w in words]
    return dict(Counter(words).most_common())

# Test
text = "The cat sat on the mat. The cat liked the mat."
print(word_frequency(text))
# {'the': 4, 'cat': 2, 'mat': 2, 'sat': 1, 'on': 1, 'liked': 1}
```

---

### Challenge 6: Matrix Transposition

**Problem:** Transpose a matrix (2D list) without using NumPy.

**Solution:**
```python
def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

# Using zip
def transpose_v2(matrix):
    return [list(row) for row in zip(*matrix)]

# Manual approach
def transpose_v3(matrix):
    rows, cols = len(matrix), len(matrix[0])
    result = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result

# Test
matrix = [[1, 2, 3], [4, 5, 6]]
print(transpose(matrix))
# [[1, 4], [2, 5], [3, 6]]
```

---

### Challenge 7: Remove Duplicates While Preserving Order

**Problem:** Remove duplicates from a list while maintaining the original order of first occurrences.

**Solution:**
```python
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Using dict.fromkeys (Python 3.7+ preserves order)
def remove_duplicates_v2(lst):
    return list(dict.fromkeys(lst))

# Test
print(remove_duplicates([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]))
# [3, 1, 4, 5, 9, 2, 6]
```

---

### Challenge 8: Group Anagrams

**Problem:** Group a list of words by their anagram groups.

**Solution:**
```python
def group_anagrams(words):
    anagram_dict = {}
    for word in words:
        sorted_word = "".join(sorted(word.lower()))
        anagram_dict.setdefault(sorted_word, []).append(word)
    return list(anagram_dict.values())

# Alternative using defaultdict
from collections import defaultdict

def group_anagrams_v2(words):
    anagram_dict = defaultdict(list)
    for word in words:
        sorted_word = "".join(sorted(word.lower()))
        anagram_dict[sorted_word].append(word)
    return list(anagram_dict.values())

# Test
words = ["listen", "silent", "enlist", "rat", "tar", "art"]
print(group_anagrams(words))
# [['listen', 'silent', 'enlist'], ['rat', 'tar', 'art']]
```

---

## Common Follow-up Questions

1. **"Can you explain why list comprehensions are faster than for loops?"**
   - List comprehensions are optimized at the C level in CPython
   - They avoid the overhead of repeated `.append()` method lookups
   - The bytecode generated is more efficient

2. **"When would you use a tuple instead of a list?"**
   - When data shouldn't change (immutable guarantee)
   - When using as dictionary keys
   - When returning multiple values from functions
   - When performance matters (tuples are slightly faster)

3. **"How do generators help with memory efficiency?"**
   - Generators yield one item at a time instead of storing all items
   - Useful for processing large datasets or infinite sequences
   - Can be chained together for pipeline processing

4. **"What happens if you modify a list while iterating over it?"**
   - Can lead to unexpected behavior - items may be skipped or repeated
   - Use a copy or build a new list instead
   - List comprehensions are safer for filtering

5. **"How does Python's garbage collection work?"**
   - Uses reference counting as primary mechanism
   - Has a cyclic garbage collector for reference cycles
   - Objects are freed when reference count reaches zero
   - `gc` module can be used to interact with the collector

---

## Tips for Answering

1. **Be specific** - Give concrete examples, not just definitions
2. **Mention trade-offs** - Every design choice has pros and cons
3. **Know the "why"** - Don't just memorize syntax; understand the reasoning
4. **Practice live coding** - Be comfortable writing code on a whiteboard or in an editor
5. **Discuss edge cases** - Mention empty inputs, single elements, and boundary conditions
6. **Know time/space complexity** - Be ready to discuss Big O notation
7. **Use proper terminology** - Show you understand concepts like "mutable," "immutable," "lazy evaluation"
8. **Ask clarifying questions** - Understand what the interviewer is really asking
9. **Consider Python versions** - Mention if behavior differs between Python 2 and 3
10. **Stay calm and think aloud** - Walk through your thought process

---

## Key Concepts to Review

| Concept | Key Points |
|---------|-----------|
| Mutability | Mutable (list, dict, set) vs Immutable (int, str, tuple) |
| Scope | LEGB rule for variable lookup |
| Identity | `is` vs `==` operators |
| Comprehensions | Concise list/dict/set/generator creation |
| Generators | Lazy evaluation, yield, memory efficiency |
| Iterators | `__iter__`, `__next__`, StopIteration |
| Interning | Small integer cache, string interning |
| Shallow vs Deep Copy | Reference copying vs recursive copying |

---

*Practice these questions regularly and always explain your reasoning. Good luck with your interview!*