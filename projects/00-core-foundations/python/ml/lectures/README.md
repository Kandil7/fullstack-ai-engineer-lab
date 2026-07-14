# Machine Learning Lectures & Glossaries

## Overview

This directory contains comprehensive lecture notes and glossary files for Machine Learning topics 13-23. Each topic includes:

- **Lecture File**: Detailed explanations, code examples, common mistakes, best practices, and exercises
- **Glossary File**: All terms defined alphabetically with examples and quick reference tables

---

## Table of Contents

### Lecture Files

| # | Topic | File | Description |
|---|-------|------|-------------|
| 13 | Correlation | [13-correlation-lecture.md](13-correlation-lecture.md) | Correlation analysis, matrices, feature selection |
| 14 | Linear Regression Example | [14-linear-regression-example-lecture.md](14-linear-regression-example-lecture.md) | Complete end-to-end regression project |
| 15 | Logistic Regression | [15-logistic-regression-lecture.md](15-logistic-regression-lecture.md) | Binary and multi-class classification |
| 16 | K-Means Clustering | [16-k-means-lecture.md](16-k-means-lecture.md) | Unsupervised clustering, elbow method |
| 17 | Hierarchical Clustering | [17-hierarchical-clustering-lecture.md](17-hierarchical-clustering-lecture.md) | Agglomerative clustering, dendrograms |
| 18 | PCA | [18-pca-lecture.md](18-pca-lecture.md) | Dimensionality reduction, explained variance |
| 19 | Naive Bayes | [19-naive-bayes-lecture.md](19-naive-bayes-lecture.md) | Probabilistic classification, Bayes' theorem |
| 20 | Random Forest | [20-random-forest-lecture.md](20-random-forest-lecture.md) | Ensemble methods, feature importance |
| 21 | SVM | [21-svm-lecture.md](21-svm-lecture.md) | Support Vector Machines, kernels |
| 22 | Cross-Validation | [22-cross-validation-lecture.md](22-cross-validation-lecture.md) | Model evaluation, K-Fold, Stratified |
| 23 | K-Nearest Neighbors | [23-k-nearest-neighbors-lecture.md](23-k-nearest-neighbors-lecture.md) | Instance-based learning, distance metrics |

### Glossary Files

| # | Topic | File |
|---|-------|------|
| 13 | Correlation | [13-correlation-glossary.md](13-correlation-glossary.md) |
| 14 | Linear Regression | [14-linear-regression-example-glossary.md](14-linear-regression-example-glossary.md) |
| 15 | Logistic Regression | [15-logistic-regression-glossary.md](15-logistic-regression-glossary.md) |
| 16 | K-Means | [16-k-means-glossary.md](16-k-means-glossary.md) |
| 17 | Hierarchical Clustering | [17-hierarchical-clustering-glossary.md](17-hierarchical-clustering-glossary.md) |
| 18 | PCA | [18-pca-glossary.md](18-pca-glossary.md) |
| 19 | Naive Bayes | [19-naive-bayes-glossary.md](19-naive-bayes-glossary.md) |
| 20 | Random Forest | [20-random-forest-glossary.md](20-random-forest-glossary.md) |
| 21 | SVM | [21-svm-glossary.md](21-svm-glossary.md) |
| 22 | Cross-Validation | [22-cross-validation-glossary.md](22-cross-validation-glossary.md) |
| 23 | KNN | [23-k-nearest-neighbors-glossary.md](23-k-nearest-neighbors-glossary.md) |

---

## Recommended Learning Order

### Phase 1: Supervised Learning Foundations

1. **Lecture 13**: Correlation — Understand feature relationships
2. **Lecture 14**: Linear Regression — Master regression basics
3. **Lecture 15**: Logistic Regression — Learn classification

### Phase 2: Unsupervised Learning

4. **Lecture 16**: K-Means — Introduction to clustering
5. **Lecture 17**: Hierarchical Clustering — Alternative clustering approach
6. **Lecture 18**: PCA — Dimensionality reduction

### Phase 3: Advanced Algorithms

7. **Lecture 19**: Naive Bayes — Probabilistic classification
8. **Lecture 20**: Random Forest — Ensemble methods
9. **Lecture 21**: SVM — Maximum margin classifiers
10. **Lecture 23**: KNN — Instance-based learning

### Phase 4: Model Evaluation

11. **Lecture 22**: Cross-Validation — Proper model evaluation (review after learning algorithms)

---

## How to Use Lectures + Glossaries Together

### Study Workflow

1. **Read the Lecture**
   - Understand the concept and theory
   - Study the code examples
   - Note common mistakes

2. **Reference the Glossary**
   - Look up unfamiliar terms
   - Use quick reference tables
   - Review code snippets

3. **Run the Code**
   - Execute examples from the lecture
   - Modify parameters to see effects
   - Complete practice exercises

4. **Review Common Mistakes**
   - Avoid pitfalls in your own code
   - Apply best practices

### Example Study Session

```bash
# 1. Read the lecture
cat 13-correlation-lecture.md

# 2. Reference glossary for terms
cat 13-correlation-glossary.md

# 3. Run the corresponding Python file
python ../13-correlation.py

# 4. Complete exercises from the lecture
```

---

## Study Schedule

### 2-Week Intensive Plan

| Day | Topics | Time |
|-----|--------|------|
| Day 1 | Lecture 13: Correlation | 2-3 hours |
| Day 2 | Lecture 14: Linear Regression | 2-3 hours |
| Day 3 | Lecture 15: Logistic Regression | 2-3 hours |
| Day 4 | Lecture 16: K-Means | 2-3 hours |
| Day 5 | Lecture 17: Hierarchical Clustering | 2-3 hours |
| Day 6 | Lecture 18: PCA | 2-3 hours |
| Day 7 | **Review Phase 1-2** | 2-3 hours |
| Day 8 | Lecture 19: Naive Bayes | 2-3 hours |
| Day 9 | Lecture 20: Random Forest | 2-3 hours |
| Day 10 | Lecture 21: SVM | 2-3 hours |
| Day 11 | Lecture 22: Cross-Validation | 2-3 hours |
| Day 12 | Lecture 23: KNN | 2-3 hours |
| Day 13-14 | **Review & Practice** | 4-6 hours |

### Weekly Plan (4 Weeks)

| Week | Topics | Focus |
|------|--------|-------|
| Week 1 | 13-15 | Supervised Learning Basics |
| Week 2 | 16-18 | Unsupervised Learning |
| Week 3 | 19-21 | Advanced Algorithms |
| Week 4 | 22-23 + Review | Evaluation & Mastery |

---

## Prerequisites

### Required Knowledge

- **Python Programming**: Variables, functions, loops, classes
- **NumPy**: Arrays, operations, indexing
- **Pandas**: DataFrames, data manipulation
- **Matplotlib/Seaborn**: Basic plotting

### Recommended Background

- **Statistics**: Mean, variance, distributions
- **Linear Algebra**: Vectors, matrices (helpful for PCA)
- **Basic ML Concepts**: Training/test split, overfitting

### Installation

```bash
pip install numpy pandas matplotlib seaborn scikit-learn scipy
```

---

## How to Use

### Reading Lectures

Each lecture follows this structure:

1. **Topic Overview** — What you'll learn
2. **Learning Objectives** — Specific goals
3. **Key Concepts** — Theory explained
4. **Code Examples** — Practical implementation
5. **Common Mistakes** — What to avoid
6. **Best Practices** — Do's and don'ts
7. **Practice Exercises** — Hands-on challenges
8. **Summary** — Key takeaways

### Using Glossaries

Each glossary includes:

1. **Quick Reference Table** — Fast lookup
2. **Detailed Definitions** — In-depth explanations
3. **Code Examples** — How to use each term
4. **Formulas Summary** — Mathematical reference
5. **Code Snippets** — Copy-paste ready

### Running Code Examples

```python
# Example from Lecture 13
import numpy as np
import pandas as pd

# Create sample data
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 6])

# Calculate correlation
correlation = np.corrcoef(x, y)[0, 1]
print(f"Correlation: {correlation:.4f}")
```

---

## Additional Resources

### Online Documentation

- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Tutorials

- [W3Schools Python ML](https://www.w3schools.com/python/python_machine_learning.asp)
- [Kaggle Learn](https://www.kaggle.com/learn)
- [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course)

### Books

- "Hands-On Machine Learning" by Aurélien Géron
- "Introduction to Statistical Learning" by James, Witten, Hastie, Tibshirani
- "Pattern Recognition and Machine Learning" by Christopher Bishop

---

## Contributing

To add new lectures or improve existing ones:

1. Follow the existing file naming convention
2. Include all required sections (see Lecture Structure above)
3. Add glossary terms for any new concepts
4. Update this README with new content

---

## License

This educational content is provided for learning purposes.

---

## Support

For questions or issues:
- Check the lecture notes and glossaries first
- Review the corresponding Python files in the parent directory
- Consult scikit-learn documentation for API details
