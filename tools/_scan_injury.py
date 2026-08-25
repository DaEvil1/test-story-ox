import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
for f in ("src/04-chapters/chapter_10.md", "src/04-chapters/chapter_11.md"):
    t = Path(f).read_text(encoding="utf-8")
    for i, line in enumerate(t.split("\n"), 1):
        if any(w in line.lower() for w in ("bandage", "dull", "finger", "injur", "wrist", "crush")):
            print(f"{f} L{i}: {line.strip()[:120]}")
