# Graph Report - .  (2026-08-02)

## Corpus Check
- 12 files · ~13,393 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 65 nodes · 112 edges · 8 communities detected
- Extraction: 73% EXTRACTED · 27% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.71)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]

## God Nodes (most connected - your core abstractions)
1. `run_benchmark()` - 10 edges
2. `score_chunks()` - 7 edges
3. `main()` - 7 edges
4. `main()` - 6 edges
5. `BenchmarkTests` - 6 edges
6. `BenchmarkConfig` - 6 edges
7. `ChunkScore` - 6 edges
8. `Document` - 6 edges
9. `build_tasks()` - 6 edges
10. `CorpusTests` - 5 edges

## Surprising Connections (you probably didn't know these)
- `CorpusTests` --uses--> `Document`  [INFERRED]
  tests/test_corpus.py → src/poscachebench/corpus.py
- `BenchmarkTests` --uses--> `BenchmarkConfig`  [INFERRED]
  tests/test_benchmark.py → src/poscachebench/benchmark.py
- `BenchmarkTests` --uses--> `ChunkScore`  [INFERRED]
  tests/test_benchmark.py → src/poscachebench/policies.py
- `score_chunks()` --calls--> `get_encoding()`  [INFERRED]
  src/poscachebench/benchmark.py → src/poscachebench/encodings.py
- `BenchmarkConfig` --uses--> `Document`  [INFERRED]
  src/poscachebench/benchmark.py → src/poscachebench/corpus.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.23
Nodes (12): BenchmarkRow, content_score(), evidence_mass(), evidence_rank(), run_benchmark(), score_chunks(), summarize(), write_csv() (+4 more)

### Community 1 - "Community 1"
Cohesion: 0.24
Nodes (10): build_tasks(), choose_query_terms(), chunk_tokens(), Document, EvidenceTask, iter_text_files(), load_documents(), strip_markdown() (+2 more)

### Community 2 - "Community 2"
Cohesion: 0.31
Nodes (6): BenchmarkConfig, budget_to_count(), ChunkScore, select_chunks(), _stratified_geometry(), BenchmarkTests

### Community 3 - "Community 3"
Cohesion: 0.39
Nodes (8): auth_status(), local_available(), main(), now(), packet(), Run two identical, independent paper-review councils and compare them., run_one(), write_comparison()

### Community 4 - "Community 4"
Cohesion: 0.4
Nodes (2): get_encoding(), PositionalEncodingProxy

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (3): main(), rate(), Verify the quantitative claims used by the internal paper draft.

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (3): main(), Generate paper figures from a pinned benchmark JSON artifact., success()

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (1): PosCacheBench package.

## Knowledge Gaps
- **4 isolated node(s):** `Run two identical, independent paper-review councils and compare them.`, `Verify the quantitative claims used by the internal paper draft.`, `Generate paper figures from a pinned benchmark JSON artifact.`, `PosCacheBench package.`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 7`** (2 nodes): `PosCacheBench package.`, `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_benchmark()` connect `Community 0` to `Community 1`, `Community 2`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `BenchmarkConfig` connect `Community 2` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `score_chunks()` connect `Community 0` to `Community 1`, `Community 2`, `Community 4`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `run_benchmark()` (e.g. with `load_documents()` and `build_tasks()`) actually correct?**
  _`run_benchmark()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `score_chunks()` (e.g. with `chunk_tokens()` and `get_encoding()`) actually correct?**
  _`score_chunks()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `main()` (e.g. with `BenchmarkConfig` and `run_benchmark()`) actually correct?**
  _`main()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BenchmarkTests` (e.g. with `BenchmarkConfig` and `ChunkScore`) actually correct?**
  _`BenchmarkTests` has 2 INFERRED edges - model-reasoned connections that need verification._