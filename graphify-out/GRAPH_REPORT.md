# Graph Report - .  (2026-06-06)

## Corpus Check
- 9 files · ~5,812 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 48 nodes · 90 edges · 9 communities detected
- Extraction: 67% EXTRACTED · 33% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.71)
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
- [[_COMMUNITY_Community 8|Community 8]]

## God Nodes (most connected - your core abstractions)
1. `run_benchmark()` - 10 edges
2. `score_chunks()` - 7 edges
3. `main()` - 7 edges
4. `BenchmarkTests` - 6 edges
5. `BenchmarkConfig` - 6 edges
6. `ChunkScore` - 6 edges
7. `Document` - 6 edges
8. `build_tasks()` - 6 edges
9. `CorpusTests` - 5 edges
10. `BenchmarkRow` - 5 edges

## Surprising Connections (you probably didn't know these)
- `CorpusTests` --uses--> `Document`  [INFERRED]
  tests/test_corpus.py → src/poscachebench/corpus.py
- `BenchmarkTests` --uses--> `BenchmarkConfig`  [INFERRED]
  tests/test_benchmark.py → src/poscachebench/benchmark.py
- `BenchmarkTests` --uses--> `ChunkScore`  [INFERRED]
  tests/test_benchmark.py → src/poscachebench/policies.py
- `BenchmarkConfig` --uses--> `Document`  [INFERRED]
  src/poscachebench/benchmark.py → src/poscachebench/corpus.py
- `BenchmarkConfig` --uses--> `EvidenceTask`  [INFERRED]
  src/poscachebench/benchmark.py → src/poscachebench/corpus.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.31
Nodes (6): BenchmarkConfig, budget_to_count(), ChunkScore, select_chunks(), _stratified_geometry(), BenchmarkTests

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (4): content_score(), score_chunks(), get_encoding(), PositionalEncodingProxy

### Community 2 - "Community 2"
Cohesion: 0.4
Nodes (3): write_csv(), build_parser(), main()

### Community 3 - "Community 3"
Cohesion: 0.7
Nodes (4): BenchmarkRow, evidence_mass(), evidence_rank(), run_benchmark()

### Community 4 - "Community 4"
Cohesion: 0.4
Nodes (4): iter_text_files(), load_documents(), strip_markdown(), tokenize()

### Community 5 - "Community 5"
Cohesion: 0.5
Nodes (2): Document, CorpusTests

### Community 6 - "Community 6"
Cohesion: 0.7
Nodes (4): build_tasks(), choose_query_terms(), chunk_tokens(), EvidenceTask

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (3): summarize(), write_json(), write_report()

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (1): PosCacheBench package.

## Knowledge Gaps
- **1 isolated node(s):** `PosCacheBench package.`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 8`** (2 nodes): `PosCacheBench package.`, `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_benchmark()` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.164) - this node is a cross-community bridge._
- **Why does `BenchmarkConfig` connect `Community 0` to `Community 2`, `Community 3`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `score_chunks()` connect `Community 1` to `Community 0`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `run_benchmark()` (e.g. with `load_documents()` and `build_tasks()`) actually correct?**
  _`run_benchmark()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `score_chunks()` (e.g. with `chunk_tokens()` and `get_encoding()`) actually correct?**
  _`score_chunks()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `main()` (e.g. with `BenchmarkConfig` and `run_benchmark()`) actually correct?**
  _`main()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BenchmarkTests` (e.g. with `BenchmarkConfig` and `ChunkScore`) actually correct?**
  _`BenchmarkTests` has 2 INFERRED edges - model-reasoned connections that need verification._