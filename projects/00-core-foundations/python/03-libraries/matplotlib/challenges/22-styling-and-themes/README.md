# Challenge 22: Styling and Themes

## 🥉 Bronze — rcParams Defaults (~15 min)

**Task:** Apply three publication defaults to the process and prove
they took effect.

**Signature:**
```python
def apply_dpi_defaults() -> None:
```

**Requirements:**
- `figure.dpi = 120`, `savefig.dpi = 150`, `font.size = 11`
- Also set `axes.grid = True`

| Input | Expected |
|-------|----------|
| none | `rcParams` reflects all four values |

**Constraints:** must be callable before any figure creation (tests
assert the values right after the call).

---

## 🥈 Silver — Perceptually Uniform Policy (~35 min)

**Task:** Return the canonical perceptually-uniform colormap names as
a sorted list.

**Signature:**
```python
def uniform_maps() -> list[str]:
```

**Requirements:**
- Return exactly the canonical PU set, sorted:
  `["cividis", "inferno", "magma", "plasma", "viridis"]`
- Do NOT include `jet` (banding, not colorblind-safe)

| Input | Expected |
|-------|----------|
| none | the 5 canonical names, sorted |

**Constraints:** exact membership; `"jet" not in result` must hold.

---

## 🥇 Gold — Annotate the Minimum (~75 min)

**Task:** Plot `y` vs `x` and annotate the observed minimum with an
arrow; return the axes so the annotation is testable.

**Signature:**
```python
def annotate_minimum(x: np.ndarray, y: np.ndarray) -> plt.Axes:
```

**Requirements:**
- `ax.plot(x, y, alpha=0.8)`; compute `i_min = int(np.argmin(y))`
- `ax.annotate("observed min", xy=(x[i_min], y[i_min]),
  xytext=..., arrowprops={"arrowstyle": "->"})`
- Return `ax` (do not close the figure — the test inspects it)

| Input (seeded parabola + noise) | Expected |
|-------|----------|
| `x = linspace(0, 10, 200)`, `y = (x-4)**2 + noise` | exactly 1 text artist whose xy is the argmin |

**Constraints:** the annotation `xy` must equal `(x[i_min], y[i_min])`
exactly; `len(ax.texts) == 1`.
**Follow-up:** how would you make the label track a *new* minimum
after the data changes? (Answer: recompute `i_min` and re-call
`annotate` with the same code path — the annotation is a pure function
of the data.)

---

## Running

```bash
python -m pytest 03-libraries/matplotlib/challenges/22-styling-and-themes/test_challenge.py -v
```

## Test File Structure

```
challenges/22-styling-and-themes/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
