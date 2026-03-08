"""Schema helpers for paper analysis outputs."""

from __future__ import annotations


REQUIRED_STATUS = {"confirmed", "inferred", "unknown"}

_SINGLE_PAPER_REQUIRED_KEYS = (
    "paper_metadata",
    "research_problem",
    "core_idea",
    "method",
    "experimental_setup",
    "datasets",
    "baselines",
    "metrics",
    "results",
    "comparison_table",
    "limitations",
    "applicability",
    "reproducibility",
    "significance",
    "credibility_assessment",
    "uncertainties",
)

_COMPARISON_REQUIRED_KEYS = (
    "papers",
    "shared_task",
    "method_comparison",
    "experiment_comparison",
    "metric_alignment",
    "baseline_alignment",
    "strengths_and_weaknesses",
    "research_gaps",
    "overall_takeaways",
)


def _validate_required_keys(data: dict, required_keys: tuple[str, ...], label: str) -> dict:
    missing = [key for key in required_keys if key not in data]
    if missing:
        missing_list = ", ".join(missing)
        raise ValueError(f"{label} is missing required keys: {missing_list}")
    return data


def single_paper_template() -> dict:
    return {
        "paper_metadata": {},
        "research_problem": {},
        "core_idea": {},
        "method": {},
        "experimental_setup": {},
        "datasets": [],
        "baselines": [],
        "metrics": [],
        "results": {},
        "comparison_table": [],
        "limitations": [],
        "applicability": [],
        "reproducibility": {},
        "significance": {},
        "credibility_assessment": {},
        "uncertainties": [],
    }


def comparison_template() -> dict:
    return {
        "papers": [],
        "shared_task": {},
        "method_comparison": [],
        "experiment_comparison": [],
        "metric_alignment": [],
        "baseline_alignment": [],
        "strengths_and_weaknesses": [],
        "research_gaps": [],
        "overall_takeaways": [],
    }


def validate_single_paper_report(data: dict) -> dict:
    return _validate_required_keys(data, _SINGLE_PAPER_REQUIRED_KEYS, "single paper report")


def validate_comparison_report(data: dict) -> dict:
    return _validate_required_keys(data, _COMPARISON_REQUIRED_KEYS, "comparison report")
