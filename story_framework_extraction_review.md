# Review of the Extracted `story-framework` Repository

I think Ox Alpha has extracted the **most important part of the original project successfully**: the creative/search architecture is now recognizably independent of *Something Was Left Behind*. But I would not quite call the repo a general story-writing framework yet.

I'd describe its current state as:

> **A genuinely general creative-search architecture wrapped in a still fairly story-specific literary-fiction measurement and run profile.**

That distinction matters, because the part that was hardest to invent — the cognitive architecture — has generalized much better than the easier-to-overlook plumbing.

## What transferred extremely well

The best part of the new repo is that the philosophy survived the extraction rather than just the files. The canonical pipeline now starts with an uncontaminated Creative Pulse, separates exploration from ordinary revision, protects PROBE from coherence pressure, treats failed experiments as useful, uses epistemic firewalls and blind comparison, distinguishes mechanical/procedural gates from subjective testimony, and explicitly says internal institutions should discover questions rather than dictate answers. That's the actual intellectual core of what emerged from the prototype.

The later refinements also made it over: Character Board findings are no longer treated as character-ground-truth commands; pairwise comparison is horizon-aware; structural comparisons get position-bias protection; every PROBE is tracked rather than only survivors; creative distance is recorded; and long-run problems such as motif capture and consolidation sanding are observations rather than automatic optimization targets.

So if you started another roughly literary speculative novella tomorrow, I think this would be a **very strong second-generation starting point**.

But that qualification — “roughly literary speculative novella” — is where I think the extraction isn't finished.

# The biggest problem: `analyze_story.py` is still the old book

This is the clearest thing I found.

The analyzer literally contains:

```text
Keji | Ari | Sera | Ira | Lio
```

in its speech attribution regex, and its voice-fingerprint analysis only recognizes Keji, Ari, Sera and Ira.

Its emotion output table is hardcoded for **ch1 through ch11**, and its motif analysis literally tracks:

> wall, pulse, hum, coin, warm, seam, ink, tide/water, palimpsest-layer, limit

which is essentially the motif vocabulary of the original novella.

It even still calls one of its coupled analyses the **“Dread Triangle.”**

That's actually useful because it reveals the architectural boundary very clearly:

**The process generalized. The instrumentation didn't.**

I'd make `analyze_story.py` almost entirely config-driven. It should get character names, motifs, emotional channels, atmosphere vocabulary and perhaps desired prose characteristics from `book.yaml` and project files. A new project should be able to have seven characters called whatever it likes, twenty-eight chapters, motifs involving oranges and elevators, and a tonal palette dominated by embarrassment and delight without touching Python.

There should be virtually **zero semantic knowledge of a story inside the analyzer code**.

# `init.py` has the same problem, just more subtly

There are some obvious fossils:

```text
opponent_pressure - none | archive | limit | character-name
stakes_scope - personal | civic
require_civic_stakes: true
```

Those aren't neutral storytelling concepts; they're descendants of the Archive/Limit/civic-stakes structure of the prototype.

The default genre is still `literary-sf`, target length is 10,000 words, and max is 50,000. It also creates `src/03-outlines/` while the autonomous protocol explicitly rejects outlining during discovery.

There are even literal template names:

> `absent_character.md`  
> `the_limit_ambiguity.md`

being copied into every new project.

And `check_story.py` still contains an explicit special case for `"The Limit"`.

Those are easy fixes, but I would take them seriously because this is precisely how hidden assumptions get inherited.

A really useful automated test would be:

> initialize a completely new project, then grep its entire generated tree for `Keji|Ari|Sera|Ira|Lio|Archive|The Limit|palimpsest|coin|tide`.

The correct result should be **zero**, except perhaps in an explicitly labeled historical case-study document.

I'd actually make that a CI test for the framework.

# The larger issue is aesthetic rather than technical

Your `style_guide.md` currently calls several choices **non-negotiable constraints for all prose passages**, including no explanation of character choices/internal states, no authorial commentary, no narrator-delivered philosophical argument, present-moment immediacy over reflection/summary, and conflicted states expressed primarily through physical action/sensation.

Those were very productive constraints for the first story.

They're absolutely not universal properties of good fiction.

They would be hostile to quite a lot of:

- omniscient fiction;
- comic narration;
- essayistic novels;
- heavily introspective first person;
- Nabokovian narrator performance;
- Austen-like free indirect commentary;
- philosophical fiction;
- stories where reflective summary is the voice.

Similarly, the 50-item rubric openly draws from one particular Western craft tradition, and then encodes things such as one central dramatic question, try-fail escalation, midpoint shift, want-vs-need, flaw-with-a-price, antagonist mirror, rising personal stakes, costly climax choice and cathartic release.

That's a perfectly defensible **craft profile**.

It's not “what all stories need.”

Imagine giving this framework *Mrs Dalloway*, *Waiting for Godot*, a slice-of-life novella, Borges, *If on a winter's night a traveler*, or a deliberately static absurdist story. The system could begin “repairing” exactly the thing that makes the work what it is.

I'd therefore make a very strong architectural distinction:

> **CORE ≠ CRAFT PROFILE**

The core is experiments, reader-state, judging, provenance, ledgers, Creative Pulse, character autonomy, consolidation, etc.

The craft profile answers:

> What kind of writing are we attempting?

Your current style guide + much of the 50-item rubric could become something like a default `modern-literary-narrative` profile rather than framework law.

Then `N/A` needs to be a legitimate rubric state.

“No antagonist mirror” shouldn't give a quiet domestic story a 2/10. It should sometimes mean:

> This criterion does not describe this book.

# The autonomous run protocol is also a **writing method**, not the framework

I actually think it's a really interesting writing method.

It says:

> create 2–4 major characters; don't outline or build maps/factions/magic systems; write first and last chapters first; discover the middle; typically reach 8–12 chapters; later run batches of exactly three experiments; finish with exactly three final passes.

That's coherent. It may be very good.

But it strongly represents what you and Alpha-Ox learned from this specific experiment about **pantsing a novella**.

It isn't yet general story creation.

For example, a sprawling political fantasy might genuinely benefit from factions and maps before drafting. A mystery may need more deliberate murder mechanics. A 150,000-word multi-POV epic isn't likely to want two to four major characters or fifteen chapters maximum. A pure pantser story may be harmed by writing its ending first.

So I wouldn't delete `AUTONOMOUS_RUN.md`.

I'd rename the conceptual level:

> **Run strategy: Bookend Discovery**

Then eventually you could have other run strategies when you've actually tested them — not invented speculatively now.

Maybe someday:

> Open-ended discovery  
> Mystery construction  
> Long-form multi-POV  
> Outline-assisted

But I'd resist creating those until another project actually teaches you why they're needed.

That keeps faith with the empirical spirit of the project.

# Things I think did get lost from the original repo

Yes — a few. Some are quite concrete.

## 1. The reference-calibration process

The README advertises reference calibration, but the original had a dedicated `docs/reference_calibration.md` that explicitly compared the manuscript against the corpus, recorded decisions, and — importantly — recorded caveats explaining why corpus values were evidence rather than pass/fail truth.

I would bring this back as a **generic calibration-report template**, not the old numbers.

This is especially important once reference sets become project-specific.

## 2. The living manual `VALIDATION_REPORT.md`

This seems to be missing from the scaffold.

The new tests README explicitly says manual findings are recorded there, but `init.py` doesn't appear to create/copy one.

The original report was actually useful: it recorded open gaps, chapter-level qualitative judgments, deliberate exceptions and historical changes in one place.

That's a real omission rather than an aesthetic preference.

## 3. External-review provenance/integration

The original `review_response_2026-08-25.md` preserved the outside review, gave every suggestion a TAKE/ADAPT/DISCARD/DEFER-style verdict, recorded disagreements, and documented which framework changes arose from it.

Given the use of NotebookLM and external framework discussions during prototyping, I think this is particularly valuable.

I'd make it optional, perhaps:

```text
docs/external_reviews/
```

with a generic response template.

Then future framework extraction can answer:

> Which abilities arose internally, and which blind spots were revealed externally?

## 4. The red-team scaffold is thinner than the original process claims

`pipeline.md` still talks about P1–P9 plus Memory Reader and Reconstructionist, but a newly initialized project's `personas.md` is blank and the generic persona template only supplies six starting roles.

The original had a broader functional panel including:

- continuity;
- impatient reading;
- representation;
- read-aloud;
- known-AI-pattern detection;
- novel-AI-pattern discovery;
- memory;
- reconstruction.

I wouldn't preserve their **story-specific personalities**.

I would preserve those **sensor functions** as reusable templates.

Those are the four things from the old repo I'd most clearly bring over.

# What I would do before letting it write Story #2

I would **not redesign the creative framework**.

I'd do one genericization pass.

Specifically:

1. Move every story semantic out of Python and into project configuration: characters, motifs, emotional lexicons, atmosphere dimensions, stakes categories, story-specific couplings.
2. Split `core` from `profiles`: keep experimental/search machinery universal; make prose doctrine, craft criteria, calibration corpus and thresholds selectable/project-defined.
3. Change hardcoded quantities such as 2–4 characters, 6–15 chapters, three experiments, three final passes and bookends-first into **strategy defaults**, not definitions of fiction.
4. Restore a generic reference-calibration report, manual validation report and optional external-review provenance workflow.
5. Make the analyzer/report generation dynamically discover chapters instead of assuming eleven, and remove every original-story literal from code/templates.
6. Add a **framework leakage test** that initializes a dummy project and fails if prototype names/concepts appear in generated output.

Then I would stop.

I wouldn't try to theoretically account for every possible genre.

Instead I'd stress-test the framework against three deliberately alien premises before committing to a serious second book.

Something like:

- a first-person comic romance with no antagonist;
- a large multi-POV fantasy that actually wants explicit world design;
- an episodic/experimental literary work with no conventional central dramatic question.

You don't even need to write all three books. Let Alpha-Ox initialize them and try the first phase or two.

Wherever it says:

> “I can't do what this story wants because my framework says I must do X”

you've found another prototype assumption masquerading as a universal principle.

# Overall

I think the extraction is **very promising**.

In fact, the hardest stuff is the stuff that generalized successfully: creative search, executable alternatives, delayed coherence, epistemic separation, blind comparison, preservation of failed discoveries, character veto, anti-bureaucratic Creative Pulse, and institutional evidence that doesn't automatically become authority.

What's still attached to the first story is mostly **measurement, aesthetics and scale assumptions**.

That's a much easier problem to solve.

Right now I'd call `story-framework`:

> **a general AI fiction search engine with a built-in modern literary-SF novella profile that is accidentally pretending to be universal.**

Separate those two layers cleanly, and I think you have something considerably more interesting: not a recipe for producing stories like the first one, but a reusable environment in which the model can discover **what kind of writer this particular story needs it to become**.
