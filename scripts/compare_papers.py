"""Multi-paper comparison entry point."""

from __future__ import annotations

import argparse
import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_schemas_module():
    module_path = Path(__file__).with_name("schemas.py")
    spec = spec_from_file_location("paper_analysis_schemas", module_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def _metric_names(report: dict) -> list[str]:
    metrics = []
    for item in report.get("metrics", []):
        if isinstance(item, dict):
            metrics.append(str(item.get("name", "unknown")))
        else:
            metrics.append(str(item))
    return metrics


def _baseline_names(report: dict) -> list[str]:
    baselines = []
    for item in report.get("baselines", []):
        if isinstance(item, dict):
            baselines.append(str(item.get("name", "unknown")))
        else:
            baselines.append(str(item))
    return baselines


def load_report(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_comparison_report(reports: list[dict]) -> dict:
    schemas = _load_schemas_module()
    comparison = schemas.comparison_template()
    comparison["papers"] = [
        {
            "title": report.get("paper_metadata", {}).get("title", "unknown"),
            "datasets": report.get("datasets", []),
            "metrics": _metric_names(report),
        }
        for report in reports
    ]
    comparison["shared_task"] = {
        "summary": "unknown",
        "status": "inferred",
    }
    comparison["method_comparison"] = [
        {
            "paper": report.get("paper_metadata", {}).get("title", "unknown"),
            "method_summary": report.get("method", {}).get("summary", "unknown"),
        }
        for report in reports
    ]
    comparison["experiment_comparison"] = [
        {
            "paper": report.get("paper_metadata", {}).get("title", "unknown"),
            "datasets": report.get("datasets", []),
            "experimental_setup": report.get("experimental_setup", {}),
        }
        for report in reports
    ]
    comparison["metric_alignment"] = [
        {
            "paper": report.get("paper_metadata", {}).get("title", "unknown"),
            "metrics": _metric_names(report),
            "datasets": report.get("datasets", []),
        }
        for report in reports
    ]
    comparison["baseline_alignment"] = [
        {
            "paper": report.get("paper_metadata", {}).get("title", "unknown"),
            "baselines": _baseline_names(report),
        }
        for report in reports
    ]
    comparison["strengths_and_weaknesses"] = [
        {
            "paper": report.get("paper_metadata", {}).get("title", "unknown"),
            "strength": report.get("results", {}).get("summary", "unknown"),
            "weakness": ", ".join(report.get("limitations", [])) or "unknown",
        }
        for report in reports
    ]
    comparison["research_gaps"] = [
        "Direct ranking is unsafe when datasets or metrics differ."
    ]
    comparison["overall_takeaways"] = [
        "Use normalized single-paper outputs before comparing claims."
    ]

    metric_sets = {tuple(sorted(_metric_names(report))) for report in reports}
    dataset_sets = {tuple(sorted(str(item) for item in report.get("datasets", []))) for report in reports}
    comparison["non_comparable_warnings"] = []
    if len(metric_sets) > 1 or len(dataset_sets) > 1:
        comparison["non_comparable_warnings"].append(
            "Results are not directly comparable because metric or dataset alignment differs."
        )

    schemas.validate_comparison_report(comparison)
    return comparison


def render_comparison_markdown(comparison: dict) -> str:
    lines = [
        "# Paper Comparison",
        "## Papers",
    ]
    for paper in comparison.get("papers", []):
        lines.append(
            f"- {paper['title']}: datasets={', '.join(paper.get('datasets', [])) or 'unknown'}; "
            f"metrics={', '.join(paper.get('metrics', [])) or 'unknown'}"
        )
    lines.extend(
        [
            "",
            "## Metric Alignment",
        ]
    )
    for entry in comparison.get("metric_alignment", []):
        lines.append(
            f"- {entry['paper']}: {', '.join(entry.get('metrics', [])) or 'unknown'}"
        )
    warnings = comparison.get("non_comparable_warnings", [])
    if warnings:
        lines.extend(["", "## Warnings"])
        for warning in warnings:
            lines.append(f"- {warning}")
    return "\n".join(lines)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare normalized paper reports.")
    parser.add_argument(
        "--report-json",
        action="append",
        required=True,
        help="Path to a single-paper report.json file. Repeat for multiple papers.",
    )
    parser.add_argument("--out-dir", required=True, help="Output directory path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    reports = [load_report(path) for path in args.report_json]
    comparison = build_comparison_report(reports)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_json(out_dir / "comparison.json", comparison)
    (out_dir / "comparison.md").write_text(
        render_comparison_markdown(comparison),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
