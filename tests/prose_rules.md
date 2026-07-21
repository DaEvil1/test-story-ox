# Tests: Prose Rules Compliance

This test validates adherence to our hard prose principles (see docs/style_guide.md).

## Rules to Check

1. **No explanations of character choices or internal states:**
   - ❌ "Keji felt uncertain about her decision."
   - ✓ Show her hands trembling, her hesitation in action.

2. **Show through action, dialogue, behavior—never through authorial commentary:**
   - ❌ "She was afraid of the Archive's response."
   - ✓ She held her breath. The terrace shuddered.

3. **No direct statements about what characters "have learned":**
   - ❌ "Keji had learned, slowly, that memory is not only a ledger of facts."
   - ❌ "She came to see the Archive's polished surfaces for what they were..."
   - ✓ Show Keji making choices that demonstrate that understanding. Let readers infer the learning.

4. **No laying out arguments or conclusions through narrator voice:**
   - ❌ "She chose a middle path that honored both truth and survival."
   - ✓ Show her writing the amendment, facing Ari, walking away.

5. **Avoid "moral of the story" moments and philosophical summary disguised as description:**
   - ❌ "A city that contained its own contradictions and kept breathing anyway." (authorial philosophy)
   - ❌ "The weight of it was enough." (author telling us what matters)
   - ✓ "The terrace shuddered. Buildings hummed and settled." (what happened)
   - ✓ "The coin in her pocket. She walked back toward the market." (just the moment)

6. **No explicit reflection on what things "mean" or their "significance":**
   - ❌ "The coin remained, waiting for someone to find it and understand what it meant. Or not understand. The weight of it was enough."
   - ✓ "The coin in her pocket. She walked back toward the market."

7. **No "what she carried" or "what was in her heart" explanations:**
   - ❌ "What she carried, in truth, was not a single logic but a memory of Lio's small hand..."
   - ✓ Show her holding Ira's ribbon. Show her gathering Lio's fragments. Let action speak.

8. **No dialogue that explicitly states moral or philosophical principles:**
   - ❌ "Some costs are just paid. They don't need to be explained." (character voicing philosophy rather than showing acceptance through action)
   - ❌ "Memory is more than facts" (characters explaining the theme)
   - ✓ Show characters making choices; let their actions reveal what they believe.

9. **No "without [motivation]" constructions that explain why something was done:**
   - ❌ "She gathered them without comment, without justification." (authorial explanation of her choice)
   - ❌ "She walked without hesitation, without doubt." (author telling us her state)
   - ✓ "She gathered them. She set them in the spine." (just the action)

10. **No poetic/metaphorical statements about significance disguised as description:**
   - ❌ "Just a shape that would hum for anyone listening carefully enough." (explaining the beauty/meaning of the action)
   - ❌ "The city kept working: palimpsest upon palimpsest, tide upon tide." (poetic summary of significance)
   - ✓ "She walked back toward the market." (just what happened)

11. **Trust the reader; they will reach conclusions:**
    - ❌ Multiple paragraphs explaining why Keji chose this path or reflecting on its significance.
    - ✓ Brief scene showing the choice; let readers interpret.

12. **Rare, intentional self-confirmation is permitted when it is the character's own immediate processing:**
    - ❌ "He saw the door open. That meant the world would end." (author narrating a conclusion)
    - ✓ "The door opened. He was alive!" (the character spells out their shock to themselves)
    - Use this sparingly and only when it feels like the character is breathing after a sudden realization.

## Validation

For each chapter:
- Scan for "had learned," "came to see," "came to understand," "realized that," "What she carried" — these are authorial explanation masquerading as narrative.
- Scan for sentences that reflect on meaning or significance (especially at chapter endings).
- Check for philosophical conclusions presented as description.
- Scan for dialogue that states moral/philosophical principles instead of showing belief through action.
- Scan for "without [motivation]" patterns — these are authorial commentary about choice.
- Scan for poetic statements about significance or beauty — if removed, does the story still work? Then they're probably authorial.
- Verify all conflicts are enacted through dialogue/behavior, not introspection.
- Strip out reflection; keep immediate, present-moment action and sensory detail.
- **Special focus:** Look for passages that could be removed without losing the story—those are usually authorial commentary.

## Test Results Against Chapters

### Chapter 1
- ✓ **PASS** — Fixed violation of Rule 10 ("felt like the first small consequence of a persistent question")
- ✓ All other rules met
- Borderline (acceptable): "as if he had once learned to stop his hands" uses "learned" but tied to observed behavior, not thematic learning
- Borderline (acceptable): "like a slow animal deciding whether to bring its cub back" is flowery metaphor but grounded in sensory experience, not authorial philosophy

### Final Chapter
- ✓ **PASS** — Fixed violations of Rules 8, 9, 10
  - Removed Ari's philosophical dialogue; replaced with silent nod
  - Removed "without comment, without justification" 
  - Removed "would hum for anyone listening carefully enough"
  - Removed "palimpsest upon palimpsest, tide upon tide"
- ✓ All other rules met
- All remaining sensory/metaphorical language is tied to Keji's immediate experience, not authorial explanation of meaning


