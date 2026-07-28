package main

import "fmt"

// DYNAMIC PROGRAMMING

// fibMemo — Fibonacci with memoization (top-down)
func fibMemo(n int, memo map[int]int) int {
	if n <= 1 {
		return n
	}
	if val, ok := memo[n]; ok {
		return val
	}
	memo[n] = fibMemo(n-1, memo) + fibMemo(n-2, memo)
	return memo[n]
}

func Fibonacci(n int) int {
	return fibMemo(n, make(map[int]int))
}

// fibTab — Fibonacci with tabulation (bottom-up)
func fibTab(n int) int {
	if n <= 1 {
		return n
	}
	dp := make([]int, n+1)
	dp[0], dp[1] = 0, 1
	for i := 2; i <= n; i++ {
		dp[i] = dp[i-1] + dp[i-2]
	}
	return dp[n]
}

// Knapsack — 0/1 knapsack problem
// Given weights and values, find max value for capacity W
func knapsack(weights, values []int, W int) int {
	n := len(weights)
	dp := make([][]int, n+1)
	for i := range dp {
		dp[i] = make([]int, W+1)
	}

	for i := 1; i <= n; i++ {
		for w := 1; w <= W; w++ {
			if weights[i-1] <= w {
				// Max of including or excluding item i-1
				include := values[i-1] + dp[i-1][w-weights[i-1]]
				exclude := dp[i-1][w]
				if include > exclude {
					dp[i][w] = include
				} else {
					dp[i][w] = exclude
				}
			} else {
				dp[i][w] = dp[i-1][w]
			}
		}
	}
	return dp[n][W]
}

// LCS — Longest Common Subsequence
func LCS(a, b string) int {
	m, n := len(a), len(b)
	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}

	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if a[i-1] == b[j-1] {
				dp[i][j] = dp[i-1][j-1] + 1
			} else {
				if dp[i-1][j] > dp[i][j-1] {
					dp[i][j] = dp[i-1][j]
				} else {
					dp[i][j] = dp[i][j-1]
				}
			}
		}
	}
	return dp[m][n]
}

// CoinChange — minimum coins needed for amount
func coinChange(coins []int, amount int) int {
	dp := make([]int, amount+1)
	for i := 1; i <= amount; i++ {
		dp[i] = amount + 1 // "infinite" sentinel
	}
	dp[0] = 0

	for _, coin := range coins {
		for i := coin; i <= amount; i++ {
			if dp[i-coin]+1 < dp[i] {
				dp[i] = dp[i-coin] + 1
			}
		}
	}
	if dp[amount] > amount {
		return -1
	}
	return dp[amount]
}

func main() {
	fmt.Println("=== Dynamic Programming Exercise ====")
	fmt.Println()

	// Fibonacci
	fmt.Println("--- Fibonacci ---")
	for _, n := range []int{0, 1, 10, 20, 30} {
		fmt.Printf("  fib(%d) = %d\n", n, Fibonacci(n))
	}
	fmt.Printf("  fibTab(30) = %d (tabulation)\n", fibTab(30))

	// 0/1 Knapsack
	fmt.Println("\n--- 0/1 Knapsack ---")
	weights := []int{2, 3, 4, 5}
	values := []int{3, 4, 5, 6}
	fmt.Printf("  Items: weights=%v, values=%v\n", weights, values)
	fmt.Printf("  Knapsack capacity 5: max value = %d\n", knapsack(weights, values, 5))
	fmt.Printf("  Knapsack capacity 10: max value = %d\n", knapsack(weights, values, 10))

	// Longest Common Subsequence
	fmt.Println("\n--- Longest Common Subsequence ---")
	fmt.Printf("  LCS(\"ABCDGH\", \"AEDFHR\") = %d\n", LCS("ABCDGH", "AEDFHR"))
	fmt.Printf("  LCS(\"AGGTAB\", \"GXTXAYB\") = %d\n", LCS("AGGTAB", "GXTXAYB"))

	// Coin Change
	fmt.Println("\n--- Coin Change ---")
	coins := []int{1, 2, 5}
	for _, amount := range []int{11, 3, 0, 7} {
		result := coinChange(coins, amount)
		if result >= 0 {
			fmt.Printf("  coins=%v, amount=%d: need %d coins\n", coins, amount, result)
		} else {
			fmt.Printf("  coins=%v, amount=%d: impossible\n", coins, amount)
		}
	}
}
