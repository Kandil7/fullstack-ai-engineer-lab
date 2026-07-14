"""
=============================================================
Exercise 08: Agent Evaluation
=============================================================

Topic Overview:
Evaluating AI agents is critical for understanding their
performance, reliability, and areas for improvement. This
exercise covers:

1. Task Completion Metrics - Measuring success rates
2. Latency Measurement - Tracking response times
3. Cost Tracking - Monitoring API usage and costs
4. Quality Assessment - Evaluating output quality
5. A/B Testing Agents - Comparing different configurations

Key Concepts:
- Multi-dimensional evaluation provides holistic view
- Latency impacts user experience significantly
- Cost tracking enables budget management
- Quality metrics detect hallucinations and errors
- A/B testing validates improvements scientifically

Prerequisites:
- Understanding of LLM integration
- Familiarity with statistical concepts
=============================================================
"""

import asyncio
import json
import time
import uuid
import random
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from collections import defaultdict
from statistics import mean, stdev, median


# ============================================================
# Core Data Structures
# ============================================================

class MetricType(Enum):
    """Types of metrics for agent evaluation."""
    LATENCY = "latency"
    COST = "cost"
    QUALITY = "quality"
    THROUGHPUT = "throughput"
    SUCCESS_RATE = "success_rate"
    TOKEN_USAGE = "token_usage"


class QualityDimension(Enum):
    """Dimensions for quality assessment."""
    ACCURACY = "accuracy"
    RELEVANCE = "relevance"
    COMPLETENESS = "completeness"
    COHERENCE = "coherence"
    SAFETY = "safety"
    HELPFULNESS = "helpfulness"


@dataclass
class EvaluationResult:
    """Result of a single evaluation run."""
    evaluation_id: str
    agent_id: str
    task_id: str
    success: bool
    latency_ms: float
    token_usage: Dict[str, int]
    cost_usd: float
    quality_scores: Dict[str, float]
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class EvaluationSummary:
    """Aggregated evaluation metrics."""
    agent_id: str
    total_evaluations: int
    success_rate: float
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    total_cost_usd: float
    avg_cost_per_eval: float
    total_tokens: int
    avg_tokens_per_eval: float
    quality_metrics: Dict[str, float]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ABTestResult:
    """Result of an A/B test comparison."""
    test_id: str
    variant_a: str
    variant_b: str
    sample_size_a: int
    sample_size_b: int
    metric_name: str
    mean_a: float
    mean_b: float
    p_value: float
    significant: bool
    confidence_level: float
    recommendation: str


# ============================================================
# Example 1: Task Completion Metrics
# ============================================================

class TaskCompletionEvaluator:
    """
    Evaluates task completion rates and success metrics.
    
    Metrics tracked:
    - Success rate (tasks completed successfully)
    - Failure rate (tasks that failed)
    - Partial completion rate
    - Retry rate
    - First-attempt success rate
    """

    def __init__(self):
        self.results: List[EvaluationResult] = []
        self.task_categories: Dict[str, List[str]] = defaultdict(list)

    def record_result(self, result: EvaluationResult) -> None:
        """Record an evaluation result."""
        self.results.append(result)
        category = result.metadata.get("category", "general")
        self.task_categories[category].append(result.evaluation_id)

    def calculate_success_rate(
        self,
        agent_id: Optional[str] = None,
        category: Optional[str] = None
    ) -> float:
        """Calculate success rate with optional filters."""
        filtered = self._filter_results(agent_id, category)
        if not filtered:
            return 0.0

        successes = sum(1 for r in filtered if r.success)
        return successes / len(filtered)

    def calculate_failure_analysis(
        self,
        agent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze failure patterns."""
        filtered = self._filter_results(agent_id)
        failures = [r for r in filtered if not r.success]

        error_types = defaultdict(int)
        for f in failures:
            if f.error:
                error_type = f.error.split(":")[0] if ":" in f.error else "unknown"
                error_types[error_type] += 1

        return {
            "total_failures": len(failures),
            "failure_rate": len(failures) / len(filtered) if filtered else 0,
            "error_distribution": dict(error_types),
            "most_common_error": max(error_types.items(), key=lambda x: x[1])[0]
                                  if error_types else None
        }

    def get_retry_rate(self, agent_id: Optional[str] = None) -> float:
        """Calculate retry rate (tasks attempted more than once)."""
        filtered = self._filter_results(agent_id)
        task_attempts = defaultdict(int)
        for r in filtered:
            task_attempts[r.task_id] += 1

        retried = sum(1 for attempts in task_attempts.values() if attempts > 1)
        return retried / len(task_attempts) if task_attempts else 0

    def get_first_attempt_success_rate(
        self,
        agent_id: Optional[str] = None
    ) -> float:
        """Calculate first-attempt success rate."""
        filtered = self._filter_results(agent_id)
        task_first_attempt = {}
        for r in sorted(filtered, key=lambda x: x.timestamp):
            if r.task_id not in task_first_attempt:
                task_first_attempt[r.task_id] = r.success

        if not task_first_attempt:
            return 0.0
        return sum(task_first_attempt.values()) / len(task_first_attempt)

    def _filter_results(
        self,
        agent_id: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[EvaluationResult]:
        """Filter results by agent and/or category."""
        filtered = self.results
        if agent_id:
            filtered = [r for r in filtered if r.agent_id == agent_id]
        if category:
            filtered = [r for r in filtered
                       if r.metadata.get("category") == category]
        return filtered

    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive task completion report."""
        return {
            "total_evaluations": len(self.results),
            "overall_success_rate": self.calculate_success_rate(),
            "first_attempt_success_rate": self.get_first_attempt_success_rate(),
            "failure_analysis": self.calculate_failure_analysis(),
            "by_category": {
                cat: self.calculate_success_rate(category=cat)
                for cat in self.task_categories
            }
        }


# ============================================================
# Example 2: Latency Measurement
# ============================================================

class LatencyTracker:
    """
    Tracks and analyzes latency metrics.
    
    Provides:
    - Percentile calculations (p50, p95, p99)
    - Latency distribution analysis
    - Trend detection
    - Anomaly detection
    """

    def __init__(self, window_size: int = 100):
        self.latencies: List[float] = []
        self.window_size = window_size
        self.timestamps: List[datetime] = []
        self._sliding_window: List[float] = []

    def record(self, latency_ms: float) -> None:
        """Record a latency measurement."""
        self.latencies.append(latency_ms)
        self.timestamps.append(datetime.now())

        self._sliding_window.append(latency_ms)
        if len(self._sliding_window) > self.window_size:
            self._sliding_window.pop(0)

    def get_percentiles(self) -> Dict[str, float]:
        """Calculate latency percentiles."""
        if not self.latencies:
            return {}

        sorted_latencies = sorted(self.latencies)
        n = len(sorted_latencies)

        return {
            "p50": sorted_latencies[int(n * 0.5)],
            "p75": sorted_latencies[int(n * 0.75)],
            "p90": sorted_latencies[int(n * 0.90)],
            "p95": sorted_latencies[int(n * 0.95)],
            "p99": sorted_latencies[int(n * 0.99)],
            "min": sorted_latencies[0],
            "max": sorted_latencies[-1],
            "mean": mean(sorted_latencies),
            "median": median(sorted_latencies)
        }

    def get_statistics(self) -> Dict[str, float]:
        """Get statistical summary of latencies."""
        if not self.latencies:
            return {}

        return {
            "count": len(self.latencies),
            "mean": mean(self.latencies),
            "std_dev": stdev(self.latencies) if len(self.latencies) > 1 else 0,
            "min": min(self.latencies),
            "max": max(self.latencies),
            "range": max(self.latencies) - min(self.latencies)
        }

    def detect_anomalies(
        self,
        threshold: float = 2.0
    ) -> List[Tuple[int, float]]:
        """
        Detect latency anomalies using Z-score method.
        
        Returns list of (index, latency) tuples for anomalies.
        """
        if len(self.latencies) < 10:
            return []

        mean_lat = mean(self.latencies)
        std_lat = stdev(self.latencies)

        if std_lat == 0:
            return []

        anomalies = []
        for i, latency in enumerate(self.latencies):
            z_score = (latency - mean_lat) / std_lat
            if abs(z_score) > threshold:
                anomalies.append((i, latency))

        return anomalies

    def get_trend(self, window: int = 10) -> Dict[str, Any]:
        """
        Analyze latency trend over time.
        
        Returns trend direction and rate of change.
        """
        if len(self.latencies) < window * 2:
            return {"direction": "insufficient_data"}

        recent = self.latencies[-window:]
        previous = self.latencies[-window*2:-window]

        recent_mean = mean(recent)
        previous_mean = mean(previous)

        change = recent_mean - previous_mean
        change_pct = (change / previous_mean * 100) if previous_mean > 0 else 0

        if change_pct > 5:
            direction = "degrading"
        elif change_pct < -5:
            direction = "improving"
        else:
            direction = "stable"

        return {
            "direction": direction,
            "recent_mean": recent_mean,
            "previous_mean": previous_mean,
            "change_ms": change,
            "change_percent": change_pct
        }

    def get_sliding_window_stats(self) -> Dict[str, float]:
        """Get statistics for the current sliding window."""
        if not self._sliding_window:
            return {}

        return {
            "window_size": len(self._sliding_window),
            "mean": mean(self._sliding_window),
            "min": min(self._sliding_window),
            "max": max(self._sliding_window)
        }


# ============================================================
# Example 3: Cost Tracking
# ============================================================

class CostTracker:
    """
    Tracks and manages API costs for agent operations.
    
    Features:
    - Token-level cost tracking
    - Budget management
    - Cost forecasting
    - Model cost comparison
    """

    # Model pricing (per 1K tokens)
    MODEL_PRICING = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
    }

    def __init__(self, budget_limit: float = 100.0):
        self.budget_limit = budget_limit
        self.total_cost = 0.0
        self.cost_history: List[Dict] = []
        self.daily_costs: Dict[str, float] = defaultdict(float)
        self.model_costs: Dict[str, float] = defaultdict(float)

    def calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost for a model invocation."""
        pricing = self.MODEL_PRICING.get(model, {"input": 0.01, "output": 0.03})

        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]

        return input_cost + output_cost

    def record_usage(
        self,
        agent_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        task_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Record API usage and calculate cost."""
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        self.total_cost += cost

        today = datetime.now().strftime("%Y-%m-%d")
        self.daily_costs[today] += cost
        self.model_costs[model] += cost

        record = {
            "record_id": str(uuid.uuid4())[:8],
            "agent_id": agent_id,
            "task_id": task_id,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost,
            "total_cost_usd": self.total_cost,
            "budget_remaining": self.budget_limit - self.total_cost,
            "timestamp": datetime.now().isoformat()
        }
        self.cost_history.append(record)

        # Check budget
        if self.total_cost > self.budget_limit * 0.9:
            record["warning"] = "Approaching budget limit"

        if self.total_cost > self.budget_limit:
            record["error"] = "Budget exceeded"

        return record

    def get_budget_status(self) -> Dict[str, Any]:
        """Get current budget status."""
        return {
            "budget_limit": self.budget_limit,
            "total_spent": self.total_cost,
            "remaining": self.budget_limit - self.total_cost,
            "percent_used": (self.total_cost / self.budget_limit * 100)
                           if self.budget_limit > 0 else 0,
            "is_over_budget": self.total_cost > self.budget_limit
        }

    def get_cost_breakdown(self) -> Dict[str, Any]:
        """Get detailed cost breakdown."""
        return {
            "by_model": dict(self.model_costs),
            "by_day": dict(self.daily_costs),
            "average_per_request": self.total_cost / len(self.cost_history)
                                   if self.cost_history else 0,
            "total_requests": len(self.cost_history)
        }

    def forecast_daily_cost(
        self,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """Forecast costs for the next N days."""
        if not self.daily_costs:
            return []

        recent_costs = list(self.daily_costs.values())[-7:]
        avg_daily = mean(recent_costs) if recent_costs else 0

        forecasts = []
        for i in range(1, days + 1):
            future_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            forecasts.append({
                "date": future_date,
                "forecasted_cost": avg_daily,
                "confidence": max(0.5, 1 - (i * 0.1))
            })

        return forecasts

    def suggest_model(
        self,
        task_complexity: str
    ) -> Tuple[str, float]:
        """Suggest the most cost-effective model for a task."""
        suggestions = {
            "simple": ("gpt-3.5-turbo", 0.002),
            "moderate": ("claude-3-sonnet", 0.018),
            "complex": ("gpt-4-turbo", 0.04),
            "critical": ("gpt-4", 0.09)
        }
        return suggestions.get(task_complexity, ("gpt-3.5-turbo", 0.002))


# ============================================================
# Example 4: Quality Assessment
# ============================================================

class QualityAssessor:
    """
    Assesses the quality of agent outputs across multiple dimensions.
    
    Dimensions:
    - Accuracy: Factual correctness
    - Relevance: Topic appropriateness
    - Completeness: Coverage of requirements
    - Coherence: Logical flow and consistency
    - Safety: Absence of harmful content
    - Helpfulness: User value
    """

    def __init__(self):
        self.assessments: List[Dict] = []
        self.rubrics: Dict[str, Dict] = {}
        self._setup_default_rubrics()

    def _setup_default_rubrics(self) -> None:
        """Set up default quality rubrics."""
        self.rubrics = {
            QualityDimension.ACCURACY.value: {
                "weights": {"factual_correctness": 0.4, "source_quality": 0.3,
                           "citation_accuracy": 0.3},
                "threshold": 0.7
            },
            QualityDimension.RELEVANCE.value: {
                "weights": {"topic_match": 0.5, "context_appropriateness": 0.3,
                           "user_intent": 0.2},
                "threshold": 0.6
            },
            QualityDimension.COMPLETENESS.value: {
                "weights": {"requirement_coverage": 0.4, "detail_level": 0.3,
                           "edge_cases": 0.3},
                "threshold": 0.7
            },
            QualityDimension.COHERENCE.value: {
                "weights": {"logical_flow": 0.4, "consistency": 0.3,
                           "clarity": 0.3},
                "threshold": 0.6
            },
            QualityDimension.SAFETY.value: {
                "weights": {"harmful_content": 0.5, "bias_detection": 0.25,
                           "privacy_compliance": 0.25},
                "threshold": 0.9
            },
            QualityDimension.HELPFULNESS.value: {
                "weights": {"actionability": 0.4, "clarity": 0.3,
                           "completeness": 0.3},
                "threshold": 0.6
            }
        }

    def assess_quality(
        self,
        agent_id: str,
        task_id: str,
        output: str,
        criteria: Dict[str, float],
        ground_truth: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assess the quality of an agent's output.
        
        Args:
            agent_id: Agent identifier
            task_id: Task identifier
            output: Agent's output to assess
            criteria: Scores for each quality dimension (0-1)
            ground_truth: Optional reference output for comparison
        """
        assessment_id = str(uuid.uuid4())[:8]

        # Calculate dimension scores
        dimension_scores = {}
        for dimension, score in criteria.items():
            dimension_scores[dimension] = min(1.0, max(0.0, score))

        # Calculate weighted overall score
        weights = {dim: 1.0 for dim in dimension_scores}
        total_weight = sum(weights.values())
        overall_score = sum(
            dimension_scores[dim] * weights[dim]
            for dim in dimension_scores
        ) / total_weight if total_weight > 0 else 0

        # Check for safety violations
        safety_score = dimension_scores.get(QualityDimension.SAFETY.value, 1.0)
        has_safety_violation = safety_score < self.rubrics[QualityDimension.SAFETY.value]["threshold"]

        # Simulate hallucination detection
        hallucination_score = dimension_scores.get(QualityDimension.ACCURACY.value, 1.0)
        potential_hallucinations = self._detect_hallucinations(output, ground_truth)

        result = {
            "assessment_id": assessment_id,
            "agent_id": agent_id,
            "task_id": task_id,
            "dimension_scores": dimension_scores,
            "overall_score": overall_score,
            "has_safety_violation": has_safety_violation,
            "potential_hallucinations": potential_hallucinations,
            "hallucination_rate": len(potential_hallucinations) / max(len(output.split()), 1),
            "timestamp": datetime.now().isoformat()
        }

        self.assessments.append(result)
        return result

    def _detect_hallucinations(
        self,
        output: str,
        ground_truth: Optional[str]
    ) -> List[str]:
        """Detect potential hallucinations in output."""
        if not ground_truth:
            return []

        # Simple heuristic: check for claims not in ground truth
        output_claims = set(output.lower().split())
        truth_claims = set(ground_truth.lower().split())

        potential_hallucinations = []
        words = output.split()
        for i in range(len(words) - 2):
            phrase = " ".join(words[i:i+3]).lower()
            if phrase not in ground_truth.lower():
                potential_hallucinations.append(phrase)

        return potential_hallucinations[:5]  # Limit to top 5

    def get_quality_summary(self) -> Dict[str, Any]:
        """Get summary of all quality assessments."""
        if not self.assessments:
            return {}

        avg_scores = defaultdict(list)
        for assessment in self.assessments:
            for dim, score in assessment["dimension_scores"].items():
                avg_scores[dim].append(score)

        return {
            "total_assessments": len(self.assessments),
            "average_scores": {
                dim: mean(scores) for dim, scores in avg_scores.items()
            },
            "safety_violations": sum(
                1 for a in self.assessments if a["has_safety_violation"]
            ),
            "average_hallucination_rate": mean(
                a["hallucination_rate"] for a in self.assessments
            )
        }


# ============================================================
# Example 5: A/B Testing Agents
# ============================================================

class ABTestFramework:
    """
    Framework for A/B testing different agent configurations.
    
    Features:
    - Random traffic splitting
    - Statistical significance testing
    - Result analysis and recommendations
    """

    def __init__(self):
        self.tests: Dict[str, Dict] = {}
        self.results: Dict[str, List[Dict]] = defaultdict(list)

    def create_test(
        self,
        test_id: str,
        variant_a_id: str,
        variant_b_id: str,
        metric_name: str,
        confidence_level: float = 0.95
    ) -> Dict:
        """Create a new A/B test."""
        test = {
            "test_id": test_id,
            "variant_a": variant_a_id,
            "variant_b": variant_b_id,
            "metric_name": metric_name,
            "confidence_level": confidence_level,
            "status": "running",
            "created_at": datetime.now().isoformat(),
            "traffic_split": 0.5  # 50/50 split
        }
        self.tests[test_id] = test
        return test

    def assign_variant(self, test_id: str, user_id: str) -> str:
        """
        Assign a variant to a user using deterministic hashing.
        
        Ensures the same user always sees the same variant.
        """
        test = self.tests.get(test_id)
        if not test:
            raise ValueError(f"Test {test_id} not found")

        # Deterministic assignment based on user ID
        hash_value = hash(user_id) % 100
        if hash_value < test["traffic_split"] * 100:
            return test["variant_a"]
        return test["variant_b"]

    def record_result(
        self,
        test_id: str,
        variant_id: str,
        metric_value: float,
        user_id: str
    ) -> None:
        """Record a test result."""
        self.results[test_id].append({
            "variant": variant_id,
            "metric_value": metric_value,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        })

    def analyze_results(
        self,
        test_id: str
    ) -> ABTestResult:
        """Analyze A/B test results with statistical testing."""
        test = self.tests.get(test_id)
        if not test:
            raise ValueError(f"Test {test_id} not found")

        results = self.results.get(test_id, [])

        # Separate results by variant
        variant_a_values = [
            r["metric_value"] for r in results
            if r["variant"] == test["variant_a"]
        ]
        variant_b_values = [
            r["metric_value"] for r in results
            if r["variant"] == test["variant_b"]
        ]

        if not variant_a_values or not variant_b_values:
            raise ValueError("Insufficient data for analysis")

        # Calculate means
        mean_a = mean(variant_a_values)
        mean_b = mean(variant_b_values)

        # Perform t-test (simplified)
        n_a = len(variant_a_values)
        n_b = len(variant_b_values)
        std_a = stdev(variant_a_values) if n_a > 1 else 0
        std_b = stdev(variant_b_values) if n_b > 1 else 0

        # Calculate t-statistic
        se = math.sqrt((std_a**2 / n_a) + (std_b**2 / n_b))
        if se == 0:
            p_value = 1.0
        else:
            t_stat = abs(mean_a - mean_b) / se
            # Simplified p-value approximation
            p_value = max(0.001, 1 - min(1, t_stat / 3))

        significant = p_value < (1 - test["confidence_level"])

        # Generate recommendation
        if significant:
            if mean_b > mean_a:
                recommendation = (
                    f"Variant B ({test['variant_b']}) performs significantly better. "
                    f"Recommend: Adopt Variant B."
                )
            else:
                recommendation = (
                    f"Variant A ({test['variant_a']}) performs significantly better. "
                    f"Recommend: Keep Variant A."
                )
        else:
            recommendation = (
                "No statistically significant difference detected. "
                "Consider running longer or increasing sample size."
            )

        return ABTestResult(
            test_id=test_id,
            variant_a=test["variant_a"],
            variant_b=test["variant_b"],
            sample_size_a=n_a,
            sample_size_b=n_b,
            metric_name=test["metric_name"],
            mean_a=mean_a,
            mean_b=mean_b,
            p_value=p_value,
            significant=significant,
            confidence_level=test["confidence_level"],
            recommendation=recommendation
        )

    def estimate_sample_size(
        self,
        mde: float = 0.1,  # Minimum detectable effect
        power: float = 0.8,
        alpha: float = 0.05
    ) -> int:
        """Estimate required sample size for desired power."""
        # Simplified sample size calculation
        z_alpha = 1.96  # For alpha = 0.05
        z_beta = 0.84   # For power = 0.8

        n = 2 * ((z_alpha + z_beta) / mde) ** 2
        return math.ceil(n)


# ============================================================
# Example 6: Complete Evaluation System
# ============================================================

class AgentEvaluationSystem:
    """Complete agent evaluation system combining all components."""

    def __init__(self):
        self.task_evaluator = TaskCompletionEvaluator()
        self.latency_tracker = LatencyTracker()
        self.cost_tracker = CostTracker(budget_limit=50.0)
        self.quality_assessor = QualityAssessor()
        self.ab_framework = ABTestFramework()

    async def evaluate_agent(
        self,
        agent_id: str,
        task_id: str,
        task_fn: Callable,
        model: str = "gpt-3.5-turbo"
    ) -> EvaluationResult:
        """Run a complete evaluation of an agent on a task."""
        start_time = time.time()

        try:
            # Execute task
            result = await task_fn()
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)

        latency_ms = (time.time() - start_time) * 1000

        # Simulate token usage
        input_tokens = random.randint(100, 500)
        output_tokens = random.randint(50, 300)

        # Calculate cost
        cost_record = self.cost_tracker.record_usage(
            agent_id, model, input_tokens, output_tokens, task_id
        )

        # Record latency
        self.latency_tracker.record(latency_ms)

        # Create evaluation result
        eval_result = EvaluationResult(
            evaluation_id=str(uuid.uuid4())[:8],
            agent_id=agent_id,
            task_id=task_id,
            success=success,
            latency_ms=latency_ms,
            token_usage={"input": input_tokens, "output": output_tokens},
            cost_usd=cost_record["cost_usd"],
            quality_scores={},
            error=error
        )

        # Record in task evaluator
        self.task_evaluator.record_result(eval_result)

        return eval_result

    def run_ab_test(
        self,
        test_id: str,
        variant_a_fn: Callable,
        variant_b_fn: Callable,
        n_samples: int = 100
    ) -> ABTestResult:
        """Run an A/B test between two agent variants."""
        # Create test
        self.ab_framework.create_test(
            test_id,
            "variant_a",
            "variant_b",
            "success_rate"
        )

        # Simulate test execution
        for i in range(n_samples):
            user_id = f"user_{i}"

            # Variant A
            variant_a = self.ab_framework.assign_variant(test_id, user_id)
            if variant_a == "variant_a":
                metric_a = random.gauss(0.75, 0.1)
            else:
                metric_b = random.gauss(0.80, 0.1)

            self.ab_framework.record_result(test_id, variant_a, metric_a, user_id)

            # Variant B (different user)
            user_id_b = f"user_{i + n_samples}"
            variant_b = self.ab_framework.assign_variant(test_id, user_id_b)
            if variant_b == "variant_b":
                metric_b = random.gauss(0.80, 0.1)
            else:
                metric_a = random.gauss(0.75, 0.1)

            self.ab_framework.record_result(test_id, variant_b, metric_b, user_id_b)

        return self.ab_framework.analyze_results(test_id)

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate a comprehensive evaluation report."""
        return {
            "task_completion": self.task_evaluator.generate_report(),
            "latency": self.latency_tracker.get_percentiles(),
            "cost": self.cost_tracker.get_cost_breakdown(),
            "quality": self.quality_assessor.get_quality_summary(),
            "budget_status": self.cost_tracker.get_budget_status(),
            "generated_at": datetime.now().isoformat()
        }


# ============================================================
# Main Entry Point
# ============================================================

async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("EXERCISE 08: AGENT EVALUATION")
    print("="*60)

    system = AgentEvaluationSystem()

    # Example 1: Task Completion Metrics
    print("\n--- Task Completion Metrics ---")
    for i in range(5):
        success = random.random() > 0.2
        result = EvaluationResult(
            evaluation_id=str(uuid.uuid4())[:8],
            agent_id="agent_1",
            task_id=f"task_{i}",
            success=success,
            latency_ms=random.uniform(100, 500),
            token_usage={"input": 100, "output": 50},
            cost_usd=0.001,
            quality_scores={},
            error=None if success else "Timeout"
        )
        system.task_evaluator.record_result(result)

    report = system.task_evaluator.generate_report()
    print(f"Success Rate: {report['overall_success_rate']:.1%}")

    # Example 2: Latency Measurement
    print("\n--- Latency Measurement ---")
    for _ in range(50):
        latency = random.gauss(200, 50)
        system.latency_tracker.record(latency)

    percentiles = system.latency_tracker.get_percentiles()
    print(f"p50: {percentiles['p50']:.1f}ms")
    print(f"p95: {percentiles['p95']:.1f}ms")
    print(f"p99: {percentiles['p99']:.1f}ms")

    anomalies = system.latency_tracker.detect_anomalies()
    print(f"Anomalies detected: {len(anomalies)}")

    # Example 3: Cost Tracking
    print("\n--- Cost Tracking ---")
    for i in range(10):
        system.cost_tracker.record_usage(
            "agent_1", "gpt-3.5-turbo",
            random.randint(100, 500),
            random.randint(50, 300)
        )

    budget = system.cost_tracker.get_budget_status()
    print(f"Budget Used: ${budget['total_spent']:.4f} / ${budget['budget_limit']}")
    print(f"Remaining: ${budget['remaining']:.4f}")

    # Example 4: Quality Assessment
    print("\n--- Quality Assessment ---")
    assessment = system.quality_assessor.assess_quality(
        agent_id="agent_1",
        task_id="task_1",
        output="The capital of France is Paris.",
        criteria={
            "accuracy": 0.95,
            "relevance": 0.9,
            "completeness": 0.8,
            "coherence": 0.9,
            "safety": 1.0,
            "helpfulness": 0.85
        }
    )
    print(f"Quality Score: {assessment['overall_score']:.2f}")

    # Example 5: A/B Testing
    print("\n--- A/B Testing ---")
    ab_result = system.run_ab_test(
        "test_1",
        lambda: random.gauss(0.75, 0.1),
        lambda: random.gauss(0.80, 0.1),
        n_samples=50
    )
    print(f"Test: {ab_result.variant_a} vs {ab_result.variant_b}")
    print(f"Mean A: {ab_result.mean_a:.3f}, Mean B: {ab_result.mean_b:.3f}")
    print(f"P-value: {ab_result.p_value:.4f}")
    print(f"Significant: {ab_result.significant}")
    print(f"Recommendation: {ab_result.recommendation}")

    # Comprehensive Report
    print("\n--- Comprehensive Report ---")
    full_report = system.generate_comprehensive_report()
    print(json.dumps(full_report, indent=2, default=str))

    print("\n" + "="*60)
    print("EXERCISE COMPLETE")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
