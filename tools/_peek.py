import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
t = Path("src/04-chapters/chapter_10.md").read_text(encoding="utf-8")
i = t.find("hid in the walls")
if i != -1:
    print("found at", i)
else:
    print("'hid in the walls' NOT FOUND")
# find ribbon mentions
import re
for m in re.finditer(r"ribbon", t):
    print(f"  ribbon at {m.start()}: {repr(t[m.start()-20:m.start()+60])}")
