# Lecture 04: Natural Language (NLP)

## Topic Overview

Text is the messiest, most abundant data on Earth — and for years it was the
hardest to model. fast.ai lesson 4 shows how that changed. Instead of building
a language model from scratch, you take a **pretrained transformer** (a network
that already "read" a huge corpus) and **fine-tune** it on your task in minutes.

This lesson deliberately steps *outside* the fastai text API and uses Hugging
Face **🤗 Transformers** directly, on a real Kaggle competition: **U.S. Patent
Phrase-to-Phrase Matching**. The goal is to score how semantically similar two
phrases are, given a technical context. We reframe that fuzzy "similarity"
question into a single input string and a numeric prediction the model can
learn — then wrap it in the `Trainer` loop.

The deepest idea in the lesson isn't the model at all. It is the
**validation set**: how you split data decides whether your reported accuracy
means anything. A great model on a broken validation set is worthless.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Lectures 01-03

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** why fine-tuning a pretrained language model beats training text
   models from scratch (transfer learning for text).
2. **Describe** tokenization — how raw text becomes subword tokens — and why
   subword schemes (BPE, WordPiece) handle any word.
3. **Perform** numericalization: mapping tokens to integer IDs with a
   `AutoTokenizer` and a fixed vocabulary.
4. **Reframe** a similarity problem as a single-input sequence-scoring task the
   model can learn.
5. **Build** a training pipeline with 🤗 `datasets`, `Dataset.from_pandas`,
   `.map`, `AutoModelForSequenceClassification`, `TrainingArguments`, and
   `Trainer`.
6. **Choose** a correct metric (Pearson correlation here) and recognize the
   danger of optimizing the wrong one.
7. **Construct** an honest train/validation/test split and explain how a bad
   validation set silently ruins a project.
8. **Diagnose** underfitting vs overfitting using the U-shaped error curve, and
   tune learning rate and epochs accordingly.

---

## Key Concepts

### 1. Transfer Learning for Text: Don't Start From Zero

A **pretrained language model** has already been trained on billions of words to
predict masked or next tokens. In doing so it learns grammar, facts, and a rich
sense of how words relate. **Fine-tuning** nudges those existing weights toward
your specific task using a small labeled dataset. This is **transfer learning**:
reuse learned representations instead of paying to learn language again.

```
FROM SCRATCH                       FINE-TUNING (transfer learning)
─────────────                      ───────────────────────────────
random weights                     pretrained weights (knows language)
        │                                    │
   millions of                          hundreds/thousands of
   labeled examples                     labeled examples
        │                                    │
   days on many GPUs                    minutes on one GPU
        ▼                                    ▼
   mediocre model                       strong model
```

The same principle powered the image classifier in Lecture 01 (`fine_tune`).
Here the pretrained backbone is a transformer such as `microsoft/deberta-v3-small`.

### 2. Tokenization: Splitting Text Into Tokens

Models cannot read characters or whole words directly; they read **tokens**.
**Tokenization** splits text into these units. Modern transformers use
**subword** tokenization so that any word — even one never seen in training —
can be represented as a sequence of known pieces.

- **BPE (Byte-Pair Encoding)** and **WordPiece** learn a fixed set of frequent
  subwords. Common words become one token; rare words split into fragments.
- **Special tokens** mark structure: `[CLS]` (start / classification slot),
  `[SEP]` (separator), `[PAD]` (padding), `[UNK]` (unknown).

```python
from transformers import AutoTokenizer

tokz = AutoTokenizer.from_pretrained("microsoft/deberta-v3-small")
tokz.tokenize("A platypus is an unusual mammal")
# ['▁A', '▁platypus', '▁is', '▁an', '▁unusual', '▁mammal']
# note: 'platypus' stayed whole; a rarer word would be split into subwords
```

### 3. Numericalization: Tokens to IDs

Once text is tokens, **numericalization** maps each token to an integer via the
tokenizer's **vocabulary** (a fixed token↔id table). The model only ever sees
these IDs plus an **attention mask** telling it which positions are real vs
padding.

```python
row = tokz("TEXT1: abatement; TEXT2: eliminating process")
row["input_ids"][:8]     # [1, 54453, 435, ...]  integer ids
row["attention_mask"][:8]  # [1, 1, 1, ...]        1 = real token, 0 = pad
tokz.vocab_size            # e.g. 128100 — size of the vocabulary
```

Tokenization + numericalization together are the *only* preprocessing text needs
for a transformer. There is no manual feature engineering.

### 4. Framing the Problem: Similarity as a Single Score

The Patent dataset gives an `anchor` phrase, a `target` phrase, and a technical
`context` code (e.g. section "A47"). We want a similarity score from 0 to 1.
The trick is to **serialize** all inputs into one string, then predict a number:

```python
def make_input(df):
    # one string carries anchor, target, and context
    return "TEXT1: " + df.context + "; TEXT2: " + df.target + "; ANC1: " + df.anchor

# label 'score' in {0.0, 0.25, 0.5, 0.75, 1.0} — predicted as a regression value
```

By concatenating with cheap separator words, the transformer can attend across
all three fields at once. We treat the score as a **regression** target (a
single continuous output), which in Transformers is just
`AutoModelForSequenceClassification` with `num_labels=1`.

### 5. The 🤗 datasets + Trainer Pipeline

Hugging Face gives a clean, batteries-included loop:

```python
from datasets import Dataset

ds = Dataset.from_pandas(df)            # pandas -> HF Dataset
def tok_func(x): return tokz(x["input"])
tok_ds = ds.map(tok_func, batched=True) # tokenize the whole dataset lazily
tok_ds = tok_ds.rename_columns({"score": "labels"})  # Trainer expects 'labels'
```

Then model, arguments, and trainer:

```python
from transformers import (AutoModelForSequenceClassification,
                          TrainingArguments, Trainer)

model = AutoModelForSequenceClassification.from_pretrained(model_nm, num_labels=1)
args  = TrainingArguments("out", learning_rate=8e-5, per_device_train_batch_size=64,
                          num_train_epochs=4, evaluation_strategy="epoch",
                          fp16=True, report_to="none")
trainer = Trainer(model, args, train_dataset=dds["train"],
                  eval_dataset=dds["test"], tokenizer=tokz,
                  compute_metrics=corr_metric)
trainer.train()
```

### 6. Metrics: Pearson Correlation, and the Danger of the Wrong One

The competition is scored by **Pearson correlation** (`r`) between predictions
and labels — how well predictions move *together* with truth, ignoring scale.
The **metric** you optimize defines success. Pick the wrong one and you can ship
a model that looks great and is useless.

```python
import numpy as np
def corr(preds, labels): return np.corrcoef(preds.flatten(), labels)[0][1]
def corr_metric(eval_pred):
    preds, labels = eval_pred
    return {"pearson": corr(preds, labels)}
```

Classic trap: optimizing **accuracy** on an imbalanced dataset. A model that
always predicts the majority class can be "95% accurate" and worthless. Always
choose a metric that reflects the real objective.

### 7. Validation and Test Sets: The Lesson That Matters Most

fast.ai hammers this point: **a bad validation set makes every number a lie.**

```
┌──────────────────────────────────────────────────────────┐
│  TRAIN        │  VALIDATION      │  TEST                   │
│  fit weights  │  tune choices    │  final honest estimate  │
│  (model sees) │  (you see)       │  (nobody tunes on it)   │
└──────────────────────────────────────────────────────────┘
        Kaggle: public LB ≈ validation, private LB ≈ test
```

- The **validation set** measures generalization *while you develop* — you use
  it to choose learning rate, epochs, model. Because you make choices based on
  it, you can still overfit to it.
- The **test set** is touched once, at the end. On Kaggle the private
  leaderboard is your true test set.
- A random split is **wrong** when data is grouped or temporal. If the same
  `anchor` appears in train and validation, the model memorizes it and your
  validation score is inflated. Use **grouped** splits (keep an anchor entirely
  in one split) or **temporal** splits (train on the past, validate on the
  future) so validation mirrors real deployment.

### 8. Underfitting vs Overfitting: The U-Shaped Curve

```
error │\                              /  ← overfitting
      │ \                            /     (val error rises,
      │  \                          /       train error tiny)
      │   \____________________ __ /
      │        \______________/    ← sweet spot
      │  underfitting (both high)
      └────────────────────────────── model capacity / epochs
```

- **Underfitting:** training and validation error both high — model too weak or
  trained too little. Fix: more capacity, more epochs, higher learning rate.
- **Overfitting:** training error keeps dropping but **validation error rises** —
  the model memorizes noise. Fix: fewer epochs, more data, regularization.
- For fine-tuned transformers, overfitting arrives fast: a few epochs
  (often 3-4) and a small learning rate (2e-5 to 1e-4) are usually enough.

---

## Code Examples

### Example 1: End-to-End Fine-Tune on Patent Phrase Matching

```python
"""
Fine-tune DeBERTa on U.S. Patent Phrase-to-Phrase Matching.
Mirrors fast.ai lesson 4 (Hugging Face Transformers, not fastai.text).
"""
import numpy as np
import pandas as pd
from datasets import Dataset
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer)

MODEL_NM = "microsoft/deberta-v3-small"

# 1. Load and FRAME: fold anchor/target/context into one input string
df = pd.read_csv("train.csv")
df["input"] = ("TEXT1: " + df.context + "; TEXT2: "
               + df.target + "; ANC1: " + df.anchor)

# 2. Tokenize + numericalize via the pretrained tokenizer
tokz = AutoTokenizer.from_pretrained(MODEL_NM)
def tok_func(x):
    return tokz(x["input"])                     # -> input_ids + attention_mask

ds = Dataset.from_pandas(df).rename_column("score", "labels")
tok_ds = ds.map(tok_func, batched=True)

# 3. VALIDATION DISCIPLINE: split so no anchor leaks across the boundary
#    (grouped split — here shown simply; prefer GroupShuffleSplit in practice)
dds = tok_ds.train_test_split(test_size=0.25, seed=42)

# 4. Model = regression head (num_labels=1) on the pretrained backbone
def corr(preds, labels):
    return {"pearson": np.corrcoef(preds.flatten(), labels)[0][1]}
def compute_metrics(eval_pred):
    return corr(eval_pred.predictions, eval_pred.label_ids)

args = TrainingArguments(
    output_dir="patent-out",
    learning_rate=8e-5,          # small LR for fine-tuning
    per_device_train_batch_size=64,
    per_device_eval_batch_size=128,
    num_train_epochs=4,          # few epochs — overfitting comes fast
    weight_decay=0.01,
    evaluation_strategy="epoch",
    fp16=True,                   # mixed precision on GPU
    report_to="none",
)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NM, num_labels=1)
trainer = Trainer(model, args, train_dataset=dds["train"],
                  eval_dataset=dds["test"], tokenizer=tokz,
                  compute_metrics=compute_metrics)
trainer.train()   # watch eval pearson each epoch — stop if it starts falling
```

### Example 2: Inspecting Tokenization Before You Trust It

```python
"""
Always look at what the tokenizer does BEFORE training.
Silent tokenization surprises are a common source of bad models.
"""
from transformers import AutoTokenizer

tokz = AutoTokenizer.from_pretrained("microsoft/deberta-v3-small")

sample = "TEXT1: A47; TEXT2: abatement of pollution; ANC1: abatement"
enc = tokz(sample)

print("tokens :", tokz.convert_ids_to_tokens(enc["input_ids"])[:12])
print("ids    :", enc["input_ids"][:12])
print("special:", tokz.all_special_tokens)   # ['[CLS]', '[SEP]', '[PAD]', ...]
print("length :", len(enc["input_ids"]), "tokens")

# Decode round-trips ids back to text — confirms nothing was mangled
print("decoded:", tokz.decode(enc["input_ids"]))
```

### Example 3: A Grouped Validation Split That Doesn't Leak

```python
"""
Random splits leak grouped data. Keep every 'anchor' fully in one side so
the validation score reflects unseen anchors — like the real test set.
"""
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

df = pd.read_csv("train.csv")
splitter = GroupShuffleSplit(test_size=0.25, n_splits=1, random_state=42)
train_idx, valid_idx = next(splitter.split(df, groups=df["anchor"]))

train_df = df.iloc[train_idx]
valid_df = df.iloc[valid_idx]

# Prove there is no leakage: shared anchors should be empty
overlap = set(train_df.anchor) & set(valid_df.anchor)
assert not overlap, f"Leak! {len(overlap)} anchors in both splits"
print(f"Clean split: {len(train_df)} train / {len(valid_df)} valid rows")
```

---

## Common Mistakes to Avoid

### Mistake 1: Random Split on Grouped Data

```python
# BAD: same anchor lands in both train and validation -> inflated score
train, valid = train_test_split(df, test_size=0.25)

# GOOD: keep each group (anchor) entirely on one side
from sklearn.model_selection import GroupShuffleSplit
gss = GroupShuffleSplit(test_size=0.25, random_state=42)
tr, va = next(gss.split(df, groups=df.anchor))
```

### Mistake 2: Optimizing the Wrong Metric

```python
# BAD: accuracy on a skewed target hides a useless model
metric = {"accuracy": (preds.round() == labels).mean()}

# GOOD: use the metric the task is actually scored by
metric = {"pearson": np.corrcoef(preds.flatten(), labels)[0][1]}
```

### Mistake 3: Training Too Many Epochs

```python
# BAD: 20 epochs -> train loss ~0, validation error climbing (overfit)
args = TrainingArguments("out", num_train_epochs=20)

# GOOD: few epochs, watch validation each epoch, stop when it stops improving
args = TrainingArguments("out", num_train_epochs=4, evaluation_strategy="epoch")
```

---

## Best Practices

1. **Fine-tune, don't train from scratch** — start from a pretrained backbone
   suited to your domain.
2. **Inspect tokenization first** — decode a few examples before you train.
3. **Frame the task explicitly** — serialize multi-field inputs into one clear
   string with separators.
4. **Rename your label column to `labels`** — the `Trainer` expects it.
5. **Build the validation set before the model** — it is the most important
   design decision.
6. **Match the split to the data** — grouped or temporal, never random when
   structure exists.
7. **Optimize the real metric** — mirror the competition/business objective.
8. **Use few epochs and a small learning rate** for transformer fine-tuning
   (start ~2e-5 to 8e-5, 3-4 epochs).
9. **Watch train vs validation error together** — diverging curves mean overfit.
10. **Treat the test set (private LB) as sacred** — look at it once, at the end.

---

## Practice Exercises

1. Load the Patent `train.csv`, build the `input` string three different ways
   (reorder fields, change separators) and compare validation Pearson. Which
   framing helps the model most?
2. Print the tokenization of five rows. Find a token that was split into
   subwords and explain why BPE/WordPiece did that.
3. Replace the random `train_test_split` with a `GroupShuffleSplit` on `anchor`.
   Report how much the validation Pearson changes and explain the direction.
4. Train for 1, 3, 6, and 12 epochs. Plot train vs validation error and mark the
   overfitting point on the U-shaped curve.
5. Swap `compute_metrics` to report accuracy instead of Pearson. Show a case
   where accuracy looks fine but Pearson reveals the model is weak.

---

## Summary

| Concept | Description |
|---------|-------------|
| Transfer learning (text) | Reuse a pretrained language model instead of training from scratch |
| Tokenization | Split text into subword tokens (BPE / WordPiece) |
| Numericalization | Map tokens to integer IDs via the tokenizer's vocabulary |
| AutoTokenizer | Loads the matching tokenizer for a pretrained model |
| AutoModelForSequenceClassification | Adds a classification/regression head on a backbone |
| Trainer / TrainingArguments | 🤗 training loop + its configuration |
| Metric | The number you optimize — must reflect the real goal (Pearson here) |
| Validation set | Held-out data to tune choices; a bad one ruins everything |
| Test set | Touched once for an honest final estimate (Kaggle private LB) |
| Overfitting | Train error falls while validation error rises |

**Key Takeaways:**
1. Fine-tuning a pretrained transformer is fast, cheap, and strong.
2. Text needs only tokenization + numericalization — no manual features.
3. Frame fuzzy problems into a single input string and a numeric target.
4. The `datasets` + `Trainer` pipeline is a few lines of glue.
5. The metric defines success — choose it deliberately.
6. Your validation set is the project. Build it to mirror the test set, or every
   number you report is a lie.

**Next lecture:** In **Lecture 05: From-Scratch Model**, we drop the library
abstractions and rebuild a neural net from tensors up — matrix multiply, ReLU,
layers, and the forward pass — to see exactly what fastai and Transformers do
for you.
