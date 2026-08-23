# Reference Corpus

Public-domain works used to calibrate the analyzer's thresholds (see
`docs/reference_calibration.md`). Sourced from Project Gutenberg; boilerplate
stripped. Do not edit — regenerate from sources if needed.

| File | Work | Author | Year | Length | Source |
|---|---|---|---|---|---|
| `the_machine_stops.md` | The Machine Stops | E.M. Forster | 1909 | ~12.2k words | Gutenberg #72890 (The Eternal Moment collection) |
| `the_metamorphosis.md` | The Metamorphosis | Franz Kafka (tr.) | 1915 | ~21.9k words | Gutenberg #5200 |
| `the_yellow_wallpaper.md` | The Yellow Wallpaper | Charlotte Perkins Gilman | 1892 | ~6.1k words | Gutenberg #1952 |
| `mrs_dalloway_in_bond_street.md` | Mrs Dalloway in Bond Street | Virginia Woolf | 1923 | ~3.1k words | Gutenberg #63107 |
| `little_brother_excerpt.md` | Little Brother (excerpt, first ~12k words) | Cory Doctorow | 2008 | ~12k words | Gutenberg #30142 (CC-licensed) |

`little_brother_excerpt.md` is the **modern in-genre calibration point**:
near-future surveillance SF, CC-licensed, length-matched to our story.
First-person voice — its "I"-opener dominance is a persona artifact, not a
band; use it for dialogue share, rhythm, and emotion-spread comparison only.

Selection rationale: PD works in the story's length/genre neighborhood —
mind-bending SF (Machine Stops), domestic surrealism with cost-driven
structure (Metamorphosis), psychological destabilization and unreliable
perception (Yellow Wallpaper), interiority/register control (Woolf).

Run: `python tools/analyze_story.py --chapters-dir references --report tests/REFERENCE_ANALYSIS.md`
