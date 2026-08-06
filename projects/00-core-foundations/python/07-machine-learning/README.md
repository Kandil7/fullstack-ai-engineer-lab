# 🤖 Phase 7: Machine Learning

40 self-contained topic directories organized into 3 levels covering ML from fundamentals through deep learning.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

```
07-machine-learning/
├── fundamentals/                 # 23 topics: Basic ML concepts
│   ├── 01-getting-started/
│   │   ├── 01-getting-started.py
│   │   ├── 01-getting-started-lecture.md
│   │   └── 01-getting-started-glossary.md
│   └── ... (23 topics)
│
├── advanced/                     # 12 topics: Pipelines, metrics, tuning
│   ├── 24-sklearn-pipelines/
│   └── ... (12 topics)
│
└── deep-learning/                # 5 topics: PyTorch, neural nets, transformers
    ├── 36-pytorch-tensors/
    └── ... (5 topics)
```

## 📚 Topics

### fundamentals/ (01-23): Basic ML Concepts
| # | Topic | Description |
|---|-------|-------------|
| 01 | Getting Started | ML overview, workflow |
| 02 | Data Mining | Data collection, exploration |
| 03 | Data Set | Dataset creation, loading |
| 04 | Clean Data | Preprocessing, handling missing values |
| 05 | Linear Regression | Simple linear regression |
| 06 | Polynomial Regression | Non-linear regression |
| 07 | R-Squared | Model evaluation metrics |
| 08 | Multiple Regression | Multiple features |
| 09 | Scale | Feature scaling, normalization |
| 10 | Train/Test Split | Data splitting strategies |
| 11 | Decision Tree | Tree-based classification |
| 12 | Confusion Matrix | Classification metrics |
| 13 | Correlation | Feature relationships |
| 14 | Linear Regression Example | Complete workflow |
| 15 | Logistic Regression | Binary classification |
| 16 | K-Means | Clustering |
| 17 | Hierarchical Clustering | Agglomerative clustering |
| 18 | PCA | Dimensionality reduction |
| 19 | Naive Bayes | Probabilistic classification |
| 20 | Random Forest | Ensemble methods |
| 21 | SVM | Support vector machines |
| 22 | Cross Validation | Model validation |
| 23 | K-Nearest Neighbors | Instance-based learning |

### advanced/ (24-35): Advanced Techniques
| # | Topic | Description |
|---|-------|-------------|
| 24 | Sklearn Pipelines | Pipeline API, chaining |
| 25 | Data Leakage | Preventing data leakage |
| 26 | Validation Strategies | Advanced validation |
| 27 | Metrics Deep Dive | Comprehensive metrics |
| 28 | Calibration | Probability calibration |
| 29 | Imbalanced Learning | Handling class imbalance |
| 30 | Gradient Boosting | XGBoost, LightGBM |
| 31 | Feature Engineering | Feature creation |
| 32 | Feature Selection | Feature importance |
| 33 | Hyperparameter Tuning | Grid/random search |
| 34 | Ensembling | Model ensembles |
| 35 | Explainability | SHAP, LIME |

### deep-learning/ (36-40): PyTorch & Neural Networks
| # | Topic | Description |
|---|-------|-------------|
| 36 | PyTorch Tensors | Tensor operations |
| 37 | PyTorch Training Loop | Training workflow |
| 38 | Neural Network Basics | NN architecture |
| 39 | Transfer Learning | Pre-trained models |
| 40 | Transformers from Scratch | Transformer architecture |

## 🚀 Quick Start

```bash
# Install dependencies
pip install scikit-learn numpy pandas matplotlib torch

# Run any topic
python fundamentals/01-getting-started/01-getting-started.py

# Run all fundamentals
for d in fundamentals/[0-9]*/; do
    py=$(ls "$d"/*.py 2>/dev/null | head -1)
    [ -n "$py" ] && echo "=== $d ===" && python "$py"
done
```

## 📖 Recommended Learning Order

### Level 1: Fundamentals (01-23)
Start with the basics of ML algorithms and workflows.

### Level 2: Advanced (24-35)
Learn production ML techniques: pipelines, metrics, tuning.

### Level 3: Deep Learning (36-40)
Introduce PyTorch and neural network architectures.

---

*Last updated: August 2026*
