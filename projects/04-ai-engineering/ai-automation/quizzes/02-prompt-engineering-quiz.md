# Quiz 02: Prompt Engineering

## Topic Overview
This quiz covers the art and science of crafting effective prompts for LLMs. Topics include prompt design principles, few-shot learning, chain-of-thought prompting, prompt templates, optimization techniques, and advanced prompting strategies.

---

## Questions

### Question 1
**What is "zero-shot prompting" in LLM interactions?**

- A) Using no prompt at all
- B) Providing task instructions without examples
- C) Using only one example in the prompt
- D) Running the model with zero tokens

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Zero-shot prompting means giving the model a task description without providing any examples of input-output pairs. The model must understand and execute the task based solely on the instructions. This is the simplest prompting approach and works well for straightforward tasks where the model has sufficient training data.
</details>

---

### Question 2
**What is the "chain-of-thought" (CoT) prompting technique?**

- A) Breaking the prompt into multiple API calls
- B) Asking the model to show its reasoning step-by-step
- C) Chaining multiple models together
- D) Using multiple system prompts in sequence

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Chain-of-thought prompting instructs the model to explain its reasoning process step-by-step before providing a final answer. This technique significantly improves performance on complex reasoning tasks like math problems, logic puzzles, and multi-step analysis. The model generates intermediate reasoning that leads to more accurate conclusions.
</details>

---

### Question 3
**In "few-shot prompting," what does "few-shot" refer to?**

- A) Using a small model
- B) Providing a few examples of the desired input-output behavior
- C) Limiting the output to a few tokens
- D) Making a few API calls

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Few-shot prompting provides the model with a small number of examples (typically 2-5) demonstrating the desired input-output pattern. The model learns the task from these examples and applies the pattern to new inputs. This approach improves consistency and accuracy compared to zero-shot prompting for complex tasks.
</details>

---

### Question 4
**What is "prompt injection" and why is it a security concern?**

- A) Injecting API keys into prompts
- B) Malicious input that overrides system instructions
- C) Adding excessive text to prompts
- D) Using prompts in production applications

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Prompt injection is an attack where malicious user input is crafted to override or bypass the system prompt instructions. For example, users might try to make the AI ignore its safety guidelines or reveal confidential information. This is a critical security concern that requires defensive prompt design and input validation.
</details>

---

### Question 5
**Which of the following is a "system prompt" best practice?**

- A) Keep it as short as possible
- B) Be specific, clear, and include constraints
- C) Include all possible instructions for edge cases
- D) Avoid using any formatting

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Effective system prompts should be specific, clear, and well-structured. They should define the model's role, behavior, constraints, and output format. While brevity is important, clarity and completeness matter more. Structured formatting with clear sections helps the model follow instructions reliably.
</details>

---

### Question 6
**What is "temperature" used for in prompt engineering?**

- A) To set the API endpoint
- B) To control output randomness
- C) To define token limits
- D) To set the model version

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Temperature controls the randomness of the model's output. Lower temperatures (0.0-0.3) produce more focused, deterministic responses, while higher temperatures (0.7-1.5) increase creativity and variability. For factual tasks, use low temperature; for creative tasks, use higher values.
</details>

---

### Question 7
**What is "prompt optimization"?**

- A) Reducing the number of API calls
- B) Systematically improving prompts to get better results
- C) Making prompts shorter
- D) Using fewer tokens in prompts

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Prompt optimization is the iterative process of testing and refining prompts to improve performance metrics like accuracy, consistency, and efficiency. It involves A/B testing different prompt versions, analyzing failures, and systematically improving instructions. This is essential for production applications where prompt quality directly impacts results.
</details>

---

### Question 8
**What is the "persona" pattern in prompt engineering?**

- A) Asking the model to act as a specific character or expert
- B) Using the user's personal information in prompts
- C) Creating multiple personas for A/B testing
- D) Assigning API access to different users

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** The persona pattern assigns a specific role or expertise to the model, such as "You are an expert Python developer" or "Act as a medical professional." This helps the model generate more relevant, accurate, and contextually appropriate responses by framing the task within a specific domain of knowledge.
</details>

---

### Question 9
**What is "structured output" in prompt engineering?**

- A) Organizing prompts in a table format
- B) Requesting the model to return data in a specific format (JSON, XML, etc.)
- C) Using structured prompts with clear sections
- D) Storing prompts in a database

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Structured output prompting requests the model to generate responses in a specific format like JSON, XML, or YAML. This makes the output machine-parseable and easier to integrate into applications. Many LLM providers now support native structured output modes that enforce valid JSON or other formats.
</details>

---

### Question 10
**Why is "prompt versioning" important in production?**

- A) To keep track of model versions
- B) To ensure reproducibility and track improvements over time
- C) To support multiple languages
- D) To reduce API costs

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Prompt versioning tracks changes to prompts over time, enabling reproducibility, rollback capability, and performance comparison. In production, even small prompt changes can significantly affect output quality. Version control allows teams to iterate safely and understand what changes improved or degraded performance.
</details>

---

### Question 11
**What is "few-shot chain-of-thought" prompting?**

- A) Using only one example with chain-of-thought
- B) Providing examples that demonstrate step-by-step reasoning
- C) Chaining multiple few-shot examples together
- D) Using chain-of-thought without any examples

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Few-shot chain-of-thought combines both techniques by providing examples that include explicit reasoning steps. Each example shows not just the input-output pair, but also the intermediate reasoning process. This is particularly effective for complex reasoning tasks as it teaches the model both the task pattern and the reasoning approach.
</details>

---

### Question 12
**What is the "self-consistency" technique in prompt engineering?**

- A) Checking if the prompt is internally consistent
- B) Generating multiple responses and selecting the most common answer
- C) Ensuring the same prompt works across different models
- D) Validating that the output matches the input format

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Self-consistency generates multiple responses at a higher temperature and selects the answer that appears most frequently. This leverages the fact that correct answers are more likely to be consistently generated across multiple samples. It's particularly effective for math and logic problems where there's a clear correct answer.
</details>

---

### Question 13
**What is "prompt chaining" in LLM applications?**

- A) Using the same prompt repeatedly
- B) Breaking complex tasks into sequential prompts where each builds on the previous output
- C) Connecting multiple API endpoints
- D) Creating a chain of API keys

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Prompt chaining breaks complex tasks into smaller, manageable steps. Each step uses a separate prompt, and the output of one step becomes the input for the next. This approach improves accuracy for complex workflows and makes debugging easier since you can inspect intermediate results.
</details>

---

### Question 14
**What is the primary benefit of "delimiter-based prompting"?**

- A) It reduces token count
- B) It clearly separates different sections of the prompt
- C) It makes prompts easier to translate
- D) It automatically formats the output

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Delimiter-based prompting uses special characters or tokens (like triple backticks, XML tags, or markdown headers) to clearly separate different sections of the prompt. This helps the model distinguish between instructions, input data, examples, and constraints, reducing ambiguity and improving instruction following.
</details>

---

### Question 15
**What is "prompt meta-prompting"?**

- A) Writing prompts about prompt engineering
- B) Using the LLM to generate or optimize prompts
- C) Creating prompts for meta-learning models
- D) Storing prompts in a meta-database

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Meta-prompting uses the LLM itself to generate, evaluate, or optimize prompts. For example, you can ask the model to analyze a task and suggest the optimal prompt structure, or to critique and improve an existing prompt. This creates a feedback loop where the model helps improve its own instruction following.
</details>

---

### Question 16
**Which technique is most effective for reducing hallucinations?**

- A) Increasing the temperature
- B) Using system prompts to constrain outputs and provide factual context
- C) Making prompts shorter
- D) Using multiple API calls

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Reducing hallucinations requires constraining the model's outputs and providing factual context. Effective techniques include: grounding prompts with retrieved documents (RAG), instructing the model to only use provided information, using low temperature for factual tasks, and asking the model to cite sources. System prompts that enforce factual grounding are essential.
</details>

---

### Question 17
**What is "prompt testing" and why is it essential?**

- A) Testing the API endpoint connection
- B) Systematically evaluating prompt performance across diverse inputs
- C) Testing the model's speed
- D) Checking token counts

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Prompt testing involves evaluating prompts against a diverse set of inputs to ensure consistent, accurate results. It includes edge cases, adversarial inputs, and representative examples. Without systematic testing, prompts may work well in development but fail in production with unexpected inputs.
</details>

---

### Question 18
**What is the "tree-of-thought" prompting technique?**

- A) Creating a decision tree of prompts
- B) Exploring multiple reasoning paths and evaluating each
- C) Using a hierarchical prompt structure
- D) Generating tree-structured data outputs

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Tree-of-thought (ToT) prompting explores multiple reasoning branches simultaneously, evaluates each path, and selects the most promising one. Unlike chain-of-thought which follows a single path, ToT considers alternatives and can backtrack when a reasoning path leads to an error. This is particularly effective for complex planning and problem-solving tasks.
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
| 7 | Medium | | |
| 8 | Medium | | |
| 9 | Medium | | |
| 10 | Medium | | |
| 11 | Hard | | |
| 12 | Hard | | |
| 13 | Medium | | |
| 14 | Easy | | |
| 15 | Hard | | |
| 16 | Medium | | |
| 17 | Easy | | |
| 18 | Hard | | |

**Score:** ____/18

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 7 | B | 13 | B |
| 2 | B | 8 | A | 14 | B |
| 3 | B | 9 | B | 15 | B |
| 4 | B | 10 | B | 16 | B |
| 5 | B | 11 | B | 17 | B |
| 6 | B | 12 | B | 18 | B |

---

*Generated for AI Automation Lab - Quiz 02 of 09*