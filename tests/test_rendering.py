from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load_module():
    module_path = Path("scripts/analyze_paper.py")
    spec = spec_from_file_location("paper_analysis_analyze", module_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_render_single_paper_markdown_contains_required_sections():
    analyze_paper = load_module()
    report = {
        "paper_metadata": {"title": "Example Paper"},
        "research_problem": {"summary": "提升 OCR 鲁棒性。"},
        "core_idea": {"summary": "使用混合编码器。"},
        "method": {"summary": "训练多模态 Transformer。"},
        "experimental_setup": {"summary": "在三个基准上评估。"},
        "datasets": [],
        "baselines": [],
        "metrics": [],
        "results": {"summary": "相比基线提升 2 个 F1。"},
        "comparison_table": [],
        "limitations": ["需要更多算力。"],
        "applicability": [],
        "reproducibility": {"summary": "承诺公开代码。"},
        "significance": {"summary": "对 OCR 流水线有实际价值。"},
        "credibility_assessment": {"summary": "证据强度中等。"},
        "uncertainties": [],
    }

    rendered = analyze_paper.render_single_paper_markdown(report)

    assert "# 论文分析报告" in rendered
    assert "## 研究问题" in rendered
    assert "## 结果与关键对比" in rendered
    assert "## 可信度评估" in rendered
    assert "提升 OCR 鲁棒性。" in rendered
    assert "证据强度中等。" in rendered
    assert "数据集：未知" in rendered
    assert "基线方法：未知" in rendered
    assert "指标：未知" in rendered
    assert "适用范围：未知" in rendered
