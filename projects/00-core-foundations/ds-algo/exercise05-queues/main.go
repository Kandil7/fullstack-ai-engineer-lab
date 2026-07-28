package main

import (
	"container/heap"
	"fmt"
)

// Queue — FIFO using slice
type Queue struct {
	items []int
}

func NewQueue() *Queue {
	return &Queue{items: make([]int, 0)}
}

func (q *Queue) Enqueue(item int) {
	q.items = append(q.items, item)
}

func (q *Queue) Dequeue() (int, bool) {
	if len(q.items) == 0 {
		return 0, false
	}
	item := q.items[0]
	q.items = q.items[1:]
	return item, true
}

func (q *Queue) IsEmpty() bool {
	return len(q.items) == 0
}

// CircularBuffer — fixed-size buffer that overwrites oldest
type CircularBuffer struct {
	buffer []int
	size   int
	head   int
	count  int
}

func NewCircularBuffer(size int) *CircularBuffer {
	return &CircularBuffer{
		buffer: make([]int, size),
		size:   size,
	}
}

func (cb *CircularBuffer) Write(val int) {
	cb.buffer[cb.head] = val
	cb.head = (cb.head + 1) % cb.size
	if cb.count < cb.size {
		cb.count++
	}
}

func (cb *CircularBuffer) Read() (int, bool) {
	if cb.count == 0 {
		return 0, false
	}
	idx := (cb.head - cb.count + cb.size) % cb.size
	cb.count--
	return cb.buffer[idx], true
}

// PriorityQueue — min-heap using container/heap
type PriorityQueue []int

func (pq PriorityQueue) Len() int           { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool  { return pq[i] < pq[j] } // Min-heap
func (pq PriorityQueue) Swap(i, j int)       { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(x interface{}) { *pq = append(*pq, x.(int)) }
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	*pq = old[:n-1]
	return item
}

func main() {
	fmt.Println("=== Queues Exercise ===")
	fmt.Println()

	// Standard queue
	fmt.Println("--- Standard Queue (FIFO) ---")
	q := NewQueue()
	q.Enqueue(1)
	q.Enqueue(2)
	q.Enqueue(3)
	for !q.IsEmpty() {
		val, _ := q.Dequeue()
		fmt.Printf("  Dequeued: %d\n", val)
	}

	// Circular buffer
	fmt.Println("\n--- Circular Buffer ---")
	cb := NewCircularBuffer(3)
	cb.Write(1)
	cb.Write(2)
	cb.Write(3)
	cb.Write(4) // overwrites 1
	for i := 0; i < 3; i++ {
		val, ok := cb.Read()
		fmt.Printf("  Read: %d (ok=%v)\n", val, ok)
	}

	// Priority queue
	fmt.Println("\n--- Priority Queue (Min-Heap) ---")
	pq := &PriorityQueue{}
	heap.Init(pq)
	heap.Push(pq, 5)
	heap.Push(pq, 1)
	heap.Push(pq, 3)
	heap.Push(pq, 2)
	fmt.Print("  Priority order: ")
	for pq.Len() > 0 {
		fmt.Printf("%d ", heap.Pop(pq))
	}
	fmt.Println()
}
