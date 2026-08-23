#!/usr/bin/env python3
"""Negation-Contrast detector v2 (evaluation mode — not wired into the checker).

Targets the "Not X. Not Y. [But] Z" / "She did not X. She wrote Y." frame:
a negation sentence followed by an affirmative counterpart. Subtler than
the banned "It was not X. It was Y." (FQ-02): subjects vary, contrast is
often implicit, and the pattern survives most phrase-level filters.

Tiers:
  STRONG  — >=2 consecutive negation sentences, then an affirmative sentence
            (same subject, or explicit contrast marker)
  MEDIUM  — single negation sentence + explicit contrast marker in the next
  WEAK    — single negation sentence + same-subject affirmative next
            (highest false-positive risk; human judgment required)

Sentence boundaries are computed on the original text (quotes intact, so
terminal punctuation inside dialogue is preserved); quote interiors are
removed only when testing the sentence against the patterns.

Usage:
    python tools/detect_negation_contrast.py [--report tests/NEGATION_REPORT.md]
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHAPTERS_DIR = REPO_ROOT / "src" / "04-chapters"

SENT_RE = re.compile(r"[^.!?]+[.!?]+[\"'\u201d\u2019)]?")
QUOTES_RE = re.compile(r"\u201c[^\u201d]*\u201d|\"[^\"]*\"")
NEG_RE = re.compile(
    r"^(?:she|he|it|they|keji|ari|sera|ira|lio|the\s+\w+)\s+"
    r"(?:did\s+not|was\s+not|were\s+not|never|would\s+not|could\s+not)\b"
    r"|^not\b",
    re.IGNORECASE,
)
POS_SAME_SUBJECT_RE = re.compile(
    r"^(?:she|he|it|they|keji|ari|sera|ira|lio)\s+[a-z]+", re.IGNORECASE
)
CONTRAST_MARKER_RE = re.compile(
    r"\b(instead|but|rather|anyway|yet|however)\b", re.IGNORECASE
)


def normalize(t: str) -> str:
    return (t.replace("\u2019", "'").replace("\u2018", "'")
             .replace("\u201c", '"').replace("\u201d", '"'))


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def testable(sentence: str) -> str:
    """Quote interiors removed so speech can't trigger or mask the frame."""
    return QUOTES_RE.sub("", normalize(sentence)).strip()


def main() -> int:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapters-dir", type=Path, default=DEFAULT_CHAPTERS_DIR)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    findings = []
    for p in sorted(args.chapters_dir.glob("*.md")):
        raw = normalize(p.read_text(encoding="utf-8"))
        sents = [{"raw": m.group(0).strip(),
                  "test": testable(m.group(0)),
                  "offset": m.start()}
                 for m in SENT_RE.finditer(raw)]
        sents = [s for s in sents if s["test"]]
        i = 0
        while i < len(sents):
            if NEG_RE.match(sents[i]["test"]):
                j = i
                while j < len(sents) and NEG_RE.match(sents[j]["test"]):
                    j += 1
                run = sents[i:j]
                nxt = sents[j] if j < len(sents) else None
                severity, reason = None, ""
                pos_next = bool(nxt and POS_SAME_SUBJECT_RE.match(nxt["test"]))
                marked_next = bool(nxt and CONTRAST_MARKER_RE.search(nxt["test"]))
                if len(run) >= 2 and nxt and (pos_next or marked_next):
                    severity, reason = "STRONG", f"{len(run)} negations then affirmative"
                elif len(run) >= 2:
                    severity, reason = "MEDIUM", f"{len(run)} negation sentences in a row"
                elif nxt and marked_next:
                    severity, reason = "MEDIUM", "negation then contrast-marked sentence"
                elif nxt and pos_next:
                    severity, reason = "WEAK", "single negation then same-subject affirmative"
                if severity:
                    preview = " ".join(s["raw"] for s in run)
                    tail = f"  >>  {nxt['raw']}" if nxt and severity in ("STRONG", "WEAK") else ""
                    findings.append({"file": p.name,
                                     "line": line_of(raw, run[0]["offset"]),
                                     "severity": severity,
                                     "reason": reason,
                                     "text": preview[:200] + tail})
                i = j
            else:
                i += 1

    order = {"STRONG": 0, "MEDIUM": 1, "WEAK": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["file"], f["line"]))
    counts = {t: sum(1 for f in findings if f["severity"] == t) for t in order}
    print(f"Negation-contrast findings: {len(findings)} "
          f"({counts['STRONG']} STRONG, {counts['MEDIUM']} MEDIUM, {counts['WEAK']} WEAK)")
    print("-" * 72)
    for f in findings:
        print(f"[{f['severity']}] {f['file']}:{f['line']}  ({f['reason']})")
        print(f"    {f['text']}")
    if args.report:
        lines = [
            "# Negation-Contrast Report (generated, evaluation mode)",
            "",
            "<!-- tools/detect_negation_contrast.py v2 — not part of the checker yet. -->",
            "",
        ]
        for f in findings:
            lines.append(f"- **[{f['severity']}]** {f['file']}:{f['line']} ({f['reason']})")
            lines.append(f"  - > {f['text']}")
        args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\nReport written to {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
