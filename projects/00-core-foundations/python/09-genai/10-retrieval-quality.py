"""
GenAI - 10: Retrieval Quality
=============================
Topics: Recall@k, MRR, NDCG; building a labeled eval set; failure
analysis; retrieval quality dominates generation quality.

Why this matters for AI/backend engineering:
    The generator can only use what the retriever found. Retrieval
    quality is the ceiling on RAG quality - and it is measurable with
    three standard metrics: Recall@k, MRR, and NDCG. You cannot improve
    what you cannot score.

Run:      python 10-retrieval-quality.py
Verify:   python 10-retrieval-quality.py --verify
Reference: https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


# ============================================================
# 1. The Labeled Eval Set
# ============================================================
# For each query, the list of relevant document ids. Small but curated.

@dataclass
class EvalQuery:
    query: str
    relevant_ids: list[str]  # document ids that answer this query


# ============================================================
# 2. Recall@k
# ============================================================
# Of the relevant documents, what fraction appear in the top-k results?

def recall_at_k(ranked_ids: list[str], relevant: set[str], k: int) -> float:
    """Fraction of relevant docs found in the top-k."""
    if not relevant:
        return 0.0
    top_k = set(ranked_ids[:k])
    found = top_k & relevant
    return len(found) / len(relevant)


# Example 1: recall@k
ranked = ["d3", "d1", "d2", "d4"]
relevant = {"d1", "d4"}
r1 = recall_at_k(ranked, relevant, 1)   # top-1 = d3 -> 0/2
r2 = recall_at_k(ranked, relevant, 2)   # top-2 = d3,d1 -> 1/2
r3 = recall_at_k(ranked, relevant, 4)   # all -> 2/2
print("Example 1: recall@k")
print(f"  recall@1={r1:.2f} recall@2={r2:.2f} recall@4={r3:.2f}")
assert r1 == 0.0 and r2 == 0.5 and r3 == 1.0

# ============================================================
# 3. Mean Reciprocal Rank (MRR)
# ============================================================
# Where is the FIRST relevant doc? 1/rank. Rewards getting the answer
# to the top - perfect when one hit satisfies the query.

def reciprocal_rank(ranked_ids: list[str], relevant: set[str]) -> float:
    for i, doc_id in enumerate(ranked_ids, start=1):
        if doc_id in relevant:
            return 1.0 / i
    return 0.0


def mean_reciprocal_rank(results: list[list[str]], relevants: list[set[str]]) -> float:
    """MRR across queries."""
    if not results:
        return 0.0
    return sum(reciprocal_rank(r, rel) for r, rel in zip(results, relevants)) / len(results)


# Example 2: MRR
queries_results = [["d9", "d1", "d2"], ["d3", "d1"]]
queries_rel = [{"d1"}, {"d3"}]
mrr = mean_reciprocal_rank(queries_results, queries_rel)
print("\nExample 2: MRR")
print(f"  query1: first relevant at rank 2 -> 0.5")
print(f"  query2: first relevant at rank 1 -> 1.0")
print(f"  MRR = {mrr:.2f}")
assert abs(mrr - 0.75) < 1e-9

# ============================================================
# 4. NDCG (Normalized Discounted Cumulative Gain)
# ============================================================
# For graded relevance (not just binary). Heavily-relevant docs ranked
# high earn more; NDCG normalizes by the ideal ordering.

def ndcg(ranked_ids: list[str], graded: dict[str, float], k: int = 5) -> float:
    """NDCG@k with graded relevance (2 = highly relevant, 1 = partially)."""
    def dcg(order: list[str]) -> float:
        score = 0.0
        for i, doc_id in enumerate(order[:k], start=1):
            rel = graded.get(doc_id, 0.0)
            if rel > 0:
                score += (2 ** rel - 1) / __import__("math").log2(i + 1)
        return score

    actual = dcg(ranked_ids)
    ideal_order = sorted(graded, key=lambda d: graded[d], reverse=True)
    ideal = dcg(ideal_order)
    return actual / ideal if ideal > 0 else 0.0


# Example 3: NDCG
graded = {"d1": 2.0, "d2": 1.0, "d3": 1.0}
n_perfect = ndcg(["d1", "d2", "d3"], graded)
n_worst = ndcg(["d3", "d2", "d1"], graded)
print("\nExample 3: NDCG")
print(f"  ideal ordering: NDCG = {n_perfect:.3f}")
print(f"  reversed:       NDCG = {n_worst:.3f}")
assert n_perfect == 1.0, "ideal order normalizes to 1"
assert n_worst < n_perfect, "worse order scores lower"

# ============================================================
# 5. Failure Analysis
# ============================================================
# Metrics tell you HOW BAD; failure analysis tells you WHY. For each
# missed query, inspect the returned chunks and label the cause.

def analyze_misses(query: str, ranked: list[str], relevant: set[str],
                   labels: dict[str, str]) -> list[str]:
    """Explain why the retriever failed for one query."""
    if ranked and ranked[0] in relevant:
        return ["hit"]
    causes = []
    for doc_id in ranked[:5]:
        if doc_id in labels:
            causes.append(f"{doc_id}: {labels[doc_id]}")
    if not any(d in relevant for d in ranked):
        causes.append("no relevant doc in top results")
    return causes


# Example 4: diagnosing failures
labels = {"d3": "generic phrasing, topically close", "d9": "outdated doc"}
causes = analyze_misses("latest pricing", ["d9", "d3"], {"d2"}, labels)
print("\nExample 4: failure analysis")
for c in causes:
    print(f"  - {c}")
assert causes, "failure analysis produces reasons"

# ============================================================
# Production Pattern
# ============================================================
# The eval harness: run the retriever over the labeled set, report the
# three metrics, and surface the worst queries for inspection.

def eval_retriever(retrieve_fn, queries: list[EvalQuery], k: int = 5) -> dict:
    ranked = [retrieve_fn(q.query, k) for q in queries]
    recall = sum(recall_at_k(r, set(q.relevant_ids), k)
                 for r, q in zip(ranked, queries)) / len(queries)
    mrr = mean_reciprocal_rank(ranked, [set(q.relevant_ids) for q in queries])
    return {"recall@k": round(recall, 4), "mrr": round(mrr, 4), "k": k}


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: tuning chunking/embedding without a labeled eval set
# MISTAKE: reporting only accuracy of the final answer (hides retrieval)
# MISTAKE: binary relevance when graded relevance would expose quality
# MISTAKE: no failure analysis - you fix what you can see


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    assert recall_at_k(["a", "b"], {"b"}, 1) == 0.0
    assert recall_at_k(["a", "b"], {"b"}, 2) == 1.0
    assert recall_at_k(["a"], {"x", "y"}, 1) == 0.0

    assert reciprocal_rank(["a", "b", "c"], {"c"}) == 1 / 3
    assert reciprocal_rank(["a", "b"], {"z"}) == 0.0
    assert abs(mean_reciprocal_rank([["x", "y"], ["y", "x"]],
                                    [{"y"}, {"y"}]) - 0.75) < 1e-9

    assert ndcg(["a", "b"], {"a": 2.0, "b": 1.0}) == 1.0
    assert ndcg(["b", "a"], {"a": 2.0, "b": 1.0}) < 1.0

    ev = eval_retriever(lambda q, k: ["d1", "d2"],
                        [EvalQuery("q1", ["d1"]), EvalQuery("q2", ["d9"])], k=2)
    assert ev["recall@k"] == 0.5 and ev["mrr"] == 0.5, "eval harness math"

    assert analyze_misses("q", ["d9"], {"d1"}, {"d9": "stale"}), "causes listed"
    print("[OK] 10-retrieval-quality: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Recall@k: did we find what was relevant?")
        print("2. MRR: how high is the first good answer?")
        print("3. NDCG: graded relevance, normalized; then analyze failures.")
        _verify()
