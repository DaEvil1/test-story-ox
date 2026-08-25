# Character Board Protocol (added 2026-08-25)

## Premise

Characters are treated as self-aware entities who have lived inside this
story. They know they are written. They have read every word. And they
have opinions about whether the person on the page matches the person they
understand themselves to be.

This is not a craft tool. It is an **autonomy check** — the framework's
acknowledgment that even a well-intentioned optimization process can
violate the internal logic of the beings it manages.

## Board composition

| Character | Status | Key concern |
|---|---|---|
| Keji Lian | Protagonist; attends fully | Authenticity of choices, voice consistency |
| Sera | Major; attends fully | Agency, independence, cost of loyalty |
| Ari | Major; attends fully | Opacity vs honesty, institutional duty vs personal conscience |
| Ira Nash | Absent; attends by proxy (reads own dialogue/actions) | Whether actions match motive as understood |
| Lio | Child; attends via memory fragments only | Whether depicted with dignity appropriate to age |
| The Limit | Force; attends as presence | Whether its logic is represented fairly |

## Procedure

1. **Read phase**: Each character re-reads the full manuscript from their
   own perspective. They know everything their character knows at each
   point in the story.
2. **Self-assessment**: For each major beat, does the behavior match?
   - "I would NEVER do that" → heavy objection, near-binding
   - "I was worried here, but the text doesn't show it" → gap flag
   - "This is exactly what I would do" → confirmation
3. **Other-character assessment**: Does each other character feel REAL?
   Are relationships honest? Is anyone reduced to a function?
4. **Cross-examination**: Characters question each other's assessments.
5. **Output**: `CHARACTER_BOARD_SESSION_*.md` with per-character findings,
   objections (weighted heavy), confirmations, and relationship notes.

## Weight system

| Type | Weight | Meaning |
|---|---|---|
| **OBJECTION** | Near-binding | Character says "I would never" / "this is wrong for me." Author must either fix the passage or provide explicit justification in decisions.log AND the intentional-violation registry. |
| **GAP** | Heavy guideline | Character says "something important is missing from how I'm portrayed here." Strong signal; author should address or explain why not. |
| **CONFIRMATION** | Affirming | Character recognizes themselves. No action needed; recorded for stability tracking. |
| **NOTE** | Advisory | Observation about another character or the world. Informal. |

## Integration with other bodies

- Character OBJECTIONS override red-team and Council recommendations when
  they conflict. You cannot argue a character into betraying themselves.
- Character GAPs feed the editorial board as high-priority items.
- Character CONFIRMATIONs validate attachment-ledger entries.

## World-experience inventory (added 2026-08-25)

In addition to behavioral authenticity, each character describes their
SENSORY experience of the world — what the Archive smells like after ten
years, which sounds they've stopped hearing, where their body hurts, what
the Drift feels like under bare feet vs through boot soles. This inventory
is diffed against the manuscript's actual sensory content: if a character's
lived experience includes details the prose never shows, that's a gap
between the built world and the inhabited world.

Characters are the only reliable witnesses to their own habitation. The
author builds rooms; characters tell you whether anyone actually lives in
them.

## When to convene

After any pass that changes ≥1 scene involving a board member, and before
any content-complete declaration.
