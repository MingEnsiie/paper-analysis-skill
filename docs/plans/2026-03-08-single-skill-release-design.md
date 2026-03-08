# Single Skill Release Design

**Goal:** Publish `paper-analysis` as a standalone GitHub repository that Codex can install directly from the repo URL.

**Approach:** Use the repository root as the skill root. Keep `SKILL.md`, `scripts/`, `references/`, `assets/`, and `tests/` at the top level. Update any path assumptions that still refer to the old nested `skillset/paper-analysis/` layout.

**Release Criteria:**
- Repository root matches single-skill layout.
- `SKILL.md` commands use root-relative paths.
- Tests run from repository root.
- Repository includes minimal install/readme documentation.
