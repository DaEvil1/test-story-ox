# Editorial Board Protocol (added 2026-08-25)

## Purpose

Distinct from the red team (adversarial scoring) and the Council (audience
reaction): the **editorial board** reads a revision together, debates what
needs changing, and produces a unified recommendation to the author. The
author reviews each item and responds: accept / adapt / discard-with-reason.

## Composition

| Role | Members | Submits |
|---|---|---|
| **Chair** | Integrator mode | Compiles agenda; ensures every item gets discussed; records consensus/dissent |
| Line editor | P4 | Sentence-level craft notes |
| Emotional reader | P3 | Resonance, vulnerability, whether beats land |
| Momentum reader | P6 | Pacing, drift, scene drive |
| AI-line analyst | P12 | Pattern discoveries + proposed fixes |
| Continuity auditor | P5 | Fact-check, timeline, geography |
| Written-only | P1, P2, P7 | Submit written notes; do not attend debate |

## Session procedure

1. Chair compiles agenda from: latest red-team round, Council session,
   analyzer flags, ledger gaps, discovery-buffer seeds, prior triage items
   marked DEFER.
2. Each attending member submits 2–5 items they want changed/discussed.
3. Chair merges overlapping items; orders by impact.
4. Board works through each item:
   - Presenter states the issue
   - Other members respond (agree / disagree / propose alternative)
   - Chair records: CONSENSUS (all agree), MAJORITY (with dissent noted),
     or DEADLOCK (author must decide)
5. Output: `EDITORIAL_SESSION_*.md` with prioritized recommendations.
6. Author responds per-item in decisions.log.

## When to convene

After any pass that changes ≥2 chapters, or before content-complete
declaration. Not every cycle — the board is for deliberation, not routine
verification (that's the quantitative gate's job).

## Experiment planning sessions

At the start of a full run, the board convenes to suggest 3 experiments.
Each suggestion names: operator, scope, question, and which member proposed
it (and why). Author selects 3 (or adjusts). Selected experiments enter the
lifecycle normally.

Before each experiment closes, the presenting member reviews the result and
reports to the board: did it answer the question? Was the yield worth the
divergence? Any surprises?

After all experiments and the consolidation run, the board reconvenes for a
post-mortem: what changed, what was gained, what lessons go into
`docs/experiment_lessons.md`.

## Lessons learned file

`docs/experiment_lessons.md` accumulates one entry per completed
experiment cycle. Each entry: what was tried, what worked, what didn't,
what surprised the board, what rule or instinct was updated as a result.
Members interpret entries through their own lens — P4 cares about craft
implications, P6 about pacing, etc. The file grows over time and becomes
institutional memory that future sessions draw from.
