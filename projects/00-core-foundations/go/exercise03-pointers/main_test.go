package main

import (
	"testing"
)

func TestPointers_BasicOperations(t *testing.T) {
	var x int = 42
	var p *int = &x

	if *p != 42 {
		t.Errorf("expected *p = 42, got %d", *p)
	}

	*p = 100
	if x != 100 {
		t.Errorf("expected x = 100 after modification, got %d", x)
	}
}

func TestPointers_NilPointer(t *testing.T) {
	var p *int
	if p != nil {
		t.Error("expected uninitialized pointer to be nil")
	}
}

func TestPointers_StructModification(t *testing.T) {
	type Point struct {
		X, Y int
	}
	p := Point{X: 10, Y: 20}
	ptr := &p
	ptr.Y = 30
	if p.Y != 30 {
		t.Errorf("expected p.Y = 30 via pointer, got %d", p.Y)
	}
}

func TestPointers_ValueVsPointerReceiver(t *testing.T) {
	// Value receiver doesn't modify original
	c1 := Counter{count: 0}
	c1.IncrementValue()
	if c1.count != 0 {
		t.Errorf("value receiver modified original: got %d, want 0", c1.count)
	}

	// Pointer receiver modifies original
	c2 := Counter{count: 0}
	c2.IncrementPointer()
	if c2.count != 1 {
		t.Errorf("pointer receiver didn't modify: got %d, want 1", c2.count)
	}
}

func BenchmarkPointerDereference(b *testing.B) {
	x := 42
	p := &x
	for i := 0; i < b.N; i++ {
		_ = *p
	}
}
