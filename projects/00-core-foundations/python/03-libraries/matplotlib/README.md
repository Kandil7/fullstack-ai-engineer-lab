# 📊 Matplotlib — Visualization Library

33 files organized into 3 subdirectories, each containing self-contained topic directories.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

```
matplotlib/
├── basics/                      # 12 topics: W3Schools series
│   ├── 01-introduction/
│   │   ├── 01-introduction.py
│   │   ├── 01-introduction-lecture.md
│   │   └── 01-introduction-glossary.md
│   └── ... (12 topics)
│
├── advanced/                    # 16 topics: OO API, styling, ML viz
│   ├── 01-pyplot/
│   └── ... (16 topics)
│
└── 3d/                          # 5 topics: 3D plotting
    ├── 13-wireframe/
    └── ... (5 topics)
```

## 📚 Contents by Subdirectory

### basics/ (01-13): W3Schools Series
Beginner-friendly coverage of matplotlib fundamentals.

### advanced/ (01-12, 21-24): OO API, Styling, ML Visualization
Professional plotting techniques and ML visualization.

### 3d/ (13-17): 3D Plotting
3D scatter, surface, and wireframe plots.

## 🚀 Quick Start

```bash
# Start with basics
python basics/01-introduction/01-introduction.py

# Progress to advanced
python advanced/01-pyplot/01-pyplot.py

# 3D plotting
python 3d/13-wireframe/13-wireframe.py
```

## 📝 Notes

- All plots save to `./output/` (headless with `MPLBACKEND=Agg`)
- **basics/** covers core plotting concepts
- **advanced/** covers OO API, styling, and ML visualization
- **3d/** covers 3D plotting techniques

---

*Last updated: August 2026*
