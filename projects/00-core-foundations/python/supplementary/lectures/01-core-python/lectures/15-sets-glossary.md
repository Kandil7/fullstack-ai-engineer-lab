# Python Sets — Glossary 15

## Quick Reference Table

| Term | Description | Example |
|------|-------------|---------|
| Set | Unordered collection of unique elements | `{1, 2, 3}` |
| Frozen Set | Immutable version of a set | `frozenset([1, 2, 3])` |
| Union | All elements from both sets | `a \| b` or `a.union(b)` |
| Intersection | Elements common to both sets | `a & b` or `a.intersection(b)` |
| Difference | Elements in one set but not the other | `a - b` or `a.difference(b)` |
| Symmetric Difference | Elements in either set but not both | `a ^ b` or `a.symmetric_difference(b)` |
| Subset | Set whose elements are all contained in another | `a <= b` or `a.issubset(b)` |
| Superset | Set containing all elements of another | `a >= b` or `a.issuperset(b)` |
| Disjoint | Sets with no common elements | `a.isdisjoint(b)` |
| Hashable | Object that can be used as a set element | `int`, `str`, `tuple` |
| Set Comprehension | Set created with a comprehension expression | `{x for x in range(10)}` |
| Membership Testing | Checking if an element exists in a set | `x in my_set` |
| Deduplication | Removing duplicate elements | `list(set(my_list))` |
| Add | Add an element to a set | `my_set.add(item)` |
| Remove | Remove an element (raises KeyError) | `my_set.remove(item)` |
| Discard | Remove an element (no error if missing) | `my_set.discard(item)` |
| Pop | Remove and return an arbitrary element | `my_set.pop()` |
| Clear | Remove all elements from a set | `my_set.clear()` |
| Copy | Create a shallow copy of a set | `my_set.copy()` |
| Update | Add multiple elements to a set | `my_set.update([1, 2, 3])` |

---

## Definitions

### Add
**Definition**: A method that adds a single element to a set. If the element already exists, the set remains unchanged.

**Example**:
```python
colors = {"red", "blue"}
colors.add("green")
print(colors)  # {'red', 'blue', 'green'}
colors.add("red")  # No effect — already exists
print(colors)  # {'red', 'blue', 'green'}
```

**Related**: `remove()`, `discard()`, `update()`

---

### Clear
**Definition**: A method that removes all elements from a set, leaving it empty.

**Example**:
```python
numbers = {1, 2, 3, 4, 5}
numbers.clear()
print(numbers)  # set()
```

**Related**: `remove()`, `discard()`, `pop()`

---

### Copy
**Definition**: A method that returns a shallow copy of a set. Changes to the copy don't affect the original.

**Example**:
```python
original = {1, 2, 3}
copy_set = original.copy()
copy_set.add(4)
print(original)  # {1, 2, 3}
print(copy_set)  # {1, 2, 3, 4}
```

**Related**: `set()` constructor

---

### Difference
**Definition**: A set operation that returns a new set containing elements that are in the first set but not in the second.

**Example**:
```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
result = a - b  # or a.difference(b)
print(result)  # {1, 2}
```

**Related**: `union()`, `intersection()`, `symmetric_difference()`

---

### Discard
**Definition**: A method that removes an element from a set if it exists. Unlike `remove()`, it does not raise an error if the element is not found.

**Example**:
```python
fruits = {"apple", "banana", "cherry"}
fruits.discard("banana")
print(fruits)  # {'apple', 'cherry'}
fruits.discard("mango")  # No error
```

**Related**: `remove()`, `pop()`, `add()`

---

### Disjoint
**Definition**: A method that returns `True` if two sets have no elements in common.

**Example**:
```python
a = {1, 2, 3}
b = {4, 5, 6}
c = {3, 4, 5}
print(a.isdisjoint(b))  # True — no overlap
print(a.isdisjoint(c))  # False — share element 3
```

**Related**: `intersection()`, `issubset()`

---

### Frozen Set
**Definition**: An immutable version of a set. Once created, elements cannot be added or removed. Can be used as dictionary keys or elements of other sets.

**Example**:
```python
fs = frozenset([1, 2, 3, 4])
print(type(fs))  # <class 'frozenset'>
# fs.add(5)  # AttributeError

# Can be used as dict key
d = {frozenset([1, 2]): "pair"}
```

**Related**: `set()`, immutability, hashability

---

### Hashable
**Definition**: A property of an object that means it has a hash value that never changes during its lifetime. Hashable objects can be used as elements in sets or keys in dictionaries.

**Example**:
```python
# Hashable types
{1, "hello", (1, 2)}  # Valid set

# Non-hashable types (cannot be set elements)
# {[1, 2]}  # TypeError
# {{'a': 1}}  # TypeError
```

**Related**: `frozenset()`, dictionary keys, set elements

---

### Intersection
**Definition**: A set operation that returns a new set containing elements common to both sets.

**Example**:
```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
result = a & b  # or a.intersection(b)
print(result)  # {3, 4}

# Intersection of multiple sets
c = {4, 5, 6, 7}
result = a & b & c  # {4}
```

**Related**: `union()`, `difference()`, `issubset()`

---

### Membership Testing
**Definition**: The operation of checking whether a specific element exists within a set. Sets provide O(1) average time complexity for membership testing.

**Example**:
```python
valid_users = {"alice", "bob", "charlie"}
username = "bob"

if username in valid_users:
    print(f"Welcome, {username}!")  # Output: Welcome, bob!

# Much faster than: username in ["alice", "bob", "charlie"]
```

**Related**: `in` operator, `not in`, lookup time complexity

---

### Pop
**Definition**: A method that removes and returns an arbitrary element from a set. Raises a `KeyError` if the set is empty.

**Example**:
```python
numbers = {1, 2, 3}
popped = numbers.pop()
print(popped)  # 1 (or 2 or 3 — arbitrary)
print(numbers)  # remaining elements
```

**Related**: `remove()`, `discard()`, `clear()`

---

### Remove
**Definition**: A method that removes a specified element from a set. Raises a `KeyError` if the element is not found.

**Example**:
```python
fruits = {"apple", "banana", "cherry"}
fruits.remove("banana")
print(fruits)  # {'apple', 'cherry'}

# fruits.remove("mango")  # KeyError: 'mango'
```

**Related**: `discard()`, `pop()`, `add()`

---

### Set
**Definition**: An unordered collection of unique, immutable (hashable) elements. Defined using curly braces `{}` or the `set()` constructor.

**Example**:
```python
# Creating sets
s1 = {1, 2, 3}
s2 = set([1, 2, 3])
s3 = set("hello")  # {'h', 'e', 'l', 'o'}
```

**Related**: `frozenset()`, set operations, set comprehension

---

### Set Comprehension
**Definition**: A concise way to create sets using a single line of code with the syntax `{expression for item in iterable if condition}`.

**Example**:
```python
# Squares of even numbers
squares = {x**2 for x in range(10) if x % 2 == 0}
print(squares)  # {0, 4, 16, 36, 64}

# First letters of names
names = ["Alice", "Bob", "Charlie"]
first_letters = {name[0] for name in names}
print(first_letters)  # {'A', 'B', 'C'}
```

**Related**: list comprehension, dictionary comprehension, generator expression

---

### Subset
**Definition**: A set A is a subset of set B if every element of A is also an element of B.

**Example**:
```python
a = {1, 2}
b = {1, 2, 3, 4}
print(a.issubset(b))  # True
print(a <= b)         # True

# Every set is a subset of itself
print(a.issubset(a))  # True
```

**Related**: `issuperset()`, `issubset()`, `<=`, `>=`

---

### Superset
**Definition**: A set A is a superset of set B if A contains all elements of B.

**Example**:
```python
a = {1, 2, 3, 4}
b = {1, 2}
print(a.issuperset(b))  # True
print(a >= b)           # True
```

**Related**: `issubset()`, `<=`, `>=`

---

### Symmetric Difference
**Definition**: A set operation that returns elements that are in either set, but not in both.

**Example**:
```python
a = {1, 2, 3}
b = {3, 4, 5}
result = a ^ b  # or a.symmetric_difference(b)
print(result)  # {1, 2, 4, 5}
```

**Related**: `union()`, `intersection()`, `difference()`

---

### Union
**Definition**: A set operation that returns a new set containing all elements from both sets.

**Example**:
```python
a = {1, 2, 3}
b = {3, 4, 5}
result = a | b  # or a.union(b)
print(result)  # {1, 2, 3, 4, 5}

# Union of multiple sets
c = {5, 6, 7}
result = a | b | c  # {1, 2, 3, 4, 5, 6, 7}
```

**Related**: `intersection()`, `difference()`, `|` operator

---

### Update
**Definition**: A method that adds multiple elements to a set. Can accept any iterable.

**Example**:
```python
s = {1, 2}
s.update([3, 4, 5])
print(s)  # {1, 2, 3, 4, 5}

s.update({6, 7}, {8})
print(s)  # {1, 2, 3, 4, 5, 6, 7, 8}
```

**Related**: `add()`, `|=`

---

## Code Examples

### Example 1: Deduplication
```python
# Remove duplicates from a list
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = list(set(data))
print(unique)  # [1, 2, 3, 4] (order may vary)
```

### Example 2: Find Common Elements
```python
# Find common elements in multiple lists
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
list3 = [5, 6, 7, 8, 9]

common = set(list1) & set(list2) & set(list3)
print(common)  # {5}
```

### Example 3: Set Operations in Practice
```python
# Which customers bought both products?
product_a_buyers = {"alice", "bob", "charlie", "diana"}
product_b_buyers = {"bob", "diana", "eve", "frank"}

both = product_a_buyers & product_b_buyers
only_a = product_a_buyers - product_b_buyers
only_b = product_b_buyers - product_a_buyers
any_buyer = product_a_buyers | product_b_buyers

print(f"Bought both: {both}")      # {'bob', 'diana'}
print(f"Only product A: {only_a}")  # {'alice', 'charlie'}
print(f"Only product B: {only_b}")  # {'eve', 'frank'}
print(f"Any buyer: {any_buyer}")    # all six customers
```

---

## Related Concepts

- **Dictionary Keys**: Like sets, dictionary keys must be hashable
- **Frozen Sets**: Immutable sets for use as dictionary keys
- **List Comprehensions**: Similar syntax but creates lists, not sets
- **Membership Testing**: `in` operator works on all iterables but is fastest with sets
- **Deduplication**: Converting a list to a set and back removes duplicates
