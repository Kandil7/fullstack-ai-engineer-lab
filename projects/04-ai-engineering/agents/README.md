# AI Agents — Educational Assistant

Agent architecture for the ThanaweyaGPT educational AI assistant. Covers tool calling,
memory management, context handling, and multi-agent coordination.

---

## Agent Architecture

### Core Agent Design

The educational assistant operates as a **ReAct agent** (Reasoning + Acting):

```
User Query
    ↓
┌─────────────────────────┐
│  ReAct Agent Loop        │
│  ┌───────────────────┐   │
│  │ Think             │   │ ← Reason about what to do
│  │ Act (Tool Call)   │   │ ← Execute tool if needed
│  │ Observe (Result)  │   │ ← Process tool output
│  │ Repeat or Answer  │   │ ← Loop until done
│  └───────────────────┘   │
└─────────────────────────┘
    ↓
Final Answer
```

### Agent Roles

| Agent              | Purpose                              | Tools Used              |
| ------------------ | ------------------------------------ | ----------------------- |
| Tutor Agent        | Main conversational agent            | RAG, Calculator, Search |
| Math Solver        | Step-by-step math problem solving    | Calculator, Code Exec   |
| Code Tutor         | Programming instruction and review   | Code Exec, Search       |
| Research Agent     | Deep topic exploration               | Search, RAG, Web Fetch  |

---

## Tool Calling

### Available Tools

| Tool            | Function                          | Input               | Output          |
| --------------- | --------------------------------- | ------------------- | ----------------|
| `search_knowledge` | Search educational content     | Query string        | Ranked documents|
| `calculator`    | Evaluate mathematical expressions | Math expression     | Numeric result  |
| `code_executor` | Run code snippets (sandboxed)     | Code + language     | Execution output|
| `web_search`    | Search the internet               | Search query        | Web results     |
| `course_lookup` | Look up course/curriculum info    | Course ID or name   | Course metadata |

### Tool Definition Format

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search the educational knowledge base for relevant content",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "course_id": {"type": "string", "description": "Filter by course"},
                    "language": {"type": "string", "enum": ["ar", "en", "tr"]},
                },
                "required": ["query"]
            }
        }
    }
]
```

### Tool Execution Flow

1. Agent decides to use a tool
2. Tool call is validated against schema
3. Tool executes with timeout (5 sec default)
4. Result returned to agent as observation
5. Agent incorporates result into reasoning

---

## Memory and Context Management

### Memory Types

| Type           | Storage      | TTL      | Purpose                      |
| -------------- | ------------ | -------- | ---------------------------- |
| Working memory | In-context   | Single   | Current conversation         |
| Short-term     | Redis        | 24 hours | Recent conversations         |
| Long-term      | PostgreSQL   | Forever  | User learning history        |
| Episodic       | Qdrant       | Forever  | Key interactions (embeddings)|

### Context Window Management

```
┌─────────────────────────────────────────────┐
│ System Prompt (fixed)                       │ ← 500 tokens
├─────────────────────────────────────────────┤
│ User Profile + Preferences                  │ ← 200 tokens
├─────────────────────────────────────────────┤
│ Retrieved Context (RAG)                     │ ← 3000 tokens
├─────────────────────────────────────────────┤
│ Conversation History                        │ ← Dynamic
├─────────────────────────────────────────────┤
│ Current Query + Tools                       │ ← Dynamic
└─────────────────────────────────────────────┘
Total budget: 8192 tokens (GPT-4) / 200K (Claude)
```

### Context Pruning Strategy

1. **Priority-based:** Keep system prompt + recent messages
2. **Relevance-based:** Drop old messages unrelated to current topic
3. **Summarization:** Compress long conversations into summaries
4. **Sliding window:** Keep last N messages, summarize older ones

---

## Multi-Agent Coordination

### Orchestration Pattern

For complex educational tasks, multiple agents collaborate:

```
Student asks: "Explain quantum mechanics and solve this problem"
    ↓
┌──────────────────┐
│ Orchestrator     │ ← Routes to appropriate agents
└────────┬─────────┘
         ├──────────────────────┐
         ↓                      ↓
┌────────────────┐    ┌────────────────┐
│ Research Agent │    │ Math Solver    │
│ (explanation)  │    │ (problem)      │
└────────────────┘    └────────────────┘
         │                      │
         └──────────┬───────────┘
                    ↓
┌────────────────────────────────────┐
│ Synthesis Agent                    │ ← Combines responses
│ ( coherent final answer )          │
└────────────────────────────────────┘
```

### Agent Communication

Agents communicate through a shared message bus:

- **Orchestrator** decomposes complex queries
- **Specialist agents** handle specific tasks
- **Synthesizer** combines results into coherent response
- **Timeout handling** — fallback if an agent fails

---

## Error Handling

| Error Type           | Handling                                    |
| -------------------- | ------------------------------------------- |
| Tool timeout         | Retry once, then skip tool                  |
| Tool error           | Log error, continue without tool            |
| Context overflow     | Prune oldest messages                       |
| Agent loop limit     | Force-stop after 10 iterations              |
| API rate limit       | Queue and retry with backoff                |

---

## Performance Targets

| Metric               | Target    |
| -------------------- | --------- |
| Response latency     | < 3 sec   |
| Tool accuracy        | > 90%     |
| Context relevance    | > 80%     |
| User satisfaction    | > 4.0/5   |
| Task completion rate | > 85%     |

---

## Getting Started

```bash
# Install dependencies
pip install openai langchain agent-protocol

# Run the agent locally
python -m agents.tutor --model gpt-4

# Test tool calling
python -m agents.test_tools --tool search_knowledge --query "quadratic formula"
```
