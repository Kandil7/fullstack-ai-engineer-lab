# Challenge 21: The Object-Oriented API

## 🥉 Bronze — Explicit Figure/Axes (~15 min)

**Task:** Draw one line plot against explicit `fig, ax` objects and
return both.

**Signature:**
```python
def explicit_line_plot() -> tuple[plt.Figure, plt.Axes]:
```

**Requirements:**
- Use `plt.subplots(figsize=(6, 4))` — never `plt.plot`
- Plot `np.sin(x)` on `ax` with `x = np.linspace(0, 2*pi, 100)`
- Set a title on `ax`; do NOT call `plt.show()`
- Close the figure after saving? No — return the live objects so the
  tests can inspect them; just do not leak (tests close it)

| Input | Expected |
|-------|----------|
| none | `(Figure, Axes)` with exactly 1 line |

**Constraints:** must return real `plt.Figure` / `plt.Axes`
instances; the figure must carry exactly one line artist.

---

## 🥈 Silver — Named Panels with subplot_mosaic (~35 min)

**Task:** Build a `subplot_mosaic` layout with named panels and return
the axes dict.

**Signature:**
```python
def mosaic_layout() -> dict[str, plt.Axes]:
```

**Requirements:**
- Layout: `[["loss", "loss"], ["grad", "hist"]]` with
  `width_ratios=(2, 1)`
- Draw one line in `"loss"`, one in `"grad"`, one histogram in
  `"hist"` (seeded `rng.normal`)
- Return the `axd` dict

| Input | Expected |
|-------|----------|
| none | `set(axd) == {"loss", "grad", "hist"}` |

**Constraints:** every value must be a real `Axes`; the `loss` panel
must span both columns (that is what the repeated label does).

---

## 🥇 Gold — Shared Axes Propagate (~75 min)

**Task:** Prove that `sharex=True` *joins* axes: changing limits on one
panel changes the other.

**Signature:**
```python
def shared_x_propagates() -> bool:
```

**Requirements:**
- `plt.subplots(2, 1, sharex=True, figsize=(6, 5))`
- Draw `np.cos` on the top panel and `np.sin` on the bottom
- `ax1.set_xlim(2, 8)`
- Return `True` iff `ax2.get_xlim()` equals `ax1.get_xlim()`
  (within 1e-9) AND
  `ax1.get_shared_x_axes().joined(ax1, ax2)` is True
- Close both figures before returning

| Input | Expected |
|-------|----------|
| none | `True` |

**Constraints:** must use `set_xlim`, not `set_xbound`; must close the
figure (tests assert no leaked figures via `plt.get_fignums()`).
**Follow-up:** what would happen with `sharex=False`? (Answer: `ax2`
would keep its default limits — the join is what propagates.)

---

## Running

```bash
python -m pytest 03-libraries/matplotlib/challenges/21-object-oriented-api/test_challenge.py -v
```

## Test File Structure

```
challenges/21-object-oriented-api/
├── README.md          # This file
├── starter.py         # Signatures only
├── solution.py        # Reference implementation
└── test_challenge.py  # Hidden tests
```
