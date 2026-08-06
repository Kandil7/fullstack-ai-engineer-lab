# Visualization — Glossary

> Companion reference for the **Pandas Visualization** lecture. Reach for it
> while working through `advanced/17-visualization.py`.

## The `plot()` API

- **`df.plot(kind="line|bar|barh|hist|box|scatter|area|pie|kde")`**: One-line plotting from a DataFrame; index is the x-axis by default.
- **Method shortcuts**: `df.plot.bar()`, `df.plot.scatter(x=, y=)`, `df.plot.hist()`, etc.
- **`ax=axes[i]`**: Route a plot into a specific subplot of a `plt.subplots` figure.
- **`fig, axes = plt.subplots(rows, cols, figsize=...)`**: Create a multi-panel figure; `axes` is an array you index into.
- **`plt.tight_layout()`**: Auto-space subplots so labels don't overlap.

## Styling

- **`ax.set_title / ax.set_xlabel / ax.set_ylabel`**: Labels and titles.
- **`ax.legend()`**: Show the series legend.
- **`ax.grid(alpha=0.3)`**: Gridlines.
- **`ax.axhline(y)` / `ax.axvline(x)`**: Reference lines (mean, threshold, event date).
- **`color`, `linewidth`, `alpha`, `linestyle="--"`**: Common plot style parameters.
- **`figsize=(w, h)`**: Figure dimensions in inches.

## Chart Kinds

- **Line**: time series / trends.
- **Bar / Barh**: categorical comparison (vertical/horizontal).
- **Hist**: distribution of one variable (`bins=20`).
- **Box**: distribution summary with quartiles + outliers.
- **Scatter**: relationship between two numeric variables.
- **Area**: cumulative parts over time.
- **Pie**: share of a whole (`autopct="%1.0f%%"` shows percentages).
- **KDE**: smoothed density estimate.

## Saving

- **`fig = plot.get_figure()`**: Grab the figure object from a pandas plot.
- **`fig.savefig(path, dpi=150, bbox_inches="tight")`**: Save with quality; `bbox_inches="tight"` prevents clipped labels.
- **Backend**: headless scripts need `import matplotlib; matplotlib.use("Agg")` before plotting.

## Real-World Patterns

- **EDA dashboards**: 2×2 subplots of trend, by-region bars, distribution hist, channel pie.
- **Reference lines**: mean threshold lines make charts self-explanatory.
- **Aggregate before plotting**: `groupby(...).sum()` first — never plot raw 10k-row lines.
