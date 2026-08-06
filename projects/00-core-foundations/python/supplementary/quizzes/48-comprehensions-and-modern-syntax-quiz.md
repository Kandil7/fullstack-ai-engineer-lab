# Comprehensions & Modern Syntax Quiz

## Topic Overview
This quiz covers list/dict/set comprehensions, generator expressions, the
walrus operator `:=`, `f"{x=}"`, positional-only and keyword-only
parameters, `zip(strict=True)`, `itertools.pairwise`, and dict merging with
`|`. These are the idioms of every AI data pipeline: batch transforms,
streaming corpora, and guarded data alignment.

## Instructions
- Each question has 4 options (A, B, C, D)
- Select the best answer for each question
- Check your answers using the Answer Key at the end
- Track your score: 1 point per correct answer

---

## Questions

### Question 1
**What is the output of this code?**
```python
nums = [1, 2, 3, 4]
squares = [n * n for n in nums if n % 2 == 0]
print(squares)
```

A) [1, 4, 9, 16]
B) [4, 16]
C) [2, 4]
D) [1, 9]

**Difficulty:** Easy

---

### Question 2
**What is the output of this code?**
```python
words = ["cat", "dog", "cat"]
unique = {w.upper() for w in words}
print(unique)
```

A) ['CAT', 'DOG']
B) {'cat', 'dog'}
C) {'CAT', 'DOG'}
D) ['CAT', 'DOG', 'CAT']

**Difficulty:** Easy

---

### Question 3
**What is the output of this code?**
```python
tokens = ["the", "cat", "sat"]
vocab = {w: i for i, w in enumerate(tokens)}
print(vocab["cat"])
```

A) 0
B) 1
C) 2
D) KeyError

**Difficulty:** Easy

---

### Question 4
**Which statement about generator expressions is TRUE?**

A) They are faster than lists for multiple iterations
B) They use O(1) memory and are single-pass
C) They can be indexed like lists
D) They always return a list

**Difficulty:** Easy

---

### Question 5
**What is the output of this code?**
```python
batches = [[1, 2], [3, 4, 5]]
flat = [x for batch in batches for x in batch]
print(flat)
```

A) [[1, 2], [3, 4, 5]]
B) [1, 2, 3, 4, 5]
C) [(1, 2), (3, 4, 5)]
D) [2, 5]

**Difficulty:** Medium

---

### Question 6
**What is the output of this code?**
```python
values = ["1.5", "x", "2.5"]
parsed = [v for v in values if (p := float(v)) is not None]
print(parsed)
```

A) [1.5, 2.5]
B) ['1.5', '2.5']
C) Error: float("x") raises ValueError
D) [1.5, 2.5, None]

**Difficulty:** Medium

---

### Question 7
**What does `zip(strict=True)` do when the inputs have different lengths?**

A) Truncates to the shortest input silently
B) Pads the shorter input with None
C) Raises ValueError
D) Returns an empty list

**Difficulty:** Easy

---

### Question 8
**What is the output of this code?**
```python
def train(model, /, *, epochs: int):
    return f"{model}:{epochs}"

print(train("bert", epochs=3))
```

A) bert:3
B) Error: model must be passed by name
C) bert:epochs
D) Error: epochs must be positional

**Difficulty:** Medium

---

### Question 9
**What is the output of this code?**
```python
defaults = {"lr": 1e-3, "seed": 0}
overrides = {"lr": 1e-4}
merged = defaults | overrides
print(merged)
```

A) {'lr': 1e-04, 'seed': 0}
B) {'lr': 1e-03, 'seed': 0}
C) {'lr': 1e-04}
D) Error: dicts cannot be merged with |

**Difficulty:** Medium

---

### Question 10
**What is the output of this code?**
```python
path = "s3://bucket/key.pt"
print(path.removeprefix("s3://").removesuffix(".pt"))
```

A) bucket/key
B) s3://bucket/key
C) bucket/key.pt
D) Error

**Difficulty:** Easy

---

### Question 11
**What is the output of this code?**
```python
import itertools
deltas = [b - a for a, b in itertools.pairwise([1, 4, 9])]
print(deltas)
```

A) [1, 4, 9]
B) [3, 5]
C) [4, 9]
D) [(1, 4), (4, 9)]

**Difficulty:** Medium

---

### Question 12
**What is the output of this code?**
```python
x = 0
values = [x for x in range(3)]
print(x, values)
```

A) 0 [0, 1, 2]
B) 2 [0, 1, 2]
C) 0 [2, 2, 2]
D) 2 [1, 2, 3]

**Difficulty:** Hard

---

### Question 13
**Which is the correct way to parse each row exactly once with a walrus?**

A) `[p for r in rows if (p := parse(r)) is not None]`
B) `[parse(r) for r in rows if parse(r) is not None]`
C) `[p for r in rows if parse(r) is not None for p in [parse(r)]]`
D) `[parse(r) for r in rows]`

**Difficulty:** Medium

---

### Question 14
**What is the output of this code?**
```python
lr = 3e-4
print(f"{lr=}")
```

A) 0.0003
B) lr=0.0003
C) lr=3e-4
D) 3e-4

**Difficulty:** Easy

---

### Question 15
**What is the output of this code?**
```python
pairs = [(i, j) for i in range(2) for j in range(2) if i != j]
print(pairs)
```

A) [(0, 1), (1, 0)]
B) [(0, 0), (0, 1), (1, 0), (1, 1)]
C) [(0, 1), (1, 1)]
D) [(0, 0), (1, 1)]

**Difficulty:** Medium

---

### Question 16
**A 10GB JSONL corpus must be processed line by line. Which approach keeps
memory flat?**

A) `lines = open(f).readlines()` then loop
B) `for line in open(f): ...` — iterating the file object directly
C) `data = json.load(open(f))` once
D) `lines = [line for line in open(f)]`

**Difficulty:** Medium

---

### Question 17
**What is the output of this code?**
```python
cfg = {"a": 1}
cfg |= {"b": 2, "a": 9}
print(cfg)
```

A) {'a': 1, 'b': 2}
B) {'a': 9, 'b': 2}
C) {'a': 9}
D) Error: |= is not valid

**Difficulty:** Medium

---

### Question 18
**What is the output of this code?**
```python
gen = (i * i for i in range(4))
print(sum(gen), sum(gen))
```

A) 14 14
B) 14 0
C) 0 14
D) Error: generators cannot be summed

**Difficulty:** Hard

---

### Question 19
**Which signature makes `model` positional-only and `lr` keyword-only?**

A) `def train(model, lr):`
B) `def train(model, /, *, lr):`
C) `def train(*, model, /, lr):`
D) `def train(model, *, /, lr):`

**Difficulty:** Medium

---

### Question 20
**What is the output of this code?**
```python
rows = [(" q ", "a"), (" ", "x"), ("q", "")]
cleaned = {(q.strip(), a.strip()) for q, a in rows if q.strip() and a.strip()}
print(cleaned)
```

A) {('q', 'a')}
B) {('q', 'a'), ('', 'x'), ('q', '')}
C) [('q', 'a')]
D) {(' ', 'x')}

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! You think in comprehensions.
- 14-17: Good job! Review the questions you missed.
- 10-13: Fair. Revisit generators and walrus.
- Below 10: Keep practicing! Review the comprehensions material.

---

## Answer Key

1. **B) [4, 16]** — the filter `n % 2 == 0` keeps only even numbers, then
   squares them: 2²=4, 4²=16. A ignores the filter; C squares nothing —
   those are the filtered values themselves; D keeps odds, the opposite
   filter.

2. **C) {'CAT', 'DOG'}** — a set comprehension uppercases and dedupes:
   "cat" appears twice but the set collapses it. A is a list, not a set;
   B forgets the `.upper()` transform; D is the untransformed list with
   duplicates.

3. **B) 1** — `enumerate` assigns 0, 1, 2 to "the", "cat", "sat", so
   `vocab["cat"] == 1`. A is the index of "the"; C is the index of "sat";
   D ignores that "cat" is a key.

4. **B) They use O(1) memory and are single-pass** — laziness is the whole
   point. A is wrong — lists beat generators for repeated iteration. C is
   wrong — generators have no indexing. D is wrong — a generator is not a
   list.

5. **B) [1, 2, 3, 4, 5]** — clauses nest left to right: for each batch, for
   each x in that batch. A is the input unchanged; C is a zip-like pairing
   that never happens; D keeps only the last elements, a different (and
   wrong) reading.

6. **C) Error: float("x") raises ValueError** — the walrus does not make
   `float` safe; "x" cannot be parsed and the exception propagates. A
   assumes invalid rows are skipped; B assumes parsed results stay strings
   (they are floats); D assumes invalid rows become None.

7. **C) Raises ValueError** — `strict=True` turns silent truncation into a
   loud error. A is plain zip behavior; B is `itertools.zip_longest`; D
   never happens.

8. **A) bert:3** — `model` is positional-only (before `/`), and passing it
   positionally is exactly right; `epochs` is keyword-only and passed by
   name. B inverts the rule; C prints the keyword name as text; D says the
   opposite of the `*` rule.

9. **A) {'lr': 1e-04, 'seed': 0}** — `|` merges both dicts with the right
   operand winning on `lr`. B keeps the default lr (wrong winner); C drops
   `seed`; D denies a valid operator.

10. **A) bucket/key** — `removeprefix("s3://")` strips the scheme, then
    `removesuffix(".pt")` strips the extension. B never strips anything;
    C keeps the extension; D is wrong — both methods exist (3.9+).

11. **B) [3, 5]** — pairwise yields (1,4) and (4,9); differences are 3 and
    5. A is the original list; C is the second elements only; D is the
    pairs, not the deltas.

12. **B) 2 [0, 1, 2]** — the comprehension variable `x` leaks (in Python
    3.x comprehensions do not scope their variable), rebinding the outer
    `x` to the last value 2. A assumes no leak; C changes the values; D
    shifts the values as if the loop started at 1.

13. **A) `[p for r in rows if (p := parse(r)) is not None]`** — parse once,
    bind to `p`, test `p`. B parses twice per row (condition and body).
    C parses twice too (the condition plus the inner `for p in [parse(r)]`).
    D parses once but has no validity filter.

14. **B) lr=0.0003** — `f"{lr=}"` prints the name, `=`, and the value. A
    drops the name; C shows the literal spelling instead of the value; D
    is the repr of the literal.

15. **A) [(0, 1), (1, 0)]** — for i in 0..1, for j in 0..1, keep pairs
    where i != j. B includes the diagonal (i == j); C includes (1,1)
    wrongly; D keeps only the diagonal.

16. **B) `for line in open(f): ...` — iterating the file object directly**
    — file objects are lazy iterators, so memory stays O(1) regardless of
    file size. A and D materialize every line into a list (~tens of GB);
    C loads the whole parsed document.

17. **B) {'a': 9, 'b': 2}** — `|=` updates in place; the right operand wins
    on `a` (9 replaces 1) and `b` is added. A keeps the old `a`; C drops
    `b`; D denies a valid operator (3.9+).

18. **B) 14 0** — the first `sum` consumes the generator (0+1+4+9=14); the
    second `sum` sees an exhausted generator and gets 0. A assumes
    reusability; C is the reverse; D is wrong — generators are summable.

19. **B) `def train(model, /, *, lr):`** — `/` makes `model`
    positional-only, `*` makes `lr` keyword-only. A has no markers; C is
    invalid (markers out of order); D is invalid syntax.

20. **A) {('q', 'a')}** — set comprehension: " q " trims to "q", "a" is
    non-empty; the other two rows fail `q.strip() and a.strip()`. B keeps
    the rows that failed the filter; C is a list, not a set; D keeps the
    row that was dropped.

---

*Quiz completed! How did you score?*
