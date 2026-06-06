# Benchmark Heatmaps

These are the benchmark comparison tables from `results/report.md`. Regenerate them with:

```bash
make bench
```

## Policy x Budget

Top-k success averaged across encoding proxies and evidence regions.

| policy | 10% KV budget | 25% KV budget | 50% KV budget |
|---|---:|---:|---:|
| full | 0.917 | 0.917 | 0.917 |
| recent | 0.143 | 0.222 | 0.571 |
| lexical_top | 1.000 | 0.937 | 0.924 |
| geometry_top | 0.800 | 0.860 | 0.905 |
| stratified_geometry | 0.222 | 0.635 | 0.863 |

## Encoding x Policy

Top-k success averaged across cache budgets and evidence regions.

| encoding | full | recent | lexical_top | geometry_top | stratified_geometry |
|---|---:|---:|---:|---:|---:|
| uniform | 1.000 | 0.312 | 1.000 | 1.000 | 0.640 |
| alibi_proxy | 0.873 | 0.312 | 0.931 | 0.746 | 0.534 |
| decay | 0.873 | 0.312 | 0.931 | 0.746 | 0.534 |
| rope_proxy | 0.921 | 0.312 | 0.952 | 0.884 | 0.577 |
| sink_rope_proxy | 0.921 | 0.312 | 0.952 | 0.899 | 0.582 |

## Region x Policy at 25% Budget

This is the main failure-mode table. Recent-only cache retention collapses on early and middle evidence at the same budget where geometry-aware policies still recover evidence.

| evidence region | recent | lexical_top | geometry_top | stratified_geometry |
|---|---:|---:|---:|---:|
| early | 0.000 | 0.810 | 0.600 | 0.248 |
| middle | 0.000 | 1.000 | 0.981 | 0.676 |
| late | 0.667 | 1.000 | 1.000 | 0.981 |

## Main Takeaway

At 25% KV budget, `recent` scores 0.000 on early and middle evidence. That means the cache can look efficient while deleting the part of the context needed for long-range retrieval. `stratified_geometry` improves middle evidence to 0.676 under the same budget, and `geometry_top` reaches 0.981.
