# Machine Learning Practice Guide

## How to Use These Exercises

Each ML file in `ml/` contains complete, working examples. Run them to learn:

```powershell
cd projects/00-core-foundations/python/ml
python 01-getting-started.py
python 05-linear-regression.py
python 16-k-means.py
```

---

## Learning Path

### Week 1: Foundations
| Day | File | Topic | What You Learn |
|-----|------|-------|----------------|
| 1 | `01-getting-started.py` | ML Overview | What ML is, types of ML |
| 2 | `02-data-mining.py` | Data Mining | Finding patterns in data |
| 3 | `03-data-set.py` | Datasets | Loading, exploring data |
| 4 | `04-clean-data.py` | Data Cleaning | Missing values, outliers |
| 5 | Review | All Week 1 | Active recall |

### Week 2: Regression
| Day | File | Topic | What You Learn |
|-----|------|-------|----------------|
| 1 | `05-linear-regression.py` | Linear Regression | Simple prediction |
| 2 | `06-polynomial-regression.py` | Polynomial Regression | Non-linear patterns |
| 3 | `07-r-squared.py` | R-Squared | Model evaluation |
| 4 | `08-multiple-regression.py` | Multiple Regression | Multiple features |
| 5 | `09-scale.py` | Feature Scaling | Normalization, standardization |
| 6 | `10-train-test.py` | Train/Test Split | Model validation |
| 7 | Review | All Week 2 | Active recall |

### Week 3: Classification
| Day | File | Topic | What You Learn |
|-----|------|-------|----------------|
| 1 | `11-decision-tree.py` | Decision Tree | Tree-based classification |
| 2 | `12-confusion-matrix.py` | Confusion Matrix | Evaluating classifiers |
| 3 | `13-correlation.py` | Correlation | Feature relationships |
| 4 | `14-linear-regression-example.py` | Full Example | Complete ML pipeline |
| 5 | `15-logistic-regression.py` | Logistic Regression | Binary classification |
| 6 | Review | All Week 3 | Active recall |

### Week 4: Clustering & Advanced
| Day | File | Topic | What You Learn |
|-----|------|-------|----------------|
| 1 | `16-k-means.py` | K-Means | Unsupervised clustering |
| 2 | `17-hierarchical-clustering.py` | Hierarchical | Tree-based clustering |
| 3 | `18-pca.py` | PCA | Dimensionality reduction |
| 4 | `19-naive-bayes.py` | Naive Bayes | Probabilistic classifier |
| 5 | `20-random-forest.py` | Random Forest | Ensemble methods |
| 6 | `21-svm.py` | SVM | Support Vector Machines |
| 7 | Review | All Week 4 | Active recall |

### Week 5: Model Evaluation
| Day | File | Topic | What You Learn |
|-----|------|-------|----------------|
| 1 | `22-cross-validation.py` | Cross Validation | Robust evaluation |
| 2 | `23-k-nearest-neighbors.py` | KNN | Instance-based learning |
| 3-5 | Review | All ML | Complete review |

---

## ML Concepts Cheat Sheet

### Supervised Learning
| Algorithm | Use Case | File |
|-----------|----------|------|
| Linear Regression | Predict continuous values | `05-linear-regression.py` |
| Polynomial Regression | Non-linear prediction | `06-polynomial-regression.py` |
| Multiple Regression | Multiple features | `08-multiple-regression.py` |
| Decision Tree | Classification | `11-decision-tree.py` |
| Logistic Regression | Binary classification | `15-logistic-regression.py` |
| Random Forest | Ensemble classification | `20-random-forest.py` |
| SVM | Complex boundaries | `21-svm.py` |
| KNN | Instance-based | `23-k-nearest-neighbors.py` |
| Naive Bayes | Probabilistic | `19-naive-bayes.py` |

### Unsupervised Learning
| Algorithm | Use Case | File |
|-----------|----------|------|
| K-Means | Clustering | `16-k-means.py` |
| Hierarchical | Tree clustering | `17-hierarchical-clustering.py` |
| PCA | Dimensionality reduction | `18-pca.py` |

### Model Evaluation
| Metric | Use Case | File |
|--------|----------|------|
| R-Squared | Regression quality | `07-r-squared.py` |
| Confusion Matrix | Classification quality | `12-confusion-matrix.py` |
| Cross Validation | Robust evaluation | `22-cross-validation.py` |
| Train/Test Split | Data splitting | `10-train-test.py` |

### Data Preprocessing
| Technique | Purpose | File |
|-----------|---------|------|
| Feature Scaling | Normalize features | `09-scale.py` |
| Data Cleaning | Handle missing data | `04-clean-data.py` |
| Correlation | Feature relationships | `13-correlation.py` |

---

## Active Recall Questions

After each week, answer these without looking at the code:

### Week 1
1. What are the 3 types of ML?
2. What is the difference between supervised and unsupervised learning?
3. Why do we clean data before training?

### Week 2
1. What is linear regression?
2. When do you use polynomial regression instead of linear?
3. What does R-squared measure?
4. Why do we split data into train/test sets?

### Week 3
1. What is a decision tree?
2. How do you read a confusion matrix?
3. What is the difference between precision and recall?
4. When do you use logistic regression vs linear regression?

### Week 4
1. What is K-Means clustering?
2. How do you choose the number of clusters (K)?
3. What is PCA and why is it useful?
4. What is the difference between KNN and K-Means?

### Week 5
1. What is cross-validation?
2. Why is it better than a single train/test split?
3. What are the pros and cons of Random Forest?

---

## The Rule

> **Write code yourself.** Run the examples, understand them, then try to modify them or solve the practice problems without looking.

**Start with:**
```powershell
cd projects/00-core-foundations/python/ml
python 01-getting-started.py
```
