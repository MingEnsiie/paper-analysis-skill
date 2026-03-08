# Prompting Guide

The single-paper pipeline is text-first.

- Extract text from the PDF when possible.
- If extraction is sparse or empty, mark fallback need explicitly instead of guessing.
- Ask the model for strict structured output aligned to `references/output-schema.md`.
- Keep uncertain claims in `uncertainties` and prefer `unknown` over invention.
- Render Markdown only from validated `report.json`.
