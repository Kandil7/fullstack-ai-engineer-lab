# Challenge 43 — Quiz: Dataclasses & NamedTuples

1. What does `@dataclass` generate automatically?
   - A) `__init__`, `__repr__`, `__eq__`  (B) only `__init__`  (C) only `__eq__`  (D) nothing
2. `@dataclass(frozen=True)` makes instances:
   - A) faster  (B) immutable and hashable  (C) JSON-serializable  (D) tuple-like
3. Which is the correct mutable default?
   - A) `items: list = []`  (B) `items: list = list()`  (C) `items: list = field(default_factory=list)`  (D) `items: list = field(default=[])`
4. `__post_init__` runs:
   - A) before `__init__`  (B) at the end of `__init__`  (C) on first attribute access  (D) on `__repr__`
5. `slots=True` (3.10+):
   - A) adds a `__dict__`  (B) removes the `__dict__`  (C) enables pickling  (D) sorts fields
6. NamedTuple is:
   - A) mutable  (B) a subclass of `tuple`  (C) slower than dataclass  (D) JSON-native
7. `order=True` compares instances:
   - A) by id  (B) by repr  (C) field-by-field like a tuple  (D) randomly
8. TypedDict is checked:
   - A) at runtime  (B) by type checkers only  (C) by the GC  (D) at import

**Answers:** 1-A, 2-B, 3-C, 4-B, 5-B, 6-B, 7-C, 8-B
