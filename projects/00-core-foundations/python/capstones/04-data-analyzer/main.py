"""
Data Analyzer — Mini Project
===============================
Combines: Pandas, NumPy, Matplotlib, data cleaning, statistics, visualization

Analyzes a dataset and generates a summary report with visualizations.

Run: python projects/04-data-analyzer/main.py
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


def generate_sample_dataset() -> pd.DataFrame:
    """Generate a realistic sample dataset for analysis."""
    np.random.seed(42)
    n = 500

    data = {
        "customer_id": range(1, n + 1),
        "age": np.random.randint(18, 75, n),
        "gender": np.random.choice(["Male", "Female", "Other"], n, p=[0.48, 0.48, 0.04]),
        "annual_income": np.random.normal(55000, 25000, n).clip(15000, 200000).round(-2),
        "spending_score": np.random.randint(1, 100, n),
        "membership_years": np.random.exponential(3, n).round(1).clip(0, 20),
        "purchase_frequency": np.random.poisson(lam=12, size=n),
        "avg_order_value": np.random.lognormal(mean=3.5, sigma=0.5, size=n).round(2),
        "region": np.random.choice(["North", "South", "East", "West"], n),
        "is_active": np.random.choice([True, False], n, p=[0.75, 0.25]),
    }
    df = pd.DataFrame(data)

    # Add some realistic missing values
    mask = np.random.random(n) < 0.05
    df.loc[mask, "annual_income"] = np.nan
    mask = np.random.random(n) < 0.03
    df.loc[mask, "avg_order_value"] = np.nan

    return df


def analyze_dataset(df: pd.DataFrame) -> dict:
    """Perform comprehensive analysis of the dataset."""
    analysis = {}

    # Basic info
    analysis["shape"] = df.shape
    analysis["columns"] = list(df.columns)
    analysis["dtypes"] = df.dtypes.to_dict()
    analysis["missing_values"] = df.isnull().sum().to_dict()
    analysis["missing_pct"] = (df.isnull().sum() / len(df) * 100).round(1).to_dict()

    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    analysis["numeric_summary"] = df[numeric_cols].describe().to_dict()

    # Categorical columns analysis
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns
    analysis["categorical_summary"] = {}
    for col in cat_cols:
        analysis["categorical_summary"][col] = {
            "unique_values": int(df[col].nunique()),
            "top_values": df[col].value_counts().head(5).to_dict(),
        }

    # Correlation matrix (numeric only)
    analysis["correlations"] = df[numeric_cols].corr().round(3).to_dict()

    # Outlier detection (IQR method)
    analysis["outliers"] = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
        analysis["outliers"][col] = {
            "count": len(outliers),
            "pct": round(len(outliers) / len(df) * 100, 1),
        }

    return analysis


def generate_report(analysis: dict, output_path: str):
    """Generate a formatted text report."""
    lines = []
    lines.append("=" * 60)
    lines.append("  DATA ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append("")

    # Dataset overview
    lines.append(f"Dataset Shape: {analysis['shape'][0]} rows × {analysis['shape'][1]} columns")
    lines.append(f"Columns: {', '.join(analysis['columns'])}")
    lines.append()

    # Missing values
    lines.append("─" * 40)
    lines.append("Missing Values:")
    for col, count in analysis["missing_values"].items():
        if count > 0:
            lines.append(f"  {col}: {count} ({analysis['missing_pct'][col]}%)")
    if all(v == 0 for v in analysis["missing_values"].values()):
        lines.append("  No missing values")
    lines.append()

    # Numeric summary
    lines.append("─" * 40)
    lines.append("Numeric Columns Summary:")
    for col, stats in analysis["numeric_summary"].items():
        lines.append(f"  {col}:")
        lines.append(f"    mean={stats.get('mean', 0):.1f}, "
                     f"std={stats.get('std', 0):.1f}, "
                     f"min={stats.get('min', 0):.1f}, "
                     f"max={stats.get('max', 0):.1f}")
    lines.append()

    # Outliers
    lines.append("─" * 40)
    lines.append("Outliers (IQR method):")
    for col, info in analysis["outliers"].items():
        if info["count"] > 0:
            lines.append(f"  {col}: {info['count']} ({info['pct']}%)")

    lines.append()
    lines.append("=" * 60)
    lines.append("  END OF REPORT")
    lines.append("=" * 60)

    report = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    return report


def create_visualizations(df: pd.DataFrame):
    """Create multiple visualizations."""
    
    # 1. Income distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    df["annual_income"].dropna().hist(bins=30, ax=ax, color="steelblue", edgecolor="white")
    ax.set_title("Annual Income Distribution", fontsize=14)
    ax.set_xlabel("Annual Income ($)")
    ax.set_ylabel("Frequency")
    ax.axvline(df["annual_income"].mean(), color="red", linestyle="--", label="Mean")
    ax.axvline(df["annual_income"].median(), color="green", linestyle="--", label="Median")
    ax.legend()
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "01_income_distribution.png"), dpi=100)
    plt.close(fig)
    print("  ✅ Created: income_distribution.png")

    # 2. Spending score vs annual income (scatter)
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        df["annual_income"], df["spending_score"],
        c=df["purchase_frequency"], cmap="viridis", alpha=0.6, s=30
    )
    ax.set_title("Spending Score vs Annual Income", fontsize=14)
    ax.set_xlabel("Annual Income ($)")
    ax.set_ylabel("Spending Score")
    plt.colorbar(scatter, ax=ax, label="Purchase Frequency")
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "02_spending_vs_income.png"), dpi=100)
    plt.close(fig)
    print("  ✅ Created: spending_vs_income.png")

    # 3. Average metrics by region (bar chart)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for i, metric in enumerate(["avg_order_value", "purchase_frequency"]):
        region_data = df.groupby("region")[metric].mean().sort_values()
        colors = plt.cm.Set2(np.linspace(0, 1, len(region_data)))
        axes[i].bar(region_data.index, region_data.values, color=colors)
        axes[i].set_title(f"Average {metric.replace('_', ' ').title()} by Region", fontsize=11)
        axes[i].set_xlabel("Region")
        axes[i].set_ylabel("Average")
        axes[i].tick_params(axis="x", rotation=0)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "03_region_metrics.png"), dpi=100)
    plt.close(fig)
    print("  ✅ Created: region_metrics.png")

    # 4. Correlation heatmap
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(corr.columns, fontsize=9)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center",
                    fontsize=8, color="white" if abs(corr.values[i, j]) > 0.5 else "black")
    plt.colorbar(im, ax=ax, label="Correlation", shrink=0.8)
    ax.set_title("Correlation Matrix", fontsize=14)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "04_correlation_matrix.png"), dpi=100)
    plt.close(fig)
    print("  ✅ Created: correlation_matrix.png")

    # 5. Membership years histogram
    fig, ax = plt.subplots(figsize=(10, 6))
    df["membership_years"].hist(bins=20, ax=ax, color="coral", edgecolor="white", alpha=0.7)
    ax.set_title("Customer Membership Duration", fontsize=14)
    ax.set_xlabel("Years")
    ax.set_ylabel("Number of Customers")
    ax.axvline(df["membership_years"].median(), color="darkred", linestyle="--",
               label=f"Median: {df['membership_years'].median():.1f}yrs")
    ax.legend()
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "05_membership_duration.png"), dpi=100)
    plt.close(fig)
    print("  ✅ Created: membership_duration.png")


def main():
    print("=" * 50)
    print("  📊 Data Analyzer")
    print("=" * 50)
    print()

    # Step 1: Generate data
    print("📦 Generating sample dataset...")
    df = generate_sample_dataset()
    print(f"  Generated: {df.shape[0]} rows × {df.shape[1]} columns")
    print()

    # Step 2: Preview
    print("👁️  Data Preview:")
    print(df.head().to_string())
    print()

    # Step 3: Analyze
    print("🔍 Running analysis...")
    analysis = analyze_dataset(df)
    print("  Analysis complete!")
    print()

    # Step 4: Generate report
    print("📝 Generating report...")
    report_path = os.path.join(OUTPUT_DIR, "analysis_report.txt")
    report = generate_report(analysis, report_path)
    print(f"  Report saved to: {report_path}")
    print()

    # Step 5: Create visualizations
    print("🎨 Creating visualizations...")
    create_visualizations(df)
    print()

    # Step 6: Display report
    print("=" * 50)
    print("  REPORT PREVIEW")
    print("=" * 50)
    # Show first 20 lines
    for line in report.split("\n")[:20]:
        print(line)
    print(f"\n  ... (full report in {report_path})")
    print()

    print("✅ Analysis complete!")
    print(f"   Output: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
