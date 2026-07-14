# AI Security Quiz: Output Filtering

## Topic Overview

Output filtering ensures that AI-generated content meets safety, compliance, and quality standards before reaching users. This quiz covers filtering strategies, response sanitization, and techniques for detecting and blocking harmful or sensitive outputs.

### Key Concepts
- Content safety classifiers
- Sensitive data detection in outputs
- Response sanitization techniques
- PII filtering and redaction
- Policy compliance validation

---

## Quiz

### Question 1 — Easy
**What is the primary purpose of output filtering in AI systems?**

- A) To increase response speed
- B) To prevent harmful or sensitive content from reaching users
- C) To reduce token usage
- D) To improve model training

**Answer: B**

**Explanation:** Output filtering acts as the final security layer, ensuring that AI-generated responses don't contain harmful, inappropriate, or sensitive information before delivery to users.

---

### Question 2 — Easy
**Which of the following should be filtered from AI outputs?**

- A) Factual information
- B) Personally identifiable information (PII)
- C) Helpful explanations
- D) Code suggestions

**Answer: B**

**Explanation:** PII such as names, addresses, phone numbers, and financial data should be filtered or redacted from outputs to protect user privacy and comply with regulations.

---

### Question 3 — Easy
**What is "output sanitization"?**

- A) Cleaning the model's training data
- B) Processing generated content to remove or modify unsafe elements
- C) Formatting output for display
- D) Compressing output text

**Answer: B**

**Explanation:** Output sanitization involves processing AI-generated content to remove, modify, or flag elements that violate safety policies, privacy requirements, or content guidelines.

---

### Question 4 — Medium
**In a multi-stage filtering pipeline, what does the "confidence threshold" control?**

- A) How fast the model generates text
- B) The minimum certainty required to allow or block content
- C) The maximum response length
- D) The number of API calls allowed

**Answer: B**

**Explanation:** Confidence thresholds determine how certain the system must be that content is safe (or harmful) before taking action, helping balance safety with usability.

---

### Question 5 — Medium
**What is a "false negative" in output filtering?**

- A) Correctly blocking harmful content
- B) Allowing harmful content to pass through the filter
- C) Blocking safe content incorrectly
- D) The filter crashing during processing

**Answer: B**

**Explanation:** False negatives are dangerous because harmful content bypasses the filter and reaches users, potentially causing harm or policy violations.

---

### Question 6 — Medium
**Which technique detects PII in AI-generated outputs?**

- A) Token counting
- B) Named Entity Recognition (NER) and pattern matching
- C) Increasing model temperature
- D) Reducing output length

**Answer: B**

**Explanation:** NER identifies entities like names, organizations, and locations, while pattern matching detects structured data like phone numbers, emails, and SSNs in generated text.

---

### Question 7 — Medium
**What is "content policy enforcement" in output filtering?**

- A) Enforcing API usage limits
- B) Checking generated content against defined safety and compliance rules
- C) Enforcing response formatting
- D) Managing user permissions

**Answer: B**

**Explanation:** Content policy enforcement validates that generated outputs comply with safety guidelines, legal requirements, and organizational policies before delivery.

---

### Question 8 — Medium
**Why might output filtering introduce latency?**

- A) Filtering is instantaneous
- B) Analysis and classification of generated content requires computation
- C) Filtering only affects training time
- D) Models generate faster with filtering

**Answer: B**

**Explanation:** Output filtering adds processing time as the system must analyze generated content using classifiers, pattern matchers, and policy checkers before returning results.

---

### Question 9 — Hard
**What is "toxicity scoring" in output filtering?**

- A) Counting the number of words
- B) Assigning numerical values to the harmfulness of generated content
- C) Measuring response quality
- D) Tracking user feedback

**Answer: B**

**Explanation:** Toxicity scoring uses classifiers to assign numerical values representing how harmful content is, allowing systems to set thresholds for blocking, warning, or allowing responses.

---

### Question 10 — Hard
**How does "context-aware filtering" improve output safety?**

- A) It ignores all context
- B) It evaluates content considering the full conversation and user intent
- C) It only checks the last sentence
- D) It randomizes filtering decisions

**Answer: B**

**Explanation:** Context-aware filtering considers the entire conversation history and user intent, helping distinguish between genuinely harmful content and benign discussions about sensitive topics.

---

### Question 11 — Hard
**What challenge does "adversarial output evasion" present?**

- A) No challenge, filtering always works
- B) Carefully crafted outputs that bypass filters while remaining harmful
- C) Filters that are too slow
- D) Outputs that are too long

**Answer: B**

**Explanation:** Adversarial evasion involves generating content that technically passes safety filters while still conveying harmful intent, requiring sophisticated detection methods.

---

### Question 12 — Hard
**Which approach handles "coded language" in outputs effectively?**

- A) Simple keyword matching
- B) Multi-signal analysis combining text patterns, context, and semantic understanding
- C) Only checking for explicit terms
- D) Ignoring potential coded language

**Answer: B**

**Explanation:** Coded language uses innocent-seeming words to convey harmful meanings. Effective detection requires analyzing multiple signals including word choice, context, and semantic patterns.

---

### Question 13 — Easy
**What is a "safety classifier" in the context of output filtering?**

- A) A model that classifies data types
- B) A system that categorizes content by potential harm level
- C) A user classification system
- D) A network classifier

**Answer: B**

**Explanation:** Safety classifiers analyze content and assign harm categories (hate speech, violence, self-harm, etc.) with confidence scores to guide filtering decisions.

---

### Question 14 — Medium
**What is "PII redaction" in output filtering?**

- A) Removing all text from outputs
- B) Masking or replacing personally identifiable information with placeholders
- C) Encrypting the entire output
- D) Logging all user data

**Answer: B**

**Explanation:** PII redaction identifies sensitive personal information in outputs and replaces it with placeholders (e.g., [NAME], [EMAIL]) to protect privacy while preserving context.

---

### Question 15 — Medium
**Which filter type handles "hallucinated" sensitive information?**

- A) Length filters
- B) Factual verification and source attribution checks
- C) Grammar checkers
- D) Translation filters

**Answer: B**

**Explanation:** Models can hallucinate sensitive information. Verification checks compare generated facts against known sources and flag claims that appear to reference private or protected data.

---

### Question 16 — Easy
**Why is real-time output filtering important?**

- A) It's not important
- B) It prevents harmful content from reaching users before delivery
- C) It only matters for stored outputs
- D) It improves model accuracy

**Answer: B**

**Explanation:** Real-time filtering catches harmful content before it reaches users, providing immediate protection rather than requiring post-hoc review and remediation.

---

### Question 17 — Hard
**What is "prompt leak detection" in output filtering?**

- A) Detecting when users try to steal prompts
- B) Identifying when generated outputs reveal system prompt content
- C) Finding errors in prompt templates
- D) Monitoring prompt usage

**Answer: B**

**Explanation:** Prompt leak detection identifies when outputs inadvertently contain system prompt content, which could reveal sensitive configuration or security measures.

---

### Question 18 — Medium
**How does "output rate limiting" contribute to safety?**

- A) It improves response quality
- B) It prevents abuse by limiting how quickly outputs can be generated
- C) It increases model speed
- D) It reduces costs only

**Answer: B**

**Explanation:** Rate limiting prevents abuse scenarios where attackers attempt to generate large volumes of harmful content, providing a throttle against automated attacks.

---

## Score Tracking

| Questions Answered | Correct | Incorrect | Score |
|-------------------|---------|-----------|-------|
|                   |         |           |       |

**Scoring Guide:**
- **15-18 correct (83-100%):** Excellent! You have strong output filtering knowledge.
- **12-14 correct (67-82%):** Good foundation, review hard topics.
- **9-11 correct (50-66%):** Needs improvement, study the explanations.
- **Below 9 (<50%):** Review the topic overview and retake.

---

## Answer Key

| Question | Answer | Difficulty |
|----------|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Medium |
| 9 | B | Hard |
| 10 | B | Hard |
| 11 | B | Hard |
| 12 | B | Hard |
| 13 | B | Easy |
| 14 | B | Medium |
| 15 | B | Medium |
| 16 | B | Easy |
| 17 | B | Hard |
| 18 | B | Medium |
