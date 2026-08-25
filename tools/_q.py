import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
d = Path("src/04-chapters")
for p in sorted(d.glob("*.md")):
    t = p.read_text(encoding="utf-8")
    straight_pairs = t.count('"') // 2
    curly_open, curly_close = t.count("\u201c"), t.count("\u201d")
    print(f"{p.name}: straight_quotes={t.count(chr(34))}  curly_open={curly_open} curly_close={curly_close}")
