# Pipeline Orchestration — Glossary 09

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Backfill | Orchestration | Re-running historical job windows |
| Backoff | Orchestration | Growing delay between retries |
| DAG | Orchestration | Directed acyclic graph of tasks |
| Dependency | Orchestration | A task that must complete first |
| Idempotent | Orchestration | Re-running yields the same result |
| Orchestrator | Orchestration | The system running pipeline DAGs |
| Retry | Orchestration | Re-attempting a failed task |
| Task | Orchestration | A unit of pipeline work |
| Topological Sort | Orchestration | Ordering nodes by dependency |
| Transient Error | Orchestration | A failure that may succeed on retry |

## Detailed Definitions
### Backfill
**Definition**: Re-running a range of historical jobs; safe only if tasks are
idempotent.
**Related**: Idempotent

### Backoff
**Definition**: Exponentially (or otherwise) growing delay between retries to
avoid hammering a failing service.
```python
delay = base * 2 ** attempt
```
**Related**: Retry

### DAG
**Definition**: A directed acyclic graph where edges are dependencies.
**Related**: Topological Sort

### Dependency
**Definition**: A prerequisite task whose output a task consumes.
**Related**: DAG

### Idempotent
**Definition**: A task whose result is identical whether run once or many
times.
**Related**: Backfill

### Orchestrator
**Definition**: The scheduler that executes tasks in dependency order with
retries and failure handling.
**Related**: DAG

### Retry
**Definition**: Re-attempting a failed task, usually with backoff and a cap.
**Related**: Backoff

### Task
**Definition**: One unit of work in a pipeline (a function with a name).
**Related**: DAG

### Topological Sort
**Definition**: An ordering where every dependency precedes its dependents.
**Related**: DAG

### Transient Error
**Definition**: A failure (network, quota) likely to succeed on retry.
**Related**: Retry

## Key Concepts Summary
### The DAG Rules
- Dependencies first
- No cycles
- Fail loudly

### Retry Safety
- Idempotent tasks make retries and backfills safe

## Practice Terms
Match each term to its definition (answers at the bottom).
1. DAG — ___
2. Idempotent — ___
3. Backoff — ___
4. Topological sort — ___
5. Backfill — ___

**Answers:** 1-b, 2-c, 3-d, 4-e, 5-a where a=re-run history, b=task graph,
c=same result on re-run, d=growing retry delay, e=dependency-first ordering.
