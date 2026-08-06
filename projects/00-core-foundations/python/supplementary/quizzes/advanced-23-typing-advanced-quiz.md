# Typing Advanced Quiz

## Topic Overview
This quiz covers structural typing with `Protocol`, generics and
`TypeVar`, `ParamSpec` decorators, `Literal` and `TypeGuard`,
`runtime_checkable`'s shallow checks, and the truth that annotations
are strings at runtime.

## Instructions
- 20 questions, 4 options each
- Suggested time: 25 minutes
- 1 point per correct answer

---

## Questions

### Question 1
**What makes a class satisfy a `Protocol`?**

A) Inheriting from the protocol class
B) Declaring `implements Protocol`
C) Having members with matching names and shapes
D) Being decorated with `@dataclass`

**Difficulty:** Easy

---

### Question 2
**What is the output of this code?**
```python
from typing import Protocol

class Speaker(Protocol):
    def speak(self) -> str: ...

class Dog:
    def speak(self) -> str:
        return "woof"

def announce(s: Speaker) -> str:
    return s.speak()

print(announce(Dog()))
```

A) `woof`
B) `TypeError: Dog is not a Speaker`
C) (nothing — static types do not run)
D) `<dog object>`

**Difficulty:** Easy

---

### Question 3
**What does `Literal["dev", "prod"]` enforce?**

A) The value is a string of length 3-4
B) The value is one of exactly `"dev"` or `"prod"`
C) The value is a lowercase string
D) The variable can never change

**Difficulty:** Easy

---

### Question 4
**What is the output of this code?**
```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

b: Box[int] = Box(42)
print(b.value + 8)
```

A) `50`
B) `428`
C) `TypeError`
D) `Box(42)`

**Difficulty:** Easy

---

### Question 5
**Which pair must be present for a `runtime_checkable` protocol to pass `isinstance`?**

A) The exact method signatures
B) The method names only
C) A class attribute `__protocol__`
D) The `@dataclass` decorator

**Difficulty:** Easy

---

### Question 6
**What does `TypeGuard` promise to callers?**

A) The function never raises
B) If the guard returns True, the value has the guarded type
C) The argument is never mutated
D) The function is pure

**Difficulty:** Easy

---

### Question 7
**What is the output of this code?**
```python
import typing

def f(x: int) -> str:
    return str(x)

print(typing.get_type_hints(f)["return"].__name__)
```

A) `str`
B) `"str"` (the quoted string)
C) `return`
D) `TypeError`

**Difficulty:** Medium

---

### Question 8
**A decorator without `ParamSpec` collapses a decorated function's signature to:**

A) The original signature, preserved by `functools.wraps`
B) `(*args, **kwargs)` — type checking of arguments dies
C) `(Any)` — one untyped parameter
D) Nothing — the signature is lost entirely

**Difficulty:** Medium

---

### Question 9
**What is the output of this code?**
```python
import inspect

def call_llm(prompt: str, temperature: float = 0.0) -> str:
    return prompt

sig = inspect.signature(call_llm)
print(list(sig.parameters)[1], sig.parameters["temperature"].default)
```

A) `temperature 0.0`
B) `prompt 0.0`
C) `temperature <class 'float'>`
D) `temperature 0.0 str`

**Difficulty:** Medium

---

### Question 10
**Why do runtime checks on annotations often fail?**

A) Annotations are erased before runtime
B) They are stored as strings/special forms and need `get_type_hints` to resolve
C) The `typing` module deletes them after import
D) They only exist inside `if TYPE_CHECKING:` blocks

**Difficulty:** Medium

---

### Question 11
**What is the output of this code?**
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Retriever(Protocol):
    def retrieve(self, query: str, k: int = 5) -> list[str]: ...

class Wrong:
    def retrieve(self, top_k: int) -> list[str]:
        return ["x"] * top_k

print(isinstance(Wrong(), Retriever))
```

A) `False` — the signatures differ
B) `True` — shallow: only member presence is checked
C) `TypeError` — protocols cannot be used with isinstance
D) `None`

**Difficulty:** Medium

---

### Question 12
**What does `TypeVar("Num", bound=float)` accept?**

A) Any type at all
B) `int` and `float` — but not `str`
C) Only the exact type `float`
D) Any numeric *value*, not type

**Difficulty:** Medium

---

### Question 13
**What is the output of this code?**
```python
from typing import Callable, ParamSpec
import functools

P = ParamSpec("P")

def logged(f: Callable[P, str]) -> Callable[P, str]:
    @functools.wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
        return "[" + f(*args, **kwargs) + "]"
    return wrapper

@logged
def greet(name: str) -> str:
    return f"hi {name}"

print(greet("ana"))
```

A) `[hi ana]`
B) `hi ana`
C) `["hi ana"]`
D) `TypeError: missing name`

**Difficulty:** Medium

---

### Question 14
**Which annotation is erased at runtime — costs nothing?**

A) `Protocol` — only the checker sees it
B) `Literal["dev"]` — values are checked at runtime
C) `TypeGuard` — the check itself runs
D) None — all annotations cost memory

**Difficulty:** Medium

---

### Question 15
**What is the output of this code?**
```python
from typing import TypeVar

Num = TypeVar("Num", bound=float)

def scale(v: Num, factor: float) -> Num:
    return v * factor

i: int = scale(10, 1.5)
print(i)
```

A) `10.0`
B) `15`
C) `15.0`
D) `TypeError: int is not a float`

**Difficulty:** Medium

---

### Question 16
**Which is the distinguishing marker a truthful `TypeGuard` should check?**

A) `hasattr(obj, "text")` — any class with that attribute
B) A field only the guarded type has, e.g. `obj.kind == "chunk"`
C) `type(obj).__name__` equality
D) `obj in a list of known instances`

**Difficulty:** Hard

---

### Question 17
**What is the output of this code?**
```python
from typing import Literal

Env = Literal["dev", "prod"]

def server(env: Env) -> str:
    return f"starting {env}"

print(server("dev"))
```

A) `starting dev`
B) `TypeError: 'test' not in Literal`
C) `starting prod`
D) `RuntimeError`

**Difficulty:** Easy

---

### Question 18
**A generic `Result[T]` with `success(42)` is — at runtime — a:**

A) Dict with the value inside
B) Plain object; the type parameter is erased
C) Typed container the interpreter enforces
D) Tuple `(True, 42)`

**Difficulty:** Hard

---

### Question 19
**Which design correctly verifies a protocol implementation at runtime?**

A) `isinstance(x, Retriever)` alone — it is complete
B) `isinstance(x, Retriever)` plus an explicit parameter-name check
C) Comparing `x.__annotations__` with the protocol's
D) `mypy` in a subprocess at import time

**Difficulty:** Hard

---

### Question 20
**Why does `functools.wraps` matter in a `ParamSpec` decorator?**

A) It makes the wrapper faster
B) It copies `__name__`, `__doc__` and `__wrapped__` onto the wrapper
C) It validates `P.args` at runtime
D) It is required for `ParamSpec` to exist

**Difficulty:** Hard

---

## Score Tracking
Count your correct answers: _____ / 20

**Scoring Guide:**
- 18-20: Excellent! The typing toolkit is yours.
- 14-17: Good! Review the shallow-check questions.
- 10-13: Fair. Re-read Protocol and ParamSpec sections.
- Below 10: Revisit the lecture and the exercise before continuing.

---

## Answer Key

1. **C) Having members with matching names and shapes** — structural
   typing. A is nominal thinking, B is invented syntax, D is
   unrelated.

2. **A) `woof`** — structural typing: `Dog` has the shape, so it
   qualifies. B is nominal thinking, C is false (the code runs; types
   are hints), D is false.

3. **B) The value is one of exactly `"dev"` or `"prod"`** — a closed
   set. A and C are looser, D is about immutability, not value sets.

4. **A) `50`** — the generic carries an int; arithmetic works. B
   concatenates, C is false (no runtime type enforcement), D prints
   the object, not the value.

5. **B) The method names only** — the shallow check. A is what
   signature verification would need, C and D are invented.

6. **B) If the guard returns True, the value has the guarded type** —
   the narrowing contract. A, C, D are unrelated promises.

7. **A) `str`** — `get_type_hints` resolves the annotation; the
   class's `__name__` is `str`. B is what `inspect.signature` would
   show raw, C is the key not the value, D is false.

8. **B) `(*args, **kwargs)` — type checking of arguments dies** —
   `ParamSpec` exists to prevent exactly this. A is the
   wraps-metadata part, C and D are false.

9. **A) `temperature 0.0`** — the second parameter and its default.
   B names the first parameter, C prints the default's type, D
   invents a fourth element.

10. **B) They are stored as strings/special forms and need
    `get_type_hints` to resolve** — the stringified-annotations
    truth. A is false (they exist), C is false, D is false (they are
    not erased by TYPE_CHECKING).

11. **B) `True` — shallow: only member presence is checked** — the
    teaching trap from lecture 23. A is what signature verification
    would say, C is false (`@runtime_checkable` enables it), D is
    false.

12. **B) `int` and `float` — but not `str`** — the bound defines the
    intersection. A is an unbounded TypeVar, C is too strict, D
    confuses values with types.

13. **A) `[hi ana]`** — the wrapper wraps the result; ParamSpec
    forwards the typed arguments. B lacks the brackets, C quotes the
    brackets, D is false (the name is passed).

14. **A) `Protocol` — only the checker sees it** — typing constructs
    are erased at runtime. B and C run actual checks, D is false.

15. **C) `15.0`** — the bound allows int in, but the *operation* is
    float multiplication, so runtime prints 15.0. The `int`
    annotation is a checker claim; at runtime `10 * 1.5` is float. B
    ignores the decimal, A is the value, D is false (int is allowed
    by the bound).

16. **B) A field only the guarded type has, e.g. `obj.kind ==
    "chunk"`** — a distinguishing marker makes the guard truthful.
    A is the shallow trap, C is brittle naming, D is not a type
    check.

17. **A) `starting dev`** — Literal is checked statically; at runtime
    the string passes through. B is what the checker would raise at
    compile time for a bad value, C is the wrong value, D is false.

18. **B) Plain object; the type parameter is erased** — generics are
    erased at runtime, the checker keeps the type. A, C, D invent
    runtime machinery.

19. **B) `isinstance(x, Retriever)` plus an explicit parameter-name
    check** — the honest two-layer verification. A is the shallow
    trap, C is unreliable (stringified annotations), D is absurd at
    runtime.

20. **B) It copies `__name__`, `__doc__` and `__wrapped__` onto the
    wrapper** — metadata preservation. A is false, C is false
    (ParamSpec needs no runtime validation), D is false.
