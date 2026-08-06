# Learning Path: Flutter Client

**Last updated:** 2026-08-06

**Goal:** build a production-quality Flutter mobile app that talks to the Go/FastAPI backend,
with clean architecture, proper state management, and solid testing.

**Primary project:** `projects/02-frontend/flutter-app`

---

## Milestones

### 1. Dart Fundamentals (Week 1)
- Variables, types, null safety (`?`, `!`, `??`), late final
- Functions, named parameters, optional positional, arrow syntax
- Classes, mixins, abstract classes, enums, sealed classes
- Asynchrony: `Future`, `async`/`await`, `Stream`, `Completer`
- Collections: `List`, `Map`, `Set`; extension methods
- Error handling: try/catch, custom exceptions, `Result` pattern

### 2. Flutter Widget Tree (Week 1–2)
- `MaterialApp`, `Scaffold`, `AppBar`, `Drawer`, `BottomNavigationBar`
- Layout widgets: `Row`, `Column`, `Stack`, `Expanded`, `Flexible`, `Wrap`
- `ListView.builder`, `GridView`, `CustomScrollView` + `Sliver` family
- `Container`, `Card`, `Padding`, `SizedBox`, `ConstrainedBox`
- `Text`, `RichText`, `Theme.of(context)`, custom `TextTheme`
- `InheritedWidget`, `Provider.of`, `Builder` — how data flows down the tree

### 3. State Management — Riverpod (Week 2–3)
- `Provider`, `StateProvider`, `StateNotifierProvider`
- `AsyncValue<T>` — `.when(data:, loading:, error:)` pattern
- `FutureProvider` for async initialization
- `Notifier` and `AsyncNotifier` for complex state
- `ref.watch()` vs `ref.read()` — when to use each
- Provider scopes, overrides, and family modifiers

### 4. State Management — BLoC (Week 3, optional alternative)
- `BlocProvider`, `BlocBuilder`, `BlocListener`, `BlocConsumer`
- Events, States, and the unidirectional data flow
- `equatable` for value comparison
- When to choose BLoC over Riverpod (team convention, complexity)

### 5. Navigation with GoRouter (Week 3–4)
- Declarative route definitions: `GoRoute`, `ShellRoute`
- Path parameters, query parameters, extra data
- Nested navigation with `StatefulShellRoute`
- Redirect guards for auth flow
- Deep linking and URL strategies

### 6. HTTP Networking with Dio (Week 4)
- Base URL, interceptors, headers, timeout configuration
- `DioException` handling — timeout, cancellation, server errors
- Request/response interceptors for JWT token injection
- Refresh token flow: interceptor that retries 401s
- `FormData`, file upload, download progress

### 7. Local Storage (Week 5)
- `shared_preferences` for simple key-value config
- `hive` or `drift` for structured offline data
- Caching strategy: cache-then-network, cache-only
- Secure storage (`flutter_secure_storage`) for tokens

### 8. Clean Architecture Pattern (Week 5–6)
```
lib/
├── core/          # theme, constants, utils, network client
├── features/
│   ├── auth/
│   │   ├── data/       # repositories (data sources + mappers)
│   │   ├── domain/     # entities, use cases, repository interfaces
│   │   └── presentation/ # pages, widgets, state (providers/blocs)
│   └── chat/
│       ├── data/
│       ├── domain/
│       └── presentation/
└── main.dart
```
- Domain layer: pure Dart, no Flutter imports — entities + use cases
- Data layer: repositories implementing domain interfaces, data sources
- Presentation layer: pages, widgets, state management
- Dependency inversion: domain defines interfaces, data provides impl

### 9. Testing (Week 6–7)
- **Unit tests:** use cases, repositories (mock HTTP layer)
- **Widget tests:** `tester.pumpWidget()`, `find.byType()`, `expect()`
- **Golden tests:** visual regression with `matchesGoldenFile()`
- **Integration tests:** `integration_test/` with real backend or mocks
- Mocking: `mockito` / `mocktail` for generating mocks
- Coverage target: 80%+ on domain and data layers

### 10. Performance Optimization (Week 7–8)
- `const` constructors everywhere possible
- `ListView.builder` lazy rendering (never build all items)
- Image caching (`cached_network_image`)
- `RepaintBoundary` for complex animations
- `DevTools` profiler: timeline, widget rebuild tracking
- Minimize `setState` scope; prefer Riverpod selective rebuilds
- Tree-shaking, split imports, deferred loading

---

## The 20% That Unlocks 80%

| Concept | Why It Matters |
|---|---|
| Null safety + late final | Eliminates entire class of runtime crashes |
| `AsyncValue.when()` | Handles every async state in one expression |
| GoRouter redirect guards | Centralizes auth routing without scattered checks |
| Dio interceptors | Single place for token refresh, logging, retry logic |
| Clean Architecture layers | Makes every feature testable and replaceable |

---

## Daily Pattern

1h theory/tutorial → 3h build (one screen or feature) → 1h AI code review → 1h recall/Anki.

---

## Key Resources

| Topic | Resource |
|---|---|
| Dart language | [dart.dev](https://dart.dev) |
| Flutter docs | [flutter.dev](https://flutter.dev) |
| Riverpod | [riverpod.dev](https://riverpod.dev) |
| GoRouter | [pub.dev/packages/go_router](https://pub.dev/packages/go_router) |
| Dio | [pub.dev/packages/dio](https://pub.dev/packages/dio) |
| Flutter Testing | [docs.flutter.dev/testing](https://docs.flutter.dev/testing) |

---

## Practice Tasks

1. Scaffold the Flutter app with Clean Architecture folder structure
2. Build a login screen that calls `POST /auth/login` via Dio
3. Store JWT in secure storage; inject via interceptor
4. Implement GoRouter with auth redirect guard
5. Build a chat screen using Riverpod `AsyncNotifier`
6. Write widget tests for login form validation
7. Profile with DevTools and fix one performance bottleneck

---

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│              Presentation Layer             │
│  Pages → Widgets → State (Riverpod/BLoC)   │
├─────────────────────────────────────────────┤
│               Domain Layer                  │
│  Entities → Use Cases → Repository Interfaces│
├─────────────────────────────────────────────┤
│                Data Layer                   │
│  Repositories → Data Sources → Dio/Storage  │
├─────────────────────────────────────────────┤
│               Core / Shared                 │
│  Theme → Constants → Utils → Network Client  │
└─────────────────────────────────────────────┘
         ↕ HTTP (Dio)  ↕ Local Storage
┌──────────────────────┐  ┌──────────────────┐
│   Go Backend (API)   │  │   Qdrant / Redis  │
└──────────────────────┘  └──────────────────┘
```

### Data Flow for a Typical Feature

```
User taps "Login" button
    ↓
LoginPage (presentation) calls AuthNotifier.login()
    ↓
AuthNotifier (Riverpod AsyncNotifier) calls LoginUseCase
    ↓
LoginUseCase (domain) calls AuthRepository.login(email, password)
    ↓
AuthRepository (data) calls AuthRemoteDataSource via Dio
    ↓
Dio sends POST /auth/login → Go backend
    ↓
Response flows back up: Dio → DataSource → Repository → UseCase → Notifier → Page
    ↓
LoginPage rebuilds with AsyncValue (loading → data or error)
```

### State Management Decision Tree

```
Do you need to share state across multiple screens?
├─ YES → ProviderScope + global provider
└─ NO → local StateProvider or BLoC
    │
    Is the state async?
    ├─ YES → AsyncNotifier / FutureProvider
    └─ NO → Notifier / StateProvider
        │
        Does it have complex business logic?
        ├─ YES → Notifier with UseCase
        └─ NO → Simple StateProvider
```

### Error Handling Pattern

```dart
// Unified error handling across the app
class AppException implements Exception {
  final String message;
  final String? code;
  final int? statusCode;

  AppException({required this.message, this.code, this.statusCode});
}

// In repository
try {
  final response = await _dio.post('/auth/login', data: data);
  return Right(AuthToken.fromJson(response.data));
} on DioException catch (e) {
  return Left(ServerFailure(
    message: e.response?.data['message'] ?? 'Unknown error',
    statusCode: e.response?.statusCode,
  ));
}
```

### Testing Strategy

| Layer | Test Type | What to Test | Mocking |
|---|---|---|---|
| Domain | Unit | Use case logic, entity validation | None (pure Dart) |
| Data | Unit | Repository, data source, mapper | Mock Dio, Mock storage |
| Presentation | Widget | UI rendering, user interactions | Mock providers |
| Integration | E2E | Full flow with real/mock backend | Mock HTTP layer |

### Key Package Versions (recommended)

```yaml
dependencies:
  flutter_riverpod: ^2.5.0
  go_router: ^14.0.0
  dio: ^5.4.0
  flutter_secure_storage: ^9.0.0
  cached_network_image: ^3.3.0
  freezed_annotation: ^2.4.0
  json_annotation: ^4.8.0

dev_dependencies:
  mocktail: ^1.0.0
  build_runner: ^2.4.0
  freezed: ^2.5.0
  json_serializable: ^6.7.0
  integration_test: ^20.1.0
```

### Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| setState in parent | Entire page rebuilds on small change | Move state to Riverpod provider |
| No const constructors | Jank during scroll | Add `const` to all widgets possible |
| Fetching in initState | Missing lifecycle handling | Use `ref.watch()` or `ref.listen()` |
| Dio without baseUrl | Hardcoded URLs everywhere | Configure base URL in dio provider |
| Storing tokens in memory | Lost on app restart | Use flutter_secure_storage |
| No error boundary | White screen on crash | Wrap MaterialApp in ErrorWidget |

---

## Self-Check

Can you explain:
- How Riverpod's `ref.watch()` triggers rebuilds vs `ref.read()`?
- The data flow: page → provider → use case → repository → Dio → backend?
- When to use `StreamProvider` vs `FutureProvider`?
- How GoRouter's redirect guard prevents unauthenticated access?
- What makes an architectural layer "testable"?
- How to handle a 401 response globally via Dio interceptor?
- The difference between `ref.watch()` and `ref.listen()`?

---

## ملخص عربي (Arabic Summary)

مسار تطوير تطبيقات Flutter المحمولة: من أساسيات Dart إلى بناء تطبيق إنتاجي يتواصل مع
الخادم الخلفي. يشمل إدارة الحالة (Riverpod/BLoC)، التنقل (GoRouter)، الشبكة (Dio),
التخزين المحلي، الهندسة المعمارية النظيفة، والاختبارات. يึدم مخططات للمعمارية
تدفق البيانات، ومعالجة الأخطاء، واستراتيجية الاختبار، وأخطاء شائعة مع حلولها.
البناء التدريجي مع مراجعة الكود بالذكاء الاصطناعي.
