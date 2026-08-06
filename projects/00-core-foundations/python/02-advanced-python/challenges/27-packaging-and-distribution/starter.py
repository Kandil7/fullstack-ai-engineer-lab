"""Challenge 27: Packaging and Distribution — starter (signatures only)."""

from __future__ import annotations

BIG = 2**63


def parse_version(v: str) -> tuple[int, int, int, int]:
    """Return (major, minor, patch, rc) — zero-padded, rc or BIG."""
    raise NotImplementedError


def compare_versions(a: str, b: str) -> int:
    """Return -1 / 0 / 1 comparing two version strings."""
    raise NotImplementedError


def matches_requirement(req: str, version: str) -> bool:
    """Evaluate comma-separated simple specifiers (>=, >, <=, <, ==)."""
    raise NotImplementedError


def latest_compatible(available: list[str], spec: str) -> str | None:
    """Return the newest available version satisfying spec, or None."""
    raise NotImplementedError


def pyproject_info(toml_text: str) -> dict:
    """Parse TOML and extract name/version/requires_python/deps/extras/scripts."""
    raise NotImplementedError
