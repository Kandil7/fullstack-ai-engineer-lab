"""
ML Pipeline — Mini Project
=============================
Combines: scikit-learn, pandas, matplotlib, data preprocessing, model evaluation

An end-to-end machine learning pipeline for classification.

Run: python projects/05-ml-pipeline/main.py
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import sys

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    from sklearn.datasets import load_iris, make_classification
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                                 f1_score, confusion_matrix, classification_report)
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("scikit-learn not installed. Install with: pip install scikit-learn")


def load_data() -> tuple:
    """Load and prepare the Iris dataset."""
    iris = load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = list(iris.target_names)
    return X, y, feature_names, target_names


def create_synthetic_data() -> tuple:
    """Create a synthetic classification dataset with known properties."""
    X, y = make_classification(
        n_samples=1000, n_features=10, n_informative=5,
        n_redundant=2, n_classes=2, random_state=42
    )
    feature_names = [f"feature_{i}" for i in range(X.shape[1])]
    target_names = ["Class_0", "Class_1"]
    return X, y, feature_names, target_names


def preprocess_data(X_train, X_test):
    """Scale features using StandardScaler."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def train_models(X_train, y_train) -> dict:
    """Train multiple classifiers and return them."""
    models = {
        "Logistic Regression": LogisticRegression(max_iter=200, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "SVM (RBF)": SVC(kernel="rbf", random_state=42),
    }
    trained = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        trained[name] = model
        print(f"  Trained: {name}")
    return trained


def evaluate_models(models: dict, X_test, y_test, target_names: list) -> pd.DataFrame:
    """Evaluate all models and return a comparison DataFrame."""
    results = []
    for name, model in models.items():
        y_pred = model.predict(X_test)
        results.append({
            "Model": name,
            "Accuracy": round(accuracy_score(y_test, y_pred), 4),
            "Precision": round(precision_score(y_test, y_pred, average="weighted"), 4),
            "Recall": round(recall_score(y_test, y_pred, average="weighted"), 4),
            "F1-Score": round(f1_score(y_test, y_pred, average="weighted"), 4),
        })

        # Cross-validation score
        cv_scores = cross_val_score(model, X_test, y_test, cv=5)
        results[-1]["CV Mean"] = round(cv_scores.mean(), 4)
        results[-1]["CV Std"] = round(cv_scores.std(), 4)

    return pd.DataFrame(results).sort_values("F1-Score", ascending=False)


def plot_results(results_df: pd.DataFrame):
    """Create comparison visualizations."""
    # 1. Model comparison bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
    x = np.arange(len(results_df))
    width = 0.2

    for i, metric in enumerate(metrics):
        ax.bar(x + i * width, results_df[metric], width, label=metric)

    ax.set_xlabel("Model")
    ax.set_ylabel("Score")
    ax.set_title("Model Performance Comparison", fontsize=14)
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(results_df["Model"], rotation=30, ha="right")
    ax.legend()
    ax.set_ylim(0, 1.05)
    ax.axhline(y=0.8, color="gray", linestyle="--", alpha=0.5, label="80% threshold")
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "01_model_comparison.png"), dpi=100)
    plt.close(fig)
    print("  Created: model_comparison.png")

    # 2. Feature importance (if random forest available)
    if "Random Forest" in results_df["Model"].values:
        fig, ax = plt.subplots(figsize=(10, 6))
        rf_model = [m for n, m in models.items() if n == "Random Forest"][0]
        importances = rf_model.feature_importances_
        indices = np.argsort(importances)[::-1][:10]
        ax.bar(range(len(indices)), importances[indices], color="forestgreen")
        ax.set_title("Top Feature Importances (Random Forest)", fontsize=14)
        ax.set_xlabel("Feature Index")
        ax.set_ylabel("Importance")
        plt.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, "02_feature_importance.png"), dpi=100)
        plt.close(fig)
        print("  Created: feature_importance.png")


def generate_report(results_df: pd.DataFrame, dataset_name: str) -> str:
    """Generate a text summary report."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"  ML PIPELINE REPORT - {dataset_name}")
    lines.append("=" * 60)
    lines.append()
    lines.append("Model Rankings:")
    lines.append(results_df.to_string(index=False))
    lines.append()
    lines.append(f"Best Model: {results_df.iloc[0]['Model']}")
    lines.append(f"Best F1-Score: {results_df.iloc[0]['F1-Score']:.4f}")
    lines.append(f"Best CV Mean: {results_df.iloc[0]['CV Mean']:.4f}")
    lines.append()
    lines.append("=" * 60)

    report = "\n".join(lines)
    report_path = os.path.join(OUTPUT_DIR, "ml_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    return report


def main():
    if not HAS_SKLEARN:
        print("\nERROR: scikit-learn is required for this project.")
        print("Install with: pip install scikit-learn")
        sys.exit(1)

    print("=" * 50)
    print("  ML Pipeline - Classification Benchmark")
    print("=" * 50)
    print()

    # Step 1: Load data
    print("Loading dataset...")
    X, y, feature_names, target_names = load_data()
    print(f"  Dataset: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"  Classes: {target_names}")
    print()

    # Step 2: Split
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
    print()

    # Step 3: Preprocess
    print("Preprocessing...")
    X_train, X_test, scaler = preprocess_data(X_train, X_test)
    print(f"  Scaled {len(feature_names)} features (mean=0, std=1)")
    print()

    # Step 4: Train
    print("Training models...")
    global models
    models = train_models(X_train, y_train)
    print()

    # Step 5: Evaluate
    print("Evaluating models...")
    results_df = evaluate_models(models, X_test, y_test, target_names)
    print()

    # Step 6: Visualize
    print("Creating visualizations...")
    plot_results(results_df)
    print()

    # Step 7: Report
    print("Generating report...")
    report = generate_report(results_df, "Iris Dataset")
    print(f"  Report saved to: {os.path.join(OUTPUT_DIR, 'ml_report.txt')}")
    print()

    # Display results
    print("=" * 50)
    print("  RESULTS")
    print("=" * 50)
    print(results_df.to_string(index=False))
    print()
    print(f"  Full output: {OUTPUT_DIR}/")
    print()

    print("Done!")


if __name__ == "__main__":
    main()
