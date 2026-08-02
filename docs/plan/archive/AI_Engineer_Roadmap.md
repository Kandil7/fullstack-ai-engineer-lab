# خطة الوصول لـ AI Engineer (Remote) - دليل شامل

> خطة full-time (5+ ساعات يومياً) - المدة الإجمالية: 8-10 أسابيع للجاهزية الأولى + مسار مستمر بعد كده

---

## الفلسفة الأساسية

- 20% نظري + 80% مشاريع فعلية
- كل مرحلة = تعلم concept واحد → تطبيقه فوراً بالكود → كسره عمداً وفهم ليه فشل → الانتقال للي بعده
- مشروع واحد متراكم طول الخطة بدل مشاريع متفرقة
- كل التوثيق والكود بالإنجليزي من اليوم الأول

---

## المشروع: "DevMate" - AI Assistant لمستودعات الكود

تطبيق بياخد GitHub repo أو مجلد docs، يجاوب أسئلة عنه، يشرح الكود، ويقترح تعديلات.
هيتطور من: CLI بسيط → RAG chatbot → API منشور → Agent كامل → نظام production-ready.

---

## الأسبوع 1: Python Refresher + بيئة الشغل

### المذاكرة
- يوم 1-2: مراجعة OOP (magic methods)، Decorators، Generators (`yield`)، Async/Await، Type Hints
- يوم 3: Git بعمق (branching, merge conflicts, rebase)
- يوم 4-5: NumPy/Pandas أساسيات عملية + virtual environments (poetry)
- يوم 6-7: بناء script يقرا كود من repo ويطلع إحصائيات (عدد functions, classes...)

### المصادر
| الموضوع | المصدر |
|---|---|
| Git | learngitbranching.js.org (تفاعلي، مجاني) |
| NumPy/Pandas | kaggle.com/learn |
| Python OOP/Async | مراجعة ذاتية + تطبيق مباشر في الكود |

### الناتج
بيئة شغل جاهزة + أول commits في المشروع + repo منظم بـ README إنجليزي

---

## الأسبوع 2: LLM APIs + Prompt Engineering

### المذاكرة
- يوم 1-2: Claude/OpenAI API - استدعاء أساسي، streaming، structured outputs
- يوم 3-4: Prompt Engineering (zero-shot, few-shot, chain-of-thought)
- يوم 5: Function calling أساسيات
- يوم 6-7: بناء CLI بيتكلم مع LLM (من غير RAG لسه)

### المصادر
| الموضوع | المصدر |
|---|---|
| Claude API | docs.claude.com |
| Prompt Engineering | promptingguide.ai |
| كورس قصير | DeepLearning.AI: "ChatGPT Prompt Engineering for Developers" |
| كتاب (بالتوازي) | AI Engineering - Chip Huyen (فصول 1-3) |

### الناتج
أداة CLI شغالة بتتكلم مع LLM

---

## الأسبوع 3-4: RAG بالتفصيل

### المذاكرة
**الأسبوع 3:**
- Embeddings (إزاي تشتغل، إمتى تستخدم إيه)
- Chunking strategies - جرب 3 طرق مختلفة وقارن النتائج
- ChromaDB - إعداد واستخدام

**الأسبوع 4:**
- Retrieval + re-ranking
- دمج الـ RAG مع الأداة - ياخد repo، يعمل embed، ويجاوب أسئلة

### المصادر
| الموضوع | المصدر |
|---|---|
| RAG من الصفر | DeepLearning.AI: "Building and Evaluating Advanced RAG" |
| Embeddings | Hugging Face: Sentence Transformers docs |
| Vector DB | ChromaDB Getting Started docs |
| RAG متقدم | Activeloop free RAG course |
| كتاب | AI Engineering - Chip Huyen (فصل RAG) |

### قاعدة مهمة
جرب بنفسك الأول، اقرا الفصل في الكتاب بعدين — مش العكس.

### الناتج
RAG chatbot شغال على repo حقيقي

---

## الأسبوع 5: FastAPI + Deployment

### المذاكرة
- يوم 1-2: FastAPI - endpoints, Pydantic, async
- يوم 3: Docker - containerize المشروع
- يوم 4-5: Deploy على Railway/Render
- يوم 6-7: واجهة بسيطة (Streamlit أو React)

### المصادر
| الموضوع | المصدر |
|---|---|
| FastAPI | fastapi.tiangolo.com/tutorial (الرسمي، كافي 100%) |
| Docker | docker-curriculum.com |
| Deployment | docs Railway/Render مباشرة |
| Streamlit | docs.streamlit.io |

### الناتج
المشروع منشور على لينك حقيقي — أول حاجة تحطها في CV

---

## الأسبوع 6-7: Agents + MCP

### المذاكرة
**الأسبوع 6:**
- Tool use / function calling بعمق
- ReAct pattern
- LangGraph أساسيات
- MCP (Model Context Protocol) - يوم أو يومين، أصبح standard في الوظائف الحديثة

**الأسبوع 7:**
- تحويل المشروع لـ Agent: يبحث في الكود، يشغّل tests، يقترح fixes، يستخدم أكتر من tool

### المصادر
| الموضوع | المصدر |
|---|---|
| Agents | Hugging Face Agents Course (مجاني + شهادة) |
| LangGraph | docs الرسمية |
| Function calling | Claude/OpenAI docs |

### قاعدة مهمة
ابدأ بـ agent واحد بأداة واحدة، ضيف tools تدريجياً بعد ما يشتغل صح.

### الناتج
Agent حقيقي بيستخدم عدة أدوات

---

## الأسبوع 8: Production-Readiness

### المذاكرة
- يوم 1-2: Evaluation (RAGAS) - قيّم دقة المشروع
- يوم 3: Caching بـ Redis
- يوم 4: Monitoring (Langfuse)
- يوم 5: Guardrails بسيطة (input validation, rate limiting)
- يوم 6-7: Testing (pytest) + Documentation احترافية

### المصادر
| الموضوع | المصدر |
|---|---|
| Evaluation | docs.ragas.io |
| Monitoring | langfuse.com/docs (self-host مجاني) |
| Testing | pytest official docs |
| كتاب | The LLM Engineering Handbook |

### الناتج
مشروع بمعايير production حقيقية

---

## الأسبوع 9: Portfolio + التقديم (Remote-focused)

- يوم 1-2: Blog post تقني عن المشروع (بالإنجليزي)
- يوم 3: CV + LinkedIn (تجهيز لسوق remote دولي)
- يوم 4-5: بدء التقديم
- يوم 6-7: مراجعة الفجوات اللي ظهرت من المقابلات

### منصات التقديم لـ Remote
| المنصة | النوع |
|---|---|
| Wellfound (AngelList) | startups remote عالمياً |
| RemoteOK, We Work Remotely | لوائح remote متخصصة |
| LinkedIn (فلتر Remote) | networking + تقديم |
| Toptal, Turing | contracting/freelance كبداية |
| workatastartup.com (YC) | شركات ناشئة remote-first |

### أمور عملية للـ Remote
- افهم الفرق بين W-2 وContractor (1099) وEOR (Deel, Remote.com)
- افتح حساب Wise أو Payoneer لاستقبال الدفعات
- انتبه لـ timezone overlap مع الفريق (3-4 ساعات تفضيل شائع)

---

## الأسبوع 10+: مستمر

- System Design أساسيات (Designing Data-Intensive Applications - فصول مختارة)
- Fine-tuning (LoRA/QLoRA) لو مطلوب في وظائف معينة
- كتاب Designing ML Systems - Chip Huyen
- متابعة الـ evaluation/observability tools الأعمق

---

## المصادر الكاملة (مرجع سريع)

### كورسات مجانية
- Google Machine Learning Crash Course
- fast.ai
- Hugging Face Courses (NLP + Agents)
- DeepLearning.AI short courses (متعددة، لكل موضوع كورس ساعة-ساعتين)
- Activeloop RAG courses

### كتب (بالترتيب)
1. **AI Engineering** - Chip Huyen (2025) — الأهم، اقراه كامل
2. **The LLM Engineering Handbook** - Paul Iusztin & Maxime Labonne — عملي جداً
3. **Designing Machine Learning Systems** - Chip Huyen (2022) — system-level thinking
4. Hands-On Machine Learning - Aurélien Géron (مرجع لأساسيات ML/DL)
5. Designing Data-Intensive Applications - Martin Kleppmann (system design عام)

### أدوات المشروع
| الفئة | الأداة |
|---|---|
| Orchestration | LangChain, LangGraph, LlamaIndex |
| Serving | FastAPI |
| Vector DB | ChromaDB |
| Evaluation | RAGAS |
| Observability | Langfuse |
| Deployment | Docker + Railway/Render |
| Cache | Redis |

---

## الإنجليزي التقني (مدمج طول الخطة، مش منفصل)

- كل كود، commits، وdocs بالإنجليزي من اليوم الأول
- 3 مرات أسبوعياً (30-45 دقيقة): مشاهدة tech talk / قراءة مقال وتلخيصه / تسجيل نفسك بتشرح مشروعك
- أدوات: Grammarly, DeepL (للمراجعة مش الترجمة الكاملة)
- الأسبوع 8-9: mock interviews بالإنجليزي

### أسئلة مقابلات للتمرين

**Behavioral:**
1. Walk me through your background and why you're interested in AI engineering
2. Tell me about a project you built. What was the biggest technical challenge?
3. Describe a time you had to debug a system that wasn't behaving as expected
4. How do you stay updated with the fast-moving AI/LLM landscape?
5. Tell me about a time you disagreed with a technical decision

**Technical - LLM/RAG:**
6. Walk me through how you'd design a RAG pipeline for a company with a million documents
7. Difference between fine-tuning and RAG - when to choose each?
8. How do you handle hallucination in an LLM-powered application?
9. Explain chunking strategies and how you decide chunk size
10. Semantic search vs keyword search - when to combine them?
11. How would you evaluate RAG response quality?
12. What is prompt injection and how do you defend against it?
13. Trade-offs between different vector databases

**Technical - System Design:**
14. Design an AI chatbot for e-commerce customer support
15. How to reduce LLM latency without sacrificing quality?
16. How do you control costs in production LLM systems?
17. What if the LLM API you depend on goes down?
18. What monitoring would you put in production?

**Technical - Agents:**
19. Explain the ReAct pattern
20. How do you prevent an agent from infinite loops?
21. Role of function calling in agent systems

**Questions to ask them:**
25. What does the LLM/AI stack look like here?
26. How does the team approach evaluation and monitoring in production?
27. What's the biggest technical challenge the team faces right now?

---

## مرتبات مرجعية (Remote/US، 2026)

| المستوى | Base Salary |
|---|---|
| Entry-level | $115K–$135K |
| Mid-level | $140K–$185K |
| Senior | $220K–$310K base ($340K–$550K total comp) |
| Staff/Principal | $280K–$400K base ($500K–$800K total comp) |
| Frontier labs (Senior) | $300K–$500K+ total comp |

⚠️ "AI Engineer" بيعني مسميات وظيفية مختلفة جداً — الفرق بين applied generalist وresearch engineer ممكن يوصل 3x في نفس المستوى.

---

## طريق الوصول لـ Senior (بعد الوظيفة الأولى)

### الفرق الجوهري
من "تنفيذ" لـ "قرارات معمارية" - تقرر هل RAG هو الحل الصح أصلاً، تصمم أنظمة تتحمل scale حقيقي، تتوقع نقط الفشل قبل حدوثها.

### خطوات عملية
1. بعد junior/mid: خد مشاريع فيها غموض (ambiguity) بدل مهام واضحة
2. ابدأ تكتب عن شغلك من أول سنة (blog)
3. ساهم بجدية في open source project واحد
4. دور على mentor
5. طور فهم عميق في: distributed systems, fine-tuning متقدم, evaluation frameworks, infrastructure (Kubernetes, cost optimization)

### Timeline تقريبي
- Junior: 0-2 سنة
- Mid: 2-4 سنين
- Senior: 4-6+ سنين (المجال الحديث ده ممكن يبقى أسرع)

---

## القواعد الذهبية للتنفيذ

1. متقفش عند خطأ أكتر من 30-45 دقيقة
2. اكتب docs وأنت شغال مش في الآخر
3. Commit يومي على الأقل
4. آخر ساعة كل يوم = مراجعة مش تعلم جديد
5. لو حسيت إنك بتدور على مصدر إضافي "عشان تتأكد إنك فاهم" - ده علامة إنك بتأجل. ارجع للكود.
