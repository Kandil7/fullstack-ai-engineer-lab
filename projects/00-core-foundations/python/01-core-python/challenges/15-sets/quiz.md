# Challenge 15 — Quiz: Sets

1. Average-case membership (`x in s`) for a `set` of n items is:
   - A) O(n)  (B) O(1)  (C) O(log n)  (D) O(n log n)
2. `list(set(["b", "a", "b"]))` guarantees:
   - A) insertion order  (B) sorted order  (C) no order guarantee  (D) reverse order
3. Which can NOT be a set element?
   - A) `"a"`  (B) `(1, 2)`  (C) `[1, 2]`  (D) `frozenset()`
4. `{"a", "b"} - {"b"}` returns:
   - A) `{"a"}`  (B) `{"b"}`  (C) `{"a", "b"}`  (D) `set()`
5. Deduping 10k ids with `if x not in result` against a *list* costs:
   - A) O(n)  (B) O(n log n)  (C) O(n^2)  (D) O(1)
6. `set(huge_generator)` on a 10^8-item stream:
   - A) stays lazy  (B) materializes every distinct item  (C) is O(1) memory  (D) errors
7. `s1.add(x)` on a set passed in by a caller:
   - A) copies first  (B) mutates the caller's set  (C) raises  (D) returns a new set
8. `{}` creates:
   - A) an empty set  (B) an empty dict  (C) a frozenset  (D) a syntax error

**Answers:** 1-B, 2-C, 3-C, 4-A, 5-C, 6-B, 7-B, 8-B
