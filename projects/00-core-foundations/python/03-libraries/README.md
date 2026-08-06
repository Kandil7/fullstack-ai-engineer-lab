# 📊 Phase 3: Data Science Libraries

200+ files across 5 major Python data science libraries, each organized into self-contained topic directories.

## 📋 Directory Structure

```
03-libraries/
├── numpy/                        # 34 topics: Arrays, ufuncs, linear algebra
│   ├── 01-introduction/
│   │   ├── 01-introduction.py
│   │   ├── 01-introduction-lecture.md
│   │   └── 01-introduction-glossary.md
│   └── ... (34 topics)
│
├── pandas/                       # DataFrames, cleaning, analysis
│   ├── basics/                   # 24 topics: W3Schools series
│   ├── advanced/                 # 21 topics: Professional series
│   ├── production/               # 6 topics: Method chaining, memory, pitfalls
│   └── case-studies/             # 2 topics: Real-world examples
│
├── matplotlib/                   # Visualization
│   ├── basics/                   # 12 topics: W3Schools series
│   ├── advanced/                 # 16 topics: OO API, styling, ML viz
│   └── 3d/                       # 5 topics: 3D plotting
│
├── scipy/                        # 16 topics: Scientific computing
│   ├── 01-introduction/
│   └── ... (16 topics)
│
└── polars/                       # 6 topics: Modern DataFrame library
    ├── 01-introduction/
    └── ... (6 topics)
```

## 📚 Libraries

| Library | Topics | Focus |
|---------|--------|-------|
| **NumPy** | 34 | Arrays, indexing, reshaping, ufuncs, random, set operations |
| **Pandas** | 53 | Series, DataFrames, I/O, cleaning, groupby, merge, plotting |
| **Matplotlib** | 33 | Line, scatter, bar, histogram, pie, 3D, contour plots |
| **SciPy** | 16 | Constants, optimization, integration, stats, I/O |
| **Polars** | 6 | Modern DataFrame library with lazy evaluation |

## 🚀 Quick Start

```bash
# Install dependencies
pip install numpy pandas matplotlib scipy polars

# Run any topic
python numpy/01-introduction/01-introduction.py

# Run all NumPy topics
for d in numpy/[0-9]*/; do
    py=$(ls "$d"/*.py 2>/dev/null | head -1)
    [ -n "$py" ] && echo "=== $d ===" && python "$py"
done
```

## 📝 Notes

- Each topic directory contains exercise, lecture, and glossary
- **numpy/** covers fundamentals through advanced topics
- **pandas/** is split into basics (W3Schools), advanced (professional), and production
- **matplotlib/** is split into basics (W3Schools), advanced (OO API, styling), and 3D
- **scipy/** covers scientific computing essentials
- **polars/** introduces modern DataFrame operations

---

*Last updated: August 2026*
