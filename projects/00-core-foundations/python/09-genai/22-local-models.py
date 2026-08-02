"""
GenAI - 22: Local Models
========================
Topics: Ollama/llama.cpp, quantized GGUF, VRAM math, throughput vs
quality, when local beats API on cost and privacy.

Why this matters for AI/backend engineering:
    Local models are a real architecture option: no per-token cost, data
    never leaves your network, offline capable. But they cost VRAM, GPU
    time, and engineering. The skill is the math: what fits, at what
    quality, for what throughput.

Run:      python 22-local-models.py
Verify:   python 22-local-models.py --verify
Reference: https://github.com/ggerganov/llama.cpp
"""

from __future__ import annotations

import sys


# ============================================================
# 1. VRAM Math
# ============================================================
# Model size (GB) = params x bits / 8. Plus overhead for KV cache
# and activations. Quantization (GGUF) is the size lever.

def model_gb(params_billions: float, bits: int) -> float:
    return params_billions * 1e9 * bits / 8 / (1024 ** 3)


# Example 1: quantization shrinks models
for bits, label in [(16, "fp16"), (8, "int8"), (4, "q4")]:
    gb = model_gb(7.0, bits)
    print(f"Example 1: 7B @ {label} -> {gb:.1f} GB")
assert model_gb(7.0, 4) < model_gb(7.0, 16), "q4 much smaller"

# ============================================================
# 2. Does It Fit? VRAM Budget
# ============================================================

def fits_in_vram(model_size_gb: float, kv_cache_gb: float,
                 vram_gb: float) -> tuple[bool, float]:
    total = model_size_gb + kv_cache_gb
    return total <= vram_gb, total


# Example 2: fit check
ok, total = fits_in_vram(model_gb(7.0, 4), kv_cache_gb=2.0, vram_gb=8.0)
print("\nExample 2: VRAM fit")
print(f"  7B q4 + 2GB KV = {total:.1f}GB in 8GB card -> fits: {ok}")
assert ok
ok2, total2 = fits_in_vram(model_gb(7.0, 16), kv_cache_gb=2.0, vram_gb=8.0)
print(f"  7B fp16 + 2GB KV = {total2:.1f}GB -> fits: {ok2}")
assert not ok2, "fp16 does not fit 8GB"

# ============================================================
# 3. Throughput
# ============================================================

def throughput_tokens_per_sec(gpu_tflops: float, model_flops_per_token: float) -> float:
    return gpu_tflops * 1e12 / model_flops_per_token


# Example 3: throughput estimate (tokens/s)
tps = throughput_tokens_per_sec(20.0, model_flops_per_token=7e9 * 2)
print("\nExample 3: throughput")
print(f"  ~{tps:.0f} tokens/s on a 20 TFLOPS GPU for a 7B model")

# ============================================================
# 4. Throughput vs Quality
# ============================================================
# Lower quantization = faster, but quality drops. The curve is
# measured, not guessed: run your eval at each quantization level.

def quality_at_quant(bits: int, base_quality: float) -> float:
    """Simple quality model: 16-bit is reference; 4-bit loses a bit."""
    return base_quality * (0.95 if bits >= 16 else (0.90 if bits == 8 else 0.82))


# Example 4: quality vs quantization
print("\nExample 4: quantization quality")
for bits in [16, 8, 4]:
    print(f"  {bits}-bit: quality {quality_at_quant(bits, 0.95):.2f}")
assert quality_at_quant(4, 0.95) < quality_at_quant(16, 0.95)

# ============================================================
# 5. Local vs API: The Decision
# ============================================================

def local_vs_api(monthly_api_cost: float, privacy_required: bool,
                 offline_required: bool, vram_available_gb: float,
                 model_size_gb: float) -> str:
    if privacy_required or offline_required:
        if vram_available_gb >= model_size_gb:
            return "LOCAL: privacy/offline needs + hardware fits"
        return "NEEDS HARDWARE: privacy/offline needed but VRAM too small"
    if monthly_api_cost > 500:  # threshold in dollars
        return "LOCAL: API cost justifies the GPU investment"
    return "API: below cost threshold and no privacy constraint"


# Example 5: the decision
print("\nExample 5: local vs API")
print("  " + local_vs_api(5000, False, False, 24.0, model_gb(7.0, 4)))
print("  " + local_vs_api(50, False, False, 8.0, model_gb(70.0, 4)))
print("  " + local_vs_api(200, True, False, 24.0, model_gb(7.0, 4)))
assert local_vs_api(5000, False, False, 24.0, model_gb(7.0, 4)).startswith("LOCAL")
assert local_vs_api(50, False, False, 8.0, model_gb(70.0, 4)).startswith("API")

# ============================================================
# Production Pattern
# ============================================================
# The production checklist: pick quant by eval, confirm VRAM, measure
# throughput against SLO, then deploy.

def local_deploy_checklist(quant_bits: int, eval_score: float,
                           min_score: float, vram_free: float,
                           model_size: float, kv_size: float) -> list[str]:
    issues = []
    if eval_score < min_score:
        issues.append(f"quant {quant_bits}-bit scores {eval_score:.2f} < {min_score}")
    if vram_free < model_size + kv_size:
        issues.append("insufficient VRAM")
    return issues


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: buying a GPU for a model that does not fit its VRAM
# MISTAKE: 4-bit everything "for speed" without measuring quality
# MISTAKE: ignoring KV cache when budgeting VRAM
# MISTAKE: running local when the API is cheaper and fine on privacy


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    assert model_gb(1.0, 16) > model_gb(1.0, 4), "quantization shrinks"
    assert model_gb(7.0, 4) < 8.0, "7B q4 under 8GB"

    ok, total = fits_in_vram(5.0, 1.0, 8.0)
    assert ok and total == 6.0
    assert not fits_in_vram(8.0, 1.0, 8.0)[0]

    assert throughput_tokens_per_sec(20.0, 1e10) == 2000.0

    assert quality_at_quant(4, 1.0) < quality_at_quant(16, 1.0)
    assert quality_at_quant(16, 1.0) == 0.95

    assert local_vs_api(1000, False, False, 24.0, 4.0).startswith("LOCAL")
    assert local_vs_api(100, False, False, 24.0, 4.0).startswith("API")
    assert local_vs_api(0, True, False, 8.0, 20.0).startswith("NEEDS HARDWARE")

    assert local_deploy_checklist(4, 0.7, 0.8, 16.0, 4.0, 1.0), "quality below min"
    assert not local_deploy_checklist(8, 0.9, 0.8, 16.0, 4.0, 1.0), "all good"
    print("[OK] 22-local-models: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. VRAM = params x bits; quantization is the size lever.")
        print("2. Budget the KV cache too; measure throughput.")
        print("3. Local for privacy/offline/big-bills; API below that.")
        _verify()
