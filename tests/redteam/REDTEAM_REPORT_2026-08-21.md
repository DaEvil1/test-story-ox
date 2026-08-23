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

---

# Round 3 — Full Eight-Persona Read (2026-08-21, post line-pass)

State read: ch6 compressed, ch7 opening tightened, opener fusions across
ch2/3/4/5/7/8 (288→238 "The"-openers, 28%→24%), stdev 6.2→6.5. New question
set: *biggest improvements since your last read* (P1–P3), *greatest
strengths* (P4–P7), and for all: **what are you most missing?** Findings
recorded only — no changes made from this round.

## P1 — Skeptical Literary Critic · 6.9

- **Biggest improvement:** "ch7 used to announce itself; now it just begins. The fused sentences in the descent chapters breathe."
- **Still best:** ribbon reveal; Ari's exit.
- **Most missing:** one passage that risks being beautiful rather than correct — "I could not underline a single sentence twice. Airtight is not a compliment." And Ira remains a cadence, never a person; the grief outruns the ghost.

## P2 — Genre Purist · 6.8

- **Biggest improvement:** the surveillance seed and failed public channel — "the world now has procedures, which means it can take things away."
- **Still best:** burst scene; injury economics.
- **Most missing:** the Archive's **payoff**. I see what editing costs, never what it gives — no scene where curation is shown working as mercy or art. Without that, the Curators argue a case with no exhibits. Also: The Limit's ontology gets no new evidence after ch10.

## P3 — Grief Reader · 7.5

- **Biggest improvement:** "The coin comes home. That one-line fix made the ending land twice as hard."
- **Still best:** coin ceremony; quay whistle.
- **Most missing:** Lio's body. I know what Lio said and drew; I don't know Lio's weight, smell, the feel of carrying them. And Keji never once breaks — fifty thousand small managed griefs, zero unmanaged ones.

## P4 — Line Editor · 7.1

- **Greatest strength:** chapter endings are now rhythmically reliable; dialogue tags invisible throughout.
- **Improvement seen:** fusion pass measurably varied the descent chapters.
- **Most missing:** a single sentence per chapter that trusts itself past thirty words — variance is rising but no sentence yet runs long on purpose. And late-book walls never do anything sensorially NEW; pulse/hum recycle.

## P5 — Continuity Auditor · 7.6

- **Greatest strength:** the coin-evidence chain and injury continuity are now airtight end to end.
- **Most missing:** geography. Hall, Drift, market, quay have no fixed relations — walking times feel invented. And Keji's ordinary caseload: one routine client would date-stamp her competence against the exceptional case.

## P6 — Impatient Skimmer · 6.7

- **Biggest improvement:** ch6's slow lane is gone; ch7 enters at speed now.
- **Still best:** every chapter ends on a pull; the burst scene grabs like a thriller beat.
- **Most missing:** a clock. Nothing anywhere ticks — no deadline, no appointment, no countdown; stakes never learn urgency. And one mid-story action beat that isn't wall-mediated.

## P7 — Representation Reader · 7.5

- **Greatest strength:** Sera — costs, philosophy, and no one's helper. Queer reading available, unlabeled, respected.
- **Most missing:** a woman inside an institution — every curator/council seat reads male-coded; care labor carries the whole female cast. And Keji has no desires outside the quest: no friend who isn't useful, no pleasure that isn't memory.

## P8 — Read-Aloud Reader (new) · 7.2

- **Reads well aloud:** the ribbon transcript ("Kitchen sounds. A stripe of morning light…") is the best breath-pattern in the book; chapter endings give the voice somewhere to land.
- **Trips:** doubled definite articles in adjacent sentences ("The wall… The door…") still cluster audibly in ch4/ch7 despite the fusion pass; a few em-dash pairs per page force mid-breath reversals.
- **Most missing:** one long read-aloud sentence worth running out of breath for.

## Cross-round observation

Every persona's "most missing" is an **absence**, not a flaw: wonder,
bodies, breaks, clocks, geography, risked sentences, women in institutions.
Nothing needs removing. Everything named needs adding — which is consistent
with the story's entire revision history (omission-class failures only).

---

# Round 4 — Full Panel After Packages A/B/C/D/F+E (2026-08-21)

State read: ferryman scene (ch8), Lio-carried memory (ch2), the break at the
ribbon (ch10), morning-bell clock + senior curator (ch11), transit geography,
two risked long sentences. 10,820 words. Same question set: improvements /
most missing / scores.

## P1 — Skeptical Literary Critic · 7.2

- **Improvement:** "The ferryman scene is the first time the prose spends
  its savings. 'Harbor with the round vowels of her home islands' — that's
  an underline-twice sentence."
- **Most missing now:** still wants one full page of abandon; notes the
  break at the ribbon is "correctly small" but wants to know if Keji is
  *capable* of a larger one.
- **Scores shift:** Pulse 6→7.

## P2 — Genre Purist · 7.3

- **Improvement:** "Exhibit A exists. The Curators finally have a case — and
  Keji looking at her own steady hands afterward keeps it honest."
- **Most missing now:** The Limit ontology still stalls post-ch10 (unchanged
  verdict); would trade a chapter for one hard ontological test.
- **Scores shift:** Consequence 7→8, Promise 7 stays.

## P3 — Grief Reader · 7.9

- **Improvement:** "You gave him weight. 'Heavier than any sleeping child had
  a right to be' — I had to put it down. And she winds the ribbon until the
  nails go white: that's the truest grief in the book because it isn't
  dignified."
- **Most missing now:** Ari's interiority remains sealed; accepts it as
  design but names it every round.
- **Scores shift:** Bond 8→9? No — holds 8, "because Lio still leaves before
  I learn what Lio wanted."

## P4 — Line Editor · 7.4

- **Improvement:** stdev climb is audible; the ferryman list-sentence ("The
  wedding on the jetty stayed, and the argument about the tiller…") runs
  beautifully.
- **Most missing:** "The"-opener share still 24%; em-dash pairs up again.
- **Scores shift:** none.

## P5 — Continuity Auditor · 7.8

- **Improvement:** clock and geography hold under audit — morning bell,
  two bridges, half the fish-market all reconcile.
- **Most missing:** the ferryman never recurs (fine), but the dawn-batch
  council procedure should stay consistent if a sequel ever exists.
- **Scores shift:** World Logic 8 confirmed.

## P6 — Impatient Skimmer · 6.9

- **Improvement:** "ch8 has a reason to be quiet now — I'd have skimmed it
  before; the ferryman made me read."
- **Most missing:** unchanged: no ticking since the bell (accepted as tone),
  and ch5 remains the longest lane.
- **Scores shift:** Structure 6→7.

## P7 — Representation Reader · 7.8

- **Improvement:** "A woman came for the seals herself. One sentence, and
  the institution cracked open exactly as the watchlist asked."
- **Most missing:** Keji's off-quest life (still nothing); notes the
  ferryman receives care without being pathologized — good.
- **Scores shift:** Bond 8 confirmed.

## P8 — Read-Aloud Reader · 7.5

- **Improvement:** "Two sentences now exist that I'd read aloud for pleasure:
  the harbor vowels, and the sea wearing lamplight 'since before anyone's
  oldest memory of it.'"
- **Most missing:** breath-trip clusters persist in ch4's chamber sequence.
- **Scores shift:** Pulse 7 confirmed.

## Round-4 score adoptions

| Criterion | Was | Now | Evidence |
|---|---|---|---|
| #12 Relationships dramatized | 7 | 8 | Lio gains a body; P3's core gap answered |
| #22 Both sides weighted | 7 | 8 | The Curator case now has exhibits (ferryman) |
| #31 Defamiliarization | 7 | 8 | Editing-as-care reframes the familiar |
| #34 Vulnerability | 7 | 8 | The ribbon-wind: unmanaged, undignified, true |

(#33 held at 7 pending lexicon ratio ≥0.70 — currently 0.68.)
