# ThanaweyaGPT

> AI-powered educational platform for Egyptian high school students.

## Overview

ThanaweyaGPT is a comprehensive AI tutoring system designed specifically for Egyptian high school students (Thanaweya Amma). It combines RAG (Retrieval-Augmented Generation) with custom AI agents to provide personalized, curriculum-aligned educational support.

### Why ThanaweyaGPT?

Egypt's Thanaweya Amma (high school leaving exam) is one of the most important exams in a student's life. ThanaweyaGPT aims to:

1. **Democratize access** to high-quality tutoring
2. **Provide 24/7 availability** for last-minute questions
3. **Align with the curriculum** (Egyptian Ministry of Education)
4. **Track progress** and identify weak areas
5. **Reduce exam anxiety** through practice and preparation

## Features

### 🎓 AI Tutor
- Ask questions in Arabic or English
- Get step-by-step explanations
- Curriculum-aligned responses
- Support for Math, Physics, Chemistry, Biology

### 📝 Question Generator
- Generate practice questions by topic
- Multiple choice, short answer, and problem-solving
- Difficulty levels (easy, medium, hard)
- Past exam question patterns

### 📊 Exam Builder
- Create custom exams from question bank
- Timer and auto-grading
- Detailed score analysis
- Recommended study topics

### 📈 Analytics Dashboard
- Track study time and progress
- Identify weak areas
- Compare with class average
- Personalized study recommendations

### 👨‍💼 Admin Panel
- Manage curriculum content
- Monitor student usage
- Analyze system performance
- Manage AI model configurations

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Flutter | Cross-platform mobile app |
| **Backend** | Go | API services, auth, CRUD |
| **AI Service** | Python | RAG pipeline, LLM integration |
| **LLM** | GPT-4 / Claude | Natural language understanding |
| **Vector DB** | Qdrant | Curriculum content retrieval |
| **Database** | PostgreSQL | User data, conversations |
| **Cache** | Redis | Sessions, rate limiting |
| **Infra** | Docker + K8s | Containerization, orchestration |
| **Monitoring** | Prometheus + Grafana | Metrics, dashboards |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Flutter Mobile App                           │
│                    (Android, iOS, Web)                              │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        API Gateway (Kong)                           │
│                    Rate Limiting, Auth, Routing                     │
└─────────┬───────────────────────┬───────────────────────┬───────────┘
          │                       │                       │
          ▼                       ▼                       ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   Auth Service  │   │  Chat Service   │   │  User Service   │
│      (Go)       │   │      (Go)       │   │      (Go)       │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   PostgreSQL    │   │     Redis       │   │   PostgreSQL    │
│  (Users, Auth)  │   │  (Cache, Rate)  │   │ (User Profiles) │
└─────────────────┘   └────────┬────────┘   └─────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    AI Gateway       │
                    │     (Python)        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
    ┌─────────────────┐ ┌───────────────┐ ┌───────────────┐
    │   LLM APIs      │ │   Qdrant      │ │  Curriculum   │
    │ (GPT-4/Claude)  │ │ (Vector DB)   │ │  (JSON/YAML)  │
    └─────────────────┘ └───────────────┘ └───────────────┘
```

## Project Structure

```
thanaweyagpt/
├── backend/           # Go API services
├── frontend/          # Flutter mobile app
├── ai/                # Python AI services
├── infra/             # Docker, K8s, deployment
└── docs/              # Documentation
```

## Curriculum Coverage

### Current Coverage (Phase 1)
- [x] Mathematics (Grade 12)
- [x] Physics (Grade 12)
- [ ] Chemistry (Grade 12)
- [ ] Biology (Grade 12)

### Planned Coverage (Phase 2)
- [ ] All subjects (Grades 10-12)
- [ ] Arabic language support
- [ ] Past exam questions (2015-2024)

## Getting Started

### Prerequisites
- Flutter SDK 3.0+
- Go 1.22+
- Python 3.11+
- Docker & Docker Compose

### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-username/thanaweyagpt.git
cd thanaweyagpt

# Start all services
docker-compose up -d

# Run Flutter app
cd frontend
flutter run
```

### Development Setup
```bash
# Backend
cd backend
make dev

# AI Service
cd ai
pip install -r requirements.txt
make dev

# Frontend
cd frontend
flutter pub get
flutter run
```

## API Documentation

API docs are available at `http://localhost:8080/docs` when running locally.

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login user |
| POST | /chat | Send message to AI tutor |
| GET | /questions/generate | Generate practice questions |
| POST | /exams/create | Create custom exam |
| GET | /analytics/progress | Get study progress |

## Mobile App Screenshots

### Key Screens
1. **Home** - Dashboard with study progress
2. **Chat** - AI tutor conversation
3. **Questions** - Practice question generator
4. **Exams** - Exam builder and history
5. **Analytics** - Progress charts and insights
6. **Profile** - User settings and preferences

## Performance Targets

| Metric | Target |
|--------|--------|
| First response latency | < 2s |
| Question generation time | < 5s |
| Exam grading time | < 10s |
| App startup time | < 3s |
| Offline support | Basic Q&A |

## Roadmap

### Phase 1: MVP (Months 1-3)
- [ ] Core chat functionality
- [ ] Basic question generation
- [ ] User authentication
- [ ] Progress tracking

### Phase 2: Enhancement (Months 4-6)
- [ ] Exam builder
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Offline mode

### Phase 3: Scale (Months 7-9)
- [ ] All subjects coverage
- [ ] Teacher dashboard
- [ ] Parent portal
- [ ] School integration

### Phase 4: Polish (Months 10-12)
- [ ] Performance optimization
- [ ] Accessibility features
- [ ] App store launch
- [ ] Marketing website

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](../../LICENSE) for details.

## Contact

- **Project Lead**: [Your Name]
- **Email**: contact@thanaweyagpt.com
- **Website**: https://thanaweyagpt.com

---

*Built with ❤️ for Egyptian students preparing for Thanaweya Amma.*
