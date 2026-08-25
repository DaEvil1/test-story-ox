from pathlib import Path

# plantpayoff: wall-game entry
p = Path("tests/analysis/plantpayoff_ledger.yaml")
t = p.read_text(encoding="utf-8")
entry = """
  - id: PP-wall-game
    kind: motif
    plant: "children pressing questions into wall-cracks before the tide (ch1)"
    payoff: "final image - a child presses a new question while Lio's name waits on unscourable stone above (ch11)"
    status: paid
"""
anchor = "# World-Term"
if "PP-wall-game" not in t:
    t = t.rstrip() + "\n" + entry
p.write_text(t, encoding="utf-8")

# questions: RQ9
q = Path("tests/analysis/questions_ledger.yaml")
t = q.read_text(encoding="utf-8")
rq9 = """
  - id: RQ9
    question: What happens when the city reads Lio Nash's name?
    opened: 11
    status: held-deliberate
    reminders: []
    # Opened on the final page; sequel-space gun.
"""
if "RQ9" not in t:
    t = t.replace("thresholds:", rq9 + "\nthresholds:", 1)
q.write_text(t, encoding="utf-8")

# attachment: Sera courage beat
a = Path("tests/analysis/attachment_ledger.yaml")
t = a.read_text(encoding="utf-8")
old = '      - {type: vulnerability, chapter: 10, note: "the grief edit \u2014 six smooth weeks she clawed back from"}'
new = old + '\n      - {type: courage, chapter: 8, note: "walks into the Curators\' hall bare-wristed and logs herself"}'
if "walks into the Curators" not in t:
    assert old in t
    t = t.replace(old, new, 1)
a.write_text(t, encoding="utf-8")
print("ledgers synced")
