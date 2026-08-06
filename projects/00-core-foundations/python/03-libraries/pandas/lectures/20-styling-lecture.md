# Pandas Styling: DataFrame.style, Conditional Formatting, Export

> **Topic 20 — Advanced pandas series.** Making DataFrames presentable for
> reports and dashboards with `.style` — highlight, color, bar charts, and
> clean exports.

Companion exercise: `advanced/20-styling.py`

---

## 1. Why Style?

Raw tables are hard to read. `.style` adds presentation without touching your
data — highlighting winners, coloring negatives, adding in-cell bars — turning
a DataFrame into a report artifact.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "region": ["north", "south", "east", "west"],
    "revenue": [120, 95, 140, 80],
    "growth": [0.12, -0.03, 0.25, -0.08],
    "users": [5000, 4200, 6100, 3800],
})
```

## 2. Basic Styling Methods

```python
styled = (
    df.style
    .highlight_max(subset=["revenue", "users"], color="lightgreen")
    .highlight_min(subset=["revenue"], color="salmon")
    .set_properties(**{"text-align": "center"})
    .set_table_styles([{"selector": "th", "props": [("background-color", "#4F81BD"), ("color", "white")]}])
)
```

- `highlight_max` / `highlight_min` — color extremes.
- `set_properties` — uniform cell CSS.
- `set_table_styles` — header/caption styling.

## 3. Conditional Formatting with Functions

Style with a callable for full control — it receives each value and returns a
CSS string:

```python
def color_growth(v):
    if v > 0.10: return "color: green; font-weight: bold"
    if v < 0:    return "color: red"
    return ""

styled = df.style.applymap(color_growth, subset=["growth"])
```

For column-wise rules use `apply(..., axis=0)` with functions that map a whole
Series/column to styles.

## 4. In-Cell Data Bars & Color Maps

```python
# Bars proportional to value
styled = df.style.bar(subset=["revenue"], color="#5DADE2")

# Sequential colormap on a column
styled = df.style.background_gradient(subset=["growth"], cmap="RdYlGn")

# Format numbers nicely
styled = df.style.format({
    "revenue": "${:,.0f}",
    "growth": "{:+.1%}",
    "users": "{:,.0f}",
})
```

`bar` gives instant visual comparison; `background_gradient` shows magnitude;
`format` fixes ugly floats (`0.1200000` → `+12.0%`).

## 5. Exporting Styled Tables

```python
# To HTML (email, dashboard, docs)
html = df.style.bar(subset=["revenue"]).to_html()
with open("report.html", "w") as f:
    f.write(html)

# To Excel with openpyxl engine (styles preserved)
df.style.bar(subset=["revenue"]).to_excel("report.xlsx", engine="openpyxl")
```

`to_html` embeds a complete styled table; `to_excel(engine="openpyxl")`
writes the formatting into the workbook.

## 6. Real-World Use Case — KPI Report

```python
kpis = pd.DataFrame({
    "metric": ["Revenue", "New users", "Churn", "NPS"],
    "value": [1_240_000, 18_500, 0.034, 42],
    "target": [1_100_000, 15_000, 0.05, 40],
})

def status(v, s):
    good = ["color: green; font-weight: bold", "color: red"]
    return [good[0] if a >= b else good[1] for a, b in zip(v, s)]

report = (
    kpis.style
    .format({"value": "{:,.0f}", "target": "{:,.0f}"})
    .bar(subset=["value"], color="#5DADE2")
    .apply(status, subset=["value", "target"], axis=0)
    .hide(axis="index")
    .to_html()
)
```

## 7. Pitfalls to Avoid

- **`.style` is display-only**: it returns a `Styler`, not a new DataFrame — chain `.data` to get the original back.
- **`applymap` vs `apply`**: `applymap` = per-cell; `apply` = per-column/row. Mixing them up is the #1 style bug.
- **`hide(axis="index")`**: hides the row index; older `hide_index()` is deprecated.
- **Chained styles must be captured**: assign the final `Styler` or call `.to_html()`/`.to_excel()` on the chain.

## Key Takeaways

1. `.style` = presentation layer; the data stays untouched.
2. `highlight_max/min`, `bar`, `background_gradient`, `format` cover 90% of needs.
3. Custom functions give pixel-level CSS control.
4. Export to HTML or Excel with the styles intact.
