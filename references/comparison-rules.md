# Comparison Rules

- Compare papers from normalized `report.json` outputs, not by rereading PDFs.
- Preserve per-paper metric and dataset metadata during alignment.
- If metrics or datasets differ, emit an explicit non-comparable warning.
- Do not rank results when the experimental setup is misaligned.
- Keep Markdown summaries derived from `comparison.json`.
