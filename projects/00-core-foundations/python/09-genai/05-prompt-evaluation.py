"""
GenAI - 05: Prompt Evaluation
=============================
Topics: golden datasets, regression tests for prompts, LLM-as-judge and
its biases, pairwise comparison, the eval loop before optimizing.

Why this matters for AI/backend engineering:
    Prompts change. If you cannot measure a prompt change, you cannot
    ship it - a "small tweak" can silently degrade quality. Eval is the
    safety net that makes prompt engineering a discipline instead of a
    vibe.

Run:      python 05-prompt-evaluation.py
Verify:   python 05-prompt-evaluation.py --verify
Reference: https://platform.openai.com/docs/guides/prompt-evaluation
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any, Callable


# ============================================================
# 1. Golden Datasets
# ============================================================
# A golden set: (input, expected) pairs that encode the behavior you
# want. Small and curated beats large and messy - you must be able to
# read every case.

@dataclass
class GoldenCase:
    input: str
    expected: str


GOLDEN_SENTIMENT = [
    GoldenCase("Great product, highly recommend!", "POSITIVE"),
    GoldenCase("Terrible, broke in a day.", "NEGATIVE"),
    GoldenCase("It's fine, nothing special.", "NEUTRAL"),
    GoldenCase("Worst purchase ever.", "NEGATIVE"),
    GoldenCase("Love it, works perfectly.", "POSITIVE"),
]


# ============================================================
# 2. The Eval Runner
# ============================================================

def run_eval(model: Callable[[str], str], cases: list[GoldenCase]) -> dict:
    correct = sum(1 for c in cases if model(c.input) == c.expected)
    return {
        "correct": correct,
        "total": len(cases),
        "accuracy": correct / len(cases),
    }


# Example 1: two candidate prompts
def prompt_a(text: str) -> str:
    return "POSITIVE" if "great" in text.lower() or "love" in text.lower() else \
        "NEGATIVE" if "terrible" in text.lower() or "worst" in text.lower() else "NEUTRAL"


def prompt_b(text: str) -> str:
    # A worse prompt: only keyword matching on "great"
    return "POSITIVE" if "great" in text.lower() else "NEUTRAL"


res_a = run_eval(prompt_a, GOLDEN_SENTIMENT)
res_b = run_eval(prompt_b, GOLDEN_SENTIMENT)
print("Example 1: golden-set evaluation")
print(f"  prompt_a accuracy: {res_a['accuracy']:.0%} ({res_a['correct']}/{res_a['total']})")
print(f"  prompt_b accuracy: {res_b['accuracy']:.0%} ({res_b['correct']}/{res_b['total']})")
assert res_a["accuracy"] >= res_b["accuracy"], "better prompt scores better"

# ============================================================
# 3. Regression Guard
# ============================================================
# Lock the eval into CI: a prompt change that drops accuracy below the
# baseline must fail the build.

@dataclass
class PromptRegressionGuard:
    baseline_accuracy: float
    threshold: float = 0.0

    def approve(self, accuracy: float) -> tuple[bool, str]:
        if accuracy < self.baseline_accuracy - self.threshold:
            return False, (f"regression: {accuracy:.0%} < baseline "
                           f"{self.baseline_accuracy:.0%}")
        return True, f"accepted: {accuracy:.0%} >= {self.baseline_accuracy:.0%}"


# Example 2: the guard
guard = PromptRegressionGuard(baseline_accuracy=0.80)
ok, msg = guard.approve(res_a["accuracy"])
print("\nExample 2: regression guard")
print(f"  {msg}")
assert ok
blocked, msg2 = guard.approve(0.40)
print(f"  {msg2}")
assert not blocked

# ============================================================
# 4. LLM-as-Judge and Its Biases
# ============================================================
# A second LLM scores outputs. Powerful, but biased: position bias
# (prefers the first answer), verbosity bias (prefers longer), and
# self-preference (prefers its own style). Mitigate with pairwise
# comparison and swapped order.

@dataclass
class PairwiseJudge:
    def choose(self, a: str, b: str) -> str:
        """Simulate a judge with a mild position bias toward 'a'."""
        # prefer longer unless clearly wrong
        if len(b) > len(a) + 10 and "wrong" not in b:
            return "B"
        return "A"


# Example 3: pairwise comparison is more stable than absolute scores
judge = PairwiseJudge()
pair_a = judge.choose("Short answer.", "A much longer, more detailed answer.")
pair_b = judge.choose("A much longer, more detailed answer.", "Short answer.")
print("\nExample 3: pairwise judge")
print(f"  (short, long)   -> winner {pair_a}")
print(f"  (long,  short)  -> winner {pair_b}")
assert pair_a == "B" and pair_b == "A", "order-swap detects position bias"

# ============================================================
# 5. The Eval Loop Before Optimizing
# ============================================================
# Order of operations: baseline -> hypothesize -> change ONE thing ->
# measure -> accept/reject. Optimizing without an eval loop is tuning
# by vibes.

def eval_loop(current: Callable[[str], str], candidate: Callable[[str], str],
              cases: list[GoldenCase], guard: PromptRegressionGuard) -> str:
    cur_res = run_eval(current, cases)
    cand_res = run_eval(candidate, cases)
    if cand_res["accuracy"] > cur_res["accuracy"]:
        ok, _ = guard.approve(cand_res["accuracy"])
        return "adopt candidate" if ok else "keep current"
    return "keep current"


# Example 4: the loop in action
verdict = eval_loop(prompt_b, prompt_a, GOLDEN_SENTIMENT, guard)
print("\nExample 4: eval loop")
print(f"  verdict: {verdict}")
assert verdict == "adopt candidate"

# ============================================================
# Production Pattern
# ============================================================
# The production eval suite: golden set + regression guard + a
# periodic re-run against real traffic (sampled, labeled).

def eval_report(name: str, model: Callable[[str], str]) -> str:
    res = run_eval(model, GOLDEN_SENTIMENT)
    ok, msg = guard.approve(res["accuracy"])
    return f"[{name}] {msg} ({res['correct']}/{res['total']})"


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: hand-waving "seems better" instead of measuring
# MISTAKE: judging with an LLM without controlling for position bias
# MISTAKE: changing prompt + examples + model in the same experiment
# MISTAKE: no regression guard - quality silently drifts down


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    res = run_eval(prompt_a, GOLDEN_SENTIMENT)
    assert res["total"] == 5 and 0.0 <= res["accuracy"] <= 1.0

    g = PromptRegressionGuard(0.8)
    assert g.approve(0.8)[0] and not g.approve(0.79)[0]
    g2 = PromptRegressionGuard(0.8, threshold=0.1)
    assert g2.approve(0.75)[0], "within tolerance"

    j = PairwiseJudge()
    assert j.choose("x", "x" * 50) == "B", "prefers longer"
    assert j.choose("x" * 50, "x") == "A"

    assert eval_loop(prompt_b, prompt_a, GOLDEN_SENTIMENT, g) == "adopt candidate"
    assert eval_loop(prompt_a, prompt_b, GOLDEN_SENTIMENT, g) == "keep current"

    report = eval_report("test", prompt_a)
    assert report.startswith("[test]") and "5/5" in report
    print("[OK] 05-prompt-evaluation: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Curated golden sets are the measurement basis.")
        print("2. Regression guards lock quality into CI.")
        print("3. Pairwise judging controls position/verbosity bias.")
        _verify()
