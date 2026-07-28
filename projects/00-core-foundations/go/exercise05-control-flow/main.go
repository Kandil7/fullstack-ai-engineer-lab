package main

import "fmt"

func main() {
	fmt.Println("=== Exercise 05: Control Flow ===")

	// 1. If-else
	fmt.Println("--- 1. If-Else ---")
	x := 10
	if x > 5 {
		fmt.Println("x > 5")
	} else if x == 5 {
		fmt.Println("x == 5")
	} else {
		fmt.Println("x < 5")
	}

	// Short statement in if
	if y := 2 * x; y > 15 {
		fmt.Println("2*x > 15:", y)
	}

	// 2. Switch
	fmt.Println("\n--- 2. Switch ---")
	day := "Tuesday"
	switch day {
	case "Monday":
		fmt.Println("Start of week")
	case "Friday":
		fmt.Println("End of week")
	case "Saturday", "Sunday":
		fmt.Println("Weekend!")
	default:
		fmt.Println("Midweek")
	}

	// Switch without expression (like if-else chain)
	switch {
	case x < 0:
		fmt.Println("negative")
	case x == 0:
		fmt.Println("zero")
	case x > 0:
		fmt.Println("positive")
	}

	// Type switch
	fmt.Println("\n--- Type Switch ---")
	var i interface{} = "hello"
	switch v := i.(type) {
	case int:
		fmt.Println("int:", v)
	case string:
		fmt.Println("string:", v)
	case bool:
		fmt.Println("bool:", v)
	default:
		fmt.Println("unknown type")
	}

	// 3. For loops
	fmt.Println("\n--- 3. For Loops ---")
	// Standard for
	sum := 0
	for i := 0; i < 5; i++ {
		sum += i
	}
	fmt.Println("Sum 0-4:", sum)

	// While-style
	n := 1
	for n < 5 {
		n *= 2
	}
	fmt.Println("While-style result:", n)

	// Infinite loop with break
	fmt.Print("Infinite with break: ")
	for {
		fmt.Print(".")
		break
	}
	fmt.Println()

	// Range over slice
	fmt.Println("Range over slice:")
	for i, v := range []int{10, 20, 30} {
		fmt.Printf("  [%d] = %d\n", i, v)
	}

	// Range over map (order not guaranteed)
	fmt.Println("Range over map:")
	for k, v := range map[string]int{"a": 1, "b": 2} {
		fmt.Printf("  %s = %d\n", k, v)
	}

	// Range over string (runes)
	fmt.Println("Range over string (runes):")
	for i, r := range "Go" {
		fmt.Printf("  [%d] = %c (U+%04X)\n", i, r, r)
	}

	// 4. Labels with break/continue
	fmt.Println("\n--- 4. Labels ---")
OuterLoop:
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if i == 1 && j == 1 {
				fmt.Println("Breaking outer loop at i=1, j=1")
				break OuterLoop
			}
			fmt.Printf("  (%d, %d)\n", i, j)
		}
	}

	// 5. Goto (rare but valid)
	fmt.Println("\n--- 5. Goto ---")
	j := 0
LoopLabel:
	if j < 3 {
		fmt.Println("  Goto iteration:", j)
		j++
		goto LoopLabel
	}

	// 6. Defer
	fmt.Println("\n--- 6. Defer ---")
	defer fmt.Println("  Deferred: runs last")
	defer fmt.Println("  Deferred: runs second to last")
	fmt.Println("  Normal: runs first")

	// Defer stack (LIFO)
	fmt.Println("Defer stack:")
	for i := 0; i < 3; i++ {
		defer fmt.Println("  Deferred:", i)
	}

	// Defer with named return values
	fmt.Println("\nNamed return with defer:")
	fmt.Println("  Result:", double(5))
}

func double(x int) (result int) {
	defer func() { result *= 2 }()
	result = x + 1
	return
}
