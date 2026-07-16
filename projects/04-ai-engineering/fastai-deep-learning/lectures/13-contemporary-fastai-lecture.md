# Lecture 13: Contemporary fast.ai — The 2026 Ecosystem

## Topic Overview

By 2026, fast.ai has transformed from a deep-learning course provider into a broader movement. The organization merged with **Answer.AI** (an R&D lab co-founded by Jeremy Howard and Eric Ries), launched the **Solveit** platform and methodology, and shifted its focus from teaching you to *use* AI to teaching you to *collaborate* with AI while maintaining human agency and understanding.

This lecture surveys the fast.ai ecosystem as it stands in 2026: the Solveit platform's production features, Answer.AI's new tools (FastHTML, fasttransform, mojokernel), the latest blog posts from Rachel Thomas on education and AI, and the overarching philosophy of **human-centered AI development** that ties it all together. Unlike previous modules that mirror specific courses, this one is a living document of the contemporary landscape.

**Duration:** 2–3 hours  
**Difficulty:** All levels  
**Prerequisites:** Module 10 (Solveit / Dialog Engineering) recommended but not required

---

## Learning Objectives

By the end of this lecture you will be able to:

1. **Describe** the fast.ai → Answer.AI transition and how it has reshaped the organization's offerings.
2. **Navigate** the Solveit platform's 2026 feature set: unified dialogs, Monaco editor, symbol browser, hosting, and sharing.
3. **Explain** what FastHTML is and how it uses Python + HTMX to build web apps without JavaScript.
4. **Use** fasttransform's reversible pipeline concept to debug data transformations.
5. **Discuss** the "anti-agentic AI" philosophy and why fast.ai argues for human agency over automation.
6. **Summarize** Rachel Thomas's 2026 critique of AI in education and her alternative vision.
7. **Connect** the Solveit methodology to the earlier Dialog Engineering lecture (Module 10) and see how the ideas evolved.
8. **Evaluate** the fast.ai ecosystem for your own development practice: which tools fit your workflow?

---

## Key Concepts

### 1. The fast.ai → Answer.AI Transition

In November 2024, Jeremy Howard announced that fast.ai was joining **Answer.AI** — a new kind of R&D lab focused on creating practical end-user products based on foundational research. This was not an acquisition or a pivot; it was a *merger of missions.*

```text
Before 2024:                    After 2024:
┌─────────────────────┐        ┌─────────────────────┐
│ fast.ai             │        │ Answer.AI           │
│  - Courses          │        │  - Solveit platform │
│  - fastai library   │  ──▶   │  - FastHTML         │
│  - nbdev            │        │  - Research          │
│  - Blog             │        │  - fasttransform     │
│  - Research         │        │  - mojokernel       │
└─────────────────────┘        │  - fastai (maintained)│
                               │  - Blog (continues)  │
                               └─────────────────────┘
```

The key insight: fast.ai's mission was always to democratize AI understanding. Answer.AI extends that by building tools that embody the same philosophy — transparency, human agency, and deep understanding over black-box automation.

### 2. Solveit Platform (2026 Edition)

The Solveit platform, introduced in Module 10, has matured significantly. By 2026 it is the central product of Answer.AI, used not just for coding courses but for system administration, legal drafting, business strategy, and research.

#### Unified Workspace ("Dialogs")

The core unit of Solveit is the **dialog** — a single document that combines:
- **Markdown notes** for planning and reflection
- **Executable Python code** with a persistent kernel
- **AI prompts and responses** as an integral part of the document

This is literate programming for the AI era: the code, the commentary, and the AI collaboration all live in one place. You can interleave a paragraph explaining your approach, a code block that implements it, and an AI prompt asking for help debugging — and the AI can see all of it.

```text
┌─────────────────────────────────────────┐
│  Solveit Dialog                          │
├─────────────────────────────────────────┤
│  ## Goal: Parse CSV files                │
│  # I need to handle edge cases...       │
│                                          │
│  ```python                               │
│  def parse_row(row: str) -> dict:        │
│      ...                                 │
│  ```                                     │
│                                          │
│  @AI: What am I missing here?           │
│  AI: You should handle quoted fields...  │
│                                          │
│  ## Revised implementation              │
│  ...                                     │
└─────────────────────────────────────────┘
```

#### Key Features Added Since Launch

| Feature | Description |
|---------|-------------|
| **Monaco Editor** | VS Code's editor engine powers the code editing experience |
| **Symbol Browser** | Live tracking of variables and functions as code executes |
| **Default Code Toggle** | Automatically prepares the editor for user code after AI responses |
| **Granular Context Control** | Pin, hide, or collapse messages to manage the AI's context window |
| **Persistent Environments** | Secure Linux instances that persist across sessions |
| **Guest Access** | Share your workspace with others for collaborative debugging |
| **Public URLs** | Expose web apps on port 8000 via public URLs |
| **ShareIt** | A community channel for sharing projects and peer feedback |

#### The Philosophy of Default Code

One of the most important design decisions: after the AI responds, the Solveit interface **defaults to letting you type code**, not accept AI output. The "Default Code" toggle ensures the human remains in the driver's seat. This is a deliberate countermeasure against automation bias (Module 09) — the platform is engineered to keep you actively engaged.

### 3. FastHTML: Web Apps Without JavaScript

**FastHTML** is a Python web framework released by Answer.AI that lets you build interactive web applications using **Python + HTMX**, with zero JavaScript.

#### Core Idea

Traditional web apps require three languages: HTML (structure), CSS (style), and JavaScript (behaviour). FastHTML replaces JS with **HTMX** — a library that lets you declare dynamic behaviour directly in HTML attributes. The server returns HTML fragments, not JSON, and HTMX swaps them into the page.

```python
from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return Titled("Hello, FastHTML!",
        P("This page was built with Python only."),
        Button("Click me", hx_get="/clicked", hx_swap="outerHTML"),
    )

@rt("/clicked")
def get():
    return P("You clicked the button! No JavaScript needed.")

serve()
```

#### Why It Matters

- **Single language:** Python only. No context-switching between Python and JS.
- **Full-stack from one codebase:** The same Python functions handle routing and rendering.
- **AI-friendly:** FastHTML includes a `/llms-ctx.txt` endpoint that tells AI assistants (Claude, ChatGPT, Copilot) how to write FastHTML code. This is unprecedented — a framework designed *for AI collaboration from the ground up*.

#### The LLM Context File

```text
# FastHTML's /llms-ctx.txt endpoint
# An AI assistant can read this to learn FastHTML patterns:
# - Use fasthtml.common for all components
# - Routes are decorated with @rt(path)
# - HTMX attributes (hx_get, hx_post, hx_swap) handle interactivity
# - No JavaScript required
```

This is fast.ai's philosophy made concrete: instead of forcing developers to learn how AIs think, make the framework AI-readable.

### 4. fasttransform: Reversible Pipelines

**fasttransform** (released February 2025) is a Python library extracted from fastcore/fastai that treats data transformations as **reversible, inspectable objects**.

#### The Problem

Traditional ML pipelines are one-way: you apply transformations to raw data, train a model, and if something goes wrong, you cannot easily trace back to see what the model *actually* saw. Was that weird prediction caused by a bad image, or by a bug in your normalization?

#### The Solution

fasttransform makes every transformation reversible and provides a `decode()` method to inspect the original data:

```python
from fasttransform import Pipeline, Resize, Normalize, ToTensor

# Pipeline of reversible transformations
pipe = Pipeline([
    Resize(224),
    Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensor(),
])

# Apply (encode)
transformed = pipe(image)

# Inspect what the model actually sees
reconstructed = pipe.decode(transformed)  # back to original image space

# Debug: what did the normalization do to this specific pixel?
original_pixel = pipe.decode_at(0, transformed[0, 100, 100])  # decode step 0 only
```

It uses **multiple dispatch** (via the `plum` library) so a single pipeline can handle different data types — images, masks, text — with different transformation logic for each.

### 5. mojokernel: Mojo in Jupyter

**Mojo** is a programming language created by Chris Lattner (creator of LLVM, Swift) that combines Python-like syntax with C-level performance. Jeremy Howard has been an active collaborator.

Answer.AI developed **mojokernel**, a custom Jupyter kernel that lets you run Mojo code in Jupyter notebooks with:
- Variable persistence across cells (like Python notebooks)
- Function definitions that survive cell re-execution
- A fast, reliable interface built on undocumented Mojo internals

This is a community project until Modular releases an official kernel, but it demonstrates Answer.AI's commitment to the Mojo ecosystem.

### 6. The Anti-Agentic AI Philosophy

Across all of fast.ai's 2026 output — the blog posts, the platform design, the course content — runs a consistent thread: **skepticism toward fully autonomous AI agents.** This is not Luddism; it is a reasoned position based on research and observation.

#### The Argument

1. **Agentic AI replaces human judgment.** When an AI autonomously writes code, makes decisions, and executes actions, the human becomes a supervisor rather than a creator. This erodes the very skills the human needs to evaluate the AI's output.

2. **The METR research.** Studies from METR (Model Evaluation and Threat Research) show that developers using heavy AI assistance often *feel* more productive while actually producing harder-to-maintain code. The perception of productivity outstrips the reality.

3. **Understanding debt (revisited).** Module 10 introduced understanding debt. The anti-agentic stance is the logical conclusion: if the AI does the thinking, the human accrues understanding debt with every action. At some point, the human can no longer meaningfully supervise.

4. **Human agency as the goal.** fast.ai argues that the purpose of AI tools should be to *augment human capability*, not replace human judgment. The Solveit platform is designed around this: the AI suggests, the human decides. The "Default Code" toggle is a physical manifestation of this philosophy.

#### The Alternative: Collaborative AI

Instead of "give me a full app," fast.ai advocates:
- "What are my options for step 1?"
- "Review my approach to step 2."
- "Help me debug this specific error."

The AI is a collaborator with specific strengths (speed, breadth of knowledge, pattern matching) and weaknesses (lack of true understanding, hallucination, context limits). The human provides what the AI cannot: genuine understanding, value judgment, and responsibility.

### 7. Rachel Thomas's 2026 Education Critique

Rachel Thomas's February 2026 essay **"What analog and AI education both get wrong"** and her December 2025 essay **"Stop Saying Boredom is Good for Kids"** form a sharp critique of contemporary education — both traditional and AI-powered.

#### Key Arguments

- **Both sides get it wrong.** Traditional "analog" education (no screens, no AI) and tech-utopian AI education (AI tutors for everything) share a common flaw: they ignore *how real learning happens.* Learning requires active struggle, iteration, and the freedom to make mistakes.

- **Learning dashboards are the wrong metric.** In "I Don't Want a Learning Dashboard for My Child" (Feb 2026), Thomas argues that the quantification of learning (progress bars, completion percentages, skill scores) creates a *simulacrum* of education. The map (the dashboard) replaces the territory (actual understanding).

- **The Solveit alternative.** The Solveit platform's ShareIt feature where students share projects and give peer feedback is presented as a counter-model: qualitative, community-driven assessment instead of quantitative metrics.

- **Boredom is not a virtue.** In "Stop Saying Boredom is Good for Kids" (Dec 2025), Thomas challenges the romantic notion that boredom builds character. Chronic boredom causes stress, disengagement, and poor well-being. The goal should be *engagement*, not enforced simplicity.

### 8. The fast.ai Library and nbdev in 2026

fast.ai's foundational libraries continue to be maintained and used:

- **fastai 2.7.x** remains stable and compatible with PyTorch 2.x. No major version bump has occurred, as the team's focus has shifted to Answer.AI tools, but the library is battle-tested and production-ready.

- **nbdev 2.3.x** continues to be the tool of choice for notebook-driven development. The Quarto-based documentation workflow is mature, and the `nbdev_mkdocs` integration makes it easy to publish docs from notebooks.

---

## Code Examples

### Example 1: A FastHTML Hello World

```python
"""A minimal FastHTML web application — Python only, no JavaScript."""

from fasthtml.common import *


app, rt = fast_app()


@rt("/")
def home():
    return Titled("FastHTML Demo",
        H1("Hello from FastHTML!"),
        P("This entire page was built with Python and HTMX."),
        Button("Click me!", hx_get="/click", hx_swap="outerHTML"),
    )


@rt("/click")
def click():
    return P("You clicked! No JavaScript was harmed in the making of this page.",
             Style("color: green; font-weight: bold;"))


@rt("/api/hello/{name}")
def hello(name: str):
    return JSONResponse({"message": f"Hello, {name}!"})


if __name__ == "__main__":
    serve()
```

### Example 2: A Reversible Pipeline with fasttransform

```python
"""Demonstrate fasttransform's reversible pipeline concept."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


class Transform:
    """A single reversible transformation."""

    def encode(self, x: Any) -> Any:
        raise NotImplementedError

    def decode(self, x: Any) -> Any:
        raise NotImplementedError


@dataclass
class Normalize(Transform):
    """Normalize values to [0, 1] using min-max scaling."""

    min_val: float = 0.0
    max_val: float = 255.0

    def encode(self, x: float | list) -> float | list:
        if isinstance(x, list):
            return [(v - self.min_val) / (self.max_val - self.min_val) for v in x]
        return (x - self.min_val) / (self.max_val - self.min_val)

    def decode(self, x: float | list) -> float | list:
        if isinstance(x, list):
            return [v * (self.max_val - self.min_val) + self.min_val for v in x]
        return x * (self.max_val - self.min_val) + self.min_val


@dataclass
class Pipeline:
    """A sequence of reversible transformations."""

    transforms: list[Transform] = field(default_factory=list)

    def encode(self, x: Any) -> Any:
        for t in self.transforms:
            x = t.encode(x)
        return x

    def decode(self, x: Any) -> Any:
        for t in reversed(self.transforms):
            x = t.decode(x)
        return x

    def decode_at(self, step: int, x: Any) -> Any:
        """Reverse only from the end back to a specific step."""
        for t in reversed(self.transforms[step:]):
            x = t.decode(x)
        return x


# Usage:
pipe = Pipeline([
    Normalize(min_val=0, max_val=255),
])

original = 128.0
encoded = pipe.encode(original)
decoded = pipe.decode(encoded)
print(f"{original} -> {encoded:.4f} -> {decoded}")
# 128.0 -> 0.5020 -> 128.0
```

### Example 3: Granular Context Management (Solveit-Inspired)

```python
"""Simulate Solveit's granular context management for AI interactions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import auto, Enum


class MessageState(Enum):
    ACTIVE = auto()     # visible to AI
    HIDDEN = auto()     # invisible to AI
    PINNED = auto()     # always visible, cannot be evicted


@dataclass
class ContextMessage:
    role: str        # "human", "ai", "system"
    content: str
    state: MessageState = MessageState.ACTIVE


class ManagedContext:
    """A Solveit-inspired context manager with granular control."""

    def __init__(self, max_tokens: int = 4096):
        self._messages: list[ContextMessage] = []
        self.max_tokens = max_tokens

    def add(self, role: str, content: str, state: MessageState = MessageState.ACTIVE) -> None:
        self._messages.append(ContextMessage(role=role, content=content, state=state))

    def hide(self, index: int) -> None:
        """Hide a message from the AI (e.g., a previous wrong answer)."""
        if 0 <= index < len(self._messages):
            self._messages[index].state = MessageState.HIDDEN

    def pin(self, index: int) -> None:
        """Pin a message so it is always included (e.g., system prompt)."""
        if 0 <= index < len(self._messages):
            self._messages[index].state = MessageState.PINNED

    def get_active_context(self) -> list[dict]:
        """Return only messages visible to the AI, with pinned ones first."""
        pinned = [m for m in self._messages if m.state == MessageState.PINNED]
        active = [m for m in self._messages if m.state == MessageState.ACTIVE]

        context = pinned + active
        # Truncate to max_tokens approximately
        total = 0
        for i, m in enumerate(context):
            total += len(m.content.split())
            if total > self.max_tokens:
                context = context[:i]
                break
        return [{"role": m.role, "content": m.content} for m in context]


# Usage:
ctx = ManagedContext()
ctx.add("system", "You are a helpful assistant.", state=MessageState.PINNED)
ctx.add("human", "How do I parse JSON in Python?")
ctx.add("ai", "Use json.loads()...")  # wrong answer
ctx.hide(2)  # hide the wrong answer
ctx.add("human", "Let me clarify: I need to parse nested JSON with error handling.")
print(ctx.get_active_context())
```

### Example 4: The METR Productivity Paradox (Simulation)

```python
"""Simulate the METR finding: perceived vs actual productivity with AI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProductivityMetrics:
    mode: str  # "solo", "ai-assisted", "agentic"
    perceived_productivity: float = 0.0  # 0-10 self-rating
    actual_output_quality: float = 0.0    # 0-10 objective measure
    code_maintainability: float = 0.0     # 0-10 expert rating
    understanding_retention: float = 0.0  # 0-10 follow-up test

    def gap(self) -> float:
        """The gap between perceived and actual productivity."""
        return self.perceived_productivity - self.actual_output_quality


# Research-based estimates (informed by METR and similar studies):
SCENARIOS = [
    ProductivityMetrics(
        mode="solo (no AI)",
        perceived_productivity=4.0,
        actual_output_quality=6.0,
        code_maintainability=8.0,
        understanding_retention=9.0,
    ),
    ProductivityMetrics(
        mode="AI-assisted (Solveit-style)",
        perceived_productivity=7.0,
        actual_output_quality=8.0,
        code_maintainability=7.0,
        understanding_retention=7.0,
    ),
    ProductivityMetrics(
        mode="agentic (full automation)",
        perceived_productivity=9.0,
        actual_output_quality=5.0,
        code_maintainability=3.0,
        understanding_retention=2.0,
    ),
]

for s in SCENARIOS:
    print(f"{s.mode:<35s} perceived={s.perceived_productivity}/10 "
          f"actual={s.actual_output_quality}/10 "
          f"gap={s.gap():+.1f} "
          f"maintain={s.code_maintainability}/10 "
          f"understand={s.understanding_retention}/10")
```

---

## Common Mistakes to Avoid

**Mistake 1 — Confusing Solveit with a standard chatbot.**

```text
BAD:  "Solveit is just another ChatGPT wrapper."
GOOD: "Solveit is a fundamentally different interaction model: editable dialogs,
      shared context, persistent environments, and a deliberate 'human-first'
      design philosophy. It treats the conversation as an engineering artifact."
```

**Mistake 2 — Assuming FastHTML requires frontend knowledge.**

```python
# BAD: reaching for JavaScript when FastHTML can do it
<script>
  document.getElementById("btn").onclick = function() { ... }
</script>

# GOOD: using HTMX declaratively in Python
Button("Click me", hx_get="/endpoint", hx_swap="outerHTML")
```

**Mistake 3 — Treating Answer.AI tools as replacements for established ones.**

```text
BAD:  "FastHTML replaces Django/Flask. fasttransform replaces scikit-learn."
GOOD: "FastHTML is a complementary tool for building interactive prototypes
      quickly. fasttransform integrates into existing pipelines. Use the right
      tool for the job — Answer.AI's tools excel at rapid iteration and
      AI-collaborative workflows."
```

---

## Best Practices

1. **Use Solveit's context management features deliberately** — pin system prompts, hide wrong answers, and collapse irrelevant sections to keep the AI focused.
2. **Enable "Default Code" mode** to keep yourself in the driver's seat after AI interactions.
3. **Use FastHTML for prototypes and internal tools** — its simplicity shines for projects where Python is the primary language.
4. **Pair fasttransform with visual debugging** — decode transformed data to images/plots to verify your pipeline is correct.
5. **Read the `/llms-ctx.txt` of any framework** before asking an AI to write code for it — this tells the AI how to generate idiomatic code.
6. **Resist the agentic temptation** — break tasks into small steps where you understand and verify each one.
7. **Participate in ShareIt-style communities** — qualitative peer feedback is more valuable than quantitative metrics.
8. **Stay engaged with the fast.ai blog** — Rachel Thomas and Jeremy Howard continue to publish some of the most thoughtful writing on AI and society.

---

## Practice Exercises

### Exercise 1: FastHTML Mini-App
Build a minimal FastHTML app with two routes: a home page with a button and an API endpoint that returns JSON when the button is clicked. Run it and verify both work.

### Exercise 2: Reversible Pipeline
Using the `Pipeline` and `Normalize` classes from Example 2, add an `AddNoise` transform that adds Gaussian noise during encoding and subtracts it during decoding. Verify that `decode(encode(x)) ≈ x` for various inputs.

### Exercise 3: Context Manager
Extend the `ManagedContext` class to support a `collapse(section_heading)` method that hides all messages under a given markdown heading. This simulates Solveit's collapsible sections feature.

### Exercise 4: Productivity Paradox
Modify the `ProductivityMetrics` simulation to model a 4-week project where understanding debt accumulates over time. Use different decay rates for each mode and plot the results.

### Exercise 5: LLM Context File
Write an `/llms-ctx.txt` for a small Python library you maintain. Follow FastHTML's pattern: explain the core API, key conventions, and example patterns. Test it by asking an AI to write code using your library.

---

## Summary

1. **fast.ai joined Answer.AI in 2024**, transitioning from a course provider to an R&D lab building human-centered AI tools.
2. **Solveit** has matured into a full-featured platform with Monaco editor, symbol browser, granular context control, and community sharing (ShareIt).
3. **FastHTML** lets you build interactive web apps with Python + HTMX, no JavaScript required. Its `/llms-ctx.txt` endpoint is a pioneering design for AI-friendly frameworks.
4. **fasttransform** makes data transformations reversible and inspectable via multiple dispatch.
5. **mojokernel** brings the Mojo language to Jupyter notebooks.
6. The **anti-agentic AI stance** is the philosophical core: AI should augment human capability, not replace it. The Solveit platform is engineered to keep humans engaged and in control.
7. **Rachel Thomas's 2026 essays** critique both traditional and AI-powered education, arguing for qualitative, community-driven learning over quantified dashboards.
8. The **fastai library and nbdev** continue to be maintained, with the Answer.AI ecosystem building on their foundations.

**This module completes the fast.ai learning track.** From training your first classifier in Module 01 to understanding the full contemporary ecosystem in 2026, you now have a comprehensive view of fast.ai's past, present, and future. The next step is to apply these principles in your own projects — building with AI, not being replaced by it.

---

## References

- fast.ai blog (2024–2026). [fast.ai](https://www.fast.ai)
- Answer.AI. [answer.ai](https://www.answer.ai)
- AnswerDotAI GitHub. [github.com/AnswerDotAI](https://github.com/AnswerDotAI)
- Solveit platform. [solve.it.com](https://solve.it.com)
- HTMX. [htmx.org](https://htmx.org)
- FastHTML. [fastht.ml](https://fastht.ml)
- Mojo language. [modular.com/mojo](https://www.modular.com/mojo)
- Thomas, R. (2026). "What analog and AI education both get wrong." *fast.ai.*
- Thomas, R. (2025). "Stop Saying Boredom is Good for Kids." *fast.ai.*
