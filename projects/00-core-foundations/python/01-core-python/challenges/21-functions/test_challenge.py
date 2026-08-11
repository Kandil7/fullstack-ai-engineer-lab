"""
Challenge 21: Functions - Tests
===============================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    CHALLENGE_USE_SOLUTION=1 python -m pytest 01-core-python/challenges/21-functions -q

Guards use object identity, tracemalloc peak, and spy call counts -- never
wall-clock time.
"""

from __future__ import annotations

import importlib.util
import inspect
import os
import tracemalloc
from pathlib import Path
from typing import Any

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


class SpyClient:
    """Records every call made to a fake provider client."""

    def __init__(self, text: str = "ok", tokens: int = 60) -> None:
        self.text = text
        self.tokens = tokens
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def __call__(self, prompt: str, **kwargs: Any) -> str:
        self.calls.append((prompt, kwargs))
        return self.text

    def as_dict_client(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        """Client flavour used by make_generate: returns text plus usage."""
        self.calls.append((prompt, kwargs))
        return {"text": self.text, "usage": {"total_tokens": self.tokens}}


def _big_tool_schema(n: int = 20_000) -> list[dict[str, Any]]:
    """A deterministic, deep-ish provider payload that is expensive to deepcopy."""
    return [{"name": f"tool_{i}", "params": {"idx": i, "label": f"p{i}"}} for i in range(n)]


class TestAppendMessage:
    """Bronze: the mutable default argument bug."""

    def test_creates_message(self) -> None:
        assert mod.append_message("user", "hi") == [{"role": "user", "content": "hi"}]

    def test_defaulted_calls_do_not_share_state(self) -> None:
        """The whole point: `history=[]` in the signature would make the second
        call return TWO messages because the default list is bound once, at
        definition time, and shared by every defaulted call forever."""
        first = mod.append_message("user", "turn-1")
        second = mod.append_message("user", "turn-2")
        assert first == [{"role": "user", "content": "turn-1"}]
        assert second == [{"role": "user", "content": "turn-2"}]
        assert first is not second

    def test_many_defaulted_calls_stay_length_one(self) -> None:
        for i in range(50):
            assert len(mod.append_message("user", f"m{i}")) == 1

    def test_appends_to_supplied_history_in_place(self) -> None:
        history: list[dict[str, str]] = [{"role": "system", "content": "be brief"}]
        returned = mod.append_message("user", "hello", history)
        assert returned is history, "a supplied history must be appended to, not copied"
        assert history == [
            {"role": "system", "content": "be brief"},
            {"role": "user", "content": "hello"},
        ]

    def test_multi_turn_accumulation(self) -> None:
        history = mod.append_message("system", "s")
        mod.append_message("user", "u", history)
        mod.append_message("assistant", "a", history)
        assert [m["role"] for m in history] == ["system", "user", "assistant"]

    def test_empty_content_allowed(self) -> None:
        assert mod.append_message("assistant", "") == [{"role": "assistant", "content": ""}]

    def test_rejects_unknown_role(self) -> None:
        with pytest.raises(ValueError):
            mod.append_message("tool", "oops")

    def test_explicit_empty_list_is_used(self) -> None:
        history: list[dict[str, str]] = []
        returned = mod.append_message("user", "x", history)
        assert returned is history and len(history) == 1


class TestCallProvider:
    """Silver: **kwargs passthrough without mutating or deep-copying config."""

    def test_forwards_prompt_and_defaults(self) -> None:
        spy = SpyClient()
        assert mod.call_provider(spy, "summarize", {"model": "m1", "temperature": 0.0}) == "ok"
        prompt, kwargs = spy.calls[0]
        assert prompt == "summarize"
        assert kwargs == {"model": "m1", "temperature": 0.0}

    def test_overrides_win(self) -> None:
        spy = SpyClient()
        mod.call_provider(spy, "p", {"model": "m1", "temperature": 0.0}, temperature=0.7)
        assert spy.calls[0][1] == {"model": "m1", "temperature": 0.7}

    def test_overrides_can_add_new_options(self) -> None:
        spy = SpyClient()
        mod.call_provider(spy, "p", {"model": "m1"}, top_p=0.9, seed=42)
        assert spy.calls[0][1] == {"model": "m1", "top_p": 0.9, "seed": 42}

    def test_empty_defaults(self) -> None:
        spy = SpyClient()
        mod.call_provider(spy, "p", {}, model="m2")
        assert spy.calls[0][1] == {"model": "m2"}

    def test_no_overrides_and_no_defaults(self) -> None:
        spy = SpyClient()
        mod.call_provider(spy, "p", {})
        assert spy.calls[0][1] == {}

    def test_calls_client_exactly_once(self) -> None:
        spy = SpyClient()
        mod.call_provider(spy, "p", {"model": "m"})
        assert len(spy.calls) == 1

    def test_does_not_mutate_shared_defaults(self) -> None:
        """`defaults.update(overrides)` is the naive-but-correct version: the
        returned text is right, yet one request's temperature leaks into every
        later request that reuses the same config object."""
        defaults = {"model": "m1", "temperature": 0.0}
        snapshot = dict(defaults)
        spy = SpyClient()
        mod.call_provider(spy, "p", defaults, temperature=0.9)
        assert defaults == snapshot, "the shared defaults dict must never be mutated"

    def test_repeated_calls_are_independent(self) -> None:
        defaults = {"model": "m1", "temperature": 0.0}
        spy = SpyClient()
        mod.call_provider(spy, "a", defaults, temperature=0.9)
        mod.call_provider(spy, "b", defaults)
        assert spy.calls[1][1] == {"model": "m1", "temperature": 0.0}

    def test_merge_is_shallow_values_passed_by_reference(self) -> None:
        """Nested values must arrive as the SAME objects. A deepcopy-based merge
        is safe but ships a duplicate of the whole tool schema on every call."""
        tools = _big_tool_schema(50)
        spy = SpyClient()
        mod.call_provider(spy, "p", {"tools": tools, "model": "m"}, temperature=0.2)
        assert spy.calls[0][1]["tools"] is tools, "merge must be shallow, not a deepcopy"

    def test_memory_guard_no_deepcopy(self) -> None:
        """tracemalloc guard: a 20k-entry tool schema lives in `defaults`.
        A shallow merge allocates one small dict (< 1 MB peak); copy.deepcopy
        reallocates the whole nested payload (~10 MB) on every call."""
        tools = _big_tool_schema(20_000)
        defaults = {"tools": tools, "model": "m1", "temperature": 0.0}
        spy = SpyClient()

        tracemalloc.start()
        try:
            mod.call_provider(spy, "p", defaults, temperature=0.3)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()

        assert spy.calls[0][1]["temperature"] == 0.3
        assert peak < 1 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 1 MB ceiling; merge the option "
            "dicts shallowly ({**defaults, **overrides}) instead of deep-copying"
        )


class TestMakeGenerate:
    """Gold: keyword-only signature, closure state, pre-flight budget check."""

    def _build(self, spy: SpyClient, budget: int = 100, defaults: dict[str, Any] | None = None):
        return mod.make_generate(spy.as_dict_client, token_budget=budget, defaults=defaults)

    def test_basic_call(self) -> None:
        spy = SpyClient(text="hello")
        gen = self._build(spy)
        assert gen("p", model="m1") == "hello"
        assert spy.calls[0][1]["model"] == "m1"

    def test_max_tokens_default_forwarded(self) -> None:
        spy = SpyClient()
        gen = self._build(spy)
        gen("p", model="m1")
        assert spy.calls[0][1]["max_tokens"] == 256

    def test_provider_options_passthrough(self) -> None:
        spy = SpyClient()
        gen = self._build(spy, defaults={"temperature": 0.0})
        gen("p", model="m1", max_tokens=8, top_p=0.5)
        _, kwargs = spy.calls[0]
        assert kwargs["max_tokens"] == 8
        assert kwargs["top_p"] == 0.5
        assert kwargs["temperature"] == 0.0

    def test_call_option_overrides_session_default(self) -> None:
        spy = SpyClient()
        defaults = {"temperature": 0.0}
        gen = self._build(spy, defaults=defaults)
        gen("p", model="m1", temperature=0.9)
        assert spy.calls[0][1]["temperature"] == 0.9
        assert defaults == {"temperature": 0.0}, "session defaults must not be mutated"

    def test_all_params_after_prompt_are_keyword_only(self) -> None:
        """Positional args are how `generate(prompt, 256, "gpt-4o")` silently
        sends max_tokens as the model name. `*` in the signature makes it a
        TypeError at the call site instead."""
        spy = SpyClient()
        gen = self._build(spy)
        params = list(inspect.signature(gen).parameters.values())
        assert params[0].kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        for p in params[1:]:
            assert p.kind in (
                inspect.Parameter.KEYWORD_ONLY,
                inspect.Parameter.VAR_KEYWORD,
            ), f"parameter {p.name!r} must be keyword-only"

    def test_positional_extra_arg_raises_type_error(self) -> None:
        spy = SpyClient()
        gen = self._build(spy)
        with pytest.raises(TypeError):
            gen("p", "gpt-4o")
        assert spy.calls == [], "a mis-ordered call must not reach the provider"

    def test_no_mutable_defaults_in_signature(self) -> None:
        spy = SpyClient()
        gen = self._build(spy)
        for p in inspect.signature(gen).parameters.values():
            if p.default is not inspect.Parameter.empty:
                assert not isinstance(p.default, (list, dict, set)), (
                    f"parameter {p.name!r} has a mutable default {p.default!r}"
                )

    def test_model_is_required(self) -> None:
        spy = SpyClient()
        gen = self._build(spy)
        with pytest.raises(TypeError):
            gen("p")

    def test_usage_accumulates(self) -> None:
        spy = SpyClient(tokens=30)
        gen = self._build(spy, budget=1000)
        gen("a", model="m")
        gen("b", model="m")
        assert gen.usage() == {"total_tokens": 60, "calls": 2}

    def test_usage_returns_a_copy(self) -> None:
        spy = SpyClient(tokens=30)
        gen = self._build(spy, budget=1000)
        gen("a", model="m")
        snapshot = gen.usage()
        snapshot["total_tokens"] = 10**9
        assert gen.usage()["total_tokens"] == 30, "usage() must hand out a copy"

    def test_budget_blocks_before_calling_provider(self) -> None:
        """Budget is checked pre-flight: an exhausted session costs $0, not one
        more billable request per retry."""
        spy = SpyClient(tokens=60)
        gen = self._build(spy, budget=100)
        gen("a", model="m")
        gen("b", model="m")  # total 120 >= 100, so the NEXT call must be refused
        assert len(spy.calls) == 2
        with pytest.raises(mod.BudgetExhausted):
            gen("c", model="m")
        assert len(spy.calls) == 2, "no provider call may happen once the budget is spent"

    def test_budget_refusals_are_repeatable_and_free(self) -> None:
        spy = SpyClient(tokens=200)
        gen = self._build(spy, budget=100)
        gen("a", model="m")
        for _ in range(5):
            with pytest.raises(mod.BudgetExhausted):
                gen("b", model="m")
        assert len(spy.calls) == 1
        assert gen.usage()["calls"] == 1

    def test_zero_budget_refuses_immediately(self) -> None:
        spy = SpyClient()
        gen = self._build(spy, budget=0)
        with pytest.raises(mod.BudgetExhausted):
            gen("a", model="m")
        assert spy.calls == []

    def test_sessions_do_not_share_counters(self) -> None:
        """Module-level counters would report session A's spend against B's cap."""
        spy_a, spy_b = SpyClient(tokens=90), SpyClient(tokens=10)
        gen_a = self._build(spy_a, budget=100)
        gen_b = self._build(spy_b, budget=100)
        gen_a("a", model="m")
        gen_a("a2", model="m")  # A is now at 180, over its cap
        assert gen_b.usage() == {"total_tokens": 0, "calls": 0}
        gen_b("b", model="m")
        assert gen_b.usage() == {"total_tokens": 10, "calls": 1}
        with pytest.raises(mod.BudgetExhausted):
            gen_a("a3", model="m")
        assert gen_b("b2", model="m") == "ok", "session B must be unaffected by A"

    def test_defaults_none_is_allowed(self) -> None:
        spy = SpyClient()
        gen = mod.make_generate(spy.as_dict_client, token_budget=50)
        gen("p", model="m")
        assert "temperature" not in spy.calls[0][1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
