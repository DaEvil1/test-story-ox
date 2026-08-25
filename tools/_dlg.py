import re
from pathlib import Path

d = Path("src/04-chapters")
DIALOGUE_RE = re.compile(r'"[^"]*"')
tot_q = tot_len = 0
for p in sorted(d.glob("*.md")):
    t = p.read_text(encoding="utf-8")
    q = sum(len(m) for m in DIALOGUE_RE.findall(t))
    tot_q += q
    tot_len += len(t)
    print(p.name, f"{q*100//max(len(t),1)}%")
print("corpus:", f"{tot_q*100//max(tot_len,1)}%", tot_q, "/", tot_len)
