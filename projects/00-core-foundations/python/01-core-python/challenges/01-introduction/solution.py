"""
Challenge 01: Introduction -- Reference Solution
================================================
"""

from __future__ import annotations

from collections.abc import Callable, Iterable


def parse_version(banner: str) -> tuple[int, int, int]:
    """Parse an interpreter banner into a (major, minor, micro) tuple.

    Why this approach: strip the optional "Python" prefix, then validate every
    component with str.isdigit() before int(). int() alone would happily accept
    "\\u0663" (Arabic-Indic three) and unicode digits, and "+3"; isdigit plus a
    length check rejects them, so a malformed banner can never be silently
    coerced into a version that passes a support check. O(len(banner)) with no
    regex compilation -- at 10^8 fleet lines the regex engine's per-call
    overhead is the difference between a 2-minute and a 20-minute audit.
    """
    text = banner.strip()
    if not text:
        raise ValueError("empty version banner")
    lowered = text.lower()
    if lowered.startswith("python"):
        text = text[len("python") :].strip()
    if not text:
        raise ValueError(f"no version in banner: {banner!r}")
    parts = text.split(".")
    if len(parts) > 3:
        raise ValueError(f"too many version components: {banner!r}")
    numbers: list[int] = []
    for part in parts:
        if not part.isdigit() or not part.isascii():
            raise ValueError(f"non-numeric version component {part!r} in {banner!r}")
        numbers.append(int(part))
    while len(numbers) < 3:
        numbers.append(0)
    return (numbers[0], numbers[1], numbers[2])


def unsupported_nodes(
    nodes: list[tuple[str, str]],
    is_supported: Callable[[tuple[int, int, int]], bool],
) -> list[str]:
    """Return the ids of nodes whose runtime is not supported, in input order.

    Why this approach: memoize `is_supported` on the parsed version, so the
    remote support-matrix is hit once per *distinct* version -- O(d) calls for
    d distinct versions instead of O(n) calls for n nodes. A fleet of 20k nodes
    running 12 interpreter builds costs 12 lookups, not 20000; at 40 ms per
    lookup that is 0.5 s instead of 13 minutes. Parsing is done before the
    lookup so a malformed banner short-circuits without spending a call.
    """
    cache: dict[tuple[int, int, int], bool] = {}
    bad: list[str] = []
    for node_id, banner in nodes:
        try:
            version = parse_version(banner)
        except ValueError:
            bad.append(node_id)
            continue
        ok = cache.get(version)
        if ok is None:
            ok = bool(is_supported(version))
            cache[version] = ok
        if not ok:
            bad.append(node_id)
    return bad


def fleet_report(banners: Iterable[str]) -> dict[str, object]:
    """Summarize an interpreter inventory in a single pass.

    Why this approach: one for-loop over the iterable accumulates every field
    at once, so memory is O(distinct versions) -- a few hundred bytes -- not
    O(lines). The readable-looking alternative, `lines = list(banners)` then
    three comprehensions over it, is both three passes (impossible on a
    one-shot iterator: passes 2 and 3 see nothing) and O(n) memory: 400k
    banners cost ~25 MB. min() is tracked incrementally rather than by
    collecting all versions first, for the same reason.
    """
    total = 0
    malformed = 0
    counts: dict[tuple[int, int, int], int] = {}
    minimum: tuple[int, int, int] | None = None
    for banner in banners:
        total += 1
        try:
            version = parse_version(banner)
        except ValueError:
            malformed += 1
            continue
        counts[version] = counts.get(version, 0) + 1
        if minimum is None or version < minimum:
            minimum = version
    return {"total": total, "malformed": malformed, "counts": counts, "minimum": minimum}
