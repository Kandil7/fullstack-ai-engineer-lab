# Matplotlib Lecture 06: Labels, Titles, and Legends — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Title | Plot heading | `plt.title('Title')` |
| Suptitle | Figure-level heading | `plt.suptitle('Main Title')` |
| xlabel | X-axis label | `plt.xlabel('Time (s)')` |
| ylabel | Y-axis label | `plt.ylabel('Amplitude')` |
| Legend | Identifies data series | `plt.legend()` |
| LaTeX | Mathematical typesetting | `r'$\sin(x)$'` |
| rcParams | Global configuration | `plt.rcParams['font.size'] = 12` |
| Font Properties | Text style settings | `fontsize=14, fontweight='bold'` |
| labelpad | Padding between label and axis | `labelpad=10` |
| Mathtext | Built-in math rendering | `r'$\alpha > \beta$'` |

## Glossary

### F

**Font Properties** — Settings that control text appearance: family, size, weight, style, color, etc.

### L

**LaTeX** — A mathematical typesetting system. In Matplotlib, `r'$\sin(x)$'` renders mathematical expressions.

**labelpad** — Distance (in points) between the axis label and the axis itself or tick labels.

**Legend** — A box that maps line/marker styles to data series names.

### M

**Mathtext** — Matplotlib's built-in math expression parser for rendering equations without LaTeX.

### R

**rcParams** — Matplotlib's runtime configuration dictionary for global defaults (font sizes, colors, etc.).

### S

**Suptitle** — A title for the entire figure, positioned above all subplots.

### T

**Title** — A text label at the top of a plot describing its content.
