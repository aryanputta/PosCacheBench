from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_+\-/.]*")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
WIKILINK_RE = re.compile(r"\[\[([^|\]]+\|)?([^\]]+)\]\]")

STOPWORDS = {
    "about",
    "above",
    "after",
    "again",
    "against",
    "also",
    "because",
    "before",
    "being",
    "between",
    "could",
    "every",
    "from",
    "have",
    "into",
    "more",
    "only",
    "other",
    "over",
    "should",
    "some",
    "such",
    "than",
    "that",
    "their",
    "then",
    "there",
    "these",
    "they",
    "this",
    "through",
    "under",
    "using",
    "when",
    "where",
    "which",
    "while",
    "with",
    "would",
}


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    path: str
    tokens: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceTask:
    task_id: str
    doc_id: str
    doc_title: str
    region: str
    evidence_chunk: int
    query_terms: tuple[str, ...]
    total_chunks: int


def strip_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n")
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            text = text[end + 4 :]
    text = LINK_RE.sub(r"\1", text)
    text = WIKILINK_RE.sub(r"\2", text)
    text = re.sub(r"`{1,3}", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[#>*_|~]", " ", text)
    return text


def tokenize(text: str) -> tuple[str, ...]:
    return tuple(match.group(0).lower() for match in TOKEN_RE.finditer(strip_markdown(text)))


def iter_text_files(root: Path) -> Iterable[Path]:
    suffixes = {".md", ".txt"}
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in suffixes:
            yield path


def load_documents(
    root: str | Path,
    *,
    max_docs: int = 40,
    min_tokens: int = 500,
    max_tokens_per_doc: int = 12000,
) -> list[Document]:
    root_path = Path(root)
    docs: list[Document] = []
    for path in iter_text_files(root_path):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        tokens = tokenize(text)
        if len(tokens) < min_tokens:
            continue
        title = path.stem.replace("-", " ").replace("_", " ").strip()
        rel = str(path.relative_to(root_path)) if path.is_relative_to(root_path) else str(path)
        docs.append(
            Document(
                doc_id=f"doc{len(docs):04d}",
                title=title,
                path=rel,
                tokens=tokens[:max_tokens_per_doc],
            )
        )
        if len(docs) >= max_docs:
            break
    return docs


def chunk_tokens(tokens: tuple[str, ...], chunk_size: int) -> list[tuple[str, ...]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    return [tokens[i : i + chunk_size] for i in range(0, len(tokens), chunk_size)]


def choose_query_terms(
    chunk: tuple[str, ...],
    doc_tokens: tuple[str, ...],
    *,
    chunks: list[tuple[str, ...]] | None = None,
    limit: int = 6,
) -> tuple[str, ...]:
    counts: dict[str, int] = {}
    for token in doc_tokens:
        counts[token] = counts.get(token, 0) + 1

    candidates = {
        token
        for token in chunk
        if len(token) >= 5 and token not in STOPWORDS and not token.replace(".", "").isdigit()
    }
    if not candidates:
        return ()

    if chunks:
        chunk_df: dict[str, int] = {}
        for doc_chunk in chunks:
            for token in set(doc_chunk):
                chunk_df[token] = chunk_df.get(token, 0) + 1
        target_df = max(2, min(8, int(len(chunks) ** 0.5)))
        repeated = [token for token in candidates if chunk_df.get(token, 0) >= 2]
        if repeated:
            ranked = sorted(
                repeated,
                key=lambda tok: (abs(chunk_df.get(tok, 0) - target_df), -counts.get(tok, 0), tok),
            )
            return tuple(ranked[:limit])

    ranked = sorted(candidates, key=lambda tok: (counts.get(tok, 0), -len(tok), tok))
    return tuple(ranked[:limit])


def build_tasks(
    docs: list[Document],
    *,
    chunk_size: int = 96,
    min_chunks: int = 6,
) -> list[EvidenceTask]:
    tasks: list[EvidenceTask] = []
    regions = {
        "early": lambda n: max(0, n // 8),
        "middle": lambda n: n // 2,
        "late": lambda n: max(0, n - 3),
    }
    for doc in docs:
        chunks = chunk_tokens(doc.tokens, chunk_size)
        if len(chunks) < min_chunks:
            continue
        for region, chooser in regions.items():
            idx = min(len(chunks) - 2, chooser(len(chunks)))
            terms = choose_query_terms(chunks[idx], doc.tokens, chunks=chunks)
            if len(terms) < 3:
                continue
            tasks.append(
                EvidenceTask(
                    task_id=f"{doc.doc_id}:{region}",
                    doc_id=doc.doc_id,
                    doc_title=doc.title,
                    region=region,
                    evidence_chunk=idx,
                    query_terms=terms,
                    total_chunks=len(chunks),
                )
            )
    return tasks
