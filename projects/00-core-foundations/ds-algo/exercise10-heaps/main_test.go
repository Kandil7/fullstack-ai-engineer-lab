package main

import (
	"reflect"
	"testing"
)

func TestMinHeap(t *testing.T) {
	h := NewMinHeap()
	h.Insert(5)
	h.Insert(3)
	h.Insert(8)
	h.Insert(1)

	min, ok := h.Peek()
	if !ok || min != 1 {
		t.Errorf("expected Peek = 1, got %d", min)
	}

	expected := []int{1, 3, 5, 8}
	for _, exp := range expected {
		val, ok := h.ExtractMin()
		if !ok {
			t.Fatalf("expected to extract %d", exp)
		}
		if val != exp {
			t.Errorf("expected %d, got %d", exp, val)
		}
	}

	if h.Size() != 0 {
		t.Errorf("expected size 0, got %d", h.Size())
	}
}

func TestMinHeapEmpty(t *testing.T) {
	h := NewMinHeap()
	_, ok := h.ExtractMin()
	if ok {
		t.Error("expected ExtractMin on empty heap to return false")
	}
	_, ok = h.Peek()
	if ok {
		t.Error("expected Peek on empty heap to return false")
	}
}

func TestMinHeapDuplicateValues(t *testing.T) {
	h := NewMinHeap()
	h.Insert(3)
	h.Insert(1)
	h.Insert(1)
	h.Insert(2)

	v1, _ := h.ExtractMin()
	if v1 != 1 {
		t.Errorf("expected 1, got %d", v1)
	}
	v2, _ := h.ExtractMin()
	if v2 != 1 {
		t.Errorf("expected 1, got %d", v2)
	}
}

func TestHeapSort(t *testing.T) {
	tests := []struct {
		input, expected []int
	}{
		{[]int{5, 3, 8, 1, 9, 2}, []int{1, 2, 3, 5, 8, 9}},
		{[]int{1, 2, 3, 4, 5}, []int{1, 2, 3, 4, 5}},
		{[]int{5, 4, 3, 2, 1}, []int{1, 2, 3, 4, 5}},
		{[]int{}, []int{}},
		{[]int{1}, []int{1}},
	}
	for _, tt := range tests {
		got := heapSort(tt.input)
		if !reflect.DeepEqual(got, tt.expected) {
			t.Errorf("heapSort(%v) = %v; want %v", tt.input, got, tt.expected)
		}
	}
}

func TestFindKthLargest(t *testing.T) {
	nums := []int{3, 2, 1, 5, 6, 4}
	tests := []struct {
		k, expected int
	}{
		{1, 6},
		{2, 5},
		{3, 4},
		{4, 3},
	}
	for _, tt := range tests {
		got := findKthLargest(nums, tt.k)
		if got != tt.expected {
			t.Errorf("findKthLargest(%v, %d) = %d; want %d", nums, tt.k, got, tt.expected)
		}
	}
}
