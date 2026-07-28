# 🏗️ Go Fundamentals — Core Foundations

> **12 progressive exercises** that take you from `package main` to building a production-quality CLI tool.

---

## 📋 Overview

Go is the **primary backend language** in this lab. Every API service, auth handler, and microservice is written in Go. This module builds the fluency you need to read, write, and debug production Go code.

## 🎯 Exercises

| # | Exercise | Topic | What You'll Learn |
|---|----------|-------|-------------------|
| 1 | `exercise01/` | Hello World + Types | Variables, zero values, `:=`, basic functions |
| 2 | `exercise02-structs/` | Structs & Interfaces | Structs, methods, interfaces, embedding, type assertions |
| 3 | `exercise03-pointers/` | Pointers & Memory | `&`, `*`, pointer/value receivers, heap vs stack |
| 4 | `exercise04-collections/` | Collections | Arrays vs slices, maps, ranges, string/runes |
| 5 | `exercise05-control-flow/` | Control Flow | if/else, for/range, switch/type-switch, defer, labels |
| 6 | `exercise06-functions/` | Functions | Variadic, closures, first-class functions, named returns |
| 7 | `exercise07-errors/` | Error Handling | Sentinel errors, wrapping, `errors.Is/As`, panic/recover, custom error types |
| 8 | `exercise08-concurrency/` | Concurrency | Goroutines, channels, select, WaitGroup, Mutex, pipelines, fan-out/fan-in |
| 9 | `exercise09-context/` | Context | `context.WithTimeout`, cancellation, values, propagation patterns |
| 10 | `exercise10-io-json/` | I/O & JSON | File I/O, `io.Reader/Writer`, JSON marshal/unmarshal, streaming, custom marshaling |
| 11 | `exercise11-testing/` | Testing | Table-driven tests, benchmarks, fuzzing, subtests, mocking |
| 12 | `exercise12-cli-tool/` | CLI Tool (Capstone) | `flag` package, JSON transformation, subcommands, file processing |

---

## 🚀 Quick Start

```bash
# Run any exercise
cd exercise01
go run .

# Run tests
go test -v

# Run benchmarks
go test -bench=. -benchmem

# Check for race conditions (ex08, ex09)
go run -race .
```

## 📖 Learning Path

See **[learning_path.md](./learning_path.md)** for the recommended order and weekly schedule.

## 🛠️ Prerequisites

- Go 1.22+ installed (`go version`)
- Basic terminal familiarity
- A text editor or IDE (VS Code recommended with Go extension)

## 📚 Resources

- [Go Tour](https://tour.golang.org/) — Interactive introduction
- [Effective Go](https://go.dev/doc/effective_go) — Idiomatic Go patterns
- [Go by Example](https://gobyexample.com/) — Quick code snippets
- [Go 1.22 Release Notes](https://go.dev/doc/go1.22) — Latest language features
- [Pro Go (Adam Bell)](https://www.manning.com/books/pro-go) — Deep reference

## ✅ Progress Checklist

- [ ] Exercise 01: Variables, types, basic functions
- [ ] Exercise 02: Structs, methods, interfaces, embedding
- [ ] Exercise 03: Pointers, memory, receiver types
- [ ] Exercise 04: Slices, maps, arrays, ranges
- [ ] Exercise 05: Conditionals, switches, loops, defer
- [ ] Exercise 06: Variadic functions, closures, function types
- [ ] Exercise 07: Error patterns, wrapping, panic/recover
- [ ] Exercise 08: Goroutines, channels, select, sync primitives
- [ ] Exercise 09: Context timeout, cancellation, propagation
- [ ] Exercise 10: File I/O, JSON marshaling, streaming
- [ ] Exercise 11: Table-driven tests, benchmarks, fuzzing
- [ ] Exercise 12: CLI tool with subcommands and flags

---

*This module feeds directly into Phase 01 (Backend Go Services). Master these exercises before moving on.*
