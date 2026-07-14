# Python Data Structures Interview Practice

## Overview

Data structures are fundamental to programming efficiency. This guide covers Python's built-in data structures, their optimal use cases, time complexity analysis, custom implementations, and advanced patterns. Master these to make informed design decisions in interviews.

---

## Interview Questions

### Q1: Compare the time complexity of list, set, dict, and tuple operations.

**Answer:**
Understanding Big O notation for data structure operations is crucial for choosing the right structure.

| Operation | list | tuple | set | dict |
|-----------|------|-------|-----|------|
| Access by index | O(1) | O(1) | N/A | O(1) |
| Search | O(n) | O(n) | O(1) | O(1) |
| Insert | O(n) | N/A | O(1) | O(1) |
| Delete | O(n) | N/A | O(1) | O(1) |
| Append | O(1)* | N/A | N/A | N/A |

*Amortized O(1) for list append

```python
import time

# Demonstrating performance difference
data = list(range(1000000))
data_set = set(data)
data_dict = {i: i for i in data}

# Search comparison
start = time.time()
999999 in data       # O(n)
list_time = time.time() - start

start = time.time()
999999 in data_set   # O(1)
set_time = time.time() - start

print(f"List search: {list_time:.6f}s")
print(f"Set search: {set_time:.6f}s")
```

---

### Q2: When should you use each data structure?

**Answer:**
- **List**: Ordered, mutable sequence; use when order matters and you need duplicates
- **Tuple**: Ordered, immutable sequence; use for fixed collections, dict keys, function returns
- **Set**: Unordered, mutable, unique elements; use for membership testing, deduplication
- **Dict**: Key-value pairs; use for fast lookups, structured data

```python
# List - when order and duplicates matter
task_queue = ["task1", "task2", "task1", "task3"]

# Tuple - when data shouldn't change
RGB_COLOR = (255, 128, 0)
COORDINATES = (40.7128, -74.0060)

# Set - when you need uniqueness and fast lookup
unique_users = {"alice", "bob", "charlie"}
if "alice" in unique_users:  # O(1) lookup
    print("User exists")

# Dict - when you need key-value mapping
user_scores = {"alice": 95, "bob": 87, "charlie": 92}
```

---

### Q3: Explain dictionary internals and hash tables.

**Answer:**
Python dictionaries use hash tables with open addressing for collision resolution.

```python
# How hashing works
hash("hello")      # Hash value
hash((1, 2, 3))   # Hashable types
# hash([1, 2, 3]) # TypeError: unhashable type

# Dictionary internals
d = {}
print(d.__sizeof__())  # Small initial size

# Adding elements triggers resizing
for i in range(100):
    d[i] = i
    if i % 20 == 0:
        print(f"Size after {i} items: {d.__sizeof__()} bytes")

# Python 3.6+ dicts maintain insertion order
# (implementation detail, not guaranteed by spec)
```

---

### Q4: What are defaultdict and OrderedDict?

**Answer:**
`defaultdict` provides default values for missing keys. `OrderedDict` maintains insertion order (in Python 3.7+, regular dicts do too, but OrderedDict has extra methods).

```python
from collections import defaultdict, OrderedDict

# defaultdict - eliminates KeyError
word_count = defaultdict(int)
words = ["hello", "world", "hello", "python"]
for word in words:
    word_count[word] += 1
print(dict(word_count))  # {'hello': 2, 'world': 1, 'python': 1}

# Grouping with defaultdict
students = [("Alice", "Math"), ("Bob", "Science"), ("Alice", "Science")]
by_student = defaultdict(list)
for name, subject in students:
    by_student[name].append(subject)
print(dict(by_student))  # {'Alice': ['Math', 'Science'], 'Bob': ['Science']}

# OrderedDict - explicit ordering with extra features
od = OrderedDict()
od["first"] = 1
od["second"] = 2
od.move_to_end("first")  # Move to end
print(list(od.keys()))   # ['second', 'first']
```

---

### Q5: Explain list vs deque for queue operations.

**Answer:**
`list` is inefficient for queue operations (O(n) for front operations), while `deque` is optimized for O(1) operations at both ends.

```python
from collections import deque
import time

# List as queue - SLOW
start = time.time()
queue_list = []
for i in range(100000):
    queue_list.append(i)      # O(1)
    _ = queue_list.pop(0)     # O(n) - shifts all elements
list_time = time.time() - start

# Deque as queue - FAST
start = time.time()
queue_deque = deque()
for i in range(100000):
    queue_deque.append(i)     # O(1)
    _ = queue_deque.popleft() # O(1)
deque_time = time.time() - start

print(f"List queue: {list_time:.4f}s")
print(f"Deque queue: {deque_time:.4f}s")

# Deque also supports maxlen
recent = deque(maxlen=3)
recent.append(1)
recent.append(2)
recent.append(3)
recent.append(4)  # Auto-removes 1
print(recent)     # deque([2, 3, 4])
```

---

### Q6: What are Counter and ChainMap?

**Answer:**
`Counter` is a dict subclass for counting hashable objects. `ChainMap` groups multiple dicts into a single view.

```python
from collections import Counter, ChainMap

# Counter - counting and statistics
text = "hello world hello python world hello"
word_count = Counter(text.split())
print(word_count.most_common(2))  # [('hello', 3), ('world', 2)]
print(word_count["missing"])      # 0 (no KeyError)

# Counter arithmetic
a = Counter(["x", "y", "x"])
b = Counter(["x", "z"])
print(a + b)  # Counter({'x': 3, 'y': 1, 'z': 1})
print(a - b)  # Counter({'y': 1})

# ChainMap - unified view of multiple dicts
defaults = {"color": "red", "user": "guest"}
environment = {"user": "admin"}
config = ChainMap(environment, defaults)
print(config["user"])     # admin (first found)
print(config["color"])    # red (from defaults)
```

---

### Q7: When would you use a frozenset?

**Answer:**
`frozenset` is an immutable set that can be used as dictionary keys or elements of another set.

```python
# As dictionary key
distances = {
    frozenset(["A", "B"]): 100,
    frozenset(["B", "C"]): 150,
}

# As element of a set (sets can't contain regular sets)
set_of_sets = {
    frozenset([1, 2]),
    frozenset([3, 4]),
    frozenset([1, 2]),  # Duplicate removed
}
print(len(set_of_sets))  # 2

# Can't modify
fs = frozenset([1, 2, 3])
# fs.add(4)  # AttributeError: 'frozenset' object has no attribute 'add'

# Useful for caching/memoization keys
def compute(input_set):
    frozen = frozenset(input_set)
    if frozen in cache:
        return cache[frozen]
    # ... compute result
```

---

### Q8: Explain heapq and when to use it.

**Answer:**
`heapq` provides a min-heap implementation for priority queue operations.

```python
import heapq

# Min-heap
heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 4)
heapq.heappush(heap, 2)

print(heapq.heappop(heap))  # 1 (smallest first)
print(heapq.heappop(heap))  # 2

# Convert list to heap in O(n)
data = [5, 2, 8, 1, 9]
heapq.heapify(data)  # In-place transformation

# Get n largest/smallest
nums = [4, 1, 7, 3, 8, 2]
print(heapq.nlargest(3, nums))   # [8, 7, 4]
print(heapq.nsmallest(2, nums))  # [1, 2]

# Priority queue pattern
tasks = []
heapq.heappush(tasks, (1, "High priority"))
heapq.heappush(tasks, (3, "Low priority"))
heapq.heappush(tasks, (2, "Medium priority"))

while tasks:
    priority, task = heapq.heappop(tasks)
    print(f"Processing: {task}")
```

---

### Q9: What are namedtuples and when are they useful?

**Answer:**
`namedtuples` are immutable, named versions of tuples that provide both index and attribute access.

```python
from collections import namedtuple

# Creating a namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)

print(p.x, p.y)      # 1 2 (attribute access)
print(p[0], p[1])     # 1 2 (index access)
print(p)              # Point(x=1, y=2)

# Useful for returning multiple values with names
def get_user_info():
    User = namedtuple("User", ["name", "email", "age"])
    return User("Alice", "alice@example.com", 30)

user = get_user_info()
print(f"{user.name} is {user.age}")

# Replace fields (creates new instance)
p2 = p._replace(x=10)
print(p2)  # Point(x=10, y=2)

# As dict key (immutable)
locations = {Point(0, 0): "origin", Point(1, 1): "unit"}
```

---

### Q10: Explain the bisect module.

**Answer:**
`bisect` provides binary search functions for maintaining sorted lists.

```python
import bisect

# Maintaining a sorted list
sorted_list = [1, 3, 5, 7, 9]

# Find insertion point
pos = bisect.bisect_left(sorted_list, 4)  # 2 (between 3 and 5)
pos = bisect.bisect_right(sorted_list, 3)  # 2 (after 3)

# Insert maintaining order
bisect.insort(sorted_list, 4)
print(sorted_list)  # [1, 3, 4, 5, 7, 9]

# Binary search
def find_closest(sorted_arr, target):
    pos = bisect.bisect_left(sorted_arr, target)
    if pos == 0:
        return sorted_arr[0]
    if pos == len(sorted_arr):
        return sorted_arr[-1]
    before = sorted_arr[pos - 1]
    after = sorted_arr[pos]
    if target - before < after - target:
        return before
    return after

nums = [1, 3, 5, 7, 9]
print(find_closest(nums, 4))  # 3
print(find_closest(nums, 6))  # 5
```

---

### Q11: When would you use array.array instead of list?

**Answer:**
`array.array` is more memory-efficient for homogeneous numeric data but less flexible than lists.

```python
import array
import sys

# List of integers
list_ints = [i for i in range(1000)]
print(f"List: {sys.getsizeof(list_ints)} bytes")

# Array of integers
array_ints = array.array('i', range(1000))
print(f"Array: {sys.getsizeof(array_ints)} bytes")

# Array operations
arr = array.array('i', [1, 2, 3, 4, 5])
arr.append(6)
arr.extend([7, 8])
print(arr)  # array('i', [1, 2, 3, 4, 5, 6, 7, 8])

# Type codes
# 'i' - signed int (4 bytes)
# 'f' - float (4 bytes)
# 'd' - double (8 bytes)
# 'b' - signed char (1 byte)
```

---

### Q12: Explain dict comprehensions and when to use them.

**Answer:**
Dict comprehensions provide a concise way to create dictionaries, similar to list comprehensions.

```python
# Basic dict comprehension
squares = {x: x**2 for x in range(10)}
print(squares)  # {0: 0, 1: 1, 2: 4, ...}

# With condition
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# Inverting a dictionary
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)  # {1: "a", 2: "b", 3: "c"}

# From two lists
keys = ["name", "age", "city"]
values = ["Alice", 30, "NYC"]
combined = {k: v for k, v in zip(keys, values)}
print(combined)  # {'name': 'Alice', 'age': 30, 'city': 'NYC'}

# Nested dict comprehension
matrix = {(i, j): i * j for i in range(3) for j in range(3)}
print(matrix)  # {(0, 0): 0, (0, 1): 0, ...}
```

---

### Q13: What is the time complexity of common operations?

**Answer:**
Understanding Big O helps you choose the right data structure.

```python
# List operations
# append: O(1) amortized
# pop(): O(1)
# pop(0): O(n)
# insert(0, x): O(n)
# remove(x): O(n)
# x in list: O(n)

# Dict operations
# get/set: O(1) average, O(n) worst case
# del: O(1) average
# x in dict: O(1) average

# Set operations
# add: O(1)
# remove: O(1)
# x in set: O(1)
# union: O(len(a) + len(b))
# intersection: O(min(len(a), len(b)))

# Example: Finding common elements
list1 = list(range(10000))
list2 = list(range(5000, 15000))

# Bad: O(n*m)
common_bad = [x for x in list1 if x in list2]

# Good: O(n+m)
common_good = set(list1).intersection(set(list2))
```

---

### Q14: Explain WeakValueDictionary and WeakSet.

**Answer:**
Weak references allow garbage collection of objects even when referenced.

```python
import weakref

class Data:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Data({self.value})"

# WeakValueDictionary
cache = weakref.WeakValueDictionary()
obj1 = Data(1)
cache["key1"] = obj1  # Weak reference

print(cache["key1"])  # Data(1)
del obj1              # Object can be garbage collected
print("key1" in cache)  # False (reference gone)

# WeakSet
ws = weakref.WeakSet()
obj2 = Data(2)
ws.add(obj2)
print(len(ws))  # 1
del obj2
print(len(ws))  # 0

# Useful for caches and observers that shouldn't prevent cleanup
```

---

### Q15: What are sets and when should you use them?

**Answer:**
Sets are unordered collections of unique elements, optimized for membership testing and mathematical operations.

```python
# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)   # Union: {1, 2, 3, 4, 5, 6}
print(a & b)   # Intersection: {3, 4}
print(a - b)   # Difference: {1, 2}
print(a ^ b)   # Symmetric difference: {1, 2, 5, 6}

# Practical uses
# 1. Remove duplicates
emails = ["a@test.com", "b@test.com", "a@test.com"]
unique_emails = list(set(emails))

# 2. Membership testing (O(1) vs O(n) for lists)
valid_codes = {100, 200, 300, 400, 500}
if 200 in valid_codes:  # O(1)
    print("Valid")

# 3. List difference
all_users = {"alice", "bob", "charlie", "david"}
premium_users = {"alice", "charlie"}
regular_users = all_users - premium_users  # {'bob', 'david'}

# 4. Data validation
required_fields = {"name", "email", "password"}
provided_fields = {"name", "email"}
missing = required_fields - provided_fields  # {'password'}
```

---

## Coding Challenges

### Challenge 1: Find Two Numbers That Sum to Target

**Problem:** Given a list of numbers and a target, find two numbers that add up to the target.

**Solution:**
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Test
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
print(two_sum([3, 2, 4], 6))        # [1, 2]

# Time: O(n), Space: O(n)
```

---

### Challenge 2: Group Anagrams Together

**Problem:** Group strings that are anagrams of each other.

**Solution:**
```python
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for word in words:
        # Sort characters to create key
        key = "".join(sorted(word.lower()))
        groups[key].append(word)
    return list(groups.values())

# Test
words = ["listen", "silent", "enlist", "rat", "tar", "art"]
print(group_anagrams(words))
# [['listen', 'silent', 'enlist'], ['rat', 'tar', 'art']]

# Time: O(n * k log k), Space: O(n * k)
```

---

### Challenge 3: Implement a Fixed-Size Cache

**Problem:** Implement an LRU cache with O(1) get and put operations.

**Solution:**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# Test
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))    # 1
cache.put(3, 3)        # Evicts key 2
print(cache.get(2))    # -1
```

---

### Challenge 4: Merge Two Sorted Lists

**Problem:** Merge two sorted lists into a single sorted list.

**Solution:**
```python
def merge_sorted(list1, list2):
    result = []
    i = j = 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    
    result.extend(list1[i:])
    result.extend(list2[j:])
    return result

# Alternative using heapq
import heapq

def merge_sorted_heapq(list1, list2):
    return list(heapq.merge(list1, list2))

# Test
print(merge_sorted([1, 3, 5], [2, 4, 6]))  # [1, 2, 3, 4, 5, 6]

# Time: O(n + m), Space: O(n + m)
```

---

### Challenge 5: Find Majority Element

**Problem:** Find the element that appears more than n/2 times in a list.

**Solution:**
```python
def majority_element(nums):
    # Boyer-Moore Voting Algorithm
    candidate = None
    count = 0
    
    for num in nums:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1
    
    # Verify (optional if majority guaranteed)
    if nums.count(candidate) > len(nums) // 2:
        return candidate
    return None

# Alternative using Counter
from collections import Counter

def majority_element_counter(nums):
    counts = Counter(nums)
    for num, count in counts.items():
        if count > len(nums) // 2:
            return num

# Test
print(majority_element([3, 3, 4]))      # 3
print(majority_element([2, 2, 1, 1, 1]))  # 1

# Time: O(n), Space: O(1)
```

---

### Challenge 6: Implement a Trie

**Problem:** Implement a trie (prefix tree) for storing and searching words.

**Solution:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def autocomplete(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        results = []
        self._dfs(node, prefix, results)
        return results
    
    def _dfs(self, node, path, results):
        if node.is_end:
            results.append(path)
        for char, child in node.children.items():
            self._dfs(child, path + char, results)

# Test
trie = Trie()
trie.insert("apple")
trie.insert("app")
trie.insert("application")
trie.insert("banana")

print(trie.search("apple"))        # True
print(trie.starts_with("app"))     # True
print(trie.autocomplete("app"))    # ['app', 'apple', 'application']
```

---

### Challenge 7: Find All Duplicates in Array

**Problem:** Find all elements that appear more than once in an array where elements are between 1 and n.

**Solution:**
```python
def find_duplicates(nums):
    result = []
    for num in nums:
        index = abs(num) - 1
        if nums[index] < 0:
            result.append(abs(num))
        else:
            nums[index] = -nums[index]
    return result

# Alternative using Counter
from collections import Counter

def find_duplicates_counter(nums):
    return [num for num, count in Counter(nums).items() if count > 1]

# Test
print(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1]))  # [2, 3]

# Time: O(n), Space: O(1) for first approach
```

---

### Challenge 8: Implement a Min Stack

**Problem:** Implement a stack that supports push, pop, top, and retrieving the minimum element in O(1).

**Solution:**
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

# Test
ms = MinStack()
ms.push(-2)
ms.push(0)
ms.push(-3)
print(ms.get_min())  # -3
ms.pop()
print(ms.top())      # 0
print(ms.get_min())  # -2
```

---

## Common Follow-up Questions

1. **"When would you use a list vs a tuple?"**
   - List: mutable, dynamic size, for collections that change
   - Tuple: immutable, fixed size, for fixed records, dict keys

2. **"How do you choose between set and list for membership testing?"**
   - Set: O(1) lookup, no duplicates, unordered
   - List: O(n) lookup, allows duplicates, ordered
   - Use set if you only need "is it there?" checks

3. **"Explain the difference between shallow and deep copy for data structures"**
   - Shallow copy: new container, references to original objects
   - Deep copy: new container, recursive copies of all objects
   - Use deep copy for nested mutable structures

4. **"When would you use collections.namedtuple vs a regular class?"**
   - namedtuple: immutable, memory-efficient, quick to create
   - Class: mutable, methods, more complex initialization
   - Use namedtuple for simple data records

5. **"How do dictionaries handle hash collisions?"**
   - Python uses open addressing (specifically, a probing sequence)
   - When collision occurs, checks next slot until empty slot found
   - Load factor triggers resize when ~2/3 full

---

## Tips for Answering

1. **Know time complexities** - Be ready to state Big O for common operations
2. **Choose based on requirements** - Consider mutability, ordering, performance
3. **Use built-ins** - Python has powerful tools (Counter, defaultdict, deque)
4. **Think about memory** - Consider space-time tradeoffs
5. **Practice implementations** - Be able to implement basic data structures from scratch
6. **Know the edge cases** - Empty collections, single elements, duplicates
7. **Discuss trade-offs** - No single "best" structure for all cases
8. **Use type hints** - Show understanding of data types
9. **Consider thread safety** - Some structures are not thread-safe
10. **Stay updated** - Python's collections module adds new utilities

---

## Key Concepts to Review

| Concept | Key Points |
|---------|-----------|
| Lists | Mutable, ordered, O(1) append, O(n) search |
| Tuples | Immutable, ordered, hashable, memory-efficient |
| Sets | Unordered, unique, O(1) lookup, set operations |
| Dicts | Key-value, O(1) lookup, hash table implementation |
| Deque | Double-ended queue, O(1) both ends |
| Counter | Counting hashable objects, most_common() |
| defaultdict | Default values, eliminate KeyError |
| heapq | Min-heap, priority queue |
| bisect | Binary search, maintaining sorted lists |

---

*Understanding data structures is crucial for writing efficient code. Practice choosing the right structure for different scenarios!*