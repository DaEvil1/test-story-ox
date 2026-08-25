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
