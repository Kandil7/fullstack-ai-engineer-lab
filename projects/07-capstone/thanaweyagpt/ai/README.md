# ThanaweyaGPT AI Services

> Python-based AI services for RAG pipeline, LLM integration, and intelligent agents.

## Overview

The AI layer provides the intelligence behind ThanaweyaGPT. It handles curriculum content retrieval, natural language understanding, question generation, and exam creation using modern AI techniques.

## Components

### 1. RAG Pipeline
- Curriculum content ingestion
- Embedding generation
- Semantic search
- Context retrieval

### 2. LLM Integration
- Multi-provider support (GPT-4, Claude, Gemini)
- Prompt template management
- Response streaming
- Token counting and cost tracking

### 3. AI Agents
- Tutor agent (Q&A)
- Question generator agent
- Exam builder agent
- Analytics agent

### 4. Evaluation
- Response quality scoring
- Curriculum alignment checking
- Hallucination detection
- A/B testing framework

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AI Gateway (FastAPI)                         │
│                    Rate Limiting, Load Balancing                    │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  RAG Service  │ │ LLM Service   │ │ Agent Service │
│  (Embeddings) │ │ (Generation)  │ │ (Orchestrate) │
└───────┬───────┘ └───────┬───────┘ └───────┬───────┘
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   Qdrant      │ │   LLM APIs    │ │   Tools       │
│ (Vector DB)   │ │ (OpenAI/etc)  │ │ (Functions)   │
└───────────────┘ └───────────────┘ └───────────────┘
```

## RAG Pipeline

### Content Ingestion

```python
# Curriculum content structure
curriculum_content = {
    "subject": "mathematics",
    "grade": 12,
    "unit": 1,
    "topic": "derivatives",
    "content": """
    المشتقات في الرياضيات
    
    التعريف: المشتقة هي معدل تغير الدالة بالنسبة لمتغيرها
    
    القواعد:
    1. مشتقة الثابت = 0
    2. مشتقة x^n = n*x^(n-1)
    3. مشتقة e^x = e^x
    """,
    "examples": [
        "إذا كانت f(x) = x²، فإن f'(x) = 2x",
        "إذا كانت f(x) = 3x³، فإن f'(x) = 9x²"
    ],
    "metadata": {
        "difficulty": "medium",
        "exam_weight": 0.15,
        "prerequisites": ["algebra", "functions"]
    }
}
```

### Embedding Generation

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    async def generate_embedding(self, text: str) -> list[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    async def generate_batch_embeddings(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
```

### Vector Storage (Qdrant)

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

class VectorStore:
    def __init__(self):
        self.client = QdrantClient(host="localhost", port=6333)
        self._ensure_collection()
    
    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if "curriculum" not in [c.name for c in collections]:
            self.client.create_collection(
                collection_name="curriculum",
                vectors_config=VectorParams(
                    size=384,  # MiniLM output size
                    distance=Distance.COSINE
                )
            )
    
    async def upsert_content(self, content_id: str, embedding: list[float], metadata: dict):
        self.client.upsert(
            collection_name="curriculum",
            points=[
                PointStruct(
                    id=content_id,
                    vector=embedding,
                    payload=metadata
                )
            ]
        )
    
    async def search(self, query_embedding: list[float], limit: int = 5) -> list[dict]:
        results = self.client.search(
            collection_name="curriculum",
            query_vector=query_embedding,
            limit=limit
        )
        return [
            {"id": r.id, "score": r.score, "payload": r.payload}
            for r in results
        ]
```

## LLM Integration

### Multi-Provider Support

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def stream(self, prompt: str, **kwargs):
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = openai.AsyncOpenAI(api_key=api_key)
    
    async def generate(self, prompt: str, model: str = "gpt-4", **kwargs) -> str:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    async def stream(self, prompt: str, model: str = "gpt-4", **kwargs):
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            **kwargs
        )
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
    
    async def generate(self, prompt: str, model: str = "claude-3-opus", **kwargs) -> str:
        response = await self.client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text
```

### Prompt Templates

```python
from string import Template

TUTOR_SYSTEM_PROMPT = Template("""
أنت مدرس خبير في مادة $subject للثانوية العامة المصرية.

التعليمات:
1. اشرح المفاهيم بطريقة واضحة وبسيطة
2. استخدم أمثلة من المنهج الدراسي
3. قدم خطوات حل المسائل
4. راجع الإجابات مع الطالب
5. شجع الطالب على الممارسة

المعلومات الأكاديمية:
$context

اجب عن سؤال الطالب بشكل مفيد ومحترف.
""")

QUESTION_GENERATOR_PROMPT = Template("""
أنشئ $count أسئلة لمادة $subject في موضوع $topic.

المستوى: $difficulty
النوع: $question_type

التعليمات:
1. يجب أن تكون الأسئلة متوافقة مع منهج الثانوية العامة
2. قدم إجابات نموذجية مع شرح
3. اذكر الدرجة لكل سؤال
4. تنوّن في أنواع الأسئلة

المعلومات الأكاديمية:
$context

أرجع الإجابة بصيغة JSON.
""")
```

### Model Router

```python
class ModelRouter:
    def __init__(self):
        self.providers = {
            "openai": OpenAIProvider(settings.OPENAI_API_KEY),
            "claude": ClaudeProvider(settings.CLAUDE_API_KEY),
        }
        
        self.model_config = {
            "simple_question": {
                "free": "gpt-3.5-turbo",
                "pro": "gpt-4-turbo",
            },
            "complex_analysis": {
                "free": "gpt-4-turbo",
                "pro": "gpt-4-turbo",
            },
            "creative_writing": {
                "free": "claude-3-haiku",
                "pro": "claude-3-opus",
            },
        }
    
    def select_model(self, task_type: str, user_tier: str) -> tuple[str, str]:
        config = self.model_config.get(task_type, {})
        model = config.get(user_tier, "gpt-4-turbo")
        
        if model.startswith("gpt"):
            return "openai", model
        elif model.startswith("claude"):
            return "claude", model
        
        return "openai", "gpt-4-turbo"
```

## AI Agents

### Tutor Agent

```python
class TutorAgent:
    def __init__(self, rag_service: RAGService, llm_service: LLMService):
        self.rag = rag_service
        self.llm = llm_service
    
    async def answer_question(
        self,
        question: str,
        subject: str,
        conversation_history: list[dict]
    ) -> AsyncGenerator[str, None]:
        # 1. Retrieve relevant context
        context = await self.rag.retrieve_context(question, subject)
        
        # 2. Build prompt with context
        prompt = TUTOR_SYSTEM_PROMPT.substitute(
            subject=subject,
            context=context
        )
        
        # 3. Add conversation history
        messages = [{"role": "system", "content": prompt}]
        for msg in conversation_history[-10:]:  # Last 10 messages
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": question})
        
        # 4. Stream response
        async for chunk in self.llm.stream(messages):
            yield chunk
```

### Question Generator Agent

```python
class QuestionGeneratorAgent:
    def __init__(self, rag_service: RAGService, llm_service: LLMService):
        self.rag = rag_service
        self.llm = llm_service
    
    async def generate_questions(
        self,
        subject: str,
        topic: str,
        count: int = 5,
        difficulty: str = "medium",
        question_type: str = "multiple_choice"
    ) -> list[dict]:
        # 1. Retrieve curriculum context
        context = await self.rag.retrieve_context(
            f"{subject} {topic}",
            subject
        )
        
        # 2. Build prompt
        prompt = QUESTION_GENERATOR_PROMPT.substitute(
            count=count,
            subject=subject,
            topic=topic,
            difficulty=difficulty,
            question_type=question_type,
            context=context
        )
        
        # 3. Generate questions
        response = await self.llm.generate(prompt)
        
        # 4. Parse and validate
        questions = json.loads(response)
        return self._validate_questions(questions)
    
    def _validate_questions(self, questions: list[dict]) -> list[dict]:
        validated = []
        for q in questions:
            if self._is_valid_question(q):
                validated.append(q)
        return validated
```

### Exam Builder Agent

```python
class ExamBuilderAgent:
    def __init__(self, question_service: QuestionService, llm_service: LLMService):
        self.questions = question_service
        self.llm = llm_service
    
    async def build_exam(
        self,
        user_id: str,
        subject: str,
        duration: int = 60,
        topics: list[str] = None
    ) -> dict:
        # 1. Get user's weak areas
        weak_areas = await self._analyze_weak_areas(user_id, subject)
        
        # 2. Select questions based on weak areas
        questions = await self.questions.select_questions(
            subject=subject,
            topics=topics or weak_areas,
            count=self._calculate_question_count(duration)
        )
        
        # 3. Create exam
        exam = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "subject": subject,
            "duration": duration,
            "questions": questions,
            "created_at": datetime.now().isoformat()
        }
        
        return exam
    
    def _calculate_question_count(self, duration: int) -> int:
        # Roughly 2 minutes per question
        return max(10, duration // 2)
```

## Evaluation

### Response Quality Scorer

```python
class ResponseEvaluator:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
    
    async def evaluate_response(
        self,
        question: str,
        response: str,
        context: str
    ) -> dict:
        prompt = f"""
        قيّم جودة الإجابة التالية:
        
        السؤال: {question}
        الإجابة: {response}
        السياق: {context}
        
        قيّم على المقياس من 1-10:
        1. الدقة العلمية (Scientific Accuracy)
        2. وضوح الشرح (Clarity)
        3. اكتمال الإجابة (Completeness)
        4. التوافق مع المنهج (Curriculum Alignment)
        
        أرجع الإجابة بصيغة JSON.
        """
        
        evaluation = await self.llm.generate(prompt)
        return json.loads(evaluation)
```

### Hallucination Detector

```python
class HallucinationDetector:
    def __init__(self, rag_service: RAGService, llm_service: LLMService):
        self.rag = rag_service
        self.llm = llm_service
    
    async def detect_hallucination(
        self,
        response: str,
        context: str
    ) -> dict:
        # 1. Extract claims from response
        claims = await self._extract_claims(response)
        
        # 2. Verify each claim against context
        verified = []
        for claim in claims:
            is_supported = await self._verify_claim(claim, context)
            verified.append({
                "claim": claim,
                "supported": is_supported
            })
        
        # 3. Calculate hallucination score
        unsupported = sum(1 for v in verified if not v["supported"])
        score = unsupported / len(verified) if verified else 0
        
        return {
            "score": score,
            "claims": verified,
            "hallucinated": score > 0.3
        }
```

## Project Structure

```
ai/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Configuration
│   ├── dependencies.py         # Dependency injection
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── rag.py          # RAG endpoints
│   │   │   ├── llm.py          # LLM endpoints
│   │   │   └── agents.py       # Agent endpoints
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth.py         # JWT validation
│   │       └── rate_limit.py   # Rate limiting
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── embedding.py    # Embedding service
│   │   │   ├── vector_store.py # Qdrant integration
│   │   │   └── retriever.py    # Context retrieval
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── providers.py    # LLM providers
│   │   │   ├── router.py       # Model routing
│   │   │   └── templates.py    # Prompt templates
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── tutor.py        # Tutor agent
│   │   │   ├── question_gen.py # Question generator
│   │   │   └── exam_builder.py # Exam builder
│   │   └── evaluation/
│   │       ├── __init__.py
│   │       ├── quality.py      # Quality scoring
│   │       └── hallucination.py # Hallucination detection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request.py          # Request models
│   │   └── response.py         # Response models
│   └── utils/
│       ├── __init__.py
│       ├── tokenizer.py        # Token counting
│       └── cache.py            # Response caching
├── data/
│   ├── curriculum/             # Curriculum content
│   │   ├── mathematics/
│   │   ├── physics/
│   │   ├── chemistry/
│   │   └── biology/
│   └── embeddings/             # Pre-computed embeddings
├── tests/
├── Dockerfile
├── requirements.txt
├── pyproject.toml
└── Makefile
```

## Setup

### Prerequisites
- Python 3.11+
- Qdrant (or Docker)
- OpenAI API key
- Anthropic API key (optional)

### Quick Start
```bash
# Navigate to AI directory
cd projects/07-capstone/thanaweyagpt/ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Run ingestion script
python scripts/ingest_curriculum.py

# Start server
uvicorn app.main:app --reload

# Server runs on http://localhost:8000
```

### Environment Variables
```bash
# Copy and customize
cp .env.example .env

# Required
OPENAI_API_KEY=sk-...
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Optional
ANTHROPIC_API_KEY=sk-ant-...
REDIS_URL=redis://localhost:6379
```

## API Documentation

API docs available at `http://localhost:8000/docs` when running locally.

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /rag/search | Semantic search in curriculum |
| POST | /llm/chat | Chat completion |
| POST | /llm/stream | Streaming chat |
| POST | /agents/tutor | Ask tutor question |
| POST | /agents/questions | Generate questions |
| POST | /agents/exam | Build exam |
| POST | /evaluate/response | Evaluate response |

## Performance Targets

| Metric | Target |
|--------|--------|
| Embedding generation | < 100ms |
| RAG retrieval | < 200ms |
| First token latency | < 1s |
| Response generation | < 5s |
| Question generation | < 10s |

## Status

| Component | Status |
|-----------|--------|
| RAG Pipeline | 🔄 In Progress |
| LLM Integration | ✅ Complete |
| Tutor Agent | 🔄 In Progress |
| Question Generator | ⬜ Not Started |
| Exam Builder | ⬜ Not Started |
| Evaluation | ⬜ Not Started |

---

*Next: [Infrastructure](../infra/) — Docker, Kubernetes, and deployment.*
