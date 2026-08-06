# 32 — Metaprogramming Glossary

## Quick Reference

| Term | Definition | Complexity |
|---|---|---|
| Metaprogramming | Code that writes or modifies code at runtime | — |
| `__init_subclass__` | Hook called when a subclass is created; auto-registration without a metaclass | O(1) per class |
| `__set_name__` | Descriptor hook that learns the attribute name during class creation | O(1) |
| Class decorator | Function receiving a class, modifying it, returning it (`@with_repr`) | O(class) |
| Metaclass | Class of a class; controls class creation for all subclasses | O(1) per class |
| `type()` factory | `type(name, bases, namespace)` builds a class at runtime | O(namespace) |
| `inspect.signature` | Reads a function's parameters, annotations, and defaults | O(1) |
| `get_type_hints` | Resolves string annotations to real types | O(1) |
| JSON schema | Contract describing a function's parameters (LLM tool calling) | O(params) |
| `@tool` pattern | Decorator that registers a callable and derives its schema | O(1) registration |
| `importlib` | Dynamic module import and plugin loading | O(1) cached |
| `getattr`/`setattr` | Dynamic attribute access by name | O(1) |
| `eval` | Executes an expression string — dangerous with untrusted input | O(code) |
| `exec` | Executes a statement string — dangerous with untrusted input | O(code) |
| Dispatch table | `{name: callable}` dict replacing `eval(name + "()")` | O(1) |
| `ast` | Parses source into a tree; analysis without execution | O(source) |
| Monkey-patching | Replacing an attribute at runtime | O(1) |
| Descriptor | Object with `__get__`/`__set__`/`__delete__`; powers `@property` | O(1) per access |
| RCE | Remote code execution — what `eval`/`exec` on untrusted input is | — |
| Reflection | Inspecting/modifying program structure at runtime | O(1) |

## Detailed Definitions

### Metaprogramming
**Definition:** Writing code that writes, inspects, or modifies code —
decorators, registries, schema-from-signature, dynamic imports. The
`@tool` decorator is metaprogramming: it reads the function's signature
and registers it for LLM calling.

```python
@tool
def search(query: str, top_k: int = 5) -> list[str]:
    """Search the knowledge base."""
    return []
# decorator runs AT DEFINITION TIME: registers schema + callable
```

**Related Terms:** Class decorator, `@tool` pattern, Reflection

### `__init_subclass__`
**Definition:** A method on a base class called automatically whenever a
subclass is created. The clean way to auto-register subclasses — no
metaclass needed.

```python
class Registry:
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Registry._registry[cls.__name__] = cls

class ToolA(Registry):
    pass

print(sorted(Registry._registry))
```

```text
# Output:
# ['ToolA']
```

**Related Terms:** Metaclass, Class decorator

### `__set_name__`
**Definition:** A descriptor hook invoked during class creation with
`(owner, name)`, so the descriptor knows its attribute name. Without it,
a descriptor cannot know which attribute it is bound to.

```python
class Column:
    def __set_name__(self, owner, name):
        self.name = name          # learned automatically

class Row:
    id = Column(int)

print(Row.id.name)
```

```text
# Output:
# id
```

**Related Terms:** Descriptor, Column pattern

### Class decorator
**Definition:** A function that receives a class, modifies it, and returns
it; applied with `@name` above the class. Visible, contained, and usually
enough — prefer it over a metaclass.

```python
def with_repr(cls):
    cls.__repr__ = lambda self: f"{type(self).__name__}(...)"
    return cls

@with_repr
class Chunk:
    pass
```

**Related Terms:** `__init_subclass__`, Metaclass

### Metaclass
**Definition:** The class of a class (`type` by default). A metaclass
controls how classes are created — the most powerful and most invasive
hook: it affects *every* subclass, so reach for it last.

```python
class Meta(type):
    def __new__(mcls, name, bases, ns):
        return super().__new__(mcls, name, bases, ns)
```

**Related Terms:** `__init_subclass__`, `type()` factory

### `type()` factory
**Definition:** Calling `type(name, bases, namespace)` builds a class at
runtime — for genuinely data-driven factories (classes from config), not
for static definitions.

```python
def make_point(name):
    return type(name, (), {"x": 0, "y": 0})

PointA = make_point("PointA")
PointB = make_point("PointB")
print(PointA is PointB)      # distinct classes
```

```text
# Output:
# False
```

**Related Terms:** Metaclass, Reflection

### `inspect.signature`
**Definition:** Returns the `Signature` of a callable: parameter names,
annotations, defaults, kinds. The raw material of schema generation.

```python
import inspect

def f(x: int, y: str = "a") -> bool:
    pass

sig = inspect.signature(f)
print(list(sig.parameters), sig.parameters["y"].default)
```

```text
# Output:
# ['x', 'y'] a
```

**Related Terms:** `get_type_hints`, JSON schema, `@tool` pattern

### `get_type_hints`
**Definition:** `typing.get_type_hints(fn)` resolves annotations to real
types, handling `from __future__ import annotations` (which stores them
as strings). Required before mapping to JSON types.

```python
from typing import get_type_hints

def f(docs: list[str]) -> None:
    pass

print(get_type_hints(f)["docs"])
```

```text
# Output:
# list[str]
```

**Related Terms:** `inspect.signature`, JSON schema

### JSON schema
**Definition:** A machine-readable contract describing a function's
parameters — the exact format LLM function-calling APIs consume. Built
from signatures so code and contract never drift.

```json
{"type": "object", "properties": {"top_k": {"type": "integer", "default": 5}}}
```

**Related Terms:** `@tool` pattern, `inspect.signature`

### `@tool` pattern
**Definition:** A decorator that (1) derives a JSON schema from the
function's signature and (2) registers the callable in a table. The
mechanism behind agent frameworks' tool calling.

```python
TOOL_SCHEMAS = {}
TOOL_FUNCS = {}

def tool(fn):
    TOOL_SCHEMAS[fn.__name__] = describe(fn)
    TOOL_FUNCS[fn.__name__] = fn
    return fn
```

**Related Terms:** JSON schema, Dispatch table, Agent tools

### `importlib`
**Definition:** The standard library for dynamic imports:
`importlib.import_module(name)` loads a module at runtime — the plugin
mechanism. Combined with `__init_subclass__`, a plugin directory registers
itself.

```python
import importlib

math_mod = importlib.import_module("math")
print(math_mod.floor(3.7))
```

```text
# Output:
# 3
```

**Related Terms:** `__init_subclass__`, Plugin loading

### `getattr` / `setattr`
**Definition:** Dynamic attribute access by string name. Safe when the
name is data (config paths, serialization); a debugging nightmare when a
static call would do.

```python
class C:
    pass

c = C()
setattr(c, "model", "base")
print(getattr(c, "model"))
```

```text
# Output:
# base
```

**Related Terms:** Reflection

### `eval`
**Definition:** Evaluates an expression string as code. With any
untrusted input it is **remote code execution** — the string *is* the
program. Replaced by dispatch tables.

```python
# NEVER: eval(user_input)
# ALWAYS: table[name]()
```

**Related Terms:** `exec`, RCE, Dispatch table

### `exec`
**Definition:** Executes a statement string as code. Same RCE hazard as
`eval`, for statements. Avoid on anything you did not write yourself.

**Related Terms:** `eval`, RCE

### Dispatch table
**Definition:** A `{name: callable}` dictionary used instead of
`eval(name + "()")`. Explicit, type-safe, cannot execute anything not in
the table.

```python
def op_a():
    return 1

table = {"op_a": op_a}
print(table["op_a"]())
```

```text
# Output:
# 1
```

**Related Terms:** `eval`, `exec`, Agent tools

### `ast`
**Definition:** Parses source into an abstract syntax tree that can be
walked **without executing** — safe analysis (linting, counting,
inspection).

```python
import ast

tree = ast.parse("def a():\n    pass")
print(sum(1 for n in ast.walk(tree)
          if isinstance(n, ast.FunctionDef)))
```

```text
# Output:
# 1
```

**Related Terms:** `eval` (its safe alternative)

### Monkey-patching
**Definition:** Replacing an attribute at runtime. Powerful for tests
(patch the network), dangerous in production (invisible, uncomposable,
breaks on upgrade). Restore after use, or prefer dependency injection.

```python
client.predict = fake_predict    # patch
...
client.predict = original        # restore
```

**Related Terms:** Dependency injection, `unittest.mock`

### Descriptor
**Definition:** An object implementing `__get__`/`__set__`/`__delete__`
that controls attribute access. `@property`, classmethods, and ORM columns
are descriptors. Combined with `__set_name__`, they know their own name.

**Related Terms:** `__set_name__`, `@property`

### RCE
**Definition:** Remote code execution — the attacker's input runs as your
program. `eval`/`exec` on untrusted input is RCE; model output counts as
untrusted, so tool selection must be a dispatch table, never evaluation.

**Related Terms:** `eval`, `exec`, Prompt injection

### Reflection
**Definition:** Inspecting and modifying a program's structure at runtime
(`inspect`, `getattr`, `type()`, `__dict__`). Powerful but slower and
less discoverable than static code; use when the name is data.

**Related Terms:** `inspect.signature`, `getattr`, Metaprogramming

## Key Concepts Summary

1. **`__init_subclass__` beats metaclasses for registration.** One hook
   on the base class does what a metaclass does with a fraction of the
   magic — prefer it (and class decorators) first.
2. **The signature is the contract.** For LLM tool calling, derive JSON
   schemas from `inspect.signature` + `get_type_hints`; hand-written
   parallel schemas drift from the code.
3. **Never execute untrusted strings.** `eval`/`exec` on user or model
   input is RCE; dispatch tables and `ast` cover the legitimate cases.
4. **Metaprogramming is for framework boundaries.** Registries, plugin
   loading, and schema generation earn their complexity; a clever
   metaclass in application code is usually a bug.
5. **Monkey-patch for tests, inject in production.** Invisible changes
   to third-party behavior are the least debuggable kind of bug.

## Practice Terms

1. **Why is `__init_subclass__` better than a metaclass for registration?**
   *Answer:* It is a single hook on the base class — no `type.__new__`
   subclass, no hidden effect on every class, easier to reason about and
   to test. Metaclasses remain for framework-level hooks that must run
   for every subclass.
2. **What happens to annotations with `from __future__ import annotations`?**
   *Answer:* They become strings at runtime, so `inspect.signature`
   reports strings; `get_type_hints(fn)` resolves them to real types.
   Forgetting this produces schemas with no `"type"` keys.
3. **What is the RCE path in an agent system?**
   *Answer:* If the model's tool-choice text is passed to `eval`/`exec`
   (or `subprocess(shell=True)`), the model output becomes code.
   Resolving tool names through a dispatch table makes the surface
   exactly the registered functions.
4. **When is `type()` the right tool?**
   *Answer:* When classes are genuinely data-driven — built from config,
   schemas, or registry entries — and a static class definition would
   duplicate logic. For one-off additions, a class decorator is simpler.
5. **What are monkey-patching's three costs?**
   *Answer:* Invisibility (not in the source), breakage on refactor, and
   non-composition (two patches conflict). Tests can pay these costs;
   production code should inject dependencies instead.
