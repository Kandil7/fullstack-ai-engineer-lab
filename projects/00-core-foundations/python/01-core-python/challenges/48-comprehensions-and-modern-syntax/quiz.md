# Challenge 48 — Quiz: Comprehensions & Modern Syntax

1. A set comprehension `{x for x in xs}` produces:
   - A) a list  (B) a deduplicated set  (C) a dict  (D) a generator
2. Generator expressions use which delimiter?
   - A) `[]`  (B) `()`  (C) `{}`  (D) `<>`
3. `zip(a, b, strict=True)` on mismatched lengths:
   - A) truncates  (B) raises ValueError  (C) returns None  (D) pads with None
4. The walrus operator `:=`:
   - A) is deprecated  (B) assigns inside an expression  (C) compares values  (D) formats strings
5. `f"{x=}"` prints:
   - A) only the value  (B) name and value  (C) the type  (D) nothing
6. `defaults | overrides`:
   - A) mutates defaults  (B) returns a new merged dict  (C) only works on sets  (D) concatenates keys
7. In `[x for b in batches for x in b]`, the outer loop is:
   - A) `for b in batches`  (B) `for x in b`  (C) neither  (D) both
8. `itertools.pairwise([1,2,3])` yields:
   - A) `[(1,2),(2,3)]`  (B) `[(1,3)]`  (C) `[1,2,3]`  (D) permutations

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-A, 8-A
