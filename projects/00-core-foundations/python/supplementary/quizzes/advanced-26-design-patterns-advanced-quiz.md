# Design Patterns Advanced Quiz

## Topic Overview
This quiz covers the production patterns: Adapter over vendor APIs,
constructor injection and honest fakes, Command with undo, the
`__init_subclass__` registry, and Strategy swaps — all viewed as
seams.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

---

## Questions

### Question 1
**What does the Adapter pattern wrap?**

A) A vendor-specific API behind your own interface
B) A database table behind a view
C) The event loop behind coroutines
D) A function behind a class

**Difficulty:** Easy

---

### Question 2
**Where does dependency injection pass dependencies?**

A) Through global variables
B) Through the constructor (or explicit setter)
C) Through class attributes defined at import
D) Through environment variables

**Difficulty:** Easy

---

### Question 3
**What is the output of this code?**
```python
class Tool:
    registry = {}
    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        cls.registry[cls.__name__.lower()] = cls

class Search(Tool):
    pass

class Calculator(Tool):
    pass

print(sorted(Tool.registry))
```

A) `['calculator', 'search']`
B) `['Search', 'Calculator']`
C) `['tool']`
D) `[]`

**Difficulty:** Easy

---

### Question 4
**What is the output of this code?**
```python
class Insert:
    def __init__(self, buf, offset, text):
        self._buf, self._offset, self._text = buf, offset, text
    def execute(self):
        self._buf.insert(self._offset, self._text)
    def undo(self):
        del self._buf[self._offset]

buf = ["a", "c"]
cmd = Insert(buf, 1, "b")
cmd.execute()
cmd.undo()
print(buf)
```

A) `['a', 'c']`
B) `['a', 'b', 'c']`
C) `['a', 'b']`
D) `['b', 'c']`

**Difficulty:** Easy

---

### Question 5
**Which is the honest fake?**

A) One satisfying the same protocol and signature as the real dependency
B) One that returns canned answers only for the tested call
C) One that records every call for later assertions
D) One that subclasses the real dependency and overrides everything

**Difficulty:** Easy

---

### Question 6
**The Strategy pattern swaps:**

A) Vendors behind an adapter
B) Algorithms behind one interface
C) Databases behind a connection
D) Threads behind a pool

**Difficulty:** Easy

---

### Question 7
**What is the output of this code?**
```python
class Greeter:
    def __init__(self, name):
        self._name = name
    def greet(self):
        return f"hi {self._name}"

print(Greeter("ana").greet())
```

A) `hi ana`
B) `ana`
C) `hi`
D) `TypeError: missing name`

**Difficulty:** Medium

---

### Question 8
**Why does an undoable `DeleteCommand` need to capture deleted text at construction time?**

A) To make the command faster
B) Because undo must restore the exact content the delete removed
C) Because `del` cannot be reversed
D) Because the buffer might change before undo

**Difficulty:** Medium

---

### Question 9
**What is the output of this code?**
```python
class LLM:
    def complete(self, prompt):
        return "real:" + prompt

class FakeLLM:
    def complete(self, prompt):
        return "fake:" + prompt

def run(llm):
    return llm.complete("x")

print(run(LLM()), run(FakeLLM()))
```

A) `real:x fake:x`
B) `fake:x real:x`
C) `real:x real:x`
D) `x x`

**Difficulty:** Medium

---

### Question 10
**A new tool joins the registry. With `__init_subclass__`, the required work is:**

A) Write the class — registration happens automatically
B) Write the class and add one line to the registry
C) Write the class and update the dispatcher
D) Write the class and restart the interpreter

**Difficulty:** Medium

---

### Question 11
**What does "open for extension, closed for modification" mean here?**

A) Add behavior by adding classes; avoid editing existing ones
B) Never change any file after release
C) Extend by copying and pasting
D) Only the registry file may change

**Difficulty:** Medium

---

### Question 12
**What is the output of this code?**
```python
class FixedChunker:
    def __init__(self, size):
        self._size = size
    def chunk(self, text):
        return [text[i:i + self._size] for i in range(0, len(text), self._size)]

def index(text, chunker):
    return chunker.chunk(text)

print(index("abcdef", FixedChunker(2)))
```

A) `['ab', 'cd', 'ef']`
B) `['ab', 'bc', 'de']`
C) `['a', 'b', 'c', 'd', 'e', 'f']`
D) `['abcdef']`

**Difficulty:** Medium

---

### Question 13
**Which is the primary benefit of constructor injection for testing?**

A) Tests run faster
B) `Summarizer(FakeLLM())` and `Summarizer(RealLLM())` are the same call shape
C) Fakes are smaller
D) No imports needed

**Difficulty:** Medium

---

### Question 14
**What is the output of this code?**
```python
class Append:
    def __init__(self, buf, item):
        self._buf, self._item = buf, item
    def execute(self):
        self._buf.append(self._item)
    def undo(self):
        self._buf.pop()

buf = []
history = []
for word in ["a", "b"]:
    c = Append(buf, word)
    c.execute()
    history.append(c)
history[-1].undo()
print(buf)
```

A) `['a']`
B) `['a', 'b']`
C) `[]`
D) `['b']`

**Difficulty:** Medium

---

### Question 15
**What is a seam?**

A) A comment marking refactor points
B) The stable interface where two parts meet and can be swapped
C) A monorepo boundary
D) An abstract class with no implementations

**Difficulty:** Medium

---

### Question 16
**What is the output of this code?**
```python
class Tool:
    registry = {}
    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        cls.registry[cls.__name__.lower()] = cls
    def run(self, args):
        raise NotImplementedError

class Calculator(Tool):
    def run(self, args):
        return str(args.get("a", 0) + args.get("b", 0))

print(Tool.registry["calculator"]().run({"a": 2, "b": 3}))
```

A) `5`
B) `'23'`
C) `NotImplementedError`
D) `23`

**Difficulty:** Hard

---

### Question 17
**Why prefer fakes over mocks?**

A) Mocks are deprecated in pytest
B) Fakes are honest implementations; mocks encode expectations that over-specify and break on refactors
C) Mocks cannot be imported
D) Fakes are always faster than mocks

**Difficulty:** Hard

---

### Question 18
**A component constructs `self._llm = OpenAILLM()` inside `__init__`. What is the design problem?**

A) It is slow
B) The seam is gone — tests cannot substitute a fake without patching
C) OpenAILLM is not a protocol
D) The constructor is too long

**Difficulty:** Hard

---

### Question 19
**What is the output of this code?**
```python
class Engine:
    def move(self):
        return "moving"

class Car:
    def __init__(self, engine):
        self._engine = engine
    def drive(self):
        return self._engine.move()

print(Car(Engine()).drive())
```

A) `moving`
B) `car moving`
C) `TypeError`
D) `engine`

**Difficulty:** Hard

---

### Question 20
**Which composition is the phase doc's canonical pattern stack?**

A) Registry + Strategy + fake over one adapter
B) Adapter (vector stores) + DI (fake LLM) + registry (tools) + Strategy (chunking)
C) Singleton + Factory + Proxy only
D) Observer + Template Method + Builder

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! The seams are yours.
- 14-17: Good! Review the injection questions.
- 10-13: Fair. Re-read the Adapter and Registry sections.
- Below 10: Revisit the lecture and the exercise before continuing.

---

## Answer Key

1. **A) A vendor-specific API behind your own interface** — the
   adapter's entire job. B, C, D are other concepts.

2. **B) Through the constructor (or explicit setter)** — injection
   means receiving, not fetching. A, C, D are the anti-patterns.

3. **A) `['calculator', 'search']`** — `__init_subclass__` registered
   both under lowercase names. B is the class names as-is, C invents
   a tool, D means registration failed.

4. **A) `['a', 'c']`** — execute inserts `'b'`, undo removes it. B
   is post-execute, C dropped `'c'`, D dropped `'a'`.

5. **A) One satisfying the same protocol and signature as the real
   dependency** — honest fakes are indistinguishable by shape. B is a
   stub, C is a spy, D couples to the real class.

6. **B) Algorithms behind one interface** — the strategy family. A
   is the Adapter's job, C and D are unrelated.

7. **A) `hi ana`** — the injected name flows into the message. B
   drops the greeting, C drops the name, D is false (the name is
   provided).

8. **B) Because undo must restore the exact content the delete
   removed** — captured state at construction. A is false, C is false
   (del is reversible with saved text), D is true but secondary.

9. **A) `real:x fake:x`** — the same call shape, different
   implementations — DI in two lines. B reverses, C duplicates, D
   drops prefixes.

10. **A) Write the class — registration happens automatically** —
    the self-maintaining registry. B and C are the manual drift
    anti-patterns, D is false.

11. **A) Add behavior by adding classes; avoid editing existing
    ones** — the open/closed principle. B is frozen code, C and D are
    false.

12. **A) `['ab', 'cd', 'ef']`** — fixed-size windows over the text.
    B overlaps windows, C is single chars, D is one chunk.

13. **B) `Summarizer(FakeLLM())` and `Summarizer(RealLLM())` are the
    same call shape** — the seam makes fakes first-class. A and C are
    incidental, D is false.

14. **A) `['a']`** — the last append is undone. B is pre-undo, C
    undoes too much, D removes the first item.

15. **B) The stable interface where two parts meet and can be
    swapped** — the definition. A, C, D are false.

16. **A) `5`** — registry lookup, instantiation, and dispatch in one
    line. B is string concatenation of the digits, C would mean no
    implementation, D is `'23'` without the sum.

17. **B) Fakes are honest implementations; mocks encode expectations
    that over-specify and break on refactors** — the testing trade.
    A and C are false, D is not the point.

18. **B) The seam is gone — tests cannot substitute a fake without
    patching** — the DI failure mode. A and D are incidental, C is
    false.

19. **A) `moving`** — the injected engine drives. B invents output,
    C is false (the engine is provided), D is the attribute, not the
    result.

20. **B) Adapter (vector stores) + DI (fake LLM) + registry (tools)
    + Strategy (chunking)** — the phase doc's canonical stack. A
    mixes roles, C and D are classic-only sets.
