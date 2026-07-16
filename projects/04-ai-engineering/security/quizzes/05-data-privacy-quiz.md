# AI Security Quiz: Data Privacy

## Topic Overview

Data privacy in AI systems involves protecting sensitive information throughout the AI pipeline — from training data to user interactions. This quiz covers privacy regulations, data protection techniques, and best practices for handling personal and sensitive data in AI applications.

### Key Concepts
- PII detection and handling
- Data anonymization and pseudonymization
- Privacy regulations (GDPR, CCPA)
- Differential privacy
- Secure data storage and transmission

---

## Quiz

### Question 1 — Easy
**What does PII stand for in data privacy?**

- A) Private Internal Information
- B) Personally Identifiable Information
- C) Protected Internal Integration
- D) Public Information Index

**Answer: B**

**Explanation:** PII refers to any data that can be used to identify a specific individual, including names, email addresses, phone numbers, Social Security numbers, and other personal details.

---

### Question 2 — Easy
**Which regulation gives EU citizens control over their personal data?**

- A) CCPA
- B) HIPAA
- C) GDPR
- D) SOX

**Answer: C**

**Explanation:** The General Data Protection Regulation (GDPR) is the EU's comprehensive data protection law that grants individuals rights over their personal data, including access, correction, and deletion.

---

### Question 3 — Easy
**What is "data anonymization"?**

- A) Encrypting all data
- B) Removing or modifying data to prevent individual identification
- C) Storing data in multiple locations
- D) Deleting all data

**Answer: B**

**Explanation:** Data anonymization transforms data so that individuals cannot be identified, either by removing direct identifiers or modifying data to prevent re-identification.

---

### Question 4 — Medium
**What is "differential privacy" in AI?**

- A) Different levels of privacy for different users
- B) Adding mathematical noise to data or queries to protect individual privacy
- C) Using different encryption keys
- D) Privacy policies that vary by region

**Answer: B**

**Explanation:** Differential privacy adds carefully calibrated noise to data or query results, providing mathematical guarantees that individual records cannot be identified while preserving aggregate utility.

---

### Question 5 — Medium
**What is the "right to be forgotten" under GDPR?**

- A) The right to forget passwords
- B) The right to have personal data deleted upon request
- C) The right to ignore data policies
- D) The right to access public data

**Answer: B**

**Explanation:** The right to erasure (right to be forgotten) allows individuals to request deletion of their personal data, requiring AI systems to support data removal from training and operational data.

---

### Question 6 — Medium
**Which technique replaces sensitive data with realistic but fake alternatives?**

- A) Encryption
- B) Data pseudonymization
- C) Data compression
- D) Data deduplication

**Answer: B**

**Explanation:** Pseudonymization replaces identifying data with artificial identifiers or fake but realistic alternatives, maintaining data utility while reducing privacy risk.

---

### Question 7 — Medium
**Why is "data minimization" important in AI systems?**

- A) It reduces model size
- B) It limits data collection to what's necessary, reducing privacy risk
- C) It makes training faster
- D) It improves accuracy

**Answer: B**

**Explanation:** Data minimization ensures only necessary data is collected and processed, reducing the attack surface and privacy risk while still enabling the AI system to function effectively.

---

### Question 8 — Medium
**What is "data masking" in the context of AI security?**

- A) Hiding the data from developers
- B) Obscuring sensitive fields while preserving data structure
- C) Encrypting database connections
- D) Logging all data access

**Answer: B**

**Explanation:** Data masking hides sensitive information by replacing it with fictional but realistic data, allowing developers and systems to work with realistic datasets without exposing actual private information.

---

### Question 9 — Hard
**What challenge does "training data memorization" pose for privacy?**

- A) Models forget training data
- B) Models may inadvertently reveal specific training examples in outputs
- C) Training takes too long
- D) Models become too accurate

**Answer: B**

**Explanation:** LLMs can memorize and reproduce specific training examples, potentially leaking private information that was in the training data, requiring techniques to prevent memorization.

---

### Question 10 — Hard
**What is "k-anonymity" in data privacy?**

- A) Using k different encryption keys
- B) Ensuring each record is indistinguishable from at least k-1 other records
- C) Storing data in k different locations
- D) Having k backup copies

**Answer: B**

**Explanation:** k-anonymity ensures that each record in a dataset is indistinguishable from at least k-1 other records on quasi-identifiers, preventing identification of specific individuals.

---

### Question 11 — Hard
**How does "federated learning" help with data privacy?**

- A) It centralizes all data
- B) It trains models across decentralized data without sharing raw data
- C) It encrypts all training data
- D) It deletes data after training

**Answer: B**

**Explanation:** Federated learning allows models to be trained across multiple decentralized data sources without transferring raw data, keeping sensitive information local while still learning from it.

---

### Question 12 — Hard
**What is the "inference attack" risk in AI privacy?**

- A) Attacks on model inference speed
- B) Using model outputs to deduce sensitive training data or attributes
- C) Attacks on the model's architecture
- D) Network-level attacks

**Answer: B**

**Explanation:** Inference attacks use model outputs to deduce information about training data, such as whether specific records were included or what attributes individuals have.

---

### Question 13 — Easy
**What is "encryption at rest"?**

- A) Encrypting data while it's being transmitted
- B) Encrypting data stored in databases or files
- C) Encrypting data in memory only
- D) Not encrypting data at all

**Answer: B**

**Explanation:** Encryption at rest protects data stored on disk or in databases, ensuring that even if storage is compromised, the data remains unreadable without the encryption key.

---

### Question 14 — Medium
**Why should AI systems implement "data retention policies"?**

- A) To keep data forever
- B) To limit how long personal data is stored, reducing privacy risk
- C) To increase data storage costs
- D) To make data retrieval faster

**Answer: B**

**Explanation:** Data retention policies define how long data is kept and when it should be deleted, minimizing the amount of personal data stored and reducing exposure in case of breaches.

---

### Question 15 — Medium
**What is "purpose limitation" in data privacy?**

- A) Limiting the size of data
- B) Restricting data use to its original intended purpose
- C) Limiting who can access data
- D) Limiting data storage locations

**Answer: B**

**Explanation:** Purpose limitation requires that data collected for one purpose cannot be repurposed without additional consent, ensuring data isn't used in ways individuals didn't agree to.

---

### Question 16 — Easy
**Which of these is considered sensitive personal data under GDPR?**

- A) Public business information
- B) Racial or ethnic origin
- C) Published news articles
- D) Government statistics

**Answer: B**

**Explanation:** Under GDPR, special categories of personal data include racial or ethnic origin, political opinions, religious beliefs, health data, and biometric data, requiring enhanced protection.

---

### Question 17 — Hard
**What is "homomorphic encryption" and why is it useful for AI?**

- A) Encryption that works on specific data types
- B) Encryption that allows computation on encrypted data without decrypting it
- C) Encryption using homomorphic keys
- D) A type of symmetric encryption

**Answer: B**

**Explanation:** Homomorphic encryption enables computations on encrypted data, allowing AI models to process sensitive information without ever accessing the raw plaintext, providing strong privacy guarantees.

---

### Question 18 — Medium
**What does a "Data Protection Officer" (DPO) do in an AI organization?**

- A) Writes code for data protection
- B) Oversees data protection strategy and compliance
- C) Manages database performance
- D) Designs AI models

**Answer: B**

**Explanation:** A DPO is responsible for overseeing data protection strategy, ensuring compliance with privacy regulations, and serving as a point of contact for data protection authorities and individuals.

---

## Score Tracking

| Questions Answered | Correct | Incorrect | Score |
|-------------------|---------|-----------|-------|
|                   |         |           |       |

**Scoring Guide:**
- **15-18 correct (83-100%):** Excellent! You have strong data privacy knowledge.
- **12-14 correct (67-82%):** Good foundation, review hard topics.
- **9-11 correct (50-66%):** Needs improvement, study the explanations.
- **Below 9 (<50%):** Review the topic overview and retake.

---

## Answer Key

| Question | Answer | Difficulty |
|----------|--------|------------|
| 1 | B | Easy |
| 2 | C | Easy |
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
