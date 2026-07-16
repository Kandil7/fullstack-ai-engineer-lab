# Lecture 10: How to Solve It With Code — Dialog Engineering & the Solveit Platform

## Topic Overview

In November 2024, fast.ai announced it was joining **Answer.AI** — a new kind of AI R&D lab co-founded by Jeremy Howard that focuses on practical end-user products built from foundational research breakthroughs. Their first major output was a reimagined educational experience: **"How to Solve It With Code,"** a course that teaches a discipline called **Dialog Engineering** through a custom-built platform called **Solveit.**

This lecture covers the philosophical shift from "vibe coding" (blindly generating large code blocks with AI) to deliberate, iterative problem-solving where the AI is a transparent partner rather than a black-box oracle. It borrows its name and ethos from George Polya's 1945 classic *How to Solve It* — a book about mathematical problem-solving heuristics — and applies those same heuristics to the modern practice of coding with AI.

**Duration:** 2–3 hours  
**Difficulty:** All levels  
**Prerequisites:** Lecture 01 (Getting Started), basic Python programming

---

## Learning Objectives

By the end of this lecture you will be able to:

1. **Explain** the "How to Solve It" philosophy and how it differs from traditional programming education and "vibe coding."
2. **Define** Dialog Engineering and its core components: fluid dialogs, shared context, and transparent tool use.
3. **Contrast** the Solveit platform's design with standard chat-based AI coding interfaces and identify where each excels.
4. **Apply** Polya's four-step problem-solving framework (understand, plan, execute, review) to an AI-assisted coding task.
5. **Practice** deliberate "side quests" — pausing to understand an AI-suggested concept before accepting it.
6. **Design** an effective shared-context prompt that gives the AI enough information to be useful without surrendering control.
7. **Critique** the "vibe coding" phenomenon and its risks (skill erosion, hidden technical debt, "understanding debt").
8. **Describe** how Solveit's fluid-dialog model prevents context degradation and maintains clean AI state over long sessions.

---

## Key Concepts

### 1. The "How to Solve It" Philosophy

George Polya's 1945 book *How to Solve It* laid out a universal four-step heuristic for solving mathematical problems:

1. **Understand the problem.** What is unknown? What are the data and conditions?
2. **Devise a plan.** Find a connection between the data and the unknown — consider analogous problems, decompose, generalize.
3. **Carry out the plan.** Execute step by step, checking each step.
4. **Look back.** Examine the solution. Can you derive it differently? Can you use it for another problem?

The Solveit course applies this same framework to modern AI-assisted coding:

```text
┌─────────────────────────────────────────────────────────┐
│            POLYA'S FRAMEWORK × AI CODING                 │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  1. UNDERSTAND ── Load context, define the goal,          │
│                   identify constraints and unknowns.       │
│                                                           │
│  2. DEVISE ────── Ask the AI for approaches; explore      │
│                   alternatives; pick a strategy.           │
│                                                           │
│  3. EXECUTE ───── Implement in small, verifiable steps;    │
│                   test each increment before moving on.    │
│                                                           │
│  4. REVIEW ────── Reflect on the outcome; extract          │
│                   reusable patterns; update your plan.     │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

The key insight: **the AI accelerates steps 2 and 3, but steps 1 and 4 remain firmly the human's responsibility.** Outsourcing understanding or review to the AI is where problems begin.

### 2. Dialog Engineering

The Solveit team coined **Dialog Engineering** to describe the discipline of structuring communication with an AI to maximize shared understanding over long, complex sessions. It treats the conversation itself as an engineering artifact — editable, pruneable, and deliberately shaped rather than passively accumulated.

#### Core principles:

**a) Fluid & Editable Dialogs**
Standard chat interfaces are append-only: every message accumulates linearly, and once sent, it cannot be removed. This means every mistake, off-topic detour, or low-quality AI response permanently degrades the conversation's "state." Solveit inverts this: you can **edit, delete, hide, or pin** messages. The AI never sees content you have hidden or deleted, so the active context stays clean.

```text
Standard chat:               Solveit fluid dialog:
┌──────────────────┐         ┌──────────────────┐
│ Q: How do I...?  │         │ Q: How do I...?  │ (pinned)
│ A: [good answer] │         │ A: [good answer] │ (pinned)
│ Q: What about...?│         │ Q: What about...?│
│ A: [wrong]       │ ← stuck │ A: [wrong]       │ ← HIDDEN
│ Q: Actually...   │         │ Q: Let me rephrase│
│ A: [confused]    │         │ A: [better]       │
└──────────────────┘         └──────────────────┘
```

**b) Shared Transparent Context**
The AI can see everything the human sees — the code, notes, file contents, and test results — in a unified workspace. Instead of pasting snippets back and forth, you work in a shared state where the AI can:

- Reference variables and functions from your code directly
- Browse your project files
- Execute Python functions (agentic actions) with your permission
- See the output of commands and tests

This eliminates the "telephone game" where you describe code to an AI that cannot see it.

**c) Proactive but Controlled Assistance**
Solveit provides "ghost text" completions and AI suggestions, but they must be **explicitly accepted** before they enter the codebase. This design forces deliberate read-before-merge, counteracting automation bias (see Lecture 09) and ensuring each line is understood.

### 3. Deliberate Practice & Side Quests

The course pedagogy emphasizes **understanding over throughput.** When the AI suggests something unfamiliar — a library, a pattern, a technique — the recommended response is to go on a **side quest**:

```text
Main task: build a web scraper
  ├── AI suggests using `BeautifulSoup`
  ├── SIDE QUEST: what is `BeautifulSoup`? How does it parse HTML?
  │   ├── Ask the AI to explain the concept
  │   ├── Write a small test to verify your understanding
  │   └── Create a flashcard with fastanki for spaced repetition
  └── Return to the main task with deeper understanding
```

These side quests build durable knowledge rather than accumulating "understanding debt" — the state where you have running code you cannot explain or modify.

### 4. Understanding Debt vs. Durable Knowledge

The course identifies a critical failure mode of AI-assisted development: **understanding debt.** This is the gap between what your code *does* and what you *understand* about it. Every AI-generated line you accept without reading, every library you import without knowing what it does, and every fix the AI applies whose root cause you never learned — all of it accrues understanding debt.

```text
                    CODE COMPLEXITY
                         ▲
                         │                        ✦ collapse point
                         │                   ✦       (can't debug,
                         │              ✦             can't extend,
                         │         ✦                  can't ship)
                         │    ✦
                         │ ✦
                         │─────────────────────────► TIME
                              UNDERSTANDING
                              grows more slowly
                              than codebase
```

The antidote is the Solveit methodology: **every new concept becomes a side quest.** The goal is not merely to produce running code, but to produce a team (human + AI) whose combined understanding of the codebase grows with it.

### 5. Beyond Programming: Universal Problem Solving

The course quickly moves beyond coding into domains like system administration, business strategy, legal drafting, and research. The reason is that Polya's heuristics and Dialog Engineering apply to **any structured problem**, not just software:

| Domain | Understand | Plan | Execute | Review |
|--------|-----------|------|---------|--------|
| Web app | Define requirements, user roles | Choose stack, plan API | Build components, test | Audit for gaps, ship |
| Legal brief | Identify facts, jurisdiction | Research precedents | Draft sections | Verify citations, logic |
| Business case | Market, competitors, constraints | Financial model | Write proposal | Stress-test assumptions |

In every case, the AI accelerates execution while the human retains control over understanding, planning, and review.

### 6. How Solveit Differs from Vibe Coding

The fast.ai blog post "Breaking the Spell of Vibe Coding" (January 2026) by Rachel Thomas draws an important distinction. **Vibe Coding** — generating large amounts of code from vague prompts and accepting the output wholesale — induces what psychologist Mihaly Csikszentmihalyi called a "dark flow" state. It *feels* productive (high-frequency, low-reward iterations) but research (e.g., from METR) shows that developers relying heavily on AI agents often **feel** more productive while actually producing harder-to-maintain code and taking longer overall.

Solveit's design explicitly counters this:

| Vibe Coding | Dialog Engineering |
|------------|-------------------|
| AI generates large blocks | Human + AI iterate in small steps |
| Code accepted with minimal review | Every line read and understood |
| Context degrades over long sessions | Context stays clean via fluid editing |
| Understanding debt accumulates | Side quests build durable knowledge |
| Human feels productive (dark flow) | Human *is* productive (verified iterations) |

---

## Code Examples

### Example 1: Setting Up a Solveit-Inspired Shared Context

While Solveit itself is a proprietary platform, you can apply its principles in any environment. The key structure: provide the AI with a clear context of files, goals, and constraints before starting.

```python
"""A Solveit-inspired shared context structure for AI-assisted coding.

This pattern gives the AI the same context you have — code, notes,
goals, and constraints — in a structured, editable form.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SharedContext:
    """Everything the AI needs to understand the current task."""

    goal: str
    constraints: list[str] = field(default_factory=list)
    relevant_files: list[Path] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    test_results: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    def add_file_contents(self, path: str) -> None:
        p = Path(path)
        if p.exists():
            self.notes.append(f"=== {path} ===\n{p.read_text()}\n=== end ===")

    def summarize(self) -> str:
        parts = [f"GOAL: {self.goal}"]
        if self.constraints:
            parts.append("CONSTRAINTS:\n- " + "\n- ".join(self.constraints))
        for note in self.notes:
            parts.append(note)
        if self.open_questions:
            parts.append("OPEN QUESTIONS:\n- " + "\n- ".join(self.open_questions))
        return "\n\n".join(parts)


# Usage:
ctx = SharedContext(
    goal="Build a web scraper for blog posts",
    constraints=["Must respect robots.txt", "Output valid JSON"],
)
ctx.add_file_contents("scraper.py")
ctx.add_file_contents("tests/test_scraper.py")
print(ctx.summarize())  # Send this as context to your AI assistant
```

### Example 2: A Side Quest Logger

When you go on a side quest, log what you learned. This turns ad-hoc exploration into a searchable knowledge base.

```python
"""Track side quests — concepts you paused to learn during development."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class SideQuest:
    """A deliberate learning detour during development."""

    topic: str
    context: str  # What task prompted this?
    what_i_learned: str
    code_example: str = ""
    tags: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_flashcard(self) -> tuple[str, str]:
        """Generate a Q/A pair for spaced repetition."""
        return (f"Q: {self.topic}", f"A: {self.what_i_learned}")


class SideQuestLog:
    """A running log of side quests from a development session."""

    def __init__(self) -> None:
        self._quests: list[SideQuest] = []

    def add(self, topic: str, context: str, learned: str) -> SideQuest:
        q = SideQuest(topic=topic, context=context, what_i_learned=learned)
        self._quests.append(q)
        return q

    def search(self, tag: str) -> list[SideQuest]:
        return [q for q in self._quests if tag in q.tags]

    def review_session(self) -> str:
        lines = ["## Side Quests from This Session"]
        for q in self._quests:
            lines.append(f"\n### {q.topic}")
            lines.append(f"- **Context:** {q.context}")
            lines.append(f"- **Learned:** {q.what_i_learned}")
        return "\n".join(lines)


# Usage:
log = SideQuestLog()
log.add(
    topic="BeautifulSoup parser basics",
    context="Building a web scraper, AI suggested BeautifulSoup",
    learned="BeautifulSoup parses malformed HTML into a parse tree. "
            "Key objects: Tag, NavigableString, BeautifulSoup. "
            "Use soup.find() and soup.find_all() for navigation.",
)
print(log.review_session())
```

### Example 3: Polya's Framework as a Code Review Checklist

Apply Polya's four steps to reviewing an AI-generated code change:

```python
"""Polya-inspired code review checklist for AI-assisted development."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PolyaReview:
    """A structured review using Polya's four-step framework."""

    step1_understand: list[str] = field(default_factory=list)
    step2_plan: list[str] = field(default_factory=list)
    step3_execute: list[str] = field(default_factory=list)
    step4_review: list[str] = field(default_factory=list)

    @classmethod
    def for_change(cls, description: str) -> "PolyaReview":
        return cls(
            step1_understand=[
                "Can I explain what this code does in one sentence?",
                f"Do I understand why this change was needed? ({description})",
                "Are there any functions, libraries, or patterns I don't recognize?",
            ],
            step2_plan=[
                "Would I have solved this the same way? If not, why not?",
                "Are there edge cases the AI might have missed?",
                "Is there a simpler approach that would work?",
            ],
            step3_execute=[
                "Does each line do what it claims? (read every line)",
                "Are there any off-by-one, type, or logic errors?",
                "Do the tests pass?",
            ],
            step4_review=[
                "Is this easy to modify later?",
                "What did I learn from this change?",
                "Should any part become a reusable pattern or utility?",
            ],
        )

    def results(self) -> str:
        parts = ["# Polya Review Results"]
        for step, questions in [
            ("1. Understand the Problem", self.step1_understand),
            ("2. Devise a Plan", self.step2_plan),
            ("3. Carry Out the Plan", self.step3_execute),
            ("4. Look Back", self.step4_review),
        ]:
            parts.append(f"\n## {step}")
            parts.extend(f"- [ ] {q}" for q in questions)
        return "\n".join(parts)
```

---

## Common Mistakes to Avoid

### Mistake 1: Vibe Coding Without Review

```text
BAD:  Ask AI "build me a full app" → accept all generated code → ship
      Result: understanding debt, hidden bugs, cannot extend

GOOD: Ask AI "what's the best approach for step 1?" → review → implement →
      test → move to step 2 → each line is understood before it ships
```

### Mistake 2: Context Dumping Without Structure

```python
# BAD: dumping everything into the prompt with no structure
prompt = """Here's my project. It has a bunch of files.
app.py does x, utils.py does y, and there's also config stuff.
Can you help me fix the login bug?"""

# GOOD: structured context with explicit goal and constraints
prompt = SharedContext(
    goal="Fix login bug: session expires after 1 second instead of 1 hour",
    constraints=["Cannot change the token library", "Must maintain backward compatibility"],
    relevant_files=["src/auth.py", "src/session.py", "tests/test_auth.py"],
).summarize()
```

### Mistake 3: Neglecting the Side Quest Habit

```text
BAD:  AI uses a library you've never seen → you accept and move on
      Next week: you cannot debug or modify the code

GOOD: AI uses a library you've never seen → ask "what is this?"
      → write a tiny test → create a flashcard → return to task
      You now own that knowledge permanently
```

---

## Best Practices

1. **Start with Polya's "Understand" step** — define the goal, constraints, and unknowns before writing a single line of code or prompt.
2. **Work in small, verifiable increments.** Each step should produce something you can test before moving on.
3. **Treat every unfamiliar concept as a side quest.** Pause, learn, document, return.
4. **Keep the dialog clean.** Delete or hide AI responses that are wrong or off-topic. Pin useful context.
5. **Give the AI the same context you have** — file contents, test output, error messages — not a paraphrase.
6. **Read every line before accepting it.** You are responsible for what the AI generates on your behalf.
7. **End each session with a review.** What did you learn? What would you do differently? What understanding debt remains?
8. **Log side quests.** Build a personal knowledge base from your AI interactions.
9. **Prefer asking for approaches over implementations.** Ask "what are the options?" before "write the code."
10. **Remember the goal is understanding, not output volume.** The AI is a multiplier for human skill, not a replacement for it.

---

## Practice Exercises

### Exercise 1: Apply Polya's Framework

Take a small programming problem (e.g., "scrape a website and extract all image URLs") and write out each of Polya's four steps before writing any code. Note where an AI assistant helped at each step.

### Exercise 2: Design a Shared Context

Given a project with three files (a Flask app, a database model, and a test file), write a single structured prompt that gives an AI everything it needs to add a new feature — without requiring back-and-forth clarification.

### Exercise 3: Side Quest Deep Dive

Ask an AI assistant to explain a concept you are curious about (e.g., "how does async/await work in Python?"). Then write a small script that demonstrates the concept. Log this as a side quest.

### Exercise 4: Compare Workflows

Solve the same problem twice: once with a "vibe coding" approach (one big prompt, accept all output) and once with the Solveit incrementally approach (small steps, review each). Compare the quality, your understanding, and the time taken.

### Exercise 5: Build a SideQuestLog

Extend the `SideQuestLog` class to persist to a JSON file and support search by topic. Use it over a full week of AI-assisted development and review the accumulated knowledge.

---

## Summary

1. **"How to Solve It With Code"** applies George Polya's four-step problem-solving framework to AI-assisted development: Understand, Plan, Execute, Review.
2. **Dialog Engineering** is the discipline of structuring AI conversations as editable, transparent, and deliberately shaped artifacts rather than passive chat logs.
3. **Solveit** implements fluid dialogs (edit/delete/hide messages), shared context (AI sees everything you see), and proactive but controlled assistance (accept-before-merge).
4. **Side quests** are the mechanism for building durable knowledge: every unfamiliar concept becomes a deliberate learning detour.
5. **Understanding debt** (code you cannot explain) is the critical risk of uncritical AI use; the antidote is reading every line and taking side quests.
6. **Vibe coding feels productive but can be counterproductive** — research shows it increases perceived productivity more than actual productivity.
7. The framework applies **beyond programming** to any structured problem domain.
8. **The human remains responsible** for steps 1 (understanding) and 4 (review) of Polya's cycle; the AI accelerates steps 2 and 3.

**Next lecture:** Lecture 11 — GPT Tokenizer: A Complete Guide to Tokenization in LLMs, where you will build a GPT-style tokenizer from scratch and understand why tokenization is the source of many LLM quirks.

---

## References

- Polya, G. (1945). *How to Solve It.* Princeton University Press.
- Howard, J. (2024). "A New Chapter for fast.ai: How To Solve It With Code." *fast.ai blog.*
- Thomas, R. (2026). "Breaking the Spell of Vibe Coding." *fast.ai blog.*
- Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience.*
- Solveit platform: https://solve.it.com
