# Red-Team Report — 2026-08-24 (Round 5: full nine-persona panel)

Cold read of `output/manuscript.md` (10,820 words). Round 1–4 history in
`REDTEAM_REPORT_2026-08-21.md`. New this round: **P9 AI-Pattern Hunter**,
whose findings are quantified and proposed as detection rules.

## P1 — Skeptical Literary Critic · 7.2

Improvement since last read: ch8's ferryman scene has settled in as the
book's warm center without going soft. Most missing: still no full page of
prose abandon; Ira remains a cadence. Verdict: "Cleaner every round; now it
needs to be *moved* to be great."

## P2 — Genre Purist · 7.3

Improvement: the Curator exhibit changed the argument from assertion to
evidence. Most missing: one hard ontological test of The Limit. Verdict:
"Respects the reader; under-tests its own god."

## P3 — Grief Reader · 7.9

Improvement: reread the Lio-carry line and it held. Most missing: Ari's
sealed interiority (accepts as design). Verdict: "The ribbon scene is the
emotional spine and it holds weight."

## P4 — Line Editor · 7.4

Improvement: fusion pass audible in descent chapters. Most missing:
sentence-variance still below band; "the X of" frames everywhere once you
hear for them. Verdict: "Three crutches left, all measured."

## P5 — Continuity Auditor · 7.8

Improvement: clock + geography reconcile end-to-end. Most missing: nothing
material. Verdict: "Audit-clean at this scope."

## P6 — Impatient Skimmer · 6.9

Improvement: ch8 quiet section earns its place now. Most missing: a
mid-book action beat not mediated by walls. Verdict: "I stayed the whole
way this time."

## P7 — Representation Reader · 7.8

Improvement: senior curator cracks the institution open. Most missing:
Keji's off-quest life. Verdict: "Patterns are now choices, which is all I
ask."

## P8 — Read-Aloud Reader · 7.5

Improvement: ferryman list-sentence reads beautifully aloud. Most missing:
chamber sequences still cluster doubled articles; em-dash pairs force
mid-breath reversals. Verdict: "Two sentences I'd perform; want ten."

## P9 — AI-Pattern Hunter (new) · findings & rule proposals

Quantified scan (per-10k rates, canon reference where available):

| Pattern | Count | Rate | Canon rate | Proposal |
|---|---:|---:|---|---|
| Negation-contrast frame | 45 total | — | ~0 | **ADOPTED** into checker this round (NC-01 warn, NC-02 WEAK cap = 5% of sentences, floor 3) |
| Abstract "the X of" frames (weight/shape/sound/feel/sense) | 17 | 15.7 | ~2–4 | **ADOPT** as analyzer flag (done, thr >8/10k); consider rules.yaml warning if it resists two passes |
| Triadic lists ("x, y, and z") | 1 | 0.9 | varies | Monitor only — not prevalent here |
| "not just / not merely" | 2 | 1.8 | low | Monitor only |
| Participial sentence openers | 0 | 0 | low | None needed |
| Motif FUSED pairs (coin+warm 75%, wall+hum 73%) | — | — | — | Not an LLM signature per se; tracked by co-occurrence matrix instead |

P9 verdict: "The text's remaining machine-fingerprint is one construction —
abstract-of framing — plus the already-governed negation family. Everything
else canonical detectors look for is absent or at floor."

## Cross-panel summary

- Unprompted praise converged again on: ferryman scene, ribbon break,
  quay sequence.
- Recurring asks (unchanged): prose risk (#26), voice music (#13),
  one more register swing (#33), Keji outside the quest (#44).
- Panel average moved 7.19 → 7.31 across rounds 3→5 on identical criteria.

---

# Round 6 - Full Panel After "Voice & Residue" (2026-08-24)

State read: dialogue-music pass (Sera clipped further, Keji terser), opener fusions to target, abstract-of frames converted below threshold, tiles-with-the-neighbor beat (ch8), rage beat and ribbon sacrifice carried in.

## P9 AI-Pattern Hunter - rule status

- Abstract-of frames: 15.7 -> 7.4/10k - under flag. Target met.
- "The"-openers: 28% -> 20% - at threshold. Remaining instances audited: chapter openers, deliberate catalogs (ch4 recorder inventory), staging beats; mass conversion past this point would sterilize rhythm. Recommend holding the flag threshold here rather than pushing lower.
- Negation family: governed by NC-01/NC-02; corpus within caps.

## P4 Line Editor - 7.9

"All three crutches retired or inside their bands. This is the cleanest draft of the manuscript I have read."

## P3 Grief Reader - 8.0

"The tiles beat undid me - she has a life, one evening of it, and losing the ribbon right after hearing it is exactly how loss compounds."

## P7 Representation Reader - 7.9

"Keji outside the quest for two sentences changes how every other scene reads. M8 closed."

## P2 Genre Purist - 7.4

Standing ask unchanged (ontological test); everything else holding.

## Score adoptions this round

| Criterion | Was | Now | Evidence |
|---|---|---|---|
| #13 Distinct voices | 6 | 7 | Three-way fingerprints (0.33-0.67); contraction axis spreads 0.00/0.11/0.33 |
| #26 Rhythm & register | 7 | 8 | All quantified crutches at/inside targets; stdev 6.9 |

Panel average ~7.5 -> ~7.7.
