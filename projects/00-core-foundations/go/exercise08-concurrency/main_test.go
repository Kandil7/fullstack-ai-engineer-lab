package main

import (
	"sync"
	"testing"
	"time"
)

func TestChannelBasic(t *testing.T) {
	ch := make(chan string)
	go func() {
		ch <- "test"
	}()
	select {
	case msg := <-ch:
		if msg != "test" {
			t.Errorf("expected 'test', got %s", msg)
		}
	case <-time.After(time.Second):
		t.Fatal("timeout waiting for channel")
	}
}

func TestBufferedChannel(t *testing.T) {
	ch := make(chan int, 3)
	ch <- 1
	ch <- 2
	ch <- 3
	close(ch)

	var sum int
	for v := range ch {
		sum += v
	}
	if sum != 6 {
		t.Errorf("expected sum 6, got %d", sum)
	}
}

func TestSelect(t *testing.T) {
	ch1 := make(chan string)
	ch2 := make(chan string)

	go func() { ch1 <- "a" }()
	go func() { ch2 <- "b" }()

	received := make(map[string]bool)
	for i := 0; i < 2; i++ {
		select {
		case msg := <-ch1:
			received[msg] = true
		case msg := <-ch2:
			received[msg] = true
		case <-time.After(time.Second):
			t.Fatal("timeout in select")
		}
	}

	if !received["a"] || !received["b"] {
		t.Errorf("expected to receive both messages, got %v", received)
	}
}

func TestWaitGroup(t *testing.T) {
	var wg sync.WaitGroup
	completed := make(chan bool, 3)

	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			completed <- true
		}(i)
	}

	wg.Wait()
	close(completed)

	count := 0
	for range completed {
		count++
	}
	if count != 3 {
		t.Errorf("expected 3 goroutines to complete, got %d", count)
	}
}

func TestMutexCounter(t *testing.T) {
	var counter int
	var mu sync.Mutex
	var wg sync.WaitGroup

	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			mu.Lock()
			counter++
			mu.Unlock()
		}()
	}

	wg.Wait()
	if counter != 100 {
		t.Errorf("expected counter 100, got %d", counter)
	}
}

func TestPipeline(t *testing.T) {
	numbers := gen(1, 2, 3, 4, 5)
	squared := sq(numbers)

	var results []int
	for n := range squared {
		results = append(results, n)
	}

	expected := []int{1, 4, 9, 16, 25}
	if len(results) != len(expected) {
		t.Fatalf("expected %d results, got %d", len(expected), len(results))
	}
	for i, v := range expected {
		if results[i] != v {
			t.Errorf("expected results[%d]=%d, got %d", i, v, results[i])
		}
	}
}

func TestCounterStruct(t *testing.T) {
	c := Counter{}
	var wg sync.WaitGroup
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			c.Increment()
		}()
	}
	wg.Wait()
	if c.Value() != 100 {
		t.Errorf("expected counter 100, got %d", c.Value())
	}
}

func TestWorkerPool(t *testing.T) {
	jobs := make(chan int, 10)
	results := make(chan int, 10)
	var wg sync.WaitGroup

	for w := 1; w <= 3; w++ {
		wg.Add(1)
		go worker(w, jobs, results, &wg)
	}

	for j := 1; j <= 9; j++ {
		jobs <- j
	}
	close(jobs)

	go func() {
		wg.Wait()
		close(results)
	}()

	count := 0
	for range results {
		count++
	}
	if count != 9 {
		t.Errorf("expected 9 results, got %d", count)
	}
}
