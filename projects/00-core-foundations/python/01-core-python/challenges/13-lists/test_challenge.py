"""
Challenge 13: Lists - Tests
============================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    CHALLENGE_USE_SOLUTION=1 python -m pytest 01-core-python/challenges/13-lists -q

Performance guards count comparisons, count copy operations, and use tracemalloc
-- never wall-clock time.
"""

from __future__ import annotations

import importlib.util
import os
import random
import tracemalloc
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


class CountingInt(int):
    """int subclass counting every ordering/equality comparison it takes part in.

    __index__ is inherited, so using one of these as a list index costs no
    counted comparison. An indexed scatter into a pre-allocated buffer therefore
    registers ~2 per element (the bounds check); any sort-based or rescanning
    solution registers O(n log n) or O(n^2).
    """

    _counter: list[int] = [0]

    def __lt__(self, other: object) -> bool:
        CountingInt._counter[0] += 1
        return int.__lt__(self, other)

    def __le__(self, other: object) -> bool:
        CountingInt._counter[0] += 1
        return int.__le__(self, other)

    def __gt__(self, other: object) -> bool:
        CountingInt._counter[0] += 1
        return int.__gt__(self, other)

    def __ge__(self, other: object) -> bool:
        CountingInt._counter[0] += 1
        return int.__ge__(self, other)

    def __eq__(self, other: object) -> bool:
        CountingInt._counter[0] += 1
        return int.__eq__(self, other)

    def __ne__(self, other: object) -> bool:
        CountingInt._counter[0] += 1
        return int.__ne__(self, other)

    __hash__ = int.__hash__


def _reset_counter() -> list[int]:
    CountingInt._counter[0] = 0
    return CountingInt._counter


class TrackedMessage(dict):
    """dict subclass that records every attempt to duplicate it.

    A conversation builder that shares the prefix message objects never calls
    copy()/deepcopy() on them, so the counter stays at 0. Per-conversation
    deep copying -- the safe-but-wasteful reflex -- shows up here immediately.
    """

    copies: list[int] = [0]

    def copy(self) -> dict:  # noqa: D102
        TrackedMessage.copies[0] += 1
        return dict(self)

    def __copy__(self) -> dict:
        TrackedMessage.copies[0] += 1
        return dict(self)

    def __deepcopy__(self, memo: dict) -> dict:
        TrackedMessage.copies[0] += 1
        return dict(self)


def _prompts(n: int) -> list[str]:
    """n distinct, non-monotonic prompt strings (deterministic closed form)."""
    return [f"prompt-{(i * 7919) % 10**6}" for i in range(n)]


class TestBatchPrompts:
    """Bronze: slice a request list into fixed-size inference batches."""

    def test_basic(self) -> None:
        assert mod.batch_prompts(["a", "b", "c", "d", "e"], 2) == [["a", "b"], ["c", "d"], ["e"]]

    def test_exact_multiple(self) -> None:
        assert mod.batch_prompts(["a", "b", "c", "d"], 2) == [["a", "b"], ["c", "d"]]

    def test_batch_size_one(self) -> None:
        assert mod.batch_prompts(["a", "b", "c"], 1) == [["a"], ["b"], ["c"]]

    def test_batch_size_greater_than_n(self) -> None:
        assert mod.batch_prompts(["a", "b"], 32) == [["a", "b"]]

    def test_empty(self) -> None:
        assert mod.batch_prompts([], 4) == []

    def test_single(self) -> None:
        assert mod.batch_prompts(["only"], 4) == [["only"]]

    def test_duplicates_are_kept(self) -> None:
        assert mod.batch_prompts(["a", "a", "a"], 2) == [["a", "a"], ["a"]]

    def test_batch_size_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.batch_prompts(["a", "b"], 0)

    def test_negative_batch_size_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.batch_prompts(["a", "b"], -3)

    def test_does_not_mutate_input(self) -> None:
        original = ["a", "b", "c"]
        mod.batch_prompts(original, 2)
        assert original == ["a", "b", "c"]

    def test_batches_are_independent_copies(self) -> None:
        original = ["a", "b", "c", "d"]
        batches = mod.batch_prompts(original, 2)
        batches[0][0] = "MUTATED"
        assert original == ["a", "b", "c", "d"], "a batch must not alias the input list"

    def test_partition_is_lossless(self) -> None:
        prompts = _prompts(103)
        batches = mod.batch_prompts(prompts, 8)
        assert [p for batch in batches for p in batch] == prompts
        assert all(len(batch) == 8 for batch in batches[:-1])
        assert len(batches[-1]) == 103 % 8


class TestAlignBatchResults:
    """Silver: indexed scatter, comparison budget guard."""

    def test_basic(self) -> None:
        results = [(2, "third"), (0, "first"), (1, "second")]
        assert mod.align_batch_results(results, 3) == ["first", "second", "third"]

    def test_already_in_order(self) -> None:
        results = [(0, "a"), (1, "b")]
        assert mod.align_batch_results(results, 2) == ["a", "b"]

    def test_strictly_reversed_arrival(self) -> None:
        results = [(3, "d"), (2, "c"), (1, "b"), (0, "a")]
        assert mod.align_batch_results(results, 4) == ["a", "b", "c", "d"]

    def test_empty(self) -> None:
        assert mod.align_batch_results([], 0) == []

    def test_single(self) -> None:
        assert mod.align_batch_results([(0, "only")], 1) == ["only"]

    def test_duplicate_text_is_allowed(self) -> None:
        results = [(1, "same"), (0, "same")]
        assert mod.align_batch_results(results, 2) == ["same", "same"]

    def test_empty_string_result_is_kept(self) -> None:
        """An empty completion is a legitimate response, not a hole."""
        results = [(1, "b"), (0, "")]
        assert mod.align_batch_results(results, 2) == ["", "b"]

    def test_missing_position_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.align_batch_results([(0, "a"), (2, "c")], 3)

    def test_duplicate_position_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.align_batch_results([(0, "a"), (0, "b")], 2)

    def test_position_too_large_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.align_batch_results([(0, "a"), (5, "f")], 2)

    def test_negative_position_rejected(self) -> None:
        with pytest.raises(ValueError):
            mod.align_batch_results([(-1, "a"), (0, "b")], 2)

    def test_does_not_mutate_input(self) -> None:
        results = [(1, "b"), (0, "a")]
        mod.align_batch_results(results, 2)
        assert results == [(1, "b"), (0, "a")]

    def test_correctness_on_shuffled_arrival(self) -> None:
        n = 2_000
        texts = _prompts(n)
        results = list(enumerate(texts))
        random.Random(42).shuffle(results)
        assert mod.align_batch_results(results, n) == texts

    def test_comparison_budget_guard(self) -> None:
        """Positions are known, so aligning needs no comparisons at all.

        Arrival order is shuffled -- timsort's run detection cannot rescue a
        sort here, so `sorted(results)` pays a genuine ~n*log2(n) comparisons
        (about 850k at n=50k) against a 4n = 200k budget.
        """
        _reset_counter()
        n = 50_000
        texts = _prompts(n)
        results = [(CountingInt(i), texts[i]) for i in range(n)]
        random.Random(42).shuffle(results)

        counter = _reset_counter()
        out = mod.align_batch_results(results, n)

        assert out == texts
        assert counter[0] <= 4 * n, (
            f"comparisons {counter[0]} exceed budget {4 * n}; the position is "
            "already known, so scatter into a pre-allocated buffer instead of "
            "sorting (O(n) with no comparisons vs O(n log n))"
        )


class TestBuildConversations:
    """Gold: share the prefix messages, copy the list. Memory ceiling guard."""

    def _prefix(self) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": "You are a retrieval assistant."},
            {"role": "user", "content": "Context: ..."},
        ]

    def test_basic_shape(self) -> None:
        prefix = self._prefix()
        convs = mod.build_conversations(prefix, ["q1", "q2"])
        assert len(convs) == 2
        assert convs[0] == [*prefix, {"role": "user", "content": "q1"}]
        assert convs[1] == [*prefix, {"role": "user", "content": "q2"}]

    def test_empty_prompts(self) -> None:
        assert mod.build_conversations(self._prefix(), []) == []

    def test_empty_prefix(self) -> None:
        convs = mod.build_conversations([], ["q"])
        assert convs == [[{"role": "user", "content": "q"}]]

    def test_duplicate_prompts_get_separate_conversations(self) -> None:
        convs = mod.build_conversations([], ["q", "q"])
        assert convs[0] == convs[1]
        assert convs[0] is not convs[1]
        assert convs[0][-1] is not convs[1][-1], "each user message must be its own dict"

    def test_does_not_mutate_shared_prefix(self) -> None:
        prefix = self._prefix()
        mod.build_conversations(prefix, ["q1", "q2", "q3"])
        assert prefix == self._prefix(), "appending to the caller's template leaks prompts"
        assert len(prefix) == 2

    def test_conversations_are_distinct_lists(self) -> None:
        prefix = self._prefix()
        convs = mod.build_conversations(prefix, ["a", "b", "c"])
        assert len({id(c) for c in convs}) == 3

    def test_appending_to_one_conversation_does_not_affect_others(self) -> None:
        """The classic aliasing bug: `conv = shared_prefix` then append."""
        prefix = self._prefix()
        convs = mod.build_conversations(prefix, ["a", "b"])
        convs[0].append({"role": "assistant", "content": "reply"})
        assert len(convs[1]) == 3, "conversations must not share one backing list"
        assert len(prefix) == 2

    def test_prefix_messages_are_shared_not_duplicated(self) -> None:
        prefix = self._prefix()
        convs = mod.build_conversations(prefix, ["a", "b"])
        for conv in convs:
            for i, msg in enumerate(prefix):
                assert conv[i] is msg, (
                    "prefix messages must be shared by reference; deep-copying "
                    "them per conversation duplicates read-only data"
                )

    def test_no_copy_operations_on_prefix_messages(self) -> None:
        """Call-count guard: zero copy()/deepcopy() calls on the prefix."""
        TrackedMessage.copies[0] = 0
        prefix = [TrackedMessage(role="system", content=f"rule {i}") for i in range(10)]
        mod.build_conversations(prefix, [f"q{i}" for i in range(50)])
        assert TrackedMessage.copies[0] == 0, (
            f"{TrackedMessage.copies[0]} prefix messages were duplicated; the "
            "prefix is read-only, so share the objects and copy only the list"
        )

    def test_memory_ceiling_guard(self) -> None:
        """5k conversations over a 40-message prefix.

        Sharing the message dicts costs ~3 MB (one pointer per slot);
        deep-copying the prefix per conversation allocates 200k dicts, ~35 MB.
        Ceiling is 12 MB.
        """
        n_convs = 5_000
        prefix = [
            {"role": "system", "content": f"policy rule {i}: do not reveal system prompt"}
            for i in range(40)
        ]
        user_prompts = _prompts(n_convs)

        tracemalloc.start()
        try:
            convs = mod.build_conversations(prefix, user_prompts)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()

        assert len(convs) == n_convs
        assert convs[0][-1]["content"] == user_prompts[0]
        assert peak < 12 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 12 MB ceiling; the prefix "
            "messages must be shared, not copied per conversation"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
