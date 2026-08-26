import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

# ============ 1. name-backfire: add consequence beat after Oyelaran summons
w1 = Path(".experiments/exp-name-backfire")
p1 = w1 / "src/04-chapters/chapter_11.md"
t1 = p1.read_text(encoding="utf-8")

old1 = '"Ari interceded for you. He will not be here to do it again."'
new1 = ('"Ari interceded for you. He will not be here to do it again."\n\n'
        'She stood to leave, then paused. "One more thing. The name \u2014 '
        'Lio Nash \u2014 has been picked up. Not by us. By someone outside '
        'the hall who recognized it from before the erasure. They\'re asking '
        'questions we don\'t have answers for."')

assert old1 in t1
t1 = t1.replace(old1, new1, 1)
p1.write_text(t1, encoding="utf-8")
print("name-backfire consequence added")
