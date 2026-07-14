# Quiz 02: Tool Calling

> **Topic Overview**: Tool calling is the mechanism that enables AI agents to interact with the external world. This quiz covers tool definition formats, function calling APIs, parameter schemas, tool execution patterns, error handling, and strategies for selecting and orchestrating multiple tools. Mastering tool calling is essential for building agents that can take meaningful actions.

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

**What is the primary purpose of tool calling in AI agents?**

- A) To improve the agent's text generation quality
- B) To enable the agent to interact with external systems and APIs
- C) To reduce the agent's memory usage
- D) To speed up the agent's training process

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tool calling enables agents to go beyond text generation by allowing them to interact with external systems—databases, APIs, file systems, web services, and more. It's the bridge between the agent's reasoning and real-world actions.

</details>

---

### Question 2 — Easy

**In OpenAI's function calling format, what describes the expected input parameters of a tool?**

- A) The tool's name
- B) A JSON Schema describing the parameters
- C) The tool's return type
- D) A natural language description only

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: OpenAI's function calling uses JSON Schema to describe each parameter's type, required/optional status, and constraints. This structured schema helps the LLM generate correctly formatted arguments for the tool.

</details>

---

### Question 3 — Easy

**Which of the following is a best practice when writing tool descriptions?**

- A) Keep descriptions as short as possible—just the tool name
- B) Provide clear, detailed descriptions including when to use and when NOT to use the tool
- C) Use technical jargon that only developers understand
- D) Omit descriptions to save token budget

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Clear, detailed tool descriptions are critical because the LLM uses them to decide when and how to invoke tools. Including both when to use AND when not to use a tool helps the agent avoid incorrect or unnecessary tool calls.

</details>

---

### Question 4 — Easy

**What happens when an LLM decides a tool should be called?**

- A) The tool executes immediately without any validation
- B) The LLM generates a tool call with arguments, which the application code validates and executes
- C) The user must manually approve every tool call
- D) The tool is called asynchronously in the background

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: When an LLM decides to call a tool, it generates a structured tool call (function name + arguments). The application code then validates the arguments, executes the tool, and returns the result to the LLM. The LLM never directly executes tools—it proposes them.

</details>

---

### Question 5 — Medium

**What is "tool use" in the Anthropic Claude API called?**

- A) Plugin system
- B) Tool use / function calling
- C) Webhook integration
- D) Event subscription

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Anthropic's Claude API uses "tool use" (also called function calling) where tools are defined with JSON schemas, and Claude generates structured tool calls that the application intercepts and executes.

</details>

---

### Question 6 — Medium

**Which of the following is a key consideration when designing tool parameters?**

- A) Make all parameters required to avoid ambiguity
- B) Use descriptive parameter names and provide descriptions for each parameter
- C) Use single-letter parameter names to save tokens
- D) Avoid using enum types for parameter constraints

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Descriptive parameter names with clear descriptions help the LLM understand what values to pass. Enums are useful for constraining choices. Not all parameters should be required—optional parameters with defaults give the LLM flexibility.

</details>

---

### Question 7 — Medium

**What is "parallel tool calling"?**

- A) Running the same tool multiple times simultaneously
- B) The LLM generating multiple independent tool calls in a single response
- C) Using multiple tools sequentially in a fixed order
- D) Having multiple agents call the same tool

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Parallel tool calling allows the LLM to generate multiple independent tool calls in a single response. The application executes them concurrently (if independent) and returns all results together, improving efficiency and reducing round trips.

</details>

---

### Question 8 — Medium

**What is the recommended approach when a tool call fails?**

- A) Retry the exact same call indefinitely
- B) Return the error to the LLM and let it reason about how to handle or retry
- C) Crash the entire agent
- D) Silently ignore the error

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Returning errors to the LLM allows it to understand what went wrong and decide on an appropriate response—whether retrying with different parameters, trying an alternative tool, or informing the user. This is more robust than blind retries.

</details>

---

### Question 9 — Medium

**What is a "tool registry"?**

- A) A database of all tools the agent has access to
- B) A structured collection of tool definitions that can be dynamically loaded and managed
- C) A log file recording all tool executions
- D) A security policy for tool access control

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A tool registry is a structured collection of tool definitions that manages available tools. It enables dynamic loading of tools based on context, access control, version management, and organized tool discovery for the LLM.

</details>

---

### Question 10 — Medium

**Which of the following is a disadvantage of giving an agent too many tools?**

- A) The agent will always choose the wrong tool
- B) The LLM may struggle to select the right tool and may make incorrect tool calls
- C) More tools always lead to better performance
- D) The agent will run out of memory

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Too many tools can overwhelm the LLM's decision-making. The model may confuse similar tools, select the wrong one, or hallucinate tool calls. A curated, well-documented set of tools typically outperforms an exhaustive but unmanageable collection.

</details>

---

### Question 11 — Hard

**What is "tool chaining" and why is it useful?**

- A) Linking tool calls together where the output of one tool becomes the input of the next
- B) Creating a physical chain of servers to execute tools
- C) Running all tools simultaneously in parallel
- D) A security mechanism to prevent tool misuse

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Tool chaining is when the agent structures a sequence of tool calls where each tool's output feeds into the next tool's input. For example: search the web → extract content → summarize → store result. This enables complex multi-step workflows.

</details>

---

### Question 12 — Hard

**What is "tool augmentation" in the context of LLMs?**

- A) Adding more tools to the agent
- B) Training the LLM specifically to be better at selecting and using tools
- C) Augmenting tool outputs with additional metadata
- D) Creating synthetic tool call examples for testing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tool augmentation (or tool-augmented training) involves fine-tuning or training LLMs specifically to improve their ability to select appropriate tools, generate correct parameters, and interpret tool results. This goes beyond just providing tool descriptions.

</details>

---

### Question 13 — Hard

**What is the "sandbox" pattern for tool execution?**

- A) Running tools in a physically isolated environment
- B) Executing tools in a restricted, isolated environment with limited permissions to prevent harm
- C) Running tools only on weekends
- D) A tool for building sandcastle simulations

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The sandbox pattern executes tools in a restricted environment with limited permissions—preventing unauthorized file access, network calls, or system modifications. This is critical for security when agents can execute arbitrary code or make external API calls.

</details>

---

### Question 14 — Hard

**In MCP (Model Context Protocol), what is a "tool resource"?**

- A) A file stored on disk
- B) A capability exposed by an MCP server that an LLM can invoke
- C) A memory allocation for tool execution
- D) A type of database connection

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: In MCP, tool resources are capabilities that MCP servers expose to LLMs. They include tools (callable functions), resources (readable data), and prompts (reusable templates). This standardized protocol enables LLMs to interact with external systems consistently.

</details>

---

### Question 15 — Hard

**What is the "argument hallucination" problem in tool calling?**

- A) The tool's output is incorrect
- B) The LLM generates plausible-looking but incorrect or fabricated parameter values
- C) The tool's name is misspelled
- D) The tool call is never sent to the server

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Argument hallucination occurs when the LLM generates tool call arguments that look valid but contain fabricated values—like inventing an email address, making up a UUID, or providing a date that doesn't exist. This requires validation and guardrails.

</details>

---

### Question 16 — Easy

**What is the difference between a "tool" and a "plugin"?**

- A) They are the same thing with different names
- B) A tool is typically a single function; a plugin is a collection of related tools and capabilities
- C) Plugins are always open source; tools are always proprietary
- D) Tools run locally; plugins always run remotely

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A tool is usually a single callable function with specific inputs and outputs. A plugin is a more comprehensive package that bundles multiple related tools, resources, and configurations together. Think of a tool as a function and a plugin as a library.

</details>

---

### Question 17 — Easy

**Why should tool descriptions include examples?**

- A) Examples increase the token budget unnecessarily
- B) Examples help the LLM understand the expected format and usage patterns
- C) Examples are only for documentation purposes
- D) Examples slow down tool execution

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Examples in tool descriptions give the LLM concrete instances of how to use the tool, including expected input formats, common use cases, and edge cases. This significantly improves the accuracy and reliability of tool calls.

</details>

---

### Question 18 — Medium

**What is "tool output parsing" and why is it important?**

- A) The process of formatting tool outputs for the user
- B) The process of extracting and structuring the tool's response so the LLM can effectively use the information
- C) Parsing the tool's source code
- D) Converting tool outputs to images

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tool output parsing extracts and structures the tool's response into a format the LLM can efficiently process. Raw API responses may be verbose or poorly structured—parsing ensures the LLM receives relevant, well-organized information without unnecessary noise.

</details>

---

### Question 19 — Hard

**What is "tool selection filtering" and when is it useful?**

- A) Removing tools from the agent permanently
- B) Dynamically limiting which tools are available to the LLM based on the current context or task
- C) Filtering out invalid tool call arguments
- D) Selecting which tools to test during QA

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tool selection filtering dynamically limits available tools based on context. For example, a coding agent might only expose file-editing tools when working on code, or a research agent might only show search tools. This reduces decision complexity and improves accuracy.

</details>

---

### Question 20 — Easy

**What is the standard format for defining tool parameters in OpenAI's API?**

- A) YAML
- B) JSON Schema
- C) XML
- D) Protocol Buffers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: OpenAI's API uses JSON Schema to define tool parameters, including property types, descriptions, required fields, and constraints like enums or minimum/maximum values. This standardized format is also used by Anthropic and other LLM providers.

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
| 11 | A | Hard |
| 12 | B | Hard |
| 13 | B | Hard |
| 14 | B | Hard |
| 15 | B | Hard |
| 16 | B | Easy |
| 17 | B | Easy |
| 18 | B | Medium |
| 19 | B | Hard |
| 20 | B | Easy |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 18-20 | Expert | Excellent tool calling mastery |
| 14-17 | Proficient | Strong understanding; review advanced patterns |
| 10-13 | Developing | Good foundation; practice tool design |
| 6-9 | Beginner | Review tool calling fundamentals |
| 0-5 | Novice | Start with basic tool calling concepts |

---

**Previous Quiz**: [01 - Agent Fundamentals](01-agent-fundamentals-quiz.md) | **Next Quiz**: [03 - Agent Memory](03-agent-memory-quiz.md)
