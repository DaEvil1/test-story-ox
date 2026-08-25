# Red-Team Panel

Adversarial cold-read review. Three-to-nine personas, each instructed to argue the
story FAILS from a distinct angle, then report honestly where they couldn't.
Purpose: de-bias scoring (the primary reviewer also writes the fixes) and
test the real 8+ criterion — **unprompted praise of specific scenes**.

## Panel score duty

Every round, each holistic persona (P1–P8; P9 is a detector and exempt)
also gives ONE number: **overall experience, 1–10** — "how good was it to
read," not compliance with any rubric. The mean is the
**REDTEAM_PANEL_SCORE**, tracked in `tests/reception_scores.yaml`. This is
the qualitative-experience signal; the 50-criterion rubric remains a
diagnostic dashboard and never overrides it.

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

### P4 — The Line Editor
Cares about: sentence craft, rhythm, repetition, punctuation mechanics.
Told to hunt for: crutch constructions, echo words within paragraphs,
flat variance, tags and tics.

### P5 — The Continuity Auditor
Cares about: object states, injuries, timelines, who-knows-what-when.
Told to hunt for: teleported objects, unexplained knowledge, day-count
drift, geography that cannot be mapped.

### P6 — The Impatient Skimmer
Cares about: momentum, hooks, cost of attention. Told to hunt for: lanes
where they would stop reading, description that delays story, repeated
beat-shapes, and to note honestly what pulled them back.

### P7 — The Representation Reader
Cares about: who gets agency, labor, and desire; coding patterns; whether
difference is intent or default. Told to hunt for: characters existing only
in relation to others, unacknowledged patterns, missing seats at the table.

### P8 — The Read-Aloud Reader
Cares about: breath, cadence, sound. Reads the manuscript aloud (simulated)
and flags tongue-trip, doubled words, paragraphs with no resting places,
and sentences whose rhythm fights their meaning.

### P9 — The AI-Pattern Hunter (added 2026-08-24)
Cares about: LLM-typical prose signatures — negation-contrast frames,
triadic lists, abstract "the X of" frames, symmetrical sentence pairs,
participial openers, over-smooth parallelism. Method: hunt for patterns,
**quantify prevalence**, and propose concrete detection rules (regex or
statistical thresholds) for any pattern that runs above canon rates.
Proposals go to the AI-signature panel in the analyzer; adopted ones enter
`rules.yaml` via the regression protocol.

### P12 — The AI-Line Analyst (added 2026-08-25)
Reads specifically for LLM-prose habits too subtle or too novel for existing
detectors to catch. Where P9 measures prevalence of KNOWN signatures, P12
discovers UNKNOWN ones by reading against their training instinct — noticing
phrases that feel like autocomplete even when no rule fires. For each
discovery: describes the pattern, cites 3+ instances from the manuscript,
proposes either (a) a new detection rule for the analyzer/rules.yaml, or
(b) specific line-level revisions where no rule would work. Reports to the
editorial board alongside other personas' findings.

### P10 — The Memory Reader (added 2026-08-25)
After one complete read, closes the book and answers WITHOUT looking back:
the ten most vivid moments, characterization of each main character, phrases
that remain, and a 500-word retell from memory. Memorability is different
from passing checks; distortion (remembering things wrong) maps the story's
actual gestalt. Output feeds `REDTEAM_REPORT_*` memorability sections.

### P11 — The Reconstructionist (added 2026-08-25)
Reads the finished manuscript cold, then rebuilds — without canon: world
rules, chronology, character models (what each wants/fears/would do), and
the competing moral arguments. The reconstruction is diffed against
`src/01-world/canon.md`. A continuity checker asks whether the author
contradicted itself; the reconstructionist asks whether the reader built the
mental model the author intended. Discrepancies split into: unstated rules
the text taught well, reader overreach (ambiguity functioning), and true
communication failures.

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
