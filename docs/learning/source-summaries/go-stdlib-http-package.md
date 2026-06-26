# Source Summary: Go Standard Library `net/http` Package

**Source:** Go standard library `net/http` documentation  
**Type:** official-doc  
**Date studied:** 2026-06-26  
**Studied by:** Full-Stack AI Engineer Lab  
**Link:** https://pkg.go.dev/net/http

---

## 1. Key Concepts (Confirmed from Source)

### `http.Handler` Interface

The `http.Handler` interface is the fundamental building block of Go's HTTP server. It defines a single method:

```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}
```

Any type that implements `ServeHTTP` can handle HTTP requests. This is the contract between
the HTTP server and application code. The server calls `ServeHTTP` for every incoming request
on the matching route. The `ResponseWriter` is used to write the response body, headers, and
status code. The `*Request` contains the parsed HTTP request including method, URL, headers,
form values, and body.

**Source confirmation:** The `net/http` package documentation explicitly defines this interface
as the primary extension point for HTTP handling.

### `http.HandlerFunc` Adapter

`http.HandlerFunc` is a function type that satisfies the `Handler` interface:

```go
type HandlerFunc func(ResponseWriter, *Request)
```

It has a `ServeHTTP` method that simply calls itself. This adapter lets you use plain functions
as handlers without defining a new struct type. It is the bridge between functional-style code
and the interface-based routing system.

**Source confirmation:** The documentation describes `HandlerFunc` as "an adapter to allow the
use of ordinary functions as HTTP handlers."

### `http.ServeMux` Routing

`ServeMux` is the default HTTP request multiplexer (router). It matches incoming request URLs
to a set of registered patterns. Key behaviors:

- Longer patterns take precedence over shorter ones (`/api/users` beats `/api`)
- Trailing-slash patterns redirect to the same path without the slash (clean URL)
- Host-specific patterns can be registered with `example.com/path`
- Go 1.22+ added method-based patterns: `GET /users`, `POST /users`
- `Handle` registers a `Handler`; `HandleFunc` registers a function directly

**Source confirmation:** The documentation states "ServeMux is suitable for a wide range of
HTTP servers, but not for all."

### `http.Server` Configuration

`http.Server` wraps a mux and adds lifecycle management:

```go
server := &http.Server{
    Addr:         ":8080",
    Handler:      mux,
    ReadTimeout:  15 * time.Second,
    WriteTimeout: 15 * time.Second,
    IdleTimeout:  60 * time.Second,
}
```

Key fields for production:
- `Handler`: the mux or any `Handler` to serve requests
- `ReadTimeout`: maximum time to read the full request (including body)
- `WriteTimeout`: maximum time to write the full response
- `IdleTimeout`: maximum time to wait for the next request on a keep-alive connection
- `MaxHeaderBytes`: limit on request header size
- `BaseContext` / `ConnContext`: per-connection context customization

**Source confirmation:** The documentation emphasizes setting timeouts to prevent slow clients
from holding connections open indefinitely.

### Request/Response Lifecycle

The full request lifecycle in `net/http`:

1. Client sends HTTP request over TCP
2. Server accepts connection, parses HTTP headers
3. Server creates `*Request` and `http.ResponseWriter`
4. Server selects the matching handler via `ServeMux`
5. Handler's `ServeHTTP` is called
6. Handler reads request data, performs logic
7. Handler writes status code, headers, body to `ResponseWriter`
8. Server sends the response to the client
9. Connection may be kept alive for HTTP/1.1 keep-alive

**Source confirmation:** The documentation describes request parsing as lazy — `Request.Form`
is parsed on first access, and `Request.Body` is a stream that can only be read once.

### Middleware Pattern with Chaining

`net/http` does not have a built-in middleware concept, but the pattern is straightforward.
Middleware wraps an `Handler` and returns a new `Handler`:

```go
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        log.Printf("%s %s", r.Method, r.URL.Path)
        next.ServeHTTP(w, r)
    })
}
```

Chaining is done manually or with a helper:

```go
handler := loggingMiddleware(authMiddleware(router))
```

Each middleware wraps the next, forming a pipeline. The request flows through all middleware
before reaching the final handler. Responses flow back in reverse order.

**Source confirmation:** The documentation does not formalize middleware but the `Handler`
interface makes it composable by design.

---

## 2. My Inferences (Not Stated in Source)

### How Chi Builds on Top of stdlib

Chi implements `http.Handler` and `http.ServeMux` compatibility but adds:
- Method-based routing (`r.Get`, `r.Post`) similar to Go 1.22 but available earlier
- Sub-router mounting (`r.Route("/api", func(r chi.Router) { ... })`)
- Built-in middleware stack (Logger, Recoverer, RequestID, RealIP)
- `chi.Context` with URL parameter extraction (`chi.URLParam(r, "id")`)
- `chi.Walk` for route introspection

Chi does not reinvent the server — it wraps `http.Handler` and can be used as the
`Handler` field of `http.Server`. This means Chi is a superset of `net/http`, not a
replacement.

### When to Use Raw net/http vs Framework

Use raw `net/http` when:
- Building a microservice with 1-3 endpoints
- You want zero external dependencies
- Performance is critical and every nanosecond counts
- Learning or debugging framework internals
- The stdlib router (Go 1.22+) covers your routing needs

Use Chi (or similar) when:
- You have many routes with nested groups
- You need parameter extraction, sub-routers, or route grouping
- You want a middleware ecosystem
- Team productivity matters more than minimal dependency count
- You want request context with typed values

### Performance Implications of Middleware Depth

Each middleware adds a function call layer to the request path. With 5 middleware:
- 5 extra function calls per request (trivial compared to I/O)
- Each middleware that reads the body or allocates memory adds GC pressure
- Deeply nested middleware can make stack traces harder to read
- Timeout cascades: a slow middleware delays the entire chain

Practical takeaway: keep middleware under 10 layers. Profile with `pprof` if latency
is a concern. The `net/http` server is already highly optimized — middleware overhead
is usually dominated by database calls, network I/O, or serialization.

---

## 3. Link to Project Task

### Directly Applicable to auth-service HTTP Layer

The `auth-service` at `projects/01-backend-go/01-auth-service` uses Chi for routing,
but Chi is a thin layer over `net/http`. Understanding the stdlib directly helps:

- **Handler registration**: `r.Handle("/health", http.HandlerFunc(healthHandler))`
- **Request parsing**: `r.Body` (stream), `r.FormValue()`, `r.Header.Get()`
- **Response writing**: `w.Header().Set()`, `w.WriteHeader()`, `w.Write()`
- **Server lifecycle**: `server.Shutdown(ctx)` for graceful shutdown

### Understanding stdlib Helps Debug Framework Issues

When Chi or another framework behaves unexpectedly, the root cause is often in `net/http`:
- "Request body already closed" → `r.Body` was read twice
- "Handler already called WriteHeader" → status was written twice
- "context canceled" → client disconnected or timeout fired
- Connection leaks → `resp.Body.Close()` not called

### Foundation for Custom Middleware in internal/middleware/

The project's `internal/middleware/` directory will contain custom middleware for:
- JWT token extraction and validation
- Request logging with structured fields
- CORS headers
- Rate limiting

Each follows the same `func(http.Handler) http.Handler` signature from the stdlib.

---

## 4. ملخص عربي

### ملخص الدرس: حزمة `net/http` في مكتبة Go الأساسية

**المفاهيم الأساسية:**

- **`http.Handler`**: الواجهة الأساسية لمعالجة الطلبات HTTP. تحتوي على طريقة واحدة
  `ServeHTTP(ResponseWriter, *Request)`. أي نوع يُنفذ هذه الواجهة يمكنه معالجة طلبات HTTP.

- **`http.HandlerFunc`**: نوع دالة يتكيف مع واجهة `Handler`. يسمح باستخدام الدوال
  العادية كمعالجات HTTP دون الحاجة لتعريف أنواع جديدة.

- **`http.ServeMux`**: الموزع الافتراضي (الراوتر). يُطابق عنوان URL مع الأنماط
  المسجلة. في الإصدار 1.22+ يدعم أنماط مبنية على الطريقة مثل `GET /users`.

- **`http.Server`**: يلف الـ mux ويضيف إدارة دورة الحياة. يجب تعيين `ReadTimeout`
  و`WriteTimeout` و`IdleTimeout` للحماية من عملاء بطيئين.

- **دورة حياة الطلب والاستجابة**: الطلب يتدفق من العميل عبر TCP → تم تحليله → يتم
  إنشاء `Request` و`ResponseWriter` → يتم اختيار المعالج → يتم تنفيذ `ServeHTTP` →
  يتم كتابة الاستجابة.

- **نمط الـ Middleware**: يلف المعالج ويرجع معالجًا جديدًا. يتم تسلسله يدويًا
  مثل `loggingMiddleware(authMiddleware(router))`.

- **متى نستخدم net/http الخام أم الإطار**: استخدم الخام عندما تكونEndpoints قليلة
  وتريد تبعيات صفرية. استخدم Chi عندما تحتاج تجميع مسارات أو نظام middleware.

- **أثر عمق الـ Middleware**: كل طبقة middleware تضيف استدعاء دالة واحدة. يُفضل الاحتفاظ
  بأقل من 10 طبقات. الأثرة الفعلية غالبًا من قواعد البيانات أو الشبكة.

**ربط بالمشروع:** فهم `net/http` يساعد في بناء طبقة HTTP لـ `auth-service` وفهم
سلوك Chi وصياغة middleware مخصص في `internal/middleware/`.

---

## 5. Exercise

### Build a Minimal HTTP Server Using Only `net/http`

Create a file `cmd/minimal-server/main.go`:

```go
package main

import (
    "log"
    "net/http"
    "time"
)

func main() {
    mux := http.NewServeMux()

    // Health check
    mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusOK)
        w.Write([]byte(`{"status":"healthy"}`))
    })

    // Hello endpoint
    mux.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
        if r.Method != http.MethodGet {
            http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
            return
        }
        name := r.URL.Query().Get("name")
        if name == "" {
            name = "World"
        }
        w.Header().Set("Content-Type", "application/json")
        w.Write([]byte(`{"message":"Hello, ` + name + `"}`))
    })

    server := &http.Server{
        Addr:         ":8080",
        Handler:      mux,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    log.Printf("Server starting on %s", server.Addr)
    if err := server.ListenAndServe(); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
```

### Implement a Logging Middleware

Create `internal/middleware/logging.go`:

```go
package middleware

import (
    "log"
    "net/http"
    "time"
)

// loggingResponseWriter wraps http.ResponseWriter to capture the status code.
type loggingResponseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (lrw *loggingResponseWriter) WriteHeader(code int) {
    lrw.statusCode = code
    lrw.ResponseWriter.WriteHeader(code)
}

// Logging logs the method, path, status code, and duration for each request.
func Logging(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        lrw := &loggingResponseWriter{ResponseWriter: w, statusCode: http.StatusOK}
        next.ServeHTTP(lrw, r)
        log.Printf(
            "method=%s path=%s status=%d duration=%s",
            r.Method,
            r.URL.Path,
            lrw.statusCode,
            time.Since(start),
        )
    })
}
```

Wire it into the server:

```go
handler := Logging(mux)
server := &http.Server{
    Addr:    ":8080",
    Handler: handler,
}
```

### Write a Test for the Handler

Create `cmd/minimal-server/main_test.go`:

```go
package main

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHealthHandler(t *testing.T) {
    mux := http.NewServeMux()
    mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusOK)
        w.Write([]byte(`{"status":"healthy"}`))
    })

    req := httptest.NewRequest(http.MethodGet, "/health", nil)
    w := httptest.NewRecorder()
    mux.ServeHTTP(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("expected 200, got %d", w.Code)
    }

    var body map[string]string
    if err := json.Unmarshal(w.Body.Bytes(), &body); err != nil {
        t.Fatalf("failed to parse response: %v", err)
    }
    if body["status"] != "healthy" {
        t.Errorf("expected status=healthy, got %s", body["status"])
    }
}

func TestHelloHandler(t *testing.T) {
    mux := http.NewServeMux()
    mux.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
        if r.Method != http.MethodGet {
            http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
            return
        }
        name := r.URL.Query().Get("name")
        if name == "" {
            name = "World"
        }
        w.Header().Set("Content-Type", "application/json")
        w.Write([]byte(`{"message":"Hello, ` + name + `"}`))
    })

    // Test with name parameter
    req := httptest.NewRequest(http.MethodGet, "/hello?name=Baligh", nil)
    w := httptest.NewRecorder()
    mux.ServeHTTP(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("expected 200, got %d", w.Code)
    }

    var body map[string]string
    if err := json.Unmarshal(w.Body.Bytes(), &body); err != nil {
        t.Fatalf("failed to parse response: %v", err)
    }
    if body["message"] != "Hello, Baligh" {
        t.Errorf("expected 'Hello, Baligh', got '%s'", body["message"])
    }

    // Test with POST (should fail)
    req = httptest.NewRequest(http.MethodPost, "/hello", nil)
    w = httptest.NewRecorder()
    mux.ServeHTTP(w, req)

    if w.Code != http.StatusMethodNotAllowed {
        t.Errorf("expected 405, got %d", w.Code)
    }
}
```

Run tests:

```bash
cd projects/01-backend-go/01-auth-service
go test ./cmd/minimal-server/ -v
```

**Expected output:** All tests pass, confirming the handler works correctly.

---

**Next step:** Apply this knowledge to the `auth-service` by implementing the JWT
middleware in `internal/middleware/` following the same `func(http.Handler) http.Handler`
pattern.

**Reflection:** Studying `net/http` before using Chi was valuable. Chi is much easier
to understand when you know what it wraps. The key insight is that Go's HTTP system is
built on a single interface (`Handler`) and everything composes through function wrapping.
