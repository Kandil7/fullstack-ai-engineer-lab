package main

import (
	"reflect"
	"testing"
)

func TestGraphBFS(t *testing.T) {
	g := NewGraph(7)
	g.AddEdge(0, 1)
	g.AddEdge(0, 2)
	g.AddEdge(1, 3)
	g.AddEdge(1, 4)
	g.AddEdge(2, 5)
	g.AddEdge(2, 6)

	got := g.BFS(0)
	expected := []int{0, 1, 2, 3, 4, 5, 6}
	if !reflect.DeepEqual(got, expected) {
		t.Errorf("BFS = %v; want %v", got, expected)
	}
}

func TestGraphDFS(t *testing.T) {
	g := NewGraph(7)
	g.AddEdge(0, 1)
	g.AddEdge(0, 2)
	g.AddEdge(1, 3)
	g.AddEdge(1, 4)
	g.AddEdge(2, 5)
	g.AddEdge(2, 6)

	got := g.DFS(0)
	// DFS order can vary, just check all vertices are visited
	if len(got) != 7 {
		t.Errorf("DFS visited %d vertices; want 7", len(got))
	}
	visited := make(map[int]bool)
	for _, v := range got {
		visited[v] = true
	}
	for i := 0; i < 7; i++ {
		if !visited[i] {
			t.Errorf("DFS missed vertex %d", i)
		}
	}
}

func TestGraphHasPath(t *testing.T) {
	g := NewGraph(5)
	g.AddEdge(0, 1)
	g.AddEdge(1, 2)
	g.AddEdge(2, 3)

	if !g.HasPathDFS(0, 3) {
		t.Error("expected path 0->3")
	}
	if g.HasPathDFS(3, 0) {
		t.Error("expected no path 3->0 (directed graph)")
	}
	if g.HasPathDFS(0, 4) {
		t.Error("expected no path to isolated vertex")
	}
}

func TestGraphCycleDetection(t *testing.T) {
	// No cycle
	g1 := NewGraph(3)
	g1.AddEdge(0, 1)
	g1.AddEdge(1, 2)
	if g1.HasCycle() {
		t.Error("expected no cycle")
	}

	// With cycle
	g2 := NewGraph(3)
	g2.AddEdge(0, 1)
	g2.AddEdge(1, 2)
	g2.AddEdge(2, 0)
	if !g2.HasCycle() {
		t.Error("expected cycle")
	}
}

func TestUndirectedGraph(t *testing.T) {
	ug := NewGraph(5)
	ug.AddUndirectedEdge(0, 1)
	ug.AddUndirectedEdge(0, 2)
	ug.AddUndirectedEdge(1, 3)
	ug.AddUndirectedEdge(1, 4)

	got := ug.BFS(0)
	if len(got) != 5 {
		t.Errorf("BFS visited %d vertices; want 5", len(got))
	}
}
