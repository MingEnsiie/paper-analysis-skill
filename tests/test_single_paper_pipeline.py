import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load_module():
    module_path = Path("skillset/paper-analysis/scripts/analyze_paper.py")
    spec = spec_from_file_location("paper_analysis_analyze", module_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_single_paper_pipeline_writes_expected_outputs(tmp_path, monkeypatch):
    analyze_paper = load_module()
    pdf_path = tmp_path / "example.pdf"
    pdf_path.write_text("fake pdf payload", encoding="utf-8")
    out_dir = tmp_path / "outputs"

    extracted_payload = {
        "source_path": str(pdf_path),
        "extraction_method": "text",
        "content": "Example extracted text",
    }
    report_payload = {
        "paper_metadata": {"title": "Example Paper"},
        "research_problem": {"summary": "Improve OCR robustness."},
        "core_idea": {"summary": "Use a hybrid encoder."},
        "method": {"summary": "Train a multimodal transformer."},
        "experimental_setup": {"summary": "Evaluate on three benchmarks."},
        "datasets": ["DocVQA"],
        "baselines": ["BaselineNet"],
        "metrics": ["F1"],
        "results": {"summary": "Outperforms the baseline by 2 F1."},
        "comparison_table": [],
        "limitations": ["Needs more compute."],
        "applicability": ["Useful for scanned documents."],
        "reproducibility": {"summary": "Code release promised."},
        "significance": {"summary": "Practical gain for OCR pipelines."},
        "credibility_assessment": {"summary": "Evidence is moderate."},
        "uncertainties": [],
    }

    monkeypatch.setattr(
        analyze_paper,
        "extract_text_from_pdf",
        lambda path: extracted_payload,
    )
    monkeypatch.setattr(
        analyze_paper,
        "analyze_extracted_content",
        lambda extracted: {"model": "mock-model", "report": report_payload},
    )

    exit_code = analyze_paper.main(
        ["--pdf", str(pdf_path), "--out-dir", str(out_dir)]
    )

    assert exit_code == 0
    assert (out_dir / "extracted.json").exists()
    assert (out_dir / "analysis.json").exists()
    assert (out_dir / "report.json").exists()
    assert (out_dir / "report.md").exists()

    report_json = json.loads((out_dir / "report.json").read_text(encoding="utf-8"))
    assert report_json["paper_metadata"]["title"] == "Example Paper"
    assert "## Research Problem" in (out_dir / "report.md").read_text(encoding="utf-8")
