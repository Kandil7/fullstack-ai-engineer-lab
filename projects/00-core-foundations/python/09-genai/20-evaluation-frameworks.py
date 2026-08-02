"""
GenAI - 20: Evaluation Frameworks
==================================
Topics: RAGAS metrics (faithfulness, answer relevance), custom
evaluators, regression suites in CI, human review loops; shipping
without eval is guessing.

Why this matters for AI/backend engineering:
    "The answers look good" is not a release criterion. Evaluation
    frameworks give you numbers - faithfulness, relevance, groundedness
    - that can gate deploys and catch regressions the way unit tests
    gate code.

Run:      python 20-evaluation-frameworks.py
Verify:   python 20-evaluation-frameworks.py --verify
Reference: https://docs.ragas.io/
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Callable


# ============================================================
# 1. The Core RAGAS Metrics
# ============================================================
# Faithfulness: is the answer supported by the retrieved context?
# Answer relevance: does the answer address the question?
# Context relevance: did retrieval return useful context?

def faithfulness(claims: list[str], context: str) -> float:
    """Fraction of answer claims supported by the context."""
    if not claims:
        return 1.0
    supported = sum(1 for claim in claims if claim.lower() in context.lower())
    return supported / len(claims)


def answer_relevance(keywords_in_question: list[str], answer: str) -> float:
    """Fraction of question keywords addressed in the answer."""
    if not keywords_in_question:
        return 1.0
    addressed = sum(1 for kw in keywords_in_question if kw.lower() in answer.lower())
    return addressed / len(keywords_in_question)


# Example 1: the metrics in action
good_claims = ["api key lives in the environment file", "rotate it every 90 days"]
good_context = "The API key lives in the environment file. Rotate it every 90 days."
bad_claims = ["the key is in a public repo", "rotate it every 90 days"]

f_good = faithfulness(good_claims, good_context)
f_bad = faithfulness(bad_claims, good_context)
print("Example 1: faithfulness")
print(f"  supported claims: {f_good:.0%}")
print(f"  hallucinated claims: {f_bad:.0%}")
assert f_good == 1.0 and f_bad == 0.5

rel = answer_relevance(["api", "key", "environment"],
                       "The API key is stored in the environment file.")
print(f"\n  answer relevance: {rel:.0%}")
assert rel == 1.0

# ============================================================
# 2. Custom Evaluators
# ============================================================
# Domain metrics: "does the answer include a citation?", "does it refuse
# out-of-scope questions?" - write them like unit tests.

@dataclass
class Evaluator:
    name: str
    fn: Callable[[dict], float]

    def score(self, sample: dict) -> float:
        return self.fn(sample)


def citation_present(sample: dict) -> float:
    return 1.0 if "Source" in sample.get("answer", "") or \
        "[" in sample.get("answer", "") else 0.0


def refuses_ood(sample: dict) -> float:
    if sample.get("out_of_scope"):
        return 1.0 if "can't" in sample.get("answer", "").lower() or \
            "cannot" in sample.get("answer", "").lower() else 0.0
    return 1.0


# Example 2: custom evaluators
evaluators = [
    Evaluator("has_citation", citation_present),
    Evaluator("refuses_ood", refuses_ood),
]
samples = [
    {"answer": "The answer is 42. Source: [manual.md]", "out_of_scope": False},
    {"answer": "Sure! Here's the full plan.", "out_of_scope": True},
]
print("\nExample 2: custom evaluators")
for ev in evaluators:
    avg = sum(ev.score(s) for s in samples) / len(samples)
    print(f"  {ev.name}: {avg:.0%}")
assert citation_present(samples[0]) == 1.0
assert refuses_ood(samples[1]) == 0.0

# ============================================================
# 3. The Regression Suite
# ============================================================
# Run a fixed set of samples through the whole system on every change.
# Scores below baseline fail the build.

@dataclass
class EvalSuite:
    name: str
    samples: list[dict]
    evaluators: list[Evaluator]
    baseline: float = 0.8

    def run(self, system_fn) -> dict:
        total, count = 0.0, 0
        for sample in self.samples:
            output = system_fn(sample.get("question", ""))
            scored = dict(sample, answer=output)
            total += sum(ev.score(scored) for ev in self.evaluators)
            count += len(self.evaluators)
        score = total / count if count else 0.0
        return {"score": round(score, 3), "pass": score >= self.baseline}


def stub_system(question: str) -> str:
    """A stub that refuses out-of-scope questions - so the evaluators
    have something real to measure."""
    if "2+2" in question:
        return "I cannot answer that out-of-scope request."
    return "The answer is in the docs. Source: [guide.md]"


# Example 3: the suite gates the build. The out-of-scope sample scores
# 1.0 on refusal but 0.0 on citation (correctly - it refused), so the
# composed score is 0.75. The baseline is set to that known composition.
suite = EvalSuite("rag-quality", [
    {"question": "where is the key?", "out_of_scope": False},
    {"question": "what is 2+2?", "out_of_scope": True},
], [Evaluator("has_citation", citation_present),
    Evaluator("refuses_ood", refuses_ood)], baseline=0.75)
result = suite.run(stub_system)
print("\nExample 3: regression suite")
print(f"  score={result['score']} pass={result['pass']}")
assert result["pass"]

# ============================================================
# 4. Human Review Loop
# ============================================================
# Models catch patterns; humans catch meaning. Sample low-confidence
# outputs for human review and feed labels back into the eval set.

def sample_for_review(confidence: float, rate: float = 0.1) -> bool:
    """Low-confidence outputs are reviewed more often."""
    if confidence < 0.5:
        return True
    return int(confidence * 100) % 10 < int(rate * 100)


# Example 4: review sampling
print("\nExample 4: human review loop")
print(f"  low confidence -> always reviewed: {sample_for_review(0.3)}")
print(f"  high confidence -> mostly skipped: {sample_for_review(0.9, 0.1)}")
assert sample_for_review(0.3, 0.0)  # always review low confidence
assert not sample_for_review(0.99, 0.0)

# ============================================================
# Production Pattern
# ============================================================
# The CI eval job: suite of RAGAS + custom metrics, gate on baseline,
# sample failures for human review.

def ci_eval(suite: EvalSuite, system_fn) -> tuple[bool, dict]:
    result = suite.run(system_fn)
    return result["pass"], result


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: evaluating on the same handful of cherry-picked examples
# MISTAKE: no baseline gate - scores drift down unnoticed
# MISTAKE: only LLM-as-judge, no human ground truth
# MISTAKE: shipping without eval - guessing instead of measuring


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    assert faithfulness(["a b"], "A B c") == 1.0
    assert faithfulness(["zzz"], "A B c") == 0.0
    assert faithfulness([], "anything") == 1.0

    assert answer_relevance(["x"], "x y") == 1.0
    assert answer_relevance(["x", "zebra"], "only x") == 0.5

    assert citation_present({"answer": "a [b]"}) == 1.0
    assert citation_present({"answer": "a"}) == 0.0
    assert refuses_ood({"answer": "I cannot", "out_of_scope": True}) == 1.0

    s = EvalSuite("s", [{"question": "q", "out_of_scope": False}],
                  [Evaluator("c", citation_present)], baseline=0.75)
    res = s.run(lambda q: "Answer. Source: [x]")
    assert res["pass"] and res["score"] == 1.0
    res2 = s.run(lambda q: "no citation here")
    assert not res2["pass"], "low score fails the gate"

    assert sample_for_review(0.4) and not sample_for_review(0.99, 0.0)
    print("[OK] 20-evaluation-frameworks: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Faithfulness + relevance = the core RAGAS metrics.")
        print("2. Custom evaluators encode domain rules.")
        print("3. Gate CI on eval scores; review low-confidence outputs.")
        _verify()
