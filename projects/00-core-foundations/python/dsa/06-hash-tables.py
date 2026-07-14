"""
DSA Tutorial 06 - Hash Tables
==============================

Hash Table: Key-value store using hash function to map keys to indices.

Operations:
- Insert: O(1) average, O(n) worst
- Delete: O(1) average, O(n) worst
- Search: O(1) average, O(n) worst

Collision Resolution:
- Chaining (linked lists)
- Open Addressing (linear probing, quadratic probing, double hashing)
"""

# =============================================================================
# 1. BASIC HASH TABLE (DICTIONARY)
# =============================================================================

print("=== Python Dictionary (Hash Table) ===")

# Python dict is a hash table
hash_map = {}
hash_map["name"] = "Alice"
hash_map["age"] = 30
hash_map["city"] = "New York"

print(f"Hash map: {hash_map}")
print(f"Get name: {hash_map['name']}")
print(f"Has key 'age': {'age' in hash_map}")
print(f"Keys: {list(hash_map.keys())}")
print(f"Values: {list(hash_map.values())}")


# =============================================================================
# 2. HASH TABLE IMPLEMENTATION (CHAINING)
# =============================================================================

class HashTable:
    """Hash table with chaining for collision resolution"""

    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        """Hash function - maps key to index"""
        if isinstance(key, str):
            hash_val = sum(ord(c) for c in key)
        elif isinstance(key, int):
            hash_val = key
        else:
            hash_val = hash(key)
        return hash_val % self.size

    def insert(self, key, value):
        """Insert key-value pair. O(1) average."""
        index = self._hash(key)

        # Check if key already exists
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return

        # New key
        self.table[index].append((key, value))
        self.count += 1

        # Resize if load factor > 0.7
        if self.count / self.size > 0.7:
            self._resize()

    def get(self, key):
        """Get value by key. O(1) average."""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        """Delete key-value pair. O(1) average."""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.count -= 1
                return True
        return False

    def contains(self, key):
        """Check if key exists. O(1) average."""
        index = self._hash(key)
        return any(k == key for k, v in self.table[index])

    def _resize(self):
        """Double the table size when load factor is high"""
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    def keys(self):
        """Return all keys. O(n)"""
        return [k for bucket in self.table for k, v in bucket]

    def values(self):
        """Return all values. O(n)"""
        return [v for bucket in self.table for k, v in bucket]

    def items(self):
        """Return all key-value pairs. O(n)"""
        return [(k, v) for bucket in self.table for k, v in bucket]

    def __str__(self):
        pairs = []
        for i, bucket in enumerate(self.table):
            if bucket:
                pairs.append(f"  {i}: {bucket}")
        return "HashTable:\n" + "\n".join(pairs)


print("\n=== Hash Table with Chaining ===")
ht = HashTable()
ht.insert("name", "Alice")
ht.insert("age", 30)
ht.insert("city", "Boston")
ht.insert("job", "Engineer")
ht.insert("email", "alice@example.com")
print(ht)
print(f"Get 'name': {ht.get('name')}")
print(f"Contains 'age': {ht.contains('age')}")
ht.delete("city")
print(f"After delete 'city': {ht.keys()}")


# =============================================================================
# 3. HASH TABLE WITH LINEAR PROBING
# =============================================================================

class LinearProbingHashTable:
    """Hash table with open addressing (linear probing)"""

    def __init__(self, size=10):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0

    def _hash(self, key):
        if isinstance(key, str):
            return sum(ord(c) for c in key) % self.size
        return hash(key) % self.size

    def _probe(self, key):
        """Find index using linear probing"""
        index = self._hash(key)
        start = index

        while self.keys[index] is not None:
            if self.keys[index] == key:
                return index
            index = (index + 1) % self.size
            if index == start:
                raise OverflowError("Hash table is full")
        return index

    def insert(self, key, value):
        if self.count >= self.size:
            raise OverflowError("Hash table is full")

        index = self._probe(key)
        if self.keys[index] is None:
            self.count += 1
        self.keys[index] = key
        self.values[index] = value

    def get(self, key):
        index = self._hash(key)
        start = index

        while self.keys[index] is not None:
            if self.keys[index] == key:
                return self.values[index]
            index = (index + 1) % self.size
            if index == start:
                break
        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        index = self._hash(key)
        start = index

        while self.keys[index] is not None:
            if self.keys[index] == key:
                self.keys[index] = None
                self.values[index] = None
                self.count -= 1
                # Rehash subsequent elements
                self._rehash_after_delete(index)
                return True
            index = (index + 1) % self.size
            if index == start:
                break
        return False

    def _rehash_after_delete(self, deleted_index):
        """Rehash elements that were displaced by the deleted element"""
        index = (deleted_index + 1) % self.size
        while self.keys[index] is not None:
            key, value = self.keys[index], self.values[index]
            self.keys[index] = None
            self.values[index] = None
            self.count -= 1
            self.insert(key, value)
            index = (index + 1) % self.size

    def __str__(self):
        pairs = []
        for i in range(self.size):
            if self.keys[i] is not None:
                pairs.append(f"  {i}: {self.keys[i]}: {self.values[i]}")
        return "LinearProbingHT:\n" + "\n".join(pairs)


print("\n=== Hash Table with Linear Probing ===")
lp = LinearProbingHashTable()
lp.insert("apple", 5)
lp.insert("banana", 3)
lp.insert("cherry", 7)
lp.insert("date", 2)
print(lp)
print(f"Get 'banana': {lp.get('banana')}")
lp.delete("banana")
print(f"After delete 'banana':")
print(lp)


# =============================================================================
# 4. WORD FREQUENCY COUNTER
# =============================================================================

def word_frequency(text):
    """Count word frequencies using hash table. O(n) time."""
    freq = {}
    words = text.lower().split()
    for word in words:
        word = word.strip(".,!?;:\"'")
        freq[word] = freq.get(word, 0) + 1
    return freq

print("\n=== Word Frequency Counter ===")
text = "the cat sat on the mat the cat ate the rat"
freq = word_frequency(text)
print(f"Text: '{text}'")
print(f"Frequencies: {freq}")
print(f"Most common: {max(freq, key=freq.get)}")


# =============================================================================
# 5. TWO SUM PROBLEM
# =============================================================================

def two_sum_hash(nums, target):
    """Find two numbers that add to target. O(n) time."""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None

print("\n=== Two Sum Problem ===")
nums = [2, 7, 11, 15, 1, 8]
target = 9
result = two_sum_hash(nums, target)
print(f"Array: {nums}, Target: {target}")
if result:
    print(f"Indices: {result} -> {nums[result[0]]} + {nums[result[1]]} = {target}")


# =============================================================================
# 6. GROUP ANAGRAMS
# =============================================================================

def group_anagrams(words):
    """Group anagram strings together. O(n * k log k) time."""
    anagram_map = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word not in anagram_map:
            anagram_map[sorted_word] = []
        anagram_map[sorted_word].append(word)
    return list(anagram_map.values())

print("\n=== Group Anagrams ===")
words = ["eat", "tea", "tan", "ate", "nat", "bat", "tab"]
groups = group_anagrams(words)
print(f"Words: {words}")
print(f"Anagram groups: {groups}")


# =============================================================================
# 7. LRU CACHE
# =============================================================================

from collections import OrderedDict

class LRUCache:
    """Least Recently Used Cache. O(1) get/put."""

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

    def __str__(self):
        return f"LRUCache({dict(self.cache)})"


print("\n=== LRU Cache ===")
cache = LRUCache(3)
cache.put(1, "A")
cache.put(2, "B")
cache.put(3, "C")
print(f"After inserts: {cache}")
cache.get(1)
print(f"After get(1): {cache}")
cache.put(4, "D")
print(f"After put(4, D): {cache}")


# =============================================================================
# 8. HASH SET IMPLEMENTATION
# =============================================================================

class HashSet:
    """Hash set using hash table"""

    def __init__(self):
        self.table = {}

    def add(self, item):
        self.table[item] = True

    def remove(self, item):
        if item in self.table:
            del self.table[item]

    def contains(self, item):
        return item in self.table

    def union(self, other):
        result = HashSet()
        for item in self.table:
            result.add(item)
        for item in other.table:
            result.add(item)
        return result

    def intersection(self, other):
        result = HashSet()
        for item in self.table:
            if other.contains(item):
                result.add(item)
        return result

    def difference(self, other):
        result = HashSet()
        for item in self.table:
            if not other.contains(item):
                result.add(item)
        return result

    def __str__(self):
        return f"HashSet({list(self.table.keys())})"


print("\n=== Hash Set ===")
s1 = HashSet()
for x in [1, 2, 3, 4, 5]:
    s1.add(x)

s2 = HashSet()
for x in [3, 4, 5, 6, 7]:
    s2.add(x)

print(f"Set 1: {s1}")
print(f"Set 2: {s2}")
print(f"Union: {s1.union(s2)}")
print(f"Intersection: {s1.intersection(s2)}")
print(f"Difference (s1 - s2): {s1.difference(s2)}")


# =============================================================================
# 9. FREQUENCY MAP FOR ANAGRAM CHECK
# =============================================================================

def are_anagrams(s1, s2):
    """Check if two strings are anagrams. O(n) time."""
    if len(s1) != len(s2):
        return False

    freq = {}
    for c in s1:
        freq[c] = freq.get(c, 0) + 1
    for c in s2:
        freq[c] = freq.get(c, 0) - 1
        if freq[c] < 0:
            return False
    return True

print("\n=== Anagram Check ===")
print(f"'listen' and 'silent': {are_anagrams('listen', 'silent')}")
print(f"'hello' and 'world': {are_anagrams('hello', 'world')}")
print(f"'a gentleman' and 'elegant man': {are_anagrams('a gentleman', 'elegant man')}")


# =============================================================================
# 10. CONSISTENT HASHING (SIMPLE)
# =============================================================================

class ConsistentHash:
    """Simple consistent hashing for distributed systems"""

    def __init__(self, nodes=None, virtual_nodes=150):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []
        self.nodes = set()

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key):
        return hash(key) % (2**32)

    def add_node(self, node):
        self.nodes.add(node)
        for i in range(self.virtual_nodes):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node):
        self.nodes.discard(node)
        for i in range(self.virtual_nodes):
            key = self._hash(f"{node}:{i}")
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)

    def get_node(self, key):
        if not self.ring:
            return None
        hash_val = self._hash(key)
        for ring_key in self.sorted_keys:
            if hash_val <= ring_key:
                return self.ring[ring_key]
        return self.ring[self.sorted_keys[0]]

    def __str__(self):
        return f"ConsistentHash(nodes={self.nodes})"


print("\n=== Consistent Hashing ===")
ch = ConsistentHash(["Server1", "Server2", "Server3"])
print(f"Nodes: {ch}")
for key in ["user123", "order456", "session789", "data000"]:
    print(f"  '{key}' -> {ch.get_node(key)}")


# =============================================================================
# 11. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Hash Tables - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Hash tables provide O(1) average case operations")
    print("2. Collisions are resolved via chaining or open addressing")
    print("3. Load factor affects performance - resize when > 0.7")
    print("4. Used in: dictionaries, sets, caches, databases")
    print("5. Consistent hashing distributes load in distributed systems")
