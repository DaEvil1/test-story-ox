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
   │    prose rules · frequency caps · negation-contrast ·      │
   │    structure · ledgers                                     │
   │ 2. python tools/analyze_story.py        -> tests/ANALYSIS.md│
   │    rhythm · openers · abstract-agents · AI-signature panel·│
   │    staleness · dialogue music · emotion · couplings ·      │
   │    motif co-occurrence                                     │
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
| Dated artifacts | Assessment and red-team reports are versioned by date (`story_assessment_YYYY-MM-DD.md`, `REDTEAM_REPORT_YYYY-MM-DD.md`); older versions are history, never overwritten |

## Red-team panel (9 personas, `tests/redteam/personas.md`)

P1 critic · P2 genre purist · P3 grief reader · P4 line editor ·
P5 continuity auditor · P6 impatient skimmer · P7 representation reader ·
P8 read-aloud reader · **P9 AI-pattern hunter** (quantifies LLM-typical
signatures and proposes detection rules; adopted proposals enter the
analyzer's AI-signature panel and then `rules.yaml` via regression protocol).

## Negation-contrast governance (adopted 2026-08-24)

- NC-01 (STRONG/MEDIUM frames): checker warning.
- NC-02 (WEAK frames): style fingerprint, capped at 5% of a chapter's
  sentences, floor 3 — e.g., an 80-sentence chapter allows ~4.
- Standalone evaluator: `python tools/detect_negation_contrast.py`.

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
