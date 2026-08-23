#!/usr/bin/env python3
"""Cut-candidate scorer: ranks scenes by how safely they could be cut or
compressed when trimming toward a word target.

Safety-to-cut score (lower = safer to cut) combines:
  +2 per new-information unit (story facts die with the scene)
  +4 if the scene pays a cost
  +2 if value_change != flat
  +1 per attachment beat in the same chapter
  +1 if the scene is marked is_final_choice
Scenes are then shown with their chapter's words-per-info from the staleness
lens, so compression targets surface alongside true cuts.

Usage:
    python tools/cut_candidates.py [--top 12] [--report tests/CUT_CANDIDATES.md]
"""

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = REPO_ROOT / "tests" / "analysis"
CHAPTERS_DIR = REPO_ROOT / "src" / "04-chapters"
DEFAULT_REPORT = REPO_ROOT / "tests" / "CUT_CANDIDATES.md"


def main() -> int:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = ap.parse_args()

    scenes = (yaml.safe_load((ANALYSIS_DIR / "scene_ledger.yaml").read_text(encoding="utf-8")) or {}).get("scenes", [])
    tension = {s.get("id"): s.get("tension", 5)
               for s in (yaml.safe_load((ANALYSIS_DIR / "tension_ledger.yaml").read_text(encoding="utf-8")) or {}).get("scenes", [])}
    attachment = yaml.safe_load((ANALYSIS_DIR / "attachment_ledger.yaml").read_text(encoding="utf-8")) or {}
    beats_per_chapter = {}
    for ch in attachment.get("characters", []):
        for b in ch.get("beats", []):
            c = b.get("chapter")
            beats_per_chapter[c] = beats_per_chapter.get(c, 0) + 1

    chapter_words = {}
    for p in CHAPTERS_DIR.glob("*.md"):
        import re
        m = re.search(r"(\d+)", p.name)
        if m:
            chapter_words[int(m.group(1))] = len(p.read_text(encoding="utf-8").split())

    rows = []
    for s in scenes:
        sid = s.get("id", "?")
        ch = s.get("chapter", 0)
        info = len(s.get("new_info") or [])
        cost = 2 if s.get("cost_paid") not in (None, "none") else 0
        value = 1 if s.get("value_change", "flat") != "flat" else 0
        irr = 1 if s.get("irreversible") else 0
        final = 1 if s.get("is_final_choice") else 0
        beats = beats_per_chapter.get(ch, 0)
        score = info * 2 + cost * 2 + value + irr * 2 + final + min(beats, 3)
        rows.append({
            "id": sid, "chapter": ch, "title": s.get("title", ""),
            "score": score, "info": info, "cost": bool(cost),
            "tension": tension.get(sid), "kind": s.get("kind", "scene"),
            "words": chapter_words.get(ch, 0),
        })

    rows.sort(key=lambda r: r["score"])
    out = [
        "# Cut Candidates (generated)",
        "",
        "<!-- tools/cut_candidates.py — safety-to-cut ranking, lower = safer. -->",
        "",
        "| Scene | Ch | Kind | Safety | NewInfo | Cost | Tension |",
        "|---|---:|---|---:|---:|---|---:|",
    ]
    for r in rows[: args.top]:
        out.append(f"| {r['id']} {r['title']} | {r['chapter']} | {r['kind']} | "
                   f"{r['score']} | {r['info']} | {'yes' if r['cost'] else 'no'} | {r['tension']} |")
    out += ["", "## Compression lens (chapters by words-per-info)", "",
            "| Chapter | Words | Info units | Words/info |", "|---|---:|---:|---:|"]
    info_by_ch = {}
    for s in scenes:
        c = s.get("chapter", 0)
        info_by_ch[c] = info_by_ch.get(c, 0) + len(s.get("new_info") or [])
    stats = sorted((c, chapter_words.get(c, 0), n) for c, n in info_by_ch.items())
    for c, w, n in stats:
        ratio = f"{w // n}" if n else "—"
        out.append(f"| ch{c} | {w} | {n} | {ratio} |")

    args.report.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Cut candidates written to {args.report.relative_to(REPO_ROOT)} "
          f"(top {min(args.top, len(rows))} of {len(rows)} scenes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
