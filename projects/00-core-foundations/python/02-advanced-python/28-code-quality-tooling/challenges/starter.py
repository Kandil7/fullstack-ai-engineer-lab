"""Challenge 28 starter — fill in the bodies (never return working code)."""
from __future__ import annotations


def find_mutable_defaults(source: str) -> list[tuple[int, str]]:
    """Return [(line, function_name)] for mutable default arguments."""
    raise NotImplementedError


def analyze(source: str, max_complexity: int = 10
            ) -> dict[str, list[tuple[int, str]]]:
    """Return {"B006": ..., "E722": ..., "C901": ...} with ONE ast.parse."""
    raise NotImplementedError


def lint_source(source: str,
                config: dict[str, list[str]] | None = None
                ) -> dict[str, list[tuple[int, str]]]:
    """Full linter: select/ignore config, noqa suppression, E999 safety."""
    raise NotImplementedError
