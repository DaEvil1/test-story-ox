# Process Guide

## Inception
- Write the core idea in `src/01-world/concept.md`
- Record setting essentials in `src/01-world/setting.md`
- Capture character sketches in `src/02-characters/`
- Draft a rough story skeleton in `src/03-outlines/outline_v1_rough.md`

## Architecture
- Expand rules, factions, and technology in `src/01-world/`
- Add deeper character motivations and relationships
- Create a second, more detailed outline version

## Planning
- Make the story concrete enough to draft chapters
- Define judgment tests in `tests/manual/` and machine rules in `tests/automated/rules.yaml`
- Add a `docs/decisions.log` entry for major creative choices

## Implementation
- Write chapters in `src/04-chapters/`
- Use `drafts/` for branch experiments and cut material
- After each drafting session, run `python tools/check_story.py` and fix or triage findings
- When a new violation pattern appears, add it to `tests/automated/rules.yaml` (regression protocol)
- Keep `src/01-world/canon.md` in sync with anything a chapter establishes

## Polish
- Review test coverage in `tests/`
- Complete manual reviews and record them in `tests/VALIDATION_REPORT.md`
- Update `README.md` with progress
- Assemble output with `python tools/build_manuscript.py`
