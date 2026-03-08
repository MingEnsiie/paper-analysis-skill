from pathlib import Path


def test_paper_analysis_skill_skeleton_exists():
    root = Path("skillset/paper-analysis")
    assert (root / "SKILL.md").exists()
    assert (root / "scripts" / "analyze_paper.py").exists()
    assert (root / "scripts" / "compare_papers.py").exists()
    assert (root / "scripts" / "schemas.py").exists()
