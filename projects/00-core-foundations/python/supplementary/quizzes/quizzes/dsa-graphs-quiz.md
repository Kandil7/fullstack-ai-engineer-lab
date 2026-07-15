# DSA: Graphs - Quiz

## Topic Overview
Graphs are versatile data structures modeling relationships between entities. They consist of vertices (nodes) and edges (connections). This quiz covers graph representations, traversals, shortest paths, minimum spanning trees, and topological sorting.

**Difficulty Levels:** Easy | Medium | Hard
**Total Questions:** 20

---

## Questions

### Q1. What is a graph in data structures?
- **A)** A hierarchical structure with one root
- **B)** A collection of vertices connected by edges
- **C)** A linear sequence of elements
- **D)** A set of key-value pairs

**Correct Answer: B** — A graph is a non-linear data structure consisting of vertices (nodes) and edges (connections between nodes).

---

### Q2. What is the difference between a directed and undirected graph?
- **A)** Directed graphs have weighted edges; undirected do not
- **B)** Directed edges have direction (one-way); undirected edges are bidirectional
- **C)** Directed graphs cannot have cycles
- **D)** Undirected graphs must be connected

**Correct Answer: B** — In directed graphs, edges have a direction (A→B doesn't imply B→A). In undirected graphs, edges go both ways.

---

### Q3. What are the two main ways to represent a graph?
- **A)** Array and string
- **B)** Adjacency matrix and adjacency list
- **C)** Stack and queue
- **D)** Tree and heap

**Correct Answer: B** — Adjacency matrix (2D array) and adjacency list (map of vertex to neighbors) are the two primary graph representations.

---

### Q4. Which representation is more space-efficient for sparse graphs?
- **A)** Adjacency matrix
- **B)** Adjacency list
- **C)** Both are equally efficient
- **D)** Edge list

**Correct Answer: B** — Adjacency list uses O(V + E) space, while adjacency matrix uses O(V²). For sparse graphs (E << V²), adjacency lists are far more efficient.

---

### Q5. What is BFS (Breadth-First Search)?
- **A)** Exploring as far as possible along each branch before backtracking
- **B)** Exploring all neighbors at the current depth before moving to the next level
- **C)** Searching for the shortest path in a weighted graph
- **D)** Finding connected components

**Correct Answer: B** — BFS explores level by level using a queue, visiting all neighbors at the current depth before moving deeper.

---

### Q6. What is DFS (Depth-First Search)?
- **A)** Exploring all neighbors before going deeper
- **B)** Going as deep as possible along each branch before backtracking
- **C)** Finding the shortest path
- **D)** Sorting vertices

**Correct Answer: B** — DFS explores as deep as possible along each branch using a stack (or recursion), then backtracks when it reaches a dead end.

---

### Q7. What data structure does BFS use internally?
- **A)** Stack
- **B)** Queue
- **C)** Priority queue
- **D)** Hash table

**Correct Answer: B** — BFS uses a queue to maintain the frontier: enqueue unvisited neighbors, dequeue the next vertex to explore.

---

### Q8. What data structure does DFS use internally?
- **A)** Queue
- **B)** Stack (or recursion)
- **C)** Heap
- **D)** Linked list

**Correct Answer: B** — DFS uses a stack (either explicit or via recursion) to track which vertices to visit next.

---

### Q9. What is Dijkstra's algorithm used for?
- **A)** Finding the minimum spanning tree
- **B)** Finding the shortest path from a source to all other vertices in a weighted graph with non-negative weights
- **C)** Detecting cycles in a graph
- **D)** Topological sorting

**Correct Answer: B** — Dijkstra's algorithm finds single-source shortest paths in graphs with non-negative edge weights using a priority queue.

---

### Q10. What is the time complexity of Dijkstra's algorithm using a binary heap?
- **A)** O(V²)
- **B)** O((V + E) log V)
- **C)** O(V log V)
- **D)** O(E log E)

**Correct Answer: B** — With a binary heap priority queue, Dijkstra's runs in O((V + E) log V) time.

---

### Q11. What is a minimum spanning tree (MST)?
- **A)** A tree that connects all vertices with the maximum total edge weight
- **B)** A tree that connects all vertices with the minimum total edge weight
- **C)** A tree with the fewest levels
- **D)** A tree with no cycles

**Correct Answer: B** — An MST connects all vertices with the minimum possible sum of edge weights, without forming cycles.

---

### Q12. Which algorithm finds the minimum spanning tree?
- **A)** Dijkstra's algorithm
- **B)** Kruskal's or Prim's algorithm
- **C)** Floyd-Warshall
- **D)** Bellman-Ford

**Correct Answer: B** — Kruskal's (sort edges, add if no cycle) and Prim's (grow tree from a vertex) both find MSTs. Kruskal's uses union-find; Prim's uses a priority queue.

---

### Q13. What is topological sorting?
- **A)** Sorting vertices by their degree
- **B)** A linear ordering of vertices such that for every directed edge (u,v), u comes before v
- **C)** Sorting edges by weight
- **D)** Sorting vertices alphabetically

**Correct Answer: B** — Topological sort produces a linear ordering where every directed edge points forward. Only possible for directed acyclic graphs (DAGs).

---

### Q14. What is the time complexity of DFS/BFS?
- **A)** O(V)
- **B)** O(E)
- **C)** O(V + E)
- **D)** O(V × E)

**Correct Answer: C** — Both DFS and BFS visit each vertex once and examine each edge once, giving O(V + E) time complexity.

---

### Q15. What is a weighted graph?
- **A)** A graph where edges have associated numerical values (weights)
- **B)** A graph with many vertices
- **C)** A graph with no edges
- **D)** A directed graph

**Correct Answer: A** — In weighted graphs, each edge has a weight/cost/distance, enabling problems like shortest path and MST.

---

### Q16. Which algorithm finds shortest paths between ALL pairs of vertices?
- **A)** Dijkstra's algorithm
- **B)** BFS
- **C)** Floyd-Warshall algorithm
- **D)** Prim's algorithm

**Correct Answer: C** — Floyd-Warshall computes shortest paths between all pairs in O(V³) time using dynamic programming. It handles negative weights (but not negative cycles).

---

### Q17. What is a cycle in a graph?
- **A)** A path that starts and ends at the same vertex
- **B)** A path with the most edges
- **C)** A disconnected component
- **D)** A vertex with no edges

**Correct Answer: A** — A cycle is a path that begins and ends at the same vertex without repeating edges.

---

### Q18. What is the Bellman-Ford algorithm used for?
- **A)** Finding MST
- **B)** Finding shortest paths, handling negative edge weights
- **C)** Detecting bipartite graphs
- **D)** Topological sorting

**Correct Answer: B** — Bellman-Ford finds single-source shortest paths even with negative edge weights. It runs in O(V × E) and can detect negative cycles.

---

### Q19. What is the adjacency matrix space complexity for a graph with V vertices?
- **A)** O(V)
- **B)** O(E)
- **C)** O(V + E)
- **D)** O(V²)

**Correct Answer: D** — An adjacency matrix is a V×V 2D array, requiring O(V²) space regardless of the number of edges.

---

### Q20. What is a bipartite graph?
- **A)** A graph with two connected components
- **B)** A graph whose vertices can be divided into two sets such that no two vertices within the same set are adjacent
- **C)** A graph with exactly two edges
- **D)** A directed acyclic graph

**Correct Answer: B** — A bipartite graph can be 2-colored (e.g., red/blue) such that adjacent vertices always have different colors. BFS/DFS can check this.

---

## Answer Key

| Q | Answer | Q | Answer |
|---|--------|---|--------|
| 1 | B | 11 | B |
| 2 | B | 12 | B |
| 3 | B | 13 | B |
| 4 | B | 14 | C |
| 5 | B | 15 | A |
| 6 | B | 16 | C |
| 7 | B | 17 | A |
| 8 | B | 18 | B |
| 9 | B | 19 | D |
| 10 | B | 20 | B |

---

## Score Tracking

| Difficulty | Questions | Correct | Score |
|------------|-----------|---------|-------|
| Easy (1-7) | 7 | ___/7 | ___% |
| Medium (8-14) | 7 | ___/7 | ___% |
| Hard (15-20) | 6 | ___/6 | ___% |
| **Total** | **20** | **___/20** | **___%** |

**Target:** 80%+ to demonstrate strong graph knowledge
