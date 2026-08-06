# ⚙️ Phase 6: Data Structures & Algorithms

20 self-contained topic directories covering all major DSA concepts from arrays to sorting algorithms.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

```
06-data-structures-algorithms/
├── 01-introduction/
│   ├── 01-introduction.py
│   ├── 01-introduction-lecture.md
│   └── 01-introduction-glossary.md
├── 02-arrays/
├── 03-stacks/
└── ... (20 topics)
```

## 📚 Topics

| # | Topic | Complexity |
|---|-------|------------|
| 01 | Introduction | Big O Notation |
| 02 | Arrays | O(1) to O(n) |
| 03 | Stacks | O(n) |
| 04 | Queues | O(1) to O(n) |
| 05 | Linked Lists | O(n) |
| 06 | Hash Tables | O(1) avg |
| 07 | Trees | O(n) |
| 08 | Binary Trees | O(n) |
| 09 | Binary Search Trees | O(log n) avg |
| 10 | AVL Trees | O(log n) |
| 11 | Graphs | O(V + E) |
| 12 | Linear Search | O(n) |
| 13 | Binary Search | O(log n) |
| 14 | Bubble Sort | O(n²) |
| 15 | Selection Sort | O(n²) |
| 16 | Insertion Sort | O(n²) |
| 17 | Quick Sort | O(n log n) avg |
| 18 | Counting Sort | O(n + k) |
| 19 | Radix Sort | O(d × n) |
| 20 | Merge Sort | O(n log n) |

## 🚀 Quick Start

```bash
# Run any topic
python 01-introduction/01-introduction.py

# Run all topics
for d in [0-9]*/; do
    py=$(ls "$d"/*.py 2>/dev/null | head -1)
    [ -n "$py" ] && echo "=== $d ===" && python "$py"
done
```

## 📖 Recommended Learning Order

### Data Structures (01-11)
1. **01-introduction** - Big O notation
2. **02-arrays** - Basic data structure
3. **03-stacks** - LIFO structure
4. **04-queues** - FIFO structure
5. **05-linked-lists** - Dynamic data structure
6. **06-hash-tables** - Fast lookups
7. **07-trees** - Hierarchical data
8. **08-binary-trees** - Specialized trees
9. **09-binary-search-trees** - Sorted data
10. **10-avl-trees** - Self-balancing trees
11. **11-graphs** - Network structures

### Algorithms (12-20)
12. **12-linear-search** - Basic search
13. **13-binary-search** - Efficient search
14. **14-bubble-sort** - Simple sort
15. **15-selection-sort** - Simple sort
16. **16-insertion-sort** - Simple sort
17. **17-quick-sort** - Fast sort
18. **18-counting-sort** - Integer sort
19. **19-radix-sort** - Integer sort
20. **20-merge-sort** - Stable sort

## 📊 Data Structures Comparison

| Structure | Access | Search | Insert | Delete | Use Case |
|-----------|--------|--------|--------|--------|----------|
| Array | O(1) | O(n) | O(n) | O(n) | Random access |
| Linked List | O(n) | O(n) | O(1) | O(1) | Frequent insert/delete |
| Stack | O(n) | O(n) | O(1) | O(1) | Undo/redo, recursion |
| Queue | O(n) | O(n) | O(1) | O(1) | BFS, scheduling |
| Hash Table | O(1) | O(1) | O(1) | O(1) | Fast lookups |
| BST | O(log n) | O(log n) | O(log n) | O(log n) | Sorted data |
| AVL Tree | O(log n) | O(log n) | O(log n) | O(log n) | Guaranteed O(log n) |

---

*Last updated: August 2026*
