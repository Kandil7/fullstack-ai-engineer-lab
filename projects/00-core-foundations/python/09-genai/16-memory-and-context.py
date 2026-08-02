"""
GenAI - 16: Memory and Context Management
==========================================
Topics: conversation history management, summarization, context-window
budgeting, retrieval as memory, sliding windows.

Why this matters for AI/backend engineering:
    Context is a finite, expensive resource. Every conversation is a
    budget problem: keep the system prompt + recent turns + retrieval,
    drop or summarize the middle, and never overflow the window.

Run:      python 16-memory-and-context.py
Verify:   python 16-memory-and-context.py --verify
Reference: https://platform.openai.com/docs/guides/text-generation
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


# ============================================================
# 1. The Context Budget
# ============================================================
# Every request = system + history + new input + reserved output.
# Budget: window - system - reserved = what history can occupy.

def history_budget(window: int, system_tokens: int, new_input_tokens: int,
                   reserved_output: int) -> int:
    """Tokens available for the conversation history."""
    return window - system_tokens - new_input_tokens - reserved_output


# Example 1: budget math
budget = history_budget(4096, system_tokens=300, new_input_tokens=200,
                        reserved_output=1000)
print("Example 1: context budget")
print(f"  4096 - 300 - 200 - 1000 = {budget} tokens for history")
assert budget == 2596

# ============================================================
# 2. Sliding Window
# ============================================================
# Keep the last N turns; drop the oldest. Simple, lossy.

def sliding_window(history: list[dict], max_turns: int) -> list[dict]:
    return history[-max_turns:]


# Example 2: sliding window
history = [{"role": "user", "content": f"msg-{i}"} for i in range(10)]
window = sliding_window(history, 4)
print("\nExample 2: sliding window")
print(f"  {len(history)} turns -> keep last 4: "
      f"{[m['content'] for m in window]}")
assert len(window) == 4 and window[0]["content"] == "msg-6"

# ============================================================
# 3. Summarization
# ============================================================
# Instead of dropping old turns, compress them into a running summary
# that keeps the important facts. A stub summarizer demonstrates the
# shape; in production it is an LLM call.

def summarize(old_turns: list[dict], summary_fn) -> dict:
    """Replace old turns with one summary message."""
    text = " ".join(m["content"] for m in old_turns)
    return {"role": "system", "content": f"Summary: {summary_fn(text)}"}


def stub_summarizer(text: str) -> str:
    return f"[compressed {len(text)} chars]"


# Example 3: summarize old turns
old = [{"role": "user", "content": "f" * 200} for _ in range(5)]
summary = summarize(old, stub_summarizer)
print("\nExample 3: summarization")
print(f"  {len(old)} turns -> {summary['content']}")
assert summary["role"] == "system" and "compressed" in summary["content"]

# ============================================================
# 4. Retrieval as Memory
# ============================================================
# For long-lived knowledge, don't stuff everything in the prompt -
# retrieve what is relevant. The vector store IS the memory.

@dataclass
class FactStore:
    facts: dict[str, str]

    def retrieve(self, query: str) -> str:
        """Naive keyword retrieval over stored facts."""
        for key, value in self.facts.items():
            if query in key:
                return value
        return "no relevant memory"


# Example 4: retrieval-based memory
facts = FactStore({
    "user prefers python": "They code in Python and dislike JS.",
    "project stack": "FastAPI + PostgreSQL + React.",
})
memory = facts.retrieve("user prefers")
print("\nExample 4: retrieval as memory")
print(f"  retrieved: {memory}")
assert "Python" in memory

# ============================================================
# 5. The Production Context Builder
# ============================================================
# Assemble the final messages: system + summary + recent turns + input,
# trimmed to the budget.

def build_context(system: str, summary: str | None, recent: list[dict],
                  new_input: str, budget: int,
                  estimate_fn) -> list[dict]:
    """Build a context that never exceeds the token budget."""
    messages = [{"role": "system", "content": system}]
    if summary:
        messages.append({"role": "system", "content": summary})
    messages.extend(recent)
    messages.append({"role": "user", "content": new_input})

    used = sum(estimate_fn(m["content"]) for m in messages)
    if used > budget:
        # drop oldest history messages until we fit
        while used > budget and len(messages) > 3:
            dropped = messages.pop(2)  # first history message
            used -= estimate_fn(dropped["content"])
    return messages


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


# Example 5: the context builder
ctx = build_context("You are a helpful assistant", "Previous: math help",
                    [{"role": "user", "content": "explain logs"}],
                    "and derivatives", budget=200, estimate_fn=estimate_tokens)
print("\nExample 5: context builder")
for m in ctx:
    print(f"  [{m['role']}] {m['content'][:30]}")
assert ctx[0]["role"] == "system" and ctx[-1]["role"] == "user"

# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: unbounded history - the window overflows and the call fails
# MISTAKE: dropping old turns with no summary - the agent forgets key facts
# MISTAKE: stuffing all knowledge into the prompt instead of retrieving
# MISTAKE: forgetting reserved output when budgeting


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    assert history_budget(100, 10, 20, 30) == 40
    assert history_budget(100, 10, 20, 90) < 0, "over budget goes negative"

    w = sliding_window([{"role": "u", "content": str(i)} for i in range(5)], 2)
    assert [m["content"] for m in w] == ["3", "4"]

    s = summarize([{"role": "u", "content": "abc"}], stub_summarizer)
    assert "compressed" in s["content"]

    f = FactStore({"x y": "value"})
    assert f.retrieve("x") == "value" and f.retrieve("zzz") == "no relevant memory"

    ctx = build_context("sys", "sum", [{"role": "u", "content": "x" * 50}], "q",
                        budget=50, estimate_fn=estimate_tokens)
    used = sum(estimate_tokens(m["content"]) for m in ctx)
    assert used <= 50, "context fits the budget"

    ctx2 = build_context("sys", None, [], "q", budget=100, estimate_fn=estimate_tokens)
    assert len(ctx2) == 2, "system + user when no history"
    print("[OK] 16-memory-and-context: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Budget: window - system - input - reserved output.")
        print("2. Sliding windows drop; summaries compress.")
        print("3. Retrieve knowledge instead of stuffing the prompt.")
        _verify()
