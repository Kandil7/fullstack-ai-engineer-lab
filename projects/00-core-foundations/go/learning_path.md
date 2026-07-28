# 🗺️ Go Learning Path

> **4-week plan** to master Go fundamentals before moving to production services.

---

## 📊 Recommended Order

```
Week 1 ──> Week 2 ──> Week 3 ──> Week 4
ex01-03     ex04-06     ex07-09     ex10-12
```

---

## 🗓️ Week 1: Foundations

### Day 1: Hello World + Variables
- Files: `exercise01/main.go`
- Concepts: `package main`, `import`, `func main()`, variables (`var`, `:=`), types, `fmt.Println`
- Practice: Print different types, use zero values, short declaration

### Day 2: Functions & Returns
- Files: `exercise01/main.go`
- Concepts: Function signatures, return types, multiple returns, named returns
- Practice: Write a function with multiple return values

### Day 3: Testing Basics
- Files: `exercise01/main_test.go`
- Concepts: `*testing.T`, `Errorf`, test functions, `go test`
- Practice: Write table-driven tests

### Day 4: Structs
- Files: `exercise02-structs/main.go`
- Concepts: Struct fields, struct literals, `%+v`
- Practice: Define structs with different field types

### Day 5: Methods & Interfaces
- Files: `exercise02-structs/main.go`
- Concepts: Value receivers, interface satisfaction, `Greeter` pattern
- Practice: Implement an interface implicitly

### Day 6: Embedding & Composition
- Files: `exercise02-structs/main.go`
- Concepts: Struct embedding, method override, polymorphism
- Practice: Create an embedded type, iterate over `[]interface`

### Day 7: Review & Test
- Run all tests: `go test ./exercise01/ ./exercise02-structs/ -v`
- Review key concepts

---

## 🗓️ Week 2: Core Types

### Day 8: Pointers Basics
- Files: `exercise03-pointers/main.go`
- Concepts: `&`, `*`, new vs make, nil pointers
- Practice: Swap values using pointers

### Day 9: Pointer Receivers
- Files: `exercise03-pointers/main.go`
- Concepts: Value vs pointer receivers, mutation
- Practice: Implement both receiver types, compare behavior

### Day 10: Arrays & Slices
- Files: `exercise04-collections/main.go`
- Concepts: Fixed arrays, dynamic slices, `append`, `make`, `copy`
- Practice: Slice operations, backing arrays

### Day 11: Maps & Ranges
- Files: `exercise04-collections/main.go`
- Concepts: Map literal, `make(map...)`, range over map, comma-ok idiom
- Practice: Build a word frequency counter

### Day 12: Strings & Runes
- Files: `exercise04-collections/main.go`
- Concepts: `string` is bytes, `[]rune`, UTF-8, range over string
- Practice: Reverse a string with runes

### Day 13: If, For, Switch
- Files: `exercise05-control-flow/main.go`
- Concepts: Short-statement if, for as while, switch without expression, type switch
- Practice: FizzBuzz with switch

### Day 14: Defer & Labels
- Files: `exercise05-control-flow/main.go`
- Concepts: Defer stack (LIFO), `break OuterLoop`, `goto`
- Practice: Trace defer execution order

---

## 🗓️ Week 3: Intermediate Go

### Day 15: Variadic Functions & Closures
- Files: `exercise06-functions/main.go`
- Concepts: `...T`, first-class functions, closure capturing
- Practice: Write a `filter` function using closures

### Day 16: Function Types & Methods
- Files: `exercise06-functions/main.go`
- Concepts: Function type alias, map of functions, method vs function
- Practice: Build a calculator dispatch table

### Day 17: Error Handling Patterns
- Files: `exercise07-errors/main.go`
- Concepts: `errors.New`, `fmt.Errorf(%w)`, sentinel errors, custom types
- Practice: Create a custom `ValidationError`

### Day 18: Error Wrapping & Is/As
- Files: `exercise07-errors/main.go`
- Concepts: `errors.Is`, `errors.As`, error chain, Go 1.20+ `errors.Join`
- Practice: Unwrap a 3-level error chain

### Day 19: Panic & Recover
- Files: `exercise07-errors/main.go`
- Concepts: `panic`, `recover()`, `defer` + recover pattern
- Practice: Build a safe HTTP handler

### Day 20: Goroutines & Channels
- Files: `exercise08-concurrency/main.go`
- Concepts: `go` keyword, `make(chan T)`, blocking send/receive
- Practice: Launch 5 goroutines, collect results via channel

### Day 21: Select & Timeout
- Files: `exercise08-concurrency/main.go`
- Concepts: `select`, `time.After`, channel priority, timeout pattern
- Practice: Implement a timeout for a slow operation

---

## 🗓️ Week 4: Advanced Go

### Day 22: WaitGroup & Mutex
- Files: `exercise08-concurrency/main.go`
- Concepts: `sync.WaitGroup`, `sync.Mutex`, race conditions
- Practice: Increment a counter safely with 100 goroutines

### Day 23: Pipeline & Fan-out/Fan-in
- Files: `exercise08-concurrency/main.go`
- Concepts: Pipeline stages, generator pattern, merging channels
- Practice: Build a 3-stage pipeline

### Day 24: Context Package
- Files: `exercise09-context/main.go`
- Concepts: `context.Background()`, `WithTimeout`, `WithCancel`, `WithValue`
- Practice: Add context-aware timeout to a request handler

### Day 25: File I/O
- Files: `exercise10-io-json/main.go`
- Concepts: `os.ReadFile`, `os.WriteFile`, `os.CreateTemp`, `io.Reader/Writer`
- Practice: Copy a file with io.Copy

### Day 26: JSON Marshal/Unmarshal
- Files: `exercise10-io-json/main.go`
- Concepts: JSON tags, `MarshalIndent`, streaming with Decoder/Encoder
- Practice: Parse a JSON array of objects

### Day 27: Testing Patterns
- Files: `exercise11-testing/main.go`, `exercise11-testing/main_test.go` (create your own)
- Concepts: Table-driven tests, subtests, coverage, benchmarks
- Practice: Write tests for a Stack implementation

### Day 28: Capstone — CLI Tool
- Files: `exercise12-cli-tool/main.go`
- Concepts: `flag`, subcommands, JSON transformation, file processing
- Practice: Run the tool on sample data, add a new subcommand

---

## 🧪 Self-Assessment

After completing all exercises, you should be able to:

- [ ] Write a Go program from scratch without referencing docs
- [ ] Use interfaces for decoupling and testability
- [ ] Handle errors idiomatically with wrapping
- [ ] Write concurrent programs with goroutines and channels
- [ ] Use context for cancellation and timeouts
- [ ] Marshal/unmarshal JSON with custom types
- [ ] Write table-driven tests and benchmarks
- [ ] Build a CLI tool with subcommands

---

## 🔗 Next Steps

After this module, move to **Phase 01: Backend Go Services**:

- `projects/01-backend-go/01-auth-service/` — JWT auth service
- `projects/01-backend-go/02-user-service/` — User CRUD with PostgreSQL
- `projects/01-backend-go/03-chat-service/` — Real-time chat with WebSockets

---

*Pro tip: Don't just read the code. Type it out. Modify it. Break it. Fix it. That's how you learn Go.*
