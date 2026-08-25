from pathlib import Path
import sys
sys.stdout.reconfigure(encoding="utf-8")

# 1. Progressive physical warning in ch2 (first descent)
p = Path("src/04-chapters/chapter_02.md")
t = p.read_text(encoding="utf-8")
old = "Her fingers brushed the threshold. The walls responded, a low vibration like a held breath."
new = ("Her fingers brushed the threshold. The walls responded\u2014a low vibration "
       "that buzzed in her fingertips and stayed for an hour afterward, a hum "
       "she kept finding under her nails.")
assert old in t
t = t.replace(old, new, 1)
p.write_text(t, encoding="utf-8")

# 2. Sharp sensory contrast in ch1 (editing hall = clean/dry vs market = wet/raw)
p = Path("src/04-chapters/chapter_01.md")
t = p.read_text(encoding="utf-8")
old = "Keji didn't smile. She moved through the Drift without speaking."
new = ("Keji didn't smile. She moved through the Drift without speaking. The air "
       "down here had weight\u2014wet, brackish, alive\u2014and her editing-hall lungs, "
       "used to filtered salt and recycled temperature, took three breaths to adjust.")
assert old in t
t = t.replace(old, new, 1)
p.write_text(t, encoding="utf-8")
print("sensory contrast beats added")
