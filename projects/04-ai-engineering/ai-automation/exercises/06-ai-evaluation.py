"""
Exercise 06: AI Evaluation
===========================
Master AI system evaluation: RAG metrics, LLM-as-judge, prompt regression
testing, agent evaluation, and comprehensive evaluation reports.

Prerequisites:
    pip install openai numpy pandas scikit-learn ragas datasets jsonlines

Environment Variables (.env):
    OPENAI_API_KEY=sk-...
"""

import os
import json
import time
import hashlib
import numpy as np
from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime
from collections import defaultdict


# ---------------------------------------------------------------------------
# 1. RAG Evaluation Metrics
# ---------------------------------------------------------------------------

@dataclass
class RetrievalResult:
    """A single retrieval result with context."""
    query: str
    retrieved_docs: list[str]
    relevant_doc_ids: list[int]
    all_doc_ids: list[int]


@dataclass
class GenerationResult:
    """A generation result with reference answer."""
    query: str
    generated_answer: str
    reference_answer: str
    context: list[str]


class RAGEvaluator:
    """Comprehensive RAG evaluation metrics."""

    def precision_at_k(self, retrieved: list[str], relevant: set[str], k: int) -> float:
        """What fraction of top-k retrieved docs are relevant?"""
        top_k = retrieved[:k]
        if not top_k:
            return 0.0
        relevant_retrieved = sum(1 for doc in top_k if doc in relevant)
        return relevant_retrieved / len(top_k)

    def recall_at_k(self, retrieved: list[str], relevant: set[str], k: int) -> float:
        """What fraction of relevant docs are in top-k?"""
        if not relevant:
            return 0.0
        top_k = retrieved[:k]
        relevant_retrieved = sum(1 for doc in top_k if doc in relevant)
        return relevant_retrieved / len(relevant)

    def ndcg_at_k(self, retrieved: list[str], relevant: set[str], k: int) -> float:
        """Normalized Discounted Cumulative Gain at k."""
        dcg = 0.0
        for i, doc in enumerate(retrieved[:k]):
            if doc in relevant:
                dcg += 1.0 / np.log2(i + 2)  # i+2 because log2(1) = 0

        # Ideal DCG
        ideal_dcg = sum(1.0 / np.log2(i + 2) for i in range(min(len(relevant), k)))
        return dcg / ideal_dcg if ideal_dcg > 0 else 0.0

    def mrr(self, retrieved: list[str], relevant: set[str]) -> float:
        """Mean Reciprocal Rank - reciprocal rank of first relevant doc."""
        for i, doc in enumerate(retrieved):
            if doc in relevant:
                return 1.0 / (i + 1)
        return 0.0

    def faithfulness_score(self, answer: str, context: list[str]) -> float:
        """How faithful is the answer to the context? (simplified)"""
        if not context:
            return 0.0

        answer_words = set(answer.lower().split())
        context_words = set()
        for ctx in context:
            context_words.update(ctx.lower().split())

        if not answer_words:
            return 0.0

        # Words in answer that are grounded in context
        grounded = answer_words & context_words
        return len(grounded) / len(answer_words)

    def relevance_score(self, answer: str, query: str) -> float:
        """How relevant is the answer to the query? (simplified)"""
        query_words = set(query.lower().split())
        answer_words = set(answer.lower().split())

        if not query_words:
            return 0.0

        overlap = query_words & answer_words
        return len(overlap) / len(query_words)

    def evaluate_rag_pair(self, result: GenerationResult) -> dict[str, float]:
        """Evaluate a single query-answer pair."""
        # Simulate retrieval (in real use, you'd track actual retrieval)
        context_str = " ".join(result.context)
        return {
            "faithfulness": self.faithfulness_score(result.generated_answer, result.context),
            "relevance": self.relevance_score(result.generated_answer, result.query),
            "answer_length": len(result.generated_answer.split()),
            "context_length": sum(len(c.split()) for c in result.context),
        }


def demo_rag_evaluation():
    """Demonstrate RAG evaluation metrics."""
    print("\n" + "=" * 60)
    print("1. RAG EVALUATION METRICS")
    print("=" * 60)

    evaluator = RAGEvaluator()

    # Simulated retrieval results
    retrieved_docs = ["doc_a", "doc_b", "doc_c", "doc_d", "doc_e"]
    relevant_docs = {"doc_a", "doc_c", "doc_f"}

    print("\nRetrieved:", retrieved_docs)
    print("Relevant:", relevant_docs)

    # Calculate metrics
    for k in [1, 3, 5]:
        precision = evaluator.precision_at_k(retrieved_docs, relevant_docs, k)
        recall = evaluator.recall_at_k(retrieved_docs, relevant_docs, k)
        ndcg = evaluator.ndcg_at_k(retrieved_docs, relevant_docs, k)
        print(f"\n@{k}:")
        print(f"  Precision: {precision:.3f}")
        print(f"  Recall:    {recall:.3f}")
        print(f"  NDCG:      {ndcg:.3f}")

    mrr = evaluator.mrr(retrieved_docs, relevant_docs)
    print(f"\nMRR: {mrr:.3f}")

    # Generation evaluation
    gen_result = GenerationResult(
        query="What is machine learning?",
        generated_answer="Machine learning is a subset of AI that enables systems to learn from data.",
        reference_answer="ML is a branch of AI that allows computers to learn without explicit programming.",
        context=[
            "Machine learning is a subset of artificial intelligence.",
            "It enables systems to learn and improve from experience."
        ]
    )

    scores = evaluator.evaluate_rag_pair(gen_result)
    print(f"\nGeneration Scores:")
    for metric, score in scores.items():
        print(f"  {metric}: {score:.3f}")


# ---------------------------------------------------------------------------
# 2. LLM-as-Judge Evaluation
# ---------------------------------------------------------------------------

@dataclass
class JudgementResult:
    """Result from LLM-as-judge evaluation."""
    score: int  # 1-5
    reasoning: str
    criteria: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class LLMJudge:
    """Use LLM to evaluate AI outputs."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.criteria_templates = {
            "relevance": """
                Evaluate how relevant this answer is to the question.
                
                Question: {question}
                Answer: {answer}
                
                Score 1-5:
                1 - Completely irrelevant
                2 - Barely related
                3 - Somewhat relevant
                4 - Mostly relevant
                5 - Completely relevant
                
                Provide your score and brief reasoning.
            """,
            "accuracy": """
                Evaluate the factual accuracy of this answer.
                
                Question: {question}
                Answer: {answer}
                Reference: {reference}
                
                Score 1-5:
                1 - Completely inaccurate
                2 - Mostly inaccurate
                3 - Partially accurate
                4 - Mostly accurate
                5 - Completely accurate
                
                Provide your score and brief reasoning.
            """,
            "completeness": """
                Evaluate how complete this answer is.
                
                Question: {question}
                Answer: {answer}
                
                Score 1-5:
                1 - Missing most information
                2 - Missing significant information
                3 - Covers basic points
                4 - Covers most points
                5 - Comprehensive coverage
                
                Provide your score and brief reasoning.
            """,
            "conciseness": """
                Evaluate the conciseness of this answer.
                
                Question: {question}
                Answer: {answer}
                
                Score 1-5:
                1 - Extremely verbose, mostly filler
                2 - Too verbose with unnecessary details
                3 - Acceptable length
                4 - Well-concise
                5 - Perfectly concise and focused
                
                Provide your score and brief reasoning.
            """,
        }

    def _call_llm(self, prompt: str) -> str:
        """Call LLM for evaluation (simplified)."""
        from openai import OpenAI
        client = OpenAI()

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=200,
        )
        return response.choices[0].message.content

    def judge(self, question: str, answer: str, criteria: str,
              reference: str = None) -> JudgementResult:
        """Evaluate an answer using LLM-as-judge."""
        template = self.criteria_templates.get(criteria, self.criteria_templates["relevance"])

        prompt = template.format(
            question=question,
            answer=answer,
            reference=reference or "N/A"
        )

        try:
            response = self._call_llm(prompt)
            # Parse score from response
            score = 3  # default
            for line in response.split("\n"):
                if line.strip().startswith(("Score:", "Score", "score:")):
                    for word in line.split():
                        if word.isdigit() and 1 <= int(word) <= 5:
                            score = int(word)
                            break

            return JudgementResult(
                score=score,
                reasoning=response,
                criteria=criteria
            )
        except Exception as e:
            return JudgementResult(
                score=3,
                reasoning=f"Error calling LLM: {e}",
                criteria=criteria
            )

    def multi_criteria_judge(self, question: str, answer: str,
                            reference: str = None) -> dict[str, JudgementResult]:
        """Evaluate across multiple criteria."""
        results = {}
        for criteria in ["relevance", "accuracy", "completeness", "conciseness"]:
            results[criteria] = self.judge(question, answer, criteria, reference)
        return results


def demo_llm_judge():
    """Demonstrate LLM-as-judge evaluation."""
    print("\n" + "=" * 60)
    print("2. LLM-AS-JUDGE EVALUATION")
    print("=" * 60)

    judge = LLMJudge()

    question = "What are the benefits of microservices?"
    good_answer = (
        "Microservices offer several benefits: 1) Independent deployment, "
        "2) Technology flexibility, 3) Scalability per service, 4) Fault isolation, "
        "5) Team autonomy. Each service can be developed, deployed, and scaled independently."
    )
    bad_answer = "Microservices are good."

    print(f"\nQuestion: {question}")
    print(f"\nGood Answer: {good_answer}")
    print(f"Bad Answer: {bad_answer}")

    # Note: In real usage, uncomment the judge calls
    # good_judgement = judge.judge(question, good_answer, "relevance")
    # bad_judgement = judge.judge(question, bad_answer, "relevance")

    print("\n[Simulated] Good answer would score: 5/5")
    print("[Simulated] Bad answer would score: 2/5")

    # Show the criteria templates
    print("\nAvailable criteria:")
    for criteria in judge.criteria_templates:
        print(f"  - {criteria}")


# ---------------------------------------------------------------------------
# 3. Prompt Regression Testing
# ---------------------------------------------------------------------------

@dataclass
class PromptTestCase:
    """A test case for prompt evaluation."""
    test_id: str
    prompt_name: str
    input_vars: dict[str, str]
    expected_behavior: str
    min_score: float = 0.7
    tags: list[str] = field(default_factory=list)


@dataclass
class TestResult:
    """Result of a prompt test case."""
    test_id: str
    passed: bool
    actual_output: str
    score: float
    latency_ms: float
    token_count: int
    error: str | None = None


class PromptRegressionTester:
    """Test prompts for regression and quality."""

    def __init__(self):
        self.test_suites: dict[str, list[PromptTestCase]] = defaultdict(list)
        self.results_history: list[dict] = []

    def add_test_case(self, suite_name: str, test_case: PromptTestCase):
        """Add a test case to a suite."""
        self.test_suites[suite_name].append(test_case)

    def _render_prompt(self, template: str, variables: dict[str, str]) -> str:
        """Render a prompt template with variables."""
        result = template
        for key, value in variables.items():
            result = result.replace(f"{{{{{key}}}}}", value)
        return result

    def _evaluate_output(self, output: str, expected_behavior: str) -> float:
        """Evaluate output against expected behavior (simplified)."""
        output_lower = output.lower()
        behavior_lower = expected_behavior.lower()

        # Simple keyword matching (in real use, use LLM judge)
        expected_words = set(behavior_lower.split())
        output_words = set(output_lower.split())

        if not expected_words:
            return 0.5

        overlap = expected_words & output_words
        return min(1.0, len(overlap) / len(expected_words) * 1.5)

    def run_test(self, prompt_template: str, test_case: PromptTestCase) -> TestResult:
        """Run a single test case."""
        try:
            # Render prompt
            rendered = self._render_prompt(prompt_template, test_case.input_vars)

            # Simulate LLM call (in real use, call actual API)
            start_time = time.time()
            # Simulated output based on expected behavior
            output = f"Simulated response for: {rendered[:50]}..."
            latency_ms = (time.time() - start_time) * 1000

            # Evaluate
            score = self._evaluate_output(output, test_case.expected_behavior)

            return TestResult(
                test_id=test_case.test_id,
                passed=score >= test_case.min_score,
                actual_output=output,
                score=score,
                latency_ms=latency_ms,
                token_count=len(output.split()),
            )
        except Exception as e:
            return TestResult(
                test_id=test_case.test_id,
                passed=False,
                actual_output="",
                score=0.0,
                latency_ms=0.0,
                token_count=0,
                error=str(e),
            )

    def run_suite(self, suite_name: str, prompt_template: str) -> list[TestResult]:
        """Run all tests in a suite."""
        results = []
        for test_case in self.test_suites.get(suite_name, []):
            result = self.run_test(prompt_template, test_case)
            results.append(result)

        # Store results
        self.results_history.append({
            "suite": suite_name,
            "timestamp": datetime.now().isoformat(),
            "results": [
                {"id": r.test_id, "passed": r.passed, "score": r.score}
                for r in results
            ]
        })

        return results

    def generate_report(self, suite_name: str, results: list[TestResult]) -> str:
        """Generate a test report."""
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        avg_score = sum(r.score for r in results) / total if total > 0 else 0

        report = [
            f"\n{'=' * 50}",
            f"PROMPT REGRESSION TEST REPORT: {suite_name}",
            f"{'=' * 50}",
            f"Total Tests: {total}",
            f"Passed: {passed}/{total} ({passed/total*100:.1f}%)",
            f"Average Score: {avg_score:.3f}",
            f"\nDetailed Results:",
        ]

        for r in results:
            status = "PASS" if r.passed else "FAIL"
            report.append(f"  [{status}] {r.test_id}: score={r.score:.3f}")

        return "\n".join(report)


def demo_prompt_regression():
    """Demonstrate prompt regression testing."""
    print("\n" + "=" * 60)
    print("3. PROMPT REGRESSION TESTING")
    print("=" * 60)

    tester = PromptRegressionTester()

    # Define test suite
    prompt_template = "You are a helpful assistant. Answer: {question}"

    test_cases = [
        PromptTestCase(
            test_id="TC001",
            prompt_name="qa_prompt",
            input_vars={"question": "What is Python?"},
            expected_behavior="programming language dynamic typed",
            min_score=0.5,
            tags=["basic", "programming"],
        ),
        PromptTestCase(
            test_id="TC002",
            prompt_name="qa_prompt",
            input_vars={"question": "Explain machine learning"},
            expected_behavior="artificial intelligence data learning patterns",
            min_score=0.5,
            tags=["ai", "concepts"],
        ),
        PromptTestCase(
            test_id="TC003",
            prompt_name="qa_prompt",
            input_vars={"question": "What is REST API?"},
            expected_behavior="http endpoints web service",
            min_score=0.5,
            tags=["api", "web"],
        ),
    ]

    # Add test cases
    for tc in test_cases:
        tester.add_test_case("qa_suite", tc)

    # Run tests
    results = tester.run_suite("qa_suite", prompt_template)

    # Generate report
    report = tester.generate_report("qa_suite", results)
    print(report)


# ---------------------------------------------------------------------------
# 4. Agent Evaluation
# ---------------------------------------------------------------------------

@dataclass
class AgentStep:
    """A single step in agent execution."""
    step_id: int
    action: str
    input_text: str
    output_text: str
    tool_used: str | None = None
    success: bool = True
    latency_ms: float = 0.0


@dataclass
class AgentTrajectory:
    """Complete trajectory of agent execution."""
    task_id: str
    query: str
    steps: list[AgentStep]
    final_answer: str
    total_latency_ms: float = 0.0


class AgentEvaluator:
    """Evaluate AI agent performance."""

    def __init__(self):
        self.trajectories: list[AgentTrajectory] = []

    def record_trajectory(self, trajectory: AgentTrajectory):
        """Record an agent trajectory."""
        self.trajectories.append(trajectory)

    def compute_metrics(self, trajectory: AgentTrajectory) -> dict[str, float]:
        """Compute evaluation metrics for a trajectory."""
        steps = trajectory.steps
        if not steps:
            return {"success_rate": 0.0, "efficiency": 0.0}

        # Success rate
        successful_steps = sum(1 for s in steps if s.success)
        success_rate = successful_steps / len(steps)

        # Efficiency (fewer steps = more efficient, normalized)
        efficiency = 1.0 / (1.0 + len(steps) * 0.1)

        # Tool utilization
        tools_used = sum(1 for s in steps if s.tool_used)
        tool_utilization = tools_used / len(steps) if steps else 0.0

        # Error recovery
        error_steps = [i for i, s in enumerate(steps) if not s.success]
        recovery_success = 0.0
        for idx in error_steps:
            if idx + 1 < len(steps) and steps[idx + 1].success:
                recovery_success += 1
        error_recovery = recovery_success / len(error_steps) if error_steps else 1.0

        # Average latency per step
        avg_latency = sum(s.latency_ms for s in steps) / len(steps)

        return {
            "success_rate": success_rate,
            "efficiency": efficiency,
            "tool_utilization": tool_utilization,
            "error_recovery": error_recovery,
            "avg_step_latency_ms": avg_latency,
            "total_steps": len(steps),
        }

    def evaluate_task_completion(self, trajectory: AgentTrajectory,
                                  expected_answer: str) -> dict[str, Any]:
        """Evaluate if the agent completed the task correctly."""
        metrics = self.compute_metrics(trajectory)

        # Simple answer similarity (in real use, use embedding similarity)
        answer_words = set(trajectory.final_answer.lower().split())
        expected_words = set(expected_answer.lower().split())

        if expected_words:
            overlap = answer_words & expected_words
            answer_similarity = len(overlap) / len(expected_words)
        else:
            answer_similarity = 0.0

        return {
            **metrics,
            "answer_similarity": answer_similarity,
            "task_completed": answer_similarity > 0.5 and metrics["success_rate"] > 0.7,
        }

    def aggregate_results(self) -> dict[str, float]:
        """Aggregate metrics across all trajectories."""
        all_metrics = []
        for traj in self.trajectories:
            metrics = self.compute_metrics(traj)
            all_metrics.append(metrics)

        if not all_metrics:
            return {}

        aggregated = {}
        for key in all_metrics[0]:
            values = [m[key] for m in all_metrics if key in m]
            aggregated[f"avg_{key}"] = sum(values) / len(values) if values else 0.0

        return aggregated


def demo_agent_evaluation():
    """Demonstrate agent evaluation."""
    print("\n" + "=" * 60)
    print("4. AGENT EVALUATION")
    print("=" * 60)

    evaluator = AgentEvaluator()

    # Simulate agent execution
    trajectory = AgentTrajectory(
        task_id="task_001",
        query="What is the capital of France?",
        steps=[
            AgentStep(1, "search", "capital of France", "Paris is the capital", "search_tool", True, 150.0),
            AgentStep(2, "verify", "Paris capital France", "Confirmed", None, True, 100.0),
            AgentStep(3, "format", "Paris", "The capital of France is Paris.", None, True, 50.0),
        ],
        final_answer="The capital of France is Paris.",
        total_latency_ms=300.0,
    )

    evaluator.record_trajectory(trajectory)

    # Compute metrics
    metrics = evaluator.compute_metrics(trajectory)
    print("\nAgent Metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.3f}")

    # Evaluate task completion
    evaluation = evaluator.evaluate_task_completion(trajectory, "Paris")
    print(f"\nTask Completion:")
    print(f"  Task Completed: {evaluation['task_completed']}")
    print(f"  Answer Similarity: {evaluation['answer_similarity']:.3f}")


# ---------------------------------------------------------------------------
# 5. Evaluation Reports & Dashboards
# ---------------------------------------------------------------------------

class EvaluationReporter:
    """Generate comprehensive evaluation reports."""

    def __init__(self):
        self.reports: list[dict] = []

    def add_report(self, name: str, metrics: dict[str, Any], details: dict = None):
        """Add an evaluation report."""
        self.reports.append({
            "name": name,
            "metrics": metrics,
            "details": details or {},
            "timestamp": datetime.now().isoformat(),
        })

    def generate_summary(self) -> str:
        """Generate a summary of all reports."""
        if not self.reports:
            return "No reports available."

        lines = [
            "=" * 60,
            "EVALUATION SUMMARY REPORT",
            "=" * 60,
            f"Generated: {datetime.now().isoformat()}",
            f"Total Reports: {len(self.reports)}",
            "",
        ]

        for report in self.reports:
            lines.append(f"\n--- {report['name']} ---")
            for metric, value in report["metrics"].items():
                if isinstance(value, float):
                    lines.append(f"  {metric}: {value:.4f}")
                else:
                    lines.append(f"  {metric}: {value}")

        return "\n".join(lines)

    def compare_models(self, model_results: dict[str, dict[str, float]]) -> str:
        """Compare evaluation results across models."""
        if not model_results:
            return "No model results to compare."

        lines = [
            "=" * 60,
            "MODEL COMPARISON REPORT",
            "=" * 60,
            "",
        ]

        # Get all metrics
        all_metrics = set()
        for metrics in model_results.values():
            all_metrics.update(metrics.keys())

        # Table header
        header = f"{'Metric':<30}"
        for model in model_results:
            header += f" {model:>15}"
        lines.append(header)
        lines.append("-" * len(header))

        # Table rows
        for metric in sorted(all_metrics):
            row = f"{metric:<30}"
            for model, metrics in model_results.items():
                value = metrics.get(metric, 0.0)
                row += f" {value:>15.4f}"
            lines.append(row)

        return "\n".join(lines)

    def export_json(self, filepath: str):
        """Export reports to JSON."""
        with open(filepath, "w") as f:
            json.dump(self.reports, f, indent=2, default=str)
        print(f"Reports exported to {filepath}")


def demo_evaluation_reports():
    """Demonstrate evaluation reporting."""
    print("\n" + "=" * 60)
    print("5. EVALUATION REPORTS")
    print("=" * 60)

    reporter = EvaluationReporter()

    # Add model evaluation reports
    reporter.add_report(
        "GPT-4o Evaluation",
        {
            "accuracy": 0.92,
            "relevance": 0.89,
            "latency_ms": 450.0,
            "cost_per_1k": 0.005,
        },
        {"model": "gpt-4o", "test_size": 100}
    )

    reporter.add_report(
        "Claude Sonnet Evaluation",
        {
            "accuracy": 0.90,
            "relevance": 0.91,
            "latency_ms": 380.0,
            "cost_per_1k": 0.003,
        },
        {"model": "claude-sonnet", "test_size": 100}
    )

    # Generate summary
    summary = reporter.generate_summary()
    print(summary)

    # Model comparison
    comparison = reporter.compare_models({
        "GPT-4o": {"accuracy": 0.92, "relevance": 0.89, "latency_ms": 450.0},
        "Claude Sonnet": {"accuracy": 0.90, "relevance": 0.91, "latency_ms": 380.0},
        "Llama 3.3": {"accuracy": 0.85, "relevance": 0.84, "latency_ms": 200.0},
    })
    print("\n" + comparison)


# ---------------------------------------------------------------------------
# Main: Run All Demos
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("EXERCISE 06: AI EVALUATION")
    print("=" * 60)

    demo_rag_evaluation()
    demo_llm_judge()
    demo_prompt_regression()
    demo_agent_evaluation()
    demo_evaluation_reports()

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS:")
    print("1. RAG evaluation requires precision, recall, NDCG, and faithfulness")
    print("2. LLM-as-judge enables scalable quality assessment")
    print("3. Prompt regression testing prevents quality degradation")
    print("4. Agent evaluation tracks step-level success and efficiency")
    print("5. Evaluation reports enable model comparison and tracking")
    print("=" * 60)
