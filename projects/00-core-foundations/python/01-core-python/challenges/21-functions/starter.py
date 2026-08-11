"""
Challenge 21: Functions - Starter Code
======================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def append_message(
    role: str,
    content: str,
    history: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    """Append {"role": role, "content": content} to a conversation history.

    When `history` is None a BRAND NEW list is created for this call only.
    When a list is passed it is appended to in place and returned (same object).
    `role` must be one of "system", "user", "assistant"; otherwise ValueError.
    """
    raise NotImplementedError


def call_provider(
    client: Callable[..., str],
    prompt: str,
    defaults: dict[str, Any],
    **overrides: Any,
) -> str:
    """Call client(prompt, **merged) where merged = defaults updated by overrides.

    `defaults` is a long-lived shared config: it must never be mutated, and the
    merge must be shallow (no deepcopy of nested values).
    """
    raise NotImplementedError


class BudgetExhausted(RuntimeError):
    """Raised by generate() when the session token budget is already spent."""


def make_generate(
    client: Callable[..., dict[str, Any]],
    *,
    token_budget: int,
    defaults: dict[str, Any] | None = None,
) -> Callable[..., str]:
    """Build a per-session generate() closure over `client`.

    The returned callable must be:
        generate(prompt, *, model, max_tokens=256, **provider_options) -> str
    - every parameter after `prompt` is KEYWORD-ONLY,
    - no parameter has a mutable default,
    - raises BudgetExhausted (without calling the client) once the accumulated
      usage has reached `token_budget`,
    - exposes `generate.usage()` returning a COPY of
      {"total_tokens": int, "calls": int},
    - keeps its counters in this closure, so two sessions never share state.

    `client(prompt, *, model, max_tokens, **options)` returns
    {"text": str, "usage": {"total_tokens": int}}.
    """
    raise NotImplementedError
