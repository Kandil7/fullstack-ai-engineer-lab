# Challenge 13 — Quiz: Lists

1. `["a","b","c"][1:99]` returns:
   - A) `IndexError`  (B) `["b","c"]`  (C) `["b"]`  (D) `None`
2. `list.insert(0, x)` on a list of n items costs:
   - A) O(1)  (B) O(log n)  (C) O(n)  (D) O(n^2)
3. For a queue you push to the front of 10^6 times, the right structure is:
   - A) `list` + `insert(0, x)`  (B) `collections.deque` + `appendleft`  (C) `tuple`  (D) `set`
4. `b = a` where `a` is a list, then `b.append(1)`:
   - A) leaves `a` unchanged  (B) appends to `a` too  (C) raises  (D) copies `a` first
5. `b = a.copy()` on `a = [[1], [2]]`, then `b[0].append(9)`:
   - A) `a` unchanged  (B) `a[0]` becomes `[1, 9]`  (C) raises  (D) `b` unchanged
6. To reorder results whose target index you already know, the right cost is:
   - A) O(n log n) via `sorted`  (B) O(n) via indexed assignment  (C) O(n^2)  (D) O(1)
7. `[[]] * 3` produces:
   - A) three independent lists  (B) three references to one list  (C) `[[], [], []]` copies  (D) an error
8. `a[:]` and `list(a)` differ in that:
   - A) `a[:]` is a deep copy  (B) `list(a)` is a deep copy  (C) neither is deep; they are equivalent  (D) `a[:]` aliases `a`

**Answers:** 1-B, 2-C, 3-B, 4-B, 5-B, 6-B, 7-B, 8-C
