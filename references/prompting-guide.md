# 提示词规则

单篇分析流程默认优先走文本抽取。

- 能提取文本时，先从 PDF 提取文本。
- 如果抽取结果稀疏或为空，要显式标记需要 fallback，不要猜内容。
- 要求模型严格按 `references/output-schema.md` 输出结构化结果。
- 不确定的判断放进 `uncertainties`，优先使用 `unknown`，不要编造。
- `Markdown` 只能从校验通过的 `report.json` 渲染。
