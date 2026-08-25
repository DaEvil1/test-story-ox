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
