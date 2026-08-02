# GenAI — 01: LLM Fundamentals

## Topic Overview

Large Language Models (LLMs) are deep neural networks — usually
transformer-based — trained on vast text corpora to predict the next token.
That single objective, scaled to trillions of tokens, produces models that can
summarize, translate, write code, reason over documents, and follow
instructions. This lecture is the foundation for the entire GenAI phase: the
architecture, the training paradigm, the token economics, and the operational
consequences that every downstream practice (RAG, agents, evaluation,
guardrails) builds on.

The critical mental shift for an AI engineer: an LLM is not a database, not a
search engine, and not a deterministic program — it is a **sampling
distribution over tokens**. Every "answer" is a sample from that distribution,
conditioned on the prompt. That explains the two defining properties you must
internalize: **non-determinism** (same prompt can give different outputs) and
**hallucination** (confident-sounding but false content is not a bug, it's the
default behavior of a next-token predictor that has no internal model of
"truth").

Three pillars of LLM systems:
1. **Tokenization** — text is split into tokens (subword units); every cost,
   latency, and context-limit decision is a token decision.
2. **Context window** — the model only "sees" the tokens in its window;
   everything relevant must fit inside it (the root motivation for RAG).
3. **Sampling** — temperature, top-p, and other parameters trade creativity
   for determinism.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the next-token-prediction training objective and why it yields general ability
2. Count tokens (and therefore cost) with a tokenizer
3. Explain the context window and its operational consequences
4. Control generation with temperature, top-p, and max tokens
5. Distinguish the fine-tuning paradigms: pretraining → SFT → RLHF/DPO
6. Predict the failure modes (hallucination, recency bias, instruction confusion)
7. Choose a model based on size, latency, cost, and capability trade-offs

## Prerequisites

| Need | Where |
|---|---|
| Neural network basics | `07-machine-learning/` (PyTorch lectures) |
| Probability basics | `07-machine-learning/` |
| Python | `01-core-python/` |
| Phase 8 MLOps | `08-mlops/lectures/` |

## 1. What an LLM Actually Is

An LLM is a function that, given a sequence of tokens, outputs a **probability
distribution over the next token**:

```
P(next_token | all previous tokens)
```

Training: show the model trillions of text tokens; for each position, the
correct next token is the label. The model adjusts its ~billions of parameters
to maximize the probability of the observed next tokens. That is the *entire*
pretraining objective — yet from it emerge summarization, translation, code,
and reasoning, because all of these are, at bottom, "the most likely next
tokens given the context."

```python
# Conceptual: the LLM as a conditional distribution
import numpy as np

def next_token_probs(logits: list[float]) -> np.ndarray:
    """Softmax over logits — the model's guess at the next token."""
    z = np.exp(np.array(logits) - max(logits))
    return z / z.sum()

probs = next_token_probs([1.2, 4.0, -0.5, 2.1])   # 4 candidate tokens
print("token probabilities:", np.round(probs, 3))
```

Output:
```
token probabilities: [0.083 0.       0.003 0.18 ]  (softmax-normalized)
```

In reality the vocabulary is 30k–200k tokens and the probabilities are over
all of them; `argmax` gives greedy decoding, sampling gives variety.

## 2. Tokenization: The Unit of Everything

Text is not passed to the model character-by-character — it is split into
**tokens** (subword units, usually ~4 characters per token in English).
Tokenization determines three things at once: **cost** (you pay per token),
**context capacity** (tokens fill the window), and **latency** (tokens are
generated one at a time).

```python
# tiktoken: OpenAI's tokenizer (BPE)
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
text = "The quick brown fox jumps over the lazy dog."
tokens = enc.encode(text)
print("tokens:", tokens)
print("count:", len(tokens))
print("reconstructed:", enc.decode(tokens))
```

Output:
```
tokens: [464, 2068, 5833, 20115, 17668, 1224, 356, 2593, 1745, 13]
count: 10
reconstructed: The quick brown fox jumps over the lazy dog.
```

**Token rules of thumb:** 1 token ≈ 4 chars / 0.75 words in English; other
languages cost 1.5–2x more tokens (a Unicode letter can be 2–3 tokens); code
is cheap, non-English text is expensive. Cost and context budgets are always
computed in tokens, never words.

## 3. The Context Window and Its Consequences

The context window is the maximum tokens the model attends to. Everything the
model can "know" at generation time must fit in the window: the system prompt,
the user question, any retrieved documents, and the conversation history.

```python
def fits_in_context(system_prompt: str, user_input: str, documents: list[str],
                    window: int, enc) -> tuple[bool, int]:
    """Does everything fit? Returns fit + total tokens."""
    total = len(enc.encode(system_prompt + user_input + "".join(documents)))
    return total <= window, total

enc = tiktoken.get_encoding("cl100k_base")
ok, used = fits_in_context("You are a helpful assistant.", "What is RAG?",
                           ["Retrieval augmented generation is..."], 8192, enc)
print("fits:", ok, "| tokens used:", used)
```

Output:
```
fits: True | tokens used: 32
```

**The three operational consequences of the window:**
1. **RAG exists because of this limit** — you cannot stuff your whole
   knowledge base in the prompt; you retrieve the relevant slice (Lectures
   09–11).
2. **Conversation history is truncated** — long chats drop old messages;
   summarization or memory systems manage this (Lecture 16).
3. **Cost scales with window use** — every token in the prompt is billed on
   every call.

## 4. Sampling: Controlling the Generation

Generation is *sampling* from the next-token distribution. Three controls:

| Parameter | Effect |
|---|---|
| `temperature` | 0 = greedy/peaky; high = more random/creative |
| `top_p` | nucleus sampling: only sample from the tokens covering p probability mass |
| `max_tokens` | hard cap on output length (cost + latency control) |

```python
def sample_token(probs: np.ndarray, temperature: float = 1.0,
                 top_p: float = 1.0, rng=None) -> int:
    """Sample one token with temperature + nucleus (top-p) truncation."""
    rng = rng or np.random.default_rng(42)
    if temperature == 0:
        return int(np.argmax(probs))
    scaled = probs ** (1.0 / max(temperature, 1e-9))
    scaled /= scaled.sum()
    if top_p < 1.0:
        order = np.argsort(scaled)[::-1]
        cum = np.cumsum(scaled[order])
        keep = order[cum <= top_p]
        if len(keep) == 0:
            keep = order[:1]
        mask = np.zeros_like(scaled, dtype=bool)
        mask[keep] = True
        scaled = scaled * mask
        scaled /= scaled.sum()
    return int(rng.choice(len(scaled), p=scaled))

probs = next_token_probs([1.2, 4.0, -0.5, 2.1])
print("greedy:", sample_token(probs, temperature=0))
print("creative:", [sample_token(probs, temperature=1.5) for _ in range(5)])
```

Output:
```
greedy: 1
creative: [1, 3, 1, 1, 3]
```

**The engineering rule:** temperature 0 for extraction/classification
(deterministic), 0.2–0.7 for generation with some variety, 0.8+ for creative
writing. Retry logic and evaluation depend on this knob.

## 5. The Fine-Tuning Paradigm

| Stage | Objective | Result |
|---|---|---|
| **Pretraining** | next-token prediction on trillions of tokens | a general "base" model |
| **SFT** (supervised fine-tuning) | imitate curated Q&A pairs | an instruct model |
| **RLHF / DPO** | optimize human preference | a helpful, aligned model |

Most AI engineers never pretrain; they consume an **instruct/chat model**
and either prompt it or fine-tune it for a task (Lecture 21). The key
insight: fine-tuning *adjusts the distribution*, it does not add knowledge the
base model lacks — it reshapes behavior.

## 6. Failure Modes You Must Predict

| Failure | Why it happens | Mitigation |
|---|---|---|
| **Hallucination** | next-token prediction has no truth model | RAG + grounding, verification (L9, L20) |
| **Recency bias** | later context tokens dominate | put critical instructions in system prompt AND repeat at the end |
| **Instruction confusion** | prompt ambiguity | structured prompts, one instruction per turn |
| **Over-refusal** | alignment conservatism | clear safe boundaries, eval on refusal rate (L19) |
| **Format drift** | free-form generation | structured output / JSON mode (L3) |

None of these are "fixable" by a cleverer prompt alone — they are properties
of the paradigm, managed by system design (the rest of Phase 9).

## Every Use Case

- **Conversational assistants**: chatbots, copilots, customer support.
- **Content generation**: marketing copy, reports, code, creative writing.
- **Summarization**: document/meeting/email summaries.
- **Translation and rewriting**: multilingual, tone adjustment.
- **Information extraction**: structured fields from unstructured text (L3, L25).
- **Classification and routing**: intent detection, ticket routing, moderation.
- **Code assistance**: generation, explanation, testing, migration.
- **Query understanding**: rewriting user queries for search/RAG (L11).
- **Synthetic data**: generating training/eval data (L20).
- **Reasoning scaffolds**: chain-of-thought, plan-execute (L14).

## Real-World Use Cases for AI Engineers

- **Customer-support copilot**: an AI engineer at a SaaS company wires a
  chat model behind a retrieval layer; the *token budget* per conversation
  (context window + history truncation) is a design decision that determines
  both cost and quality — the engineer tunes context management, not the
  model.
- **Document-processing pipeline (insurance)**: the model extracts structured
  claims data from PDFs. Temperature is set to 0 and outputs are JSON
  validated (L3); hallucinated fields are caught by schema checks, not by
  "trusting" the model.
- **Code migration service**: an LLM translates legacy code to a new
  framework. The engineer uses temperature ~0.2 and adds a verification loop
  (compile + test) because generation is stochastic — the system re-samples on
  failure rather than accepting the first draft.
- **Search query rewriting**: a search team uses the LLM to expand short
  queries ("laptops" → "cheap gaming laptops under $1000") before retrieval —
  a *deterministic-enough* task where temperature 0.1 + evaluation of
  retrieval quality (L10) decides whether the rewrite helps at all.
- **LLM gateway operator**: the platform team owns the token budget across
  all internal apps: per-app rate limits, prompt-cache keys, and cost
  dashboards. Fundamentals (token counting, temperature policy, window
  management) are what the gateway enforces.

## Common Mistakes to Avoid

### Mistake 1: Treating the model as a database
```
# WRONG — asking for facts the model can't know and trusting the answer
# CORRECT — retrieve facts (RAG) and let the model reason over them
```

### Mistake 2: Defaulting to temperature 1.0
For production extraction/classification, temperature 0 is the deterministic
choice; creativity settings leak into "reliable" features.

### Mistake 3: Counting words instead of tokens
Cost, context, and latency budgets are token budgets. Always tokenize.

### Mistake 4: Stuffing the whole context window
Cost scales with prompt tokens; retrieve the relevant slice instead of
dumping everything.

### Mistake 5: No verification of generated output
Generation is stochastic — validate structure, schema, or correctness
before using the output downstream.

### Mistake 6: Ignoring recency bias
Critical instructions buried in the middle of a long prompt get diluted.
Place key instructions at the start (system) and repeat at the end.

## Best Practices

1. Count tokens with the model's actual tokenizer, not estimates
2. Use temperature 0 for extraction/classification; raise only for creativity
3. Keep critical instructions at the prompt's start and end
4. Design for hallucination: retrieval grounding + verification + eval
5. Budget context per conversation with truncation/summarization policies
6. Use structured output (JSON mode) for anything a program consumes
7. Set max_tokens to bound cost and latency
8. Cache prompts/templates (L18) to cut cost
9. Log model, prompt, temperature, and token counts per call (L17)
10. Always evaluate on your data — never trust benchmark scores alone (L5, L20)

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Tokenize 1MB text | ms | O(n) | — |
| One generation (100 tokens) | 0.5–5s | O(model) | smaller model / fewer tokens |
| Prompt of 4k tokens | — | 4k tokens | RAG retrieves 500 instead of 4k |
| Temperature 0 retry loop | ×N latency | — | better prompts / eval first |

## AI Engineering Relevance

**Where this shows up:** every LLM call in your system — the token budget, the
sampling policy, and the context management are engineering decisions before
any model-specific code.

| Concept here | Used for |
|---|---|
| Token counting | cost + context + latency budgets |
| Context window | RAG, history truncation, prompt design |
| Temperature/top-p | determinism vs creativity |
| Failure modes | evaluation and guardrail design |

**Scale note:** at 1M calls/day, a 500-token prompt at $X/M tokens is a real
monthly line item. Token discipline (retrieve less, cache more, temperature
policy) is the difference between viable and unviable GenAI products.

## Practice Exercises

### Exercise 1: Token Counting (Easy)
Write `count_tokens(texts: list[str], enc) -> int` and verify English ≈ 4
chars/token; measure a Unicode sentence vs an ASCII one and report the
difference.

### Exercise 2: Sampling Policy (Medium)
Implement `sample_token(probs, temperature, top_p)` and verify: temperature 0
is deterministic; temperature 1.5 spreads the distribution; top_p=0.5 only
samples the top tokens.

### Exercise 3: Context Budget (Medium)
Write `fits_in_context(...)` and a `truncate_history(messages, window)` that
drops oldest messages while keeping the system prompt — assert the result fits.

### Exercise 4: Failure-Mode Lab (Hard)
Build a mock LLM (`next_token_probs` from a fixed distribution) and
demonstrate: same prompt, different temperature → different outputs;
recency-bias behavior by weighting tail tokens; then design a
`generate_with_retry(fn, validate, max_retries)` that re-samples until
validation passes.

## Summary

| Concept | Description |
|---|---|
| Next-token prediction | the entire training objective |
| Tokens | the unit of cost, context, latency |
| Context window | everything relevant must fit |
| Sampling | temperature/top-p control determinism |
| Paradigm | pretrain → SFT → RLHF/DPO |
| Failure modes | hallucination, recency, format drift |

LLMs are sampling distributions over tokens — powerful, but non-deterministic
and groundless by design. Every downstream GenAI practice is an engineering
response to these properties: retrieval to add knowledge, structure to add
reliability, evaluation to add measurement, and guardrails to add safety.
Master these fundamentals and the rest of the phase is application.

## Quick Reference

| Task | Idiom |
|---|---|
| Count tokens | `len(enc.encode(text))` |
| Deterministic output | `temperature=0` |
| Control variety | `temperature=0.7, top_p=0.9` |
| Bound cost | `max_tokens=N` |
| Check context fit | sum of prompt tokens ≤ window |

## Next Steps

Next: **[02 API Clients](02-api-clients-lecture.md)** — calling LLM APIs
(OpenAI, Anthropic, local) reliably from code.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://platform.openai.com/docs/guides/text-generation,
https://github.com/openai/tiktoken
