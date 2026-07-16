# Quiz 13: Contemporary fast.ai — The 2026 Ecosystem

## Topic Overview

This quiz covers the fast.ai ecosystem as it exists in 2026: the Answer.AI transition, Solveit platform features, FastHTML, fasttransform, the anti-agentic AI philosophy, Rachel Thomas's education essays, and the contemporary tooling landscape.

---

## Questions

### Question 1

**What happened to fast.ai in November 2024?**

- A) It launched a new deep learning library
- B) It merged with Answer.AI, an R&D lab co-founded by Jeremy Howard and Eric Ries
- C) It was acquired by a large tech company
- D) It shut down its course offerings

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** fast.ai joined Answer.AI, a new AI R&D lab focused on creating practical end-user products. This was not an acquisition but a merger of missions — the blog and community continue, while the core R&D work happens under the Answer.AI umbrella.

</details>

---

### Question 2

**What is the fundamental unit of work in the Solveit platform?**

- A) A chatbot conversation
- B) A pull request
- C) A cell (like a Jupyter notebook)
- D) A dialog — a single document containing markdown, executable code, and AI prompts

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** The "dialog" in Solveit combines planning notes (markdown), executable Python code (with a persistent kernel), and AI conversation turns in a single document. This is literate programming for the AI era — the AI can see everything the human is working on, and the conversation is the workspace.

</details>

---

### Question 3

**What is the purpose of Solveit's "Default Code" toggle?**

- A) It toggles between dark and light mode
- B) It enables automatic code generation
- C) After the AI responds, the editor defaults to accepting user code input rather than AI output, keeping the human in the driver's seat
- D) It sets the default programming language to Python

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The "Default Code" feature is a deliberate design choice: after the AI provides a suggestion, the editor automatically prepares for the human to type code, not accept AI output. This counteracts automation bias and keeps the human actively engaged in the development process.

</details>

---

### Question 4

**What is FastHTML?**

- A) A CSS framework for responsive design
- B) A database query language
- C) A faster version of HTML
- D) A Python web framework that uses HTMX for interactivity, enabling web apps without JavaScript

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** FastHTML is a Python web framework by Answer.AI that lets you build interactive web applications using Python + HTMX. The server returns HTML fragments (not JSON), and HTMX handles dynamic page updates. No JavaScript is required.

</details>

---

### Question 5

**What is special about FastHTML's `/llms-ctx.txt` endpoint?**

- A) It logs all AI interactions for debugging
- B) It displays the server's current context window usage
- C) It returns the framework's license information
- D) It provides a plain-text description of the framework's API and conventions that AI assistants can read to generate idiomatic code

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** FastHTML is designed for AI collaboration from the ground up. The `/llms-ctx.txt` endpoint exposes the framework's API, conventions, and patterns in a format an AI can consume. An AI assistant can fetch this file and immediately learn how to write correct FastHTML code, eliminating the need for extensive context in each prompt.

</details>

---

### Question 6

**What problem does fasttransform solve?**

- A) It converts between different data formats
- B) ML pipelines are traditionally one-way — when errors arise, you cannot easily trace back to see what the model actually processed. fasttransform makes transformations reversible.
- C) It replaces pandas for data analysis
- D) It speeds up PyTorch model training

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Traditional ML pipelines apply transformations (resize, normalize, etc.) and the transformed data is fed to the model. If something goes wrong, you cannot easily see what the model *actually* saw. fasttransform provides a `decode()` method that reverses the transformations, letting you inspect the original data that corresponds to a given model input.

</details>

---

### Question 7

**What is the anti-agentic AI stance advocated by fast.ai in 2026?**

- A) AI should augment human capability, not replace human judgment — the human should remain the active decision-maker
- B) AI development should be regulated by governments
- C) AI should never be used for software development
- D) Only open-source AI models should be used

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** fast.ai's anti-agentic stance is not anti-AI — it is pro-human-agency. The argument is that fully autonomous AI agents erode the skills needed to evaluate their output, create understanding debt, and ultimately make systems less maintainable. The alternative is collaborative AI where the AI suggests and the human decides.

</details>

---

### Question 8

**What does METR research cited by Rachel Thomas show about heavy AI assistance?**

- A) Heavy AI assistance is the most effective way to learn programming
- B) AI assistance has no measurable effect on code quality
- C) It always increases productivity
- D) Developers often *feel* more productive while actually producing harder-to-maintain code — the perception gap

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** METR (Model Evaluation and Threat Research) studies found that developers using heavy AI assistance often report feeling significantly more productive, even when objective measures show they are actually slower and producing less maintainable code. This perception gap is part of what Rachel Thomas calls the "dark flow" phenomenon.

</details>

---

### Question 9

**In her February 2026 essay, what does Rachel Thomas critique about both traditional and AI-powered education?**

- A) Both require too much screen time
- B) Both cost too much money
- C) Both ignore how real learning happens — they focus on metrics (dashboards, scores, progress bars) rather than genuine understanding and community
- D) Both are too focused on STEM subjects

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** In "What analog and AI education both get wrong" (Feb 2026), Thomas argues that both traditional "no screens" education and tech-utopian AI education share a common flaw: they substitute quantitative metrics for genuine understanding. She advocates for community-driven, qualitative learning (as exemplified by Solveit's ShareIt feature) over quantified dashboards.

</details>

---

### Question 10

**What is the "ShareIt" feature in the Solveit ecosystem?**

- A) A code collaboration tool similar to GitHub
- B) A file sharing service
- C) A social media platform for AI developers
- D) A community channel where students share projects and give peer feedback

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** ShareIt is a community channel in the Solveit ecosystem where students share their diverse creative projects and receive peer feedback. It embodies fast.ai's philosophy of qualitative, community-driven assessment over quantitative metrics (scores, completion percentages).

</details>

---

### Question 11

**What is mojokernel?**

- A) A tool for optimizing Mojo code
- B) A database engine
- C) A new operating system for AI workloads
- D) A Jupyter kernel for the Mojo programming language, developed by Answer.AI

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** mojokernel is a custom Jupyter kernel for the Mojo programming language (created by Chris Lattner). Developed by Answer.AI as a community project, it supports variable persistence across cells and function definition preservation — essential features for notebook-driven development.

</details>

---

### Question 12

**According to fast.ai's philosophy, what is the proper role of an AI assistant in software development?**

- A) The AI should only answer questions, never write code
- B) The AI should write all code autonomously while the human reviews
- C) The AI should be a collaborator with specific strengths (speed, knowledge) and acknowledged weaknesses (no true understanding) — the human provides judgment and responsibility
- D) The AI should replace human developers entirely

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** fast.ai advocates for a collaborative model where the AI is a partner with known strengths and weaknesses. The AI suggests approaches, helps implement small steps, and surfaces relevant knowledge. The human provides genuine understanding, value judgment, and ultimate responsibility for what is built. This is the Solveit model: small steps, verified increments, human in control.

</details>

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 7 | A |
| 2 | D | 8 | D |
| 3 | C | 9 | C |
| 4 | D | 10 | D |
| 5 | D | 11 | D |
| 6 | B | 12 | C |

---

*Generated for fast.ai Deep Learning — Module 13 (Contemporary fast.ai: The 2026 Ecosystem). This completes the fast.ai learning track.*
