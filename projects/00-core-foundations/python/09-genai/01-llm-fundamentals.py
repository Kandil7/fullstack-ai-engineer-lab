"""
GenAI - 01: LLM Fundamentals
============================
Topics: tokenization (BPE) and why token != word; context windows;
autoregressive generation; temperature/top-p/top-k; why the same prompt
gives different answers; cost per token.

Why this matters for AI/backend engineering:
    Every LLM decision - model choice, context budget, cost estimate,
    caching strategy - starts from tokens. Tokens are the currency of
    LLM engineering: you must be able to count, price, and reason about
    them before you write a single API call.

Run:      python 01-llm-fundamentals.py
Verify:   python 01-llm-fundamentals.py --verify
Reference: https://platform.openai.com/docs/concepts/tokens
"""

from __future__ import annotations

import sys


# ============================================================
# 1. Tokenization - Why Token != Word
# ============================================================
# BPE (Byte-Pair Encoding) splits text into sub-word units. Common words
# are one token; rare words split into several; "hello" is 1 token,
# "hallucination" is ~4. A token is roughly 0.75 words for English.

def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token, or ~1.3 tokens/word."""
    chars = len(text)
    words = len(text.split())
    return max(1, (chars // 4 + words // 2) // 1)


# Example 1: token estimation
texts = {
    "hello world": None,
    "The quick brown fox jumps over the lazy dog": None,
    "Supercalifragilisticexpialidocious": None,
}
print("Example 1: token estimation (approx)")
for t in texts:
    print(f"  {t[:40]:<44} ~{estimate_tokens(t)} tokens")

# ============================================================
# 2. Context Windows
# ============================================================
# Context = prompt + completion. If your prompt is 90k tokens and the
# window is 128k, the model has ~38k left to write.

def completion_budget(context_window: int, prompt_tokens: int,
                      reserved_output: int) -> int | None:
    """Tokens left for the model to generate; None if prompt overflows."""
    if prompt_tokens + reserved_output > context_window:
        return None
    return context_window - prompt_tokens - reserved_output


# Example 2: context budget math
budget = completion_budget(128_000, 90_000, 4_096)
print("\nExample 2: context window budgeting")
print(f"  128k window, 90k prompt, 4k reserved -> {budget} tokens for output")
assert budget == 33_904
assert completion_budget(128_000, 130_000, 4_096) is None, "overflow -> None"

# ============================================================
# 3. Autoregressive Generation
# ============================================================
# The model predicts the NEXT token given all previous ones, one at a
# time. It cannot "plan" beyond the next token - coherence emerges from
# the strength of the probability distribution.

def simple_autoregressive(probs: dict[str, float], steps: int,
                          temperature: float = 1.0) -> list[str]:
    """Greedy-ish token-by-token generation for a tiny toy model."""
    import random
    random.seed(42)
    tokens = []
    for _ in range(steps):
        # temperature: lower = more confident/deterministic
        scaled = {k: v ** (1.0 / temperature) for k, v in probs.items()}
        total = sum(scaled.values())
        r = random.random() * total
        acc = 0.0
        chosen = list(scaled)[0]
        for k, v in scaled.items():
            acc += v
            if r <= acc:
                chosen = k
                break
        tokens.append(chosen)
    return tokens


# Example 3: temperature changes determinism
toy = {"the": 0.5, "a": 0.25, "an": 0.25}
cold = simple_autoregressive(toy, 10, temperature=0.2)
hot = simple_autoregressive(toy, 10, temperature=2.0)
print("\nExample 3: temperature effect")
print(f"  cold (T=0.2): {cold}")
print(f"  hot  (T=2.0): {hot}")

# ============================================================
# 4. Sampling Parameters
# ============================================================
# top-p (nucleus): keep the smallest set of tokens whose cumulative
# probability reaches p. top-k: keep only the k most likely tokens.

def top_p_filter(probs: dict[str, float], p: float) -> list[str]:
    """Return the token names in the top-p nucleus."""
    ranked = sorted(probs.items(), key=lambda kv: kv[1], reverse=True)
    keep: list[str] = []
    acc = 0.0
    for tok, prob in ranked:
        acc += prob
        keep.append(tok)
        if acc >= p:
            break
    return keep


# Example 4: top-p nucleus
probs = {"cat": 0.6, "dog": 0.25, "bird": 0.1, "fish": 0.05}
print("\nExample 4: top-p nucleus")
print(f"  top-p=0.9 -> {top_p_filter(probs, 0.9)}")
print(f"  top-p=0.7 -> {top_p_filter(probs, 0.7)}")
assert top_p_filter(probs, 0.9) == ["cat", "dog", "bird"]
assert top_p_filter(probs, 0.7) == ["cat", "dog"]

# ============================================================
# 5. Cost per Token
# ============================================================

def prompt_cost(prompt_tokens: int, output_tokens: int,
                price_in: float, price_out: float) -> float:
    """Cost of one call in dollars (prices per 1M tokens)."""
    return (prompt_tokens * price_in + output_tokens * price_out) / 1_000_000


# Example 5: cost math
cost = prompt_cost(10_000, 2_000, price_in=3.0, price_out=15.0)
print("\nExample 5: cost per call")
print(f"  10k in + 2k out -> ${cost:.4f}")
assert abs(cost - (10_000 * 3 + 2_000 * 15) / 1_000_000) < 1e-9

# ============================================================
# Production Pattern
# ============================================================
# Always count tokens BEFORE sending: refuse calls that would overflow
# the context window, and log cost per call for observability.

def prepare_request(prompt: str, context_window: int,
                    max_output: int, price_in: float, price_out: float,
                    estimate_fn=estimate_tokens) -> dict:
    """Validate a request against the context window and price it."""
    prompt_tokens = estimate_fn(prompt)
    budget = completion_budget(context_window, prompt_tokens, max_output)
    if budget is None:
        raise ValueError(f"prompt {prompt_tokens} tokens exceeds window "
                         f"with {max_output} reserved for output")
    return {
        "prompt_tokens": prompt_tokens,
        "max_output": max_output,
        "estimated_cost": prompt_cost(prompt_tokens, max_output, price_in, price_out),
    }


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: assuming 1 token = 1 word (English is ~1.3 tokens/word)
# MISTAKE: filling the whole window with prompt - no room to generate
# MISTAKE: same prompt, different answers treated as a bug
#   (sampling is stochastic; set temperature=0 for determinism)


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    assert estimate_tokens("hello world") >= 1, "estimate is positive"
    assert completion_budget(100, 50, 30) == 20, "budget math"
    assert completion_budget(100, 90, 30) is None, "overflow detected"

    toy = {"a": 0.7, "b": 0.2, "c": 0.1}
    assert top_p_filter(toy, 0.75) == ["a", "b"], "top-p nucleus"
    assert top_p_filter(toy, 0.5) == ["a"], "tiny nucleus"

    seq = simple_autoregressive(toy, 5, temperature=1.0)
    assert len(seq) == 5 and all(t in toy for t in seq), "tokens in vocabulary"

    c = prompt_cost(1_000_000, 0, 1.0, 1.0)
    assert abs(c - 1.0) < 1e-9, "1M input tokens at $1/M = $1"

    req = prepare_request("hi there", 4096, 512, 1.0, 1.0)
    assert req["prompt_tokens"] >= 1 and req["estimated_cost"] > 0, "request priced"
    try:
        prepare_request("x" * 50_000, 4096, 512, 1.0, 1.0)
        raised = False
    except ValueError:
        raised = True
    assert raised, "overflowing prompt rejected"
    print("[OK] 01-llm-fundamentals: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Tokens, not words, are the unit of LLM work.")
        print("2. Budget context: prompt + reserved output <= window.")
        print("3. temperature/top-p/top-k control sampling; cost = tokens x price.")
        _verify()
