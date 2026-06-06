from __future__ import annotations

import argparse
from pathlib import Path

from .benchmark import BenchmarkConfig, run_benchmark, write_csv, write_json, write_report


def parse_budgets(value: str) -> tuple[float, ...]:
    budgets = tuple(float(part.strip()) for part in value.split(",") if part.strip())
    if not budgets:
        raise argparse.ArgumentTypeError("at least one budget is required")
    for budget in budgets:
        if not 0 < budget <= 1:
            raise argparse.ArgumentTypeError("budgets must be in (0, 1]")
    return budgets


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="poscachebench")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="run the positional cache benchmark")
    run.add_argument("--corpus", default="/Users/srini/Brain/raw", help="markdown/text corpus root")
    run.add_argument("--max-docs", type=int, default=40)
    run.add_argument("--chunk-size", type=int, default=96)
    run.add_argument("--budgets", type=parse_budgets, default=(0.10, 0.25, 0.50))
    run.add_argument("--top-k", type=int, default=5)
    run.add_argument("--out", default="results/benchmark.json")
    run.add_argument("--csv", default="results/benchmark.csv")
    run.add_argument("--report", default="results/report.md")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd == "run":
        config = BenchmarkConfig(
            corpus=args.corpus,
            max_docs=args.max_docs,
            chunk_size=args.chunk_size,
            budgets=args.budgets,
            top_k=args.top_k,
        )
        rows, docs, tasks = run_benchmark(config)
        if not rows:
            raise SystemExit("no benchmark rows produced; choose a corpus with longer markdown/text documents")
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        write_json(args.out, rows, config)
        write_csv(args.csv, rows)
        write_report(args.report, rows, docs, tasks)
        print(f"documents={len(docs)} tasks={len(tasks)} rows={len(rows)}")
        print(f"json={args.out}")
        print(f"csv={args.csv}")
        print(f"report={args.report}")
        return
    parser.error(f"unknown command {args.cmd}")

