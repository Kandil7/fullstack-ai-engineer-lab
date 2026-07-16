"""
=============================================================
EXERCISE 04: Natural Language (NLP)
=============================================================
Topic: Fine-tuning a pretrained transformer with Hugging Face
       (fast.ai lesson 4 — U.S. Patent Phrase-to-Phrase Matching)

Goal:
    Build the full text pipeline by hand: FRAME the similarity task
    into one input string, TOKENIZE + NUMERICALIZE it, wrap it in a
    Hugging Face `datasets` Dataset, and fine-tune an
    AutoModelForSequenceClassification with the `Trainer` — while
    building an honest validation split and scoring with Pearson r.

Prerequisites:
    Python 3.10+
    pip install transformers datasets scikit-learn pandas numpy

GPU note:
    Fine-tuning is far faster on a GPU. fast.ai recommends the FREE
    Kaggle / Paperspace GPUs. The tokenization/framing sections run
    fine on CPU; guard the actual `Trainer.train()` behind a check.
=============================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ============================================================
# SECTION 1: Load and FRAME the problem as a single input string
# ============================================================
def build_dataframe() -> pd.DataFrame:
    """Return a tiny stand-in for the Patent train.csv and frame inputs."""
    df = pd.DataFrame(
        {
            "anchor": ["abatement", "abatement", "opc drum", "adjust gas flow"],
            "target": ["eliminating process", "forest region", "opc", "gas flow"],
            "context": ["A47", "A47", "G02", "F23"],
            "score": [0.5, 0.0, 0.75, 1.0],
        }
    )
    # EXERCISE: fold context + target + anchor into ONE "input" column.
    # Use clear separators, e.g. "TEXT1: <context>; TEXT2: <target>; ANC1: <anchor>"
    # df["input"] = ...
    return df


# ============================================================
# SECTION 2: Tokenization + Numericalization
# ============================================================
def tokenize_dataset(df: pd.DataFrame, model_nm: str):
    """Turn a framed DataFrame into a tokenized HF Dataset."""
    from datasets import Dataset
    from transformers import AutoTokenizer

    tokz = AutoTokenizer.from_pretrained(model_nm)

    def tok_func(batch: dict) -> dict:
        # EXERCISE: return tokz(batch["input"]) so each row gets
        # input_ids + attention_mask (numericalization happens here).
        raise NotImplementedError("Implement tok_func using the tokenizer")

    ds = Dataset.from_pandas(df).rename_column("score", "labels")
    tok_ds = ds.map(tok_func, batched=True)
    return tok_ds, tokz


def inspect_tokenization(model_nm: str) -> None:
    """Always LOOK at tokenization before trusting it."""
    from transformers import AutoTokenizer

    tokz = AutoTokenizer.from_pretrained(model_nm)
    sample = "TEXT1: A47; TEXT2: abatement of pollution; ANC1: abatement"
    enc = tokz(sample)
    print("  tokens :", tokz.convert_ids_to_tokens(enc["input_ids"])[:12])
    print("  ids    :", enc["input_ids"][:12])
    print("  special:", tokz.all_special_tokens)
    print("  vocab  :", tokz.vocab_size)


# ============================================================
# SECTION 3: Build an HONEST validation split (no leakage)
# ============================================================
def grouped_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split so each `anchor` stays entirely on one side (no leak)."""
    from sklearn.model_selection import GroupShuffleSplit

    # EXERCISE: use GroupShuffleSplit(test_size=0.25, random_state=42)
    # grouping on df["anchor"]; return (train_df, valid_df).
    # Then assert there is NO overlapping anchor between the two splits.
    raise NotImplementedError("Implement a grouped, leak-free split")


# ============================================================
# SECTION 4: Metric — Pearson correlation (the RIGHT metric)
# ============================================================
def pearson(preds: np.ndarray, labels: np.ndarray) -> float:
    """Pearson r between predictions and labels."""
    # EXERCISE: return np.corrcoef(preds.flatten(), labels)[0][1]
    raise NotImplementedError("Implement Pearson correlation")


def compute_metrics(eval_pred) -> dict[str, float]:
    """Trainer-compatible metric callback."""
    preds, labels = eval_pred
    return {"pearson": pearson(np.asarray(preds), np.asarray(labels))}


# ============================================================
# SECTION 5: Fine-tune with Trainer (GPU recommended)
# ============================================================
def fine_tune(tok_ds, tokz, model_nm: str):
    """Fine-tune a regression head on the pretrained backbone."""
    from transformers import (
        AutoModelForSequenceClassification,
        Trainer,
        TrainingArguments,
    )

    dds = tok_ds.train_test_split(test_size=0.25, seed=42)

    # EXERCISE: load AutoModelForSequenceClassification with num_labels=1
    # (regression), then build TrainingArguments with a SMALL learning_rate
    # (~8e-5), FEW epochs (~4), evaluation_strategy="epoch", report_to="none".
    model = AutoModelForSequenceClassification.from_pretrained(
        model_nm, num_labels=1
    )
    args = TrainingArguments(
        output_dir="patent-out",
        learning_rate=8e-5,
        per_device_train_batch_size=16,
        num_train_epochs=4,
        evaluation_strategy="epoch",
        report_to="none",
    )
    trainer = Trainer(
        model,
        args,
        train_dataset=dds["train"],
        eval_dataset=dds["test"],
        tokenizer=tokz,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    return trainer


# ============================================================
# MAIN
# ============================================================
def main() -> None:
    model_nm = "microsoft/deberta-v3-small"

    print("=" * 55)
    print("SECTION 1: Frame the task")
    print("=" * 55)
    df = build_dataframe()
    print(df.head())

    print("\n" + "=" * 55)
    print("SECTION 2: Inspect tokenization (runs on CPU)")
    print("=" * 55)
    try:
        inspect_tokenization(model_nm)
    except Exception as exc:  # transformers / network may be unavailable
        print(f"  [skipped] {exc}")

    print("\n" + "=" * 55)
    print("SECTION 3: Grouped split (implement to remove NotImplementedError)")
    print("=" * 55)
    try:
        train_df, valid_df = grouped_split(df)
        print(f"  train={len(train_df)} valid={len(valid_df)} (leak-free)")
    except NotImplementedError as exc:
        print(f"  TODO: {exc}")

    print("\n" + "=" * 55)
    print("SECTION 5: Fine-tune (GPU recommended — enable when ready)")
    print("=" * 55)
    print("  Uncomment below after completing Sections 1-4.")
    # tok_ds, tokz = tokenize_dataset(df, model_nm)
    # fine_tune(tok_ds, tokz, model_nm)


if __name__ == "__main__":
    main()
