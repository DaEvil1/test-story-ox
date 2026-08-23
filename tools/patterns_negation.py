"""Shared negation-contrast detection.

Used by tools/detect_negation_contrast.py (standalone evaluator) and
tools/check_story.py (checker integration, adopted 2026-08-24).

Tiers:
  STRONG — >=2 consecutive negation sentences then an affirmative
           (same subject or explicit contrast marker)
  MEDIUM — single negation + explicit contrast marker in next sentence
  WEAK   — single negation + same-subject affirmative (style fingerprint;
           capped per chapter at 5% of sentences, floor 3)
"""

import re

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

WEAK_RATE = 0.05   # 5% of the chapter's sentences
WEAK_FLOOR = 3


def normalize(t: str) -> str:
    return (t.replace("\u2019", "'").replace("\u2018", "'")
             .replace("\u201c", '"').replace("\u201d", '"'))


def testable(sentence: str) -> str:
    return QUOTES_RE.sub("", normalize(sentence)).strip()


def find(raw: str):
    """Yield dicts: {line, severity, reason, text} for one chapter's text."""
    sents = []
    for m in SENT_RE.finditer(raw):
        s = m.group(0).strip()
        if s:
            sents.append({"raw": s, "test": testable(s), "offset": m.start()})
    sents = [s for s in sents if s["test"]]
    i = 0
    while i < len(sents):
        if NEG_RE.match(sents[i]["test"]):
            j = i
            while j < len(sents) and NEG_RE.match(sents[j]["test"]):
                j += 1
            run = sents[i:j]
            nxt = sents[j] if j < len(sents) else None
            pos_next = bool(nxt and POS_SAME_SUBJECT_RE.match(nxt["test"]))
            marked_next = bool(nxt and CONTRAST_MARKER_RE.search(nxt["test"]))
            severity = reason = None
            if len(run) >= 2 and nxt and (pos_next or marked_next):
                severity, reason = "STRONG", f"{len(run)} negations then affirmative"
            elif len(run) >= 2:
                severity, reason = "MEDIUM", f"{len(run)} negation sentences in a row"
            elif nxt and marked_next:
                severity, reason = "MEDIUM", "negation then contrast-marked sentence"
            elif nxt and pos_next:
                severity, reason = "WEAK", "single negation then same-subject affirmative"
            if severity:
                preview = " ".join(s["raw"] for s in run)[:200]
                tail = f"  >>  {nxt['raw'][:100]}" if nxt and severity in ("STRONG", "WEAK") else ""
                yield {"line": raw.count("\n", 0, run[0]["offset"]) + 1,
                       "severity": severity,
                       "reason": reason,
                       "text": preview + tail}
            i = j
        else:
            i += 1
