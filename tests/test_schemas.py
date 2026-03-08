from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest


def load_module():
    module_path = Path("scripts/schemas.py")
    spec = spec_from_file_location("paper_analysis_schemas", module_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_single_paper_template_exposes_required_keys():
    schemas = load_module()

    template = schemas.single_paper_template()

    assert "research_problem" in template
    assert "comparison_table" in template
    assert "credibility_assessment" in template


def test_comparison_template_exposes_required_keys():
    schemas = load_module()

    template = schemas.comparison_template()

    assert "papers" in template
    assert "research_gaps" in template


def test_single_paper_validator_rejects_missing_required_keys():
    schemas = load_module()

    with pytest.raises(ValueError):
        schemas.validate_single_paper_report({"paper_metadata": {}})


def test_comparison_validator_rejects_missing_required_keys():
    schemas = load_module()

    with pytest.raises(ValueError):
        schemas.validate_comparison_report({"papers": []})
