# GenAI — 15: Multi-Agent

## Topic Overview

Multi-agent systems coordinate **multiple specialized agents** — each with its
own role, tools, and prompt — to complete tasks no single agent does well:
research that spans domains, workflows that need parallel work, or complex
tasks that benefit from division of labor. The canonical architecture is the
**orchestrator/worker** pattern: a planner agent decomposes the task, dispatches
workers (research, code, analysis), and a synthesizer merges results.

Why multi-agent at all? Three reasons: **expertise** (a "security agent" has a
narrower, better-tuned prompt than a generalist), **parallelism** (independent
sub-tasks run concurrently, cutting wall-clock), and **composability** (adding
a capability = adding an agent, not rewriting one). But multi-agent also
multiplies cost, latency, and failure surface — so the senior rule is: *start
single-agent; go multi-agent only when a measured single-agent ceiling
justifies it* (L20 evaluation decides).

The engineering pillars: **task decomposition** (splitting well), **message
contracts** (how agents communicate — structured output, L3), **lifecycle
management** (spawn, monitor, kill, budget), and **failure handling** (one
worker failing must not kill the system).

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the orchestrator/worker architecture and when it earns its complexity
2. Decompose tasks into dispatchable units with a planner
3. Define message contracts between agents (L3 structured output)
4. Run workers in parallel and merge results deterministically
5. Handle worker failures (retry, quarantine, degrade) without killing the system
6. Budget the whole system (steps, tokens, cost per agent — L14/L18)
7. Evaluate multi-agent vs single-agent and decide with numbers (L20)

## Prerequisites

| Need | Where |
|---|---|
| Agent patterns | `09-genai/lectures/14-agent-patterns-lecture.md` |
| Tool calling | `09-genai/lectures/13-tool-calling-lecture.md` |
| Structured output | `09-genai/lectures/03-structured-output-lecture.md` |
| Evaluation | `09-genai/lectures/20-evaluation-frameworks-lecture.md` |

## 1. The Orchestrator/Worker Architecture

```
               ┌──────────  orchestrator (planner) ──────────┐
               │  decompose task → dispatch → synthesize      │
               └──────┬──────────┬──────────┬──────────┬──────┘
                      ▼          ▼          ▼          ▼
                   worker A   worker B   worker C   worker D
                  (research)  (code)    (analysis)  (writing)
                      └──────────┴──────────┴──────────┘
                       results → orchestrator synthesizes
```

The orchestrator owns the plan; workers own execution. The orchestrator's
three jobs: **decompose** (task → sub-tasks), **dispatch** (which worker gets
what), **synthesize** (merge results into the final answer).

```python
def orchestrator(task: str, workers: dict, llm_client, max_steps: int = 6) -> str:
    plan = decompose(task, llm_client)                # L3 JSON: sub-tasks + worker
    results = {}
    for sub in plan["subtasks"]:                      # (parallelize in prod)
        results[sub["id"]] = workers[sub["worker"]](sub["instruction"])
    return synthesize(task, plan, results, llm_client)
```

Output:
```
Decompose "market analysis" → [research competitors, analyze pricing, draft
report] → workers run → orchestrator merges into the final report.
```

## 2. Task Decomposition: The Quality Bottleneck

The orchestrator is only as good as its plan. Decomposition must produce:
**complete** sub-tasks (nothing dropped), **independent** sub-tasks (no hidden
dependencies — or explicit ordering), and **dispatchable** units (each worker
has the tools for its unit).

```python
DECOMPOSE_PROMPT = """Decompose the task into independent sub-tasks, each
assignable to ONE worker. Output JSON:
{"subtasks": [{"id": "s1", "worker": "research", "instruction": "..."}]}
Workers available: {worker_names}. Task: {task}"""

# validation: every sub-task's worker exists; instructions are non-empty
```

Output:
```
{"subtasks": [{"id": "s1", "worker": "research", "instruction": "Gather Q2 market size"},
              {"id": "s2", "worker": "analysis", "instruction": "Compute growth rate"}]}
```

**Validation rule:** the plan is parsed and validated (L3) — unknown worker →
re-plan or fail loudly, never dispatch garbage.

## 3. Message Contracts Between Agents

Agents communicate via **structured messages**, not prose. Each worker returns
a typed result (L3 discipline) so the orchestrator can merge reliably:

```python
from pydantic import BaseModel

class WorkerResult(BaseModel):
    worker: str
    subtask_id: str
    summary: str
    data: dict = {}
    citations: list[str] = []

def worker_result(worker: str, subtask_id: str, summary: str, **kw) -> WorkerResult:
    return WorkerResult(worker=worker, subtask_id=subtask_id,
                        summary=summary, **kw)
```

Output:
```
WorkerResult(worker='research', subtask_id='s1', summary='Q2 market: $4.2B',
             citations=['src3'], data={...})
```

**Why contracts matter:** the orchestrator merges results; unstructured prose
from 4 workers is unmergeable and un-debuggable. Typed results (with
citations!) are what make the final synthesis grounded (L9) and auditable.

## 4. Parallelism and Deterministic Merging

Independent sub-tasks run concurrently (asyncio/threads/processes); the merge
order must be deterministic so the system is reproducible (Phase 8 L1):

```python
import asyncio

async def run_parallel(workers: dict, subtasks: list) -> list[WorkerResult]:
    """Run independent sub-tasks concurrently; merge in plan order."""
    async def run(s):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, workers[s["worker"]], s["instruction"])
    results = await asyncio.gather(*(run(s) for s in subtasks))
    # deterministic merge: sort by plan order (subtask_id)
    return sorted(results, key=lambda r: r.subtask_id)
```

Output:
```
All workers finish concurrently; results merged in subtask_id order —
reproducible across runs.
```

## 5. Failure Handling: One Worker Down ≠ System Down

Workers fail — a tool times out, a research source is empty. The system
designs for it:

| Failure | Policy |
|---|---|
| Worker returns empty/invalid result | retry once, then quarantine that sub-task |
| Worker crashes | re-dispatch to a fallback worker |
| Tool fails (L13) | error fed back to the worker (self-correct) |
| Orchestrator plan invalid | re-plan once, then abort with a clear message |
| Budget exceeded | kill the whole system, return partial results + alert |

```python
def run_with_retry(worker_fn, instruction, retries: int = 2) -> WorkerResult:
    for attempt in range(retries + 1):
        try:
            res = worker_fn(instruction)
            if res.summary.strip():
                return res
            raise ValueError("empty worker result")
        except Exception as e:
            if attempt == retries:
                return WorkerResult(worker="?", subtask_id="?",
                                    summary=f"FAILED: {e}")
    raise RuntimeError("unreachable")
```

Output:
```
Worker flaky → retried → succeeds, or → quarantined with a clean FAILED result
the orchestrator can degrade around.
```

**The orchestrator degrades gracefully**: a failed sub-task becomes a
"not available" section in the final answer — never a crash.

## 6. Budgets and Lifecycle

Multi-agent multiplies cost (L18). One shared budget across the system:

```python
class MultiAgentBudget:
    def __init__(self, per_agent_steps: int = 5, max_total_tokens: int = 50_000):
        self.per_agent_steps = per_agent_steps
        self.total_tokens = 0
        self.max_total_tokens = max_total_tokens

    def spend(self, tokens: int) -> bool:
        self.total_tokens += tokens
        return self.total_tokens <= self.max_total_tokens
```

Output:
```
System-wide token budget; agents are killed (with partial results) when spent.
```

**Lifecycle discipline:** every agent is spawned with a budget, monitored
(step counter + token counter), and killed on budget breach — a "runaway
worker" must never drag the whole system over budget.

## 7. When Multi-Agent Earns Its Complexity

The decision is measured, not fashionable:

```python
def decide_single_vs_multi(single_score: float, multi_score: float,
                           cost_ratio: float, threshold: float = 0.05) -> str:
    """Choose multi-agent only if it beats single by more than threshold
    despite the cost ratio."""
    gain = multi_score - single_score
    return ("multi-agent" if gain >= threshold and cost_ratio < 3.0
            else "single-agent")

print(decide_single_vs_multi(0.80, 0.86, 2.5))
```

Output:
```
'multi-agent'   (+6 points for 2.5x cost — worth it)
# if gain were +2 points → 'single-agent' (cost not justified)
```

The L20 eval scoreboard + L18 cost accounting decide. Multi-agent is a tool,
not a status symbol.

## Every Use Case

- **Deep research**: parallel research workers + synthesis.
- **Complex coding**: planner + code/test/review agents.
- **Content pipelines**: research → outline → draft → edit agents.
- **Business analysis**: data + market + writing workers.
- **Support escalation**: triage agent → specialist agents (billing, tech).
- **Regulated workflows**: orchestrator + state-machine workers (L14).
- **Competitor monitoring**: parallel watchers + report synthesis.
- **RAG augmentation**: multiple retrieval workers (by source) merged.

## Real-World Use Cases for AI Engineers

- **Investment research**: an orchestrator dispatches 4 research workers
  (market data, filings, news, analyst notes) in parallel and synthesizes a
  grounded report with per-claim citations. Wall-clock dropped 4x vs
  single-agent; the typed worker results (L3) make citations verifiable.
- **Enterprise support**: a triage agent routes to specialist workers; a
  billing worker's failure degrades to "billing specialist will follow up"
  instead of a failed ticket — the graceful-degradation pattern is what
  keeps the system shippable.
- **Content marketing**: plan → research → draft → SEO-edit agents cut a
  report's production from days to hours; the eval (L20) showed multi-agent
  beat single-agent on completeness by 9 points — the numbers, not the hype,
  justified the architecture.
- **Compliance monitoring**: a compliance copilot runs parallel workers per
  regulation domain and synthesizes findings with citations — the
  orchestrator's deterministic merge is what makes the daily report
  reproducible (Phase 8 L1).
- **Startup**: 2 engineers use a 3-worker orchestrator for sales research;
  the system-wide budget keeps a runaway research worker from blowing the
  monthly LLM bill (L18).

## Common Mistakes to Avoid

### Mistake 1: Multi-agent because it sounds impressive
Single-agent that works beats multi-agent that impresses. Measure (L20).

### Mistake 2: No message contracts
Unstructured worker prose is unmergeable. Typed WorkerResult (L3).

### Mistake 3: No system-wide budget
Cost multiplies per agent. One shared budget + lifecycle kills.

### Mistake 4: Non-deterministic merging
Parallel results merged in nondeterministic order break reproducibility.
Sort by plan order.

### Mistake 5: Whole-system crash on one worker failure
Quarantine + degrade; never let one worker kill the system.

### Mistake 6: Unvalidated plans
Unknown worker names dispatch garbage. Validate the plan (L3).

### Mistake 7: Ignoring wall-clock savings
Parallelism is a real win — but measure it; on sequential hardware the
"parallel" system can be slower.

## Best Practices

1. Start single-agent; go multi only when the L20 scoreboard justifies it
2. Orchestrator owns the plan; workers own execution
3. Validate decomposition (workers exist, instructions non-empty)
4. Use typed message contracts (L3) with citations
5. Run independent workers in parallel; merge deterministically
6. Design failure handling: retry → quarantine → degrade
7. One system-wide budget with lifecycle management
8. Log the full orchestration trace (L17) for audit and debugging
9. Evaluate completion + efficiency vs single-agent (L20)
10. Keep worker prompts specialized and narrow (expertise is the point)

## Complexity and Cost

| Dimension | Single-agent | Multi-agent |
|---|---|---|
| Calls per task | 2-8 | 5-25+ |
| Wall-clock | sequential | parallel (if independent) |
| Cost | 1x | 2-4x (L18) |
| Failure surface | one loop | N loops + orchestration |
| Audit | one trace | N traces + plan |

## AI Engineering Relevance

**Where this shows up:** research, support, content, code, and analysis
systems that outgrow a single agent. Multi-agent is the composition layer —
and the discipline (contracts, budgets, failure handling, evaluation) is what
keeps the composition reliable.

| Concept here | Used for |
|---|---|
| Orchestrator/worker | division of labor |
| Message contracts | reliable communication |
| Parallel + deterministic merge | speed without chaos |
| Budgets + degradation | cost and failure control |
| Measured decision | single vs multi by the numbers |

**Scale note:** at high volume, parallel workers hit provider rate limits —
budget concurrency; at any scale, the orchestrator's trace is the audit
artifact (L17/L24). Multi-agent complexity only earns its keep when the eval
says so.

## Practice Exercises

### Exercise 1: Plan Validation (Easy)
Write `validate_plan(plan, worker_names)` asserting every sub-task's worker
exists; test unknown-worker and empty-instruction rejections.

### Exercise 2: Deterministic Merge (Medium)
Implement `merge_in_order(results, plan)` sorting by subtask_id; assert the
merge is identical across two shuffled result orderings.

### Exercise 3: Graceful Degradation (Medium)
Implement `run_with_retry` and test: success, transient failure → retry →
success, and persistent failure → quarantined FAILED result.

### Exercise 4: Decision + Budget (Hard)
Build `decide_single_vs_multi` + a `MultiAgentBudget`; simulate a task where
multi wins (gain > threshold, cost ratio ok) and one where it doesn't —
assert both decisions, and assert the budget kills the system on breach.

## Summary

| Concept | Description |
|---|---|
| Orchestrator/worker | plan, dispatch, synthesize |
| Contracts | typed, citable worker results |
| Parallelism | speed, deterministic merge |
| Failure handling | retry → quarantine → degrade |
| Measured decision | single vs multi by eval + cost |

Multi-agent systems divide labor across specialized agents — winning on
expertise, parallelism, and composability — at the price of multiplied cost
and failure surface. The professional practice is discipline-first:
contracts, budgets, graceful degradation, and an eval that decides whether
the complexity earns its keep.

## Quick Reference

| Task | Idiom |
|---|---|
| Decompose | L3 JSON plan: sub-tasks + workers |
| Dispatch | worker per sub-task, parallel |
| Merge | sort by subtask_id (deterministic) |
| Fail | retry → quarantine → degrade |
| Decide | eval gain vs cost ratio (L20/L18) |

## Next Steps

Next: **[16 Memory and Context](16-memory-and-context-lecture.md)** — giving
agents and assistants persistence across turns.
Continues in: **[Phase 9 — GenAI](../../09-genai/README.md)**.
Official docs: https://www.anthropic.com/research/building-effective-agents
