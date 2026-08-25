import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
t = Path("tests/ANALYSIS.md").read_text(encoding="utf-8")
for sec in ("## Atmosphere panel", "## Sentence rhythm", "| the |"):
    i = t.find(sec)
    print(t[i:i + 350])
    print("---")
