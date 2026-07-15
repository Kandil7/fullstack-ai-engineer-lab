# Graphs Glossary - Data Structures and Algorithms

## Quick Reference Table

| Term | Definition | Time Complexity |
|------|------------|-----------------|
| Vertex | A node in a graph | - |
| Edge | A connection between vertices | - |
| Adjacency | Two vertices connected by an edge | - |
| Degree | Number of edges connected to a vertex | O(1) |
| Directed Graph | Graph with directed edges | - |
| Undirected Graph | Graph with bidirectional edges | - |
| Weighted Graph | Graph with edge weights | - |
| Adjacency List | Graph representation using lists | O(V + E) space |
| Adjacency Matrix | Graph representation using 2D array | O(V²) space |
| BFS | Breadth-First Search traversal | O(V + E) |
| DFS | Depth-First Search traversal | O(V + E) |
| Cycle | Path from a vertex back to itself | O(V + E) |
| DAG | Directed Acyclic Graph | - |
| Connected Component | Maximal connected subgraph | O(V + E) |
| Topological Sort | Linear ordering of DAG vertices | O(V + E) |
| Shortest Path | Minimum weight path between vertices | Varies |
| Bipartite Graph | 2-colorable graph | O(V + E) |

---

## Detailed Definitions

### A

#### Adjacency
Two vertices are adjacent if they are connected by an edge.

```python
# In adjacency list representation
graph = {
    'A': ['B', 'C'],  # B and C are adjacent to A
    'B': ['A', 'D'],  # A and D are adjacent to B
    'C': ['A'],
    'D': ['B']
}

def are_adjacent(graph, v1, v2):
    return v2 in graph.get(v1, [])

print(are_adjacent(graph, 'A', 'B'))  # True
print(are_adjacent(graph, 'A', 'D'))  # False
```

**Related Terms:** Edge, Vertex, Degree

---

#### Adjacency List
A graph representation where each vertex stores a list of its adjacent vertices.

```python
class AdjacencyListGraph:
    def __init__(self):
        self.graph = {}
    
    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = []
    
    def add_edge(self, v1, v2):
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.graph[v1].append(v2)
        self.graph[v2].append(v1)  # For undirected
    
    def get_neighbors(self, v):
        return self.graph.get(v, [])

# Example
g = AdjacencyListGraph()
g.add_edge('A', 'B')
g.add_edge('A', 'C')
print(g.graph)  # {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}
```

**Space Complexity:** O(V + E)
**Best For:** Sparse graphs

**Related Terms:** Adjacency Matrix, Sparse Graph

---

#### Adjacency Matrix
A graph representation using a 2D array where `matrix[i][j]` indicates an edge from vertex i to vertex j.

```python
class AdjacencyMatrixGraph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.n = len(vertices)
        self.vertex_map = {v: i for i, v in enumerate(vertices)}
        self.matrix = [[0] * self.n for _ in range(self.n)]
    
    def add_edge(self, v1, v2, weight=1):
        i, j = self.vertex_map[v1], self.vertex_map[v2]
        self.matrix[i][j] = weight
        self.matrix[j][i] = weight  # For undirected
    
    def has_edge(self, v1, v2):
        i, j = self.vertex_map[v1], self.vertex_map[v2]
        return self.matrix[i][j] != 0

# Example
g = AdjacencyMatrixGraph(['A', 'B', 'C'])
g.add_edge('A', 'B')
print(g.matrix)  # [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
```

**Space Complexity:** O(V²)
**Best For:** Dense graphs

**Related Terms:** Adjacency List, Dense Graph

---

#### Adjacent
See Adjacency.

---

#### Arc
A directed edge in a graph. Same as "directed edge."

```python
# Arc from A to B (A -> B)
graph.add_edge('A', 'B')  # Creates an arc
```

**Related Terms:** Directed Edge, Edge

---

### B

#### BFS (Breadth-First Search)
A graph traversal algorithm that explores all vertices at the present depth before moving to vertices at the next depth level.

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    traversal = []
    
    while queue:
        vertex = queue.popleft()
        traversal.append(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return traversal

# Example
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print(bfs(graph, 'A'))  # ['A', 'B', 'C', 'D', 'E', 'F']
```

**Time Complexity:** O(V + E)
**Space Complexity:** O(V)

**Applications:**
- Shortest path in unweighted graphs
- Level-order traversal
- Finding connected components

**Related Terms:** DFS, Queue, Level-Order Traversal

---

#### Bipartite Graph
A graph whose vertices can be divided into two disjoint sets such that every edge connects vertices from different sets.

```python
def is_bipartite(graph):
    color = {}
    
    def bfs_check(start):
        queue = [start]
        color[start] = 0
        
        while queue:
            vertex = queue.pop(0)
            for neighbor in graph[vertex]:
                if neighbor not in color:
                    color[neighbor] = 1 - color[vertex]
                    queue.append(neighbor)
                elif color[neighbor] == color[vertex]:
                    return False
        return True
    
    for v in graph:
        if v not in color:
            if not bfs_check(v):
                return False
    return True

# Bipartite example
bipartite = {
    'A': ['C', 'D'],
    'B': ['C', 'D'],
    'C': ['A', 'B'],
    'D': ['A', 'B']
}
print(is_bipartite(bipartite))  # True
```

**Related Terms:** 2-Colorable, Matching

---

#### Bridge
An edge whose removal increases the number of connected components.

```python
def find_bridges(graph):
    n = len(graph)
    disc = [-1] * n
    low = [-1] * n
    timer = [0]
    bridges = []
    
    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        
        for v in graph[u]:
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent:
                low[u] = min(low[u], disc[v])
    
    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)
    
    return bridges
```

**Related Terms:** Articulation Point, Cut Edge

---

### C

#### Connected Component
A maximal subgraph in which any two vertices are connected to each other by paths.

```python
def connected_components(graph):
    visited = set()
    components = []
    
    def dfs(vertex, component):
        visited.add(vertex)
        component.append(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for v in graph:
        if v not in visited:
            component = []
            dfs(v, component)
            components.append(component)
    
    return components

# Example with disconnected graph
graph = {
    'A': ['B'],
    'B': ['A'],
    'C': ['D'],
    'D': ['C'],
    'E': []
}

print(connected_components(graph))
# [['A', 'B'], ['C', 'D'], ['E']]
```

**Time Complexity:** O(V + E)
**Related Terms:** Connected Graph, Disconnected Graph

---

#### Cycle
A path that starts and ends at the same vertex without repeating edges.

```python
def has_cycle_undirected(graph):
    visited = set()
    
    def dfs(vertex, parent):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                if dfs(neighbor, vertex):
                    return True
            elif neighbor != parent:
                return True
        return False
    
    for v in graph:
        if v not in visited:
            if dfs(v, None):
                return True
    return False

# Graph with cycle
cyclic = {
    'A': ['B', 'C'],
    'B': ['A', 'C'],
    'C': ['A', 'B']
}
print(has_cycle_undirected(cyclic))  # True
```

**Related Terms:** Acyclic, DAG, Cycle Detection

---

### D

#### DAG (Directed Acyclic Graph)
A directed graph with no cycles.

```python
def topological_sort_dag(graph):
    """Topological sort - only works on DAGs"""
    visited = set()
    stack = []
    
    def dfs(vertex):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(vertex)
    
    for v in graph:
        if v not in visited:
            dfs(v)
    
    return stack[::-1]

# DAG example (course prerequisites)
dag = {
    'CS101': ['CS201', 'CS202'],
    'CS201': ['CS301'],
    'CS202': ['CS301'],
    'CS301': []
}

print(topological_sort_dag(dag))
# ['CS101', 'CS201', 'CS202', 'CS301'] or similar
```

**Applications:**
- Task scheduling with dependencies
- Build systems
- Course prerequisites

**Related Terms:** Topological Sort, Cycle, Directed Graph

---

#### Degree
The number of edges connected to a vertex.

```python
def get_degree(graph, vertex):
    """For undirected graph"""
    return len(graph[vertex])

def get_in_degree(graph, vertex):
    """For directed graph - edges pointing to vertex"""
    return sum(1 for v in graph if vertex in graph[v])

def get_out_degree(graph, vertex):
    """For directed graph - edges from vertex"""
    return len(graph[vertex])

# Example
directed = {
    'A': ['B', 'C'],
    'B': ['C'],
    'C': []
}

print(f"Out-degree of A: {get_out_degree(directed, 'A')}")  # 2
print(f"In-degree of C: {get_in_degree(directed, 'C')}")    # 2
```

**Related Terms:** In-Degree, Out-Degree, Handshaking Lemma

---

#### Dense Graph
A graph with many edges, close to the maximum possible (V²).

```python
# Dense graph: O(V²) edges
# Adjacency matrix is preferred
dense_graph = [[0, 1, 1, 1],
               [1, 0, 1, 1],
               [1, 1, 0, 1],
               [1, 1, 1, 0]]
```

**Related Terms:** Sparse Graph, Adjacency Matrix

---

#### DFS (Depth-First Search)
A graph traversal algorithm that explores as far as possible along each branch before backtracking.

```python
def dfs_recursive(graph, vertex, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(vertex)
    traversal = [vertex]
    
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            traversal.extend(dfs_recursive(graph, neighbor, visited))
    
    return traversal

def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    traversal = []
    
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            traversal.append(vertex)
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return traversal

# Example
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print(dfs_recursive(graph, 'A'))  # ['A', 'B', 'D', 'E', 'F', 'C']
```

**Time Complexity:** O(V + E)
**Space Complexity:** O(V)

**Applications:**
- Cycle detection
- Topological sorting
- Path finding
- Connected components

**Related Terms:** BFS, Backtracking, Stack

---

#### Directed Graph (Digraph)
A graph where edges have a direction (from one vertex to another).

```python
class DirectedGraph:
    def __init__(self):
        self.graph = {}
    
    def add_edge(self, v1, v2):
        if v1 not in self.graph:
            self.graph[v1] = []
        self.graph[v1].append(v2)
        # Don't add reverse edge
    
    def has_edge(self, v1, v2):
        return v2 in self.graph.get(v1, [])

g = DirectedGraph()
g.add_edge('A', 'B')  # A -> B only
print(g.has_edge('A', 'B'))  # True
print(g.has_edge('B', 'A'))  # False
```

**Related Terms:** Undirected Graph, Arc, Directed Edge

---

### E

#### Edge
A connection between two vertices in a graph.

```python
class Edge:
    def __init__(self, source, destination, weight=None):
        self.source = source
        self.destination = destination
        self.weight = weight
    
    def __repr__(self):
        if self.weight:
            return f"{self.source} --{self.weight}--> {self.destination}"
        return f"{self.source} --> {self.destination}"

# Creating edges
e1 = Edge('A', 'B')
e2 = Edge('A', 'B', weight=5)
print(e1)  # A --> B
print(e2)  # A --5--> B
```

**Related Terms:** Vertex, Weight, Directed Edge

---

### G

#### Graph
A non-linear data structure consisting of vertices (nodes) and edges (connections).

```python
class Graph:
    def __init__(self, directed=False):
        self.adj_list = {}
        self.directed = directed
    
    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
    
    def add_edge(self, v1, v2):
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.adj_list[v1].append(v2)
        if not self.directed:
            self.adj_list[v2].append(v1)
    
    def display(self):
        for vertex in self.adj_list:
            print(f"{vertex}: {self.adj_list[vertex]}")

# Creating a graph
g = Graph(directed=False)
g.add_edge('A', 'B')
g.add_edge('A', 'C')
g.add_edge('B', 'D')
g.display()
```

**Related Terms:** Vertex, Edge, Adjacency

---

### M

#### Multi-Graph
A graph that allows multiple edges between the same pair of vertices.

```python
from collections import defaultdict

class MultiGraph:
    def __init__(self):
        self.graph = defaultdict(list)
    
    def add_edge(self, v1, v2, label=""):
        self.graph[v1].append((v2, label))
        self.graph[v2].append((v1, label))

# Multiple edges between A and B
mg = MultiGraph()
mg.add_edge('A', 'B', 'road1')
mg.add_edge('A', 'B', 'road2')
print(mg.graph['A'])  # [('B', 'road1'), ('B', 'road2')]
```

**Related Terms:** Simple Graph, Parallel Edges

---

### S

#### Simple Graph
A graph with no self-loops and no multiple edges between the same pair of vertices.

```python
class SimpleGraph:
    def __init__(self):
        self.graph = {}
    
    def add_edge(self, v1, v2):
        if v1 == v2:  # No self-loops
            return
        if v1 not in self.graph:
            self.graph[v1] = set()
        if v2 not in self.graph:
            self.graph[v2] = set()
        
        # No duplicate edges
        self.graph[v1].add(v2)
        self.graph[v2].add(v1)

g = SimpleGraph()
g.add_edge('A', 'B')
g.add_edge('A', 'B')  # Ignored (duplicate)
g.add_edge('A', 'A')  # Ignored (self-loop)
```

**Related Terms:** Multi-Graph, Self-Loop

---

#### Sparse Graph
A graph with relatively few edges compared to the maximum possible.

```python
# Sparse graph: O(V) edges
# Adjacency list is preferred
sparse_graph = {
    'A': ['B'],
    'B': ['A', 'C'],
    'C': ['B', 'D'],
    'D': ['C']
}
# Only 3 edges for 4 vertices (max would be 6)
```

**Related Terms:** Dense Graph, Adjacency List

---

### T

#### Topological Sort
A linear ordering of vertices in a DAG such that for every directed edge (u, v), vertex u comes before v.

```python
def topological_sort_kahn(graph):
    """Kahn's algorithm (BFS-based)"""
    in_degree = {v: 0 for v in graph}
    for v in graph:
        for neighbor in graph[v]:
            in_degree[neighbor] += 1
    
    queue = [v for v in graph if in_degree[v] == 0]
    order = []
    
    while queue:
        vertex = queue.pop(0)
        order.append(vertex)
        
        for neighbor in graph[vertex]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) != len(graph):
        return None  # Graph has cycle
    
    return order

# DAG
dag = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}

print(topological_sort_kahn(dag))  # ['A', 'B', 'C', 'D'] or similar
```

**Time Complexity:** O(V + E)
**Applications:**
- Task scheduling
- Build systems
- Course prerequisites

**Related Terms:** DAG, In-Degree, Kahn's Algorithm

---

### U

#### Undirected Graph
A graph where edges have no direction (bidirectional).

```python
class UndirectedGraph:
    def __init__(self):
        self.graph = {}
    
    def add_edge(self, v1, v2):
        if v1 not in self.graph:
            self.graph[v1] = []
        if v2 not in self.graph:
            self.graph[v2] = []
        
        self.graph[v1].append(v2)
        self.graph[v2].append(v1)  # Both directions

g = UndirectedGraph()
g.add_edge('A', 'B')
print(g.graph)  # {'A': ['B'], 'B': ['A']}
```

**Related Terms:** Directed Graph, Bidirectional

---

### V

#### Vertex (Node)
A fundamental unit of which graphs are made.

```python
class Vertex:
    def __init__(self, key):
        self.key = key
        self.neighbors = []
        self.visited = False
    
    def add_neighbor(self, vertex):
        self.neighbors.append(vertex)

# Creating vertices
v1 = Vertex('A')
v2 = Vertex('B')
v1.add_neighbor(v2)
```

**Related Terms:** Edge, Degree, Adjacency

---

### W

#### Weighted Graph
A graph where edges have associated weights (costs, distances, etc.).

```python
class WeightedGraph:
    def __init__(self):
        self.graph = {}
    
    def add_edge(self, v1, v2, weight):
        if v1 not in self.graph:
            self.graph[v1] = []
        if v2 not in self.graph:
            self.graph[v2] = []
        
        self.graph[v1].append((v2, weight))
        self.graph[v2].append((v1, weight))

g = WeightedGraph()
g.add_edge('A', 'B', 5)
g.add_edge('A', 'C', 3)
print(g.graph['A'])  # [('B', 5), ('C', 3)]
```

**Related Terms:** Unweighted Graph, Dijkstra's Algorithm

---

## Common Patterns

### Pattern 1: BFS for Shortest Path
```python
def shortest_path_bfs(graph, start, end):
    if start == end:
        return [start]
    
    visited = {start}
    queue = [(start, [start])]
    
    while queue:
        vertex, path = queue.pop(0)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))
    return None
```

### Pattern 2: DFS for Cycle Detection
```python
def has_cycle(graph):
    visited = set()
    rec_stack = set()
    
    def dfs(vertex):
        visited.add(vertex)
        rec_stack.add(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(vertex)
        return False
    
    for v in graph:
        if v not in visited:
            if dfs(v):
                return True
    return False
```

### Pattern 3: Connected Components
```python
def count_components(graph):
    visited = set()
    count = 0
    
    def dfs(vertex):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs(neighbor)
    
    for v in graph:
        if v not in visited:
            dfs(v)
            count += 1
    
    return count
```

---

## Complexity Cheat Sheet

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| BFS | O(V + E) | O(V) | Shortest path (unweighted) |
| DFS | O(V + E) | O(V) | Cycle detection, topological sort |
| Dijkstra | O((V + E) log V) | O(V) | Shortest path (weighted) |
| Topological Sort | O(V + E) | O(V) | Task scheduling |
| Connected Components | O(V + E) | O(V) | Network analysis |
| Bipartite Check | O(V + E) | O(V) | 2-coloring |

---

## Interview Tips

1. **Clarify the graph type** (directed/undirected, weighted/unweighted)
2. **Choose the right representation** (list for sparse, matrix for dense)
3. **Always handle disconnected graphs**
4. **Use BFS for shortest path in unweighted graphs**
5. **Use DFS for cycle detection and topological sort**
6. **Consider using sets for O(1) visited checks**
7. **Watch out for infinite loops** in cyclic graphs