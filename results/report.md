# PosCacheBench Report

## Corpus

- Documents loaded: 21
- Evidence tasks: 63
- Benchmark rows: 4725

## Best Configurations

| encoding | policy | budget | top-k success | retention | mean mass | cost |
|---|---|---:|---:|---:|---:|---:|
| uniform | lexical_top | 0.10 | 1.000 | 1.000 | 0.6888 | 0.115 |
| uniform | geometry_top | 0.10 | 1.000 | 1.000 | 0.6888 | 0.115 |
| alibi_proxy | lexical_top | 0.10 | 1.000 | 1.000 | 0.6731 | 0.115 |
| decay | lexical_top | 0.10 | 1.000 | 1.000 | 0.6731 | 0.115 |
| rope_proxy | lexical_top | 0.10 | 1.000 | 1.000 | 0.6928 | 0.115 |
| sink_rope_proxy | lexical_top | 0.10 | 1.000 | 1.000 | 0.6855 | 0.115 |
| uniform | lexical_top | 0.25 | 1.000 | 1.000 | 0.4231 | 0.259 |
| uniform | geometry_top | 0.25 | 1.000 | 1.000 | 0.4231 | 0.259 |
| uniform | lexical_top | 0.50 | 1.000 | 1.000 | 0.3144 | 0.496 |
| uniform | geometry_top | 0.50 | 1.000 | 1.000 | 0.3144 | 0.496 |
| uniform | full | 0.10 | 1.000 | 1.000 | 0.2855 | 1.000 |
| uniform | full | 0.25 | 1.000 | 1.000 | 0.2855 | 1.000 |

## Policy x Budget Heatmap

| policy | 0.10 | 0.25 | 0.50 |
|---|---:|---:|---:|
| full | 0.917 | 0.917 | 0.917 |
| recent | 0.143 | 0.222 | 0.571 |
| lexical_top | 1.000 | 0.937 | 0.924 |
| geometry_top | 0.800 | 0.860 | 0.905 |
| stratified_geometry | 0.222 | 0.635 | 0.863 |

## Encoding x Policy Heatmap

| encoding | full | recent | lexical_top | geometry_top | stratified_geometry |
|---|---:|---:|---:|---:|---:|
| uniform | 1.000 | 0.312 | 1.000 | 1.000 | 0.640 |
| alibi_proxy | 0.873 | 0.312 | 0.931 | 0.746 | 0.534 |
| decay | 0.873 | 0.312 | 0.931 | 0.746 | 0.534 |
| rope_proxy | 0.921 | 0.312 | 0.952 | 0.884 | 0.577 |
| sink_rope_proxy | 0.921 | 0.312 | 0.952 | 0.899 | 0.582 |

## Recent-Only Failure Check

- Budget 0.10: recent top-k success 0.143, stratified_geometry 0.222, delta +0.079.
- Budget 0.25: recent top-k success 0.222, stratified_geometry 0.635, delta +0.413.
- Budget 0.50: recent top-k success 0.571, stratified_geometry 0.863, delta +0.292.

## Region Breakdown

| region | policy | budget | top-k success | retention |
|---|---|---:|---:|---:|
| early | recent | 0.10 | 0.000 | 0.000 |
| early | recent | 0.25 | 0.000 | 0.000 |
| early | recent | 0.50 | 0.000 | 0.000 |
| early | geometry_top | 0.10 | 0.486 | 0.486 |
| early | geometry_top | 0.25 | 0.600 | 0.743 |
| early | geometry_top | 0.50 | 0.733 | 0.943 |
| early | stratified_geometry | 0.10 | 0.000 | 0.000 |
| early | stratified_geometry | 0.25 | 0.248 | 0.390 |
| early | stratified_geometry | 0.50 | 0.610 | 0.819 |
| middle | recent | 0.10 | 0.000 | 0.000 |
| middle | recent | 0.25 | 0.000 | 0.000 |
| middle | recent | 0.50 | 0.714 | 0.714 |
| middle | geometry_top | 0.10 | 0.933 | 0.933 |
| middle | geometry_top | 0.25 | 0.981 | 0.981 |
| middle | geometry_top | 0.50 | 0.981 | 1.000 |
| middle | stratified_geometry | 0.10 | 0.048 | 0.048 |
| middle | stratified_geometry | 0.25 | 0.676 | 0.676 |
| middle | stratified_geometry | 0.50 | 0.981 | 1.000 |
| late | recent | 0.10 | 0.429 | 0.429 |
| late | recent | 0.25 | 0.667 | 0.667 |
| late | recent | 0.50 | 1.000 | 1.000 |
| late | geometry_top | 0.10 | 0.981 | 0.981 |
| late | geometry_top | 0.25 | 1.000 | 1.000 |
| late | geometry_top | 0.50 | 1.000 | 1.000 |
| late | stratified_geometry | 0.10 | 0.619 | 0.619 |
| late | stratified_geometry | 0.25 | 0.981 | 0.981 |
| late | stratified_geometry | 0.50 | 1.000 | 1.000 |

## Region x Policy Heatmap at 25% Budget

| region | recent | lexical_top | geometry_top | stratified_geometry |
|---|---:|---:|---:|---:|
| early | 0.000 | 0.810 | 0.600 | 0.248 |
| middle | 0.000 | 1.000 | 0.981 | 0.676 |
| late | 0.667 | 1.000 | 1.000 | 0.981 |

## Interpretation

If recent-only retention collapses on early or middle evidence while stratified geometry survives at the same budget, the result supports the project claim: KV-cache failure is not only a memory-size problem. It is a policy-plus-position problem.
