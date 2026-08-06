"""
Challenge 32: Metaprogramming — Solution
========================================
"""

from __future__ import annotations

import importlib
import inspect
from typing import Any, Callable, get_type_hints


# ============================================================
# Bronze: Auto-Registering Tools
# ============================================================

class Tool:
    """Base class: every subclass registers itself by class name."""

    registry: dict[str, type["Tool"]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Register the subclass in Tool.registry. O(1)."""
        super().__init_subclass__(**kwargs)
        Tool.registry[cls.__name__] = cls

    def run(self) -> str:
        """Override in subclasses."""
        raise NotImplementedError


# ============================================================
# Silver: Signature -> JSON Schema
# ============================================================

def schema_for(fn: Callable[..., object]) -> dict[str, object]:
    """Build an LLM function-calling schema from the signature."""
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


# ============================================================
# Gold: @tool Registry + Dynamic Plugin Load
# ============================================================

TOOLS: dict[str, Callable[..., object]] = {}
TOOL_SCHEMAS: dict[str, dict[str, object]] = {}


def tool(fn: Callable[..., object]) -> Callable[..., object]:
    """Register fn in TOOLS and its schema in TOOL_SCHEMAS. O(1)."""
    TOOL_SCHEMAS[fn.__name__] = schema_for(fn)
    TOOLS[fn.__name__] = fn
    return fn


def load_plugin(module_name: str) -> Any:
    """Import a module by name at runtime. O(1) per load (cached)."""
    return importlib.import_module(module_name)
