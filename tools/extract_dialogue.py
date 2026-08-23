#!/usr/bin/env python3
"""Extract all dialogue into a single flow document for voice passes.

Groups quoted speech by chapter, preserving order, with speaker guesses
from attribution windows. Purpose: read every conversation back-to-back
to check voices, escalation, and whether any exchange could be cut.

Usage:
    python tools/extract_dialogue.py [--report tests/DIALOGUE.md]
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHAPTERS_DIR = REPO_ROOT / "src" / "04-chapters"
DEFAULT_REPORT = REPO_ROOT / "tests" / "DIALOGUE.md"

DIALOGUE_RE = re.compile(r"\u201c[^\u201d]*\u201d|\"[^\"]*\"")
ATTRIB_RE = re.compile(
    r"\b(Keji|Ari|Sera|Ira|Lio|he|she|it|the voice|a voice)\s+"
    r"(said|asked|whispered|murmured|added|answered|went on|replied|spoke)\b",
    re.IGNORECASE,
)


def normalize(t: str) -> str:
    return (t.replace("\u2019", "'").replace("\u2018", "'")
             .replace("\u201c", '"').replace("\u201d", '"'))


def main() -> int:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapters-dir", type=Path, default=DEFAULT_CHAPTERS_DIR)
    ap.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = ap.parse_args()

    out = ["# Dialogue Flow (generated)", "",
           "<!-- tools/extract_dialogue.py — read conversations back-to-back. -->",
           ""]
    total = 0
    for p in sorted(args.chapters_dir.glob("*.md")):
        if p.name.upper() == "README.MD":
            continue
        text = normalize(p.read_text(encoding="utf-8"))
        out.append(f"## {p.name.replace('.md', '').replace('_', ' ').title()}")
        out.append("")
        count = 0
        for m in DIALOGUE_RE.finditer(text):
            quote = m.group(0).strip()
            window = text[max(0, m.start() - 90):m.end() + 60]
            am = ATTRIB_RE.search(window)
            who = am.group(1) if am else "?"
            out.append(f"- **{who}:** {quote}")
            count += 1
        total += count
        if count == 0:
            out.append("*(no dialogue)*")
        out.append("")

    out += ["---", f"**Total lines:** {total}", ""]
    args.report.write_text("\n".join(out), encoding="utf-8")
    print(f"Dialogue flow written to {args.report.relative_to(REPO_ROOT)} ({total} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
