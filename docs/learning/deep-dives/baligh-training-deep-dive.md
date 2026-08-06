# Deep Dive: Baligh LLM Fine-Tuning

**Last updated:** 2026-08-06

**Context:** Fine-tuning and deploying a specialized LLM for Arabic domain-specific tasks,
covering dataset preparation, training methodology, evaluation, and production deployment.

---

## 1. Why Fine-Tune a Base Model?

### When Fine-Tuning Makes Sense
- **Domain vocabulary:** base models struggle with specialized terminology
  - Legal Arabic, medical Arabic, technical Arabic have unique vocabularies
- **Style alignment:** need specific response format or tone
  - Formal MSA vs conversational, structured vs free-form
- **Task specialization:** focused performance on specific task types
  - Classification, extraction, summarization for a narrow domain
- **Cost optimization:** smaller fine-tuned model can replace larger general model
  - 7B fine-tuned on domain task ≈ 70B general model for that specific task
- **Data sovereignty:** keep sensitive domain data within your infrastructure

### When NOT to Fine-Tune
- Simple prompt engineering can solve the task
- Insufficient training data (< 100 high-quality examples)
- Task is too broad — fine-tuning narrows capability
- Base model already performs well on the task

---

## 2. Dataset Preparation

### Data Sources
- Internal documentation (manuals, guides, FAQs)
- Domain-specific corpora (Arabic Wikipedia, Al Jazeera, published papers)
- Synthetic data: use GPT-4/Claude to generate training examples from templates
- Human-annotated data: domain experts label responses

### Data Format
```json
{
  "instruction": "Summarize the following Arabic legal text in 2-3 sentences.",
  "input": "ينص القانون على أن كل عقد يجب أن يكون...',
  "output": "يلزم القانون أن تتضمن العقود ثلاثة عناصر أساسية: التراضي والأهلية والموضوع القانوني."
}
```

### Arabic-Specific Data Quality

**Diacritics Normalization**
- Decide: include or strip diacritics consistently
- Most fine-tuning works better with stripped diacritics (reduces noise)
- Exception: poetry, Quranic text, or diacritics-dependent content

**Text Cleaning**
```python
import re

def clean_arabic(text: str) -> str:
    # Normalize alef variants: أ إ آ → ا
    text = re.sub(r'[أإآ]', 'ا', text)
    # Normalize ta marbuta: ة → ه
    text = re.sub(r'ة', 'ه', text)
    # Normalize ya: ي → ى (at end of word)
    text = re.sub(r'ي(?=\s|$)', 'ى', text)
    # Remove tatweel (kashida)
    text = re.sub(r'\u0640', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

**Quality Checklist**
- [ ] Consistent encoding (UTF-8)
- [ ] No mixed encoding artifacts (mojibake)
- [ ] Balanced dialect representation (if targeting colloquial)
- [ ] No duplicate instructions (exact and semantic)
- [ ] Minimum output length: 20+ tokens (avoid trivial responses)
- [ ] Maximum output length: within model context window
- [ ] Instruction variety: rephrase similar tasks differently

### Dataset Size Guidelines
| Task Type | Minimum | Recommended | Ideal |
|---|---|---|---|
| Classification | 200 | 1,000 | 5,000+ |
| Summarization | 500 | 2,000 | 10,000+ |
| Q&A | 500 | 3,000 | 10,000+ |
| Code generation | 1,000 | 5,000 | 20,000+ |

---

## 3. Training Methodology

### Model Selection
- **Base model:** Llama 3.1 8B, Mistral 7B, or Arabic-specialized (Jais, AceGPT)
- **Why 7-8B:** fine-tunable on single GPU (A100 40GB), good quality/cost ratio
- **Arabic consideration:** multilingual models (Llama, Mistral) handle Arabic decently;
  Arabic-specific models (Jais) may be better for pure Arabic tasks

### Fine-Tuning Approaches

**Full Fine-Tuning**
- Update all model parameters
- Best quality, highest compute cost
- Requires: A100 80GB or multi-GPU setup
- Use when: sufficient compute budget, maximum quality needed

**LoRA (Low-Rank Adaptation)**
- Freeze base model, train low-rank adapter matrices
- ~1-5% of parameters are trainable
- Good quality, much lower compute cost
- Requires: single A100 40GB or even consumer GPU (24GB)
- Use when: limited compute, good quality acceptable

**QLoRA**
- LoRA on quantized (4-bit) base model
- Even lower memory, slight quality tradeoff
- Requires: single 24GB GPU (RTX 4090)
- Use when: minimal compute budget

### Hyperparameters
```yaml
# LoRA fine-tuning config
model: meta-llama/Llama-3.1-8B
method: lora
lora_rank: 16           # rank of adapter matrices
lora_alpha: 32          # scaling factor
lora_dropout: 0.05      # regularization

training:
  epochs: 3
  batch_size: 4
  gradient_accumulation: 8  # effective batch size = 32
  learning_rate: 2e-4
  warmup_steps: 100
  weight_decay: 0.01
  max_seq_length: 2048

optimizer: adamw
scheduler: cosine
  
# Data split
train_split: 0.9
eval_split: 0.1
```

### Training Monitoring
- **Loss curves:** training loss should decrease smoothly; watch for overfitting
- **Eval loss:** should decrease then plateau; if it increases → overfitting
- **Learning rate:** warmup then cosine decay
- **Gradient norms:** spikes indicate instability
- **GPU memory:** ensure no OOM during training

---

## 4. Evaluation Methodology

### Automated Metrics

**Perplexity**
- Measures how "surprised" the model is by held-out text
- Lower = better language modeling
- Use: general quality signal, not task-specific

**BLEU / ROUGE**
- BLEU: n-precision overlap with reference (generation quality)
- ROUGE: n-recall overlap with reference (summary quality)
- Limitations: poor correlation with human judgment for Arabic

**Task-Specific Metrics**
- Classification: accuracy, F1, precision, recall
- Extraction: exact match, token-level F1
- Summarization: ROUGE-L, factual consistency score

### Human Evaluation
- **5-point Likert scale** for:
  - Fluency (is the Arabic natural?)
  - Accuracy (is the information correct?)
  - Relevance (does it answer the question?)
  - Completeness (is anything missing?)
- **Side-by-side comparison:** fine-tuned vs base model, blind evaluation
- **Domain expert review:** essential for specialized content

### Evaluation Dataset
```
evaluation/
├── classification/
│   └── test_100.jsonl     # 100 classification examples
├── summarization/
│   └── test_50.jsonl      # 50 summarization examples
├── qa/
│   └── test_100.jsonl     # 100 Q&A examples
└── general/
    └── test_50.jsonl      # 50 general Arabic tasks
```

---

## 5. Deployment

### Model Export
```python
# Merge LoRA weights with base model
from peft import PeftModel
from transformers import AutoModelForCausalLM

base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
model = PeftModel.from_pretrained(base_model, "./checkpoint-500")
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./baligh-merged")
```

### Quantization for Inference
- **GPTQ:** post-training quantization, good quality at 4-bit
- **AWQ:** activation-aware quantization, faster inference
- **GGUF:** for CPU/edge inference (llama.cpp)

### Serving Options
| Option | Latency | Cost | Complexity |
|---|---|---|---|
| vLLM | ~50ms/token | GPU server | Medium |
| TGI | ~60ms/token | GPU server | Medium |
| Ollama | ~100ms/token | Local GPU | Low |
| API (replicate) | Variable | Pay-per-use | Very Low |

### Production Considerations
- **Batching:** vLLM's continuous batching for high throughput
- **Prompt caching:** cache system prompts and common prefixes
- **Rate limiting:** per-user quotas to prevent abuse
- **A/B testing:** compare fine-tuned vs base model on real traffic
- **Monitoring:** latency, throughput, error rate, token usage
- **Rollback:** keep previous model version ready for instant revert

---

## 6. Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Overfitting | Train loss ↓, eval loss ↑ | More data, early stopping, dropout |
| Catastrophic forgetting | Good at fine-tuned task, bad at general | LoRA instead of full fine-tune, mix in general data |
| Data leakage | Perfect eval scores, poor real-world | Ensure no overlap between train/eval |
| Inconsistent diacritics | Garbled Arabic output | Normalize all data consistently |
| Style collapse | All outputs sound the same | Diverse training examples, temperature > 0 |

---

## Self-Check

Can you explain:
- When LoRA is preferable to full fine-tuning?
- How to normalize Arabic text for consistent training data?
- The difference between BLEU and human evaluation for Arabic?
- Why catastrophic forgetting happens and how to prevent it?
- The deployment tradeoffs between vLLM, TGI, and Ollama?

---

## ملخص عربي (Arabic Summary)

نظرة معمقة في صقل نموذج Baligh للغة العربية: اختيار النموذج الأساسي، تحضير البيانات
مع التطبيع الصرفي، منهجيات التدريب (LoRA/QLoRA)، التقييم التلقائي والبشري، ونشر
الإنتاج. يشمل فخاخ شائعة مثل التعلق الزائد والنسيان الكارثي وتسرب البيانات.
