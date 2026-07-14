# Quiz 05: Planning & Reasoning

> **Topic Overview**: Planning and reasoning are the cognitive capabilities that enable agents to decompose complex tasks, formulate strategies, and make informed decisions. This quiz covers task decomposition, hierarchical planning, goal-directed reasoning, constraint satisfaction, common reasoning frameworks (CoT, ToT, GoT), and strategies for managing planning complexity.

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

**What is "task decomposition" in the context of AI agents?**

- A) Breaking down the agent's hardware
- B) Breaking a complex task into smaller, manageable subtasks
- C) Decomposing the LLM's parameters
- D) Removing tasks from the queue

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Task decomposition is the process of breaking a complex task into smaller, more manageable subtasks. This makes it easier for agents to plan, execute, and track progress toward a goal.

</details>

---

### Question 2 — Easy

**What is "Chain-of-Thought" (CoT) prompting?**

- A) A method for chaining multiple LLMs together
- B) A prompting technique that encourages the model to show its reasoning step by step
- C) A way to chain API calls
- D) A debugging technique for code

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Chain-of-Thought prompting encourages the LLM to produce intermediate reasoning steps before arriving at a final answer. This improves performance on complex tasks by making the reasoning process explicit and verifiable.

</details>

---

### Question 3 — Easy

**Why is planning important for AI agents?**

- A) It makes the agent use less memory
- B) It helps the agent work toward goals efficiently by anticipating steps and resource needs
- C) It eliminates the need for tools
- D) It reduces the agent's response time to zero

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Planning helps agents work efficiently by anticipating future steps, allocating resources, identifying dependencies, and creating a roadmap to the goal. Without planning, agents may waste resources, take unnecessary steps, or miss critical requirements.

</details>

---

### Question 4 — Easy

**What is the difference between "reactive" and "deliberative" planning?**

- A) Reactive planning is slower; deliberative planning is faster
- B) Reactive planning responds to immediate situations; deliberative planning creates plans before acting
- C) They are the same thing
- D) Reactive planning uses LLMs; deliberative planning uses rule engines

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reactive planning responds to immediate stimuli without creating detailed plans—adapting on the fly. Deliberative planning creates a comprehensive plan before acting, considering future steps and consequences. Most effective agents combine both approaches.

</details>

---

### Question 5 — Medium

**What is the "Tree of Thoughts" (ToT) framework?**

- A) A data structure for storing agent thoughts
- B) A reasoning framework that explores multiple reasoning paths in a tree structure, allowing backtracking
- C) A visualization tool for agent architectures
- D) A method for growing agent capabilities

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tree of Thoughts (ToT) extends CoT by allowing the LLM to explore multiple reasoning paths simultaneously in a tree structure. It can evaluate each path, backtrack from unproductive ones, and explore alternative branches—improving performance on tasks requiring exploration.

</details>

---

### Question 6 — Medium

**What is "hierarchical planning"?**

- A) Planning that requires admin privileges
- B) Planning at multiple levels of abstraction—strategic, tactical, and operational
- C) Planning that only works in organizational hierarchies
- D) Planning from top to bottom of a document

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Hierarchical planning breaks down goals at multiple levels: high-level strategic plans (what to achieve), mid-level tactical plans (how to organize), and low-level operational plans (specific actions). Each level provides context for the level below it.

</details>

---

### Question 7 — Medium

**What is "goal decomposition" in agent planning?**

- A) Destroying the agent's goals
- B) Breaking a high-level goal into concrete, actionable sub-goals
- C) Combining multiple goals into one
- D) Removing goals from the agent's agenda

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Goal decomposition breaks a high-level goal into specific, actionable sub-goals. For example, "build a web app" might decompose into: design UI, implement backend, create database, write tests, deploy. Each sub-goal is more concrete and actionable.

</details>

---

### Question 8 — Medium

**What is the "Graph of Thoughts" (GoT) framework?**

- A) A graph database for storing thoughts
- B) An extension of ToT that allows thoughts to be combined, refined, and connected in arbitrary graph structures
- C) A network diagram of agent components
- D) A social network for AI agents

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Graph of Thoughts extends ToT by allowing reasoning paths to be combined, merged, and refined in graph structures (not just trees). This enables more complex reasoning patterns like synthesis, refinement loops, and iterative improvement.

</details>

---

### Question 9 — Medium

**What is "constraint satisfaction" in agent planning?**

- A) Satisfying the user's desires without limits
- B) Finding solutions that meet all specified constraints and requirements
- C) Ignoring all constraints
- D) Satisfying only the easiest constraints

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Constraint satisfaction involves finding solutions that meet all specified requirements and limitations—time, resources, dependencies, quality standards, etc. Agents must balance multiple constraints to find viable solutions.

</details>

---

### Question 10 — Medium

**What is "subgoal retirement" in agent planning?**

- A) Removing subgoals that are no longer relevant
- B) The process of determining when a subgoal has been achieved and removing it from the active plan
- C) Retiring the entire agent
- D) Storing subgoals for later use

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Subgoal retirement is the process of recognizing when a subgoal has been achieved and removing it from the active plan. This keeps the plan focused and prevents the agent from wasting resources on already-completed objectives.

</details>

---

### Question 11 — Hard

**What is "backward planning" (also called "backward chaining")?**

- A) Planning from the current state forward to the goal
- B) Starting from the goal and working backward to determine what steps are needed to reach it
- C) Planning in reverse chronological order
- D) Undoing previously completed steps

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Backward planning starts with the desired goal and works backward, determining what conditions must be true for the goal to be achieved, then what actions would create those conditions, and so on until reaching the current state. This is useful when the goal is well-defined but the path is unclear.

</details>

---

### Question 12 — Hard

**What is the "planning horizon" problem?**

- A) The agent can only plan for activities happening on the horizon
- B) The tradeoff between planning depth (how far ahead to plan) and planning cost/resource usage
- C) The agent's inability to see beyond its immediate surroundings
- D) The distance between the agent's servers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The planning horizon problem is the tradeoff between how far ahead an agent plans and the cost of planning. Deeper planning provides better long-term decisions but requires more computation and may be based on uncertain predictions. Shallow planning is faster but may miss important considerations.

</details>

---

### Question 13 — Hard

**What is "abductive reasoning" in the context of AI agents?**

- A) Reasoning that always produces correct conclusions
- B) Inference to the best explanation—choosing the most likely explanation given incomplete information
- C) Reasoning by contradiction
- D) Reasoning that ignores evidence

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Abductive reasoning infers the most likely explanation from incomplete or ambiguous information. Unlike deductive reasoning (which guarantees correct conclusions), abductive reasoning produces plausible hypotheses that must be verified. It's valuable when agents face uncertainty.

</details>

---

### Question 14 — Hard

**What is "iterative refinement" in agent planning?**

- A) Creating the perfect plan on the first try
- B) Creating an initial plan, executing it, learning from the results, and improving the plan through repeated cycles
- C) Never changing the original plan
- D) Refining the LLM's training data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Iterative refinement creates an initial plan, executes it (or parts of it), observes results, and uses those observations to improve the plan. This adaptive approach handles uncertainty better than static planning and improves plan quality over time.

</details>

---

### Question 15 — Hard

**What is "resource-bounded planning"?**

- A) Planning that never uses any resources
- B) Planning that explicitly accounts for and optimizes the use of limited resources (time, tokens, money, etc.)
- C) Planning on a budget
- D) Planning that only uses free tools

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Resource-bounded planning explicitly accounts for limited resources—API token budgets, time constraints, compute costs, and human attention. The agent must make tradeoffs between plan quality and resource consumption, choosing approaches that maximize value within constraints.

</details>

---

### Question 16 — Easy

**What is "step-by-step reasoning"?**

- A) Walking through the code line by line
- B) Breaking down a problem into sequential logical steps to arrive at a solution
- C) Processing data one byte at a time
- D) Training the model one epoch at a time

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Step-by-step reasoning breaks down complex problems into sequential logical steps, making the reasoning process transparent and verifiable. This is the foundation of Chain-of-Thought prompting and helps agents handle multi-step problems.

</details>

---

### Question 17 — Medium

**What is the "least commitment" principle in planning?**

- A) Committing to the easiest option
- B) Deferring decisions as long as possible until more information is available
- C) Always making the first decision that comes to mind
- D) Never committing to any plan

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The least commitment principle defers decisions until necessary, keeping options open as long as possible. This is valuable in uncertain environments where premature commitments may need to be revised, wasting resources and time.

</details>

---

### Question 18 — Medium

**What is "plan monitoring" in agent systems?**

- A) Watching the plan execute from a distance
- B) Continuously tracking plan execution to detect deviations and trigger replanning when needed
- C) Monitoring the agent's CPU usage
- D) Reading the plan document

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Plan monitoring continuously tracks whether the plan is being executed as expected. It detects deviations, failures, and unexpected outcomes, triggering replanning when the current plan is no longer viable. This is essential for robust agent behavior.

</details>

---

### Question 19 — Hard

**What is "contingency planning" in agent systems?**

- A) Planning only for worst-case scenarios
- B) Creating alternative plans that can be activated if the primary plan fails or conditions change
- C) Making backup copies of the plan file
- D) Planning for holidays

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Contingency planning creates alternative plans (Plan B, Plan C) that can be activated if the primary plan fails or conditions change unexpectedly. This makes agents more resilient to uncertainty and able to recover from failures gracefully.

</details>

---

### Question 20 — Easy

**Which prompting technique explicitly asks the LLM to "think step by step"?**

- A) Zero-shot prompting
- B) Chain-of-Thought prompting
- C) Few-shot prompting
- D) System prompting

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Chain-of-Thought prompting explicitly encourages the LLM to reason step by step. This simple instruction ("think step by step") significantly improves performance on reasoning tasks by making the intermediate reasoning process explicit.

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
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Medium |
| 9 | B | Medium |
| 10 | B | Medium |
| 11 | B | Hard |
| 12 | B | Hard |
| 13 | B | Hard |
| 14 | B | Hard |
| 15 | B | Hard |
| 16 | B | Easy |
| 17 | B | Medium |
| 18 | B | Medium |
| 19 | B | Hard |
| 20 | B | Easy |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 18-20 | Expert | Excellent planning and reasoning knowledge |
| 14-17 | Proficient | Strong understanding; explore advanced frameworks |
| 10-13 | Developing | Good foundation; implement planning patterns |
| 6-9 | Beginner | Review CoT and basic planning concepts |
| 0-5 | Novice | Start with Chain-of-Thought fundamentals |

---

**Previous Quiz**: [04 - ReAct Pattern](04-react-pattern-quiz.md) | **Next Quiz**: [06 - Multi-Agent Orchestration](06-multi-agent-orchestration-quiz.md)
