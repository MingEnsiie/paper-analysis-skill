# 输出结构说明

`report.json` 是单篇论文分析的事实源。

## 单篇论文字段

- `paper_metadata`
- `research_problem`
- `core_idea`
- `method`
- `experimental_setup`
- `datasets`
- `baselines`
- `metrics`
- `results`
- `comparison_table`
- `limitations`
- `applicability`
- `reproducibility`
- `significance`
- `credibility_assessment`
- `uncertainties`

## 多篇对比字段

- `papers`
- `shared_task`
- `method_comparison`
- `experiment_comparison`
- `metric_alignment`
- `baseline_alignment`
- `strengths_and_weaknesses`
- `research_gaps`
- `overall_takeaways`

遇到缺失信息时，使用 `unknown` 或 `not_reported` 这类显式占位值，不要补猜。
