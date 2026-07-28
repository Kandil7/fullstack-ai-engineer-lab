package main

import (
	"container/heap"
	"testing"
)

func TestQueue(t *testing.T) {
	q := NewQueue()
	if !q.IsEmpty() {
		t.Error("expected new queue to be empty")
	}
	q.Enqueue(1)
	q.Enqueue(2)
	q.Enqueue(3)

	val, ok := q.Dequeue()
	if !ok || val != 1 {
		t.Errorf("expected Dequeue() = 1, got %d", val)
	}
	val, ok = q.Dequeue()
	if !ok || val != 2 {
		t.Errorf("expected Dequeue() = 2, got %d", val)
	}
	val, ok = q.Dequeue()
	if !ok || val != 3 {
		t.Errorf("expected Dequeue() = 3, got %d", val)
	}
	if !q.IsEmpty() {
		t.Error("expected queue to be empty after dequeueing all")
	}
}

func TestQueueEmptyDequeue(t *testing.T) {
	q := NewQueue()
	_, ok := q.Dequeue()
	if ok {
		t.Error("expected Dequeue on empty queue to return false")
	}
}

func TestCircularBuffer(t *testing.T) {
	cb := NewCircularBuffer(3)
	// Read from empty buffer
	_, ok := cb.Read()
	if ok {
		t.Error("expected Read on empty buffer to return false")
	}

	cb.Write(1)
	cb.Write(2)
	cb.Write(3)

	val, ok := cb.Read()
	if !ok || val != 1 {
		t.Errorf("expected Read = 1, got %d", val)
	}
	val, ok = cb.Read()
	if !ok || val != 2 {
		t.Errorf("expected Read = 2, got %d", val)
	}
}

func TestCircularBufferOverwrite(t *testing.T) {
	cb := NewCircularBuffer(3)
	cb.Write(1)
	cb.Write(2)
	cb.Write(3)
	cb.Write(4) // overwrites 1

	val, _ := cb.Read()
	if val != 2 {
		t.Errorf("expected first read after overwrite = 2, got %d", val)
	}
}

func TestPriorityQueue(t *testing.T) {
	pq := &PriorityQueue{}
	heap.Init(pq)
	heap.Push(pq, 5)
	heap.Push(pq, 1)
	heap.Push(pq, 3)

	expected := []int{1, 3, 5}
	for _, exp := range expected {
		val := heap.Pop(pq).(int)
		if val != exp {
			t.Errorf("expected %d, got %d", exp, val)
		}
	}
}
