import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
d = Path("src/04-chapters")
corpus = "\n".join(p.read_text(encoding="utf-8") for p in sorted(d.glob("*.md")))
words = len(corpus.split())
em_pairs = re.findall(r"\u2014[^\u2014]+\u2014", corpus)
print(f"Em-dash parenthetical pairs: {len(em_pairs)} ({len(em_pairs)*10000//words}/10k)")
not_but = re.findall(r"\bnot\s+\w+[^.\u2014]*\u2014\s*(?:but\s+)?", corpus, re.IGNORECASE)
print(f"'not X — but' constructions: {len(not_but)}")
# negation fragment pairs: "Not X. Y." or "Not X. Not Y."
nf = re.findall(r"(?:^|(?<=[.!?\u201d]))\s*(Not\s+[a-z]+[^.!?\u201d]*)\.(\s*Not\s+[a-z]+[^.!?\u201d]*\.)?", corpus)
print(f"'Not X.' fragments (incl paired): {len(nf)}")
