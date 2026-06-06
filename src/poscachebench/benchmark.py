from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import json
from pathlib import Path
from statistics import mean

from .corpus import Document, EvidenceTask, build_tasks, chunk_tokens, load_documents
from .encodings import ENCODINGS, get_encoding
from .policies import POLICIES, ChunkScore, budget_to_count, select_chunks


@dataclass(frozen=True)
class BenchmarkConfig:
    corpus: str
    max_docs: int = 40
    chunk_size: int = 96
    budgets: tuple[float, ...] = (0.10, 0.25, 0.50)
    top_k: int = 5


@dataclass(frozen=True)
class BenchmarkRow:
    task_id: str
    doc_title: str
    region: str
    total_chunks: int
    evidence_chunk: int
    evidence_distance: int
    query_terms: str
    encoding: str
    policy: str
    budget_ratio: float
    retained_chunks: int
    cost_ratio: float
    evidence_retained: bool
    evidence_rank: int
    evidence_mass: float
    full_evidence_mass: float
    topk_success: bool


def content_score(query_terms: tuple[str, ...], chunk: tuple[str, ...]) -> float:
    if not query_terms:
        return 0.0
    counts: dict[str, int] = {}
    for token in chunk:
        counts[token] = counts.get(token, 0) + 1
    score = 0.0
    for term in query_terms:
        if term in counts:
            score += 1.0 + min(counts[term] - 1, 3) * 0.25
    return score / len(query_terms)


def score_chunks(
    doc: Document,
    task: EvidenceTask,
    *,
    chunk_size: int,
    encoding_name: str,
) -> list[ChunkScore]:
    chunks = chunk_tokens(doc.tokens, chunk_size)
    encoding = get_encoding(encoding_name)
    query_index = len(chunks)
    max_distance = max(1, query_index)
    scores: list[ChunkScore] = []
    for idx, chunk in enumerate(chunks):
        distance = query_index - idx
        c_score = content_score(task.query_terms, chunk)
        p_weight = encoding.weight(distance, max_distance, chunk_index=idx)
        salience = c_score * p_weight
        scores.append(
            ChunkScore(
                chunk_index=idx,
                content_score=c_score,
                positional_weight=p_weight,
                salience=salience,
                distance=distance,
            )
        )
    return scores


def evidence_rank(scores: list[ChunkScore], selected: set[int], evidence_chunk: int) -> int:
    ranked = sorted(
        (score for score in scores if score.chunk_index in selected),
        key=lambda s: (s.salience, s.content_score, -s.distance),
        reverse=True,
    )
    for rank, score in enumerate(ranked, start=1):
        if score.chunk_index == evidence_chunk:
            return rank
    return 0


def evidence_mass(scores: list[ChunkScore], selected: set[int], evidence_chunk: int) -> float:
    denom = sum(max(score.salience, 0.0) for score in scores if score.chunk_index in selected)
    if denom <= 0:
        return 0.0
    for score in scores:
        if score.chunk_index == evidence_chunk and score.chunk_index in selected:
            return max(score.salience, 0.0) / denom
    return 0.0


def run_benchmark(config: BenchmarkConfig) -> tuple[list[BenchmarkRow], list[Document], list[EvidenceTask]]:
    docs = load_documents(config.corpus, max_docs=config.max_docs)
    tasks = build_tasks(docs, chunk_size=config.chunk_size)
    doc_by_id = {doc.doc_id: doc for doc in docs}
    rows: list[BenchmarkRow] = []

    for task in tasks:
        doc = doc_by_id[task.doc_id]
        for encoding_name in ENCODINGS:
            scores = score_chunks(doc, task, chunk_size=config.chunk_size, encoding_name=encoding_name)
            full_selected = {score.chunk_index for score in scores}
            full_mass = evidence_mass(scores, full_selected, task.evidence_chunk)
            for budget_ratio in config.budgets:
                budget = budget_to_count(len(scores), budget_ratio)
                for policy in POLICIES:
                    selected = select_chunks(policy, scores, budget if policy != "full" else len(scores))
                    rank = evidence_rank(scores, selected, task.evidence_chunk)
                    retained = task.evidence_chunk in selected
                    mass = evidence_mass(scores, selected, task.evidence_chunk)
                    rows.append(
                        BenchmarkRow(
                            task_id=task.task_id,
                            doc_title=task.doc_title,
                            region=task.region,
                            total_chunks=task.total_chunks,
                            evidence_chunk=task.evidence_chunk,
                            evidence_distance=task.total_chunks - task.evidence_chunk,
                            query_terms=" ".join(task.query_terms),
                            encoding=encoding_name,
                            policy=policy,
                            budget_ratio=budget_ratio,
                            retained_chunks=len(selected),
                            cost_ratio=len(selected) / max(len(scores), 1),
                            evidence_retained=retained,
                            evidence_rank=rank,
                            evidence_mass=mass,
                            full_evidence_mass=full_mass,
                            topk_success=retained and 0 < rank <= config.top_k,
                        )
                    )
    return rows, docs, tasks


def write_json(path: str | Path, rows: list[BenchmarkRow], config: BenchmarkConfig) -> None:
    payload = {
        "config": asdict(config),
        "rows": [asdict(row) for row in rows],
        "summary": summarize(rows),
    }
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(path: str | Path, rows: list[BenchmarkRow]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()) if rows else [])
        if rows:
            writer.writeheader()
            for row in rows:
                writer.writerow(asdict(row))


def summarize(rows: list[BenchmarkRow]) -> dict[str, dict[str, float]]:
    groups: dict[str, list[BenchmarkRow]] = {}
    for row in rows:
        key = f"{row.encoding}|{row.policy}|{row.budget_ratio:.2f}"
        groups.setdefault(key, []).append(row)
    summary: dict[str, dict[str, float]] = {}
    for key, vals in groups.items():
        summary[key] = {
            "topk_success_rate": mean(1.0 if row.topk_success else 0.0 for row in vals),
            "evidence_retention_rate": mean(1.0 if row.evidence_retained else 0.0 for row in vals),
            "mean_evidence_mass": mean(row.evidence_mass for row in vals),
            "mean_cost_ratio": mean(row.cost_ratio for row in vals),
            "n": float(len(vals)),
        }
    return summary


def write_report(path: str | Path, rows: list[BenchmarkRow], docs: list[Document], tasks: list[EvidenceTask]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    summary = summarize(rows)
    ranked = sorted(
        summary.items(),
        key=lambda item: (item[1]["topk_success_rate"], item[1]["evidence_retention_rate"], -item[1]["mean_cost_ratio"]),
        reverse=True,
    )

    lines = [
        "# PosCacheBench Report",
        "",
        "## Corpus",
        "",
        f"- Documents loaded: {len(docs)}",
        f"- Evidence tasks: {len(tasks)}",
        f"- Benchmark rows: {len(rows)}",
        "",
        "## Best Configurations",
        "",
        "| encoding | policy | budget | top-k success | retention | mean mass | cost |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for key, stats in ranked[:12]:
        encoding, policy, budget = key.split("|")
        lines.append(
            f"| {encoding} | {policy} | {budget} | "
            f"{stats['topk_success_rate']:.3f} | {stats['evidence_retention_rate']:.3f} | "
            f"{stats['mean_evidence_mass']:.4f} | {stats['mean_cost_ratio']:.3f} |"
        )

    lines.extend(["", "## Policy x Budget Heatmap", ""])
    budgets = sorted({row.budget_ratio for row in rows})
    lines.append("| policy | " + " | ".join(f"{budget:.2f}" for budget in budgets) + " |")
    lines.append("|---|" + "|".join("---:" for _ in budgets) + "|")
    for policy in POLICIES:
        vals = []
        for budget in budgets:
            subset = [row for row in rows if row.policy == policy and row.budget_ratio == budget]
            vals.append(f"{mean(1.0 if row.topk_success else 0.0 for row in subset):.3f}" if subset else "n/a")
        lines.append(f"| {policy} | " + " | ".join(vals) + " |")

    lines.extend(["", "## Encoding x Policy Heatmap", ""])
    lines.append("| encoding | " + " | ".join(POLICIES) + " |")
    lines.append("|---|" + "|".join("---:" for _ in POLICIES) + "|")
    for encoding in ENCODINGS:
        vals = []
        for policy in POLICIES:
            subset = [row for row in rows if row.encoding == encoding and row.policy == policy]
            vals.append(f"{mean(1.0 if row.topk_success else 0.0 for row in subset):.3f}" if subset else "n/a")
        lines.append(f"| {encoding} | " + " | ".join(vals) + " |")

    lines.extend(["", "## Recent-Only Failure Check", ""])
    for budget in sorted({row.budget_ratio for row in rows}):
        recent = [row for row in rows if row.policy == "recent" and row.budget_ratio == budget]
        strat = [row for row in rows if row.policy == "stratified_geometry" and row.budget_ratio == budget]
        if not recent or not strat:
            continue
        recent_success = mean(1.0 if row.topk_success else 0.0 for row in recent)
        strat_success = mean(1.0 if row.topk_success else 0.0 for row in strat)
        lines.append(
            f"- Budget {budget:.2f}: recent top-k success {recent_success:.3f}, "
            f"stratified_geometry {strat_success:.3f}, delta {strat_success - recent_success:+.3f}."
        )

    lines.extend(["", "## Region Breakdown", ""])
    lines.append("| region | policy | budget | top-k success | retention |")
    lines.append("|---|---|---:|---:|---:|")
    for region in ("early", "middle", "late"):
        for policy in ("recent", "geometry_top", "stratified_geometry"):
            for budget in sorted({row.budget_ratio for row in rows}):
                vals = [row for row in rows if row.region == region and row.policy == policy and row.budget_ratio == budget]
                if not vals:
                    continue
                lines.append(
                    f"| {region} | {policy} | {budget:.2f} | "
                    f"{mean(1.0 if row.topk_success else 0.0 for row in vals):.3f} | "
                    f"{mean(1.0 if row.evidence_retained else 0.0 for row in vals):.3f} |"
                )

    lines.extend(["", "## Region x Policy Heatmap at 25% Budget", ""])
    target_budget = 0.25
    lines.append("| region | recent | lexical_top | geometry_top | stratified_geometry |")
    lines.append("|---|---:|---:|---:|---:|")
    for region in ("early", "middle", "late"):
        vals = []
        for policy in ("recent", "lexical_top", "geometry_top", "stratified_geometry"):
            subset = [
                row
                for row in rows
                if row.region == region and row.policy == policy and abs(row.budget_ratio - target_budget) < 1e-9
            ]
            vals.append(f"{mean(1.0 if row.topk_success else 0.0 for row in subset):.3f}" if subset else "n/a")
        lines.append(f"| {region} | " + " | ".join(vals) + " |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "If recent-only retention collapses on early or middle evidence while stratified geometry survives at the same budget, the result supports the project claim: KV-cache failure is not only a memory-size problem. It is a policy-plus-position problem.",
            "",
        ]
    )
    out.write_text("\n".join(lines), encoding="utf-8")
