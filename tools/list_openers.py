import re
from pathlib import Path

d = Path("src/04-chapters")
total = 0
the_count = 0
for p in sorted(d.glob("*.md"), key=lambda x: x.name):
    text = p.read_text(encoding="utf-8")
    body = re.sub(r"^Chapter [^\n]*", "", text, flags=re.IGNORECASE)
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", body.replace("\n", " ")) if s.strip()]
    thes = [s for s in sents if s.startswith("The ")]
    total += len(sents)
    the_count += len(thes)
    print(f"--- {p.name}: {len(thes)}/{len(sents)}")
    for s in thes:
        print("   *", s[:88])
print(f"\nTOTAL: {the_count}/{total} = {the_count*100//max(total,1)}%")
