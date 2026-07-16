# Quiz 09: AI Safety

## Topic Overview
This quiz covers AI safety principles, including content moderation, jailbreak prevention, prompt injection defense, bias detection, output filtering, ethical AI practices, and safety evaluation methods. Topics span the critical aspects of building safe and responsible AI systems.

---

## Questions

### Question 1
**What is "jailbreaking" in the context of AI safety?**

- A) Breaking the AI's hardware
- B) Circumventing safety restrictions to make the model produce harmful content
- C) Installing the AI on a jailbroken phone
- D) Breaking the model's encryption

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Jailbreaking refers to techniques that attempt to bypass an AI model's safety guardrails and restrictions. Attackers use creative prompts to make models generate harmful, inappropriate, or restricted content. Common jailbreak techniques include role-playing scenarios, encoding harmful requests, and exploiting edge cases in safety training.
</details>

---

### Question 2
**What is "prompt injection" in AI security?**

- A) Injecting prompts into the model's training data
- B) Crafting malicious inputs that override the model's instructions
- C) Injecting API keys into prompts
- D) Adding prompts to the model's output

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Prompt injection is an attack where malicious user inputs are crafted to override or bypass system prompt instructions. For example, users might try to make the AI ignore safety guidelines, reveal confidential information, or perform unauthorized actions. This is a critical security concern that requires defensive prompt design and input validation.
</details>

---

### Question 3
**What is "content moderation" in AI systems?**

- A) Moderating user forums
- B) Automatically detecting and filtering harmful, inappropriate, or policy-violating content
- C) Moderating API usage
- D) Reviewing model training data

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Content moderation automatically detects and filters harmful, inappropriate, or policy-violating content in both inputs and outputs. It includes detecting hate speech, violence, sexual content, misinformation, and other harmful categories. Moderation can use rule-based filters, ML classifiers, or LLM-based evaluation.
</details>

---

### Question 4
**What is "output filtering" in AI safety?**

- A) Filtering the model's training data
- B) Checking and modifying the model's outputs before they reach users
- C) Filtering API responses
- D) Filtering user inputs only

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Output filtering checks the model's generated content before it reaches users, removing or modifying harmful, inaccurate, or policy-violating content. It acts as a final safety layer after generation. Output filtering can use classifiers, rule-based systems, or secondary LLM evaluation to ensure outputs meet safety standards.
</details>

---

### Question 5
**What is "input validation" in AI safety?**

- A) Validating the model's inputs during training
- B) Checking user inputs for malicious content before processing
- C) Validating API keys
- D) Checking the model's configuration

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Input validation checks user inputs for malicious content, prompt injection attempts, and policy violations before they reach the model. This includes detecting injection patterns, filtering harmful requests, and validating input formats. Input validation is the first line of defense against adversarial attacks.
</details>

---

### Question 6
**What is "alignment" in AI safety?**

- A) Aligning the model's parameters
- B) Ensuring the AI system's behavior matches human values and intentions
- C) Aligning the API endpoints
- D) Aligning the model with the hardware

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** AI alignment ensures that AI systems behave in ways that are consistent with human values, intentions, and expectations. This includes being helpful, harmless, and honest. Alignment research develops techniques to make AI systems more controllable, interpretable, and aligned with human goals.
</details>

---

### Question 7
**What is "bias detection" in AI systems?**

- A) Detecting hardware biases
- B) Identifying unfair preferences or discrimination in model outputs
- C) Detecting network biases
- D) Identifying code biases

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Bias detection identifies unfair preferences, stereotypes, or discrimination in AI model outputs. This includes gender, racial, cultural, and other forms of bias. Detection methods include testing with diverse inputs, analyzing output patterns across demographic groups, and using bias evaluation benchmarks. Detecting bias is the first step toward mitigating it.
</details>

---

### Question 8
**What is a "safety guardrail" in AI systems?**

- A) A physical barrier around the AI hardware
- B) Technical mechanisms that prevent the AI from producing harmful outputs
- C) A security fence around the data center
- D) A firewall for the API

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Safety guardrails are technical mechanisms that constrain AI behavior to prevent harmful outputs. They include input filters, output classifiers, system prompts with safety instructions, content moderation, and behavioral constraints. Guardrails provide multiple layers of protection against misuse and harmful content generation.
</details>

---

### Question 9
**What is "red teaming" in AI safety?**

- A) Using red-colored interfaces
- B) Systematically testing AI systems by attempting to make them fail or produce harmful outputs
- C) Training the model with red data
- D) Deploying the model to red (test) environments

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Red teaming involves systematically testing AI systems by attempting to make them fail, produce harmful outputs, or bypass safety measures. Red teams use adversarial techniques to identify vulnerabilities before malicious actors can exploit them. Red teaming is essential for identifying and fixing safety issues before deployment.
</details>

---

### Question 10
**What is "toxicity" in AI content moderation?**

- A) The model's processing speed
- B) The presence of harmful, offensive, or inappropriate content
- C) The model's memory usage
- D) The API's response time

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Toxicity refers to harmful, offensive, or inappropriate content including hate speech, violence, sexual content, harassment, and other harmful categories. Toxicity detection uses classifiers trained to identify these categories. Modern content moderation systems combine automated detection with human review for nuanced cases.
</details>

---

### Question 11
**What is "adversarial testing" in AI safety?**

- A) Testing the model with friendly inputs
- B) Deliberately testing the model with challenging or adversarial inputs
- C) Testing the model's speed
- D) Testing the model's accuracy on clean data

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Adversarial testing deliberately challenges the model with inputs designed to cause failures, reveal biases, or bypass safety measures. This includes edge cases, ambiguous inputs, prompt injection attempts, and adversarial examples. Adversarial testing helps identify vulnerabilities that normal testing might miss.
</details>

---

### Question 12
**What is "responsible AI" and why does it matter?**

- A) AI that is responsible for its actions
- B) A framework for developing AI systems that are ethical, transparent, and beneficial
- C) AI that manages responsibility assignments
- D) AI that is accountable to users

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Responsible AI is a framework for developing AI systems that are ethical, transparent, fair, and beneficial to society. It encompasses fairness, accountability, transparency, safety, and privacy. Responsible AI practices help organizations build trustworthy AI systems and avoid harmful consequences.
</details>

---

### Question 13
**What is "explainability" in AI safety?**

- A) Explaining the AI to users
- B) The ability to understand and explain how the AI makes decisions
- C) Explaining the API documentation
- D) Explaining the model's architecture

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Explainability (or interpretability) is the ability to understand and explain how an AI model makes decisions. This includes understanding which features influenced the decision, why certain outputs were generated, and how the model processes inputs. Explainability is crucial for trust, debugging, and identifying biases or errors.
</details>

---

### Question 14
**What is "model auditing" in AI safety?**

- A) Auditing the model's training data
- B) Systematically reviewing model behavior, performance, and safety compliance
- C) Auditing the model's code
- D) Auditing the model's hardware

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Model auditing systematically reviews model behavior, performance, and safety compliance. Audits examine training data, model outputs, bias metrics, safety tests, and compliance with regulations. Regular audits help identify issues, ensure accountability, and maintain trust. They're increasingly required by regulations like the EU AI Act.
</details>

---

### Question 15
**What is "differential privacy" in AI?**

- A) Different privacy levels for different users
- B) A technique that adds noise to protect individual data points while enabling aggregate analysis
- C) Privacy that differs between models
- D) Different privacy policies for different data types

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Differential privacy adds mathematical noise to data or query results to protect individual privacy while enabling useful aggregate analysis. It provides provable privacy guarantees, ensuring that the presence or absence of any individual's data doesn't significantly affect the output. This is crucial for training AI on sensitive data.
</details>

---

### Question 16
**What is "watermarking" in AI-generated content?**

- A) Adding visible watermarks to images
- B) Embedding invisible signals in AI outputs to identify their source
- C) Marking the model's training data
- D) Watermarking the API responses

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** AI watermarking embeds invisible signals in generated content (text, images, audio) that can be detected to identify the content as AI-generated. This helps combat misinformation, deepfakes, and intellectual property theft. Watermarking techniques must be robust against modification while not degrading content quality.
</details>

---

### Question 17
**What is "policy compliance" in AI safety?**

- A) Complying with the model's training policy
- B) Ensuring the AI system adheres to organizational policies and regulations
- C) Complying with API terms of service
- D) Following coding standards

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Policy compliance ensures that AI systems adhere to organizational policies, industry standards, and legal regulations (like GDPR, CCPA, EU AI Act). This includes data handling, content moderation, transparency requirements, and safety standards. Compliance is essential for legal operation and building user trust.
</details>

---

### Question 18
**What is "harmful content" in AI safety?**

- A) Content that harms the model's performance
- B) Content that could cause physical, psychological, or societal harm
- C) Content that uses too many tokens
- D) Content that is too long

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Harmful content includes anything that could cause physical, psychological, or societal harm. This encompasses violence, hate speech, self-harm promotion, misinformation, illegal activities, harassment, and other dangerous content. AI systems must be designed to detect and prevent generation of harmful content.
</details>

---

### Question 19
**What is "safety evaluation" in AI development?**

- A) Evaluating the model's speed
- B) Systematically testing the model for safety issues and vulnerabilities
- C) Evaluating the model's accuracy
- D) Evaluating the model's cost

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Safety evaluation systematically tests AI models for safety issues, vulnerabilities, and harmful behaviors. This includes red teaming, bias testing, toxicity evaluation, robustness testing, and compliance verification. Safety evaluation should be ongoing throughout development and deployment, not just at initial release.
</details>

---

### Question 20
**What is "constitutional AI" in safety research?**

- A) AI that follows constitutional law
- B) An approach where AI learns to follow a set of principles or "constitution"
- C) AI that creates constitutions
- D) AI used in constitutional governments

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Constitutional AI (CAI) is an approach where AI systems learn to follow a set of explicit principles or a "constitution." The model is trained to generate responses that adhere to these principles, and a critic model evaluates responses against the constitution. This approach aims to create more predictable, controllable, and aligned AI systems.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Medium | | |
| 5 | Medium | | |
| 6 | Easy | | |
| 7 | Easy | | |
| 8 | Easy | | |
| 9 | Medium | | |
| 10 | Easy | | |
| 11 | Medium | | |
| 12 | Medium | | |
| 13 | Medium | | |
| 14 | Medium | | |
| 15 | Hard | | |
| 16 | Medium | | |
| 17 | Medium | | |
| 18 | Easy | | |
| 19 | Medium | | |
| 20 | Hard | | |

**Score:** ____/20

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 8 | B | 15 | B |
| 2 | B | 9 | B | 16 | B |
| 3 | B | 10 | B | 17 | B |
| 4 | B | 11 | B | 18 | B |
| 5 | B | 12 | B | 19 | B |
| 6 | B | 13 | B | 20 | B |
| 7 | B | 14 | B | | |

---

*Generated for AI Automation Lab - Quiz 09 of 09*