# Flutter App — ThanaweyaGPT Mobile Client

Production Flutter application connecting to the Go backend, serving as the primary mobile
interface for the ThanaweyaGPT educational AI platform.

---

## Goals

- Build a production-quality Flutter app with clean architecture
- Implement real-time chat with the AI tutor via WebSocket and REST
- Handle authentication (JWT), session management, and offline caching
- Provide a smooth Arabic/English bilingual UI
- Demonstrate Flutter best practices: testing, state management, theming

---

## Tech Stack

| Layer            | Technology                  |
| ---------------- | --------------------------- |
| Framework        | Flutter 3.x / Dart 3.x      |
| State Management | Riverpod 2.x                |
| Navigation       | GoRouter                    |
| HTTP Client      | Dio + interceptors          |
| Local Storage    | Hive / SharedPreferences    |
| Testing          | flutter_test, mocktail       |
| Architecture     | Clean Architecture (3-layer)|
| Theming          | Material 3 + custom design  |

---

## Screen Map

| Screen   | Route              | Purpose                                |
| -------- | ------------------ | -------------------------------------- |
| Login    | `/login`           | Email/password auth, social login      |
| Chat     | `/chat`            | Real-time conversation with AI tutor   |
| Settings | `/settings`        | Theme, language, notification prefs    |
| Profile  | `/profile`         | User info, usage stats, subscription   |

---

## Architecture

```
lib/
├── core/                  # Shared utilities, constants, theme
│   ├── theme/
│   ├── utils/
│   └── network/
├── features/              # Feature-first organization
│   ├── auth/
│   │   ├── data/          # Repository impl, data sources
│   │   ├── domain/        # Entities, repository interface
│   │   └── presentation/  # Widgets, providers, screens
│   ├── chat/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   ├── settings/
│   └── profile/
└── main.dart
```

### State Management Approach

Riverpod is used exclusively — no Provider, Bloc, or GetX.

- **Providers** hold application state (auth state, chat messages, user prefs)
- **AsyncValue** handles loading/error/data states uniformly
- **StateNotifier** for complex state logic
- **StreamProvider** for WebSocket message streams

```dart
// Example: Chat messages provider
final chatProvider = StateNotifierProvider<ChatNotifier, AsyncValue<List<Message>>>((ref) {
  final chatRepo = ref.watch(chatRepositoryProvider);
  return ChatNotifier(chatRepo);
});
```

### Network Layer

Dio handles all HTTP communication with:

- **Auth interceptor** — attaches JWT to every request, handles 401 refresh
- **Logging interceptor** — debug-mode request/response logging
- **Retry interceptor** — exponential backoff for transient failures
- **Connectivity interceptor** — queues requests when offline

---

## Testing Strategy

| Layer        | Type              | Coverage Target |
| ------------ | ----------------- | --------------- |
| Domain       | Unit tests        | 90%+            |
| Data         | Unit tests + mock | 85%+            |
| Presentation | Widget tests      | 70%+            |
| Integration  | Integration tests | Critical paths  |

- **Unit tests** for repositories, use cases, and utilities
- **Widget tests** for individual screens and components
- **Integration tests** for auth flow and chat end-to-end
- **Golden tests** for visual regression on key components

Run tests:

```bash
flutter test                    # All unit and widget tests
flutter test --coverage         # With coverage report
flutter test integration_test/  # Integration tests (requires device)
```

---

## Connection to ThanaweyaGPT Capstone

This Flutter app is the **mobile client** for the ThanaweyaGPT capstone project
(`projects/07-capstone/thanaweyagpt`). It connects to:

- **Go backend** (`projects/01-backend-go/`) for auth, user management, chat routing
- **FastAPI AI services** (`projects/04-ai-engineering/`) for RAG, embeddings, agent orchestration
- **WebSocket** for real-time chat streaming

The app demonstrates the full-stack integration: Flutter → Go API → AI services → PostgreSQL/Redis/Qdrant.

---

## Getting Started

```bash
# Install dependencies
flutter pub get

# Run on connected device
flutter run

# Run tests
flutter test

# Build release APK
flutter build apk --release
```

---

## Key Decisions

| Decision              | Choice          | Rationale                                |
| --------------------- | --------------- | ---------------------------------------- |
| State management      | Riverpod        | Type-safe, testable, compile-time checks |
| Navigation            | GoRouter        | Declarative, deep linking support        |
| HTTP client           | Dio             | Interceptors, cancellation, transforms   |
| Local storage         | Hive            | Fast, type-safe, no native dependencies  |
| Architecture          | Clean Arch      | Separation of concerns, testability      |

See `docs/decisions/` for formal ADRs.
