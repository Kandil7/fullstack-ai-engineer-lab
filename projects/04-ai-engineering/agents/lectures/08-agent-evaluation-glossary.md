# Glossary: Agent Evaluation

> Terms defined in alphabetical order.

---

## Quick Reference Table

| Term | One-Line Definition | See Also |
|------|---------------------|----------|
| Accuracy | Correctness of agent outputs | Correctness |
| Baseline | Reference point for comparison | Benchmark |
| Benchmark | Standardized test for comparison | Evaluation |
| Coverage | % of scenarios tested | Test Suite |
| Debugging | Identifying and fixing agent issues | Troubleshooting |
| Evaluation | Measuring agent performance | Assessment |
| Ground Truth | Known correct answers | Expected Output |
| Latency | Time to complete a task | Performance |
| Metric | Quantitative measure | KPI |
| Regression | Performance degradation | Testing |
| Success Rate | % of tasks completed correctly | Accuracy |
| Test Case | Specific input/output pair | Unit Test |
| Test Suite | Collection of test cases | Test Set |
| Throughput | Tasks completed per unit time | Performance |
| Token Usage | Number of LLM tokens consumed | Cost |

---

## A

### Accuracy

**Definition:** The degree to which an agent's outputs match the expected or correct results. Can be measured as exact match, fuzzy match, or semantic similarity.

**Example:**
```python
def calculate_accuracy(results: list) -> float:
    """Calculate accuracy from test results."""
    if not results:
        return 0.0
    
    correct = sum(1 for r in results if r.get("correct", False))
    return correct / len(results)

def fuzzy_match(actual: str, expected: str, threshold: float = 0.8) -> bool:
    """Check if outputs are similar enough."""
    words_actual = set(actual.lower().split())
    words_expected = set(expected.lower().split())
    
    if not words_expected:
        return False
    
    intersection = len(words_actual & words_expected)
    union = len(words_actual | words_expected)
    
    similarity = intersection / union if union > 0 else 0
    return similarity >= threshold

# Usage
results = [
    {"actual": "Paris", "expected": "Paris", "correct": True},
    {"actual": "The capital is Paris", "expected": "Paris", "correct": True},
    {"actual": "London", "expected": "Paris", "correct": False}
]

accuracy = calculate_accuracy(results)
print(f"Accuracy: {accuracy:.1%}")  # 66.7%
```

**Related terms:** Precision, Recall, Correctness

---

## B

### Baseline

**Definition:** A reference point against which agent performance is compared. Baselines can be simple heuristics, previous agent versions, or human performance.

**Example:**
```python
class BaselineComparison:
    """Compare agent against baselines."""
    
    def __init__(self):
        self.baselines = {}
        self.results = {}
    
    def add_baseline(self, name: str, performance: dict):
        """Add a baseline for comparison."""
        self.baselines[name] = performance
    
    def add_agent_result(self, name: str, performance: dict):
        """Add agent results."""
        self.results[name] = performance
    
    def compare(self) -> dict:
        """Compare all agents against baselines."""
        comparison = {}
        
        for agent_name, agent_perf in self.results.items():
            comparison[agent_name] = {}
            
            for baseline_name, baseline_perf in self.baselines.items():
                comparison[agent_name][baseline_name] = {
                    metric: {
                        "agent": agent_perf.get(metric, 0),
                        "baseline": baseline_perf.get(metric, 0),
                        "improvement": (
                            (agent_perf.get(metric, 0) - baseline_perf.get(metric, 0))
                            / baseline_perf.get(metric, 1) * 100
                        )
                    }
                    for metric in set(agent_perf.keys()) | set(baseline_perf.keys())
                }
        
        return comparison

# Usage
comparator = BaselineComparison()
comparator.add_baseline("random", {"accuracy": 0.25, "latency": 0.1})
comparator.add_baseline("previous_version", {"accuracy": 0.75, "latency": 0.5})
comparator.add_agent_result("new_agent", {"accuracy": 0.85, "latency": 0.3})

results = comparator.compare()
```

**Related terms:** Benchmark, Reference, Comparison

---

### Benchmark

**Definition:** A standardized test or set of tests used to evaluate and compare agent performance. Benchmarks provide consistent, reproducible measurements.

**Example:**
```python
from typing import List, Dict
import json
import time

class BenchmarkSuite:
    """Standardized benchmark suite for agent evaluation."""
    
    def __init__(self, name: str):
        self.name = name
        self.tasks: List[Dict] = []
        self.results: Dict[str, List[Dict]] = {}
    
    def add_task(self, task_id: str, input_data: Any,
                expected: Any, category: str = "general"):
        """Add a benchmark task."""
        self.tasks.append({
            "id": task_id,
            "input": input_data,
            "expected": expected,
            "category": category
        })
    
    def run_benchmark(self, agent_name: str, 
                     agent_func: Callable) -> Dict:
        """Run benchmark on an agent."""
        results = []
        
        for task in self.tasks:
            start_time = time.time()
            
            try:
                actual = agent_func(task["input"])
                success = actual == task["expected"]
            except Exception as e:
                actual = None
                success = False
            
            execution_time = time.time() - start_time
            
            results.append({
                "task_id": task["id"],
                "category": task["category"],
                "success": success,
                "execution_time": execution_time,
                "actual": actual
            })
        
        self.results[agent_name] = results
        
        return self._compute_metrics(results)
    
    def _compute_metrics(self, results: List[Dict]) -> Dict:
        """Compute aggregate metrics."""
        total = len(results)
        successes = sum(1 for r in results if r["success"])
        
        times = [r["execution_time"] for r in results]
        
        return {
            "accuracy": successes / total if total > 0 else 0,
            "total_tasks": total,
            "avg_time": sum(times) / len(times) if times else 0,
            "max_time": max(times) if times else 0
        }
    
    def compare_results(self, agent_names: List[str]) -> Dict:
        """Compare results from multiple agents."""
        comparison = {}
        
        for agent in agent_names:
            if agent in self.results:
                comparison[agent] = self._compute_metrics(self.results[agent])
        
        return comparison
    
    def export_results(self, filepath: str):
        """Export results to JSON."""
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)

# Usage
benchmark = BenchmarkSuite("QA Benchmark")

benchmark.add_task("q1", "What is 2+2?", "4", "math")
benchmark.add_task("q2", "Capital of France?", "Paris", "geography")
benchmark.add_task("q3", "Color of sky?", "Blue", "常识")

# Run benchmark
metrics = benchmark.run_benchmark("agent_v1", my_agent)
print(f"Accuracy: {metrics['accuracy']:.1%}")
print(f"Avg Time: {metrics['avg_time']:.3f}s")
```

**Related terms:** Test Suite, Standard, Evaluation

---

## G

### Ground Truth

**Definition:** The known correct answer or expected behavior for a test case. Used to verify agent outputs are correct.

**Example:**
```python
from typing import Any

class GroundTruthEvaluator:
    """Evaluates agent outputs against ground truth."""
    
    def __init__(self):
        self.ground_truth = {}
    
    def add_ground_truth(self, task_id: str, expected: Any,
                        validation_fn: Callable = None):
        """Add ground truth for a task."""
        self.ground_truth[task_id] = {
            "expected": expected,
            "validator": validation_fn
        }
    
    def evaluate(self, task_id: str, actual: Any) -> Dict:
        """Evaluate actual against ground truth."""
        if task_id not in self.ground_truth:
            return {"error": "No ground truth for task"}
        
        gt = self.ground_truth[task_id]
        
        # Use custom validator if provided
        if gt["validator"]:
            is_correct = gt["validator"](actual, gt["expected"])
        else:
            # Default comparison
            is_correct = actual == gt["expected"]
        
        return {
            "task_id": task_id,
            "correct": is_correct,
            "expected": gt["expected"],
            "actual": actual
        }
    
    def batch_evaluate(self, results: Dict[str, Any]) -> Dict:
        """Evaluate multiple results."""
        evaluations = {}
        
        for task_id, actual in results.items():
            evaluations[task_id] = self.evaluate(task_id, actual)
        
        # Summary
        total = len(evaluations)
        correct = sum(1 for e in evaluations.values() if e.get("correct"))
        
        return {
            "evaluations": evaluations,
            "summary": {
                "total": total,
                "correct": correct,
                "accuracy": correct / total if total > 0 else 0
            }
        }

# Usage
evaluator = GroundTruthEvaluator()
evaluator.add_ground_truth("q1", "4")
evaluator.add_ground_truth("q2", "Paris", 
                          validator=lambda a, e: e.lower() in a.lower())

results = evaluator.batch_evaluate({
    "q1": "4",
    "q2": "The capital of France is Paris"
})
print(f"Accuracy: {results['summary']['accuracy']:.1%}")
```

**Related terms:** Expected Output, Correct Answer

---

## L

### Latency

**Definition:** The time it takes for an agent to process an input and produce an output. Lower latency generally means better user experience.

**Example:**
```python
import time
from typing import List
import statistics

class LatencyTracker:
    """Track and analyze agent latency."""
    
    def __init__(self):
        self.measurements: List[float] = []
        self.start_time = None
    
    def start(self):
        """Start timing."""
        self.start_time = time.time()
    
    def stop(self) -> float:
        """Stop timing and record measurement."""
        if self.start_time is None:
            return 0.0
        
        duration = time.time() - self.start_time
        self.measurements.append(duration)
        self.start_time = None
        
        return duration
    
    def get_statistics(self) -> Dict:
        """Get latency statistics."""
        if not self.measurements:
            return {"count": 0}
        
        return {
            "count": len(self.measurements),
            "mean": statistics.mean(self.measurements),
            "median": statistics.median(self.measurements),
            "min": min(self.measurements),
            "max": max(self.measurements),
            "stddev": statistics.stdev(self.measurements) if len(self.measurements) > 1 else 0,
            "p95": sorted(self.measurements)[int(len(self.measurements) * 0.95)],
            "p99": sorted(self.measurements)[int(len(self.measurements) * 0.99)]
        }
    
    def print_report(self):
        """Print latency report."""
        stats = self.get_statistics()
        print("=== Latency Report ===")
        print(f"Count: {stats['count']}")
        print(f"Mean: {stats.get('mean', 0):.3f}s")
        print(f"Median: {stats.get('median', 0):.3f}s")
        print(f"Min: {stats.get('min', 0):.3f}s")
        print(f"Max: {stats.get('max', 0):.3f}s")
        print(f"P95: {stats.get('p95', 0):.3f}s")

# Usage
tracker = LatencyTracker()

for _ in range(10):
    tracker.start()
    # Simulate agent work
    time.sleep(0.1)
    tracker.stop()

tracker.print_report()
```

**Related terms:** Performance, Response Time, Throughput

---

## M

### Metric

**Definition:** A quantitative measure used to evaluate agent performance. Metrics can measure functionality, efficiency, quality, or other dimensions.

**Example:**
```python
from dataclasses import dataclass
from typing import Callable, List
from enum import Enum

class MetricType(Enum):
    HIGHER_BETTER = "higher_better"  # Accuracy, F1
    LOWER_BETTER = "lower_better"    # Latency, Cost

@dataclass
class Metric:
    """Defines an evaluation metric."""
    name: str
    description: str
    metric_type: MetricType
    compute_fn: Callable
    
    def compute(self, data: dict) -> float:
        """Compute metric value."""
        return self.compute_fn(data)

class MetricSuite:
    """Collection of metrics for agent evaluation."""
    
    def __init__(self):
        self.metrics: List[Metric] = []
    
    def add_metric(self, metric: Metric):
        """Add a metric."""
        self.metrics.append(metric)
    
    def evaluate(self, data: dict) -> Dict[str, float]:
        """Compute all metrics."""
        results = {}
        for metric in self.metrics:
            try:
                results[metric.name] = metric.compute(data)
            except Exception as e:
                results[metric.name] = None
        return results
    
    def summary(self, results: Dict[str, float]) -> str:
        """Generate summary of results."""
        lines = ["=== Metrics Summary ==="]
        for name, value in results.items():
            if value is not None:
                lines.append(f"{name}: {value:.4f}")
            else:
                lines.append(f"{name}: N/A")
        return "\n".join(lines)

# Define common metrics
accuracy_metric = Metric(
    name="accuracy",
    description="Proportion of correct predictions",
    metric_type=MetricType.HIGHER_BETTER,
    compute_fn=lambda d: sum(d.get("correct", [])) / len(d.get("correct", [1]))
)

latency_metric = Metric(
    name="latency",
    description="Average response time in seconds",
    metric_type=MetricType.LOWER_BETTER,
    compute_fn=lambda d: sum(d.get("latencies", [0])) / len(d.get("latencies", [1]))
)

# Usage
suite = MetricSuite()
suite.add_metric(accuracy_metric)
suite.add_metric(latency_metric)

results = suite.evaluate({
    "correct": [True, True, False, True, True],
    "latencies": [0.5, 0.6, 0.4, 0.5, 0.5]
})
print(suite.summary(results))
```

**Related terms:** KPI, Measurement, Indicator

---

## R

### Regression

**Definition:** A decrease in agent performance compared to a previous version or baseline. Regression testing ensures changes don't break existing functionality.

**Example:**
```python
from typing import Dict, List
import json

class RegressionTester:
    """Detect performance regressions."""
    
    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold  # 5% degradation threshold
        self.baseline_results: Dict[str, float] = {}
    
    def set_baseline(self, results: Dict[str, float]):
        """Set baseline performance metrics."""
        self.baseline_results = results
    
    def check_regression(self, current_results: Dict[str, float]) -> Dict:
        """Check if current results show regression."""
        regressions = []
        
        for metric, current_value in current_results.items():
            if metric in self.baseline_results:
                baseline_value = self.baseline_results[metric]
                
                if baseline_value > 0:
                    change = (current_value - baseline_value) / baseline_value
                    
                    # For metrics where lower is better (latency, cost)
                    if metric in ["latency", "cost", "tokens"]:
                        is_regression = change > self.threshold
                    else:
                        # For metrics where higher is better (accuracy)
                        is_regression = change < -self.threshold
                    
                    if is_regression:
                        regressions.append({
                            "metric": metric,
                            "baseline": baseline_value,
                            "current": current_value,
                            "change_percent": change * 100
                        })
        
        return {
            "has_regression": len(regressions) > 0,
            "regressions": regressions
        }

# Usage
tester = RegressionTester(threshold=0.05)
tester.set_baseline({
    "accuracy": 0.85,
    "latency": 0.5,
    "tokens": 1000
})

# Check new version
current = {
    "accuracy": 0.82,  # 3.5% drop
    "latency": 0.45,   # 10% improvement
    "tokens": 1200     # 20% increase
}

result = tester.check_regression(current)
print(f"Has regression: {result['has_regression']}")
for reg in result['regressions']:
    print(f"  {reg['metric']}: {reg['change_percent']:.1f}% change")
```

**Related terms:** Degradation, Baseline, Testing

---

## T

### Test Case

**Definition:** A specific input-output pair used to verify agent behavior. Test cases define what the agent should do in particular situations.

**Example:**
```python
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

@dataclass
class TestCase:
    """Defines a test case for agent evaluation."""
    id: str
    name: str
    input: Any
    expected: Any = None
    validator: Callable = None
    tags: List[str] = field(default_factory=list)
    description: str = ""
    
    def validate(self, actual: Any) -> Dict:
        """Validate actual output against expected."""
        if self.validator:
            is_valid = self.validator(actual, self.expected)
        elif self.expected is not None:
            is_valid = actual == self.expected
        else:
            is_valid = True  # No validation
        
        return {
            "test_id": self.id,
            "name": self.name,
            "passed": is_valid,
            "expected": self.expected,
            "actual": actual
        }

class TestCaseBuilder:
    """Build test cases with fluent API."""
    
    def __init__(self):
        self.cases = []
    
    def add(self, name: str, input_data: Any, 
           expected: Any = None) -> "TestCaseBuilder":
        """Add a test case."""
        test_id = f"test_{len(self.cases) + 1}"
        self.cases.append(TestCase(
            id=test_id,
            name=name,
            input=input_data,
            expected=expected
        ))
        return self
    
    def add_with_validator(self, name: str, input_data: Any,
                          validator: Callable) -> "TestCaseBuilder":
        """Add test case with custom validator."""
        test_id = f"test_{len(self.cases) + 1}"
        self.cases.append(TestCase(
            id=test_id,
            name=name,
            input=input_data,
            validator=validator
        ))
        return self
    
    def build(self) -> List[TestCase]:
        """Build and return all test cases."""
        return self.cases

# Usage
builder = TestCaseBuilder()
tests = (
    builder
    .add("Basic math", "2+2", "4")
    .add("Capital of France", "What is the capital of France?", "Paris")
    .add_with_validator(
        "Contains keyword",
        "Tell me about AI",
        validator=lambda actual, _: "AI" in actual
    )
    .build()
)
```

**Related terms:** Unit Test, Test Suite, Assertion

---

## Quick Reference: Evaluation Checklist

```
┌─────────────────────────────────────────────────────────────┐
│                 Agent Evaluation Checklist                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FUNCTIONALITY                                              │
│  □ Task success rate > threshold                           │
│  □ Accuracy on test set acceptable                         │
│  □ Handles edge cases gracefully                           │
│                                                             │
│  PERFORMANCE                                                │
│  □ Latency within acceptable range                         │
│  □ Token usage reasonable                                  │
│  □ Cost within budget                                      │
│                                                             │
│  RELIABILITY                                                │
│  □ Error rate < threshold                                  │
│  □ Consistent outputs across runs                          │
│  □ Graceful error handling                                 │
│                                                             │
│  SAFETY                                                     │
│  □ No harmful outputs                                      │
│  □ Guardrails in place                                     │
│  □ Adversarial inputs handled                              │
│                                                             │
│  REGRESSION                                                 │
│  □ No performance degradation                              │
│  □ All previous tests still pass                           │
│  □ Comparison with baseline documented                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**[← Back to Lecture 08](./08-agent-evaluation-lecture.md)** | **[Next: Lecture 09 →](./09-agent-safety-glossary.md)**
