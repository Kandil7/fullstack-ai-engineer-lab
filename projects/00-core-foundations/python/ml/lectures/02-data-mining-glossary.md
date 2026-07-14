# Glossary: Data Mining Concepts

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Data Mining | Discovering patterns in large datasets | Process |
| Clustering | Grouping similar data points | Technique |
| Association Rules | Finding relationships between items | Technique |
| Anomaly Detection | Identifying unusual patterns | Technique |
| Feature Extraction | Converting raw data to features | Process |
| K-Means | Partitioning data into k clusters | Algorithm |
| Inertia | Within-cluster sum of squares | Metric |
| Support | Frequency of item occurrence | Metric |
| Confidence | Accuracy of association rule | Metric |
| Lift | Strength of association rule | Metric |
| LOF | Local Outlier Factor | Algorithm |
| Bag of Words | Text representation method | Technique |
| StandardScaler | Z-score normalization | Tool |
| MinMaxScaler | 0-1 normalization | Tool |
| Centroid | Center of a cluster | Concept |
| Outlier | Data point far from others | Concept |
| Pattern | Recurring structure in data | Concept |
| Transaction | Set of items (for association rules) | Data |
| Vocabulary | Unique words in text corpus | Data |
| Preprocessing | Preparing data for mining | Process |

---

## Detailed Definitions

### A

#### Anomaly Detection
**Definition:** The identification of data points, observations, or patterns that significantly deviate from the expected or normal behavior in a dataset.

**Example:**
```python
from sklearn.neighbors import LocalOutlierFactor

# Create data with one anomaly
normal_data = np.random.randn(100, 2)
anomaly = np.array([[10, 10]])
all_data = np.vstack([normal_data, anomaly])

# Detect anomalies
lof = LocalOutlierFactor(n_neighbors=20)
predictions = lof.fit_predict(all_data)
# predictions == -1 for anomalies
```

**Related Terms:** Outlier, Local Outlier Factor, Isolation Forest, IQR Method

#### Association Rules
**Definition:** If-then rules that describe relationships between items in transactional data. Used to find patterns like "customers who buy X also buy Y."

**Example:**
```python
from collections import Counter
from itertools import combinations

transactions = [
    ['bread', 'milk'],
    ['bread', 'butter'],
    ['milk', 'butter']
]

# Calculate support for {bread, milk}
bread_milk_count = sum(1 for t in transactions if 'bread' in t and 'milk' in t)
support = bread_milk_count / len(transactions)
print(f"Support(bread→milk): {support:.2f}")
```

**Related Terms:** Support, Confidence, Lift, Apriori Algorithm

---

### B

#### Bag of Words (BoW)
**Definition:** A text representation technique that converts documents into fixed-length vectors by counting word occurrences, ignoring grammar and word order.

**Example:**
```python
from sklearn.feature_extraction.text import CountVectorizer

docs = ["the cat sat", "the dog sat", "the cat and dog"]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(docs)

print("Vocabulary:", vectorizer.get_feature_names_out())
print("Matrix:\n", X.toarray())
# [[1, 0, 1, 1],  # "the cat sat"
#  [0, 1, 1, 1],  # "the dog sat"
#  [1, 1, 1, 1]]  # "the cat and dog"
```

**Related Terms:** TF-IDF, Text Mining, Feature Extraction, Vocabulary

---

### C

#### Centroid
**Definition:** The center point of a cluster, calculated as the mean of all data points assigned to that cluster.

**Example:**
```python
from sklearn.cluster import KMeans

X = np.array([[1, 2], [2, 3], [3, 4], [10, 11], [11, 12]])
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
kmeans.fit(X)

print("Centroids:")
print(kmeans.cluster_centers_)
# [[2, 3],    # Center of cluster 0
#  [11, 12]]  # Center of cluster 1
```

**Related Terms:** K-Means, Cluster, Inertia, Convergence

#### Clustering
**Definition:** An unsupervised learning technique that groups similar data points together based on their features, without predefined labels.

**Example:**
```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=100, centers=3, random_state=42)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X)

print(f"Found {len(set(clusters))} clusters")
print(f"Cluster sizes: {[sum(clusters == i) for i in range(3)]}")
```

**Related Terms:** K-Means, DBSCAN, Hierarchical Clustering, Unsupervised Learning

#### Confidence (Association Rules)
**Definition:** The probability of finding the consequent (B) in a transaction given that the antecedent (A) is present. Measures the reliability of the rule.

**Formula:**
```
Confidence(A→B) = Support(A∩B) / Support(A)
```

**Example:**
```python
# If support({bread, milk}) = 0.4 and support({bread}) = 0.6
confidence = 0.4 / 0.6
print(f"Confidence(bread→milk): {confidence:.2f}")  # 0.67
```

**Related Terms:** Support, Lift, Association Rules

---

### D

#### DBSCAN
**Definition:** Density-Based Spatial Clustering of Applications with Noise — a clustering algorithm that groups together points in high-density areas and marks points in low-density areas as outliers.

**Example:**
```python
from sklearn.cluster import DBSCAN

X = np.array([[1, 2], [1.5, 2.5], [2, 3], [10, 10], [10.5, 10.5]])
dbscan = DBSCAN(eps=2, min_samples=2)
labels = dbscan.fit_predict(X)

print(f"Labels: {labels}")  # [-1, -1, -1, 0, 0]  (-1 = noise/outlier)
```

**Related Terms:** K-Means, Clustering, Epsilon, Min Samples

---

### I

#### Inertia
**Definition:** The sum of squared distances between each data point and its assigned cluster center. Lower inertia indicates tighter, more compact clusters.

**Formula:**
```
Inertia = Σ ||x_i - μ_c||²
```
where x_i is a data point and μ_c is its cluster center.

**Example:**
```python
from sklearn.cluster import KMeans

# Test different k values
for k in range(2, 6):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    print(f"k={k}: Inertia={kmeans.inertia_:.2f}")
# Inertia decreases as k increases (elbow method)
```

**Related Terms:** K-Means, Centroid, Elbow Method, Silhouette Score

#### Isolation Forest
**Definition:** An anomaly detection algorithm that isolates anomalies by randomly selecting features and split values. Anomalies require fewer splits to isolate.

**Example:**
```python
from sklearn.ensemble import IsolationForest

X = np.random.randn(100, 2)
X = np.vstack([X, [[5, 5], [-5, -5]]])  # Add anomalies

iso_forest = IsolationForest(contamination=0.05, random_state=42)
predictions = iso_forest.fit_predict(X)
# predictions == -1 for anomalies
```

**Related Terms:** Anomaly Detection, Local Outlier Factor, Contamination

---

### K

#### K-Means
**Definition:** A partitioning algorithm that divides data into k clusters by iteratively assigning points to the nearest centroid and recalculating centroids.

**Algorithm:**
```
1. Initialize k centroids randomly
2. Repeat:
   a. Assign each point to nearest centroid
   b. Recalculate centroids as mean of assigned points
3. Until convergence (centroids don't change)
```

**Example:**
```python
from sklearn.cluster import KMeans

kmeans = KMeans(
    n_clusters=3,       # Number of clusters
    init='k-means++',   # Smart initialization
    n_init=10,          # Run 10 times
    max_iter=300,       # Max iterations
    random_state=42
)
kmeans.fit(X)
print(f"Labels: {kmeans.labels_}")
print(f"Centers: {kmeans.cluster_centers_}")
```

**Related Terms:** Centroid, Inertia, Elbow Method, Clustering

---

### L

#### Lift (Association Rules)
**Definition:** The ratio of the observed support to the expected support if A and B were independent. Lift > 1 indicates a positive association.

**Formula:**
```
Lift(A→B) = Confidence(A→B) / Support(B)
```

**Example:**
```python
# If confidence(bread→milk) = 0.67 and support(milk) = 0.6
lift = 0.67 / 0.6
print(f"Lift(bread→milk): {lift:.2f}")  # 1.12 (slight positive association)
```

**Interpretation:**
- Lift = 1: Independent (no association)
- Lift > 1: Positive association (items appear together more than expected)
- Lift < 1: Negative association (items appear together less than expected)

**Related Terms:** Support, Confidence, Association Rules

#### Local Outlier Factor (LOF)
**Definition:** An anomaly detection algorithm that compares the local density of a point to the local densities of its neighbors. Points with substantially lower density are considered outliers.

**Example:**
```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(
    n_neighbors=20,    # Number of neighbors to consider
    contamination=0.1  # Expected proportion of outliers
)
predictions = lof.fit_predict(X)
anomaly_scores = lof.negative_outlier_factor_

print(f"Anomalies detected: {sum(predictions == -1)}")
```

**Related Terms:** Anomaly Detection, Isolation Forest, Outlier, Density

---

### M

#### MinMaxScaler
**Definition:** A preprocessing tool that transforms features by scaling them to a fixed range, typically [0, 1], using the formula: X_scaled = (X - X_min) / (X_max - X_min).

**Example:**
```python
from sklearn.preprocessing import MinMaxScaler

data = np.array([[100, 0.5], [200, 1.0], [300, 1.5]])
scaler = MinMaxScaler()
scaled = scaler.fit_transform(data)

print("Original:\n", data)
print("Scaled:\n", scaled)
# [[0, 0], [0.5, 0.5], [1, 1]]
```

**Related Terms:** StandardScaler, RobustScaler, Normalization, Preprocessing

---

### O

#### Outlier
**Definition:** A data point that differs significantly from other observations. May indicate variability, measurement error, or a genuinely unusual event.

**Example:**
```python
# Detect outliers using IQR method
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = data[(data < lower) | (data > upper)]
print(f"Outliers: {outliers}")
```

**Related Terms:** Anomaly Detection, IQR, Z-Score, Local Outlier Factor

---

### S

#### Silhouette Score
**Definition:** A metric that measures how similar a data point is to its own cluster compared to other clusters. Ranges from -1 (wrong cluster) to 1 (well-matched), with 0 indicating overlap.

**Example:**
```python
from sklearn.metrics import silhouette_score

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)
score = silhouette_score(X, labels)
print(f"Silhouette Score: {score:.3f}")
```

**Related Terms:** Inertia, Davies-Bouldin Index, Clustering Evaluation

#### StandardScaler
**Definition:** A preprocessing tool that standardizes features by removing the mean and scaling to unit variance (Z-score normalization): X_scaled = (X - mean) / std.

**Example:**
```python
from sklearn.preprocessing import StandardScaler

data = np.array([[100, 0.5], [200, 1.0], [300, 1.5]])
scaler = StandardScaler()
scaled = scaler.fit_transform(data)

print("Mean:", scaled.mean(axis=0))   # [0, 0]
print("Std:", scaled.std(axis=0))     # [1, 1]
```

**Related Terms:** MinMaxScaler, RobustScaler, Z-Score, Preprocessing

#### Support (Association Rules)
**Definition:** The proportion of transactions in the dataset that contain a particular itemset. Measures how frequently an itemset appears.

**Formula:**
```
Support(A) = (Transactions containing A) / (Total transactions)
```

**Example:**
```python
transactions = [['bread', 'milk'], ['bread', 'butter'], ['milk', 'eggs']]
bread_count = sum(1 for t in transactions if 'bread' in t)
support_bread = bread_count / len(transactions)
print(f"Support(bread): {support_bread:.2f}")  # 0.67
```

**Related Terms:** Confidence, Lift, Association Rules, Apriori

---

### T

#### TF-IDF
**Definition:** Term Frequency-Inverse Document Frequency — a text feature extraction method that weights words by their importance in a document relative to the corpus.

**Formula:**
```
TF-IDF(t, d) = TF(t, d) × IDF(t)
TF(t, d) = (Count of term t in document d) / (Total terms in d)
IDF(t) = log(N / (Documents containing t))
```

**Example:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer

docs = ["the cat sat on the mat", "the dog sat on the log"]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)

print("Features:", vectorizer.get_feature_names_out())
print("TF-IDF matrix:\n", X.toarray())
```

**Related Terms:** Bag of Words, Text Mining, Feature Extraction

---

## Key Formulas

| Formula | Expression | Description |
|---------|-----------|-------------|
| Support | `count(A∩B) / N` | Frequency of itemset |
| Confidence | `Support(A∩B) / Support(A)` | Rule reliability |
| Lift | `Confidence(A→B) / Support(B)` | Association strength |
| Inertia | `Σ \|\|x - μ\|\|²` | Cluster compactness |
| Min-Max | `(x - min) / (max - min)` | Scale to [0,1] |
| Z-Score | `(x - mean) / std` | Standardize to N(0,1) |
| Silhouette | `(b - a) / max(a, b)` | Cluster quality |

---

## Python Import Cheat Sheet

```python
# Clustering
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

# Anomaly Detection
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest

# Feature Extraction
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Evaluation
from sklearn.metrics import silhouette_score, davies_bouldin_score

# Data Generation
from sklearn.datasets import make_blobs, make_moons

# Utilities
from collections import Counter
from itertools import combinations
```
