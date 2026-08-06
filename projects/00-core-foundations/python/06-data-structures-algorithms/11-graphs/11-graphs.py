"""
DSA Tutorial 11 - Graphs
=========================

Graph: Collection of vertices (nodes) and edges (connections).

Types:
- Directed vs Undirected
- Weighted vs Unweighted
- Cyclic vs Acyclic
- Connected vs Disconnected

Representations:
- Adjacency Matrix: O(V^2) space
- Adjacency List: O(V + E) space
"""

# =============================================================================
# 1. GRAPH REPRESENTATIONS
# =============================================================================

class Graph:
    """Graph using adjacency list"""

    def __init__(self, directed=False):
        self.adj_list = {}
        self.directed = directed

    def add_vertex(self, vertex):
        """Add a vertex. O(1)"""
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, v1, v2, weight=None):
        """Add an edge. O(1)"""
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.adj_list[v1].append((v2, weight))
        if not self.directed:
            self.adj_list[v2].append((v1, weight))

    def remove_edge(self, v1, v2):
        """Remove an edge. O(E)"""
        self.adj_list[v1] = [(v, w) for v, w in self.adj_list[v1] if v != v2]
        if not self.directed:
            self.adj_list[v2] = [(v, w) for v, w in self.adj_list[v2] if v != v1]

    def get_neighbors(self, vertex):
        """Get neighbors of vertex. O(1)"""
        return self.adj_list.get(vertex, [])

    def get_vertices(self):
        """Get all vertices. O(V)"""
        return list(self.adj_list.keys())

    def has_edge(self, v1, v2):
        """Check if edge exists. O(degree)"""
        return any(v == v2 for v, _ in self.adj_list.get(v1, []))

    def display(self):
        """Display the graph"""
        for vertex in self.adj_list:
            edges = [(v, w) for v, w in self.adj_list[vertex]]
            print(f"{vertex} -> {edges}")


print("=== Graph Basics ===")

# Undirected graph
g = Graph()
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")
g.add_edge("C", "D")
g.add_edge("D", "E")

print("Undirected Graph:")
g.display()
print(f"Vertices: {g.get_vertices()}")
print(f"Neighbors of D: {g.get_neighbors('D')}")

# Weighted directed graph
wg = Graph(directed=True)
wg.add_edge("A", "B", 4)
wg.add_edge("A", "C", 2)
wg.add_edge("B", "D", 3)
wg.add_edge("C", "B", 1)
wg.add_edge("D", "E", 5)

print("\nWeighted Directed Graph:")
wg.display()


# =============================================================================
# 2. ADJACENCY MATRIX
# =============================================================================

class AdjMatrixGraph:
    """Graph using adjacency matrix"""

    def __init__(self, vertices, directed=False):
        self.vertices = vertices
        self.n = len(vertices)
        self.vertex_map = {v: i for i, v in enumerate(vertices)}
        self.matrix = [[0] * self.n for _ in range(self.n)]
        self.directed = directed

    def add_edge(self, v1, v2, weight=1):
        i, j = self.vertex_map[v1], self.vertex_map[v2]
        self.matrix[i][j] = weight
        if not self.directed:
            self.matrix[j][i] = weight

    def has_edge(self, v1, v2):
        i, j = self.vertex_map[v1], self.vertex_map[v2]
        return self.matrix[i][j] != 0

    def get_neighbors(self, vertex):
        i = self.vertex_map[vertex]
        neighbors = []
        for j in range(self.n):
            if self.matrix[i][j] != 0:
                neighbors.append((self.vertices[j], self.matrix[i][j]))
        return neighbors

    def display(self):
        print(f"  {''.join(f'{v:>4}' for v in self.vertices)}")
        for i, v in enumerate(self.vertices):
            row = ''.join(f'{self.matrix[i][j]:>4}' for j in range(self.n))
            print(f"{v}: {row}")


print("\n=== Adjacency Matrix ===")
mg = AdjMatrixGraph(["A", "B", "C", "D", "E"])
mg.add_edge("A", "B")
mg.add_edge("A", "C")
mg.add_edge("B", "D")
mg.add_edge("C", "D")
mg.add_edge("D", "E")
mg.display()


# =============================================================================
# 3. BFS (BREADTH-FIRST SEARCH)
# =============================================================================

def bfs(graph, start):
    """BFS traversal. O(V + E) time, O(V) space"""
    visited = set()
    queue = [start]
    visited.add(start)
    order = []

    while queue:
        vertex = queue.pop(0)
        order.append(vertex)

        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order

print("\n=== BFS ===")
print(f"BFS from A: {bfs(g, 'A')}")


# =============================================================================
# 4. DFS (DEPTH-FIRST SEARCH)
# =============================================================================

def dfs_recursive(graph, start, visited=None):
    """DFS using recursion. O(V + E) time, O(V) space"""
    if visited is None:
        visited = set()

    visited.add(start)
    order = [start]

    for neighbor, _ in graph.get_neighbors(start):
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))

    return order

def dfs_iterative(graph, start):
    """DFS using stack. O(V + E) time, O(V) space"""
    visited = set()
    stack = [start]
    order = []

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    stack.append(neighbor)

    return order

print("\n=== DFS ===")
print(f"DFS recursive from A: {dfs_recursive(g, 'A')}")
print(f"DFS iterative from A: {dfs_iterative(g, 'A')}")


# =============================================================================
# 5. CYCLE DETECTION
# =============================================================================

def has_cycle_undirected(graph):
    """Detect cycle in undirected graph. O(V + E)"""
    visited = set()

    def dfs(vertex, parent):
        visited.add(vertex)
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                if dfs(neighbor, vertex):
                    return True
            elif neighbor != parent:
                return True
        return False

    for v in graph.get_vertices():
        if v not in visited:
            if dfs(v, None):
                return True
    return False

def has_cycle_directed(graph):
    """Detect cycle in directed graph. O(V + E)"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph.get_vertices()}

    def dfs(vertex):
        color[vertex] = GRAY
        for neighbor, _ in graph.get_neighbors(vertex):
            if color[neighbor] == GRAY:
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[vertex] = BLACK
        return False

    for v in graph.get_vertices():
        if color[v] == WHITE:
            if dfs(v):
                return True
    return False

print("\n=== Cycle Detection ===")
print(f"Undirected graph has cycle: {has_cycle_undirected(g)}")

# Create directed graph with cycle
cycle_graph = Graph(directed=True)
cycle_graph.add_edge("A", "B")
cycle_graph.add_edge("B", "C")
cycle_graph.add_edge("C", "A")
print(f"Directed graph has cycle: {has_cycle_directed(cycle_graph)}")


# =============================================================================
# 6. SHORTEST PATH (BFS - UNWEIGHTED)
# =============================================================================

def shortest_path_bfs(graph, start, end):
    """Shortest path in unweighted graph. O(V + E)"""
    if start == end:
        return [start]

    visited = {start}
    queue = [(start, [start])]

    while queue:
        vertex, path = queue.pop(0)

        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))

    return None

print("\n=== Shortest Path (BFS) ===")
path = shortest_path_bfs(g, "A", "E")
print(f"Shortest path A -> E: {path}")


# =============================================================================
# 7. DIJKSTRA'S ALGORITHM (WEIGHTED)
# =============================================================================

import heapq

def dijkstra(graph, start):
    """Shortest paths from start to all vertices. O((V + E) log V)"""
    distances = {v: float('inf') for v in graph.get_vertices()}
    distances[start] = 0
    previous = {v: None for v in graph.get_vertices()}
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, vertex = heapq.heappop(pq)

        if vertex in visited:
            continue
        visited.add(vertex)

        for neighbor, weight in graph.get_neighbors(vertex):
            if neighbor not in visited:
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = vertex
                    heapq.heappush(pq, (new_dist, neighbor))

    return distances, previous

def get_path(previous, end):
    """Reconstruct path from previous dict"""
    path = []
    current = end
    while current:
        path.append(current)
        current = previous[current]
    return path[::-1]

print("\n=== Dijkstra's Algorithm ===")
distances, previous = dijkstra(wg, "A")
print(f"Distances from A: {distances}")
for vertex in wg.get_vertices():
    path = get_path(previous, vertex)
    print(f"  Path to {vertex}: {' -> '.join(path)} (distance: {distances[vertex]})")


# =============================================================================
# 8. TOPOLOGICAL SORT
# =============================================================================

def topological_sort(graph):
    """Topological sort using DFS. O(V + E)"""
    visited = set()
    stack = []

    def dfs(vertex):
        visited.add(vertex)
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(vertex)

    for v in graph.get_vertices():
        if v not in visited:
            dfs(v)

    return stack[::-1]

print("\n=== Topological Sort ===")
# DAG for course prerequisites
dag = Graph(directed=True)
dag.add_edge("A", "B")
dag.add_edge("A", "C")
dag.add_edge("B", "D")
dag.add_edge("C", "D")
dag.add_edge("D", "E")
print(f"Topological order: {topological_sort(dag)}")


# =============================================================================
# 9. CONNECTED COMPONENTS
# =============================================================================

def connected_components(graph):
    """Find all connected components. O(V + E)"""
    visited = set()
    components = []

    def dfs(vertex, component):
        visited.add(vertex)
        component.append(vertex)
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                dfs(neighbor, component)

    for v in graph.get_vertices():
        if v not in visited:
            component = []
            dfs(v, component)
            components.append(component)

    return components

print("\n=== Connected Components ===")
disconnected = Graph()
disconnected.add_edge("A", "B")
disconnected.add_edge("C", "D")
disconnected.add_vertex("E")
print(f"Components: {connected_components(disconnected)}")


# =============================================================================
# 10. BIPARTITE CHECK
# =============================================================================

def is_bipartite(graph):
    """Check if graph is bipartite. O(V + E)"""
    color = {}

    def bfs_check(start):
        queue = [start]
        color[start] = 0

        while queue:
            vertex = queue.pop(0)
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor not in color:
                    color[neighbor] = 1 - color[vertex]
                    queue.append(neighbor)
                elif color[neighbor] == color[vertex]:
                    return False
        return True

    for v in graph.get_vertices():
        if v not in color:
            if not bfs_check(v):
                return False
    return True

print("\n=== Bipartite Check ===")
bipartite = Graph()
bipartite.add_edge("A", "C")
bipartite.add_edge("A", "D")
bipartite.add_edge("B", "C")
bipartite.add_edge("B", "D")
print(f"Is bipartite: {is_bipartite(bipartite)}")


# =============================================================================
# 11. MAJORITY ELEMENT (GRAPH APPLICATION)
# =============================================================================

def find_all_paths(graph, start, end):
    """Find all paths between two vertices. O(V!)"""
    paths = []

    def dfs(vertex, path):
        if vertex == end:
            paths.append(path.copy())
            return
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in path:
                path.append(neighbor)
                dfs(neighbor, path)
                path.pop()

    dfs(start, [start])
    return paths

print("\n=== All Paths ===")
all_paths = find_all_paths(g, "A", "E")
print(f"All paths A -> E: {all_paths}")


# =============================================================================
# 12. MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Graphs - Complete!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Graphs model relationships between entities")
    print("2. BFS explores level-by-level, DFS explores depth-first")
    print("3. Dijkstra finds shortest paths in weighted graphs")
    print("4. Topological sort orders DAGs")
    print("5. Used in: social networks, maps, networks, compilers")
