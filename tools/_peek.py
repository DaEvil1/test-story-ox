import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
t = Path("src/04-chapters/chapter_11.md").read_text(encoding="utf-8")
i = t.find("That is enough")
print(repr(t[max(0, i - 100):i + 140]))
