# PosCacheBench

Benchmarking how positional-attention geometry interacts with KV-cache budget pressure in long-context inference.

## Gap

Existing KV-cache benchmarks usually compare eviction or compression policies as if token importance is independent of the model's positional-attention geometry. In practice, a token can be semantically relevant but become fragile when the positional encoding, evidence distance, and cache budget conflict.

**Gap statement:** Long-context inference systems preserve or evict KV blocks under memory pressure, but they fail to explain when positional encoding geometry makes far evidence unrecoverable under a fixed cache budget. This matters because cache policies can look efficient on latency and memory while silently destroying long-range retrieval.

## What This Builds

PosCacheBench is a CPU-only benchmark harness that uses real local documents from Aryan's Brain as the corpus. It creates long-document retrieval tasks from real source text, then evaluates whether positional-attention proxy functions and KV retention policies preserve the evidence chunk under different cache budgets.

This is not a full LLM runtime. It is the first systems probe: isolate positional geometry and cache selection before spending GPU time on model-level evaluation.

## Research Base

Stored in `/Users/srini/Brain/ml/papers/inference/`:

- `Attention Is All You Need.pdf`
- `vLLM paper.pdf`
- `SGLang paper.pdf`
- `R-KV- RAN .pdf`
- `Using group theory to explore the space of positional encodings for attention.md`

Related Brain synthesis: `[[Jane Street ML Design Clippings]]`.

## System Design

```text
real Brain corpus
  -> document tokenization
  -> evidence tasks by position: early, middle, late
  -> positional-attention proxy scoring
  -> KV budget policies
  -> retention, rank, attention-mass, and cost metrics
  -> CSV/JSON/Markdown report
```

## Run

```bash
make test
make bench
```

Outputs:

- `results/benchmark.json`
- `results/benchmark.csv`
- `results/report.md`

Privacy note: JSON/CSV outputs can contain document titles and query terms from the local corpus, so they are ignored by git. Commit only aggregate reports unless the corpus is public.

You can point it at another corpus:

```bash
PYTHONPATH=src python3 -m poscachebench run --corpus /path/to/docs --report results/report.md
```

## Baselines

- `full`: keep every chunk.
- `recent`: keep only the most recent chunks.
- `lexical_top`: keep chunks with strongest query-term overlap.
- `geometry_top`: keep chunks with strongest overlap times positional weight.
- `stratified_geometry`: reserve recent chunks but also keep high-salience chunks across distance buckets.

## Encodings

These are scalar proxies for positional-attention behavior, not exact implementations of full model attention:

- `uniform`: content-only, no distance penalty.
- `alibi_proxy`: monotone linear-bias-like decay.
- `decay`: exponential recency pressure.
- `rope_proxy`: oscillatory phase-similarity proxy with mild long-range damping.
- `sink_rope_proxy`: RoPE proxy with attention-sink boost for the first chunks.

## Success Criteria

The project is useful if it can show:

- where `recent` cache retention fails on early or middle evidence,
- whether geometry-aware policies preserve more evidence at the same cache budget,
- which positional proxy is most fragile under fixed budget pressure,
- how much cache cost is saved relative to full retention.

Initial target:

```text
At 25% KV budget, stratified_geometry should improve evidence top-k success over recent-only retention on early/middle evidence, while using the same retained-token budget.
```

## Industry Alignment

- **NVIDIA:** inference serving, KV-cache management, GPU memory pressure, TensorRT-LLM-style runtime thinking.
- **Google DeepMind / Meta FAIR:** long-context model behavior, attention structure, evaluation methodology.
- **Microsoft / Azure AI:** serving infrastructure and cost-quality tradeoffs under production constraints.

## Brain Review

See `docs/BRAIN_REVIEW.md` for the project check against Aryan's Brain standards and the Jane Street clipping lessons that generated this project.
