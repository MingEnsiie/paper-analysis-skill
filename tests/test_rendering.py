from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load_module():
    module_path = Path("skillset/paper-analysis/scripts/analyze_paper.py")
    spec = spec_from_file_location("paper_analysis_analyze", module_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_render_single_paper_markdown_contains_required_sections():
    analyze_paper = load_module()
    report = {
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

    rendered = analyze_paper.render_single_paper_markdown(report)

    assert "# Paper Analysis" in rendered
    assert "## Research Problem" in rendered
    assert "## Results And Key Comparisons" in rendered
    assert "## Credibility Assessment" in rendered
    assert "Improve OCR robustness." in rendered
    assert "Evidence is moderate." in rendered
