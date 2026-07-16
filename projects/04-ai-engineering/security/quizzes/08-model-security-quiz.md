# AI Security Quiz: Model Security

## Topic Overview

Model security encompasses protecting AI models from theft, tampering, adversarial attacks, and unauthorized access. This quiz covers model protection techniques, adversarial robustness, supply chain security, and secure model deployment practices.

### Key Concepts
- Model theft and intellectual property protection
- Adversarial attacks on models
- Model supply chain security
- Secure model serving
- Watermarking and fingerprinting

---

## Quiz

### Question 1 — Easy
**What is "model theft" in AI security?**

- A) Physical theft of servers
- B) Unauthorized copying or extraction of trained model weights
- C) Stealing training data only
- D) Stealing API keys

**Answer: B**

**Explanation:** Model theft involves unauthorized extraction of model weights or architecture, allowing attackers to replicate proprietary models without the development investment.

---

### Question 2 — Easy
**Why should model endpoints be protected with authentication?**

- A) To improve response time
- B) To prevent unauthorized access and abuse
- C) To increase model accuracy
- D) To reduce costs

**Answer: B**

**Explanation:** Authentication ensures only authorized users can access and use the model, preventing abuse, unauthorized usage, and potential exposure of model capabilities.

---

### Question 3 — Easy
**What is an "adversarial example" in AI security?**

- A) A well-crafted user prompt
- B) A specially modified input designed to cause incorrect model outputs
- C) An example from the training data
- D) A model's best prediction

**Answer: B**

- **Explanation:** Adversarial examples are inputs deliberately crafted to cause models to make errors, often with imperceptible modifications that are invisible to humans.

---

### Question 4 — Medium
**What is "model watermarking"?**

- A) Adding visible logos to model outputs
- B) Embedding unique identifiers in models to prove ownership
- C) Printing model documentation
- D) Labeling model parameters

**Answer: B**

**Explanation:** Model watermarking embeds identifiable patterns in model behavior or weights that prove ownership, helping detect unauthorized copies of proprietary models.

---

### Question 5 — Medium
**What is "model inversion" in AI security?**

- A) Inverting the model's architecture
- B) Using model outputs to reconstruct sensitive training data
- C) Flipping model predictions
- D) Inverting the model's parameters

**Answer: B**

**Explanation:** Model inversion attacks use a model's outputs to reconstruct or infer sensitive information from its training data, potentially exposing private information.

---

### Question 6 — Medium
**What is "membership inference" attacks?**

- A) Inferring user membership in groups
- B) Determining whether specific data was used in model training
- C) Inferring model parameters
- D) Predicting model outputs

**Answer: B**

**Explanation:** Membership inference attacks determine if specific data records were part of the training set, potentially revealing privacy-sensitive information about individuals.

---

### Question 7 — Medium
**What is "model extraction"?**

- A) Downloading model files from servers
- B) Querying a model systematically to recreate its functionality
- C) Extracting training data
- D) Removing model features

**Answer: B**

**Explanation:** Model extraction involves making numerous queries to a model to approximate its behavior, potentially creating a knock-off that circumvents licensing or access controls.

---

### Question 8 — Medium
**What is the risk of "model poisoning"?**

- A) Models become too accurate
- B) Training data manipulation causes models to produce incorrect or malicious outputs
- C) Models consume too much memory
- D) Models run too slowly

**Answer: B**

**Explanation:** Model poisoning involves manipulating training data to cause models to learn incorrect patterns, potentially inserting backdoors or degrading performance in targeted ways.

---

### Question 9 — Hard
**What is a "backdoor attack" on an AI model?**

- A) Physical access to model servers
- B) Embedding hidden triggers that activate specific behaviors when present
- C) Deleting model checkpoints
- D) Modifying API endpoints

**Answer: B**

**Explanation:** Backdoor attacks embed hidden triggers in models that cause specific, attacker-controlled behaviors when activated by particular inputs, while appearing normal otherwise.

---

### Question 10 — Hard
**What is "federated learning security" concerned with?**

- A) Learning federation concepts
- B) Protecting distributed model training from malicious participants
- C) Federating API access
- D) Combining multiple databases

**Answer: B**

**Explanation:** Federated learning security addresses threats from malicious participants who may submit poisoned model updates, attempt to extract data, or compromise the distributed training process.

---

### Question 11 — Hard
**What is "model supply chain security"?**

- A) Securing physical delivery of hardware
- B) Ensuring integrity of models, libraries, and dependencies throughout the development lifecycle
- C) Managing model versions
- D) Distributing model files

**Answer: B**

**Explanation:** Model supply chain security ensures that pre-trained models, frameworks, and dependencies haven't been tampered with, preventing compromised components from entering the AI system.

---

### Question 12 — Hard
**What is "differential privacy" in the context of model training?**

- A) Different privacy levels for different users
- B) Adding noise during training to provide mathematical privacy guarantees
- C) Encrypting training data
- D) Using different privacy policies

**Answer: B**

**Explanation:** Differential privacy in training adds calibrated noise to gradients or updates, providing mathematical guarantees that individual training examples cannot be inferred from the model.

---

### Question 13 — Easy
**Why should model outputs be validated?**

- A) To improve speed
- B) To ensure outputs don't contain harmful or unintended content
- C) To increase model size
- D) To reduce costs

**Answer: B**

**Explanation:** Output validation ensures that model responses meet safety, quality, and policy requirements before reaching users, catching potential issues like harmful content or sensitive data leakage.

---

### Question 14 — Medium
**What is "concept drift" monitoring for model security?**

- A) Monitoring network traffic
- B) Detecting when model behavior changes unexpectedly
- C) Tracking model version changes
- D) Monitoring server performance

**Answer: B**

**Explanation:** Concept drift monitoring detects unexpected changes in model behavior that could indicate tampering, data poisoning, or degradation from adversarial attacks.

---

### Question 15 — Medium
**What is "model access logging" and why is it important?**

- A) Logging model parameters
- B) Recording all model queries for security auditing and anomaly detection
- C) Logging training progress
- D) Recording user feedback

**Answer: B**

**Explanation:** Access logging records all model interactions, enabling detection of unusual patterns like extraction attempts, abuse, or unauthorized access through security auditing.

---

### Question 16 — Easy
**What is "model serving security"?**

- A) Serving food to model developers
- B) Protecting deployed models from attacks during inference
- C) Storing model files securely
- D) Managing model versions

**Answer: B**

**Explanation:** Model serving security focuses on protecting deployed models during inference, including input validation, output filtering, resource protection, and access control.

---

### Question 17 — Hard
**What is a "canary token" in model security?**

- A) A bird-tracking device
- B) A deceptive marker that detects unauthorized access or copying
- C) A model performance metric
- D) A user authentication token

**Answer: B**

**Explanation:** Canary tokens are deceptive markers embedded in models or data that trigger alerts when accessed, helping detect unauthorized use or extraction of protected assets.

---

### Question 18 — Medium
**What is the purpose of "model encryption"?**

- A) Encrypting model documentation
- B) Protecting model weights and parameters from unauthorized access
- C) Encrypting training data
- D) Compressing model size

**Answer: B**

**Explanation:** Model encryption protects the intellectual property and sensitive information in model weights, ensuring that even if files are accessed, they remain unreadable without proper decryption.

---

## Score Tracking

| Questions Answered | Correct | Incorrect | Score |
|-------------------|---------|-----------|-------|
|                   |         |           |       |

**Scoring Guide:**
- **15-18 correct (83-100%):** Excellent! You have strong model security knowledge.
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
