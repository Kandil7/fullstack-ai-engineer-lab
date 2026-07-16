# Glossary: Contemporary fast.ai — The 2026 Ecosystem

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Answer.AI | AI R&D lab co-founded by Jeremy Howard and Eric Ries; created Solveit, FastHTML, fasttransform | fast.ai merged here in 2024 |
| Solveit | Platform for Dialog Engineering: unified dialogs, Monaco editor, symbol browser, hosting | The flagship Answer.AI product |
| Dialog | Solveit's unit of work: markdown + executable code + AI prompts in one document | Literate programming for the AI era |
| Default Code | Solveit feature that defaults to code input after AI responses | Keeps the human in the driver's seat |
| Symbol Browser | Live tracking of variables and functions as code executes | Debugging aid for notebook-style workflows |
| ShareIt | Community channel for sharing Solveit projects with peer feedback | Qualitative over quantitative assessment |
| FastHTML | Python web framework using HTMX for interactivity — no JavaScript needed | Full-stack web apps in one language |
| HTMX | Library that adds dynamic behaviour via HTML attributes; server returns HTML fragments | Replaces JavaScript for most interactivity |
| LLMs-ctx.txt | Endpoint that tells AI assistants how to write code for a framework | Framework designed for AI collaboration |
| fasttransform | Library for reversible data transformation pipelines using multiple dispatch | Debug pipelines by decoding back to original |
| Multiple Dispatch | Dispatch a function based on the types of ALL arguments (not just the first) | Enables pipelines to handle different data types |
| mojokernel | Jupyter kernel for the Mojo programming language by Answer.AI | Run Mojo code in notebooks |
| Mojo | Python-syntax language with C-level performance (Chris Lattner) | Combines Python ease with systems speed |
| Anti-agentic AI | Philosophy that AI should augment human capability, not replace judgment | The core of fast.ai's 2026 stance |
| METR | Model Evaluation and Threat Research — studies showing perceived productivity outpaces actual | Evidence for anti-agentic stance |
| Understanding Debt | Gap between what code does and what you understand (revisited for agentic AI) | Grows faster with autonomous AI |
| Collaborative AI | AI as a partner with specific strengths (speed, knowledge) and weaknesses (no true understanding) | The Solveit interaction model |
| Learning Dashboard | Quantified metrics for education (progress bars, scores) — critiqued by Rachel Thomas | Map replacing the territory |
| Monaco Editor | VS Code's editor engine, used in Solveit for code editing | Professional-grade editing in the browser |

---

## Detailed Definitions

### Answer.AI

**Definition:** An AI R&D lab co-founded by Jeremy Howard (fast.ai) and Eric Ries (The Lean Startup). Its mission is to create practical end-user products based on foundational research, with a strong emphasis on human agency and transparent AI collaboration. Products include Solveit, FastHTML, fasttransform, and mojokernel.

**Related Terms:** Solveit, FastHTML, fasttransform

- Founded 2023; fast.ai joined in November 2024.
- Focuses on tools, not just models or courses.
- Open-source: most projects on [github.com/AnswerDotAI](https://github.com/AnswerDotAI).

---

### Solveit

**Definition:** A web-based platform and methodology for Dialog Engineering. Combines markdown notes, executable Python code, and AI prompts into unified "dialogs" with a persistent Linux environment. Features include editable conversation history, granular context control, Monaco code editor, symbol browser, and community sharing.

**Related Terms:** Dialog, Default Code, ShareIt

- Available at solve.it.com.
- Powers the "How to Solve It With Code" course.
- Designed to counter "vibe coding" and keep humans engaged.

---

### Dialog (Solveit)

**Definition:** The fundamental unit of work in Solveit. A single document containing markdown (notes/planning), executable Python code blocks, and AI conversation turns. The AI can see everything in the dialog, enabling rich, context-aware collaboration.

**Related Terms:** Solveit, Default Code, ShareIt

- Literate programming for the AI era.
- Code, commentary, and AI collaboration coexist.
- Editable and pruneable — unlike standard chat logs.

---

### Default Code

**Definition:** A Solveit design feature that automatically sets the editor to accept user code input immediately after an AI response, rather than defaulting to accepting the AI's output. This keeps the human actively engaged and thinking, counteracting automation bias.

**Related Terms:** Solveit, anti-agentic AI, automation bias

- A physical manifestation of the human-first philosophy.
- You must actively choose to accept AI output.
- Prevents the passive "vibe coding" pattern.

---

### FastHTML

**Definition:** A Python web framework by Answer.AI that enables building interactive web applications using Python and HTMX, with zero JavaScript required. Includes an `/llms-ctx.txt` endpoint for AI assistants to learn the framework.

**Related Terms:** HTMX, LLMs-ctx.txt

- Full-stack from one Python codebase.
- Routes, rendering, and interactivity all in Python.
- Designed alongside AI tools, not retrofitted for them.

---

### HTMX

**Definition:** A JavaScript library (used by FastHTML) that allows you to declare dynamic web page behaviour directly in HTML attributes. Instead of returning JSON and writing client-side JS, the server returns HTML fragments that HTMX swaps into the page.

**Related Terms:** FastHTML

- `hx_get`, `hx_post`, `hx_swap` replace event listeners and fetch calls.
- Dramatically reduces client-side complexity.
- Not a replacement for all JS, but covers most interactivity.

---

### LLMs-ctx.txt

**Definition:** A convention (pioneered by FastHTML) where a web framework exposes a `/llms-ctx.txt` endpoint containing a plain-text description of the framework's API, conventions, and patterns. AI assistants can read this file to generate idiomatic code for the framework.

**Related Terms:** FastHTML

- An AI assistant can fetch and learn the framework in real time.
- Makes the framework discoverable and usable by AI tools.
- Could become a standard convention for AI-friendly frameworks.

---

### fasttransform

**Definition:** A Python library (from fastcore/fastai, extracted and released by Answer.AI) that treats data transformations as reversible objects with `encode()` and `decode()` methods. Uses multiple dispatch to handle different data types (images, masks, text) through the same pipeline.

**Related Terms:** Pipeline, multiple dispatch

- `decode()` reconstructs the original data from transformed data.
- `decode_at(step)` shows intermediate states.
- Essential for debugging ML pipelines where errors are hard to trace.

---

### Multiple Dispatch

**Definition:** A programming language feature where a function is dispatched based on the types of ALL its arguments (not just the first, as in single dispatch). Used by fasttransform to define different transformation logic for different data types.

**Related Terms:** fasttransform

- Example: `encode(img: PIL.Image)` and `encode(mask: torch.Tensor)` in the same pipeline.
- Implemented in Python via the `plum` library.
- Makes pipelines extensible to new data types without modification.

---

### Anti-agentic AI

**Definition:** The philosophical stance, central to fast.ai's 2026 ecosystem, that AI should augment human capability rather than replace human judgment. Argues against fully autonomous "AI agents" that write code, make decisions, and execute actions without human oversight.

**Related Terms:** collaborative AI, understanding debt, METR

- Not anti-AI — pro-human-agency.
- Solveit is the practical implementation of this philosophy.
- Supported by METR research on productivity perception gaps.

---

### Collaborative AI

**Definition:** The alternative model to agentic AI, advocated by fast.ai. The AI is a collaborator with specific strengths (speed, knowledge breadth, pattern matching) and acknowledged weaknesses (no true understanding, hallucination, limited context). The human provides understanding, judgment, and responsibility.

**Related Terms:** anti-agentic AI, Solveit, Dialog Engineering

- AI suggests, human decides.
- Tasks are broken into small, verifiable steps.
- The human reads and understands every line before accepting it.

---

### METR (Model Evaluation and Threat Research)

**Definition:** An organization that studies the capabilities and risks of advanced AI models. Their research, cited by Rachel Thomas in "Breaking the Spell of Vibe Coding," found that developers using heavy AI assistance often feel more productive while actually producing harder-to-maintain code.

**Related Terms:** anti-agentic AI, understanding debt, vibe coding

- Key finding: perception of productivity > actual productivity.
- Used by fast.ai as empirical support for the anti-agentic stance.
- Available at [metr.org](https://metr.org).

---

### Mojo

**Definition:** A programming language created by Chris Lattner (LLVM, Swift, C++). Combines Python-like syntax with C/rust-level performance through MLIR (Multi-Level Intermediate Representation). Jeremy Howard is an active collaborator.

**Related Terms:** mojokernel, Answer.AI

- Designed to be a superset of Python.
- Can call Python code directly (interoperability).
- Performance-critical AI code is a primary use case.

---

### mojokernel

**Definition:** A custom Jupyter kernel for the Mojo programming language, developed by Answer.AI. Supports variable persistence across cells and function definition preservation — features essential for notebook-driven development.

**Related Terms:** Mojo, Answer.AI

- Community project until an official kernel is released.
- Uses undocumented Mojo internals for performance.
- Available on [github.com/AnswerDotAI](https://github.com/AnswerDotAI).

---

## Summary

1. **Answer.AI** is the successor organization to fast.ai's R&D efforts, building tools that embody human-centered AI principles.
2. **Solveit** is the flagship product — a platform for Dialog Engineering with editable context, persistent environments, and a deliberate "human-first" design.
3. **FastHTML + HTMX** enables full-stack Python web apps without JavaScript; its `/llms-ctx.txt` is a paradigm shift for AI-friendly framework design.
4. **fasttransform** brings reversibility to ML pipelines via multiple dispatch — decode transformed data to debug what your model actually sees.
5. The **anti-agentic AI stance** distinguishes fast.ai from much of the industry: AI should augment, not replace, human capability.
6. **Rachel Thomas's 2026 essays** challenge both traditional and AI education, advocating qualitative, community-driven learning.
7. Tools like **mojokernel** and collaborations like **Mojo** extend the ecosystem beyond Python into high-performance computing.
