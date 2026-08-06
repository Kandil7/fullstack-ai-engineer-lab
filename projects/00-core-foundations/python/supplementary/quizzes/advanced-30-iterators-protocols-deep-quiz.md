# Iterators and Protocols Deep Quiz

## Topic Overview
This quiz covers Python's data-model protocols: the iterator protocol,
the `__getitem__` fallback, Sequence/Mapping ABCs, context managers,
`__call__`, the `__hash__`/`__eq__` contract, total_ordering, and
`__getattr__` vs `__getattribute__`.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

---

## Questions

### Question 1
**What signals the end of iteration in the iterator protocol?**

A) Returning `None` from `__next__`
B) Raising `StopIteration`
C) Raising `IndexError` from `__iter__`
D) Setting a flag attribute named `done`

**Difficulty:** Easy

---

### Question 2
**What is the output of this code?**
```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        v = self.current
        self.current -= 1
        return v

print(list(Countdown(2)))
```

A) `[2, 1]`
B) `[2, 1, 0]`
C) `[1, 0]`
D) `[2, 1, 0, -1]`

**Difficulty:** Easy

---

### Question 3
**Which objects can a `for` loop iterate, even without `__iter__`?**

A) Only lists and tuples
B) Any object with `__getitem__` that raises `IndexError` past the end
C) Any object with a `next` method
D) Only objects that subclass `Iterator`

**Difficulty:** Medium

---

### Question 4
**What is the output of this code?**
```python
class SliceByIndex:
    def __init__(self, items):
        self.items = items

    def __getitem__(self, i):
        return self.items[i]

print(list(SliceByIndex([10, 20, 30])))
```

A) `[10, 20, 30]`
B) `[]`
C) `TypeError: object is not iterable`
D) `[0, 1, 2]`

**Difficulty:** Medium

---

### Question 5
**Which two methods unlock the full `Sequence` ABC interface?**

A) `__iter__` and `__next__`
B) `__len__` and `__getitem__`
C) `__contains__` and `__reversed__`
D) `__eq__` and `__hash__`

**Difficulty:** Easy

---

### Question 6
**What is the output of this code?**
```python
from collections.abc import Sequence

class Pair(Sequence):
    def __init__(self, a, b):
        self._items = (a, b)

    def __len__(self):
        return 2

    def __getitem__(self, i):
        return self._items[i]

p = Pair(1, 2)
print(1 in p, p[1:], list(reversed(p)))
```

A) `True (2,) [2, 1]`
B) `True (1, 2) [2, 1]`
C) `False (2,) [1, 2]`
D) `True (2,) [1, 2]`

**Difficulty:** Medium

---

### Question 7
**What is the hash/eq contract?**

A) `hash(a)` must be the same as `id(a)`
B) If `a == b` then `hash(a) == hash(b)`, and a hash must never change while the object is in a dict/set
C) `a == b` must be `True` for all objects with the same hash
D) Hashing requires defining `__eq__`

**Difficulty:** Easy

---

### Question 8
**What is the output of this code?**
```python
class MutableKey:
    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return hash(self.v)

    def __eq__(self, other):
        return isinstance(other, MutableKey) and self.v == other.v

k = MutableKey("a")
table = {k: 1}
k.v = "b"
fresh = MutableKey("b")
print(fresh == k, fresh in table, len(table))
```

A) `True True 1`
B) `True False 1`
C) `False False 0`
D) `True False 0`

**Difficulty:** Hard

---

### Question 9
**What happens when you define `__eq__` but not `__hash__` on a class?**

A) The class uses `id()` as its hash automatically
B) Instances become unhashable (`__hash__` is set to `None`)
C) Hashing raises a `Warning` but works
D) `__hash__` is inherited from `object` unchanged

**Difficulty:** Medium

---

### Question 10
**What is the output of this code?**
```python
import functools

@functools.total_ordering
class Score:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

    def __lt__(self, other):
        return self.v < other.v

a, b = Score(1), Score(2)
print(a <= b, b >= a, a > b)
```

A) `True True False`
B) `True True True`
C) `False True False`
D) `True False False`

**Difficulty:** Medium

---

### Question 11
**Which of these is the correct way to return a bound handle from `with`?**

A) `__enter__` returns `self`
B) `__enter__` returns `True`
C) `__exit__` returns `self`
D) `with` always binds `None`

**Difficulty:** Easy

---

### Question 12
**What is the output of this code?**
```python
class Session:
    def __init__(self):
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.closed = True
        return False

try:
    with Session() as s:
        raise ValueError("boom")
except ValueError:
    pass
print(s.closed)
```

A) `False`
B) `True`
C) `Error: Session has no attribute closed`
D) `None`

**Difficulty:** Medium

---

### Question 13
**When does `__getattr__` run?**

A) On every attribute access
B) Only when normal attribute lookup fails
C) Only for private attributes
D) Only on class-level attributes

**Difficulty:** Easy

---

### Question 14
**What is the output of this code?**
```python
class Config:
    def __init__(self, known):
        self.known = known

    def __getattr__(self, name):
        return self.known.get(name, 0)

cfg = Config({"batch": 8})
print(cfg.batch, cfg.lr)
```

A) `8 0`
B) `8 8`
C) `0 0`
D) `AttributeError`

**Difficulty:** Medium

---

### Question 15
**Why must `__getattribute__` delegate to `object.__getattribute__`?**

A) To support multiple inheritance
B) To avoid infinite recursion — direct attribute access re-enters `__getattribute__`
C) To make attribute access faster
D) It is optional; delegation is a style choice

**Difficulty:** Medium

---

### Question 16
**What is the output of this code?**
```python
class Adder:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return x + self.n

add10 = Adder(10)
print(add10(5))
```

A) `5`
B) `10`
C) `15`
D) `TypeError: 'Adder' object is not callable`

**Difficulty:** Easy

---

### Question 17
**What is the PyTorch `Dataset` protocol?**

A) `__iter__` and `__next__` only
B) `__len__` and `__getitem__` — a DataLoader needs length and indexing
C) `__call__` and `__enter__`/`__exit__`
D) `__hash__` and `__eq__`

**Difficulty:** Medium

---

### Question 18
**What is the output of this code?**
```python
class TagSet:
    def __init__(self, tags):
        self.tags = {t.lower() for t in tags}

    def __contains__(self, item):
        return isinstance(item, str) and item.lower() in self.tags

print("PY" in TagSet(["py", "ml"]), "java" in TagSet(["py", "ml"]))
```

A) `True False`
B) `True True`
C) `False False`
D) `False True`

**Difficulty:** Medium

---

### Question 19
**A dict whose key's hash changed after insertion shows which symptom?**

A) The dict raises `RuntimeError` on the next lookup
B) Lookups with equal keys miss silently, and the entry stays orphaned
C) The entry automatically re-hashes itself
D) The dict is garbage-collected

**Difficulty:** Hard

---

### Question 20
**Which design prevents the hash-corruption bug entirely?**

A) Overriding `__eq__` to compare by identity
B) A frozen dataclass whose fields are the hash input
C) Defining `__hash__` to return a constant
D) Calling `dict.copy()` before every lookup

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! The data model is yours.
- 14-17: Good! Review the contracts you missed.
- 10-13: Fair. Re-read the key concepts sections.
- Below 10: Revisit the lecture and the exercise before continuing.

---

## Answer Key

1. **B) Raising `StopIteration`** — that is the protocol's exhaustion
   signal, caught by `for` and `next()`. A would make `None` a value,
   C confuses `__iter__` with the fallback, D is a made-up convention.

2. **B) `[2, 1, 0]`** — counts down and includes 0; stops when current
   goes negative. A stops one early, C skips the start value, D includes
   a value past the stop condition.

3. **B) Any object with `__getitem__` that raises `IndexError` past the
   end** — the legacy fallback protocol. A is too narrow (dicts, sets,
   and custom objects iterate), C describes the iterator side (`next` is
   not used by `for`), D is backwards (the ABC is not required).

4. **A) `[10, 20, 30]`** — `__getitem__` with `IndexError` drives
   iteration. B would require the method to return empty immediately,
   C is wrong because the fallback exists, D is the loop index, not the
   items.

5. **B) `__len__` and `__getitem__`** — the ABC derives
   `__contains__`/`__iter__`/`__reversed__`/`index`/`count` from them.
   A is the iterator pair (a different protocol), C is what you get for
   free, D is the hashing pair.

6. **A) `True (2,) [2, 1]`** — membership works (ABC `__contains__`),
   `p[1:]` slices with the tuple, and `reversed` uses `__len__` +
   `__getitem__`. B shows the wrong slice result, C and D show reversed
   order incorrectly or wrong membership.

7. **B) If `a == b` then `hash(a) == hash(b)`, and a hash must never
   change while the object is in a dict/set** — the full contract. A is
   false (hash ≠ id), C is backwards (hash collisions do not imply
   equality), D is false (you may define `__hash__` alone).

8. **B) `True False 1`** — the fresh key equals the mutated key, but the
   dict probes `hash("b")` while the entry sits under `hash("a")`, so
   membership misses and the orphaned entry stays. A would mean no
   corruption, C breaks equality, D wrongly reports an empty dict.

9. **B) Instances become unhashable (`__hash__` is set to `None`)** —
   defining `__eq__` opts out of the default hash. A is false (that is
   object's default only without `__eq__`), C is false, D is false.

10. **A) `True True False`** — `total_ordering` derives `<=`, `>=` from
    `__lt__` + `__eq__`; `a > b` is correctly `False`. B wrongly claims
    `a > b`, C gets `a <= b` wrong, D gets `b >= a` wrong.

11. **A) `__enter__` returns `self`** — `with x as y` binds whatever
    `__enter__` returns. B (`True`) would bind a bool, C is wrong
    (`__exit__` returns suppression, not a handle), D is false.

12. **B) `True`** — `__exit__` runs even when the block raises, closing
    the session; returning `False` lets `ValueError` propagate (caught
    outside). A would mean cleanup failed, C is false (the attribute
    exists), D misreads the flow.

13. **B) Only when normal attribute lookup fails** — the fallback hook.
    A describes `__getattribute__`, C and D are invented rules.

14. **A) `8 0`** — `batch` exists in `known`; `lr` does not, so
    `__getattr__` returns the default 0. B invents a value for `lr`,
    C loses the known value, D forgets the fallback exists.

15. **B) To avoid infinite recursion** — `self.value` inside
    `__getattribute__` re-enters it forever. A is unrelated, C is false
    (delegation is the *only* way out), D is false — it is mandatory.

16. **C) `15`** — `__call__` makes the instance callable; `add10(5)` =
    `5 + 10`. A returns the argument, B returns the bound value, D
    forgets `__call__` exists.

17. **B) `__len__` and `__getitem__`** — DataLoader needs `len(ds)` and
    `ds[i]`. A is the iterator protocol (not what DataLoader requires),
    C mixes other protocols, D is the hashing pair.

18. **A) `True False`** — membership is case-insensitive: "PY" matches
    "py", "java" matches nothing. B invents a match, C loses the
    case-insensitivity, D reverses both results.

19. **B) Lookups with equal keys miss silently, and the entry stays
    orphaned** — the corruption signature: no error, len stays 1, `in`
    returns False. A is false (no runtime error), C is false (dicts do
    not re-hash), D is false (the dict is alive, just wrong).

20. **B) A frozen dataclass whose fields are the hash input** — the hash
    derives from immutable fields, so it can never change; eq/hash are
    generated consistently. A (identity eq) changes semantics, C (constant
    hash) degrades performance and still allows eq/hash mismatch, D
    avoids nothing.
