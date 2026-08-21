# Tests

Quality checks for the story, split by how they run.

## `automated/` — enforced by script

- `rules.yaml` — machine-checkable prose and structure rules (banned phrases,
  patterns, duplicate-title detection).
- `prose_rules.md` — the human-readable spec for those rules, plus the list of
  judgment calls that need manual review.

Run after every drafting session:

```
python tools/check_story.py                          # console report
python tools/check_story.py --report tests/STATUS.md # also regenerate status file
python tools/check_story.py --strict                 # warnings fail too
```

Requires Python 3.10+ and PyYAML (`pip install pyyaml`).

**Regression protocol:** when you find a violation during editing or review,
add its pattern to `rules.yaml` so it can never silently reappear. Log
substantive rule changes in `docs/decisions.log`.

## `manual/` — judgment checklists

Reviewed by a human (or AI read-through), not pattern-matched:

- `character_arcs.md`, `consistency.md`, `ira_characterization.md`,
  `motif_usage.md`, `plot_completeness.md`, `style.md`,
  `thematic_coherence.md`, `the_limit_ambiguity.md`

Manual review results are recorded in `VALIDATION_REPORT.md`.

## Generated files

- `STATUS.md` — per-chapter automated results. **Generated — do not edit.**
- `VALIDATION_REPORT.md` — living record of manual validation and open gaps.
