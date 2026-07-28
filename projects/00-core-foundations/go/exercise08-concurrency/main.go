package main

import (
	"bytes"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

func main() {
	fmt.Println("=== Exercise 08: Concurrency - Goroutines and Channels ===")

	// 1. Basic goroutine
	fmt.Println("--- 1. Basic Goroutine ---")
	go sayHello("Goroutine 1")
	go sayHello("Goroutine 2")
	time.Sleep(100 * time.Millisecond) // Wait for goroutines

	// 2. Channel basics
	fmt.Println("\n--- 2. Channel Basics ---")
	ch := make(chan string)
	go func() {
		ch <- "Hello from channel"
	}()
	msg := <-ch
	fmt.Println("Received:", msg)

	// 3. Buffered channel
	fmt.Println("\n--- 3. Buffered Channel ---")
	buffered := make(chan int, 3)
	buffered <- 1
	buffered <- 2
	buffered <- 3
	fmt.Println("Buffered channel length:", len(buffered), "capacity:", cap(buffered))
	close(buffered)
	for v := range buffered {
		fmt.Println("  Received:", v)
	}

	// 4. Channel directions (send-only, receive-only)
	fmt.Println("\n--- 4. Channel Directions ---")
	sendOnly := make(chan<- int, 2)
	receiveOnly := make(<-chan int, 2)
	sendOnly <- 42
	_ = sendOnly
	_ = receiveOnly

	// 5. Select statement
	fmt.Println("\n--- 5. Select Statement ---")
	ch1 := make(chan string)
	ch2 := make(chan string)
	go func() { time.Sleep(50 * time.Millisecond); ch1 <- "from ch1" }()
	go func() { time.Sleep(30 * time.Millisecond); ch2 <- "from ch2" }()

	for i := 0; i < 2; i++ {
		select {
		case msg := <-ch1:
			fmt.Println("  Received:", msg)
		case msg := <-ch2:
			fmt.Println("  Received:", msg)
		case <-time.After(100 * time.Millisecond):
			fmt.Println("  Timeout!")
		}
	}

	// 6. Worker pool pattern
	fmt.Println("\n--- 6. Worker Pool Pattern ---")
	const numJobs = 10
	const numWorkers = 3
	jobs := make(chan int, numJobs)
	results := make(chan int, numJobs)
	var wg sync.WaitGroup

	for w := 1; w <= numWorkers; w++ {
		wg.Add(1)
		go worker(w, jobs, results, &wg)
	}

	for j := 1; j <= numJobs; j++ {
		jobs <- j
	}
	close(jobs)

	go func() {
		wg.Wait()
		close(results)
	}()

	for r := range results {
		fmt.Println("  Result:", r)
	}

	// 7. Pipeline pattern
	fmt.Println("\n--- 7. Pipeline Pattern ---")
	numbers := gen(1, 2, 3, 4, 5)
	squared := sq(numbers)
	for n := range squared {
		fmt.Println("  Square:", n)
	}

	// 8. Fan-out, Fan-in
	fmt.Println("\n--- 8. Fan-out, Fan-in ---")
	done := make(chan struct{})
	defer close(done)

	in := gen(1, 2, 3, 4, 5, 6)
	c1 := sq(in)
	c2 := sq(in)
	for n := range merge(done, c1, c2) {
		fmt.Println("  Merged:", n)
	}

	// 9. sync.WaitGroup
	fmt.Println("\n--- 9. sync.WaitGroup ---")
	var wg2 sync.WaitGroup
	for i := 1; i <= 3; i++ {
		wg2.Add(1)
		go func(id int) {
			defer wg2.Done()
			fmt.Printf("  Task %d started\n", id)
			time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
			fmt.Printf("  Task %d done\n", id)
		}(i)
	}
	wg2.Wait()
	fmt.Println("  All tasks complete")

	// 10. sync.Mutex for shared state
	fmt.Println("\n--- 10. sync.Mutex ---")
	counter := Counter{}
	var wg3 sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg3.Add(1)
		go func() {
			defer wg3.Done()
			counter.Increment()
		}()
	}
	wg3.Wait()
	fmt.Println("  Final counter value:", counter.Value())

	// 11. sync.Once for initialization
	fmt.Println("\n--- 11. sync.Once ---")
	var once sync.Once
	loadConfig := func() {
		fmt.Println("  Loading config...")
	}
	for i := 0; i < 5; i++ {
		once.Do(loadConfig)
	}
	fmt.Println("  Config loaded only once")

	// 12. sync.Pool for object reuse
	fmt.Println("\n--- 12. sync.Pool ---")
	pool := &sync.Pool{
		New: func() interface{} {
			return &bytes.Buffer{}
		},
	}
	buf := pool.Get().(*bytes.Buffer)
	buf.WriteString("Hello from Pool!")
	fmt.Println("  Buffer content:", buf.String())
	buf.Reset()
	pool.Put(buf)
	fmt.Println("  Buffer returned to pool")

	// 13. Race condition demo (run with: go run -race .)
	fmt.Println("\n--- 13. Race Condition (run with: go run -race .) ---")
	racyCounter := 0
	var mu2 sync.Mutex
	for i := 0; i < 100; i++ {
		go func() {
			mu2.Lock()
			racyCounter++
			mu2.Unlock()
		}()
	}
	time.Sleep(50 * time.Millisecond)
	fmt.Println("  Race demo complete (no race with mutex)")

	// 14. Context cancellation pattern (simplified)
	fmt.Println("\n--- 14. Cancellation Pattern ---")
	cancel := make(chan struct{})
	go func() {
		time.Sleep(200 * time.Millisecond)
		close(cancel)
		fmt.Println("  Cancellation signal sent")
	}()

	resultCh := make(chan int)
	go func() {
		for i := 0; ; i++ {
			select {
			case <-cancel:
				resultCh <- i
				return
			default:
				time.Sleep(10 * time.Millisecond)
			}
		}
	}()

	count := <-resultCh
	fmt.Println("  Work done before cancellation:", count)
}

func sayHello(name string) {
	for i := 0; i < 3; i++ {
		fmt.Printf("  %s: Hello %d\n", name, i)
		time.Sleep(10 * time.Millisecond)
	}
}

func worker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for j := range jobs {
		fmt.Printf("  Worker %d processing job %d\n", id, j)
		time.Sleep(time.Duration(rand.Intn(50)) * time.Millisecond)
		results <- j * 2
	}
}

// Pipeline functions
func gen(nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for _, n := range nums {
			out <- n
		}
	}()
	return out
}

func sq(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for n := range in {
			out <- n * n
		}
	}()
	return out
}

func merge(done <-chan struct{}, cs ...<-chan int) <-chan int {
	out := make(chan int)
	var wg sync.WaitGroup
	wg.Add(len(cs))
	for _, c := range cs {
		go func(ch <-chan int) {
			defer wg.Done()
			for n := range ch {
				select {
				case out <- n:
				case <-done:
					return
				}
			}
		}(c)
	}
	go func() {
		wg.Wait()
		close(out)
	}()
	return out
}

// Counter with mutex
type Counter struct {
	mu    sync.Mutex
	value int
}

func (c *Counter) Increment() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value++
}

func (c *Counter) Value() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}
