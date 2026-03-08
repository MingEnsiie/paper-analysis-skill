"""Single-paper analysis entry point."""

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


def _stringify(value) -> str:
    if isinstance(value, dict):
        summary = value.get("summary")
        if summary:
            return str(summary)
        if not value:
            return "unknown"
        return ", ".join(f"{key}: {item}" for key, item in value.items())
    if isinstance(value, list):
        if not value:
            return "unknown"
        return ", ".join(str(item) for item in value)
    if value in (None, ""):
        return "unknown"
    return str(value)


def render_single_paper_markdown(report: dict) -> str:
    title = report.get("paper_metadata", {}).get("title", "Paper Analysis")
    sections = [
        "# Paper Analysis",
        f"## Paper Overview\n\n{title}",
        f"## Research Problem\n\n{_stringify(report.get('research_problem', {}))}",
        f"## Core Idea\n\n{_stringify(report.get('core_idea', {}))}",
        f"## Method\n\n{_stringify(report.get('method', {}))}",
        f"## Experimental Design\n\n{_stringify(report.get('experimental_setup', {}))}",
        "## Results And Key Comparisons\n\n"
        f"Results: {_stringify(report.get('results', {}))}\n\n"
        f"Datasets: {_stringify(report.get('datasets', []))}\n\n"
        f"Baselines: {_stringify(report.get('baselines', []))}\n\n"
        f"Metrics: {_stringify(report.get('metrics', []))}",
        "## Limitations And Applicability\n\n"
        f"Limitations: {_stringify(report.get('limitations', []))}\n\n"
        f"Applicability: {_stringify(report.get('applicability', []))}",
        f"## Reproducibility\n\n{_stringify(report.get('reproducibility', {}))}",
        f"## Significance\n\n{_stringify(report.get('significance', {}))}",
        f"## Credibility Assessment\n\n{_stringify(report.get('credibility_assessment', {}))}",
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
    report["research_problem"] = {"summary": text[:200] or "unknown"}
    report["core_idea"] = {"summary": "unknown"}
    report["method"] = {"summary": "unknown"}
    report["experimental_setup"] = {"summary": "unknown"}
    report["uncertainties"] = []
    return {
        "model": "stub-text-analysis",
        "report": report,
    }


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze one PDF research paper.")
    parser.add_argument("--pdf", required=True, help="Input PDF path")
    parser.add_argument("--out-dir", required=True, help="Output directory path")
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
