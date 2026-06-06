# Brain Review

This review checks PosCacheBench against Aryan's Brain standards and the Jane Street clipping lessons that created the project.

## What The Brain Says To Preserve

- [[Project Style]]: every project needs a real gap, real data, reproducible commands, modular code, tests, and benchmark artifacts.
- [[Jane Street ML Design Clippings]]: prototype fast, but make the prototype a disposable proposal with a clear benchmark gate.
- [[Technical Mindset]]: inspect structure and failure modes before claiming optimization wins.
- [[AI Inference Optimization]]: treat [[positional encodings]] as systems-relevant sequence geometry because they affect [[KV cache]] pressure and long-context retrieval.

## Code Check

The implementation matches the first project milestone:

- `corpus.py` uses real local markdown/text documents instead of synthetic examples.
- `encodings.py` isolates positional-attention proxies so the assumptions are explicit.
- `policies.py` separates cache selection logic from scoring logic.
- `benchmark.py` emits reproducible JSON, CSV, and Markdown outputs.
- `tests/` checks tokenization, chunking, budgets, policies, and encoding sanity.

## What We Learned From Jane Street

The Jane Street design workflow lesson is not "ship AI-generated code." It is: make the idea executable early so reviewers can test the actual behavior. PosCacheBench does this by turning the vague claim "position matters for KV cache retention" into a runnable benchmark.

The positional-encoding article gives the technical frame: attention depends on relative position through constrained mathematical structure. PosCacheBench turns that into a systems question:

```text
When the cache budget shrinks, does the positional structure help or hurt evidence recovery?
```

The reverse-engineering and visualization articles add the debugging posture: do not only report an aggregate score. Inspect where the system fails by region, distance, and policy.

## Current Evidence

First local run:

- Corpus: 21 real Brain raw documents
- Evidence tasks: 63
- Benchmark rows: 4,725
- Unit tests: 6 passed

At 25% KV budget:

- `recent` top-k success: 0.222
- `stratified_geometry` top-k success: 0.635
- delta: +0.413

Interpretation: recency-only retention collapses on early and middle evidence, while geometry-aware selection preserves more evidence at the same budget.

## Publishing Note

The detailed JSON/CSV outputs are ignored because they are generated from private Brain documents and may contain document titles or query terms. The aggregate Markdown report is safe enough for a private repo, but a future public repo should use a public long-context dataset mode.

## Next Code Review Targets

1. Replace scalar positional proxies with measured attention traces from a small Hugging Face model.
2. Add a public dataset adapter so the repo can become public without Brain leakage.
3. Add plots for evidence distance versus success.
4. Convert `geometry_top` from an oracle diagnostic into an implementable online policy.
5. Add CI once the repo is public or has stable dependency policy.

