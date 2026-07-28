package main

import (
	"context"
	"fmt"
	"time"
)

func main() {
	fmt.Println("=== Exercise 09: Context ===")

	// 1. Basic context with timeout
	fmt.Println("--- 1. Context with Timeout ---")
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	select {
	case <-time.After(200 * time.Millisecond):
		fmt.Println("Operation completed")
	case <-ctx.Done():
		fmt.Println("Timeout:", ctx.Err())
	}

	// 2. Context with cancellation
	fmt.Println("\n--- 2. Context Cancellation ---")
	ctx2, cancel2 := context.WithCancel(context.Background())
	go func() {
		time.Sleep(50 * time.Millisecond)
		cancel2()
		fmt.Println("Cancel signal sent")
	}()

	select {
	case <-ctx2.Done():
		fmt.Println("Context cancelled:", ctx2.Err())
	}

	// 3. Context with values
	fmt.Println("\n--- 3. Context with Values ---")
	ctx3 := context.WithValue(context.Background(), "userID", 12345)
	ctx3 = context.WithValue(ctx3, "traceID", "abc-123")

	printContextValues(ctx3)

	// 4. Context propagation in call chain
	fmt.Println("\n--- 4. Context Propagation ---")
	rootCtx := context.Background()
	result := processRequest(rootCtx, "request-1")
	fmt.Println("Result:", result)

	// 5. Deadline vs Timeout
	fmt.Println("\n--- 5. Deadline vs Timeout ---")
	// Deadline: specific time point
	deadlineCtx, deadlineCancel := context.WithDeadline(context.Background(), time.Now().Add(50*time.Millisecond))
	defer deadlineCancel()
	// Timeout: duration from now
	timeoutCtx, timeoutCancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer timeoutCancel()
	_ = deadlineCtx
	_ = timeoutCtx
	fmt.Println("Deadline and timeout contexts created")

	// 6. Context in HTTP-like server pattern
	fmt.Println("\n--- 6. Server Request Pattern ---")
	handleRequest(context.Background(), "/api/users")
	handleRequest(context.Background(), "/api/slow")

	// 7. Merging contexts (manual)
	fmt.Println("\n--- 7. Multiple Context Sources ---")
	ctxA, cancelA := context.WithTimeout(context.Background(), 200*time.Millisecond)
	ctxB, cancelB := context.WithCancel(context.Background())

	// Simulate external cancellation
	go func() {
		time.Sleep(50 * time.Millisecond)
		cancelB()
	}()

	// Wait for either context to be done
	select {
	case <-ctxA.Done():
		fmt.Println("Context A done:", ctxA.Err())
	case <-ctxB.Done():
		fmt.Println("Context B done:", ctxB.Err())
	}
	cancelA()
	cancelB()

	// 8. Context best practices
	fmt.Println("\n--- 8. Best Practices ---")
	fmt.Println("✓ Pass context as first parameter")
	fmt.Println("✓ Don't store context in structs")
	fmt.Println("✓ Use context.Background() at root")
	fmt.Println("✓ Use context.TODO() when unsure")
	fmt.Println("✓ Always cancel derived contexts")
	fmt.Println("✓ Don't use context for optional params")
}

func printContextValues(ctx context.Context) {
	if userID := ctx.Value("userID"); userID != nil {
		fmt.Println("  userID:", userID)
	}
	if traceID := ctx.Value("traceID"); traceID != nil {
		fmt.Println("  traceID:", traceID)
	}
}

func processRequest(ctx context.Context, reqID string) string {
	ctx = context.WithValue(ctx, "requestID", reqID)
	return step1(ctx)
}

func step1(ctx context.Context) string {
	return step2(ctx)
}

func step2(ctx context.Context) string {
	if ctx.Value("requestID") != nil {
		return "Processed: " + ctx.Value("requestID").(string)
	}
	return "No request ID"
}

func handleRequest(ctx context.Context, path string) {
	// Simulate request with timeout
	reqCtx, cancel := context.WithTimeout(ctx, 100*time.Millisecond)
	defer cancel()

	fmt.Printf("  Handling %s...\n", path)

	// Simulate work
	workDuration := 50 * time.Millisecond
	if path == "/api/slow" {
		workDuration = 200 * time.Millisecond
	}

	select {
	case <-time.After(workDuration):
		fmt.Printf("  %s completed\n", path)
	case <-reqCtx.Done():
		fmt.Printf("  %s cancelled: %v\n", path, reqCtx.Err())
	}
}
