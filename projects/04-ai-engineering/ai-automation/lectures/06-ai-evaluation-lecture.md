# Lecture 06: AI Evaluation

## Topic Overview

AI evaluation is the systematic process of measuring the quality, performance, and reliability of AI systems. Without evaluation, you're flying blind—you can't improve what you can't measure. This lecture covers evaluation metrics, testing strategies, benchmarking, and how to build evaluation pipelines that ensure your AI systems work correctly in production.

**Duration:** 3-4 hours  
**Difficulty:** Intermediate to Advanced  
**Prerequisites:** Lectures 01-05

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Design** comprehensive evaluation frameworks for AI systems
2. **Implement** automated evaluation pipelines
3. **Measure** key metrics (accuracy, relevance, faithfulness, latency)
4. **Build** test datasets and benchmarks
5. **Use** LLM-as-judge for evaluation
6. **Detect** and diagnose common AI failures
7. **Monitor** AI quality in production
8. **A/B test** different AI approaches

---

## Key Concepts

### 1. Why Evaluate?

```
Without Evaluation:
┌─────────────────────────────────────────────────┐
│  Build → Deploy → Hope it works → User complaints│
└─────────────────────────────────────────────────┘

With Evaluation:
┌─────────────────────────────────────────────────┐
│  Build → Test → Measure → Deploy → Monitor      │
│                      ↑              │            │
│                      └──────────────┘            │
│                  (Continuous Improvement)         │
└─────────────────────────────────────────────────┘
```

**Evaluation tells you:**
- Is the system working correctly?
- How does it compare to alternatives?
- Where are the failure modes?
- Is it improving over time?

### 2. Evaluation Dimensions

| Dimension | What It Measures | Example Metrics |
|-----------|------------------|-----------------|
| Quality | Output correctness | Accuracy, F1, BLEU |
| Relevance | Response appropriateness | Relevance score, NDCG |
| Faithfulness | Grounded in facts | Hallucination rate |
| Safety | Harmful content | Toxicity score |
| Performance | Speed and efficiency | Latency, throughput |
| Cost | Resource usage | Tokens/call, $/request |

### 3. Automated Evaluation

```python
from dataclasses import dataclass
from typing import List, Dict, Any
from openai import OpenAI


@dataclass
class EvalCase:
    """A test case for evaluation."""
    input_data: Any
    expected_output: Any
    metadata: Dict = None


@dataclass
class EvalResult:
    """Result of evaluating a single case."""
    case_id: str
    input_data: Any
    actual_output: Any
    expected_output: Any
    score: float
    passed: bool
    details: Dict = None


class AutoEvaluator:
    """Automated evaluation framework."""
    
    def __init__(self):
        self.client = OpenAI()
    
    def evaluate_exact_match(
        self,
        test_cases: List[EvalCase]
    ) -> List[EvalResult]:
        """Evaluate using exact match."""
        results = []
        
        for i, case in enumerate(test_cases):
            actual = self._get_output(case.input_data)
            passed = str(actual).strip() == str(case.expected_output).strip()
            
            results.append(EvalResult(
                case_id=f"case_{i}",
                input_data=case.input_data,
                actual_output=actual,
                expected_output=case.expected_output,
                score=1.0 if passed else 0.0,
                passed=passed
            ))
        
        return results
    
    def evaluate_similarity(
        self,
        test_cases: List[EvalCase],
        threshold: float = 0.8
    ) -> List[EvalResult]:
        """Evaluate using semantic similarity."""
        results = []
        
        for i, case in enumerate(test_cases):
            actual = self._get_output(case.input_data)
            
            # Get embeddings
            similarity = self._calculate_similarity(
                str(actual),
                str(case.expected_output)
            )
            
            results.append(EvalResult(
                case_id=f"case_{i}",
                input_data=case.input_data,
                actual_output=actual,
                expected_output=case.expected_output,
                score=similarity,
                passed=similarity >= threshold
            ))
        
        return results
    
    def evaluate_llm_judge(
        self,
        test_cases: List[EvalCase],
        criteria: str = "correctness"
    ) -> List[EvalResult]:
        """Evaluate using LLM-as-judge."""
        results = []
        
        for i, case in enumerate(test_cases):
            actual = self._get_output(case.input_data)
            
            score = self._llm_judge(
                input_data=case.input_data,
                actual_output=actual,
                expected_output=case.expected_output,
                criteria=criteria
            )
            
            results.append(EvalResult(
                case_id=f"case_{i}",
                input_data=case.input_data,
                actual_output=actual,
                expected_output=case.expected_output,
                score=score,
                passed=score >= 0.7
            ))
        
        return results
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=[text1, text2]
        )
        
        emb1 = response.data[0].embedding
        emb2 = response.data[1].embedding
        
        # Cosine similarity
        import numpy as np
        return float(np.dot(emb1, emb2) / (
            np.linalg.norm(emb1) * np.linalg.norm(emb2)
        ))
    
    def _llm_judge(
        self,
        input_data: Any,
        actual_output: str,
        expected_output: str,
        criteria: str
    ) -> float:
        """Use LLM to evaluate output quality."""
        
        prompt = f"""Rate the quality of this output on a scale of 0 to 1.

Input: {input_data}
Actual Output: {actual_output}
Expected Output: {expected_output}

Evaluation Criteria: {criteria}

Rate based on:
- 0: Completely wrong
- 0.5: Partially correct
- 1: Fully correct and complete

Provide only the numerical score (0-1)."""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        try:
            return float(response.choices[0].message.content.strip())
        except ValueError:
            return 0.5
    
    def _get_output(self, input_data: Any) -> str:
        """Get output from the system being evaluated."""
        # Override this method with your actual system
        return "placeholder output"


def summarize_results(results: List[EvalResult]) -> Dict:
    """Summarize evaluation results."""
    
    if not results:
        return {"error": "No results"}
    
    scores = [r.score for r in results]
    passed = sum(1 for r in results if r.passed)
    
    return {
        "total_cases": len(results),
        "pass_rate": passed / len(results),
        "avg_score": sum(scores) / len(scores),
        "min_score": min(scores),
        "max_score": max(scores),
        "failed_cases": [
            {"case_id": r.case_id, "score": r.score}
            for r in results if not r.passed
        ]
    }
```

### 4. RAG Evaluation

Specific evaluation for RAG systems:

```python
from dataclasses import dataclass
from typing import List
from openai import OpenAI


@dataclass
class RAGEvalCase:
    """Test case for RAG evaluation."""
    question: str
    expected_answer: str
    relevant_doc_ids: List[str]


class RAGEvaluator:
    """Evaluate RAG system quality."""
    
    def __init__(self):
        self.client = OpenAI()
    
    def evaluate(
        self,
        rag_system,
        test_cases: List[RAGEvalCase]
    ) -> Dict:
        """Complete RAG evaluation."""
        
        retrieval_results = []
        generation_results = []
        faithfulness_results = []
        
        for case in test_cases:
            # Get RAG response
            response = rag_system.generate(case.question)
            
            # Evaluate retrieval
            retrieval_score = self._evaluate_retrieval(
                retrieved_ids=[doc["doc_id"] for doc in response["context_docs"]],
                relevant_ids=case.relevant_doc_ids
            )
            retrieval_results.append(retrieval_score)
            
            # Evaluate generation
            generation_score = self._evaluate_generation(
                question=case.question,
                answer=response["answer"],
                expected=case.expected_answer
            )
            generation_results.append(generation_score)
            
            # Evaluate faithfulness
            faithfulness_score = self._evaluate_faithfulness(
                answer=response["answer"],
                context=[doc["content"] for doc in response["context_docs"]]
            )
            faithfulness_results.append(faithfulness_score)
        
        return {
            "retrieval": {
                "precision": self._average([r["precision"] for r in retrieval_results]),
                "recall": self._average([r["recall"] for r in retrieval_results]),
                "mrr": self._average([r["mrr"] for r in retrieval_results])
            },
            "generation": {
                "avg_score": self._average(generation_results)
            },
            "faithfulness": {
                "avg_score": self._average(faithfulness_results)
            }
        }
    
    def _evaluate_retrieval(
        self,
        retrieved_ids: List[str],
        relevant_ids: List[str]
    ) -> Dict:
        """Evaluate retrieval quality."""
        
        retrieved_set = set(retrieved_ids)
        relevant_set = set(relevant_ids)
        
        if not retrieved_set:
            return {"precision": 0, "recall": 0, "mrr": 0}
        
        # Precision@k
        hits = len(retrieved_set.intersection(relevant_set))
        precision = hits / len(retrieved_set)
        
        # Recall@k
        recall = hits / len(relevant_set) if relevant_set else 0
        
        # MRR (Mean Reciprocal Rank)
        mrr = 0
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in relevant_set:
                mrr = 1 / (i + 1)
                break
        
        return {"precision": precision, "recall": recall, "mrr": mrr}
    
    def _evaluate_generation(
        self,
        question: str,
        answer: str,
        expected: str
    ) -> float:
        """Evaluate answer quality."""
        
        prompt = f"""Rate the quality of this answer.

Question: {question}
Generated Answer: {answer}
Expected Answer: {expected}

Rate 0-1 based on:
- Correctness
- Completeness
- Clarity

Score:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        try:
            return float(response.choices[0].message.content.strip())
        except ValueError:
            return 0.5
    
    def _evaluate_faithfulness(
        self,
        answer: str,
        context: List[str]
    ) -> float:
        """Evaluate if answer is grounded in context."""
        
        context_text = "\n".join(context)
        
        prompt = f"""Evaluate if this answer is faithful to the context.

Context:
{context_text}

Answer: {answer}

Rate 0-1:
- 0: Contains hallucinations
- 0.5: Partially supported
- 1: Fully supported

Score:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        try:
            return float(response.choices[0].message.content.strip())
        except ValueError:
            return 0.5
    
    def _average(self, values: List[float]) -> float:
        """Calculate average."""
        return sum(values) / len(values) if values else 0
```

### 5. Agent Evaluation

Evaluating autonomous agent systems:

```python
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


class TaskStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


@dataclass
class AgentEvalCase:
    """Test case for agent evaluation."""
    task: str
    expected_actions: List[str]
    expected_result: str
    max_steps: int = 10


class AgentEvaluator:
    """Evaluate agent performance."""
    
    def evaluate(
        self,
        agent,
        test_cases: List[AgentEvalCase]
    ) -> Dict:
        """Evaluate agent on test cases."""
        
        results = []
        
        for case in test_cases:
            # Run agent
            agent.reset()
            result = agent.run(case.task)
            
            # Evaluate
            eval_result = self._evaluate_single(agent, case, result)
            results.append(eval_result)
        
        return self._summarize(results)
    
    def _evaluate_single(
        self,
        agent,
        case: AgentEvalCase,
        result: str
    ) -> Dict:
        """Evaluate a single task."""
        
        # Task completion
        completion_score = self._evaluate_completion(
            result,
            case.expected_result
        )
        
        # Efficiency (steps taken)
        steps_taken = len(agent.memory)
        efficiency_score = max(0, 1 - (steps_taken / case.max_steps))
        
        # Tool usage
        tool_usage_score = self._evaluate_tool_usage(
            agent.memory,
            case.expected_actions
        )
        
        # Overall status
        if completion_score >= 0.8:
            status = TaskStatus.SUCCESS
        elif completion_score >= 0.5:
            status = TaskStatus.PARTIAL
        else:
            status = TaskStatus.FAILED
        
        return {
            "task": case.task,
            "status": status,
            "completion_score": completion_score,
            "efficiency_score": efficiency_score,
            "tool_usage_score": tool_usage_score,
            "steps_taken": steps_taken,
            "result": result
        }
    
    def _evaluate_completion(
        self,
        actual: str,
        expected: str
    ) -> float:
        """Evaluate task completion."""
        
        # Simple comparison - can be enhanced with LLM judge
        actual_lower = actual.lower()
        expected_lower = expected.lower()
        
        # Check key terms
        expected_terms = expected_lower.split()
        found = sum(1 for term in expected_terms if term in actual_lower)
        
        return found / len(expected_terms) if expected_terms else 0
    
    def _evaluate_tool_usage(
        self,
        memory: List[Dict],
        expected_actions: List[str]
    ) -> float:
        """Evaluate if correct tools were used."""
        
        # Extract actions from memory
        actual_actions = []
        for item in memory:
            if "Action:" in str(item):
                action = str(item).split("Action:")[-1].split("\n")[0].strip()
                actual_actions.append(action)
        
        if not expected_actions:
            return 1.0  # No specific actions expected
        
        # Check how many expected actions were taken
        matches = sum(1 for a in expected_actions if a in actual_actions)
        return matches / len(expected_actions)
    
    def _summarize(self, results: List[Dict]) -> Dict:
        """Summarize evaluation results."""
        
        if not results:
            return {"error": "No results"}
        
        successful = sum(1 for r in results if r["status"] == TaskStatus.SUCCESS)
        partial = sum(1 for r in results if r["status"] == TaskStatus.PARTIAL)
        
        return {
            "total_tasks": len(results),
            "success_rate": successful / len(results),
            "partial_rate": partial / len(results),
            "failure_rate": 1 - (successful + partial) / len(results),
            "avg_completion_score": sum(r["completion_score"] for r in results) / len(results),
            "avg_efficiency_score": sum(r["efficiency_score"] for r in results) / len(results),
            "avg_steps": sum(r["steps_taken"] for r in results) / len(results)
        }
```

---

## Code Examples

### Example 1: Complete Evaluation Framework

```python
"""
Production evaluation framework with multiple strategies.
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Callable, Optional
from enum import Enum
import json
from openai import OpenAI
from datetime import datetime


class EvalStrategy(Enum):
    EXACT_MATCH = "exact_match"
    CONTAINS = "contains"
    SIMILARITY = "similarity"
    LLM_JUDGE = "llm_judge"
    CUSTOM = "custom"


@dataclass
class TestCase:
    """A test case with input and expected output."""
    id: str
    input_data: Any
    expected_output: Any
    tags: List[str] = None
    metadata: Dict = None


@dataclass
class EvalResult:
    """Result of evaluating a single test case."""
    test_id: str
    input_data: Any
    actual_output: Any
    expected_output: Any
    score: float
    passed: bool
    strategy: EvalStrategy
    latency_ms: float
    details: Dict = None


class EvaluationFramework:
    """Comprehensive evaluation framework."""
    
    def __init__(self):
        self.client = OpenAI()
        self.test_cases: List[TestCase] = []
        self.results: List[EvalResult] = []
    
    def add_test_cases(self, cases: List[TestCase]):
        """Add test cases."""
        self.test_cases.extend(cases)
    
    def evaluate(
        self,
        system_fn: Callable,
        strategy: EvalStrategy = EvalStrategy.LLM_JUDGE,
        **kwargs
    ) -> Dict:
        """Run evaluation."""
        
        self.results = []
        
        for test_case in self.test_cases:
            start_time = datetime.now()
            
            # Get actual output
            actual_output = system_fn(test_case.input_data)
            
            # Calculate latency
            latency_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            # Evaluate based on strategy
            score = self._evaluate_output(
                actual_output,
                test_case.expected_output,
                strategy,
                **kwargs
            )
            
            self.results.append(EvalResult(
                test_id=test_case.id,
                input_data=test_case.input_data,
                actual_output=actual_output,
                expected_output=test_case.expected_output,
                score=score,
                passed=score >= kwargs.get("threshold", 0.7),
                strategy=strategy,
                latency_ms=latency_ms
            ))
        
        return self.generate_report()
    
    def _evaluate_output(
        self,
        actual: Any,
        expected: Any,
        strategy: EvalStrategy,
        **kwargs
    ) -> float:
        """Evaluate output based on strategy."""
        
        if strategy == EvalStrategy.EXACT_MATCH:
            return 1.0 if str(actual).strip() == str(expected).strip() else 0.0
        
        elif strategy == EvalStrategy.CONTAINS:
            return 1.0 if str(expected).lower() in str(actual).lower() else 0.0
        
        elif strategy == EvalStrategy.SIMILARITY:
            return self._calculate_similarity(str(actual), str(expected))
        
        elif strategy == EvalStrategy.LLM_JUDGE:
            return self._llm_judge(actual, expected, **kwargs)
        
        elif strategy == EvalStrategy.CUSTOM:
            custom_fn = kwargs.get("custom_fn")
            if custom_fn:
                return custom_fn(actual, expected)
            return 0.5
        
        return 0.5
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=[text1, text2]
        )
        
        import numpy as np
        emb1 = response.data[0].embedding
        emb2 = response.data[1].embedding
        
        return float(np.dot(emb1, emb2) / (
            np.linalg.norm(emb1) * np.linalg.norm(emb2)
        ))
    
    def _llm_judge(
        self,
        actual: Any,
        expected: Any,
        **kwargs
    ) -> float:
        """Use LLM to judge output quality."""
        
        criteria = kwargs.get("criteria", "correctness and completeness")
        
        prompt = f"""Rate the quality of this output.

Actual Output: {actual}
Expected Output: {expected}

Criteria: {criteria}

Rate 0-1:
- 0: Completely wrong
- 0.5: Partially correct
- 1: Fully correct

Score:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        try:
            return float(response.choices[0].message.content.strip())
        except ValueError:
            return 0.5
    
    def generate_report(self) -> Dict:
        """Generate evaluation report."""
        
        if not self.results:
            return {"error": "No results"}
        
        scores = [r.score for r in self.results]
        passed = [r for r in self.results if r.passed]
        failed = [r for r in self.results if not r.passed]
        latencies = [r.latency_ms for r in self.results]
        
        return {
            "summary": {
                "total_cases": len(self.results),
                "pass_rate": len(passed) / len(self.results),
                "avg_score": sum(scores) / len(scores),
                "min_score": min(scores),
                "max_score": max(scores)
            },
            "performance": {
                "avg_latency_ms": sum(latencies) / len(latencies),
                "p50_latency_ms": sorted(latencies)[len(latencies) // 2],
                "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)]
            },
            "failures": [
                {
                    "test_id": r.test_id,
                    "score": r.score,
                    "input": str(r.input_data)[:100],
                    "actual": str(r.actual_output)[:100],
                    "expected": str(r.expected_output)[:100]
                }
                for r in failed[:10]
            ]
        }
    
    def compare_strategies(
        self,
        system_fn: Callable,
        strategies: List[EvalStrategy]
    ) -> Dict:
        """Compare different evaluation strategies."""
        
        comparisons = {}
        
        for strategy in strategies:
            results = []
            
            for test_case in self.test_cases:
                actual_output = system_fn(test_case.input_data)
                score = self._evaluate_output(
                    actual_output,
                    test_case.expected_output,
                    strategy
                )
                results.append(score)
            
            comparisons[strategy.value] = {
                "avg_score": sum(results) / len(results),
                "scores": results
            }
        
        return comparisons


# Usage example
def main():
    # Create framework
    framework = EvaluationFramework()
    
    # Add test cases
    framework.add_test_cases([
        TestCase(
            id="math_1",
            input_data="What is 2 + 2?",
            expected_output="4",
            tags=["math", "basic"]
        ),
        TestCase(
            id="math_2",
            input_data="What is 10 * 5?",
            expected_output="50",
            tags=["math", "basic"]
        ),
        TestCase(
            id="geo_1",
            input_data="What is the capital of France?",
            expected_output="Paris",
            tags=["geography"]
        )
    ])
    
    # Define system to evaluate
    def simple_qa_system(question):
        # Simple mock - replace with actual system
        if "2 + 2" in question:
            return "4"
        elif "10 * 5" in question:
            return "50"
        elif "capital of France" in question:
            return "Paris"
        return "I don't know"
    
    # Run evaluation
    results = framework.evaluate(
        system_fn=simple_qa_system,
        strategy=EvalStrategy.EXACT_MATCH
    )
    
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
```

---

## Common Mistakes to Avoid

### 1. Testing on Training Data
```python
# ❌ BAD: Testing on data the model has seen
train_data = load_data("train.csv")
test_data = train_data  # Same data!

# ✅ GOOD: Separate test set
train_data = load_data("train.csv")
test_data = load_data("test.csv")  # Unseen data
```

### 2. Ignoring Edge Cases
```python
# ❌ BAD: Only testing happy path
test_cases = [
    ("What is 2+2?", "4"),
    ("What is 3+3?", "6"),
]

# ✅ GOOD: Include edge cases
test_cases = [
    ("What is 2+2?", "4"),
    ("What is 0+0?", "0"),
    ("What is -1+1?", "0"),
    ("What is 999999+1?", "1000000"),
    ("", "I need a question"),  # Empty input
    (None, "Invalid input"),    # Null input
]
```

### 3. No Latency Measurement
```python
# ❌ BAD: Only measuring quality
score = evaluate_quality(output, expected)

# ✅ GOOD: Measure both quality and speed
start = time.time()
output = system(input)
latency = time.time() - start
quality = evaluate_quality(output, expected)
```

---

## Best Practices

1. **Test on unseen data** - Never test on training data
2. **Include edge cases** - Empty, null, malicious inputs
3. **Measure multiple dimensions** - Quality, latency, cost
4. **Automate evaluation** - Manual testing doesn't scale
5. **Use multiple strategies** - No single metric tells the whole story
6. **Version control test suites** - Track changes over time
7. **Set clear thresholds** - Define what "pass" means
8. **Monitor in production** - Detect quality degradation
9. **A/B test changes** - Compare approaches objectively
10. **Document failure modes** - Know where your system fails

---

## Practice Exercises

### Exercise 1: Build an Evaluation Suite
Create an evaluation suite for a QA system with:
- 20+ test cases covering different categories
- Multiple evaluation strategies
- Automated reporting

### Exercise 2: RAG Evaluation
Build a RAG evaluator that measures:
- Retrieval precision and recall
- Answer faithfulness
- End-to-end accuracy

### Exercise 3: Agent Evaluation
Create an agent evaluator that measures:
- Task completion rate
- Efficiency (steps taken)
- Tool usage accuracy

### Exercise 4: A/B Testing Framework
Build a framework that:
- Compares two system versions
- Calculates statistical significance
- Recommends which version to use

### Exercise 5: Production Monitoring
Create a monitoring system that:
- Logs predictions and inputs
- Detects quality degradation
- Alerts on anomalies

---

## Summary

AI evaluation is essential for building reliable systems:

1. **Metrics matter** - Choose the right metrics for your use case
2. **Automate everything** - Manual testing doesn't scale
3. **Test thoroughly** - Include edge cases and failure modes
4. **Monitor production** - Detect degradation early
5. **Iterate continuously** - Evaluation drives improvement

**Next lecture:** AI Deployment - Getting your systems into production.
