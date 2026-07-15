# Glossary: Collections Module

## Quick Reference Table

| Term | Definition | Python Type | Key Methods |
|------|------------|-------------|-------------|
| Counter | Dictionary subclass for counting hashable objects | `collections.Counter` | most_common(), elements(), update() |
| defaultdict | Dictionary with default factory for missing keys | `collections.defaultdict` | Uses standard dict methods |
| namedtuple | Tuple subclass with named fields | `collections.namedtuple` | _asdict(), _replace(), _make() |
| deque | Double-ended queue with O(1) appends/pops | `collections.deque` | append(), popleft(), rotate() |
| ChainMap | Group multiple dicts into single view | `collections.ChainMap` | new_child(), maps |
| OrderedDict | Dictionary remembering insertion order | `collections.OrderedDict` | move_to_end(), popitem() |
| UserDict | Wrapper class for custom dict behavior | `collections.UserDict` | Inherits dict interface |
| UserList | Wrapper class for custom list behavior | `collections.UserList` | Inherits list interface |
| UserString | Wrapper class for custom string behavior | `collections.UserString` | Inherits string interface |

---

## Alphabetical Definitions

### ChainMap

**Definition**: A `ChainMap` groups multiple dictionaries (or other mappings) into a single, unified view. Lookups search the underlying mappings in order, returning the first match found.

**Example**:
```python
from collections import ChainMap

defaults = {"color": "red", "user": "guest"}
environment = {"user": "admin"}
command_line = {"color": "blue"}

config = ChainMap(command_line, environment, defaults)

# Priority: command_line > environment > defaults
print(config["color"])  # blue (from command_line)
print(config["user"])   # admin (from environment)
print(config["debug"])  # KeyError (not in any)
```

**Related Terms**: dictionary, mapping, priority chain, configuration

**Key Methods**:
- `maps`: List of underlying mappings
- `new_child(m=None)`: Create new ChainMap with m prepended
- `parents`: ChainMap excluding first mapping

---

### Counter

**Definition**: A `Counter` is a dictionary subclass designed for counting hashable objects. It stores elements as dictionary keys and their counts as values.

**Example**:
```python
from collections import Counter

# Count from iterable
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
word_count = Counter(words)
print(word_count)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})

# Most common elements
print(word_count.most_common(2))  # [('apple', 3), ('banana', 2)]

# Arithmetic
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2})
```

**Related Terms**: frequency, counting, histogram, tally

**Key Methods**:
- `most_common(n)`: Return n most common elements
- `elements()`: Iterator over elements repeating by count
- `update()`: Add counts from another iterable/mapping
- `subtract()`: Subtract counts from another iterable/mapping

---

### deque

**Definition**: A `deque` (double-ended queue) is an optimized list-like container that provides O(1) appends and pops from both ends, with O(n) random access in the middle.

**Example**:
```python
from collections import deque

dq = deque([1, 2, 3, 4, 5])

# O(1) operations at both ends
dq.append(6)      # Add to right
dq.appendleft(0)  # Add to left

right = dq.pop()      # Remove from right
left = dq.popleft()   # Remove from left

# Rotate elements
dq.rotate(2)   # Rotate right by 2
dq.rotate(-2)  # Rotate left by 2

# Bounded deque
bounded = deque(maxlen=3)
bounded.append(1)
bounded.append(2)
bounded.append(3)
bounded.append(4)  # Automatically removes 1
```

**Related Terms**: queue, stack, FIFO, LIFO, circular buffer

**Key Methods**:
- `append(x)`: Add x to the right end
- `appendleft(x)`: Add x to the left end
- `pop()`: Remove and return from right end
- `popleft()`: Remove and return from left end
- `rotate(n)`: Rotate deque n steps to the right
- `extend(iterable)`: Extend deque with elements from iterable
- `extendleft(iterable)`: Extend deque from left (reversed)

---

### defaultdict

**Definition**: A `defaultdict` is a dictionary subclass that calls a factory function to provide default values for missing keys, eliminating KeyError.

**Example**:
```python
from collections import defaultdict

# Group by first letter
words = ["apple", "banana", "avocado", "blueberry"]
grouped = defaultdict(list)
for word in words:
    grouped[word[0]].append(word)
print(dict(grouped))  # {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry']}

# Count occurrences
sentence = "the cat sat on the mat"
counts = defaultdict(int)
for word in sentence.split():
    counts[word] += 1
print(dict(counts))  # {'the': 1, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}
```

**Related Terms**: dictionary, missing key, factory function, default value

**Key Features**:
- `default_factory`: Callable that provides default values
- Automatic key creation on first access
- Common factories: `int` (0), `list` ([]), `set` (set()), `str` ("")

---

### named tuple

**Definition**: A `namedtuple` is a factory function that creates tuple subclasses with named fields, providing both the efficiency of tuples and the readability of named attributes.

**Example**:
```python
from collections import namedtuple

# Create namedtuple class
Point = namedtuple("Point", ["x", "y"])

# Create instances
p = Point(3, 4)
print(p.x, p.y)  # 3 4
print(p)          # Point(x=3, y=4)

# Immutable
try:
    p.x = 5
except AttributeError:
    print("Cannot modify namedtuple")

# Convert to dict
d = p._asdict()
print(d)  # {'x': 3, 'y': 4}

# Replace (creates new instance)
p2 = p._replace(x=10)
print(p2)  # Point(x=10, y=4)
```

**Related Terms**: tuple, immutable, data class, record

**Key Methods**:
- `_asdict()`: Return ordered dict
- `_make(iterable): Create new instance from iterable
- `_replace(**kwargs)`: Return new instance with replaced fields
- `_fields`: Tuple of field names
- `_field_defaults`: Dictionary of default values

---

### OrderedDict

**Definition**: An `OrderedDict` is a dictionary subclass that maintains the order in which keys were inserted. It provides additional methods for order manipulation.

**Example**:
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
key, value = od.popitem(last=True)
print(f"Popped: {key}={value}")  # Popped: first=1

# Equality considers order
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
print(od1 == od2)  # False (different order)
```

**Related Terms**: dictionary, insertion order, LRU cache, move operations

**Key Methods**:
- `move_to_end(key, last=True)`: Move key to beginning or end
- `popitem(last=True)`: Remove and return last (or first) item

**Note**: In Python 3.7+, regular dicts maintain insertion order. Use `OrderedDict` when you need:
- Order-sensitive equality comparison
- `move_to_end()` functionality
- `popitem(last=False)` for FIFO behavior

---

### UserDict

**Definition**: A `UserDict` is a wrapper class designed for creating custom dictionary subclasses. It provides a cleaner interface than directly subclassing `dict`.

**Example**:
```python
from collections import UserDict

class CaseInsensitiveDict(UserDict):
    def __getitem__(self, key):
        return super().__getitem__(key.lower())
    
    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)
    
    def __contains__(self, key):
        return super().__contains__(key.lower())

cid = CaseInsensitiveDict()
cid["Name"] = "Alice"
print(cid["name"])  # Alice (case-insensitive access)
```

**Related Terms**: dictionary, subclassing, wrapper class

**Advantages over dict subclassing**:
- Easier to override methods
- Less risk of bypassing custom behavior
- Clearer inheritance hierarchy

---

### UserList

**Definition**: A `UserList` is a wrapper class designed for creating custom list subclasses. It provides a cleaner interface than directly subclassing `list`.

**Example**:
```python
from collections import UserList

class MaxSizeList(UserList):
    def __init__(self, maxsize, initlist=None):
        super().__init__(initlist)
        self.maxsize = maxsize
    
    def append(self, item):
        if len(self) >= self.maxsize:
            raise OverflowError(f"List cannot exceed {self.maxsize} items")
        super().append(item)

msl = MaxSizeList(3)
msl.append(1)
msl.append(2)
msl.append(3)
try:
    msl.append(4)  # OverflowError
except OverflowError as e:
    print(e)  # List cannot exceed 3 items
```

**Related Terms**: list, subclassing, wrapper class

---

### UserString

**Definition**: A `UserString` is a wrapper class designed for creating custom string subclasses. It provides a cleaner interface than directly subclassing `str`.

**Example**:
```python
from collections import UserString

class ReversibleString(UserString):
    def reverse(self):
        return self.data[::-1]
    
    def scramble(self):
        import random
        chars = list(self.data)
        random.shuffle(chars)
        return ''.join(chars)

rs = ReversibleString("hello")
print(rs.reverse())  # olleh
print(rs.scramble())  # Random permutation like "olleh"
```

**Related Terms**: string, subclassing, wrapper class

---

## Concept Relationships

```
collections module
├── Counter
│   ├── Inherits from dict
│   ├── Used for: counting, frequency analysis
│   └── Related to: Counter arithmetic, most_common()
│
├── defaultdict
│   ├── Inherits from dict
│   ├── Used for: grouping, counting, nested structures
│   └── Related to: factory function, default values
│
├── namedtuple
│   ├── Inherits from tuple
│   ├── Used for: immutable records, data classes
│   └── Related to: _asdict(), _replace(), named fields
│
├── deque
│   ├── Implements: double-ended queue
│   ├── Used for: queues, stacks, sliding windows
│   └── Related to: O(1) append/pop, rotate()
│
├── ChainMap
│   ├── Implements: multiple dict views
│   ├── Used for: configuration, scope chains
│   └── Related to: priority lookup, new_child()
│
├── OrderedDict
│   ├── Inherits from dict
│   ├── Used for: ordered operations, LRU caches
│   └── Related to: move_to_end(), order-sensitive equality
│
├── UserDict
│   ├── Wrapper for: custom dict subclasses
│   └── Related to: cleaner subclassing than dict
│
├── UserList
│   ├── Wrapper for: custom list subclasses
│   └── Related to: cleaner subclassing than list
│
└── UserString
    ├── Wrapper for: custom string subclasses
    └── Related to: cleaner subclassing than str
```

---

## When to Use Each Collection

| Scenario | Use | Example |
|----------|-----|---------|
| Count word frequencies | `Counter` | `Counter(text.split())` |
| Group items by key | `defaultdict(list)` | `grouped[key].append(item)` |
| Count occurrences | `defaultdict(int)` | `counts[key] += 1` |
| Store immutable records | `namedtuple` | `Point = namedtuple("Point", ["x", "y"])` |
| Implement FIFO queue | `deque` | `queue.append(item); queue.popleft()` |
| Implement LIFO stack | `deque` | `stack.append(item); stack.pop()` |
| Configuration with priority | `ChainMap` | `ChainMap(cmd_config, env_config, defaults)` |
| Move items in dict | `OrderedDict` | `od.move_to_end("key")` |
| Custom dict behavior | `UserDict` | `class MyDict(UserDict): ...` |

---

## Common Patterns

### 1. Grouping Pattern
```python
from collections import defaultdict

groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)
```

### 2. Counting Pattern
```python
from collections import Counter

counts = Counter(items)
for item, count in counts.most_common(10):
    print(f"{item}: {count}")
```

### 3. FIFO Queue Pattern
```python
from collections import deque

queue = deque()
queue.append(task1)
queue.append(task2)

while queue:
    task = queue.popleft()
    process(task)
```

### 4. Sliding Window Pattern
```python
from collections import deque

def sliding_window(iterable, size):
    window = deque(maxlen=size)
    for item in iterable:
        window.append(item)
        if len(window) == size:
            yield list(window)
```

### 5. LRU Cache Pattern
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```
