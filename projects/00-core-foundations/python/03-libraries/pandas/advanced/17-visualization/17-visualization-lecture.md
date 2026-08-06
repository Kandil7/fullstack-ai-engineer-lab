# Pandas Visualization: Built-in Plotting with Matplotlib

> **Topic 17 — Advanced pandas series.** Quick, expressive plots straight from
> DataFrames — `plot()`, subplots, styling, and saving for reports.

Companion exercise: `advanced/17-visualization.py`

---

## 1. The `df.plot()` Entry Point

Pandas wraps Matplotlib so you can plot a DataFrame in one line. By default it
uses the **index** as the x-axis and every column as a line:

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "date": pd.date_range("2026-01-01", periods=30),
    "sales": np.random.randint(80, 200, 30),
    "target": 150,
}).set_index("date")

df.plot()                       # line chart
df.plot(kind="bar")             # or: df.plot.bar()
df.plot(kind="scatter", x="a", y="b")
```

**Note**: you need an interactive/agg backend. In Jupyter, `%matplotlib inline`
just works; in scripts use `import matplotlib; matplotlib.use("Agg")` for
headless saving.

## 2. Plot Kinds at a Glance

| `kind` / method | Use case |
|---|---|
| `line` / `.plot.line()` | Time series, trends |
| `bar` / `.plot.bar()` | Compare categories (vertical) |
| `barh` / `.plot.barh()` | Compare categories (horizontal, long labels) |
| `hist` / `.plot.hist()` | Distribution of one variable |
| `box` / `.plot.box()` | Distribution + outliers summary |
| `scatter` / `.plot.scatter(x, y)` | Relationship between two variables |
| `area` / `.plot.area()` | Cumulative parts over time |
| `pie` / `.plot.pie(y=...)` | Share of a whole |
| `kde` / `.plot.kde()` | Smoothed density |

```python
df["sales"].hist(bins=20, color="steelblue", alpha=0.8)
df.plot.scatter(x="visits", y="sales", alpha=0.6)
```

## 3. Subplots — Multiple Charts in One Figure

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

df["sales"].hist(bins=20, ax=axes[0], color="steelblue")
axes[0].set_title("Sales distribution")

df["sales"].plot(ax=axes[1], color="crimson")
axes[1].set_title("Sales over time")

plt.tight_layout()
```

Passing `ax=axes[i]` targets a specific subplot — the standard way to compose
multi-panel figures.

## 4. Styling & Annotations

```python
ax = df["sales"].plot(figsize=(10, 5), color="teal", linewidth=2)
ax.axhline(df["sales"].mean(), color="orange", linestyle="--", label="mean")
ax.set_title("Daily Sales", fontsize=14, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Revenue ($)")
ax.legend()
ax.grid(alpha=0.3)
```

`axhline`/`axvline` draw reference lines (means, thresholds, event dates);
`ax.set_*` controls labels; `grid`, `legend`, `title` polish the chart.

## 5. Saving Figures

```python
fig = df["sales"].plot().get_figure()
fig.savefig("reports/sales.png", dpi=150, bbox_inches="tight")
```

`bbox_inches="tight"` prevents clipped labels. Export to PNG for docs or SVG
for vector-quality figures.

## 6. Real-World Use Case — EDA Dashboard Snippet

```python
df = pd.read_csv("sales.csv", parse_dates=["date"])

fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# Revenue trend
df.groupby("date")["revenue"].sum().plot(ax=axes[0, 0], title="Revenue trend")

# Revenue by region (top 5)
df.groupby("region")["revenue"].sum().sort_values().tail(5).plot.barh(
    ax=axes[0, 1], title="Revenue by region"
)

# Order size distribution
df["order_value"].hist(ax=axes[1, 0], bins=30, title="Order value")

# Channel mix
df.groupby("channel")["revenue"].sum().plot.pie(ax=axes[1, 1], title="Channel mix", autopct="%1.0f%%")

plt.tight_layout()
fig.savefig("reports/eda.png", dpi=150)
```

## 7. Pitfalls to Avoid

- **Plotting object columns**: convert to numeric first — pandas silently
  produces empty/weird charts.
- **Density of line charts**: 10k points on one line is unreadable — resample,
  aggregate, or use `alpha`.
- **Scatter needs two columns**: `df.plot.scatter(x=..., y=...)` — forgetting
  `x`/`y` errors out.
- **Pie for > 6 slices**: pie charts are over-used; a bar chart is usually
  clearer.

## Key Takeaways

1. `df.plot(kind=...)` gives quick charts from any DataFrame.
2. `ax=` routing builds multi-panel figures.
3. Reference lines + labels + grid turn default plots into report-ready charts.
4. Always save with `bbox_inches="tight"` and `dpi` for quality exports.
