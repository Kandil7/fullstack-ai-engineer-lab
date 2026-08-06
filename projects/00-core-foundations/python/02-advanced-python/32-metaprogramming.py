"""
Advanced Python — 32: Metaprogramming
======================================
Topics: __init_subclass__ (usually better than a metaclass); __set_name__;
class decorators vs metaclasses; type() dynamic creation; inspect
(signatures, source, stack); ast for code analysis; importlib dynamic
import; setattr/getattr patterns; exec/eval and why to avoid them;
monkey-patching and its costs; descriptors recap; when metaprogramming is
the wrong answer

Why this matters for AI/backend engineering:
    Agent frameworks' @tool decorators are metaprogramming: a decorator
    reads a function's signature with inspect.signature, builds a JSON
    schema from it, and registers the function so the LLM can call it.
    That is exactly what this file builds. Plugin loading, framework
    registries, and ORM model layers are the same pattern: code that
    writes code, carefully.

Run:      python 32-metaprogramming.py
Verify:   python 32-metaprogramming.py --verify
Reference: https://docs.python.org/3/reference/datamodel.html
"""

from __future__ import annotations

import ast
import importlib
import inspect
import json
import sys
import types
from typing import Callable, get_type_hints


# ============================================================
# 1. __init_subclass__ — subclass registration WITHOUT a metaclass
# ============================================================
# When a subclass is created, Python calls the parent's
# __init_subclass__ (if defined). This is the clean way to auto-register
# subclasses — no metaclass needed.

class ToolRegistry:
    """Base class: every subclass registers itself by name."""
    _registry: dict[str, type["ToolRegistry"]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Auto-register each subclass under its class name. O(1)."""
        super().__init_subclass__(**kwargs)
        ToolRegistry._registry[cls.__name__] = cls


class SearchTool(ToolRegistry):
    """Example registered tool."""

    def run(self) -> str:
        """Fake search."""
        return "search results"


class EmbedTool(ToolRegistry):
    """Example registered tool."""

    def run(self) -> str:
        """Fake embedding."""
        return "vector [0.1, 0.2]"


# Example 1: subclasses appear in the registry automatically
print(f"registry: {sorted(ToolRegistry._registry)}")
print(f"instantiate by name: {ToolRegistry._registry['EmbedTool']().run()}")

# Output:
# registry: ['EmbedTool', 'SearchTool']
# instantiate by name: vector [0.1, 0.2]


# ============================================================
# 2. __set_name__ — the descriptor hook that sees the owner class
# ============================================================
# Descriptors get __set_name__(owner, name) called when the class is
# created, so they know their attribute name without being told.

class Column:
    """A mini descriptor: validates the attribute on assignment."""

    def __init__(self, dtype: type) -> None:
        self.dtype = dtype
        self.name = "<unset>"

    def __set_name__(self, owner: type, name: str) -> None:
        """Learn the attribute name from the class definition. O(1)."""
        self.name = name

    def __get__(self, obj: object | None, objtype: type | None = None) -> object:
        """Return the stored value. O(1)."""
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj: object, value: object) -> None:
        """Validate then store. O(1)."""
        if not isinstance(value, self.dtype):
            raise TypeError(
                f"{self.name} must be {self.dtype.__name__}, got {type(value).__name__}"
            )
        obj.__dict__[self.name] = value


class Row:
    """A typed row: id must be int, name must be str."""
    id: int = Column(int)        # noqa: E701 - descriptor assignment
    name: str = Column(str)


# Example 2: descriptor knows its own attribute name
row = Row()
row.id = 7
row.name = "doc-1"
print(f"descriptor names: {Row.id.name}, {Row.name.name}")
try:
    row.id = "not-an-int"
except TypeError as exc:
    print(f"rejected: {exc}")

# Output:
# descriptor names: id, name
# rejected: id must be int, got str


# ============================================================
# 3. type() dynamic class creation vs class decorators
# ============================================================
# type(name, bases, namespace) builds a class at runtime. Usually you
# want a class decorator instead (explicit, visible at definition);
# type() is for genuinely dynamic factories.

def with_repr(cls: type) -> type:
    """Class decorator: add a default __repr__. O(1)."""
    def __repr__(self: object) -> str:
        fields = ", ".join(
            f"{k}={v!r}" for k, v in vars(self).items()
        )
        return f"{type(self).__name__}({fields})"

    cls.__repr__ = __repr__          # monkey-patch the class, in place
    return cls


@with_repr
class Chunk:
    """A RAG chunk with a decorator-supplied repr."""

    def __init__(self, text: str, score: float) -> None:
        self.text = text
        self.score = score


# type() factory for schemas at runtime (config-driven classes)
def make_point(name: str) -> type:
    """Dynamically create a 2D point class. O(1) class build."""
    return type(name, (), {"x": 0, "y": 0})


PointA = make_point("PointA")
PointB = make_point("PointB")

# Example 3: decorator-added repr and dynamic classes
print(Chunk("hello", 0.9))
print(f"PointA is PointB? {PointA is PointB}")
p = PointA()
print(f"PointA fields: {p.x}, {p.y}")

# Output:
# Chunk(text='hello', score=0.9)
# PointA is PointB? False
# PointA fields: 0, 0


# ============================================================
# 4. inspect — signatures, source, stack
# ============================================================
# inspect.signature is the backbone of @tool: you read the parameters,
# their types, and defaults, and turn them into a JSON schema.

def embed_documents(docs: list[str], model: str = "base",
                    batch_size: int = 32) -> list[list[float]]:
    """Embed a list of documents."""
    return [[0.1] * batch_size for _ in docs]


def describe(fn: Callable[..., object]) -> dict[str, object]:
    """Build a JSON-schema fragment from a function's signature. O(1).

    Uses get_type_hints to resolve string annotations (from
    __future__ import annotations makes them strings at runtime).
    """
    sig = inspect.signature(fn)
    try:
        hints = get_type_hints(fn)
    except Exception:                          # noqa: BLE001 - unresolvable
        hints = {}
    schema: dict[str, object] = {
        "name": fn.__name__,
        "description": (fn.__doc__ or "").strip().splitlines()[0]
                       if fn.__doc__ else "",
        "parameters": {"type": "object", "properties": {}},
    }
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }
    for param in sig.parameters.values():
        if param.name in ("self", "cls"):
            continue
        prop: dict[str, object] = {}
        annotation = hints.get(param.name, param.annotation)
        if annotation is not inspect.Parameter.empty:
            if annotation in type_map:
                prop["type"] = type_map[annotation]
            elif getattr(annotation, "__origin__", None) is list:
                prop["type"] = "array"
        if param.default is not inspect.Parameter.empty:
            prop["default"] = param.default
        schema["parameters"]["properties"][param.name] = prop  # type: ignore[index]
    return schema


# Example 4: signature -> JSON schema (the LLM function-calling format)
schema = describe(embed_documents)
print(json.dumps(schema, indent=2, sort_keys=True))

# Output:
# {
#   "description": "Embed a list of documents.",
#   "name": "embed_documents",
#   "parameters": {
#     "properties": {
#       "batch_size": {
#         "default": 32,
#         "type": "integer"
#       },
#       "docs": {
#         "type": "array"
#       },
#       "model": {
#         "default": "base",
#         "type": "string"
#       }
#     },
#     "type": "object"
#   }
# }


# ============================================================
# 5. The @tool pattern — auto-registration + schema from signature
# ============================================================
# This is the mechanism behind agent frameworks: register the callable,
# and derive the LLM-facing schema from the signature. No manual
# schema-writing.

TOOL_SCHEMAS: dict[str, dict[str, object]] = {}
TOOL_FUNCS: dict[str, Callable[..., object]] = {}


def tool(fn: Callable[..., object]) -> Callable[..., object]:
    """Register a function as an LLM-callable tool. O(1) registration."""
    TOOL_SCHEMAS[fn.__name__] = describe(fn)
    TOOL_FUNCS[fn.__name__] = fn
    return fn


@tool
def search(query: str, top_k: int = 5) -> list[str]:
    """Search the knowledge base."""
    return [f"result-{i}" for i in range(top_k)]


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"sunny in {city}"


# Example 5: tools auto-registered with schemas
print(f"tools: {sorted(TOOL_FUNCS)}")
print(f"search top_k default: {TOOL_SCHEMAS['search']['parameters']['properties']['top_k']}")  # noqa: E501
print(f"call by name: {TOOL_FUNCS['get_weather']('Cairo')}")

# Output:
# tools: ['get_weather', 'search']
# search top_k default: {'default': 5, 'type': 'integer'}
# call by name: sunny in Cairo


# ============================================================
# 6. importlib — dynamic import and plugin loading
# ============================================================
# importlib lets you load modules by name at runtime — the plugin
# mechanism behind drop-in tool directories.

def load_plugin(module_name: str) -> types.ModuleType:
    """Import a module by name (absolute import). O(1) per load."""
    return importlib.import_module(module_name)


# Example 6: load a stdlib module dynamically and read it
math_mod = load_plugin("math")
print(f"dynamic import: {math_mod.floor(3.7)}")
print(f"math has sin: {hasattr(math_mod, 'sin')}")

# Output:
# dynamic import: 3
# math has sin: True


# ============================================================
# 7. getattr/setattr patterns — safe dynamic access
# ============================================================

def get_path(obj: object, path: str, default: object = None) -> object:
    """Resolve 'a.b.c' attribute paths safely. O(depth)."""
    current: object = obj
    for part in path.split("."):
        if not hasattr(current, part):
            return default
        current = getattr(current, part)
    return current


class Config:
    """Nested config object for getattr probing."""

    def __init__(self) -> None:
        self.embedding = types.SimpleNamespace(model="base", dim=384)


# Example 7: safe attribute-path resolution
cfg = Config()
print(f"config path: {get_path(cfg, 'embedding.model')}")
print(f"missing path: {get_path(cfg, 'embedding.unknown_key', 'n/a')}")

# Output:
# config path: base
# missing path: n/a


# ============================================================
# 8. exec/eval — and why to avoid them
# ============================================================
# exec/eval run arbitrary strings as code. Any untrusted input reaching
# them is remote code execution. Prefer explicit dispatch tables:
# {name: callable} instead of eval(name + "()").

def dispatch_table_example() -> int:
    """Dispatch by name via a dict — the safe exec replacement. O(1)."""

    def op_a() -> int:
        return 1

    def op_b() -> int:
        return 2

    table = {"op_a": op_a, "op_b": op_b}
    return table["op_b"]()


# Example 8: dict dispatch instead of eval
print(f"dispatch: {dispatch_table_example()}")

# Output:
# dispatch: 2


# ============================================================
# 9. ast — read code as data (safe analysis, unlike exec)
# ============================================================

def count_functions(source: str) -> int:
    """Count def nodes in source without executing it. O(source size)."""
    tree = ast.parse(source)
    return sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))


# Example 9: analyze a code string safely
sample = "def a():\n    pass\ndef b():\n    pass\nx = 1"
print(f"functions found: {count_functions(sample)}")

# Output:
# functions found: 2


# ============================================================
# 10. Monkey-patching — power and its costs
# ============================================================
# Replacing an attribute at runtime is powerful (testing, plugins) but
# invisible: the patch is not in the source, breaks with refactors, and
# does not compose across libraries. Use dependency injection instead
# when you can.

class ModelClient:
    """A fake client whose method we monkey-patch for tests."""

    def predict(self, text: str) -> str:
        """Real call (simulated)."""
        return f"real prediction for {text}"


# Example 10: patch for a test, restore after
client = ModelClient()
original = client.predict

def fake_predict(text: str) -> str:
    """Test double: no network."""
    return "fake prediction"

client.predict = fake_predict                     # monkey-patch
print(client.predict("x"))
client.predict = original                         # restore
print(client.predict("x"))

# Output:
# fake prediction
# real prediction for x


# ============================================================
# 11. When metaprogramming is the wrong answer
# ============================================================
# MISTAKE: a metaclass where __init_subclass__ or a class decorator
#   would do. Metaclasses change class creation for EVERY subclass and
#   confuse type checks. Prefer, in order:
#     1. plain function / decorator
#     2. class decorator (visible at definition)
#     3. __init_subclass__ (subclass hook, no metaclass)
#     4. metaclass (last resort)
# MISTAKE: eval/exec on any input you did not write yourself — RCE.
# MISTAKE: descriptor magic instead of a plain @property.
# MISTAKE: monkey-patching a third-party lib in production code —
#   upgrade instead, or inject the dependency.


# ============================================================
# Self-Verification  (MANDATORY — every file ends with this)
# ============================================================
def _verify() -> None:
    """Assert every claim this file makes. Silent on success."""
    # --- __init_subclass__ auto-registration ---
    assert "SearchTool" in ToolRegistry._registry, \
        "__init_subclass__ must register subclasses by name"
    assert "EmbedTool" in ToolRegistry._registry, \
        "every subclass must be registered"
    assert ToolRegistry._registry["EmbedTool"]().run() == "vector [0.1, 0.2]", \
        "registered classes must be instantiable by name"

    # --- __set_name__ descriptor ---
    row = Row()
    row.id = 7
    assert Row.id.name == "id" and Row.name.name == "name", \
        "__set_name__ must learn the attribute name"
    try:
        row.id = "x"                             # type: ignore[assignment]
        raise AssertionError("type check failed to fire")
    except TypeError:
        pass
    assert row.name == "doc-1" or row.id == 7, "valid assignment still works"

    # --- class decorator + type() ---
    assert "score=0.9" in repr(Chunk("hello", 0.9)), \
        "class decorator must add a repr"
    assert PointA is not PointB, \
        "each type() call creates a distinct class"

    # --- inspect.signature matches the declared signature ---
    sig = inspect.signature(embed_documents)
    assert list(sig.parameters) == ["docs", "model", "batch_size"], \
        "inspect.signature must reflect the declared parameters"
    assert sig.parameters["model"].default == "base", \
        "defaults must be read from the signature"

    # --- schema from signature ---
    schema = describe(embed_documents)
    assert schema["name"] == "embed_documents", "schema carries the name"
    assert schema["parameters"]["properties"]["docs"]["type"] == "array", \
        "list annotations map to JSON array"
    assert schema["parameters"]["properties"]["batch_size"]["default"] == 32, \
        "defaults flow into the schema"

    # --- @tool registry ---
    assert set(TOOL_FUNCS) == {"search", "get_weather"}, \
        "@tool must auto-register every decorated function"
    assert TOOL_SCHEMAS["search"]["parameters"]["properties"]["top_k"] == \
        {"default": 5, "type": "integer"}, \
        "schemas must be derived from signatures, not hand-written"
    assert TOOL_FUNCS["get_weather"]("Cairo") == "sunny in Cairo", \
        "registered tools must be callable by name"

    # --- importlib dynamic import ---
    math_mod = load_plugin("math")
    assert math_mod.floor(3.7) == 3, \
        "dynamic import must load a module by name"
    assert hasattr(math_mod, "sin"), \
        "loaded module must expose its attributes"

    # --- getattr path resolution ---
    assert get_path(Config(), "embedding.model") == "base", \
        "nested attribute paths must resolve"
    assert get_path(Config(), "embedding.nope", "n/a") == "n/a", \
        "missing paths must return the default"

    # --- exec avoidance ---
    assert dispatch_table_example() == 2, \
        "dict dispatch replaces eval(name + '()')"

    # --- ast analysis ---
    assert count_functions("def a():\n    pass\ndef b():\n    pass") == 2, \
        "ast must count def nodes without executing source"

    # --- monkey-patch round trip ---
    client = ModelClient()
    original = client.predict
    client.predict = lambda text: "fake"         # noqa: E731
    assert client.predict("x") == "fake", "patch must take effect"
    client.predict = original
    assert client.predict("x") == "real prediction for x", \
        "restoring must bring back the original behavior"

    print("[OK] 32-metaprogramming: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. __init_subclass__ registers subclasses without a metaclass")
        print("2. inspect.signature -> JSON schema is the @tool mechanism")
        print("3. importlib loads plugins; dict dispatch beats eval")
        print("4. Monkey-patching is a test tool, not a production pattern")
        _verify()
