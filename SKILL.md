---
name: paper-analysis
description: Use when analyzing one PDF research paper or comparing multiple paper reports into structured Markdown and JSON outputs with explicit uncertainty handling
---

# Paper Analysis

Use this skill for research-paper requests such as:

- "Analyze this PDF paper"
- "Summarize the method, experiments, and significance"
- "Compare these papers and align baselines or metrics"

## Prerequisites

- Python 3.12
- A readable PDF path for single-paper analysis, or existing normalized `report.json` files for comparison

## Single-Paper Workflow

Use `scripts/analyze_paper.py` when the input is one PDF.

```bash
python skillset/paper-analysis/scripts/analyze_paper.py --pdf <paper.pdf> --out-dir <output-dir>
```

Outputs:

- `extracted.json`
- `analysis.json`
- `report.json`
- `report.md`

Read `references/output-schema.md` before changing output fields or prompting shape.
Read `references/prompting-guide.md` when extraction is sparse, ambiguous, or likely to need multimodal fallback.

## Multi-Paper Workflow

Use `scripts/compare_papers.py` when you already have one or more normalized single-paper `report.json` files.

```bash
python skillset/paper-analysis/scripts/compare_papers.py --report-json <report-a.json> --report-json <report-b.json> --out-dir <output-dir>
```

Outputs:

- `comparison.json`
- `comparison.md`

Read `references/comparison-rules.md` before making cross-paper rankings or alignment claims.

## Rules

- `JSON` is the source of truth. Render Markdown from validated JSON only.
- Use `unknown` or `not_reported` instead of guessing.
- Record uncertain or missing evidence explicitly.
- Mark results as non-comparable when metrics, datasets, or setups do not align.
