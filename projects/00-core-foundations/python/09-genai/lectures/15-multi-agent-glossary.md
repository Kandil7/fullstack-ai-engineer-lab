# Multi-Agent — Glossary 15

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Agent | System | An LLM with role, tools, and a loop |
| Fan-Out | Cost | Spawning many parallel agents |
| Handoff | Coordination | Passing a task with a contract between agents |
| Orchestrator | Topology | The central controller delegating work |
| Peer-to-Peer | Topology | Agents messaging each other directly |
| Shared State | Coordination | A registry deduplicating effort |
| Worker | Topology | A specialist agent executing subtasks |

## Detailed Definitions
### Agent
**Definition**: A model configured with a role, tools, and an execution loop.
**Related**: Worker

### Fan-Out
**Definition**: Parallel delegation to many agents; scales work and cost.
**Related**: Orchestrator

### Handoff
**Definition**: A message transferring a task with context and an output
contract.
**Related**: Orchestrator

### Orchestrator
**Definition**: The central agent that decomposes goals and assigns subtasks.
**Related**: Worker

### Peer-to-Peer
**Definition**: A topology where agents exchange messages directly.
**Related**: Orchestrator

### Shared State
**Definition**: A common registry tracking completed work to avoid duplication.
**Related**: Fan-Out

### Worker
**Definition**: A specialist agent executing an assigned subtask.
**Related**: Orchestrator

## Key Concepts Summary
### The Rules
- Start with an orchestrator
- Define handoff contracts
- Dedupe with shared state
- Fan-out costs money; cap it

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Orchestrator — ___
2. Handoff — ___
3. Worker — ___
4. Fan-out — ___
5. Shared state — ___

**Answers:** 1-d, 2-b, 3-e, 4-c, 5-a where a=dedup registry, b=task with
contract, c=parallel spawn, d=central controller, e=specialist executor.
