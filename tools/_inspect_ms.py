from pathlib import Path

t = Path("references/_ms_collection.txt").read_text(encoding="utf-8", errors="replace")
print(repr(t[2860:3320].replace("\n", " | ")))
