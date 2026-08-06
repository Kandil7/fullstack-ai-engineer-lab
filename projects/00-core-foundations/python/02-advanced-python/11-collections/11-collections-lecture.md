# Lecture 11: Collections Module

## Topic Overview

Python's `collections` module provides specialized container data types that go beyond the built-in `dict`, `list`, `set`, and `tuple`. These containers are optimized for specific use cases and provide efficient implementations for common programming patterns.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Use Counter** for counting hashable objects and performing frequency analysis
2. **Implement defaultdict** to handle missing keys with default values
3. **Create namedtuple** for lightweight, immutable data classes
4. **Work with deque** for efficient queue and stack operations
5. **Apply ChainMap** for treating multiple dictionaries as one
6. **Utilize OrderedDict** for maintaining insertion order with special operations
7. **Choose the right collection type** for different scenarios

---

## Key Concepts

### 1. Counter - Counting Elements

`Counter` is a dictionary subclass for counting hashable objects. It's one of the most useful tools for data analysis and frequency counting.

#### Basic Usage

```python
from collections import Counter

# Count characters in a string
text = "hello world"
char_count = Counter(text)
print(char_count)  # Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})

# Count words in a sentence
sentence = "the cat sat on the mat the cat"
word_count = Counter(sentence.split())
print(word_count)  # Counter({'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1})

# Count elements in a list
colors = ["red", "blue", "red", "green", "blue", "red"]
color_count = Counter(colors)
print(color_count)  # Counter({'red': 3, 'blue': 2, 'green': 1})
```

#### Advanced Operations

```python
# Most common elements
print(word_count.most_common(2))  # [('the', 3), ('cat', 2)]

# Update counts
word_count.update({"the": 1, "new": 5})
print(word_count)  # Counter({'the': 4, 'new': 5, ...})

# Arithmetic operations
counter1 = Counter(a=3, b=1)
counter2 = Counter(a=1, b=2)

# Addition: combines counts
print(counter1 + counter2)  # Counter({'a': 4, 'b': 3})

# Subtraction: removes counts (only keeps positive)
print(counter1 - counter2)  # Counter({'a': 2})

# Intersection: minimum counts
print(counter1 & counter2)  # Counter({'a': 1, 'b': 1})

# Union: maximum counts
print(counter1 | counter2)  # Counter({'a': 3, 'b': 2})
```

#### Practical Examples

```python
# Word frequency analysis
def analyze_text(text):
    words = text.lower().split()
    word_freq = Counter(words)
    
    print(f"Total words: {sum(word_freq.values())}")
    print(f"Unique words: {len(word_freq)}")
    print(f"Most common: {word_freq.most_common(3)}")
    
    # Find words appearing only once
    rare_words = [word for word, count in word_freq.items() if count == 1]
    print(f"Rare words: {rare_words}")

# DNA sequence analysis
def analyze_dna(sequence):
    return Counter(sequence)

dna = "ATCGATCGATCG"
print(analyze_dna(dna))  # Counter({'A': 3, 'T': 3, 'C': 3, 'G': 3})
```

---

### 2. defaultdict - Default Values

`defaultdict` is a dictionary subclass that calls a factory function to provide default values for missing keys.

#### Basic Usage

```python
from collections import defaultdict

# Group items by first letter
words = ["apple", "banana", "avocado", "blueberry", "cherry", "apricot"]
grouped = defaultdict(list)

for word in words:
    grouped[word[0]].append(word)

print(dict(grouped))
# {'a': ['apple', 'avocado', 'apricot'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}
```

#### Different Default Factories

```python
# Count with int (default 0)
sentence = "the cat sat on the mat the cat"
counts = defaultdict(int)
for word in sentence.split():
    counts[word] += 1
print(dict(counts))  # {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}

# Accumulate values with list
scores = defaultdict(list)
scores["Alice"].append(95)
scores["Alice"].append(87)
scores["Bob"].append(82)
print(dict(scores))  # {'Alice': [95, 87], 'Bob': [82]}

# Use set for unique values
index = defaultdict(set)
for i, char in enumerate("hello"):
    index[char].add(i)
print(dict(index))  # {'h': {0}, 'e': {1}, 'l': {2, 3}, 'o': {4}}
```

#### Nested defaultdict

```python
# Create nested structure
nested = defaultdict(lambda: defaultdict(list))

data = [
    ("science", "physics", "Newton"),
    ("science", "chemistry", "Periodic Table"),
    ("math", "algebra", "Equations"),
]

for subject, topic, fact in data:
    nested[subject][topic].append(fact)

# Access nested data
print(nested["science"]["physics"])  # ['Newton']
```

---

### 3. namedtuple - Lightweight Classes

`namedtuple` creates tuple subclasses with named fields. It provides a lightweight way to create immutable data classes.

#### Basic Usage

```python
from collections import namedtuple

# Create a namedtuple class
Point = namedtuple("Point", ["x", "y"])

# Create instances
p = Point(3, 4)
print(p.x, p.y)  # 3 4
print(p)  # Point(x=3, y=4)

# Named tuples are immutable
try:
    p.x = 5
except AttributeError as e:
    print(f"Error: {e}")  # can't set attribute
```

#### Advanced Features

```python
# Multiple field definitions
Person = namedtuple("Person", "name age email")

# With defaults
PersonWithDefaults = namedtuple(
    "PersonWithDefaults", 
    ["name", "age", "email"], 
    defaults=["unknown@example.com"]
)

p1 = PersonWithDefaults("Alice", 30)
print(p1.email)  # unknown@example.com

# Convert to dictionary
d = p._asdict()
print(d)  # {'x': 3, 'y': 4}

# Replace values (returns new tuple)
p2 = p._replace(x=10)
print(p2)  # Point(x=10, y=4)

# Unpack like regular tuples
x, y = p
print(f"x={x}, y={y}")
```

#### Practical Example

```python
# Representing database records
Employee = namedtuple("Employee", ["id", "name", "department", "salary"])

employees = [
    Employee(1, "Alice", "Engineering", 95000),
    Employee(2, "Bob", "Marketing", 75000),
    Employee(3, "Charlie", "Engineering", 105000),
]

# Filter by department
engineers = [e for e in employees if e.department == "Engineering"]
print(f"Engineers: {[e.name for e in engineers]}")

# Calculate average salary
avg_salary = sum(e.salary for e in employees) / len(employees)
print(f"Average salary: ${avg_salary:,.2f}")
```

---

### 4. deque - Double-Ended Queue

`deque` (double-ended queue) provides O(1) appends and pops from both ends, making it ideal for queue and stack implementations.

#### Basic Operations

```python
from collections import deque

# Create deque
dq = deque([1, 2, 3, 4, 5])

# Append/appendleft (O(1))
dq.append(6)
dq.appendleft(0)
print(dq)  # deque([0, 1, 2, 3, 4, 5, 6])

# Pop/popleft (O(1))
right = dq.pop()  # 6
left = dq.popleft()  # 0

# Rotate
dq.rotate(2)  # Rotate right by 2
print(dq)
dq.rotate(-2)  # Rotate left by 2
```

#### Bounded deque

```python
# Automatically removes items when full
bounded = deque(maxlen=3)
for i in range(5):
    bounded.append(i)
    print(f"append({i}): {list(bounded)}")
# Output:
# append(0): [0]
# append(1): [0, 1]
# append(2): [0, 1, 2]
# append(3): [1, 2, 3]  # Removed 0
# append(4): [2, 3, 4]  # Removed 1
```

#### Queue Implementation

```python
# FIFO Queue
queue = deque()
queue.append("task1")
queue.append("task2")
queue.append("task3")

while queue:
    task = queue.popleft()
    print(f"Processing: {task}")

# LIFO Stack
stack = deque()
stack.append("item1")
stack.append("item2")
stack.append("item3")

while stack:
    item = stack.pop()
    print(f"Popped: {item}")
```

---

### 5. ChainMap - Multiple Dictionaries

`ChainMap` groups multiple dictionaries into a single view, searching through them in order.

#### Basic Usage

```python
from collections import ChainMap

# Configuration with priority
defaults = {"color": "red", "user": "guest", "debug": False}
environment = {"user": "admin", "debug": True}
command_line = {"color": "blue"}

# ChainMap searches in order (first match wins)
config = ChainMap(command_line, environment, defaults)

print(config["color"])  # blue (from command_line)
print(config["user"])   # admin (from environment)
print(config["debug"])  # True (from environment)
```

#### Practical Applications

```python
# Scope chain (like in programming languages)
def example_scope():
    local_var = "local"
    scope = ChainMap(
        {"local_var": local_var},  # Local scope
        {"global_var": "global"},  # Global scope
        {"builtin_var": "builtin"}  # Built-in scope
    )
    print(scope["local_var"])  # local

# Settings management
class Settings:
    def __init__(self):
        self.defaults = {"timeout": 30, "retries": 3}
        self.user_settings = {}
        self.temp_settings = {}
        self._chain = ChainMap(self.temp_settings, self.user_settings, self.defaults)
    
    def get(self, key):
        return self._chain[key]
    
    def set_temp(self, key, value):
        self.temp_settings[key] = value
```

---

### 6. OrderedDict - Ordered Dictionary

`OrderedDict` remembers the insertion order of keys. While standard dicts in Python 3.7+ maintain insertion order, `OrderedDict` provides additional methods.

#### Special Features

```python
from collections import OrderedDict

od = OrderedDict()
od["first"] = 1
od["second"] = 2
od["third"] = 3

# Move to end
od.move_to_end("first")
print(list(od.keys()))  # ['second', 'third', 'first']

# Move to beginning
od.move_to_end("third", last=False)
print(list(od.keys()))  # ['third', 'second', 'first']

# Pop last item (LIFO)
last_key, last_value = od.popitem()
print(f"Popped: {last_key}={last_value}")  # Popped: first=1

# Pop first item (FIFO)
first_key, first_value = od.popitem(last=False)
print(f"Popped: {first_key}={first_value}")  # Popped: third=3
```

#### Equality Comparison

```python
# Regular dicts (order doesn't matter for equality)
d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
print(d1 == d2)  # True

# OrderedDicts (order matters for equality)
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
print(od1 == od2)  # False (different order)
```

---

## Common Mistakes to Avoid

### 1. Using Counter for Non-Hashable Items

```python
# WRONG - lists are not hashable
try:
    counter = Counter([[1, 2], [3, 4]])  # TypeError
except TypeError as e:
    print(f"Error: {e}")

# CORRECT - use tuple instead
counter = Counter([(1, 2), (3, 4)])  # Works
```

### 2. Forgetting defaultdict Creates Default on Access

```python
# This creates a key even if you don't set it
dd = defaultdict(int)
value = dd["missing_key"]  # Creates key with value 0
print("missing_key" in dd)  # True (unexpected!)

# Use dict.get() if you don't want to create keys
d = {}
value = d.get("missing_key", 0)  # Doesn't create key
```

### 3. Mutating Named Tuples

```python
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)

# WRONG
try:
    p.x = 3  # AttributeError
except AttributeError:
    pass

# CORRECT - use _replace()
p2 = p._replace(x=3)
```

### 4. Not Understanding deque Rotation

```python
dq = deque([1, 2, 3, 4, 5])
dq.rotate(1)  # Rotates RIGHT
print(dq)  # [5, 1, 2, 3, 4]

dq.rotate(-1)  # Rotates LEFT
print(dq)  # [1, 2, 3, 4, 5]
```

---

## Best Practices

### 1. Choose the Right Collection

| Task | Best Collection | Why |
|------|-----------------|-----|
| Counting items | `Counter` | Optimized for frequency analysis |
| Grouping items | `defaultdict(list)` | Automatic list creation |
| Immutable records | `namedtuple` | Lightweight, memory-efficient |
| Queue/Stack | `deque` | O(1) operations on both ends |
| Config hierarchy | `ChainMap` | Priority-based lookup |
| Sorted iteration | `OrderedDict` | Move operations, equality by order |

### 2. Performance Considerations

```python
# Counter is faster than manual counting
from collections import Counter

# SLOW
counts = {}
for item in large_list:
    counts[item] = counts.get(item, 0) + 1

# FAST
counts = Counter(large_list)
```

### 3. Memory Efficiency

```python
# namedtuple vs dict
from collections import namedtuple
import sys

PointNT = namedtuple("Point", ["x", "y"])

class PointDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

nt = PointNT(1, 2)
pd = PointDict(1, 2)

print(f"namedtuple: {sys.getsizeof(nt)} bytes")
print(f"dict class: {sys.getsizeof(pd)} bytes")
```

---

## Practice Exercises

### Exercise 1: Word Frequency Analyzer
```python
def analyze_text(text):
    """
    Analyze text and return:
    - Total word count
    - Unique word count
    - Top 5 most common words
    - Average word length
    """
    # Your code here
    pass
```

### Exercise 2: Group by Category
```python
def group_by_category(items):
    """
    Given a list of (name, category) tuples,
    group items by category using defaultdict.
    """
    # Your code here
    pass
```

### Exercise 3: LRU Cache
```python
class LRUCache:
    """
    Implement an LRU cache using OrderedDict.
    Should support get(key) and put(key, value) operations.
    """
    def __init__(self, capacity):
        # Your code here
        pass
```

### Exercise 4: Sliding Window
```python
def sliding_window_average(data, window_size):
    """
    Calculate sliding window average using deque.
    """
    # Your code here
    pass
```

---

## Summary

| Collection | Purpose | Key Features |
|------------|---------|--------------|
| `Counter` | Counting hashable objects | most_common(), arithmetic operations |
| `defaultdict` | Dictionaries with defaults | Automatic key creation |
| `namedtuple` | Lightweight immutable classes | Named fields, _asdict(), _replace() |
| `deque` | Double-ended queue | O(1) append/pop from both ends |
| `ChainMap` | Multiple dict views | Priority-based lookup |
| `OrderedDict` | Order-sensitive dictionary | move_to_end(), popitem() |

### Key Takeaways

1. **Counter** is essential for frequency analysis and data science
2. **defaultdict** eliminates KeyError and simplifies grouping logic
3. **namedtuple** provides memory-efficient immutable data structures
4. **deque** is the go-to for queues and stacks
5. **ChainMap** is perfect for configuration management and scope chains
6. **OrderedDict** is needed when order matters for equality or iteration

---

## Further Reading

- [Python collections documentation](https://docs.python.org/3/library/collections.html)
- [Counter examples](https://docs.python.org/3/library/collections.html#counter-examples)
- [deque documentation](https://docs.python.org/3/library/collections.html#deque-objects)
