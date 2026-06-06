from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PositionalEncodingProxy:
    name: str
    description: str

    def weight(self, distance: int, max_distance: int, *, chunk_index: int = 0) -> float:
        if distance <= 0:
            return 0.0
        if self.name == "uniform":
            return 1.0
        if self.name == "alibi_proxy":
            slope = 3.0 / max(max_distance, 1)
            return math.exp(-slope * distance)
        if self.name == "decay":
            tau = max(max_distance / 3.0, 1.0)
            return math.exp(-distance / tau)
        if self.name == "rope_proxy":
            phase = math.cos(distance / 8.0)
            damping = math.exp(-distance / max(max_distance * 2.0, 1.0))
            return max(0.05, abs(phase) * damping)
        if self.name == "sink_rope_proxy":
            phase = math.cos(distance / 8.0)
            damping = math.exp(-distance / max(max_distance * 2.0, 1.0))
            sink = 0.35 if chunk_index < 2 else 0.0
            return max(0.05, abs(phase) * damping + sink)
        raise KeyError(f"unknown encoding proxy: {self.name}")


ENCODINGS = {
    "uniform": PositionalEncodingProxy("uniform", "Content-only score with no distance penalty."),
    "alibi_proxy": PositionalEncodingProxy("alibi_proxy", "Monotone ALiBI-like distance penalty."),
    "decay": PositionalEncodingProxy("decay", "Exponential recency pressure."),
    "rope_proxy": PositionalEncodingProxy("rope_proxy", "Oscillatory RoPE-like phase similarity proxy."),
    "sink_rope_proxy": PositionalEncodingProxy(
        "sink_rope_proxy",
        "RoPE-like phase proxy with an attention-sink boost for the first chunks.",
    ),
}


def get_encoding(name: str) -> PositionalEncodingProxy:
    try:
        return ENCODINGS[name]
    except KeyError as exc:
        choices = ", ".join(sorted(ENCODINGS))
        raise ValueError(f"unknown encoding {name!r}; choose one of {choices}") from exc

