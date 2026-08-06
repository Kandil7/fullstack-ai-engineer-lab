"""
Challenge 32: Metaprogramming — Starter
=======================================
Implement all three tiers. Replace every NotImplementedError.
"""

from __future__ import annotations

from typing import Any, Callable


# ============================================================
# Bronze: Auto-Registering Tools
# ============================================================

class Tool:
    """Base class: every subclass registers itself by class name."""

    registry: dict[str, type["Tool"]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Register the subclass in Tool.registry. O(1)."""
        raise NotImplementedError

    def run(self) -> str:
        """Override in subclasses."""
        raise NotImplementedError


# ============================================================
# Silver: Signature -> JSON Schema
# ============================================================

def schema_for(fn: Callable[..., object]) -> dict[str, object]:
    """Build an LLM function-calling schema from the signature.

    Returns:
        {
          "name": str,
          "description": str (first docstring line, "" if none),
          "parameters": {
            "type": "object",
            "properties": {param: {"type": ..., "default": ...}},
          },
        }

    - list[str] annotations map to "array" (via get_type_hints).
    - self/cls parameters are skipped.
    - Unannotated params get no "type" key.
    """
    raise NotImplementedError


# ============================================================
# Gold: @tool Registry + Dynamic Plugin Load
# ============================================================

TOOLS: dict[str, Callable[..., object]] = {}
TOOL_SCHEMAS: dict[str, dict[str, object]] = {}


def tool(fn: Callable[..., object]) -> Callable[..., object]:
    """Register fn in TOOLS and its schema in TOOL_SCHEMAS. O(1)."""
    raise NotImplementedError


def load_plugin(module_name: str) -> Any:
    """Import a module by name at runtime. O(1) per load (cached)."""
    raise NotImplementedError
