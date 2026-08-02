"""
GenAI - 21: Fine-Tuning
=======================
Topics: when fine-tuning beats prompting (and when it does not); LoRA/
QLoRA; dataset prep (JSONL); SFT vs DPO; evaluation; serving adapters.

Why this matters for AI/backend engineering:
    Fine-tuning is a tool, not a trophy. It wins when you need a model
    to internalize a style, a format, or domain knowledge; it loses on
    facts that change (use RAG) and on tasks prompting already solves
    (use prompting). The skill is the decision PLUS the dataset.

Run:      python 21-fine-tuning.py
Verify:   python 21-fine-tuning.py --verify
Reference: https://huggingface.co/docs/peft/en/index
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass


# ============================================================
# 1. When Fine-Tuning Wins (and When It Doesn't)
# ============================================================

def ft_decision(task_kind: str, facts_change: bool,
                style_required: bool) -> str:
    if facts_change:
        return "RAG: facts change; fine-tuning bakes in stale knowledge"
    if style_required and task_kind in ("format", "style", "domain_language"):
        return "FINE-TUNE: teach the model the format/style once"
    if task_kind == "simple_instruction":
        return "PROMPT: prompting already solves this - don't over-engineer"
    return "EVALUATE: measure whether fine-tuning lifts the score"


# Example 1: the decision matrix
cases = [
    ("format", False, True),   # JSON extraction -> fine-tune
    ("qa", True, False),       # changing facts -> RAG
    ("simple_instruction", False, False),  # trivial -> prompt
]
print("Example 1: fine-tune vs RAG vs prompt")
for kind, facts, style in cases:
    print(f"  {kind:<20} -> {ft_decision(kind, facts, style)}")
assert ft_decision("format", False, True).startswith("FINE-TUNE")
assert ft_decision("qa", True, False).startswith("RAG")
assert ft_decision("simple_instruction", False, False).startswith("PROMPT")

# ============================================================
# 2. Dataset Prep - JSONL
# ============================================================
# The SFT format: one {"messages": [...]} per line. Quality beats
# quantity: 1000 clean, deduplicated examples beat 100k scraped ones.

@dataclass
class SFTExample:
    system: str
    user: str
    assistant: str

    def to_jsonl(self) -> str:
        return json.dumps({
            "messages": [
                {"role": "system", "content": self.system},
                {"role": "user", "content": self.user},
                {"role": "assistant", "content": self.assistant},
            ]
        })


# Example 2: build a JSONL dataset
examples = [
    SFTExample("You convert text to JSON.", "Order for 3 pens", 
               '{"items": [{"name": "pen", "qty": 3}]}'),
    SFTExample("You convert text to JSON.", "One laptop", 
               '{"items": [{"name": "laptop", "qty": 1}]}'),
]
lines = [e.to_jsonl() for e in examples]
print("Example 2: SFT dataset (JSONL)")
print(f"  {lines[0]}")
parsed = json.loads(lines[0])
assert parsed["messages"][2]["role"] == "assistant"

# ============================================================
# 3. Dataset Hygiene
# ============================================================
# Dedupe, check label balance, and split train/val - the same hygiene
# as classical ML, because the same failure modes apply.

def dedupe(examples: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for e in examples:
        key = json.dumps(e, sort_keys=True)
        if key not in seen:
            seen.add(key)
            out.append(e)
    return out


def train_val_split(examples: list[dict], val_frac: float = 0.1) -> tuple[list, list]:
    n_val = max(1, int(len(examples) * val_frac))
    return examples[n_val:], examples[:n_val]


# Example 3: hygiene
raw = [{"u": "a", "a": "1"}] * 5 + [{"u": "b", "a": "2"}]
unique = dedupe(raw)
print("\nExample 3: dataset hygiene")
print(f"  {len(raw)} rows -> {len(unique)} unique")
assert len(unique) == 2

# ============================================================
# 4. LoRA / QLoRA
# ============================================================
# Full fine-tuning trains every weight; LoRA trains small low-rank
# adapters (1-2% of params); QLoRA quantizes the base model and trains
# adapters on top - fitting on consumer GPUs.

def lora_trainable_params(total_params: int, rank: int,
                          adapter_layers: int, hidden: int) -> float:
    """Trainable parameters for LoRA adapters (2 matrices per layer)."""
    return adapter_layers * 2 * rank * hidden


def trainable_fraction(total: int, trainable: float) -> float:
    return trainable / total


# Example 4: LoRA economics
total = 7_000_000_000  # 7B model
trainable = lora_trainable_params(total, rank=16, adapter_layers=32, hidden=4096)
frac = trainable_fraction(total, trainable)
print("\nExample 4: LoRA")
print(f"  trainable: {trainable/1e6:.1f}M of {total/1e9:.0f}B params "
      f"({frac:.2%})")
assert frac < 0.01, "LoRA trains under 1% of parameters"

# ============================================================
# 5. SFT vs DPO
# ============================================================
# SFT: imitate good answers. DPO: learn PREFERENCE (which answer is
# better) - needs pairs, aligns closer to human judgment.

def sft_vs_dpo(data_type: str) -> str:
    if data_type == "pairs_preference":
        return "DPO: preference pairs directly optimize desirability"
    if data_type == "demonstrations":
        return "SFT: supervised imitation of good examples"
    return "SFT first, then DPO on the hard cases"


# Example 5: method choice
print("\nExample 5: SFT vs DPO")
print(f"  {sft_vs_dpo('demonstrations')}")
print(f"  {sft_vs_dpo('pairs_preference')}")
assert sft_vs_dpo("pairs_preference").startswith("DPO")

# ============================================================
# Production Pattern
# ============================================================
# After training: evaluate the adapter against the base model on the
# SAME eval set, and only ship the adapter if it measures better.

def decide_to_ship(base_score: float, ft_score: float,
                   cost_multiple: float, budget: float) -> tuple[bool, str]:
    if ft_score <= base_score:
        return False, "no quality gain - keep the base model"
    if cost_multiple > budget:
        return False, f"cost {cost_multiple:.1f}x exceeds budget {budget:.1f}x"
    return True, f"ship adapter: {ft_score:.3f} vs base {base_score:.3f}"


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: fine-tuning on facts that change (stale knowledge, use RAG)
# MISTAKE: scraped, un-deduplicated datasets (model learns the noise)
# MISTAKE: no eval vs base - shipping a more expensive, no-better model
# MISTAKE: ignoring LoRA - full FT is usually unnecessary


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    e = SFTExample("s", "u", "a")
    j = json.loads(e.to_jsonl())
    assert [m["role"] for m in j["messages"]] == ["system", "user", "assistant"]

    raw = [{"x": 1}] * 3 + [{"x": 2}]
    assert len(dedupe(raw)) == 2
    tr, va = train_val_split([{"i": i} for i in range(10)], 0.2)
    assert len(tr) == 8 and len(va) == 2

    t = lora_trainable_params(1e9, 8, 24, 1024)
    assert t == 24 * 2 * 8 * 1024, "LoRA param math"

    assert sft_vs_dpo("demonstrations").startswith("SFT")
    assert sft_vs_dpo("pairs_preference").startswith("DPO")

    ok, msg = decide_to_ship(0.8, 0.8, 1.5, 2.0)
    assert not ok and "no quality gain" in msg
    ok2, _ = decide_to_ship(0.8, 0.95, 1.2, 2.0)
    assert ok2, "better + affordable ships"
    ok3, msg3 = decide_to_ship(0.8, 0.9, 5.0, 2.0)
    assert not ok3 and "budget" in msg3, "cost over budget blocks"
    print("[OK] 21-fine-tuning: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. RAG for facts, prompting for simple tasks, FT for style.")
        print("2. JSONL datasets, deduplicated and split.")
        print("3. LoRA trains <1%; ship only if it beats the base model.")
        _verify()
