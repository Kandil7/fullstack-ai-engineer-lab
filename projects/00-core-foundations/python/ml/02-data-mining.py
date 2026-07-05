"""
W3Schools Python Tutorial - ML NN: Data Mining Concepts
=======================================================
Topics: Data Mining, Pattern Discovery, Clustering, Association Rules

Run: python 02-data-mining.py
Reference: https://www.w3schools.com/python/ml_data_mining.asp
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

# ============================================================
# What is Data Mining?
# ============================================================

# Example 1: Data mining definition
print("Example 1: Data Mining")
print("Data mining is the process of discovering patterns in large data sets")
print("It uses methods from statistics, machine learning, and database systems")

# ============================================================
# Pattern Discovery
# ============================================================

# Example 2: Finding patterns in data
print("\nExample 2: Pattern Discovery")
np.random.seed(42)
data = np.random.rand(50, 3)

# Simple pattern: values above 0.5
pattern1 = data[data[:, 0] > 0.5]
print(f"Pattern 1: {len(pattern1)} samples with feature 1 > 0.5")

# Cluster pattern
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(data)
print(f"Pattern 2: Found {len(np.unique(clusters))} clusters")

# ============================================================
# Clustering Overview
# ============================================================

# Example 3: K-means clustering
print("\nExample 3: K-means Clustering")
X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=42)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans.fit(X)
labels = kmeans.labels_
centers = kmeans.cluster_centers_

print(f"Generated {len(X)} data points in 4 clusters")
print(f"Cluster centers:\n{centers}")

# Example 4: Cluster evaluation
print("\nExample 4: Evaluating Clusters")
inertia = kmeans.inertia_
print(f"Inertia (within-cluster sum of squares): {inertia:.2f}")

# ============================================================
# Association Rules
# ============================================================

# Example 5: Simple association rules
print("\nExample 5: Association Rules")
# Simulated transaction data
transactions = [
    ['bread', 'milk', 'eggs'],
    ['bread', 'butter', 'jam'],
    ['milk', 'butter', 'eggs'],
    ['bread', 'milk', 'butter'],
    ['bread', 'milk', 'butter', 'eggs']
]

# Count item frequencies
from collections import Counter
all_items = [item for transaction in transactions for item in transaction]
item_counts = Counter(all_items)
print("Item frequencies:")
for item, count in item_counts.most_common():
    print(f"  {item}: {count}")

# ============================================================
# Data Mining Techniques
# ============================================================

# Example 6: Classification for pattern discovery
print("\nExample 6: Classification Patterns")
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Generate synthetic data
np.random.seed(42)
X = np.random.rand(200, 4)
y = (X[:, 0] + X[:, 1] > 1).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

# Feature importance
importances = clf.feature_importances_
print("Feature importances:")
for i, imp in enumerate(importances):
    print(f"  Feature {i}: {imp:.3f}")

# ============================================================
# Anomaly Detection
# ============================================================

# Example 7: Simple anomaly detection
print("\nExample 7: Anomaly Detection")
np.random.seed(42)
normal_data = np.random.randn(100, 2)
anomaly = np.array([[5, 5]])

# Simple distance-based detection
from sklearn.neighbors import LocalOutlierFactor
lof = LocalOutlierFactor(n_neighbors=20)
predictions = lof.fit_predict(np.vstack([normal_data, anomaly]))

anomaly_count = np.sum(predictions == -1)
print(f"Detected {anomaly_count} anomalies in dataset")

# ============================================================
# Feature Extraction
# ============================================================

# Example 8: Feature extraction
print("\nExample 8: Feature Extraction")
# Text data example
documents = [
    "machine learning is great",
    "data mining is useful",
    "machine learning and data mining"
]

# Simple bag of words
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

print("Vocabulary:", vectorizer.get_feature_names_out())
print("Document-term matrix shape:", X.shape)

# ============================================================
# Data Preprocessing for Mining
# ============================================================

# Example 9: Data preprocessing
print("\nExample 9: Data Preprocessing")
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Sample data
data = np.array([[100, 0.5], [200, 1.0], [300, 1.5], [400, 2.0]])

# Standardization
scaler = StandardScaler()
standardized = scaler.fit_transform(data)
print("Standardized data (mean=0, std=1):")
print(standardized)

# Normalization
normalizer = MinMaxScaler()
normalized = normalizer.fit_transform(data)
print("\nNormalized data (0-1 range):")
print(normalized)

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("Summary:")
print("- Data mining: Discovering patterns in large datasets")
print("- Key techniques: Clustering, classification, association rules")
print("- Pattern discovery helps understand data structure")
print("- Feature extraction converts raw data to useful features")
print("- Data preprocessing is crucial for effective mining")
print("="*60)