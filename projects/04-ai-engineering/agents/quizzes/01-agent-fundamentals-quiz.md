# Quiz 01: Agent Fundamentals

> **Topic Overview**: AI agents are autonomous systems that perceive their environment, make decisions, and take actions to achieve specific goals. This quiz covers core agent concepts including perception, decision-making, autonomy levels, agent architectures, and the distinction between agents and traditional software. Understanding these fundamentals is essential for building effective AI-powered systems.

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

**What is the primary characteristic that distinguishes an AI agent from a simple chatbot?**

- A) It can generate text responses
- B) It can take autonomous actions in an environment to achieve goals
- C) It uses large language models
- D) It can handle multiple languages

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The defining characteristic of an AI agent is its ability to autonomously perceive its environment, reason about goals, and take actions to achieve them. A chatbot typically responds to prompts, while an agent operates in a loop of observation → reasoning → action.

</details>

---

### Question 2 — Easy

**Which of the following best describes "agent autonomy"?**

- A) The agent never needs electricity
- B) The agent's ability to operate and make decisions without human intervention
- C) The agent's ability to run on any operating system
- D) The agent's independence from network connectivity

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Agent autonomy refers to the degree to which an agent can operate, make decisions, and take actions without requiring human input. Full autonomy means the agent handles all decisions; partial autonomy means it defers to humans for certain choices.

</details>

---

### Question 3 — Easy

**In the context of AI agents, what does "perception" refer to?**

- A) The agent's ability to see physical objects
- B) The process of gathering and interpreting information from the environment
- C) The agent's user interface design
- D) The speed at which the agent processes data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Perception in AI agents is the process of gathering, filtering, and interpreting information from the environment. This can include reading files, parsing API responses, processing user messages, or any form of environmental input the agent uses to inform its decisions.

</details>

---

### Question 4 — Easy

**What is a "goal" in the context of AI agents?**

- A) A static configuration file
- B) A desired outcome or state that the agent works to achieve
- C) A fixed list of instructions
- D) A database of stored memories

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A goal is the desired end state or outcome that an agent strives to achieve. Goals can be explicit (user-provided) or implicit (derived from the system design), and agents use their reasoning capabilities to determine actions that move them closer to their goals.

</details>

---

### Question 5 — Medium

**Which agent architecture pattern uses a loop of Observe → Think → Act?**

- A) Pipeline Architecture
- B) ReAct (Reason + Act)
- C) Microservices Architecture
- D) Event-Driven Architecture

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: ReAct (Reason + Act) is a foundational agent architecture that alternates between observing the environment, reasoning about what to do next, and acting upon that reasoning. This creates a tight loop that allows agents to iteratively work toward goals.

</details>

---

### Question 6 — Medium

**What is a "tool" in the context of AI agents?**

- A) A physical device the agent controls
- B) A callable function or API that extends the agent's capabilities beyond text generation
- C) A type of training dataset
- D) A hardware component of the agent's server

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: In AI agents, tools are functions, APIs, or capabilities that extend the agent beyond pure text generation. Tools allow agents to search the web, execute code, query databases, send emails, or interact with external systems—enabling real-world actions.

</details>

---

### Question 7 — Medium

**Which of the following is NOT a typical component of an AI agent system?**

- A) Perception module
- B) Decision-making/reasoning engine
- C) Action execution mechanism
- D) Static HTML rendering engine

<details>
<summary>Reveal Answer</summary>

**Correct Answer: D**

**Explanation**: A static HTML rendering engine is not a component of an AI agent. Typical agent components include: perception (gathering input), reasoning (deciding what to do), action execution (carrying out decisions), and memory (storing past experiences).

</details>

---

### Question 8 — Medium

**What is the "agent loop"?**

- A) A single pass through the agent's code
- B) The continuous cycle of perceiving, reasoning, and acting until a goal is achieved or a stopping condition is met
- C) A network loop that connects multiple agents
- D) The training loop used to fine-tune the agent's model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The agent loop is the core execution cycle: the agent observes its environment, reasons about the next step, takes an action, observes the result, and repeats. This continues until the goal is achieved, a stopping condition is met, or resources are exhausted.

</details>

---

### Question 9 — Medium

**Which of the following best describes a "reactive agent"?**

- A) An agent that plans extensively before acting
- B) An agent that responds directly to current stimuli without maintaining internal state
- C) An agent that only works with React.js applications
- D) An agent that requires human approval for every action

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A reactive agent responds to immediate environmental stimuli without maintaining internal state or memory of past experiences. It maps perceptions directly to actions based on predefined rules, making it fast but limited in handling complex, multi-step tasks.

</details>

---

### Question 10 — Medium

**What is the primary advantage of using LLMs as the reasoning engine in AI agents?**

- A) They are faster than traditional algorithms
- B) They can understand natural language instructions and reason across diverse domains
- C) They require less memory than rule-based systems
- D) They are guaranteed to always produce correct outputs

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: LLMs excel at understanding natural language, reasoning across diverse domains, and handling ambiguous instructions. This makes them powerful reasoning engines for agents that need to operate in open-ended environments where rigid rule-based systems would fail.

</details>

---

### Question 11 — Hard

**In the BDI (Belief-Desire-Intention) agent model, what do "intentions" represent?**

- A) What the agent knows about the world
- B) What the agent wants to achieve
- C) The plans the agent has committed to pursuing
- D) The agent's ethical constraints

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: In the BDI model: Beliefs = what the agent knows (knowledge), Desires = what the agent wants (goals), Intentions = the plans the agent has committed to executing. Intentions are the bridge between desires and actions, representing chosen courses of action.

</details>

---

### Question 12 — Hard

**What is the "frame problem" in AI agent design?**

- A) The difficulty of defining the agent's input/output boundaries
- B) The challenge of determining what remains unchanged when an action is performed
- C) The problem of fitting the agent into a specific hardware frame
- D) The issue of formatting the agent's output correctly

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The frame problem is a classic AI challenge: when an agent performs an action, how does it know what aspects of the world have changed and what remains the same? This is critical for efficient reasoning—without solving it, agents must re-evaluate everything after each action.

</details>

---

### Question 13 — Hard

**Which of the following best describes "emergent behavior" in multi-agent systems?**

- A) Behavior explicitly programmed into each agent
- B) Complex collective behavior that arises from simple individual agent interactions
- C) A bug that causes agents to behave unpredictably
- D) The behavior that emerges when agents are first deployed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Emergent behavior in multi-agent systems refers to complex, high-level patterns that arise from the interactions of multiple agents following simple rules. No single agent is programmed to produce this behavior—it emerges naturally from their collective interactions.

</details>

---

### Question 14 — Hard

**What is "satisficing" in the context of agent decision-making?**

- A) Always choosing the optimal solution regardless of cost
- B) Choosing the first solution that meets minimum acceptable criteria
- C) Never making a decision due to analysis paralysis
- D) Always deferring decisions to human operators

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Satisficing (a portmanteau of "satisfy" and "suffice") is a decision-making strategy where the agent chooses the first option that meets a threshold of acceptability, rather than exhaustively searching for the optimal solution. This is often more practical than optimization in complex environments.

</details>

---

### Question 15 — Hard

**What is the "intentional stance" as proposed by Daniel Dennett?**

- A) A physical posture that agents must maintain
- B) A strategy of predicting an entity's behavior by attributing beliefs, desires, and intentions to it
- C) A coding convention for agent implementation
- D) A security posture for protecting agent systems

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Dennett's intentional stance is a strategy for understanding and predicting behavior by treating an entity as if it has beliefs, desires, and rational intentions. It's foundational to how we conceptualize and design AI agents—we design them as if they are rational agents with goals.

</details>

---

### Question 16 — Easy

**What is an "environment" in agent terminology?**

- A) The physical computer running the agent
- B) Everything outside the agent that it can sense and interact with
- C) The programming language used to build the agent
- D) The agent's internal memory system

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The environment encompasses everything external to the agent that it can perceive and interact with. This includes the user, external APIs, databases, files, other agents, and any other resources the agent can observe or act upon.

</details>

---

### Question 17 — Easy

**Which of the following is an example of a simple reflex agent?**

- A) A chess-playing AI that plans several moves ahead
- B) A thermostat that turns on heat when temperature drops below a threshold
- C) A self-driving car navigating complex roads
- D) An AI assistant that writes code based on natural language descriptions

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A thermostat is a classic simple reflex agent—it maps a single percept (temperature) directly to an action (turn heat on/off) based on a condition, without any planning, learning, or internal state management.

</details>

---

### Question 18 — Medium

**What is the key difference between a "model-based" and "model-free" agent?**

- A) Model-based agents are slower; model-free agents are faster
- B) Model-based agents maintain an internal representation of the world; model-free agents map perceptions directly to actions
- C) Model-based agents use Python; model-free agents use JavaScript
- D) There is no practical difference

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Model-based agents maintain an internal model or representation of the world, allowing them to reason about unobserved states and predict consequences. Model-free agents skip this step and learn direct mappings from observations to actions, which can be faster but less flexible.

</details>

---

### Question 19 — Hard

**In multi-agent reinforcement learning, what does "non-stationarity" refer to?**

- A) The agents operating in different time zones
- B) The environment's dynamics change because other agents are also learning and adapting simultaneously
- C) The agents have inconsistent internet connections
- D) The reward function changes at random intervals

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Non-stationarity in multi-agent RL means the environment is constantly changing because each agent is simultaneously learning and adapting. What works today may not work tomorrow because other agents have changed their behavior, creating a moving target for learning algorithms.

</details>

---

### Question 20 — Easy

**What is the most basic form of an AI agent?**

- A) A neural network
- B) A function that maps inputs to outputs using an if-else rule
- C) A database query
- D) A CSS stylesheet

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: At its most basic, an AI agent is a function that maps inputs (perceptions) to outputs (actions) using rules. Simple reflex agents operate exactly this way—checking conditions and executing corresponding actions. More complex agents add reasoning, planning, and learning on top of this foundation.

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
| 7 | D | Medium |
| 8 | B | Medium |
| 9 | B | Medium |
| 10 | B | Medium |
| 11 | C | Hard |
| 12 | B | Hard |
| 13 | B | Hard |
| 14 | B | Hard |
| 15 | B | Hard |
| 16 | B | Easy |
| 17 | B | Easy |
| 18 | B | Medium |
| 19 | B | Hard |
| 20 | B | Easy |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 18-20 | Expert | You have a strong grasp of agent fundamentals |
| 14-17 | Proficient | Solid understanding; review hard topics |
| 10-13 | Developing | Good foundation; study agent architectures |
| 6-9 | Beginner | Review core concepts before advancing |
| 0-5 | Novice | Start with the agent fundamentals reading material |

---

**Next Quiz**: [02 - Tool Calling Quiz](02-tool-calling-quiz.md)
