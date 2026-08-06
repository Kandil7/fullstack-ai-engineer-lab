# Design Patterns Advanced — Glossary 26

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Adapter | Pattern | Wraps a vendor API behind your own interface |
| Command | Pattern | Operation as an object with execute/undo |
| composition over inheritance | Principle | Build behavior by holding objects, not by subclassing |
| constructor injection | Technique | Dependencies passed through `__init__`, never built inside |
| decoupling | Goal | Components depend on interfaces, not on each other's internals |
| dependency injection | Pattern | The component receives its dependencies instead of constructing them |
| fake | Test double | A lightweight stand-in satisfying the same protocol as the real thing |
| `__init_subclass__` | Hook | Class method run when a subclass is defined — registry magic |
| open/closed principle | Principle | Open for extension, closed for modification |
| Registry | Pattern | Declarative collection of implementations by name |
| seam | Concept | The stable interface where two parts meet and can be swapped |
| Strategy | Pattern | Swappable algorithm family behind one interface |
| test double | Concept | Umbrella term: fake, stub, mock, spy |
| undo stack | Pattern | History of executed Commands supporting undo/redo |
| vendor lock-in | Risk | Code coupled to one vendor's API, expensive to leave |

## Detailed Definitions

### Adapter
**Definition**: A structural pattern wrapping a vendor-specific API behind your own interface, so the rest of the system speaks only your vocabulary. `QdrantAdapter` and `ChromaAdapter` both implement the same `VectorStore` protocol; callers never see vendor types.
**Example**:
```python
class Store:
    def get(self, key: str) -> str: ...

class RedisAdapter:
    def __init__(self) -> None:
        self._data: dict[str, str] = {}
    def get(self, key: str) -> str:           # redis client would go here
        return self._data.get(key, "")

print(RedisAdapter().get("k"))
```
```text
(empty string)
```
**Related**: seam, vendor lock-in, decoupling

### Command
**Definition**: A behavioral pattern modeling an operation as an object with `execute()` and `undo()`. Callers queue, replay, and reverse operations uniformly — the basis of undo/redo editors and retryable actions.
**Example**:
```python
class InsertCommand:
    def __init__(self, buf: list[str], offset: int, text: str) -> None:
        self._buf, self._offset, self._text = buf, offset, text
    def execute(self) -> None:
        self._buf.insert(self._offset, self._text)
    def undo(self) -> None:
        del self._buf[self._offset]

buf = ["a", "c"]
cmd = InsertCommand(buf, 1, "b")
cmd.execute()
print(buf)
cmd.undo()
print(buf)
```
```text
['a', 'b', 'c']
['a', 'c']
```
**Related**: undo stack, decoupling

### composition over inheritance
**Definition**: The design principle that objects should gain behavior by *holding* other objects (adapters, strategies, injected dependencies) rather than by subclassing. Inheritance couples; composition swaps. Most GoF patterns are composition in disguise.
**Example**:
```python
class Writer:
    def write(self, s: str) -> str:
        return s

class Printer:
    def __init__(self, writer: Writer) -> None:   # holds, not extends
        self._writer = writer
    def print(self, s: str) -> str:
        return self._writer.write(s)

print(Printer(Writer()).print("hi"))
```
```text
hi
```
**Related**: dependency injection, Strategy

### constructor injection
**Definition**: Passing dependencies through `__init__` parameters: `Summarizer(llm: LLMClient)`. The component never imports or instantiates its vendor, so tests pass a fake and production passes the real client through the same seam.
**Example**:
```python
class Greeter:
    def __init__(self, name: str) -> None:   # injected, not global
        self._name = name
    def greet(self) -> str:
        return f"hi {self._name}"

print(Greeter("ana").greet())
```
```text
hi ana
```
**Related**: dependency injection, fake

### decoupling
**Definition**: The goal state where components interact through stable interfaces and can evolve independently. Coupling is measured in "how much changes when one part changes" — adapters, DI, and strategies all reduce that measure.
**Example**:
```python
class Engine:
    def move(self) -> str:
        return "moving"

class Car:
    def __init__(self, engine: Engine) -> None:   # decoupled from engine impl
        self._engine = engine
    def drive(self) -> str:
        return self._engine.move()

print(Car(Engine()).drive())
```
```text
moving
```
**Related**: seam, dependency injection, Adapter

### dependency injection
**Definition**: The pattern of supplying a component's dependencies from outside rather than letting it construct them. The payoff is honest testing: `Summarizer(FakeLLMClient())` and `Summarizer(OpenAILLM())` are the same line of code, differing only in what is handed in.
**Example**:
```python
class LLM:
    def complete(self, prompt: str) -> str:
        return "real:" + prompt

class FakeLLM:
    def complete(self, prompt: str) -> str:
        return "fake:" + prompt

def run(llm: LLM) -> str:
    return llm.complete("x")

print(run(LLM()), run(FakeLLM()))
```
```text
real:x fake:x
```
**Related**: constructor injection, fake, seam

### fake
**Definition**: A lightweight implementation of an interface used in tests — deterministic, fast, no network. A good fake is *honest*: it satisfies the same protocol and signature as the real dependency, so consumers cannot tell them apart.
**Example**:
```python
class FakeLLMClient:
    def complete(self, prompt: str, temperature: float = 0.0) -> str:
        return f"FAKE:{prompt[:5]}:{temperature}"

print(FakeLLMClient().complete("summarize this doc"))
```
```text
FAKE:summ:0.0
```
**Related**: test double, dependency injection

### `__init_subclass__`
**Definition**: A classmethod hook invoked automatically when a subclass is defined. It lets a parent maintain a registry of its children with zero registration code — write the class, it registers itself.
**Example**:
```python
class Tool:
    registry: dict[str, type["Tool"]] = {}

    def __init_subclass__(cls, **kw) -> None:
        super().__init_subclass__(**kw)
        cls.registry[cls.__name__.lower()] = cls

class Search(Tool):
    pass

class Calculator(Tool):
    pass

print(sorted(Tool.registry))
```
```text
['calculator', 'search']
```
**Related**: Registry, open/closed principle

### open/closed principle
**Definition**: "Open for extension, closed for modification": add new behavior by adding classes (new adapters, strategies, tools) without editing existing ones. Registries and protocol seams are how Python achieves this cheaply.
**Example**:
```python
class Plugin:
    plugins: list[type["Plugin"]] = []

    def __init_subclass__(cls, **kw) -> None:
        super().__init_subclass__(**kw)
        cls.plugins.append(cls)

    def run(self) -> str:
        raise NotImplementedError

class A(Plugin):
    def run(self) -> str:
        return "A"

class B(Plugin):
    def run(self) -> str:
        return "B"

print([p().run() for p in Plugin.plugins])
```
```text
['A', 'B']
```
**Related**: Registry, `__init_subclass__`, decoupling

### Registry
**Definition**: A name → implementation map, populated declaratively. Dispatch looks up the name and instantiates. The LLM tool registry — the model sees the schema, the router calls `registry[name]` — is the AI-system case.
**Example**:
```python
class Tool:
    registry: dict[str, type["Tool"]] = {}

    def __init_subclass__(cls, **kw) -> None:
        super().__init_subclass__(**kw)
        cls.registry[cls.__name__.lower()] = cls

    def run(self, args: dict) -> str:
        raise NotImplementedError

class Calculator(Tool):
    def run(self, args: dict) -> str:
        return str(args.get("a", 0) + args.get("b", 0))

tool = Tool.registry["calculator"]()
print(tool.run({"a": 2, "b": 3}))
```
```text
5
```
**Complexity**: O(1) lookup by name.
**Related**: `__init_subclass__`, open/closed principle

### seam
**Definition**: The stable interface where two parts of a system meet — the place designed for swapping. Every pattern in this lecture is one seam: the adapter seam, the DI constructor parameter, the strategy protocol. Seams are where change is cheap.
**Example**:
```python
from typing import Protocol

class Sender(Protocol):
    def send(self, msg: str) -> str: ...

def notify(s: Sender, msg: str) -> str:      # the seam: any Sender works
    return s.send(msg)

class Email:
    def send(self, msg: str) -> str:
        return f"email:{msg}"

print(notify(Email(), "hi"))
```
```text
email:hi
```
**Related**: decoupling, Adapter, dependency injection

### Strategy
**Definition**: A behavioral pattern that keeps an algorithm family behind one interface and swaps members at runtime — chunking policies, rerankers, eviction rules. The caller stays algorithm-agnostic; the choice happens at construction.
**Example**:
```python
class FixedChunker:
    def __init__(self, size: int) -> None:
        self._size = size
    def chunk(self, text: str) -> list[str]:
        return [text[i:i + self._size] for i in range(0, len(text), self._size)]

def index(text: str, chunker: FixedChunker) -> list[str]:
    return chunker.chunk(text)

print(index("abcdef", FixedChunker(2)))
```
```text
['ab', 'cd', 'ef']
```
**Related**: composition over inheritance, seam

### test double
**Definition**: The umbrella term for any stand-in used in tests: fakes (working lightweight implementations), stubs (fixed canned answers), mocks (recorded expectations), spies (wrapped originals). Fakes are the most honest; mocks the most brittle.
**Example**:
```python
class Stub:
    def complete(self, prompt: str) -> str:
        return "canned"          # same answer every time

print(Stub().complete("anything"))
```
```text
canned
```
**Related**: fake, dependency injection

### undo stack
**Definition**: The Command pattern's bookkeeping: a list of executed commands; undo pops and calls `undo()`, redo re-executes. Each command captured the state needed to reverse itself — capture at construction, not at undo time.
**Example**:
```python
class Append:
    def __init__(self, buf: list[str], item: str) -> None:
        self._buf, self._item = buf, item
    def execute(self) -> None:
        self._buf.append(self._item)
    def undo(self) -> None:
        self._buf.pop()

buf: list[str] = []
history: list[Append] = []
for word in ["a", "b"]:
    c = Append(buf, word)
    c.execute()
    history.append(c)
print(buf)
history[-1].undo()
print(buf)
```
```text
['a', 'b']
['a']
```
**Related**: Command, decoupling

### vendor lock-in
**Definition**: The risk that code is so coupled to one vendor's API that switching costs a rewrite. Adapters are the insurance policy: the vendor hides behind the seam, and migrating means writing one new adapter, not touching callers.
**Example**:
```python
class Store:
    def put(self, k: str, v: str) -> str:
        return f"put {k}={v}"

def save(s: Store, k: str, v: str) -> str:   # depends on OUR interface
    return s.put(k, v)

print(save(Store(), "a", "1"))
```
```text
put a=1
```
**Related**: Adapter, seam, decoupling

## Key Concepts Summary

### Every Pattern Is a Seam
- Adapter seams the vendor out of the domain.
- DI seams construction out of the component.
- Command seams the operation from its execution.
- Strategy seams the algorithm from its caller.
- Seams are where change is cheap and tests are honest.

### Declarative Extension
- `__init_subclass__` keeps registries self-maintaining.
- Open/closed: add classes, don't edit existing ones.
- Registry lookup is O(1); new tools join by existing.

### Testing Through the Seam
- Constructor injection makes fakes indistinguishable from real dependencies.
- Honest fakes satisfy the protocol *and* the signature.
- Test doubles: prefer fakes over brittle mocks.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Adapter — ___
2. Command — ___
3. constructor injection — ___
4. fake — ___
5. `__init_subclass__` — ___
6. Registry — ___
7. Strategy — ___
8. undo stack — ___
9. seam — ___
10. vendor lock-in — ___

A. Wraps a vendor API behind your interface
B. Operation as an object with execute/undo
C. Dependencies passed through __init__
D. Lightweight stand-in satisfying the same protocol
E. Hook that registers subclasses automatically
F. Declarative name -> implementation map
G. Swappable algorithm family behind one interface
H. History of executed commands for undo/redo
I. The stable interface where swapping happens
J. Coupling that makes switching vendors expensive

**Answers:** 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H, 9-I, 10-J
