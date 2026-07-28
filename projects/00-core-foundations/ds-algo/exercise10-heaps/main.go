package main

import "fmt"

// MinHeap — binary min-heap implementation
type MinHeap struct {
	data []int
}

func NewMinHeap() *MinHeap {
	return &MinHeap{data: make([]int, 0)}
}

func (h *MinHeap) Insert(val int) {
	h.data = append(h.data, val)
	h.siftUp(len(h.data) - 1)
}

func (h *MinHeap) ExtractMin() (int, bool) {
	if len(h.data) == 0 {
		return 0, false
	}
	min := h.data[0]
	h.data[0] = h.data[len(h.data)-1]
	h.data = h.data[:len(h.data)-1]
	h.siftDown(0)
	return min, true
}

func (h *MinHeap) Peek() (int, bool) {
	if len(h.data) == 0 {
		return 0, false
	}
	return h.data[0], true
}

func (h *MinHeap) Size() int {
	return len(h.data)
}

func (h *MinHeap) siftUp(idx int) {
	for idx > 0 {
		parent := (idx - 1) / 2
		if h.data[parent] <= h.data[idx] {
			break
		}
		h.data[parent], h.data[idx] = h.data[idx], h.data[parent]
		idx = parent
	}
}

func (h *MinHeap) siftDown(idx int) {
	n := len(h.data)
	for {
		smallest := idx
		left := 2*idx + 1
		right := 2*idx + 2

		if left < n && h.data[left] < h.data[smallest] {
			smallest = left
		}
		if right < n && h.data[right] < h.data[smallest] {
			smallest = right
		}
		if smallest == idx {
			break
		}
		h.data[idx], h.data[smallest] = h.data[smallest], h.data[idx]
		idx = smallest
	}
}

// heapSort sorts an array using heap sort
func heapSort(arr []int) []int {
	h := NewMinHeap()
	for _, v := range arr {
		h.Insert(v)
	}
	result := make([]int, 0, len(arr))
	for h.Size() > 0 {
		val, _ := h.ExtractMin()
		result = append(result, val)
	}
	return result
}

// findKthLargest finds the kth largest element using a min-heap of size k
func findKthLargest(nums []int, k int) int {
	h := NewMinHeap()
	for _, num := range nums {
		h.Insert(num)
		if h.Size() > k {
			h.ExtractMin()
		}
	}
	val, _ := h.Peek()
	return val
}

func main() {
	fmt.Println("=== Heaps Exercise ===")
	fmt.Println()

	// Min-heap operations
	fmt.Println("--- Min Heap ---")
	h := NewMinHeap()
	values := []int{5, 3, 8, 1, 9, 2}
	for _, v := range values {
		h.Insert(v)
		fmt.Printf("  Insert %d: heap = %v\n", v, h.data)
	}

	fmt.Print("\n  Extracting min: ")
	for h.Size() > 0 {
		val, _ := h.ExtractMin()
		fmt.Printf("%d ", val)
	}
	fmt.Println()

	// Heap sort
	fmt.Println("\n--- Heap Sort ---")
	arr := []int{5, 3, 8, 1, 9, 2}
	fmt.Printf("  Before: %v\n", arr)
	fmt.Printf("  After:  %v\n", heapSort(arr))

	// Kth largest element
	fmt.Println("\n--- Kth Largest Element ---")
	nums := []int{3, 2, 1, 5, 6, 4}
	for k := 1; k <= 3; k++ {
		fmt.Printf("  %dth largest in %v = %d\n", k, nums, findKthLargest(nums, k))
	}
}
