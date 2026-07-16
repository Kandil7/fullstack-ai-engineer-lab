# AI Security Quiz: Input Validation

## Topic Overview

Input validation for AI systems ensures that user-provided data is safe, properly formatted, and within expected parameters before processing. This quiz covers validation strategies, sanitization techniques, and secure input handling for LLM applications.

### Key Concepts
- Schema validation and type checking
- Input length and format constraints
- Special character handling
- Parameter validation for tool calls
- Secure data preprocessing

---

## Quiz

### Question 1 — Easy
**Why is input validation critical for AI systems?**

- A) It improves model accuracy
- B) It prevents injection attacks and malformed data processing
- C) It reduces training costs
- D) It increases model size

**Answer: B**

**Explanation:** Input validation acts as the first line of defense, preventing malicious or malformed inputs from reaching the model and causing security vulnerabilities or errors.

---

### Question 2 — Easy
**Which of the following is a basic input validation technique?**

- A) Accepting all inputs without checking
- B) Defining allowed input types and formats
- C) Running the model on all inputs immediately
- D) Storing all inputs in a database

**Answer: B**

**Explanation:** Basic validation involves defining expected input types, formats, and ranges, then checking incoming data against these specifications before processing.

---

### Question 3 — Easy
**What is "whitelist-based" validation?**

- A) Blocking all known bad inputs
- B) Only allowing inputs that match approved patterns
- C) Randomly selecting inputs
- D) Accepting all inputs

**Answer: B**

**Explanation:** Whitelist-based validation is more secure than blacklist approaches because it only allows known-good inputs rather than trying to block all possible bad inputs.

---

### Question 4 — Medium
**What is schema validation in the context of LLM tool calls?**

- A) Checking the model's architecture
- B) Verifying tool parameters match expected types and formats
- C) Validating the training data schema
- D) Checking the database schema

**Answer: B**

**Explanation:** Schema validation for tool calls ensures that parameters passed to tools match expected types, required fields are present, and values are within acceptable ranges.

---

### Question 5 — Medium
**Why should input length be limited in LLM applications?**

- A) To improve response quality only
- B) To prevent resource exhaustion and reduce attack surface
- C) To increase token costs
- D) To make the model faster

**Answer: B**

**Explanation:** Length limits prevent denial-of-service attacks, reduce processing costs, and limit the space available for crafting complex injection attempts.

---

### Question 6 — Medium
**Which approach handles Unicode-based input attacks?**

- A) Ignoring all Unicode characters
- B) Normalizing and validating Unicode input against expected ranges
- C) Converting all input to ASCII only
- D) Blocking non-English characters

**Answer: B**

**Explanation:** Unicode normalization and validation ensures characters are properly encoded and within expected ranges, preventing attacks using homoglyphs, zero-width characters, or other Unicode tricks.

---

### Question 7 — Medium
**What is "parameter pollution" in AI tool calls?**

- A) Excessive logging of tool parameters
- B) Sending unexpected or malicious parameters to tools
- C) Using too many tools simultaneously
- D) Storing tool parameters in memory

**Answer: B**

**Explanation:** Parameter pollution occurs when attackers inject unexpected parameters into tool calls, potentially exploiting vulnerabilities in how tools process their inputs.

---

### Question 8 — Medium
**Which validation technique checks for SQL injection in user inputs to LLM tools?**

- A) Token counting
- B) Parameterized queries and input escaping
- C) Increasing context window
- D) Using higher temperature

**Answer: B**

**Explanation:** When LLM tools interact with databases, parameterized queries and proper escaping prevent SQL injection attacks that could be triggered through user inputs.

---

### Question 9 — Hard
**What is "type confusion" in AI security?**

- A) When the model confuses two similar concepts
- B) When inputs are interpreted as different types than intended
- C) When the model generates wrong data types
- D) When the system confuses user roles

**Answer: B**

**Explanation:** Type confusion occurs when inputs crafted to look like one type (e.g., a string) are interpreted as another (e.g., an object), potentially bypassing validation logic.

---

### Question 10 — Hard
**Why is JSON validation important for LLM tool inputs?**

- A) JSON is the only valid format
- B) Malformed JSON can cause parsing errors and injection vulnerabilities
- C) JSON is faster than other formats
- D) All APIs require JSON

**Answer: B**

**Explanation:** Invalid JSON can cause unexpected parsing behavior, potentially allowing injection attacks or causing the system to process data incorrectly, leading to security issues.

---

### Question 11 — Hard
**What challenge does "nested input" validation present?**

- A) It requires less validation
- B) Complex nested structures can hide malicious payloads in deep levels
- C) It always improves performance
- D) It eliminates all security risks

**Answer: B**

**Explanation:** Deeply nested input structures can hide malicious payloads in sub-objects, requiring recursive validation that checks every level of the input hierarchy.

---

### Question 12 — Hard
**Which technique detects adversarial inputs designed to bypass validation?**

- A) Only checking input length
- B) Behavioral analysis combined with pattern matching
- C) Using fixed validation rules only
- D) Accepting all inputs

**Answer: B**

**Explanation:** Adversarial inputs may pass simple validation checks. Behavioral analysis and pattern matching detect inputs that technically pass validation but exhibit suspicious characteristics.

---

### Question 13 — Easy
**What is "input encoding" validation?**

- A) Checking if input is properly encoded for the expected format
- B) Encrypting all inputs
- C) Encoding model outputs
- D) Compressing input data

**Answer: A**

**Explanation:** Input encoding validation ensures that data is properly formatted (UTF-8, base64, etc.) and doesn't contain encoding-based attacks like double encoding or null bytes.

---

### Question 14 — Medium
**Why should file upload inputs be strictly validated?**

- A) Files are always safe
- B) Files can contain malicious code, oversized content, or unexpected formats
- C) File validation slows down the system
- D) All file types are safe for AI processing

**Answer: B**

**Explanation:** File uploads can contain malware, oversized content causing resource exhaustion, or malformed files that exploit parsing vulnerabilities in the system.

---

### Question 15 — Medium
**What is the principle of "fail-safe defaults" in input validation?**

- A) Accept input when validation fails
- B) Reject input when validation encounters errors
- C) Log but allow invalid inputs
- D) Retry validation indefinitely

**Answer: B**

**Explanation:** Fail-safe defaults mean that when validation encounters ambiguity or errors, the system rejects the input rather than allowing potentially dangerous data through.

---

### Question 16 — Easy
**Which of these is NOT a valid input validation technique?**

- A) Type checking
- B) Length limits
- C) Accepting all inputs without verification
- D) Format validation

**Answer: C**

**Explanation:** Accepting inputs without verification is the opposite of validation and leaves the system vulnerable to attacks and errors from malformed data.

---

### Question 17 — Hard
**How does "fuzz testing" help validate AI inputs?**

- A) It generates random inputs to find validation gaps
- B) It only tests valid inputs
- C) It validates the model's training data
- D) It tests network security only

**Answer: A**

**Explanation:** Fuzz testing generates large volumes of random, malformed, or unexpected inputs to identify edge cases and vulnerabilities in input validation logic that normal testing might miss.

---

### Question 18 — Medium
**What is the risk of inadequate input validation for AI tool parameters?**

- A) Slower model performance
- B) Tool misuse, data leakage, or system compromise
- C) Better user experience
- D) Lower computational costs

**Answer: B**

**Explanation:** Without proper validation, tool parameters can be exploited to access unauthorized data, execute unintended actions, or compromise the entire system.

---

## Score Tracking

| Questions Answered | Correct | Incorrect | Score |
|-------------------|---------|-----------|-------|
|                   |         |           |       |

**Scoring Guide:**
- **15-18 correct (83-100%):** Excellent! You have strong input validation knowledge.
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
| 13 | A | Easy |
| 14 | B | Medium |
| 15 | B | Medium |
| 16 | C | Easy |
| 17 | A | Hard |
| 18 | B | Medium |
