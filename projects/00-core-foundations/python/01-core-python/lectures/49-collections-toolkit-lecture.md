# 01-core-python — 49: Collections Toolkit — The Workhorses of Retrieval

## Topic Overview

Four standard-library modules do most of the heavy lifting in retrieval and
ranking work: `deque` (O(1) append/pop at both ends), `heapq` (priority
queues and top-k), `bisect` (search and insert into sorted lists in O(log n)),
and `collections` (`Counter`, `defaultdict`, `ChainMap`, `OrderedDict`).
They are measured at **zero occurrences** in the first 41 exercises of this
module — yet `heapq.nlargest(k, ...)` *is* top-k retrieval, and
`deque(maxlen=n)` *is* a sliding conversation window.

The cost model is the centerpiece: `sorted(scores)[:k]` is O(n log n);
`heapq.nlargest(k, scores)` is O(n log k). At n = 10^6 and k = 10 that is
the difference between 20 million comparisons and one million. These four
tools replace half of what people reach for numpy or a database for.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Use `deque` for O(1) work at both ends and `maxlen` ring buffers
2. Build priority queues and top-k selections with `heapq`
3. Search and maintain sorted lists with `bisect` in O(log n)
4. Count tokens and find most-common items with `Counter`
5. Group data without boilerplate using `defaultdict`
6. Layer config lookups with `ChainMap`
7. Explain when `OrderedDict` still matters on modern dicts
8. Compute and justify the complexity of each toolkit operation
9. Combine the tools into a hybrid retrieval pattern

## Prerequisites

| Need | Where |
|------|-------|
| Lists, dicts, sets | `13-lists.py`, `16-dictionaries.py`, `15-sets.py` |
| Sorting and `sorted()` | `13-lists.py`, `12-operators.py` |
| Big-O reasoning | `24-iterators.py` (laziness), `21-functions.py` |
| Dict merge `\|` | `48-comprehensions-and-modern-syntax.py` |

## 1. `deque` — Both Ends, O(1)

A `deque` (double-ended queue) supports `append`, `appendleft`, `pop`, and
`popleft` — all O(1). A `list` only gives O(1) at the *end*: `list.insert(0, x)`
shifts every element and costs O(n). The `maxlen` parameter turns a deque
into a ring buffer that evicts the oldest item automatically.

```python
from collections import deque

recent = deque(maxlen=3)
for t in ["q1", "q2", "q3", "q4"]:
    recent.append(t)
print(f"Sliding window (maxlen=3): {list(recent)}")

jobs = deque(["a", "b", "c"])
print(f"Next job: {jobs.popleft()}, remaining: {list(jobs)}")
```

```
# Output:
# Sliding window (maxlen=3): ['q2', 'q3', 'q4']
# Next job: a, remaining: ['b', 'c']
```

The ring buffer is the exact data structure for a sliding conversation
window in a chat application: keep the last N turns, forget the rest, never
copy the list.

## 2. `heapq` — Priority Queue and Top-K

A heap is a list that maintains the "smallest item first" invariant with
O(log n) push/pop. `heapq.nlargest(k, items)` scans the input once, keeping
a heap of size k — O(n log k) total. This is the algorithm behind top-k
retrieval.

```python
import heapq

scores = [0.1, 0.9, 0.4, 0.8, 0.3, 0.7, 0.2, 0.6]
top3 = heapq.nlargest(3, scores)
print(f"Top-3 scores: {top3}")

pq: list[tuple[int, str]] = []
heapq.heappush(pq, (3, "embedding job"))
heapq.heappush(pq, (1, "health check"))
heapq.heappush(pq, (2, "rerank job"))
while pq:
    print(f"  run: {heapq.heappop(pq)[1]}")
```

```
# Output:
# Top-3 scores: [0.9, 0.8, 0.7]
#   run: health check
#   run: rerank job
#   run: embedding job
```

`heapq` is a min-heap: `heapq.heappop` returns the smallest. For a priority
queue, push `(priority, item)` tuples — the tuple comparison orders by
priority first. `heapq.nlargest`/`nsmallest` return *descending*/ascending
lists respectively and never disturb the input.

## 3. `bisect` — Sorted-List Search in O(log n)

`bisect` finds insertion points in a sorted list with binary search:
`bisect_left` returns the index of the first element >= x (so duplicates go
to the right of existing equal elements), `bisect_right` the first element
> x. `insort` inserts while keeping the list sorted — O(n) for the shift,
but the *search* is O(log n).

```python
import bisect

data = [1, 3, 5, 7, 7, 9]
print(f"bisect_left(7)  -> {bisect.bisect_left(data, 7)}  (first 7)")
print(f"bisect_right(7) -> {bisect.bisect_right(data, 7)}  (after last 7)")

xs: list[int] = [10, 20, 40]
bisect.insort(xs, 30)
print(f"After insort(30): {xs}")
```

```
# Output:
# bisect_left(7)  -> 3  (first 7)
# bisect_right(7) -> 5  (after last 7)
# After insort(30): [10, 20, 30, 40]
```

Use `bisect` when **reads vastly outnumber writes** — e.g., serving
"how many scores are above threshold t?" queries against a stable list.
If writes dominate, a heap or a sorted-container library is better.

## 4. `Counter` — Frequency in One Line

`Counter(iterable)` tallies occurrences in O(n); `most_common(k)` returns
the top-k items in O(n log k) (or O(n log n) if you take all). Counters
also merge with `+`, which makes shard-level aggregation trivial.

```python
from collections import Counter

tokens = ["the", "cat", "the", "dog", "the", "cat"]
freq = Counter(tokens)
print(f"Token counts: {dict(freq)}")
print(f"Top-2: {freq.most_common(2)}")

shard_a = Counter(a=3, b=1)
shard_b = Counter(a=2, c=4)
print(f"Merged: {dict(shard_a + shard_b)}")
```

```
# Output:
# Token counts: {'the': 3, 'cat': 2, 'dog': 1}
# Top-2: [('the', 3), ('cat', 2)]
# Merged: {'a': 5, 'b': 1, 'c': 4}
```

`most_common` tie-breaking follows first-seen order of the underlying dict,
so for a fully deterministic order (e.g., alphabetical among ties) sort the
items yourself: `sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))`.

## 5. `defaultdict` — Grouping Without Boilerplate

`defaultdict(factory)` supplies a fresh default value for *missing keys*
on `__getitem__` — which removes the `get/setdefault` dance from grouping
code. Remember the factory runs only on `__getitem__`; a plain read with
`.get()` does not create keys.

```python
from collections import defaultdict

groups = defaultdict(list)
for word in ["cat", "car", "dog", "door"]:
    groups[word[0]].append(word)
print(f"By first letter: {dict(groups)}")
```

```
# Output:
# By first letter: {'c': ['cat', 'car'], 'd': ['dog', 'door']}
```

Grouping documents by label, tokens by chunk, requests by status code —
all the same shape, and `defaultdict(list)` or `defaultdict(int)` removes
the `if key not in d: d[key] = []` boilerplate.

## 6. `ChainMap` — Layered Lookups

`ChainMap(*maps)` stacks dicts and resolves every key with **first hit
wins**. It is the natural representation of layered configuration:
overrides -> environment -> defaults, with no merging or copying.

```python
from collections import ChainMap

defaults = {"lr": 1e-3, "seed": 0, "gpu": False}
env = {"gpu": True}
overrides = {"lr": 1e-4}
config = ChainMap(overrides, env, defaults)
print(f"ChainMap lr={config['lr']} gpu={config['gpu']} seed={config['seed']}")
```

```
# Output:
# ChainMap lr=0.0001 gpu=True seed=0
```

`lr` came from `overrides`, `gpu` from `env`, `seed` from `defaults` — no
dict was copied or mutated, and the layers stay independently updatable.

## 7. `OrderedDict` vs dict Today

Since Python 3.7, plain dicts preserve insertion order, so most
`OrderedDict` uses are obsolete. It still exists for two things:
`move_to_end` (reordering without rebuild) and `popitem(last=...)` (FIFO
eviction). If you need those, use it; otherwise a plain dict is faster and
smaller.

```python
from collections import OrderedDict

od = OrderedDict(a=1, b=2, c=3)
od.move_to_end("a")
print(f"After move_to_end: {list(od)}")
print(f"popitem(last=False) -> {od.popitem(last=False)} (FIFO)")
```

```
# Output:
# After move_to_end: ['b', 'c', 'a']
# popitem(last=False) -> ('b', 1) (FIFO)
```

## 8. Production Pattern — Hybrid Retrieval Top-K

The toolkit composes: `heapq` for top-k, `deque` for a context window,
`Counter` for query term frequency. This is the skeleton of a retrieval
service's ranking step.

```python
import heapq


def top_k_by_score(docs: dict[str, float], k: int) -> list[tuple[str, float]]:
    """Return the k highest-scoring documents."""
    if k <= 0:
        return []
    return heapq.nlargest(k, docs.items(), key=lambda item: item[1])


docs = {"doc_a": 0.85, "doc_b": 0.91, "doc_c": 0.78, "doc_d": 0.91}
print(f"Top-2 docs: {top_k_by_score(docs, 2)}")
```

```
# Output:
# Top-2 docs: [('doc_b', 0.91), ('doc_d', 0.91)]
```

`nlargest` with a `key` extracts the score per item, so tuples compare by
score, not lexicographically. For 1M candidates and k=10 this is one pass
over the data with a 10-element heap — no full sort, no materialized
ranking table.

## Common Mistakes to Avoid

### Mistake 1: A list for front-insert or sliding-window patterns
```python
# WRONG - insert(0) shifts the whole list, O(n) per call
items.insert(0, x)
window = items[-64:]  # copies 64 elements per step

# CORRECT - O(1) at both ends
from collections import deque
window = deque(items, maxlen=64)
window.appendleft(x)
```

### Mistake 2: `sorted()` for top-k
```python
# WRONG - O(n log n) even when k=10
top = sorted(scores, reverse=True)[:10]

# CORRECT - O(n log k)
top = heapq.nlargest(10, scores)
```

### Mistake 3: Treating a heap as a sorted list
```python
# WRONG - heap[0] is the minimum, but heap[1] is NOT the second minimum
second = pq[1]

# CORRECT - pop or use nsmallest
second = heapq.nsmallest(2, pq)[1]
```

### Mistake 4: `defaultdict` reads create keys by accident
```python
# WRONG - the read itself inserts "missing" with value []
d = defaultdict(list)
_ = d["missing"]          # d now contains "missing"!

# CORRECT - use .get() for read-only access
d = defaultdict(list)
_ = d.get("missing")      # None, and no key created
```

### Mistake 5: Forgetting `key=` in nlargest over pairs
```python
# WRONG - tuples compare lexicographically: ("doc_z", 0.1) > ("doc_a", 0.9)
top = heapq.nlargest(k, docs.items())

# CORRECT - rank by the score field
top = heapq.nlargest(k, docs.items(), key=lambda item: item[1])
```

## Best Practices

1. Reach for `deque(maxlen=n)` for any sliding window or FIFO queue.
2. Use `heapq.nlargest`/`nsmallest` for top-k instead of full sorts.
3. Let `bisect_left`/`bisect_right` define *where* an element would land;
   use the two variants deliberately with duplicates.
4. Use `Counter` for frequency tables and merge shards with `+`.
5. Use `defaultdict(list)`/`defaultdict(int)` for grouping and counting.
6. Model layered config as `ChainMap(overrides, env, defaults)` — no copying.
7. Prefer plain dicts; reach for `OrderedDict` only for `move_to_end`/FIFO.
8. Always state the complexity before choosing a collection in a hot path.

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| `list.insert(0, x)` | O(n) | O(1) | `deque.appendleft` — O(1) |
| `deque.append`/`popleft` | O(1) | O(1) | — |
| `heapq.heappush`/`heappop` | O(log n) | O(1) | — |
| `heapq.heapify(list)` | O(n) | O(1) | — |
| `sorted(xs)[:k]` | O(n log n) | O(n) | `heapq.nlargest(k, xs)` — O(n log k), O(k) |
| `heapq.nlargest(k, xs)` | O(n log k) | O(k) | — |
| `bisect_left`/`bisect_right` | O(log n) | O(1) | — |
| `bisect.insort` | O(n) (shift) | O(1) | a heap for write-heavy workloads |
| `Counter(iterable)` | O(n) | O(n) | — |
| `Counter.most_common(k)` | O(n log k) | O(k) | — |
| `defaultdict` missing key | O(1) amortized | O(1) | — |
| `ChainMap` lookup | O(#layers) | O(1) | — |
| `x in list` | O(n) | O(1) | `x in set` — O(1) |

## AI Engineering Relevance

**Where this shows up:** retrieval ranking, conversation state, token
statistics, and layered configuration in every ML service. These tools are
the stdlib replacement for reaching into numpy or redis.

| Concept here | Used for |
|---|---|
| `heapq.nlargest` | top-k retrieved documents by similarity score |
| `deque(maxlen=n)` | sliding conversation window fed to a chat model |
| `bisect` | "how many scores exceed threshold t" over a stable list |
| `Counter.most_common` | token frequency, stopword detection, label balance |
| `defaultdict(list)` | grouping retrieved chunks by source document |
| `ChainMap` | overrides -> env -> defaults for model config |

**Scale note:** at 10^6 candidates per query and k=10, `sorted` costs ~20
million comparisons per query; `nlargest` costs ~1 million — the difference
between 100 queries/s and 2000 queries/s on one worker. At 10^7 tokens,
`Counter` builds the whole frequency table in one O(n) pass while a
`defaultdict(int)` loop does the same work with more code.

## Practice Exercises

### Exercise 1: Sliding Window (Difficulty: Easy)
Write `recent_turns(turns: list[str], n: int) -> list[str]` returning the
last `n` turns using `deque(maxlen=n)`.

### Exercise 2: Token Top-K (Difficulty: Easy)
Write `top_k_tokens(tokens: list[str], k: int) -> list[tuple[str, int]]`
using `Counter.most_common`, with ties broken alphabetically (sort by
`(-count, token)`).

### Exercise 3: Threshold Count (Difficulty: Medium)
Write `count_above(scores: list[float], t: float) -> int` that counts
scores strictly greater than `t` using `bisect_right` on a pre-sorted list.
State the complexity.

### Exercise 4: Priority Queue Processing (Difficulty: Medium)
Write `run_jobs(jobs: list[tuple[int, str]]) -> list[str]` that executes
jobs in priority order (smallest number first, FIFO on ties) using `heapq`.

### Exercise 5: Grouped Retrieval (Difficulty: Medium)
Write `group_by_source(chunks: list[tuple[str, str]]) -> dict[str, list[str]]`
grouping chunk texts by source id using `defaultdict(list)`, preserving
input order within each group.

### Exercise 6: Streaming Top-K (Difficulty: Hard)
Write `stream_top_k(stream: Iterable[float], k: int) -> list[float]` that
returns the k largest values using a heap of size k, in O(n log k) time and
O(k) memory — it must work for `n = 10**9` without materializing the stream.

## Summary

| Concept | Description |
|---|---|
| `deque` | O(1) at both ends; `maxlen` = automatic ring buffer |
| `heapq` | O(log n) push/pop; `nlargest` = O(n log k) top-k |
| `bisect` | O(log n) search in a sorted list; `insort` inserts |
| `Counter` | O(n) frequency table; `most_common(k)` top-k |
| `defaultdict` | Auto-initialized values for grouping |
| `ChainMap` | Layered lookups, first hit wins, no copying |
| `OrderedDict` | `move_to_end` and FIFO `popitem` still justify it |

The collections toolkit is where Python's standard library earns its keep
in AI work: every retrieval service is a heap, a deque, and a Counter in a
trench coat. Choose the structure by its cost model, and the cost model is
the difference between a service that scales and one that melts under load.

## Quick Reference

| Task | Idiom |
|---|---|
| Sliding window | `deque(maxlen=n)` + `append` |
| FIFO queue | `deque` + `popleft` |
| Top-k | `heapq.nlargest(k, items, key=...)` |
| Priority queue | `heapq.heappush(pq, (prio, item))` |
| Insertion point | `bisect_left(xs, x)` / `bisect_right(xs, x)` |
| Keep sorted | `bisect.insort(xs, x)` |
| Frequency table | `Counter(tokens)` |
| Top-k by count | `freq.most_common(k)` |
| Group by key | `defaultdict(list)` |
| Layered config | `ChainMap(overrides, env, defaults)` |
| Reorder dict | `OrderedDict` + `move_to_end` |

## Next Steps

Next: **[50-datetime-and-timezones](50-datetime-and-timezones-lecture.md)** — timezone-aware time handling for logs, splits, and TTLs.
Continues in: **[02-advanced-python — 11 collections](../../02-advanced-python/lectures/11-collections-lecture.md)** (deeper `collections` coverage).
Official docs: https://docs.python.org/3/library/collections.html and https://docs.python.org/3/library/heapq.html
