# 49: Collections Toolkit — Glossary

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| `appendleft` | Method | O(1) insert at the front of a deque |
| `bisect_left` | Function | Index of the first element >= x in a sorted list |
| `bisect_right` | Function | Index of the first element > x in a sorted list |
| `ChainMap` | Class | Layered dict lookups, first hit wins |
| `Counter` | Class | O(n) frequency table from an iterable |
| `defaultdict` | Class | Dict with an auto-initializer for missing keys |
| `deque` | Class | Double-ended queue, O(1) both ends |
| `heapify` | Function | Turns a list into a heap in O(n) |
| `heappop` | Function | Removes and returns the smallest heap item, O(log n) |
| `heappush` | Function | Adds an item to a heap, O(log n) |
| `insort` | Function | Insert into a sorted list, keeping it sorted |
| `maxlen` | Parameter | Ring-buffer capacity; oldest items evicted |
| `most_common` | Method | Top-k items by count from a Counter |
| `nlargest` | Function | Top-k largest from an iterable, O(n log k) |
| `nsmallest` | Function | Top-k smallest from an iterable, O(n log k) |
| `OrderedDict` | Class | Dict with move_to_end and FIFO popitem |
| `popleft` | Method | O(1) pop from the front of a deque |
| priority queue | Pattern | Items processed smallest-first via a heap |

## Detailed Definitions

### `appendleft`
**Definition**: `deque.appendleft(x)` inserts at the front in O(1) — the
operation that makes a deque the right choice for front-insert patterns
where `list.insert(0, x)` would shift the whole list.

**Example**:
```python
from collections import deque
q = deque([1, 2])
q.appendleft(0)
print(list(q))  # [0, 1, 2]
```

**Complexity**: O(1).

**Related**: `deque`, `popleft`, `maxlen`

### `bisect_left`
**Definition**: `bisect.bisect_left(xs, x)` returns the insertion index for
`x` such that all elements before it are strictly less than `x` — i.e. the
first position where an equal element would sit. For duplicates, it lands
on the *first* equal element.

**Example**:
```python
import bisect
xs = [1, 3, 5, 7, 7, 9]
print(bisect.bisect_left(xs, 7))   # 3
print(bisect.bisect_left(xs, 6))   # 3 (between 5 and 7)
```

**Complexity**: O(log n).

**Related**: `bisect_right`, `insort`

### `bisect_right`
**Definition**: `bisect.bisect_right(xs, x)` returns the insertion index
*after* all equal elements — the first position where an element is
strictly greater than `x`. Use it to count elements <= x via the difference
of the two variants.

**Example**:
```python
import bisect
xs = [1, 3, 5, 7, 7, 9]
print(bisect.bisect_right(xs, 7))   # 5 (past the second 7)
print(bisect.bisect_right(xs, 7) - bisect.bisect_left(xs, 7))  # 2 (count of 7s)
```

**Complexity**: O(log n).

**Related**: `bisect_left`, `insort`

### `ChainMap`
**Definition**: A view over a stack of dicts that resolves each key with
first-hit-wins semantics, without copying or mutating any layer. The
standard model for config precedence: overrides -> env -> defaults.

**Example**:
```python
from collections import ChainMap
cfg = ChainMap({"lr": 1e-4}, {"lr": 1e-3, "seed": 0})
print(cfg["lr"], cfg["seed"])  # 0.0001 0
```

**Complexity**: O(#layers) per lookup.

**Related**: dict merge `|`, `defaultdict`

### `Counter`
**Definition**: A dict subclass that tallies occurrences of an iterable's
elements in one O(n) pass. `most_common(k)` returns the top-k as
`(item, count)` pairs; counters merge with `+`.

**Example**:
```python
from collections import Counter
freq = Counter(["a", "b", "a", "a"])
print(dict(freq))              # {'a': 3, 'b': 1}
print(freq.most_common(1))     # [('a', 3)]
```

**Complexity**: O(n) to build; O(n log k) for `most_common(k)`.

**Related**: `defaultdict`, `most_common`

### `defaultdict`
**Definition**: A dict subclass whose `__getitem__` invokes a factory for
missing keys, removing the `if key not in d` boilerplate from grouping and
counting code. Reads via `.get()` do not create keys.

**Example**:
```python
from collections import defaultdict
groups = defaultdict(list)
groups["c"].append(1)
print(dict(groups))   # {'c': [1]}
print(groups.get("x"))  # None - no key created
```

**Complexity**: O(1) amortized per operation.

**Related**: `Counter`, `ChainMap`

### `deque`
**Definition**: A double-ended queue with O(1) append/pop at both ends,
backed by a doubly-linked block list. With `maxlen` it becomes a ring
buffer that evicts the oldest item on overflow.

**Example**:
```python
from collections import deque
d = deque(maxlen=2)
for x in [1, 2, 3]:
    d.append(x)
print(list(d))  # [2, 3]
```

**Complexity**: O(1) per end operation; O(1) amortized append.

**Related**: `appendleft`, `popleft`, `maxlen`

### `heapify`
**Definition**: `heapq.heapify(xs)` rearranges a list in place so it
satisfies the heap invariant (smallest first) in O(n) — faster than n
`heappush` calls (O(n log n)). Use it when you already hold the items.

**Example**:
```python
import heapq
xs = [5, 1, 3]
heapq.heapify(xs)
print(xs[0])  # 1
```

**Complexity**: O(n).

**Related**: `heappush`, `heappop`

### `heappop`
**Definition**: `heapq.heappop(xs)` removes and returns the smallest item,
then restores the heap invariant in O(log n). Popping repeatedly yields
ascending order.

**Example**:
```python
import heapq
xs = [3, 1, 2]
heapq.heapify(xs)
print(heapq.heappop(xs))  # 1
print(heapq.heappop(xs))  # 2
```

**Complexity**: O(log n).

**Related**: `heappush`, `heapify`, `nlargest`

### `heappush`
**Definition**: `heapq.heappush(xs, x)` adds an item and restores the heap
invariant in O(log n). Pairs naturally with `heappop` to form a priority
queue.

**Example**:
```python
import heapq
pq = []
heapq.heappush(pq, (2, "rerank"))
heapq.heappush(pq, (1, "health"))
print(heapq.heappop(pq))  # (1, 'health')
```

**Complexity**: O(log n).

**Related**: `heappop`, `heapify`

### `insort`
**Definition**: `bisect.insort(xs, x)` inserts `x` into a sorted list at
its correct position. The search is O(log n); the list shift makes the
insert O(n). Choose it when reads vastly outnumber writes.

**Example**:
```python
import bisect
xs = [10, 20, 40]
bisect.insort(xs, 30)
print(xs)  # [10, 20, 30, 40]
```

**Complexity**: O(n) time (O(log n) search + O(n) shift), O(1) space.

**Related**: `bisect_left`, `bisect_right`

### `maxlen`
**Definition**: The optional deque capacity. When the deque is full, a new
append evicts the oldest item automatically — the ring-buffer behavior that
models a sliding window.

**Example**:
```python
from collections import deque
w = deque(maxlen=3)
for t in ["q1", "q2", "q3", "q4"]:
    w.append(t)
print(list(w))  # ['q2', 'q3', 'q4']
```

**Complexity**: O(1) per append.

**Related**: `deque`, `appendleft`

### `most_common`
**Definition**: `Counter.most_common(k)` returns the k most frequent
`(item, count)` pairs, descending by count. With no argument it returns all
items. Ties follow first-seen order — sort explicitly for deterministic
tie-breaking.

**Example**:
```python
from collections import Counter
freq = Counter("abacaba")
print(freq.most_common(2))  # [('a', 4), ('b', 2)]
```

**Complexity**: O(n log k); O(n log n) when k == n.

**Related**: `Counter`, `nlargest`

### `nlargest`
**Definition**: `heapq.nlargest(k, iterable, key=...)` returns the k
largest elements in descending order, scanning the input once with a
k-element heap: O(n log k) — far cheaper than `sorted(...)[:k]` for small k.

**Example**:
```python
import heapq
scores = {"a": 0.1, "b": 0.9, "c": 0.5}
print(heapq.nlargest(2, scores.items(), key=lambda kv: kv[1]))
# [('b', 0.9), ('c', 0.5)]
```

**Complexity**: O(n log k) time, O(k) space.

**Related**: `nsmallest`, `heappush`

### `nsmallest`
**Definition**: The mirror of `nlargest`: the k smallest elements in
ascending order, O(n log k). Useful for bottom-k analysis (worst-scoring
documents, largest outliers below a floor).

**Example**:
```python
import heapq
print(heapq.nsmallest(2, [5, 1, 4, 2]))  # [1, 2]
```

**Complexity**: O(n log k) time, O(k) space.

**Related**: `nlargest`

### `OrderedDict`
**Definition**: A dict subclass that predates ordered plain dicts (3.7+).
Still valuable for `move_to_end` (reorder without rebuild) and
`popitem(last=False)` (FIFO eviction). For plain insertion-order behavior,
a regular dict is smaller and faster.

**Example**:
```python
from collections import OrderedDict
od = OrderedDict(a=1, b=2)
od.move_to_end("a")
print(list(od))  # ['b', 'a']
print(od.popitem(last=False))  # ('b', 2)
```

**Complexity**: O(1) per operation.

**Related**: dict, `deque`

### `popleft`
**Definition**: `deque.popleft()` removes and returns the front item in
O(1) — the FIFO counterpart to `append`. Together they implement queue
semantics with no list shifting.

**Example**:
```python
from collections import deque
jobs = deque(["a", "b"])
print(jobs.popleft())  # a
print(list(jobs))      # ['b']
```

**Complexity**: O(1).

**Related**: `deque`, `appendleft`

### priority queue
**Definition**: A queue where the smallest (or highest-priority) item is
served first, implemented with a heap: `heappush` to enqueue, `heappop` to
dequeue. Priority is typically the first element of a tuple.

**Example**:
```python
import heapq
pq = []
heapq.heappush(pq, (3, "slow job"))
heapq.heappush(pq, (1, "urgent"))
print(heapq.heappop(pq)[1])  # urgent
```

**Complexity**: O(log n) per operation.

**Related**: `heappush`, `heappop`

## Key Concepts Summary

### Choose the Structure by Cost
| Need | Wrong choice | Right choice |
|---|---|---|
| Front inserts / sliding window | `list.insert(0, x)` — O(n) | `deque` — O(1) |
| Top-k of a big list | `sorted(xs)[:k]` — O(n log n) | `heapq.nlargest` — O(n log k) |
| "Where does x belong?" | `xs.index` or linear scan — O(n) | `bisect_left/right` — O(log n) |
| Frequency table | hand-rolled dict counting | `Counter` — O(n) |
| Grouping | `if key not in d` boilerplate | `defaultdict(list)` |
| Layered config | three dicts merged by hand | `ChainMap` — first hit wins |

### Heap Rules
- `heap[0]` is the minimum; the rest of the heap is **not** sorted.
- Never read `heap[1]` as "second smallest" — use `nsmallest(2)`.
- `heappop` repeatedly = ascending order.

### Counter Rules
- `most_common` tie order is first-seen, not alphabetical — sort
  `(-count, token)` for deterministic output.
- Counters merge with `+`, so shard aggregation is `sum(shards, Counter())`.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. `deque` — ___
2. `nlargest` — ___
3. `bisect_left` — ___
4. `Counter` — ___
5. `defaultdict` — ___
6. `ChainMap` — ___
7. `maxlen` — ___
8. `heappop` — ___
9. `insort` — ___
10. `OrderedDict` — ___

A. Double-ended queue with O(1) operations at both ends
B. Top-k largest in O(n log k)
C. First index where an equal element would sit
D. Frequency table built in O(n)
E. Auto-initializes values for missing keys
F. Layered lookups with first-hit-wins
G. Ring-buffer capacity that evicts the oldest
H. Removes and returns the smallest heap item
I. Inserts into a sorted list, keeping it sorted
J. Dict with `move_to_end` and FIFO `popitem`

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H, 9-I, 10-J
