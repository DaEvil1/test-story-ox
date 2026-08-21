# Red-Team Protocol

Adversarial cold-read review. Three personas, each instructed to argue the
story FAILS from a distinct angle, then report honestly where they couldn't.
Purpose: de-bias scoring (the primary reviewer also writes the fixes) and
test the real 8+ criterion — **unprompted praise of specific scenes**.

## Personas

### P1 — The Skeptical Literary Critic
Cares about: prose quality, subtext, restraint, originality vs. genre
derivativeness. Told to hunt for: mannerism, authorial intrusion, sentiment
unearned by craft, ambiguity used as evasion.

### P2 — The Genre Purist
Cares about: SF idea-content, world logic, the "mind-bending" contract,
escalation of consequence. Told to hunt for: concept borrowing without
development, stakes that stay abstract, endings that dodge the premise's
hardest question.

### P3 — The Grief Reader
Cares about: emotional honesty, relationships, whether loss lands. Has
personal experience of estrangement and bereavement (simulated). Told to
hunt for: sentimentality substitutes, grief that is asserted rather than
inhabited, characters who exist only to be lost.

## Procedure per pass

1. Cold read of `output/manuscript.md` under one persona; fresh session per
   persona; no access to ledgers or assessments beforehand.
2. Output: per-pillar scores (1–10), three scenes that worked (with why),
   three scenes that didn't (with why), one unprompted-praise list item
   minimum if any, verdict sentence.
3. Record in a dated `REDTEAM_REPORT_*.md`. Disagreements between personas
   are findings, not noise — map each to its criterion.

## Known limitation

All personas are simulated by the same underlying reviewer; blind spots are
correlated. The protocol still forces divergent reading angles and produces
falsifiable claims ("scene X praised by ≥2 personas"). Human readers remain
the gold standard this approximates.
