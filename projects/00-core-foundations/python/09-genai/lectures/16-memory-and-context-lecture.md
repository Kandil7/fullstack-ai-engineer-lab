# GenAI — 16: Memory and Context

## Topic Overview

Memory is what lets an assistant or agent be useful *across turns*: remember
what the user said yesterday, carry a long conversation within the context
window, and recall task-relevant facts without re-asking. The fundamental
constraint is the **context window** (Lecture 1): everything the model sees at
generation time must fit in N tokens. Memory is the engineering that manages
that constraint — selecting, compressing, and persisting what matters.

The memory hierarchy, from simplest to most sophisticated:

| Layer | What it is | Used for |
|---|---|---|
| **Session context** | the current conversation's messages | multi-turn chat |
| **Truncation/summarization** | drop old messages / compress them | long conversations |
| **Working memory** | task-relevant state in an agent loop (L14) | agent steps |
| **Long-term memory** | persisted facts the user/system taught | cross-session recall |
| **Episodic/vector memory** | retrieved past interactions (embeddings, L6) | "you asked about this before" |

Why this matters: memory design *is* the quality/cost trade in conversational
and agentic products. Too little memory → the assistant forgets and re-asks
(poor UX); too much → context bloat (cost, L18) and recency-bias dilution
(L1). The professional skill is choosing what to keep, in what form, and
retrieving it when needed.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Implement message-history management (append, truncate, cap)
2. Implement conversation summarization when history overflows
3. Build a long-term memory store (facts, upserts)
4. Build episodic memory with embeddings + retrieval (L6/L9)
5. Combine memory layers into a coherent context assembler
6. Budget the context: what to include, what to drop, at what cost (L18)
7. Manage privacy: what *not* to remember and when to forget

## Prerequisites

| Need | Where |
|---|---|
| Context window | `09-genai/lectures/01-llm-fundamentals-lecture.md` |
| Embeddings | `09-genai/lectures/06-embeddings-lecture.md` |
| RAG retrieval | `09-genai/lectures/09-rag-baseline-lecture.md` |
| Agent loops | `09-genai/lectures/14-agent-patterns-lecture.md` |

## 1. Session Context: The Message Window

The baseline: keep the conversation's messages, capped at the window. The
management decisions are **what to keep** (system prompt always; recent
turns always; old turns if room) and **what to drop** (oldest first):

```python
def assemble_context(system_prompt: str, messages: list[dict], enc,
                     window: int) -> list[dict]:
    """Build the prompt: system always kept; drop oldest user/assistant turns
    until it fits."""
    out = [{"role": "system", "content": system_prompt}]
    for m in reversed(messages):                    # most recent first
        trial = [{"role": "system", "content": system_prompt}] + [m] + out[1:]
        if len(enc.encode("".join(x["content"] for x in trial))) <= window:
            out.insert(1, m)
        else:
            break
    return out
```

Output:
```
Keeps the last N turns that fit; drops the oldest — system prompt survives.
```

**Cost note (L18):** every token in the history is re-sent on *every* call —
a 20-turn chat with 8k-token history costs 8k tokens per subsequent turn. The
window management IS the cost control.

## 2. Summarization: Compression Instead of Deletion

Dropping old turns loses facts. Summarization compresses them: when history
overflows, summarize the oldest block into a compact summary that stays in
context:

```python
SUMMARY_PROMPT = """Compress the conversation into a concise summary
preserving: user preferences, resolved facts, and open questions.
Conversation:
{messages}
Summary:"""

def compress_history(old_turns: list[dict], llm_client) -> str:
    return llm_client.complete(SUMMARY_PROMPT.format(messages=old_turns))

# context = [system, summary, recent_turns]
```

Output:
```
[system, "User prefers monthly billing; resolved refund question; open:
  upgrade pricing", ...recent turns]
```

**The trade:** summarization costs one call + tokens but preserves facts and
cuts per-turn cost. The "summary + recent turns" pattern is the standard
production design for long conversations.

## 3. Long-Term Memory: Facts That Persist

Cross-session memory stores durable facts (name, preferences, account
context) keyed by user, upserted over time:

```python
import json

class FactMemory:
    """User-keyed fact store: upsert, retrieve, forget."""
    def __init__(self, path: str = "outputs/memory.json"):
        self.path = path
        self._facts: dict[str, dict] = {}
        try:
            self._facts = json.load(open(path))
        except (FileNotFoundError, json.JSONDecodeError):
            self._facts = {}

    def upsert(self, user_id: str, key: str, value: str) -> None:
        self._facts.setdefault(user_id, {})[key] = value
        json.dump(self._facts, open(self.path, "w"))

    def get(self, user_id: str, key: str) -> str | None:
        return self._facts.get(user_id, {}).get(key)

    def forget(self, user_id: str, key: str) -> None:
        self._facts.get(user_id, {}).pop(key, None)

m = FactMemory()
m.upsert("u1", "plan", "pro")
print(m.get("u1", "plan"))
```

Output:
```
pro   (persisted; next session recalls it)
```

**Privacy is a first-class method**: `forget()` isn't optional — GDPR
"right to be forgotten" and product trust both require it. Remember only
what the user would expect, and store nothing sensitive you don't need.

## 4. Episodic Memory: Retrieved Past Interactions

For "you asked about this before" recall, store past interactions as
embeddings (L6) and retrieve the relevant ones (L9):

```python
class EpisodicMemory:
    """Past interactions embedded and retrieved by similarity."""
    def __init__(self, embed_fn):
        self.embed = embed_fn
        self.items: list[tuple[str, list[float]]] = []   # (text, vector)

    def remember(self, text: str) -> None:
        self.items.append((text, self.embed(text)))

    def recall(self, query: str, k: int = 3) -> list[str]:
        qv = self.embed(query)
        scored = sorted(self.items,
                        key=lambda it: cosine_similarity(qv, it[1]),
                        reverse=True)
        return [t for t, _ in scored[:k]]

m = EpisodicMemory(embed_fn=embed_text)
m.remember("User prefers email summaries")
print(m.recall("how should I send reports?", 1))
```

Output:
```
['User prefers email summaries']   — retrieved because semantically relevant
```

Episodic memory is RAG over your own history — the same retrieval discipline
(L10) applies, and the same cost model (embedding + search, L18).

## 5. Assembling the Context: The Layered Prompt

Production systems combine the layers. The assembler decides, per call, what
to include — ordered by importance and budgeted by tokens:

```python
def assemble_full_context(user_id: str, messages: list[dict], fact_memory,
                          episodic, system_prompt, enc, window: int) -> list[dict]:
    """Layer: system + facts + episodic recalls + summarized history +
    recent turns — all inside the window."""
    facts = "\n".join(f"- {k}: {v}" for k, v in fact_memory.get_all(user_id).items())
    recalls = episodic.recall(messages[-1]["content"], k=2)
    summary = load_or_build_summary(user_id)          # from compression step
    blocks = [system_prompt, f"User facts:\n{facts}",
              f"Prior context:\n{summary}", f"Related past: {recalls}"]
    # ... include recent turns last (recency bias, L1) ...
    return trim_to_window(blocks, messages, enc, window)
```

Output:
```
[system, user facts, prior summary, related past, ...recent turns]
```

**Ordering principle (L1 recency bias):** the most recent and most important
instructions go last; durable background (facts, summary) goes first.

## 6. Budgeting Memory: What It Costs

Every memory layer has a cost (L18) — the budget table:

| Layer | Per-call cost | Value |
|---|---|---|
| Recent turns | tokens × every call | conversation coherence |
| Summary | 1 compression call + tokens/call | long-chat facts |
| Facts | small, always | continuity |
| Episodic recall | embed query + 2-3 chunks | "remembered" UX |
| Full history (unbounded) | huge, every call | rarely worth it |

```python
def memory_budget(facts: int, summary: int, turns: int, recent: int,
                  window: int) -> tuple[bool, int]:
    used = facts + summary + turns + recent
    return used <= window, used
```

Output:
```
(True, 4100) — within an 8k window; the assembler keeps it there by design.
```

## Every Use Case

- **Long-running support chats**: summary + recent turns.
- **Personal assistants**: facts (preferences) + episodic (past requests).
- **Agent loops (L14)**: working memory = the step trace + state.
- **RAG + memory hybrid**: memory recalls + retrieved docs in one context.
- **Compliance-bound products**: forgetting on demand, audit of what's stored.
- **Code assistants**: remember project conventions across turns.
- **Sales/CRM copilots**: client facts + conversation history.
- **Health/coaching apps**: longitudinal user context (with consent + privacy).

## Real-World Use Cases for AI Engineers

- **Support chat (fintech)**: 40-turn conversations with a summary + recent
  turns pattern — the assistant remembers the whole thread for 30% of the
  per-turn cost of full history. The compression call is amortized across
  turns; cost-per-conversation dropped measurably (L18).
- **Personal finance copilot**: fact memory stores goals and preferences
  ("prefers biweekly summaries"); episodic memory recalls "you asked about
  mortgage refinancing in March." The user feels remembered; the context
  stays small.
- **CRM assistant**: salespeople get a context assembler that layers client
  facts + last conversation + current question — a 2-token-call budget per
  call, tuned with the L18 dashboard.
- **Compliance (GDPR)**: the memory store exposes `forget(user_id)` as a
  product feature, and the storage log is the audit evidence. The engineer
  designed privacy in — not as an afterthought.
- **Agent platform**: agents persist working memory between steps and
  sessions; a crashed long-running agent resumes from its persisted context
  (L14) instead of starting over.

## Common Mistakes to Avoid

### Mistake 1: Stuffing full history into every call
```
# WRONG — 8k-token history × every turn = cost blowup + diluted instructions
# CORRECT — summary + recent turns
```

### Mistake 2: Dropping old turns without summarizing
Facts die with the dropped turns. Compress, don't just delete.

### Mistake 3: Forgetting recency bias in ordering
Instructions buried in the middle get diluted. Durable context first,
critical instructions last.

### Mistake 4: No privacy controls
Storing what users expect forgotten is a compliance incident. `forget()` +
storage audit.

### Mistake 5: Unbounded fact growth
Ten thousand facts per user = token bloat. Curate facts; keep only durable ones.

### Mistake 6: Memory without eviction policy
Summaries age too. Re-summarize or expire stale memory.

### Mistake 7: No cost visibility per memory layer
Layers add tokens; measure the budget per layer (L18).

## Best Practices

1. Cap the session window; drop oldest first (system prompt survives)
2. Summarize overflow instead of just deleting
3. Persist durable facts; curate their growth
4. Use episodic (vector) memory for "you mentioned X before" recall
5. Assemble context in layers: system → facts → summary → recalls → recent
6. Order by importance + recency (L1 recency bias)
7. Budget tokens per layer and per call (L18)
8. Design privacy in: consent, forget, storage audit
9. Persist agent working memory for crash recovery (L14)
10. Evaluate memory value: does recalling it improve the L20 metrics?

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Truncate window | O(n) | O(n) | — |
| Summarize overflow | 1 call | O(summary) | only when overflow |
| Fact upsert | O(1) | O(facts) | — |
| Episodic recall | embed + search | O(history) | k=2-3, capped |
| Full context assemble | O(blocks) | O(window) | budget by design |

## AI Engineering Relevance

**Where this shows up:** every conversational product, every agent with state,
every assistant that should "remember." Memory is the quality/cost frontier —
the design choice between "remembers everything (expensive)" and "forgets
everything (useless)."

| Concept here | Used for |
|---|---|
| Window management | cost + coherence |
| Summarization | facts without bloat |
| Facts + episodic | cross-session continuity |
| Context assembly | layered, budgeted prompts |
| Privacy | forgetting as a feature |

**Scale note:** at 1M conversations/day, a 50% history-truncation saving is a
real monthly line item (L18). Memory design is where conversational cost is
won or lost — and where user trust (privacy) is kept or broken.

## Practice Exercises

### Exercise 1: Window Truncation (Easy)
Implement `assemble_context` (section 1) and assert the system prompt always
survives and the oldest turns drop first.

### Exercise 2: Summarize Overflow (Medium)
Build `compress_history` with a mock LLM; test that a full conversation
becomes [system, summary, recent] and fits the window.

### Exercise 3: Fact Memory (Medium)
Implement `FactMemory` with upsert/get/forget; test persistence across two
instances and that `forget` removes the fact.

### Exercise 4: Context Assembler (Hard)
Build `assemble_full_context` with all four layers and a token budget; assert
the assembled context fits the window, includes facts + recalls, orders
durable-first, and that budget overflow is handled (drop recalls before
system prompt).

## Summary

| Concept | Description |
|---|---|
| Window management | cap + drop oldest |
| Summarization | compress instead of delete |
| Facts | durable cross-session memory |
| Episodic | retrieved past interactions |
| Layered assembly | system → facts → summary → recalls → recent |
| Privacy | forget as a designed feature |

Memory is the engineering of context: what to keep, in what form, and what it
costs. The layered assembler — system, facts, summary, episodic recalls,
recent turns — delivers continuity within the window's budget, and the
discipline of compression, curation, and forgetting keeps both cost (L18)
and trust in check.

## Quick Reference

| Task | Idiom |
|---|---|
| Cap history | drop oldest, keep system |
| Compress | summarize overflow block |
| Persist | FactMemory.upsert / get / forget |
| Recall | episodic: embed + cosine top-k |
| Assemble | system → facts → summary → recalls → recent |

## Next Steps

Next: **[17 LLM Observability](17-llm-observability-lecture.md)** — logging,
tracing, and monitoring the LLM layer in production.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://www.langchain.com/langsmith,
https://docs.llamaindex.ai/en/stable/observability/overview.html
