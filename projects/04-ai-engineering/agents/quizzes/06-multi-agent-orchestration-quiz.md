# Quiz 06: Multi-Agent Orchestration

> **Topic Overview**: Multi-agent orchestration coordinates multiple specialized agents to accomplish complex tasks. This quiz covers orchestration patterns (supervisor, peer-to-peer, hierarchical), agent coordination mechanisms, task delegation, communication protocols, concurrency patterns, and strategies for managing complexity in multi-agent systems.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 20 |
| Correct Answers | 0 |
| Score | 0% |
| Difficulty Rating | — |

---

## Questions

### Question 1 — Easy

**What is a "multi-agent system"?**

- A) An agent that runs on multiple computers
- B) A system composed of multiple autonomous agents that interact to solve problems
- C) A system with multiple users
- D) An agent with multiple tools

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A multi-agent system (MAS) consists of multiple autonomous agents that interact, coordinate, and collaborate to solve problems. Each agent typically has specialized capabilities, and the system's overall capability exceeds what any single agent could achieve.

</details>

---

### Question 2 — Easy

**What is a "supervisor" pattern in multi-agent orchestration?**

- A) A human who monitors the agents
- B) A central coordinator agent that delegates tasks to specialized worker agents
- C) A tool for supervising API calls
- D) A security agent that watches for threats

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: In the supervisor pattern, a central orchestrator agent receives the user's request, decomposes it into subtasks, and delegates each subtask to appropriate specialized worker agents. The supervisor coordinates the workflow and assembles the final result.

</details>

---

### Question 3 — Easy

**What is "agent specialization" in multi-agent systems?**

- A) Making all agents identical
- B) Designing agents to excel at specific types of tasks
- C) Creating agents that specialize in different programming languages
- D) Making agents faster

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Agent specialization means designing each agent to excel at specific types of tasks. For example, one agent might specialize in research, another in code writing, and another in testing. This allows each agent to have optimized prompts, tools, and expertise for its domain.

</details>

---

### Question 4 — Easy

**Why use multiple agents instead of a single powerful agent?**

- A) Multiple agents are always cheaper
- B) Specialization allows each agent to focus on what it does best, improving overall quality
- C) Multiple agents are easier to debug
- D) Single agents can't use tools

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Multiple agents provide specialization—each agent can be optimized for its specific task with tailored prompts, tools, and evaluation criteria. This division of labor often produces better results than a single agent trying to handle everything.

</details>

---

### Question 5 — Medium

**What is the "orchestrator-workers" pattern?**

- A) One agent does all the work alone
- B) An orchestrator breaks tasks into parts, and multiple worker agents execute them in parallel
- C) Workers create the plan and the orchestrator executes it
- D) All agents work on the same task simultaneously without coordination

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: In the orchestrator-workers pattern, a central orchestrator agent decomposes the task and dispatches subtasks to multiple worker agents. Workers execute their subtasks (potentially in parallel), and the orchestrator assembles the final result.

</details>

---

### Question 6 — Medium

**What is "peer-to-peer" agent coordination?**

- A) All agents communicate directly with each other without a central coordinator
- B) Agents only communicate through a central hub
- C) Agents never communicate
- D) Agents share a single brain

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Peer-to-peer coordination allows agents to communicate directly with each other without a central coordinator. This is more flexible but can be harder to manage and debug. It's useful when agents need to negotiate or share information dynamically.

</details>

---

### Question 7 — Medium

**What is "task delegation" in multi-agent systems?**

- A) Assigning tasks to humans
- B) The process of assigning specific subtasks to the most appropriate agent
- C) Removing tasks from the queue
- D) Delegating all tasks to a single agent

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Task delegation is the process of assigning subtasks to agents based on their capabilities, availability, and the task's requirements. Effective delegation considers each agent's strengths, current workload, and the dependencies between tasks.

</details>

---

### Question 8 — Medium

**What is "agent communication" in multi-agent systems?**

- A) Agents talking to each other via natural language messages
- B) The exchange of information, requests, and results between agents through defined protocols
- C) Agents communicating with the database
- D) The network connection between agent servers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Agent communication is the structured exchange of information between agents. This can include task assignments, results, status updates, and queries. Communication protocols define the format and rules for these exchanges.

</details>

---

### Question 9 — Medium

**What is "parallel execution" in multi-agent orchestration?**

- A) Running all agents sequentially
- B) Executing independent tasks simultaneously across multiple agents
- C) Running agents on parallel circuits
- D) Processing data in parallel

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Parallel execution runs independent subtasks simultaneously across multiple agents. This significantly reduces total execution time compared to sequential processing. However, it requires careful management of shared resources and result aggregation.

</details>

---

### Question 10 — Medium

**What is "result aggregation" in multi-agent systems?**

- A) Agents combining their results into a single coherent output
- B) Agents competing to produce the best result
- C) Storing results in a database
- D) Deleting duplicate results

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Result aggregation combines the outputs of multiple agents into a single coherent result. This may involve merging code files, synthesizing research findings, resolving conflicts between agent outputs, or formatting results for the user.

</details>

---

### Question 11 — Hard

**What is "hierarchical multi-agent architecture"?**

- A) Agents arranged in a flat structure
- B) Multiple layers of supervisors and workers, creating a tree-like delegation structure
- C) Agents ranked by seniority
- D) A single agent with multiple tools

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Hierarchical multi-agent architecture creates multiple layers of supervision. A top-level supervisor delegates to mid-level supervisors, who delegate to worker agents. This scales to complex tasks by distributing coordination across multiple levels.

</details>

---

### Question 12 — Hard

**What is "consensus building" in multi-agent systems?**

- A) Agents agreeing to disagree
- B) The process of multiple agents reaching agreement on a shared decision or plan
- C) Building the agent's consensus training data
- D) Agents voting on which tool to use

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Consensus building is the process by which multiple agents reach agreement on a shared decision. This may involve voting, negotiation, or evaluation of proposals. It's essential when agents have different perspectives or expertise that must be reconciled.

</details>

---

### Question 13 — Hard

**What is the "blackboard" pattern in multi-agent coordination?**

- A) Agents writing on a blackboard
- B) A shared data structure that agents read from and write to, enabling indirect communication and collaboration
- C) Hiding all agent outputs
- D) A security mechanism for agent isolation

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The blackboard pattern provides a shared data structure (the "blackboard") where agents post information, read others' contributions, and collaborate indirectly. This decouples agents and allows flexible, emergent collaboration patterns.

</details>

---

### Question 14 — Hard

**What is "agent swarm" intelligence?**

- A) Agents that behave like a swarm of bees
- B) Emergent intelligent behavior arising from many simple agents following local rules and interacting
- C) A swarm of drones controlled by AI
- D) An agent that controls a swarm of robots

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Agent swarm intelligence is emergent behavior where many simple agents, each following local rules, collectively produce intelligent global behavior. No single agent directs the swarm—complex behavior emerges from simple interactions, similar to ant colonies or bird flocks.

</details>

---

### Question 15 — Hard

**What is "fault tolerance" in multi-agent systems?**

- A) Agents that never fail
- B) The system's ability to continue operating correctly even when individual agents fail
- C) Tolerance for agent behavior that deviates from expectations
- D) The agent's ability to handle network faults

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Fault tolerance ensures the multi-agent system continues functioning when individual agents fail. This requires redundancy, error detection, retry mechanisms, and fallback strategies. Without fault tolerance, a single agent failure can cascade through the entire system.

</details>

---

### Question 16 — Easy

**What is a "specialist agent" in multi-agent systems?**

- A) An agent that specializes in everything
- B) An agent designed to excel at a specific type of task or domain
- C) An agent that requires special hardware
- D) A premium-tier agent

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

</details>

**Explanation**: A specialist agent is designed to excel at a specific type of task. Examples include a research agent that finds information, a coding agent that writes code, or a testing agent that validates results. Specialization improves quality and efficiency.

</details>

---

### Question 17 — Medium

**What is "load balancing" in multi-agent orchestration?**

- A) Balancing the agent's workload evenly across available agents
- B) Making sure all agents have the same number of tools
- C) Balancing the agent's memory usage
- D) Distributing network traffic

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Load balancing distributes tasks evenly across available agents to prevent any single agent from being overloaded while others are idle. This improves throughput, reduces latency, and prevents bottlenecks in the system.

</details>

---

### Question 18 — Medium

**What is "agent discovery" in multi-agent systems?**

- A) Finding new agents on the internet
- B) The process of identifying which agents are available and what capabilities they have
- C) Discovering new use cases for agents
- D) Training new agents

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Agent discovery is the process of identifying available agents and their capabilities. This allows the orchestrator to select the right agent for each task. It may involve service registries, capability descriptions, or dynamic discovery protocols.

</details>

---

### Question 19 — Hard

**What is "emergent behavior" in multi-agent systems and why is it challenging?**

- A) Behavior that is explicitly programmed into each agent
- B) Unpredictable collective behavior that arises from agent interactions and is difficult to predict or control
- C) A bug in the agent's code
- D) Behavior that emerges during agent training

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Emergent behavior in multi-agent systems refers to collective behavior that wasn't explicitly programmed but arises from agent interactions. It's challenging because it's difficult to predict, test, and control—emergent behaviors can be beneficial or harmful.

</details>

---

### Question 20 — Easy

**What is the primary benefit of using a supervisor agent?**

- A) It eliminates the need for worker agents
- B) It provides centralized coordination, task delegation, and result assembly
- C) It does all the work itself
- D) It reduces the system's capabilities

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A supervisor agent provides centralized coordination—it decomposes tasks, delegates to appropriate workers, monitors progress, handles errors, and assembles results. This creates a clear organizational structure and makes the system easier to manage and debug.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Easy |
| 5 | B | Medium |
| 6 | A | Medium |
| 7 | B | Medium |
| 8 | B | Medium |
| 9 | B | Medium |
| 10 | A | Medium |
| 11 | B | Hard |
| 12 | B | Hard |
| 13 | B | Hard |
| 14 | B | Hard |
| 15 | B | Hard |
| 16 | B | Easy |
| 17 | A | Medium |
| 18 | B | Medium |
| 19 | B | Hard |
| 20 | B | Easy |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 18-20 | Expert | Excellent multi-agent orchestration knowledge |
| 14-17 | Proficient | Strong understanding; explore advanced patterns |
| 10-13 | Developing | Good foundation; implement a multi-agent system |
| 6-9 | Beginner | Review orchestration patterns and examples |
| 0-5 | Novice | Start with single-agent fundamentals first |

---

**Previous Quiz**: [05 - Planning & Reasoning](05-planning-reasoning-quiz.md) | **Next Quiz**: [07 - Agent Communication](07-agent-communication-quiz.md)
