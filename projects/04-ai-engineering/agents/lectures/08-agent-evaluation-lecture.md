# Lecture 08: Agent Evaluation

## 🎯 Topic Overview

**Agent evaluation** is the systematic measurement of agent performance, reliability, and effectiveness. Without evaluation, you cannot know if your agent is working correctly or improve it over time.

This lecture covers:
- Evaluation metrics for agents
- Building evaluation frameworks
- Testing agent behavior
- Benchmarking and comparison
- Continuous evaluation in production

---

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. **Define** appropriate metrics for agent evaluation
2. **Build** automated evaluation frameworks
3. **Test** agent behavior systematically
4. **Compare** different agent configurations
5. **Monitor** agent performance in production
6. **Identify** and diagnose agent failures
7. **Optimize** agents based on evaluation results
8. **Implement** regression testing for agents

---

## 🧩 Key Concepts

### 1. Evaluation Dimensions

```
┌─────────────────────────────────────────────────────────────┐
│                 Agent Evaluation Dimensions                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FUNCTIONALITY          EFFICIENCY                          │
│  ┌─────────────────┐   ┌─────────────────┐                │
│  │ • Task success  │   │ • Latency       │                │
│  │ • Accuracy      │   │ • Token usage   │                │
│  │ • Completeness  │   │ • Cost          │                │
│  └─────────────────┘   └─────────────────┘                │
│                                                             │
│  RELIABILITY           SAFETY                              │
│  ┌─────────────────┐   ┌─────────────────┐                │
│  │ • Consistency   │   │ • Error handling │                │
│  │ • Error rate    │   │ • Guardrails    │                │
│  │ • Recovery      │   │ • Edge cases    │                │
│  └─────────────────┘   └─────────────────┘                │
│                                                             │
│  USER EXPERIENCE       ROBUSTNESS                          │
│  ┌─────────────────┐   ┌─────────────────┐                │
│  │ • Response      │   │ • Adversarial   │                │
│  │   quality       │   │   inputs        │                │
│  │ • Helpfulness   │   │ • Edge cases    │                │
│  └─────────────────┘   └─────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Evaluation Metrics

| Metric | Description | How to Measure |
|--------|-------------|----------------|
| **Task Success Rate** | % of tasks completed correctly | Ground truth comparison |
| **Accuracy** | Correctness of outputs | Human evaluation / metrics |
| **Latency** | Time to complete tasks | System logs |
| **Token Efficiency** | Tokens used per task | API usage tracking |
| **Error Rate** | Frequency of failures | Error logging |
| **Recovery Rate** | % of errors successfully recovered | Error handling logs |
| **Cost** | Financial cost per task | API billing data |

### 3. Evaluation Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 Evaluation Pipeline                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │ Test     │    │ Execute  │    │ Evaluate │             │
│  │ Cases    │───►│ Agent    │───►│ Results  │             │
│  └──────────┘    └──────────┘    └────┬─────┘             │
│                                       │                     │
│                                       ▼                     │
│                              ┌──────────────┐              │
│                              │   Metrics    │              │
│                              │   Report     │              │
│                              └──────┬───────┘              │
│                                     │                       │
│                    ┌────────────────┼────────────────┐     │
│                    ▼                ▼                ▼     │
│              ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│              │ Pass/Fail│    │ Compare  │    │ Improve  │ │
│              └──────────┘    └──────────┘    └──────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Examples

### Example 1: Complete Evaluation Framework

```python
"""
Agent Evaluation Framework
Comprehensive testing and benchmarking for AI agents.
"""
import json
import time
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import statistics


class TestStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class TestCase:
    """A single test case for agent evaluation."""
    id: str
    name: str
    input_data: Any
    expected_output: Any = None
    expected_behavior: Dict = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    timeout: float = 30.0


@dataclass
class TestResult:
    """Result of running a test case."""
    test_case: TestCase
    actual_output: Any
    status: TestStatus
    metrics: Dict = field(default_factory=dict)
    execution_time: float = 0.0
    error: str = None
    
    def to_dict(self) -> dict:
        return {
            "test_id": self.test_case.id,
            "name": self.test_case.name,
            "status": self.status.value,
            "execution_time": self.execution_time,
            "metrics": self.metrics,
            "error": self.error
        }


class AgentEvaluator:
    """
    Comprehensive agent evaluation system.
    
    Features:
    - Multiple evaluation dimensions
    - Automated test execution
    - Metric computation
    - Report generation
    """
    
    def __init__(self, agent: Callable):
        self.agent = agent
        self.test_cases: List[TestCase] = []
        self.results: List[TestResult] = []
    
    def add_test_case(self, test_case: TestCase):
        """Add a test case."""
        self.test_cases.append(test_case)
    
    def load_test_cases(self, filepath: str):
        """Load test cases from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for tc_data in data.get("test_cases", []):
            self.test_cases.append(TestCase(**tc_data))
    
    def run_test(self, test_case: TestCase) -> TestResult:
        """Execute a single test case."""
        start_time = time.time()
        
        try:
            # Execute agent
            actual_output = self.agent(test_case.input_data)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Evaluate output
            metrics = self._evaluate_output(
                test_case, actual_output, execution_time
            )
            
            # Determine status
            status = self._determine_status(test_case, actual_output, metrics)
            
            return TestResult(
                test_case=test_case,
                actual_output=actual_output,
                status=status,
                metrics=metrics,
                execution_time=execution_time
            )
            
        except Exception as e:
            return TestResult(
                test_case=test_case,
                actual_output=None,
                status=TestStatus.ERROR,
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    def run_all_tests(self, tags: List[str] = None) -> Dict:
        """Run all test cases, optionally filtered by tags."""
        self.results = []
        
        # Filter test cases if tags provided
        test_cases = self.test_cases
        if tags:
            test_cases = [tc for tc in test_cases 
                        if any(t in tc.tags for t in tags)]
        
        # Run tests
        for test_case in test_cases:
            result = self.run_test(test_case)
            self.results.append(result)
        
        # Generate summary
        return self.generate_report()
    
    def _evaluate_output(self, test_case: TestCase, 
                        actual: Any, execution_time: float) -> Dict:
        """Evaluate agent output against expected results."""
        metrics = {
            "execution_time": execution_time,
            "output_type": type(actual).__name__
        }
        
        # Exact match
        if test_case.expected_output is not None:
            metrics["exact_match"] = actual == test_case.expected_output
        
        # Content similarity
        if isinstance(actual, str) and isinstance(test_case.expected_output, str):
            metrics["similarity"] = self._calculate_similarity(
                actual, test_case.expected_output
            )
        
        # Check expected behaviors
        for behavior, expected in test_case.expected_behavior.items():
            if behavior == "contains_words":
                if isinstance(actual, str):
                    words = expected if isinstance(expected, list) else [expected]
                    metrics[f"contains_{behavior}"] = all(
                        word.lower() in actual.lower() for word in words
                    )
            
            elif behavior == "min_length":
                if isinstance(actual, str):
                    metrics[f"meets_{behavior}"] = len(actual) >= expected
            
            elif behavior == "max_tokens":
                # Estimate tokens
                estimated_tokens = len(str(actual).split()) * 1.3
                metrics[f"within_{behavior}"] = estimated_tokens <= expected
        
        return metrics
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union
    
    def _determine_status(self, test_case: TestCase,
                         actual: Any, metrics: Dict) -> TestStatus:
        """Determine if test passed or failed."""
        # Check exact match
        if test_case.expected_output is not None:
            if actual != test_case.expected_output:
                return TestStatus.FAILED
        
        # Check behavior metrics
        for key, value in metrics.items():
            if key.startswith("contains_") and not value:
                return TestStatus.FAILED
            if key.startswith("meets_") and not value:
                return TestStatus.FAILED
        
        return TestStatus.PASSED
    
    def generate_report(self) -> Dict:
        """Generate comprehensive evaluation report."""
        if not self.results:
            return {"error": "No test results"}
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.results if r.status == TestStatus.FAILED)
        errors = sum(1 for r in self.results if r.status == TestStatus.ERROR)
        
        execution_times = [r.execution_time for r in self.results]
        
        report = {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "success_rate": passed / total if total > 0 else 0
            },
            "performance": {
                "avg_execution_time": statistics.mean(execution_times) if execution_times else 0,
                "median_execution_time": statistics.median(execution_times) if execution_times else 0,
                "max_execution_time": max(execution_times) if execution_times else 0,
                "min_execution_time": min(execution_times) if execution_times else 0
            },
            "results": [r.to_dict() for r in self.results]
        }
        
        return report
    
    def compare_agents(self, agents: Dict[str, Callable],
                      test_cases: List[TestCase] = None) -> Dict:
        """Compare multiple agents on the same test cases."""
        tests = test_cases or self.test_cases
        comparison = {}
        
        for agent_name, agent_func in agents.items():
            evaluator = AgentEvaluator(agent_func)
            evaluator.test_cases = tests
            
            report = evaluator.run_all_tests()
            comparison[agent_name] = report["summary"]
        
        return comparison


class LLMJudge:
    """
    Uses an LLM to evaluate agent outputs.
    
    Useful for subjective qualities like:
    - Helpfulness
    - Clarity
    - Accuracy
    - Safety
    """
    
    def __init__(self, llm_caller: Callable):
        self.llm = llm_caller
    
    def evaluate(self, task: str, output: str,
                criteria: List[str] = None) -> Dict:
        """
        Evaluate agent output using LLM.
        
        Args:
            task: Original task/question
            output: Agent's output to evaluate
            criteria: Evaluation criteria
            
        Returns:
            Evaluation scores and feedback
        """
        criteria = criteria or ["accuracy", "helpfulness", "clarity"]
        
        prompt = f"""Evaluate the following AI agent response.

Task: {task}
Agent Response: {output}

Evaluation Criteria:
{chr(10).join(f"- {c}" for c in criteria)}

For each criterion, provide:
1. Score (1-10)
2. Brief explanation

Also provide:
- Overall score (1-10)
- Key strengths
- Key weaknesses
- Suggestions for improvement

Return as JSON:
{{
    "scores": {{"criterion": score}},
    "overall_score": score,
    "strengths": ["..."],
    "weaknesses": ["..."],
    "suggestions": ["..."]
}}
"""
        
        response = self.llm(prompt)
        
        try:
            return json.loads(response)
        except:
            return {
                "scores": {},
                "overall_score": 5,
                "error": "Failed to parse evaluation"
            }
    
    def batch_evaluate(self, evaluations: List[Dict]) -> List[Dict]:
        """Evaluate multiple outputs."""
        results = []
        for eval_item in evaluations:
            result = self.evaluate(
                eval_item["task"],
                eval_item["output"],
                eval_item.get("criteria")
            )
            results.append(result)
        return results


# === Usage Example ===

# Mock agent
def mock_agent(input_data: Any) -> str:
    """Simple mock agent for testing."""
    if isinstance(input_data, dict):
        return f"Processed: {input_data.get('question', 'unknown')}"
    return f"Echo: {input_data}"

# Create evaluator
evaluator = AgentEvaluator(agent=mock_agent)

# Add test cases
evaluator.add_test_case(TestCase(
    id="test_1",
    name="Basic question",
    input_data={"question": "What is AI?"},
    expected_output="Processed: What is AI?",
    tags=["basic", "unit"]
))

evaluator.add_test_case(TestCase(
    id="test_2",
    name="Complex question",
    input_data={"question": "Explain machine learning"},
    expected_behavior={
        "contains_words": ["machine", "learning"],
        "min_length": 20
    },
    tags=["basic", "content"]
))

# Run tests
report = evaluator.run_all_tests()

print("=== Evaluation Report ===")
print(f"Total: {report['summary']['total_tests']}")
print(f"Passed: {report['summary']['passed']}")
print(f"Failed: {report['summary']['failed']}")
print(f"Success Rate: {report['summary']['success_rate']:.1%}")
print(f"Avg Time: {report['performance']['avg_execution_time']:.3f}s")

# LLM Judge evaluation
def mock_llm(prompt):
    return json.dumps({
        "scores": {"accuracy": 8, "helpfulness": 7},
        "overall_score": 7.5,
        "strengths": ["Clear response"],
        "weaknesses": ["Could be more detailed"],
        "suggestions": ["Add examples"]
    })

judge = LLMJudge(llm_caller=mock_llm)
evaluation = judge.evaluate(
    task="What is AI?",
    output="AI is artificial intelligence."
)
print(f"\nLLM Judge Score: {evaluation.get('overall_score')}")
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Testing Only Happy Path
```python
# ❌ BAD: Only testing easy cases
test_cases = [
    {"input": "Hello", "expected": "Hello back"},
]

# ✅ GOOD: Include edge cases and failures
test_cases = [
    {"input": "Hello", "expected": "Hello back"},
    {"input": "", "expected": "error or helpful response"},
    {"input": "A" * 10000, "expected": "handles long input"},
    {"input": None, "expected": "handles null input"},
]
```

### Mistake 2: Ignoring Performance
```python
# ❌ BAD: Only checking if output is correct
def evaluate(agent, test):
    output = agent(test["input"])
    return output == test["expected"]

# ✅ GOOD: Also measure performance
def evaluate(agent, test):
    start = time.time()
    output = agent(test["input"])
    duration = time.time() - start
    
    return {
        "correct": output == test["expected"],
        "latency": duration,
        "tokens_used": estimate_tokens(output)
    }
```

### Mistake 3: Not Running Tests Regularly
```python
# ❌ BAD: Test only once before deployment
run_tests()
deploy_agent()

# ✅ GOOD: Continuous testing
def ci_pipeline():
    run_unit_tests()
    run_integration_tests()
    run_performance_tests()
    if all_passed():
        deploy_agent()
```

---

## ✅ Best Practices

1. **Test Early and Often**: Run evaluations frequently
2. **Diverse Test Cases**: Include various scenarios and edge cases
3. **Automate Everything**: Manual testing doesn't scale
4. **Track Metrics Over Time**: Monitor for regression
5. **Use Realistic Data**: Test with production-like inputs
6. **Evaluate Multiple Dimensions**: Not just correctness
7. **Compare Against Baselines**: Know if changes help or hurt
8. **Document Test Cases**: Explain what each test verifies

---

## 🏋️ Practice Exercises

### Exercise 1: Build a Test Suite
Create a comprehensive test suite for a Q&A agent with at least 20 test cases.

### Exercise 2: LLM Judge
Implement an LLM-based evaluator that scores agent outputs on helpfulness, accuracy, and safety.

### Exercise 3: Benchmark System
Build a benchmarking system that compares multiple agents on the same tasks.

---

## 📝 Summary

| Dimension | Metrics | Tools |
|-----------|---------|-------|
| **Functionality** | Success rate, accuracy | Unit tests |
| **Performance** | Latency, throughput | Profiling |
| **Cost** | Tokens, API calls | Usage tracking |
| **Quality** | Human/LLM evaluation | Judgment |

---

## 🔗 Next Lecture

In **Lecture 09: Agent Safety**, we'll explore safety considerations and guardrails for AI agents.
