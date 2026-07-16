# Glossary: AI Evaluation

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Evaluation | Measuring AI system quality | Essential for improvement |
| Metric | Quantitative measure | Accuracy, latency, cost |
| Test Case | Input/expected output pair | Foundation of evaluation |
| Benchmark | Standardized test suite | Enables comparison |
| LLM-as-Judge | Using LLM to evaluate | Flexible, scalable |
| Precision | Correct predictions / all predictions | Quality of positive predictions |
| Recall | Correct predictions / all positives | Coverage of positives |
| F1 Score | Harmonic mean of precision and recall | Balanced metric |
| Latency | Time to produce output | Performance metric |
| Throughput | Requests per second | Capacity metric |
| Faithfulness | Grounded in facts | RAG-specific metric |
| Hallucination | Made-up information | What to detect |

---

## Detailed Definitions

### Evaluation

**Definition:** The systematic process of measuring AI system quality across multiple dimensions to ensure it meets requirements and identifies areas for improvement.

**Example:**
```python
class Evaluation:
    def __init__(self, system):
        self.system = system
        self.results = []
    
    def run(self, test_cases):
        for case in test_cases:
            output = self.system(case.input)
            score = self.measure(output, case.expected)
            self.results.append(score)
        
        return self.summarize()
    
    def summarize(self):
        return {
            "avg_score": sum(self.results) / len(self.results),
            "pass_rate": sum(1 for r in self.results if r >= 0.7) / len(self.results)
        }
```

**Related Terms:** Metrics, Testing, Quality Assurance

**Dimensions:**
- Quality: Output correctness
- Performance: Speed and efficiency
- Safety: Harmful content detection
- Cost: Resource usage

---

### Metric

**Definition:** A quantitative measure used to evaluate AI system performance. Different metrics capture different aspects of quality.

**Example:**
```python
def calculate_metrics(predictions, labels):
    """Calculate common classification metrics."""
    
    # Accuracy
    correct = sum(1 for p, l in zip(predictions, labels) if p == l)
    accuracy = correct / len(labels)
    
    # Precision (for binary)
    tp = sum(1 for p, l in zip(predictions, labels) if p == 1 and l == 1)
    fp = sum(1 for p, l in zip(predictions, labels) if p == 1 and l == 0)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    
    # Recall
    fn = sum(1 for p, l in zip(predictions, labels) if p == 0 and l == 1)
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    # F1
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }
```

**Related Terms:** Accuracy, Precision, Recall, F1

**Common Metrics:**
- Classification: Accuracy, Precision, Recall, F1, AUC
- Generation: BLEU, ROUGE, METEOR
- Ranking: NDCG, MRR, MAP
- System: Latency, Throughput, Cost

---

### Test Case

**Definition:** A single input-output pair used to evaluate system behavior. Test cases define what the system should do for specific inputs.

**Example:**
```python
from dataclasses import dataclass
from typing import Any

@dataclass
class TestCase:
    id: str
    input_data: Any
    expected_output: Any
    tags: list = None
    
# Example test cases
test_cases = [
    TestCase(
        id="math_1",
        input_data="What is 2 + 2?",
        expected_output="4",
        tags=["math", "basic"]
    ),
    TestCase(
        id="math_2",
        input_data="What is 10 / 0?",
        expected_output="Error: Division by zero",
        tags=["math", "edge_case"]
    ),
    TestCase(
        id="geo_1",
        input_data="Capital of France?",
        expected_output="Paris",
        tags=["geography"]
    )
]
```

**Related Terms:** Input, Expected Output, Assertion

**Best Practices:**
- Cover happy path and edge cases
- Include diverse scenarios
- Version control test suites
- Tag for selective testing

---

### Benchmark

**Definition:** A standardized test suite used to compare different AI systems or versions. Enables objective comparison across approaches.

**Example:**
```python
class Benchmark:
    def __init__(self, name, test_cases):
        self.name = name
        self.test_cases = test_cases
        self.results = {}
    
    def evaluate(self, system_name, system_fn):
        """Evaluate a system on the benchmark."""
        scores = []
        
        for case in self.test_cases:
            output = system_fn(case.input_data)
            score = self._score(output, case.expected_output)
            scores.append(score)
        
        self.results[system_name] = {
            "avg_score": sum(scores) / len(scores),
            "scores": scores
        }
    
    def compare(self):
        """Compare all evaluated systems."""
        return sorted(
            self.results.items(),
            key=lambda x: x[1]["avg_score"],
            reverse=True
        )

# Usage
benchmark = Benchmark("qa_benchmark", test_cases)
benchmark.evaluate("system_v1", v1_fn)
benchmark.evaluate("system_v2", v2_fn)
print(benchmark.compare())
```

**Related Terms:** Evaluation, Comparison, Standardized

**Purpose:**
- Objective comparison
- Track improvements
- Identify regressions
- Share results

---

### LLM-as-Judge

**Definition:** Using a large language model to evaluate the quality of outputs from another AI system. Flexible and scalable evaluation method.

**Example:**
```python
def llm_judge(actual, expected, criteria="correctness"):
    """Use LLM to judge output quality."""
    
    prompt = f"""Rate the quality of this output.

Actual: {actual}
Expected: {expected}
Criteria: {criteria}

Rate 0-1:
- 0: Completely wrong
- 0.5: Partially correct
- 1: Fully correct

Score:"""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    
    return float(response.choices[0].message.content.strip())

# Usage
score = llm_judge(
    actual="Paris is the capital of France",
    expected="The capital of France is Paris",
    criteria="correctness and completeness"
)
```

**Related Terms:** Evaluation, Quality, Judgment

**Advantages:**
- Flexible criteria
- No labeled data needed
- Handles nuance
- Scalable

**Considerations:**
- Cost per evaluation
- Potential bias
- Consistency issues

---

### Precision

**Definition:** The proportion of positive predictions that are actually correct. Measures the quality of positive predictions.

**Example:**
```python
def precision(predicted_positives, actual_positives):
    """Calculate precision."""
    if not predicted_positives:
        return 0.0
    
    true_positives = len(set(predicted_positives) & set(actual_positives))
    return true_positives / len(predicted_positives)

# Example
predicted = ["spam", "spam", "not_spam", "spam"]
actual = ["spam", "not_spam", "not_spam", "spam"]

prec = precision(predicted, actual)
print(f"Precision: {prec:.2f}")  # 0.67 (2 of 3 spam predictions correct)
```

**Related Terms:** Recall, F1 Score, Accuracy

**When to Use:**
- Cost of false positives is high
- Want to minimize false alarms
- Example: Spam detection, fraud detection

---

### Recall

**Definition:** The proportion of actual positives that were correctly identified. Measures coverage of positives.

**Example:**
```python
def recall(predicted_positives, actual_positives):
    """Calculate recall."""
    if not actual_positives:
        return 0.0
    
    true_positives = len(set(predicted_positives) & set(actual_positives))
    return true_positives / len(actual_positives)

# Example
predicted = ["spam", "spam", "not_spam", "spam"]
actual = ["spam", "spam", "not_spam", "not_spam"]

rec = recall(predicted, actual)
print(f"Recall: {rec:.2f}")  # 0.50 (found 1 of 2 actual spam)
```

**Related Terms:** Precision, F1 Score, Sensitivity

**When to Use:**
- Cost of false negatives is high
- Want to find all positives
- Example: Disease detection, security threats

---

### F1 Score

**Definition:** The harmonic mean of precision and recall. Provides a single score that balances both concerns.

**Example:**
```python
def f1_score(precision, recall):
    """Calculate F1 score."""
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

# Example
prec = 0.8
rec = 0.6
f1 = f1_score(prec, rec)
print(f"F1 Score: {f1:.2f}")  # 0.69
```

**Related Terms:** Precision, Recall, Harmonic Mean

**When to Use:**
- Need balance between precision and recall
- Single metric for comparison
- Class imbalance

---

### Latency

**Definition:** The time it takes for a system to produce output. Critical for user experience and real-time applications.

**Example:**
```python
import time

def measure_latency(system_fn, input_data, n_runs=10):
    """Measure system latency."""
    latencies = []
    
    for _ in range(n_runs):
        start = time.time()
        output = system_fn(input_data)
        latency = (time.time() - start) * 1000  # ms
        latencies.append(latency)
    
    return {
        "avg_ms": sum(latencies) / len(latencies),
        "min_ms": min(latencies),
        "max_ms": max(latencies),
        "p50_ms": sorted(latencies)[len(latencies) // 2],
        "p95_ms": sorted(latencies)[int(len(latencies) * 0.95)]
    }

# Usage
metrics = measure_latency(my_system, "test input")
print(f"Average latency: {metrics['avg_ms']:.0f}ms")
```

**Related Terms:** Throughput, Performance, Response Time

**Types:**
- Time to first token (TTFT)
- Time to completion
- End-to-end latency

---

### Throughput

**Definition:** The number of requests a system can handle per unit time. Measures system capacity.

**Example:**
```python
import time
from concurrent.futures import ThreadPoolExecutor

def measure_throughput(system_fn, inputs, max_workers=10):
    """Measure system throughput."""
    
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(system_fn, inputs))
    
    elapsed = time.time() - start
    throughput = len(inputs) / elapsed
    
    return {
        "requests_per_second": throughput,
        "total_requests": len(inputs),
        "total_time_seconds": elapsed
    }

# Usage
inputs = [f"query_{i}" for i in range(100)]
metrics = measure_throughput(my_system, inputs)
print(f"Throughput: {metrics['requests_per_second']:.1f} req/s")
```

**Related Terms:** Latency, Capacity, Concurrency

**When to Measure:**
- Capacity planning
- Cost estimation
- Performance optimization

---

### Faithfulness

**Definition:** A RAG-specific metric measuring whether the generated answer is supported by the retrieved context. Low faithfulness indicates hallucination.

**Example:**
```python
def evaluate_faithfulness(answer, context):
    """Evaluate if answer is grounded in context."""
    
    prompt = f"""Evaluate if this answer is faithful to the context.

Context: {context}
Answer: {answer}

Rate 0-1:
- 0: Contains hallucinations
- 0.5: Partially supported
- 1: Fully supported

Score:"""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    
    return float(response.choices[0].message.content.strip())

# Usage
answer = "Python was created by Guido van Rossum in 1991"
context = "Python is a programming language created in the late 1980s"

score = evaluate_faithfulness(answer, context)
# Score might be low because context doesn't mention Guido van Rossum
```

**Related Terms:** Grounding, Hallucination, RAG

**Why Important:**
- Detects hallucination
- Ensures accuracy
- Builds trust
- Critical for RAG

---

### Hallucination

**Definition:** When an AI system generates information that is factually incorrect or not supported by the context. A major concern in AI systems.

**Example:**
```python
# Hallucination example
context = "The Eiffel Tower is in Paris, France"
question = "When was the Eiffel Tower built?"
answer = llm.generate(f"Context: {context}\nQuestion: {question}")

# Potential hallucination: "The Eiffel Tower was built in 1889"
# (1889 is correct, but not in the context - model used training data)

# To detect hallucination:
def detect_hallucination(answer, context):
    """Check if answer contains information not in context."""
    # Simple check - more sophisticated methods exist
    answer_facts = extract_facts(answer)
    context_facts = extract_facts(context)
    
    unsupported = answer_facts - context_facts
    return len(unsupported) > 0, unsupported
```

**Related Terms:** Grounding, Faithfulness, Accuracy

**Causes:**
- Model uncertainty
- Lack of context
- Training data gaps
- Conflicting information

---

### Accuracy

**Definition:** The proportion of correct predictions out of all predictions. Simple but often misleading metric.

**Example:**
```python
def accuracy(predictions, labels):
    """Calculate accuracy."""
    correct = sum(1 for p, l in zip(predictions, labels) if p == l)
    return correct / len(labels)

# Example
predictions = ["cat", "cat", "dog", "cat"]
labels = ["cat", "dog", "dog", "cat"]

acc = accuracy(predictions, labels)
print(f"Accuracy: {acc:.2f}")  # 0.75
```

**Related Terms:** Precision, Recall, F1 Score

**When to Use:**
- Balanced classes
- All errors equally costly
- Simple baseline

**When NOT to Use:**
- Imbalanced classes
- Different error costs

---

### BLEU Score

**Definition:** Bilingual Evaluation Understudy - a metric for evaluating machine translation quality by comparing n-gram overlap with reference translations.

**Example:**
```python
from nltk.translate.bleu_score import sentence_bleu

# Reference translations
reference = [["the", "cat", "is", "on", "the", "mat"]]

# Machine translation output
candidate = ["the", "cat", "sat", "on", "the", "mat"]

# Calculate BLEU score
score = sentence_bleu(reference, candidate)
print(f"BLEU Score: {score:.2f}")  # ~0.69
```

**Related Terms:** ROUGE, METEOR, Translation Quality

**Limitations:**
- Doesn't capture meaning well
- Favors short outputs
- Requires multiple references

---

### ROUGE Score

**Definition:** Recall-Oriented Understudy for Gisting Evaluation - a metric for evaluating summarization quality by comparing n-gram overlap with reference summaries.

**Example:**
```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# Reference summary
reference = "The cat sat on the mat"

# Generated summary
generated = "The cat was sitting on the mat"

# Calculate ROUGE scores
scores = scorer.score(reference, generated)
print(f"ROUGE-1: {scores['rouge1'].fmeasure:.2f}")  # ~0.77
print(f"ROUGE-2: {scores['rouge2'].fmeasure:.2f}")  # ~0.57
print(f"ROUGE-L: {scores['rougeL'].fmeasure:.2f}")  # ~0.77
```

**Related Terms:** BLEU, Summarization Quality

**Variants:**
- ROUGE-1: Unigram overlap
- ROUGE-2: Bigram overlap
- ROUGE-L: Longest common subsequence

---

### A/B Testing

**Definition:** Comparing two versions of a system by randomly assigning users to each version and measuring performance differences.

**Example:**
```python
import random
from scipy import stats

def ab_test(system_a, system_b, test_cases, confidence=0.95):
    """Compare two systems using A/B testing."""
    
    results_a = []
    results_b = []
    
    for case in test_cases:
        # Randomly assign to A or B
        if random.random() < 0.5:
            output = system_a(case.input_data)
            score = evaluate(output, case.expected_output)
            results_a.append(score)
        else:
            output = system_b(case.input_data)
            score = evaluate(output, case.expected_output)
            results_b.append(score)
    
    # Statistical test
    t_stat, p_value = stats.ttest_ind(results_a, results_b)
    
    return {
        "system_a_avg": sum(results_a) / len(results_a),
        "system_b_avg": sum(results_b) / len(results_b),
        "p_value": p_value,
        "significant": p_value < (1 - confidence),
        "winner": "A" if sum(results_a)/len(results_a) > sum(results_b)/len(results_b) else "B"
    }
```

**Related Terms:** Statistical Significance, Experiment

**Key Considerations:**
- Sample size
- Random assignment
- Statistical significance
- Practical significance

---

### Confusion Matrix

**Definition:** A table showing true vs predicted labels, helping visualize classification performance.

**Example:**
```python
def confusion_matrix(predictions, labels, classes):
    """Generate confusion matrix."""
    matrix = {c: {c2: 0 for c2 in classes} for c in classes}
    
    for pred, label in zip(predictions, labels):
        matrix[label][pred] += 1
    
    return matrix

# Example
predictions = ["cat", "cat", "dog", "dog", "cat"]
labels = ["cat", "dog", "dog", "dog", "cat"]
classes = ["cat", "dog"]

matrix = confusion_matrix(predictions, labels, classes)
for true_class in classes:
    for pred_class in classes:
        print(f"True {true_class}, Predicted {pred_class}: {matrix[true_class][pred_class]}")
```

**Related Terms:** Precision, Recall, F1 Score

**Components:**
- True Positives (TP)
- True Negatives (TN)
- False Positives (FP)
- False Negatives (FN)

---

### Error Analysis

**Definition:** Systematically examining failures to understand patterns and root causes. Essential for improving AI systems.

**Example:**
```python
def error_analysis(results):
    """Analyze patterns in failures."""
    
    failures = [r for r in results if not r.passed]
    
    # Categorize failures
    categories = {}
    for failure in failures:
        category = categorize_failure(failure)
        if category not in categories:
            categories[category] = []
        categories[category].append(failure)
    
    # Summarize
    summary = {}
    for category, items in categories.items():
        summary[category] = {
            "count": len(items),
            "examples": items[:3]
        }
    
    return summary

def categorize_failure(result):
    """Categorize the type of failure."""
    if "timeout" in str(result.error).lower():
        return "timeout"
    elif "incorrect" in str(result.error).lower():
        return "accuracy"
    else:
        return "other"
```

**Related Terms:** Debugging, Root Cause Analysis

**Steps:**
1. Collect failures
2. Categorize by type
3. Identify patterns
4. Prioritize fixes
5. Measure improvement

---

## Summary

Understanding these terms is essential for effective AI evaluation:

1. **Evaluation:** Systematic quality measurement
2. **Metric:** Quantitative measure
3. **Test Case:** Input/output pair
4. **Benchmark:** Standardized test suite
5. **LLM-as-Judge:** Using LLM for evaluation
6. **Precision/Recall/F1:** Classification metrics
7. **Latency/Throughput:** Performance metrics
8. **Faithfulness:** RAG quality metric
9. **Hallucination:** What to detect
10. **A/B Testing:** Comparative evaluation

**Next:** See Lecture 07 for AI deployment.
