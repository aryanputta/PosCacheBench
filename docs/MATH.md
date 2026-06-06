# Math Model

PosCacheBench uses a CPU proxy for the part of transformer inference that matters for this project: whether a relevant past chunk remains useful after the KV working set is compressed.

## Attention Proxy

For a query at decode step \(q\) and a previous chunk \(i\), define:

$$
s_i = c(q, x_i)\,p(q-i)
$$

where:

- \(c(q, x_i)\) is the content match between the query terms and chunk \(x_i\)
- \(p(q-i)\) is the positional-attention proxy for distance \(q-i\)
- \(s_i\) is the salience score used by geometry-aware cache policies

The benchmark is not claiming this is exact model attention. It is an isolation test for the systems question:

$$
\text{Does positional geometry change which evidence survives under a fixed KV budget?}
$$

## Content Score

For query terms \(T\) and chunk tokens \(x_i\):

$$
c(q, x_i) = \frac{1}{|T|}\sum_{t \in T}\mathbf{1}[t \in x_i]\left(1 + 0.25 \cdot \min(\operatorname{count}_{x_i}(t)-1, 3)\right)
$$

This makes repeated evidence terms count slightly more, but caps repetition so one repeated word cannot dominate the score.

## Positional Proxies

Uniform:

$$
p_{\text{uniform}}(d)=1
$$

ALiBI-style monotone decay:

$$
p_{\text{alibi}}(d)=e^{-\alpha d}
$$

Exponential recency decay:

$$
p_{\text{decay}}(d)=e^{-d/\tau}
$$

RoPE-style phase proxy:

$$
p_{\text{rope}}(d)=\max\left(0.05,\ |\cos(d/8)|e^{-d/(2D)}\right)
$$

Sink-augmented RoPE proxy:

$$
p_{\text{sink-rope}}(d,i)=p_{\text{rope}}(d)+0.35\cdot\mathbf{1}[i<2]
$$

where \(d=q-i\), \(D\) is the maximum distance in the document, and \(i<2\) marks the first two chunks as attention-sink candidates.

## Cache Budget

For a document with \(N\) chunks and budget ratio \(b\):

$$
B = \max(1,\ \operatorname{round}(bN))
$$

A policy selects:

$$
S_B \subset \{0,\ldots,N-1\}, \quad |S_B| \le B
$$

## Success Metric

Let \(e\) be the evidence chunk. The benchmark records top-k success as:

$$
\operatorname{success@k} =
\mathbf{1}\left[e \in S_B \land \operatorname{rank}_{S_B}(e) \le k\right]
$$

Evidence mass is:

$$
m_e =
\frac{s_e}{\sum_{j \in S_B} s_j}
$$

if \(e \in S_B\), otherwise \(m_e=0\).

## What The Heatmaps Show

The report heatmaps compare:

- evidence region: early, middle, late
- cache policy: recent, lexical, geometry, stratified geometry
- budget: 10%, 25%, 50%

The important pattern is not that one policy wins everywhere. The important pattern is where recent-only retention collapses:

$$
\Delta =
\operatorname{success@k}_{\text{stratified-geometry}}
-
\operatorname{success@k}_{\text{recent}}
$$

At 25% budget in the first run:

$$
\Delta = 0.635 - 0.222 = 0.413
$$

That is the first evidence for the project claim: cache failure is a policy-plus-position failure, not only a cache-size failure.

