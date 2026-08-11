"""
Challenge 01: Introduction -- Starter Code
==========================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable


def parse_version(banner: str) -> tuple[int, int, int]:
    """Parse an interpreter banner into a (major, minor, micro) tuple.

    Accepts "Python 3.11.4", "python 3.11", " PYTHON  3.11.4 ", "3.11.4".
    A missing micro (or minor) defaults to 0. Anything else -- an empty
    string, a non-numeric component such as "3.13.0rc1", more than three
    components, a negative number -- raises ValueError.
    """
    raise NotImplementedError


def unsupported_nodes(
    nodes: list[tuple[str, str]],
    is_supported: Callable[[tuple[int, int, int]], bool],
) -> list[str]:
    """Return the ids of nodes whose runtime is not supported, in input order.

    `is_supported` is a support-matrix lookup: treat it as a remote call. It
    must be invoked at most once per *distinct* version, never once per node.
    A node whose banner does not parse counts as unsupported and must not
    reach `is_supported`.
    """
    raise NotImplementedError


def fleet_report(banners: Iterable[str]) -> dict[str, object]:
    """Summarize an interpreter inventory in a single pass.

    Returns a dict with keys:
        "total"     -- int, lines seen
        "malformed" -- int, lines that did not parse
        "counts"    -- dict[tuple[int, int, int], int], nodes per version
        "minimum"   -- the lowest parsed version, or None if there was none

    `banners` may be a one-shot iterator over hundreds of millions of lines:
    consume it exactly once and never materialize it.
    """
    raise NotImplementedError
