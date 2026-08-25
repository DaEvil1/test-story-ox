from pathlib import Path
import sys
sys.stdout.reconfigure(encoding="utf-8")

# 1. ch02-voice: add recorded message in descent
w = Path(".experiments/exp-ch02-voice")
p = w / "src/04-chapters/chapter_02.md"
t = p.read_text(encoding="utf-8")
old = ("Inside was a chamber of recorded sound, not the clean Archive voice she "
       "edited every day, but a tangle of tonalities.")
new = (old + " Somewhere in the walls an old message played on loop\u2014a woman "
       "saying \u201cremember to eat\u201d in a language Keji didn\u2019t recognize, "
       "patient as wallpaper.")
assert old in t
t = t.replace(old, new, 1)
p.write_text(t, encoding="utf-8")
print("ch2 voice added")

# 2. senior-curator: name + one motivation beat in ch11
w2 = Path(".experiments/exp-senior-curator")
p2 = w2 / "src/04-chapters/chapter_11.md"
t2 = p2.read_text(encoding="utf-8")
old2 = '"The council\'s senior curator brought these down herself while you were saving your amendment," he said.'
new2 = ('"Madam Oyelaran brought these down herself while you were saving your '
        'amendment," he said. "She read the plaque order twice\u2014once as policy, '
        'once as a mother, I think. Then she asked for my seals." He looked at the '
        'near-empty box without touching it.')
assert old2 in t2
t2 = t2.replace(old2, new2, 1)

old3 = '"Keep the private ledger well. I am apparently done keeping things."'
new3 = '"Keep the private ledger well. She let me keep that much."'
assert old3 in t2
t2 = t2.replace(old3, new3, 1)
p2.write_text(t2, encoding="utf-8")
print("senior-curator named + motivated")

# 3. tide-gift: the tide brings something unexpected to the quay
w3 = Path(".experiments/exp-tide-gift")
p3 = w3 / "src/04-chapters/chapter_11.md"
t3 = p3.read_text(encoding="utf-8")
old4 = "They watched the water for a while, and the watching was enough."
new4 = ("They watched the water for a while. At some point the tide left something "
        "on the stones between their feet: a child's shoe, salt-stiff, laces still "
        "tied. Neither of them reached for it. After a while the next wave took it back.")
assert old4 in t3
t3 = t3.replace(old4, new4, 1)
p3.write_text(t3, encoding="utf-8")
print("tide-gift added to quay")
