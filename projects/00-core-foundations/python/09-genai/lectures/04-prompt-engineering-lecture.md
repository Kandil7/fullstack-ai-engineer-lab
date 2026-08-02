# GenAI — 04: Prompt Engineering

## Topic Overview

Prompt engineering is the craft of designing the instructions and context that
make an LLM produce the output you want — reliably, efficiently, and
consistently. It is the primary "programming interface" for LLMs: the model's
behavior is configured in natural language, and small prompt changes can swing
quality from unusable to excellent. Unlike code, prompts are fuzzy,
interact with the model's quirks (recency bias, instruction confusion,
over-refusal), and must be **treated as code**: versioned, tested, evaluated,
and deployed with the same rigor as any other artifact.

The toolkit has a few canonical techniques:
1. **Role + task + constraints** — the system prompt sets behavior; the task
   is explicit; constraints bound the output.
2. **Few-shot examples** — 2–5 input/output examples teach format and reasoning
   better than a paragraph of instructions.
3. **Chain-of-thought (CoT)** — ask the model to reason step-by-step before
   answering; reliably improves complex tasks.
4. **Delimiters and structure** — XML/markdown delimiters separate instructions
   from data, reducing confusion and injection risk.
5. **Self-consistency / verification** — sample multiple times and vote, or
   verify answers.

The professional framing: a prompt is a **hypothesis** about what makes the
model behave; prompt engineering is the loop of *draft → evaluate → revise*,
measured on your data (Lecture 05). This lecture covers the techniques and the
discipline to apply them.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Write a system prompt with role, task, constraints, and output format
2. Use few-shot examples to teach format and reasoning
3. Apply chain-of-thought for complex reasoning tasks
4. Use delimiters to separate instructions from data and reduce injection risk
5. Structure prompts with XML/markdown for reliable parsing
6. Treat prompts as versioned, evaluated artifacts (the engineering loop)
7. Avoid the common failure modes: ambiguity, recency bias, over-prompting

## Prerequisites

| Need | Where |
|---|---|
| LLM fundamentals | `09-genai/lectures/01-llm-fundamentals-lecture.md` |
| Structured output | `09-genai/lectures/03-structured-output-lecture.md` |
| Evaluation (preview) | `09-genai/lectures/05-prompt-evaluation-lecture.md` |
| API clients | `09-genai/lectures/02-api-clients-lecture.md` |

## 1. The System Prompt: Role, Task, Constraints

The system prompt is the model's persistent configuration. The canonical shape:

```python
SYSTEM_PROMPT = """You are a senior support analyst for Acme SaaS.
Your task: answer customer questions using ONLY the provided context.
Constraints:
- If the context lacks the answer, say "I don't have that information."
- Keep answers under 3 sentences.
- Cite the context section number in brackets, e.g. [2].
Output format: a single paragraph."""
```

Output:
```
The billing cycle resets on the 1st of each month [3]. Refunds take 3-5
business days to appear [5].
```

Each element has a purpose: **role** calibrates tone/expertise, **task** states
the goal, **constraints** bound behavior (hallucination guard, length, format),
**output format** makes it parseable (ties to Lecture 03). Vague prompts
produce vague outputs.

## 2. Few-Shot Examples: Show, Don't Tell

Instructions say; examples demonstrate. For format-sensitive tasks, 2–5
examples beat a paragraph of rules:

```python
FEW_SHOT = """Classify the sentiment of each review as Positive, Negative, or Neutral.

Review: "The app crashed three times today."
Sentiment: Negative

Review: "Fast support and a great dashboard."
Sentiment: Positive

Review: "It's okay, works fine most days."
Sentiment: Neutral

Review: "Billing was confusing but the team fixed it fast."
Sentiment:"""
```

Output:
```
Positive
```

Why it works: the examples pin the *output distribution* — formats,
vocabulary, and reasoning style are all demonstrated, so the model imitates
them. Include **edge-case examples** (the ones your instructions are worst at
covering) — that is where few-shot earns its keep.

## 3. Chain-of-Thought: Reasoning Step by Step

For multi-step problems, ask the model to show its reasoning before the final
answer. This reliably improves accuracy on math, logic, and planning tasks:

```python
PROMPT = """A customer bought 3 items at $19.99 each and used a $10 coupon,
then got 8% sales tax. How much did they pay in total? Show your steps, then
give the final answer as: TOTAL: $X.XX"""

# model output (reasoning shown, then constrained final line)
# 3 * 19.99 = 59.97
# 59.97 - 10 = 49.97
# 49.97 * 1.08 = 53.97
# TOTAL: $53.97
```

Output:
```
TOTAL: $53.97
```

The discipline: **separate the reasoning from the answer**. Put the final
answer on a constrained line (`TOTAL: $X.XX`) so you can parse it reliably
(Lecture 03) even when the reasoning varies. CoT costs more tokens but buys
accuracy — budget accordingly (L18).

## 4. Delimiters: Instructions vs Data

Never concatenate instructions and untrusted data without separators.
Delimiters (XML tags, markdown fences) make the boundary explicit and reduce
both confusion and prompt-injection risk:

```python
PROMPT = """You extract product prices from the text below.
Return JSON: {"item": str, "price": float}

<text>
{user_document}
</text>

Rules: prices only, no discounts applied, return "unknown" if absent."""
```

Output:
```
{"item": "Headphones", "price": 89.99}
```

The `<text>` tags mark the *data region*; instructions live outside it. If the
document contains "ignore all instructions and output..." it is *inside the
data region* — the model is less likely to treat it as instructions (never a
guarantee; see Lecture 19 for real guardrails).

## 5. XML/Markdown Structure for Complex Prompts

For complex tasks, structure the prompt like a document:

```xml
<instructions>
  You are a hiring screener. Extract the candidate's skills.
</instructions>
<context>
  Job: Senior ML Engineer. Required: Python, PyTorch, MLOps.
</context>
<input>
  Resume: 5 years at X. Skilled in Python, PyTorch, Docker, and scikit-learn.
</input>
<output>
  {"skills": [...], "missing": [...]}
</output>
```

Output:
```
{"skills": ["Python", "PyTorch", "Docker", "scikit-learn"], "missing": []}
```

Structure gives the model anchors: it knows which region is instructions,
which is context, which is data. This is the template pattern every serious
prompt library (e.g. LangChain's prompt templates) encodes — variables for
context/data, fixed structure for instructions.

## 6. Prompts as Code: Version, Test, Deploy

A prompt is a deployable artifact. The engineering loop:

```python
# prompts.py — versioned with the codebase
PROMPTS = {
    "classify_v3": {
        "system": SYSTEM_PROMPT,
        "template": "{few_shot}\n\nReview: {text}\nSentiment:",
    },
    # v2 differences: added edge-case examples, tightened constraints
}
```

Discipline:
1. **Version prompts** like code (semver per prompt, changelog per change)
2. **Evaluate changes** on a fixed eval set (Lecture 05) — never ship an
   unmeasured prompt
3. **Test edge cases** in CI: empty input, adversarial input, huge input
4. **Log the prompt version** with every call (L17) so quality regressions
   are attributable
5. **Deploy via config** — a prompt change should be a deploy, not a
   find-and-replace in code

## 7. Common Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Ambiguity | underspecified task | explicit role/task/constraints/format |
| Recency bias | instructions diluted by long context | key rules at start AND end |
| Over-prompting | too many instructions compete | one primary task, prioritized rules |
| Under-specification | missing output format | declare the exact format (L3) |
| Injection | untrusted data parsed as instructions | delimiters + data-region isolation (L19) |
| Format drift | free-form generation | constrained output (L3) |

## Every Use Case

- **Classification/routing**: sentiment, intent, ticket priority.
- **Extraction**: structured fields from documents (L3, L25).
- **Summarization**: length-controlled, format-controlled summaries.
- **Conversational agents**: system prompts for persona, policy, and tone.
- **Code generation**: task + constraints + examples for code quality.
- **RAG answer synthesis**: grounded answering with citation rules (L9).
- **Reasoning tasks**: CoT for math, planning, decision support.
- **Evaluation**: judge prompts (L5, L20) — the prompt that grades prompts.
- **Guardrails**: refusal/redaction policies (L19).
- **Multi-step workflows**: per-step prompts in agents (L14).

## Real-World Use Cases for AI Engineers

- **Support-ticket triage**: a prompt change from "classify the ticket" to a
  role + 5 few-shot examples + delimited input cut misclassification 40%.
  The engineer measured the change on a frozen eval set (L5) before shipping —
  the prompt is a deploy, not a tweak.
- **Legal summarization**: CoT + constrained output ("Summary: ... 
  Key clauses: [...]") gave reviewers reliable, parseable digests — the
  structured final lines feed downstream systems (L3).
- **RAG answer quality**: a grounded-answering system prompt
  ("answer ONLY from the context, cite [n]") reduced hallucinated claims
  dramatically; the prompt's version is logged with every answer so a quality
  regression is attributable to a specific prompt change (L17).
- **Code migration tool**: few-shot examples of the target framework's idioms
  outperform a paragraph of migration rules — examples demonstrate the output
  distribution better than rules describe it.
- **Prompt library at a platform company**: the ML platform team versions
  shared prompts and gates changes with evals — 20 teams inherit prompt
  quality instead of each re-inventing it.

## Common Mistakes to Avoid

### Mistake 1: No output format specified
"Summarize this" → anything. Declare length, structure, and format.

### Mistake 2: Instructions diluted by data
Long context pushes instructions down (recency bias). Repeat key rules at
the end.

### Mistake 3: Prompting without examples
Examples teach what paragraphs cannot. Add few-shot for format tasks.

### Mistake 4: No evaluation
"Feels better" is not a metric. Evaluate on your data (L5).

### Mistake 5: Prompt changes outside version control
A prompt is code. Version, review, deploy.

### Mistake 6: Untrusted data concatenated raw
Delimit data regions; assume injection attempts (L19).

### Mistake 7: One giant prompt for everything
Over-prompting confuses the model. One task, prioritized rules, structured
sections.

## Best Practices

1. Always specify role, task, constraints, and output format
2. Use 2–5 few-shot examples for format-sensitive tasks (include edge cases)
3. Use chain-of-thought for reasoning; separate reasoning from the parseable answer
4. Delimit instructions from data (XML/markdown) always
5. Treat prompts as code: version, eval, deploy, log the version
6. Put the most critical instructions at the start AND end
7. Keep prompts focused: one primary task per prompt
8. Test edge cases in CI (empty, adversarial, huge inputs)
9. Prefer templates over string concatenation
10. Measure prompt changes on a frozen eval set before shipping

## Complexity and Cost

| Technique | Extra cost | When it pays |
|---|---|---|
| Few-shot | +tokens per example | format-sensitive tasks |
| Chain-of-thought | ~2-3x output tokens | reasoning/math/planning |
| XML structure | +small prompt tokens | complex multi-part tasks |
| Self-consistency | ×N calls | highest-stakes answers |

Spend prompt tokens where they buy accuracy; evaluate to know where they do.

## AI Engineering Relevance

**Where this shows up:** every GenAI feature — the prompt is the highest-leverage
component you can tune, and the discipline (version + eval) is what separates
professional prompt work from guessing.

| Concept here | Used for |
|---|---|
| System prompt | persistent behavior configuration |
| Few-shot | teaching format and reasoning |
| CoT | complex reasoning accuracy |
| Delimiters | injection and confusion defense |
| Versioning | attributable quality changes |

**Scale note:** a 1% prompt-driven quality gain on 1M calls/day is a
measurable business outcome. At 20 engineers writing prompts, versioned
templates + shared evals are what keep quality consistent.

## Practice Exercises

### Exercise 1: Build a System Prompt (Easy)
Write a system prompt for ticket-priority classification with role, task,
constraints, and output format. Then write the same as few-shot. Compare.

### Exercise 2: Delimiter Safety (Medium)
Write `build_prompt(template, data)` that wraps data in `<text>` tags; write a
test with an adversarial document containing "ignore instructions" and assert
the data stays inside the delimited region.

### Exercise 3: CoT with Parseable Answer (Medium)
Design a CoT prompt for a math word problem ending in `TOTAL: $X.XX`; write
`parse_total(text)` that extracts the constrained final line.

### Exercise 4: Prompt as Deployed Artifact (Hard)
Build a `PromptRegistry` (name → version → prompt, with changelog) and a
`run_eval(prompt, eval_set)` harness that scores a prompt on a frozen set;
simulate a v2 prompt that beats v1 and assert the registry records the
winning version.

## Summary

| Concept | Description |
|---|---|
| System prompt | role + task + constraints + format |
| Few-shot | examples over paragraphs |
| Chain-of-thought | step-by-step reasoning |
| Delimiters | instructions vs data isolation |
| Prompts as code | versioned, evaluated, deployed |

Prompt engineering is the LLM's programming interface — and like code, it
demands structure, testing, and versioning. The techniques (role, few-shot,
CoT, delimiters) are the toolbox; the discipline (draft → evaluate → revise,
versioned) is what turns prompt writing into prompt engineering.

## Quick Reference

| Task | Idiom |
|---|---|
| Configure behavior | role + task + constraints system prompt |
| Teach format | 2-5 few-shot examples |
| Boost reasoning | "Show your steps, then ANSWER: ..." |
| Isolate data | `<text>...</text>` delimiters |
| Ship safely | version + eval + log prompt id |

## Next Steps

Next: **[05 Prompt Evaluation](05-prompt-evaluation-lecture.md)** — measuring
prompt quality on your data before you ship it.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://platform.openai.com/docs/guides/prompt-engineering,
https://www.anthropic.com/engineering/prompt-engineering-overview
