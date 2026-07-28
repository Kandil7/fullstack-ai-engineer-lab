package main

import "fmt"

// TWO-POINTER TECHNIQUE

// isPalindrome checks if a string is a palindrome using two pointers
func isPalindrome(s string) bool {
	runes := []rune(s)
	i, j := 0, len(runes)-1
	for i < j {
		if runes[i] != runes[j] {
			return false
		}
		i++
		j--
	}
	return true
}

// reverseString reverses a string in-place using two pointers
func reverseString(s string) string {
	runes := []rune(s)
	i, j := 0, len(runes)-1
	for i < j {
		runes[i], runes[j] = runes[j], runes[i]
		i++
		j--
	}
	return string(runes)
}

// SLIDING WINDOW

// maxSubarraySum finds the maximum sum of any contiguous subarray of size k
func maxSubarraySum(arr []int, k int) int {
	if len(arr) < k || k <= 0 {
		return 0
	}
	// Calculate sum of first window
	windowSum := 0
	for i := 0; i < k; i++ {
		windowSum += arr[i]
	}
	maxSum := windowSum
	// Slide the window
	for i := k; i < len(arr); i++ {
		windowSum = windowSum - arr[i-k] + arr[i]
		if windowSum > maxSum {
			maxSum = windowSum
		}
	}
	return maxSum
}

// removeDuplicates removes duplicates from a sorted array in-place
func removeDuplicates(arr []int) []int {
	if len(arr) == 0 {
		return arr
	}
	writeIdx := 1
	for readIdx := 1; readIdx < len(arr); readIdx++ {
		if arr[readIdx] != arr[readIdx-1] {
			arr[writeIdx] = arr[readIdx]
			writeIdx++
		}
	}
	return arr[:writeIdx]
}

// rotateArray rotates an array to the right by k steps
func rotateArray(arr []int, k int) {
	n := len(arr)
	if n == 0 {
		return
	}
	k = k % n
	if k == 0 {
		return
	}
	reverse(arr, 0, n-1)
	reverse(arr, 0, k-1)
	reverse(arr, k, n-1)
}

func reverse(arr []int, start, end int) {
	for start < end {
		arr[start], arr[end] = arr[end], arr[start]
		start++
		end--
	}
}

func main() {
	fmt.Println("=== Arrays & Strings Exercise ===")
	fmt.Println()

	// Palindrome check
	fmt.Println("--- Two-Pointer: Palindrome ---")
	testStrings := []string{"racecar", "hello", "A man a plan a canal panama", "golang"}
	for _, s := range testStrings {
		fmt.Printf("  isPalindrome(%q) = %v\n", s, isPalindrome(s))
	}

	// Reverse string
	fmt.Println("\n--- Two-Pointer: String Reverse ---")
	fmt.Printf("  reverse(%q) = %q\n", "hello", reverseString("hello"))
	fmt.Printf("  reverse(%q) = %q\n", "Go语言", reverseString("Go语言"))

	// Sliding window maximum sum
	fmt.Println("\n--- Sliding Window ---")
	arr := []int{2, 1, 5, 1, 3, 2}
	fmt.Printf("  arr=%v, k=3, max sum = %d\n", arr, maxSubarraySum(arr, 3))

	// Remove duplicates
	fmt.Println("\n--- In-Place Array Modification ---")
	dups := []int{0, 0, 1, 1, 1, 2, 2, 3, 3, 4}
	result := removeDuplicates(dups)
	fmt.Printf("  removeDuplicates from %v -> %v (len=%d)\n", dups[:10], result, len(result))

	// Rotate array
	fmt.Println("\n--- Array Rotation ---")
	rotArr := []int{1, 2, 3, 4, 5, 6, 7}
	rotateArray(rotArr, 3)
	fmt.Printf("  rotate([1,2,3,4,5,6,7], 3) = %v\n", rotArr)
}
