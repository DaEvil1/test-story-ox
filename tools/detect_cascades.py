#!/usr/bin/env python3
"""Negation-cascade & fragment-run detector.

Detects two related AI-prose signatures at the paragraph level:

1. NO-CASCADE: 2+ consecutive sentences starting with "No <noun>" within
   one paragraph. Rhythm builds false certainty through repetition.
2. FRAGMENT-RUN: 2+ consecutive verbless fragments (noun phrases with no
   finite verb) used as dramatic beats.

Both are legitimate techniques when rare. The detector reports density so
the author can judge whether the rate serves the prose or the habit owns it.

Usage:
    python tools/detect_cascades.py [--report tests/CASCADE_REPORT.md]
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHAPTERS_DIR = REPO_ROOT / "src" / "04-chapters"

# Sentences that start with "No <word>" (not questions, not dialogue)
NO_CASCADE_RE = re.compile(r"^No\s+[A-Z\u2019']", re.IGNORECASE)

# Very rough verbless test: no common finite-verb markers
VERB_MARKERS = re.compile(
    r"\b(is|are|was|were|had|has|have|did|does|do|will|would|can|could|"
    r"said|asked|felt|came|went|took|gave|made|put|kept|let|turned|"
    r"stood|sat|walked|looked|watched|heard|knew|thought|wanted|needed)\b",
    re.IGNORECASE,
)

SENT_SPLIT = re.compile(r"(?<=[.!?\u201d\u201d])\s+")


def normalize(t: str) -> str:
    return (t.replace("\u2019", "'").replace("\u2018", "'")
             .replace("\u201c", '"').replace("\u201d", '"'))


def is_fragment(sentence: str) -> bool:
    """Very rough: no finite-verb marker = probable fragment."""
    clean = re.sub(r'"[^"]*"', '', sentence)  # remove dialogue
    return not VERB_MARKERS.search(clean)


def main() -> int:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapters-dir", type=Path, default=DEFAULT_CHAPTERS_DIR)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    findings = []
    total_no_starts = 0
    total_fragment_runs = 0

    for p in sorted(args.chapters_dir.glob("*.md")):
        if p.name.upper() == "README.MD":
            continue
        text = normalize(p.read_text(encoding="utf-8"))
        paragraphs = [q.strip() for q in text.split("\n\n") if q.strip()]

        for para_i, para in enumerate(paragraphs):
            # strip dialogue for analysis
            prose = re.sub(r"\u201c[^\u201d]*\u201d", '""', para)
            prose = re.sub(r'"[^"]*"', '""', prose)
            sents = [s.strip() for s in SENT_SPLIT.split(prose) if s.strip()]

            # 1. No-cascade: count consecutive "No X" starts within paragraph
            run_start = None
            for i, s in enumerate(sents):
                if NO_CASCADE_RE.match(s):
                    if run_start is None:
                        run_start = i
                else:
                    if run_start is not None:
                        run_len = i - run_start
                        if run_len >= 2:
                            cascade_sents = sents[run_start:i]
                            findings.append({
                                "file": p.name, "para": para_i + 1,
                                "type": "NO-CASCADE", "len": run_len,
                                "text": " ".join(cascade_sents)[:180],
                                "followed_by": s.strip()[:80] if i < len(sents) else "(end)",
                            })
                            total_no_starts += 1
                    run_start = None
            # trailing run
            if run_start is not None:
                cascade_sents = sents[run_start:]
                if len(cascade_sents) >= 2:
                    findings.append({
                        "file": p.name, "para": para_i + 1,
                        "type": "NO-CASCADE", "len": len(cascade_sents),
                        "text": " ".join(cascade_sents)[:180],
                        "followed_by": "(paragraph end)",
                    })
                    total_no_starts += 1

            # 2. Fragment-runs: 2+ consecutive verbless sentences
            frag_run = []
            for i, s in enumerate(sents):
                if is_fragment(s):
                    frag_run.append((i, s))
                else:
                    if len(frag_run) >= 2:
                        findings.append({
                            "file": p.name, "para": para_i + 1,
                            "type": "FRAGMENT-RUN", "len": len(frag_run),
                            "text": " ".join(s for _, s in frag_run)[:180],
                            "followed_by": "",
                        })
                        total_fragment_runs += 1
                    frag_run = []

    findings.sort(key=lambda f: (f["file"], f["para"]))
    types = {}
    for f in findings:
        types[f["type"]] = types.get(f["type"], 0) + 1
    print("Cascade/fragment findings:")
    for t, n in sorted(types.items()):
        print(f"  {t}: {n}")
    print(f"  Total: {len(findings)}")
    print("-" * 72)
    for f in findings:
        print(f"[{f['type']}] {f['file']} para~{f['para']} ({f['len']} frags)")
        print(f"    {f['text']}")
        print()

    if args.report:
        lines = ["# Cascade Report (generated)", ""]
        for f in findings:
            lines.append(f"- **[{f['type']}]** {f['file']} para~{f['para']}: "
                         f"{f['text']}")
        args.report.write_text("\n".join(lines), encoding="utf-8")
        print(f"Report written to {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
