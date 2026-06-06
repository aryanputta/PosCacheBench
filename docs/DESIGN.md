# Design

## Core Question

When a long-context model must shrink its KV working set, does the failure come only from a small cache, or from a mismatch between cache policy and positional-attention geometry?

PosCacheBench isolates that question with a CPU benchmark.

## Derivation

For a query at decode step `q` and a previous chunk `i`, a simplified attention score can be written as:

```text
score(i) = content_match(query, chunk_i) * positional_weight(q - i)
```

The real transformer uses learned query/key vectors and a positional encoding inside the attention dot product. This benchmark replaces learned vector similarity with a lexical evidence proxy so the experiment can run on real documents without a GPU.

The important systems variable is not the absolute score. It is whether the evidence chunk survives after a cache policy keeps only `B` out of `N` chunks:

```text
selected = policy(score, content_match, distance, budget=B)
success = evidence_chunk in selected and rank(evidence_chunk) <= top_k
```

If `recent` fails but `stratified_geometry` succeeds at the same budget, the project has evidence that cache policy needs distance-aware structure, not only recency.

## Why This Is Different From Existing Aryan Projects

- `kvcache-bench` evaluates eviction policies directly.
- `EigenKache` explores landmark compression.
- `IntentCache` predicts future reasoning-useful blocks.
- `RKV-VL-Lab` evaluates multimodal decode compression.

PosCacheBench focuses on the missing diagnostic layer: whether positional geometry explains where cache policies fail before choosing a compression method.

