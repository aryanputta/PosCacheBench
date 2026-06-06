# Design

## Core Question

When a long-context model must shrink its KV working set, does the failure come only from a small cache, or from a mismatch between cache policy and positional-attention geometry?

PosCacheBench isolates that question with a CPU benchmark.

## Derivation

For a query at decode step `q` and a previous chunk `i`, a simplified attention score can be written as:

$$
s_i = c(q, x_i)\,p(q-i)
$$

Here \(c(q, x_i)\) is content match and \(p(q-i)\) is a positional-attention proxy.

The real transformer uses learned query/key vectors and a positional encoding inside the attention dot product. This benchmark replaces learned vector similarity with a lexical evidence proxy so the experiment can run on real documents without a GPU.

The important systems variable is not the absolute score. It is whether the evidence chunk survives after a cache policy keeps only `B` out of `N` chunks:

$$
S_B = P(s, c, d, B)
$$

$$
A_k =
\mathbf{1}\left[e \in S_B \land r_B(e) \le k\right]
$$

If `recent` fails but `stratified_geometry` succeeds at the same budget, the project has evidence that cache policy needs distance-aware structure, not only recency.

Full formulas are in `docs/MATH.md`.

## Why This Is Different From Existing Aryan Projects

- `kvcache-bench` evaluates eviction policies directly.
- `EigenKache` explores landmark compression.
- `IntentCache` predicts future reasoning-useful blocks.
- `RKV-VL-Lab` evaluates multimodal decode compression.

PosCacheBench focuses on the missing diagnostic layer: whether positional geometry explains where cache policies fail before choosing a compression method.
