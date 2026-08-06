# Styling — Glossary

> Companion reference for the **DataFrame Styling** lecture. Reach for it
> while working through `advanced/20-styling.py`.

## The Styler Object

- **`df.style`**: Entry point returning a `Styler` — the presentation layer; the DataFrame itself is untouched.
- **`.data`**: Get the original DataFrame back from a Styler.
- **`Styler` is not a DataFrame**: chain `.to_html()` / `.to_excel()` / assign it — don't treat it as data.

## Built-in Styling

- **`highlight_max(subset=...)` / `highlight_min(...)`**: Color the max/min values.
- **`set_properties(**{"text-align": "center"})`**: Uniform CSS for all cells.
- **`set_table_styles([{"selector": "th", "props": [...]}])`**: Style header/caption elements.
- **`bar(subset=..., color=...)`**: In-cell data bars proportional to value.
- **`background_gradient(subset=..., cmap="RdYlGn")`**: Colormap background by magnitude.
- **`format({col: fmt})`**: Format display values (`"${:,.0f}"`, `"{:+.1%}"`).
- **`hide(axis="index")`**: Hide the row index (`hide_index()` is deprecated).

## Custom Functions

- **`applymap(func, subset=...)`**: Per-**cell** styling — function receives one value, returns a CSS string.
- **`apply(func, axis=0|1, subset=...)`**: Per-column/row styling — function receives a Series and returns a list of CSS strings.
- **CSS strings**: `"color: green; font-weight: bold"` — the return type for style functions.

## Export

- **`to_html()`**: Render the styled table as an HTML string (dashboards, emails, docs).
- **`to_excel("x.xlsx", engine="openpyxl")`**: Write styles into a real workbook.
- **`to_string()`**: Plain-text fallback (terminals, logs).

## Real-World Patterns

- **KPI scorecards**: format + bar + conditional green/red vs target.
- **Budget vs actual**: `background_gradient` on variance column.
- **Dashboards**: chain styles then `to_html()` into a template.
