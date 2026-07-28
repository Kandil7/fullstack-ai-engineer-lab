package main

import "fmt"

// BIG-O ANALYSIS
//
// This exercise demonstrates common time complexities with Go code.

// O(1) — Constant time: array access by index
func constantAccess(arr []int, index int) int {
	return arr[index] // Always one operation
}

// O(n) — Linear time: sum all elements
func linearSum(arr []int) int {
	sum := 0
	for _, v := range arr {
		sum += v // One operation per element
	}
	return sum
}

// O(n²) — Quadratic time: bubble sort (worst case)
func quadraticBubbleSort(arr []int) {
	n := len(arr)
	for i := 0; i < n-1; i++ {
		for j := 0; j < n-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
			}
		}
	}
}

// O(log n) — Logarithmic time: binary search
func logarithmicBinarySearch(arr []int, target int) int {
	low, high := 0, len(arr)-1
	for low <= high {
		mid := low + (high-low)/2
		if arr[mid] == target {
			return mid
		}
		if arr[mid] < target {
			low = mid + 1
		} else {
			high = mid - 1
		}
	}
	return -1
}

// O(2ⁿ) — Exponential time: naive Fibonacci
func exponentialFib(n int) int {
	if n <= 1 {
		return n
	}
	return exponentialFib(n-1) + exponentialFib(n-2)
}

// O(n log n) — Linearithmic: merge sort
func linearithmicMergeSort(arr []int) []int {
	if len(arr) <= 1 {
		return arr
	}
	mid := len(arr) / 2
	left := linearithmicMergeSort(arr[:mid])
	right := linearithmicMergeSort(arr[mid:])
	return merge(left, right)
}

func merge(left, right []int) []int {
	result := make([]int, 0, len(left)+len(right))
	i, j := 0, 0
	for i < len(left) && j < len(right) {
		if left[i] <= right[j] {
			result = append(result, left[i])
			i++
		} else {
			result = append(result, right[j])
			j++
		}
	}
	result = append(result, left[i:]...)
	result = append(result, right[j:]...)
	return result
}

func main() {
	fmt.Println("=== Big-O Analysis Exercise ===")
	fmt.Println()
	fmt.Println("Complexity cheat sheet (smallest to largest):")
	fmt.Println("  O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)")
	fmt.Println()

	// O(1) demo
	arr := []int{10, 20, 30, 40, 50}
	fmt.Printf("O(1) - Constant: arr[2] = %d\n", constantAccess(arr, 2))

	// O(n) demo
	fmt.Printf("O(n) - Linear: sum = %d\n", linearSum(arr))

	// O(log n) demo
	sorted := []int{1, 3, 5, 7, 9, 11, 13}
	fmt.Printf("O(log n) - Logarithmic: binary search for 7 at index %d\n",
		logarithmicBinarySearch(sorted, 7))

	// O(n log n) demo
	unsorted := []int{38, 27, 43, 3, 9, 82, 10}
	sortedResult := linearithmicMergeSort(unsorted)
	fmt.Printf("O(n log n) - Linearithmic: merge sort = %v\n", sortedResult)

	// O(n²) demo
	unsorted2 := []int{64, 34, 25, 12, 22, 11, 90}
	quadraticBubbleSort(unsorted2)
	fmt.Printf("O(n²) - Quadratic: bubble sort = %v\n", unsorted2)

	// O(2ⁿ) demo
	fmt.Printf("O(2ⁿ) - Exponential: fib(10) = %d\n", exponentialFib(10))
	fmt.Println()
	fmt.Println("Tip: Run 'go test -bench=.' to see real performance differences!")
}
