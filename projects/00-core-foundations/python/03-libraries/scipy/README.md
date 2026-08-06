# 🔬 SciPy — Scientific Computing

16 self-contained topic directories covering scientific computing from basics through advanced topics.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

```
scipy/
├── 01-introduction/
│   ├── 01-introduction.py
│   ├── 01-introduction-lecture.md
│   └── 01-introduction-glossary.md
├── 02-getting-started/
└── ... (16 topics)
```

## 📚 Topics

| # | Topic | Description |
|---|-------|-------------|
| 01 | Introduction | What is SciPy, relationship with NumPy |
| 02 | Getting Started | Installation, first operations |
| 03 | Basic Functions | Math, special functions, constants |
| 04 | Statistics | Descriptive statistics, distributions |
| 05 | Integration | Numerical integration (quad, trapz) |
| 06 | Interpolation | 1D and N-D interpolation |
| 07 | Optimization | Minimization, curve fitting |
| 08 | Linear Algebra | Matrix operations, decompositions |
| 09 | FFT | Fast Fourier Transform |
| 10 | Spatial Data | KDTree, distance calculations |
| 11 | Image Processing | Filters, transforms, measurements |
| 12 | I/O | Reading/writing files (MMIO, WAV, ARFF) |
| 13 | Statistical Tests | Hypothesis testing, significance |
| 14 | Optimization Advanced | Global optimization, root finding |
| 15 | Sparse Matrices | Sparse data structures, operations |
| 16 | Distance and Similarity | Distance metrics, similarity measures |

## 🚀 Quick Start

```bash
# Run any topic
python 01-introduction/01-introduction.py

# Run all topics
for d in [0-9]*/; do
    py=$(ls "$d"/*.py 2>/dev/null | head -1)
    [ -n "$py" ] && echo "=== $d ===" && python "$py"
done
```

## 📖 Recommended Learning Order

1. **Fundamentals** (01-03): Introduction, setup, basic functions
2. **Core Modules** (04-09): Statistics, integration, interpolation, optimization, linear algebra, FFT
3. **Specialized** (10-12): Spatial data, image processing, I/O
4. **Advanced** (13-16): Statistical tests, optimization, sparse matrices, distance metrics

---

*Last updated: August 2026*
