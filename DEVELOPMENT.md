# Development Workflow

This project treats writing as software development with iterative phases and quality checks.

## Phases

1. Inception
   - Define core concept, setting, and philosophical stakes.
   - Draft initial character sketches.
   - Create a first rough outline.

2. Architecture
   - Deepen world details and system rules.
   - Flesh out character arcs and thematic roles.
   - Produce a more detailed outline.

3. Planning
   - Refine outline with scene-level beats.
   - Define style guide and story tests.
   - Prepare for chapter drafting.

4. Implementation
   - Write chapter drafts iteratively.
   - Validate against tests after each milestone.
   - Branch experiments as needed.

5. Polish
   - Final consistency and style pass.
   - Run story tests.
   - Prepare final assembled output.

## Project Structure

- `src/01-world/` — Concept, world-building artifacts, and `canon.md` (the continuity ledger)
- `src/02-characters/` — Character sketches and role descriptions
- `src/03-outlines/` — Iterative narrative outlines
- `src/04-chapters/` — Draft prose by chapter
- `tests/automated/` — Machine-checkable rules (`rules.yaml`) run by `tools/check_story.py`
- `tests/manual/` — Judgment-based checklists reviewed by a human/AI read
- `drafts/` — Brainstorms, experiments, and discarded scenes
- `docs/` — Process and style documentation
- `output/` — Assembled final artifacts
- `tools/` — Automation scripts (checks and manuscript build)

## Tooling

Requires Python 3.10+ with PyYAML.

```
python tools/check_story.py                           # run automated prose/structure checks
python tools/check_story.py --report tests/STATUS.md  # regenerate the status file
python tools/build_manuscript.py                      # assemble output/manuscript.md from book.yaml
```

Workflow rules of thumb:

- Run the checker after every drafting session; fix or triage findings before committing.
- When review uncovers a new violation pattern, add it to `tests/automated/rules.yaml`
  so it can't reappear (regression protocol), and note substantive rule changes in
  `docs/decisions.log`.
- Update `src/01-world/canon.md` in the same session that establishes new canon;
  `tests/manual/consistency.md` checks drafts against it.
- Record manual (judgment) review results in `tests/VALIDATION_REPORT.md`.
