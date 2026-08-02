# Prompt Engineering — Glossary 04

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Chain of Thought | Technique | Instructing step-by-step reasoning before answering |
| Few-Shot | Technique | Teaching with worked input→output examples |
| Golden Set | Evaluation | A fixed set of scored examples for regression testing |
| Prompt Injection | Security | Malicious instructions smuggled into input data |
| Role Framing | Technique | Assigning persona and constraints via system prompt |
| Scoring Harness | Evaluation | Tooling that measures prompt quality |
| System Prompt | Structure | Top-level instructions defining behavior |
| Zero-Shot | Technique | Asking without examples |

## Detailed Definitions
### Chain of Thought
**Definition**: Prompting "think step by step" to improve multi-step reasoning.
**Related**: Zero-Shot

### Few-Shot
**Definition**: Providing 2-3 example pairs to teach by demonstration.
**Related**: Zero-Shot

### Golden Set
**Definition**: A curated set of prompts with known-good outputs used to score
changes.
**Related**: Scoring Harness

### Prompt Injection
**Definition**: An attack where user data contains instructions that override
the system prompt.
**Related**: System Prompt

### Role Framing
**Definition**: Giving the model a role and constraints to shape style and
scope.
**Related**: System Prompt

### Scoring Harness
**Definition**: Code that compares model outputs to goldens and reports scores.
**Related**: Golden Set

### System Prompt
**Definition**: The opening instructions that set behavior for the whole
conversation.
**Related**: Role Framing

### Zero-Shot
**Definition**: Asking the model to perform a task with no examples.
**Related**: Few-Shot

## Key Concepts Summary
### The Levers
- Role, format, examples, reasoning

### The Rules
- Measure every change
- One task per prompt

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Few-shot — ___
2. Chain of thought — ___
3. System prompt — ___
4. Golden set — ___
5. Zero-shot — ___

**Answers:** 1-b, 2-e, 3-a, 4-c, 5-d where a=behavior instructions, b=teach by
examples, c=scored reference set, d=no examples, e=step-by-step reasoning.
