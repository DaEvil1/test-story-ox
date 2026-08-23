# Reference Calibration — 2026-08-21

The analyzer was run over four public-domain reference works
(`references/README.md`; full data in `tests/REFERENCE_ANALYSIS.md`) to
replace guessed thresholds with evidence. Story numbers below are from the
same day's run.

## Corpus comparison

| Metric | References (band) | Our story | Verdict |
|---|---|---|---|
| Sentence mean length | 15–24 words | ~10 | Deliberate clipped style; acceptable, but see stdev |
| Sentence-length **stdev** | 12–17 | 5.8 | **Our variance is low vs canon.** Aspirational band: ≥8 |
| Fragments (≤3 words) | 4% | 10% | We fragment 2.5× more than the reference band |
| Em-dashes per 10k | up to 70 | 40 | Em-dash usage is historically normal; no cap warranted |
| Top sentence-opener share ("the") | 8% | 28% → flagged at >15% | **Mannerism confirmed** — canon rarely exceeds ~10% on any opener |
| Abstract-noun-as-agent | ~0 per 10k (1 instance total) | 13 per 10k | **Clear mannerism signal** — target ≤5/10k |
| Dialogue share | 7–42% (corpus 21%) | 16% | Within band, lower edge |
| Fear lexicon /10k | 11.5 | 18.6 | We run hot on dread |
| Grief lexicon /10k | 12.4 | 19.6 | Hot, but grief is our engine — accepted |
| Joy lexicon /10k | 9.9 | 10.8 | ✓ now in band (was 6 pre-revision) |
| Awe/wonder /10k | 5.3 | 1.0 | **Starved** — grow wonder beats |
| Anger /10k | 4.1 | 5.9 | ✓ fine |

## Decisions taken

1. **Opener DOMINANT flag lowered 25% → 15%.** Canon evidence says any single
   opener above ~10–15% is drift.
2. **Abstract-agent tracking stays; mannerism zone set at ≥8/10k.** Canon
   baseline is effectively zero.
3. **No em-dash cap.** The reference corpus uses more than we do.
4. **Sentence-variance aspiration recorded (stdev ≥8)** as a line-pass goal,
   not a hard rule — our clipped register is a choice, but it currently
   flattens rhythm beyond what canon does even in restrained modes.
5. **Awe/wonder identified as the thinnest emotional channel** (1.0 vs
   canonical 5.3) — the strongest evidence-backed case for where new warmth/
   wonder beats go.

## Caveats

Period styles inflate length/variance bands (1900s–1920s prose runs longer);
translations (Metamorphosis) add their own cadence. Bands are directional
evidence for revision targeting, not pass/fail gates — hard rules stay in
`tests/automated/rules.yaml` and `tests/analysis/*.yaml` only where the
coupling map justifies them.

## Modern point (added 2026-08-21)

Cory Doctorow's *Little Brother* excerpt (2008, CC, length-matched) anchors
the modern end: dialogue 33% of text (ours 16%), em-dashes 73/10k (ours 58),
fragments 5%, sentence stdev 15.8, all five emotion categories within a
narrow band (4.0–11.2/10k). Takeaways: our dialogue share sits at the very
bottom of the PD band AND far under the modern point; our fear/grief run
roughly double the modern rates while joy is at parity — the "managed
melancholy" fingerprint, now measured against both centuries.
