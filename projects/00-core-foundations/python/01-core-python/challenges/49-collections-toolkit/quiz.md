# Challenge 49 — Quiz: Collections Toolkit

1. `deque(maxlen=3)` evicts:
   - A) random items  (B) the oldest  (C) the newest  (D) nothing
2. `heapq.nlargest(k, items)` runs in:
   - A) O(n log n)  (B) O(n log k)  (C) O(n^2)  (D) O(k)
3. `heapq.heappop` returns:
   - A) the largest  (B) the smallest  (C) any item  (D) the newest
4. `bisect.bisect_left([1,3,3,5], 3)` returns:
   - A) 0  (B) 1  (C) 2  (D) 3
5. `Counter("aab").most_common(1)` returns:
   - A) `[("a", 2)]`  (B) `["a"]`  (C) `{"a": 2}`  (D) `2`
6. Reading a missing key via `d["x"]` on a `defaultdict(list)`:
   - A) raises KeyError  (B) inserts `[]` and returns it  (C) returns None  (D) crashes
7. `ChainMap(a, b)["k"]` returns:
   - A) merged values  (B) the first hit  (C) the last hit  (D) a list
8. For top-k of a million scores, the right tool is:
   - A) `sorted()[:k]`  (B) `heapq.nlargest`  (C) `max()`  (D) `bisect`

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-A, 6-B, 7-B, 8-B
