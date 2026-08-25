import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
t = Path("C:/Repos/test-story-ox-exp-ch11-ending/src/01-world/canon.md").read_text(encoding="utf-8")
i = t.find("Civic procedure")
print(t[i:i + 340])
