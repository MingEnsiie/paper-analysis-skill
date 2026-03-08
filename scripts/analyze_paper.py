"""单篇论文分析入口。"""

from __future__ import annotations

import argparse
import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

UNKNOWN = "未知"
NO_TEXT_SUMMARY = "未提取到有效论文文本。"


def _load_schemas_module():
    module_path = Path(__file__).with_name("schemas.py")
    spec = spec_from_file_location("paper_analysis_schemas", module_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _stringify(value) -> str:
    if isinstance(value, dict):
        summary = value.get("summary")
        if summary:
            return str(summary)
        if not value:
            return UNKNOWN
        return ", ".join(f"{key}: {item}" for key, item in value.items())
    if isinstance(value, list):
        if not value:
            return UNKNOWN
        return ", ".join(str(item) for item in value)
    if value in (None, ""):
        return UNKNOWN
    return str(value)


def render_single_paper_markdown(report: dict) -> str:
    title = report.get("paper_metadata", {}).get("title", "论文分析报告")
    sections = [
        "# 论文分析报告",
        f"## 论文概览\n\n{title}",
        f"## 研究问题\n\n{_stringify(report.get('research_problem', {}))}",
        f"## 核心思路\n\n{_stringify(report.get('core_idea', {}))}",
        f"## 方法\n\n{_stringify(report.get('method', {}))}",
        f"## 实验设计\n\n{_stringify(report.get('experimental_setup', {}))}",
        "## 结果与关键对比\n\n"
        f"结果：{_stringify(report.get('results', {}))}\n\n"
        f"数据集：{_stringify(report.get('datasets', []))}\n\n"
        f"基线方法：{_stringify(report.get('baselines', []))}\n\n"
        f"指标：{_stringify(report.get('metrics', []))}",
        "## 局限性与适用范围\n\n"
        f"局限性：{_stringify(report.get('limitations', []))}\n\n"
        f"适用范围：{_stringify(report.get('applicability', []))}",
        f"## 复现信息\n\n{_stringify(report.get('reproducibility', {}))}",
        f"## 意义\n\n{_stringify(report.get('significance', {}))}",
        f"## 可信度评估\n\n{_stringify(report.get('credibility_assessment', {}))}",
    ]
    return "\n\n".join(sections)


def extract_text_from_pdf(path: str | Path) -> dict:
    pdf_path = Path(path)
    raw_bytes = pdf_path.read_bytes()
    text_content = raw_bytes.decode("utf-8", errors="ignore").strip()
    return {
        "source_path": str(pdf_path),
        "extraction_method": "text",
        "content": text_content,
        "fallback_recommended": not bool(text_content),
    }


def analyze_extracted_content(extracted: dict) -> dict:
    text = extracted.get("content", "").strip()
    title = Path(extracted.get("source_path", "paper")).stem.replace("-", " ").title()
    report = _load_schemas_module().single_paper_template()
    report["paper_metadata"] = {"title": title}
    report["research_problem"] = {"summary": text[:200] or NO_TEXT_SUMMARY}
    report["core_idea"] = {"summary": UNKNOWN}
    report["method"] = {"summary": UNKNOWN}
    report["experimental_setup"] = {"summary": UNKNOWN}
    report["uncertainties"] = []
    return {
        "model": "stub-text-analysis",
        "report": report,
    }


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="分析单篇 PDF 论文。")
    parser.add_argument("--pdf", required=True, help="输入 PDF 路径")
    parser.add_argument("--out-dir", required=True, help="输出目录路径")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    extracted = extract_text_from_pdf(args.pdf)
    analysis = analyze_extracted_content(extracted)
    report = analysis["report"]
    _load_schemas_module().validate_single_paper_report(report)

    _write_json(out_dir / "extracted.json", extracted)
    _write_json(out_dir / "analysis.json", analysis)
    _write_json(out_dir / "report.json", report)
    (out_dir / "report.md").write_text(
        render_single_paper_markdown(report),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
