import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load_module():
    module_path = Path("scripts/compare_papers.py")
    spec = spec_from_file_location("paper_analysis_compare", module_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_comparison_pipeline_writes_outputs_and_warnings(tmp_path):
    compare_papers = load_module()
    paper_a = {
        "paper_metadata": {"title": "Paper A"},
        "research_problem": {"summary": "Task A"},
        "core_idea": {"summary": "Idea A"},
        "method": {"summary": "Method A"},
        "experimental_setup": {"summary": "Setup A"},
        "datasets": ["Dataset A"],
        "baselines": ["Baseline A"],
        "metrics": ["Accuracy"],
        "results": {"summary": "Accuracy improves."},
        "comparison_table": [],
        "limitations": [],
        "applicability": [],
        "reproducibility": {},
        "significance": {},
        "credibility_assessment": {},
        "uncertainties": [],
    }
    paper_b = {
        "paper_metadata": {"title": "Paper B"},
        "research_problem": {"summary": "Task B"},
        "core_idea": {"summary": "Idea B"},
        "method": {"summary": "Method B"},
        "experimental_setup": {"summary": "Setup B"},
        "datasets": ["Dataset B"],
        "baselines": ["Baseline B"],
        "metrics": ["F1"],
        "results": {"summary": "F1 improves."},
        "comparison_table": [],
        "limitations": [],
        "applicability": [],
        "reproducibility": {},
        "significance": {},
        "credibility_assessment": {},
        "uncertainties": [],
    }

    report_a = tmp_path / "paper-a.json"
    report_b = tmp_path / "paper-b.json"
    report_a.write_text(json.dumps(paper_a), encoding="utf-8")
    report_b.write_text(json.dumps(paper_b), encoding="utf-8")
    out_dir = tmp_path / "comparison"

    exit_code = compare_papers.main(
        [
            "--report-json",
            str(report_a),
            "--report-json",
            str(report_b),
            "--out-dir",
            str(out_dir),
        ]
    )

    assert exit_code == 0
    assert (out_dir / "comparison.json").exists()
    assert (out_dir / "comparison.md").exists()

    comparison = json.loads((out_dir / "comparison.json").read_text(encoding="utf-8"))
    assert comparison["metric_alignment"]
    assert comparison["non_comparable_warnings"]
    assert comparison["shared_task"]["summary"] == "未知"
    assert comparison["research_gaps"] == ["当数据集或指标不一致时，不能直接做结论性排序。"]
    assert comparison["overall_takeaways"] == ["应先基于标准化的单篇 report.json 再进行跨论文比较。"]
    assert comparison["non_comparable_warnings"] == [
        "由于数据集或指标未对齐，结果不可直接比较。"
    ]
    markdown = (out_dir / "comparison.md").read_text(encoding="utf-8")
    assert "Accuracy" in markdown
    assert "由于数据集或指标未对齐，结果不可直接比较。" in markdown
