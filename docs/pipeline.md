# The Standard Pipeline

This document is the canonical definition of how this project runs. If a
step isn't here, it isn't part of the standard; if it is here, skipping it
requires a `decisions.log` entry.

## The loop

```
            ┌─────────────────────────────────────────────┐
            │  DRAFT / REVISE (src/04-chapters/)          │
            └──────────────────┬──────────────────────────┘
                               ▼
   ┌──────────────────── QUANTITATIVE GATE ─────────────────────┐
   │ 1. python tools/check_story.py --report tests/STATUS.md    │
   │    prose rules · frequency caps · structure · ledgers      │
   │ 2. python tools/analyze_story.py        -> tests/ANALYSIS.md│
   │    rhythm · openers · abstract-agents · staleness ·        │
   │    dialogue music · emotion lexicons · couplings           │
   │ 3. Fix or triage every error. Warnings need a home         │
   │    (fix now, ledger as known-work, or documented accept).  │
   └──────────────────┬─────────────────────────────────────────┘
                     ▼
   ┌──────────────────── STORY LEDGERS ─────────────────────────┐
   │ Update in the SAME session that changes the story:         │
   │ scene · tension · questions · plantpayoff · attachment ·   │
   │ ambiguity · relationship · promise · worldterms · surprise │
   │ reception  (all in tests/analysis/)                        │
   └──────────────────┬─────────────────────────────────────────┘
                     ▼
   ┌──────────────────── BUILD ─────────────────────────────────┐
   │ python tools/build_manuscript.py  -> output/manuscript.md  │
   │ (band check against book.yaml floor/ceiling)               │
   └──────────────────┬─────────────────────────────────────────┘
                     ▼
   ┌──────────────────── QUALITATIVE LAYER ────────────────────┐
   │ Red-team rounds (tests/redteam/personas.md, 8 personas)    │
   │  -> REDTEAM_REPORT_*.md                                    │
   │  -> synthesis doc when direction is needed                 │
   │ Rubric re-score (docs/story_craft_criteria.md, 50 items)   │
   │  -> scores_current.yaml + scores_history.yaml snapshot     │
   │  -> pillar report (tools/pillar_report.py -> PILLARS.md)   │
   └──────────────────┬─────────────────────────────────────────┘
                     ▼
        docs/decisions.log entry → commit → push
```

## Cadence

| Event | Trigger |
|---|---|
| Checker + analyzer | Every drafting session |
| Ledger updates | Same session as any story change |
| Build | Before every commit |
| Red-team round | After any pass that adds/changes ≥1 scene, or before milestones |
| Full rubric re-score | After any red-team round whose findings were implemented |
| History snapshot | With every rubric re-score (`scores_history.yaml`) |
| Synthesis doc | Whenever red-team output should choose a direction (not before) |

## Score governance

- `scores_current.yaml` mirrors the assessment doc — update both together.
- Scores move only with named evidence (a scene, a measured delta); a score
  never moves because a revision "felt better".
- The pillar report penalizes internal spread; raw and adjusted overall are
  both tracked, and their gap is itself a metric.

## Regression protocol

Any violation found anywhere (checker, review, red-team) becomes either a
`rules.yaml` pattern or a ledger rule so it cannot silently return.

## Calibration sources

- `references/` — PD corpus for analyzer bands (`docs/reference_calibration.md`)
- Re-calibrate whenever thresholds feel guessed rather than measured.
