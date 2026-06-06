Project: PosCacheBench

Gap: Long-context inference systems preserve or evict KV blocks under memory pressure, but they fail to explain when positional encoding geometry makes far evidence unrecoverable under a fixed cache budget.

Stack: Python 3.10+, standard library only, Makefile, unittest, JSON/CSV/Markdown outputs.

Data: Real local Brain documents from `/Users/srini/Brain/raw` or another user-provided markdown/text corpus.

Build:
1. Corpus loader: read real markdown/text documents, strip metadata/markdown, tokenize, chunk, and produce long-document retrieval tasks. Verify with unit tests for tokenization, chunking, and task creation.
2. Positional encoding proxies: implement uniform, ALiBI-like decay, exponential decay, RoPE-like oscillatory proxy, and sink-augmented RoPE proxy. Verify weights are bounded and distance-sensitive.
3. Cache policies: implement full, recent-only, lexical top-k, geometry top-k, and stratified geometry. Verify budgets are respected and evidence selection is measurable.
4. Benchmark engine: run every task across encodings, policies, and budgets; emit retention, evidence rank, attention-mass proxy, success, and cost metrics. Verify JSON/CSV are reproducible.
5. Report generator: summarize success by encoding, policy, budget, and evidence region. Verify Markdown report includes the gap statement, best policies, and failure modes.

Benchmark against: full retention and recent-only retention.

Success: at 25% KV budget, `stratified_geometry` improves evidence top-k success over `recent` for early/middle evidence on real Brain documents while using the same cache budget.

