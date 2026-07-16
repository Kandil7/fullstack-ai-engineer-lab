# fast.ai Deep Learning — Lecture Series

## Welcome

This directory mirrors [fast.ai](https://course.fast.ai)'s **Practical Deep
Learning for Coders** (Part 1) in this lab's teaching format: every module
has a **lecture**, a **glossary**, a runnable **exercise**, and a **quiz**.

fast.ai teaches **top-down**: you train a working model in lesson 1, then
progressively unpack how it works until you can build the pieces from
scratch. These notes preserve that arc — start by *doing*, then understand.

---

## What this directory contains

- **9 lectures** (8 core lessons + a data-ethics bonus)
- **9 glossaries** with definitions, code, and cross-references
- Companion **exercises** (`../exercises/`) and **quizzes** (`../quizzes/`)
- An **nbdev demo package** (`../nbdev-demo/`) for notebook-driven development

---

## Lecture topics

### 1. [Getting Started](01-getting-started-lecture.md)
- The top-down method; why train first, theory later
- `vision_learner`, transfer learning, `fine_tune`
- Datasets, `DataLoaders`, and the first image classifier
- Interpreting results with a confusion matrix

**Glossary:** [01-getting-started-glossary.md](01-getting-started-glossary.md)

### 2. [Deployment & the fastai Stack](02-deployment-lecture.md)
- The `DataBlock` API and data cleaning
- Building a model you can ship
- Exporting a `Learner`, inference, and a Gradio app

**Glossary:** [02-deployment-glossary.md](02-deployment-glossary.md)

### 3. [Neural Net Foundations (SGD)](03-neural-net-foundations-lecture.md)
- Gradient descent from first principles
- The training loop: forward, loss, backward, step
- Tensors, `requires_grad`, and `nn.Parameter`

**Glossary:** [03-neural-net-foundations-glossary.md](03-neural-net-foundations-glossary.md)

### 4. [Natural Language (NLP)](04-nlp-lecture.md)
- Tokenization and numericalization
- Fine-tuning a pretrained transformer with 🤗 Transformers
- Classification metrics and validation discipline

**Glossary:** [04-nlp-glossary.md](04-nlp-glossary.md)

### 5. [From-Scratch Model](05-from-scratch-model-lecture.md)
- A neural net from tensors up: matrix mult, ReLU, layers
- Broadcasting, initialization, and the forward pass
- Reimplementing what fastai does for you

**Glossary:** [05-from-scratch-model-glossary.md](05-from-scratch-model-glossary.md)

### 6. [Random Forests & Tabular](06-random-forests-lecture.md)
- Decision trees, bagging, and random forests
- Feature importance and partial dependence
- When trees beat deep learning on tabular data

**Glossary:** [06-random-forests-glossary.md](06-random-forests-glossary.md)

### 7. [Collaborative Filtering](07-collaborative-filtering-lecture.md)
- Latent factors and embeddings
- Building a recommender with dot products + bias
- Embedding interpretation and the bootstrap problem

**Glossary:** [07-collaborative-filtering-glossary.md](07-collaborative-filtering-glossary.md)

### 8. [Convolutions (CNNs)](08-convolutions-lecture.md)
- What a convolution computes and why it works for images
- Kernels, stride, padding, channels, receptive field
- From a hand-built conv to a full CNN

**Glossary:** [08-convolutions-glossary.md](08-convolutions-glossary.md)

### 9. [Data Ethics (Bonus)](09-data-ethics-lecture.md)
- Feedback loops, bias, and disaggregated evaluation
- Recourse, accountability, and the human in the loop
- A practical checklist before you ship a model

**Glossary:** [09-data-ethics-glossary.md](09-data-ethics-glossary.md)

---

## Recommended learning order

```
┌─────────────────────────────────────────────────────────────────┐
│                    fast.ai LEARNING PATH                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  DO FIRST (train a real model):                                   │
│  1. Getting Started ───────────────────────┐                     │
│  2. Deployment & the fastai Stack ─────────┤                     │
│                                            ▼                     │
│  UNDERSTAND THE ENGINE:                                           │
│  3. Neural Net Foundations (SGD) ──────────┤                     │
│  5. From-Scratch Model ────────────────────┤                     │
│  8. Convolutions (CNNs) ───────────────────┤                     │
│                                            ▼                     │
│  BREADTH ACROSS DOMAINS:                                          │
│  4. Natural Language (NLP) ────────────────┤                     │
│  6. Random Forests & Tabular ──────────────┤                     │
│  7. Collaborative Filtering ───────────────┤                     │
│                                            ▼                     │
│  ALWAYS:                                                          │
│  9. Data Ethics ───────────────────────────┘                     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

fast.ai recommends watching/reading a lesson, then **immediately** running
and modifying the code before moving on. Don't wait until you "understand
everything" — understanding comes from iteration.

---

## Study schedule

### 4-week pace (aligned with Roadmap Phase 3)

| Week | Modules | Focus |
|------|---------|-------|
| 1 | 01–02 | Train + deploy a classifier end-to-end |
| 2 | 03, 05, 08 | The engine: SGD, from-scratch net, convolutions |
| 3 | 04, 06, 07 | NLP, tabular/forests, collaborative filtering |
| 4 | 09 + projects | Ethics + apply one idea in a lab project |

### 8-week pace (1 module per ~4–5 days)
One module per sitting: read → run exercise → take quiz → apply → reflect.

---

## Prerequisites

- **Python:** comfortable with functions, classes, lists/dicts (see
  `projects/00-core-foundations/`)
- **Math:** none required up front. fast.ai introduces the little you need
  (derivatives-as-slopes, matrix multiply) as it goes.
- **Compute:** a free **Kaggle** or **Paperspace** GPU for the heavier
  lessons. The lectures are readable without one.

---

## How lectures + glossaries + exercises fit together

1. **Lecture** — concepts, code, diagrams, mistakes, best practices.
2. **Glossary** — quick term lookup while reading.
3. **Exercise** (`../exercises/NN-*.py`) — run, predict, modify.
4. **Quiz** (`../quizzes/NN-*.md`) — self-check with explained answers.

Every module ends by pointing you at a lab project to apply the idea, per the
repo's **source → artifact** rule.

---

## Additional resources

- [The course](https://course.fast.ai) · [fastai docs](https://docs.fast.ai)
- [The book (free notebooks)](https://github.com/fastai/fastbook)
- [Are You Ready? — course prereqs](https://course.fast.ai)
- [PyTorch docs](https://pytorch.org/docs/stable/index.html)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)

---

**Train first. Understand deeply. Ship responsibly. 🚀**
