from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class ChunkScore:
    chunk_index: int
    content_score: float
    positional_weight: float
    salience: float
    distance: int


def budget_to_count(total_chunks: int, budget_ratio: float) -> int:
    if not 0 < budget_ratio <= 1:
        raise ValueError("budget_ratio must be in (0, 1]")
    return max(1, min(total_chunks, int(round(total_chunks * budget_ratio))))


def select_chunks(policy: str, scores: list[ChunkScore], budget: int) -> set[int]:
    if budget >= len(scores):
        return {score.chunk_index for score in scores}
    if policy == "full":
        return {score.chunk_index for score in scores}
    if policy == "recent":
        return {score.chunk_index for score in sorted(scores, key=lambda s: s.chunk_index)[-budget:]}
    if policy == "lexical_top":
        ranked = sorted(scores, key=lambda s: (s.content_score, -s.distance, s.chunk_index), reverse=True)
        return {score.chunk_index for score in ranked[:budget]}
    if policy == "geometry_top":
        ranked = sorted(scores, key=lambda s: (s.salience, s.content_score, -s.distance), reverse=True)
        return {score.chunk_index for score in ranked[:budget]}
    if policy == "stratified_geometry":
        return _stratified_geometry(scores, budget)
    choices = ", ".join(POLICIES)
    raise ValueError(f"unknown policy {policy!r}; choose one of {choices}")


def _stratified_geometry(scores: list[ChunkScore], budget: int) -> set[int]:
    recent_count = max(1, budget // 2)
    recent = {
        score.chunk_index
        for score in sorted(scores, key=lambda s: s.chunk_index, reverse=True)[:recent_count]
    }
    remaining = budget - len(recent)
    if remaining <= 0:
        return recent

    buckets: dict[int, list[ChunkScore]] = {}
    for score in scores:
        if score.chunk_index in recent:
            continue
        bucket = int(math.log2(max(score.distance, 1)))
        buckets.setdefault(bucket, []).append(score)

    selected = set(recent)
    bucket_ids = sorted(buckets)
    for bucket in bucket_ids:
        buckets[bucket].sort(key=lambda s: (s.salience, s.content_score), reverse=True)

    while len(selected) < budget and bucket_ids:
        progressed = False
        for bucket in list(bucket_ids):
            while buckets[bucket] and buckets[bucket][0].chunk_index in selected:
                buckets[bucket].pop(0)
            if not buckets[bucket]:
                bucket_ids.remove(bucket)
                continue
            selected.add(buckets[bucket].pop(0).chunk_index)
            progressed = True
            if len(selected) >= budget:
                break
        if not progressed:
            break
    return selected


POLICIES = ("full", "recent", "lexical_top", "geometry_top", "stratified_geometry")

