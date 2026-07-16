# fast.ai — Practical Deep Learning for Coders

A source-driven track mirroring [fast.ai](https://www.fast.ai)'s
**Practical Deep Learning for Coders** (Part 1), adapted to this lab's
`lecture → glossary → exercise → quiz` format and its top-down,
"train a real model in lesson 1" teaching philosophy.

> **Source:** <https://course.fast.ai> · **Book:** *Practical Deep Learning
> for Coders with fastai and PyTorch* · **Libraries:** PyTorch, fastai,
> Hugging Face Transformers, Gradio.

---

## Why fast.ai here

The lab's AI-engineering tracks (`ai-automation`, `agents`) teach how to
*use* LLMs and build systems around them. fast.ai fills the layer beneath:
**how models are trained, why they work, and how to ship one**. It maps to
Roadmap Phase 3 (AI fundamentals) and feeds Phase 4 (RAG) and Phase 7
(capstone).

fast.ai's pedagogy is deliberately **top-down**: you train a working image
classifier in lesson 1, then peel back layers until you can build the pieces
from scratch. The modules below follow that arc.

---

## Track layout

```text
fastai-deep-learning/
├── README.md              # this file
├── requirements.txt       # pinned fastai / torch / nbdev / tooling
├── setup.ps1              # CPU-only install by default (see notes)
├── .env.example           # optional tokens (HF, Kaggle)
├── lectures/              # 8 lectures + glossaries (+ series README)
├── exercises/             # one runnable .py per module
├── quizzes/               # one .md quiz per module
└── nbdev-demo/            # notebook-driven-development sample package
```

---

## Environment setup

fastai + PyTorch are large (~2 GB with CUDA). Installation is an **opt-in**
step, separate from the rest of the repo.

```powershell
# From this directory:
./setup.ps1              # CPU-only PyTorch (recommended on Windows)
./setup.ps1 -Gpu         # default CUDA wheels (needs NVIDIA + drivers)
./setup.ps1 -SkipHeavy   # nbdev + tooling only, no torch/fastai
```

> **fast.ai's own advice:** don't train on your own machine unless you're
> comfortable with Linux/GPU/CUDA. Prefer free **Kaggle Notebooks** or
> **Paperspace Gradient** GPUs for the heavier lessons. The lectures are
> written so you can read + reason about the code even without a GPU.

### nbdev on Windows

nbdev's Python package and its `export`/`test` commands work on native
Windows, but the **full docs workflow (Quarto rendering) is only fully
supported on macOS, Linux, or Windows-via-WSL**. Run doc rendering under WSL
if you want the published-site experience. See `nbdev-demo/README.md`.

> **Config note (nbdev ≥ 2024):** newer nbdev moved project config from
> `settings.ini` to `pyproject.toml` (`[tool.nbdev]`), per PEP 621. The demo
> here uses the classic `settings.ini` (nbdev 3.2.x, pinned) and documents
> the migration path (`nbdev-migrate-config`).

---

## Modules

| # | Module | fast.ai lesson | Core idea |
|---|--------|----------------|-----------|
| 01 | [Getting Started](lectures/01-getting-started-lecture.md) | 1 | Train an image classifier in minutes; transfer learning |
| 02 | [Deployment & the fastai Stack](lectures/02-deployment-lecture.md) | 2 | Data cleaning, `DataBlock`, ship with Gradio |
| 03 | [Neural Net Foundations (SGD)](lectures/03-neural-net-foundations-lecture.md) | 3 | Gradient descent, the training loop, from-scratch |
| 04 | [Natural Language (NLP)](lectures/04-nlp-lecture.md) | 4 | Fine-tuning transformers with 🤗 Transformers |
| 05 | [From-Scratch Model](lectures/05-from-scratch-model-lecture.md) | 5 | Build a neural net with nothing but tensors |
| 06 | [Random Forests & Tabular](lectures/06-random-forests-lecture.md) | 6 | Trees, bagging, feature importance, tabular DL |
| 07 | [Collaborative Filtering](lectures/07-collaborative-filtering-lecture.md) | 7 | Embeddings, latent factors, recommenders |
| 08 | [Convolutions (CNNs)](lectures/08-convolutions-lecture.md) | 8 | How CNNs see; convolution from scratch |
| — | [Data Ethics](lectures/09-data-ethics-lecture.md) | Bonus | Bias, feedback loops, responsibility |

Start with the [lecture series README](lectures/README.md) for the full
learning path and study schedule.

---

## How to work through a module (lab rule: source → artifact)

1. **Read** the lecture; keep the glossary open for terms.
2. **Run** the matching `exercises/NN-*.py` (or port it into a notebook /
   Kaggle). Predict outputs before running.
3. **Take** the `quizzes/NN-*.md` quiz; check answers.
4. **Apply** one idea in a lab project (e.g. an embeddings experiment feeds
   `projects/04-ai-engineering/embeddings/`).
5. **Reflect** in `docs/learning/notes/weekly/` and update the source note in
   `learning-sources/`.

---

## Links

- Course: <https://course.fast.ai>
- fastai docs: <https://docs.fast.ai>
- nbdev: <https://nbdev.fast.ai>
- Book (free notebooks): <https://github.com/fastai/fastbook>
