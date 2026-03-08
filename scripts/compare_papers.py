"""多篇论文对比入口。"""

from __future__ import annotations

import argparse
import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

UNKNOWN = "未知"


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
            metrics.append(str(item.get("name", UNKNOWN)))
        else:
            metrics.append(str(item))
    return metrics


def _baseline_names(report: dict) -> list[str]:
    baselines = []
    for item in report.get("baselines", []):
        if isinstance(item, dict):
            baselines.append(str(item.get("name", UNKNOWN)))
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
            "title": report.get("paper_metadata", {}).get("title", UNKNOWN),
            "datasets": report.get("datasets", []),
            "metrics": _metric_names(report),
        }
        for report in reports
    ]
    comparison["shared_task"] = {
        "summary": UNKNOWN,
        "status": "inferred",
    }
    comparison["method_comparison"] = [
        {
            "paper": report.get("paper_metadata", {}).get("title", UNKNOWN),
            "method_summary": report.get("method", {}).get("summary", UNKNOWN),
        }
        for report in reports
    ]
    comparison["experiment_comparison"] = [
        {
            "paper": report.get("paper_metadata", {}).get("title", UNKNOWN),
            "datasets": report.get("datasets", []),
            "experimental_setup": report.get("experimental_setup", {}),
        }
        for report in reports
    ]
    comparison["metric_alignment"] = [
        {
            "paper": report.get("paper_metadata", {}).get("title", UNKNOWN),
            "metrics": _metric_names(report),
            "datasets": report.get("datasets", []),
        }
        for report in reports
    ]
    comparison["baseline_alignment"] = [
        {
            "paper": report.get("paper_metadata", {}).get("title", UNKNOWN),
            "baselines": _baseline_names(report),
        }
        for report in reports
    ]
    comparison["strengths_and_weaknesses"] = [
        {
            "paper": report.get("paper_metadata", {}).get("title", UNKNOWN),
            "strength": report.get("results", {}).get("summary", UNKNOWN),
            "weakness": ", ".join(report.get("limitations", [])) or UNKNOWN,
        }
        for report in reports
    ]
    comparison["research_gaps"] = [
        "当数据集或指标不一致时，不能直接做结论性排序。"
    ]
    comparison["overall_takeaways"] = [
        "应先基于标准化的单篇 report.json 再进行跨论文比较。"
    ]

    metric_sets = {tuple(sorted(_metric_names(report))) for report in reports}
    dataset_sets = {tuple(sorted(str(item) for item in report.get("datasets", []))) for report in reports}
    comparison["non_comparable_warnings"] = []
    if len(metric_sets) > 1 or len(dataset_sets) > 1:
        comparison["non_comparable_warnings"].append(
            "由于数据集或指标未对齐，结果不可直接比较。"
        )

    schemas.validate_comparison_report(comparison)
    return comparison


def render_comparison_markdown(comparison: dict) -> str:
    lines = [
        "# 多篇论文对比报告",
        "## 论文列表",
    ]
    for paper in comparison.get("papers", []):
        lines.append(
            f"- {paper['title']}：数据集={', '.join(paper.get('datasets', [])) or UNKNOWN}；"
            f"指标={', '.join(paper.get('metrics', [])) or UNKNOWN}"
        )
    lines.extend(
        [
            "",
            "## 指标对齐",
        ]
    )
    for entry in comparison.get("metric_alignment", []):
        lines.append(
            f"- {entry['paper']}：{', '.join(entry.get('metrics', [])) or UNKNOWN}"
        )
    warnings = comparison.get("non_comparable_warnings", [])
    if warnings:
        lines.extend(["", "## 警告"])
        for warning in warnings:
            lines.append(f"- {warning}")
    return "\n".join(lines)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="对比标准化后的论文报告。")
    parser.add_argument(
        "--report-json",
        action="append",
        required=True,
        help="单篇论文 report.json 路径。多篇论文可重复传入该参数。",
    )
    parser.add_argument("--out-dir", required=True, help="输出目录路径")
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
