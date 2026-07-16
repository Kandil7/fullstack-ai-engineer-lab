"""
09 - Data Ethics
================
Goal: practice the *auditing* side of ML that fast.ai's data-ethics bonus
lesson emphasizes. There is no model to train here; the skill is measuring how
a model behaves across subgroups and over time, and documenting it.

You will:
  1. Compute confusion-matrix-based per-group error rates (disaggregated eval).
  2. Simulate a runaway feedback loop (predictive-policing style).
  3. Build a minimal model-card dataclass and render it.

Prerequisites:
  - numpy
  - pandas
  - scikit-learn

Run:
  python 09-data-ethics.py
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


# ============================================================
# 1. Disaggregated evaluation: per-group confusion-matrix rates
# ============================================================
def per_group_rates(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    groups: np.ndarray,
) -> pd.DataFrame:
    """Return accuracy, FPR, and FNR computed separately per group.

    Reporting a single aggregate metric hides subgroup failure; this is the
    core habit from the lecture.
    """
    records: list[dict[str, float]] = []
    for g in np.unique(groups):
        mask = groups == g
        # confusion_matrix with labels=[0, 1] -> [[tn, fp], [fn, tp]]
        tn, fp, fn, tp = confusion_matrix(
            y_true[mask], y_pred[mask], labels=[0, 1]
        ).ravel()
        total = int(mask.sum())
        records.append(
            {
                "group": str(g),
                "n": total,
                "accuracy": (tp + tn) / max(total, 1),
                "fpr": fp / max(fp + tn, 1),  # false-positive rate
                "fnr": fn / max(fn + tp, 1),  # false-negative rate
            }
        )
    return pd.DataFrame(records)


def flag_disparities(table: pd.DataFrame, tolerance: float = 0.10) -> list[str]:
    """Flag metrics whose max-min gap across groups exceeds ``tolerance``."""
    warnings: list[str] = []
    for metric in ("accuracy", "fpr", "fnr"):
        gap = float(table[metric].max() - table[metric].min())
        if gap > tolerance:
            warnings.append(f"{metric}: gap {gap:.2f} exceeds {tolerance:.2f}")
    return warnings


# ============================================================
# 2. Feedback-loop simulation (predictive-policing style)
# ============================================================
def simulate_feedback_loop(
    rounds: int = 20,
    initial_patrol_a: float = 0.6,
    reinforcement: float = 1.6,
    rng: np.random.Generator | None = None,
) -> pd.DataFrame:
    """Simulate patrol allocation driven by past *observed* arrests.

    True crime is EQUAL in both districts. Observed arrests grow *super-linearly*
    with patrol (``reinforcement`` > 1): concentrating officers finds
    proportionally more to arrest, and next round's patrol is allocated by the
    share of observed arrests. The small initial imbalance therefore amplifies
    toward one district -- a runaway loop / Goodhart's Law in action.
    """
    if rng is None:
        rng = np.random.default_rng(42)

    true_crime_a = true_crime_b = 100.0  # identical ground truth
    patrol_a = initial_patrol_a
    history: list[dict[str, float]] = []

    for r in range(rounds):
        patrol_b = 1.0 - patrol_a
        # observed arrests depend super-linearly on patrol intensity
        obs_a = true_crime_a * patrol_a ** reinforcement + abs(rng.normal(0, 0.5))
        obs_b = true_crime_b * patrol_b ** reinforcement + abs(rng.normal(0, 0.5))
        history.append(
            {"round": r, "patrol_a": patrol_a, "arrests_a": obs_a, "arrests_b": obs_b}
        )
        # reallocate next round's patrol by share of observed arrests
        patrol_a = obs_a / max(obs_a + obs_b, 1e-9)

    return pd.DataFrame(history)


# ============================================================
# 3. Model card as a dataclass
# ============================================================
@dataclass(frozen=True)
class ModelCard:
    """Minimal model card (after Mitchell et al., 2019)."""

    name: str
    version: str
    intended_use: str
    out_of_scope_uses: str
    disaggregated_metrics: dict[str, dict[str, float]]
    caveats: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [
            f"# Model Card: {self.name} (v{self.version})",
            f"**Intended use:** {self.intended_use}",
            f"**Out-of-scope:** {self.out_of_scope_uses}",
            "## Disaggregated metrics",
        ]
        for group, metrics in self.disaggregated_metrics.items():
            pretty = ", ".join(f"{k}={v:.3f}" for k, v in metrics.items())
            lines.append(f"- **{group}:** {pretty}")
        if self.caveats:
            lines.append("## Caveats")
            lines.extend(f"- {c}" for c in self.caveats)
        return "\n".join(lines)


# ============================================================
# Vibe Coding Self-Audit Checklist
# ============================================================
VIBE_CODING_AUDIT: list[str] = [
    "Do you read every line of AI-generated code before accepting it?",
    "Can you explain the architecture of your last AI-assisted project without looking at it?",
    "Do you take side quests to learn unfamiliar concepts suggested by AI?",
    "Do you write tests before or alongside AI-generated code?",
    "Do you review the AI's approach before accepting the first suggestion?",
    "Do you end sessions by reflecting on what you learned?",
    "Can you identify which parts of your codebase you understand vs. accepted on faith?",
]


def main() -> None:
    rng = np.random.default_rng(0)
    n = 1000

    print("=" * 60)
    print("1. Disaggregated evaluation")
    print("=" * 60)
    groups = rng.choice(["A", "B"], size=n, p=[0.7, 0.3])
    y_true = rng.integers(0, 2, size=n)
    # Inject a disparity: predictions are noisier for group B.
    y_pred = y_true.copy()
    flip_a = (groups == "A") & (rng.random(n) < 0.05)
    flip_b = (groups == "B") & (rng.random(n) < 0.30)
    y_pred[flip_a | flip_b] ^= 1

    table = per_group_rates(y_true, y_pred, groups)
    print(table.to_string(index=False))
    aggregate = float((y_pred == y_true).mean())
    print(f"\nAggregate accuracy: {aggregate:.3f}  <- this HIDES the gap")
    for w in flag_disparities(table, tolerance=0.10):
        print(f"  WARNING: {w}")

    # EXERCISE: change the flip probabilities so group A is the disadvantaged
    # one. Re-run and confirm the warning follows the disparity, not the label.

    print("\n" + "=" * 60)
    print("2. Feedback-loop simulation (equal true crime)")
    print("=" * 60)
    sim = simulate_feedback_loop(rounds=20, rng=rng)
    print(sim[["round", "patrol_a"]].head(6).to_string(index=False))
    print("...")
    print(f"Final patrol share for district A: {sim['patrol_a'].iloc[-1]:.3f}")
    print("True crime was EQUAL -- divergence is the runaway loop.")

    # EXERCISE: set initial_patrol_a=0.5 (perfectly fair start). Does the loop
    # still diverge? What does that tell you about correcting a loop after the
    # fact vs. preventing biased initial conditions?

    print("\n" + "=" * 60)
    print("3. Model card")
    print("=" * 60)
    card = ModelCard(
        name="ExampleClassifier",
        version="1.0.0",
        intended_use="Binary triage screening; advisory only.",
        out_of_scope_uses="Automated final decisions without human review.",
        disaggregated_metrics={
            row["group"]: {"accuracy": row["accuracy"], "fnr": row["fnr"]}
            for _, row in table.iterrows()
        },
        caveats=[
            "Group B has a materially higher error rate; do not deploy as-is.",
            "Trained on synthetic data; provenance is illustrative only.",
            "No recourse mechanism is wired up yet.",
        ],
    )
    print(card.to_markdown())

    # EXERCISE: add an `ethical_considerations` field to ModelCard and render it.
    # Because the dataclass is frozen, you must build a NEW card, not mutate one.

    print("\n" + "=" * 60)
    print("4. [NEW] Vibe Coding Self-Audit (Supplement Exercise)")
    print("=" * 60)
    print()
    print("Reflect on your own AI-assisted coding habits:")
    print()
    print("Rate yourself 1-5 (1=never, 5=always):")
    print()
    for q in VIBE_CODING_AUDIT:
        print(f"  [ ] {q}")
    print()
    print("If you scored 3+ on any of the first 3 questions,")
    print("you may be in dark flow. See Lecture 09 supplement")
    print("for strategies to shift to deliberate engineering.")
    print()

    print("\n" + "=" * 60)
    print("5. [NEW] Close Reading Workflow (Supplement Challenge)")
    print("=" * 60)
    print()
    print("To practice close reading with AI:")
    print()
    print("  1. Find a technical article you want to understand deeply")
    print("  2. Ask an AI to help you interrogate it (not summarize it)")
    print("  3. Test at least one specific claim from the article")
    print("  4. Create 3 flashcards from what you learned")
    print("  5. Log this as a side quest (see exercise 10-solveit.py)")
    print()


if __name__ == "__main__":
    main()
