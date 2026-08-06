# Matplotlib Lecture 07: Grid and Layout — Glossary

## Quick Reference

| Term | Definition | Example |
|------|-----------|---------|
| Grid | Reference lines on plot | `plt.grid(True)` |
| Major Grid | Grid at major ticks | `which='major'` |
| Minor Grid | Grid at minor ticks | `which='minor'` |
| Spine | Axis boundary line | `ax.spines['top']` |
| `tight_layout` | Auto-adjust spacing | `plt.tight_layout()` |
| `constrained_layout` | Layout constraint solver | `subplots(constrained_layout=True)` |
| `subplots_adjust` | Manual layout adjustment | `plt.subplots_adjust(wspace=0.3)` |
| Tick Locator | Controls tick positions | `MultipleLocator(0.5)` |

## Glossary

### C

**constrained_layout** — An automatic layout manager that prevents overlapping plot elements.

### G

**Grid** — Reference lines at tick positions that help readers estimate data values.

### M

**Major Grid** — Grid lines at major tick positions (the main tick marks on axes).

**Minor Grid** — Grid lines at minor tick positions (between major ticks).

### S

**Spine** — The lines connecting axis tick marks that frame the plot area (top, bottom, left, right).

**subplots_adjust** — Manual control of figure layout with parameters: left, right, top, bottom, wspace, hspace.

### T

**Tick Locator** — Controls where ticks appear on an axis (MultipleLocator, AutoLocator, FixedLocator, etc.).

**tight_layout** — Automatically adjusts subplot parameters to fit elements within the figure.
