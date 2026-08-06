# Typing Advanced — Glossary 23

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Any | Type | Opt-out of type checking; accepts and returns anything |
| Callable | Type | `Callable[[int, str], bool]` — signature-shaped function type |
| Generic | Class | Class parameterized by a type variable: `Result[T]` |
| get_type_hints | API | Resolves stringified annotations into real type objects |
| inspect.signature | API | Introspects parameter names, defaults, and string annotations |
| Literal | Type | A closed set of allowed values: `Literal["dev", "prod"]` |
| nominal typing | Concept | Type identity by class name/inheritance (isinstance semantics) |
| ParamSpec | Type | Captures a function's full signature for decorators |
| PEP 484 | Standard | The original type-hints spec; foundation of `typing` |
| Protocol | Type | Structural contract: any object with matching members qualifies |
| runtime_checkable | Decorator | Lets `isinstance` test a Protocol — shallowly (members only) |
| structural typing | Concept | Type identity by shape: members, not class names |
| TypeGuard | Type | A user function that narrows a value's type for callers |
| TypeVar | Type | A type variable standing for "caller's choice of type" |
| TypeVar bound | Type | Constrains a TypeVar: `TypeVar("Num", bound=float)` |

## Detailed Definitions

### Any
**Definition**: The typing escape hatch. A value annotated `Any` accepts every operation and makes the checker stop verifying — useful at truly dynamic boundaries, corrosive everywhere else. Prefer explicit unions or `Protocol` instead.
**Example**:
```python
from typing import Any

def passthrough(x: Any) -> Any:
    return x

print(passthrough(1) + passthrough(2), passthrough("a") * 2)
```
```text
3 aa
```
**Related**: Callable, TypeGuard

### Callable
**Definition**: The function type: `Callable[[arg types...], return type]`. `Callable[..., T]` accepts any signature. Used with `ParamSpec` when you need to capture the exact signature rather than a shape.
**Example**:
```python
from typing import Callable

def apply(f: Callable[[int], int], n: int) -> int:
    return f(n)

print(apply(lambda x: x * 3, 4))
```
```text
12
```
**Related**: ParamSpec, Protocol

### Generic
**Definition**: A class declared `class Result(Generic[T])` whose behavior and attributes depend on a type parameter chosen by the caller. The type information is erased at runtime but visible to the checker — `Result.success(42)` is a `Result[int]`.
**Example**:
```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

b: Box[int] = Box(42)
print(b.value + 8)
```
```text
50
```
**Related**: TypeVar, TypeVar bound

### get_type_hints
**Definition**: `typing.get_type_hints(func)` resolves annotations — which are stored as strings or special forms — into real type objects, evaluating them in the function's module namespace. The reliable way to inspect a function's true types.
**Example**:
```python
import typing

def f(x: int) -> str:
    return str(x)

print(typing.get_type_hints(f))
```
```text
{'x': <class 'int'>, 'return': <class 'str'>}
```
**Related**: inspect.signature, structural typing

### inspect.signature
**Definition**: `inspect.signature(func)` returns a `Signature` with parameters, defaults, and annotations (as strings unless evaluated). The runtime tool for contract checks — parameter *names* are reliable; annotation objects are not.
**Example**:
```python
import inspect

def call_llm(prompt: str, temperature: float = 0.0) -> str:
    return prompt

sig = inspect.signature(call_llm)
print(list(sig.parameters), sig.parameters["temperature"].default)
```
```text
['prompt', 'temperature'] 0.0
```
**Related**: get_type_hints, ParamSpec

### Literal
**Definition**: `Literal["dev", "prod"]` restricts a value to a closed set — stricter than `str`. The checker rejects anything else at compile time; ideal for model names, environments, and modes that should never be arbitrary strings.
**Example**:
```python
from typing import Literal

Env = Literal["dev", "prod"]

def server(env: Env) -> str:
    return f"starting {env}"

print(server("dev"))
```
```text
starting dev
```
**Related**: TypeGuard, Any

### nominal typing
**Definition**: The "is-a" model: `isinstance(x, Foo)` is true because `Foo` is in the class hierarchy. Python's default, and what `runtime_checkable` protocols pretend to offer with `isinstance` — except protocols check shape, not names.
**Example**:
```python
class Base:
    pass

class Derived(Base):
    pass

print(isinstance(Derived(), Base))
```
```text
True
```
**Related**: structural typing, Protocol, runtime_checkable

### ParamSpec
**Definition**: `ParamSpec("P")` captures the full signature of a decorated callable so the wrapper can forward `P.args`/`P.kwargs`. Without it, decorators flatten every signature to `(*args, **kwargs)` and type checking dies.
**Example**:
```python
from typing import Callable, ParamSpec
import functools

P = ParamSpec("P")

def logged(f: Callable[P, str]) -> Callable[P, str]:
    @functools.wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
        return f(*args, **kwargs)
    return wrapper

@logged
def greet(name: str) -> str:
    return f"hi {name}"

print(greet("ana"))
```
```text
hi ana
```
**Related**: Callable, inspect.signature

### PEP 484
**Definition**: The specification that brought type hints to Python (2015): annotation syntax, `typing` module, and how checkers treat them. Everything in this glossary stands on it; later PEPs (585, 604, 646, 695) modernized the syntax.
**Example**:
```python
from typing import Dict, List, Optional   # PEP 484 era

def f(x: Optional[int]) -> List[int]:
    return [x if x is not None else 0]

print(f(None))
```
```text
[0]
```
**Related**: Protocol, TypeVar

### Protocol
**Definition**: A class decorated base for structural contracts: `class Retriever(Protocol): def retrieve(...)`. Any object whose members match — regardless of class or inheritance — satisfies it. The interface of choice for vendor seams (Qdrant/Chroma/FAISS all "are" retrievers).
**Example**:
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
```text
woof
```
**Related**: structural typing, runtime_checkable, nominal typing

### runtime_checkable
**Definition**: `@runtime_checkable` on a Protocol makes `isinstance(x, Protocol)` work. The check is shallow — it verifies members exist, never their signatures. A class with the right method names but wrong parameter shapes still passes.
**Example**:
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Speaker(Protocol):
    def speak(self) -> str: ...

class Wrong:
    def speak(self, volume: int) -> str:    # wrong signature, right name
        return "x"

print(isinstance(Wrong(), Speaker))
```
```text
True   # shallow: name exists, signature unchecked
```
**Related**: Protocol, structural typing, inspect.signature

### structural typing
**Definition**: Type identity by shape rather than class name: "if it quacks, it's a duck." `Protocol` implements it. It is what lets one `search(retriever)` accept any store with a `retrieve` method, and what makes fakes indistinguishable from real dependencies.
**Example**:
```python
from typing import Protocol

class HasLen(Protocol):
    def __len__(self) -> int: ...

def size(x: HasLen) -> int:
    return len(x)

print(size([1, 2]), size("abc"), size({1: 2}))
```
```text
2 3 1
```
**Related**: Protocol, nominal typing, TypeGuard

### TypeGuard
**Definition**: A function annotated `-> TypeGuard[X]` that promises: if it returns True, the argument is an `X`. Callers' code after the check is narrowed accordingly. Only truthful when the check genuinely distinguishes — structural lookalikes fool it.
**Example**:
```python
from typing import TypeGuard

class Real:
    def __init__(self) -> None:
        self.kind = "real"

def is_real(obj: object) -> TypeGuard[Real]:
    return hasattr(obj, "kind") and obj.kind == "real"   # distinguishing marker

print(is_real(Real()), is_real(object()))
```
```text
True False
```
**Related**: Protocol, Any, Literal

### TypeVar
**Definition**: `T = TypeVar("T")` declares a placeholder type chosen per call site. It preserves relationships — the function's output type matches its input — which `Any` and concrete types cannot express.
**Example**:
```python
from typing import TypeVar

T = TypeVar("T")

def identity(x: T) -> T:
    return x

print(identity(10), identity("s"))
```
```text
10 s
```
**Related**: Generic, TypeVar bound

### TypeVar bound
**Definition**: `TypeVar("Num", bound=float)` restricts what types may fill `Num` — here `int` and `float` but not `str`. The result keeps the caller's exact type: `scale(10, 1.5)` stays an `int` while still being checked.
**Example**:
```python
from typing import TypeVar

Num = TypeVar("Num", bound=float)

def scale(v: Num, factor: float) -> Num:
    return v * factor

i: int = scale(10, 1.5)          # int in -> int out
print(i, scale(2.5, 2.0))
```
```text
15 5.0
```
**Related**: TypeVar, Generic

## Key Concepts Summary

### Contracts Without Inheritance
- `Protocol` = structural typing: shape, not class names.
- `runtime_checkable` = shallow isinstance; verify signatures separately.
- Nominal typing remains for real class hierarchies.

### Generics Preserve Information
- `Generic[T]` parameterizes classes; `TypeVar` preserves call-site types.
- Bounds constrain what may fill the variable.
- All of it is erased at runtime — zero cost.

### Decorators Must Not Lie
- `ParamSpec` forwards the original signature through wrappers.
- `functools.wraps` keeps metadata; `get_type_hints` resolves annotations.
- Annotations are strings at runtime — assert on parameter names.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Protocol — ___
2. ParamSpec — ___
3. Literal — ___
4. TypeGuard — ___
5. runtime_checkable — ___
6. structural typing — ___
7. Generic — ___
8. TypeVar bound — ___
9. get_type_hints — ___
10. nominal typing — ___

A. Shape-based identity: members define the type
B. Structural contract satisfied by matching members
C. Captures a decorated function's true signature
D. Closed value set checked at compile time
E. Narrowing promise trusted by callers
F. Shallow isinstance support on a Protocol
G. Class parameterized by a type variable
H. Constrains which types may fill a TypeVar
I. Resolves stringified annotations to type objects
J. Identity by class name and inheritance

**Answers:** 1-B, 2-C, 3-D, 4-E, 5-F, 6-A, 7-G, 8-H, 9-I, 10-J
