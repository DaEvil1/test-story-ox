from pathlib import Path

p = Path("src/04-chapters/chapter_05.md")
t = p.read_text(encoding="utf-8")

old_head = """The wall in the Drift was not the same wall that had resisted her. It had become a scrape of raw memory, exposed where the city had not yet covered it. Keji leaned against it and felt the ink pulse under her palm.

Sera watched her. \"What did you bring back?\"

Keji put the recorder on the wall between them. The red light blinked. The first line played in her ears again, precise and thin: AUTHORIZE RESET. PRESERVE NETWORK. REMOVE CHANNEL.

Sera's fingers tapped the console. \"So this is the thing. The door is a brick wall. The Limit is a hand on the wall.\"
"""

new_head = """Down in the Drift, a woman sat against a breathing wall with an echo-bottle open in her cupped hands. Her husband's last hours played raw around her: half sentences, a cough, somebody's radio. She had refused the Curators' offer to clean it. \"The cough is where he still is,\" she said—to no one, to everyone.

Sera brought Keji to her before anything else.

\"This is what keeping looks like,\" Sera said quietly. Then she nodded at the recorder in Keji's hand. \"Now show me what you carried out of there.\"

Keji put the recorder on the wall between them. The red light blinked. The first line played in her ears again, precise and thin: AUTHORIZE RESET. PRESERVE NETWORK. REMOVE CHANNEL.

Sera's fingers tapped the console. \"So this is the thing. The door is a brick wall. The Limit is a hand on the wall.\"
"""
assert old_head in t
t = t.replace(old_head, new_head, 1)

# remove the now-redundant mid-chapter widow paragraph
old_widow = """Down the passage, a woman sat against a breathing wall with an echo-bottle open in her cupped hands. Her husband's last hours played raw in the air around her—half sentences, a cough, somebody's radio. Sera lowered her voice. \"The Curators offered to clean it. Take out the coughing, make him coherent. She refused.\" The woman's thumb moved over the bottle's seam. \"She says the cough is where he still is.\"

"""
assert old_widow in t
t = t.replace(old_widow, "", 1)

p.write_text(t, encoding="utf-8")
print("ch5 merged with variant B")
