import re
from pathlib import Path

d = Path("src/04-chapters")
corpus = "\n".join(p.read_text(encoding="utf-8") for p in sorted(d.glob("*.md")))
words = len(corpus.split())

triads = re.findall(r"\b\w[\w'-]*(?:,\s+[\w'-]+)+,\s+and\s+[\w'-]+", corpus)
weight_shape = re.findall(r"\bthe (?:weight|shape|sound|feel|sense) of\b", corpus)
not_just = re.findall(r"\bnot just\b|\bnot merely\b", corpus, re.IGNORECASE)
participial = re.findall(r"(?:^|\.\s+)([A-Z]\w+ing\b[^,.]{10,})", corpus)
something_in = re.findall(r"\bsomething (?:in|inside|behind)\b", corpus, re.IGNORECASE)

print(f"words: {words}")
print(f"triadic lists: {len(triads)} ({len(triads)*10000//words}/10k)")
for t in triads[:8]:
    print("   ", t[:80])
print(f"'the weight/shape/sound of' frames: {len(weight_shape)}")
print(f"'not just/merely': {len(not_just)}")
print(f"participial openers: {len(participial)}")
for t in participial[:6]:
    print("   ", t[:70])
print(f"'something in/inside/behind': {len(something_in)}")
