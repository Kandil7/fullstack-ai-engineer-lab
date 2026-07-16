# Glossary: Natural Language (NLP)

> Terms for fast.ai lesson 4 — fine-tuning pretrained transformers with 🤗
> Transformers. Each entry includes a definition, example, and related terms.

---

## Quick Reference Table

| Term | One-Line Definition | See Also |
|------|---------------------|----------|
| Tokenization | Splitting text into tokens the model can read | Subword, Vocabulary |
| Subword / BPE | Encoding words as reusable frequent sub-pieces | WordPiece, Token |
| WordPiece | BERT-family subword scheme (`##` continuation) | Subword / BPE |
| Numericalization | Mapping tokens to integer IDs | Vocabulary, Tokenization |
| Vocabulary | Fixed token↔id table used by a model | Tokenization, Special token |
| Special token | Structural marker like `[CLS]`, `[SEP]`, `[PAD]` | Vocabulary |
| Pretrained LM | Model already trained on a huge text corpus | Fine-tuning, Transfer learning |
| Fine-tuning | Adapting a pretrained model to your task | Transfer learning |
| Transfer learning (text) | Reusing learned language representations | Pretrained LM |
| AutoTokenizer | Loads the tokenizer matching a pretrained model | Tokenization |
| AutoModelForSequenceClassification | Backbone + classification/regression head | Trainer |
| Trainer | 🤗 training/eval loop | TrainingArguments |
| Epoch | One full pass over the training data | Overfitting |
| Validation set | Held-out data to tune choices | Test set |
| Test set | Data used once for an honest final estimate | Validation set |
| Metric | The number you optimize toward | Pearson correlation |
| Pearson correlation | Linear-correlation score of preds vs labels | Metric |
| Overfitting / Underfitting | Memorizing noise vs failing to learn | Epoch, Validation set |

---

## Detailed Definitions

### Tokenization

**Definition:** The process of splitting raw text into **tokens** — the atomic
units a transformer consumes. Modern models tokenize into *subwords* so that any
input string, including unseen words, can be represented.

## Example
```python
from transformers import AutoTokenizer
tokz = AutoTokenizer.from_pretrained("microsoft/deberta-v3-small")
tokz.tokenize("unbelievable")   # ['▁un', 'bel', 'ievable'] — subword pieces
```

**Related Terms:**
- Subword / BPE — the encoding scheme tokenization uses
- Numericalization — the step that follows, turning tokens into IDs
- Vocabulary — the fixed set of tokens available

---

### Subword / BPE

**Definition:** **Byte-Pair Encoding** builds a vocabulary of the most frequent
character sequences, merging pairs iteratively. Common words stay whole; rare
words split into known pieces. This guarantees no word is ever fully unknown.

## Example
```python
# 'tokenization' may split; 'the' stays a single token
tokz.tokenize("tokenization")   # ['▁token', 'ization']
tokz.tokenize("the")            # ['▁the']
```

**Related Terms:**
- WordPiece — a closely related subword scheme
- Vocabulary — the learned set of subwords
- Tokenization — the operation that applies BPE

---

### WordPiece

**Definition:** The subword algorithm used by BERT-family models. Like BPE, it
uses learned frequent pieces, marking word-continuation pieces with a `##`
prefix so the original word can be reconstructed.

## Example
```python
# WordPiece output style (BERT tokenizer):
# 'playing' -> ['play', '##ing']
bert = AutoTokenizer.from_pretrained("bert-base-uncased")
bert.tokenize("playing")   # ['playing'] or ['play', '##ing'] depending on vocab
```

**Related Terms:**
- Subword / BPE — the sibling technique
- Vocabulary — where the pieces live

---

### Numericalization

**Definition:** Converting tokens into the integer **IDs** the model expects, by
looking each token up in the vocabulary. The output is `input_ids` plus an
`attention_mask` marking real vs padding positions.

## Example
```python
enc = tokz("abatement of pollution")
enc["input_ids"]        # [1, 54453, 1104, 15877, 2]  <- integers
enc["attention_mask"]   # [1, 1, 1, 1, 1]             <- 1 = real, 0 = pad
```

**Related Terms:**
- Tokenization — the step before it
- Vocabulary — the lookup table it uses

---

### Vocabulary

**Definition:** The fixed, ordered table mapping every known token to a unique
integer ID (and back). Its size (`vocab_size`) sets the model's input embedding
dimension. A pretrained model and its tokenizer must share the same vocabulary.

## Example
```python
tokz.vocab_size                       # e.g. 128100
tokz.convert_tokens_to_ids("▁the")    # 262
tokz.convert_ids_to_tokens(262)       # '▁the'
```

**Related Terms:**
- Numericalization — uses the vocabulary
- Special token — reserved vocabulary entries

---

### Special Token

**Definition:** Reserved vocabulary entries that encode structure rather than
content: `[CLS]` (sequence/classification slot), `[SEP]` (separator), `[PAD]`
(padding), `[UNK]` (unknown), `[MASK]` (masked position).

## Example
```python
tokz.all_special_tokens   # ['[CLS]', '[SEP]', '[PAD]', '[UNK]', '[MASK]']
tokz.cls_token_id         # id used at the start of every sequence
```

**Related Terms:**
- Vocabulary — where special tokens are registered
- Tokenization — inserts them automatically

---

### Pretrained Language Model

**Definition:** A network already trained on a massive corpus (predicting
masked or next tokens) so it encodes grammar, facts, and word relationships.
It is the starting point you fine-tune, never a blank slate.

## Example
```python
from transformers import AutoModelForSequenceClassification
# weights arrive already knowing language:
model = AutoModelForSequenceClassification.from_pretrained(
    "microsoft/deberta-v3-small", num_labels=1)
```

**Related Terms:**
- Fine-tuning — how you adapt it
- Transfer learning (text) — the principle behind it

---

### Fine-Tuning

**Definition:** Continuing training of a pretrained model on your (usually
small) labeled dataset, gently updating its weights so it specializes to your
task. Requires far less data, time, and compute than training from scratch.

## Example
```python
trainer = Trainer(model, args, train_dataset=dds["train"],
                  eval_dataset=dds["test"], tokenizer=tokz)
trainer.train()   # fine-tunes the pretrained weights
```

**Related Terms:**
- Pretrained LM — the input to fine-tuning
- Epoch — a unit of fine-tuning
- Overfitting — the risk if you fine-tune too long

---

### Transfer Learning (Text)

**Definition:** Reusing representations learned on one (large, general) task to
boost a different (small, specific) task. For text, a model pretrained on the
web transfers its language understanding to classification, regression, or QA.

## Example
```python
# The backbone already understands English; we only teach it the patent task.
# That is why 4 epochs on a few thousand rows can beat a from-scratch model.
```

**Related Terms:**
- Pretrained LM — the source of transferred knowledge
- Fine-tuning — the mechanism of transfer

---

### AutoTokenizer

**Definition:** A factory class that loads the exact tokenizer paired with a
pretrained checkpoint via `from_pretrained`, guaranteeing the same vocabulary
and preprocessing the model was trained with.

## Example
```python
from transformers import AutoTokenizer
tokz = AutoTokenizer.from_pretrained("microsoft/deberta-v3-small")
row = tokz("TEXT1: A47; TEXT2: abatement")   # ready-to-feed input_ids
```

**Related Terms:**
- Tokenization / Numericalization — what it performs
- AutoModelForSequenceClassification — the paired model loader

---

### AutoModelForSequenceClassification

**Definition:** A factory that loads a pretrained backbone and attaches a
sequence-level head. With `num_labels=1` it becomes a regression head predicting
a single continuous value; with `num_labels=k` it predicts class logits.

## Example
```python
from transformers import AutoModelForSequenceClassification
model = AutoModelForSequenceClassification.from_pretrained(
    "microsoft/deberta-v3-small", num_labels=1)   # regression: one output
```

**Related Terms:**
- Pretrained LM — the backbone it loads
- Trainer — what drives it during training

---

### Trainer

**Definition:** The 🤗 Transformers high-level training/evaluation loop. Given a
model, `TrainingArguments`, datasets, tokenizer, and a `compute_metrics`
function, it handles batching, optimization, mixed precision, and evaluation.

## Example
```python
from transformers import Trainer
trainer = Trainer(model, args, train_dataset=dds["train"],
                  eval_dataset=dds["test"], tokenizer=tokz,
                  compute_metrics=corr_metric)
trainer.train()
```

**Related Terms:**
- TrainingArguments — its configuration object
- Metric — computed via `compute_metrics`
- Epoch — how long it trains

---

### Epoch

**Definition:** One complete pass over the entire training dataset. Fine-tuning
transformers typically needs only a few epochs (3-4); too many cause
overfitting.

## Example
```python
from transformers import TrainingArguments
args = TrainingArguments("out", num_train_epochs=4,
                         evaluation_strategy="epoch")  # evaluate each epoch
```

**Related Terms:**
- Overfitting / Underfitting — diagnosed across epochs
- Trainer — runs the epochs

---

### Validation Set

**Definition:** Data held out of training and used *during development* to tune
choices (learning rate, epochs, model). Because you make decisions from it, you
can still overfit to it — so it must faithfully mirror the test distribution.

## Example
```python
dds = tok_ds.train_test_split(test_size=0.25, seed=42)
# dds["test"] here acts as the validation set the Trainer evaluates on
```

**Related Terms:**
- Test set — the untouched final judge
- Overfitting — what a bad validation set hides

---

### Test Set

**Definition:** Data used exactly once, at the very end, to estimate true
generalization. Nobody tunes on it. In a Kaggle competition, the private
leaderboard is the real test set.

## Example
```python
# You never call .train() or pick hyperparameters using the test set.
# On Kaggle: public LB ~ validation, private LB = test (revealed at the end).
```

**Related Terms:**
- Validation set — used repeatedly during development
- Metric — computed on the test set for the final number

---

### Metric

**Definition:** The quantitative measure of model quality you optimize and
report. It must reflect the real objective; the wrong metric can make a useless
model look excellent (e.g. accuracy on imbalanced data).

## Example
```python
def compute_metrics(eval_pred):
    preds, labels = eval_pred
    import numpy as np
    return {"pearson": np.corrcoef(preds.flatten(), labels)[0][1]}
```

**Related Terms:**
- Pearson correlation — the metric for this task
- Validation set / Test set — where metrics are computed

---

### Pearson Correlation

**Definition:** A measure (`r`, from -1 to 1) of how linearly predictions move
with the true labels, independent of scale. The Patent competition is scored by
Pearson `r`, so it is the metric to optimize here.

## Example
```python
import numpy as np
r = np.corrcoef(preds.flatten(), labels)[0][1]   # 1.0 = perfect, 0 = none
```

**Related Terms:**
- Metric — Pearson is the chosen metric
- Test set — evaluated there for the final score

---

### Overfitting / Underfitting

**Definition:** **Overfitting** — training error keeps falling while validation
error rises; the model memorizes noise. **Underfitting** — both errors stay
high; the model is too weak or undertrained. The gap between the two curves is
the diagnostic.

## Example
```python
# Symptom of overfitting across epochs:
# epoch 1: train_loss 0.20  val_pearson 0.80
# epoch 8: train_loss 0.01  val_pearson 0.71  <- val getting worse -> STOP
```

**Related Terms:**
- Epoch — overfitting grows with epochs
- Validation set — where you detect it

---

## Summary

Lesson 4 turns text into something a network can learn from — **tokenize**,
**numericalize**, feed it to a **pretrained** transformer, and **fine-tune** via
the `Trainer`. The techniques are a few lines of code; the judgment is not.
Choosing the right **metric** and, above all, building a **validation set** that
mirrors the **test set** is what separates a real result from a self-deception.

**Next:** See Lecture 05 (From-Scratch Model) to rebuild the neural network
underneath these abstractions — tensors, matrix multiply, ReLU, and layers.
