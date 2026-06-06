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

## Interpretation

If recent-only retention collapses on early or middle evidence while stratified geometry survives at the same budget, the result supports the project claim: KV-cache failure is not only a memory-size problem. It is a policy-plus-position problem.
