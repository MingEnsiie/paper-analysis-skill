---
name: paper-analysis
description: Use when analyzing one PDF research paper or comparing multiple paper reports into structured Markdown and JSON outputs with explicit uncertainty handling
---

# 论文分析

在这类论文请求中使用这个 skill：

- “分析这篇 PDF 论文”
- “总结这篇论文的方法、实验和意义”
- “对比这几篇论文，并对齐 baseline 或指标”

## 前置条件

- Python 3.12
- 单篇分析需要可读取的 PDF 路径；多篇对比需要已有的标准化 `report.json`

## 单篇论文工作流

当输入是一篇 PDF 时，使用 `scripts/analyze_paper.py`。

```bash
python scripts/analyze_paper.py --pdf <paper.pdf> --out-dir <output-dir>
```

输出：

- `extracted.json`
- `analysis.json`
- `report.json`
- `report.md`

修改输出字段或提示词结构前，先阅读 `references/output-schema.md`。
当抽取结果稀疏、含糊，或明显需要多模态兜底时，阅读 `references/prompting-guide.md`。

## 多篇论文对比工作流

当你已经有一个或多个单篇标准化 `report.json` 时，使用 `scripts/compare_papers.py`。

```bash
python scripts/compare_papers.py --report-json <report-a.json> --report-json <report-b.json> --out-dir <output-dir>
```

输出：

- `comparison.json`
- `comparison.md`

做跨论文排序、指标对齐或结论归纳前，先阅读 `references/comparison-rules.md`。

## 规则

- `JSON` 是事实源，`Markdown` 只能从校验通过的 JSON 渲染。
- 不确定时使用 `未知` 或 `not_reported`，不要猜测。
- 证据缺失或不确定时要显式记录。
- 指标、数据集或实验设置不一致时，必须标记为不可直接比较。
