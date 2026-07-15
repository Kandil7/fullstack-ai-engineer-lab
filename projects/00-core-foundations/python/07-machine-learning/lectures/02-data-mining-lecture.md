# Lecture 02: Data Mining Concepts

## Topic Overview

Data Mining is the process of discovering patterns, correlations, and useful information from large datasets. It sits at the intersection of statistics, machine learning, and database systems. This lecture covers the core techniques of data mining: pattern discovery, clustering, association rules, anomaly detection, and feature extraction.

Data Mining is not just about running algorithms — it's about asking the right questions and finding meaningful insights hidden in data. The techniques you learn here form the foundation for more advanced ML topics.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define Data Mining and its role in the data science pipeline
2. Apply clustering techniques to discover natural groupings in data
3. Understand association rules and how they reveal item relationships
4. Use classification for pattern discovery
5. Detect anomalies and outliers in datasets
6. Extract meaningful features from raw data
7. Preprocess data effectively for mining operations
8. Evaluate the quality of discovered patterns

---

## Key Concepts

### 1. What is Data Mining?

Data Mining is the automated or semi-automated discovery of patterns in large datasets. It uses techniques from:

- **Statistics:** Hypothesis testing, correlation analysis
- **Machine Learning:** Classification, clustering, prediction
- **Database Systems:** SQL queries, data warehousing
- **Pattern Recognition:** Sequence mining, graph mining

**The Data Mining Process:**
```
Raw Data → Preprocessing → Feature Extraction → Pattern Discovery → Evaluation → Knowledge
```

**Key Goals:**
- **Classification:** Assign data to predefined categories
- **Clustering:** Group similar data points together
- **Association:** Find relationships between items
- **Anomaly Detection:** Identify unusual patterns
- **Regression:** Predict numerical values
- **Sequential Patterns:** Find time-ordered patterns

### 2. Pattern Discovery

Pattern discovery is the core of data mining — finding recurring structures, relationships, or regularities in data.

**Types of Patterns:**
- **Frequent Patterns:** Items that appear together often
- **Sequential Patterns:** Ordered sequences of events
- **Subgraph Patterns:** Recurring structures in graph data
- **Outlier Patterns:** Data points that deviate from normal

```python
# Simple pattern: find all samples where feature 1 > 0.5
pattern1 = data[data[:, 0] > 0.5]
print(f"Found {len(pattern1)} samples matching pattern")
```

### 3. Clustering

Clustering groups similar data points together without predefined labels. Unlike classification, there are no "correct" answers — the algorithm discovers natural groupings.

**K-Means Clustering:**
```
1. Choose k (number of clusters)
2. Initialize k random centroids
3. Assign each point to nearest centroid
4. Recalculate centroids as mean of assigned points
5. Repeat steps 3-4 until convergence
```

**Evaluating Clusters:**
- **Inertia:** Sum of squared distances to centroids (lower = tighter clusters)
- **Silhouette Score:** How similar a point is to its own cluster vs. other clusters
- **Davies-Bouldin Index:** Average similarity between clusters

### 4. Association Rules

Association rules find relationships between items in transactional data. Famous example: "Customers who buy diapers also tend to buy beer."

**Key Metrics:**
- **Support:** How often items appear together
  ```
  Support(A→B) = P(A ∩ B) = (Transactions with A and B) / (Total transactions)
  ```

- **Confidence:** How often the rule is correct
  ```
  Confidence(A→B) = P(B|A) = Support(A→B) / Support(A)
  ```

- **Lift:** How much more likely B is when A is present
  ```
  Lift(A→B) = Confidence(A→B) / Support(B)
  ```

### 5. Anomaly Detection

Anomaly detection identifies data points that significantly differ from the majority. These are called outliers, anomalies, or novelties.

**Types of Anomalies:**
- **Point Anomalies:** Individual data points that are far from others
- **Contextual Anomalies:** Anomalous in a specific context
- **Collective Anomalies:** A collection of data points that is anomalous

**Detection Methods:**
- **Statistical:** Z-score, IQR method
- **Distance-based:** k-NN distance
- **Density-based:** Local Outlier Factor (LOF)
- **Model-based:** Isolation Forest, One-Class SVM

---

## Code Examples

### Example 1: K-Means Clustering

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# Generate synthetic data with 4 natural clusters
X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=42)

# Apply K-Means
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans.fit(X)

labels = kmeans.labels_          # Cluster assignments
centers = kmeans.cluster_centers_  # Cluster centers

print(f"Data points: {len(X)}")
print(f"Cluster centers:\n{centers}")
print(f"Inertia: {kmeans.inertia_:.2f}")
```

**Explanation:**
- `make_blobs()` generates data with known cluster structure
- `n_clusters=4` tells K-Means to find 4 groups
- `labels_` contains the cluster assignment for each point
- `cluster_centers_` are the mean positions of each cluster
- `inertia_` measures how tight the clusters are (lower = better)

### Example 2: Association Rules

```python
from collections import Counter

# Transaction data
transactions = [
    ['bread', 'milk', 'eggs'],
    ['bread', 'butter', 'jam'],
    ['milk', 'butter', 'eggs'],
    ['bread', 'milk', 'butter'],
    ['bread', 'milk', 'butter', 'eggs']
]

# Count item frequencies
all_items = [item for transaction in transactions for item in transaction]
item_counts = Counter(all_items)

print("Item frequencies:")
for item, count in item_counts.most_common():
    print(f"  {item}: {count} ({count/len(transactions)*100:.0f}%)")

# Calculate support for item pairs
from itertools import combinations
pair_counts = Counter()
for transaction in transactions:
    for pair in combinations(transaction, 2):
        pair_counts[tuple(sorted(pair))] += 1

print("\nPair support:")
for pair, count in pair_counts.most_common():
    support = count / len(transactions)
    print(f"  {pair}: {support:.2f}")
```

### Example 3: Classification for Pattern Discovery

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Generate data with known patterns
np.random.seed(42)
X = np.random.rand(200, 4)
y = (X[:, 0] + X[:, 1] > 1).astype(int)  # Pattern: sum of first 2 features > 1

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

# Discover feature importances
importances = clf.feature_importances_
print("Feature importances (pattern discovery):")
for i, imp in enumerate(importances):
    print(f"  Feature {i}: {imp:.3f}")

# The model "discovered" that features 0 and 1 are important
```

### Example 4: Anomaly Detection

```python
from sklearn.neighbors import LocalOutlierFactor

# Normal data + anomaly
np.random.seed(42)
normal_data = np.random.randn(100, 2)
anomaly = np.array([[5, 5]])  # Far from normal distribution

all_data = np.vstack([normal_data, anomaly])

# Detect anomalies
lof = LocalOutlierFactor(n_neighbors=20)
predictions = lof.fit_predict(all_data)

anomaly_count = np.sum(predictions == -1)
print(f"Detected {anomaly_count} anomalies in {len(all_data)} samples")
print(f"Anomaly indices: {np.where(predictions == -1)[0]}")
```

**Explanation:**
- `LocalOutlierFactor` measures local density deviation
- Points with significantly lower density than neighbors are outliers
- `predictions == -1` indicates anomalous points
- `predictions == 1` indicates normal points

### Example 5: Feature Extraction (Text)

```python
from sklearn.feature_extraction.text import CountVectorizer

documents = [
    "machine learning is great",
    "data mining is useful",
    "machine learning and data mining"
]

# Convert text to numerical features (Bag of Words)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

print("Vocabulary:", vectorizer.get_feature_names_out())
print("Document-term matrix shape:", X.shape)
print("Matrix:\n", X.toarray())
```

**Explanation:**
- `CountVectorizer` creates a vocabulary of unique words
- Each document becomes a vector of word counts
- Shape is (3 documents, 7 unique words)
- This transforms text data into numerical format for ML

### Example 6: Data Preprocessing

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

data = np.array([[100, 0.5], [200, 1.0], [300, 1.5], [400, 2.0]])

# Standardization (Z-score): mean=0, std=1
scaler = StandardScaler()
standardized = scaler.fit_transform(data)
print("Standardized:")
print(standardized)

# Normalization (Min-Max): range 0-1
normalizer = MinMaxScaler()
normalized = normalizer.fit_transform(data)
print("\nNormalized:")
print(normalized)
```

---

## Common Mistakes to Avoid

1. **Not preprocessing data** — Scaling and normalization are crucial for many algorithms
2. **Choosing wrong k in K-Means** — Use elbow method or silhouette analysis
3. **Ignoring domain knowledge** — Patterns should make business/scientific sense
4. **Mining too much** — Focus on relevant features and questions
5. **Over-interpreting patterns** — Correlation ≠ causation
6. **Not validating results** — Use holdout data to verify discovered patterns
7. **Ignoring data quality** — Dirty data leads to misleading patterns

---

## Best Practices

1. **Understand your data first** — Visualize distributions and relationships
2. **Preprocess carefully** — Handle missing values, scale features, encode categories
3. **Use multiple techniques** — Different algorithms reveal different patterns
4. **Validate discoveries** — Test patterns on unseen data
5. **Consider domain context** — Not all statistically significant patterns are useful
6. **Document your process** — Record what you tried and what you found
7. **Start simple** — Begin with basic techniques before complex ones

---

## Practice Exercises

### Exercise 1: Clustering
Generate 200 data points with 3 natural clusters. Apply K-Means with k=3 and k=5. Which is better? How can you tell?

### Exercise 2: Association Rules
Create a transaction dataset with at least 10 transactions and 5 items. Calculate support and confidence for 3 different rules.

### Exercise 3: Anomaly Detection
Generate 100 normal data points and 5 anomalies. Use `LocalOutlierFactor` to detect them. What percentage did you catch?

### Exercise 4: Feature Extraction
Create a list of 5 sentences. Use `CountVectorizer` to convert them to numerical features. How many unique words are in the vocabulary?

### Exercise 5: Pattern Discovery
Create a dataset where class 1 is defined by `x1 > 0.5 AND x2 < 0.5`. Can a decision tree discover this pattern? What are the feature importances?

---

## Summary

| Technique | Purpose | Algorithm Example |
|-----------|---------|-------------------|
| **Clustering** | Group similar items | K-Means, DBSCAN |
| **Association Rules** | Find item relationships | Apriori, FP-Growth |
| **Classification** | Discover predictive patterns | Decision Tree, k-NN |
| **Anomaly Detection** | Find unusual patterns | LOF, Isolation Forest |
| **Feature Extraction** | Convert raw data to features | CountVectorizer, TF-IDF |
| **Preprocessing** | Clean and prepare data | StandardScaler, MinMaxScaler |

**Key Takeaway:** Data Mining is about discovering hidden patterns in data. Master the techniques of clustering, association rules, anomaly detection, and feature extraction to extract meaningful insights from any dataset.

---

## Next Lecture

In [Lecture 03: Working with Datasets](03-data-set-lecture.md), we'll learn about dataset structure, features vs targets, and how to properly split data for training and testing.
