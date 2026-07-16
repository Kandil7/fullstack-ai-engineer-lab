"""
10 - How to Solve It With Code: Dialog Engineering
==================================================
Goal: Practice the "Dialog Engineering" discipline — structuring AI
interactions deliberately, managing understanding debt, and applying
Polya's problem-solving framework to AI-assisted development.

You will:
  1. Use a SharedContext class to structure prompts for an AI assistant.
  2. Log side quests and review the knowledge accumulated.
  3. Run a Polya Review on a code change.
  4. Simulate the difference between vibe coding and deliberate iteration.

Prerequisites:
  - Python 3.10+
  - No external dependencies required (pure Python stdlib)

Run:
  python 10-solveit.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol


# ============================================================
# 1. SharedContext — structured context for AI-assisted work
# ============================================================
@dataclass
class SharedContext:
    """Everything an AI needs to understand the current task.

    Pattern: give the AI the *same* context you have, not a paraphrase.
    """

    goal: str
    constraints: list[str] = field(default_factory=list)
    relevant_files: list[Path] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    def add_file_contents(self, path: str) -> None:
        """Read a file and append its contents to the context notes."""
        p = Path(path)
        if p.exists():
            self.notes.append(f"=== {path} ===\n{p.read_text()}\n=== end ===")

    def summarize(self) -> str:
        """Render the context as a structured prompt for an AI assistant."""
        parts = [f"GOAL: {self.goal}"]
        if self.constraints:
            parts.append("CONSTRAINTS:\n- " + "\n- ".join(self.constraints))
        for note in self.notes:
            parts.append(note)
        if self.open_questions:
            parts.append("OPEN QUESTIONS:\n- " + "\n- ".join(self.open_questions))
        return "\n\n".join(parts)


# ============================================================
# 2. SideQuestLog — track learning detours
# ============================================================
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

    def add(self, topic: str, context: str, learned: str, tags: list[str] | None = None) -> SideQuest:
        """Record a side quest."""
        q = SideQuest(topic=topic, context=context, what_i_learned=learned, tags=tags or [])
        self._quests.append(q)
        return q

    def search(self, tag: str) -> list[SideQuest]:
        """Find all side quests with a given tag."""
        return [q for q in self._quests if tag in q.tags]

    def __len__(self) -> int:
        return len(self._quests)

    def review_session(self) -> str:
        """Generate a markdown summary of all side quests."""
        if not self._quests:
            return "No side quests recorded."
        lines = ["## Side Quests Log"]
        for q in self._quests:
            lines.append(f"\n### {q.topic} ({q.timestamp})")
            lines.append(f"- **Context:** {q.context}")
            lines.append(f"- **Learned:** {q.what_i_learned}")
            if q.code_example:
                lines.append(f"- **Code:**\n```python\n{q.code_example}\n```")
            if q.tags:
                lines.append(f"- **Tags:** {', '.join(q.tags)}")
        return "\n".join(lines)


# ============================================================
# 3. PolyaReview — structured code review using Polya's framework
# ============================================================
@dataclass
class PolyaReview:
    """Apply Polya's four steps to reviewing an AI-generated change."""

    change_description: str = ""
    step1_understand: list[str] = field(default_factory=list)
    step2_plan: list[str] = field(default_factory=list)
    step3_execute: list[str] = field(default_factory=list)
    step4_review: list[str] = field(default_factory=list)

    @classmethod
    def for_change(cls, description: str) -> "PolyaReview":
        """Create a review with default checklist items."""
        return cls(
            change_description=description,
            step1_understand=[
                "Can I explain what this code does in one sentence?",
                "Do I understand why this change was needed?",
                "Are there any functions, libraries, or patterns I don't recognize?",
            ],
            step2_plan=[
                "Would I have solved this the same way? If not, why not?",
                "Are there edge cases the AI might have missed?",
                "Is there a simpler approach that would work?",
            ],
            step3_execute=[
                "Does each line do what it claims?",
                "Are there any off-by-one, type, or logic errors?",
                "Do the tests pass?",
            ],
            step4_review=[
                "Is this easy to modify later?",
                "What did I learn from this change?",
                "Should any part become a reusable pattern?",
            ],
        )

    def results(self) -> str:
        parts = [f"# Polya Review: {self.change_description}"]
        for step, questions in [
            ("1. Understand the Problem", self.step1_understand),
            ("2. Devise a Plan", self.step2_plan),
            ("3. Carry Out the Plan", self.step3_execute),
            ("4. Look Back", self.step4_review),
        ]:
            parts.append(f"\n## {step}")
            parts.extend(f"- [ ] {q}" for q in questions)
        return "\n".join(parts)

    def score(self) -> tuple[int, int]:
        """Return (questions_answered_yes, total_questions)."""
        all_q = self.step1_understand + self.step2_plan + self.step3_execute + self.step4_review
        # In a real scenario, you'd mark items as checked; here we return total count.
        return (0, len(all_q))


# ============================================================
# 4. Simulation: Vibe Coding vs. Deliberate Iteration
# ============================================================
@dataclass
class CodingSession:
    """Track how a coding session went — vibe vs deliberate."""

    mode: str  # "vibe" or "deliberate"
    prompt_count: int = 0
    lines_generated: int = 0
    lines_read: int = 0
    bugs_introduced: int = 0
    bugs_fixed: int = 0
    side_quests_taken: int = 0
    time_minutes: float = 0.0
    understanding_gained: int = 0  # self-rated 1-10

    def summary(self) -> str:
        understanding_debt = max(0, self.lines_generated - self.lines_read)
        return (
            f"Mode: {self.mode}\n"
            f"  Prompts: {self.prompt_count} | Lines: {self.lines_generated}\n"
            f"  Lines read: {self.lines_read} | Debt: {understanding_debt}\n"
            f"  Bugs introduced: {self.bugs_introduced} | Fixed: {self.bugs_fixed}\n"
            f"  Side quests: {self.side_quests_taken} | Understanding: {self.understanding_gained}/10\n"
            f"  Time: {self.time_minutes:.0f}m\n"
        )


def simulate_vibe_session() -> CodingSession:
    """Simulate what a vibe-coding session looks like."""
    return CodingSession(
        mode="vibe",
        prompt_count=5,
        lines_generated=800,
        lines_read=50,
        bugs_introduced=12,
        bugs_fixed=1,
        side_quests_taken=0,
        time_minutes=45,
        understanding_gained=3,
    )


def simulate_deliberate_session() -> CodingSession:
    """Simulate what a deliberate Dialog Engineering session looks like."""
    return CodingSession(
        mode="deliberate",
        prompt_count=20,
        lines_generated=200,
        lines_read=200,
        bugs_introduced=3,
        bugs_fixed=3,
        side_quests_taken=4,
        time_minutes=90,
        understanding_gained=8,
    )


# ============================================================
# 5. Main demonstration
# ============================================================
def main() -> None:
    print("=" * 60)
    print("1. Shared Context Demo")
    print("=" * 60)

    ctx = SharedContext(
        goal="Build a function that validates email addresses",
        constraints=[
            "Must handle internationalized email addresses",
            "Must return clear error messages",
            "Must be testable without network access",
        ],
    )
    print(ctx.summarize())
    print()

    print("=" * 60)
    print("2. Side Quest Log Demo")
    print("=" * 60)

    log = SideQuestLog()
    log.add(
        topic="Email validation regex patterns",
        context="Building email validator, AI mentioned RFC 5321",
        learned=(
            "Email validation is surprisingly complex. RFC 5321 defines the "
            "SMTP format, while RFC 5322 defines the display format. A simple "
            "regex catches most typos but cannot validate that a domain exists "
            "or that the mailbox is real — that requires SMTP verification."
        ),
        tags=["email", "regex", "networking"],
    )
    log.add(
        topic="Internationalized email addresses (EAI)",
        context="Constraint mentioned international addresses",
        learned=(
            "Traditional SMTP only supports ASCII. EAI (RFC 6531) allows UTF-8 "
            "in both local part and domain. Python's `email` package supports "
            "this with `smtp.UTF8SMTP` but many legacy systems do not."
            "Always check if EAI is needed for your use case."
        ),
        tags=["email", "unicode", "internationalization"],
    )
    print(log.review_session())
    print()

    print("=" * 60)
    print("3. Polya Review Demo")
    print("=" * 60)
    review = PolyaReview.for_change("Add email validation function")
    print(review.results())
    print()

    print("=" * 60)
    print("4. Vibe vs. Deliberate Comparison")
    print("=" * 60)
    vibe = simulate_vibe_session()
    deliberate = simulate_deliberate_session()
    print(vibe.summary())
    print(deliberate.summary())

    # Compare
    print("Comparison:")
    print(f"  Vibe:       {vibe.understanding_gained}/10 understanding, {vibe.bugs_introduced} bugs, "
          f"debt={vibe.lines_generated - vibe.lines_read}")
    print(f"  Deliberate: {deliberate.understanding_gained}/10 understanding, {deliberate.bugs_introduced} bugs, "
          f"debt={deliberate.lines_generated - deliberate.lines_read}")

    # EXERCISE: add `written_notes` and `flashcards_created` fields to CodingSession
    # and update the simulations. Then compare the long-term knowledge retention
    # between the two modes using these new fields.

    # EXERCISE: create a SharedContext for the email validator task with real file
    # paths from your project. Use `add_file_contents()` to include existing
    # validation code if any exists.


if __name__ == "__main__":
    main()
