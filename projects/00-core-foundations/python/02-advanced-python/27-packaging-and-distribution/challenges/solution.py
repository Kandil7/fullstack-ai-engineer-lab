"""Challenge 27: Packaging and Distribution — reference solution.

Why these approaches:
- Bronze: the rc suffix must be partitioned BEFORE splitting the core —
  int("0rc1") raises ValueError.
- Silver: versions compare as int tuples, never as strings — the
  lexicographic trap ("1.10.0" < "1.9.9") is the whole point.
- Gold: the resolver is a max over parsed, spec-checked versions; the
  manifest reader uses tomllib with zero dependencies.
"""

from __future__ import annotations

import tomllib

BIG = 2**63


def parse_version(v: str) -> tuple[int, int, int, int]:
    """Partition the rc suffix first, then zero-pad the dotted core."""
    core, _, rc = v.partition("rc")
    parts = [int(p) for p in core.split(".")]
    while len(parts) < 3:
        parts.append(0)
    return (parts[0], parts[1], parts[2], int(rc) if rc else BIG)


def compare_versions(a: str, b: str) -> int:
    pa, pb = parse_version(a), parse_version(b)
    return -1 if pa < pb else (1 if pa > pb else 0)


def _check_one(op: str, ver: str, parsed: tuple) -> bool:
    target = parse_version(ver)
    if op == ">=":
        return parsed >= target
    if op == "<=":
        return parsed <= target
    if op == ">":
        return parsed > target
    if op == "<":
        return parsed < target
    if op == "==":
        return parsed == target
    raise ValueError(f"unsupported operator: {op}")


def matches_requirement(req: str, version: str) -> bool:
    parsed = parse_version(version)
    # pip-style default: pre-releases are excluded unless the spec
    # itself mentions a pre-release token (rc/a/b/dev/post).
    tokens = [t for t in req.replace(",", " ").split()]
    mentions_prerelease = any(
        "rc" in t or "dev" in t or "post" in t or t[-1] in "ab" for t in tokens
    )
    if parsed[3] != BIG and not mentions_prerelease:
        return False
    for clause in req.split(","):
        clause = clause.strip()
        for op in (">=", "<=", "==", ">", "<"):
            if clause.startswith(op):
                if not _check_one(op, clause[len(op):].strip(), parsed):
                    return False
                break
        else:
            raise ValueError(f"malformed clause: {clause}")
    return True


def latest_compatible(available: list[str], spec: str) -> str | None:
    """Newest version satisfying spec — a parsed max, never max(str)."""
    best: str | None = None
    for version in available:
        if matches_requirement(spec, version):
            if best is None or compare_versions(version, best) > 0:
                best = version
    return best


def pyproject_info(toml_text: str) -> dict:
    data = tomllib.loads(toml_text)
    project = data["project"]
    return {
        "name": project["name"],
        "version": project["version"],
        "requires_python": project.get("requires-python"),
        "dependencies": project.get("dependencies", []),
        "extras": project.get("optional-dependencies", {}),
        "scripts": project.get("scripts", {}),
    }
