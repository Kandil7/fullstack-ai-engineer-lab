# ThanaweyaGPT Frontend

> Flutter mobile application for the ThanaweyaGPT educational platform.

## Overview

A cross-platform mobile app built with Flutter that provides AI-powered tutoring, practice questions, exam building, and progress tracking for Egyptian high school students.

## Features

### Core Screens
1. **Home** - Dashboard with study progress and quick actions
2. **Chat** - AI tutor conversation with streaming responses
3. **Questions** - Practice question generator by subject and topic
4. **Exams** - Exam builder, timer, and history
5. **Analytics** - Progress charts and personalized insights
6. **Profile** - User settings and preferences

### Key Capabilities
- **Offline Support**: Cache conversations and questions for offline use
- **Streaming Responses**: Real-time AI responses with typing indicators
- **Arabic Support**: Full RTL text support for Arabic content
- **Dark Mode**: Eye-friendly dark theme for late-night studying
- **Push Notifications**: Study reminders and exam alerts

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Flutter 3.0+ | Cross-platform UI |
| **State Management** | Riverpod 3.0 | Reactive state |
| **Navigation** | GoRouter | Declarative routing |
| **HTTP Client** | Dio | API communication |
| **Local Storage** | Hive | Offline caching |
| **Charts** | fl_chart | Progress visualization |
| **Animations** | Rive | Smooth transitions |

## Project Structure

```
frontend/
├── lib/
│   ├── main.dart                # App entry point
│   ├── app.dart                 # App configuration
│   ├── config/
│   │   ├── theme.dart           # App theme
│   │   ├── routes.dart          # Route definitions
│   │   └── constants.dart       # App constants
│   ├── features/
│   │   ├── auth/
│   │   │   ├── screens/
│   │   │   │   ├── login_screen.dart
│   │   │   │   └── register_screen.dart
│   │   │   ├── providers/
│   │   │   │   └── auth_provider.dart
│   │   │   └── services/
│   │   │       └── auth_service.dart
│   │   ├── chat/
│   │   │   ├── screens/
│   │   │   │   ├── chat_screen.dart
│   │   │   │   └── conversation_list_screen.dart
│   │   │   ├── widgets/
│   │   │   │   ├── message_bubble.dart
│   │   │   │   └── typing_indicator.dart
│   │   │   ├── providers/
│   │   │   │   └── chat_provider.dart
│   │   │   └── services/
│   │   │       └── chat_service.dart
│   │   ├── questions/
│   │   │   ├── screens/
│   │   │   │   └── questions_screen.dart
│   │   │   ├── widgets/
│   │   │   │   ├── question_card.dart
│   │   │   │   └── option_tile.dart
│   │   │   └── providers/
│   │   │       └── questions_provider.dart
│   │   ├── exams/
│   │   │   ├── screens/
│   │   │   │   ├── exam_builder_screen.dart
│   │   │   │   ├── exam_screen.dart
│   │   │   │   └── exam_results_screen.dart
│   │   │   ├── widgets/
│   │   │   │   ├── timer_widget.dart
│   │   │   │   └── question_navigator.dart
│   │   │   └── providers/
│   │   │       └── exam_provider.dart
│   │   ├── analytics/
│   │   │   ├── screens/
│   │   │   │   └── analytics_screen.dart
│   │   │   └── widgets/
│   │   │       ├── progress_chart.dart
│   │   │       └── subject_card.dart
│   │   └── profile/
│   │       ├── screens/
│   │       │   └── profile_screen.dart
│   │       └── widgets/
│   │           └── settings_tile.dart
│   ├── shared/
│   │   ├── widgets/
│   │   │   ├── app_bar.dart
│   │   │   ├── button.dart
│   │   │   ├── card.dart
│   │   │   └── loading_indicator.dart
│   │   ├── services/
│   │   │   ├── api_service.dart
│   │   │   ├── storage_service.dart
│   │   │   └── notification_service.dart
│   │   └── models/
│   │       ├── user.dart
│   │       ├── message.dart
│   │       └── question.dart
│   └── core/
│       ├── network/
│       │   ├── api_client.dart
│       │   └── interceptors.dart
│       ├── utils/
│       │   ├── validators.dart
│       │   └── formatters.dart
│       └── extensions/
│           └── context_extensions.dart
├── assets/
│   ├── images/
│   ├── icons/
│   └── animations/
├── test/
├── android/
├── ios/
├── web/
├── pubspec.yaml
└── analysis_options.yaml
```

## State Management

### Riverpod Providers

```dart
// Auth Provider
@riverpod
class AuthNotifier extends _$AuthNotifier {
  @override
  AuthState build() => AuthState.initial();

  Future<void> login(String email, String password) async {
    state = const AuthState.loading();
    try {
      final user = await ref.read(authServiceProvider).login(email, password);
      state = AuthState.authenticated(user);
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }
}

// Chat Provider
@riverpod
class ChatNotifier extends _$ChatNotifier {
  @override
  List<Message> build() => [];

  Future<void> sendMessage(String content, String subject) async {
    final userMessage = Message(
      id: const Uuid().v4(),
      role: 'user',
      content: content,
      timestamp: DateTime.now(),
    );
    
    state = [...state, userMessage];
    
    // Stream AI response
    await for (final chunk in ref.read(chatServiceProvider).streamResponse(content, subject)) {
      // Update assistant message
    }
  }
}
```

## Navigation

### GoRouter Configuration

```dart
final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/chat',
      builder: (context, state) => const ChatScreen(),
    ),
    GoRoute(
      path: '/chat/:conversationId',
      builder: (context, state) => ConversationScreen(
        conversationId: state.pathParameters['conversationId']!,
      ),
    ),
    GoRoute(
      path: '/questions',
      builder: (context, state) => const QuestionsScreen(),
    ),
    GoRoute(
      path: '/exams',
      builder: (context, state) => const ExamsScreen(),
    ),
    GoRoute(
      path: '/exams/:examId',
      builder: (context, state) => ExamScreen(
        examId: state.pathParameters['examId']!,
      ),
    ),
    GoRoute(
      path: '/analytics',
      builder: (context, state) => const AnalyticsScreen(),
    ),
    GoRoute(
      path: '/profile',
      builder: (context, state) => const ProfileScreen(),
    ),
  ],
);
```

## Offline Support

### Caching Strategy

```dart
class StorageService {
  final HiveInterface _hive;
  
  Future<void> cacheConversation(Conversation conversation) async {
    final box = await _hive.openBox('conversations');
    await box.put(conversation.id, conversation.toJson());
  }
  
  Future<List<Conversation>> getCachedConversations() async {
    final box = await _hive.openBox('conversations');
    return box.values
        .map((json) => Conversation.fromJson(json))
        .toList();
  }
  
  Future<void> cacheQuestions(List<Question> questions) async {
    final box = await _hive.openBox('questions');
    for (final question in questions) {
      await box.put(question.id, question.toJson());
    }
  }
}
```

### Offline Queue

```dart
class OfflineQueue {
  final List<QueuedAction> _queue = [];
  
  Future<void> enqueue(QueuedAction action) async {
    _queue.add(action);
    await _persistQueue();
  }
  
  Future<void> processQueue(ApiClient api) async {
    for (final action in _queue.toList()) {
      try {
        await action.execute(api);
        _queue.remove(action);
      } catch (e) {
        // Retry later
      }
    }
    await _persistQueue();
  }
}
```

## UI Components

### Message Bubble

```dart
class MessageBubble extends StatelessWidget {
  final Message message;
  
  const MessageBubble({super.key, required this.message});
  
  @override
  Widget build(BuildContext context) {
    final isUser = message.role == 'user';
    
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.8,
        ),
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isUser
              ? Theme.of(context).colorScheme.primary
              : Theme.of(context).colorScheme.surface,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              message.content,
              style: TextStyle(
                color: isUser
                    ? Theme.of(context).colorScheme.onPrimary
                    : Theme.of(context).colorScheme.onSurface,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              DateFormat('HH:mm').format(message.timestamp),
              style: TextStyle(
                fontSize: 10,
                color: isUser
                    ? Theme.of(context).colorScheme.onPrimary.withOpacity(0.7)
                    : Theme.of(context).colorScheme.onSurface.withOpacity(0.5),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## Setup

### Prerequisites
- Flutter SDK 3.0+
- Dart SDK 3.0+
- Android Studio / VS Code
- iOS: Xcode (for iOS builds)

### Quick Start
```bash
# Navigate to frontend directory
cd projects/07-capstone/thanaweyagpt/frontend

# Install dependencies
flutter pub get

# Run on connected device
flutter run

# Run on specific platform
flutter run -d chrome  # Web
flutter run -d android # Android
flutter run -d ios     # iOS
```

### Building for Production

```bash
# Android APK
flutter build apk --release

# Android App Bundle
flutter build appbundle --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

## Testing

### Unit Tests
```bash
flutter test
```

### Widget Tests
```bash
flutter test test/widget/
```

### Integration Tests
```bash
flutter test integration_test/
```

## Performance Optimization

### Key Optimizations
- **Lazy loading**: Load conversations on demand
- **Image caching**: Cache AI-generated images
- **Code splitting**: Split by feature for faster initial load
- **Animation optimization**: Use Rive for complex animations
- **Memory management**: Dispose controllers properly

### Performance Targets
| Metric | Target |
|--------|--------|
| App startup time | < 2s |
| Screen transition | < 300ms |
| API response display | < 100ms |
| Memory usage | < 200MB |
| App size | < 50MB |

## Status

| Feature | Status |
|---------|--------|
| Project structure | ✅ Complete |
| Auth screens | ✅ Complete |
| Chat screen | 🔄 In Progress |
| Questions screen | ⬜ Not Started |
| Exam screen | ⬜ Not Started |
| Analytics screen | ⬜ Not Started |
| Offline support | ⬜ Not Started |

---

*Next: [AI Service](../ai/) — Python-based AI services for RAG and LLM integration.*
