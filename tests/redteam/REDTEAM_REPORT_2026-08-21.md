# Red-Team Report — 2026-08-21 (Revision 6 cold read)

Three adversarial personas per `tests/redteam/personas.md`, each reading
`output/manuscript.md` (~10.5k words, title now "Something Was Left Behind").
Simulated by one underlying reviewer — correlated blind spots are possible;
divergent instructions were enforced. Findings below are recorded verbatim in
spirit; the actionable ones were triaged same-session.

## P1 — Skeptical Literary Critic

Pillars: Structure 5 · Consequence 7 · Trust 8 · Pulse 6 · Bond 6 · World 8 · Mind 8 · Promise 6 → **~6.6**

- **Worked:** the ribbon reveal ("the answer was in her pocket through every sealed door" — earned irony); Ari's exit ("'I finally decided.' He did not say what he had decided" — subtext held); the quay restraint.
- **Didn't:** "The city is a palimpsest" (ch1) is a definitional label dropped into narration — telling the theme in word one. *(Triage: fixed same-session — label removed, evidence kept.)* Body-sensation formulas persist at low density ("Her throat closed" family).
- **Unprompted praise:** ribbon reveal sequence.
- **Verdict:** "Controlled to a fault; when it risks warmth it earns it, but the register never fully relaxes even when the story does."

## P2 — Genre Purist

Pillars: Structure 6 · Consequence 7 · Trust 7 · Pulse 6 · Bond 5 · World 8 · Mind 7 · Promise 6 → **~6.5**

- **Worked:** the Drift burst — first time the premise's danger is *shown* at civic scale; node enforcement logic is consistent and costly (fingers, permanent seal); surveillance beat (terminal greeting her by name) is proper SF dread.
- **Didn't:** the destabilizing material arrives at the 80% mark; The Limit's thesis is never tested against its own extreme (nobody tries full exposure, so its claim stays hypothetical); Lio's ultimate nature unresolved will read as dodge to some genre readers.
- **Unprompted praise:** the injury scene ("the Archive charges for access — that's the right kind of world").
- **Verdict:** "A literary ghost story wearing SF clothes — delivers dread, withholds wonder. The label promises more mind than it bends."

## P3 — Grief Reader

Pillars: Structure 6 · Consequence 8 · Trust 8 · Pulse 7 · Bond 8 · World 7 · Mind 7 · Promise 7 → **~7.3**

- **Worked:** the coin ceremony ("One for you, because you lose things"); Sera's grief-edit confession ("I wanted the rough parts back. They were his."); the whistle exchange at the quay; the kitchen laugh inside the ribbon.
- **Didn't:** ch4's procedural language distances at exactly the emotional core; Ari grieves only through furniture — we never see him feel; Lio vanishes from the texture of the back half until the quay.
- **Unprompted praise:** tidepool memory; "Crooked holds."
- **Verdict:** "'Made room' broke me. This knows that grief is a logistics problem — what to carry, where to put it."

## Cross-persona findings

**Scenes praised unprompted by ≥2 personas (success test):**
1. Ribbon reveal (P1, P3)
2. ch9 injury cost (P2, P3)
3. Quay sequence incl. whistle (P1 mild, P3)

→ The 8+ criterion "cold reader praises specific scenes unprompted" is now
partially met: three scenes survive adversarial reads.

**Disagreements mapped to criteria:**
| Disagreement | Personas | Criterion |
|---|---|---|
| Prose mannerism: fatal flaw vs. non-issue | P1 vs P2 | #26/#27 |
| Ambiguity: rich vs. evasion | P3 vs P2 | #19/#40 |
| Ari's opacity: masterful vs. unearned | P1 vs P3 | #12/#34 |

**Score impact adopted this session:** #2 → 7 (title + scale-promise + reliability beat close the contract gap both P1 and P2 flagged), #40 → 7 (burst + ribbon + reliability question deliver the label's core experience, though still gently). All other scores unchanged pending next full re-score.

---

# Round 2 — Four Additional Personas (2026-08-21)

## P4 — The Line Editor

Pillars: Structure 6 · Consequence 7 · Trust 8 · Pulse 5 · Bond 7 · World 8 · Mind 7 · Promise 6 → **~6.75**

- **Worked:** dialogue tags are invisible (clean "said" discipline); the triple anaphora in ch5 ("She thought of… She thought of… She thought of…") is rhetorical and earns its repetition; fragment control at chapter endings.
- **Didn't:** "The"-openers dominate chamber descriptions (28% corpus vs ~8% canon — see `docs/reference_calibration.md`); abstract-noun-as-agent constructions persist ("The name lodged in her chest", "a pressure settled in her ribs", "The silence remained") where canon runs ~zero; sentence-length variance is flat against the reference band (stdev 5.8 vs 12–17).
- **Unprompted praise:** the ribbon transcript paragraph's rhythm ("Kitchen sounds. A stripe of morning light…").
- **Verdict:** "The revision passes are real — the prose is clean. What remains is a house style leaning on three crutches the canon doesn't use."

## P5 — The Continuity Auditor

Pillars: Structure 7 · Consequence 8 · Trust 9 · Pulse 7 · Bond 7 · World 8 · Mind 7 · Promise 7 → **~7.5**

- **Tracked clean:** recorder state (introduced ch4 → desk ch11); spindle (cracked ch9, never returns); coin custody chain; bandaged-hand/good-hand usage from ch9 on; who-knows-what (Sera never told about the ledger card and never references it); timeline of days across ch8–11.
- **Found two wobbles:** (1) ch3 exit doesn't say she retrieved the glitch from Ari's desk — ch4 has her folding it again; (2) ch11 sets the coin on the desk beside Ari's seals, but the final walk has it warming in her pocket — retrieval unshown.
- **Unprompted praise:** the coin-custody chain itself ("the mark pressed into her palm is tracked like evidence").
- **Verdict:** "Above average continuity for a serialized draft; two one-line repairs needed." *(Both triaged: fixed same-session.)*

## P6 — The Impatient Skimmer

Pillars: Structure 6 · Consequence 7 · Trust 7 · Pulse 6 · Bond 6 · World 7 · Mind 6 · Promise 6 → **~6.4**

- **Where attention dropped:** ch6's first third (packet + spindle mechanics before Sera arrives) is the slowest lane; ch7's opening re-ran the door-refusal pattern one time too many; ch2's strata description is lovely but skimmable.
- **What pulled them back:** every chapter now ends on a pull (they checked — all 11 pass); the front-door beat rescued ch8's quiet opening; the burst scene "grabbed like a thriller beat."
- **Unprompted praise:** chapter-ending hooks as a system.
- **Verdict:** "I only almost left once, at ch6's midpoint, and the node paid me back for staying."
- *(Triage: ch7 opening compressed same-session; ch6 noted as the standing candidate for the next compression pass.)*

## P7 — The Representation Reader

Pillars: Structure 7 · Consequence 8 · Trust 8 · Pulse 7 · Bond 8 · World 7 · Mind 8 · Promise 7 → **~7.5**

- **Observation:** institutions are male-coded (Ari, the Council), care labor and memory-work are female-coded (Keji, Sera, the widow, the water-seller) — a defensible thematic pattern, but the text never acknowledges it as choice; risks reading as default. A queer reading of Keji-and-Ira is available and handled without labels — genuinely well done.
- **Verified neutral:** Ira and Lio carry no pronouns anywhere in the manuscript, and the character docs match (watchlist concern closed).
- **Recommendation:** record the institution/care gendering as an intentional pattern in the canon ledger so future revisions preserve or consciously break it.
- **Unprompted praise:** Sera — "a female character whose philosophy costs something and who is never anyone's helper."
- **Verdict:** "Nobody here exists to be lost. That's rarer than it should be."

## Round-2 triage summary

| Finding | Source | Action |
|---|---|---|
| Glitch retrieval gap after Ari's desk | P5 | Fixed (ch3 exit line) |
| Coin re-pocket unshown | P5 | Fixed (ch11) |
| Abstract-agents ×3 flagged | P4 | Converted (ch3, ch4, ch11) |
| ch7 opening déjà vu | P6 | Compressed |
| Awe channel starved | Calibration | Seeded: "how gently it let him go" (ch10) |
| Institution/care gendering | P7 | Recorded as intentional pattern in canon watchlist |
| ch6 first-third slowness | P6 | Banked — next compression pass target |

No criterion score changes this round; findings banked with quantified targets already documented in `docs/reference_calibration.md`.
