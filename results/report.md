# PosCacheBench Report

## Corpus

- Documents loaded: 32
- Evidence tasks: 96
- Benchmark rows: 7200

## Best Configurations

| encoding | policy | budget | top-k success | retention | mean mass | cost |
|---|---|---:|---:|---:|---:|---:|
| uniform | lexical_top | 0.25 | 0.979 | 1.000 | 0.3390 | 0.259 |
| uniform | geometry_top | 0.25 | 0.979 | 1.000 | 0.3390 | 0.259 |
| uniform | lexical_top | 0.50 | 0.979 | 1.000 | 0.2574 | 0.496 |
| uniform | geometry_top | 0.50 | 0.979 | 1.000 | 0.2574 | 0.496 |
| uniform | full | 0.10 | 0.979 | 1.000 | 0.2364 | 1.000 |
| uniform | full | 0.25 | 0.979 | 1.000 | 0.2364 | 1.000 |
| uniform | full | 0.50 | 0.979 | 1.000 | 0.2364 | 1.000 |
| uniform | lexical_top | 0.10 | 0.979 | 0.979 | 0.5526 | 0.111 |
| uniform | geometry_top | 0.10 | 0.979 | 0.979 | 0.5526 | 0.111 |
| uniform | stratified_geometry | 0.50 | 0.958 | 0.979 | 0.3161 | 0.496 |
| alibi_proxy | lexical_top | 0.10 | 0.917 | 0.979 | 0.5436 | 0.111 |
| decay | lexical_top | 0.10 | 0.917 | 0.979 | 0.5436 | 0.111 |

## Policy x Budget Heatmap

| policy | 0.10 | 0.25 | 0.50 |
|---|---:|---:|---:|
| full | 0.829 | 0.829 | 0.829 |
| recent | 0.188 | 0.250 | 0.521 |
| lexical_top | 0.908 | 0.846 | 0.833 |
| geometry_top | 0.738 | 0.787 | 0.821 |
| stratified_geometry | 0.312 | 0.629 | 0.785 |

## Encoding x Policy Heatmap

| encoding | full | recent | lexical_top | geometry_top | stratified_geometry |
|---|---:|---:|---:|---:|---:|
| uniform | 0.979 | 0.319 | 0.979 | 0.979 | 0.715 |
| alibi_proxy | 0.781 | 0.319 | 0.840 | 0.684 | 0.531 |
| decay | 0.781 | 0.319 | 0.840 | 0.684 | 0.531 |
| rope_proxy | 0.802 | 0.319 | 0.826 | 0.774 | 0.549 |
| sink_rope_proxy | 0.802 | 0.319 | 0.826 | 0.788 | 0.552 |

## Recent-Only Failure Check

- Budget 0.10: recent top-k success 0.188, stratified_geometry 0.312, delta +0.125.
- Budget 0.25: recent top-k success 0.250, stratified_geometry 0.629, delta +0.379.
- Budget 0.50: recent top-k success 0.521, stratified_geometry 0.785, delta +0.265.

## Region Breakdown

| region | policy | budget | top-k success | retention |
|---|---|---:|---:|---:|
| early | recent | 0.10 | 0.000 | 0.000 |
| early | recent | 0.25 | 0.000 | 0.000 |
| early | recent | 0.50 | 0.000 | 0.000 |
| early | geometry_top | 0.10 | 0.444 | 0.506 |
| early | geometry_top | 0.25 | 0.525 | 0.756 |
| early | geometry_top | 0.50 | 0.625 | 0.938 |
| early | stratified_geometry | 0.10 | 0.069 | 0.081 |
| early | stratified_geometry | 0.25 | 0.287 | 0.456 |
| early | stratified_geometry | 0.50 | 0.544 | 0.819 |
| middle | recent | 0.10 | 0.000 | 0.000 |
| middle | recent | 0.25 | 0.000 | 0.000 |
| middle | recent | 0.50 | 0.562 | 0.562 |
| middle | geometry_top | 0.10 | 0.794 | 0.819 |
| middle | geometry_top | 0.25 | 0.838 | 0.938 |
| middle | geometry_top | 0.50 | 0.838 | 0.988 |
| middle | stratified_geometry | 0.10 | 0.150 | 0.163 |
| middle | stratified_geometry | 0.25 | 0.625 | 0.688 |
| middle | stratified_geometry | 0.50 | 0.825 | 0.975 |
| late | recent | 0.10 | 0.562 | 0.562 |
| late | recent | 0.25 | 0.750 | 0.750 |
| late | recent | 0.50 | 1.000 | 1.000 |
| late | geometry_top | 0.10 | 0.975 | 0.975 |
| late | geometry_top | 0.25 | 1.000 | 1.000 |
| late | geometry_top | 0.50 | 1.000 | 1.000 |
| late | stratified_geometry | 0.10 | 0.719 | 0.719 |
| late | stratified_geometry | 0.25 | 0.975 | 0.975 |
| late | stratified_geometry | 0.50 | 0.988 | 0.988 |

## Region x Policy Heatmap at 25% Budget

| region | recent | lexical_top | geometry_top | stratified_geometry |
|---|---:|---:|---:|---:|
| early | 0.000 | 0.688 | 0.525 | 0.287 |
| middle | 0.000 | 0.850 | 0.838 | 0.625 |
| late | 0.750 | 1.000 | 1.000 | 0.975 |

## Interpretation

If recent-only retention collapses on early or middle evidence while stratified geometry survives at the same budget, the result supports the project claim: KV-cache failure is not only a memory-size problem. It is a policy-plus-position problem.
