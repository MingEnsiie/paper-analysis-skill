# paper-analysis

`paper-analysis` is a single Codex skill repository for analyzing one PDF paper or comparing multiple normalized paper reports.

## Repository Layout

- `SKILL.md`
- `scripts/`
- `references/`
- `assets/`
- `tests/`

## Local Usage

From the repository root:

```bash
python scripts/analyze_paper.py --pdf path/to/paper.pdf --out-dir out/single
python scripts/compare_papers.py --report-json out/a/report.json --report-json out/b/report.json --out-dir out/compare
pytest tests -q
```

## Remote Install

Install as a single-skill GitHub repo with Codex's GitHub skill installer by pointing it at this repository URL.

After installing, restart Codex to pick up the new skill.
