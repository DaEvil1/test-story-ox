import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

d = Path("src/04-chapters")


def normalize(t):
    return (t.replace("\u2019", "'").replace("\u2018", "'")
             .replace("\u201c", '"').replace("\u201d", '"'))


files = sorted(f for f in d.glob("*.md") if f.name.upper() != "README.MD")
texts = {f.name: normalize(f.read_text(encoding="utf-8")) for f in files}
corpus = "\n".join(texts.values())
DIALOGUE_RE = re.compile(r'"[^"]*"')

qt = sum(len(m) for m in DIALOGUE_RE.findall(corpus))
print("analyzer-style corpus:", f"{qt*100//max(len(corpus),1)}%", qt, "/", len(corpus))

qt2 = sum(len(m.group(0)) for name in texts for m in DIALOGUE_RE.finditer(texts[name]))
print("per-chapter sum style:", f"{qt2*100//max(len(corpus),1)}%", qt2)
