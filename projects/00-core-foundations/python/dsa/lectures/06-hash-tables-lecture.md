# Lecture 06: Hash Tables

## Topic Overview

A **hash table** (hash map) is a data structure that maps keys to values using a **hash function**. It provides O(1) average-time complexity for insertions, deletions, and lookups — making it one of the most useful data structures in practice.

Python's `dict` and `set` are hash table implementations.

Key concepts: hash functions, collision resolution (chaining and open addressing), load factor, and rehashing.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** how hash functions work and their properties
2. **Implement** a hash table with separate chaining
3. **Handle** hash collisions using chaining and open addressing
4. **Analyze** average and worst-case complexities of hash table operations
5. **Use** Python dicts and sets effectively
6. **Solve** frequency counting, two-sum, and grouping problems
7. **Understand** load factor and rehashing strategies

---

## Key Concepts

### 1. How Hash Tables Work

```
Hash Table Structure:

Key: "alice"  →  hash("alice")  →  index 3  →  Value: 95
Key: "bob"    →  hash("bob")    →  index 1  →  Value: 87
Key: "carol"  →  hash("carol")  →  index 3  →  Collision! → Chain or probe

Underlying array:
Index:  [0]    [1]    [2]    [3]    [4]
Value:  None   87     None  "alice" None
                       ↓
                     "carol" (chaining)
```

### 2. Hash Function

A hash function converts a key into an array index.

**Properties of a good hash function:**
- **Deterministic:** Same key always produces the same hash
- **Uniform distribution:** Keys are spread evenly across the table
- **Efficient:** O(1) to compute
- **Minimize collisions:** Different keys rarely map to the same index

```python
# Python's built-in hash function
print(hash("hello"))     # Integer hash
print(hash(42))
print(hash((1, 2, 3)))   # Tuples are hashable
# print(hash([1, 2, 3])) # Lists are NOT hashable (mutable)

# Simple hash function for integers
def simple_hash(key, table_size):
    return key % table_size

# Example: table_size = 10
# hash(25) = 25 % 10 = 5
# hash(35) = 35 % 10 = 5  ← Collision with 25!
```

### 3. Collision Resolution

#### Separate Chaining (Open Hashing)
Each bucket contains a linked list (or another data structure) of all entries that hash to that index.

```python
class HashTableChaining:
    """Hash table with separate chaining."""
    
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
    
    def _hash(self, key):
        """Compute bucket index from key."""
        return hash(key) % self.capacity
    
    def put(self, key, value):
        """Insert or update key-value pair. O(1) average."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Update if key exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Insert new pair
        bucket.append((key, value))
        self.size += 1
        
        # Resize if load factor > 0.75
        if self.size / self.capacity > 0.75:
            self._resize()
    
    def get(self, key):
        """Retrieve value by key. O(1) average."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        raise KeyError(key)
    
    def delete(self, key):
        """Remove key-value pair. O(1) average."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return v
        
        raise KeyError(key)
    
    def contains(self, key):
        """Check if key exists. O(1) average."""
        index = self._hash(key)
        return any(k == key for k, _ in self.buckets[index])
    
    def _resize(self):
        """Double capacity and rehash all entries."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def __len__(self):
        return self.size
    
    def __repr__(self):
        items = []
        for bucket in self.buckets:
            for k, v in bucket:
                items.append(f"{k}: {v}")
        return "{" + ", ".join(items) + "}"
```

#### Open Addressing (Closed Hashing)
All entries are stored in the array itself. When a collision occurs, probe for the next open slot.

```python
class HashTableOpenAddressing:
    """Hash table with linear probing."""
    
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.keys = [None] * capacity
        self.values = [None] * capacity
    
    def _hash(self, key):
        return hash(key) % self.capacity
    
    def _probe(self, key):
        """Find index for key using linear probing."""
        index = self._hash(key)
        
        while self.keys[index] is not None:
            if self.keys[index] == key:
                return index  # Key found
            index = (index + 1) % self.capacity  # Probe next slot
        
        return index  # Empty slot found
    
    def put(self, key, value):
        if self.size / self.capacity > 0.7:
            self._resize()
        
        index = self._probe(key)
        
        if self.keys[index] is None:
            self.size += 1
        
        self.keys[index] = key
        self.values[index] = value
    
    def get(self, key):
        index = self._hash(key)
        
        while self.keys[index] is not None:
            if self.keys[index] == key:
                return self.values[index]
            index = (index + 1) % self.capacity
        
        raise KeyError(key)
    
    def _resize(self):
        old_keys = self.keys
        old_values = self.values
        self.capacity *= 2
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0
        
        for k, v in zip(old_keys, old_values):
            if k is not None:
                self.put(k, v)
```

### 4. Load Factor and Rehashing

```
Load Factor (α) = number of entries / number of buckets

When α > threshold (typically 0.75):
  1. Create a new table with 2× capacity
  2. Rehash all existing entries
  3. Replace old table with new table

Impact:
  Low α (< 0.5): Lots of wasted space, but fast operations
  High α (> 0.75): More collisions, slower operations
  Sweet spot: 0.5 - 0.75
```

### 5. Time Complexity

| Operation | Average | Worst Case |
|-----------|---------|------------|
| Insert | O(1) | O(n) |
| Lookup | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Space | O(n) | O(n) |

**Worst case O(n)** occurs when all keys hash to the same bucket (all keys collide).

### 6. Python dict and Set

```python
# === DICTIONARY (Hash Map) ===
student = {}
student["alice"] = 90       # O(1) insert
student["bob"] = 85
print(student["alice"])     # O(1) lookup → 90
del student["bob"]          # O(1) delete
print("alice" in student)   # O(1) membership test → True
print(len(student))         # O(1) size → 1

# Dict comprehension
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# === SET (Hash Set) ===
unique = set()
unique.add(1)               # O(1)
unique.add(2)
unique.add(1)               # Duplicate ignored
print(1 in unique)          # O(1) → True
unique.discard(2)           # O(1)

# Set operations
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)   # Union: {1, 2, 3, 4, 5}
print(a & b)   # Intersection: {3}
print(a - b)   # Difference: {1, 2}
print(a ^ b)   # Symmetric difference: {1, 2, 4, 5}
```

---

## Complete Code Examples

### Example 1: Frequency Counter

```python
"""
Count frequency of each element.
Time: O(n), Space: O(k) where k = number of unique elements
"""

def frequency_count(arr):
    freq = {}
    for item in arr:
        freq[item] = freq.get(item, 0) + 1
    return freq

# Test
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
print(frequency_count(words))
# {'apple': 3, 'banana': 2, 'cherry': 1}

# Find most common element
freq = frequency_count(words)
most_common = max(freq, key=freq.get)
print(f"Most common: {most_common}")  # apple
```

### Example 2: Two Sum Using Hash Map

```python
"""
Given an array and target, find two numbers that sum to target.
Time: O(n), Space: O(n)
"""

def two_sum(nums, target):
    seen = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Test
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
```

### Example 3: Group Anagrams

```python
"""
Group strings that are anagrams of each other.
Time: O(n × k log k) where k = max string length
Space: O(n × k)
"""

def group_anagrams(strs):
    groups = {}
    for s in strs:
        # Sort the string to create a key
        key = ''.join(sorted(s))
        if key not in groups:
            groups[key] = []
        groups[key].append(s)
    return list(groups.values())

# Test
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

### Example 4: First Non-Repeating Character

```python
"""
Find the first non-repeating character in a string.
Time: O(n), Space: O(1) — at most 26 lowercase letters
"""

def first_non_repeating(s):
    freq = {}
    
    # Count frequencies
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    
    # Find first with frequency 1
    for char in s:
        if freq[char] == 1:
            return char
    
    return None

# Test
print(first_non_repeating("aabxbxc"))  # "y" (if present) or None
```

### Example 5: Subarray Sum Equals K

```python
"""
Count the number of subarrays whose sum equals k.
Uses prefix sum + hash map.
Time: O(n), Space: O(n)
"""

def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    seen = {0: 1}  # prefix_sum → count
    
    for num in nums:
        prefix_sum += num
        # If (prefix_sum - k) was seen before,
        # there's a subarray with sum k
        if prefix_sum - k in seen:
            count += seen[prefix_sum - k]
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    
    return count

# Test
print(subarray_sum([1, 1, 1], 2))       # 2
print(subarray_sum([1, 2, 3], 3))       # 2
```

---

## Common Mistakes to Avoid

### Mistake 1: Using Mutable Objects as Keys
```python
# WRONG: Lists can't be dict keys (they're mutable/unhashable)
d = {}
# d[[1, 2]] = "value"  # TypeError: unhashable type: 'list'

# RIGHT: Use tuples instead
d = {}
d[(1, 2)] = "value"  # Tuples are hashable
```

### Mistake 2: Modifying Dict During Iteration
```python
# WRONG: Runtime error
d = {"a": 1, "b": 2, "c": 3}
for key in d:
    if d[key] == 2:
        del d[key]  # RuntimeError: dictionary changed size

# RIGHT: Create a list of keys first
for key in list(d.keys()):
    if d[key] == 2:
        del d[key]
```

### Mistake 3: Assuming Dict Ordering Guarantee
```python
# Python 3.7+ guarantees insertion order, but don't rely on it
# for algorithm correctness — hash tables are conceptually unordered

# WRONG: Assuming sorted order from dict
d = {"c": 3, "a": 1, "b": 2}
# In Python 3.7+: iterates as c, a, b (insertion order)
# NOT sorted order!
```

### Mistake 4: Forgetting `get()` Default Value
```python
# WRONG: KeyError if key doesn't exist
freq = {}
for word in words:
    freq[word] += 1  # KeyError on first occurrence

# RIGHT: Use get() with default
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1
```

---

## Best Practices

1. **Use `dict.get(key, default)`** to avoid KeyError
2. **Use `collections.Counter`** for frequency counting
3. **Use `set` for O(1) membership testing** instead of list
4. **Understand Python's hash()** — same object must always return same hash
5. **Use dict comprehension** for clean transformations
6. **For counting patterns**, hash maps are almost always the answer
7. **Watch out for hash DoS** — untrusted input can cause O(n²) performance in worst case

---

## Practice Exercises

### Exercise 1: Valid Anagram
```python
def is_anagram(s, t):
    """
    Check if two strings are anagrams.
    Time: O(n), Space: O(1) for 26 lowercase letters
    """
    # Your solution here — use frequency counting
    pass
```

### Exercise 2: Longest Consecutive Sequence
```python
def longest_consecutive(nums):
    """
    Find the length of the longest consecutive sequence.
    Input: [100, 4, 200, 1, 3, 2]
    Output: 4 (sequence: 1, 2, 3, 4)
    Time: O(n)
    """
    # Your solution here — use a set
    pass
```

### Exercise 3: Top K Frequent Elements
```python
def top_k_frequent(nums, k):
    """
    Find the k most frequent elements.
    Input: [1,1,1,2,2,3], k=2
    Output: [1, 2]
    """
    # Your solution here — use Counter + heap
    pass
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Hash Function** | Maps keys to array indices |
| **Collision** | Two keys mapping to same index |
| **Chaining** | Each bucket holds a list of entries |
| **Open Addressing** | Find next open slot when collision occurs |
| **Load Factor** | Ratio of entries to capacity — triggers resize |
| **Average O(1)** | For insert, lookup, delete |
| **Worst O(n)** | When all keys collide |

**Key Insight:** Hash tables are the workhorse of modern computing. Understanding them explains why `dict` and `set` are so fast and when they might slow down.

**Next Lecture:** Trees — hierarchical data structures that enable efficient searching and sorting.
