package main

import "fmt"

// Graph — adjacency list representation
type Graph struct {
	vertices int
	adjList  map[int][]int
}

func NewGraph(vertices int) *Graph {
	return &Graph{
		vertices: vertices,
		adjList:  make(map[int][]int),
	}
}

func (g *Graph) AddEdge(u, v int) {
	g.adjList[u] = append(g.adjList[u], v)
}

func (g *Graph) AddUndirectedEdge(u, v int) {
	g.AddEdge(u, v)
	g.AddEdge(v, u)
}

// BFS — breadth-first traversal from source
func (g *Graph) BFS(start int) []int {
	visited := make([]bool, g.vertices)
	queue := []int{start}
	var result []int

	visited[start] = true
	for len(queue) > 0 {
		vertex := queue[0]
		queue = queue[1:]
		result = append(result, vertex)

		for _, neighbor := range g.adjList[vertex] {
			if !visited[neighbor] {
				visited[neighbor] = true
				queue = append(queue, neighbor)
			}
		}
	}
	return result
}

// DFS — depth-first traversal from source (iterative)
func (g *Graph) DFS(start int) []int {
	visited := make([]bool, g.vertices)
	stack := []int{start}
	var result []int

	for len(stack) > 0 {
		vertex := stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		if !visited[vertex] {
			visited[vertex] = true
			result = append(result, vertex)

			// Add neighbors in reverse for consistent order
			neighbors := g.adjList[vertex]
			for i := len(neighbors) - 1; i >= 0; i-- {
				if !visited[neighbors[i]] {
					stack = append(stack, neighbors[i])
				}
			}
		}
	}
	return result
}

// HasPathDFS checks if there's a path between two vertices (recursive)
func (g *Graph) HasPathDFS(start, end int) bool {
	visited := make([]bool, g.vertices)
	return g.hasPathHelper(start, end, visited)
}

func (g *Graph) hasPathHelper(current, target int, visited []bool) bool {
	if current == target {
		return true
	}
	visited[current] = true
	for _, neighbor := range g.adjList[current] {
		if !visited[neighbor] {
			if g.hasPathHelper(neighbor, target, visited) {
				return true
			}
		}
	}
	return false
}

// HasCycle detects if the directed graph has a cycle
func (g *Graph) HasCycle() bool {
	visited := make([]bool, g.vertices)
	recStack := make([]bool, g.vertices)

	for i := 0; i < g.vertices; i++ {
		if !visited[i] {
			if g.hasCycleHelper(i, visited, recStack) {
				return true
			}
		}
	}
	return false
}

func (g *Graph) hasCycleHelper(vertex int, visited, recStack []bool) bool {
	visited[vertex] = true
	recStack[vertex] = true

	for _, neighbor := range g.adjList[vertex] {
		if !visited[neighbor] {
			if g.hasCycleHelper(neighbor, visited, recStack) {
				return true
			}
		} else if recStack[neighbor] {
			return true
		}
	}

	recStack[vertex] = false
	return false
}

func main() {
	fmt.Println("=== Graphs Exercise ===")
	fmt.Println()

	// Create a directed graph
	g := NewGraph(7)
	g.AddEdge(0, 1)
	g.AddEdge(0, 2)
	g.AddEdge(1, 3)
	g.AddEdge(1, 4)
	g.AddEdge(2, 5)
	g.AddEdge(2, 6)

	fmt.Println("Graph structure:")
	fmt.Println("    0")
	fmt.Println("   / \\")
	fmt.Println("  1   2")
	fmt.Println(" / \\ / \\")
	fmt.Println("3  4 5  6")
	fmt.Println()

	fmt.Printf("BFS from 0:  %v\n", g.BFS(0))
	fmt.Printf("DFS from 0:  %v\n", g.DFS(0))

	// Path checking
	fmt.Printf("\nHasPath(0, 4): %v\n", g.HasPathDFS(0, 4))
	fmt.Printf("HasPath(2, 3): %v\n", g.HasPathDFS(2, 3))

	// Cycle detection
	fmt.Println("\n--- Cycle Detection ---")
	fmt.Printf("Has cycle: %v\n", g.HasCycle())

	gWithCycle := NewGraph(3)
	gWithCycle.AddEdge(0, 1)
	gWithCycle.AddEdge(1, 2)
	gWithCycle.AddEdge(2, 0) // creates cycle
	fmt.Printf("Graph with cycle: %v\n", gWithCycle.HasCycle())

	// Undirected graph
	fmt.Println("\n--- Undirected Graph ---")
	ug := NewGraph(5)
	ug.AddUndirectedEdge(0, 1)
	ug.AddUndirectedEdge(0, 2)
	ug.AddUndirectedEdge(1, 3)
	ug.AddUndirectedEdge(1, 4)
	fmt.Printf("Undirected BFS from 0: %v\n", ug.BFS(0))
	fmt.Printf("Undirected DFS from 0: %v\n", ug.DFS(0))
}
