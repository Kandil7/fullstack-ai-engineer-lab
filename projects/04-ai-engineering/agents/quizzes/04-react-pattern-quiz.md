# Quiz 04: ReAct Pattern

> **Topic Overview**: The ReAct (Reason + Act) pattern is one of the most fundamental and widely-used agent architectures. This quiz covers the ReAct loop, reasoning chains, action selection, observation processing, variants like ReWOO, and comparisons with other patterns like chain-of-thought prompting and plan-and-solve.

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

**What does "ReAct" stand for?**

- A) React.js for AI agents
- B) Reason + Act
- C) Retrieve and Transform
- D) Recursive Action

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: ReAct stands for "Reason + Act." It's an agent pattern where the model alternates between reasoning about what to do (Thought) and taking actions (Action), then observing the results (Observation) before reasoning again.

</details>

---

### Question 2 — Easy

**What is the basic cycle of the ReAct pattern?**

- A) Think → Code → Deploy
- B) Thought → Action → Observation → repeat
- C) Plan → Execute → Stop
- D) Read → Write → Verify

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The ReAct cycle consists of three steps: Thought (reason about the current state and what to do next), Action (execute a tool or action), Observation (observe the result), then repeat until the goal is achieved.

</details>

---

### Question 3 — Easy

**In the ReAct pattern, what is the "Thought" step?**

- A) The user's input
- B) The LLM's internal reasoning about what it knows, what it needs, and what action to take next
- C) A database query
- D) The final output to the user

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The Thought step is the LLM's reasoning phase where it analyzes the current state, considers what information it has and what it still needs, and decides on the next action. This reasoning is typically hidden from the user but is critical for correct decision-making.

</details>

---

### Question 4 — Easy

**What is the "Action" step in the ReAct pattern?**

- A) Writing code
- B) The LLM selects and invokes a tool or performs an action based on its reasoning
- C) Sending an email
- D) Deploying to production

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: In the Action step, the LLM uses the conclusions from its reasoning (Thought) to select an appropriate tool, generate its arguments, and execute the action. This is where the agent interacts with the external world.

</details>

---

### Question 5 — Medium

**Why is the "Observation" step important in ReAct?**

- A) It's where the agent observes the user
- B) It provides feedback about what happened as a result of the action, informing the next reasoning cycle
- C) It's optional and can be skipped
- D) It only records logs

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The Observation step feeds the result of the action back into the reasoning loop. Without observations, the agent would be reasoning in a vacuum—unable to verify if its actions succeeded, failed, or produced unexpected results.

</details>

---

### Question 6 — Medium

**How does ReAct differ from pure Chain-of-Thought (CoT) prompting?**

- A) ReAct doesn't use reasoning
- B) CoT reasons without acting; ReAct alternates between reasoning and acting with real-world feedback
- C) They are identical
- D) CoT is always more effective than ReAct

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Chain-of-Thought prompting produces reasoning traces but never actually acts on them—it reasons in isolation. ReAct integrates reasoning with real actions and observations, allowing the agent to interact with the environment and adapt based on actual results.

</details>

---

### Question 7 — Medium

**What is a common stopping condition for the ReAct loop?**

- A) After exactly 3 iterations
- B) When the agent determines it has sufficient information to answer or when a maximum iteration limit is reached
- C) When the context window is completely full
- D) When the user sends a new message

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

</details>

**Explanation**: The ReAct loop stops when either: the agent determines it has enough information to provide a final answer, the goal has been achieved, or a predefined maximum iteration count is reached (to prevent infinite loops).

</details>

---

### Question 8 — Medium

**Which of the following is a potential issue with the ReAct pattern?**

- A) The agent can only perform one action per turn
- B) The agent may enter infinite loops if it keeps re-trying failed actions
- C) The agent never needs to reason
- D) ReAct only works with text-based tools

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Without proper stopping conditions, an agent using ReAct can enter infinite loops—repeatedly trying the same failed action or cycling between actions without progress. This is why iteration limits and error handling are essential in ReAct implementations.

</details>

---

### Question 9 — Medium

**What is "interleaved reasoning" in the ReAct pattern?**

- A) Mixing reasoning from multiple LLMs
- B) Reasoning that is interspersed with actions throughout the process rather than front-loaded
- C) Reasoning only about past actions
- D) Parallel reasoning across multiple threads

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Interleaved reasoning means the agent reasons at each step, taking actions based on that reasoning, observing results, then reasoning again. This contrasts with approaches that do all reasoning upfront before taking any actions.

</details>

---

### Question 10 — Medium

**In a typical ReAct prompt format, what does the "Observation:" section contain?**

- A) The user's original question
- B) The output returned by the tool that was called in the Action step
- C) The agent's final answer
- D) System configuration details

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The Observation section contains the result returned by the tool execution. This is fed back to the LLM so it can assess whether the action succeeded, what information was obtained, and what to do next.

</details>

---

### Question 11 — Hard

**What is "ReWOO" (Reasoning Without Observation) and how does it differ from ReAct?**

- A) ReWOO skips all reasoning and only acts
- B) ReWOO plans all actions upfront in a single reasoning step, then executes them all, reducing the number of LLM calls
- C) ReWOO is the same as ReAct with a different name
- D) ReWOO removes the Action step entirely

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: ReWOO (Reasoning Without Observation) plans all necessary actions in a single reasoning step upfront, then executes them all. This reduces the number of LLM calls compared to ReAct's step-by-step approach, but sacrifices the ability to adapt based on intermediate results.

</details>

---

### Question 12 — Hard

**What is the "error recovery" pattern in ReAct agents?**

- A) Restarting the entire agent from scratch
- B) When an action fails, the agent reasons about the failure and tries an alternative approach in the next Thought step
- C) Ignoring errors and continuing with the original plan
- D) Asking the user to fix the error manually

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Error recovery in ReAct uses the Observation step to detect failures, then the Thought step to analyze what went wrong and reason about alternative approaches. This enables agents to self-correct and adapt their strategy based on real-world outcomes.

</details>

---

### Question 13 — Hard

**How does ReAct handle the "hallucination" problem?**

- A) It doesn't address hallucination at all
- B) By grounding reasoning in real tool outputs (Observations), which constrains the agent's responses to verified facts
- C) By using a larger LLM
- D) By reducing the number of reasoning steps

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: ReAct partially addresses hallucination by grounding each reasoning step in real tool outputs. Since the agent reasons based on actual observations rather than making up facts, it's less likely to fabricate information—though hallucination in the Thought step itself is still possible.

</details>

---

### Question 14 — Hard

**What is the "planning ReAct" variant?**

- A) ReAct without any planning
- B) Combining high-level planning with the ReAct execution loop—the plan provides a roadmap, and ReAct handles the detailed steps
- C) Planning after completing all ReAct steps
- D) A version of ReAct that never takes actions

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Planning ReAct combines a high-level plan (created upfront or dynamically) with the ReAct execution loop. The plan provides strategic direction while ReAct handles tactical execution with real-world feedback, combining the benefits of both approaches.

</details>

---

### Question 15 — Hard

**What is the "ReAct vs. Plan-and-Solve" tradeoff?**

- A) ReAct is always better
- B) ReAct is more adaptive but slower; Plan-and-Solve is faster but less adaptable to unexpected results
- C) Plan-and-Solve is always better
- D) There is no practical difference between them

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: ReAct adapts at each step based on observations but requires an LLM call for each iteration. Plan-and-Solve creates a complete plan upfront and executes it—faster but less able to adapt when intermediate results reveal new information or failures.

</details>

---

### Question 16 — Easy

**Who introduced the ReAct pattern?**

- A) OpenAI researchers
- B) Google researchers (Yao et al., 2022)
- C) Meta researchers
- D) Microsoft researchers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The ReAct pattern was introduced by Shunyu Yao and colleagues at Princeton/Google in their 2022 paper "ReAct: Synergizing Reasoning and Acting in Language Models," which demonstrated the power of interleaving reasoning and action.

</details>

---

### Question 17 — Medium

**What happens when the ReAct loop reaches the maximum iteration limit?**

- A) The agent crashes
- B) The agent returns the best answer it has so far or an error message indicating it couldn't complete the task
- C) The agent automatically increases the limit
- D) The loop resets and starts over

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: When the maximum iteration limit is reached, the agent typically returns the best answer it has accumulated, or it returns an error indicating the task couldn't be completed within the allowed steps. This prevents infinite loops and excessive resource usage.

</details>

---

### Question 18 — Medium

**Why might you want to hide the Thought step from end users?**

- A) It's always irrelevant
- B) Reasoning traces may contain internal details, uncertainty, or verbose analysis that isn't useful or appropriate for the user
- C) It's always too short to show
- D) Users can't read text

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The Thought step may contain uncertain reasoning, internal deliberation, or verbose analysis that would confuse or concern users. Hiding it provides a cleaner user experience while still benefiting from the reasoning capability internally.

</details>

---

### Question 19 — Hard

**What is "self-consistency" checking in ReAct?**

- A) Checking if the agent is consistent in personality
- B) Running multiple ReAct trajectories and selecting the answer that appears most frequently across all runs
- C) Checking if the code compiles
- D) Ensuring the agent uses the same tool every time

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Self-consistency runs the same ReAct process multiple times (with temperature > 0) and selects the most common answer across all runs. This reduces variance and improves reliability by leveraging the wisdom of multiple reasoning paths.

</details>

---

### Question 20 — Easy

**In a ReAct agent, what comes first: Thought or Action?**

- A) Action
- B) Thought
- C) They happen simultaneously
- D) It depends on the specific implementation

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: In the ReAct pattern, Thought always comes before Action. The agent reasons about what it knows and what to do, then takes an action based on that reasoning. This ensures actions are deliberate rather than random.

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
| 18-20 | Expert | Excellent understanding of ReAct patterns |
| 14-17 | Proficient | Strong knowledge; explore advanced variants |
| 10-13 | Developing | Good foundation; implement a ReAct agent |
| 6-9 | Beginner | Review the ReAct paper and examples |
| 0-5 | Novice | Start with basic agent loop concepts |

---

**Previous Quiz**: [03 - Agent Memory](03-agent-memory-quiz.md) | **Next Quiz**: [05 - Planning & Reasoning](05-planning-reasoning-quiz.md)
