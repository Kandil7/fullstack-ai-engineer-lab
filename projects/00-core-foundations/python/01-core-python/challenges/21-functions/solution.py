"""
Challenge 21: Functions - Reference Solution
============================================
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

_VALID_ROLES = frozenset({"system", "user", "assistant"})


def append_message(
    role: str,
    content: str,
    history: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    """Append a message to a conversation history and return that history.

    Why this approach: the default is None and the list is created inside the
    body, so every defaulted call gets a fresh list. The natural-looking
    `history=[]` binds ONE list at function-definition time and shares it across
    every call for the life of the process -- turn 1 of session B then sees
    session A's messages, which in a served agent means cross-tenant prompt
    leakage plus a context window that grows without bound (O(total requests)
    memory instead of O(1)). None-default costs one extra branch; the mutable
    default costs a data-leak incident.
    """
    if role not in _VALID_ROLES:
        raise ValueError(f"invalid role {role!r}; expected one of {sorted(_VALID_ROLES)}")
    if history is None:
        history = []
    history.append({"role": role, "content": content})
    return history


def call_provider(
    client: Callable[..., str],
    prompt: str,
    defaults: dict[str, Any],
    **overrides: Any,
) -> str:
    """Forward prompt plus (defaults <- overrides) to a provider client.

    Why this approach: `{**defaults, **overrides}` builds one new dict of k
    entries -- O(k) time, O(k) space -- and the *values* are shared by
    reference, so a 300k-element tool schema in `defaults` is passed through as
    the same object. The two tempting alternatives both lose:
    `defaults.update(overrides)` is O(k) but mutates a shared module-level
    config, so one request's temperature silently becomes every later request's
    temperature; `copy.deepcopy(defaults)` is safe but O(size of the whole
    nested payload), turning a constant-cost merge into megabytes of copying on
    every single call.
    """
    merged: dict[str, Any] = {**defaults, **overrides}
    return client(prompt, **merged)


class BudgetExhausted(RuntimeError):
    """Raised by generate() when the session token budget is already spent."""


def make_generate(
    client: Callable[..., dict[str, Any]],
    *,
    token_budget: int,
    defaults: dict[str, Any] | None = None,
) -> Callable[..., str]:
    """Build a per-session generate() closure with a hard token budget.

    Why this approach: the counters live in the closure cell of this factory, so
    each session owns O(1) private state and two sessions can never contaminate
    each other's budget -- the module-level-counter alternative is O(1) too but
    is a single shared mutable, which under any concurrency reports one
    session's spend against another's cap. Everything after `prompt` is
    keyword-only (`*` in the signature), which converts the classic
    `generate(prompt, 256, "gpt-4o")` argument-order mistake from a silently
    wrong request into an immediate TypeError. The budget is checked BEFORE the
    call, so an exhausted session costs zero dollars instead of one more
    billable request per attempt.
    """
    base: dict[str, Any] = dict(defaults) if defaults else {}
    state = {"total_tokens": 0, "calls": 0}

    def generate(
        prompt: str,
        *,
        model: str,
        max_tokens: int = 256,
        **provider_options: Any,
    ) -> str:
        if state["total_tokens"] >= token_budget:
            raise BudgetExhausted(
                f"session used {state['total_tokens']} of {token_budget} tokens"
            )
        options: dict[str, Any] = {**base, **provider_options}
        response = client(prompt, model=model, max_tokens=max_tokens, **options)
        state["total_tokens"] += int(response["usage"]["total_tokens"])
        state["calls"] += 1
        return str(response["text"])

    def usage() -> dict[str, int]:
        return dict(state)

    generate.usage = usage  # type: ignore[attr-defined]
    return generate
