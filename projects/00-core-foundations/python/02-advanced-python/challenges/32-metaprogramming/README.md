# Challenge 32: Metaprogramming

Build a mini agent-tool framework: `__init_subclass__` registration,
signature-derived JSON schemas, and dynamic plugin loading — the exact
mechanism behind `@tool` decorators.

## 🥉 Bronze — Auto-Registering Tools (~15 min)

**Task:** Implement `Tool` with `__init_subclass__` so every subclass
registers itself in `Tool.registry` under its class name. Subclasses
provide `run(self) -> str`.

| Input | Expected |
|-------|----------|
| `class SearchTool(Tool)` | `"SearchTool" in Tool.registry` |
| `Tool.registry["SearchTool"]().run()` | whatever `run` returns |
| registry keys | exact class names, no base class |

**Constraints:** No metaclass. n ≤ 10^2 tools. Registration happens at
class-definition time.

---

## 🥈 Silver — Signature → JSON Schema (~35 min)

**Task:** Implement `schema_for(fn) -> dict` that builds an LLM
function-calling schema from `inspect.signature` + `get_type_hints`:
`name`, `description` (first docstring line), and `parameters` with
`properties` (type + default per parameter). Must handle `list[str]`
→ `"array"` and skip `self`/`cls`.

**Signature:**
```python
def schema_for(fn) -> dict: ...
```

| Input | Expected |
|-------|----------|
| `def f(docs: list[str], top_k: int = 5) -> None` | `"docs": {"type": "array"}`, `"top_k": {"type": "integer", "default": 5}` |
| untyped param | property with no `"type"` key |
| method with `self` | `self` excluded from properties |

**Constraints:** Must work when the module has `from __future__ import
annotations` (string annotations!) — resolve via `get_type_hints`.

---

## 🥇 Gold — `@tool` Registry + Dynamic Plugin Load (~75 min)

**Task:** Implement `@tool` so a decorated function is registered in
`TOOLS` (name → callable) and `TOOL_SCHEMAS` (name → schema from
Silver). Then implement `load_plugin(module_name) -> Module` that
imports a module dynamically and returns it.

**API:**
```python
TOOLS: dict[str, Callable] = {}
TOOL_SCHEMAS: dict[str, dict] = {}

def tool(fn) -> Callable: ...              # register + schema
def load_plugin(module_name: str): ...     # importlib

@tool
def search(query: str, top_k: int = 5) -> list[str]:
    """Search the knowledge base."""
    return [f"result-{i}" for i in range(top_k)]
```

| Input | Expected |
|-------|----------|
| after `@tool def search(...)` | `search` in `TOOLS` and `TOOL_SCHEMAS` |
| `TOOL_SCHEMAS["search"]["parameters"]["properties"]["top_k"]` | `{"type": "integer", "default": 5}` |
| `TOOLS["search"]("x", 2)` | `["result-0", "result-1"]` |
| `load_plugin("math").floor(3.7)` | `3` |
| schema description | first line of the docstring |

**Constraints:** `tool` must derive the schema (never hand-write it);
`load_plugin` must handle repeated calls (cached by Python). n ≤ 10^2
tools. No `eval`/`exec` anywhere.

**Follow-up:** what happens when two tools share a name, and how would
you namespace plugin-loaded tools?

---

## Running

```bash
pytest challenges/32-metaprogramming/test_challenge.py -v
```
