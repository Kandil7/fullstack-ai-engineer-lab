# Agent Patterns — Glossary 14

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Agent | Pattern | A model with tools, memory, and a loop |
| Planner | Pattern | Agent that decomposes a task into steps |
| ReAct | Pattern | Reason-then-act loop for grounded decisions |
| Reflection | Pattern | Self-critique loop improving outputs |
| Tool Call | Core | A model-requested function invocation |
| Tool Message | Core | The result of a tool call fed back to the model |
| Tool Schema | Core | The typed contract for a tool's arguments |

## Detailed Definitions
### Agent
**Definition**: A model augmented with tools, memory, and an execution loop
pursuing a goal.
**Related**: Planner

### Planner
**Definition**: An agent that breaks a goal into ordered subtasks before
acting.
**Related**: Agent

### ReAct
**Definition**: Interleaved reasoning and acting: think, call a tool, observe,
repeat.
**Related**: Agent

### Reflection
**Definition**: Generating, critiquing, then revising - a self-improvement
loop.
**Related**: ReAct

### Tool Call
**Definition**: The model's structured request to execute a declared function.
**Related**: Tool Message

### Tool Message
**Definition**: The execution result returned to the conversation as a tool
role.
**Related**: Tool Call

### Tool Schema
**Definition**: The JSON contract: name, description, argument types and
requirements.
**Related**: Tool Call

## Key Concepts Summary
### The Families
- Planner: think before acting
- ReAct: interleave thinking and acting
- Reflection: critique then revise

### The Core
- Tools are declared, called, executed, and fed back

## Practice Terms
Match each term to its definition (answers at the bottom).
1. ReAct — ___
2. Reflection — ___
3. Tool schema — ___
4. Planner — ___
5. Agent — ___

**Answers:** 1-c, 2-e, 3-b, 4-a, 5-d where a=task decomposition, b=typed tool
contract, c=reason-act loop, d=model+loop+goals, e=critique-revise loop.
