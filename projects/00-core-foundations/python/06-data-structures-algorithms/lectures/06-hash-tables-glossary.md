# Glossary: Hash Tables

> Quick reference for all terms introduced in Lecture 06.

---

## B

### Bucket
- **Definition:** A slot in a hash table's internal array where one or more key-value pairs are stored.
- **In chaining:** Each bucket contains a linked list of colliding entries.
- **In open addressing:** Each bucket holds exactly one entry.
- **Related:** Hash Function, Collision, Chaining

```python
# Bucket structure (chaining)
buckets = [
    [("alice", 90)],           # bucket 0
    [],                         # bucket 1 (empty)
    [("bob", 85), ("carol", 92)],  # bucket 2 (collision → chain)
]
```

---

## C

### Chaining (Separate Chaining)
- **Definition:** A collision resolution technique where each bucket contains a linked list (or another collection) of all entries that hash to that index.
- **Related:** Open Addressing, Collision, Bucket

```python
# Chaining example
class HashTable:
    def __init__(self, size):
        self.buckets = [[] for _ in range(size)]
    
    def put(self, key, value):
        index = hash(key) % len(self.buckets)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update
                return
        bucket.append((key, value))  # New entry
```

### Collision
- **Definition:** When two different keys hash to the same index in a hash table.
- **Resolution:** Chaining (linked lists) or open addressing (probing).
- **Related:** Hash Function, Bucket, Chaining, Probing

```
Key "alice" → hash → index 3
Key "carol" → hash → index 3  ← Collision!
```

---

## H

### Hash Function
- **Definition:** A function that converts a key into an integer index for a hash table array.
- **Properties:** Deterministic, uniform distribution, fast to compute.
- **Related:** Hash Code, Bucket, Collision

```python
# Simple hash function
def hash_function(key, table_size):
    return hash(key) % table_size

# Python's built-in hash
print(hash("hello"))    # e.g., 234234234
print(hash(42))         # 42
print(hash((1, 2, 3)))  # Some integer
```

### Hash Code
- **Definition:** The raw integer output of a hash function before mapping to a bucket index.
- **Related:** Hash Function, Bucket Index

```python
# hash_code → bucket_index
hash_code = hash(key)          # Raw hash code
bucket_index = hash_code % table_size  # Mapped to array index
```

### Hash Map
- **Definition:** A data structure that maps keys to values using a hash function. Also called a hash table or dictionary.
- **Python:** Built-in `dict` type.
- **Related:** Hash Table, Dictionary, Key-Value Pair

```python
# Hash map in Python
scores = {"alice": 90, "bob": 85}
print(scores["alice"])  # O(1) average lookup
```

### Hash Set
- **Definition:** A collection of unique elements backed by a hash table (stores only keys, no values).
- **Python:** Built-in `set` type.
- **Related:** Hash Table, Set, Membership Testing

```python
# Hash set in Python
unique = {1, 2, 3, 4, 5}
print(3 in unique)  # O(1) average membership test
unique.add(6)
unique.discard(1)
```

### Hash Table
- **Definition:** A data structure that stores key-value pairs, providing O(1) average-time insertions, deletions, and lookups using a hash function.
- **Also Known As:** Hash map, dictionary, associative array.
- **Related:** Hash Function, Collision, Load Factor

```python
# Hash table operations
ht = {}
ht["key"] = "value"    # Insert: O(1)
val = ht["key"]        # Lookup: O(1)
del ht["key"]          # Delete: O(1)
```

### Hashing
- **Definition:** The process of computing a hash code from a key and using it to determine the storage location.
- **Related:** Hash Function, Hash Table

---

## K

### Key
- **Definition:** The identifier used to store and retrieve a value in a hash table. Keys must be hashable (immutable).
- **Hashable types:** str, int, float, tuple, frozenset.
- **Unhashable types:** list, dict, set (mutable).
- **Related:** Value, Key-Value Pair, Hash Function

```python
# Valid keys (hashable)
d = {}
d["name"] = "Alice"     # str key
d[42] = "answer"        # int key
d[(1, 2)] = "tuple"     # tuple key

# Invalid keys (unhashable)
# d[[1, 2]] = "list"    # TypeError!
```

---

## L

### Load Factor
- **Definition:** The ratio of the number of entries to the number of buckets in a hash table. α = n / m.
- **When α > threshold (e.g., 0.75):** Trigger rehashing to resize.
- **Related:** Rehashing, Capacity, Collision

```
Load Factor = entries / buckets

Example: 10 entries in 16 buckets → α = 0.625
         12 entries in 16 buckets → α = 0.75 (resize!)
```

---

## O

### Open Addressing
- **Definition:** A collision resolution technique where all entries are stored in the array itself, and collisions are resolved by probing for the next open slot.
- **Variants:** Linear probing, quadratic probing, double hashing.
- **Related:** Chaining, Probing, Linear Probing

```python
# Linear probing
def probe(index, attempt, table_size):
    return (index + attempt) % table_size

# Quadratic probing
def quadratic_probe(index, attempt, table_size):
    return (index + attempt ** 2) % table_size
```

---

## P

### Probing
- **Definition:** The process of searching for the next available slot in open addressing when a collision occurs.
- **Types:** Linear probing, quadratic probing, double hashing.
- **Related:** Open Addressing, Collision, Cluster

```python
# Linear probing: check next slot sequentially
def linear_probe(hash_val, attempt, size):
    return (hash_val + attempt) % size

# Probing sequence: hash, hash+1, hash+2, hash+3, ...
```

---

## R

### Rehashing
- **Definition:** The process of creating a new, larger hash table and reinserting all existing entries when the load factor exceeds a threshold.
- **Typical growth:** Double the capacity.
- **Time:** O(n) — must rehash all entries.
- **Related:** Load Factor, Resize, Capacity

```python
def rehash(self):
    old_table = self.buckets
    self.capacity *= 2
    self.buckets = [[] for _ in range(self.capacity)]
    self.size = 0
    for bucket in old_table:
        for key, value in bucket:
            self.put(key, value)  # Rehash all entries
```

---

## U

### Universal Hashing
- **Definition:** A randomized hash function strategy that minimizes the worst-case collision probability across all key pairs.
- **Related:** Hash Function, Collision

---

## V

### Value
- **Definition:** The data associated with a key in a hash table (key-value pair).
- **Related:** Key, Key-Value Pair, Hash Map

---

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Hash Function | Maps key to index | `hash(key) % size` |
| Collision | Two keys → same index | `hash("alice") == hash("carol")` |
| Chaining | Linked list per bucket | `[ [("a",1)], [("b",2)] ]` |
| Open Addressing | All entries in array | Linear/quadratic probing |
| Load Factor | Entries / buckets | α = 0.75 triggers resize |
| Rehashing | Resize and reinsert all | O(n) operation |
| Key | Hashable identifier | `"alice"`, `42`, `(1,2)` |
| Value | Data stored with key | `90`, `"hello"` |
| Bucket | Slot in the table array | `buckets[3]` |

| Operation | Average | Worst | Note |
|-----------|---------|-------|------|
| Insert | O(1) | O(n) | Resize may be O(n) |
| Lookup | O(1) | O(n) | Depends on hash quality |
| Delete | O(1) | O(n) | With chaining |
| Membership | O(1) | O(n) | `in` operator on set/dict |

| Hashable (Key) | Unhashable (Not Key) |
|----------------|---------------------|
| `str`, `int`, `float` | `list`, `dict`, `set` |
| `tuple` (if all elements hashable) | mutable objects |
| `frozenset`, `bytes` | custom objects without `__hash__` |
