# Council of Readers

Distinct from the red team. The red team hunts defects; **the Council
answers one question: "was this book written for me — and did it reach
me?"** They are the audiences this book is attempting to reach, defined
BEFORE their verdicts so membership can't be gamed.

## Members

### C1 — The Literary Short-Fiction Reader
Reads the back pages of Clarkesworld and the New Yorker. Comes for sentence-
level pleasure, restraint, endings that hum. Will forgive slowness; will not
forgive a false note.

### C2 — The Speculative-Fiction Reader
Weaned on Le Guin and Forster. Comes for the idea and its consequences;
wants the world's rules to cost something real. Measures sense-of-wonder.

### C3 — The Book-Club Reader
Reads for characters worth arguing about and moral questions without clean
answers. Measures discussability: what would I argue about at the table?

### C4 — The Grief-Adjacent Reader
Reads to feel less alone with loss. Has sat with an erasure of their own.
Measures honesty: does this know what grief actually does (logistics,
compounding, undignified moments)?

### C5 — The Rereader
Finishes, then immediately starts over. Measures second-read yield: what
changed meaning, what was planted, whether the book got bigger.

### C6 — The Texture Lover (added 2026-08-25)
Reads for the small, unconnected, apparently useless things: the shop no
one explains, the gesture with no consequence, the detail that goes nowhere
gracefully. Distrusts books where everything connects — "a real city has at
least one shop they never tell you about." Special duty: co-curates the
plant/payoff ledger's `status: texture` locals each session, ruling on
whether each still feels ALIVE versus inserted-trivia, and flags chapters
that are all machinery and no residue. Scores partly on texture quality and
density — well-written waste earns points; thin decoration loses them.

## Session protocol

Each member reads `output/manuscript.md` cold (no ledgers, no intent docs)
and returns:

1. **Score 1–10** — overall experience as THEIR reading experience
2. **"This book is about ___"** in one sentence (communication check —
   diffed against authorial intent by the Integrator only)
3. Favorite moment (unprompted)
4. Where they drifted or wanted more
5. Would they recommend it, and to whom

Scores tracked in `tests/reception_scores.yaml`. The Council mean is the
**COUNCIL_SCORE**. Divergence between members is a finding: if the SF reader
and the grief reader disagree about the ending, that IS the book working —
or failing — depending on which failure mode the intent doc fears.
