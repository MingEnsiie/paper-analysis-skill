# Single Skill Release Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make `paper-analysis` publishable as a standalone GitHub skill repository.

**Architecture:** Normalize all paths to repository-root-relative usage, retain the existing skill contents, and add only the minimum release metadata needed for remote installation and maintenance.

**Tech Stack:** Markdown, Python, pytest, git

---

### Task 1: Normalize repository-root paths

**Files:**
- Modify: `SKILL.md`
- Modify: `tests/test_rendering.py`
- Modify: `tests/test_single_paper_pipeline.py`
- Modify: `tests/test_comparison_pipeline.py`
- Modify: `tests/test_schemas.py`
- Modify: `tests/test_structure.py`

**Step 1: Write the failing test**

Run the existing tests from repository root and confirm they fail because they still reference `skillset/paper-analysis/...`.

**Step 2: Write minimal implementation**

Change commands and test module paths to use repository-root-relative paths.

**Step 3: Run tests to verify they pass**

Run: `pytest tests -q`

### Task 2: Add release metadata

**Files:**
- Create: `README.md`
- Create: `docs/plans/2026-03-08-single-skill-release-design.md`
- Create: `docs/plans/2026-03-08-single-skill-release-plan.md`

**Step 1: Add minimal documentation**

Document repository layout, local usage, and remote install intent without changing the skill behavior.

### Task 3: Verify and publish

**Files:**
- Test: `tests/`

**Step 1: Run verification**

Run: `pytest tests -q`

**Step 2: Commit and push**

Commit the release-ready repository shape and push it to the target GitHub repository.
