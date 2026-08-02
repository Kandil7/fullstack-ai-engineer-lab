# Evaluation Frameworks — Glossary 20

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Faithfulness | Metric | Answer supported by the given context |
| Golden Set | Eval | Reference inputs with expected outputs |
| Ground Truth | Eval | The known-correct answer to a sample |
| Hallucination | Failure | A claim not supported by context |
| LLM-as-Judge | Eval | A model scoring outputs against rubrics |
| Off-Topic | Metric | Answer not relevant to the question |
| Reference Answer | Eval | The expected/golden output for a sample |
| Suite | Eval | A batch of cases with aggregated scores |

## Detailed Definitions
### Faithfulness
**Definition**: Whether each answer claim is supported by the retrieved
context.
**Related**: Hallucination

### Golden Set
**Definition**: Curated samples with reference answers for regression
testing.
**Related**: Reference Answer

### Ground Truth
**Definition**: The known-correct answer used as the target.
**Related**: Golden Set

### Hallucination
**Definition**: A fluent claim unsupported by context.
**Related**: Faithfulness

### LLM-as-Judge
**Definition**: A model grading output quality on rubrics or preferences.
**Related**: Golden Set

### Off-Topic
**Definition**: An answer that fails to address the question.
**Related**: Faithfulness

### Reference Answer
**Definition**: The expected output attached to a sample.
**Related**: Ground Truth

### Suite
**Definition**: The full set of samples and the aggregate score over them.
**Related**: Golden Set

## Key Concepts Summary
### The Metrics
- Faithfulness, relevance, safety, completeness

### The Practice
- Golden sets + LLM judges + CI

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Faithfulness — ___
2. Hallucination — ___
3. Golden set — ___
4. LLM-as-judge — ___
5. Ground truth — ___

**Answers:** 1-b, 2-e, 3-a, 4-c, 5-d where a=curated eval cases, b=context
support, c=model scoring, d=known-correct answer, e=unsupported claim.
