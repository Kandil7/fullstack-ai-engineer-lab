# 32 — Metaprogramming Lecture

## 1. Topic Overview

Metaprogramming is **code that writes code**: a decorator that modifies a
function, a class hook that registers subclasses automatically, a registry
that turns a function signature into a JSON schema. Agent frameworks are
built on it — the `@tool` decorator you see in every agent library is
metaprogramming: it reads the function's signature, builds a JSON schema
the LLM can understand, and registers the function in a callable table.

This topic is about *restraint* as much as power. The Python data model
gives you deep hooks (`__init_subclass__`, descriptors, `__set_name__`,
even metaclasses), but the best metaprogramming is often the simplest:
**prefer plain functions, then class decorators, then `__init_subclass__`,
and reach for a metaclass only as a last resort.** The lecture ends with
"when metaprogramming is the wrong answer" — because `eval` on untrusted
input is remote code execution, and a metaclass you do not need is a bug
you will debug for a week.

## 2. Learning Objectives

By the end of this lecture you will be able to:

1. Explain why `__init_subclass__` is usually better than a metaclass, and
   use it to auto-register subclasses.
2. Use `__set_name__` so descriptors learn their attribute name.
3. Distinguish class decorators from metaclasses and `type()` factories.
4. Read a function's signature with `inspect.signature` and build a JSON
   schema from it — the `@tool` mechanism.
5. Load modules dynamically with `importlib`.
6. Resolve nested attribute paths safely with `getattr`/`setattr`.
7. Explain why `exec`/`eval` are dangerous and replace them with dispatch
   tables.
8. Analyze code as data with `ast` (safe) instead of executing it.
9. Describe monkey-patching, its costs, and when it is acceptable.
10. Recognize when metaprogramming is the wrong answer.

## 3. Prerequisites

- **`01-decorators.py`** — decorators are the entry point to this topic.
- **`23-type-hints.py`** — annotations are the raw material for
  signature-driven schemas.
- **`30-iterators-protocols-deep.py`** — descriptors recap lives here.
- Basic classes, inheritance, and `__repr__`.

## 4. Key Concepts

### 4.1 `__init_subclass__` — registration without a metaclass

When you define a subclass, Python calls the parent's `__init_subclass__`
method (if it exists) with the new class. That makes auto-registration
trivial — no metaclass, no magic in the class body:

```python
class ToolRegistry:
    _registry: dict[str, type] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ToolRegistry._registry[cls.__name__] = cls

class SearchTool(ToolRegistry):
    def run(self):
        return "search results"

class EmbedTool(ToolRegistry):
    def run(self):
        return "vector [0.1, 0.2]"

print(sorted(ToolRegistry._registry))
print(ToolRegistry._registry["EmbedTool"]().run())
```

```text
# Output:
# ['EmbedTool', 'SearchTool']
# vector [0.1, 0.2]
```

**Why this matters:** plugin systems work by subclassing a base class in
any module; the base class discovers them. A metaclass would do the same
job, but `__init_subclass__` is *one hook on the parent* — less magic, no
`type.__new__` subclass to reason about.

### 4.2 `__set_name__` — descriptors learn their own name

Descriptors (`__get__`/`__set__`/`__delete__`) are the machinery under
`@property`. Without `__set_name__`, a descriptor has no idea what
attribute it is bound to; with it, Python tells it during class creation:

```python
class Column:
    def __init__(self, dtype):
        self.dtype = dtype
        self.name = "<unset>"

    def __set_name__(self, owner, name):
        self.name = name          # called when the class is built

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.dtype):
            raise TypeError(f"{self.name} must be {self.dtype.__name__}")
        obj.__dict__[self.name] = value

class Row:
    id = Column(int)
    name = Column(str)

row = Row()
row.id = 7
row.name = "doc-1"
print(Row.id.name, Row.name.name)     # descriptors know their names
try:
    row.id = "not-an-int"
except TypeError as exc:
    print(exc)
```

```text
# Output:
# id name
# id must be int, got str
```

**Why this matters:** ORMs (SQLAlchemy, Django) use exactly this to know
which column a descriptor maps to, without you passing the name twice.

### 4.3 Class decorators vs `type()` vs metaclasses

Three ways to influence class creation:

| Mechanism | When | Visibility |
|---|---|---|
| Class decorator (`@with_repr`) | Add/modify after definition | Explicit at the class |
| `type(name, bases, ns)` | Build a class dynamically from data | Explicit at the call |
| Metaclass (`__metaclass__`) | Change class creation for *all* subclasses | Hidden, far-reaching |

A class decorator adds a `__repr__` in place:

```python
def with_repr(cls):
    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({fields})"
    cls.__repr__ = __repr__
    return cls

@with_repr
class Chunk:
    def __init__(self, text, score):
        self.text = text
        self.score = score

print(Chunk("hello", 0.9))
```

```text
# Output:
# Chunk(text='hello', score=0.9)
```

`type()` builds distinct classes from data:

```python
def make_point(name):
    return type(name, (), {"x": 0, "y": 0})

PointA = make_point("PointA")
PointB = make_point("PointB")
print(PointA is PointB)     # distinct classes
p = PointA()
print(p.x, p.y)
```

```text
# Output:
# False
# 0 0
```

**Rule of thumb:** if you can write it as a decorator, do that. `type()`
is for genuinely data-driven factories (e.g. building classes from config
files). Metaclasses are for framework authors who need hooks on *every*
subclass — and even then `__init_subclass__` often suffices.

### 4.4 `inspect.signature` — reading a function's shape

The heart of the `@tool` pattern. `inspect.signature(fn)` returns a
`Signature` whose `.parameters` maps names to `Parameter` objects with
`.annotation`, `.default`, and `.kind`:

```python
import inspect

def embed_documents(docs: list[str], model: str = "base",
                    batch_size: int = 32) -> list[list[float]]:
    """Embed a list of documents."""
    return [[0.1] * batch_size for _ in docs]

sig = inspect.signature(embed_documents)
print(list(sig.parameters))
print(sig.parameters["model"].default)
```

```text
# Output:
# ['docs', 'model', 'batch_size']
# base
```

**Trap:** with `from __future__ import annotations`, annotations are
*strings* at runtime (`"list[str]"`, not `list[str]`). Resolve them with
`typing.get_type_hints(fn)` before mapping to JSON types.

### 4.5 The `@tool` pattern — schema from signature

This is the exact mechanism behind agent frameworks' `@tool` decorators:

```python
from typing import Callable, get_type_hints

TOOL_SCHEMAS = {}
TOOL_FUNCS = {}

def describe(fn):
    sig = inspect.signature(fn)
    hints = get_type_hints(fn)
    schema = {
        "name": fn.__name__,
        "description": (fn.__doc__ or "").strip().splitlines()[0],
        "parameters": {"type": "object", "properties": {}},
    }
    type_map = {str: "string", int: "integer", float: "number",
                bool: "boolean", list: "array", dict: "object"}
    for param in sig.parameters.values():
        if param.name in ("self", "cls"):
            continue
        prop = {}
        annotation = hints.get(param.name, param.annotation)
        if annotation is not inspect.Parameter.empty:
            if annotation in type_map:
                prop["type"] = type_map[annotation]
            elif getattr(annotation, "__origin__", None) is list:
                prop["type"] = "array"
        if param.default is not inspect.Parameter.empty:
            prop["default"] = param.default
        schema["parameters"]["properties"][param.name] = prop
    return schema

def tool(fn):
    TOOL_SCHEMAS[fn.__name__] = describe(fn)
    TOOL_FUNCS[fn.__name__] = fn
    return fn

@tool
def search(query: str, top_k: int = 5) -> list[str]:
    """Search the knowledge base."""
    return [f"result-{i}" for i in range(top_k)]

print(TOOL_SCHEMAS["search"])
```

```text
# Output:
# {'name': 'search', 'description': 'Search the knowledge base.',
#  'parameters': {'type': 'object',
#                 'properties': {'query': {'type': 'string'},
#                                'top_k': {'type': 'integer', 'default': 5}}}}
```

**Why this matters for AI:** the LLM sees `TOOL_SCHEMAS` as the
function-calling contract; when it emits a JSON tool call, your runtime
looks up `TOOL_FUNCS[name]` and invokes it with the LLM-provided
arguments. No hand-written schemas, no drift between code and contract —
the signature *is* the contract.

### 4.6 `importlib` — dynamic import and plugin loading

```python
import importlib

math_mod = importlib.import_module("math")
print(math_mod.floor(3.7))
print(hasattr(math_mod, "sin"))
```

```text
# Output:
# 3
# True
```

Plugin directories work like this: scan a folder for modules, import each
by name, and any class subclassing your base registers itself (4.1).

### 4.7 `getattr`/`setattr` — safe dynamic access

```python
import types

def get_path(obj, path, default=None):
    current = obj
    for part in path.split("."):
        if not hasattr(current, part):
            return default
        current = getattr(current, part)
    return current

class Config:
    def __init__(self):
        self.embedding = types.SimpleNamespace(model="base", dim=384)

cfg = Config()
print(get_path(cfg, "embedding.model"))
print(get_path(cfg, "embedding.unknown", "n/a"))
```

```text
# Output:
# base
# n/a
```

This is how config systems resolve `"model.embedding.dim"` from env or
YAML without a cascade of `if hasattr`.

### 4.8 `exec`/`eval` — and why to avoid them

`eval("2 + 2")` and `exec("do_something()")` run *arbitrary strings as
code*. If any part of that string comes from a user, a model's output, or
a config file, it is **remote code execution** — the attacker's string
*is* your program.

The replacement is a dispatch table:

```python
def op_a():
    return 1

def op_b():
    return 2

table = {"op_a": op_a, "op_b": op_b}
print(table["op_b"]())
```

```text
# Output:
# 2
```

A dict lookup is explicit, type-safe, and cannot execute anything that is
not in the table. If you genuinely need to evaluate untrusted arithmetic,
use a parser (e.g. `ast` + a whitelist), never `eval`.

### 4.9 `ast` — code as data, safely

`ast.parse` reads source into a tree you can walk **without executing
it** — safe analysis (linting, counting, extracting, rewriting):

```python
import ast

def count_functions(source):
    tree = ast.parse(source)
    return sum(1 for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef))

print(count_functions("def a():\n    pass\ndef b():\n    pass\nx = 1"))
```

```text
# Output:
# 2
```

### 4.10 Monkey-patching — power and its costs

Replacing an attribute at runtime works — and is invisible. That is the
cost: the patch is not in the source, breaks silently on refactors, and
two libraries patching the same thing fight.

```python
class ModelClient:
    def predict(self, text):
        return f"real prediction for {text}"

client = ModelClient()
original = client.predict

def fake_predict(text):
    return "fake prediction"

client.predict = fake_predict      # patch
print(client.predict("x"))
client.predict = original          # restore
print(client.predict("x"))
```

```text
# Output:
# fake prediction
# real prediction for x
```

**When it is acceptable:** tests (patching network calls) — with a
restore, and prefer `unittest.mock` or dependency injection. **When it is
not:** production code patching third-party libraries — upgrade instead,
or inject the dependency explicitly.

### 4.11 When metaprogramming is the wrong answer

1. **A metaclass where `__init_subclass__` works** — metaclasses change
   class creation for every subclass and confuse `isinstance`/`type`
   checks. Reach for them last.
2. **Descriptor magic instead of `@property`** — `@property` is a
   descriptor; write plain code first, add magic only when it removes
   real duplication.
3. **`eval`/`exec` on any input you did not write** — RCE, full stop.
   Dispatch tables and `ast` cover the legitimate cases.
4. **Monkey-patching third parties in production** — invisible,
   uncomposable, breaks on upgrade. Inject instead.
5. **Reflection where a plain call works** — `getattr(obj, "method")()`
   is slower, less checkable, and less discoverable than `obj.method()`.
   Use dynamic access only when the name is genuinely data.

## 5. Common Mistakes

1. **Forgetting `from __future__ import annotations` makes annotations
   strings.** `inspect.signature` shows them as strings; always resolve
   with `get_type_hints` before mapping to JSON types.
2. **Writing a metaclass for registration.** `__init_subclass__` does it
   with a tenth of the complexity.
3. **`eval` for dispatch.** Any untrusted input = RCE. Dict dispatch is
   the safe, explicit replacement.
4. **Monkey-patching without restoring.** Tests leak patches into other
   tests; restore in `finally` or use a context manager.
5. **Descriptor without `__set_name__`.** Without it, the descriptor
   cannot know its attribute name — leading to "hard-coded attribute
   name" bugs the moment a class renames the field.
6. **Reflection where a static call works.** Dynamic access is a
   debugging nightmare; use it only when the attribute name is data.

## 6. Best Practices

- **Order of preference:** plain function → class decorator →
  `__init_subclass__` → metaclass. The simpler the mechanism, the fewer
  the surprises.
- **The signature is the contract.** For tool/plugin systems, derive
  schemas from `inspect.signature` + `get_type_hints`; never hand-write
  parallel schemas that can drift.
- **Never `eval`/`exec` untrusted strings.** Use dispatch tables; use
  `ast` when you must analyze code.
- **Keep registries class-level and documented.** `_registry` dicts are
  process-global state — make the naming convention explicit.
- **Restore monkey-patches** (or use `unittest.mock`) and prefer
  dependency injection for new code.
- **Write one test per metaprogramming trick.** Registration, schema
  shape, and descriptor behavior are the three things that break first.

## 7. Complexity and Cost

| Pattern | Time | Space | Hidden cost |
|---|---|---|---|
| `__init_subclass__` | O(1) per class | O(classes) | Registry = global state |
| `__set_name__` | O(1) | O(1) | Runs once per class build |
| Class decorator | O(class) | O(1) | Visible, contained |
| Metaclass | O(1) per class | O(1) | Affects *every* subclass |
| `type()` factory | O(namespace) | O(class) | Classes built at runtime |
| `inspect.signature` | O(1) | O(params) | Cached per call is optional |
| `get_type_hints` | O(1) | O(hints) | Must resolve names |
| `importlib.import_module` | O(1) cached | O(module) | Import side effects |
| `ast.parse` | O(source) | O(tree) | No execution — safe |
| `eval`/`exec` | O(code) | O(code) | **RCE if untrusted** |

**Scale notes:** registries scale to thousands of subclasses (dictionary
lookup); `inspect` on hot paths (every tool call) is cheap but worth
caching in the registry; `ast` is the only safe way to analyze large
codebases. The expensive mistakes are architectural, not computational.

## 8. AI Engineering Relevance

- **`@tool` decorators** (4.5) are how agent frameworks expose functions
  to LLMs: signature → JSON schema → callable table. Building one is the
  core of this topic.
- **Plugin loading** (4.6 + 4.1) is how evaluation harnesses discover
  scorers, how vector-store backends register, how agent teams add tools
  without editing the core.
- **Dispatch tables over eval** (4.8) matters because *model output is
  untrusted*: an LLM "choosing" a tool must resolve to a table lookup,
  never to evaluated code — that is the difference between a function
  call and arbitrary code execution.
- **`ast` analysis** powers linting for prompt templates and safe
  inspection of generated code (e.g. verifying a generated script only
  contains allowed nodes).
- **Monkey-patching discipline** protects the model-serving hot path:
  inject the client, don't patch it.

## 9. Practice Exercises

1. **Plugin registry:** build `RegistryBase` with `__init_subclass__`;
   define three tools in a separate module; import it dynamically with
   `importlib`; assert all three appear in the registry by name.
2. **Tool schema for a real function:** write a function with typed
   params (str, int, list[str], float default); assert `describe()`
   produces the exact JSON schema dict — including `array` for
   `list[str]` via `get_type_hints`.
3. **Dispatch vs eval:** implement `run_op(name, a, b)` over a dict of
   operators; assert it raises `KeyError` for unknown names (never
   `eval`).
4. **Descriptor with `__set_name__`:** extend `Column` with a
   `nullable` flag; assert a `None` assignment is rejected unless
   `nullable=True`, and the error message contains the descriptor's
   *own* name.
5. **Safe config path:** implement `get_path` (4.7) and assert it
   resolves `"a.b.c"` and returns the default for any missing segment.

## 10. Summary

- `__init_subclass__` auto-registers subclasses **without** a metaclass —
  the plugin pattern.
- `__set_name__` gives descriptors their attribute name.
- Class decorators > metaclasses for most jobs; `type()` for
  data-driven factories.
- `inspect.signature` + `get_type_hints` = the `@tool` schema engine.
- `importlib` loads plugins; `ast` analyzes code safely.
- **Never `eval`/`exec` untrusted input** — dispatch tables instead.
- Monkey-patch for tests only; inject in production.
- When in doubt: prefer the simplest mechanism that works.

## 11. Quick Reference

| Need | Tool |
|---|---|
| Auto-register subclasses | `__init_subclass__` in the base |
| Descriptor knows its name | `__set_name__` |
| Add behavior at class definition | Class decorator |
| Build a class from data | `type(name, bases, ns)` |
| Read a function's parameters | `inspect.signature` |
| Resolve string annotations | `typing.get_type_hints` |
| Schema from signature (LLM tools) | `describe(fn)` + `@tool` registry |
| Load a module by name | `importlib.import_module` |
| Safe attribute path lookup | `getattr` loop with `hasattr` |
| Dispatch by string name | Dict `{name: callable}` |
| Analyze code without running it | `ast.parse` + `ast.walk` |
| Patch for tests | `unittest.mock`, restore after |
| Run untrusted code | **Never** — `eval`/`exec` are RCE |

## 12. Next Steps

- **`33-security-essentials`** — why the "never eval untrusted input"
  rule is a security topic: injection classes, safe deserialization,
  and secrets handling (a `.pkl` model file is a supply-chain vector).
- **`31-concurrency-patterns`** — the `@tool` registry pairs with the
  breaker/rate-limiter stack when tools call external providers.
- **`08-mlops`** — model packaging and plugin-driven evaluation
  harnesses build on the registry patterns here.
- Practice the RAG angle: a `@tool`-exposed `search` function whose
  schema is derived (not written by hand) is the foundation of
  function-calling agents.
