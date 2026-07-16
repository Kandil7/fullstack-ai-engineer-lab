# Quiz 08: Agent Evaluation

> **Topic Overview**: Evaluating AI agents requires measuring correctness, efficiency, reliability, and safety across multiple dimensions. This quiz covers evaluation metrics, benchmarking approaches, A/B testing, human evaluation, automated testing frameworks, regression testing, and strategies for systematically measuring and improving agent performance.

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

**Why is evaluating AI agents more challenging than evaluating traditional software?**

- A) Agents are simpler than traditional software
- B) Agent outputs are often non-deterministic and correctness may be subjective
- C) Agents don't produce any output
- D) Traditional software is harder to test

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: AI agents produce non-deterministic outputs (same input may produce different outputs), correctness is often subjective or contextual, and there are multiple valid solutions to many problems. This makes traditional pass/fail testing insufficient.

</details>

---

### Question 2 — Easy

**What is a "benchmark" in agent evaluation?**

- A) A wooden desk for the agent
- B) A standardized set of tasks and metrics used to measure agent performance
- C) A tool for debugging
- D) A deployment platform

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A benchmark is a standardized evaluation framework with predefined tasks, expected outcomes, and metrics. It enables consistent comparison of agent performance across different models, configurations, and versions.

</details>

---

### Question 3 — Easy

**What is "task completion rate" in agent evaluation?**

- A) How fast the agent completes tasks
- B) The percentage of tasks the agent successfully completes out of all attempted tasks
- C) How many tasks are in the queue
- D) The complexity of completed tasks

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Task completion rate is the percentage of tasks successfully completed. It's a fundamental metric—measuring whether the agent can achieve the desired outcome. However, it doesn't capture quality, efficiency, or safety.

</details>

---

### Question 4 — Easy

**What is "hallucination rate" in agent evaluation?**

- A) The rate at which the agent generates incorrect or fabricated information
- B) The rate at which the agent hallucinates during processing
- C) The agent's creativity score
- D) The rate of visual output generation

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

</details>

**Explanation**: Hallucination rate measures how often the agent generates incorrect, fabricated, or unsupported information. This is a critical safety metric—high hallucination rates indicate the agent is making up facts, which can lead to harmful outcomes.

</details>

---

### Question 5 — Medium

**What is "human-in-the-loop" evaluation?**

- A) Evaluating the agent using only automated metrics
- B) Having human evaluators assess agent outputs for quality, correctness, and appropriateness
- C) Evaluating the agent's ability to interact with humans
- D) Humans programming the evaluation tests

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Human-in-the-loop evaluation uses human judgment to assess agent outputs. Humans can evaluate nuance, appropriateness, and subjective quality that automated metrics miss. This is essential for evaluating open-ended tasks like writing, reasoning, or creative work.

</details>

---

### Question 6 — Medium

**What is an "eval set" (evaluation dataset)?**

- A) A set of evaluation tools
- B) A collection of test cases with inputs, expected outputs, and metadata used to systematically evaluate agent performance
- C) A configuration file for the agent
- D) A set of production data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An eval set is a curated collection of test cases, each with inputs, expected outputs, difficulty ratings, and tags. It provides systematic, reproducible evaluation of agent performance across different scenarios and capabilities.

</details>

---

### Question 7 — Medium

**What is "A/B testing" in the context of agent evaluation?**

- A) Testing two different agents with identical inputs to compare their performance
- B) Testing the agent's A and B functionalities
- C) Testing in environment A and environment B
- D) Binary testing (pass/fail only)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: A/B testing compares two versions of an agent (or two configurations) by running identical test cases through both and measuring performance differences. This helps identify which version performs better on specific metrics.

</details>

---

### Question 8 — Medium

**What is the "regression" problem in agent evaluation?**

- A) Agent performance improving over time
- B) Agent performance degrading on previously-passing test cases after changes
- C) The agent regressing to earlier behavior
- D) Agent memory growing over time

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Regression occurs when changes to an agent (prompt updates, model changes, new tools) cause it to fail on test cases it previously passed. Regression testing—running existing eval sets after changes—is critical for preventing performance degradation.

</details>

---

### Question 9 — Medium

**What is "latency" measurement in agent evaluation?**

- A) The agent's typing speed
- B) The time elapsed from user input to complete agent response
- C) The agent's network speed
- D) The time to deploy the agent

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Latency measures the time from user input to complete agent response. It includes LLM inference time, tool execution time, and network overhead. Latency is critical for user experience—high latency can make agents unusable for interactive applications.

</details>

---

### Question 10 — Medium

**What is "cost per task" in agent evaluation?**

- A) The cost of building the agent
- B) The total API and compute cost to complete a single task
- C) The developer's hourly rate
- D) The cost of the evaluation dataset

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cost per task measures the total API and compute costs to complete a single task. This includes LLM token costs, tool API costs, and compute infrastructure costs. It's essential for understanding the economic viability of the agent.

</details>

---

### Question 11 — Hard

**What is "fuzzy matching" in agent evaluation?**

- A) Matching agents that are similar
- B) Evaluating agent outputs by comparing them to expected outputs with tolerance for minor variations
- C) Matching test cases randomly
- D) A method for finding similar evaluation datasets

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Fuzzy matching evaluates agent outputs by comparing them to expected outputs with tolerance for minor variations. For example, "New York City" and "New York" might both be considered correct. This is essential when there are multiple valid representations of the same answer.

</details>

---

### Question 12 — Hard

**What is "grader reliability" in automated evaluation?**

- A) The reliability of the agent being graded
- B) The consistency and accuracy of the automated grading system itself
- C) The reliability of the network connection during grading
- D) The reliability of the human graders

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Grader reliability measures whether the automated evaluation system produces consistent, accurate results. If the grader itself is unreliable (inconsistent, biased, or incorrect), evaluation results are meaningless. Grader reliability must be validated independently.

</details>

---

### Question 13 — Hard

**What is "multi-dimensional evaluation" in agent assessment?**

- A) Evaluating the agent in multiple environments
- B) Assessing agent performance across multiple dimensions (accuracy, latency, cost, safety, etc.) simultaneously
- C) Evaluating multiple agents at once
- D) Using multiple evaluation tools

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Multi-dimensional evaluation assesses agent performance across multiple criteria simultaneously—correctness, speed, cost, safety, user satisfaction, etc. A high-performing agent must balance these dimensions, as optimizing one may degrade another.

</details>

---

### Question 14 — Hard

**What is "evaluation contamination" in agent benchmarks?**

- A) The benchmark being corrupted
- B) Test cases from the evaluation set leaking into the agent's training data or prompts
- C) The agent contaminating the evaluation environment
- D) Cross-contamination between different evaluation datasets

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Evaluation contamination occurs when test cases from the evaluation set appear in the agent's training data or context. This inflates performance scores artificially—the agent appears better because it has seen the answers before, not because it truly understands the task.

</details>

---

### Question 15 — Hard

**What is "process evaluation" vs "outcome evaluation"?**

- A) They are the same thing
- B) Process evaluation assesses HOW the agent works (steps taken, tools used); outcome evaluation assesses WHAT it produces
- C) Process evaluation is faster; outcome evaluation is slower
- D) Process evaluation is for debugging; outcome evaluation is for production

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Process evaluation examines the agent's reasoning steps, tool usage, and decision-making process. Outcome evaluation examines the final result. Both are important—an agent might produce a correct answer through incorrect reasoning, or a wrong answer through mostly correct reasoning.

</details>

---

### Question 16 — Easy

**What is a "golden set" in agent evaluation?**

- A) A set of gold-colored test cases
- B) A curated set of high-quality test cases with verified correct answers
- C) The most expensive evaluation dataset
- D) A set of production queries

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A golden set is a carefully curated collection of test cases where the expected outputs have been manually verified. It serves as the gold standard for evaluating agent accuracy and is used to validate other automated evaluation methods.

</details>

---

### Question 17 — Medium

**What is "coverage" in agent evaluation?**

- A) How much of the code is tested
- B) The percentage of important scenarios, edge cases, and capabilities that are tested
- C) How much documentation covers the agent
- D) The network coverage of the agent's API

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Coverage in agent evaluation measures what percentage of important scenarios and capabilities are tested. Low coverage means important behaviors may be untested. High coverage provides confidence that the agent handles a wide range of situations correctly.

</details>

---

### Question 18 — Medium

**What is "adversarial testing" in agent evaluation?**

- A) Testing the agent against adversarial weather
- B) Deliberately testing the agent with inputs designed to cause failures, errors, or harmful outputs
- C) Testing two agents against each other
- D) Testing the agent's competitive abilities

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Adversarial testing deliberately crafts inputs designed to cause failures—jailbreak attempts, ambiguous queries, edge cases, and inputs that might cause hallucinations or unsafe outputs. This identifies vulnerabilities that normal testing might miss.

</details>

---

### Question 19 — Hard

**What is the "Pareto frontier" in multi-objective agent evaluation?**

- A) A database of agent performance data
- B) The set of agent configurations where no single metric can be improved without degrading another
- C) The top 10% of agent configurations
- D) A graph showing agent performance over time

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The Pareto frontier represents the set of optimal trade-offs between competing objectives (e.g., accuracy vs. latency, quality vs. cost). Configurations on the Pareto frontier cannot improve one metric without making another worse—they represent the best achievable trade-offs.

</details>

---

### Question 20 — Easy

**What is the most basic evaluation metric for an agent?**

- A) Code coverage
- B) Whether the agent's output matches the expected answer
- C) The agent's memory usage
- D) The number of tools used

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The most basic metric is whether the agent's output matches the expected answer—often called "accuracy" or "exact match." While simple, it's the foundation of agent evaluation. More sophisticated metrics build on this basic concept.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | A | Easy |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | A | Medium |
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
| 18-20 | Expert | Excellent evaluation methodology knowledge |
| 14-17 | Proficient | Strong understanding; build evaluation pipelines |
| 10-13 | Developing | Good foundation; create evaluation datasets |
| 6-9 | Beginner | Review evaluation concepts and metrics |
| 0-5 | Novice | Start with basic testing and evaluation concepts |

---

**Previous Quiz**: [07 - Agent Communication](07-agent-communication-quiz.md) | **Next Quiz**: [09 - Agent Safety](09-agent-safety-quiz.md)
