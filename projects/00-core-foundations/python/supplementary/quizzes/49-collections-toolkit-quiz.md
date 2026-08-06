# Collections Toolkit Quiz

## Topic Overview
This quiz covers the standard-library workhorses of retrieval: `deque`,
`heapq`, `bisect`, `Counter`, `defaultdict`, `ChainMap`, and `OrderedDict`.
The emphasis is the cost model — choosing the right structure by its
complexity, because top-k retrieval, sliding windows, and frequency tables
are the daily work of AI engineering.

## Instructions
- Each question has 4 options (A, B, C, D)
- Select the best answer for each question
- Check your answers using the Answer Key at the end
- Track your score: 1 point per correct answer

---

## Questions

### Question 1
**What is the time complexity of `deque.appendleft(x)`?**

A) O(n) — it shifts all elements
B) O(1)
C) O(log n)
D) O(n log n)

**Difficulty:** Easy

---

### Question 2
**What is the output of this code?**
```python
from collections import deque
d = deque(maxlen=3)
for x in [1, 2, 3, 4, 5]:
    d.append(x)
print(list(d))
```

A) [1, 2, 3]
B) [3, 4, 5]
C) [1, 2, 3, 4, 5]
D) [4, 5]

**Difficulty:** Easy

---

### Question 3
**What is the output of this code?**
```python
import heapq
h = []
for x in [5, 1, 3]:
    heapq.heappush(h, x)
print(h[0])
```

A) 5
B) 1
C) 3
D) [1, 3, 5]

**Difficulty:** Easy

---

### Question 4
**Which is the correct complexity of `heapq.nlargest(k, items)`?**

A) O(n log n)
B) O(n log k)
C) O(k log n)
D) O(n + k)

**Difficulty:** Easy

---

### Question 5
**What is the output of this code?**
```python
import bisect
xs = [1, 3, 5, 7, 7, 9]
print(bisect.bisect_left(xs, 7), bisect.bisect_right(xs, 7))
```

A) 3 5
B) 3 4
C) 4 5
D) 3 3

**Difficulty:** Medium

---

### Question 6
**What is the output of this code?**
```python
from collections import Counter
freq = Counter(["a", "b", "a", "c", "a"])
print(freq.most_common(2))
```

A) [('a', 3), ('b', 1)]
B) [('a', 3), ('c', 1)]
C) [('b', 1), ('c', 1)]
D) {'a': 3, 'b': 1}

**Difficulty:** Easy

---

### Question 7
**Which structure should you use for a sliding conversation window of the
last N turns?**

A) `list` with `insert(0, turn)`
B) `deque(maxlen=N)`
C) `sorted` list maintained with `bisect.insort`
D) `heapq` priority queue

**Difficulty:** Easy

---

### Question 8
**What is the output of this code?**
```python
from collections import defaultdict
d = defaultdict(list)
x = d.get("missing")
print(x, "missing" in d)
```

A) [] True
B) None False
C) [] False
D) None True

**Difficulty:** Medium

---

### Question 9
**What is the output of this code?**
```python
from collections import ChainMap
cfg = ChainMap({"lr": 1e-4}, {"lr": 1e-3, "seed": 0})
print(cfg["lr"], cfg["seed"])
```

A) 0.001 0
B) 0.0001 0
C) 0.001 None
D) 0.0001 None

**Difficulty:** Medium

---

### Question 10
**Which is the cheapest way to get the top 10 scores from 10^6 scores?**

A) `sorted(scores, reverse=True)[:10]`
B) `heapq.nlargest(10, scores)`
C) `max(scores)` repeated 10 times
D) `scores.sort(reverse=True)` then slice

**Difficulty:** Medium

---

### Question 11
**What is the output of this code?**
```python
import heapq
pq = []
heapq.heappush(pq, (3, "embed"))
heapq.heappush(pq, (1, "health"))
heapq.heappush(pq, (2, "rerank"))
print(heapq.heappop(pq)[1])
```

A) embed
B) health
C) rerank
D) (1, health)

**Difficulty:** Easy

---

### Question 12
**What is the output of this code?**
```python
import bisect
xs = [10, 20, 40]
bisect.insort(xs, 30)
print(xs)
```

A) [10, 20, 30, 40]
B) [10, 20, 40, 30]
C) [30, 10, 20, 40]
D) [10, 30, 20, 40]

**Difficulty:** Easy

---

### Question 13
**A heap is a partially ordered list. Which statement is TRUE?**

A) `heap[1]` is always the second smallest element
B) Only `heap[0]` is guaranteed to be the minimum
C) The heap is fully sorted in ascending order
D) `heap[-1]` is always the maximum

**Difficulty:** Medium

---

### Question 14
**What is the output of this code?**
```python
from collections import Counter
a = Counter(x=2, y=1)
b = Counter(y=3, z=1)
print(dict(a + b))
```

A) {'x': 2, 'y': 4, 'z': 1}
B) {'x': 2, 'y': 3, 'z': 1}
C) {'x': 2, 'y': 1, 'z': 1}
D) {'x': 2, 'y': 4}

**Difficulty:** Medium

---

### Question 15
**When is `bisect.insort` the right choice?**

A) When writes vastly outnumber reads
B) When reads vastly outnumber writes and the list stays sorted
C) When the list is unsorted
D) When you need O(1) insert

**Difficulty:** Medium

---

### Question 16
**What is the output of this code?**
```python
import heapq
h = [5, 1, 3]
heapq.heapify(h)
print(heapq.heappop(h), heapq.heappop(h))
```

A) 5 3
B) 1 3
C) 3 5
D) 1 5

**Difficulty:** Medium

---

### Question 17
**Which structure is correct for token-frequency top-k over a 10^7-token
corpus?**

A) `Counter(tokens).most_common(k)`
B) `sorted(set(tokens))[:k]`
C) `[tokens.count(t) for t in set(tokens)][:k]`
D) `deque(tokens, maxlen=k)`

**Difficulty:** Medium

---

### Question 18
**What is the output of this code?**
```python
from collections import defaultdict
d = defaultdict(int)
d["a"] += 1
d["b"] += 1
d["a"] += 1
print(dict(d))
```

A) {'a': 2, 'b': 1}
B) {'a': 1, 'b': 1}
C) {'a': 2, 'b': 2}
D) Error: cannot += on missing key

**Difficulty:** Medium

---

### Question 19
**You must repeatedly answer "how many of these 10^6 scores exceed
threshold t?" against a static list. Which structure is best?**

A) A sorted list + `bisect_right` — O(log n) per query
B) A linear scan per query — O(n) each
C) A heap — O(log n) but you lose the sorted order
D) `Counter` — counts are unordered

**Difficulty:** Hard

---

### Question 20
**What is the output of this code?**
```python
from collections import OrderedDict
od = OrderedDict(a=1, b=2, c=3)
od.move_to_end("a")
od.popitem(last=False)
print(list(od))
```

A) ['a', 'b', 'c']
B) ['b', 'c']
C) ['c', 'a']
D) ['a', 'c']

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You choose collections by cost.
- 14-17: Good job! Review the questions you missed.
- 10-13: Fair. Revisit the complexity table.
- Below 10: Keep practicing! Review the collections toolkit material.

---

## Answer Key

1. **B) O(1)** — deques guarantee O(1) at both ends. A describes
   `list.insert(0, x)`. C and D are heap/sort costs, not deque costs.

2. **B) [3, 4, 5]** — `maxlen=3` makes it a ring buffer: each append past
   capacity evicts the oldest, so after five appends the three survivors
   are the last three. A keeps the first three (the ring would have evicted
   them); C ignores the cap; D drops a live element.

3. **B) 1** — a heap always has the minimum at index 0. A is the last
   pushed; C is the second pushed; D is the heap's *eventual pop order*,
   not its current state — `h[0]` is a single value.

4. **B) O(n log k)** — one pass with a k-element heap. A is `sorted()[:k]`.
   C is a confusion of the two; D understates the heap maintenance.

5. **A) 3 5** — `bisect_left` lands on the first 7 (index 3); `bisect_right`
   lands after the last 7 (index 5). B and C misplace one of the two; D
   ignores the duplicate handling.

6. **A) [('a', 3), ('b', 1)]** — most_common descends by count; 'a' leads
   with 3, and among the 1-count ties, first-seen order picks 'b'. B picks
   'c' over 'b' (tie order is not alphabetical); C drops the leader;
   D is a dict, not the list of pairs returned.

7. **B) `deque(maxlen=N)`** — O(1) appends and automatic eviction. A is
   O(n) per insert. C keeps sorted order you do not need. D serves
   priority, not recency.

8. **B) None False** — `.get()` performs a plain read: the factory does
   *not* run and no key is created. A and C assume the factory runs on
   `.get()`; D assumes a key is inserted by the read — the classic
   defaultdict trap.

9. **B) 0.0001 0** — first-hit wins: `lr` comes from the leftmost dict
   (override), `seed` only exists in the defaults layer. A swaps the
   precedence; C and D are wrong because `seed` resolves through the chain.

10. **B) `heapq.nlargest(10, scores)`** — O(n log k) ≈ 10^6 comparisons.
    A and D are O(n log n) ≈ 2×10^7 comparisons; C repeats an O(n) scan
    ten times — O(10n), but it also fails to handle k > 1 cleanly and is
    still slower than a single heap pass.

11. **B) health** — heappop returns the smallest priority first: 1. A is
    the largest priority; C is the middle; D is the tuple, but `[1]`
    extracts the name.

12. **A) [10, 20, 30, 40]** — insort finds the insertion point with binary
    search and shifts to keep the list sorted. B appends; C prepends;
    D inserts at the wrong position.

13. **B) Only `heap[0]` is guaranteed to be the minimum** — the heap
    invariant is partial: parents ≤ children, siblings unordered. A and C
    assume full ordering; D assumes a max-heap layout that plain `heapq`
    does not use.

14. **A) {'x': 2, 'y': 4, 'z': 1}** — Counter `+` merges counts
    element-wise: y = 1+3 = 4. B under-adds y; C ignores b's y; D drops z.

15. **B) When reads vastly outnumber writes and the list stays sorted** —
    the O(log n) search pays off only when inserts are rare. A is the
    opposite regime (use a heap). C violates the sorted precondition.
    D is impossible — insort shifts, O(n).

16. **B) 1 3** — after heapify, pops return ascending order: 1 then 3.
    A and C are non-ascending; D skips 3.

17. **A) `Counter(tokens).most_common(k)`** — one O(n) pass plus O(n log k).
    B sorts *unique* tokens (wrong rank, no counts). C is O(n²) — `count`
    rescans the corpus per unique token. D is a sliding window, not a rank.

18. **A) {'a': 2, 'b': 1}** — `defaultdict(int)` initializes missing keys
    to 0, so `+=` works: a goes 0→1→2, b 0→1. B counts a once; C double
    counts b; D forgets the factory makes `+=` legal.

19. **A) A sorted list + `bisect_right` — O(log n) per query** — the
    static list is sorted once (O(n log n)), then each threshold query is
    O(log n). B is O(n) per query — at 10^6 scores and 10^4 queries that is
    10^10 operations. C loses the ordering needed for counting; D cannot
    count above a threshold.

20. **C) ['c', 'a']** — `move_to_end("a")` reorders to b, c, a; then
    `popitem(last=False)` removes the *first* key (b), leaving c, a.
    A is the pre-move order; B drops the moved key instead of the first
    key; D keeps the wrong survivor after the pop.

---

*Quiz completed! How did you score?*
