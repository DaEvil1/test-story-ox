# The Standard Pipeline

This document is the canonical definition of how this project runs. If a
step isn't here, it isn't part of the standard; if it is here, skipping it
requires a `decisions.log` entry.

## The loop

```
                ┌────────────────────────────┐
                │  ORIENT / CREATIVE PULSE   │
                │  What does the story want  │
                │  right now?                │
                └──────────┬─────────────────┘
                           │
          CONTINUE / POLISH│         │ EXPLORE (curiosity or stuck)
                           ▼         ▼
   ┌──────────────────────────┐   ┌────────────────────────────────┐
   │ DRAFT / REVISE           │   │ EXPERIMENT BRANCH (worktree)   │
   │ (src/04-chapters/)       │   │ PROBE → INCUBATE → CANDIDATE   │
   └──────────┬───────────────┘   │ QA suspended until CANDIDATE   │
              │                   └──────────┬─────────────────────┘
              ▼                              ▼
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
   │ Red-team rounds (tests/redteam/personas.md — panel P1–P9,  │
   │ plus standing readers P10 memory / P11 reconstructionist)  │
   │  -> REDTEAM_REPORT_*.md + REDTEAM_PANEL_SCORE              │
   │ Council of Readers sessions (tests/council/, C1–C5)        │
   │  -> COUNCIL_SCORE                                           │
   │ Integrator triage of all feedback (TAKE/ADAPT/DISCARD/DEFER)│
   │ Rubric re-score (docs/story_craft_criteria.md, 50 items)   │
   │  -> scores_current.yaml + scores_history.yaml snapshot     │
   │  -> pillar report (tests/PILLARS.md)                       │
   └──────────────────┬─────────────────────────────────────────┘
                     ▼
        docs/decisions.log entry → commit → push
```


## Comparison horizons (pairwise second question is horizon-aware)

| Candidate type | Second question |
|---|---|
| Unfinished middle chapter | "Which creates the more promising road ahead?" |
| Ending / final chapter | "Which leaves the stronger residue — more inevitable-yet-surprising as a WHOLE story?" |
| Line revision | "Which is better prose in context?" |
| Structural branch | Both: present quality AND future possibility |

For structural CANDIDATE merges, counterbalance ballots or add one
reversed-order consistency judge; position bias does not vanish because
assignment is random. Broad style passes (many small edits across chapters)
require representative-chapter OLD/NEW comparisons before landing —
"metrics improved" and "writing improved" are different claims.

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
  git worktrees under `.experiments/` (inside the repo root, gitignored) so
  canon cannot be mutated accidentally and no out-of-workspace access occurs.
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
road ahead?* Majority-preference for OLD reverts the change. Ballot
integrity: judges record preference plus free-text reaction only — attempting
to identify provenance voids the ballot (round H16 annulled for this).

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

## Intentional violations & pairwise revision judging (adopted 2026-08-25)

**Regression constraints, not style laws.** A rule may be violated when
there is a positive case on file: `tests/intentional_violations.yaml`
(rule + file + matching pattern + justification). The checker suppresses
covered findings and reports them under "Intentional violations honored."
Rules:
- Warning-level rules may be overridden freely.
- Error-level rules additionally require a `docs/decisions.log` reference.
- Justifications are re-read at every zero-based audit; stale ones die.
The test is not "did we find a loophole" but "does obeying the rule here
produce a weaker sentence?" If yes, the violation is protected.

**Pairwise revision judging.** Revision is not monotonically positive —
editing often produces *cleaner but worse*. For any nontrivial revision:

```
python tools/pairwise.py start --chapter <file> --base HEAD~N
#   send tests/pairwise/<id>/A.md and B.md to 3 fresh judge contexts
python tools/pairwise.py record <id> J1 B "reason"
python tools/pairwise.py tally <id>     # majority-OLD -> revert
python tools/pairwise.py clean <id>
```

Anonymized A/B, randomized assignment, judges never know which side is the
revision or how much work it cost. The rubric stays a diagnostic dashboard;
pairwise preference is the fitness signal for individual changes.

## Zero-based audit (adopted 2026-08-25)

Run periodically — always before any "content-complete" declaration, and
after any round where red-team findings become purely omission-class.

Prompt: *assume the manuscript is a sophisticated but fundamentally mistaken
solution to the premise.* Then:

1. List the five most load-bearing creative decisions.
2. For each, describe — seriously, in prose — the story in which that
   decision never existed.
3. Verdict per decision: KEEP (no dominant alternative found) or ESCALATE
   (an alternative plausibly dominates → open an `exp/zero-base` branch).

This is architectural review, not criticism. Refactoring assumes the design;
the audit asks whether the design should exist. Results are dated files in
`docs/zero_base_audit_*.md`; any harvested seeds go to the discovery buffer.

## The Integrator & the instinct filter (adopted 2026-08-25)

Feedback is not instruction. Red-team findings and Council responses are
*testimony*; the **Integrator mode** (author context: canon, intent,
coupling map, full history) decides what takes power. Every substantive
piece of feedback gets one of four verdicts, recorded in
`docs/integrator_triage_*.md`:

- **TAKE** — aligns with intent, cost understood, survives the questions below
- **ADAPT** — true observation, wrong prescription; fix it another way
- **DISCARD** — conflicts with what the book is; discarding is legitimate and logged
- **DEFER** — real, but belongs to a later pass or sequel space

The instinct is not a checklist, but five questions asked honestly:

1. Does accepting make the story more *itself*, or more generic?
2. Is this about the text, or about the reader's unrelated preference?
3. What does the fix break? (coupling map — nothing is free)
4. Would the change survive blind pairwise judging against what exists?
5. **The stranger-version test:** is the flaw everyone identifies actually
   the book?

Precedent: "add an ontological test of The Limit" (P2, three rounds) →
DISCARD — the ask conflicts with designed ambiguity that behavioral reader
data shows functioning. "Keji needs a life outside the quest" (P7) → TAKE.
Discarded feedback stays in the triage log; instincts get re-checked at
zero-based audits, because sometimes the discarded thing was right later.

## Consequence discipline

After canonizing a discovery: implement the **unavoidable** consequences; be
selective with merely **interesting** ones (retrofit-everything reads as
theme park). Distinguish intentional plants from harvested plants — existing
details that acquire meaning retroactively are first-class wins.

## Long-run observation register (adopted 2026-08-25)

The framework is **feature-complete for sustained empirical use**.
Infrastructure freeze unless repeated execution reveals a concrete failure
mode. What follows are phenomena to OBSERVE, not rules to enforce:

- **Motif capture**: discoveries getting promoted until they become the
  thematic operating system. The machinery rewards reread yield,
  plant/payoff, and integration — five independent incentives to braid.
  Watch whether new finds stay weird or get promoted everywhere.
- **Operator bias**: does one operator dominate choices or acceptance rates?
  (`veto` may legitimately run hot — it uniquely pairs surprise with
  causality; nerf only if "characters have minds of their own" becomes a
  fetish rather than a measured pattern.)
- **Judge novelty-bias**: do blind judges systematically prefer the newer
  branch? Counterbalanced ballots exist partly to detect this.
- **Discovery-buffer decay**: does HARVEST accumulate seductive junk that
  never becomes canon?
- **Consolidation sanding**: do polish passes quietly remove exactly the
  strangeness experiments introduce?
- **Texture starvation**: the framework rewards connection (plant/payoff,
  integration, reread yield) and has no metric for unconnected life.
  Countermeasure in place: `status: texture` items in the plant/payoff
  ledger are protected locals — exempt from orphan warnings, reviewed at
  zero-based audits to confirm they still feel alive rather than decorative.
  Rule of thumb: every chapter should contain at least one detail that pays
  off nowhere.
- **Neighborhood drift**: track each experiment's `distance` field (low /
  medium / high / very-high). Twenty near-excursions are less search than a
  mix of near and distant ones. After ~20 experiments, analyze the log:
  operator distribution, outcome rates, trigger patterns, harvest-to-canon
  rate, regression-causing accepts.

Status language: the framework is not "complete." It is *feature-complete
for sustained empirical use.*

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
