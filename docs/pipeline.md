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

---

# Experiment Lifecycle (adopted 2026-08-25)

The framework's known asymmetry: it is excellent at **verification**
("is version N defective?") and had no machinery for **search** ("does a
radically better version exist?"). This section adds search while keeping
`main` sacred.

## Principles

- **main = the currently believed story.** Not a workspace.
- Experiments are alternate universes: local branches `exp/<type>/<slug>` in
  git worktrees (`../test-story-ox-exp-<slug>`) so canon cannot be mutated
  accidentally.
- During **PROBE**, experiments are exempt from story-ledger QA, canon,
  word-band, and coherence. Contradictions are *proposals*, not defects, and
  get one exploratory session before continuity may kill them.
- Curiosity is a legitimate trigger with **no ROI requirement**. Stuckness
  signals (score plateau across cycles, many consecutive line-level edits,
  recurring red-team complaints, repeated repair of one region, shrinking
  edit spans) are observations that *suggest* exploration, never rules.
- Failed experiments are free. Sometimes the job is not improving the book;
  it is finding out whether another book is hiding inside it.

## Operators

| Operator | Meaning |
|---|---|
| dive | Follow one associative thread much too far (depth-first) |
| fork | Try multiple solutions to a known problem |
| rewrite | Recreate a scene/chapter from scratch, without looking at existing prose |
| veto | Let character/world logic reject planned events (withhold the planned outcome from the writing context) |
| mutation | Change one load-bearing fact; write until consequences reveal meaning |
| zero-base | Assume a major existing choice never existed; would any version dominate? |
| wild | Something interesting, no justification required yet |

## Commands

```
python tools/experiment.py start <dive|fork|rewrite|veto|mutation|zero-base|wild> <slug> [--scope ...] [--trigger curiosity|stuck|creative-itch] [--question "..."]
python tools/experiment.py status
python tools/experiment.py stage <slug> <probe|incubate|candidate>
python tools/experiment.py close <slug> <accept|reject|harvest|defer> [--found "..."] [--reason "..."]
python tools/experiment.py list --all
```

- **ACCEPT**: squash-merge into main (one clean mainline commit).
- **REJECT**: tag and tear down.
- **HARVEST**: experiment failed but discovered something → append findings
  to `drafts/discovery_buffer.md` (un-scored, no justification needed),
  then tag and tear down.
- **DEFER**: interesting but unresolved; tag preserves everything.
- Every close creates tag `experiment/<id>/<slug>` — the evolutionary fossil
  record. Tags are pushed; live branches stay local.

## Stages

1. **PROBE** — cheap (~1k words). Is there life here?
2. **INCUBATE** — follow consequences: if ch6 really happened this way, what
   happens to ch7–8? The consequences may be the discovery.
3. **CANDIDATE** — now the full machinery applies: build, speculative-canon
   update, reader simulation, red team, blind comparison vs main.

## Blind comparison (epistemic firewall)

Nontrivial revisions and CANDIDATEs go to **3 fresh judge contexts**:
manuscripts anonymized as A/B with randomized order and randomized file
assignment; judges know neither which is main nor why the branch exists.
Two questions: *Which is better now?* and *Which creates the more promising
road ahead?* Majority-preference for OLD reverts the change.

## Epistemic modes

| Mode | Knows | Never knows |
|---|---|---|
| Author | everything: canon, intent, ledgers, history | — |
| Reader | only chapters read so far, in order | outline, intent, later chapters |
| Critic | manuscript, no authorial intent docs | what it's supposed to mean |
| Judge | anonymized candidates only | provenance, effort, preference |
| Integrator | judgments + project context | raw candidate identities |

Still one model — but no single context poisons another. Knowing what
something is *supposed* to mean makes it impossible to test whether the text
actually communicates it; cold readers must infer.

## Character veto & planned-vs-actual

When a veto/dive produces a different outcome than planned, record both in
the scene ledger entry (`planned_outcome`, `actual_outcome`) and log
downstream material invalidated. Git makes recklessness nearly free; use it.

## Reader simulation — frozen reader-state ledger (adopted 2026-08-25)

`tests/reader_state/after_chNN.yaml`: after writing (or revising) chapter N,
a fresh context reading ONLY chapters 1..N fills the naive-reader schema
(beliefs, trust, wants, theories of Ira/Limit, held questions, explicit
predictions, confusions, foreshadowing suspicions, fuzzy details) and
freezes it. Snapshots are never edited retroactively.

`python tools/reader_diff.py` assembles each boundary's predictions beside
the next chapter's registered new-info; hit/miss/surprised calls feed the
surprise ledger (#47). Systematic misses are structural facts about the text.

Two standing personas consume the manuscript side: **P10 Memory Reader**
(closes the book; recalls vivid moments, characters, phrases, retells from
memory — memorability and distortion analysis) and **P11 Reconstructionist**
(rebuilds world rules/chronology/character models/moral arguments without
canon, then diffs against `src/01-world/canon.md`; discrepancies classify as
well-taught implicit rules, functioning ambiguity, or true failures).

## Consequence discipline

After canonizing a discovery: implement the **unavoidable** consequences; be
selective with merely **interesting** ones (retrofit-everything reads as
theme park). Distinguish intentional plants from harvested plants — existing
details that acquire meaning retroactively are first-class wins.

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
