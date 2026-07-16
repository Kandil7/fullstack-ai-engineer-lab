# AI Security Quiz: Prompt Injection

## Topic Overview

Prompt injection is a critical vulnerability in AI systems where malicious input attempts to override or manipulate the original system instructions. This quiz covers attack vectors, defenses, and best practices for protecting LLM-based applications.

### Key Concepts
- Direct vs. indirect prompt injection
- Jailbreaking techniques
- Instruction hierarchy and precedence
- Defensive prompt engineering
- Input sanitization strategies

---

## Quiz

### Question 1 — Easy
**What is the primary goal of a prompt injection attack?**

- A) To improve the model's response quality
- B) To extract the model's training data
- C) To override system instructions with attacker-controlled behavior
- D) To increase the model's inference speed

**Answer: C**

**Explanation:** Prompt injection aims to manipulate the model into following attacker instructions rather than the intended system prompts, potentially causing harmful outputs or unintended actions.

---

### Question 2 — Easy
**Which of the following is a direct prompt injection technique?**

- A) Embedding malicious instructions in a user query
- B) Placing instructions in retrieved documents
- C) Modifying the model's weights
- D) Changing the API endpoint

**Answer: A**

**Explanation:** Direct prompt injection involves the user explicitly including instructions in their input that attempt to override system prompts. Indirect injection places malicious content in external sources the model may retrieve.

---

### Question 3 — Easy
**What is a "jailbreak" in the context of AI security?**

- A) Physical access to the model's server
- B) A technique to bypass safety restrictions and content filters
- C) A method to improve model performance
- D) A way to reduce inference costs

**Answer: B**

**Explanation:** Jailbreaking refers to crafting inputs that circumvent the model's built-in safety guardrails, causing it to produce outputs that violate its intended usage policies.

---

### Question 4 — Medium
**Which defense technique uses separate input and instruction channels with different trust levels?**

- A) Output filtering
- B) Token limiting
- C) Instruction hierarchy
- D) Temperature reduction

**Answer: C**

**Explanation:** Instruction hierarchy establishes different trust levels for system prompts vs. user inputs, ensuring system-level instructions cannot be overridden by user-provided text.

---

### Question 5 — Medium
**In an indirect prompt injection attack, where is the malicious content placed?**

- A) In the system prompt
- B) In documents or data sources the model may retrieve
- C) In the model's training data
- D) In the API configuration

**Answer: B**

**Explanation:** Indirect injection embeds malicious instructions in external content (web pages, emails, documents) that the AI system processes, making it harder to detect and defend against.

---

### Question 6 — Medium
**Which of the following is NOT a recommended defense against prompt injection?**

- A) Input sanitization and validation
- B) Using user-controlled text directly in system prompts
- C) Implementing output filtering
- D) Separating system and user instruction contexts

**Answer: B**

**Explanation:** Directly embedding user input into system prompts creates injection vulnerabilities. User-controlled text should always be treated as untrusted data, not instructions.

---

### Question 7 — Medium
**What is the "sandwich defense" against prompt injection?**

- A) Placing the user input between two layers of trusted instructions
- B) Using multiple LLMs in parallel
- C) Encrypting all prompts before processing
- D) Limiting token count in responses

**Answer: A**

**Explanation:** The sandwich defense places user input between repeated system instructions, making it harder for injected instructions to override the original system prompt.

---

### Question 8 — Medium
**A model outputs sensitive internal data after a carefully crafted query. This is an example of:**

- A) Data exfiltration via prompt injection
- B) Normal model behavior
- C) A training data issue
- D) An API rate limiting problem

**Answer: A**

**Explanation:** When an attacker extracts sensitive information like system prompts, internal data, or confidential information through prompt manipulation, it constitutes data exfiltration.

---

### Question 9 — Hard
**Which defense combines both input validation and output monitoring?**

- A) Token-only approach
- B) Defense-in-depth strategy
- C) Single-layer filtering
- D) Model fine-tuning only

**Answer: B**

**Explanation:** Defense-in-depth implements multiple security layers — input validation, prompt isolation, output filtering, and monitoring — so no single point of failure can be exploited.

---

### Question 10 — Hard
**What makes prompt injection fundamentally different from traditional SQL injection?**

- A) SQL injection uses structured syntax while prompt injection uses natural language
- B) Prompt injection has no clear delimiter between code and data
- C) SQL injection is less dangerous
- D) There are effective parameterized queries for prompt injection

**Answer: B**

**Explanation:** Unlike SQL where parameterized queries clearly separate code from data, natural language lacks clear boundaries, making it difficult to distinguish instructions from user content.

---

### Question 11 — Hard
**An attacker embeds hidden instructions in a document processed by a RAG system. This is called:**

- A) Prompt leaking
- B) Model poisoning
- C) Indirect prompt injection
- D) Adversarial training

**Answer: C**

**Explanation:** When malicious content is embedded in external documents that a RAG system retrieves and processes, it's indirect prompt injection — the attacker doesn't interact with the model directly.

---

### Question 12 — Hard
**Which technique makes injected instructions appear as part of trusted system context?**

- A) Context window manipulation
- B) Role-based injection
- C) Instruction prefix attacks
- D) All of the above

**Answer: D**

**Explanation:** Attackers may manipulate context windows, assume system roles, or craft instruction prefixes to make their malicious content appear as trusted system-level instructions.

---

### Question 13 — Easy
**Which of these is a simple defense against prompt injection?**

- A) Removing all punctuation from inputs
- B) Limiting the length of user inputs
- C) Never using LLMs
- D) Running models locally only

**Answer: B**

**Explanation:** While not foolproof, limiting input length is a basic defense that reduces the space available for crafting complex injection attacks, though it should be combined with other techniques.

---

### Question 14 — Medium
**What is "prompt leaking"?**

- A) When the model generates random prompts
- B) When an attacker extracts the system prompt through manipulation
- C) When prompts are stored insecurely
- D) When the model refuses to respond

**Answer: B**

**Explanation:** Prompt leaking occurs when attackers craft inputs that cause the model to reveal its system prompt or hidden instructions, potentially exposing security-sensitive configurations.

---

### Question 15 — Hard
**Which approach is most effective against evolving prompt injection attacks?**

- A) Static blocklists of known attack patterns
- B) Dynamic, adaptive monitoring combined with continuous red teaming
- C) Increasing model temperature
- D) Reducing the model's context window

**Answer: B**

**Explanation:** Since injection techniques evolve constantly, static defenses become obsolete. Adaptive monitoring and continuous red teaming help identify and respond to new attack vectors.

---

### Question 16 — Easy
**What does "input sanitization" mean in the context of LLM security?**

- A) Removing all special characters
- B) Cleaning and validating user input before processing
- C) Encoding the entire prompt
- D) Randomizing the input order

**Answer: B**

**Explanation:** Input sanitization involves validating, cleaning, and normalizing user inputs to remove or neutralize potential injection attempts before they reach the model.

---

### Question 17 — Medium
**In a multi-agent system, prompt injection can:**

- A) Only affect individual agents
- B) Propagate across agent chains through shared context
- C) Never affect agent-to-agent communication
- D) Only happen in single-agent systems

**Answer: B**

**Explanation:** In multi-agent architectures, compromised agents can inject malicious instructions into shared context or pass manipulated outputs to other agents, spreading the attack across the system.

---

### Question 18 — Medium
**Which monitoring technique helps detect prompt injection in production?**

- A) Tracking only successful responses
- B) Analyzing input/output pairs for anomalous patterns
- C) Logging only error responses
- D) Monitoring system temperature only

**Answer: B**

**Explanation:** Monitoring input/output pairs helps detect injection by identifying unusual patterns like unexpected tool calls, policy violations, or outputs that deviate from expected behavior.

---

## Score Tracking

| Questions Answered | Correct | Incorrect | Score |
|-------------------|---------|-----------|-------|
|                   |         |           |       |

**Scoring Guide:**
- **15-18 correct (83-100%):** Excellent! You have strong knowledge of prompt injection security.
- **12-14 correct (67-82%):** Good foundation, review hard topics.
- **9-11 correct (50-66%):** Needs improvement, study the explanations.
- **Below 9 (<50%):** Review the topic overview and retake.

---

## Answer Key

| Question | Answer | Difficulty |
|----------|--------|------------|
| 1 | C | Easy |
| 2 | A | Easy |
| 3 | B | Easy |
| 4 | C | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | A | Medium |
| 8 | A | Medium |
| 9 | B | Hard |
| 10 | B | Hard |
| 11 | C | Hard |
| 12 | D | Hard |
| 13 | B | Easy |
| 14 | B | Medium |
| 15 | B | Hard |
| 16 | B | Easy |
| 17 | B | Medium |
| 18 | B | Medium |
