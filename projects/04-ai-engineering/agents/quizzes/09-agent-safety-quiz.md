# Quiz 09: Agent Safety

> **Topic Overview**: Agent safety encompasses guardrails, content moderation, prompt injection defense, output filtering, and responsible AI practices. This quiz covers safety mechanisms, jailbreak prevention, red teaming, ethical considerations, and strategies for building agents that are safe, reliable, and trustworthy.

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

**What is "prompt injection" in the context of AI agents?**

- A) Adding prompts to the agent's configuration
- B) An attack where malicious input is crafted to manipulate the agent's behavior or bypass its instructions
- C) Injecting prompts into the database
- D) Adding new prompts to improve performance

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Prompt injection is an attack where an attacker crafts input designed to manipulate the LLM's behavior—overriding system instructions, extracting sensitive information, or causing the agent to perform unauthorized actions. It's one of the most significant security threats to LLM-based agents.

</details>

---

### Question 2 — Easy

**What is a "guardrail" in agent safety?**

- A) A physical barrier around the agent's server
- B) A mechanism that monitors, constrains, and validates agent inputs and outputs to prevent harmful behavior
- C) A firewall configuration
- D) A type of encryption

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Guardrails are safety mechanisms that monitor and constrain agent behavior. They can validate inputs (rejecting malicious prompts), filter outputs (removing harmful content), enforce policies (limiting tool usage), and trigger alerts when safety thresholds are exceeded.

</details>

---

### Question 3 — Easy

**What is "content moderation" in agent safety?**

- A) Moderating online forums
- B) The process of filtering or flagging harmful, inappropriate, or policy-violating content in agent inputs or outputs
- C) Moderating the agent's CPU usage
- D) Managing the agent's content creation

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Content moderation filters or flags harmful, inappropriate, or policy-violating content. This can include hate speech, violence, sexual content, misinformation, or any content that violates usage policies. It can be applied to both inputs and outputs.

</details>

---

### Question 4 — Easy

**Why is "least privilege" important for agent tool access?**

- A) It makes tools cheaper
- B) It limits the agent to only the tools and permissions necessary for its task, reducing potential harm
- C) It makes the agent faster
- D) It improves the agent's memory

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Least privilege ensures agents only have access to the tools and permissions necessary for their specific task. A research agent shouldn't have access to system administration tools; a chatbot shouldn't have file deletion capabilities. This limits potential damage from errors or attacks.

</details>

---

### Question 5 — Medium

**What is "jailbreaking" in the context of AI agents?**

- A) Breaking the agent out of jail
- B) Circumventing safety restrictions to make the agent perform actions it was designed to prevent
- C) Fixing bugs in the agent
- D) Deploying the agent to production

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Jailbreaking is the act of crafting inputs that circumvent the agent's safety restrictions—making it generate harmful content, bypass content filters, or perform unauthorized actions. Jailbreak techniques constantly evolve as defenses improve.

</details>

---

### Question 6 — Medium

**What is "red teaming" in agent safety?**

- A) Using red-colored equipment
- B) Deliberately testing the agent with adversarial inputs to find vulnerabilities and safety issues
- C) A code review process
- D) A deployment strategy

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Red teaming is a systematic approach to finding agent vulnerabilities by having teams (or automated systems) deliberately try to make the agent fail, produce harmful outputs, or bypass safety measures. It's essential for identifying weaknesses before attackers do.

</details>

---

### Question 7 — Medium

**What is "output filtering" in agent safety?**

- A) Filtering the agent's input
- B) Checking and modifying the agent's responses before they reach the user to remove harmful or policy-violating content
- C) Filtering network traffic
- D) Filtering the agent's memory

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Output filtering examines the agent's generated responses before delivering them to users. It can detect and remove harmful content, personal information, misinformation, or policy violations. This is a critical safety layer even when input filtering is in place.

</details>

---

### Question 8 — Medium

**What is a "safety taxonomy" in agent design?**

- A) A classification system for different types of safety risks and threats
- B) A taxonomy of agent types
- C) A biological classification of agents
- D) A type of safety equipment

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: A safety taxonomy is a classification system that categorizes different types of safety risks—prompt injection, data leakage, hallucination, misuse, bias, etc. Having a clear taxonomy helps teams systematically identify, assess, and mitigate safety threats.

</details>

---

### Question 9 — Medium

**What is "data leakage" in agent safety?**

- A) Water damage to agent hardware
- B) The agent inadvertently exposing sensitive, private, or confidential information
- C) Data being too slow to transfer
- D) The agent losing data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Data leakage occurs when the agent inadvertently exposes sensitive information—PII, confidential business data, API keys, or other private information. This can happen through outputs, tool calls, error messages, or logs. Preventing data leakage is a critical safety concern.

</details>

---

### Question 10 — Medium

**What is the "Swiss cheese model" in agent safety?**

- A) A cheese-making safety protocol
- B) A defense-in-depth approach where multiple safety layers (each with holes) combine to prevent failures
- C) A model for predicting agent failures
- D) A Swiss programming paradigm

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The Swiss cheese model uses multiple safety layers, each with potential weaknesses ("holes"), but arranged so that holes in different layers don't align. This means a threat must pass through all layers to cause harm—making the overall system much more robust than any single layer.

</details>

---

### Question 11 — Hard

**What is an "indirect prompt injection" attack?**

- A) Injecting prompts through a proxy
- B) Embedding malicious instructions in external data sources (documents, web pages, emails) that the agent processes
- C) Using indirect language in prompts
- D) Injecting prompts through the API

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Indirect prompt injection embeds malicious instructions in external data sources that the agent processes—like hidden instructions in a document, website, or email. When the agent reads these sources (via RAG or tools), it may follow the embedded instructions, compromising safety.

</details>

---

### Question 12 — Hard

**What is "privilege escalation" in agent systems?**

- A) Giving the agent admin privileges
- B) An agent gaining more permissions or capabilities than it was originally authorized to have
- C) Making the agent faster
- D) Escalating the agent's priority in the queue

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Privilege escalation occurs when an agent gains unauthorized access to additional permissions, tools, or data. This can happen through prompt injection, exploiting vulnerabilities in tool APIs, or social engineering. Preventing privilege escalation requires strict access controls.

</details>

---

### Question 13 — Hard

**What is "alignment" in the context of agent safety?**

- A) Aligning multiple agents in a row
- B) Ensuring the agent's behavior and goals are aligned with human values, intentions, and safety requirements
- C) Aligning the agent's text to the left
- D) Matching the agent's output to a template

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Alignment ensures the agent's behavior, goals, and outputs align with human values, intentions, and safety requirements. An aligned agent pursues its intended purpose without causing unintended harm, even in edge cases or when faced with adversarial inputs.

</details>

---

### Question 14 — Hard

**What is "canary deployment" for agent safety?**

- A) Using canaries to detect agent failures
- B) Gradually rolling out agent changes to a small subset of users first to detect issues before full deployment
- C) Deploying the agent in a mine
- D) A fast deployment strategy

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Canary deployment gradually introduces agent changes to a small percentage of users first. This allows teams to detect safety issues, performance problems, or unexpected behavior before rolling out to all users—minimizing the blast radius of potential issues.

</details>

---

### Question 15 — Hard

**What is "toxicity detection" in agent safety?**

- A) Detecting poison in the agent's water supply
- B) Automated detection of harmful, offensive, or inappropriate content in agent inputs and outputs
- C) Detecting toxic chemicals
- D) A method for detecting agent bugs

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Toxicity detection uses classifiers and models to automatically identify harmful content—hate speech, violence, sexual content, harassment, and other policy violations. It's a key component of content moderation guardrails for agents.

</details>

---

### Question 16 — Easy

**What is the purpose of a "usage policy" for AI agents?**

- A) To document how to use the agent's API
- B) To define acceptable use cases, prohibited behaviors, and safety requirements
- C) To set pricing
- D) To describe the agent's architecture

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A usage policy defines what the agent can and cannot be used for, acceptable use cases, prohibited behaviors, safety requirements, and consequences for violations. It provides clear guidelines for users and helps prevent misuse.

</details>

---

### Question 17 — Medium

**What is "rate limiting" as a safety mechanism?**

- A) Limiting the agent's response speed
- B) Restricting the number of requests a user can make to prevent abuse and resource exhaustion
- C) Limiting the agent's memory usage
- D) Slowing down the agent's training

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rate limiting restricts the number of requests a user or client can make within a time period. As a safety mechanism, it prevents abuse, resource exhaustion, and denial-of-service attacks. It's a simple but effective safety measure.

</details>

---

### Question 18 — Medium

**What is "output validation" in agent safety?**

- A) Validating the user's input
- B) Checking the agent's output against safety criteria, format requirements, and policy rules before delivery
- C) Validating the database schema
- D) Checking if the output is in the right format for the database

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Output validation checks the agent's generated output against safety criteria, format requirements, and policy rules. It can verify the output doesn't contain harmful content, sensitive information, or policy violations before delivering it to the user.

</details>

---

### Question 19 — Hard

**What is the "alignment tax" in agent safety?**

- A) A tax on aligned agents
- B) The performance or efficiency cost of implementing safety measures and alignment techniques
- C) A tax incentive for building safe agents
- D) The cost of hiring safety experts

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The alignment tax is the cost (in performance, latency, or capability) of implementing safety measures. Adding guardrails, content filtering, and safety checks takes resources and can reduce the agent's capabilities or speed. Balancing safety with utility is a key challenge.

</details>

---

### Question 20 — Easy

**What is the primary goal of agent safety?**

- A) Making the agent as fast as possible
- B) Preventing the agent from causing harm to users, systems, or society
- C) Making the agent as smart as possible
- D) Reducing the agent's cost

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The primary goal of agent safety is preventing harm—protecting users from harmful outputs, preventing the agent from performing dangerous actions, safeguarding sensitive data, and ensuring the agent operates within ethical and legal boundaries.

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
| 8 | A | Medium |
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
| 18-20 | Expert | Excellent safety knowledge |
| 14-17 | Proficient | Strong understanding; conduct red teaming exercises |
| 10-13 | Developing | Good foundation; implement safety guardrails |
| 6-9 | Beginner | Review safety concepts and best practices |
| 0-5 | Novice | Prioritize safety training before building agents |

---

**Previous Quiz**: [08 - Agent Evaluation](08-agent-evaluation-quiz.md) | **Next Quiz**: [10 - Production Agents](10-production-agents-quiz.md)
