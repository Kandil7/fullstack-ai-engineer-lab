# Quiz 08: Multi-Agent Systems

## Topic Overview
This quiz covers multi-agent architectures, including orchestrator-worker patterns, agent communication, task decomposition, parallel execution, state management, and coordination strategies. Topics span the design and implementation of complex multi-agent systems.

---

## Questions

### Question 1
**What is a "multi-agent system" in AI?**

- A) An agent that can perform multiple tasks
- B) A system where multiple AI agents collaborate to solve complex problems
- C) An agent with multiple models
- D) A system with multiple users

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A multi-agent system coordinates multiple specialized agents, each with specific capabilities, to collaborate on complex tasks. This follows the divide-and-conquer principle: a planner agent decomposes tasks, worker agents execute subtasks, and results are synthesized. Multi-agent systems can handle tasks too complex for a single agent.
</details>

---

### Question 2
**What is the "orchestrator-worker" pattern in multi-agent systems?**

- A) A pattern where workers manage the orchestrator
- B) A pattern where a central orchestrator delegates tasks to specialized worker agents
- C) A pattern where all agents have equal authority
- D) A pattern for training agents

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The orchestrator-worker pattern uses a central orchestrator agent to manage the workflow. The orchestrator decomposes tasks, assigns subtasks to specialized workers, monitors progress, and synthesizes results. Workers focus on specific capabilities (coding, research, analysis) and return results to the orchestrator.
</details>

---

### Question 3
**What is "task decomposition" in multi-agent systems?**

- A) Breaking down the agent's code into modules
- B) Splitting complex tasks into smaller, manageable subtasks
- C) Decomposing the model's architecture
- D) Breaking down the API into endpoints

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Task decomposition breaks complex goals into smaller, more manageable subtasks that can be assigned to specialized agents. Good decomposition identifies independent tasks that can be parallelized, dependent tasks that need sequencing, and shared resources that need coordination. Effective decomposition is critical for multi-agent system efficiency.
</details>

---

### Question 4
**What is "parallel execution" in multi-agent systems?**

- A) Running multiple agents on the same task
- B) Executing independent subtasks simultaneously across multiple agents
- C) Running agents in sequence
- D) Using parallel computing for training

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Parallel execution runs independent subtasks simultaneously across multiple agents, significantly reducing total execution time. For example, if a task has three independent research components, three agents can work on them concurrently. Parallel execution requires identifying independent tasks and managing shared resources appropriately.
</details>

---

### Question 5
**What is "agent communication" in multi-agent systems?**

- A) Agents talking to users
- B) The methods agents use to exchange information and coordinate actions
- C) Agents communicating with API endpoints
- D) Agents sending emails

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Agent communication enables agents to share information, coordinate actions, and collaborate effectively. Communication patterns include: message passing, shared memory, blackboard systems, and event-driven architectures. Effective communication is essential for multi-agent coordination and preventing conflicts or duplicated work.
</details>

---

### Question 6
**What is "shared state" in multi-agent systems?**

- A) All agents share the same model weights
- B) A common data store that all agents can read from and write to
- C) Agents sharing the same API key
- D) Agents having the same configuration

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Shared state provides a common data store (like a database, file system, or in-memory store) that all agents can access. This enables agents to share context, results, and coordination information. Shared state must be managed carefully to prevent conflicts, ensure consistency, and handle concurrent access.
</details>

---

### Question 7
**What is a "pipeline" pattern in multi-agent systems?**

- A) A pattern where agents process data through a sequential chain
- B) A pattern for training models
- C) A pattern for deploying agents
- D) A pattern for monitoring agents

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** The pipeline pattern chains agents in a sequential flow where each agent processes the output of the previous one. For example: Document Parser → Content Analyzer → Summary Generator → Output Formatter. Pipelines are simple to implement and debug but don't support parallelism for independent tasks.
</details>

---

### Question 8
**What is "agent specialization" in multi-agent systems?**

- A) Making agents specialized for specific hardware
- B) Designing agents with specific expertise or capabilities for particular tasks
- C) Specializing agents for specific users
- D) Creating agents with special permissions

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Agent specialization designs agents with focused expertise for specific tasks. A coding agent excels at writing code, a research agent specializes in information gathering, and an analysis agent focuses on data processing. Specialization improves quality and efficiency compared to general-purpose agents trying to do everything.
</details>

---

### Question 9
**What is "conflict resolution" in multi-agent systems?**

- A) Resolving conflicts between users
- B) Handling situations where agents disagree or their actions conflict
- C) Resolving API conflicts
- D) Fixing bugs in agent code

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Conflict resolution handles situations where agents produce conflicting results, make incompatible decisions, or compete for shared resources. Strategies include: priority-based resolution, voting mechanisms, consensus algorithms, and arbitration by a coordinator agent. Effective conflict resolution prevents system deadlocks and inconsistent outputs.
</details>

---

### Question 10
**What is a "supervisor agent" in multi-agent architectures?**

- A) An agent that monitors other agents' performance
- B) A higher-level agent that coordinates and manages other agents
- C) An agent with administrative privileges
- D) An agent that supervises user interactions

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A supervisor agent (or coordinator agent) manages other agents by assigning tasks, monitoring progress, handling failures, and synthesizing results. It has a broader view of the overall goal and can make strategic decisions about task allocation. The supervisor pattern is common in complex multi-agent workflows.
</details>

---

### Question 11
**What is "agent memory sharing" in multi-agent systems?**

- A) Agents sharing their source code
- B) Agents accessing a common memory store to share information
- C) Agents sharing API keys
- D) Agents sharing user data

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Agent memory sharing enables agents to access a common memory store (like a vector database, shared file system, or key-value store) to share context, results, and learned information. This enables agents to build on each other's work and maintain consistent state across the system.
</details>

---

### Question 12
**What is the "scatter-gather" pattern in multi-agent systems?**

- A) A pattern for distributing data
- B) A pattern where a task is scattered to multiple agents and results are gathered
- C) A pattern for collecting user feedback
- D) A pattern for managing agent lifecycles

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The scatter-gather pattern distributes a task to multiple agents (scatter), each processes a portion independently, and results are collected and combined (gather). For example, scattering a search query to multiple research agents and gathering their findings. This pattern enables parallel processing and comprehensive coverage.
</details>

---

### Question 13
**What is "agent orchestration" and why is it important?**

- A) Tuning agent parameters
- B) The coordination and management of multiple agents to achieve a goal
- C) Creating orchestral music with AI
- D) Organizing agent documentation

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Agent orchestration coordinates multiple agents to work together effectively. It involves task assignment, progress monitoring, error handling, and result synthesis. Good orchestration ensures efficient resource utilization, prevents conflicts, and produces coherent outputs from multiple agent contributions.
</details>

---

### Question 14
**What is "agent failure handling" in multi-agent systems?**

- A) Handling user complaints about agents
- B) Strategies for detecting and recovering from agent failures
- C) Preventing agents from failing
- D) Training agents to handle failures

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Agent failure handling includes detecting when agents fail, diagnosing the cause, and recovering gracefully. Strategies include: retrying with different parameters, reassigning tasks to alternative agents, providing fallback outputs, and alerting human operators. Robust failure handling is essential for reliable multi-agent systems.
</details>

---

### Question 15
**What is "consensus" in multi-agent decision-making?**

- A) All agents agreeing on the same answer
- B) A process where agents negotiate to reach a collective decision
- C) The model reaching consensus in its training
- D) Users reaching consensus on agent behavior

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Consensus mechanisms enable agents to negotiate and reach collective decisions. Approaches include: majority voting, weighted voting based on expertise, deliberative discussion, and iterative refinement. Consensus is important when multiple agents provide different perspectives and a unified decision is needed.
</details>

---

### Question 16
**What is a "blackboard system" in multi-agent architecture?**

- A) A system with a dark interface
- B) A shared workspace where agents post and read information
- C) A system that blocks certain agents
- D) A monitoring dashboard

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A blackboard system provides a shared workspace (the "blackboard") where agents can post information, read others' contributions, and collaboratively build solutions. Agents independently decide when to contribute based on what's on the blackboard. This pattern enables loose coupling between agents and flexible collaboration.
</details>

---

### Question 17
**What is "agent load balancing" in multi-agent systems?**

- A) Balancing the load on a single agent
- B) Distributing tasks evenly across multiple agents
- C) Balancing the agent's memory usage
- D) Balancing API rate limits

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Agent load balancing distributes tasks across multiple agents to prevent bottlenecks and ensure efficient resource utilization. Strategies include: round-robin assignment, least-loaded assignment, capability-based assignment, and dynamic rebalancing based on agent performance. Good load balancing improves throughput and reduces latency.
</details>

---

### Question 18
**What is "agent versioning" in multi-agent systems?**

- A) Versioning individual agent code
- B) Managing different versions of agents and their interactions
- C) Versioning the agent's training data
- D) Versioning the API endpoints

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

</details>

</details>

---

### Question 19
**What is the "hub-spoke" pattern in multi-agent systems?**

- A) A pattern where agents connect directly to each other
- B) A pattern where a central hub coordinates multiple spoke agents
- C) A pattern for deploying agents to different regions
- D) A pattern for monitoring agent performance

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The hub-spoke pattern uses a central hub agent that coordinates multiple spoke agents. The hub receives requests, delegates to appropriate spokes, and aggregates results. Spokes communicate only through the hub, simplifying coordination. This pattern provides central control while enabling specialized processing.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Medium | | |
| 5 | Easy | | |
| 6 | Medium | | |
| 7 | Medium | | |
| 8 | Medium | | |
| 9 | Medium | | |
| 10 | Medium | | |
| 11 | Medium | | |
| 12 | Hard | | |
| 13 | Easy | | |
| 14 | Medium | | |
| 15 | Hard | | |
| 16 | Hard | | |
| 17 | Medium | | |
| 18 | Medium | | |
| 19 | Hard | | |

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
| 7 | A | 14 | B | | |

---

*Generated for AI Automation Lab - Quiz 08 of 09*