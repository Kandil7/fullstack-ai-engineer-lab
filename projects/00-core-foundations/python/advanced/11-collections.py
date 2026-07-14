"""
Collections - Advanced Python Exercises
========================================
collections provides specialized container types
for efficient data operations.
"""

from collections import (
    Counter, defaultdict, namedtuple, OrderedDict, deque,
    ChainMap, UserDict, UserList
)
from typing import List, Dict, Tuple


# =============================================================================
# 1. Counter - Counting Elements
# =============================================================================

def demo_counter():
    """Demonstrate Counter for counting."""
    # Basic counting
    text = "hello world hello python world hello"
    word_count = Counter(text.split())
    print(f"  Word counts: {word_count}")

    # Most common
    print(f"  Most common 2: {word_count.most_common(2)}")

    # Counter from iterable
    colors = ["red", "blue", "red", "green", "blue", "red"]
    color_count = Counter(colors)
    print(f"  Color counts: {color_count}")

    # Arithmetic with counters
    counter1 = Counter(a=3, b=1)
    counter2 = Counter(a=1, b=2)
    print(f"  Sum: {counter1 + counter2}")
    print(f"  Difference: {counter1 - counter2}")

    # Count characters
    print(f"  Char counts in 'mississippi': {Counter('mississippi')}")


# =============================================================================
# 2. defaultdict - Default Values
# =============================================================================

def demo_defaultdict():
    """Demonstrate defaultdict for grouping."""
    # Group by first letter
    words = ["apple", "banana", "avocado", "blueberry", "cherry", "apricot"]
    grouped = defaultdict(list)
    for word in words:
        grouped[word[0]].append(word)
    print(f"  Grouped by first letter: {dict(grouped)}")

    # Count with defaultdict(int)
    sentence = "the cat sat on the mat the cat"
    counts = defaultdict(int)
    for word in sentence.split():
        counts[word] += 1
    print(f"  Word counts: {dict(counts)}")

    # Nested defaultdict
    nested = defaultdict(lambda: defaultdict(list))
    data = [
        ("science", "physics", " Newton"),
        ("science", "chemistry", " Periodic Table"),
        ("math", "algebra", " Equations"),
    ]
    for subject, topic, fact in data:
        nested[subject][topic].append(fact)
    print(f"  Nested: {dict(nested)}")

    # defaultdict with set
    index = defaultdict(set)
    words = "the cat sat on the mat".split()
    for i, word in enumerate(words):
        index[word].add(i)
    print(f"  Word index: {dict(index)}")


# =============================================================================
# 3. namedtuple - Lightweight Classes
# =============================================================================

Point = namedtuple("Point", ["x", "y"])
Person = namedtuple("Person", "name age email", defaults=["unknown@example.com"])


def demo_namedtuple():
    """Demonstrate namedtuple usage."""
    # Basic usage
    p = Point(3, 4)
    print(f"  Point: {p}")
    print(f"  x={p.x}, y={p.y}")

    # With defaults
    person = Person("Alice", 30)
    print(f"  Person: {person}")
    person2 = Person("Bob", 25, "bob@example.com")
    print(f"  Person2: {person2}")

    # Named tuples are immutable
    try:
        p.x = 5
    except AttributeError as e:
        print(f"  Cannot modify: {e}")

    # Convert to dict
    print(f"  As dict: {p._asdict()}")

    # Replace values (returns new tuple)
    p2 = p._replace(x=10)
    print(f"  Replaced: {p2}")

    # Unpack
    x, y = p
    print(f"  Unpacked: x={x}, y={y}")


# =============================================================================
# 4. OrderedDict - Ordered Dictionary
# =============================================================================

def demo_ordereddict():
    """Demonstrate OrderedDict for ordered operations."""
    # Move to end
    od = OrderedDict()
    od["first"] = 1
    od["second"] = 2
    od["third"] = 3
    print(f"  Original: {list(od.keys())}")

    od.move_to_end("first")
    print(f"  After move_to_end(first): {list(od.keys())}")

    od.move_to_end("third", last=False)
    print(f"  After move_to_end(third, last=False): {list(od.keys())}")

    # Pop last
    last_key, last_value = od.popitem()
    print(f"  Popped last: {last_key}={last_value}")

    # Equality considers order
    od1 = OrderedDict([("a", 1), ("b", 2)])
    od2 = OrderedDict([("b", 2), ("a", 1)])
    print(f"  Order matters: {od1 == od2}")


# =============================================================================
# 5. deque - Double-Ended Queue
# =============================================================================

def demo_deque():
    """Demonstrate deque for efficient operations."""
    # Basic deque
    dq = deque([1, 2, 3, 4, 5])
    print(f"  Deque: {dq}")

    # Append and appendleft
    dq.append(6)
    dq.appendleft(0)
    print(f"  After append/appendleft: {dq}")

    # Pop and popleft
    right = dq.pop()
    left = dq.popleft()
    print(f"  Popped right={right}, left={left}")

    # Rotate
    dq.rotate(2)
    print(f"  After rotate(2): {dq}")
    dq.rotate(-2)
    print(f"  After rotate(-2): {dq}")

    # Bounded deque (max length)
    bounded = deque(maxlen=3)
    for i in range(5):
        bounded.append(i)
        print(f"  append({i}): {list(bounded)}")

    # Deque as queue
    queue = deque()
    queue.append("task1")
    queue.append("task2")
    queue.append("task3")
    while queue:
        task = queue.popleft()
        print(f"  Processing: {task}")


# =============================================================================
# 6. ChainMap - Multiple Dictionaries
# =============================================================================

def demo_chainmap():
    """Demonstrate ChainMap for combining dicts."""
    defaults = {"color": "red", "user": "guest", "debug": False}
    environment = {"user": "admin", "debug": True}
    command_line = {"color": "blue"}

    # ChainMap searches in order
    config = ChainMap(command_line, environment, defaults)
    print(f"  Config color: {config['color']}")  # From command_line
    print(f"  Config user: {config['user']}")    # From environment
    print(f"  Config debug: {config['debug']}")  # From environment
    print(f"  Config keys: {list(config.keys())}")

    # New child dict
    child = config.new_child({"timeout": 30})
    print(f"  Child timeout: {child['timeout']}")
    print(f"  Parent still has timeout? {'timeout' in config}")


# =============================================================================
# 7. Practical Examples
# =============================================================================

def demo_practical():
    """Practical collections examples."""
    # Word frequency analysis
    text = """Python is great. Python is versatile. 
    Python is used for web, data science, and automation."""
    words = text.lower().split()
    word_freq = Counter(words)
    print(f"  Top 3 words: {word_freq.most_common(3)}")

    # Student grades with defaultdict
    grades = defaultdict(list)
    students_grades = [
        ("Alice", 95), ("Bob", 87), ("Alice", 92),
        ("Bob", 91), ("Charlie", 78), ("Alice", 88),
    ]
    for name, grade in students_grades:
        grades[name].append(grade)

    print(f"  Student grades:")
    for name, grade_list in grades.items():
        avg = sum(grade_list) / len(grade_list)
        print(f"    {name}: {grade_list} (avg: {avg:.1f})")

    # LRUCache using OrderedDict
    class LRUCache:
        def __init__(self, capacity: int):
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

    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    print(f"  LRU Cache get(a): {cache.get('a')}")
    cache.put("d", 4)  # Evicts "b"
    print(f"  LRU Cache get(b): {cache.get('b')}")
    print(f"  Cache order: {list(cache.cache.keys())}")


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("COLLECTIONS DEMO")
    print("=" * 60)

    print("\n--- Counter ---")
    demo_counter()

    print("\n--- defaultdict ---")
    demo_defaultdict()

    print("\n--- namedtuple ---")
    demo_namedtuple()

    print("\n--- OrderedDict ---")
    demo_ordereddict()

    print("\n--- deque ---")
    demo_deque()

    print("\n--- ChainMap ---")
    demo_chainmap()

    print("\n--- Practical Examples ---")
    demo_practical()

    print("\n" + "=" * 60)
    print("All collections demos complete!")
    print("=" * 60)
