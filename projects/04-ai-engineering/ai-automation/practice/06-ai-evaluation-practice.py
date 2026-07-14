"""
Practice Problems — Module 06: AI Evaluation (NO SOLUTIONS)
============================================================
Solve these yourself! No hints, no solutions.

Run: python 06-ai-evaluation-practice.py
Select a problem number to see the description.

Categories:
  EASY (20 XP):   Problems 1-5
  MEDIUM (50 XP): Problems 6-10
  HARD (100 XP):  Problems 11-15

Prerequisites:
    pip install openai numpy scikit-learn python-dotenv
"""

import numpy as np
from dataclasses import dataclass, field


# ============================================================
# EASY PROBLEMS (20 XP)
# ============================================================

# Problem 1: Precision Calculator
# Write a function that computes precision: tp / (tp + fp)
# Handle the edge case where tp + fp = 0 (return 0.0).
def problem_01():
    pass  # Write your code here


# Problem 2: Recall Calculator
# Write a function that computes recall: tp / (tp + fn)
# Handle the edge case where tp + fn = 0 (return 0.0).
def problem_02():
    pass  # Write your code here


# Problem 3: F1 Score
# Write a function that computes F1 score: 2 * (precision * recall) / (precision + recall)
# Handle edge case where precision + recall = 0 (return 0.0).
def problem_03():
    pass  # Write your code here


# Problem 4: Accuracy Calculator
# Write a function that computes accuracy: (correct predictions) / (total predictions)
# Takes two lists: predicted and actual. Return the float accuracy.
def problem_04():
    pass  # Write your code here


# Problem 5: Confusion Matrix Builder
# Write a function that builds a confusion matrix from predicted and actual labels.
# Labels are strings. Return a dict: {(actual, predicted): count}
# Example: confusion_matrix(["a","b","a"], ["a","a","a"]) → {("a","a"): 2, ("b","a"): 1}
def problem_05():
    pass  # Write your code here


# ============================================================
# MEDIUM PROBLEMS (50 XP)
# ============================================================

# Problem 6: Precision@K
# Write a function that computes Precision@K:
# - Takes retrieved list (ordered by relevance) and a set of relevant items
# - Returns fraction of top-K that are relevant
# Example: precision_at_k(["a","b","c","d"], {"a","c"}, k=3) → 2/3
def problem_06():
    pass  # Write your code here


# Problem 7: Mean Reciprocal Rank (MRR)
# Write a function that computes MRR:
# - Takes a list of retrieved items and a set of relevant items
# - MRR = 1/rank_of_first_relevant
# - If no relevant item found, MRR = 0
# Example: MRR(["b","a","c"], {"a"}) → 0.5 (first relevant at rank 2)
def problem_07():
    pass  # Write your code here


# Problem 8: NDCG@K
# Write a function that computes Normalized Discounted Cumulative Gain at K:
# - DCG@K = sum(rel_i / log2(i+2)) for i in 0..K-1
# - IDCG@K = DCG of ideal ranking
# - NDCG = DCG / IDCG
# Assume binary relevance (1 if relevant, 0 otherwise).
def problem_08():
    pass  # Write your code here


# Problem 9: LLM-as-Judge Scorer
# Write a function that uses an LLM to score a generated answer:
# - Takes the question, generated answer, and reference answer
# - Prompts the LLM: "Rate 1-5 for: relevance, accuracy, completeness"
# - Parses the LLM response to extract scores
# - Returns {"relevance": int, "accuracy": int, "completeness": int, "avg": float}
def problem_09():
    pass  # Write your code here


# Problem 10: Prompt Regression Tester
# Write a function that tests if a prompt change causes regressions:
# - Takes old_prompt, new_prompt, and a list of test_cases
# - Each test_case: {"input": str, "expected_output": str}
# - Runs each test through both prompts
# - Compares outputs using similarity
# - Returns report: {passed, failed, regressions: list}
def problem_10():
    pass  # Write your code here


# ============================================================
# HARD PROBLEMS (100 XP)
# ============================================================

# Problem 11: Faithfulness Evaluator
# Write a FaithfulnessEvaluator class that:
# - Takes a generated answer and source context
# - Splits the answer into atomic claims
# - For each claim, checks if it's supported by the context
# - Computes faithfulness = supported_claims / total_claims
# - Returns detailed report with claim-by-claim analysis
class FaithfulnessEvaluator:
    def __init__(self):
        pass  # Write your code here

    def evaluate(self, answer: str, context: list[str]) -> dict:
        pass  # Write your code here


# Problem 12: Evaluation Dataset Builder
# Write an EvalDatasetBuilder class that:
# - Takes a list of source documents
# - Generates test cases using LLM: question, expected_answer, relevant_docs
# - Validates each test case (answer matches question?)
# - Deduplicates similar test cases
# - Exports to JSONL format
class EvalDatasetBuilder:
    def __init__(self):
        pass  # Write your code here

    def generate(self, documents: list[str], n_questions: int = 10):
        pass  # Write your code here

    def validate(self, test_cases: list[dict]) -> list[dict]:
        pass  # Write your code here

    def export(self, test_cases: list[dict], path: str):
        pass  # Write your code here


# Problem 13: Automated Evaluation Pipeline
# Write an EvalPipeline class that:
# - Takes a RAG system (retrieval + generation functions) and test dataset
# - Runs all test cases
# - Computes retrieval metrics (precision@k, recall@k, MRR, NDCG)
# - Computes generation metrics (faithfulness, relevance, correctness)
# - Aggregates results with confidence intervals
# - Generates a summary report
class EvalPipeline:
    def __init__(self, retrieval_fn, generation_fn):
        pass  # Write your code here

    def run(self, test_cases: list[dict]) -> dict:
        pass  # Write your code here

    def aggregate(self, results: list[dict]) -> dict:
        pass  # Write your code here

    def confidence_interval(self, values: list[float], confidence: float = 0.95):
        pass  # Write your code here


# Problem 14: A/B Comparison Engine
# Write an ABComparison class that:
# - Takes two systems (A and B) and a test dataset
# - Runs both systems on each test case
# - Computes win/tie/loss counts
# - Uses paired bootstrap test for statistical significance
# - Reports: win_rate_A, win_rate_B, p_value, significant (p < 0.05)
class ABComparison:
    def __init__(self, system_a_fn, system_b_fn):
        pass  # Write your code here

    def compare(self, test_cases: list[dict], n_bootstrap: int = 1000) -> dict:
        pass  # Write your code here


# Problem 15: Evaluation Dashboard Data
# Write a DashboardData class that:
# - Aggregates evaluation results over time
# - Stores historical runs with timestamps
# - Computes trends (improving/declining/stable)
# - Detects anomalies (sudden drops in metrics)
# - Generates data for visualization (time series, distributions)
# - Exports to JSON for frontend consumption
class DashboardData:
    def __init__(self):
        pass  # Write your code here

    def add_run(self, run_id: str, metrics: dict):
        pass  # Write your code here

    def get_trends(self, metric_name: str, window: int = 10) -> dict:
        pass  # Write your code here

    def detect_anomalies(self, metric_name: str, threshold: float = 2.0) -> list[dict]:
        pass  # Write your code here

    def export_for_dashboard(self) -> dict:
        pass  # Write your code here


# ============================================================
# MAIN — Run to see problem descriptions
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Module 06: AI Evaluation — Practice Problems")
    print("=" * 60)
    print()

    problems = {
        1: ("Precision Calculator", "Easy", 20),
        2: ("Recall Calculator", "Easy", 20),
        3: ("F1 Score", "Easy", 20),
        4: ("Accuracy Calculator", "Easy", 20),
        5: ("Confusion Matrix Builder", "Easy", 20),
        6: ("Precision@K", "Medium", 50),
        7: ("Mean Reciprocal Rank (MRR)", "Medium", 50),
        8: ("NDCG@K", "Medium", 50),
        9: ("LLM-as-Judge Scorer", "Medium", 50),
        10: ("Prompt Regression Tester", "Medium", 50),
        11: ("Faithfulness Evaluator", "Hard", 100),
        12: ("Evaluation Dataset Builder", "Hard", 100),
        13: ("Automated Evaluation Pipeline", "Hard", 100),
        14: ("A/B Comparison Engine", "Hard", 100),
        15: ("Evaluation Dashboard Data", "Hard", 100),
    }

    total_xp = sum(p[2] for p in problems.values())
    print(f"Total Problems: {len(problems)}")
    print(f"Total XP: {total_xp}")
    print()

    for num, (name, diff, xp) in problems.items():
        print(f"  [{num:2d}] {name:<40} {diff:<8} +{xp} XP")

    print()
    print("Select a problem number to see its full description.")
    print("Solve each function by replacing 'pass' with your implementation.")
    print("No solutions are provided — figure it out yourself!")
    print("=" * 60)
