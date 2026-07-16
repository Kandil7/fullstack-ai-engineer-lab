# Glossary: How to Solve It With Code — Dialog Engineering

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Dialog Engineering | The discipline of structuring AI conversations as editable, transparent artifacts | Treat the conversation as code — shaped, pruned, and deliberate |
| Solveit | Custom-built platform for Dialog Engineering with fluid dialogs and shared context | By Answer.AI / fast.ai, 2024 |
| Fluid Dialog | A conversation where messages can be edited, deleted, hidden, or pinned | Prevents context degradation |
| Shared Context | The AI sees everything the human sees — code, notes, files, test output | Eliminates the "telephone game" |
| Ghost Text | AI completions that must be explicitly accepted before entering the codebase | Forces deliberate review |
| Side Quest | A deliberate learning detour to understand an unfamiliar concept | Builds durable knowledge |
| Understanding Debt | The gap between what code does and what you understand about it | Accrues when you accept without reading |
| Vibe Coding | Generating large code blocks from vague prompts with minimal review | Feels productive, often isn't |
| Dark Flow | A superficial "flow" state characterized by high-frequency, low-reward iterations | Induced by vibe coding |
| Polya's Framework | Four-step problem-solving: Understand, Plan, Execute, Review | Universal heuristic from 1945 |
| Ghost Text vs Autocomplete | Ghost text must be accepted; autocomplete can be tabbed through | Ghost text is more deliberate |

---

## Detailed Definitions

### Dialog Engineering

**Definition:** The discipline of structuring communication with an AI to maximize shared understanding over long, complex sessions. The conversation itself is treated as an engineering artifact — editable, pruneable, and deliberately shaped rather than passively accumulated.

## Example

```text
Dialog Engineering:               Passive Chat:
Q: How do I parse JSON?          Q: How do I parse JSON?
A: [wrong approach] → HIDDEN      A: [wrong approach]
Q: Let me clarify...              Q: Actually, I meant...
A: [correct approach] → PIN       A: [confused by wrong history]
```

**Related Terms:** Fluid Dialog, Shared Context, Solveit

- Treats the conversation state as something to be actively maintained.
- Counteracts the "context decay" problem in long AI sessions.

---

### Solveit

**Definition:** A web-based platform built by Answer.AI and fast.ai that implements Dialog Engineering through fluid, editable dialogs, shared context (the AI sees everything you see), and tool-agnostic support for any domain.

**Related Terms:** Dialog Engineering, Fluid Dialog, Shared Context

- Powers everything from coding to legal drafting to business strategy.
- Designed for the "How to Solve it With Code" course.
- URL: solve.it.com

---

### Fluid Dialog

**Definition:** A conversation model where messages can be edited, deleted, hidden, or pinned. Hidden content is invisible to the AI, so the active context stays clean and focused.

## Example

```text
Standard chat is append-only: every mistake accumulates.
Fluid dialog lets you prune mistakes, so the AI never sees them.
```

**Related Terms:** Dialog Engineering, Shared Context

- The single most important design difference from standard chat interfaces.
- Prevents the model from learning from or being confused by earlier mistakes.

---

### Shared Context

**Definition:** A design where the AI has access to the same information the human does — including code files, notes, test output, and results — in a unified workspace.

## Example

```python
# Instead of describing code to the AI:
prompt = "I have a function that does X..."

# Solveit lets the AI read the actual file:
# AI sees: the file contents, test results, error messages directly
```

**Related Terms:** Dialog Engineering, Fluid Dialog

- Eliminates the "telephone game" of describing context.
- The AI can reference variables and functions by name.

---

### Ghost Text

**Definition:** AI-generated code suggestions that are displayed inline but must be explicitly accepted (e.g., by pressing Tab or clicking Accept) before they enter the codebase.

**Related Terms:** Dialog Engineering, Understanding Debt

- Differs from autocomplete: ghost text requires deliberate acceptance.
- Forces read-before-merge, counteracting automation bias.

---

### Side Quest

**Definition:** A deliberate learning detour taken when the AI suggests an unfamiliar concept. Instead of accepting blindly, you pause to understand, experiment with, and document the concept before returning to the main task.

## Example

```text
Main: Build a scraper
  → AI suggests "try BeautifulSoup"
  → SIDE QUEST: What is BeautifulSoup? How does parse tree work?
    → Write a tiny HTML parser
    → Test it
    → Create a flashcard
  → Return to scraper with deeper understanding
```

**Related Terms:** Understanding Debt, Dialog Engineering

- The primary mechanism for building durable knowledge.
- Turns AI interactions into learning opportunities, not dependencies.

---

### Understanding Debt

**Definition:** The gap between what your code *does* and what you *understand* about it. Every AI-generated line you accept without reading, every library you import without knowing what it does, and every fix whose root cause you never learned — all of it accrues understanding debt.

## Example

```text
Codebase grows:     ████████████████░░  (100% working)
Understanding:      ████░░░░░░░░░░░░░░  (30% understood)
                    └────────────────►
                      Understanding debt = 70%
```

**Related Terms:** Side Quest, Dialog Engineering

- The critical risk of uncritical AI use.
- Eventually makes debugging, extending, or shipping impossible.
- The collapse point is when you can no longer fix what breaks.

---

### Vibe Coding

**Definition:** A style of AI-assisted development where the human gives vague, high-level prompts, accepts large blocks of generated code with minimal review, and moves quickly to the next task — creating a "vibe" of productivity that research shows may not match actual output.

**Related Terms:** Dark Flow, Understanding Debt, Dialog Engineering

- Identified and critiqued by Rachel Thomas (fast.ai, Jan 2026).
- Induces a "dark flow" state that feels productive.
- METR research: developers *feel* more productive but often produce harder-to-maintain code.

---

### Dark Flow

**Definition:** A term adapted from Csikszentmihalyi's concept of flow. Unlike true flow (a positive, growth-producing state), "dark flow" is a superficial addiction characterized by high-frequency, low-reward iterations — similar to the "loss disguised as a win" mechanics in addictive slot machines.

**Related Terms:** Vibe Coding, Understanding Debt

- Coined in Rachel Thomas's "Breaking the Spell of Vibe Coding" (2026).
- Key signal: you feel productive but cannot explain what you produced.
- The antidote is deliberate, reviewed, incrementally verified work.

---

### Polya's Framework

**Definition:** A four-step problem-solving heuristic from George Polya's 1945 book *How to Solve It*: (1) Understand the problem, (2) Devise a plan, (3) Carry out the plan, (4) Look back and review.

## Example

```text
Applied to AI-assisted coding:
1. UNDERSTAND: What are we building? What constraints exist?
2. PLAN:      Ask AI for approaches; choose one.
3. EXECUTE:   Implement in small steps; test each.
4. REVIEW:    Reflect on the result; extract patterns.
```

**Related Terms:** Dialog Engineering, Side Quest

- Steps 1 (Understand) and 4 (Review) are the human's core responsibility.
- AI accelerates steps 2 and 3.
- Skipping steps 1 or 4 is the root cause of understanding debt.

---

## Summary

1. **Dialog Engineering** is the discipline of treating AI conversations as editable, deliberate artifacts — implemented by the **Solveit** platform.
2. **Fluid dialogs** let you clean context by hiding/editing/deleting messages, preventing the context decay that plagues standard chat.
3. **Shared context** eliminates the telephone game: the AI sees exactly what you see.
4. **Side quests** are the practice of pausing to learn unfamiliar concepts — building durable knowledge instead of **understanding debt**.
5. **Vibe coding** (accepting AI output without review) feels productive but induces a **dark flow** state and accrues understanding debt until the codebase becomes unmanageable.
6. **Polya's framework** (Understand → Plan → Execute → Review) is a universal scaffolding for deliberate AI collaboration; the human must own steps 1 and 4.
