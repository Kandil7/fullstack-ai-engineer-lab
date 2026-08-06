"""
Challenge 32: Metaprogramming — Hidden Tests
============================================
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


solution = _load("solution")
import pytest  # noqa: E402


# ============================================================
# Bronze: Auto-Registering Tools
# ============================================================

class SearchTool(solution.Tool):
    def run(self) -> str:
        return "search results"


class EmbedTool(solution.Tool):
    def run(self) -> str:
        return "vector [0.1, 0.2]"


def test_subclasses_auto_register():
    assert "SearchTool" in solution.Tool.registry
    assert "EmbedTool" in solution.Tool.registry


def test_registry_instantiates_by_name():
    assert solution.Tool.registry["EmbedTool"]().run() == "vector [0.1, 0.2]"
    assert solution.Tool.registry["SearchTool"]().run() == "search results"


def test_base_class_not_registered():
    assert "Tool" not in solution.Tool.registry, "base must not self-register"


def test_registry_values_are_classes():
    for name, cls in solution.Tool.registry.items():
        assert isinstance(cls, type), "registry holds classes"


# ============================================================
# Silver: Signature -> JSON Schema
# ============================================================

def _sample(docs: list[str], top_k: int = 5) -> None:
    """Sample tool with typed params."""
    return None


def test_schema_name_and_description():
    schema = solution.schema_for(_sample)
    assert schema["name"] == "_sample"
    assert schema["description"] == "Sample tool with typed params."


def test_schema_types_from_hints():
    schema = solution.schema_for(_sample)
    props = schema["parameters"]["properties"]
    assert props["docs"] == {"type": "array"}, "list[str] -> array"
    assert props["top_k"] == {"type": "integer", "default": 5}


def test_schema_untyped_param_has_no_type():
    def f(x, y: int = 1) -> None:
        """No type on x."""
        return None

    schema = solution.schema_for(f)
    props = schema["parameters"]["properties"]
    assert "type" not in props["x"], "untyped param gets no type key"
    assert props["y"] == {"type": "integer", "default": 1}


def test_schema_skips_self():
    class C:
        def method(self, value: str = "a") -> None:
            """Method doc."""
            return None

    schema = solution.schema_for(C.method)
    assert "self" not in schema["parameters"]["properties"]
    assert schema["parameters"]["properties"]["value"] == \
        {"type": "string", "default": "a"}


def test_schema_handles_string_annotations():
    # The test file itself has `from __future__ import annotations`,
    # so ALL annotations here are strings at runtime. This test would
    # fail without get_type_hints.
    schema = solution.schema_for(_sample)
    assert schema["parameters"]["properties"]["docs"] == {"type": "array"}


def test_schema_empty_docstring():
    def f(a: int) -> None:
        return None

    schema = solution.schema_for(f)
    assert schema["description"] == ""


def test_schema_multiple_types():
    def f(s: str, n: float = 0.5, b: bool = True) -> None:
        """Mixed types."""
        return None

    props = solution.schema_for(f)["parameters"]["properties"]
    assert props["s"] == {"type": "string"}
    assert props["n"] == {"type": "number", "default": 0.5}
    assert props["b"] == {"type": "boolean", "default": True}


# ============================================================
# Gold: @tool Registry + Dynamic Plugin Load
# ============================================================

@solution.tool
def search(query: str, top_k: int = 5) -> list[str]:
    """Search the knowledge base."""
    return [f"result-{i}" for i in range(top_k)]


@solution.tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"sunny in {city}"


def test_tool_registers_callable_and_schema():
    assert "search" in solution.TOOLS
    assert "search" in solution.TOOL_SCHEMAS
    assert solution.TOOLS["search"] is search, "registry holds the callable"


def test_tool_schema_is_derived_not_handwritten():
    schema = solution.TOOL_SCHEMAS["search"]
    props = schema["parameters"]["properties"]
    assert props["query"] == {"type": "string"}
    assert props["top_k"] == {"type": "integer", "default": 5}
    assert schema["description"] == "Search the knowledge base."


def test_tool_callable_by_name():
    assert solution.TOOLS["search"]("x", 2) == ["result-0", "result-1"]
    assert solution.TOOLS["get_weather"]("Cairo") == "sunny in Cairo"


def test_load_plugin_imports_by_name():
    math_mod = solution.load_plugin("math")
    assert math_mod.floor(3.7) == 3
    assert hasattr(math_mod, "sin")


def test_load_plugin_is_cached():
    math_a = solution.load_plugin("math")
    math_b = solution.load_plugin("math")
    assert math_a is math_b, "importlib caches: same module object"


def test_no_eval_or_exec_in_solution():
    source = (HERE / "solution.py").read_text(encoding="utf-8")
    for forbidden in ("eval(", "exec("):
        assert forbidden not in source, f"solution must not use {forbidden!r}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
