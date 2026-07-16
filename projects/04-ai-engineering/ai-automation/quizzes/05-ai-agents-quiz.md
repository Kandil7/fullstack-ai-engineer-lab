# Quiz 05: AI Agents

## Topic Overview
This quiz covers AI agent architecture, including ReAct patterns, tool use, memory systems, planning, multi-step reasoning, and agent orchestration. Topics span the fundamental concepts of building autonomous AI systems.

---

## Questions

### Question 1
**What is an AI agent in the context of LLM applications?**

- A) A chatbot that only responds to messages
- B) An autonomous system that can plan, reason, and use tools to achieve goals
- C) A database for storing AI models
- D) A monitoring tool for API usage

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** An AI agent is an autonomous system that can observe its environment, plan actions, and use tools to achieve specified goals. Unlike simple chatbots, agents can break down complex tasks, make decisions, take actions, and iterate until the goal is achieved. They combine LLM reasoning with external tool use and memory.
</details>

---

### Question 2
**What does "ReAct" stand for in agent design?**

- A) React.js for AI development
- B) Reasoning and Acting
- C) Recursive Agent Network
- D) Real-time Agent Notification

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** ReAct (Reasoning and Acting) is a prompting framework where the agent alternates between reasoning about what to do and taking actions. The agent generates thought-action-observation cycles: it thinks about the current state, decides on an action, executes it, observes the result, and repeats until the task is complete.
</details>

---

### Question 3
**What is "tool use" in AI agents?**

- A) Using the LLM API as a tool
- B) The agent's ability to call external functions, APIs, or execute code
- C) Using tools to train the model
- D) A development environment for agents

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Tool use (or function calling) allows agents to interact with external systems by invoking predefined functions, APIs, databases, or executing code. Tools extend the agent's capabilities beyond text generation, enabling it to search the web, query databases, make calculations, send emails, or control other systems.
</details>

---

### Question 4
**What is the "observation" step in a ReAct agent loop?**

- A) The agent observing the user's behavior
- B) The agent processing the result of its previous action
- C) Monitoring the agent's performance
- D) The user observing the agent's output

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The observation step is where the agent processes the result or feedback from its previous action. After the agent takes an action (like calling a tool), it receives output (the observation), which it uses to update its understanding and decide the next step. This feedback loop enables iterative problem-solving.
</details>

---

### Question 5
**What is "agent memory" and why is it important?**

- A) The agent's ability to remember user passwords
- B) A system for storing and retrieving information across agent interactions
- C) The agent's training data
- D) The agent's source code

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Agent memory enables the agent to store and retrieve information across conversations and tasks. Types include: short-term memory (conversation history), long-term memory (persistent facts and preferences), and episodic memory (past experiences). Memory allows agents to maintain context, learn from past interactions, and provide personalized responses.
</details>

---

### Question 6
**What is "planning" in AI agent architecture?**

- A) The user planning how to use the agent
- B) The agent's ability to create step-by-step strategies before taking actions
- C) Scheduling API calls
- D) Planning the agent's training schedule

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Planning is the agent's ability to decompose complex goals into manageable steps and create execution strategies. Planning can be: one-shot (create a complete plan upfront), iterative (re-plan after each step), or hierarchical (break goals into sub-goals). Good planning improves efficiency and reduces unnecessary tool calls.
</details>

---

### Question 7
**What is a "tool registry" in agent systems?**

- A) A list of all available APIs
- B) A centralized system that defines, manages, and routes tool calls
- C) A database of tool usage statistics
- D) A backup system for tools

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A tool registry is a centralized system that defines available tools (their names, descriptions, parameters, and schemas), manages tool versions, and routes tool calls to the appropriate handlers. It enables agents to discover and use tools dynamically, supports adding new tools without modifying the agent, and provides validation and error handling.
</details>

---

### Question 8
**What is "reflection" in agent design?**

- A) The agent reflecting on its existence
- B) The agent evaluating its own outputs and correcting errors
- C) Mirroring the user's behavior
- D) Reflecting API responses back to the user

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Reflection is a technique where the agent evaluates its own outputs, identifies errors or improvements, and iterates on its work. This creates a self-improvement loop that catches mistakes, improves quality, and ensures the output meets requirements. Reflection is particularly useful for complex tasks requiring high accuracy.
</details>

---

### Question 9
**What is the "perception" step in an agent loop?**

- A) The agent perceiving the user's emotions
- B) The agent gathering information about its current environment
- C) The user perceiving the agent's output
- D) Monitoring the agent's performance metrics

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Perception is the agent's ability to observe and gather information about its current state and environment. This includes reading tool outputs, checking system status, understanding user messages, and assessing the current context. Perception feeds into the agent's reasoning and decision-making processes.
</details>

---

### Question 10
**What is "agentic RAG"?**

- A) RAG that uses agents for retrieval
- B) An agent that dynamically decides when and how to retrieve information
- C) RAG with faster retrieval speed
- D) RAG using agent-specific embedding models

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Agentic RAG extends traditional RAG by giving the agent control over the retrieval process. Instead of always retrieving, the agent decides when retrieval is needed, what queries to use, how many documents to retrieve, and whether to re-retrieve based on initial results. This creates more adaptive and efficient retrieval strategies.
</details>

---

### Question 11
**What is the "tool selection" challenge in agent design?**

- A) Choosing the right programming language for tools
- B) The agent's ability to select the most appropriate tool for a given task
- C) Selecting the right agent for a task
- D) Choosing the right API endpoint

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Tool selection is the challenge of enabling the agent to choose the right tool from a set of available tools based on the task requirements. This requires clear tool descriptions, parameter schemas, and the agent's ability to understand task needs and match them to tool capabilities. Poor tool selection leads to failed or inefficient task execution.
</details>

---

### Question 12
**What is "multi-agent orchestration"?**

- A) Running multiple LLMs in parallel
- B) Coordinating multiple specialized agents to work together on complex tasks
- C) Managing multiple API keys
- D) Running multiple versions of the same agent

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Multi-agent orchestration coordinates multiple specialized agents, each with specific capabilities, to collaborate on complex tasks. This follows the divide-and-conquer principle: a planner agent decomposes tasks, worker agents execute subtasks, and a synthesizer combines results. Benefits include parallel execution, specialized expertise, and improved reliability.
</details>

---

### Question 13
**What is the "sandbox" concept in agent execution?**

- A) A physical testing environment
- B) An isolated environment for safely executing agent code and tool calls
- C) A sandbox game for training agents
- D) A user interface for agent configuration

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A sandbox provides an isolated, controlled environment where agents can execute code, call APIs, and perform actions without affecting production systems. Sandboxes limit resource usage, restrict access to sensitive data, and provide safety guarantees. They're essential for testing and deploying agents that execute code or interact with external systems.
</details>

---

### Question 14
**What is the "agent loop" or "agent cycle"?**

- A) The agent running in a circular buffer
- B) The continuous perceive-think-act cycle that drives agent behavior
- C) A loop in the agent's code
- D) The agent's training loop

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The agent loop is the core cycle that drives agent behavior: Perceive (gather information) → Think (reason about what to do) → Act (take an action) → Observe (process the result). This cycle repeats until the task is complete or a stopping condition is met. The loop enables iterative problem-solving and adaptation.
</details>

---

### Question 15
**What is "error recovery" in agent systems?**

- A) Recovering from system crashes
- B) The agent's ability to detect and recover from failed actions
- C) Recovering lost data
- D) Reverting to previous agent versions

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Error recovery enables agents to handle failures gracefully. When an action fails (tool error, timeout, invalid output), the agent should: detect the failure, diagnose the cause, try alternative approaches, and continue towards the goal. Robust error recovery prevents agents from getting stuck and improves overall task completion rates.
</details>

---

### Question 16
**What is a "state machine" approach to agent design?**

- A) Using a state management library
- B) Modeling agent behavior as a finite set of states with defined transitions
- C) Storing agent state in a database
- D) Converting the agent to a stateful application

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The state machine approach models agent behavior as a set of discrete states (e.g., idle, planning, executing, reflecting) with defined transitions between them. Each state has specific behaviors and valid transitions. This provides structured, predictable agent behavior and makes it easier to debug, test, and control agent actions.
</details>

---

### Question 17
**What is "grounding" in agent systems?**

- A) Connecting the agent to physical hardware
- B) Ensuring the agent's actions and outputs are based on real data and observations
- C) Training the agent on grounded data
- D) Grounding the agent's electrical connections

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Grounding ensures that the agent's reasoning, decisions, and outputs are based on actual observations and data rather than assumptions or hallucinations. Grounded agents verify facts, cite sources, and base actions on real tool outputs. This is crucial for reliability and trustworthiness in production agent systems.
</details>

---

### Question 18
**What is the "human-in-the-loop" pattern in agent design?**

- A) A human physically present during agent execution
- B) Incorporating human oversight, approval, or input at key decision points
- C) Training the agent with human feedback
- D) The agent interacting with humans via chat

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Human-in-the-loop (HITL) incorporates human oversight into the agent's workflow. Humans can approve high-risk actions, provide input when the agent is uncertain, review outputs before execution, or intervene when the agent gets stuck. HITL balances autonomy with safety and is essential for high-stakes applications.
</details>

---

### Question 19
**What is "agent observability"?**

- A) Users observing the agent's interface
- B) Monitoring and tracking agent actions, decisions, and performance
- C) Making the agent visible in the network
- D) Observing the agent's physical environment

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Agent observability provides visibility into what the agent is doing, why it's making certain decisions, and how it's performing. It includes logging tool calls, tracking reasoning steps, monitoring token usage, measuring task completion rates, and analyzing failure patterns. Observability is essential for debugging, optimizing, and maintaining production agents.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Easy | | |
| 5 | Medium | | |
| 6 | Medium | | |
| 7 | Medium | | |
| 8 | Medium | | |
| 9 | Medium | | |
| 10 | Hard | | |
| 11 | Medium | | |
| 12 | Medium | | |
| 13 | Medium | | |
| 14 | Easy | | |
| 15 | Medium | | |
| 16 | Hard | | |
| 17 | Medium | | |
| 18 | Easy | | |
| 19 | Medium | | |

**Score:** ____/19

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 8 | B | 15 | B |
| 2 | B | 9 | B | 16 | B |
| 3 | B | 10 | B | 17 | B |
| 4 | B | 11 | B | 18 | B |
| 5 | B | 12 | B | 19 | B |
| 6 | B | 13 | B | | |
| 7 | B | 14 | B | | |

---

*Generated for AI Automation Lab - Quiz 05 of 09*