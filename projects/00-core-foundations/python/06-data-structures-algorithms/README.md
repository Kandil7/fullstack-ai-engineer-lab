# Python Data Structures & Algorithms (DSA) Tutorial

Complete implementations of all major DSA concepts from the W3Schools Python DSA tutorial.

## Table of Contents

| # | File | Topic | Complexity |
|---|------|-------|------------|
| 01 | [01-introduction.py](01-introduction.py) | Introduction to DSA, Big O Notation | - |
| 02 | [02-arrays.py](02-arrays.py) | Arrays, Two Pointers, Sliding Window | O(1) to O(n) |
| 03 | [03-stacks.py](03-stacks.py) | Stacks, Bracket Matching, Expression Evaluation | O(n) |
| 04 | [04-queues.py](04-queues.py) | Queues, Deque, Priority Queue, Circular Queue | O(1) to O(n) |
| 05 | [05-linked-lists.py](05-linked-lists.py) | Singly, Doubly, Circular Linked Lists | O(n) |
| 06 | [06-hash-tables.py](06-hash-tables.py) | Hash Tables, LRU Cache, Consistent Hashing | O(1) avg |
| 07 | [07-trees.py](07-trees.py) | General Trees, N-ary Trees, Traversals | O(n) |
| 08 | [08-binary-trees.py](08-binary-trees.py) | Binary Trees, Traversals, Views | O(n) |
| 09 | [09-binary-search-trees.py](09-binary-search-trees.py) | BST, Search, Insert, Delete | O(log n) avg |
| 10 | [10-avl-trees.py](10-avl-trees.py) | AVL Trees, Rotations, Self-balancing | O(log n) |
| 11 | [11-graphs.py](11-graphs.py) | Graphs, BFS, DFS, Dijkstra, Topological Sort | O(V + E) |
| 12 | [12-linear-search.py](12-linear-search.py) | Linear Search, Interpolation Search | O(n) |
| 13 | [13-binary-search.py](13-binary-search.py) | Binary Search, Variants, Rotated Arrays | O(log n) |
| 14 | [14-bubble-sort.py](14-bubble-sort.py) | Bubble Sort, Cocktail Shaker, Comb Sort | O(n^2) |
| 15 | [15-selection-sort.py](15-selection-sort.py) | Selection Sort, Double Selection, Cyclic Sort | O(n^2) |
| 16 | [16-insertion-sort.py](16-insertion-sort.py) | Insertion Sort, Shell Sort, Binary Insertion | O(n^2) |
| 17 | [17-quick-sort.py](17-quick-sort.py) | Quick Sort, Lomuto/Hoare Partition, Quick Select | O(n log n) avg |
| 18 | [18-counting-sort.py](18-counting-sort.py) | Counting Sort, Radix Sort Subroutine | O(n + k) |
| 19 | [19-radix-sort.py](19-radix-sort.py) | Radix Sort (LSD/MSD), String Sorting | O(d * n) |
| 20 | [20-merge-sort.py](20-merge-sort.py) | Merge Sort, Bottom-Up, Inversion Count | O(n log n) |

## How to Run

```bash
# Run any individual file
python 01-introduction.py

# Run all files
for f in *.py; do echo "=== $f ==="; python "$f"; echo; done
```

## Data Structures Covered

- **Linear**: Arrays, Linked Lists, Stacks, Queues
- **Hash-based**: Hash Tables, Hash Sets
- **Trees**: Binary Trees, BST, AVL Trees
- **Graphs**: Adjacency List/Matrix, Weighted/Unweighted

## Algorithms Covered

### Searching
- Linear Search: O(n)
- Binary Search: O(log n)
- Interpolation Search: O(log log n) average

### Sorting
- Bubble Sort: O(n^2)
- Selection Sort: O(n^2)
- Insertion Sort: O(n^2)
- Quick Sort: O(n log n) average
- Merge Sort: O(n log n)
- Counting Sort: O(n + k)
- Radix Sort: O(d * n)
- Shell Sort: O(n^1.25)

### Graph Algorithms
- BFS (Breadth-First Search): O(V + E)
- DFS (Depth-First Search): O(V + E)
- Dijkstra's Algorithm: O((V + E) log V)
- Topological Sort: O(V + E)

## Key Concepts

### Time Complexity Hierarchy
```
O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) < O(n!)
```

### When to Use What

| Data Structure | Use Case |
|----------------|----------|
| Array | Random access, iteration |
| Linked List | Frequent insert/delete |
| Stack | Undo/redo, recursion, parsing |
| Queue | BFS, scheduling, buffering |
| Hash Table | Fast lookups, caching |
| BST | Sorted data, range queries |
| AVL Tree | Guaranteed O(log n) |
| Graph | Relationships, networks |

| Algorithm | Best For |
|-----------|----------|
| Binary Search | Sorted arrays |
| Quick Sort | General purpose (fastest average) |
| Merge Sort | Stable sort, linked lists |
| Counting Sort | Small integer ranges |
| BFS | Shortest path (unweighted) |
| Dijkstra | Shortest path (weighted) |
| DFS | Cycle detection, topological sort |

## Exercises

Each file contains multiple implementations and examples:
1. Basic implementation
2. Optimized variants
3. Step-by-step visualization
4. Performance analysis
5. Practical applications
6. Common interview problems

## Running Tests

All files include comprehensive test cases and examples. Simply run any file to see the output:

```bash
python 09-binary-search-trees.py
```

## License

Educational use - W3Schools Python DSA Tutorial implementations.
