# LLM Fundamentals — Glossary 01

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Autoregressive | Generation | Predicting the next token and feeding it back |
| Context Window | Model | Total tokens a model can attend to at once |
| Hallucination | Failure | Confidently generated content that is false |
| Sampling | Generation | Picking a token from a probability distribution |
| Temperature | Generation | Knob shaping distribution randomness |
| Token | Model | The model's unit of text: word, subword, or char |
| Tokenizer | Model | Maps text to token IDs and back |
| Vocabulary | Model | The set of tokens a model knows |

## Detailed Definitions
### Autoregressive
**Definition**: Generation loop: predict next token, append it, repeat.
```python
while len(out) < max_tokens:
    nxt = sample(model(out))
    out.append(nxt)
```
**Related**: Sampling

### Context Window
**Definition**: The maximum tokens (input + output) the model can attend to.
**Related**: Token

### Hallucination
**Definition**: Output that is fluent but false; structural risk of LLMs.
**Related**: Temperature

### Sampling
**Definition**: Selecting the next token from the model's probability
distribution.
**Related**: Temperature, Autoregressive

### Temperature
**Definition**: Scaling that flattens (high) or sharpens (low) the next-token
distribution.
**Related**: Sampling

### Token
**Definition**: The atomic text unit the model reads and writes.
**Related**: Tokenizer

### Tokenizer
**Definition**: Component converting text ↔ token IDs.
**Related**: Token

### Vocabulary
**Definition**: The complete token set of a tokenizer.
**Related**: Tokenizer

## Key Concepts Summary
### The Rules
- Models predict tokens, not text
- Context is a hard budget
- No memory, no ground truth

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Token — ___
2. Temperature — ___
3. Context window — ___
4. Autoregressive — ___
5. Hallucination — ___

**Answers:** 1-c, 2-e, 3-a, 4-b, 5-d where a=max attention budget, b=predict
next then feed back, c=text unit, d=fluent falsehood, e=randomness knob.
