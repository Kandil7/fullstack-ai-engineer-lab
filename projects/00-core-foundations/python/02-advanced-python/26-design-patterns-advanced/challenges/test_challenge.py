"""
Challenge 26: Design Patterns Advanced — Hidden Tests
=====================================================
Runs against starter.py by default; set CHALLENGE_MODULE=solution to
verify the reference implementation.
"""

from __future__ import annotations

import importlib.util
import inspect
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


target = _load(os.environ.get("CHALLENGE_MODULE", "starter"))


class TestRegistry:
    def test_calculator(self):
        assert target.registry_dispatch("calculator", {"a": 2, "b": 3}) == "5"

    def test_search(self):
        assert target.registry_dispatch("search", {"q": "rag"}) == "results-for:rag"

    def test_unknown_raises(self):
        with pytest.raises(ValueError):
            target.registry_dispatch("unknown", {})

    def test_registered_via_init_subclass(self):
        assert sorted(target.Tool.registry) == ["calculator", "search"]


class TestRegistrySource:
    def test_no_manual_assignment_in_solution(self):
        # Manual registration uses a literal string key:
        # `Tool.registry["calculator"] = Calculator`. The legitimate
        # __init_subclass__ line uses `cls.__name__`, so it is exempt.
        src_path = HERE / (os.environ.get("CHALLENGE_MODULE", "starter") + ".py")
        src = src_path.read_text(encoding="utf-8")
        manual = [line.strip() for line in src.splitlines()
                  if ("registry[" in line and "=" in line
                      and ('registry["' in line or "registry['" in line))]
        assert manual == [], f"manual registration lines found: {manual}"


class TestEditor:
    def test_insert_and_text(self):
        e = target.Editor()
        e.insert(0, "hello")
        assert e.text() == "hello"

    def test_delete_captures_and_undo_restores(self):
        e = target.Editor()
        e.insert(0, "hello")
        e.delete(0, 2)
        assert e.text() == "llo"
        e.undo()
        assert e.text() == "hello", "undo must restore the exact deleted text"

    def test_double_undo(self):
        e = target.Editor()
        e.insert(0, "hello")
        e.delete(0, 2)
        e.undo()
        e.undo()
        assert e.text() == ""

    def test_redo(self):
        e = target.Editor()
        e.insert(0, "hello")
        e.undo()
        e.redo()
        assert e.text() == "hello"

    def test_new_edit_discards_redo(self):
        e = target.Editor()
        e.insert(0, "hello")
        e.insert(5, "!")
        e.undo()                    # removes "!"
        e.insert(5, "?")            # new edit: redo history must be gone
        assert e.text() == "hello?"
        e.redo()                    # must do nothing now
        assert e.text() == "hello?"

    def test_delete_undo_middle(self):
        e = target.Editor()
        e.insert(0, "abcdef")
        e.delete(2, 3)
        assert e.text() == "abf"
        e.undo()
        assert e.text() == "abcdef"


class TestDependencyInjection:
    def test_fake_prefix(self):
        svc = target.Summarizer(target.FakeLLMClient())
        assert svc.summarize("x").startswith("FAKE:")

    def test_real_prefix(self):
        svc = target.Summarizer(target.RealLLMClient())
        assert svc.summarize("x").startswith("REAL:")

    def test_prompt_and_temp_flow(self):
        svc = target.Summarizer(target.FakeLLMClient())
        # prompt becomes "summarize: hello world" -> first 5 chars: "summa"
        assert svc.summarize("hello world") == "FAKE:summa:0.0"

    def test_constructor_injection_signature(self):
        params = list(inspect.signature(target.Summarizer.__init__).parameters)
        assert "llm" in params, (
            f"no llm parameter ({params}): the client is constructed inside"
        )

    def test_both_satisfy_protocol(self):
        assert isinstance(target.FakeLLMClient(), target.LLMClient)
        assert isinstance(target.RealLLMClient(), target.LLMClient)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
